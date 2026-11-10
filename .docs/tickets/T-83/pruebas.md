# T-83 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `sistema_global/marco_comun_c/pruebas/pruebas_parametros_doc_t83.py` | no existía | 62 comprobaciones, TODAS LAS PRUEBAS PASAN (~3 s, con 6 subprocesos) |
| Baterías del marco (`.docs/scripts/pruebas_marco.sh`) | 60 pasan | 61 pasan, 0 fallan |
| `.docs/scripts/leeme_marco.py` | — | SIN DIFERENCIAS (0); la batería nueva ejecuta 62 y el LEEME cita 62 |
| pytest A · A-Forex · B (gate completo) | 317 · 68 · 176 | 317 · 68 · 176 (sin tocar) |

## Criterio de aceptación → prueba

| Criterio | Prueba (`pruebas_parametros_doc_t83.py`) |
| --- | --- |
| CA-1 | `cobertura_{PARAMETROS,CONFIG_DEFECTO,POLITICA_DEFECTO}_sin_documentar`, `cobertura_*_documentadas_que_no_existen`, `faltan_vacio_con_el_codigo_de_hoy`, `cobertura_cuenta_las_claves_del_codigo`, `las_tablas_son_las_del_codigo`, `politica_f_es_la_politica_de_F` |
| CA-2 | `defectos_de_forma_ninguno`, `registros_con_los_cuatro_campos`, `estado_valido_en_todos`, `fuente_no_vacia_y_bien_formada`, `fuente_existe_en_su_documento`, `fuente_inventada_no_existe`, `ratificado_cita_una_decision_ratificada_de_la_constitucion`, `los_ratificados_son_los_de_la_constitucion`, `justificacion_de_una_o_dos_frases`, `propuesto_con_pregunta`, `ratificado_con_pregunta`, `tecnico_sin_pregunta`, `pregunta_en_lenguaje_sencillo`, `preguntas_distintas`, `tecnico_solo_sin_numeros_y_en_la_configuracion`, `politica_f_tecnico_porque_sus_limites_van_uno_a_uno`, `los_modulos_declaran_sus_valores_de_partida_propuestos` |
| CA-3 | `marcas_coinciden_{PARAMETROS,CONFIG_DEFECTO,POLITICA_DEFECTO}`, `marcas_de_las_lecturas_de_PARAMETROS_coinciden`, `toda_clave_leida_esta_documentada`; que el análisis no es vacío: `el_analisis_ve_las_marcas`, `el_analisis_ve_un_comentario_de_la_linea_anterior`, `el_analisis_ve_una_marca_cambiada`, `el_analisis_ignora_marcas_dentro_de_textos` |
| CA-4 | `mutacion_la_copia_sin_cambios_pasa`, `mutacion_parametros_sin_documentar_hace_fallar_la_bateria`, `mutacion_config_sin_documentar_hace_fallar_la_bateria`, `mutacion_politica_sin_documentar_hace_fallar_la_bateria`, `mutacion_marca_cambiada_hace_fallar_la_bateria`, `mutacion_propuesto_sin_pregunta_hace_fallar_la_bateria` |
| CA-5 | `doc_devuelve_el_registro_con_tabla_y_clave`, `doc_con_su_tabla`, `doc_devuelve_copia`, `doc_registros_de_solo_lectura`, `doc_sin_documentar_es_KeyError`, `doc_en_otra_tabla_es_KeyError`, `doc_tabla_desconocida_es_ValueError`, `doc_ambigua_es_ValueError_y_con_tabla_responde`, `por_estado_es_una_particion`, `por_estado_en_el_orden_del_codigo`, `por_estado_desconocido_es_ValueError`, `faltan_detecta_sin_documentar_y_no_existe`, `faltan_con_tablas_incompletas_es_ValueError`, `preguntas_pendientes_son_las_de_los_propuestos`, `preguntas_pendientes_con_el_valor_de_partida_del_codigo`, `preguntas_pendientes_serializables`, `preguntas_pendientes_devuelve_copias` |
| CA-6 | `no_cambia_el_esquema_del_codigo`, `no_cambia_al_importar_solo_biblioteca_estandar`, `no_cambia_ningun_valor`; las 61 baterías (entre ellas `pruebas_integracion_v053.py`, que comprueba el esquema registrado, y `pruebas_catalogo_codigos.py`, que recorre `validador/`) y `leeme_marco.py` |

## Regresiones

- **CA-4 se demuestra fallando.** La batería copia `validador/` y `esquemas/` a una carpeta temporal y se ejecuta a sí misma en un subproceso (`T83_VALIDADOR`; dentro del subproceso no se repiten las mutaciones).
  - Copia sin cambios: pasa (código 0).
  - Cada una de las cinco mutaciones hace fallar la batería (código 1, «HAY FALLOS»), y falla precisamente la comprobación esperada:
    - una clave nueva en `_VALORES` de `parametros.py` → `cobertura_PARAMETROS_sin_documentar`;
    - una clave nueva en `CONFIG_DEFECTO` → `cobertura_CONFIG_DEFECTO_sin_documentar`;
    - una clave nueva en `POLITICA_DEFECTO` → `cobertura_POLITICA_DEFECTO_sin_documentar`;
    - `[RATIFICADO]` de `n_dias_embudo` cambiado a `[PROPUESTO]` → `marcas_coinciden_PARAMETROS`;
    - la pregunta de `i_indice_sombra` a None → `propuesto_con_pregunta`.
- **La batería no lanza ante una mutación.** En la primera versión, la mutación de `POLITICA_DEFECTO` hacía lanzar un KeyError a `politica_f_tecnico_porque_sus_limites_van_uno_a_uno`: la batería fallaba, pero por un motivo equivocado. Se corrigió con accesos que no lanzan, y ahora esa mutación falla por la cobertura.
- **El análisis del fuente no es vacío.**
  - Ve 3 `[RATIFICADO]` en `PARAMETROS` y las marcas de las líneas de solo comentario anteriores (`umbral_l2_eur`, `importe_max_activo_eur`).
  - En memoria, cambiar una marca da exactamente una discrepancia.
  - Las marcas dentro de textos no cuentan.
- **Una fuente inventada no pasa** (`fuente_inventada_no_existe`). Al escribir esa prueba, «V0.09» resultó existir en `documentos_0/` y se cambió por «V0.99», que no existe: así la prueba comprueba lo que dice.

## Gate

`.docs/scripts/gate.sh --completo` (log en la carpeta de logs de `.docs/scripts/`, `gate_20261110_184809.log`): 11 de 12 en verde.

- **Falla `mypy bloque_b: 160 > cuota 159`.** No es de esta tarea: T-83 no toca `bloque_b/`. Con el árbol de HEAD (commit `99160b3`, T-90), `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_b/11_Ejecutor/bloque_b` da ya 160 líneas. Queda para quien lleve T-90 o la cuota.
- **En verde:** corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff, mypy A y A-Forex, y pytest A 317, A-Forex 68 y B 176.

Comandos usados:

```
cd sistema_global/marco_comun_c && ../../.venv/bin/python -I pruebas/pruebas_parametros_doc_t83.py
.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c
.docs/scripts/pruebas_marco.sh
.docs/scripts/gate.sh --completo
```
