"""QA r05 · sonda 03: un estado y un diario guardados con el código de la r04 (commit c482bf1, antes de H-16, mismo esquema V0.68)
con el origen reencargado y BLOQUEADO mientras el DIRECTA tenía S1 en juego. ¿Qué hace el código actual al cargarlos?
Uso: python -I -B r05_03_estado_de_la_r04.py <carpeta marco_comun_c de una copia en c482bf1>
     (p. ej. git worktree add --detach <dir> c482bf1; luego <dir>/sistema_global/marco_comun_c). Sin argumento: SALTA.
(Datos SIMULADOS.)"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, fin  # noqa: E402
import persistencia as pe  # noqa: E402
import diario as di  # noqa: E402

GEN = r'''
import sys
from pathlib import Path
M = Path(sys.argv[1])
sys.path.insert(0, str(M / "validador")); sys.path.insert(0, str(M / "pruebas"))
from pruebas_orquestador import AHORA, COND_OBS, encargo, nuevo, sobre_para
import diario as di
r = di.crear(nuevo(), sys.argv[2], sys.argv[3], AHORA); assert r["ok"], r
o = r["diario"]
assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
e2 = encargo(1); e2["event_id"] = "EV-ENC-0001-B"
assert o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)["ok"]
s2 = sobre_para(1, None); s2["event_id"] = "EV-SOB-0001-B"; s2["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
assert o.entregar_sobre("EXP-0001", s2, AHORA)["codigo"] == "O-32"
import persistencia as pe
assert pe.guardar(o._o, sys.argv[4], AHORA)["ok"]
print("generado con el código de", M)
'''

if len(sys.argv) < 2:
    print("SALTA: falta la carpeta marco_comun_c de una copia en c482bf1")
    sys.exit(0)
with tempfile.TemporaryDirectory() as d:
    est, dia, solo = os.path.join(d, "e.json"), os.path.join(d, "d.jsonl"), os.path.join(d, "solo.json")
    g = subprocess.run([sys.executable, "-I", "-B", "-c", GEN, sys.argv[1], est, dia, solo], capture_output=True, text=True)
    print(g.stdout.strip(), g.stderr.strip()[-300:])
    assert g.returncode == 0
    r = di.abrir(est, dia)
    print("diario de la r04 abierto con el código actual:", r["ok"], r["codigo"], r["motivo"][:110])
    chk("a_el_diario_no_se_reproduce_en_silencio", not r["ok"], r)
    r = pe.cargar_de(solo, None)
    print("estado de la r04 cargado con el código actual:", r["ok"], r["codigo"])
    o = r["orquestador"]
    print("   origen", o.expedientes["EXP-0001"]["estado"], "con exclusion", bool(o.expedientes["EXP-0001"].get("exclusion")),
          "| DIRECTA", o.expedientes["EXP-DD-01"]["estado"], o.expedientes["EXP-DD-01"]["sobre"]["event_id"], "| integridad", o.integridad())
    rc = o.comparar(["EXP-DD-01"], "D", AHORA)
    rp = o.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01")) if rc["ok"] else rc
    print("   comparar y proponer el DIRECTA con S1:", rc["codigo"], rp["ok"], rp["codigo"])
    print("INFO  b_estado_r04_cargado_el_DIRECTA_llega_a", o.expedientes["EXP-DD-01"]["estado"])
sys.exit(fin())
