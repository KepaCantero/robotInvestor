"""T-84, QA r01 de la V0.63: un SEGUNDO corte en el diario firmado, después de un primer corte y su recuperación (hueco 1 que
señaló GLM en la entrega de la V0.63).

Recorre la semana de pruebas/pruebas_semana.py con sus mismos pasos, gemelos e instantes (el miércoles, su corte a medias en
el diario sin clave; desde el jueves, diario y estado firmados), y en la parte firmada mete cortes:

  C1  jueves_stop: primer corte en el diario firmado (media última línea RES: la OP queda sin resultado) y recuperación.
  C2  jueves_conciliar: SEGUNDO corte, barrido de posiciones: en cada línea del paso, al principio, un byte dentro, a la
      mitad, justo antes del salto y justo después. Cada posición, en una copia de los ficheros. Se exige que abrir funcione,
      que el estado sea el de cargar el estado guardado y aplicar las k operaciones cuya línea OP quedó entera (réplica
      independiente, sin usar abrir), que el diario reescrito tenga k OP, cada una con su RES, y ninguna repetida, y que
      reabrir otra vez dé lo mismo, byte a byte (idempotente). Si quedan todas las OP, el estado es el del gemelo en memoria.
  C3  jueves_conciliar, en copias: diarios firmados alterados tras los dos cortes (un byte de una línea del medio, una línea
      completa falsificada sin la clave, con salto final o sin él, o firmada con otra clave). Ninguno se acepta.
  C4  jueves_degradar: corte a medias y, al recuperarlo, otro corte DENTRO de la reescritura del diario (el fichero temporal
      queda escrito y no llega a sustituir al bueno). Se vuelve a abrir.
  C5  jueves_restablecer: corte a medias y, al recuperarlo, otro corte a mitad de escribir el RES que abrir completa.
  C6  noche del jueves, en copias: corte dentro del punto de control firmado (tras anotar el PUNTO y antes de guardar el
      estado; tras guardar el estado y antes de reducir el diario; con media línea PUNTO escrita).
  C7  viernes_kill: dos recuperaciones seguidas del mismo corte dan el mismo estado y el mismo fichero; después, otro primer
      corte vivo (C1) y, en viernes_rearmar (acusar avisos, conciliar y rearmar: varias operaciones), el barrido C2 y los
      diarios alterados C3.
Después, la semana sigue hasta el final con los mismos controles finales que pruebas_semana.py: si algo se perdió o se
duplicó, los gemelos se separan.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.63_revision/r02_segundo_corte_firmado.py
"""
import glob
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

MARCO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
import pruebas_semana as sm  # noqa: E402

CLAVE = sm.CLAVE
OTRA = bytes(range(100, 148))
T_VOLCADO = "2026-11-14T00:00:00+00:00"


class Corte(BaseException):
    """Un corte de luz: no lo recoge ningún except Exception del código."""


class H:
    def __init__(self):
        self.n, self.fallos = 0, 0

    def chk(self, nombre, cond, detalle=""):
        self.n += 1
        if not cond:
            self.fallos += 1
        print(("OK   " if cond else "FALLA"), nombre, "" if cond else str(detalle)[:300])
        return bool(cond)


h = H()


def vol(o):
    return pe.volcar(o.orquestador if isinstance(o, di.Diario) else o, T_VOLCADO)


def lineas_de(texto_bytes):
    """[(inicio, fin_sin_salto, dict o None)] de las líneas completas (con salto) del diario."""
    out, i = [], 0
    while True:
        j = texto_bytes.find(b"\n", i)
        if j < 0:
            break
        try:
            e = json.loads(texto_bytes[i:j])
        except ValueError:
            e = None
        out.append((i, j, e))
        i = j + 1
    return out


def copia_ficheros(rutas, carpeta, diario_bytes=None):
    os.makedirs(carpeta)
    re2, rd2 = os.path.join(carpeta, "estado.json"), os.path.join(carpeta, "diario")
    shutil.copy2(rutas[0], re2)
    if diario_bytes is None:
        shutil.copy2(rutas[1], rd2)
    else:
        with open(rd2, "wb") as f:
            f.write(diario_bytes)
    return re2, rd2


def replica(ruta_estado, ops, k):
    """Réplica independiente de lo que abrir debe dar: el estado guardado más las k primeras OP, aplicadas a mano."""
    c = pe.cargar_de(ruta_estado, CLAVE)
    assert c["ok"], c
    o = c["orquestador"]
    for e in ops[:k]:
        getattr(o, e["metodo"])(*e["args"], **e["kwargs"])
    return o


def ops_enteras(prefijo):
    """Las OP cuya línea quedó entera (con o sin su salto final) en un prefijo del diario."""
    res = []
    for x in prefijo.split(b"\n"):
        try:
            e = json.loads(x)
        except ValueError:
            continue
        if isinstance(e, dict) and e.get("tipo") == "OP" and di._h({k: v for k, v in e.items() if k not in ("hash", "firma")}) == e["hash"]:
            res.append(e)
    return res


def forma_tras_abrir(ruta_diario, k):
    """El diario reescrito: un PUNTO y k pares OP-RES, sin OP repetidas, cada RES de su OP."""
    ls, cortada, _, err = di._leer(ruta_diario, CLAVE)
    if err or cortada:
        return False, ("leer", err, cortada)
    resto = [e for e in ls if e["tipo"] != "PUNTO"]
    ops = [e for e in resto if e["tipo"] == "OP"]
    pares = all(resto[i]["tipo"] == "OP" and resto[i + 1]["tipo"] == "RES" and resto[i + 1]["op"] == resto[i]["n"]
                for i in range(0, len(resto) - 1, 2)) and len(resto) % 2 == 0
    sin_rep = len({e["hash"] for e in ops}) == len(ops) and len({json.dumps([e["metodo"], e["args"], e["kwargs"]]) for e in ops}) == len(ops)
    return (len(ops) == k and pares and sin_rep), {"ops": len(ops), "k": k, "pares": pares, "sin_rep": sin_rep}


def media_ultima(ruta_diario):
    """Deja la última línea (un RES) a medias: la OP anterior queda sin resultado."""
    b = open(ruta_diario, "rb").read()
    ls = lineas_de(b)
    ini, fin, e = ls[-1]
    assert e["tipo"] == "RES", e
    with open(ruta_diario, "wb") as f:
        f.write(b[:ini + (fin - ini) // 2])


# ------------------------------------------------------------------------------------------------ los cortes
def c1_primer_corte(ctx, nombre):
    media_ultima(ctx["rutas"][1])
    ab = di.abrir(*ctx["rutas"], clave=CLAVE)
    h.chk(f"C1 {nombre}: primer corte en el diario firmado (RES a medias): abrir lo recupera y lo dice",
          ab["ok"] and ab["linea_incompleta"] and ab["aplicadas"] >= 1, (ab["codigo"], ab["motivo"]))
    return ab


def c2_barrido(ctx, nombre, ini_paso, tmp):
    b = open(ctx["rutas"][1], "rb").read()
    ls = [x for x in lineas_de(b) if x[0] >= ini_paso]
    todas = ops_enteras(b)
    previas = len(ops_enteras(b[:ini_paso]))
    posiciones = set()
    for ini, fin, _ in ls:
        posiciones |= {ini, ini + 1, (ini + fin) // 2, fin, fin + 1}
    posiciones = sorted(p for p in posiciones if ini_paso <= p <= len(b))
    malos, n_ok, ref_g = [], 0, vol(ctx["g"])
    for i, p in enumerate(posiciones):
        re2, rd2 = copia_ficheros(ctx["rutas"], os.path.join(tmp, f"c2_{nombre}_{i}"), b[:p])
        k = len(ops_enteras(b[:p]))
        ab = di.abrir(re2, rd2, clave=CLAVE)
        if not ab["ok"]:
            malos.append((p, "abrir", ab["codigo"], ab["motivo"]))
            continue
        esperado = vol(replica(re2, todas, k))
        forma, det = forma_tras_abrir(rd2, k)
        bytes1 = open(rd2, "rb").read()
        ab2 = di.abrir(re2, rd2, clave=CLAVE)
        idem = ab2["ok"] and vol(ab2["diario"]) == vol(ab["diario"]) and open(rd2, "rb").read() == bytes1
        todo = k == len(todas)
        if vol(ab["diario"]) != esperado or not forma or not idem or (todo and vol(ab["diario"]) != ref_g) or k < previas:
            malos.append((p, k, vol(ab["diario"]) == esperado, det, idem, todo))
        else:
            n_ok += 1
    h.chk(f"C2 {nombre}: segundo corte en el diario firmado, {len(posiciones)} posiciones dentro de las {len(ls)} líneas del paso: "
          "abrir recupera, sin perder lo ya anotado ni repetir nada, e idempotente", not malos and n_ok == len(posiciones), malos[:3])
    return b


def c3_alterados(ctx, b, tmp, nombre):
    ls = lineas_de(b)
    casos = {}
    # 1) un byte de una RES del medio
    ini, fin, e = next(x for x in ls[1:-2] if x[2]["tipo"] == "RES")
    linea = b[ini:fin].decode()
    pos = linea.index('"resultado":"') + len('"resultado":"')
    nuevo = linea[:pos] + ("0" if linea[pos] != "0" else "1") + linea[pos + 1:]
    casos["un byte de una RES del medio"] = b[:ini] + nuevo.encode() + b[fin:]
    # 2) una línea OP completa falsificada sin la clave (hash bueno, firma inventada), con salto final
    ult = ls[-1][2]
    falsa = {"n": ult["n"] + 1, "tipo": "OP", "metodo": "activar_kill_switch", "args": ["falsificada", "OPERADOR", "2026-11-12T12:00:00+00:00"],
             "kwargs": {}, "prev": ult["hash"]}
    falsa["hash"] = di._h(falsa)
    falsa["firma"] = "0" * 64
    linea_falsa = json.dumps(falsa, ensure_ascii=True, separators=(",", ":")).encode()
    casos["OP falsificada completa, con salto"] = b + linea_falsa + b"\n"
    # 3) la misma firmada con OTRA clave
    falsa2 = {k: v for k, v in falsa.items() if k != "firma"}
    falsa2["firma"] = pe.firmar(OTRA, "robot-investor/diario/" + falsa2["hash"])
    casos["OP firmada con otra clave, con salto"] = b + json.dumps(falsa2, ensure_ascii=True, separators=(",", ":")).encode() + b"\n"
    # 4) una OP del medio sustituida por otra con su hash rehecho (sin clave no se puede refirmar)
    ini4, fin4, e4 = next(x for x in ls[1:] if x[2]["tipo"] == "OP")
    e4 = dict(e4)
    e4["args"] = list(e4["args"])
    e4["metodo"] = "degradar" if e4["metodo"] != "degradar" else "activar_kill_switch"   # otro método que el que había
    e4["hash"] = di._h({k: v for k, v in e4.items() if k not in ("hash", "firma")})
    casos["OP del medio cambiada con su hash rehecho"] = b[:ini4] + json.dumps(e4, ensure_ascii=True, separators=(",", ":")).encode() + b[fin4:]
    for i, (que, datos) in enumerate(casos.items()):
        assert datos != b, que   # cada caso cambia de verdad el diario
        re2, rd2 = copia_ficheros(ctx["rutas"], os.path.join(tmp, f"c3_{nombre}_{i}"), datos)
        ab = di.abrir(re2, rd2, clave=CLAVE)
        h.chk(f"C3 {nombre}: diario firmado alterado tras los dos cortes ({que}): no se acepta (DI-02) y no toca el fichero",
              not ab["ok"] and ab["codigo"] == "DI-02" and open(rd2, "rb").read() == datos, (ab["codigo"], ab["motivo"]))
    # 5) la OP falsificada SIN salto final: parece un corte; se descarta sin aplicarla
    re2, rd2 = copia_ficheros(ctx["rutas"], os.path.join(tmp, f"c3_{nombre}_sin_salto"), b + linea_falsa)
    ab = di.abrir(re2, rd2, clave=CLAVE)
    h.chk(f"C3 {nombre}: OP falsificada sin salto final: se toma por un corte, se descarta y NO se aplica (sin kill falso, estado del gemelo)",
          ab["ok"] and ab["linea_incompleta"] and ab["diario"].orquestador.kill is None and vol(ab["diario"]) == vol(ctx["g"])
          and b"falsificada" not in open(rd2, "rb").read(), (ab["codigo"], ab.get("linea_incompleta")))
    # 6) límite conocido (T-03, Fase 3: falta el ancla monótona): quitar limpiamente el último par OP-RES no se nota
    ini6 = ls[-2][0]
    re2, rd2 = copia_ficheros(ctx["rutas"], os.path.join(tmp, f"c3_{nombre}_recorte"), b[:ini6])
    ab = di.abrir(re2, rd2, clave=CLAVE)
    conocido = ab["ok"] and not ab["linea_incompleta"] and vol(ab["diario"]) != vol(ctx["g"])
    print(("INFO " if conocido else "CAMBIO"), f"C3 {nombre}: límite conocido de T-03 (ancla monótona, Fase 3): un recorte limpio del último par OP-RES "
          f"{'se acepta sin aviso y la operación se pierde' if conocido else 'ya NO se acepta: revisar la deuda de T-03'}")


def c4_corte_en_la_reescritura(ctx, nombre):
    media_ultima(ctx["rutas"][1])
    original = di._escribir_atomico

    def cortado(ruta, texto):   # escribe el temporal y se corta antes del os.replace
        carpeta = os.path.dirname(os.path.abspath(ruta))
        fd, tmp = tempfile.mkstemp(prefix=".diario-", suffix=".tmp", dir=carpeta)
        with os.fdopen(fd, "w", encoding="ascii") as f:
            f.write(texto)
        raise Corte()
    di._escribir_atomico = cortado
    try:
        di.abrir(*ctx["rutas"], clave=CLAVE)
        cortada = False
    except Corte:
        cortada = True
    finally:
        di._escribir_atomico = original
    h.chk(f"C4 {nombre}: el corte llega dentro de la reescritura que limpia la línea cortada", cortada)
    ab = di.abrir(*ctx["rutas"], clave=CLAVE)
    h.chk(f"C4 {nombre}: al volver a abrir se recupera, con la operación aplicada una sola vez (estado del gemelo)",
          ab["ok"] and vol(ab["diario"]) == vol(ctx["g"]), (ab["codigo"], ab["motivo"]))
    restos = glob.glob(os.path.join(os.path.dirname(ctx["rutas"][1]), ".diario-*.tmp"))
    ctx["restos_tmp"] = restos
    return ab


def c5_corte_en_el_res_de_abrir(ctx, nombre):
    media_ultima(ctx["rutas"][1])
    original = di.Diario._anotar

    def a_medias(self, entrada):
        e = di._linea({"n": self._n + 1, **entrada}, self._ultimo, self._clave)
        texto = json.dumps(e, ensure_ascii=True, separators=(",", ":")) + "\n"
        with open(self._ruta_diario, "a", encoding="ascii") as f:
            f.write(texto[: len(texto) // 2])
        raise Corte()
    di.Diario._anotar = a_medias
    try:
        di.abrir(*ctx["rutas"], clave=CLAVE)
        cortada = False
    except Corte:
        cortada = True
    finally:
        di.Diario._anotar = original
    h.chk(f"C5 {nombre}: el corte llega a mitad del RES que abrir completa al recuperar", cortada)
    ab = di.abrir(*ctx["rutas"], clave=CLAVE)
    h.chk(f"C5 {nombre}: al volver a abrir se recupera otra vez, sin repetir la operación (estado del gemelo)",
          ab["ok"] and ab["linea_incompleta"] and vol(ab["diario"]) == vol(ctx["g"]), (ab["codigo"], ab["motivo"]))
    return ab


def c6_corte_en_el_punto(ctx, inst, tmp):
    ref = vol(ctx["g"])
    for i, (que, llamada) in enumerate((("tras anotar el PUNTO, antes de guardar el estado", 1),
                                        ("tras guardar el estado, antes de reducir el diario", 2),
                                        ("con media línea PUNTO escrita", 0))):
        re2, rd2 = copia_ficheros(ctx["rutas"], os.path.join(tmp, f"c6_{i}"))
        ab = di.abrir(re2, rd2, clave=CLAVE)
        assert ab["ok"], ab
        dd = ab["diario"]
        orig_e, orig_a, cuenta = di._escribir_atomico, di.Diario._anotar, [0]

        def e_cortado(ruta, texto):
            cuenta[0] += 1
            if cuenta[0] == llamada:
                raise Corte()
            return orig_e(ruta, texto)

        def a_cortado(self, entrada):
            if entrada.get("tipo") == "PUNTO":
                e = di._linea({"n": self._n + 1, **entrada}, self._ultimo, self._clave)
                t = json.dumps(e, ensure_ascii=True, separators=(",", ":")) + "\n"
                with open(self._ruta_diario, "a", encoding="ascii") as f:
                    f.write(t[: len(t) // 2])
                raise Corte()
            return orig_a(self, entrada)
        if llamada:
            di._escribir_atomico = e_cortado
        else:
            di.Diario._anotar = a_cortado
        try:
            dd.punto(inst)
            cortada = False
        except Corte:
            cortada = True
        finally:
            di._escribir_atomico, di.Diario._anotar = orig_e, orig_a
        ab2 = di.abrir(re2, rd2, clave=CLAVE)
        ok = cortada and ab2["ok"] and vol(ab2["diario"]) == ref
        if ok:   # y el punto se puede rehacer y reabrir
            pc = ab2["diario"].punto(inst)
            ab3 = di.abrir(re2, rd2, clave=CLAVE)
            ok = pc["ok"] and ab3["ok"] and vol(ab3["diario"]) == ref and len(di._leer(rd2, CLAVE)[0]) == 1
        h.chk(f"C6 noche del jueves, corte dentro del punto firmado ({que}): se recupera el estado del gemelo y el punto se rehace", ok,
              (cortada, ab2["codigo"], ab2["motivo"]))


def c7_dos_recuperaciones(ctx, nombre, tmp):
    b = open(ctx["rutas"][1], "rb").read()
    ini, fin, _ = lineas_de(b)[-1]
    re2, rd2 = copia_ficheros(ctx["rutas"], os.path.join(tmp, "c7"), b[:ini + (fin - ini) // 2])
    a1 = di.abrir(re2, rd2, clave=CLAVE)
    b1 = open(rd2, "rb").read()
    a2 = di.abrir(re2, rd2, clave=CLAVE)
    h.chk(f"C7 {nombre}: dos recuperaciones seguidas del mismo corte dan el mismo estado (el del gemelo) y el mismo fichero",
          a1["ok"] and a2["ok"] and vol(a1["diario"]) == vol(a2["diario"]) == vol(ctx["g"]) and open(rd2, "rb").read() == b1
          and a2["aplicadas"] == a1["aplicadas"] and not a2["linea_incompleta"], (a1["codigo"], a2["codigo"]))


# ------------------------------------------------------------------------------------------------ la semana
def main():
    with tempfile.TemporaryDirectory(prefix="t84-r02-") as tmp:
        re_, rd = os.path.join(tmp, "estado.json"), os.path.join(tmp, "diario")
        g = sm.nuevo(sm.CFG_SEMANA, sellos=(sm.S2,))
        c = di.crear(sm.nuevo(sm.CFG_SEMANA, sellos=(sm.S2,)), re_, rd, sm.DIAS["lunes"])
        assert c["ok"], c
        d = c["diario"]
        bg, bd = sm.broker(), sm.broker()
        m = sm.Maquina(d, [bg, bd], sm.DIAS["lunes"])
        ctx = {"g": g, "rutas": (re_, rd), "clave": None}
        dia_actual = "lunes"
        t_prev = m.instante()
        completa = True
        for nombre, paso, delta in sm.pasos_semana():
            dia = nombre.split("_")[0]
            if dia != dia_actual:
                m.pasar(120)
                inst = m.instante()
                if dia_actual == "jueves":
                    c6_corte_en_el_punto(ctx, inst, tmp)
                pc = d.punto(inst)
                assert pc["ok"], pc
                m.para()
                if dia == "jueves":
                    ab = di.abrir(*ctx["rutas"])
                    assert ab["ok"], ab
                    re2, rd2 = os.path.join(tmp, "estado_firmado.json"), os.path.join(tmp, "diario_firmado")
                    cf = di.crear(ab["diario"].orquestador, re2, rd2, sm.DIAS["jueves"], clave=CLAVE)
                    assert cf["ok"], cf
                    ctx["rutas"], ctx["clave"] = (re2, rd2), CLAVE
                ab = di.abrir(*ctx["rutas"], clave=ctx["clave"])
                assert ab["ok"], ab
                d = ab["diario"]
                m = sm.Maquina(d, [bg, bd], sm.DIAS[dia])
                dia_actual = dia
                t_prev = m.instante()
            m.pasar(delta)
            t = m.instante()
            ini_paso = os.path.getsize(ctx["rutas"][1])
            rg = paso(g, bg, t, t_prev)
            rd_ = paso(d, bd, t, t_prev)
            if not (rg == rd_ and sm.ESPERADO[nombre](rg)):
                h.chk(f"{nombre}: mismo resultado y el esperado", False, (rg, rd_))
                completa = False
                break
            if nombre == "miercoles_libre":
                sm.cortar(ctx["rutas"][1])   # el corte de la propia semana, en el diario sin clave
            ab = None
            if nombre == "jueves_stop":
                ab = c1_primer_corte(ctx, nombre)
            elif nombre == "jueves_conciliar":
                b = c2_barrido(ctx, nombre, ini_paso, tmp)
                c3_alterados(ctx, b, tmp, nombre)
                media_ultima(ctx["rutas"][1])   # y el segundo corte de verdad, en el diario vivo
                ab = di.abrir(*ctx["rutas"], clave=CLAVE)
                h.chk(f"C2 {nombre}: segundo corte en el diario vivo y recuperación", ab["ok"] and ab["linea_incompleta"], (ab["codigo"], ab["motivo"]))
            elif nombre == "jueves_degradar":
                ab = c4_corte_en_la_reescritura(ctx, nombre)
            elif nombre == "jueves_restablecer":
                ab = c5_corte_en_el_res_de_abrir(ctx, nombre)
            elif nombre == "viernes_kill":
                c7_dos_recuperaciones(ctx, nombre, tmp)
                ab = c1_primer_corte(ctx, nombre)   # otro primer corte, vivo, en el diario firmado del viernes
            elif nombre == "viernes_rearmar":   # paso de varias operaciones: el barrido del segundo corte, línea a línea
                b = c2_barrido(ctx, nombre, ini_paso, tmp)
                c3_alterados(ctx, b, tmp, nombre)
            if ab is None:
                ab = di.abrir(*ctx["rutas"], clave=ctx["clave"])
            if not ab["ok"]:
                h.chk(f"{nombre}: el diario se reabre", False, (ab["codigo"], ab["motivo"]))
                completa = False
                break
            d = ab["diario"]
            if vol(d) != vol(g):
                h.chk(f"{nombre}: tras reiniciar, el estado es el del gemelo", False)
                completa = False
                break
            t_prev = t
        h.chk("la semana entera llega al final con los cortes, y en cada paso el estado del diario es el del gemelo", completa)
        if completa:
            m.pasar(120)
            o = d.orquestador
            h.chk("final: posiciones como en pruebas_semana (la primera por el stop, la de TRADING por el operador)",
                  o.posiciones["POS-EXP-0001"]["estado"] == "CERRADA" and o.posiciones["POS-EXP-0003"]["estado"] == "CERRADA"
                  and len(o.posiciones["POS-EXP-0001"]["reducciones"]) == 1)
            h.chk("final: un kill-switch y un rearme, una degradación restablecida: nada duplicado",
                  o.kill is None and len(o.rearmes) == 1 and o.nivel("TACTICA") == "L1")
            pc = d.punto(m.instante())
            ab = di.abrir(*ctx["rutas"], clave=CLAVE)
            h.chk("final: punto de control, el diario firmado se reabre, idéntico al gemelo e íntegro",
                  pc["ok"] and ab["ok"] and vol(ab["diario"]) == vol(g) and ab["diario"].orquestador.integridad() == [])
        restos = ctx.get("restos_tmp", [])
        print(f"\nnota: tras el corte C4 quedan {len(restos)} fichero(s) temporal(es) .diario-*.tmp en la carpeta del diario (nadie los limpia)")
    print(f"\n{h.n} comprobaciones, {h.fallos} fallos")
    print("RESULTADO r02:", "TODO FALLA CERRADO" if h.fallos == 0 else "HAY FALLOS")
    return 0 if h.fallos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
