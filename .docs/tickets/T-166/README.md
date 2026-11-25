# T-166 · Entrega del corpus del Bloque A: Catálogo V5.0 en los prompts MC, fichas y RF existentes en los ejemplos, y respuesta final de CT-03 en el Anexo B (Documento 0 V5.3)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r03 APTO) |
| Pieza | bloque_a (corpus congelado: Documento 0, prompts MC-01 a MC-05 y del Evaluador, funciones del Motor, Registro de cálculos; goldens de contratos) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | aprobada por delegación el 2026-11-16: «Esas decisiones que me tocan a mí quiero que las decidas tú por mí» (D-2 a D-4 de T-157 en `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` §1 y §6); la nueva entrega del Documento 0 con el Anexo B que describe el código, autorizada el 15-11-2026 (T-143) |
| Deuda técnica | T-166 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la actualiza la sesión coordinadora, como en T-143) |

## Objetivo

Publicar una entrega del corpus del Bloque A que corrija lo que el verificador de IDs (T-157) y el registro de decisiones dejaron pendiente antes de la Fase 5 (con la API real, los prompts llegan tal cual al modelo): «Catálogo V4.0» → «V5.0» (D-2), la ficha inexistente FX-MC10-003 → FC-EVAL-001 (D-3), la RF inexistente RF-0123 → una RF de F9 (D-4), y el Anexo B con la respuesta final de CT-03 (`respuesta_final`, T-162 y T-169). Tras la entrega, el verificador da 0 errores.

## Alcance

- Entra:
  - **D-2.** Las seis menciones de «Catálogo V4.0» en los prompts MC-01 a MC-05 (`bloque_a/02_System_prompts/`, una en prosa y cinco en ejemplos JSON) y la de MOTOR-F05 en las funciones del Motor (`bloque_a/03_Funciones/…Motor de Cálculo Avanzado…`), a «Catálogo V5.0».
  - **D-3.** En el ejemplo ficticio del Registro de cálculos (`bloque_a/05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0).md`, §7): `ficha_id` FX-MC10-003 → FC-EVAL-001 y `catalog_version` "4.0" → "5.0" (la octava mención del AVISO, que INC-T157-03 asigna a D-3). `ficha_version` "1.0" ya es la de FC-EVAL-001.
  - **D-4.** En el ejemplo de `fiabilidad_fuentes` del prompt del Evaluador: RF-0123 → **RF-0046** (Goldman Sachs Global Investment Research, TF-05, fuente de opinión con previsiones de estrategia; el ejemplo mide `RV×H3` y el Evaluador mide la fiabilidad de las fuentes de opinión para el Buscador).
  - **Anexo B.** Documento 0 **V5.3**: la V5.2 con un párrafo nuevo en CT-03 que describe la respuesta final como la escribe `bloque_a/respuesta_final.py` (campos, resultados, estado común, referencias, confianza, una sola vez, F5), cabecera de versión y fila del Anexo F.
  - **Histórico.** `bloque_a/99_Historico_V5.2/`: la V5.2 del Documento 0 (no tenía `.docx`) y los ocho archivos que esta entrega corrige, `.md` y `.docx`, sin un byte cambiado, en sus mismas subcarpetas (`01_Gobernanza`, `02_System_prompts`, `03_Funciones`, `05_Archivos_operativos`). Los `.md` nuevos se quedan en su sitio con el mismo nombre y sin `.docx` (INC-T166-01).
  - README índice del bloque: fila de `01_Gobernanza` (V5.3), fila nueva `99_Historico_V5.2` y entrada del registro (§8).
  - Goldens: `anexo_b_esquemas.json` (CT-03.RETORNO admite `respuesta_final`; marca «V5.3»), re-congelado con `goldens_ct.py --update --motivo "T-166: …"`.
  - Pruebas nuevas `tests/test_t166_entrega_corpus.py` y la de T-143 que compara V5.1 → V5.2 leyendo la V5.2 del histórico.
  - Referencias vivas a la ruta de la V5.2: `prompts/FASE0_VERIFICADOR_IDS.md`, `prompts/FASE3_GOLDENS_CONTRATOS.md`, `bloque_a/11_Ejecutor/README.md`, `tests/MAPA_PLAN_DE_PRUEBAS.md`, `config/por_defecto.yaml` (línea 2), docstring de `contratos.py` y de `respuesta_final.py` (cita la V5.1), el generador del borrador del Anexo B y lo que diga `tools/refs_vivas.py`.
  - `docs/auditoria_ids_bloque_a.json` y `docs/auditoria_ids_bloque_a.md` regenerados; INC-T157-03 a 05 «aplicada en T-166»; INC-T166-01 (sin `.docx`); INC-T162-01 «descrita en el Anexo B V5.3»; filas D-2 a D-4 del registro de decisiones.
  - Re-congelado del corpus con `tools/corpus_integridad.py --update`.
- No entra:
  - cambiar el código de producción del ejecutor (manda el código; el Anexo B lo describe);
  - el `method_id` ficticio «MET-TASA-BASE-REL» del ejemplo del Registro de cálculos (D-3 solo cambia la ficha y su versión de Catálogo);
  - otros textos del corpus con «V4.0» que no son el Catálogo (cabeceras «Bloque A V4.0», «Mapa de conocimientos V4.0», Anexo G);
  - renombrar los prompts: su nombre «Versión óptima V5.0» es el del diseño del agente; el ejecutor los busca por nombre de agente y registra la huella del texto (`Prompts.version`);
  - `CLAUDE.md` (dice 696 archivos y la trampa «Catálogo V4.0»): solo lo cambia el operador en su sesión; se deja el texto propuesto en el análisis técnico para la sesión coordinadora;
  - `bloque_b/`, `sistema_global/marco_comun_c/`, la Constitución y la fila T-166 de la deuda;
  - generar `.docx`.

## Diseño

### Decisiones `[PROPUESTO]` (agente, por la regla del 13-11-2026)

- **V5.3, no corrección dentro de la V5.2.** Cada entrega deja huella: la V5.2 se conserva sin cambios en `99_Historico_V5.2/01_Gobernanza/` y la V5.3 la sustituye en `01_Gobernanza`, como hizo T-143. Cambia el texto de un anexo, no los formatos: `version_contrato` sigue en "5.1".
- **Los prompts y los demás archivos corregidos se editan en su sitio, con el mismo nombre.** El ejecutor carga el prompt por el nombre del agente (`prompts.NOMBRES_ALTERNATIVOS` y `configuracion.buscar_versionado`, versión más alta de `02_System_prompts`); un nombre nuevo no aporta nada y el texto ya queda trazado por su huella. Las versiones anteriores (`.md` y su `.docx`) van a `99_Historico_V5.2/` con la misma subcarpeta, para que el estado del corpus de la V5.2 se pueda reconstruir y ningún `.docx` vivo quede desfasado de su `.md`.
- **RF-0046** para RF-0123 (motivo arriba).
- **El Anexo B describe la final con frases fijas** que una prueba compara con `respuesta_final.ESQUEMA`, `RESULTADOS`, `ESTADO_F5`, `CONFIANZAS` y `PATRON_REF`; el esquema derivado de CT-03.RETORNO admite `respuesta_final` (opcional: la provisional y la N0 no lo llevan) con sus dos campos y los cinco resultados.

- Contratos CT afectados: ninguno cambia de formato. CT-03 ya emite la final desde T-162; el Anexo B la describe.
- Estado persistido: no cambia.
- Números: ninguno nuevo.
- Cómo falla cerrado: las pruebas nuevas fallan si vuelve «Catálogo V4.0» a un prompt MC, si el verificador vuelve a dar un error, o si el Anexo B y `respuesta_final.py` dejan de decir lo mismo (mutantes de código y de prosa).

## Ronda r02 (QA r01 NO APTO)

Hallazgos de `qa.md` (r01), corregidos con el texto exacto que propone el revisor. Cambia el Documento 0 V5.3 (aún no publicado en `develop`): se re-congelan el manifiesto y `huellas.json`, y el histórico no cambia. Sin cambios de código del ejecutor:

- H-01 (media): la última frase del párrafo enumera `respuesta_final.ERRORES_DE_CONTROL` y dice que cualquier otro error da FALLIDO; la frase de las pendientes, la excepción (integridad o control paran la consulta o el ciclo). Frases fijas al día y mutantes de código y de prosa nuevos.
- H-02 (media): sin RUN- el sobre no lleva `run_id`; la copia de la final en F5 lo deja nulo.
- H-03 (media): «antes de escribir la final en F5 (un rechazo de la mensajería deja su incidencia en HA, como con cualquier mensaje)».
- H-04: las cuatro frases fijas y los seis mutantes de prosa de `revisores/r01_02` en `MUTANTES_PROSA`.
- H-05: la prueba parametrizada de la confianza sin resultado (de `revisores/r01_01`).
- H-06: `tests/goldens/README.md` (l. 14) y `docs/auditoria_ids_bloque_a.md` (D-2 a D-4 aplicadas por T-166).

Criterios de la r02: CA-10, H-01 a H-06 corregidos; CA-11, `revisores/r01_02` da 0 vivos y `r01_03` no deja vivo en T-166 ningún mutante que no maten T-162 y T-169; los demás, como en la r01.

## Ronda r03 (QA r02 NO APTO)

Un hallazgo, H-07 (media): la frase de las finales pendientes de la r02 decía que todo error de control para la consulta, pero `DatosSensibles` y `MensajeInvalido` (`RECHAZOS_SIN_EFECTO`) se apartan. Se corrige con el texto exacto de `qa.md`: «…se aparta una vez con una incidencia escalada al operador, también si la rechazan su esquema o la mensajería (R8 o un mensaje que no cumple su contrato), salvo un fallo de integridad o cualquier otro error de control, que para la consulta o el ciclo.» Frase fija, `rechazos` en `_codigo` y `_final_que_difiere`, un mutante de código y otro de prosa, y la prueba de `revisores/r02_01` (dos casos) en CA-5. Re-congelado del manifiesto (solo la V5.3) y de `huellas.json`; auditoría de IDs regenerada. Criterio de la r03: CA-12, H-07 corregido y `r02_01` en verde; los demás, como en la r02.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Cambia el texto de un prompt y algo del ejecutor o un golden dependía de él | Suite roja o golden que cambia sin motivo | Suite completa de A; `goldens_ct.py`; el diff del manifiesto solo con las rutas de la tarea |
| Mover un `.docx` rompe una prueba o un gate | Gate rojo | `check_all.sh --core`, `refs_vivas.py`, `nfc_check.py` |
| El párrafo de la final dice algo que el código no hace | El Documento 0 vuelve a mentir | Cada frase sale de `respuesta_final.py`; las comprobables, con prueba y mutantes |
| Re-congelar trabajo ajeno | Se congela algo de otra sesión | Worktree limpio sobre `origin/develop`; diff del manifiesto revisado línea a línea |

## Criterios de aceptación (binarios)

1. CA-1: ningún `.md` vivo del corpus del Bloque A (sin `11_Ejecutor/` ni `99_Historico*`) cita «Catálogo V4.0», y los prompts MC-01 a MC-05 citan «Catálogo V5.0» donde antes citaban V4.0.
2. CA-2: el verificador de IDs sobre el corpus termina con 0 errores y sin el AVISO MENCION_OTRA_VERSION; el ejemplo del Registro de cálculos cita FC-EVAL-001 con `catalog_version` "5.0", y el prompt del Evaluador, RF-0046, que existe en F9.
3. CA-3: en `01_Gobernanza` solo está la V5.3; la V5.2 está en `99_Historico_V5.2/01_Gobernanza/` con su SHA-256 del manifiesto; fuera del Anexo B, la V5.3 solo difiere de la V5.2 en la cabecera de versión y en una fila nueva del Anexo F; dentro del Anexo B, solo en el párrafo de CT-03 (y la mención de versión de «Cómo se lee este anexo»).
4. CA-4: los ocho archivos corregidos tienen su versión anterior (`.md` y `.docx`) en `99_Historico_V5.2/` con los SHA-256 del manifiesto anterior, y difieren de ella solo en las líneas de D-2 a D-4.
5. CA-5: el Anexo B V5.3 describe `respuesta_final` con los campos, los cinco resultados, el estado común de cada uno, los prefijos de las referencias y las reglas de referencias y de confianza de `respuesta_final.py`; una prueba lo compara con el código y mutantes de código y de prosa la hacen fallar.
6. CA-6: el esquema derivado de CT-03.RETORNO admite `respuesta_final` y lo valida; `divergencias_anexo_b.json` sigue sin diferencias medidas; `aceptaciones_rechazos.json` no cambia; `goldens_ct.py` termina en 0 y el re-congelado está en `goldens/REGISTRO.md`.
7. CA-7: el ejecutor sigue encontrando los prompts corregidos (`Prompts.archivo` de AG-13 y de los MC, y AG-20) y su texto es el nuevo.
8. CA-8: el diff del manifiesto solo toca las rutas de esta tarea; `corpus_integridad.py` y `refs_vivas.py` pasan.
9. CA-9: suite completa de A ≥ 607 y en verde; ruff ≤ 2813 y mypy de A ≤ 109; gates ligeros en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t166_*` de «Catálogo V4.0» en prompts y corpus vivo | regresión, fallo cerrado | CA-1 |
| `test_t166_*` del verificador sobre el corpus real (0 errores) y de las entradas D-3 y D-4 | integración | CA-2 |
| `test_t166_*` de la V5.3 frente a la V5.2 del histórico y de los ocho archivos frente a su versión anterior | regresión | CA-3, CA-4 |
| `test_t166_*` del párrafo de la final frente a `respuesta_final.py` (con mutantes parametrizados) | contrato, fallo cerrado | CA-5 |
| Flujo `consulta_que_escala`: la final cumple el derivado; `goldens_ct.py` | contrato | CA-6 |
| `Prompts.archivo` y `Prompts.texto` | integración | CA-7 |
| `corpus_integridad.py`, `git diff -U0 tools/corpus_manifest.txt`, `refs_vivas.py` | integración | CA-8 |
| `pytest -q` de A, cuotas, `check_all.sh --core` | integración | CA-9 |

## Scripts

- `tools/corpus_integridad.py --update`, `bloque_a/11_Ejecutor/tests/goldens_ct.py --update --motivo`, `python -m bloque_a.herramientas.verificador_ids --json … --auditoria …`, `.docs/scripts/borrador_anexo_b.py --comprobar`, `.docs/scripts/evidencias_plan_a.py`.

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan y criterios
- 2026-11-17 · EN CURSO · claude · implementación en una copia limpia sobre `origin/develop`
- 2026-11-17 · EN QA (r01) · claude · implementado y probado; falta la QA r01 con un revisor nuevo sin contexto
- 2026-11-17 · EN CURSO · claude · ronda r02 (QA r01 NO APTO: H-01 a H-06)
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · ronda r02 implementada y probada; falta la QA r02
- 2026-11-17 · EN CURSO · claude · ronda r03 (QA r02 NO APTO: H-07)
- 2026-11-17 · EN QA (r03: QA r02 NO APTO) · claude · ronda r03 implementada y probada; falta la QA r03
- 2026-11-17 · CERRADO · claude (revisor) · QA r03 APTO: H-01 a H-07 corregidos y verificados con el ejecutor
