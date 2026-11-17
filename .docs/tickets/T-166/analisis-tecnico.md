# T-166 · Análisis técnico

## Causa raíz o motivo

La auditoría de identificadores de T-157 (`docs/auditoria_ids_bloque_a.md`) dejó dos errores y un aviso en el corpus congelado del Bloque A, propuestos como D-2 a D-4: el «Catálogo V4.0» en los prompts MC-01 a MC-05 y en las funciones del Motor (el vigente es V5.0, 81 fichas), la ficha inexistente FX-MC10-003 (con `catalog_version` 4.0) en el ejemplo del Registro de cálculos y la RF inexistente RF-0123 en el ejemplo del prompt del Evaluador. El operador las delegó en el agente el 16-11-2026 y el agente las decidió así: se corrigen en una nueva entrega del corpus, antes de la Fase 5, porque con la API real esos prompts llegan tal cual al modelo (`sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`, §6). Además, T-162 y T-169 añadieron la respuesta final de CT-03 (`respuesta_final`), que el Anexo B V5.2 no describía (INC-T162-01, que dejaba la descripción para la siguiente entrega del Documento 0).

## Evidencia

- Antes: `verificador_ids` sale con 1 y da 2 errores (FICHA_CITADA_INEXISTENTE FX-MC10-003, REF_INEXISTENTE RF-0123) y 2 avisos (MENCION_OTRA_VERSION con 8 menciones, REF_FORMA_DISTINTA RF-1).
- Después: sale con 0, 0 errores y 1 aviso (RF-1, la tarjeta del informe visual del Auditor, que INC-T157-05 deja sin acción). `docs/auditoria_ids_bloque_a.json` y `docs/auditoria_ids_bloque_a.md` regenerados con el propio verificador.
- `goldens_ct.py`: solo cambian la huella del Documento 0 y la de `anexo_b_esquemas.json` (en `huellas.json`); `divergencias_anexo_b.json`, `mensajes_ejemplo.json`, `formas_flujos_mock.json` y `aceptaciones_rechazos.json` no cambian.

Reproducir (desde `bloque_a/11_Ejecutor`): `../../.venv/bin/python -m bloque_a.herramientas.verificador_ids >/dev/null; echo $?` → 0.

## Implementación

### Archivos

Corpus (re-congelado):

- `bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md` (nuevo): la V5.2 con la cabecera de versión (título, fecha, «Sustituye a», «Actualizado»), una fila nueva en el Anexo F, «Cómo se lee este anexo (V5.2 y V5.3)» y, en el párrafo de CT-03 del Anexo B, una línea nueva «Respuesta final (V5.3)» (no empieza por `**`, así que `goldens_ct.parrafos_anexo_b` la cuenta en CT-03).
- `bloque_a/99_Historico_V5.2/` (nuevo): la V5.2 del Documento 0 (movida con `git mv`; no tenía `.docx`) y la versión anterior de los ocho archivos corregidos: el `.md` copiado y el `.docx` movido con `git mv`, en su misma subcarpeta. Los SHA-256 son los del manifiesto anterior (ver «Corpus»).
- Corregidos en su sitio y con el mismo nombre:
  - `02_System_prompts/System prompt - MC-01 … MC-05 … - Versión óptima V5.0.md`: «Catálogo V4.0» → «Catálogo V5.0» (seis sitios: la regla 1 de MC-01 y los cinco ejemplos JSON);
  - `03_Funciones/Funciones, tareas y cometidos – Motor de Cálculo Avanzado … – óptima V5.0.md`: MOTOR-F05, ídem;
  - `05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0).md`: `"ficha_id":"FC-EVAL-001"` y `"catalog_version":"5.0"` (`ficha_version` 1.0 ya era la de FC-EVAL-001; `modulos` ya era `["MC-10"]`);
  - `02_System_prompts/System prompt - Evaluador de Previsiones y Aprendizaje - Versión óptima V5.0.md`: `"ref_id":"RF-0046"`.
- `bloque_a/README - Índice de la entrega y registro de la actualización V5.1.md`: fila de `01_Gobernanza` (V5.3), fila nueva `99_Historico_V5.2` y entrada del registro (§8). La entrada no cita los identificadores viejos (el verificador lee este README y los contaría: lo vi en la primera pasada, con 1 error y 1 aviso).

Fuera del corpus:

- `bloque_a/11_Ejecutor/tests/goldens/anexo_b_esquemas.json`: CT-03.RETORNO admite `respuesta_final` (no exigido) con `provisional_msg_id` y `resultado_analisis` (los cinco resultados), y su `$comment` lo dice; los 38 `$comment` dicen «derivado del Anexo B del Documento 0 V5.3». Re-congelado con `goldens_ct.py --update --motivo` (línea en `goldens/REGISTRO.md`).
- `bloque_a/11_Ejecutor/tests/test_t166_entrega_corpus.py` (nuevo) y `tests/test_fase3_goldens.py` (la prueba de T-143 lee la V5.2 del histórico; la lista de huellas cita la V5.3).
- Referencias vivas a la V5.2: `prompts/FASE0_VERIFICADOR_IDS.md`, `prompts/FASE3_GOLDENS_CONTRATOS.md`, `bloque_a/11_Ejecutor/README.md` y `tests/MAPA_PLAN_DE_PRUEBAS.md` (línea 3), `config/por_defecto.yaml` (comentario de la línea 2), docstring de `contratos.py` (línea 1) y de `respuesta_final.py` (una frase: el Anexo B V5.3 describe la final). Ningún cambio de código ejecutable.
- `.docs/scripts/borrador_anexo_b.py` y `.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`: la ruta de la V5.2 en el histórico, la V5.3 como vigente y «Lo que queda contra la V5.3»; `--comprobar` pasa.
- `.docs/tickets/T-143/README.md` y `analisis-tecnico.md`, y `docs/incidencias.md` (ronda T-143 de INC-T114-01): la ruta de la V5.2 pasa a la del histórico con la nota «en `01_Gobernanza` hasta T-166». Es lo único que se toca de un ticket cerrado: `refs_vivas.py` exige que la ruta citada exista, y la lista `tools/refs_allowlist.txt` es solo para entregables futuros.
- `docs/incidencias.md`: INC-T157-03, 04 y 05 «aplicada en T-166»; INC-T162-01 «descrita en el Anexo B V5.3»; INC-T166-01 nueva (sin `.docx` y decisiones `[PROPUESTO]`).
- `docs/auditoria_ids_bloque_a.json` y `docs/auditoria_ids_bloque_a.md`: el informe regenerado y, fuera de las marcas, el texto y la tabla de decisiones con «aplicada por T-166».
- `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`: filas D-2, D-3 y D-4 «Aplicada en T-166» y la de «Nueva entrega del Documento 0» con la V5.3.
- `tools/corpus_manifest.txt`: re-congelado.

### Decisiones y desviaciones del plan

Todas `[PROPUESTO]`, del agente, por la delegación del operador del 16-11-2026 (y la regla del 13-11-2026):

- **V5.3 y no una corrección dentro de la V5.2.** Cada entrega deja huella, como T-143: la V5.2 se conserva sin cambios y el Anexo F tiene su fila. El cambio es de texto de un anexo; `version_contrato` sigue en «5.1».
- **Los archivos corregidos conservan su nombre.** El ejecutor carga los prompts por el nombre del agente (`prompts.NOMBRES_ALTERNATIVOS` + `configuracion.buscar_versionado` sobre `02_System_prompts`, versión más alta) y registra la huella del texto que envía (`CatalogoPrompts.version`): un sufijo nuevo no aporta trazabilidad y obligaría a renombrar también su `.docx`. Los prompts MC no los carga el ejecutor (el Motor es determinista: no hay agente MC en `NOMBRES_ALTERNATIVOS`); el del Evaluador (AG-20), sí, y la prueba CA-7 lo comprueba.
- **Histórico `99_Historico_V5.2/`** con lo que esta entrega sustituye, en su misma subcarpeta, `.md` y `.docx`. Así ningún `.docx` vivo queda desfasado de su `.md` y el corpus de la V5.2 se reconstruye entero. Es lo que hizo T-143 con el Documento 0 (lo movió con su `.docx`); aquí, para los ocho archivos que siguen vivos, el `.md` se copia y el `.docx` se mueve. Ningún `.docx` se edita ni se genera (INC-T166-01).
- **RF-0046** (Goldman Sachs Global Investment Research): TF-05, «Análisis de bancos de inversión y casas de análisis», fuente de opinión con previsiones de estrategia, «Aprobada» y fuera del Registro de bajas. El ejemplo es un informe del Evaluador con la celda RV×H3, y `fiabilidad_fuentes` mide el historial de las fuentes de opinión para el Buscador (los extractos por destinatario del mismo prompt). Es ficticio en las cifras (`n`, `bss_shrunk`), como el resto del ejemplo; la ficha de F9 dice «Historial: sin uso observado», que es su estado real y no lo contradice el ejemplo.
- **`method_id` «MET-TASA-BASE-REL»** del ejemplo del Registro de cálculos no se toca: D-3 decide la ficha y su versión de Catálogo. El ejecutor escribe `method_id` RI-TB para la tasa base; queda anotado aquí, sin incidencia, porque el ejemplo es ficticio y el `method_id` no es un identificador del Catálogo.
- **Respuesta final en el Anexo B.** Una línea en el párrafo de CT-03 con frases fijas que `test_t166_entrega_corpus.py` compara con `respuesta_final.ESQUEMA`, `RESULTADOS`, `ESTADO_F5`, `CONFIANZAS` y `PATRON_REF` (y con `_resultado` y `_menos_confiada`). `respuesta_final` se marca opcional en el retorno CT-03 («solo la lleva la final»), que es lo que exige la regla de lectura del propio Anexo B para un campo que el derivado no exige. La final sí lo exige: lo dice «La final lleva …, y ningún otro campo».
- **Esquema derivado.** CT-03.RETORNO admite `respuesta_final` con sus dos campos exigidos y los cinco resultados. No se añade un ejemplo nuevo a `anexo_b_ejemplos.json` (una clave por contrato y sentido; el ejemplo N0 sigue cumpliendo); la prueba CA-6 valida una final contra el derivado y `test_t162_respuesta_final.py` ya valida la final real del flujo simulado contra él.
- **CLAUDE.md no se toca** (como en T-143): solo lo cambia el operador en su sesión, y ninguna ruta suya queda rota. Quedan desfasadas dos frases, que propongo a la sesión coordinadora:
  - «El corpus canónico congelado por hash (696 archivos …)» → «(705 archivos …)»;
  - en «Trampas conocidas», «los prompts MC congelados citan "Catálogo V4.0"; el catálogo entregado es V5.0» → «desde T-166 (17-11-2026) los prompts MC citan el Catálogo V5.0, el entregado (81 fichas); la versión anterior está en `bloque_a/99_Historico_V5.2/`».
- **La fila T-166 de la deuda técnica** no se toca: la actualiza la sesión coordinadora.

### Corpus

`.venv/bin/python tools/corpus_integridad.py --update` (696 → 705 archivos). Diff del manifiesto (`git diff -U0 tools/corpus_manifest.txt`), 45 líneas:

- quitadas (18): la V5.2 de `01_Gobernanza`; los ocho `.docx` y los ocho `.md` corregidos con su hash anterior; el README índice con su hash anterior;
- puestas (27): la V5.3 (`05a825a3…`); los ocho `.md` corregidos con su hash nuevo; el README índice (`e25d7eb7…` → `b3c4d7b1…`); en `99_Historico_V5.2/` la V5.2 (`d8f9e3d0…`, el mismo hash) y los ocho `.md` y los ocho `.docx` con **los mismos hashes** que tenían en `02_System_prompts`, `03_Funciones` y `05_Archivos_operativos`.

Ninguna otra entrada cambia: 696 − 1 (V5.2) − 8 (`.docx`) + 1 (V5.3) + 17 (histórico) = 705.

**Texto del motivo para el commit:**

> fase0: Bloque A, T-166, entrega del corpus decidida por delegación del operador el 16-11-2026 (D-2 a D-4 de T-157): «Catálogo V4.0» → «V5.0» en los prompts MC-01 a MC-05 y en MOTOR-F05, FC-EVAL-001 con catalog_version 5.0 en el ejemplo del Registro de cálculos, RF-0046 en el ejemplo del Evaluador; Documento 0 V5.3 con la respuesta final de CT-03 en el Anexo B (T-162, T-169). La V5.2 y la versión anterior de los ocho archivos (.md y .docx, sin cambios) pasan a bloque_a/99_Historico_V5.2; sin .docx nuevos (INC-T166-01). Re-congelado deliberado del corpus con tools/corpus_integridad.py --update por ese motivo (696 → 705: solo las rutas de la entrega y el README índice) y de los goldens con goldens_ct.py --update --motivo (solo huellas.json; anexo_b_esquemas.json admite respuesta_final). Verificador de IDs: 0 errores [pendiente QA]

### Límites conocidos

- Las frases fijas de la final son las que la prueba sabe leer: un cambio de redacción que las rompa hace fallar la prueba (falla cerrado), y hay que actualizar la lista a propósito.
- Lo que no comparan las pruebas de la final con el código, sino con las pruebas de T-162 y T-169 que ya lo fijan: el texto exacto de `respuesta`, el orden de las referencias, el apartado de una final pendiente y qué errores paran la consulta (`test_t162_respuesta_final.py`, `test_t169_*`).
- El README índice tiene `.docx` (copia de consulta) que no se actualiza, como en T-143.
- `03_Funciones` y el Registro de cálculos no los lee el ejecutor; su corrección es para quien lea el corpus y para el verificador.

### Comandos para probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids >/dev/null; echo $?      # 0
../../.venv/bin/python tests/goldens_ct.py                                             # coinciden
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t166_entrega_corpus.py tests/test_fase3_goldens.py tests/test_t162_respuesta_final.py
cd ../..
.venv/bin/python tools/corpus_integridad.py && .venv/bin/python tools/refs_vivas.py && .venv/bin/python tools/nfc_check.py
.venv/bin/python .docs/scripts/borrador_anexo_b.py --comprobar
git diff -U0 origin/develop -- tools/corpus_manifest.txt
```

## Ronda r02 (QA r01 NO APTO)

### Qué cambia, hallazgo a hallazgo

| Hallazgo | Cambio | Dónde |
| --- | --- | --- |
| H-01 (media) | Última frase: «Un fallo de integridad del almacén o un error de control durante el análisis (los controles del almacén y de la mensajería, un mensaje que no cumple su contrato, una fuga de información de HT-01 o una respuesta sin grabar en el modo de reproducción: `respuesta_final.ERRORES_DE_CONTROL`) para la consulta: no hay provisional ni final; cualquier otro error da la final FALLIDO.» Pendientes: «…con una incidencia escalada al operador, salvo un fallo de integridad o un error de control, que para la consulta o el ciclo.» | Documento 0 V5.3; `test_t166_entrega_corpus.py`: `ERRORES_DE_CONTROL_EN_LA_PROSA` (cada clase de `ERRORES_DE_CONTROL` con su descripción, comparada con el código), dos frases fijas, mutantes de código «la fuga de información no para» y «otro error de control», tres de prosa y `test_ca5_los_errores_de_control_son_los_que_paran_la_consulta` (`PermissionError` cubre los controles del almacén y de la mensajería; otro error, FALLIDO) |
| H-02 (media) | «(si no, el sobre no lleva `run_id`, y la copia de la final en F5 lo deja nulo)» (`Mensajeria.crear` solo pone `run_id` si lo hay) | Documento 0; frase fija y dos mutantes de prosa |
| H-03 (media) | «…y por la mensajería antes de escribir la final en F5 (un rechazo de la mensajería deja su incidencia en HA, como con cualquier mensaje), sale una sola vez…» | Documento 0; frase fija y mutante de prosa |
| H-04 | Frases fijas: la primera entera, `` `escalado` (el mismo que la provisional) ``, la de `provisional_msg_id` y «La confianza es, con opciones, la más baja de las suyas en F3 (»; los seis mutantes de `r01_02` en `MUTANTES_PROSA` | `test_t166_entrega_corpus.py`; `r01_02`: vivos 0 |
| H-05 | `test_ca5_sin_resultado_la_confianza_es_la_mas_baja_entre_la_provisional_y_especulativo` (×4, con `nuevo_bloque` y una consulta sin escalado) | `test_t166_entrega_corpus.py`; M4 de `r01_03` muere |
| H-06 | `tests/goldens/README.md` l. 14: «…del Documento 0 V5.3 (hasta T-166, de la V5.2; hasta T-143, de la V5.1)»; `docs/auditoria_ids_bloque_a.md`: «…D-1 la aplicó después T-160, y D-2 a D-4, T-166.» | los dos archivos |

### Re-congelado

- `goldens_ct.py --update --motivo "T-166 r02 …"`: solo `huellas.json` (la huella del Documento 0, `05a825a3…` → `04046f02…`), con su línea en `goldens/REGISTRO.md`.
- `tools/corpus_integridad.py --update`: 705 archivos; frente a la r01, el diff del manifiesto es una sola línea (la V5.3, `05a825a3…` → `04046f02…`). Frente a `origin/develop`, las mismas rutas que en la r01. `git diff -- bloque_a/99_Historico_V5.2` vacío: el histórico no cambia.
- `docs/auditoria_ids_bloque_a.json` y `.md` regenerados (cita la huella del Documento 0): 0 errores, 1 aviso.

El texto del motivo del commit de la r01 sigue valiendo; se añade: «r02 (QA r01 NO APTO, H-01 a H-06): el párrafo de la respuesta final dice qué errores paran la consulta, que sin RUN- el sobre no lleva run_id y que un rechazo de la mensajería deja su incidencia en HA».

## Ronda r03 (QA r02 NO APTO)

- **H-07 (media).** En `enviar_pendientes`, `except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO)` aparta la pendiente con el almacén íntegro: `DatosSensibles` (R8) y `MensajeInvalido` no paran aunque estén en `ERRORES_DE_CONTROL`. La frase de las pendientes del Documento 0 V5.3 pasa a «…se aparta una vez con una incidencia escalada al operador, también si la rechazan su esquema o la mensajería (R8 o un mensaje que no cumple su contrato), salvo un fallo de integridad o cualquier otro error de control, que para la consulta o el ciclo.».
- **`test_t166_entrega_corpus.py`:** frase fija nueva; `rechazos` (`RECHAZOS_SIN_EFECTO`) en `_codigo` y su comprobación en `_final_que_difiere`; mutante de código «un rechazo más se aparta» y de prosa (quitar el inciso); el mutante de prosa de la excepción, con el texto nuevo; `test_ca5_los_rechazos_de_la_mensajeria_son_de_control_y_no_paran_se_apartan` (DatosSensibles y MensajeInvalido, de `revisores/r02_01`). Orden de los imports arreglado (`ruff --fix`, I001).
- **Re-congelado:** `goldens_ct.py --update --motivo "T-166 r03 …"` (solo `huellas.json`, Documento 0 `04046f02…` → `12cc5182…`, con su línea en `REGISTRO.md`); `corpus_integridad.py --update` (705; frente a la r02, solo la línea de la V5.3; el histórico no cambia); auditoría de IDs regenerada (0 errores, 1 aviso).
