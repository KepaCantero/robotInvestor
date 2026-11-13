# T-114 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (recogidas) | 3693 | 3744 con T-114 (51 nuevas en `tests/test_fase3_goldens.py`) |
| ruff (cuenta del gate) | 2902 | 2902 |
| mypy `bloque_a` | 109 | 109 (no se toca el paquete) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_ca1_cada_golden_coincide_byte_a_byte` (6), `test_ca1_no_sobra_ni_falta_ningun_fichero`, `test_ca1_un_fichero_de_mas_o_de_menos_se_detecta`, `test_ca1_los_goldens_tienen_la_forma_canonica` |
| CA-2 | `test_ca2_mutar_un_campo_del_golden_hace_fallar_la_comparacion` (6), `test_ca2_un_solo_byte_de_diferencia_basta`, `test_ca2_cambiar_una_tabla_del_codigo_cambia_lo_generado` (8), `…la_version_o_los_estados…` (2), `…un_esquema_del_codigo…` (5), `test_ca2_un_campo_minimo_nuevo_cambia_los_mensajes_y_las_divergencias`; y la mutación a mano de abajo |
| CA-3 | `test_ca3_las_tablas_cubren_ct01_a_ct25`, `test_ca3_son_los_contratos_del_documento_0` |
| CA-4 | `test_ca4_hay_esquema_derivado_para_cada_contrato_con_campos_en_el_anexo_b`, `…cada_esquema_es_valido_lleva_la_marca_y_su_ejemplo_lo_cumple`, `…un_ejemplo_sin_un_campo_obligatorio_o_fuera_de_lista_no_cumple`, `…el_seguimiento_exige_seg_id_y_opp_id_en_ct05`, `…los_campos_de_cada_esquema_estan_en_el_anexo_b` |
| CA-5 | `test_ca5_el_ejemplo_del_paquete_cumple_su_esquema_publicado`, `test_ca5_el_ejemplo_de_seguimiento_cumple_su_esquema_salvo_la_clave_de_aviso` (desviación: INC-T114-02) |
| CA-6 | `test_ca6_recongelar_sin_motivo_falla_y_no_escribe`, `test_ca6_recongelar_con_motivo_escribe_y_registra`, `test_ca6_el_registro_y_el_readme_dicen_la_regla` |
| CA-7 | `test_ca7_una_divergencia_nueva_no_coincide_con_el_golden`, `test_ca7_un_mensaje_del_ciclo_fuera_del_anexo_b_aparece`, `test_ca7_las_divergencias_estan_en_las_incidencias_y_en_la_deuda` |
| CA-8 | `test_ca8_dos_generaciones_seguidas_dan_el_mismo_texto`, `test_ca8_las_formas_no_dependen_del_orden_de_los_mensajes` |
| CA-9 | `git diff --stat ab95d41 -- bloque_a/11_Ejecutor/bloque_a bloque_a/01_Gobernanza bloque_a/06_Plantillas_entregables`: T-114 no cambia nada ahí (el cambio de `diseno_v6.py` es de T-117) |
| CA-10 | Gate: ver abajo |

## Mutación a mano (13-11-2026, en una copia desechable de `bloque_a`)

`python tests/goldens_ct.py` desde `bloque_a/11_Ejecutor`:

| Paso | Salida | Código |
| --- | --- | --- |
| Sin tocar | `goldens de contratos: coinciden` | 0 |
| Golden mutado (`fecha_corte` → `fecha_de_corte` en `tablas_contratos.json`) | `DIFERENCIA · tablas_contratos.json: difiere del golden congelado (línea 64: congelado «"fecha_de_corte"», generado «"fecha_corte"»)` | 1 |
| Golden restaurado | coinciden | 0 |
| Código mutado (CT-10 exige `tolerancia`) | difieren `divergencias_anexo_b.json`, `mensajes_ejemplo.json` y `tablas_contratos.json` | 1 |
| Código mutado (`N1` en el `enum` de `ruta` de CONSULTA) | difiere `esquemas_respuestas.json` (línea 140) | 1 |
| Esquema derivado tocado a mano (`INMEDIATA` → `URGENTE`) | difiere `huellas.json` | 1 |
| `--update` sin motivo | `ERROR: el re-congelado exige un motivo` | 2 |
| Todo restaurado | coinciden | 0 |

## Regresiones

No aplica: no se corrige ningún fallo.

## Gate

Gates ligeros en la copia de trabajo (13-11-2026): secretos, refs vivas, nombres NFC y corpus (695) en verde. El gate completo 12/12 lo pasa `commit_limpio.sh` al hacer el commit; su resultado se anota en el registro del ticket.
