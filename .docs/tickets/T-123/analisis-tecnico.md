# T-123 · Análisis técnico

## Motivo

T-120 y T-122 dejaron declarado como límite que R8 no detectaba números de tarjeta ni IBAN de otros países. Era uno de los huecos menores de la deuda que el operador pidió completar el 14-11-2026.

## Implementación

- `contratos.py`: `LONGITUD_IBAN`, `RE_CANDIDATO_IBAN`, `RE_CANDIDATO_TARJETA`, `_iban_valido`, `ibanes_en_texto`, `_luhn`, `_red_de_tarjeta`, `tarjetas_en_texto`, y una línea en `secretos_en_texto`.
- Decisiones `[PROPUESTO]` (INC-T123-01): la tabla de longitudes es un dato de un estándar (ISO 13616), no un umbral, y cubre 42 países; un IBAN de un país que no está en ella no se reconoce. Las redes de tarjeta son las corrientes; una de otra red o de longitud no estándar, no.
- Límites: tarjeta con separadores de más de un carácter o en grupos con puntos; IBAN extranjero en un formato con más de dos separadores seguidos; tarjetas de redes locales.
- El Bloque A Forex tiene su propia copia de `RE_SECRETO` y no se toca (un bloque por tarea; el Forex no se integra).
- Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t123_r8_iban_y_tarjetas.py`.
