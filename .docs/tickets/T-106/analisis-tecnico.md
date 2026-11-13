# T-106 · Análisis técnico

## Implementación

- **Fichas.** Una función por ficha, con la interfaz de los manejadores del Motor: `fn(ent, params) -> (resultado, limitaciones)`. Las entradas van en línea (`valores`) o como series por rol. Lo que falta o es incoherente lanza `ErrorFicha`, que el Motor traduce en RECHAZADO con DATOS_INSUFICIENTES. Las advertencias fijas de cada ficha («Supuestos y limitaciones») van en `resultado["advertencias"]`; en TCV, el Motor las saca de las limitaciones (`_advertencias_aparte`).
- **Números.** Solo los de cada ficha («Parámetros», en `PARAMETROS_POR_DEFECTO` con la ficha citada) y las convenciones del Catálogo. Donde la ficha no fija un nivel, se toma de otra ficha del Catálogo y se declara (INC-T106-01).
- **Manda el Catálogo.** `madurez_catalogo()` lee la última columna de la tabla del §2 (81 filas). `servible(f)` exige que haya código, que la ficha no esté en `DOCUMENTADAS_CON_CODIGO`, que el Catálogo la dé por IMPLEMENTADO o VALIDADO y, para GARCH, que esté `arch`. Antes de promover, el conjunto servible coincidía exactamente con las 14 del Catálogo.
- **Casos de control.** `Motor.verificar_casos_control()` ejecuta cada caso dos veces (deben coincidir) y escribe una entrada CASOS_CONTROL en RC por ficha. No depende de la madurez, que es justo lo que permite promover.
- **Promoción.** `.docs/scripts/promover_fichas_catalogo.py --aplicar` corrió con las 21 fichas, que superaron sus 50 casos. Cambió 21 filas, 21 líneas de madurez y el §1.3. Después se re-congeló el corpus con `tools/corpus_integridad.py --update` (695 archivos; cambia la huella del Catálogo).

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

## Ronda r02 (QA r01 NO APTO)

**Motor (`servicio.py`).**
- **H-02:** una excepción de una ficha que no es `ErrorFicha` (`ValueError`, `TypeError`, `ArithmeticError`, `LinAlgError`…) se rechaza como DATOS_INSUFICIENTES y queda en RC. En las fichas de T-106, una cifra no finita en el resultado también se rechaza.
- **H-04:** el Catálogo se lee de `rutas.raiz_paquete` de la configuración (`Motor.raiz`).
- **H-05:** bytes que no son UTF-8 dan un Catálogo vacío (no se sirve nada).
- **H-06:** solo cuenta la tabla del índice (§4), y la lectura se cachea por ruta y fecha de modificación.
- **H-12:** el rechazo de VOL-GARCH-001 sin `arch` dice que falta la dependencia.
- **H-13:**
  - el `code_ref` del artefacto en RC es el módulo real de la función. Para las 14 fichas anteriores apunta ahora a `servicio`, que es donde están sus envolturas;
  - la aserción con `or` se quita;
  - los casos eran 50, no 53.

**Fichas (los tres agentes, en sus módulos).**
- **H-01 (MON-EXP-001):** el bootstrap resuelve todos los tramos a la vez por mínimos cuadrados con todos los nodos y exige reproducirlos dentro de la tolerancia. Rechaza la curva que no identifica un tramo por reunión, la que no tiene contraste (sistema justo) y la que el redondeo de las cotizaciones movería un incremento Δ. Se añaden H-09 (la lectura del tipo vigente, en el docstring y con prueba) y H-10.
- **H-02:** validación explícita de entradas (tipos, finitud, longitudes y dominios) en las 21 fichas, y una envoltura por módulo que convierte lo que se escape en `ErrorFicha`. TCV-TP-001 acota los plazos a 1–120 meses (la ficha: vencimientos de 1 a 10 años); TCV fija los umbrales de rechazo, que ya no se pueden bajar por parámetro.
- **H-03:** las advertencias fijas de FON y DER pasan a `resultado["advertencias"]`. FON-LEV-001 sigue con una limitación, porque su simulación no se sirve.
- **H-07 (IDX-REL-001):** exige historia mensual.
- **H-08:** casos de control reforzados con datos que no anulan los términos (r ≠ 0, K₀ ≠ F, pesos distintos). Pasan de 50 a 66, y los mutantes de `r01_04` mueren.
- **H-11:** las fechas numéricas se rechazan.

**Nuevas decisiones de método (INC-T106-01).**
- En MON-EXP-001, la precisión declarada de las cotizaciones relaja la tolerancia por nodo, y el umbral de identificación es el incremento Δ de la ficha. Una curva cotizada plana en tipos simples se rechaza.
- En TCV, los rangos de los parámetros salen de las fichas citadas (FIR-CARRY-001, RISK-VAR-001).
