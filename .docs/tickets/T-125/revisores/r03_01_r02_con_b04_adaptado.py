"""QA r03 de T-125 (revisor sin contexto): vuelve a ejecutar `r02_01_ataques_ciclo.py` del revisor de la r02 SIN cambiar su
fichero. Su bloque B04 llamaba a `_fecha_de_calendario("now")` esperando una fecha; desde la r03 esa llamada lanza
`ValueError` (falla cerrado, que es lo que pedía H-10), y el script se paraba ahí. Aquí se sustituye solo B04, en memoria, por
una versión que comprueba que cada palabra relativa o formato libre se rechaza; B01–B03 y B05–B12 se ejecutan tal cual.

Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r03_01_r02_con_b04_adaptado.py
"""
import re
import sys
from pathlib import Path

ORIGINAL = Path(__file__).with_name("r02_01_ataques_ciclo.py")
fuente = ORIGINAL.read_text(encoding="utf-8")
m = re.search(r"^# -+ B04 .*?^(?=# -+ B05 )", fuente, flags=re.MULTILINE | re.DOTALL)
assert m, "no encuentro el bloque B04 del script de la r02"

B04_NUEVO = '''# ------------------------------------------------------------------ B04 (adaptado en la r03) · palabras relativas y formatos libres
from bloque_a.evaluador import _fecha_de_calendario  # noqa: E402

lect = {}
for t in ("now", "today", "tomorrow", "1/7/2026", "July 1 2026", "2026", "2026-07", "20260701", "2026/07/01", "01-07-2026"):
    try:
        lect[t] = "LEÍDA " + str(_fecha_de_calendario(t).date())
    except ValueError:
        lect[t] = "rechazada"
hoy_maquina = pd.Timestamp.now().date()
m_hoy = motivo_pronostico_fuente_no_registrable({**base, "fecha_emision": "today", "fecha_objetivo": str(hoy_maquina + pd.Timedelta(days=10))},
                                                F9A, str(hoy_maquina + pd.Timedelta(days=3)), refs)
print(f"B04 · lecturas {lect} · emisión «today» con registro a +3 días y objetivo a +10: "
      f"{'REGISTRABLE' if m_hoy is None else 'rechazada: ' + m_hoy}")

'''
sys.argv = [str(ORIGINAL)]
codigo = fuente[:m.start()] + B04_NUEVO + fuente[m.end():]
exec(compile(codigo, str(ORIGINAL) + " (B04 adaptado)", "exec"), {"__name__": "__main__", "__file__": str(ORIGINAL)})  # noqa: S102
