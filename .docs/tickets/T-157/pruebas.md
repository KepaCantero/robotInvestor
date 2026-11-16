# T-157 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`bloque_a/11_Ejecutor`, completa) | 6624 superadas, 2 omitidas, 0 fallos (6626 recogidas; 36 min 53 s) | 6660 recogidas: las 6626 de antes, sin cambios, más las 34 de `tests/test_t157_verificador_ids.py`, que pasan |
| `tests/test_t157_verificador_ids.py` | — (no existía) | 34 superadas (7 s) |
| Suites que leen `docs/incidencias.md` o los README (`test_t65_resto_t53`, `test_fase3_goldens`, `test_t148`), otra vez con los cambios | en verde | 185 superadas, junto con las 34 nuevas |
| Bloque A Forex, Bloque B | no se tocan | no se ejecutan (regla 8; ningún archivo suyo cambia) |

La pasada completa se lanzó en el commit `4f7ea73`, antes de añadir la prueba nueva. El cambio no toca código existente: es
un módulo nuevo que ninguna otra prueba importa, más documentación. Por eso no se repitió la suite entera (≈37 min); sí se
repitieron las suites que leen los documentos tocados.

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 (orden, JSON y Markdown, salidas 0/1) | `test_orden_de_consola_escribe_json_y_markdown` (subproceso `python -m`, salida 1 con errores), y la ejecución real (salida 1, 3 errores) |
| CA-2 (un fallo de cada clase a–e, más f) | `test_a_contratos`, `test_b_reglas`, `test_c_archivos_y_mapa_por_h1`, `test_d_fichas_cuatro_clases`, `test_d_menciones_de_otra_version_y_secciones`, `test_e_referencias`, `test_f_puertas`, `test_un_error_de_cada_clase`, `test_cada_hallazgo_con_ubicacion_real` |
| CA-3 (mapa F por H1, nombre distinto) | `test_c_archivos_y_mapa_por_h1` |
| CA-4 (fallo cerrado) | `test_sin_documento_0_falla_cerrado`, `test_dos_documentos_0_fallan_cerrado`, `test_sin_catalogo_falla_cerrado`, `test_sin_seccion_del_documento_0_falla_cerrado` (×5), `test_main_sale_2_y_no_escribe`; límite NFC: `test_documento_0_en_nfd_se_encuentra` |
| CA-5 (versión, huellas, determinismo) | `test_determinista_con_version_y_huellas`, `test_version_del_titulo_distinta_avisa`, `test_rango_del_titulo_contra_la_tabla` |
| CA-6 (esquema) | `test_informe_que_no_valida_no_se_escribe` |
| CA-7 (sin `99_Historico*` ni `11_Ejecutor`) | `test_no_lee_historico_ni_ejecutor`, `test_real_no_lee_historico` |
| CA-8 (corpus y código reales contados aparte) | `test_real_documento_0_por_patron`, `test_real_fichas_contadas_aparte`, `test_real_contratos_contados_aparte` |
| Código frente al Catálogo (versión, ruta, madurez leída, literales) | `test_version_ruta_y_madurez_leida_del_codigo`, `test_catalogo_que_promete_lo_que_el_codigo_no_sirve`, `test_codigo_sin_promover_y_no_servible` |
| Contextos que no son citas | `test_contextos_que_no_son_citas` |
| CA-9 (auditoría e incidencias) | `test_auditoria_solo_cambia_entre_marcas`; `docs/auditoria_ids_bloque_a.md` con D-1 a D-4 y `docs/incidencias.md` con INC-T157-01 a 05 (revisión manual) |
| CA-10 (suite, cuotas, gates) | sección «Gate» |

## Regresiones

No hay fallo corregido (pieza nueva). En su lugar, mutantes (`.docs/tickets/T-157/mutantes_t157.py`, desde
`bloque_a/11_Ejecutor`): cada uno quita una protección y la prueba citada falla; el mutante nulo, de control, la deja pasar.

| Mutante | Prueba | Resultado |
| --- | --- | --- |
| nulo (control) | `test_a_contratos` | pasa (vivo, como debe) |
| lee `99_Historico*` | `test_no_lee_historico_ni_ejecutor` | falla (matado) |
| sin contextos ajenos | `test_contextos_que_no_son_citas` | falla (matado) |
| sin emparejar ID parecidos | `test_d_fichas_cuatro_clases` | falla (matado) |
| sin validar el esquema | `test_informe_que_no_valida_no_se_escribe` | falla (matado) |
| Documento 0 sin exigir uno solo | `test_dos_documentos_0_fallan_cerrado` | falla (matado) |
| `canal_permitido` ignorado | `test_a_contratos` | falla (matado) |

## Gate

No se pasó `./tools/check_all.sh` completo: ejecutaría otra vez las tres suites (más de 40 min), y la sesión coordinadora pidió
una sola pasada de A y los gates ligeros. Uno a uno:

| Gate | Resultado |
| --- | --- |
| corpus-integridad (`tools/corpus_integridad.py`) | «Corpus íntegro: 695 archivos coinciden con el manifiesto congelado.» |
| nombres-nfc (`tools/nfc_check.py`) | en verde |
| yaml-configs | los tres `por_defecto.yaml` parsean |
| secrets (`tools/secrets_scan.py`) | sin hallazgos |
| refs-vivas (`tools/refs_vivas.py`) | en verde, ya sin las dos líneas de la Fase 0 en `tools/refs_allowlist.txt` |
| ruff (cuota 2831) | 2831 (los dos archivos nuevos, limpios) |
| mypy bloque_a (cuota 109) | 109 (el módulo nuevo, sin errores) |
| pytest bloque_a (≥ 607) | 6624 + 34, sin fallos |
| `.docs/scripts/pruebas_*.py` | no aplica: no se tocó `.docs/scripts/` |

Las cuotas quedan iguales, no más bajas: bajarlas obligaría a tocar código ajeno a esta tarea (regla 9 de `ri-implementar`).

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider                                 # suite completa (antes)
../../.venv/bin/python -m pytest -q -p no:cacheprovider --collect-only | tail -1        # 6660
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t157_verificador_ids.py
../../.venv/bin/python ../../.docs/tickets/T-157/mutantes_t157.py
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids \
  --json ../../docs/auditoria_ids_bloque_a.json --auditoria ../../docs/auditoria_ids_bloque_a.md   # salida 1: 3 errores
cd ../..
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
```

## Ronda r02 (16-11-2026)

En la copia `t157r02` (HEAD `6220a38`, con T-157, T-158, T-159 y T-160 integrados).

| Suite o comprobación | Resultado |
| --- | --- |
| Suite completa de A, una pasada en segundo plano (`../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | **6765 superadas, 2 omitidas, 0 fallos** (59 min); 6767 recogidas, 46 de ellas de T-157 (12 nuevas) |
| `tests/test_t157_verificador_ids.py` en su versión final (la suite se recogió antes de tres retoques de aserciones: R28 en la línea con «JEL» y el caso del destino al revés) | 46 superadas |
| `.docs/tickets/T-157/mutantes_t157.py` (6 de r01 y 7 nuevos, de las reglas de r02) | nulo vivo; los 13, matados |
| `revisores/r01_01_cifras.py <informe nuevo>` | «FALLOS: ninguno» (salida 0) |
| `revisores/r01_02_siembra.py` | 39/43. Fallan 4, todos esperados: «RF de 3 cifras» y «RF de 5 cifras» (H-04, se mantiene AVISO a propósito, INC-T157-01) y los dos «T-143: mismos 3 errores», que fijan 3 y ahora son 2 porque T-160 corrigió D-1 (la copia base da los mismos 2). Pasan ya las de H-01 (mismo JSON con 4 semillas, y el del repositorio coincide), H-02, H-03, H-05 y H-06 |
| `revisores/r01_03_mutantes.py` | 25 matados de 27, 1 vivo y 1 roto: M13 vivo por el arnés, como en r01 (la prueba de consola en subproceso lo mata con el cambio escrito en el archivo); M10 roto porque su texto ya no existe (la regla del campo JSON se sustituyó; su equivalente, «r02 cualquier campo JSON declara símbolo», muere en `mutantes_t157.py`). M01–M07, M09, M12, M14, M20, M21 y M26, vivos en r01, ahora matados |
| Determinismo: `PYTHONHASHSEED` 0, 1, 3, 7 y 42 con el corpus real | un solo JSON y un solo Markdown |
| ruff (las tres carpetas de ejecutor, cuota 2825) | 2825 |
| mypy `bloque_a/11_Ejecutor/bloque_a` (cuota 109) | 109; ninguno en `verificador_ids.py` |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py`, YAML | en verde; «Corpus íntegro: 695 archivos» |
| Informe real regenerado | 2 errores, 2 avisos, 12 notas (salida 1): FX-MC10-003 y RF-0123; 8 menciones al «Catálogo V4.0» y RF-1 |

### Criterio → prueba (r02)

| Hallazgo | Prueba |
| --- | --- |
| H-01 | `test_r02_clave_id_desempata_por_la_cadena`, `test_r02_mismo_json_y_markdown_con_semillas_distintas` |
| H-02, H-03, H-05 | `test_r02_contextos_no_excusan_de_mas`, `test_r02_rango_de_funciones_con_un_extremo_ajeno_no_excusa`, `test_contextos_que_no_son_citas` |
| H-06 | `test_r02_destino_imposible_sale_2_y_no_escribe_nada` |
| H-07 | `test_r02_filas_y_fichas_duplicadas_y_total`, `test_r02_ct_solo_en_canales_v6_o_campos_minimos`, `test_r02_alternativa_sin_ficha_y_referencia_definida_y_de_baja`, `test_r02_versiones_escritas_en_los_py`, `test_r02_el_paquete_real_no_escribe_otra_version_del_catalogo`, `test_r02_validar_informe_comprueba_errores_y_auditoria_marcas_repetidas`, `test_r02_orden_de_hallazgos_con_desempate_por_codigo`, `test_nombres_en_nfd_se_encuentran`, `test_no_lee_historico_ni_ejecutor` (carpeta con punto) |

### Comandos (r02)

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --json /tmp/r02.json          # salida 1: 2 errores
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_01_cifras.py /tmp/r02.json
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_02_siembra.py
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_03_mutantes.py
../../.venv/bin/python ../../.docs/tickets/T-157/mutantes_t157.py
for s in 0 1 3 7 42; do PYTHONHASHSEED=$s ../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --json /tmp/h$s.json; done; md5sum /tmp/h*.json
```

## Mensaje de commit propuesto (para la sesión coordinadora)

```
fase0: verificador de consistencia de IDs del Bloque A (T-157) [pendiente QA]

`python -m bloque_a.herramientas.verificador_ids` (desde bloque_a/11_Ejecutor) escanea el corpus
vigente (Documento 0 y Catálogo por patrón, falla cerrado con cero o más de uno; sin 99_Historico*)
y el código, y emite un informe JSON validado contra su esquema y otro en Markdown: contratos CT,
reglas R, archivos F con su archivo real por H1, fichas del Catálogo (IMPLEMENTADO, SOLO_CATALOGO,
SOLO_CODIGO, ID_DISTINTO), referencias de 05_Archivos_operativos y puertas PS.

Resultado (docs/auditoria_ids_bloque_a.md y .json): el desfase V4.0-V5.0 está resuelto en el
código (81 fichas IMPLEMENTADO: 80 por CT-09 y AUD-REX-001 por CT-10); quedan 3 errores
(catalog_version 4.0 escrito en evaluador.py, la ficha FX-MC10-003 del ejemplo de RC y RF-0123
en un ejemplo del Evaluador) y 8 menciones al «Catálogo V4.0» en el corpus. Cuatro decisiones
propuestas, sin aplicar (INC-T157-01 a 05). 34 pruebas nuevas; suite de A sin fallos; ruff 2831
y mypy A 109, sin cambios; refs_allowlist sin las líneas de la Fase 0.
```

Con las líneas de atribución que corresponda a la sesión que haga el commit.

Mensaje propuesto para la r02:

```
fase0: T-157 r02 (QA r01 NO APTO): el informe del verificador de IDs es el mismo en cualquier proceso (desempate por la cadena), una ficha en un valor JSON ya no se excusa salvo que el corpus la declare símbolo de una serie, contextos que solo excusan lo que llevan dentro (lista JEL, fórmula en F, rango de funciones), familias desconocidas, minúsculas y guion U+2011, destino imposible con salida 2 sin escribir nada; D-1 a D-4 en el registro de decisiones; informe regenerado (2 errores y 2 avisos tras T-160) [pendiente QA]
```
