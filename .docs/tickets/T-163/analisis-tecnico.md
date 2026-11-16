# T-163 · Análisis técnico

## Causa raíz o motivo

Hallazgos de la QA r01 de T-160 (`.docs/tickets/T-160/qa.md`, veredicto APTO):

- **H-01 (media).** `motivo_sin_reejecucion` (lo que mira CT-04) comprobaba que la CT-10 citada existe, coincide y re-ejecuta un
  FC-EVAL-001 de la misma clase × horizonte, pero no que fuera **la de ese certificado**: ni las cifras del CERT- frente a las
  del soporte, ni el método (la petición no lo llevaba), ni que la re-ejecución la citara un solo certificado. Un PROPUESTO falso
  con cifras infladas y la re-ejecución de otro entraba en vigor.
- **H-02 (media).** `certificados_vigentes` devolvía cualquier VIGENTE de F6, citara o no re-ejecución (límite declarado de T-160
  para los anteriores; valía igual para uno escrito hoy).
- **H-03 (baja).** La emisión directa (`aprendizaje.solo_endurecer` false) no pasaba por la comprobación de CT-04: un Motor que
  respondía «SI» sin escribir la REEJECUCION en el RC dejaba un VIGENTE citando un CALC- inexistente.
- **H-04 (baja).** `f_fc_eval` hacía `int(params["min_conglomerados"])`: 0, −1, `True` o 1,5 pasaban.
- **H-05 (baja).** CT-04 solo miraba la re-ejecución citada: una CT-10 posterior del mismo soporte con NO (p. ej. del Auditor)
  no impedía la aprobación.
- **H-06 (baja).** Mutantes vivos M12 (la materialidad no mueve el q90 del nulo) y M17 (CT-04 no mira la ficha del soporte).

## Evidencia

- Los ataques del revisor (`.docs/tickets/T-160/revisores/r01_01_ataques.py`): con el código de HEAD fallan las `test_h0*`
  (4 casos); con T-163 pasan las 35 menos una, `test_una_auditoria_ct10_posterior_que_no_coincide_no_impide_la_aprobacion`, que
  documentaba el comportamiento de H-05 y ahora falla por diseño (CT-04 rechaza con «una re-ejecución CT-10 posterior de
  CALC-… no coincide»).
- Mutantes del revisor (`r01_03_mutantes.py`) y mutantes propios de T-163 (`.docs/tickets/T-163/mutantes_t163.py`): resultados
  en `pruebas.md`.

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`:
    - `campos_certificado(m)`: las cifras del CERT- desde la salida de `evaluar_celda` (la emisión las escribía en línea; ahora
      las usa también el ayudante de pruebas). `cifras_del_soporte(payload)` y `cifras_del_certificado(cert)`: las mismas cifras
      a los dos lados para comparar (sin la p de DM-HLN, que el CERT- no guarda; con el método del IC del BSS). Lo que en el
      CERT- no tiene la forma esperada se deja tal cual para que la comparación lo marque.
    - `_contexto_reejecucion()`: el RC por calc_id, el `_seq` de cada entrada, las REEJECUCION de cada cálculo y el primer CERT-
      de F6 que cita cada re-ejecución, leído una vez.
    - `motivo_sin_reejecucion(c, contexto=None)`: tras las comprobaciones de T-160 (sin cambiar su orden ni sus mensajes),
      método del soporte (`parametros.metodo`), entradas (huella de los datos del soporte = `huella_entradas` del CERT- = la de
      los datos de la REEJECUCION, y la misma `operacion`), orden (`_seq` de la CT-10 > `_seq` del soporte), ninguna CT-10 del
      mismo soporte posterior a la citada fuera de SI / DENTRO_TOLERANCIA (H-05), exclusividad (el primer CERT- que la cita es
      este; uno sin escribir, solo si nadie la cita) y cifras con `servicio.comparar` y la tolerancia de la ficha (H-01).
    - `_verificar_reejecucion`: la petición FC-EVAL-001 lleva `metodo` en los parámetros; devuelve también `huella_entradas`
      (la de los datos del soporte en el RC).
    - `revisar_certificados`: antes de evaluar, revoca los VIGENTE que no pasan `motivo_sin_reejecucion` (CERT_REVOCACION con el
      motivo; `revocados` y la clave nueva `vigentes_sin_reejecucion`) y evalúa su celda como si no tuviera certificado (H-02); el
      borrador del CERT- (con `huella_entradas`, id puesto solo al escribirlo) pasa por `motivo_sin_reejecucion` antes de
      escribirse; si no pasa, no hay certificado, la celda queda en `sin_reejecucion_coincidente` y hay una incidencia
      `HERRAMIENTA` Material (H-03).
    - `certificados_vigentes`: solo los VIGENTE que pasan `motivo_sin_reejecucion` (H-02); `_vigentes_en_f6`, los de F6 tal cual,
      que usan la revisión y CT-04 (para no aprobar un segundo VIGENTE de una celda mientras el anterior no se ha revocado).
    - `_min_conglomerados`: el suelo sale de `servicio.MIN_CONGLOMERADOS` (mismo 2).
  - `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py`: `MIN_CONGLOMERADOS = 2` (con su origen) y `min_conglomerados_valido`;
    `f_fc_eval` con `fechas` rechaza (ErrorFicha → DATOS_INSUFICIENTES) un `min_conglomerados` que no es un entero ≥ 2 (no
    booleano). Sin `fechas`, como antes; sin la clave, el KeyError de T-160 sigue siendo el rechazo.
  - `bloque_a/11_Ejecutor/tests/test_t163_hallazgos_t160.py` (nuevo): 48 pruebas.
  - `bloque_a/11_Ejecutor/tests/conftest.py`: `certificado_con_reejecucion(almacen, celda, cid, estado, motor, cfg)`, que escribe
    un CERT- con su soporte FC-EVAL-001 (datos sintéticos, con el método de la celda) y su CT-10 coincidente por el Motor de
    verdad. Además, cuatro `noqa: E402` sin uso quitados (ruff RUF100).
  - Pruebas que escribían un VIGENTE a mano sin re-ejecución para probar otra cosa, ahora con el ayudante; sus aserciones no
    cambian: `test_fase4_huecos.py` (PB-33 ×2, revocación por deterioro; PB-32, publicación solo en la celda certificada),
    `test_t53_evaluacion_y_almacen.py` (ECE = 0 no revoca; umbral de revocación de la configuración), `test_t66_evaluacion.py`
    (PA-10, revocar es automático), `test_t87_datos.py` (R13, certificado por método en la entrega). Sin el cambio, las de
    revocación pasarían por otro motivo («sin re-ejecución» en lugar de «deterioro») o fallarían (ECE = 0), y las de
    publicación no publicarían: por eso se les da un certificado válido y no se relajan. `test_t87_datos.py`: orden de los
    imports (ruff I001).
  - `docs/incidencias.md` (INC-T160-01, ampliada), `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (fila de
    T-160 en §4, que remite a la decisión del §1; la fila del §1 la mantiene la sesión coordinadora) y `bloque_a/11_Ejecutor/README.md`.
- **Decisiones tomadas y desviaciones del plan:**
  - H-02, decidido por el agente por delegación del operador (§1 de Decisiones, «Certificados de horizonte VIGENTE anteriores a
    T-160»): la opción prudente; se revoca (no se deja en suspenso) y se vuelve a proponer. Anotado en INC-T160-01 como decidido.
  - Exclusividad: la re-ejecución es del **primer** CERT- de F6 que la cita, no se invalidan los dos (si no, escribir una copia
    tumbaría el legítimo).
  - H-05: cuenta una CT-10 posterior **a la citada** (no cualquiera del soporte): con la caché del Motor, un certificado que se
    vuelve a proponer reutiliza el mismo soporte con una CT-10 nueva, posterior a la NO, y así puede volver (lo prueba
    `test_h05_un_vigente_cuyo_soporte_no_coincide_despues_…`).
  - H-04: suelo 2, no 1 como sugería el encargo («o lo que diga la ficha»): la ficha no fija ninguno, y 2 es la regla que el
    Evaluador ya aplicaba a la configuración (con un conglomerado el bootstrap por fechas no varía). Más estricto, falla cerrado.
  - Sin cambios en `orquestacion.py`, `cli.py`, `guias.py`, el verificador, el corpus ni los goldens. El mapa del plan de pruebas
    no cambia (no se regeneran las evidencias).
- **Límites conocidos:**
  - Se ata el certificado a su soporte; que las entradas del soporte sean los PRG resueltos de la celda en la fecha de emisión no
    se vuelve a comprobar en CT-04 (el Evaluador las construye él mismo al emitir).
  - Holm no se re-verifica en CT-04 (criterio entre celdas; el CERT- no guarda la p de DM).
  - Los certificados de T-160 (soporte sin `metodo`, sin `huella_entradas`) dejan de valer y vuelven por la vía normal; con
    `solo_endurecer`, el operador tiene que volver a aprobarlos.
  - `certificados_vigentes` lee el RC y F6 una vez por llamada cuando hay algún VIGENTE.
  - La prueba del revisor que documentaba H-05 (`test_una_auditoria_ct10_posterior_…`) falla ahora por diseño.
- **Comandos exactos para probarlo** (desde la raíz de la copia):

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t163_hallazgos_t160.py tests/test_t160_reejecucion_certificado.py tests/test_t66_evaluacion.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase4_huecos.py tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py tests/test_t66_propuestas.py -k "pb33 or pb32 or r13 or ece_cero or umbral_de_revocacion or revoca or cert or pa10 or pa03"
../../.venv/bin/python tests/goldens_ct.py
cd ../..
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut»> \
  tests/test_t163_hallazgos_t160.py ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
.venv/bin/python .docs/tickets/T-163/mutantes_t163.py <copia «…_mut»>
```

(La copia de los mutantes del revisor lleva `bloque_a/` entero y `.docs/tickets/T-160/revisores/r01_01_ataques.py`.)
