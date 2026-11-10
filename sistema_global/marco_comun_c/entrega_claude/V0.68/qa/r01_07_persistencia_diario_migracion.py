"""QA r01 · sonda 07: persistencia, diario y migración con lo nuevo.
  - un estado con expedientes DIRECTA (C, D y E) y consultas se guarda, se carga y vuelve a dar el mismo texto;
  - un fichero con el rastro SC-5 o un campo DIRECTA tocado se carga con O-13 y kill-switch;
  - los estados guardados de V0.45, V0.50 y V0.52 cargan (migración hasta MIG-006), íntegros y con el rastro vacío;
  - el diario reproduce operaciones rechazadas y aceptadas de abrir_directa/consultar y da el mismo estado.
"""
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, MARCO, chk, descartado_por_operador, enc_directa, fin, hasta, nuevo  # noqa: E402
import persistencia as pe  # noqa: E402
import diario as di  # noqa: E402

MOT = "solo hay un candidato en la cartera: lo pidió el operador"
CB = {"consulta_id": "CON-0001", "correlation_id": "COR-CON-0001", "tipo": "COMPARAR", "bloque": "D", "cartera": "TACTICA",
      "analisis": ["EV-SOB-0001"], "pregunta": "¿Este análisis rinde más que el benchmark?"}


def poblado():
    o = nuevo()
    descartado_por_operador(o, 1)
    assert o.consultar(CB, "BROKER", AHORA)["ok"]
    assert o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT, consulta_id="CON-0001")["ok"]
    assert o.abrir_directa("EXP-DC-05", "COR-EXP-DC-05", "TACTICA", "C", "BROKER", AHORA, encargo=enc_directa("EXP-DC-05", 5))["ok"]
    return o


o = poblado()
t = pe.volcar(o, AHORA)
rc = pe.cargar(t)
chk("guardar_cargar_ida_y_vuelta", rc["ok"] and pe.volcar(rc["orquestador"], AHORA) == t and rc["orquestador"].integridad() == [], rc.get("motivo"))

# quien reescribe el fichero sin clave recalcula la huella del fichero (PE-02); lo que lo para es integridad() al cargar
import copy  # noqa: E402
o2 = copy.deepcopy(o)
o2.consultas["entradas"][0]["consulta"]["pregunta"] = "otra pregunta escrita a mano en el fichero"
rc = pe.cargar(pe.volcar(o2, AHORA))
chk("fichero_con_SC5_tocado_O13", not rc["ok"] and rc["codigo"] == "O-13" and rc["orquestador"].kill is not None, (rc.get("codigo"), rc.get("motivo")))
o2 = copy.deepcopy(o)
o2.expedientes["EXP-DE-01"]["bloque_entrada"] = "D"
rc = pe.cargar(pe.volcar(o2, AHORA))
chk("fichero_con_bloque_entrada_tocado_O13", not rc["ok"] and rc["codigo"] == "O-13", (rc.get("codigo"), rc.get("motivo")))
o2 = copy.deepcopy(o)
o2.consultas = {"historial": [], "estado": "VIGENTE", "entradas": []}
rc = pe.cargar(pe.volcar(o2, AHORA))
print("fichero con el rastro SC-5 vaciado (huella recalculada):", rc["ok"], rc.get("codigo"), (rc.get("motivo") or "")[:80],
      "| EXP-DE-01.consulta_ref:", rc["orquestador"].expedientes["EXP-DE-01"]["consulta_ref"] if rc.get("orquestador") else None)
d = json.loads(t)
d["estado"]["consultas"]["entradas"][0]["consulta"]["pregunta"] = "tocado sin recalcular la huella"
rc = pe.cargar(json.dumps(d))
chk("fichero_tocado_sin_recalcular_huella_PE02", not rc["ok"] and rc["codigo"] == "PE-02", rc.get("codigo"))
d = json.loads(t)
del d["estado"]["consultas"]
rc = pe.cargar(json.dumps(d))
chk("fichero_sin_el_atributo_consultas_no_carga", not rc["ok"], (rc.get("codigo"), rc.get("motivo")))

for f in sorted((MARCO / "pruebas" / "estados").glob("estado_V0_*.json")):
    import migraciones as mg  # noqa: E402
    rm = mg.migrar(f.read_text(encoding="utf-8"), "2026-11-10T09:00:00+00:00", "QA r01 de T-80: migrar a la V0.68")
    print(f"   {f.stem}: migraciones {[m if isinstance(m, str) else m.get('id', m) for m in rm.get('migraciones', [])]}", rm["codigo"])
    rc = pe.cargar(rm["texto"]) if rm["ok"] else rm
    ok = rc["ok"] and rc["orquestador"].integridad() == [] and rc["orquestador"].consultas == {"historial": [], "estado": "VIGENTE", "entradas": []}
    chk(f"migra_{f.stem}_hasta_V0_68_integro", ok, (rc.get("codigo"), rc.get("motivo")))
    if ok:   # y con el estado migrado se puede abrir un DIRECTA si hay un análisis reutilizable (o rechazar sin romper nada)
        om = rc["orquestador"]
        reg = om.analisis_vigentes(om.ultimo_ahora or AHORA)
        print(f"   {f.stem}: {len(om.expedientes)} expedientes, registro de análisis vigentes: {len(reg)}")

with tempfile.TemporaryDirectory() as tmp:
    o = nuevo()
    descartado_por_operador(o, 1)
    rd = di.crear(o, Path(tmp) / "e.json", Path(tmp) / "d.jsonl", AHORA)
    D = rd["diario"]
    rs = [D.consultar(CB, "BROKER", AHORA),
          D.consultar({**CB, "pregunta": "otra pregunta con el mismo id"}, "BROKER", AHORA),          # O-03
          D.abrir_directa("EXP-X", "COR-X", "TACTICA", "F", "BROKER", AHORA, analisis="EV-SOB-0001"),  # O-01
          D.abrir_directa("EXP-X", "COR-X", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id="CON-0001"),
          D.abrir_directa("EXP-Y", "COR-Y", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"),  # O-06: en juego
          D.comparar(["EXP-X"], "D", AHORA),
          D.abrir_directa("EXP-DC-05", "COR-EXP-DC-05", "TACTICA", "C", "BROKER", AHORA, encargo=enc_directa("EXP-DC-05", 5)),
          D.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", extra=1)]   # argumento que no existe
    print("diario:", [(r["ok"], r["codigo"]) for r in rs])
    ra = di.abrir(Path(tmp) / "e.json", Path(tmp) / "d.jsonl")
    chk("diario_reproduce_igual", ra.get("ok") and pe.volcar(ra["diario"]._o, AHORA) == pe.volcar(D._o, AHORA), ra.get("motivo"))
sys.exit(fin())
