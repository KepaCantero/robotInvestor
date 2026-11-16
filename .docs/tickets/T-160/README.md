# T-160 · Bloque A, Evaluador: re-ejecución CT-10 antes de certificar un horizonte (PB-32) y catalog_version del Registro de cálculos (D-1 de T-157)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | bloque_a (ejecutor: `bloque_a/evaluador.py` y `bloque_a/motor/servicio.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: completa una función del diseño (PB-32, EVAL-F05) y corrige un literal; no cambia contratos CT, esquemas del corpus, la Constitución ni los controles. Solo endurece: un certificado exige una condición más. Lo que el diseño no dice se decide por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`) |
| Deuda técnica | T-160 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Que el Evaluador no proponga ni emita un certificado de horizonte (R13) sin una re-ejecución CT-10 coincidente del cálculo que
lo sostiene, como piden PB-32 (resultado esperado: «re-ejecución CT-10 coincidente»), EVAL-F05 y el punto 5 de §6.6 del prompt
del Evaluador; y que la entrada del Registro de cálculos de la tasa base RI-TB cite el Catálogo vigente (`servicio.CATALOG_VERSION`)
y no un 4.0 escrito a mano (D-1 de T-157, INC-T157-02).

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`: verificación CT-10 de cada celda certificable antes de escribir el CERT-;
    `aprobar_certificados` (CT-04) solo pone en vigor un PROPUESTO con su re-ejecución coincidente en el RC; una propuesta
    anterior sin ella se retira; `catalog_version` desde `servicio.CATALOG_VERSION`.
  - `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py`: FC-EVAL-001 acepta las fechas de conglomerado (`fechas` en los valores y
    `min_conglomerados` en los parámetros, PA-03), para que el cálculo del Motor sea el mismo que el del certificado; una función
    pública `comparar` con la regla de tolerancia de CT-10.
  - `bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py`: el docstring dice «Catálogo de cálculos V5.0» (la otra mitad de D-1).
  - Pruebas nuevas en `bloque_a/11_Ejecutor/tests/test_t160_reejecucion_certificado.py`; las de `tests/test_t66_evaluacion.py`
    que esperan un certificado reciben un Motor (sin él, ahora no hay certificado).
  - `tests/mapa_plan_pruebas.json` (PB-32) y `docs/evidencias_pruebas_bloque_a.md` regenerado con
    `.docs/scripts/evidencias_plan_a.py --ejecutar`.
  - `docs/incidencias.md` (INC-T160-01 y las notas «aplicada» de INC-T157-02 y de PB-32 en INC-T116-03),
    `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (una fila en §4) y `bloque_a/11_Ejecutor/README.md`.
- No entra:
  - La re-ejecución CT-10 de una revocación o de una recalibración (el prompt del Evaluador también la cita): revocar y retirar
    endurecen y siguen siendo automáticos; la recalibración es siempre propuesta (PA-10). Queda como límite.
  - Los certificados VIGENTE ya emitidos antes de T-160: no se revocan por no tener re-ejecución (límite declarado).
  - El corpus congelado, el Documento 0, los goldens y `tests/test_fase3_goldens.py`; `orquestacion.py`, `guias.py`, `cli.py`,
    `llm.py`, `consumo.py`, `cadena_b.py`, `motor/frontera_b.py`; otros bloques; `docs/auditoria_ids_bloque_a.*` (entregable de
    T-157: la próxima regeneración del verificador dejará de dar el ERROR de D-1).

## Diseño

- **Qué sostiene el certificado.** Las cifras del CERT- (n, n_eff, Brier, BSS y su IC, ECE, q90 del nulo, p de DM-HLN) salen de
  `evaluacion.evaluar_celda`, que es FC-EVAL-001 + FC-CAL-001. Antes de escribir el certificado, el Evaluador pide al Motor
  (CT-09, solicitante AG-20, como ya hace `_brier_del_motor`) FC-EVAL-001 con las mismas entradas (p, o, p_ref, fechas de
  conglomerado) y los mismos parámetros (réplicas, simulaciones, nivel, semilla, mínimo de conglomerados, tasa base). Ese
  `calc_id` es el cálculo de soporte (`calc_soporte`, y `curva_fiabilidad` del esquema de F6 4.3, porque la curva va en él).
- **Comparación 1 (el certificado y su cálculo).** Las cifras del certificado y las del cálculo servido se comparan con la regla
  de CT-10 (`servicio.comparar`) y la tolerancia de la ficha. Si difieren, no hay certificado.
- **Comparación 2 (CT-10).** El Evaluador encarga `Motor.reejecutar(calc_soporte, motivo, "AG-20")` (CT-10, AUD-REX-001; AG-20
  es emisor de CT-10 en `contratos.CANALES`). Sigue solo si `coincide` es `SI` o `DENTRO_TOLERANCIA`.
- **Tolerancia y su origen.** La de la ficha FC-EVAL-001 en `servicio.IMPLEMENTADAS` (1e-8 relativa), la que usa el Motor en
  CT-10: el Catálogo V5.0 dice que la re-ejecución usa «las [tolerancias] de la ficha original» (AUD-REX-001) y la ficha
  FC-EVAL-001 fija 1e-8 en métricas y 1e-6 en IC con la misma semilla (el ejecutor usa 1e-8 para todo: la más estricta). El
  Anexo A y la configuración no tienen ninguna. El certificado guarda el valor y su origen.
- **Materialidad (MC-08 §6.3).** Una diferencia dentro de tolerancia que cruza un umbral del certificado obliga a NO. Si alguna de
  las dos comparaciones no es exacta, el criterio se vuelve a aplicar con cada cifra movida en contra del certificado lo máximo
  que permite la tolerancia acumulada; si así ya no certifica, no hay certificado. `[PROPUESTO INC-T160-01]`.
- **Falla cerrado.** Sin Motor, con FC-EVAL-001 rechazado, con una excepción, con cifras distintas, con CT-10 `NO` (cualquier
  categoría) o con diferencia material: no se escribe el CERT-; la celda sale en `evaluadas` con `certificable: false` y el motivo,
  en `sin_reejecucion_coincidente`, y se registra una incidencia en HA (`HERRAMIENTA`; Material si las cifras no coinciden,
  Operativa si no se pudo re-ejecutar). El diseño no dice qué incidencia: `[PROPUESTO INC-T160-01]`. En la revisión siguiente se
  vuelve a intentar.
- **Entrada en vigor (CT-04, PA-10).** `aprobar_certificados` valida, antes de escribir nada, que cada PROPUESTO cita en
  `reejecucion` una entrada REEJECUCION del RC (CT-10, solicitante AG-20) coincidente cuyo `calc_original` es su `calc_soporte`,
  un SERVICIO de FC-EVAL-001. Si no, ValueError y F6 sin cambios. Una propuesta PROPUESTO sin re-ejecución (anterior a T-160) se
  retira en la revisión (retirar endurece, PA-10) y la celda se vuelve a evaluar en esa misma revisión. `[PROPUESTO INC-T160-01]`.
- **Contratos CT afectados:** ninguno cambia de forma. CT-10 se usa como el Motor ya lo sirve (sin mensaje en la mensajería: el
  Evaluador llama al Motor como en CT-09; así no cambia la golden de flujos, que dice que ningún flujo emite CT-09 ni CT-10).
- **Estado persistido:** F6 gana campos en el CERT- (`calc_soporte`, `curva_fiabilidad`, `reejecucion`, `reejecucion_ct10`), los
  del esquema de F6 4.3 más el detalle. Ningún lector exige que falten; nada se migra (F6 es de solo añadir).
- **Números y su origen:** réplicas, simulaciones, nivel del IC, mínimo de conglomerados, `min_certificar`, `ece_max` y
  `alfa_holm` de `evaluacion.*` (configuración); la semilla, la de `evaluar_celda` por defecto (se lee de su firma, no se escribe);
  la tolerancia, de la ficha. Cambio deliberado: el certificado pasa `evaluacion.nivel_ic` (0,90) en vez del valor por defecto de
  la función (también 0,90): mismo número, ahora de la configuración y el mismo en el certificado y en el Motor.
- **D-1.** `"catalog_version": servicio.CATALOG_VERSION` en `tasa_base`; docstring de `motor/operaciones.py`. Ninguna golden ni
  prueba fijaba el 4.0 (comprobado con `grep` en `tests/` y `tests/goldens/`): no se re-congela nada.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Pruebas que construyen el Evaluador sin Motor y esperan un certificado | Dejan de emitirlo | Esas pruebas reciben un Motor; la prueba nueva fija que sin Motor no hay certificado |
| Coste: cuatro pasadas más de FC-EVAL-001 por celda certificable | Revisión más lenta | Solo en celdas que ya pasan el criterio y no tienen certificado; en mock, segundos |
| La golden de flujos cambia si CT-10 va por la mensajería | Re-congelado no pedido | Se llama al Motor directamente, como en CT-09 |
| Una caché del Motor devuelve un resultado de otra petición | Comparación falsa | La clave de caché del Motor incluye datos, parámetros y fecha de corte; además se compara cifra a cifra |

## Criterios de aceptación (binarios)

1. CA-1: nominal. Una celda certificable sale con un CERT- cuyo `reejecucion` es un CALC- de CT-10 del RC con `coincide` SI o
   DENTRO_TOLERANCIA, `calc_original` = `calc_soporte` (SERVICIO de FC-EVAL-001, solicitante AG-20), y la tolerancia y su origen.
2. CA-2: no coincide. Con el recálculo CT-10 alterado (ERROR_ORIGINAL) no hay CERT- en F6, la celda no es certificable con el
   motivo CT-10 y hay una incidencia Material en HA.
3. CA-3: no se puede re-ejecutar. Sin Motor, con FC-EVAL-001 rechazado o con los datos del artefacto irresolubles en CT-10
   (ERROR_REEJECUCION): no hay CERT- y hay una incidencia.
4. CA-4: cifras distintas o diferencia material. Si el Motor no reproduce las cifras del certificado, o una diferencia dentro de
   tolerancia cruza un umbral, no hay CERT-.
5. CA-5: CT-04. `aprobar_certificados` rechaza (ValueError, F6 sin cambios) un PROPUESTO sin re-ejecución coincidente en el RC y
   aprueba uno con ella; una propuesta antigua sin re-ejecución se retira y la celda se vuelve a proponer con CT-10.
6. CA-6: PB-32 de extremo a extremo con el simulado: RF × H3 × método con habilidad y RV × H3 sin ella → un solo certificado (RF),
   con CT-10 coincidente; aprobado por CT-04; el ciclo siguiente publica la probabilidad solo en RF H3 con `certificado_ref` y
   G3 APTO.
7. CA-7: D-1. La entrada RC de la tasa base lleva `servicio.CATALOG_VERSION` (y sigue a la constante si cambia); el verificador
   de IDs ya no da CATALOG_VERSION_LITERAL ni la mención V4.0 del código.
8. CA-8: PB-32 pasa a «Superada» en `docs/evidencias_pruebas_bloque_a.md`, regenerado con el script.
9. CA-9: suite de A entera en verde (≥ la línea base), ruff ≤ 2828, mypy A ≤ 109, goldens y gates ligeros en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Certificado con CT-10 coincidente y sus referencias en el RC | nominal | CA-1 |
| Recálculo CT-10 alterado → ERROR_ORIGINAL, sin CERT- | fallo cerrado / regresión | CA-2 |
| Sin Motor; FC-EVAL-001 rechazado; datos irresolubles en CT-10 | fallo cerrado | CA-3 |
| Cifras del Motor distintas; DENTRO_TOLERANCIA material y no material | límite / fallo cerrado | CA-4 |
| CT-04 con y sin re-ejecución; propuesta antigua retirada y re-propuesta | fallo cerrado / regresión | CA-5 |
| PB-32 de punta a punta con `Bloque` y `MockClient` | integración | CA-6 |
| `catalog_version` de la tasa base y del verificador | regresión | CA-7 |
| `evidencias_plan_a.py --ejecutar` | integración | CA-8 |
| Vecinas (Evaluador, certificados, PA-10, T-66), goldens, gates ligeros, suite de A, cuotas | regresión | CA-9 |

## Scripts

`.docs/scripts/evidencias_plan_a.py` (comprobar el mapa y `--ejecutar`) y `tests/goldens_ct.py` (comprobar los goldens). Ninguno
nuevo.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios escritos
- 2026-11-16 · EN CURSO · claude · implementación y pruebas
- 2026-11-16 · EN QA · claude · implementado y probado; commit local «wip local: T-160»; el commit definitivo lo hace la sesión coordinadora
