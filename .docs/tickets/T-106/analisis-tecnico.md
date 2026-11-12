# T-106 · Análisis técnico

## Implementación

- **Fichas.** Una función por ficha, con la interfaz de los manejadores del Motor: `fn(ent, params) -> (resultado, limitaciones)`. Las entradas van en línea (`valores`) o como series por rol. Lo que falta o es incoherente lanza `ErrorFicha`, que el Motor traduce en RECHAZADO con DATOS_INSUFICIENTES. Las advertencias fijas de cada ficha («Supuestos y limitaciones») van en `resultado["advertencias"]`; en TCV, el Motor las saca de las limitaciones (`_advertencias_aparte`).
- **Números.** Solo los de cada ficha («Parámetros», en `PARAMETROS_POR_DEFECTO` con la ficha citada) y las convenciones del Catálogo. Donde la ficha no fija un nivel, se toma de otra ficha del Catálogo y se declara (INC-T106-01).
- **Manda el Catálogo.** `madurez_catalogo()` lee la última columna de la tabla del §2 (81 filas). `servible(f)` exige que haya código, que la ficha no esté en `DOCUMENTADAS_CON_CODIGO`, que el Catálogo la dé por IMPLEMENTADO o VALIDADO y, para GARCH, que esté `arch`. Antes de promover, el conjunto servible coincidía exactamente con las 14 del Catálogo.
- **Casos de control.** `Motor.verificar_casos_control()` ejecuta cada caso dos veces (deben coincidir) y escribe una entrada CASOS_CONTROL en RC por ficha. No depende de la madurez, que es justo lo que permite promover.
- **Promoción.** `.docs/scripts/promover_fichas_catalogo.py --aplicar` corrió con las 21 fichas, que superaron sus 53 casos. Cambió 21 filas, 21 líneas de madurez y el §1.3. Después se re-congeló el corpus con `tools/corpus_integridad.py --update` (695 archivos; cambia la huella del Catálogo).

## Qué queda fuera o como dato de entrada (por ficha)

Resumen de los informes de los tres agentes:
- **MON-EXP-001:** el ajuste de convexidad de los futuros a más de 1 año y el tipo esperado del día anterior (para las sorpresas), como dato.
- **MON-REAL-001:** el tipo real neutral, como dato con fuente.
- **IDX-ERP-001:** SCN-H-001 en H4 y la segunda vía por ACC-ERP-001 (DOCUMENTADO), con limitación.
- **IDX-REL-001:** la diferencia de E[R] y las revisiones de BPA, como datos.
- **IDX-REB-001:** los activos indexados, como dato con fuente.
- **FON-DISC-001:** los catalizadores, como dato.
- **FON-LEV-001:** sin la simulación SIM-MC-001 (DOCUMENTADO), con limitación.
- **DER-VRP-001:** la réplica libre de modelo, solo para hoy.
- **DER-ROLL-001:** en bonos, sin cupón corrido ni opción de entrega.
- **TCV-SLOPE-001:** los regresores, como datos con vintage.
- **TCV-BEI-001:** el modelo afín, como dato con fuente.
- **TCV-CDS-001:** el DV01 con duración continua aproximada.
- **TCV-VIXTS-001:** las rentabilidades históricas de la exposición, como dato.
- **TCV-TP-001:** ACM implementado y verificado con una curva afín sintética (identidad exacta y error de ajuste de unos 1e-11 pb). En ejecución, un RMSE ≥ 5 pb lo rechaza; las alternativas (serie publicada y encuesta) se piden por `metodo`.

## Límites

- Solo datos sintéticos: las fichas están IMPLEMENTADO («implementado, no validado»), no VALIDADO.
- La copia `.docx` del Catálogo sigue diciendo DOCUMENTADO para estas 21 (las `.docx` no se editan; manda el `.md`).
- Las decisiones de INC-T106-01 son `[PROPUESTO]`.

## Comandos

```bash
.venv/bin/python -I .docs/scripts/promover_fichas_catalogo.py            # informe sin escribir
```

```bash
.venv/bin/pytest -q bloque_a/11_Ejecutor/tests/test_t106_motor.py bloque_a/11_Ejecutor/tests/test_fase1_mon_idx.py bloque_a/11_Ejecutor/tests/test_fase1_fon_der.py bloque_a/11_Ejecutor/tests/test_fase1_tcv.py
```
