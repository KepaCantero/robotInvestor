"""QA r01 de T-176 (revisor independiente): ataques a PB-36 y PB-33.

Uso (desde la raíz del repo, con el venv):  python .docs/tickets/T-176/revisores/r01_ataques.py
Cada ataque imprime OK / HALLAZGO. No toca nada fuera de un directorio temporal."""
import sys
import tempfile
import threading
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(RAIZ / "bloque_a/11_Ejecutor"), str(RAIZ / "bloque_a/11_Ejecutor/tests")]

import pandas as pd  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.evaluador import Evaluador  # noqa: E402
from conftest import config_pruebas, nuevo_bloque  # noqa: E402
from test_t176_pb36_pb33 import _historia_umbral_e  # noqa: E402

RES = []


def informe(nombre, ok, detalle=""):
    RES.append((nombre, ok))
    print(f"{'OK      ' if ok else 'HALLAZGO'} · {nombre}{' · ' + detalle if detalle else ''}")


def evaluador(tmp, fecha="2026-04-06", **extra):
    a = Almacen(Path(tmp))
    a.reloj.fijar(fecha)
    return Evaluador(a, None, None, config_pruebas(**extra), None)


def prg(a, i, e, y, fr="2026-03-02"):
    pid = f"PRG-2026-{i:04d}"
    a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": "RV", "horizonte": "H3", "prob_interna": 0.65,
                               "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "sentido": "POSITIVO",
                               "fecha_emision": "2026-01-02", "estado": "ABIERTO", "fecha_resolucion": fr,
                               "puntuaciones_opcion": {"E": e}})
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": y, "valor_observado": 0.0, "comprobacion_fuga": "SUPERADA",
                                              "fecha_resuelto": fr}})


# 1. Youden a mano. E = 50,55,60,65,70 (×6 = 30 PRG), aciertos en 55, 65, 70.
#    pos = 18, neg = 12. J(t) = TPR − FPR con E ≥ t:
#    t=50: 1 − 1 = 0 · t=55: 1 − 6/12 = 0,5 · t=60: 12/18 − 6/12 = 0,1667 · t=65: 12/18 − 0 = 0,6667 · t=70: 6/18 − 0 = 0,333
#    → óptimo 65, J = 2/3.
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d, "2026-06-05")
    i = 0
    for _ in range(6):
        for ee, y in ((50, 0), (55, 1), (60, 0), (65, 1), (70, 1)):
            i += 1
            prg(e.almacen, i, ee, y)
    ev = e.evidencia_umbral_e("2026-06-05")
    informe("Youden a mano (óptimo 65, J 2/3)", ev["objetivo"] == 65.0 and abs(ev["indice_youden"] - 2 / 3) < 1e-12, str(ev.get("objetivo")))
    # NaN, inf, bool, None en E y en el resultado: no entran
    for k, (ee, y) in enumerate(((float("nan"), 1), (float("inf"), 0), (True, 1), (None, 0), (62, None), (62, 2), (62, True))):
        prg(e.almacen, 100 + k, ee, y)
    ev2 = e.evidencia_umbral_e("2026-06-05")
    informe("Youden ignora E/resultado no válidos (True cuenta como 1: n=31; con E=62 acierto el óptimo pasa a 62)", ev2["n"] == 31 and ev2["objetivo"] == 62.0, f"n={ev2['n']}")

# 2. proponer_ajuste: tipos inesperados y componentes
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d)
    errores = []
    for args in (("P-09", "E", True), ("P-09", "E", float("inf")), ("P-09", "E", None), ("P-09", "E", "50"),
                 ("P-09", None, 50), ("P-09", "Z", 50), ("P-30", None, 1)):
        try:
            e.proponer_ajuste(args[0], args[1], args[2], {}, "2026-04-06")
            errores.append(args)
        except (ValueError, KeyError, TypeError):
            pass
    informe("proponer_ajuste falla cerrado con tipos inesperados", not errores, str(errores))
    informe("ninguna vía escribe F10", not e.almacen.leer("F10"))

# 3. P-11 por proponer_ajuste: tiene banda en el Anexo A (±0,05/±0,15) pero no en bandas_f10 → tipo 3 (más restrictivo)
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d)
    try:
        r = e.proponer_ajuste("P-11", "A", 0.47, {}, "2026-04-06")
        ok, det = r["tipo_entrada"] == "P3", r["motivo"]
    except KeyError as ex:
        ok, det = True, f"KeyError: {ex}"
    informe("P-11 vía proponer_ajuste falla cerrado (tipo 3 o KeyError, nunca AJU)", ok, det)

# 4. Propuesta abierta con otro objetivo: ¿se apila una segunda P3- del mismo parámetro?
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d)
    p1 = e.proponer_ajuste("P-09", "E", 48, {}, "2026-04-06")
    e.almacen.reloj.fijar("2026-07-06")
    p2 = e.proponer_ajuste("P-09", "E", 47, {}, "2026-07-06")      # trimestre siguiente, la primera sigue ENVIADA
    abiertas = [x for x in e.almacen.estado("F6", clave="id").values() if x.get("tipo_entrada") == "P3" and x.get("estado") == "ENVIADA"]
    informe("una P3- abierta de P-09·E no se apila con otro objetivo", len(abiertas) == 1,
            f"{len(abiertas)} P3- abiertas: {[x['a'] for x in abiertas]}")
    # estado manipulado: la P3- pasa a APROBADA (decisión del operador); una nueva propuesta igual sí puede salir
    e.almacen.escribir("F6", "AG-20", {"tipo_entrada": "P3", "id": p1["id"], "estado": "RECHAZADA"})
    p3 = e.proponer_ajuste("P-09", "E", 48, {}, "2026-07-06")
    informe("P3- rechazada no bloquea una propuesta nueva", p3["id"] != p1["id"])

# 5. Recalibración de RK (T-176 eleva sus P3-): ¿dos C5 seguidos con la misma evidencia fuera de banda dejan dos P3- en HA?
with tempfile.TemporaryDirectory() as d:
    from test_t66_evaluacion import _celda_recalibrable
    univ = __import__("conftest").cargar_universo(__import__("conftest").RUTA_UNIVERSO_EJEMPLO)
    rr = {"paso": 0.05, "banda_trimestral": 0.05, "banda_total": 0.02, "dif_ic_min": 0.10, "meses_sombra": 3}
    b = nuevo_bloque(d, univ, cfg=config_pruebas(evaluacion={"recalibracion_rk": rr}))
    b.reloj.fijar("2026-01-02")
    _celda_recalibrable(b.almacen, contaminados=0)
    b.fijar_fecha("2026-01-02")
    b.evaluador.recalibrar("2026-01-02")
    b.elevar_propuestas_tipo3("2026-01-02", "RUN-2026-0001")
    b.fijar_fecha("2026-01-09")
    b.evaluador.recalibrar("2026-01-09")                            # C5 de la semana siguiente, misma evidencia
    b.elevar_propuestas_tipo3("2026-01-09", "RUN-2026-0002")
    cola = [x for x in b.almacen.estado("HA").values() if x.get("tipo_entrada") == "P3" and x.get("origen") == "EVAL"]
    informe("P3- de P-11 no se duplica en la cola de HA en C5 sucesivos", len(cola) == 1,
            f"{len(cola)} P3 EVAL PENDING_OPERATOR para el mismo objeto")
    informe("P3- de P-11 elevada lleva plan_reversion (F6 4.7)", all(c.get("plan_reversion") for c in cola),
            str([c.get("plan_reversion") for c in cola]))

# 6. Concurrencia: dos Evaluadores sobre la misma carpeta, revisión trimestral a la vez
with tempfile.TemporaryDirectory() as d:
    a0 = Almacen(Path(d))
    a0.reloj.fijar("2026-05-01")
    _historia_umbral_e(a0)
    evs = [evaluador(d, "2026-06-05") for _ in range(2)]
    barrera = threading.Barrier(2)
    fallos = []

    def correr(ev):
        barrera.wait()
        try:
            ev.revision_trimestral("2026-06-05", "RUN-X")
        except Exception as ex:  # noqa: BLE001
            fallos.append(repr(ex))

    hs = [threading.Thread(target=correr, args=(ev,)) for ev in evs]
    [h.start() for h in hs]
    [h.join() for h in hs]
    a1 = Almacen(Path(d))
    p3 = [x for x in a1.leer("F6") if x.get("tipo_entrada") == "P3"]
    rtr = [x for x in a1.leer("F6") if x.get("tipo_entrada") == "RTR"]
    informe("revisión trimestral concurrente: una P3- y un RTR-", len(p3) == 1 and len(rtr) == 1,
            f"P3={len(p3)} RTR={len(rtr)} fallos={fallos}")

# 7. Fallo a mitad de la elevación: la escritura en F6 falla tras el CT-19 y el HA → reintento sin duplicar HA
with tempfile.TemporaryDirectory() as d:
    univ = __import__("conftest").cargar_universo(__import__("conftest").RUTA_UNIVERSO_EJEMPLO)
    b = nuevo_bloque(d, univ)
    b.fijar_fecha("2026-06-05")
    p = b.evaluador.proponer_ajuste("P-09", "E", 48, {"x": 1}, "2026-06-05")
    orig = b.almacen.escribir

    def roto(archivo, autor, entrada):
        if archivo == "F6" and entrada.get("elevada_via"):
            raise OSError("disco lleno (simulado)")
        return orig(archivo, autor, entrada)

    b.almacen.escribir = roto
    try:
        b.elevar_propuestas_tipo3("2026-06-05", "RUN-2026-0001")
    except OSError:
        pass
    b.almacen.escribir = orig
    b.elevar_propuestas_tipo3("2026-06-05", "RUN-2026-0002")
    ha = [x for x in b.almacen.leer("HA") if x.get("tipo_entrada") == "P3"]
    f6 = b.almacen.estado("F6", clave="id")[p["id"]]
    informe("fallo a mitad de la elevación: HA sin duplicar y reintento anota elevada_via", len(ha) == 1 and bool(f6.get("elevada_via")),
            f"HA={len(ha)} elevada_via={f6.get('elevada_via')}")
    # estado manipulado: P3- con elevada_via de un msg inexistente y sin HA → nunca llega a la cola
    p2 = b.evaluador.proponer_ajuste("P-09", "E", 66, {"x": 2}, "2026-06-05")
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "P3", "id": p2["id"], "elevada_via": "MSG-FALSO"})
    b.elevar_propuestas_tipo3("2026-06-05", "RUN-2026-0003")
    informe("P3- con elevada_via manipulada y sin HA (no detectado; observación)", p2["id"] in b.almacen.estado("HA"))

# 8. Novedades: idempotencia de la rehechura y sin texto libre sensible
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d, "2026-06-01")
    a = e.almacen
    a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0001", "estado": "VIGENTE", "tipo": "PREDICTIVA",
                               "observacion": "texto libre con IBAN ES00 0000", "ambito": {"clase": "RV"}})
    n1 = e.publicar_novedades("2026-06-01")
    n1b = e.publicar_novedades("2026-06-01")
    quitar = {"run_id", "hasta_seq"}
    same = {k: v for k, v in n1.items() if k not in quitar} == {k: v for k, v in n1b.items() if k not in quitar}
    informe("Novedades: rehacer la misma semana sin cambios da la misma sección", same)
    informe("Novedades: no copia texto libre de la lección", "IBAN" not in str(n1))
    # cambio de año ISO: 2026-12-31 es 2026-W53; 2027-01-04 es 2027-W01
    a.reloj.fijar("2026-12-31")
    a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0002", "estado": "VIGENTE", "tipo": "PREDICTIVA"})
    n53 = e.publicar_novedades("2026-12-31")
    a.reloj.fijar("2027-01-04")
    a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2027-0001", "estado": "VIGENTE", "tipo": "PREDICTIVA"})
    n01 = e.publicar_novedades("2027-01-04")
    informe("Novedades en el cambio de año ISO", n53["id"] == "NOV-2026-W53" and n01["id"] == "NOV-2027-W01"
            and [x["id"] for x in n01["lecciones"]] == ["LEC-2027-0001"], f"{n53['id']} {n01['id']}")

# 9. ajuste_en_sombra: un AJU- de P-11 en sombra (sin campo parametro, formato antiguo) sigue siendo la sombra de HT-03
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d)
    e.almacen.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-2026-0009", "estado": "EN_SOMBRA", "a": {"A": 0.5}})
    e.almacen.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-2026-0010", "estado": "EN_SOMBRA", "parametro": "P-09"})
    s = e.ajuste_en_sombra("2026-04-06")
    informe("ajuste_en_sombra solo devuelve P-11 (y el formato antiguo)", s is not None and s["id"] == "AJU-2026-0009")


# 10. Concurrencia más dura: 8 instancias proponen a la vez el mismo ajuste y elevan a la vez
with tempfile.TemporaryDirectory() as d:
    evs = [evaluador(d, "2026-06-05") for _ in range(8)]
    barrera = threading.Barrier(8)

    def proponer(ev):
        barrera.wait()
        ev.proponer_ajuste("P-09", "E", 48, {}, "2026-06-05")

    hs = [threading.Thread(target=proponer, args=(ev,)) for ev in evs]
    [h.start() for h in hs]
    [h.join() for h in hs]
    p3 = {x["id"] for x in Almacen(Path(d)).leer("F6") if x.get("tipo_entrada") == "P3"}
    informe("8 propuestas concurrentes iguales dejan una sola P3-", len(p3) == 1, f"{len(p3)} P3- distintas")

print(f"\n{sum(ok for _, ok in RES)}/{len(RES)} sin hallazgo")
