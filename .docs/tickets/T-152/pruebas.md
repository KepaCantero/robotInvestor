# T-152 · Pruebas

Las pruebas se hicieron en el árbol de trabajo y en una copia desechable con «t147_mut» en la ruta: HEAD extraído con `git archive`, los ficheros cambiados encima y `.venv` enlazado. Sin red ni coste.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t150.py` | 79 | **102 passed** (+23 `test_t152_*`) |
| Vecinas (`test_t150`, `t149`, `t147`, `t144`, `t142_cadena_b` y `t141_datos_bce`) | — | 357 passed, 2 skipped (36 s) |
| Suite completa de A | 6525 passed, 2 skipped (QA r01 de T-150) | En el gate de `commit_limpio.sh` |
| `.docs/scripts/pruebas_scripts.sh` | 231 | 231 (línea base 231) |
| ruff, desde la raíz, sobre `test_t150.py`, `cadena_a_b.py` y `T-152/*.py` | — | sin avisos |

## Criterio de aceptación → prueba

| Criterio | Prueba y resultado |
| --- | --- |
| CA-1 (H-01) | `test_t152_h01_un_tramo_contenido_en_otro_no_acorta_la_union`, `…un_correo_dentro_de_una_contrasena_no_deja_su_cola`, `…el_aviso_de_sin_entrega_se_limpia` y `…el_traslado_a_medias_nombra_solo_los_escritos` (fallo en el 2.º, 3.º, 4.º y 6.º CSV). `T-150/revisores/r01_04_mutantes_qa.py <copia>`: **Y01, Z03 y W01 muertos**; también X01, X03 a X07, Y02, Y03, Z01, Z02, Z04 y W02 a W04; X08 y Z05, equivalentes como se esperaba. Vive **X02**, el casi equivalente de O-03 del revisor: el script termina con 1 solo por él (ver «Límites») |
| CA-2 (H-02) | `test_t152_h02_el_umbral_del_desplazamiento_esta_en_q_p_del_1_por_ciento`, en 4 tramos con 12 semillas cada uno. **X01 muerto**. `medir_umbral.py --semillas 100` (salida en `medir_umbral_100.txt`), con el resultado y la propuesta en INC-T127-01, ronda T-152 |
| CA-3 (O-01) | `test_t152_o01_un_cambio_de_metodo_a_mitad_de_la_historia_no_se_agrupa`: la copia mixta no se agrupa y cada mitad sola sí. Nombrada en INC-T127-01 |
| CA-4 (O-02) | `test_t152_o02_una_correspondencia_que_no_son_textos…` (4 formas) y `…un_paquete_sin_la_forma_da_paquete_ilegible` (6 formas, con un correo y una marca sin datos de R8 que no puede salir en el mensaje ni en el resumen). Además, `…el_paquete_de_ejemplo_tiene_la_forma`. Las 11 fallan con `cadena_a_b.py` de HEAD y pasan con el nuevo |
| CA-5 | `T-152/mutantes.py <copia>`: **15 de 15 muertos**. `T-150/mutantes.py <copia>`: 0 vivos. `T-149/revisores/r01_02_mutantes_qa.py <copia>`: 0 vivos (sin contar los equivalentes). Cadena real con los dos ejecutores simulados (`cadena_a_b.py --sonda-sin-correspondencia`): código 0, ENTREGADA, G3 APTO, 3 enviables, 1 envío con un paquete del Bloque B válido y la sonda ADMITIDA. Suite completa y gate, en el commit |

## Límites

- **X02** (media anchura truncada q/2p̃ en vez de (q/2)/(p̃ + q/2)) sigue vivo, y es la observación O-03 del revisor. La diferencia es del orden de (q/2p̃)², por debajo de la resolución de cualquier prueba de serie. No entraba en el alcance.
- **Resolución de la prueba del umbral.** Mata un umbral un 5 % más bajo y uno un 10 % más alto (U2b y U2). Uno un 3 % más alto no lo distingue ninguna serie probada (`analisis-tecnico.md`).
- **Mutante descartado.** El primer intento de los mutantes usó una copia con solo `bloque_a` y `.docs/scripts`: todos «morían» porque faltaba `bloque_b/11_Ejecutor/config/ambitos_ejemplo.yaml`. Se rehízo con la copia completa, que pasa las 216 pruebas sin mutar, y los resultados de arriba son los de esa copia.

## Gate

Se ejecuta en el commit con `.docs/scripts/commit_limpio.sh`: el gate completo en una copia limpia.
