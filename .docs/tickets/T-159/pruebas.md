# T-159 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A, `bloque_a/11_Ejecutor` (recogidas) | 6674 | 6684 (+10 de `tests/test_t159_extremo_a_extremo.py`) |
| Bloque A, suite completa | — | 6682 superadas, 2 omitidas, código 0 (47 min 52 s, máquina compartida con otras suites) |
| `tests/test_fase4_mapa.py` | 23 | 23 (un caso parametrizado pasa de PB-02 a PB-08, ver abajo) |
| `.docs/scripts/pruebas_scripts.sh` | — | 231 superadas |
| Evidencias del plan | 21 Superada · 37 en parte · 171 pruebas citadas | 29 Superada · 29 en parte · 181 de 181 pruebas citadas superadas |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | Tabla de los 37 en `analisis-tecnico.md`: 8 A, 27 B, 2 C |
| CA-2 | PB-02 `test_pb02_dos_opciones_y_la_de_banda_marginal_fuera_con_su_segunda_pasada`; PB-03 `test_pb03_alt_sin_vehiculo_minorista_queda_sin_opciones_y_en_gris`; PB-30 `test_pb30_la_cifra_sin_artefacto_bloquea_se_retira_y_lo_entregado_no_la_lleva`; PB-39 `test_pb39_el_visual_por_debajo_de_70_se_bloquea_y_tras_la_reescritura_se_entrega` y `test_pb39_si_la_reescritura_sigue_por_debajo_de_70_no_se_entrega_ningun_visual`; PB-41 `test_pb41_el_factor_comun_de_rf_reit_y_rv_queda_en_un_cluster_y_los_tres_entregables_coinciden`; PB-44 `test_pb44_el_historial_publicado_es_el_recuento_de_f4_con_su_muestra_y_el_mismo_dato_en_los_informes`; PB-47 `test_pb47_un_metodo_documentado_no_se_usa_y_la_entrega_lo_declara`; PB-67 `test_pb67_el_ciclo_c6_propone_el_envio_a_b_sin_enviar_nada` (todas en `tests/test_t159_extremo_a_extremo.py`, 10 superadas en unos 45 s) |
| CA-3 | `.venv/bin/python .docs/scripts/evidencias_plan_a.py` → «67 pruebas del plan, 181 pruebas automáticas citadas y todas existen · AUTOMATICA 29, DOCUMENTAL 1, PARCIAL 29, PENDIENTE_API 7, REQUIERE_USUARIOS 1»; `tests/test_fase4_mapa.py` 23 superadas |
| CA-4 | `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` → «escrito docs/evidencias_pruebas_bloque_a.md · 181 de 181 pruebas citadas superadas», código 0 (6 min 53 s) |
| CA-5 | INC-T159-01 en `docs/incidencias.md` (diez casos) |
| CA-6 | Suite completa de A (arriba), gates ligeros y cuotas (abajo) |

Fallo cerrado: `test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega` (PB-52, parte cumplida: nada se entrega, nada se
congela, ningún G3V-). La misma situación muestra lo que falta (PB-52 pasa a B, INC-T159-01).

## Regresiones

No hay correcciones de código: no aplica «falla sin la corrección». Cada prueba comprueba antes que su siembra ocurrió (papeles
de las candidatas en PB-02, finalistas de ALT en PB-03, el CALC- sin artefacto ausente del RC en PB-30, dos llamadas a AG-17 y un
primer visual por debajo de 70 en PB-39, el clúster común en PB-41, la NO_RESOLUBLE en PB-44, el rechazo de ML-CLUS-001 en
PB-47 y la recomendación dentro de doce semanas en PB-67).

`tests/test_fase4_mapa.py::test_ca6_un_mapa_estropeado_se_detecta`: el caso que dejaba en blanco el «no comprueba» de PB-02 dependía
de que PB-02 fuera PARCIAL; ahora lo hace sobre PB-08, que sigue PARCIAL. Comprueba lo mismo (una fila PARCIAL sin «no comprueba»
es un problema); no se debilita.

## Gate

Gates ligeros, desde la raíz:

| Gate | Resultado |
| --- | --- |
| `tools/refs_vivas.py` | «todas las rutas citadas en CLAUDE.md/prompts/docs existen» |
| `tools/secrets_scan.py` | «sin hallazgos (allowlist aplicada)» |
| `tools/nfc_check.py` | «todos los nombres de archivo en forma canónica» |
| `tools/corpus_integridad.py` | «695 archivos coinciden con el manifiesto congelado» |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2831 (cuota 2831; no sube) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109; no se toca el paquete) |

`./tools/check_all.sh` completo no se ejecutó (encargo: gates ligeros y la suite de A una vez; hay otras suites corriendo en la
máquina).

Comandos:

- desde `bloque_a/11_Ejecutor`: `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t159_extremo_a_extremo.py tests/test_fase4_mapa.py`
- suite completa, desde `bloque_a/11_Ejecutor`: `../../.venv/bin/python -m pytest -q -p no:cacheprovider`
- desde la raíz: `.venv/bin/python .docs/scripts/evidencias_plan_a.py`, `--ejecutar`, `bash .docs/scripts/pruebas_scripts.sh` y los
  cuatro `tools/*.py` de la tabla.
