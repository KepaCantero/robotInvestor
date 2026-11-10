"""T-66 · QA r01 · PA-09 y PA-21: anonimización «auto» con ReplayClient, grabaciones anteriores, backtest con un cliente
con conocimiento previo (hitos H5 incluidos), PRG antiguos sin los campos nuevos, valores raros de prob_analista."""
import json
import tempfile
from pathlib import Path

from r01_comun import AS_OF, DATOS, RUTA_UNIVERSO_EJEMPLO, Gancho, bloque, cfg, comprobar, fin

from bloque_a.backtest import ejecutar_backtest
from bloque_a.evaluador import Evaluador, contaminacion_posible
from bloque_a.llm import MockClient, ReplayClient, ReplayFaltante


class ConMemoria(MockClient):
    conocimiento_previo = True


# 1 · ReplayClient: grabar con el simulado de base y reproducir con el valor por defecto (auto)
tmp = Path(tempfile.mkdtemp(prefix="r01_replay_"))
rec = ReplayClient(tmp / "g.jsonl", "grabar", base=MockClient())
b = bloque(cfg(), cliente=rec, tmp=tmp / "a")
comprobar("ReplayClient (base simulada) en backtest: auto anonimiza (prudente: no sabe qué modelo grabó)", b.anon is not None,
          f"anon={'sí' if b.anon else 'no'}; contaminacion_posible={b.contaminacion_posible(AS_OF)}", hallazgo=False)
b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
rep = ReplayClient(tmp / "g.jsonl", "reproducir")
b2 = bloque(cfg(), cliente=rep, tmp=tmp / "b")
try:
    r = b2.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    comprobar("grabar y reproducir con auto: reproduce sin faltantes", True)
except ReplayFaltante as e:
    comprobar("grabar y reproducir con auto: reproduce sin faltantes", False, str(e)[:80])

# 2 · Grabación anterior a T-66 (backtest sin anonimizar, el valor por defecto de antes) reproducida con auto
tmp2 = Path(tempfile.mkdtemp(prefix="r01_replay2_"))
rec = ReplayClient(tmp2 / "g.jsonl", "grabar", base=MockClient())
b = bloque(cfg(backtest={"anonimizar": False}), cliente=rec, tmp=tmp2 / "a")
b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
try:
    bloque(cfg(), cliente=ReplayClient(tmp2 / "g.jsonl", "reproducir"), tmp=tmp2 / "b").ciclo(AS_OF, alcance={"clases": ["DIV"]})
    comprobar("grabación sin anonimizar (anterior) + auto: se reproduce", True, hallazgo=False)
except ReplayFaltante as e:
    comprobar("grabación sin anonimizar (anterior) + auto: no se reproduce (cambia la clave); hay que fijar anonimizar: false",
              False, str(e)[:70], hallazgo=False)

# 3 · Backtest con cliente con conocimiento previo: todo PRG (hitos H5 incluidos) marcado, nada certificado ni aprendido
out = Path(tempfile.mkdtemp(prefix="r01_bt_"))
res = ejecutar_backtest(cfg(), "2026-03-06", "2026-05-22", str(DATOS), str(RUTA_UNIVERSO_EJEMPLO), str(out), clases=["DIV", "RF"],
                        cliente=ConMemoria())
f4 = [json.loads(x) for x in (out / "estado").glob("F4*").__next__().read_text(encoding="utf-8").splitlines() if x.strip()]
altas = [p for p in f4 if p.get("tipo_entrada") == "ALTA"]
hitos = [p for p in altas if p.get("es_hito")]
comprobar("backtest con memoria: todos los PRG (y hitos) con contaminacion_posible",
          altas and all(p.get("contaminacion_posible") is True for p in altas), f"{len(altas)} altas, {len(hitos)} hitos")
f6 = [json.loads(x) for x in (out / "estado").glob("F6*").__next__().read_text(encoding="utf-8").splitlines() if x.strip()]
apr = [x for x in f6 if x.get("tipo_entrada") in ("CERT", "LEC", "AJU", "AJUSTE")]
comprobar("backtest con memoria: sin certificados, lecciones ni ajustes", not apr, f"{[x.get('tipo_entrada') for x in apr]}")
m = res["metricas"]
comprobar("backtest con memoria: métricas admisibles vacías y las no admisibles aparte",
          not m["por_clase_horizonte"] and m["excluidos_contaminacion"]["total"] > 0,
          f"admisibles {len(m['por_clase_horizonte'])} celdas; excluidos {m['excluidos_contaminacion']['total']}")

# 4 · El mismo backtest después de la fecha de corte: nada marcado
out2 = Path(tempfile.mkdtemp(prefix="r01_bt2_"))
res2 = ejecutar_backtest(cfg(backtest={"fecha_corte_modelo": "2026-01-01"}), "2026-03-06", "2026-04-03", str(DATOS),
                         str(RUTA_UNIVERSO_EJEMPLO), str(out2), clases=["DIV"], cliente=ConMemoria())
comprobar("backtest con memoria posterior al corte: nada excluido", res2["metricas"]["excluidos_contaminacion"]["total"] == 0)


# 5 · PRG antiguos (sin contaminacion_posible ni prob_analista) y valores raros
def alta(a, pid, **c):
    base = {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-1", "clase": "RF", "horizonte": "H3", "prob_interna": 0.65,
            "sentido": "POSITIVO", "en_informe": True, "fecha_emision": "2025-01-02", "referencia_ingenua": {"valor_o_prob": 0.5},
            "estado": "ABIERTO", "fecha_resolucion": "2025-03-01"}
    a.escribir("F4", "AG-10", {**base, **c})
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": 1, "comprobacion_fuga": "SUPERADA", "valor_observado": 0.01,
                                              "fecha_resuelto": "2025-03-01"}})


from bloque_a.almacen import Almacen   # noqa: E402

a = Almacen(Path(tempfile.mkdtemp(prefix="r01_old_")))
a.reloj.fijar("2026-01-02")
alta(a, "PRG-OLD-1")                                                      # antiguo: sin campos nuevos
alta(a, "PRG-OLD-2", contaminacion_posible=None, prob_analista=None)
alta(a, "PRG-RARO-1", contaminacion_posible="false", prob_analista="0.7")   # cadena: ante la duda, contaminado; prob inválida
alta(a, "PRG-RARO-2", prob_analista=float("nan"))
alta(a, "PRG-RARO-3", prob_analista=True)
alta(a, "PRG-OK", prob_analista=0.6)
e = Evaluador(a, None, None, cfg(), None)
m = e.metricas("2026-01-02")
cel = m.get("RF|H3") or m.get(("RF", "H3")) or next(iter(m.values()))
comprobar("PRG antiguos: se leen como no contaminados", not contaminacion_posible({}) and cel["n"] == 5, f"n={cel['n']}")
comprobar("contaminacion_posible='false' (cadena): cuenta como contaminado", cel.get("excluidos_contaminacion") == 1)
avp = cel.get("analista_vs_prospectiva") or {}
comprobar("prob_analista inválidos (NaN, bool; la cadena va en un PRG contaminado, excluido) no entran y se cuentan",
          avp.get("n") == 1 and avp.get("invalidos") == 2, f"{avp}")
fin()
