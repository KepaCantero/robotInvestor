"""Pruebas del panel de la consola con el estado del sistema (V0.64): kill-switch, autonomía, reloj y diario,
y la línea de la última migración. Datos SIMULADOS, sin azar y sin reloj real (las fuentes del reloj se inyectan).

Uso: python3 pruebas/pruebas_consola_sistema.py
"""
import copy
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
import reloj as rl  # noqa: E402
from consola import panel  # noqa: E402
from pruebas_migraciones_t03 import a_010  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo  # noqa: E402
from pruebas_semana import a_010_v045  # noqa: E402

BASE = datetime(2026, 11, 6, 9, 0, 0, tzinfo=timezone.utc).timestamp()
MOTIVO_REARME = "Revisado: alguien cambió la hora de la máquina por error"
DE_HOY = ("integridad", "datos", "presupuesto", "avisos", "decisiones")   # las comprobaciones del panel de siempre


def iso(s):
    return datetime.fromtimestamp(s, timezone.utc).isoformat()


class Fuentes:
    """Reloj de pared y monótono controlables (como el de pruebas_reloj_t03), con el monótono capaz de fallar o de dar NaN."""

    def __init__(self, pared=BASE, mono=1000.0):
        self.p, self.m = pared, mono
        self.falla_mono = False
        self.nan_mono = False

    def pared(self):
        return self.p

    def mono(self):
        if self.falla_mono:
            raise OSError("sin reloj monótono")
        if self.nan_mono:
            return float("nan")
        return self.m

    def pasa(self, s, pared=None):
        self.m += s
        self.p += s if pared is None else pared


def nuevo_reloj(contrastar=True, **kw):
    """Un reloj con fuentes simuladas, ya contrastado con una referencia que coincide con él (salvo contrastar=False)."""
    f = Fuentes()
    r = rl.Reloj(f.pared, f.mono, **kw)
    if contrastar:
        assert r.contrastar(iso(f.p), "REFERENCIA DE PRUEBA")["ok"]
    return f, r


def nuevo_diario(tmp, o=None):
    """Un Diario nuevo sobre una carpeta temporal para el Orquestador dado (o uno limpio)."""
    os.makedirs(tmp, exist_ok=True)   # crear() no hace carpetas (DI-05)
    o = o if o is not None else nuevo()
    r = di.crear(o, os.path.join(tmp, "estado.json"), os.path.join(tmp, "diario"), AHORA)
    assert r["ok"], r
    return r["diario"]


def comp(o, que, ahora=AHORA, **kw):
    """La comprobación `que` del panel (fallo si no está: lo que no aparece no se acepta)."""
    p = panel(o, ahora, **kw)
    c = next((x for x in p["comprobaciones"] if x["que"] == que), None)
    assert c is not None, f"no está la comprobación {que}: {p}"
    return c


def estado_reloj(r):
    """El estado mutable del reloj (sin las fuentes, que no cambian): para ver que `estado()` no lo toca."""
    return copy.deepcopy({k: v for k, v in r.__dict__.items() if k not in ("_pared", "_monotono")})


def main():
    h = Arnes()
    tmp = tempfile.mkdtemp()

    # ------------------------------------------------------------- sin reloj ni diario: el panel de hoy más lo nuevo
    o = nuevo()
    p = panel(o, AHORA)
    h.chk("sin_reloj_ni_diario_el_panel_es_el_de_hoy", [x["que"] for x in p["comprobaciones"]] == list(DE_HOY) + ["kill_switch", "autonomia"]
          and all(x["nivel"] == "VERDE" for x in p["comprobaciones"]) and p["nivel"] == "VERDE", p)
    p2 = panel(o, AHORA, reloj=None, diario=None)
    h.chk("el_panel_es_determinista", p == p2, (p, p2))

    # el panel no cambia nada del Orquestador ni del reloj ni del diario (volcado igual antes y después)
    o = nuevo()
    d = nuevo_diario(os.path.join(tmp, "a"), o)
    f, r = nuevo_reloj()
    antes, antes_r, antes_d = copy.deepcopy(o.__dict__), estado_reloj(r), (d._n, d._roto)
    panel(o, AHORA, reloj=r, diario=d)
    h.chk("el_panel_no_cambia_nada", antes == o.__dict__ and antes_r == estado_reloj(r) and antes_d == (d._n, d._roto))

    # ------------------------------------------------------------- kill-switch (ROJO) y autonomía (ÁMBAR)
    o = nuevo()
    assert o.activar_kill_switch("prueba de kill manual del operador", "OPERADOR", AHORA)["ok"]
    k = comp(o, "kill_switch")
    p = panel(o, AHORA)
    h.chk("kill_activo_es_rojo_con_actor_motivo_e_instante", k["nivel"] == "ROJO" and "OPERADOR" in k["motivo"]
          and "prueba de kill manual del operador" in k["motivo"] and AHORA in k["motivo"], k)
    h.chk("kill_activo_deja_el_panel_entero_rojo", p["nivel"] == "ROJO" and comp(o, "kill_switch")["nivel"] == "ROJO", p)
    h.chk("kill_activo_degrada_y_lo_dice_la_autonomia", comp(o, "autonomia")["nivel"] == "AMBAR"
          and all(c in comp(o, "autonomia")["motivo"] for c in ("TRADING", "TACTICA", "LARGO_PLAZO")), comp(o, "autonomia"))

    o = nuevo(); o.kill = "basura"
    h.chk("kill_ilegible_es_rojo_sin_lanzar", comp(o, "kill_switch")["nivel"] == "ROJO" and "ilegible" in comp(o, "kill_switch")["motivo"])

    o = nuevo()
    o.rearmes.append({"kill": {"motivo": "x", "actor": "ORQUESTADOR", "ahora": AHORA}, "lista": {}, "ahora": AHORA})
    k = comp(o, "kill_switch")
    h.chk("verde_menciona_el_ultimo_rearme", k["nivel"] == "VERDE" and "último rearme" in k["motivo"] and AHORA in k["motivo"], k)

    o = nuevo()
    assert o.degradar("TACTICA", "el intermediario tarda: datos viejos", "G", AHORA)["ok"]
    a = comp(o, "autonomia")
    h.chk("cartera_degradada_es_ambar_y_sale_en_el_motivo", a["nivel"] == "AMBAR" and "TACTICA" in a["motivo"]
          and "el intermediario tarda: datos viejos" in a["motivo"] and f"TACTICA en {o.nivel('TACTICA')}" in a["motivo"], a)
    h.chk("con_una_degradacion_el_panel_deja_de_ser_verde", panel(o, AHORA)["nivel"] == "ROJO"   # el aviso O-19 es de prioridad alta
          and comp(o, "autonomia")["nivel"] == "AMBAR" and comp(o, "kill_switch")["nivel"] == "VERDE")
    assert o.acusar_aviso(o.avisos[-1]["id"], "OPERADOR", AHORA)["ok"]
    h.chk("acusado_el_aviso_la_degradacion_deja_el_panel_en_ambar", panel(o, AHORA)["nivel"] == "AMBAR"
          and comp(o, "autonomia")["nivel"] == "AMBAR" and comp(o, "avisos")["nivel"] == "VERDE")

    o = nuevo()
    o.degradar("TACTICA", "primera", "G", AHORA)
    o.degradar("TRADING", "segunda", "H", AHORA)
    a = comp(o, "autonomia")["motivo"]
    h.chk("dos_degradadas_salen_ordenadas_y_deterministas", a.index("TACTICA") < a.index("TRADING")
          and comp(o, "autonomia")["motivo"] == a, a)

    o = nuevo(); o.degradadas["TRADING"] = "basura"
    h.chk("degradacion_ilegible_no_rompe_el_panel", comp(o, "autonomia")["nivel"] == "AMBAR" and "ilegible" in comp(o, "autonomia")["motivo"])

    # ------------------------------------------------------------- el reloj (solo si se pasa reloj)
    o = nuevo()
    f, r = nuevo_reloj(contrastar=False)
    h.chk("reloj_sin_contrastar_es_ambar", comp(o, "reloj", reloj=r)["nivel"] == "AMBAR"
          and "no se ha contrastado" in comp(o, "reloj", reloj=r)["motivo"])
    antes_r = estado_reloj(r)
    comp(o, "reloj", reloj=r)
    h.chk("el_panel_no_lee_ahora_del_reloj", antes_r == estado_reloj(r) and r.bloqueo is None)   # si lo leyera, avanzaría el reloj

    f, r = nuevo_reloj()
    h.chk("reloj_bien_es_verde", comp(o, "reloj", reloj=r)["nivel"] == "VERDE" and "contrastado" in comp(o, "reloj", reloj=r)["motivo"])
    f.pasa(10, pared=20)   # salto de la pared respecto al monótono: RL-01 al leer
    assert r.ahora()["codigo"] == "RL-01"
    k = comp(o, "reloj", reloj=r)
    h.chk("reloj_bloqueado_RL01_es_rojo_con_codigo_y_motivo", k["nivel"] == "ROJO" and "RL-01" in k["motivo"]
          and comp(o, "reloj", reloj=r)["motivo"] == k["motivo"], k)

    f, r = nuevo_reloj(max_sin_contraste_s=3600)
    h.chk("reloj_bien_tras_contrastar_es_verde", comp(o, "reloj", reloj=r)["nivel"] == "VERDE")
    f.pasa(3601)   # sin leer el reloj: `estado()` ya ve que toca contrastar otra vez
    h.chk("pasado_el_plazo_pide_otro_contraste_es_ambar", comp(o, "reloj", reloj=r)["nivel"] == "AMBAR"
          and "contrástalo" in comp(o, "reloj", reloj=r)["motivo"])
    assert r.contrastar(iso(f.p), "INTERMEDIARIO")["ok"]
    h.chk("contrastado_de_nuevo_es_verde", comp(o, "reloj", reloj=r)["nivel"] == "VERDE")

    f, r = nuevo_reloj()
    assert r.ahora()["ok"]
    f.pasa(10, pared=20)   # salto: el reloj se bloquea (RL-01) y el operador lo rearma tras revisarlo
    assert r.ahora()["codigo"] == "RL-01"
    assert r.rearmar("OPERADOR", MOTIVO_REARME)["ok"]
    h.chk("reloj_rearmado_pide_contraste_es_ambar", comp(o, "reloj", reloj=r)["nivel"] == "AMBAR")

    # `Reloj.estado()`: no cambia el reloj (dos `ahora()` seguidos dan lo mismo con y sin `estado()` en medio)
    f, r = nuevo_reloj()
    a1 = r.ahora()["ahora"]; r.estado(); a2 = r.ahora()["ahora"]
    f2, r2 = nuevo_reloj()
    b1 = r2.ahora()["ahora"]; b2 = r2.ahora()["ahora"]
    h.chk("estado_no_cambia_el_reloj_dos_ahora_iguales", a1 == a2 == b1 == b2, (a1, a2, b1, b2))

    f, r = nuevo_reloj()
    antes_r = estado_reloj(r)
    e = r.estado()
    h.chk("estado_devuelve_la_foto_de_solo_lectura", set(e) == {"bloqueo", "contrastado", "segundos_desde_contraste", "incidentes"}
          and e["bloqueo"] is None and e["contrastado"] is True and e["segundos_desde_contraste"] == 0.0 and e["incidentes"] == 0, e)
    h.chk("estado_no_toca_el_reloj_y_es_determinista", estado_reloj(r) == antes_r and r.estado() == e)
    e["bloqueo"] = {"codigo": "inventado"}
    h.chk("estado_devuelve_una_copia_del_bloqueo", r.bloqueo is None)

    f.pasa(0.001)
    f.falla_mono = True   # el monótono falla: no se puede confirmar el contraste, y el panel no lo pinta verde
    h.chk("estado_con_monotono_roto_no_confirma_el_contraste", (r.estado()["contrastado"], r.estado()["segundos_desde_contraste"]) == (True, None)
          and comp(o, "reloj", reloj=r)["nivel"] == "AMBAR" and "no se puede confirmar" in comp(o, "reloj", reloj=r)["motivo"])
    f.falla_mono = False; f.nan_mono = True
    h.chk("estado_con_monotono_nan_tampoco_confirma", r.estado()["segundos_desde_contraste"] is None
          and comp(o, "reloj", reloj=r)["nivel"] == "AMBAR")

    # ------------------------------------------------------------- el diario (solo si se pasa diario)
    o = nuevo()
    d = nuevo_diario(os.path.join(tmp, "b"), o)
    k = comp(o, "diario", diario=d)
    h.chk("diario_operativo_es_verde", k["nivel"] == "VERDE" and "1 línea(s)" in k["motivo"], k)

    d.cotizaciones["EURUSD"] = {"ultima": 1.0}   # un cambio por fuera del diario: la operación siguiente lo para (DI-06)
    assert d.barrer(AHORA)["codigo"] == "DI-06"
    k = comp(o, "diario", diario=d)
    h.chk("diario_bloqueado_DI06_es_rojo_con_la_marca", k["nivel"] == "ROJO" and "el estado cambió sin pasar por el diario" in k["motivo"], k)
    h.chk("con_el_diario_rojo_el_panel_es_rojo_y_sigue_calculado", panel(o, AHORA, diario=d)["nivel"] == "ROJO"
          and [x["que"] for x in panel(o, AHORA, diario=d)["comprobaciones"]] == list(DE_HOY) + ["kill_switch", "autonomia", "diario"])

    o = nuevo()
    d = nuevo_diario(os.path.join(tmp, "c"), o)
    for _ in range(501):   # 501 operaciones = 1.002 líneas más el PUNTO inicial: el diario real, sin trucos
        assert d.barrer(AHORA)["ok"]
    k = comp(o, "diario", diario=d)
    h.chk("diario_con_muchas_lineas_es_ambar_con_el_umbral_por_defecto", k["nivel"] == "AMBAR" and "1003" in k["motivo"] and "1000" in k["motivo"], k)
    assert d.punto(AHORA)["ok"]
    h.chk("tras_el_punto_el_diario_vuelve_a_verde", comp(o, "diario", diario=d)["nivel"] == "VERDE")

    assert d.barrer(AHORA)["ok"]   # punto deja _n=1; una operación anota OP y RES: _n=3
    h.chk("el_umbral_es_el_parametro_y_el_tope_se_cuenta_igual", comp(o, "diario", diario=d, lineas_diario_ambar=2)["nivel"] == "AMBAR"
          and comp(o, "diario", diario=d, lineas_diario_ambar=3)["nivel"] == "VERDE")   # 3 > 2, pero 3 no es > 3

    class DiarioFalso:
        _roto = None
        _n = True
    h.chk("diario_ilegible_es_rojo", comp(o, "diario", diario="un texto")["nivel"] == "ROJO"
          and comp(o, "diario", diario=12345)["nivel"] == "ROJO"
          and comp(o, "diario", diario=DiarioFalso())["nivel"] == "ROJO"
          and "número de líneas" in comp(o, "diario", diario=DiarioFalso())["motivo"])
    h.chk("umbral_ilegible_es_rojo_sin_lanzar", comp(o, "diario", diario=d, lineas_diario_ambar=None)["nivel"] == "ROJO"
          and comp(o, "diario", diario=d, lineas_diario_ambar="x")["nivel"] == "ROJO")

    # V0.67 (QA de Claude, r01): un NaN, un infinito o un bool como tope daban VERDE (fallaba abierto)
    h.chk("r01_umbral_nan_inf_o_bool_es_rojo", all(comp(o, "diario", diario=d, lineas_diario_ambar=t)["nivel"] == "ROJO"
                                                   for t in (float("nan"), float("inf"), True, False, 0, -1, 2.5)))
    h.chk("r01_umbral_por_defecto_sale_de_parametros", panel.__defaults__[-1] == __import__("parametros").PARAMETROS["n_lineas_diario_ambar"]
          and comp(o, "diario", diario=d)["nivel"] == "VERDE")

    # V0.67 (QA de T-79, H-03): un registro de degradadas que no es un dict no se pinta como «autonomía plena»
    malos = []
    for raro in (None, [], 0, "", set()):
        ox = nuevo(); ox.degradadas = raro
        malos.append(comp(ox, "autonomia")["nivel"])
    h.chk("r02_degradadas_ilegible_es_rojo", malos == ["ROJO"] * 5, malos)
    # V0.67 (QA de T-79, H-04): la foto del reloj no pierde un bloqueo ilegible
    _f4, r4 = nuevo_reloj(); r4.bloqueo = "RL-01 escrito a mano"
    h.chk("r02_estado_del_reloj_conserva_un_bloqueo_ilegible", r4.estado()["bloqueo"] is not None, r4.estado())

    class RelojFalso:
        bloqueo = "x"   # bloqueado con un registro que no es un diccionario
    h.chk("bloqueo_ilegible_del_reloj_es_rojo", comp(o, "reloj", reloj=RelojFalso())["nivel"] == "ROJO"
          and "ilegible" in comp(o, "reloj", reloj=RelojFalso())["motivo"])

    # ------------------------------------------------------------- la última migración
    o = nuevo()
    t = mg.migrar(a_010_v045(a_010(pe.volcar(o, AHORA))), AHORA, "prueba del panel: estado migrado a este código")
    assert t["ok"] and t["migraciones"], t
    om = t["orquestador"]
    m = comp(om, "migracion")
    h.chk("con_una_migracion_hecha_aparece_la_linea_informativa", m["nivel"] == "VERDE" and "migrado a este código" in m["motivo"]
          and AHORA in m["motivo"] and all(i in m["motivo"] for i in t["migraciones"]), m)
    h.chk("sin_migracion_no_hay_linea", all(x["que"] != "migracion" for x in panel(nuevo(), AHORA)["comprobaciones"]))
    o = nuevo(); o.limites["entradas"].append({"tipo": "MIGRACION"})
    m = comp(o, "migracion")
    h.chk("migracion_ilegible_es_rojo", m["nivel"] == "ROJO" and "no la deja leer" in m["motivo"], m)

    # ------------------------------------------------------------- lo imposible no sale disparando
    o = nuevo()
    p = panel(None, AHORA, reloj="x", diario=5)
    h.chk("panel_basura_no_lanza_y_es_rojo", p["nivel"] == "ROJO" and [x["que"] for x in p["comprobaciones"]] == ["panel"], p)
    p = panel(o, "no-es-fecha", reloj="x", diario=5)
    h.chk("ahora_ilegible_es_rojo_como_hoy", p["nivel"] == "ROJO" and len(p["comprobaciones"]) == 1, p)
    p = panel(o, AHORA, reloj="x", diario=5)
    re_ = {x["que"]: x["nivel"] for x in p["comprobaciones"]}
    h.chk("reloj_y_diario_ilegibles_son_rojo_y_no_cuelan", re_.get("reloj") == "ROJO" and re_.get("diario") == "ROJO"
          and p["nivel"] == "ROJO" and len(p["comprobaciones"]) == len(DE_HOY) + 4, p)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CONSOLA SISTEMA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
