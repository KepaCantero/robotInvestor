# Handoff · T-184

Claude revisa los criterios de aceptación del README y reproduce las pruebas con Python 3.12.

`.venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests/test_t184_altas.py`

La entrada exige fecha de publicación para las altas nuevas. Las fichas antiguas sin fecha quedan detrás de las fechadas a igual calidad. Usar la configuración de la instancia para indicar el directorio operativo.

## Ronda r02

Ejemplo de una entrada de F9 para `alta-referencias --archivo F9 --json lote.json` en la configuración de prueba:

```json
[{"id":"RF-9000","tematica":"TF-04","titulo":"Observación de ejemplo","url":"https://example.org/observacion","fecha_publicacion":"2026-01-10","tipologia":"primaria","puntos":[20,10,15,15,10,10,10]}]
```

Usar las opciones globales `--estado` y `--as-of` antes del subcomando para seleccionar la instancia y la fecha histórica. Ejecutar `.venv/bin/python .docs/tickets/T-184/mutantes.py` para revisar las 14 hipótesis originales sobre el código reorganizado y las tres adicionales. La observación O-01 sobre la admisión de enlaces pendientes en PS1 sigue remitida al coordinador.
