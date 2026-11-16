# T-163 · Bloque A, Evaluador: hallazgos de la QA r01 de T-160 (CT-04 ata la re-ejecución al certificado, VIGENTE sin re-ejecución, H-03 a H-06)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | bloque_a (ejecutor: `bloque_a/evaluador.py` y `bloque_a/motor/servicio.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: corrige hallazgos de QA y solo endurece (un certificado exige más condiciones; un VIGENTE sin re-ejecución deja de usarse). No cambia contratos CT, esquemas del corpus, la Constitución ni los controles. H-02 **decidido** por el agente por delegación del operador (16-11-2026, `Decisiones_del_operador_Bloque_A.md` §1, «Certificados de horizonte VIGENTE anteriores a T-160»): la opción prudente |
| Deuda técnica | T-163 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Cerrar los hallazgos H-01 a H-06 de la QA r01 de T-160 (`.docs/tickets/T-160/qa.md`): que la re-ejecución CT-10 que cita un
certificado sea de verdad la suya (sus cifras, su método, su celda, sus entradas, solo suya y sin un NO posterior), que un VIGENTE
sin ella no habilite probabilidades, que la emisión directa tenga la misma comprobación que CT-04, que FC-EVAL-001 valide el
mínimo de conglomerados y que mueran los mutantes M12 y M17.

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`:
    - `motivo_sin_reejecucion` (la usan CT-04, la emisión y `certificados_vigentes`) comprueba además, contra el Registro de
      cálculos: el método del soporte (`parametros.metodo`) es el de la celda; las entradas del soporte son las del certificado
      (`huella_entradas`) y las de la re-ejecución; la re-ejecución es posterior al soporte; ninguna CT-10 del mismo soporte
      posterior a la citada da NO (H-05); la re-ejecución no la cita antes otro certificado (cada una sirve a uno solo); y las
      cifras del CERT- coinciden con las del soporte con la tolerancia de CT-10 (H-01).
    - La petición FC-EVAL-001 del certificado lleva `metodo` en los parámetros; el CERT- lleva `huella_entradas`.
    - La emisión pasa el borrador del CERT- por `motivo_sin_reejecucion` antes de escribirlo (H-03).
    - `certificados_vigentes` solo devuelve los VIGENTE con su re-ejecución coincidente; `revisar_certificados` revoca los que no
      la tienen (con su motivo) y la celda se vuelve a evaluar y a proponer en la misma revisión (H-02, decidido).
  - `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py`: `f_fc_eval` exige, con `fechas`, un `min_conglomerados` entero ≥ 2 (no
    booleano), el mismo suelo que el Evaluador aplica a `evaluacion.min_conglomerados_bootstrap` (H-04).
  - Pruebas nuevas en `bloque_a/11_Ejecutor/tests/test_t163_hallazgos_t160.py` (H-01 a H-06); un ayudante de pruebas que escribe
    un certificado VIGENTE con su soporte y su re-ejecución (`tests/conftest.py`), para las pruebas que antes escribían un VIGENTE
    a mano sin re-ejecución y comprueban otra cosa (publicación y revocación por deterioro).
  - `docs/incidencias.md` (INC-T160-01, ampliada con T-163), `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`
    (fila de T-160 en §4) y `bloque_a/11_Ejecutor/README.md`.
- No entra: otros bloques, `sistema_global/marco_comun_c/`, la Constitución, el corpus (695), el Documento 0, `guias.py`, `cli.py`,
  `orquestacion.py`, `herramientas/verificador_ids.py`, los goldens; comprobar que las entradas del soporte son exactamente los PRG
  resueltos de la celda en la fecha de emisión (límite: se ata el certificado a su soporte, no el soporte a F4); verificar Holm en
  CT-04 (es un criterio entre celdas y el CERT- no guarda la p de DM).

## Diseño

- **Qué es «la re-ejecución de este certificado»** (H-01). Con el RC (`almacen.estado("RC")`, que guarda el `_seq` de cada entrada)
  y F6 leídos una vez por llamada:
  1. las comprobaciones de T-160 (CT-10 del Evaluador, re-ejecuta el soporte, coincide, el soporte es FC-EVAL-001 de la celda);
  2. el método: `parametros.metodo` del soporte es `celda.metodo` (la petición lo lleva desde T-163);
  3. las entradas: la huella de los datos del soporte es la `huella_entradas` del CERT- y la de la re-ejecución;
  4. el orden: la re-ejecución está en el RC después del soporte, y ninguna REEJECUCION del mismo soporte posterior a la citada
     tiene `coincide` fuera de SI / DENTRO_TOLERANCIA (H-05);
  5. la exclusividad: el primer CERT- de F6 que cita la re-ejecución es este (un certificado nuevo, aún sin escribir, solo si
     nadie la cita);
  6. las cifras: n, n_eff, Brier, Brier de referencia, BSS y su IC (y su método), ECE, q90 del nulo y la muestra efectiva del
     CERT- frente a las del `resultado.payload` del soporte con `servicio.comparar` y la tolerancia de la ficha (1e-8, la de CT-10).
  Un certificado de antes de T-163 no lleva `metodo` en el soporte ni `huella_entradas`: no pasa (falla cerrado) y vuelve por la
  vía normal.
- **VIGENTE sin re-ejecución** (H-02, decidido: la opción prudente de la QA, por delegación del operador, §1 de Decisiones): `certificados_vigentes` (lo que leen la síntesis,
  G3, el backtest y el diseño V6) no los devuelve; `revisar_certificados` los revoca (`CERT_REVOCACION`, motivo «sin re-ejecución
  CT-10 coincidente…», en `revocados` y en `vigentes_sin_reejecucion`) y la celda se evalúa como si no tuviera certificado: si
  cumple, se propone con su CT-10 (PROPUESTO con `solo_endurecer`). Revocar endurece (PA-10): es automático. Los VIGENTE anteriores a T-160 dejan de usarse hasta que se vuelven a
  proponer y se aprueban por CT-04.
- **Emisión directa** (H-03): el borrador del CERT- pasa por `motivo_sin_reejecucion` antes de escribirse; si no pasa, no hay
  certificado, la celda queda en `sin_reejecucion_coincidente` y hay una incidencia `HERRAMIENTA` Material.
- **FC-EVAL-001** (H-04): con `fechas`, `min_conglomerados` tiene que ser un entero (no booleano) ≥ `servicio.MIN_CONGLOMERADOS`
  (2); si no, rechazo DATOS_INSUFICIENTES. La ficha no fija el mínimo; el suelo es el mismo que valida el Evaluador para
  `evaluacion.min_conglomerados_bootstrap` (con un conglomerado el bootstrap por fechas no varía), y el Evaluador pasa a leerlo de
  esa constante. Sin `fechas`, igual que antes.
- **Contratos CT:** ninguno cambia de forma. **Estado persistido:** F6 gana `huella_entradas` en el CERT-; el RC, `metodo` en los
  parámetros del soporte. F6 es de solo añadir; nada se migra (lo anterior falla cerrado y se vuelve a proponer).
- **Números:** la tolerancia, de la ficha (`servicio.IMPLEMENTADAS["FC-EVAL-001"]["tol"]`); el suelo de conglomerados, la regla del
  Evaluador ya existente (ahora una constante con su origen). Ningún número nuevo.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Pruebas que escriben un VIGENTE a mano sin re-ejecución para probar otra cosa | Dejan de ver el certificado | Un ayudante escribe el VIGENTE con su soporte y su CT-10 de verdad (por el Motor); sus aserciones no cambian |
| `certificados_vigentes` más lento (lee RC y F6) | Ciclos y backtests más lentos | Solo si hay algún VIGENTE; una lectura por llamada |
| Un certificado legítimo de T-160 deja de valer | Hay que volver a proponerlo (y aprobarlo) | Es lo prudente y lo que pide la QA; vuelve solo en la revisión siguiente |
| Los mutantes de r01_03 dejan de aplicar | No se puede repetir la ronda de la QA | Se conservan las líneas que mutan; se ejecutan todos |
| La prueba de r01_01 que documenta H-05 (`auditoria_ct10_posterior`) pasa a fallar | Parece una regresión | Es el comportamiento que H-05 pide cambiar; la prueba nueva fija el contrario. Se anota en `pruebas.md` |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): CT-04 rechaza (ValueError, F6 sin cambios) un PROPUESTO con cifras distintas de su soporte, con otro método, con
   otras entradas, que cita una re-ejecución ya citada por otro certificado o anterior a su soporte; aprueba el legítimo.
2. CA-2 (H-05): con una CT-10 del mismo soporte posterior a la citada que da NO, CT-04 rechaza; una SI posterior no impide.
3. CA-3 (H-02): un VIGENTE sin re-ejecución coincidente no sale en `certificados_vigentes`; la revisión lo revoca con su motivo
   y vuelve a proponer la celda con su CT-10; un VIGENTE legítimo sigue vigente.
4. CA-4 (H-03): un Motor que responde SI sin escribir en el RC no deja certificado, ni con `solo_endurecer` true ni false.
5. CA-5 (H-04): FC-EVAL-001 con fechas rechaza `min_conglomerados` 0, −1, 1, `True`, 1,5, "x" y None; acepta 2 y 10; sin fechas,
   igual que antes.
6. CA-6 (H-06): M12 y M17 mueren; los 26 mutantes de r01_03 aplican y solo sobreviven los equivalentes M13 y M14.
7. CA-7: las `test_h0*` de `r01_01_ataques.py` pasan; el resto también, salvo la que documenta H-05.
8. CA-8: regresión: `test_t160_reejecucion_certificado.py`, `test_t66_evaluacion.py`, las vecinas, goldens, gates ligeros y la suite
   completa de A en verde (≥ 607); ruff ≤ 2821; mypy A ≤ 109; PB-32 sigue «Superada».

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Propuestas falsas: cifras, método, entradas, re-ejecución ajena, orden; legítima aprobada | fallo cerrado / regresión | CA-1 |
| CT-10 posterior con NO y con SI | fallo cerrado / límite | CA-2 |
| VIGENTE a mano sin re-ejecución; VIGENTE legítimo; revisión que revoca y vuelve a proponer | regresión / integración | CA-3 |
| Motor que dice SI sin escribir, con `solo_endurecer` true y false | fallo cerrado | CA-4 |
| `min_conglomerados` raros y válidos, con y sin fechas | límite / fallo cerrado | CA-5 |
| Materialidad con ECE = q90·(1 − 1,5·tol); soporte de otra ficha con las mismas cifras | regresión (mutantes) | CA-6 |
| `r01_03_mutantes.py` con `.docs/scripts/mutantes_revisor_ampliado.py` en una copia «qa31_…_mut» | mutantes | CA-6 |
| `r01_01_ataques.py` | regresión | CA-7 |
| Vecinas, goldens, gates ligeros, suite de A, cuotas, evidencias de PB-32 | regresión | CA-8 |

## Scripts

`.docs/scripts/mutantes_revisor_ampliado.py` (mutantes del revisor con las pruebas nuevas), `tests/goldens_ct.py`,
`.docs/scripts/evidencias_plan_a.py` (comprobar el mapa; `--pb PB-32`). Ninguno nuevo.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios escritos
- 2026-11-16 · EN CURSO · claude · implementación y pruebas
- 2026-11-16 · EN CURSO · claude · H-02 decidido por la sesión coordinadora por delegación del operador (§1 de Decisiones): la opción prudente; quitado el `[PROPUESTO]` y la pregunta
- 2026-11-16 · EN QA · claude · implementado y probado (`pruebas.md`); commit local «wip local: T-163»; el commit definitivo lo hace la sesión coordinadora
