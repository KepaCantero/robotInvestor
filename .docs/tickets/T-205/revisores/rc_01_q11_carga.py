"""Ronda de cierre de la QA r01 de T-205 (revisor): la prueba determinista de la transacción
(`test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion`) con la máquina cargada. Arranca N procesos que queman CPU y
ejecuta la prueba K veces con el código tal cual (debe pasar siempre) y K veces con el mutante Q11 (debe fallar siempre).
Reescribe `seguimiento.py`: ejecútese en una copia que no use nadie más.
Uso (desde bloque_a/11_Ejecutor de esa copia): ../../.venv/bin/python <ruta>/rc_01_q11_carga.py . [K] [N]"""
import multiprocessing as mp
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
K = int(sys.argv[2]) if len(sys.argv) > 2 else 15
N = int(sys.argv[3]) if len(sys.argv) > 3 else 6
PRUEBA = "tests/test_t205_clase_seguimiento.py::test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion"
VIEJO = ("        with b.almacen._transaccion():\n            previas = b.almacen.leer(\"HA\", filtro=lambda e: e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"\n"
         "                                     and e.get(\"campo_afectado\") == \"clase\" and all(e.get(k) == v for k, v in clave.items()))\n")
NUEVO = ("        previas = b.almacen.leer(\"HA\", filtro=lambda e: e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"\n"
         "                                 and e.get(\"campo_afectado\") == \"clase\" and all(e.get(k) == v for k, v in clave.items()))\n"
         "        with b.almacen._transaccion():\n")


def quemar():
    x = 0
    while True:
        x = (x * 31 + 7) % 1000003


def veces(k):
    ok = 0
    for _ in range(k):
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", PRUEBA], cwd=EJ, capture_output=True, text=True)
        ok += r.returncode == 0
    return ok


ruta = EJ / "bloque_a/seguimiento.py"
original = ruta.read_text(encoding="utf-8")
assert original.count(VIEJO) == 1
quemadores = [mp.Process(target=quemar, daemon=True) for _ in range(N)]
for q in quemadores:
    q.start()
try:
    bien = veces(K)
    ruta.write_text(original.replace(VIEJO, NUEVO), encoding="utf-8")
    mut = veces(K)
finally:
    ruta.write_text(original, encoding="utf-8")
    for q in quemadores:
        q.terminate()
print(f"con {N} quemadores: código tal cual {bien}/{K} pasan; mutante Q11 {K - mut}/{K} mueren")
sys.exit(0 if bien == K and mut == 0 else 1)
