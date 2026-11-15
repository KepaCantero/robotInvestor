# T-130 · Análisis técnico

- `contratos.py`: `RE_GRUPOS_TARJETA` (separador de un carácter; sin letra, cifra ni «_» pegados; sin cifra y punto o coma delante), `BBAN_NUMERICO`, `LETRAS_BBAN_MAX`, `SIN_LIMITE_DE_LETRAS`, `_bban_plausible` e `ibanes_en_texto` (letras pegadas al final; bucle por índice).
- Las listas de países salen del registro ISO 13616 de SWIFT (formato del BBAN de cada país): es un dato de un estándar, no un umbral.
- Límites que quedan (INC-T123-01): cuatro grupos de cuatro cifras al azar con Luhn y prefijo de red (forma de tarjeta, también una huella de 16 hex que sea solo cifras, 1 de cada 100 000); una tarjeta con dos espacios entre grupos, con puntos o en varias líneas; un número de 16 cifras seguido de una parte decimal se marca.
