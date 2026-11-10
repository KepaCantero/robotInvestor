"""r01 (QA T-79): un estado guardado por el código de la V0.53 se carga y se migra con el de la V0.67 (MIG-005) y la migración
respeta PROHIBIDAS.

Fase 1, con el código de la V0.53 (subproceso): guarda cuatro estados genuinos —uno sencillo con un expediente ABIERTO,
uno con el kill-switch activo, uno con una cartera degradada y uno firmado con clave— y un diario con operaciones después de
su punto de control.
Fase 2, con el código de la V0.67: los carga y los migra, compara el estado antes y después campo a campo y prueba registros
de migración hostiles que intentan tocar lo PROHIBIDO o lo no declarado entre V0.53 y V0.67.

Uso: python3 -I r01_migracion_v053_a_v067.py <marco V0.53> <marco V0.67> <carpeta de trabajo vacía>
"""
import json
import subprocess
import sys
from pathlib import Path

V053, V067, TRABAJO = (Path(a).resolve() for a in sys.argv[1:4])
CLAVE_HEX = bytes(range(32)).hex()   # clave de prueba (0x00..0x1f), generada para esta sonda (no es un secreto)
AHORA_M = "2026-11-12T10:00:00+00:00"
MOTIVO = "QA T-79: paso el estado guardado por V0.53 al código de V0.67"

FASE1 = r'''
import sys, json
from pathlib import Path
marco, trabajo, clave = Path(sys.argv[1]), Path(sys.argv[2]), bytes.fromhex(sys.argv[3])
sys.path.insert(0, str(marco / "validador")); sys.path.insert(0, str(marco / "pruebas"))
import persistencia as pe, diario as di
from pruebas_orquestador import nuevo, hasta, AHORA
def g(o, nombre, clave=None):
    r = pe.guardar(o, str(trabajo / nombre), AHORA, clave); assert r["ok"], r
o = nuevo(); hasta(o, "ABIERTA"); g(o, "sencillo.json")
o = nuevo(); hasta(o, "ABIERTA"); assert o.activar_kill_switch("Prueba de QA: kill-switch activo", "OPERADOR", AHORA)["ok"]; g(o, "kill.json")
o = nuevo(); hasta(o, "ABIERTA"); r = o.degradar("TACTICA", "Prueba de QA: cartera degradada", "OPERADOR", AHORA); assert r["ok"], r; g(o, "degradada.json")
o = nuevo(); hasta(o, "ABIERTA"); g(o, "firmado.json", clave)
o = nuevo(); r = di.crear(o, str(trabajo / "estado_diario.json"), str(trabajo / "diario.jsonl"), AHORA); assert r["ok"], r
d = r["diario"]; assert d.detectar("EXP-0009", "COR-0009", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
o = nuevo(); r = di.crear(o, str(trabajo / "estado_punto.json"), str(trabajo / "diario_punto.jsonl"), AHORA); assert r["ok"], r
d = r["diario"]; assert d.detectar("EXP-0009", "COR-0009", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert d.punto(AHORA)["ok"]
print("esquema", pe.esquema_actual())
'''


def main():
    TRABAJO.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", "-c", FASE1, str(V053), str(TRABAJO), CLAVE_HEX], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit("fase 1 con V0.53 fallida")
    esquema053 = r.stdout.split()[-1]
    sys.path.insert(0, str(V067 / "validador"))
    sys.path.insert(0, str(V067 / "pruebas"))
    import diario as di
    import migraciones as mg
    import persistencia as pe
    fallos = []

    def chk(nombre, cond, detalle=""):
        print(("OK    " if cond else "FALLA ") + nombre + ("" if cond else f"  {detalle}"))
        if not cond:
            fallos.append(nombre)

    clave = bytes.fromhex(CLAVE_HEX)
    chk("el_codigo_de_V053_guarda_con_ESQUEMA_V0_53", esquema053 == mg.ESQUEMA_V0_53, esquema053)
    chk("el_codigo_de_V067_tiene_ESQUEMA_V0_67", pe.esquema_actual() == mg.ESQUEMA_V0_67)
    chk("camino_V053_a_V067_es_solo_MIG005", [m.id for m in mg.camino(pe.FORMATO, mg.ESQUEMA_V0_53, mg.ESQUEMA_V0_67)] == ["MIG-005"])
    for nombre, cl in (("sencillo.json", None), ("kill.json", None), ("degradada.json", None), ("firmado.json", clave)):
        texto = (TRABAJO / nombre).read_text(encoding="utf-8")
        c = pe.cargar(texto, cl)
        chk(f"{nombre}: sin_migrar_no_se_carga_PE08", not c["ok"] and c["codigo"] == "PE-08", c.get("codigo"))
        m = mg.migrar(texto, AHORA_M, MOTIVO, cl)
        chk(f"{nombre}: MIG005_lo_migra", m["ok"] and m["migraciones"] == ["MIG-005"], (m.get("codigo"), m.get("motivo")))
        if not m["ok"]:
            continue
        e0 = json.loads(texto)["estado"]
        e1 = json.loads(m["texto"])["estado"]
        distintos = sorted(k for k in set(e0) | set(e1) if json.dumps(e0.get(k), sort_keys=True) != json.dumps(e1.get(k), sort_keys=True))
        chk(f"{nombre}: solo_cambian_limites_ultimo_ahora_y_huella_config", set(distintos) <= {"limites", "ultimo_ahora", "huella_config"}, distintos)
        for p in ("kill", "rearmes", "degradadas", "cfg", "expedientes", "posiciones"):
            if p in e0:
                chk(f"{nombre}: {p}_igual", e0[p] == e1[p])
        ent0, ent1 = e0["limites"]["entradas"], e1["limites"]["entradas"]
        chk(f"{nombre}: limites_solo_anade_una_MIGRACION", ent1[:-1] == ent0 and ent1[-1].get("tipo") == "MIGRACION"
            and ent1[-1].get("migraciones") == ["MIG-005"] and e1["limites"]["historial"][:-1] == e0["limites"]["historial"])
        o = m["orquestador"]
        chk(f"{nombre}: integro_tras_migrar", o.integridad() == [] and o.config_integra(), o.integridad())
        chk(f"{nombre}: migrar_otra_vez_no_hace_nada", (lambda r2: r2["ok"] and r2["migraciones"] == [])(mg.migrar(m["texto"], AHORA_M, MOTIVO, cl)))
        c2 = pe.cargar(m["texto"], cl)
        chk(f"{nombre}: el_migrado_se_carga", c2["ok"], c2.get("motivo"))
        if nombre == "kill.json":
            chk("kill.json: sigue_con_el_kill_switch", o.kill is not None)
        if nombre == "degradada.json":
            chk("degradada.json: sigue_degradada", "TACTICA" in o.degradadas and o.nivel("TACTICA") == json.loads(texto)["estado"]["cfg"]["nivel_autonomia"].get("TACTICA") or "TACTICA" in o.degradadas)
        if nombre == "firmado.json":
            chk("firmado.json: sin_clave_no_migra", not mg.migrar(texto, AHORA_M, MOTIVO)["ok"])
            chk("firmado.json: con_otra_clave_no_migra", not mg.migrar(texto, AHORA_M, MOTIVO, bytes(range(1, 33)))["ok"])

    # estado de V0.53 tocado: un campo cambiado sin rehacer la huella, y la configuración tocada con la huella rehecha
    texto = (TRABAJO / "sencillo.json").read_text(encoding="utf-8")
    d = json.loads(texto)
    d["estado"]["cfg"]["politica_f"] = {**d["estado"]["cfg"]["politica_f"]}
    d2 = json.loads(texto); d2["estado"]["kill"] = None; d2["estado"]["ultimo_ahora"] = "2026-11-06T09:30:00+00:00"
    r2 = mg.migrar(json.dumps(d2), AHORA_M, MOTIVO)
    chk("V053_tocado_sin_rehacer_la_huella_no_migra", not r2["ok"] and r2["codigo"] in ("PE-02", "PE-03"), (r2.get("codigo"), r2.get("motivo")))
    d3 = json.loads(texto)
    k = next(iter(sorted(d3["estado"]["cfg"]["politica_f"])))
    d3["estado"]["cfg"]["max_por_dia_test"] = 1
    d3["huella"] = pe._huella(d3["estado"])
    r3 = mg.migrar(json.dumps(d3, ensure_ascii=True, sort_keys=True, separators=(",", ":")), AHORA_M, MOTIVO)
    chk("V053_con_cfg_tocada_y_huella_rehecha_no_migra", not r3["ok"], (r3.get("codigo"), r3.get("motivo"), k))
    d4 = json.loads(texto); d4["esquema"] = mg.ESQUEMA_V0_67; d4["huella"] = pe._huella(d4["estado"])
    r4 = pe.cargar(json.dumps(d4, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    chk("V053_que_dice_ser_V067_no_se_carga_sin_mas", not r4["ok"] or r4["orquestador"].integridad() != [], (r4.get("codigo"), r4.get("motivo")))

    # registros hostiles entre V0.53 y V0.67: tocar lo PROHIBIDO (aunque se declare) o lo no declarado es MG-04
    base = tuple(m for m in mg.MIGRACIONES if m.id != "MIG-005")
    def hostil(fn, cambia):
        return base + (mg.Migracion("MIG-X", pe.FORMATO, mg.ESQUEMA_V0_53, mg.ESQUEMA_V0_67, fn, frozenset(cambia), "hostil de la QA"),)
    def quita_kill(e):
        e["kill"] = {"actor": "X", "motivo": "x", "ahora": "2026-11-06T09:00:00+00:00"}; return e
    def nivel(e):
        e["cfg"]["nivel_autonomia"] = {c: "L3" for c in e["cfg"]["nivel_autonomia"]}; return e
    def limite(e):
        e["cfg"]["politica_f"][mg.LIMITE_PERDIDA] = e["cfg"]["politica_f"][mg.LIMITE_PERDIDA] * 10; return e
    def rearmes(e):
        e["rearmes"] = e["rearmes"] + [{"actor": "X", "ahora": "2026-11-06T09:00:00+00:00", "lista": {}}]; return e
    def expediente(e):
        e["expedientes"] = {}; return e
    for etiqueta, fn, cambia in (("kill_declarado", quita_kill, {"kill"}), ("nivel_declarado", nivel, {"cfg.nivel_autonomia"}),
                                  ("limite_perdida_declarado", limite, {"cfg.politica_f"}), ("rearmes_declarado", rearmes, {"rearmes"}),
                                  ("kill_sin_declarar", quita_kill, set()), ("expedientes_sin_declarar", expediente, set())):
        for nombre in ("sencillo.json", "kill.json"):
            r = mg.migrar((TRABAJO / nombre).read_text(encoding="utf-8"), AHORA_M, MOTIVO, registro=hostil(fn, cambia))
            chk(f"hostil_{etiqueta}_{nombre}: MG04", not r["ok"] and r["codigo"] == "MG-04", (r.get("codigo"), r.get("motivo")))
    # PROHIBIDAS sigue siendo la de la V0.53
    chk("PROHIBIDAS_no_cambia_respecto_de_V053", mg.PROHIBIDAS == ("limites", "kill", "rearmes", "ultimo_ahora", "huella_config",
                                                                 f"cfg.politica_f.{mg.LIMITE_PERDIDA}", "cfg.nivel_autonomia"))

    # diario de V0.53: sin migrar no abre; migrar_ficheros lo deja abrible con V0.67 y con lo operado después del punto
    ab = di.abrir(str(TRABAJO / "estado_diario.json"), str(TRABAJO / "diario.jsonl"))
    chk("diario_V053_sin_migrar_no_abre", not ab["ok"], ab.get("codigo"))
    mf = mg.migrar_ficheros(str(TRABAJO / "estado_diario.json"), str(TRABAJO / "diario.jsonl"), AHORA_M, MOTIVO)
    chk("diario_V053_con_operaciones_tras_el_punto_no_migra_MG06", not mf["ok"] and mf["codigo"] == "MG-06", (mf.get("codigo"), mf.get("motivo")))
    chk("y_no_toca_los_ficheros", di.abrir(str(TRABAJO / "estado_diario.json"), str(TRABAJO / "diario.jsonl"))["codigo"] == "PE-08")
    mf = mg.migrar_ficheros(str(TRABAJO / "estado_punto.json"), str(TRABAJO / "diario_punto.jsonl"), AHORA_M, MOTIVO)
    chk("migrar_ficheros_V053_con_punto_ok_MIG005", mf["ok"] and mf["migraciones"] == ["MIG-005"], (mf.get("codigo"), mf.get("motivo")))
    ab = di.abrir(str(TRABAJO / "estado_punto.json"), str(TRABAJO / "diario_punto.jsonl"))
    chk("diario_migrado_abre_y_conserva_EXP0009", ab["ok"] and "EXP-0009" in ab["diario"].orquestador.expedientes, (ab.get("codigo"), ab.get("motivo")))

    print(f"\n{len(fallos)} fallos")
    print("RESULTADO r01 MIGRACION V0.53->V0.67:", "TODAS LAS PRUEBAS PASAN" if not fallos else "HAY FALLOS")


main()
