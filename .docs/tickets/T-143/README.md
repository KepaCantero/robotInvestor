# T-143 · Nueva entrega del Documento 0 del Bloque A (V5.2) con el Anexo B corregido

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r04 APTO tras la ronda de cierre) |
| Pieza | bloque_a (Documento 0 y goldens de contratos) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | aprobada el 2026-11-15: «Nueva entrega del Documento 0. Autorizada: el Anexo B se corrige con el borrador para que describa lo que hace el ejecutor» (`sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`); y la del 13-11-2026: «manda el código» |
| Deuda técnica | T-143 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila no se toca en esta tarea: la actualiza la sesión coordinadora) |

## Objetivo

Publicar la V5.2 del Documento 0 del Bloque A: la V5.1 con el Anexo B corregido para que describa lo que hace el ejecutor (decisión del operador del 13-11-2026, INC-T114-01), y dejar los goldens de contratos midiendo contra ella, de forma que las diferencias que el Anexo B ya describe desaparezcan y una diferencia nueva siga haciendo fallar la suite.

## Alcance

- Entra:
  - `bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md`: la V5.1 con el Anexo B reescrito según el borrador, la cabecera de versión y una fila nueva en el Anexo F (registro de cambios);
  - la V5.1 (`.md` y `.docx`), sin cambios, a `bloque_a/99_Historico_V5.1/01_Gobernanza/` (precedente: `99_Historico_V3.0`);
  - los goldens de contratos: los esquemas y ejemplos derivados del Anexo B (`anexo_b_esquemas.json`, `anexo_b_ejemplos.json`), la batería (solo para que siga midiendo lo mismo), su README y el re-congelado con `goldens_ct.py --update --motivo`;
  - las pruebas `tests/test_fase3_goldens.py`, actualizadas a propósito y con pruebas nuevas que comparan el Anexo B V5.2 con el código (esquemas de respuesta, estados propios, retornos del Motor);
  - las referencias a la V5.1 por nombre o ruta: prompts de fase, README índice del bloque, CLAUDE.md si cita el nombre, código y pruebas;
  - el borrador (`.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`) marcado como aplicado y su generador ajustado para decir lo que queda;
  - INC-T114-01 (ronda T-143) e incidencia nueva de que la V5.2 no tiene `.docx` todavía; la fila de la decisión del operador con «aplicada en la V5.2»;
  - el re-congelado del corpus con `tools/corpus_integridad.py --update`.
- No entra:
  - cambiar el código de producción del ejecutor: manda el código; el único cambio de código permitido es el imprescindible para leer la entrega nueva, y no hace falta ninguno (el ejecutor no lee el Documento 0; las pruebas lo buscan con `glob("Documento 0*.md")`);
  - nada del Documento 0 fuera del Anexo B, salvo la cabecera de versión y la fila del Anexo F; en particular, los §7.6 y §7.9 (CT-22, «tipo») no se tocan: el Anexo B dice qué campo lleva cada valor;
  - el ejemplo publicado del informe de seguimiento (INC-T114-02): vive en `06_Plantillas_entregables`, no en el Documento 0;
  - los system prompts (`02_System_prompts`) y el resto del corpus que cita «Documento 0 óptima V5.1»: son datos congelados;
  - `bloque_a_forex/`, `bloque_b/` (también su Documento 0, que cita «Documento 0 del Bloque A V5.1»), `sistema_global/marco_comun_c/`, la Constitución y la fila T-143 de la deuda;
  - generar un `.docx` de la V5.2.

## Diseño

### Decisiones

- **Versión V5.2, no V6.0 ni V5.1.1.** Cambia el texto de un anexo para que coincida con lo que ya hace el código; no cambia ningún formato ni la versión de los contratos (`version_contrato` sigue en «5.1»). La numeración del documento sube un menor, como la V5.0 → V5.1.
- **Ubicación.** La V5.2 en `bloque_a/01_Gobernanza/` con su nombre de versión; la V5.1 entera (`.md` y `.docx`) en `bloque_a/99_Historico_V5.1/01_Gobernanza/`, sin un byte cambiado, como `99_Historico_V3.0`. Así `01_Gobernanza` solo tiene un Documento 0 y las pruebas que lo buscan por `glob` (o que exigen uno solo, `test_t142_cadena_b.py`) leen la V5.2 sin cambiar.
- **Sin `.docx` de la V5.2.** Los `.docx` son copias de consulta que no se editan; no se genera uno. Se declara en `docs/incidencias.md` (INC-T143-01).
- **README índice del bloque.** No se renombra: el bloque sigue siendo la entrega V5.1 con un Documento 0 V5.2 (su nombre es el de la entrega, como el del README de la raíz). Es parte del corpus congelado, pero es el índice que hay que leer primero (CLAUDE.md): se le añade una fila al registro de actualizaciones y se corrige la fila de `01_Gobernanza`. Entra en el re-congelado.
- **Campos que el ejecutor no exige: opcionales** (decisión del operador, manda el código). Donde el borrador ofrecía «o exigirlos en el código», se marcan «opcional» o «si aplica».
- **CT-22.** Se documentan los dos campos como están (`tipo` para DECISIONES_BROKER y PREGUNTA_REPETIDA; `tipo_aviso` para CONSULTA_RECURRENTE y DECISION_SEGUIMIENTO). Unificar en el código sería un cambio de formato, que esta tarea no hace. El Anexo B dice que la palabra «tipo» de los §7.6 y §7.9 se refiere a uno u otro campo según el valor, para no tocar esas secciones.
- **Retornos internos (CT-06 a CT-08 y CT-11 a CT-14).** El borrador pide describir los campos de los esquemas de respuesta de `ESQUEMAS`, no marcar opcionales los de hoy. El Anexo B V5.2 lo hace con una frase fija por esquema («con `CLAVE`, que exige …; admite además …»), que una prueba nueva compara con `contratos.ESQUEMAS`. Como no pasan por la mensajería, el esquema derivado del mensaje no exige ningún campo; sí nombra los del esquema de respuesta.
- **Retornos del Motor (CT-09 y CT-10).** Se describen las claves que devuelven `Motor.servir` y `Motor.reejecutar`; una prueba nueva las compara con lo que devuelve el Motor de verdad.
- **Fases de CT-06.** Se añaden las que el ejecutor emite: CRIBADO_E_INVESTIGACION y RESPUESTA_OBJECIONES (las del borrador) y además REVISION_VIGENTES, que el golden no nombraba porque su mensaje de error es el mismo. Se conservan CRIBADO, INVESTIGACION y PROFUNDIZACION, como dice el borrador («añadirlas»), porque los system prompts congelados las usan.
- **Lotes (CT-11 a CT-13).** Cada elemento se describe con los campos que el ejecutor envía de verdad (los de `orquestacion.py` y `diseno_v6.py`), no con los nombres de la V5.1 que el borrador copiaba: por ejemplo, el ejecutor no envía `fechas` ni `unidad_divisa` en CT-11, ni `tesis`, `evidencias_clave` ni `prospectiva` en CT-13 (PA-05: el Contradictor no ve la tesis).
- **CT-16, CT-17 y CT-19.** Se dan los campos de lo que el ejecutor emite, como propone el borrador. CT-18, CT-20 y CT-21 siguen remitidos a los prompts.
- **La batería no cambia lo que mide.** Los casos que partían de un ejemplo que cambia pasan a llevar su cuerpo (el ejemplo V5.1) dentro del caso, con un script de una vez; así `aceptaciones_rechazos.json` sale idéntico y se ve que ninguna regla de la mensajería cambió.

- Contratos CT afectados y versión de esquema: ninguno cambia de formato; `version_contrato` «5.1».
- Estado persistido: no cambia.
- Números: ninguno nuevo. El Anexo B no escribe cifras de configuración.
- Cómo falla cerrado: las pruebas nuevas fallan si el Anexo B y el código vuelven a diferir (un campo nuevo o quitado en `ESQUEMAS`, en las claves del Motor, en los estados propios o en lo que se emite).
- Decisiones del operador usadas como `[PROPUESTO]`: ninguna nueva; las de esta tarea las tomo por defecto (regla del 13-11-2026) y quedan en INC-T114-01.

## Ronda r02 (QA r01 NO APTO)

Hallazgos de `qa.md` (r01), todos de texto del Anexo B salvo H-05 (pruebas) y H-06 (cabecera de la configuración). Como la V5.2 aún no está en el corpus de `develop`, se corrige ahora todo lo que el código contradice, sin cambiar código:

- H-01: CT-04 nombra el quinto bloque, `aprobar_certificados` (PA-10), y «un CT-04 sin ninguno de los cinco se rechaza».
- H-02: el retorno de CT-15 es `REDACCION` (y `SINTESIS` en V6), descrito con la frase fija; CT-15 entra en la lista de retornos internos.
- H-03: los campos anidados de los retornos internos se describen con los de su esquema de respuesta («En `CLAVE`, cada elemento de `campo` lleva …; admite además …»), con los valores de sus listas cerradas; `estado_run` de CT-03 «solo si se ejecutó el análisis». Buscando otros iguales: el retorno de CT-05 es `INTEGRACION` y el retorno parcial no lo lee el ejecutor; CT-05 tiene el tipo INTEGRACION; dentro del `alcance` de CT-01 todo es opcional; las referencias de `BUSQUEDA` solo exigen `ref_id`.
- H-04: la `fecha_corte` de CT-09 la exige la mensajería; el Motor, sin ella, usa la del proveedor.
- H-05: pruebas nuevas `test_t143_r02_*` para los mutantes vivos (valores de las listas en la prosa, cuándo se emite cada fase de CT-06, prosa que vuelve a exigir un campo, anidados).
- H-06: la línea 2 de `bloque_a/11_Ejecutor/config/por_defecto.yaml` cita la V5.2. **CLAUDE.md no se toca** (ver el análisis): la aprobación de cambiar «695» por «696» llega en un mensaje de la sesión coordinadora, no del operador, y CLAUDE.md solo se cambia con la aprobación del propio operador en su sesión.

Criterios de la r02: CA-11, todos los hallazgos de la r01 corregidos o explicados; CA-12, `test_t143_r02_*` matan los mutantes vivos de `r01_03` que siguen aplicando; los demás criterios, como en la r01.

## Ronda r03 (QA r02 NO APTO)

Hallazgos de la sección «Ronda r02» de `qa.md`, todos de texto del Anexo B salvo H-11 (pruebas). Sin cambios de código del ejecutor ni de `CLAUDE.md`:

- H-07: CT-05 dice qué lleva `memoria` (y `delta_gc0`) en la orden del ciclo, en SEGUIMIENTO y en INTEGRACION, y que en el diseño V6 no hay orden INTEGRACION.
- H-08: la ficha de `finalistas` da los valores de sus listas cerradas (`tipo_opcion`, `horizontes_aplicables`, `regiones` y, entre los opcionales, `naturaleza_inversion`, `horizonte_principal` y `liquidez`), nombra sus opcionales y describe sus anidados con «En `FINALISTA`, …»: la regla de lectura se cumple sin acotarla. La prueba mira dentro de la ficha.
- H-09: el retorno de CT-17 se describe con `AUDITORIA` y CT-17 entra en la lista de retornos internos.
- H-10: de cada referencia de `BUSQUEDA`, lo que el ejecutor lee además y que en backtest solo cuentan las ofrecidas.
- H-11: la marca de «opcional» tiene que acompañar al campo; frases fijas para CT-05, CT-06, CT-14 y CT-15; la captura de los flujos ya no rompe con `IndexError` si un cambio deja el ciclo sin opciones (C21).

Criterios de la r03: CA-13, H-07 a H-11 corregidos o explicados; CA-14, las pruebas nuevas matan los mutantes vivos de `r02_02` y los cambios de prosa de `r02_03` que siguen aplicando; los demás, como en la r01.

## Ronda r04 (QA r03 NO APTO)

Hallazgos de la sección «Ronda r03» de `qa.md`. Por decisión del operador (16-11-2026), los bajos no se aplazan y se corrigen aquí. Sin cambios de código del ejecutor ni de `CLAUDE.md`:

- H-12 (media): la nota del V6 de CT-05, con y sin `v6.sintetizador`; CT-15 dice cuándo responde el Sintetizador y que sus campos de integración son la integración del V6.
- H-13: CT-11 (curación solo en N2 y N3; en el V6, solo con `v6.curacion_llm`) y CT-14 (dictamen por regla en el V6 salvo con `v6.dictamen_g3_llm`).
- H-14: `objeto` de cada hallazgo de `AUDITORIA` y las tres primeras referencias de `BUSQUEDA`.
- H-15: pruebas que miden con el ejecutor lo que se lee de cada referencia y de cada hallazgo, y lo que cambia en el V6.

Criterios de la r04: CA-15, H-12 a H-15 corregidos; CA-16, mueren C28, C29, D30 y D31 de `r03_02`; los demás, como en la r01.

## Ronda de cierre (QA r04 APTO con H-16 a H-18)

La QA r04 dio APTO con tres bajos; por la regla del operador (16-11-2026) se subsanan aquí, con la corrección exacta de `qa.md`, antes de cerrar. Sin cambios de código del ejecutor, del Documento 0 ni de `CLAUDE.md`; sin re-congelado (goldens y corpus no cambian):

- H-16: en `tests/test_fase3_goldens.py`, `test_t143_r04b_dictamen_g3_del_v6` (V5, V6 y V6 con `v6.dictamen_g3_llm` × HT-09 en ADVERTENCIA y en BLOQUEO) y `test_t143_r04b_curacion_por_nivel_y_diseno` (N1 y N2 × V5, V6 y V6 con `v6.curacion_llm`); las dos frases nuevas de CT-15 en `FRASES_FIJAS`, comprobadas ahora en `test_t143_r04_lo_que_cambia_en_el_v6_…`; y fuera la aserción vacía `("CT-14", "DICTAMEN_G3") not in v6` de esa prueba (el ciclo simulado no llega a CT-14).
- H-17: en `pruebas.md`, el párrafo de D12 tras el de D29.
- H-18: resuelto al partir de `develop`. La copia de esta ronda es un worktree nuevo sobre `origin/develop` con `git merge --no-ff --no-commit 238ef4d` (sin conflictos) y `qa.md` y `revisores/` traídos de `6336cdc`; la instantánea de la pausa (`0b09071`) no se integra. `git diff --name-status origin/develop` no lleva `.venv` ni la deuda técnica.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| El Anexo B V5.2 describe algo que el código no hace | El Documento 0 vuelve a mentir | Cada afirmación nueva sale del código leído; las comprobables tienen prueba (ESQUEMAS, Motor, estados propios, flujos simulados) |
| Debilitar las pruebas al quitar divergencias | Una diferencia futura pasaría sin aviso | Las pruebas que fijaban divergencias pasan a fijar la coincidencia y se añaden mutantes que la rompen |
| Recongelar el corpus con cambios ajenos | Se congela trabajo de otra sesión | Diff del manifiesto: solo las entradas de los ficheros movidos, nuevos o el README índice |
| Otras pruebas leen el Documento 0 | Fallan con dos documentos o con la V5.2 | Solo queda uno en `01_Gobernanza`; se pasa la suite completa de A |

## Criterios de aceptación (binarios)

1. CA-1: existe la V5.2 en `bloque_a/01_Gobernanza/`; fuera del Anexo B solo difiere de la V5.1 en la cabecera de versión y en una fila nueva del Anexo F con fecha 15/11/2026 y motivo.
2. CA-2: la V5.1 (`.md` y `.docx`) está en `bloque_a/99_Historico_V5.1/01_Gobernanza/` con los mismos SHA-256 que tenía en el manifiesto; en `01_Gobernanza` queda un solo Documento 0.
3. CA-3: `divergencias_anexo_b.json` regenerado contra la V5.2 no tiene diferencias por contrato, ni mensajes de los flujos que no cumplan, ni valores en otro campo; lo que queda (contratos sin campos) está explicado en el análisis técnico.
4. CA-4: las pruebas de `test_fase3_goldens.py` que fijaban divergencias fijan ahora la coincidencia, y fallan si se reintroduce una diferencia (mutantes en las pruebas); hay pruebas nuevas que comparan el Anexo B V5.2 con `ESQUEMAS`, con los estados propios de CT-23 a CT-25 y con lo que devuelve el Motor.
5. CA-5: `aceptaciones_rechazos.json` no cambia (la batería mide lo mismo) y `goldens_ct.py` termina en 0; el re-congelado está anotado en `goldens/REGISTRO.md` con su motivo.
6. CA-6: ninguna referencia viva (código, pruebas, `prompts/`, README índice, CLAUDE.md, `docs/` vivos) cita por nombre o ruta la V5.1 como vigente; `tools/refs_vivas.py` pasa. Las citas del corpus congelado y de los registros históricos se quedan y están apuntadas.
7. CA-7: el corpus recongelado coincide con el manifiesto nuevo, y el diff del manifiesto solo toca la V5.1 (2 rutas que se mueven), la V5.2 (nueva) y el README índice del bloque.
8. CA-8: el borrador dice que está aplicado en la V5.2, `borrador_anexo_b.py --comprobar` pasa y lo generado dice lo que queda.
9. CA-9: INC-T114-01 lleva la ronda T-143, hay incidencia del `.docx` que falta y la decisión del operador dice «aplicada en la V5.2».
10. CA-10: la suite completa de A no baja de 607 y pasa; ruff ≤ 2831 y mypy de A ≤ 109; gates ligeros en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Diff textual V5.1 → V5.2 fuera del Anexo B (script en el análisis) | regresión | CA-1 |
| `sha256sum` de la V5.1 movida frente al manifiesto viejo | regresión | CA-2 |
| `test_ca4_*`, `test_ca7_*` actualizados y `test_t143_*` nuevos en `test_fase3_goldens.py` | contrato, fallo cerrado (mutantes) | CA-3, CA-4 |
| `python tests/goldens_ct.py` y `cmp` de `aceptaciones_rechazos.json` | regresión | CA-5 |
| `tools/refs_vivas.py`, grep de «V5.1» | regresión | CA-6 |
| `tools/corpus_integridad.py` y `diff` del manifiesto | integración | CA-7 |
| `.docs/scripts/borrador_anexo_b.py --comprobar`, `pruebas_scripts.sh` | regresión | CA-8 |
| `pytest -q` de A, cuotas de ruff y mypy, `check_all.sh --core` | integración | CA-10 |

## Scripts

- `bloque_a/11_Ejecutor/tests/goldens_ct.py` (`--update --motivo`), `tools/corpus_integridad.py --update`, `.docs/scripts/borrador_anexo_b.py`, `.docs/scripts/nuevo_ticket.sh`.
- Script de una vez (no se guarda: no se repite) para pasar los casos de la batería a cuerpo propio: en `analisis-tecnico.md`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan y criterios
- 2026-11-15 · EN CURSO · claude · implementación
- 2026-11-15 · EN QA · claude · implementado y probado; falta la QA r01 con un revisor nuevo
- 2026-11-15 · EN CURSO · claude · ronda r02 (QA r01 NO APTO: H-01 a H-06)
- 2026-11-15 · EN QA · claude · ronda r02 implementada y probada; falta la QA r02
- 2026-11-16 · EN CURSO · claude · ronda r03 (QA r02 NO APTO: H-07 a H-11)
- 2026-11-16 · EN QA · claude · ronda r03 implementada y probada; falta la QA r03
- 2026-11-16 · EN CURSO · claude · ronda r04 (QA r03 NO APTO: H-12 a H-15)
- 2026-11-16 · EN QA · claude · ronda r04 implementada y probada; falta la QA r04
- 2026-11-17 · EN CURSO · claude · ronda de cierre (QA r04 APTO con H-16 a H-18), sobre `develop` sin la instantánea `0b09071` (H-18)
- 2026-11-17 · EN QA · claude · ronda de cierre implementada y probada; falta repasar `r04_02` y `git diff --name-status develop`
- 2026-11-17 · CERRADO · revisor (QA r04) · ronda de cierre comprobada: H-16 a H-18 corregidos; QA r04 APTO
