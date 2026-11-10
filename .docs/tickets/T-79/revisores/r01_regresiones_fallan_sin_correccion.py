"""r01 (QA T-79), CA-3: cada corrección de Claude tiene una prueba que falla sin ella. En copias del marco se deshace una
corrección cada vez y se comprueba qué batería cae y por qué comprobación.

- G-02: se quita la validación del tope en consola._diario.
- G-03: se devuelve el tope a la firma (1000 literal) y se quita n_lineas_diario_ambar de parametros.py, con su PAR-0.4.0.
- MIG-005: se deja el parámetro en parametros.py pero se quita MIG-005 y ESQUEMA_V0_67 (lo que pasaría si se olvida).
- G-01: se quita del LEEME la línea de pruebas_reduccion_t43.py (pruebas_marco.sh lo avisa; aquí se mira el aviso con grep).

Uso: python3 -I r01_regresiones_fallan_sin_correccion.py <carpeta marco_comun_c> <carpeta temporal vacía>
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

M, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
res = []


def chk(nombre, cond, detalle=""):
    res.append(cond)
    print(("OK       " if cond else "HALLAZGO ") + nombre + ("" if cond else f"  -> {detalle}"))


def copia(nombre):
    d = TMP / nombre
    shutil.rmtree(d, ignore_errors=True)
    for sub in ("validador", "pruebas", "esquemas"):
        shutil.copytree(M / sub, d / sub, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(M / "LEEME.md", d / "LEEME.md")
    return d


def cambia(ruta, viejo, nuevo):
    t = ruta.read_text(encoding="utf-8")
    assert viejo in t, f"no encuentro el texto a deshacer en {ruta.name}: {viejo[:60]}"
    ruta.write_text(t.replace(viejo, nuevo, 1), encoding="utf-8")


def corre(d, bateria):
    r = subprocess.run([sys.executable, "-I", bateria], cwd=d / "pruebas", capture_output=True, text=True, timeout=300)
    fallan = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FALLA")]
    ult = (r.stdout.strip().splitlines() or [r.stderr.strip()[-160:]])[-1]
    return fallan, ult, r.returncode


TMP.mkdir(parents=True, exist_ok=True)
V = "validador"
# G-02
d = copia("g02")
cambia(d / V / "consola.py", '    if isinstance(tope, bool) or not isinstance(tope, int) or tope < 1:\n        return "ROJO", f"el tope de líneas del diario no es un entero positivo ({tope!r}): revisa la configuración"\n', "")
f, ult, rc = corre(d, "pruebas_consola_sistema.py")
print(f"         (info) G-02 deshecha: fallan {f}")
chk("G-02 deshecha: cae r01_umbral_nan_inf_o_bool_es_rojo", "r01_umbral_nan_inf_o_bool_es_rojo" in f and rc != 0, (f, ult))

# G-03 (vuelta a la V0.66: tope literal en la firma, sin parámetro)
d = copia("g03")
c = d / V / "consola.py"
t = c.read_text(encoding="utf-8").replace('lineas_diario_ambar=PARAMETROS["n_lineas_diario_ambar"]', "lineas_diario_ambar=1000")
c.write_text(t.replace("from parametros import PARAMETROS\n", ""), encoding="utf-8")
cambia(d / V / "parametros.py", '    "n_lineas_diario_ambar": 1000,', "")
cambia(d / V / "parametros.py", 'VERSION_PARAMETROS = "PAR-0.4.0"', 'VERSION_PARAMETROS = "PAR-0.3.0"')
f, ult, rc = corre(d, "pruebas_consola_sistema.py")
print(f"         (info) G-03 deshecha: consola_sistema -> {f or ult}")
chk("G-03 deshecha: cae la batería del panel (r01_umbral_por_defecto_sale_de_parametros o import)", rc != 0, (f, ult))
f2, ult2, rc2 = corre(d, "pruebas_comparador_t17.py")
chk("G-03 deshecha: cae parametros_versionados de T-17 (PAR-0.4.0)", "parametros_versionados" in f2, (f2, ult2))

# MIG-005 olvidada: parámetro nuevo sin registrar el esquema ni la migración
d = copia("mig005")
m = d / V / "migraciones.py"
t = m.read_text(encoding="utf-8")
t = re.sub(r'    Migracion\("MIG-005".*?\),\n(?=\))', "", t, flags=re.S)
m.write_text(t, encoding="utf-8")
f, ult, rc = corre(d, "pruebas_migraciones_t03.py")
print(f"         (info) MIG-005 quitada: migraciones_t03 -> {f[:6] or ult}")
chk("sin MIG-005 cae pruebas_migraciones_t03.py", rc != 0 and bool(f), (f, ult))
f, ult, rc = corre(d, "pruebas_integracion_v053.py")
chk("sin MIG-005 cae pruebas_integracion_v053.py (v067_esquema_actual_y_MIG005_sin_cambios)", "v067_esquema_actual_y_MIG005_sin_cambios" in f, (f, ult))

# G-01: la lista del LEEME frente al disco (lo que avisa pruebas_marco.sh)
d = copia("g01")
cambia(d / "LEEME.md", "python3 pruebas/pruebas_reduccion_t43.py\n", "")
lista = d.joinpath("LEEME.md").read_text(encoding="utf-8")
faltan = [p.name for p in (d / "pruebas").glob("pruebas_*.py") if f"python3 pruebas/{p.name}" not in lista]
chk("G-01 deshecha: el aviso de pruebas_marco.sh la detectaría", faltan == ["pruebas_reduccion_t43.py"], faltan)

shutil.rmtree(TMP, ignore_errors=True)
n = res.count(False)
print(f"\nRESULTADO r01 REGRESIONES: {'TODAS FALLAN SIN SU CORRECCION' if not n else f'{n} HALLAZGO(S)'}")
