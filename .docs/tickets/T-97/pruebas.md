# T-97 · Pruebas

Ejecutadas el 12-11-2026 por Claude, con el `.venv` de T-96 (Python 3.12).

| Suite | Antes (V0.73) | Después (V0.74) |
| --- | --- | --- |
| Baterías del marco (`.docs/scripts/pruebas_marco.sh`) | 61 | 62 pasan, 0 fallan |
| `pruebas_tanda2_t97.py` (nueva) | — | 49 comprobaciones |
| `pruebas_integracion_v053.py` | 36 | 37 |
| `leeme_marco.py` | — | sin diferencias |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `sistema_global/documentos_0/V0.74_Valores_por_defecto_de_la_tanda_2.md`, citado en el LEEME | OK |
| CA-2 | `sin_foto_ni_capital_declarado_no_hay_encargo_con_coste`, `con_capital_declarado_el_primero_cabe`, `el_segundo_no_cabe_por_la_reserva_del_primero_O43`, `al_llegar_al_tope_registrar_gasto_avisa_O43`, `una_rutina_sin_IA_sigue_con_el_tope_agotado`, `con_foto_manda_la_foto_y_no_el_capital_declarado`, `tope_en_euros_y_reservas`, `el_anio_natural_no_arrastra_el_anterior` | OK |
| CA-3 | `cartera_pequena_F14_frena_al_25_por_ciento` (500 € con 4.500 € ya invertidos de 20.000 €), `cartera_grande_F14_como_en_V073_en_euros`, `cartera_grande_mismo_resultado_que_sin_los_porcentajes` | OK |
| CA-4 | `trading_con_4_por_ciento_en_la_semana_no_abre`, `tactica_con_4_por_ciento_si_abre`, `largo_plazo_con_5_por_ciento_no_abre`, `cartera_grande_la_semana_manda_en_euros`, y al enviar con y sin capital y con capital no válido | OK |
| CA-5 | Fuera del ticket (T-98): la alerta sigue en −5 % y `pruebas_vigilancia_t49.py` pasa sin cambios | OK |
| CA-6 | `usd_principal_con_0_6_por_ciento_se_rechaza`, `usd_principal_con_0_4_por_ciento_pasa`, `usd_sin_ser_principal_con_0_6_por_ciento_pasa`, `usd_sin_ser_principal_con_3_1_por_ciento_se_rechaza`, `divisa_sin_clasificar_usa_la_general` | OK |
| CA-7 | `MIG010_anade_las_claves_con_su_valor_de_partida`, `MIG010_no_cambia_lo_que_ya_tenia`, `MIG010_la_tolerancia_principal_nunca_mas_laxa_que_la_general`, `MIG010_una_version_propia_no_se_pisa`, `MIG010_en_la_cadena_desde_un_estado_guardado` (V0.52 → V0.74) | OK |
| CA-8 | `pruebas_parametros_doc_t83.py`: `faltan()` y `desfasados()` vacíos | OK (109) |
| CA-9 | 62 baterías, LEEME sin diferencias y gate del repositorio (ver abajo) | OK |
| CA-10 | `git status`: solo `sistema_global/marco_comun_c/`, `sistema_global/documentos_0/`, la deuda técnica, `CLAUDE.md` y `.docs/` | OK |

## Fallo cerrado

- Configuración: no arranca con la tolerancia de las principales más laxa que la general o nula, el euro o una divisa repetida o mal formada entre las principales, un tope anual de 0, mayor que 10 o infinito, o un capital declarado cero, negativo o no numérico; la política de F sin las claves nuevas o con un % fuera de rango no vale.
- Sin foto ni capital declarado, ningún encargo con coste.
- Al enviar, un capital cero, negativo, infinito o no numérico da un único VETA de F-01.

## Regresiones

Antes de ajustar los datos, la primera pasada dio 53 baterías en rojo por el tope anual sin foto (las de mecánica emiten encargos antes de registrar una foto) y después 13 por versiones y holguras del tipo de cambio; cada ajuste está en `analisis-tecnico.md`, y en ninguno se cambió lo que la prueba comprueba.

## Gate

Pasa en la copia limpia de `.docs/scripts/commit_limpio.sh`, que ejecuta también las pruebas del marco y su LEEME.
