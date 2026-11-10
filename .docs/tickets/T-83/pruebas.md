# T-83 · Pruebas

## Ronda r02 (corrección de la QA r01)

| Suite | r01 | r02 |
| --- | --- | --- |
| `sistema_global/marco_comun_c/pruebas/pruebas_parametros_doc_t83.py` | 62 comprobaciones | 109 comprobaciones, TODAS LAS PRUEBAS PASAN (~5 s, con 12 subprocesos: la copia limpia y 11 mutaciones) |
| `.docs/tickets/T-83/r02_contra_head.py` | — | H-01 a H-06: FALLA con HEAD (`dd96e19`) y OK con el árbol: «CADA HALLAZGO FALLA ANTES Y PASA AHORA» |
| Baterías del marco (`.docs/scripts/pruebas_marco.sh`) | 61 pasan | 61 pasan, 0 fallan |
| `.docs/scripts/leeme_marco.py` | SIN DIFERENCIAS | la batería nueva ejecuta 109 y el LEEME cita 109 (`… pruebas_parametros_doc_t83.py`: SIN DIFERENCIAS). Con todas, dos diferencias que no son de T-83 (ver abajo) |

### Criterio de aceptación → prueba (lo nuevo de la r02)

| Criterio | Prueba (`pruebas_parametros_doc_t83.py`) |
| --- | --- |
| CA-1 (también campo a campo) | `cobertura_CONFIG_DEFECTO.{aprobacion,avisos,kill_switch,promocion_nivel,mandatos,referencias}_*`, `compuestas_documentadas_campo_a_campo`, `cada_subtabla_es_de_su_clave_compuesta`, `toda_compuesta_de_campos_fijos_va_campo_a_campo` |
| CA-2 | `ratificado_con_pregunta_o_cerrado_por_una_decision_ratificada`, `cerrada_por_solo_en_ratificados_sin_pregunta`, `compuesta_sin_pregunta_propia_y_con_el_estado_de_sus_campos`, `registros_con_todos_sus_campos` |
| CA-5 | `doc_de_un_campo_con_punto`, `doc_ambiguo_entre_subtablas_es_ValueError` |
| CA-7 · H-01 | `la_D16_esta_ratificada_y_cierra_el_apalancamiento`, `apalancamiento_ratificado_por_D16_sin_pregunta_POLITICA_DEFECTO`, `apalancamiento_ratificado_por_D16_sin_pregunta_CONFIG_DEFECTO.mandatos`, `apalancamiento_documentado_es_sin_apalancar`, `ninguna_pregunta_pendiente_ofrece_apalancamiento`, `exposicion_cita_D16_y_no_ofrece_pasar_del_total`, `los_ratificados_son_los_de_la_constitucion`; mutación `apalancamiento_otra_vez_propuesto` |
| CA-7 · H-02 | `aprobacion_pregunta_cada_valor`, `aprobacion_canal_con_segundo_factor_de_la_D19`, `aprobacion_perdida_que_activa_la_espera_de_la_D18`, `mandatos_documentados_campo_a_campo`, `mandatos_pregunta_instrumentos_y_exclusiones`, `faltan_detecta_un_campo_nuevo_o_quitado_en_una_compuesta`, `faltan_detecta_una_compuesta_que_deja_de_serlo`; mutaciones `subclave_nueva_en_aprobacion`, `subclave_nueva_en_promocion` y `campo_nuevo_en_el_mandato` |
| CA-7 · H-03 | `aprobacion_horario_es_espera_y_no_prohibicion` |
| CA-7 · H-04 | `revision_pregunta_por_el_maximo`, `rangos_de_cambio_se_preguntan_como_confirmacion`, `referencia_dice_que_es_un_marcador_contra_el_7` |
| CA-7 · H-05 | `valores_documentados_al_dia`, `valor_documentado_igual_al_del_codigo_en_cada_registro`, `desfasados_detecta_un_valor_cambiado`, `desfasados_detecta_una_entrada_nueva_en_un_mapa`; mutaciones `valor_cambiado_en_parametros` y `valor_cambiado_en_politica` |
| CA-7 · H-06 | `preguntas_pendientes_falla_cerrado_como_faltan`, `preguntas_pendientes_con_el_codigo_de_hoy` |

### Regresiones: fallan sin la corrección

- **Prueba contra HEAD.** `.venv/bin/python -I .docs/tickets/T-83/r02_contra_head.py` evalúa cada hallazgo con el mismo criterio que la batería. Usa el `parametros_doc.py` de HEAD (`dd96e19`, el de la r01) y el del árbol, y da:

  ```
  H-01: HEAD FALLA · árbol OK
  H-02: HEAD FALLA · árbol OK
  H-03: HEAD FALLA · árbol OK
  H-04: HEAD FALLA · árbol OK
  H-05: HEAD FALLA · árbol OK
  H-06: HEAD FALLA · árbol OK
  RESULTADO r02 CONTRA HEAD: CADA HALLAZGO FALLA ANTES Y PASA AHORA
  ```

  La batería entera no arranca con el módulo de HEAD, porque usa la API nueva (`TODAS`, `SUBTABLAS`, `desfasados()`).
- **Mutaciones de la batería.** Las seis mutaciones nuevas de la batería (H-01, H-02 y H-05) fallan por la comprobación esperada, y la copia sin cambios pasa.
- **Sondas de la QA.** `entrega_claude/V0.72/qa/r01_mutaciones_bateria.py` da ahora «5 DISTINTAS DE LO ESPERADO», y las cinco diferencias son las corregidas:
  - las cuatro mutaciones que en la r01 «vivían» (`subclave_nueva_en_aprobacion`, `subclave_nueva_en_promocion`, `valor_cambiado_justificacion_rancia` y `valor_cambiado_politica_justificacion_rancia`) ahora matan la batería;
  - `estado_apalancamiento_a_ratificado` ya no encuentra su texto, porque `apalancamiento_max` ya es RATIFICADO.
- **Corrección de la propia batería.** En la primera versión de la r02, una copia mutada hacía lanzar `preguntas_pendientes()` (ValueError, que es lo correcto desde H-06) y las búsquedas de `doc()` sobre campos nuevos, de modo que la batería moría por una excepción y no por la comprobación esperada. Ahora `preguntas_pendientes_con_el_codigo_de_hoy` lo registra como FALLA y la batería sigue; las 11 mutaciones fallan por su comprobación y con «HAY FALLOS».

### Baterías de otros trabajos

`leeme_marco.py` da dos diferencias que no son de T-83: `pruebas_reloj_t03.py` ejecuta 80 y el LEEME cita 77, y `pruebas_semana.py` ejecuta 176 y el LEEME cita 123. Esos ficheros los están cambiando a la vez otros trabajos (V0.73 y T-84), que no han actualizado todavía su fila del LEEME. Con la batería de T-83 sola: SIN DIFERENCIAS.

### Gate

`.docs/scripts/gate.sh --completo` (log `gate_20261110_195928.log` en la carpeta de logs de `.docs/scripts/`) da 12 de 12 en verde, «TODOS LOS GATES PASARON»:
- corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas y ruff;
- mypy A, A-Forex y B;
- pytest A 326, A-Forex 68 y B 176.

El árbol tiene, además de T-83, los cambios sin commit de otros trabajos: el bloque A con T-65, y el marco con V0.73.

## Ronda r01

| Suite | Antes | Después |
| --- | --- | --- |
| `sistema_global/marco_comun_c/pruebas/pruebas_parametros_doc_t83.py` | no existía | 62 comprobaciones, TODAS LAS PRUEBAS PASAN (~3 s, con 6 subprocesos) |
| Baterías del marco (`.docs/scripts/pruebas_marco.sh`) | 60 pasan | 61 pasan, 0 fallan |
| `.docs/scripts/leeme_marco.py` | — | SIN DIFERENCIAS (0); la batería nueva ejecuta 62 y el LEEME cita 62 |
| pytest A · A-Forex · B (gate completo) | 317 · 68 · 176 | 317 · 68 · 176 (sin tocar) |

La matriz de criterios CA-1 a CA-6 de la r01 sigue valiendo, con las pruebas renombradas en la r02:
- `registros_con_los_cuatro_campos` pasa a `registros_con_todos_sus_campos`;
- `ratificado_con_pregunta` pasa a `ratificado_con_pregunta_o_cerrado_por_una_decision_ratificada`;
- `politica_f_tecnico_porque_sus_limites_van_uno_a_uno` pasa a `compuestas_documentadas_campo_a_campo`, porque `politica_f` ya no es TECNICO sino compuesta.

Las demás pruebas de la r01 se mantienen:
- **Cobertura:** `cobertura_*` y `faltan_*`.
- **Forma:** `estado_*`, `fuente_*`, `justificacion_*`, `pregunta_*` y `tecnico_*`.
- **Marcas:** `marcas_*` y `el_analisis_*`.
- **Consulta y no cambios:** `doc_*`, `por_estado_*`, `preguntas_pendientes_*` y `no_cambia_*`.
- **Mutaciones:** las cinco mutaciones originales.

En la r01, el gate completo dio 11 de 12, con `mypy bloque_b` en 160 frente a una cuota de 159. Venía de HEAD `99160b3` (T-90), y `dd96e19` lo devolvió a 159.

Comandos usados:

```
.venv/bin/python -I .docs/tickets/T-83/r02_contra_head.py
cd sistema_global/marco_comun_c && ../../.venv/bin/python -I pruebas/pruebas_parametros_doc_t83.py
cd sistema_global/marco_comun_c && ../../.venv/bin/python -I entrega_claude/V0.72/qa/r01_mutaciones_bateria.py
.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c
.docs/scripts/pruebas_marco.sh
.docs/scripts/gate.sh --completo
```
