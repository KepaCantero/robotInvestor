"""QA r02 de T-196: tras `reconciliar` (otro día), ¿`enviar_pendientes` con el as_of de la consulta manda otra final?
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r02_final_doble.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))
import pandas as pd  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a import respuesta_final  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

T0 = pd.Timestamp(f"{AS_OF}T09:00", tz="Europe/Madrid")
b = nuevo_bloque(tempfile.mkdtemp(), cargar_universo(RUTA_UNIVERSO_EJEMPLO))
q = b.consulta("¿Qué opinas de las divisas frente a la renta fija?", as_of=AS_OF, encolar_escalado=True, instante=T0)
b.cola.tomar(T0 + pd.Timedelta(minutes=1))      # nadie la sirve: huérfana en este proceso
for desfase in (pd.Timedelta(hours=1), pd.Timedelta(days=1)):
    pass
rec = b.cola.reconciliar(q["peticion_cola"], "revisado", T0 + pd.Timedelta(days=1))
print("final de reconciliar:", rec["respuesta_final"]["msg_id"], rec["respuesta_final"]["repetido"])
for as_of in (AS_OF, None):
    p = respuesta_final.enviar_pendientes(b, as_of)
    print(f"enviar_pendientes(as_of={as_of}):", [(f["msg_id"], f.get("repetido")) for f in p])
finales = [m for m in b.mensajeria.registro if m.get("contrato") == "CT-03" and (m.get("respuesta_final") or m.get("tipo_mensaje") == "RETORNO")]
print("mensajes CT-03 en el registro:", len([m for m in b.mensajeria.registro if m.get("contrato") == "CT-03"]))
print("respuesta_final en F5:", b.almacen.estado("F5")[q["query_id"]].get("respuesta_final", {}).get("msg_id"))
