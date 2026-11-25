# T-206 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A, pruebas nuevas (`tests/test_t206_tipo_incidencia.py`) | — | 35 casos superados (unos 14 s) |
| Bloque A, ficheros que cambian y sus vecinos[^vecinos] | — | 353 superadas, 0 fallos |
| Bloque A, suite completa (en el gate) | — | 8579 superadas, 0 fallos (línea base 607) |
| A-Forex, B | sin tocar | sin tocar |

[^vecinos]: Son `test_t198_buscador_ct19.py`, `test_t125_r02.py`, `test_t65_qa_r01.py`, `test_t65_qa_r02.py`, `test_t65_qa_r03.py`, `test_t65_hallazgos.py`, `test_t103_r8_y_bajos.py`, `test_t116_r05.py`, `test_t174_pb61_revision_c2.py`, `test_t93_hallazgos.py`, `test_t169_r02.py` y `test_t92_revision.py`.

## Criterio de aceptación → prueba

Todas las pruebas de esta tabla están en `tests/test_t206_tipo_incidencia.py`.

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_ca1_el_enumerado_del_codigo_es_el_del_esquema_de_ha`: lee la línea de INC- de 4.8 del esquema del corpus. `test_ca1_el_enumerado_solo_se_escribe_en_almacen`: AST, ninguna tupla, lista o conjunto con tres o más tipos fuera de `almacen.py`. `test_ca1_todas_las_llamadas_del_paquete_usan_un_tipo_del_esquema`: AST de cada `incidencia(…)` y `_incidencia_interna(…)` |
| CA-2 | `test_ca2_un_tipo_fuera_del_esquema_falla_cerrado_sin_escribir_nada`, con 10 casos: DATOS, vacío, None, `otro`, `OTRO `, ` SEGURIDAD`, `HERRAMIENTAS`, 7, `["OTRO"]` y `("OTRO",)`. Prueba `incidencia` y `_incidencia_interna`, compara byte a byte todos los ficheros del almacén y comprueba el contador. También `…_el_rechazo_es_un_error_propio_y_no_cita_mas_que_el_tipo`, `…_cada_tipo_del_esquema_se_escribe` (7 casos, validados con jsonschema) y `…_la_de_datos_no_admite_otra_categoria` |
| CA-3 | Una prueba por camino: `test_ca3_broker_revision_c2_sin_tipos_que_revisar`, `…_broker_consulta_con_plazo_ilegible`, `…_orquestacion_referencia_de_comparacion_invalida`, `…_orquestacion_datos_invalidos_de_un_simbolo`, `…_orquestacion_ct19_no_atendido_por_el_buscador`, `…_orquestacion_pronostico_de_fuente_no_registrable`, `…_fiabilidad_f9_sin_fichas_de_f9` y `…_fiabilidad_f9_fuente_que_ya_no_es_de_f9`. Cada una exige una sola INC- nueva con `tipo` OTRO y `categoria` DATOS, validada con jsonschema, y sus marcas propias. Además, las pruebas de antes de cada camino siguen pasando con `es_incidencia_de_datos` |
| CA-4 | `test_ca4_un_ha_antiguo_con_datos_se_abre_integro_y_se_reconoce`, `…_el_lector_no_toma_otras_entradas_por_de_datos`, `…_las_fue_marcadas_en_un_ha_antiguo_no_vuelven_al_ct19` y `…_el_estado_del_operador_muestra_las_escaladas_antiguas_y_las_nuevas` |
| CA-5 | `test_ca5_ciclo_mock_por_defecto_con_un_dato_invalido_solo_deja_tipos_del_esquema`, con `cargar_config()` tal cual. Además, la equivalencia con develop, la suite completa y el gate (abajo) |

La configuración por defecto se prueba tal cual en CA-5. Las demás pruebas usan la de pruebas (`config_pruebas`) o un `Almacen` solo.

## Sin el cambio

Las pruebas nuevas se copiaron sobre `origin/develop` (`358576c3`). Como allí no existen `TIPOS_INCIDENCIA`, `CATEGORIA_DATOS`, `TipoIncidenciaNoAdmitido` ni `es_incidencia_de_datos`, se definieron dentro de la propia prueba para que el módulo importe. Resultado: **25 fallos y 10 superadas**.

Las 10 que pasan comprueban lo que ya era cierto en develop o lo que aporta esa definición:
- cada uno de los 7 tipos del esquema se escribe;
- el enumerado frente al esquema, que en develop es la definición de la prueba;
- el lector;
- la deduplicación de F9 con un HA antiguo, que ya funcionaba y es la compatibilidad que se pide conservar.

Fallan todas las de fallo cerrado, las de un solo sitio, las de lectura estática y las de los ocho caminos (escriben DATOS), además de las de HA antiguo que usan `incidencia_de_datos` y la del ciclo mock.

## Mutantes

`.docs/tickets/T-206/mutantes.py` tiene 20 mutantes: **19 muertos, 0 vivos y 1 equivalente**.

- **Validación (M1 a M4):** M1 y M2 quitan la comprobación de `incidencia` y de `_incidencia_interna`; M3 la hace después de gastar el contador; M4 quita `isinstance`.
- **Enumerado (M5 y M6):** el enumerado admite DATOS o pierde ESCRITURA.
- **Escritura de los de datos (M7 y M8):** los de datos van como HERRAMIENTA, o sin `categoria`.
- **Lector (M9 a M11):** no reconoce las antiguas, o no reconoce las nuevas, o no mira `tipo_entrada`.
- **Los ocho caminos (M12 a M19):** cada mutante devuelve un camino a DATOS, uno por uno. Es la prueba de que cada camino falla sin el cambio.
- **Deduplicación de F9 (M20):** no cuenta la marca antigua.

M4 es equivalente. Un tipo que no es texto tampoco está en la tupla: la pertenencia compara con ==, sin hash, así que se rechaza igual.

## Regresión del ciclo mock

`.docs/tickets/T-201/equivalencia.sh . origin/develop` ejecuta la misma secuencia con el código de develop y con el de la copia. La secuencia es el backtest del README (`--cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`), el ciclo, la petición, la consulta, el alta y la ejecución de un seguimiento, `evaluar` y `estado`.

Resultado: 89 ficheros por lado, **ninguno distinto tras normalizar**, veredicto EQUIVALENTE y testigo de sensibilidad sin puntos ciegos. En el camino normal no se escribe ninguna incidencia de datos, así que nada cambia. El caso con un dato inválido lo cubre CA-5.

## Evidencias del plan

`.docs/scripts/evidencias_plan_a.py --ejecutar` superó 420 de 420 pruebas citadas. Solo cambia el commit de la cabecera de `docs/evidencias_pruebas_bloque_a.md`. El mapa (`tests/mapa_plan_pruebas.json`) no cambia, porque T-206 no tiene caso del plan.

## Gate

`./tools/check_all.sh` completo sobre el commit del ticket, lanzado con `setsid nohup` y con su log en el scratchpad de la sesión (`gate_t206.log`): **12 de 12 superados**.

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas | OK |
| ruff | 2797, con cuota 2797 |
| mypy de A | 67, con cuota 67 |
| mypy de A-Forex | 174, con cuota 174 |
| mypy de B | 159, con cuota 159 |
| pytest de A | 8579 superadas |
| pytest de A-Forex | 68 superadas |
| pytest de B | 176 superadas |

Ninguna cuota sube ni baja, así que `tools/cuotas.txt` no cambia. El orden del import de `test_t198_buscador_ct19.py` se corrigió para no sumar un hallazgo de ruff.

**Rebase sobre `d11662ff` (T-203).** El gate se pasó con el ticket encima de `358576c3`. Después, develop avanzó con T-203, que bajó la cuota de ruff a 2735. El rebase entró sin conflictos. Tras el rebase se repitieron estas comprobaciones:
- ruff da 2735, igual que la cuota nueva;
- mypy de A da 67;
- `test_t206_tipo_incidencia.py`, `test_t203_cuotas.py` y `test_fase4_mapa.py`: 63 superadas;
- seis de los ficheros de pruebas cambiados (`test_t198_buscador_ct19.py`, `test_t125_r02.py`, `test_t65_qa_r01.py`, `test_t65_qa_r02.py`, `test_t103_r8_y_bajos.py` y `test_t116_r05.py`): 150 superadas.

El gate completo no se repitió sobre la base nueva.

## Ronda de cierre de la QA r01 (H-01 a H-06)

Rebase sobre `6c8910c1` (develop con T-205). Las salidas de esta ronda están en esta carpeta y en el scratchpad de la sesión.

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t206_tipo_incidencia.py` | 52 casos superados: los 35 de la r01, con las ocho `test_ca3_*` y las de CA-4 ampliadas, y 17 nuevos (2 tipos hostiles, 7 de categoría, 7 de `escribir` y la de la documentación) |
| `test_t198_buscador_ct19.py`, `test_t116_r05.py`, `test_t205_clase_seguimiento.py`, `test_fase4_huecos.py`, `test_unitarias.py` | 142 superadas |
| `mutantes.py` propio | 41 mutantes, **41 muertos, 0 vivos, ningún equivalente** (`evidencia_mutantes_cierre.txt`). M4 ya no es equivalente; se añadieron M4b, M21 a M30 (H-02 a H-04 y H-06) y los diez del revisor (Q6, Q14, Q15, Q16, Q18, Q20, Q21, Q22, Q24 y Q25, H-05) |
| `revisores/r01_01_ataques.py` | 0 HALLAZGO (16 OK) |
| `revisores/r01_02_mutantes.py` | 25 mutantes: 24 muertos en la etapa 1 y Q3 vivo, equivalente (el mensaje mutado solo repite el tipo); 0 vivos no equivalentes. La primera ejecución dio a Q3 por muerto por una muerte espuria (H-07 de la ronda de cierre); la evidencia buena es la ejecución limpia del revisor (`revisores/rc_02_mutantes.txt`) |
| `revisores/r01_03_ciclo_mock.sh` | RESULTADO: OK (las antiguas DATOS intactas, la nueva de EURUSD=X es OTRO con DATOS, `estado` muestra la escalada antigua y el almacén está íntegro) |
| Equivalencia con develop (`.docs/tickets/T-201/equivalencia.sh . origin/develop`, base `6c8910c1`) | 89 ficheros por lado, ninguno distinto tras normalizar, EQUIVALENTE, testigo sin puntos ciegos. La vista `estado` no cambia en el camino normal, porque ninguna escalada lleva `categoria` |
| ruff y mypy de A, antes del gate | 2735 (cuota 2735) y 67 (cuota 67) |

Los tres scripts del revisor se adaptaron en tres puntos donde la corrección pedida chocaba con su montaje. Se explica en `analisis-tecnico.md`, «Ronda de cierre», y el diff exacto está en `cierre_adaptacion_revisores.diff`.

**Evidencias del plan.** Se regeneraron con `.docs/scripts/evidencias_plan_a.py --ejecutar` antes del commit de cierre: 420 de 420 citadas superadas. La cabecera cita el commit HEAD en el momento de ejecutarlas, `786ad26a`: el commit r01 de T-206 rebasado sobre `6c8910c1`, padre del commit de cierre. El script toma siempre HEAD.

**Gate de cierre (H-01).** Se pasó `./tools/check_all.sh` completo sobre el commit de cierre `ea534285` (base `6c8910c1`), lanzado con `setsid nohup` y con su log en el scratchpad de la sesión (`gate_t206_cierre.log`). Resultado: **12 de 12**.

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas | OK |
| ruff | 2735, con cuota 2735 |
| mypy de A | 67, con cuota 67 |
| mypy de A-Forex | 174, con cuota 174 |
| mypy de B | 159, con cuota 159 |
| pytest de A | 8629 superadas |
| pytest de A-Forex | 68 superadas |
| pytest de B | 176 superadas |

Las cuotas no cambian. Después solo se reescribió el commit (amend) para añadir este párrafo a `pruebas.md`: el código y las pruebas son los de `ea534285`. El gate anterior (`gate_t206.log`) era de antes del rebase y queda sustituido por este.
