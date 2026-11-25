"""T-201 r02 (QA r01, H-01): testigo de sensibilidad de la prueba de equivalencia. Lo lanza `equivalencia.sh` tras comparar.

Uso: sensibilidad.py <carpeta de trabajo de equivalencia.sh> <comparar.py> <raiz_nuevo (…/bloque_a)>
Cambia en `r_nuevo` UN valor que no es una ruta ni una latencia, lanza `comparar.py`, que tiene que dar DISTINTO, y lo deshace.
Si alguno da EQUIVALENTE, la comparación normaliza de más (un punto ciego) y el script termina con 1. Los casos de dominio e
instantes son los de `revisores/r02_sensibilidad_equivalencia.py` del revisor, más el estado de F3 y los reintentos de
`consumo.csv` (la columna vecina de la latencia), y las dos latencias, que tienen que dar EQUIVALENTE (lo único que se enmascara).
Un caso cuyo patrón no aparece en la ejecución cuenta como fallo: el testigo no puede quedarse sin probar nada en silencio.
"""
import re
import subprocess
import sys
from pathlib import Path

EQ, COMPARAR, RAIZ_NUEVO = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
F3, F4 = "estado/F3_registro_oportunidades.jsonl", "estado/F4_registro_pronosticos.jsonl"
# (nombre, fichero relativo a r_nuevo, patrón, sustitución, veredicto esperado); se cambia solo la primera aparición
CASOS = [
    ("F3 liquidez", F3, r'"liquidez": "alta"', '"liquidez": "baja"', "DISTINTO"),
    ("F3 estado de una opción", F3, r'"estado": "PROPUESTA"', '"estado": "DESCARTADA"', "DISTINTO"),
    ("F3 dimensión T «duracion» (entrada de HT-03)", F3, r'"duracion": 80', '"duracion": 10', "DISTINTO"),
    ("RC «duracion_sesiones» (resultado del Motor)", "estado/RC_registro_calculos.jsonl", r'"duracion_sesiones": (\d+)',
     '"duracion_sesiones": 1', "DISTINTO"),
    ("F4 «fecha_congelacion»", F4, r'"fecha_congelacion": "(\d{4}-\d{2}-\d{2})T(\d{2})', r'"fecha_congelacion": "\1T23', "DISTINTO"),
    ("F3 fecha con hora", F3, r'(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})', r'\1T23:59:59', "DISTINTO"),
    ("F11 «_ts»", "estado/F11_registro_seguimientos.jsonl", r'"_ts": "(\d{4}-\d{2}-\d{2})T(\d{2})', r'"_ts": "\1T23', "DISTINTO"),
    ("03_peticion.out «timestamp» del acuse", "03_peticion.out", r'"timestamp": "(\d{4}-\d{2}-\d{2})T(\d{2})', r'"timestamp": "\1T23',
     "DISTINTO"),
    ("consumo.csv reintentos (vecina de la latencia)", "bt/consumo.csv", r"(?m)^(RUN-2024-0001,(?:[^,\r\n]*,){11})0,", r"\g<1>1,",
     "DISTINTO"),
    ("04_consulta.out «latencia_s» (se enmascara)", "04_consulta.out", r'"latencia_s": [0-9.eE+-]+', '"latencia_s": 999.0',
     "EQUIVALENTE"),
    ("F5 «tiempo_respuesta_s» (se enmascara)", "estado/F5_historial_analisis.jsonl", r'"tiempo_respuesta_s": [0-9.eE+-]+',
     '"tiempo_respuesta_s": 999.0', "EQUIVALENTE"),
    ("consumo.csv latencia (se enmascara)", "bt/consumo.csv", r"(?m)^(RUN-2024-0001,[^\r\n]*,)[0-9.]+(\r?)$", r"\g<1>999.0\2",
     "EQUIVALENTE"),
]

fallos = []
for nombre, rel, pat, sus, esperado in CASOS:
    f = EQ / "r_nuevo" / rel
    original = f.read_bytes()
    texto = original.decode("utf-8")
    nuevo, n = re.subn(pat, sus, texto, count=1)
    if not n or nuevo == texto:
        print(f"  FALLO {nombre}: el patrón no aparece en la ejecución")
        fallos.append(nombre)
        continue
    try:
        f.write_bytes(nuevo.encode("utf-8"))
        r = subprocess.run([sys.executable, "-I", str(COMPARAR), str(EQ / "r_base"), str(EQ / "r_nuevo"), str(EQ / "base" / "bloque_a"),
                            str(RAIZ_NUEVO)], capture_output=True, text=True, check=False)
    finally:
        f.write_bytes(original)
    ver = "DISTINTO" if r.returncode else "EQUIVALENTE"
    print(f"  {'OK   ' if ver == esperado else 'FALLO'} {nombre}: {ver} (esperado {esperado})")
    if ver != esperado:
        fallos.append(nombre)
print("SENSIBILIDAD:", "puntos ciegos: ninguno" if not fallos else f"FALLA en {fallos}")
sys.exit(1 if fallos else 0)
