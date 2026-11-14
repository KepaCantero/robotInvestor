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

## Ronda r02 (14-11-2026)

Lo de arriba es la primera entrega. Esta sección es lo vigente.

| Suite | Antes de la r02 | Después |
| --- | --- | --- |
| `tests/test_fase3_goldens.py` | 51 | 102 (92 s en una máquina sin carga; con la máquina compartida y cargada llegó a 233 s) |
| `bloque_a/11_Ejecutor` (suite completa) | 3825 (3876 menos las 51 nuevas; la QA r01 midió 3811 en un commit anterior) | **3876 passed** en 1016 s, una sola pasada |
| ruff (cuenta del gate, los tres `11_Ejecutor`) | 2902 | 2902 |
| mypy `bloque_a` | 109 | 109 (no se toca el paquete) |

### Hallazgo → prueba

| Hallazgo | Prueba |
| --- | --- |
| H-01 a (reglas de valor de la mensajería) | `test_h01_la_bateria_cubre_los_25_contratos_con_admitidos_y_rechazados`, `test_h01_las_reglas_de_valor_estan_en_la_bateria`, `test_h01_un_caso_mal_escrito_es_un_error_y_no_un_rechazo`, `test_h01_la_copia_sin_cambios_de_contratos_da_el_golden`, `test_h01_un_cambio_en_las_reglas_de_la_mensajeria_cambia_el_golden` (22) |
| H-01 b y c (más flujos, rutas anidadas y tipos) | `test_h01_los_flujos_cubren_los_contratos_que_el_ejecutor_emite`, `test_h01_las_rutas_llevan_claves_anidadas_tipos_y_combinaciones`, `test_h01_un_cambio_en_lo_que_el_ejecutor_emite_cambia_las_formas` (14), `test_ca8_las_formas_no_dependen_del_orden_de_los_mensajes`, `test_h01_el_readme_declara_el_alcance_y_los_limites` |
| H-02 (CT-22) | `test_ca4_hay_esquema_derivado_para_cada_contrato_con_campos_en_el_anexo_b`, `test_ca4_de_ct16_a_ct22_el_anexo_b_solo_nombra_el_tipo_de_ct22`, `test_ca7_el_tipo_de_ct22_que_el_ejecutor_emite_en_tipo_aviso_esta_congelado` |
| H-05 (CT-23 y retornos) | `test_ca4_el_contenido_de_ct23_solo_va_en_entrante`, `test_ca4_los_retornos_declaran_que_el_anexo_b_no_describe_el_retorno_rechazado` |
| H-06 (nada inventado, por párrafo) | `test_ca4_los_campos_de_cada_esquema_estan_en_el_parrafo_de_su_contrato`, `test_ca4_un_campo_de_otro_contrato_se_detecta` |
| H-04 | Documentación: CA-5 del README |
| H-03 | No se toca la deuda; el texto propuesto va en el informe de entrega |

### Regresiones: fallan sin la corrección

- **H-01.** Los mutantes del revisor, con sus scripts sin cambiar, en una copia desechable:

  | Script | r01 | r02 |
  | --- | --- | --- |
  | `r01_01_mutantes_contratos.py` | 21 detectados de 39 aplicables | 39 de 39 (M10 sigue sin aplicarse: su texto aparece dos veces en `contratos.py`) |
  | `r01_03_mutantes_emision.py` | 1 de 11 | 11 de 11 |
  | `r01_04_supervivientes_suite_completa.py`, los 23 a la vez | `goldens_ct.py` rc=0; suite: 3 fallos de 3811 | `goldens_ct.py` rc=1; suite: 42 fallos de 3876 (39 de `test_fase3_goldens.py` y los 3 de antes) |
  | `r01_02_goldens_determinismo_y_update.py` | 24 de 24 | 27 de 27 |

  Dentro de la suite, los mismos cambios están como pruebas: 22 sobre una copia de `contratos.py` y 14 sobre los mensajes capturados.
- **H-02.** `test_ca7_el_tipo_de_ct22…` comprueba que, si los avisos llevaran el valor en `tipo`, la diferencia desaparecería del cálculo. Con los esquemas de la r01 (sin `CT-22.ENCARGO`) las pruebas de CA-4 nuevas fallan.
- **H-06.** `test_ca4_un_campo_de_otro_contrato_se_detecta` pone un campo de CT-09 en CT-10 y comprueba que la búsqueda de la r01 (en todo el Anexo B) no lo veía y la nueva sí.

### Determinismo

`r01_02`: cuatro procesos con `PYTHONHASHSEED` 0, 1, 12345 y aleatorio dan los siete goldens idénticos entre sí y al congelado; también con `TZ=Pacific/Kiritimati` y `LC_ALL=C`. Dentro de la suite, `test_ca8_dos_generaciones_seguidas_dan_el_mismo_texto` vuelve a ejecutar todos los flujos.

### Gates (14-11-2026, en la copia de trabajo)

| Qué | Resultado |
| --- | --- |
| `python tests/goldens_ct.py` | `goldens de contratos: coinciden`, código 0 (36 s) |
| `python tests/goldens_ct.py --update` | código 2, nada escrito |
| `tools/corpus_integridad.py` | 695 archivos coinciden |
| `tools/refs_vivas.py`, `tools/secrets_scan.py`, `tools/nfc_check.py` | los tres en verde; la lista permitida de secretos no se ha tocado |
| `git diff --stat 3fc54d5 HEAD -- bloque_a/11_Ejecutor/bloque_a bloque_a/01_Gobernanza bloque_a/06_Plantillas_entregables` | vacío (3fc54d5 es el commit del que parte la ronda) |
| `./tools/check_all.sh` completo | **no ejecutado** en esta ronda (máquina compartida); es condición de cierre |

Los valores de la batería que hacen de dato protegido son ficticios y con una forma que el gate de secretos no marca: un documento de identidad de ceros, una cuenta de ceros y una cabecera de autorización de equis.
