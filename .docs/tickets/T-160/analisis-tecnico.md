# T-160 · Análisis técnico

## Causa raíz o motivo

- **PB-32.** El resultado esperado del plan exige para el CERT- una «re-ejecución CT-10 coincidente», y lo mismo EVAL-F05 y el
  punto 5 de §6.6 del prompt del Evaluador; el esquema de F6 (4.3) tiene los campos `curva_fiabilidad` y `reejecucion` (CALC- de
  CT-10). `Evaluador.revisar_certificados` calculaba las cifras con `evaluacion.evaluar_celda` y escribía el certificado sin
  pasar por el Motor: no había artefacto en el Registro de cálculos que re-ejecutar. INC-T116-03 lo dejó «sin tocar» por ser una
  función nueva, y la fila PB-32 de las evidencias quedaba «Superada en parte».
- **D-1 de T-157.** `Evaluador.tasa_base` escribía `"catalog_version": "4.0"` en la entrada RC de RI-TB; el Catálogo vigente es
  V5.0 (`servicio.CATALOG_VERSION`), y una re-ejecución CT-10 usa la versión citada en el artefacto (§1.1 del Catálogo). El
  docstring de `motor/operaciones.py` decía «Catálogo de cálculos V4.0».

## Evidencia

- `grep -rn "catalog_version\|\"4.0\"" bloque_a/11_Ejecutor/tests/` solo da `test_t157_verificador_ids.py` (versiones de juguete
  8.0 y 9.0): ninguna prueba ni golden fijaba el 4.0. `tests/goldens/*.json` no tiene `catalog_version`, `RI-TB`, `CERT` ni
  `FC-EVAL`; `tests/goldens_ct.py` sigue diciendo «coinciden» tras el cambio. No se re-congela nada.
- Antes del cambio, en una copia de HEAD con solo los ayudantes puros añadidos (para que el fichero de pruebas se pueda
  importar), 15 de las 16 pruebas nuevas fallan; la que pasa es la prueba unitaria de esos ayudantes (ver `pruebas.md`).

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`:
    - Constantes `FICHA_CERTIFICADO` (FC-EVAL-001), `COINCIDE_CT10` (SI, DENTRO_TOLERANCIA), `ORIGEN_TOLERANCIA` y
      `_DEFECTO_CELDA` (semilla y h leídas de la firma de `evaluar_celda`: no se escribe ningún número).
    - Funciones `cifras_certificado` (las cifras que cita el CERT- y usa su criterio), `holgura_tolerancia` (desviación
      relativa máxima tras k comparaciones con tolerancia relativa t: (1 + t/(1−t))^k − 1) y `criterio_desfavorable`
      (materialidad: el criterio con cada cifra movida en contra).
    - `Evaluador._parametros_certificado` y `_entradas_celda`: las mismas entradas y parámetros para el cálculo propio y para
      la petición al Motor. `revisar_certificados` las usa (el nivel del IC pasa a salir de `evaluacion.nivel_ic`).
    - `Evaluador._verificar_reejecucion`: CT-09 de FC-EVAL-001 (solicitante AG-20) → comparación de cifras con
      `servicio.comparar` y la tolerancia de la ficha → `Motor.reejecutar` (CT-10, AG-20) → materialidad si algo no es exacto.
      Nunca lanza: devuelve `coincide`, motivo, severidad, `calc_soporte`, `reejecucion` y el detalle.
    - `revisar_certificados`: retira las propuestas sin re-ejecución coincidente (anteriores a T-160) antes de evaluar; por
      cada celda certificable sin certificado llama a `_verificar_reejecucion`; si falla, la celda queda no certificable con
      el motivo, en `sin_reejecucion_coincidente`, y con una incidencia `HERRAMIENTA` en HA; si coincide, el CERT- lleva
      `calc_soporte`, `curva_fiabilidad`, `reejecucion` y `reejecucion_ct10`.
    - `motivo_sin_reejecucion` y `aprobar_certificados`: CT-04 valida en el RC la re-ejecución de cada PROPUESTO antes de
      escribir nada.
    - `tasa_base`: `"catalog_version": servicio.CATALOG_VERSION`.
    - Dos `zip(x, x[1:])` → `itertools.pairwise` (mismo resultado; baja la cuota de ruff).
  - `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py`: `f_fc_eval` pasa `fechas` (de los valores) y `min_conglomerados` (de
    los parámetros) a `evaluar_celda`; sin fechas, igual que antes; con fechas y sin mínimo, KeyError → rechazo
    DATOS_INSUFICIENTES. `comparar(a, b, tol)`, envoltura pública de la regla de comparación de CT-10. `startswith` con tupla
    en `citable_segun_catalogo` (mismo resultado; baja la cuota).
  - `bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py`: docstring «Catálogo de cálculos V5.0».
  - `bloque_a/11_Ejecutor/tests/test_t160_reejecucion_certificado.py` (nuevo): 16 pruebas.
  - `bloque_a/11_Ejecutor/tests/test_t66_evaluacion.py`: las cuatro pruebas que esperan que se emita un certificado
    construyen el Evaluador con un Motor (`_con_motor`). Sus aserciones no cambian; sin Motor ya no hay certificado, y eso lo
    fija `test_ca3_sin_motor_no_hay_certificado`. No es debilitar: el requisito nuevo pide el Motor.
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: PB-32 pasa a AUTOMATICA con las pruebas nuevas y `no_comprueba` vacío.
  - `docs/evidencias_pruebas_bloque_a.md`: regenerado con `.docs/scripts/evidencias_plan_a.py --ejecutar`.
  - `docs/incidencias.md`: INC-T160-01 y las notas «aplicada» de PB-32 (INC-T116-03) y de INC-T157-02.
  - `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`: una fila en §4.
  - `bloque_a/11_Ejecutor/README.md`: el párrafo «Re-ejecución CT-10 antes de certificar».
- **Decisiones tomadas y desviaciones del plan:** las de INC-T160-01 (`[PROPUESTO]`): el cálculo de soporte es FC-EVAL-001 del
  Motor; tolerancia de la ficha (la de CT-10) con su origen; materialidad con las cifras movidas en contra; fallo cerrado con
  incidencia `HERRAMIENTA` (Material o Operativa); CT-04 exige la re-ejecución en el RC; propuestas antiguas retiradas; CT-10
  sin mensaje en la mensajería, como CT-09 desde el Evaluador. Sin desviaciones del plan. Además, dos arreglos de ruff en los
  ficheros tocados (`pairwise`, `startswith`) para bajar la cuota.
- **Límites conocidos:**
  - Los certificados VIGENTE anteriores a T-160 no se revocan por falta de re-ejecución.
  - No se re-ejecuta la revocación ni la recalibración (el prompt del Evaluador también lo cita): endurecen o son propuesta.
  - La re-ejecución corre en el mismo proceso y con el mismo código que el cálculo original (es lo que hace hoy CT-10 en el
    ejecutor): detecta artefactos alterados, datos distintos, falta de determinismo y una implementación que cambia, no un
    error común a las dos pasadas.
  - Coste: cuatro pasadas más de `evaluar_celda` por celda certificable sin certificado (dos del servicio, dos de CT-10), y
    0,02 UC de Motor por la petición CT-09 (`uc.motor_por_plan.PLAN_MIN`).
  - Una celda que no pasa la re-ejecución deja una incidencia en cada revisión en que se reintenta.
  - `docs/auditoria_ids_bloque_a.*` no se regenera aquí (entregable de T-157): la próxima regeneración ya no tendrá el ERROR
    CATALOG_VERSION_LITERAL ni el AVISO del docstring (lo comprueba `test_ca7_el_verificador_de_ids_ya_no_ve_la_version_escrita_a_mano`).
- **Comandos exactos para probarlo** (desde la raíz de la copia):

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t160_reejecucion_certificado.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t66_evaluacion.py tests/test_t66_propuestas.py \
  tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py tests/test_t157_verificador_ids.py tests/test_t112_motor.py \
  tests/test_t118_hallazgos.py tests/test_t121_hallazgos.py tests/test_unitarias.py tests/test_fase3_goldens.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase4_huecos.py tests/test_integracion.py -k "cert or pb32 or pa10 or pa03 or pa09 or holm"
../../.venv/bin/python tests/goldens_ct.py
cd ../.. && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-32
```
