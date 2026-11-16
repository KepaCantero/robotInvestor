# T-152 · Pruebas

Las pruebas se hicieron en el árbol de trabajo y en una copia desechable **completa** con «t147_mut» en la ruta: HEAD extraído con `git archive`, los ficheros cambiados encima y `.venv` enlazado. Sin red ni coste. Esta es la versión definitiva, con el umbral a q/p ≤ 2 % por decisión del operador (16-11-2026). La primera versión, con el umbral en el 1 %, se subió en `4e39324`. Su QA se detuvo al empezar, cuando llegó la decisión.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t150.py` | 79 | **103 passed** (+24 `test_t152_*`) |
| Las 14 suites de A que tocan `frontera_b` o IDX-CONC-001 (`test_fase1_mon_idx`, `t106_r03`, `t113_deuda`, `t121`, `t127` ×3, `t128` ×2, `t135_motor`, `t144`, `t149`, `t150` y `t165_g3_met13`) | — | 884 passed, 2 skipped (2 min 28 s) |
| Vecinas de la cadena y del BCE (`test_t147`, `t142_cadena_b` y `t141_datos_bce`) | — | en verde (con las de arriba, 357 passed, 2 skipped en la primera versión) |
| Suite completa de A | 6525 passed, 2 skipped (QA r01 de T-150) | En el gate de `commit_limpio.sh` (la primera versión pasó el gate entero, 12/12) |
| `.docs/scripts/pruebas_scripts.sh` | 231 | 231 (línea base 231) |
| ruff, desde la raíz, sobre los ficheros tocados | — | sin avisos |

## Criterio de aceptación → prueba

| Criterio | Prueba y resultado |
| --- | --- |
| CA-1 (H-01) | `test_t152_h01_un_tramo_contenido_en_otro_no_acorta_la_union`, `…un_correo_dentro_de_una_contrasena_no_deja_su_cola`, `…el_aviso_de_sin_entrega_se_limpia` y `…el_traslado_a_medias_nombra_solo_los_escritos` (fallo en el 2.º, 3.º, 4.º y 6.º CSV). Revisor de T-150 (`mutantes_heredados.py`, sin X01, que ahora es el código): **Y01, Z03 y W01 muertos**, y todos los demás muertos o equivalentes salvo **X02**, el casi equivalente de O-03 |
| CA-2 (H-02) | `medir_umbral.py --semillas 100`, salida en `medir_umbral_100.txt` (idéntica con el código nuevo, porque el script reconstruye el módulo con cada umbral). Umbral a q/p ≤ 2 %. `T-150/medir_truncado.py --semillas 300`, nuevo frente al de antes (`--modulo`): **idéntico**. `T-149/medir_copias.py --semillas 300`: idéntico salvo tres casillas del límite declarado de los fondos (284 → 283, 287 → 288 y 196 → 195). `test_t152_h02_el_umbral_del_desplazamiento_esta_en_q_p_del_2_por_ciento` (5 tramos × 12 semillas). Mutantes U1 (el 1 % de antes) y U2b (un 5 % más bajo) muertos; U2 (el doble) equivalente, como se esperaba |
| CA-3 (O-01) | `test_t152_o01_un_cambio_de_metodo_a_mitad_de_la_historia_no_se_agrupa`: la copia mixta no se agrupa, y cada mitad sola sí. Nombrada en INC-T127-01 |
| CA-4 (O-02) | `test_t152_o02_una_correspondencia_que_no_son_textos…` (4 formas) y `…un_paquete_sin_la_forma_da_paquete_ilegible` (6 formas, con un correo y una marca sin datos de R8 que no puede salir ni en el mensaje ni en el resumen). Además, `…el_paquete_de_ejemplo_tiene_la_forma`. Las 11 fallan con el `cadena_a_b.py` de antes de T-152 y pasan con el nuevo |
| CA-5 | `T-152/mutantes.py <copia>`: **16 muertos y 1 equivalente esperado (U2), 0 vivos**. `T-150/mutantes.py` (con F3 sobre la línea nueva, vía `mutantes_heredados.py`): **22 de 22 muertos**. `T-149/revisores/r01_02_mutantes_qa.py <copia>`: 0 vivos (sin contar los equivalentes). Cadena real con los dos ejecutores simulados (`cadena_a_b.py --sonda-sin-correspondencia`, primera versión; el umbral no la toca): código 0, ENTREGADA, G3 APTO, 3 enviables, 1 envío con un paquete del Bloque B válido y la sonda ADMITIDA. Gate, en el commit |

## Límites

- **X02** (media anchura truncada q/2p̃ en vez de (q/2)/(p̃ + q/2)) sigue vivo: es la observación O-03 del revisor. La diferencia es del orden de (q/2p̃)², por debajo de la resolución de cualquier prueba con series.
- **Resolución de la prueba del umbral:** mata un umbral un 5 % más bajo y el 1 % de antes. Uno más alto es equivalente, porque por encima del 2 % la cota está en el tope (`analisis-tecnico.md`).
- **Scripts heredados.** X01 del revisor de T-150 y F3 de `T-150/mutantes.py` mutan la línea de antes («`desplaza = 2 * rel <= tol`»), y sus scripts se paran con un `assert` si no la encuentran. `mutantes_heredados.py` los ejecuta con la línea nueva: no toca los originales, escribe copias adaptadas en una carpeta temporal. El revisor de T-150 termina con 1 por X02.
- **Mutante descartado.** El primer intento de los mutantes usó una copia con solo `bloque_a` y `.docs/scripts`. Todos «morían» porque faltaba `bloque_b/11_Ejecutor/config/ambitos_ejemplo.yaml`. Se rehízo con la copia completa, que pasa las 217 pruebas sin mutar.

## Comandos

```bash
.venv/bin/python -I .docs/tickets/T-152/medir_umbral.py --semillas 100
git show 4e39324:bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py > <tmp>/frontera_b_1pc.py
.venv/bin/python -I .docs/tickets/T-150/medir_truncado.py --semillas 300 [--modulo <tmp>/frontera_b_1pc.py]
.venv/bin/python -I .docs/tickets/T-149/medir_copias.py --semillas 300 [--modulo <tmp>/frontera_b_1pc.py]
.venv/bin/python .docs/tickets/T-152/mutantes.py <copia «t147_mut»>
.venv/bin/python .docs/tickets/T-152/mutantes_heredados.py <copia «t147_mut»> <carpeta temporal>
.venv/bin/python .docs/tickets/T-149/revisores/r01_02_mutantes_qa.py <copia «t147_mut»>
```

## Gate

Se ejecuta en el commit con `.docs/scripts/commit_limpio.sh`: el gate completo en una copia limpia.
