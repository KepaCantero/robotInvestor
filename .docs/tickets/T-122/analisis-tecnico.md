# T-122 · Análisis técnico

## Causa raíz

- **IBAN:** el patrón de T-120 solo admitía un espacio ASCII, un punto o un guion entre grupos de cuatro. Un IBAN copiado de una web o de un PDF trae espacios duros, y el formato impreso agrupa 4 4 2 10.
- **Lecciones:** el valor se convertía con `int(...)` sin validar.
- **Conjuntos:** `json.dumps(default=str)` vuelca un conjunto como su representación de Python, con comillas simples, que no casa con los patrones de R8.

## Implementación

- `contratos.py`: `\b[Ee][Ss]\d{2}(?:[\s.\-]{0,2}\d){20}\b`. Admite cualquier agrupación porque exige exactamente 20 cifras tras las dos de control; tres separadores seguidos ya no se detectan (declarado).
- `evaluador.py`: `lecciones_por_encargo(cfg)` y `LECCIONES_POR_ENCARGO_MAX = 10` (12.3 del Documento 0).
- `llm.py`: `_json_por_defecto` y segunda pasada en `contenido_sensible` solo cuando hay conjuntos (el recorrido de hojas ya los visita, así que no añade coste a lo que no los tiene).
- Pruebas ajustadas: en `test_t120_r8_y_lecciones.py` dejan de figurar como «legítimos» el IBAN con dos espacios y el escrito en minúsculas, que ahora se detectan.
- Límites conocidos: IBAN de otros países y números de tarjeta (huecos menores de la deuda, se tratan aparte); tres o más separadores seguidos; la regla de los romanos (INC-T122-01).
- Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t122_hallazgos.py tests/test_t120_r8_y_lecciones.py tests/test_t113_deuda.py`.
