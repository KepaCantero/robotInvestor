# T-120 · Análisis técnico

## Causa raíz o motivo

- **IBAN:** `contratos.RE_SECRETO` solo reconocía `ES` seguido de 22 cifras juntas. Un IBAN se escribe casi siempre en grupos de cuatro, y así pasaba el filtro: un CT-04 con el IBAN en el comentario se aplicaba y el dato quedaba en `F5_historial_analisis.jsonl`.
- **Lecciones:** el máximo de 10 del 12.3 del Documento 0 estaba como valor por defecto de un argumento (`max_n: int = 10`), contra la regla 2.

## Evidencia

`.docs/tickets/T-116/revisores/r01_01_filas_automaticas_a_mano.py`, apartado PB-21: «solo IBAN con espacios: ADMITIDO (estado APLICADA)… valor en archivos: F5». Tras la corrección: rechazado con `DatosSensibles`, una incidencia SEGURIDAD y cero coincidencias.

## Implementación

- Archivos cambiados y por qué: `bloque_a/11_Ejecutor/bloque_a/contratos.py` (patrón del IBAN), `bloque_a/evaluador.py` (`lecciones_vigentes`), `config/por_defecto.yaml` (`aprendizaje.lecciones_por_encargo`), `tests/test_t120_r8_y_lecciones.py`.
- Decisiones tomadas: un solo separador entre grupos (dos espacios seguidos no se detectan: declarado); no se añaden tarjetas ni IBAN de otros países.
- Límites conocidos: un IBAN partido de otra forma (grupos de dos, saltos de línea, letras intercaladas) no se detecta; el Forex conserva el patrón antiguo.
- Comandos exactos para probarlo, desde `bloque_a/11_Ejecutor`: `python -m pytest -q tests/test_t120_r8_y_lecciones.py`.
