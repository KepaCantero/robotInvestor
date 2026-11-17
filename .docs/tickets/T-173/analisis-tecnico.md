# T-173 · Análisis técnico

## Causa raíz o motivo

INC-T116-03 dejó dos cláusulas del Plan de pruebas V3.0 sin hacer:

- **PB-50.** 12.2 del Documento 0 V5.3 permite bajar solo de «Sí» a «Limitado» un horizonte cuyo acierto es inferior a la referencia ingenua con significación (DM-HLN). El Evaluador solo tenía la degradación de H5 por hitos (`aplicar_degradacion_h5`), así que RF × H2 perdiendo con n = 35 seguía en «Sí».
- **PB-64.** `Evaluador.estado_h5` calculaba los estados (EN_CURSO_CONFORME, DESVIADO, INVALIDADO) y el seguimiento C6 los usaba, pero no se publicaban ni en F6 (esquema de F4, 5.1: «el Evaluador publica en F6 el estado de cada PRG H5») ni en el paquete ni en el informe técnico (prompt del Evaluador, 6.7 bis.4).

## Evidencia

- Antes: `docs/evidencias_pruebas_bloque_a.md`, filas PB-50 y PB-64 «Superada en parte», con los huecos en «No comprueba».
- Después: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-50` y `--pb PB-64` → «Superada».

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`:
    - `_p31_ya_movida` y `_bajar_a_limitado`: la regla de un escalón por celda y trimestre y la escritura AJU- (F6) + CFG- de P-31 y de P-30 (F10). Salen tal cual de `aplicar_degradacion_h5`, que ahora las usa: lo que escribe H5 no cambia.
    - `degradacion_dm(as_of)`: por celda clase × H1–H4, con los PRG admisibles resueltos (PA-09), la DM-HLN con `d = pérdida_ref − pérdida_pronóstico` (Brier). Su p unilateral es la de «el pronóstico pierde». Degrada si n ≥ `evaluacion.min_calibrar` y p ≤ `evaluacion.alfa_holm`.
    - `aplicar_degradacion_dm(as_of, run_id)`: solo «SI» → «LIMITADO» en la matriz vigente (F10 con `efectivo_el`, o la tabla 8.3). La evidencia del AJU- lleva la DM-HLN (estadístico, p, h, hipótesis), α, n, n mínima, los Brier y los PRG-.
    - `estado_hito`, `ESTADOS_H5`, `estados_h5_publicables`, `publicar_estados_h5` (entrada `EH5-AAAA-MM-DD` en F6) y `estados_h5_vigentes` (la última EH5- hasta el corte, que es lo que leen los entregables).
    - `ciclo` (C5): llama a la degradación DM (dentro de un try, como la fiabilidad: si falla, deja una incidencia en HA) y a `publicar_estados_h5`. El resultado gana `degradacion_dm` y `estados_h5`.
  - `bloque_a/11_Ejecutor/bloque_a/sintesis.py`: cada hito de una vista H5 lleva su `estado` (enum del esquema). El paquete lleva `x_estados_h5` (ampliación `x_` de la raíz), copiado de la EH5- de F6.
  - `bloque_a/11_Ejecutor/bloque_a/redaccion.py` (informe técnico, dos puntos pequeños): el estado del PRG H5 y de cada hito junto a sus hitos, y en la sección 8 la tabla de PRG H5 abiertos y la de celdas tipo × H5 (tasa y PRG por estado).
  - `bloque_a/11_Ejecutor/tests/test_t173.py` (16 pruebas, nuevo) y `tests/mapa_plan_pruebas.json`: PB-50 y PB-64 pasan a AUTOMATICA con sus pruebas.
  - `bloque_a/11_Ejecutor/tests/test_fase4_huecos.py::test_pb33_…`: con sus datos (dice 0,65 y acierta el 50 % en 120 casos), RV × H3 también pierde con significación. Así que, por 12.2, ahora baja a «Limitado» en el mismo C5 y el RUN- ya no ofrece H3. La prueba afirma esa degradación y que ninguna vista publicada de RV lleva probabilidad. Lo que pide PB-33 (revocación, alerta y ninguna probabilidad) sigue afirmado igual. Antes la prueba miraba solo las vistas H3, que ahora no existen.
  - `bloque_a/11_Ejecutor/README.md`, `docs/incidencias.md` (INC-T173-01 y la nota en INC-T116-03), y la deuda técnica (fila T-173).
- **Decisiones y desviaciones del plan:** ninguna desviación. Lo `[PROPUESTO]` va en INC-T173-01: α sin Holm, n mínima, pérdida y h, alcance (solo «Sí» → «Limitado», sin proponer nada desde «Limitado»), prefijo EH5- y publicación por `x_estados_h5`.
- **Límites conocidos:**
  - La degradación corre en cada C5, no solo en la revisión mensual (como la de H5).
  - Los H5 congelados en un RUN- salen en la EH5- del C5 siguiente: el C5 corre antes del análisis.
  - El informe visual y el CT-19 no llevan los estados.
  - En los datos sintéticos del ciclo mock por defecto (perfil DIV) no hay H5 ni celdas que pierdan: el ciclo de la CLI no cambia.
- **Comandos exactos para probarlo:**
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t173.py`
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-50` y `--pb PB-64`
  - Mutantes propios: `cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-173/mutantes.py .`. 14 mutaciones, todas muertas (`pruebas.md`).

## Ronda r02 (QA r01 NO APTO)

Rebasada sobre `origin/develop` (`375d24b`, con T-165 y T-171). El único conflicto estaba en la deuda técnica y se resolvió conservando los dos lados: las filas T-171 y T-172 de develop y la T-173.

- **H-01 (alta), muestra de PA-03.** Cambios en `degradacion_dm`:
  - toma los conglomerados por fecha de resolución (`_fechas_conglomerado`); sin fechas, no evalúa;
  - calcula la n_eff de Kish (`ev.n_efectiva`) y exige n_eff ≥ `evaluacion.min_calibrar` y al menos `_min_conglomerados()` fechas distintas;
  - calcula la DM-HLN sobre la serie de medias de d por fecha, en orden de fecha, y no por PRG;
  - lleva `n_eff`, `conglomerados` y `n_conglomerados` (el de la DM) a la evidencia del AJU-.

  En el fijo de las pruebas, cada PRG tiene ahora su propia fecha de resolución. Hay regresiones para §4 (una semana: un conglomerado), §4b/§12 (61 conglomerados en los que gana: p = 0,99999), sin fechas, con 9 conglomerados y con n = 60 y n_eff < 30.
- **H-02 (media), escritura transaccional.**
  - `_bajar_a_limitado` construye las tres entradas antes de escribir ninguna.
  - Si una escritura en F10 falla: revierte en F10 el CFG- de P-31, si llegó a escribirse (`revierte_a` y la matriz anterior); deja el AJU- en `ANULADO` (`aplicado_en_produccion: False`, `cfg_p31_revertido`, motivo); y relanza la excepción.
  - `_p31_ya_movida` ignora los ANULADO. Así el reintento degrada (§10).
  - Vale también para H5, que comparte el código.
- **H-03 (media), revisión mensual con Holm.**
  - `aplicar_degradacion_dm` es la revisión mensual de PB-50 (paso 2). La hace el primer C5 de cada mes natural, que deja `RDM-AAAA-MM` en F6 (celdas, p, umbrales, motivos y ajustes). Con ese registro, el resto de C5 del mes no evalúa.
  - Si la revisión falla, no queda registro y se repite en el C5 siguiente; así el reintento de H-02 puede ser en el mismo mes.
  - Holm escalonado (`ev.holm`, α = `evaluacion.alfa_holm`) entre las celdas que pueden bajar: muestra suficiente y «Sí» en la matriz vigente. Una celda en «Limitado» o «No» ya no es «degradable» y queda fuera de la familia, con su motivo.
  - No hay número nuevo: la periodicidad «mensual» sale de PB-50 y de EVAL-F19, y el primer C5 del mes es `[PROPUESTO]` (INC-T173-01, con las tasas).
- **H-04 (baja), variante de PB-33.** `test_fase4_huecos.py` saca la preparación de PB-33 a `_pb33_revision_y_run` y añade `test_pb33_con_la_degradacion_dm_neutralizada_…`, con la afirmación original sobre las vistas H3. Está citada en el mapa (PB-33).
- **Observación §8 de la QA.** Una celda con una referencia o una probabilidad ausente deja de abortar la revisión de las demás: esa celda queda con su motivo.
- **Desviación:** la r01 decía «corre en cada C5»; ahora es mensual. El segundo control de «Sí» dentro de `aplicar_degradacion_dm` se ha quitado, porque ya lo filtra la familia de `degradacion_dm` (el mutante que lo quitaba era equivalente).
- **Límites:**
  - Con una sola celda en la revisión, Holm es la prueba a α, y las miradas mensuales sobre datos acumulados dan unas tasas falsas de 12,8 % por trimestre y 20,4 % por año (`r02_tasa_falsa.py`). El Anexo A no da un gasto de α entre miradas.
  - Los RDM- se escriben aunque no haya celdas: es el registro de que la revisión se hizo.
- **Comandos de la r02:**
  - Ataques del revisor, sección a sección: `cd bloque_a/11_Ejecutor && PYTHONPATH=. ../../.venv/bin/python ../../.docs/tickets/T-173/r02_ejecutar_ataques_r01.py [--fechas-distintas]`.
  - Tasas falsas: `.venv/bin/python .docs/tickets/T-173/r02_tasa_falsa.py` (≈ 3 min).

## Ronda de cierre de la QA r02 (APTO con dos bajos)

- **H-05.** Al revertir el CFG- de P-31, `_bajar_a_limitado` escribía en la reversión la `methodology_version` de `comun`, y eso anunciaba un cambio de versión que no llegó a ocurrir. Ahora la reversión lleva `{"de": mv["de"], "a": mv["de"]}`. La prueba `test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31` lo afirma.
- **H-06.** Decisión del operador por delegación del 17-11-2026, opción (b). En `degradacion_dm`:
  - La familia de Holm de la revisión mensual es fija: todas las celdas H1–H4 en «Sí» de la matriz vigente del bloque (32 en la tabla 8.3; `HORIZONTES_DM`). Las celdas que no se pueden evaluar entran con p ausente, que `ev.holm` trata como no rechazable.
  - Una sola celda evaluable tiene ahora un umbral de α/32.
  - No hay ningún número nuevo.
  - Se añade la prueba `test_pb50_cierre_h06_la_familia_es_fija_y_cuenta_las_celdas_sin_muestra`. La de Holm se rehace: p = 0,061 ya no degrada sola.
  - Se añaden los mutantes M25 (H-05) y M26 (H-06).
  - El `type: ignore[arg-type]` de `ev.holm` está justificado en la propia línea: `holm` acepta p ausentes, aunque su firma diga `float`.
- **Efecto en PB-33.** Con la familia fija, RV × H3 (p ≈ 0,05) ya no supera el umbral de la revisión y sigue en «Sí». `test_pb33_…` vuelve a afirmar lo original sobre las vistas H3: que no faltan y que no llevan probabilidad. Además comprueba en la RDM- que la p supera el umbral. La variante con la degradación neutralizada (H-04) sigue en la suite.
- **Tasas y potencia:** en INC-T173-01 y en `pruebas.md`. La familia fija cuesta mucha potencia: una celda que pierde con σ = 0,18, sola en la revisión, se degradaba el 42,5 % de los años con α entero y ahora el 1,4 %. Es la contrapartida de bajar las falsas de 22,4 % a 0,3 % al año.
