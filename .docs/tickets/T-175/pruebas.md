# T-175 · Pruebas

| Suite | Antes (80751da) | Después |
| --- | --- | --- |
| Bloque A, pytest (recogidas) | 7975 | 7984 (+9, `tests/test_t175_alternativas.py`) |
| Bloque A, en el gate | — | 7982 superadas (las 2 restantes son omisiones previas, `skipif`/`skip`); base 607 |
| Bloque A-Forex, en el gate | 68 | 68 |
| Bloque B, en el gate | 176 | 176 |
| Relacionadas (`test_t165_g3_met13`, `test_autocritica`, `test_integracion`, `test_fase3_goldens`, `test_t53_seleccion_y_entrega`) | — | 388 superadas |
| Plan de pruebas (`evidencias_plan_a.py --ejecutar`) | Superada 32 · en parte 26 | Superada 33 · en parte 25 (PB-38); 216 de 216 citadas superadas |
| Mutantes propios (`.docs/tickets/T-175/mutantes.py`) | — | 12/12 muertos |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_pb38_la_opcion_con_objecion_fuerte_sin_resolver_es_una_alternativa_documentada_en_el_tecnico`, `test_pb38_tambien_en_el_diseno_v6`, `test_objeciones_de_la_alternativa_estado_y_condicion` |
| CA-2 | las mismas dos primeras (fila de la sección 6 con la `OPP-` y `SIN_RESOLVER`) |
| CA-3 | `test_pb38_la_alternativa_no_entra_en_el_json_ni_altera_la_coherencia_ni_el_dictamen`, `test_objecion_fuerte_sin_resolver_excluye_del_top3` (ya existía) |
| CA-4 | `diff_tecnico.py comparar`, que se pasó dos veces. Ciclo mock de doce clases: 10 líneas nuevas esperadas y 0 cambios fuera de lo esperado. V6 de doce clases (revisor `r01_03`): solo 4.2.4, 4.4.4 y 4 filas de la sección 6; JSON y visual idénticos. Backtest mock del README (13 ciclos, solo DIV): 0 cambios en los 13 técnicos. JSON, visual, `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos. `consumo.csv` solo difiere en la columna de duración, y F5 y los sellos en la carpeta de salida |
| CA-5 | `test_solo_se_listan_las_no_elegibles_que_no_son_opcion_ni_vigentes_ni_de_arrastre_en_orden_de_rk`, `test_un_texto_con_barra_o_salto_de_linea_no_rompe_las_tablas`, `test_tecnico_sin_seleccion_en_extras_no_cambia` |
| CA-6 | (r02) `test_un_texto_del_modelo_que_g3_met13_rechaza_en_una_alternativa_se_retira_y_la_entrega_sale` (ficha desconocida y «validada» persistente: ENTREGADA, texto sustituido, ADVERTENCIA en HA), `test_la_sustitucion_cubre_nombre_resumen_respuesta_y_que_la_resolveria`; además, la parte final de `test_pb38_la_alternativa_no_entra…` comprueba que no aparece la raíz «valid-» en 4.N.4 |
| CA-7 | mapa y evidencias (PB-38 «Superada»), gate 12/12, cuotas |

## Regresiones

- **Sin la corrección:** con `redaccion.py` y `sintesis.py` de 80751da, 7 de las 8 pruebas que había entonces fallan. Pasa `test_tecnico_sin_seleccion_en_extras_no_cambia`, que es una prueba de no regresión. La prueba V6 se añadió después y es la misma comprobación.
- **Mutantes (12, todos muertos):**
  - sin la subsección;
  - sin las filas de la sección 6;
  - filtro de elegibilidad invertido;
  - vigentes listadas;
  - listas de arrastre;
  - estado siempre RESPONDIDA;
  - regla del estado sin exigir la resolución;
  - sin «qué la resolvería»;
  - sin los `OBJ-` en el motivo;
  - orden ascendente;
  - sin escapar «|»;
  - sin las moderadas.

## Gate

`./tools/check_all.sh` en la copia `t175` (con `.venv` enlazado al del repo): **12/12**.

- corpus, NFC, YAML, secretos y refs-vivas en verde;
- ruff 2813 / 2813;
- mypy A 102 / 102 (antes 109; la cuota baja a 102);
- mypy A-Forex 174 / 174;
- mypy B 159 / 159;
- pytest: A 7982, A-Forex 68, B 176.

Comandos:

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t175_alternativas.py
.venv/bin/python .docs/tickets/T-175/mutantes.py
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/diff_tecnico.py generar despues.md   # y comparar antes.md despues.md
python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv --salida <dir> backtest --desde 2024-01-05 --hasta 2024-03-29   # en las dos copias
./tools/check_all.sh
```

## Ronda r02 (QA r01 NO APTO), sobre origin/develop `375d24b`

| Suite | develop `375d24b` | r02 |
| --- | --- | --- |
| Bloque A, pytest (recogidas) | 8149 | 8160 (+11: `test_t175_alternativas.py`, con la prueba de H-01 en dos variantes) |
| Bloque A, en el gate | — | 8158 superadas (2 omisiones previas) |
| A-Forex · B, en el gate | 68 · 176 | 68 · 176 |
| `test_t165_g3_met13` + `test_t175_alternativas` + `test_autocritica` | — | 160 superadas |
| Plan de pruebas (`--ejecutar`) | — | 217 de 217 citadas superadas · Superada 33 · en parte 25 |
| Mutantes propios | — | 22/22 muertos (los 12 de la r01, 6 de H-01 y 4 de H-02) |

**Pruebas del revisor**

- **`r01_01_casos_raros.py`:** 0 RARO. Los casos «motivos int», «_objeciones int» y «RK True/nan/inf» salen OK.
- **`r01_02_met13_alternativa.py`:**

  | Modo | Texto | Entrega | Detalle |
  | --- | --- | --- | --- |
  | `alternativa` | ficha desconocida, modelo que obedece | ENTREGADA | APTO_CON_ADVERTENCIAS; en F7, G3-MET-13 ADVERTENCIA; 4.N.4 presente; ninguna «validada» en el técnico |
  | `alternativa` | sin más argumentos (la raíz persiste) | ENTREGADA | ídem |
  | `opcion` | ficha desconocida, modelo que obedece | ENTREGADA | F6 retira la opción, top-3 sin XLU |
  | `opcion` | sin más argumentos | ENTREGADA | ídem |

- **`r01_03_regresion.py`:** frente a develop. V5 y V6 de doce clases, ENTREGADA APTO. JSON y visual idénticos. En el técnico, solo 4.1.4 (V5) y 4.2.4 y 4.4.4 (V6), con sus filas de la sección 6.

**Ciclos mock frente a develop**

- `diff_tecnico.py`: 10 líneas nuevas esperadas y 0 cambios fuera de lo esperado.
- Backtest mock del README: 13 técnicos sin cambios. `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos.

**Regresión**

Con `sintesis.py` y `redaccion.py` de la r01 fallan 4 pruebas: la de filtro y orden (H-02), las dos variantes de H-01 y la de la sustitución.

**Gate**

`./tools/check_all.sh`: **12/12**.
- ruff 2813 / 2813;
- mypy A 102 / 102;
- mypy A-Forex 174;
- mypy B 159.

## Ronda de cierre de la QA r02 (H-04)

**Pruebas**
- `test_t175_alternativas.py` + `test_t165_g3_met13.py`: 160 superadas. `test_t175` tiene 13 pruebas.
- Mutantes: 25 de 25 muertos (+3 de H-04).

**Scripts del revisor**
- `r02_01_fugas_y_orden_ha.py`: 70 OK, 0 FUGA, 0 TAPA.
- `r01_02`, modo `alternativa`, con la ficha desconocida y con «validada» persistente: ENTREGADA.
- `r01_02`, modo `opcion`: ENTREGADA, sin XLU.
- `r01_03` frente a develop `375d24b`, V5 y V6: ENTREGADA APTO; el JSON y el visual son idénticos. En el técnico solo hay líneas nuevas (10 en V5 y 20 en V6) y ninguna quitada.

**Cuotas**
- ruff 2813 (límite 2813);
- mypy A 102 (límite 102).

No se volvió a ejecutar la suite completa: no se pidió en esta ronda.
