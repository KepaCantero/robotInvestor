# T-194 · Pruebas

Estado tras la ronda r02 (QA r01 NO APTO). Las cifras de rondas anteriores están en «Historia», al final.

| Suite | Antes de T-194 | r02 |
| --- | --- | --- |
| `pruebas_cola_astra.py` (pytest, recogidas) | 0 (el script tenía `main`, sin `test_`; a mano daba 5 FALLA de 13) | 50 superadas |
| `pruebas_autor_generico.py` | 12 (una leía la cola real) | 12 (ninguna lee la cola real) |
| `.docs/scripts/pruebas_scripts.sh` | 349 (línea base 349) | 399 superadas (línea base 399) |
| `.docs/tickets/T-194/mutantes.py` | — | 49 de 49 muertos |
| `revisores/r01_aislamiento.sh`, `r01_ruta_no_ascii.py` y `r01_mutantes_revisor.py` | — | en verde (rc 0) |
| `.venv/bin/ruff check` de los ficheros tocados | 0 en el `pruebas_cola_astra.py` viejo | 0 en `pruebas_cola_astra.py`, `pruebas_autor_generico.py`, `cola_astra.py` y `mutantes.py` |
| Bloques A, A-Forex, B | sin tocar | sin tocar |

## Criterio de aceptación → prueba

| Criterio | Prueba (`.docs/scripts/pruebas_cola_astra.py` salvo que se diga) |
| --- | --- |
| CA-1 | `pruebas_scripts.sh` cuenta 399 |
| CA-2 | La fixture `repo` hace `git init` en `tmp_path` y escribe la cola (`FILAS`). `revisores/r01_aislamiento.sh` lo comprueba sin la cola real, con un git config, un `.env` y unas variables `GIT_*` personales: pasan las 50 y las 12 de `pruebas_autor_generico.py`, y la salida no lleva el autor |
| CA-3 · cola limpia y la siguiente | `test_cola_limpia_sin_errores_y_la_siguiente_es_la_primera_pendiente` |
| CA-3 · HECHA sin entregable | `test_hecha_sin_entregable_es_error`, `test_hecha_con_el_entregable_sin_commit_es_error` |
| CA-3 · borrador | `test_hecha_con_un_borrador_es_error` (en minúsculas y con espacios delante) |
| CA-3 · HECHA con entregable | `test_hecha_con_el_entregable_no_da_error_y_pasa_a_la_siguiente`, `test_h03_una_revision_anterior_a_la_cola_cuenta` |
| CA-3 · entregable sin marcar | `test_entregable_sin_marcar_hecha_es_aviso`, `test_qa_con_veredicto_sin_marcar_es_aviso` |
| CA-3 · sección del rediseño de B | `test_la_revision_de_b_sin_la_seccion_del_rediseno_es_error`, `test_la_seccion_del_rediseno_solo_la_pide_la_revision_de_b` |
| CA-3 · EN CURSO viejo | `test_en_curso_viejo_es_aviso_y_es_la_siguiente`, `test_en_curso_el_limite_de_tres_dias`, `test_en_curso_sin_fecha_es_aviso`, `test_los_dias_de_en_curso_son_los_del_docstring` |
| CA-3 · dos EN CURSO | `test_dos_en_curso_a_la_vez_es_aviso_y_manda_la_primera` |
| CA-3 · cambios sin commit | `test_cambios_sin_commit_en_un_entregable_es_aviso`, `test_un_entregable_nuevo_sin_anadir_en_una_carpeta_con_commit_es_aviso`, `…_en_una_carpeta_nueva_es_aviso` (INC-T194-01), `test_h07_un_entregable_con_ruta_no_ascii_y_cambios_sin_commit_es_aviso` (2 casos) |
| CA-3 · QA anterior a la cola | `test_qa_marcada_con_un_qa_md_anterior_a_la_cola_es_error`, `test_qa_del_mismo_dia_de_la_cola_cuenta`, `test_qa_sin_veredicto_rellenado_es_error` (3 casos); para IMPLEMENTAR, `test_h02_implementar_con_un_readme_anterior_a_la_cola_es_error` |
| CA-3 · RETIRADA | `test_retirada_con_entregable_no_avisa`, `test_retirada_no_es_la_siguiente_y_se_cuenta`, `test_sin_pendientes_no_hay_siguiente` |
| CA-3 · estado desconocido | `test_estado_desconocido_es_aviso` (3 casos) |
| CA-3 · además | `test_implementar_cuenta_por_el_estado_del_ticket` (3 casos), `test_h03_el_estado_del_ticket_es_el_de_su_fila_a_principio_de_linea`, `test_h02_un_tipo_desconocido_marcado_hecha_es_error`, `test_una_fila_con_columnas_de_menos_es_error`, `test_h03_una_fila_rota_tambien_es_error_en_json`, `test_json_da_la_cuenta_la_siguiente_y_los_errores` |
| CA-4 | `test_con_el_autor_generico_del_git_config_no_hay_error_de_autor`, `test_un_git_config_personal_es_error_sin_repetirlo` (3 casos), `test_un_env_personal_en_la_raiz_es_error_aunque_el_git_config_sea_generico` (2 casos), `test_h03_un_env_generico_entre_comillas_vale_aunque_el_git_config_sea_personal`, `test_el_entorno_generico_manda_sobre_un_git_config_personal`, `test_el_entorno_generico_manda_sobre_un_env_personal`; en `pruebas_autor_generico.py`, `test_la_cola_da_error_con_un_autor_personal`, ahora con su propia cola (H-06) |
| CA-5 | `.docs/scripts/linea_base_pruebas.txt` = 399; `pruebas_scripts.sh` en verde |
| CA-6 | `.docs/tickets/T-194/mutantes.py`: 49 mutantes, 49 muertos |
| CA-7 | Gate (abajo) |

## Hallazgos de la QA r01 → regresión

| Hallazgo | Corrección | Prueba de regresión | Mutante |
| --- | --- | --- | --- |
| H-01 (baja) | `unset COLA_ASTRA_SCRIPT` en `pruebas_scripts.sh` antes de pytest | `test_h01_pruebas_scripts_quita_cola_astra_script_antes_de_pytest`; `r01_aislamiento.sh` paso 3 en OK | — (es del gate, no de `cola_astra.py`) |
| H-02 (media) | dos pruebas | `test_h02_implementar_con_un_readme_anterior_a_la_cola_es_error`, `test_h02_un_tipo_desconocido_marcado_hecha_es_error` | M43 (R01), M44 (R02) |
| H-03 (baja) | tres pruebas, y una cuarta para R03 | `test_h03_una_revision_anterior_a_la_cola_cuenta`, `test_h03_el_estado_del_ticket_es_el_de_su_fila_a_principio_de_linea`, `test_h03_una_fila_rota_tambien_es_error_en_json`, `test_h03_un_env_generico_entre_comillas_vale_aunque_el_git_config_sea_personal` | M45 (R04), M46 (R06), M47 (R09), M49 (R03) |
| H-04 (baja) | `re.MULTILINE` y `_` donde no se usa `rc` | `.venv/bin/ruff check .docs/scripts/pruebas_cola_astra.py` → «All checks passed!» | — |
| H-05 (baja) | este fichero, `analisis-tecnico.md` y `handoff.md` al día | `grep -n "389\|41 muertos\|xfail" .docs/tickets/T-194/*.md` (salvo `qa.md`) solo devuelve la historia, marcada como tal | — |
| H-06 (baja) | la prueba de `pruebas_autor_generico.py` escribe su cola en `tmp_path` y simula todo `git`; no se quita (decisión del coordinador) | `r01_aislamiento.sh` paso 2 en OK | — |
| H-07 (baja) | `git -c core.quotePath=false status --porcelain --untracked-files=all` en `cola_astra.py` (autorizado por el coordinador) | `test_h07_…` (2 casos: con commit y nuevo), `r01_ruta_no_ascii.py` en OK | M48 |

- **Fallan sin el cambio:**
  - Contra el `cola_astra.py` de la r01b (`4a3fd27`), fallan los dos casos de H-07 y pasan las otras 47 que había entonces.
  - Las de H-02 y H-03 las comprueban sus mutantes.
  - La de H-01 falla con el `pruebas_scripts.sh` de `4a3fd27`, que no tiene el `unset`.
- **Mutantes del revisor** (`r01_mutantes_revisor.py`): 9 de 9 muertos. Antes de la r02 vivían R01, R02, R03, R04, R06 y R09.

## Gate

- El gate completo de `d5744b7` dio 12/12 (rc 0): ruff 2807, mypy A 102, A-Forex 174 y B 159; pytest A 8359, A-Forex 68 y B 176.
- La r01b y la r02 solo tocan `.docs/scripts` y el ticket, así que el completo no se relanza (instrucción del coordinador). La integración en `develop` lo vuelve a pasar todo con `commit_limpio.sh`.
- En la r02: `pruebas_scripts.sh` da 399 de 399, `mutantes.py` 49 de 49 muertos, `revisores/` en verde y ruff en 0 sobre los ficheros tocados.

## Historia

- **r01 (`d5744b7`):**
  - 41 recogidas: 40 superadas y 1 marcada `xfail` estricta por INC-T194-01.
  - `pruebas_scripts.sh` daba 389 superadas y 1 xfailed, con la línea base en 389.
  - 41 mutantes, 41 muertos. En la primera pasada vivieron M39 y M40.
- **r01b (`4a3fd27`):**
  - `--untracked-files=all`: la prueba de INC-T194-01 deja de ser `xfail`.
  - 41 superadas, línea base 390.
  - 42 de 42 mutantes muertos (M42).
