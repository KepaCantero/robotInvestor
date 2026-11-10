"""T-84, QA r01 de la V0.63: arranque con el reloj POR DETRÁS del último instante del estado guardado (hueco 2 que señaló GLM en
la entrega de la V0.63).

Monta el lunes de pruebas/pruebas_semana.py (mismos pasos, gemelo en memoria y diario, aquí firmado desde el principio), hace
el punto de control de la noche y vuelve a arrancar con relojes atrasados respecto a `ultimo_ahora` del estado guardado:

  B1  un día detrás, con el intermediario de acuerdo con la máquina: RL-02, reloj bloqueado; contrastar y ahora no dan instante.
  B2  una hora detrás, con el intermediario en hora: RL-02.
  B3  5,5 s detrás (fuera de la tolerancia de desfase de 5 s): RL-02.
  B4  justo 5 s detrás y B5 4 s detrás (dentro): arranca, pero ningún instante es anterior al del estado y se opera sin O-16.
  B6  tras el RL-02, degradar_por_reloj a través del diario: todas las carteras en L1, con el instante del estado (nunca uno
      anterior), anotado en el diario firmado (al reabrir sigue ahí) e integridad limpia.
  B7  el operador rearma el reloj sin corregir la hora (un día detrás): contrastar se bloquea (RL-01) y no da instantes; con 6 s
      detrás, rearmado, el instante que da es el del estado, no uno anterior.
  B8  un arranque que NO llama comprobar_estado (como el que olvidara la integración): ¿qué da el reloj y qué hace el
      Orquestador con ese instante?
  B9  la Maquina de la propia semana arrancada con el reloj detrás: ¿lo cuenta como un fallo de la batería?
  B10 el reloj detrás del instante con que se GUARDÓ el estado (guardado_en del punto de la noche, que la semana toma 2 min
      después de la última operación) pero por delante de su ultimo_ahora; y un punto con ese instante.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.63_revision/r03_reloj_detras_del_estado.py
"""
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

MARCO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
import pruebas_semana as sm  # noqa: E402
import reloj as rl  # noqa: E402

CLAVE = sm.CLAVE
T_VOLCADO = "2026-11-14T00:00:00+00:00"
MOTIVO = "revisado el incidente del reloj en la prueba T-84"


class H:
    def __init__(self):
        self.n, self.fallos, self.hallazgos = 0, 0, []

    def chk(self, nombre, cond, detalle=""):
        self.n += 1
        self.fallos += not cond
        print(("OK   " if cond else "FALLA"), nombre, "" if cond else str(detalle)[:300])
        return bool(cond)

    def hallazgo(self, nombre, cond, detalle=""):
        """Lo que se espera de un reloj que falla cerrado; si no se cumple es un hallazgo del informe, no un fallo de la sonda."""
        self.n += 1
        if not cond:
            self.hallazgos.append(nombre)
        print(("OK   " if cond else "HALLAZGO"), nombre, "" if cond else str(detalle)[:300])


h = H()


def dt(x):
    return datetime.fromisoformat(x)


def reloj_en(segundos):
    f = sm.Fuentes(segundos)
    return f, rl.Reloj(f.pared, f.mono)


def vol(o):
    return pe.volcar(o.orquestador if isinstance(o, di.Diario) else o, T_VOLCADO)


def lunes(tmp):
    """El lunes de la semana, firmado; devuelve las rutas tras el punto de la noche y el gemelo en memoria."""
    re_, rd = os.path.join(tmp, "estado.json"), os.path.join(tmp, "diario")
    g = sm.nuevo(sm.CFG_SEMANA, sellos=(sm.S2,))
    c = di.crear(sm.nuevo(sm.CFG_SEMANA, sellos=(sm.S2,)), re_, rd, sm.DIAS["lunes"], clave=CLAVE)
    assert c["ok"], c
    d = c["diario"]
    bg, bd = sm.broker(), sm.broker()
    m = sm.Maquina(d, [bg, bd], sm.DIAS["lunes"])
    t_prev = m.instante()
    for nombre, paso, delta in sm.pasos_semana():
        if not nombre.startswith("lunes"):
            break
        m.pasar(delta)
        t = m.instante()
        rg, rd_ = paso(g, bg, t, t_prev), paso(d, bd, t, t_prev)
        assert rg == rd_ and sm.ESPERADO[nombre](rg), nombre
        t_prev = t
    m.pasar(120)
    assert d.punto(m.instante())["ok"]
    return (re_, rd), g, bd


def abre(rutas):
    ab = di.abrir(*rutas, clave=CLAVE)
    assert ab["ok"], ab
    return ab["diario"]


def main():
    with tempfile.TemporaryDirectory(prefix="t84-r03-") as tmp:
        rutas, g, broker = lunes(tmp)
        d = abre(rutas)
        u_txt = d.orquestador.ultimo_ahora
        u = dt(u_txt).timestamp()
        print(f"último instante del estado guardado: {u_txt}\n")

        # B1 a B3: detrás más allá de la tolerancia
        for caso, atraso, ref in (("B1 un día detrás, intermediario de acuerdo con la máquina", 86400, "maquina"),
                                  ("B2 una hora detrás, intermediario en hora", 3600, "estado"),
                                  ("B3 5,5 s detrás", 5.5, "maquina")):
            f, r = reloj_en(u - atraso)
            ce = r.comprobar_estado(d)
            ref_iso = sm.iso(f.p if ref == "maquina" else u)
            c = r.contrastar(ref_iso, "INTERMEDIARIO")
            a = r.ahora()
            h.chk(f"{caso}: comprobar_estado da RL-02 y bloquea; contrastar y ahora no dan instante (RL-04)",
                  ce["codigo"] == "RL-02" and r.bloqueo["codigo"] == "RL-02" and c["codigo"] == "RL-04" and c["ahora"] is None
                  and a["codigo"] == "RL-04" and a["ahora"] is None and r.estado()["bloqueo"]["codigo"] == "RL-02", (ce, c, a))

        # B4 y B5: detrás dentro de la tolerancia
        for caso, atraso in (("B4 justo 5 s detrás", 5.0), ("B5 4 s detrás", 4.0)):
            f, r = reloj_en(u - atraso)
            ce = r.comprobar_estado(d)
            c = r.contrastar(sm.iso(f.p), "INTERMEDIARIO")
            f.pasa(1)
            a1 = r.ahora()
            f.pasa(10)
            a2 = r.ahora()
            dados = [x["ahora"] for x in (c, a1, a2)]
            h.chk(f"{caso}: arranca (dentro de la tolerancia), y ningún instante es anterior al del estado: {dados}",
                  ce["ok"] and all(x is not None and dt(x).timestamp() >= u for x in dados) and dados == sorted(dados, key=dt), (ce, dados))
        dd = abre(rutas)
        f, r = reloj_en(u - 4.0)
        r.comprobar_estado(dd)
        t = r.contrastar(sm.iso(f.p), "INTERMEDIARIO")["ahora"]
        x = dd.degradar("TRADING", "prueba T-84: operar con el reloj 4 s detrás del estado", "G", t)
        h.chk("B5 con ese instante se opera a través del diario sin O-16", x["ok"], x)

        # B6: degradación por el reloj tras RL-02, a través del diario firmado
        d = abre(rutas)
        antes = vol(d)
        f, r = reloj_en(u - 86400)
        ce = r.comprobar_estado(d)
        dg = rl.degradar_por_reloj(d, ce)
        fechas = [v.get("ahora") for v in d.orquestador.degradadas.values()]
        d2 = abre(rutas)
        h.chk("B6 tras RL-02, degradar_por_reloj por el diario: las tres carteras en L1, con el instante del estado y nunca uno anterior",
              dg["ok"] and set(dg["carteras"]) == {"TRADING", "TACTICA", "LARGO_PLAZO"} and d.orquestador.ultimo_ahora == u_txt
              and all(d.orquestador.nivel(c) == "L1" for c in rl.CARTERAS) and fechas and all(x == u_txt for x in fechas), (dg, fechas))
        h.chk("B6 la degradación queda en el diario firmado: al reabrir sigue ahí, idéntica, e integridad limpia",
              vol(d2) == vol(d) != antes and d2.orquestador.integridad() == [] and all(d2.orquestador.nivel(c) == "L1" for c in rl.CARTERAS))

        # B7: rearme sin corregir la hora
        d = abre(rutas)
        f, r = reloj_en(u - 86400)
        r.comprobar_estado(d)
        ra = r.rearmar("OPERADOR", MOTIVO)
        c = r.contrastar(sm.iso(f.p), "INTERMEDIARIO")
        h.chk("B7 rearmado sin corregir la hora (un día detrás): contrastar se bloquea (RL-01) y no da instante",
              ra["ok"] and c["codigo"] == "RL-01" and c["ahora"] is None and r.ahora()["ahora"] is None, (ra, c))
        f, r = reloj_en(u - 6.0)
        ce = r.comprobar_estado(d)
        ra = r.rearmar("OPERADOR", MOTIVO)
        c = r.contrastar(sm.iso(f.p), "INTERMEDIARIO")
        h.chk("B7 6 s detrás: RL-02; tras el rearme, el instante que da es el del estado, no uno anterior",
              ce["codigo"] == "RL-02" and ra["ok"] and c["ok"] and dt(c["ahora"]).timestamp() >= u, (ce, c))

        # B8: arranque que no llama comprobar_estado
        d = abre(rutas)
        antes = vol(d)
        f, r = reloj_en(u - 3600)
        c = r.contrastar(sm.iso(f.p), "INTERMEDIARIO")
        a = r.ahora()
        h.hallazgo("B8 sin comprobar_estado, el Reloj no da instantes (exigiría comprobar el estado antes del primero)",
                   c["ahora"] is None and a["ahora"] is None,
                   f"contrastar da {c['ahora']} y ahora da {a['ahora']}, una hora ANTES del último instante del estado ({u_txt})")
        x = d.degradar("TRADING", "prueba T-84: operar con un instante anterior al estado", "G", c["ahora"] or u_txt)
        d3 = abre(rutas)
        h.chk("B8 el Orquestador sí lo rechaza (O-16) sin cambiar nada, y al reabrir el estado es el mismo",
              x["codigo"] == "O-16" and vol(d) == antes and vol(d3) == antes, x)
        g_ej = __import__("ejecucion_g").ejecutar(d, "EXP-0001", broker, c["ahora"] or u_txt)
        h.chk("B8 y G tampoco envía nada con ese instante", not g_ej["ok"] and vol(d) == antes, g_ej)
        ce = r.comprobar_estado(d)
        h.chk("B8 si después se llama comprobar_estado, da RL-02 (tarde: el instante anterior ya se dio)", ce["codigo"] == "RL-02", ce)

        # B10: el reloj detrás del instante de GUARDADO del estado (el del punto de la noche), pero no de su último instante
        d = abre(rutas)
        import json
        guardado = json.loads(open(rutas[0], encoding="utf-8").read())["guardado_en"]
        gs = dt(guardado).timestamp()
        f, r = reloj_en(gs - 60)
        ce = r.comprobar_estado(d)
        c = r.contrastar(sm.iso(f.p), "INTERMEDIARIO")
        h.hallazgo(f"B10 reloj 60 s detrás del guardado_en del estado ({guardado}) y por delante de su ultimo_ahora: no da instantes anteriores al guardado",
                   not c["ok"] or dt(c["ahora"]).timestamp() >= gs,
                   f"comprobar_estado {ce['codigo']}, contrastar da {c['ahora']}: anterior al instante con que se guardó el estado")
        pc = d.punto(c["ahora"]) if c["ok"] else {"ok": False}
        nuevo = json.loads(open(rutas[0], encoding="utf-8").read())["guardado_en"]
        h.hallazgo("B10 punto() no acepta un instante anterior al del punto anterior (ni al último instante del Orquestador)",
                   not pc["ok"], f"punto ok y el estado guardado pasa de guardado_en {guardado} a {nuevo}: retrocede")

        # B9: la Maquina de la semana con el reloj detrás
        d = abre(rutas)
        try:
            sm.Maquina(d, [sm.broker()], sm.iso(u - 3600))
            como = "arranca"
        except AssertionError:
            como = "AssertionError"
        h.chk("B9 la Maquina de la semana no arranca con el reloj detrás del estado (para la batería con un assert)", como == "AssertionError", como)

    print(f"\n{h.n} comprobaciones, {h.fallos} fallos, {len(h.hallazgos)} hallazgo(s): {h.hallazgos}")
    print("RESULTADO r03:", "TODO FALLA CERRADO" if not h.fallos and not h.hallazgos else ("HAY FALLOS" if h.fallos else "FALLA CERRADO (CON HALLAZGOS)"))
    return 0 if not h.fallos else 1


if __name__ == "__main__":
    sys.exit(main())
