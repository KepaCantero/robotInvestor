"""r04 (análisis) · Resultado del backtest largo: incidencias R11 en HA, altas/resoluciones de F4, entregas bloqueadas,
restos de _borradores y _bloqueados, estados finales de F4."""
import json, pathlib, collections, sys
d = pathlib.Path(sys.argv[1])
est = d / "salida" / "estado"
def jl(n): 
    p = est / n
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
f4 = jl("F4_registro_pronosticos.jsonl"); ha = jl("HA_historial_auditorias.jsonl"); f5 = jl("F5_historial_analisis.jsonl")
print("F4 entradas por tipo:", collections.Counter(e.get("tipo_entrada") for e in f4))
print("F4 hitos:", sum(1 for e in f4 if e.get("es_hito") and e.get("tipo_entrada") == "ALTA"))
ests = {}
for e in f4: ests[e["prg_id"]] = e.get("estado", ests.get(e["prg_id"]))
print("F4 estado final:", collections.Counter(ests.values()))
print("HA incidencias R11/ESCRITURA:", [x.get("detalle") for x in ha if x.get("tipo") in ("ESCRITURA", "ACCESO_FUERA_DE_MATRIZ")][:5])
runs = [x for x in f5 if x.get("tipo_entrada") == "RUN"]
print("RUN:", len(runs), "| entrega:", collections.Counter(x.get("entrega") for x in runs), "| estado:", collections.Counter(x.get("estado") for x in runs))
sal = d / "salida"
print("_borradores restantes:", [str(p) for p in sal.rglob("_borradores")][:3])
print("_bloqueados:", [str(p.relative_to(sal)) for p in sal.rglob("_bloqueados")][:5])
log = (d / "log.txt").read_text().splitlines()
print("log (traceback):", [l for l in log if "Traceback" in l or "Error" in l][:5], "| última:", log[-1])
