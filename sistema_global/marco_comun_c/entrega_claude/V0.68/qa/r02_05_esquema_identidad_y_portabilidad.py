"""QA r02 · sonda 05: esquema V0.68 re-registrado, H-07 (_identidad_ok y _candidato_d) y portabilidad del código corregido.
  a) El esquema del código es ESQUEMA_V0_68, está en esquemas_codigo.json y el de la r01 (124145…) ya no.
  b) Un estado guardado con el código de la r01 (commit 9a5225d, publicado en origin/develop) no se carga (PE-08) y no tiene
     camino de migración (MG-01): falla cerrado, pero queda varado. Se genera con una extracción de ese commit.
  c) H-07: los campos DIRECTA en un expediente que no lo es, también con valor None, dejan el expediente no íntegro; _candidato_d
     no reescribe el expediente_id del sobre de un expediente que no es DIRECTA aunque lleve analisis_ref.
  d) orquestador.py se puede leer con Python 3.11 (la r01 sí; el diff de la r01 mete un f-string con comillas anidadas, PEP 701).
(Datos SIMULADOS.)"""
import ast
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, MARCO, chk, fin, hasta, nuevo  # noqa: E402
from orquestador import Orquestador  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402

REPO = MARCO.parents[1]
R01 = "124145355f7c0eff9febc17c1b7f5553e65a8f8a18a1f01879960427240a4175"

# a)
act = pe.esquema_actual()
reg = json.loads((MARCO / "validador" / "esquemas_codigo.json").read_text(encoding="ascii"))
chk("a_esquema_actual_es_V0_68_y_registrado", act == mg.ESQUEMA_V0_68 and reg.get(act, {}).get("version") == "V0.68", act)
chk("a_el_esquema_de_la_r01_ya_no_esta", R01 not in reg)

# b) un estado guardado con el código de la r01
tmp = Path(tempfile.mkdtemp(prefix="r02_05_"))
try:
    arch = subprocess.run(["git", "-C", str(REPO), "archive", "9a5225d", "sistema_global/marco_comun_c"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tmp)], input=arch, check=True)
    m01 = tmp / "sistema_global" / "marco_comun_c"
    gen = ("import sys; sys.path[:0] = [sys.argv[1] + '/validador', sys.argv[1] + '/pruebas']\n"
           "from pruebas_orquestador import nuevo, hasta, AHORA\nimport persistencia as pe\n"
           "o = nuevo(); hasta(o, 'VALIDADA', 1)\nprint(pe.esquema_actual()); sys.stdout.flush()\n"
           "open(sys.argv[2], 'w').write(pe.volcar(o, AHORA))\n")
    out = subprocess.run([sys.executable, "-I", "-B", "-c", gen, str(m01), str(tmp / "estado_r01.json")], capture_output=True, text=True)
    print("b) esquema del código de la r01:", out.stdout.strip()[:12], out.stderr.strip()[-200:])
    texto = (tmp / "estado_r01.json").read_text()
    rc = pe.cargar(texto)
    rm = mg.migrar(texto, "2026-11-06T10:00:00+00:00", "migrar un estado de la r01 de T-80 (sonda r02_05)")
    print("b) cargar:", rc["codigo"], "| migrar:", rm["codigo"], rm["motivo"][:90])
    chk("b_estado_de_la_r01_falla_cerrado", out.stdout.strip() == R01 and not rc["ok"] and rc["codigo"] == "PE-08" and not rm["ok"], (rc["codigo"], rm["codigo"]))
    print("INFO  b) ese estado queda varado: no hay migración desde el esquema de la r01 (el Documento 0, §5, dice que ningún estado se guardó con él)")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# c) H-07
o = nuevo()
hasta(o, "VALIDADA", 1)
for campo in ("bloque_entrada", "analisis_ref", "consulta_ref"):
    o2 = copy.deepcopy(o)
    o2.expedientes["EXP-0001"][campo] = None
    chk(f"c_{campo}_None_en_un_no_DIRECTA_se_detecta", "EXP:EXP-0001" in o2.integridad(), o2.integridad())
x = copy.deepcopy(o.expedientes["EXP-0001"])
x["analisis_ref"] = "EV-SOB-0001"
x["sobre"]["documento"]["expediente_id"] = "EXP-AJENO"
c = Orquestador._candidato_d(x)
chk("c_candidato_d_no_reescribe_un_no_DIRECTA", c["sobre"]["expediente_id"] == "EXP-AJENO", c["sobre"]["expediente_id"])

# d) portabilidad
py311 = shutil.which("python3.11")
if py311:
    def lee_311(fuente):
        r = subprocess.run([py311, "-I", "-c", "import ast,sys; ast.parse(sys.stdin.read())"], input=fuente, capture_output=True, text=True)
        return r.returncode == 0, r.stderr.strip().splitlines()[-1:] if r.stderr else ""
    ahora_ok, err = lee_311((MARCO / "validador" / "orquestador.py").read_text(encoding="utf-8"))
    antes = subprocess.run(["git", "-C", str(REPO), "show", "9a5225d:sistema_global/marco_comun_c/validador/orquestador.py"],
                           capture_output=True, text=True, check=True).stdout
    antes_ok, _ = lee_311(antes)
    print("d) orquestador.py con Python 3.11: r01", antes_ok, "| ahora", ahora_ok, err)
    chk("d_orquestador_se_lee_con_python_3_11_como_en_la_r01", ahora_ok or not antes_ok, err)
else:
    print("INFO  d) no hay python3.11 en esta máquina: no se comprueba")
ast.parse((MARCO / "validador" / "orquestador.py").read_text(encoding="utf-8"))
sys.exit(fin())
