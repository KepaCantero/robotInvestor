# T-180 · Análisis técnico

## Causa raíz o motivo

Hallazgos de la QA r01 de T-163 (`.docs/tickets/T-163/qa.md`, veredicto APTO):

- **H-01 (media).** `motivo_sin_reejecucion` (lo que miran CT-04, la emisión, `certificados_vigentes` y la revisión) ataba el CERT-
  a su soporte (método, entradas, orden, exclusividad, cifras), pero no miraba si ese soporte **cumple el criterio** del certificado
  ni quién lo pidió. Con los permisos del Evaluador (Motor y F6 como AG-20), el soporte y la CT-10 de las entradas reales de una
  celda de habilidad débil (BSS 0,053, IC [−0,064; 0,16], p de DM 0,20) daban un PROPUESTO que CT-04 ponía en vigor, y la revisión lo
  mantenía (solo revoca por deterioro: BSS ≤ 0 o ECE ≥ `ece_revocacion`).
- **H-02 (baja).** La clave de la caché del Motor (`clave_hash(ficha, versión, datos, parámetros, semilla, perfil, corte)`) lleva la
  clase (el Motor la pone en `parametros.clase`) pero no el horizonte. Dos celdas H2 y H3 con las mismas entradas: la segunda
  recibía el soporte de la primera, su borrador no pasaba «no es un servicio FC-EVAL-001 de la celda RF|H2» y no se certificaba nunca
  (fallaba cerrado, con una incidencia Material en cada revisión).
- **H-03 (baja).** (a) `test_umbral_de_revocacion_ece_sale_de_la_configuracion` (t53) y `test_pa10_revocar_y_retirar_siguen_siendo_automaticos`
  (t66) afirmaban que se revoca, no por qué: con el ayudante roto (N05) seguían pasando, revocado por «sin re-ejecución». (b) Ninguna
  prueba del ticket mataba N03 (muestra efectiva), N04 (Brier de referencia) ni N07 (lote con dos PROPUESTO de una celda).

## Evidencia

- `.docs/tickets/T-163/revisores/r01_01_ataques.py` en la base (`192499e`): 2 fallan (`test_h01_ct04_no_aprueba_un_certificado_cuyas_cifras_no_cumplen_el_criterio`
  y `test_h02_dos_horizontes_con_las_mismas_entradas_se_certifican_los_dos`), 29 pasan.
- Con T-180, pasan las dos y fallan, por diseño, tres que forjan un certificado «válido por sí mismo» con `_fabricadas()`: esas
  entradas no cumplen el criterio (ECE 0,10 > q90 del nulo 0,04, comprobado con `ev.criterio_certificado`), y CT-04 ahora lo mira.
- Resultados de las pruebas, regresiones y mutantes en `pruebas.md`.

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`:
    - `motivo_sin_reejecucion`: tras las comprobaciones de T-160 y T-163 (sin cambiar su orden ni sus mensajes), (1) después de
      la celda del soporte, que el soporte lo pidió AG-20 («CALC-… no lo pidió el Evaluador (AG-20), sino …»); (2) al final, tras las
      cifras, `criterio_desfavorable(payload, holgura_tolerancia(tol, pasos), n_cert, ece_max, alfa_holm)` sobre el `payload` del
      soporte, con `pasos` = 0 si la CT-10 citada es «SI» (entonces es `criterio_certificado` tal cual) y 1 si es DENTRO_TOLERANCIA
      (la materialidad de la propuesta). Si las cifras no tienen forma de número, el criterio no se puede aplicar y el certificado no
      vale (TypeError, ValueError o AttributeError capturados: no lanza).
    - `_umbrales_certificado()` (nuevo): `evaluacion.min_certificar`, `evaluacion.ece_max` y `evaluacion.alfa_holm`, leídos en un sitio
      para la revisión y para la comprobación del soporte.
    - `revisar_certificados`: lee los umbrales de `_umbrales_certificado()` y aplica Holm también con una sola celda candidata
      (`alfa_k = umbrales[…]`, antes `None` con una celda).
    - `_verificar_reejecucion`: `"horizonte": k[1]` en los parámetros de la petición FC-EVAL-001 (antes de `tasa_base`, para no tocar
      la línea que muta T11 de T-163).
    - Docstrings de `certificados_vigentes`, `motivo_sin_reejecucion` y `revisar_certificados`.
  - `bloque_a/11_Ejecutor/tests/conftest.py`: `certificado_con_reejecucion` con 160 pronósticos calibrados (p 0,9 y 0,1 con
    frecuencias exactas 0,9 y 0,1) en 160 fechas hábiles distintas: n_eff 160 ≥ 100, ECE 0, BSS 0,64. La petición lleva `horizonte`.
    El ayudante afirma que su soporte cumple el criterio con los umbrales de la configuración (si alguien lo rompe, lo dice él).
  - `bloque_a/11_Ejecutor/tests/test_t180_hallazgos_t163.py` (nuevo): 27 pruebas.
  - `test_t53_evaluacion_y_almacen.py::test_umbral_de_revocacion_ece_sale_de_la_configuracion`: además de «se revoca», que es por
    deterioro con el umbral de la configuración (`motivo_cambio` acaba en «ECE ≥ 0.0») y que `vigentes_sin_reejecucion` está vacío.
  - `test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos`: la propuesta de MP la escribe el ayudante (con
    su soporte y su CT-10), para que se retire porque la celda ya no cumple el criterio y no por no tener re-ejecución (esa vía la
    cubren las pruebas de T-160); se afirma el motivo de las dos (deterioro; «la celda ya no cumple el criterio»).
  - `.docs/scripts/mutantes_revisor_ampliado.py`: la lista `PRUEBAS` del revisor puede ocupar varias líneas (la de
    `r01_02_mutantes.py` de T-163 ocupa dos y el script no la leía). Fila de la tabla de `.docs/README.md` actualizada.
  - `.docs/tickets/T-180/mutantes_t180.py` (nuevo): U01–U09, un mutante por comprobación nueva.
  - `docs/incidencias.md` (INC-T160-01, ampliada con T-180), `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (fila
    de §4 de la re-ejecución CT-10) y `bloque_a/11_Ejecutor/README.md`.
- **Decisiones tomadas y desviaciones del plan:**
  - **Holm con una sola celda** (agente, por defecto; endurece). CT-04 no puede rehacer Holm (es entre celdas), pero sí su condición
    necesaria, p ≤ α. Para que una celda sola legítima con p > α no quede propuesta y luego rechazada por CT-04 (o con una incidencia
    Material en cada revisión por el borrador de H-03 de T-163), la revisión aplica Holm también con una celda: con una hipótesis es
    la prueba a α. El Anexo A habla de Holm «con varias celdas candidatas» y no dice nada de una; esto es más estricto y hace cierto
    el `holm_superado: true` de todo CERT-. En la práctica no cambia nada: con el IC del BSS por conglomerados > 0 la p de DM-HLN
    (h = 1, sin conglomerados) sale mucho menor que 0,10; la suite completa no cambia ningún resultado. Anotado en INC-T160-01 y en
    §4 de Decisiones.
  - **Materialidad en CT-04.** El plan decía «`criterio_certificado` (o la función que use el Evaluador al proponer)»; se usa
    `criterio_desfavorable`, la de la materialidad, con 0 pasos (idéntica a `criterio_certificado`) o 1 si la CT-10 citada es
    DENTRO_TOLERANCIA. Un legítimo siempre lo pasa: el soporte difiere de las cifras propias `m` en ≤ `holgura(1)`, `m` aguantó al
    proponer el movimiento `holgura(pasos)` y el criterio es monótono en cada cifra; mover el soporte `holgura(1)` más queda dentro
    de `holgura(2)` respecto de `m`.
  - **El horizonte, en la petición y no en la clave del Motor.** Las dos opciones del encargo valían; esta toca solo el cliente que
    lo necesita y no cambia la clave de ninguna otra ficha (ni sus `clave_idempotencia`). CT-04 no exige `parametros.horizonte`: la
    celda del soporte se sigue comprobando con su `horizonte` (que el Motor escribe de la petición); un certificado de T-163 vale si
    cumple el criterio.
  - **Atar las entradas del soporte a los PRG:** no se hace; no sale barato (ver Límites). Se queda en INC-T160-01.
  - Sin cambios en `motor/servicio.py`, `orquestacion.py`, `guias.py`, `herramientas/`, el corpus, los goldens ni lo de las lecciones.
- **Límites conocidos:**
  - Las entradas del soporte no se atan a los PRG resueltos de la celda. Exigiría recalcular `resueltos` y `_entradas_celda` a la
    fecha del soporte en CT-04 y en cada `certificados_vigentes` (síntesis, G3, backtest, diseño V6) con F4 y la configuración
    vigentes: un PRG resuelto tarde o un cambio de configuración (admisibles, contaminación, conglomerados) revocaría un certificado
    legítimo. Con los permisos del Evaluador, unas entradas inventadas que cumplen el criterio siguen pasando CT-04; lo documenta
    `test_limite_declarado_un_soporte_con_entradas_inventadas_que_cumplen_el_criterio_entra`.
  - Holm entre celdas no se re-verifica en CT-04: un soporte con p entre su umbral de Holm y α pasa (solo con los permisos del Evaluador).
  - Un cambio de configuración más estricto (`min_certificar`, `ece_max`, `alfa_holm` más exigentes) revoca en la revisión siguiente
    los VIGENTE cuyo soporte ya no lo cumple. Es lo coherente con «los mismos umbrales» y endurece.
  - Las tres pruebas de `r01_01_ataques.py` de T-163 que forjan con `_fabricadas()` un certificado «válido por sí mismo» fallan por
    diseño; las del ticket cubren lo mismo con datos que cumplen el criterio (N07, segundo certificado de una celda, límite declarado).
- **Comandos exactos para probarlo** (desde la raíz de la copia):

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t180_hallazgos_t163.py tests/test_t163_hallazgos_t160.py tests/test_t160_reejecucion_certificado.py tests/test_t66_evaluacion.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-163/revisores/r01_01_ataques.py      # 3 fallan por diseño
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase4_huecos.py tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py
../../.venv/bin/python tests/goldens_ct.py
cd ../..
.venv/bin/python .docs/tickets/T-180/mutantes_t180.py <copia «…_mut»>
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-163/revisores/r01_02_mutantes.py <copia «…_mut»> tests/test_t180_hallazgos_t163.py
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut»> \
  tests/test_t163_hallazgos_t160.py tests/test_t180_hallazgos_t163.py ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
```

(Cada copia lleva `bloque_a/` entero y `.docs/tickets/T-160` y `T-163`.)
