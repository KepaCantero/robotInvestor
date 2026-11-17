"""QA r04 de T-143 · Las frases nuevas de la r04 en el Anexo B V5.2, medidas con el ejecutor (no con la prosa).

Lo que las pruebas `test_t143_r04_*` no miden por sí solas, porque el ciclo simulado sale APTO en HT-09 (no llega a CT-14) y
sus dos tipos van en N2 (no ven N0/N1 ni el V6 con `v6.curacion_llm`):

1. CT-14: con HT-09 en ADVERTENCIA o BLOQUEO, en el V5, en el V6 por defecto y en el V6 con `v6.dictamen_g3_llm`: si se emite
   el CT-14, si se pide `DICTAMEN_G3` a AG-18 y qué dictamen queda.
2. CT-11: con niveles N1, N2 y N3, en el V5, en el V6 por defecto y en el V6 con `v6.curacion_llm`: si se emite el CT-11.
3. CT-07/CT-08: con cinco referencias, todas ofrecidas, solo cuentan tres; con una no ofrecida entre las tres primeras, no la
   sustituye la cuarta.
4. CT-17: `objeto` de cada hallazgo y, sin él, el run.

Desde la raíz, con el Python del .venv:  .venv/bin/python .docs/tickets/T-143/revisores/r04_01_interruptores_v6.py
Termina con 1 si algo no coincide con lo que dice el Anexo B. Sin red ni gasto (cliente simulado).
"""
from __future__ import annotations

import sys
import tempfile
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]

import conftest  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a import orquestacion  # noqa: E402

FECHA = pd.Timestamp("2026-06-05")
FALLOS: list[str] = []


def anota(ok: bool, texto: str) -> None:
    print(("OK      " if ok else "HALLAZGO") + " " + texto)
    if not ok:
        FALLOS.append(texto)


def bloque(tmp, **extra):
    cfg = conftest.config_pruebas(**extra) if extra else None
    return conftest.nuevo_bloque(tmp, conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO), cfg=cfg)


DISENOS = {"V5": {}, "V6": {"diseno": "v6"}}


# ---------------------------------------------------------------- 1. CT-14
def g3(tmp, extra, resultado):
    b = bloque(tmp, **extra)
    creados, invocados = [], []
    crear = b.mensajeria.crear
    b.mensajeria.crear = lambda ct, *a, **k: (creados.append(ct), crear(ct, *a, **k))[1]
    b._invocar = lambda ag, ct, msg, esq, *a, **k: (invocados.append((ag, ct, esq)),
                                                    types.SimpleNamespace(datos={"dictamen": "APTO_CON_ADVERTENCIAS", "motivo": "m"}))[1]
    inc = [{"ruta": "x", "detalle": "d"}]
    comp = [{"id": "C05", "resultado": resultado, "incidencias": inc}]
    original = orquestacion.sint.ht09_validar
    orquestacion.sint.ht09_validar = lambda *a, **k: {"dictamen": resultado, "comprobaciones": comp}
    try:
        _, res = b._validar_g3({"clases": {}, "limitaciones": []}, {}, FECHA, "RUN-2026-0001")
    finally:
        orquestacion.sint.ht09_validar = original
    return "CT-14" in creados, ("AG-18", "CT-14", "DICTAMEN_G3") in invocados, res["dictamen"]


casos_g3 = {"V5": {}, "V6": {"diseno": "v6"}, "V6 con dictamen_g3_llm": {"diseno": "v6", "v6": {"dictamen_g3_llm": True}}}
for nombre, extra in casos_g3.items():
    for resultado, esperado in (("ADVERTENCIA", "APTO_CON_ADVERTENCIAS"), ("BLOQUEO", "BLOQUEADO")):
        with tempfile.TemporaryDirectory() as t:
            emitido, pedido, dictamen = g3(t, extra, resultado)
        debe_pedir = nombre != "V6"
        anota(emitido and pedido == debe_pedir and dictamen == esperado,
              f"CT-14 · {nombre} · HT-09 {resultado}: CT-14 emitido={emitido}, DICTAMEN_G3 pedido={pedido} (Anexo B: {debe_pedir}), "
              f"dictamen={dictamen} (esperado {esperado})")


# ---------------------------------------------------------------- 2. CT-11
class Parar(Exception):
    pass


def curacion(tmp, extra, nivel):
    b = bloque(tmp, **extra)
    creados = []
    crear = b.mensajeria.crear
    b.mensajeria.crear = lambda ct, *a, **k: (creados.append(ct), crear(ct, *a, **k))[1]

    def invocar(ag, ct, *a, **k):
        raise Parar(ct)
    b._invocar = invocar
    b._filtrar_evidencia = lambda *a, **k: None
    an = {"clase": "RV", "nivel": nivel, "finalistas": [{"proxy": "EJEMPLO", "_piezas": [
        {"afirmacion": "a", "fuente": "REF-2026-0001", "direccion": "neutra", "extracto": "e"}]}]}
    try:
        b._registrar_evidencia_clase(an, FECHA, "RUN-2026-0001")
    except Exception:   # lo que viene después de la curación no se mide aquí
        pass
    return "CT-11" in creados


casos_cur = {"V5": {}, "V6": {"diseno": "v6"}, "V6 con curacion_llm": {"diseno": "v6", "v6": {"curacion_llm": True}}}
for nombre, extra in casos_cur.items():
    for nivel in ("N0", "N1", "N2", "N3"):
        with tempfile.TemporaryDirectory() as t:
            emitido = curacion(t, extra, nivel)
        debe = nivel in ("N2", "N3") and nombre != "V6"
        anota(emitido == debe, f"CT-11 · {nombre} · {nivel}: emitido={emitido} (Anexo B: {debe})")


# ---------------------------------------------------------------- 3. CT-07 / CT-08
def piezas(tmp, refs, ofrecidas=(1, 2, 3, 4, 5)):
    b = bloque(tmp)
    b.referencias.para_clase = lambda *a, **k: {"referencias": [{"ref_id": f"REF-2026-000{i}", "anio": 2025} for i in ofrecidas]}
    b._invocar = lambda *a, **k: types.SimpleNamespace(datos={"referencias": refs, "sintesis": "S.", "lagunas": []})
    out = b._peticion_conocimiento("RV", {"proxy": "EJEMPLO", "horizontes_aplicables": ["H3"]}, {"tipo": "CT-08", "pregunta": "?"},
                                   None, FECHA, "RUN-2026-0001", None)
    return [p["fuente"] for p in out["piezas"]]


cinco = [{"ref_id": f"REF-2026-000{i}", "afirmacion": f"A{i}."} for i in range(1, 6)]
with tempfile.TemporaryDirectory() as t:
    f = piezas(t, cinco)
anota(f == ["REF-2026-0001", "REF-2026-0002", "REF-2026-0003"], f"CT-07/CT-08 · cinco ofrecidas: cuentan {f} (Anexo B: las tres primeras)")
with tempfile.TemporaryDirectory() as t:
    f = piezas(t, cinco, ofrecidas=(1, 3, 4, 5))
anota(f == ["REF-2026-0001", "REF-2026-0003"],
      f"CT-07/CT-08 · la segunda sin ofrecer: cuentan {f} (Anexo B: de las tres primeras, las ofrecidas; la cuarta no entra)")


# ---------------------------------------------------------------- 4. CT-17
with tempfile.TemporaryDirectory() as t:
    b = bloque(t, auditoria={"en_backtest": True})
    b._invocar = lambda *a, **k: types.SimpleNamespace(datos={"resumen": "r", "hallazgos": [
        {"regla": "R1", "descripcion": "d", "severidad": "Menor", "objeto": "OPP-2026-0001"},
        {"regla": "R2", "descripcion": "d", "severidad": "Menor", "objeto": None},
        {"regla": "R3", "descripcion": "d", "severidad": "Menor"}]})
    b._auditar({"paquete": {"clases": {}, "limitaciones": []}, "g3_entregables": {},
                "entregables": {"informe_tecnico": "a", "informe_visual": "b", "paquete_json": "c"}},
               "PERIODICO", {"RV": "N2"}, FECHA, "RUN-2026-0001")
    obj = [e["objeto"] for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "HAL"]
anota(obj[0] == "OPP-2026-0001" and obj[2] == "RUN-2026-0001",
      f"CT-17 · objeto de cada hallazgo: {obj} (Anexo B: el suyo; si no lo trae, el run)")
print(f"(nota) CT-17 con `objeto: null` explícito queda {obj[1]!r}: «si lo trae» no lo distingue; sin efecto sobre el esquema")

print(f"\n{len(FALLOS)} hallazgo(s)")
sys.exit(1 if FALLOS else 0)
