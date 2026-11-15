> **Número renumerado (15-11-2026).** Este ticket del Bloque A se abrió como T-133, pero otra sesión usó T-133 para los hallazgos del banco de medida (T-94) y lo subió antes. El ticket del Bloque A sigue en **`.docs/tickets/T-136/`**; lo de esta carpeta es la copia antigua y no se actualiza (de `.docs/` no se borra nada: lo viejo se marca).

# T-133 · Análisis técnico

- `contratos.py`: `ESTRUCTURA_BBAN`, `RE_BBAN`, `BBAN_NUMERICO` (derivado), `LETRAS_GRUPO_MAX`, `_bban_plausible` (estructura del país, ninguna palabra de más de 4 letras, ninguna cifra suelta en un grupo intermedio), `_misma_caja` y, en `tarjetas_en_texto`, `GRUPOS_FILA_DE_TABLA`.
- Las estructuras son datos de un estándar (registro ISO 13616 de SWIFT), no umbrales. Una prueba comprueba que cada una suma la longitud de su país.
- El banco de IBAN de la r01 de T-123 (`r01_01_banco_iban_tarjetas.py`) genera los «válidos» con un BBAN solo de cifras en los 42 países; los 11 cuya estructura pide letras (BG, BR, GB, GI, IE, IT, LV, MT, NL, RO, SM) ya no se detectan con ese BBAN, que no es un IBAN real. Sus ejemplos publicados sí se detectan.
- `estimar_coste_ciclo_a.py`: `estimar(…, factor_tokens, continuaciones)`; el margen está en `config/precios_anthropic.yaml` con su origen.
