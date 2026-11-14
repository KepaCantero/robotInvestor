"""QA r02 de T-117 · Mutantes sobre el código de la r02. Seis mutantes de la r01 (G02, G03, G05, G06, G07 y G30) ya no se
aplican porque sus líneas cambiaron con las correcciones: aquí están sus equivalentes, más los de las correcciones nuevas
(H-01: umbral del CT-06; H-02: recuento no entero; H-03: tipo de `umbral_por_perfil`; H-06: motivo del descarte).

Uso:  python r02_01_mutantes_r02.py <copia desechable del repositorio, con «qa_f3_mut» o «qa2_mut» en la ruta>
Ejecuta tests/test_t117_gc1.py con cada mutante. MUERTO = alguna prueba falla; VIVO = todas pasan.
"""
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
copia = Path(sys.argv[1]).resolve()
assert "qa_f3_mut" in str(copia) or "qa2_mut" in str(copia), "solo en la copia desechable"
ej = copia / "bloque_a" / "11_Ejecutor"
D, O = "bloque_a/diseno_v6.py", "bloque_a/orquestacion.py"
MUT = [
    ("R01", O, "H-01: el CT-06 vuelve a llevar el umbral general en la V6",
     '"umbral_senal_gc1": (v6.umbral_gc1(self, clase) if v6.activo(self, "gc1.por_codigo")\n                                    else parametro(self.cfg, "seleccion.umbral_senal_gc1")),',
     '"umbral_senal_gc1": parametro(self.cfg, "seleccion.umbral_senal_gc1"),'),
    ("R02", O, "H-01: el CT-06 lleva el umbral del tipo también en la V5",
     '"umbral_senal_gc1": (v6.umbral_gc1(self, clase) if v6.activo(self, "gc1.por_codigo")\n                                    else parametro(self.cfg, "seleccion.umbral_senal_gc1")),',
     '"umbral_senal_gc1": v6.umbral_gc1(self, clase),'),
    ("R03", D, "G02': el umbral del tipo se ignora (siempre el general)",
     '    return float(propio if propio is not None else parametro(bloque.cfg, "seleccion.umbral_senal_gc1"))',
     '    return float(parametro(bloque.cfg, "seleccion.umbral_senal_gc1"))'),
    ("R04", D, "G03': familias: < pasa a <=", "return math.isfinite(float(n)) and float(n) < fam_min", "return math.isfinite(float(n)) and float(n) <= fam_min"),
    ("R05", D, "G05': familias: nunca se exige", "return math.isfinite(float(n)) and float(n) < fam_min", "return False"),
    ("R06", D, "G06': sin recuento SÍ se descarta",
     "        if fam_min <= 0 or isinstance(n, bool) or not isinstance(n, numbers.Real):   # H-02: también float o numpy enteros\n            return False",
     "        if fam_min <= 0:\n            return False\n        if isinstance(n, bool) or not isinstance(n, numbers.Real):\n            return True"),
    ("R07", D, "G07'/H-02: solo cuenta un int de Python (un float o un entero de numpy pasan)",
     "isinstance(n, bool) or not isinstance(n, numbers.Real):   # H-02", "isinstance(n, bool) or not isinstance(n, int):   # H-02"),
    ("R08", D, "G30': se compara con un 2 fijo en vez de con familias_min", "return math.isfinite(float(n)) and float(n) < fam_min", "return math.isfinite(float(n)) and float(n) < 2"),
    ("R09", D, "H-02: un recuento no finito descarta", "return math.isfinite(float(n)) and float(n) < fam_min", "return not math.isfinite(float(n)) or float(n) < fam_min"),
    ("R10", D, "H-03: vuelve el `or {}` (0, '', [] y False se aceptan)", "    upp = {} if upp is None else upp\n", "    upp = upp or {}\n"),
    ("R11", D, "H-06: el motivo vuelve a redondear a dos decimales", "    return corto if float(corto) < umbral else f\"{valor:.8g}\"", "    return corto"),
]
vivos = []
for mid, fich, desc, viejo, nuevo in MUT:
    ruta = ej / fich
    original = ruta.read_text(encoding="utf-8")
    if original.count(viejo) != 1:
        print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}", flush=True)
        continue
    try:
        ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t117_gc1.py"], cwd=ej, capture_output=True, text=True)
        ult = (r.stdout + r.stderr).strip().splitlines()[-1][:110]
        print(f"{mid} · {'MUERTO' if r.returncode else 'VIVO  '} · {desc} · {ult}", flush=True)
        if r.returncode == 0:
            vivos.append(mid)
    finally:
        ruta.write_text(original, encoding="utf-8")
print("vivos: " + (", ".join(vivos) or "ninguno"))
