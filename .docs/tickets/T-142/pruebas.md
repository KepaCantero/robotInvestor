# T-142 · Pruebas

Intérprete: `/home/user/robotinvestor/.venv/bin/python` (en adelante `PY`). Todo con el cliente simulado: sin red, sin API y sin coste. Fecha de corte fija: 2024-03-29.

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor/tests/test_t142_cadena_b.py` (nueva) | — | 30 pasan (≈ 4 s) |
| Vecinas de A que leen la configuración: `test_t65_hallazgos`, `test_t66_propuestas`, `test_fase3_goldens`, `test_t131_preparativos`, `test_t129_modo_sombra` | pasan | 226 pasan (150 s) |
| `PY tests/goldens_ct.py` (A) | coinciden | coinciden |
| Suite completa de A | 607 (línea base) | 637 esperadas (607 + 30), sin ejecutar: el encargo pedía no lanzarla |
| Bloque B (`pytest -q bloque_b/11_Ejecutor`) | 174 | Sin ejecutar: el Bloque B no se ha tocado |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1, la petición la admite el ejecutor de B | `cadena_a_b.py`: OPP-2024-0002 → PET-B-2024-0001 `ADMITIDA`, sin rechazo ni `MensajeRechazado`. Campo a campo frente al Anexo B.1 de B (leído del Documento 0 de B como dato): `test_peticion_campo_a_campo_frente_al_anexo_b1_del_bloque_b`, `test_paquete_para_b_cubre_los_campos_que_el_bloque_b_espera` y `test_las_dos_claves_van_donde_las_pone_el_ejemplo_del_bloque_b`. Sin mutar el paquete: `test_no_muta_el_paquete` |
| CA-1, sin correspondencia, sin inventar la clave | `test_sin_correspondencia_falla_cerrado`, `test_sin_simbolo_no_hay_correspondencia`, `test_configuracion_ausente_o_mal_formada_falla_cerrado` (5 casos) y `test_sin_valor_por_defecto_de_la_peticion_falla_cerrado` (3). En la cadena, OPP-2024-0001 y OPP-2024-0003 quedan en `SIN_CORRESPONDENCIA_AMBITO`. Sonda, sin clave: `test_sonda_sin_correspondencia_no_lleva_clave`; lo que hace B, en el resumen (abajo) |
| CA-1, correspondencia coherente | `test_correspondencia_por_defecto_casa_con_los_dos_universos`: cada clave existe en `ambitos_ejemplo.yaml` de B, cada símbolo en el universo de A, y los tipos de activo casan |
| CA-2, entrega de B válida contra su esquema | `cadena_a_b.py`: 1 entrega `ENTREGADA`, paquete válido contra `Esquema JSON - Paquete de análisis de mercado - Bloque B - V2.0.json` (0 errores). Código de salida 0 |
| CA-3, pruebas nuevas en A, líneas base | Las 30 de `test_t142_cadena_b.py`. B no se toca, así que no lleva prueba nueva. La línea base de A sube a 637. El gate 12/12 queda para la QA, porque el encargo pedía no lanzarlo; abajo, los gates sueltos |
| Encargo de A validado antes de enviar | `test_encargo_que_no_cumple_el_esquema_de_a_no_se_envia` (4 casos), `test_opcion_desconocida_o_duplicada` y `test_paquete_invalido` (3) |
| Broker: qué opciones se envían | `test_opciones_enviables_son_las_de_enviar_a_b`, con el ejemplo publicado (7) y el ciclo simulado (3); `test_tipos_secundarios_de_la_opcion_entran_en_los_admitidos` |
| Vuelta (CT-04) | `test_ct04_de_vuelta_con_los_campos_del_anexo_b_de_a` (frente al Anexo B de A, leído como dato), `test_ct04_solo_con_lo_que_devuelve_b` y `test_ct04_lo_registra_el_bloque_a` (F3 `decision_broker`, F5 RET, integridad). En la cadena, RET-2024-0001 queda `APLICADA` |
| El script falla cerrado | `test_script_rechaza_una_correspondencia_con_claves_que_b_no_tiene`: código 2 sin llegar a ejecutar ningún bloque |

## Cadena de punta a punta (`cadena_a_b.py`)

```bash
PY .docs/scripts/cadena_a_b.py --trabajo <carpeta nueva> --sonda-sin-correspondencia    # ≈ 9 s, código 0
```

Salida resumida (dos ejecuciones dan el mismo resumen, salvo la carpeta):

| Paso | Resultado |
| --- | --- |
| Bloque A, ciclo C1 | RUN-2024-0001 `COMPLETO`, `ENTREGADA`, G3 `APTO`. DIV: OPP-2024-0001 (USD/JPY), 0002 (AUD/USD) y 0003 (USD/MXN), las tres con `ENVIAR_A_BLOQUE_B` |
| Broker | Las tres son enviables. 0002 → `divisas_materias_primas`. 0001 y 0003 → `SIN_CORRESPONDENCIA_AMBITO`: no se envían |
| Bloque B, `analizar` | PET-B-2024-0001 `ADMITIDA`. PT30 en ejecución (AUT-B-2024-0001, recomendación `CONTINUAR`); el Broker autoriza con `CONTINUAR` y el análisis termina `ENTREGADA`. REC-B-2024-0001, veredicto `VIGILAR`, `CONCLUYENTE`, G3 `APTO`, PV1–PV3 superadas. En el paquete de B, `origen` es `{tipo: BLOQUE_A, opp_id_A: OPP-2024-0002}` |
| Esquema del paquete de B | Válido (0 errores) |
| Vuelta, CT-04 al Bloque A | RET-2024-0001 `APLICADA`. `resultado_comunicado`: «Bloque B PET-B-2024-0001; admisión ADMITIDA; estado ENTREGADA; registro REC-B-2024-0001; veredicto VIGILAR; resultado CONCLUYENTE» |
| Sonda sin clave (OPP-2024-0001, USD/JPY, Japón) | El Bloque B la **admite** y su Director elige `divisas_materias_primas`; queda en PT30 (`EN_PAUSA_PUNTO_CONTROL`). No contesta `AMBITO_INDETERMINADO`. Es la evidencia para fallar cerrado en el Broker (INC-T142-01) |
| Veredicto de la cadena | `{entregadas: 1, todas_validas: true, vueltas_registradas: 1}` |

## Regresiones (mutantes a mano sobre `cadena_b.py`, cada uno restaurado después)

| Mutante | Pruebas que fallan |
| --- | --- |
| Sin fila, se usa la primera clave de la tabla (inventar) | 3 |
| Se salta la validación del encargo contra el esquema de A | 4 |
| Un campo de más en la petición | 1 |
| `x_clave_universo` por defecto aunque no haya correspondencia | 1 |
| Decisión `ENVIADA` en vez de `ENVIADA_A_BLOQUE_B` | 2 |

## Gate

No se ha lanzado `./tools/check_all.sh` (lo pedía el encargo). Gates sueltos, desde la raíz de la copia:

| Gate | Resultado |
| --- | --- |
| ruff (`ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2838 (cuota 2838). El módulo, la prueba y el script, sin hallazgos |
| mypy A (`mypy bloque_a/11_Ejecutor/bloque_a --ignore-missing-imports --no-error-summary \| wc -l`) | 109 (cuota 109); ninguno en `cadena_b.py` |
| mypy B | 159 (cuota 159), sin cambios |
| `PY tools/corpus_integridad.py` | 695 archivos coinciden |
| `PY tools/refs_vivas.py`, `nfc_check.py`, `secrets_scan.py` | Verdes |
