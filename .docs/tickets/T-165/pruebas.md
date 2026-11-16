# T-165 · Pruebas

Copia: worktree en la instantánea `189ee55` con `.venv` enlazado; sin red ni gasto (cliente simulado). Todo desde
`bloque_a/11_Ejecutor` con `../../.venv/bin/python` salvo los gates y las cuotas (desde la raíz). Ojo: el ejecutable `bloque-a`
del `.venv` enlazado importa el paquete de la copia principal; para el backtest se usa `python -m bloque_a.cli` desde esta carpeta.

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A completa (`pytest -q -p no:cacheprovider`) | 6897 recogidas (HEAD) | 6944 recogidas (+47). Una ejecución completa (85 min, carga 12–16, con 41 de las 47 nuevas, las que había al empezar): 6934 superadas, 2 omitidas y 2 fallos, explicados abajo |
| `tests/test_t165_g3_met13.py` (nueva) | — | 47 superadas |
| `tests/test_t159_extremo_a_extremo.py` | 10 | 10 superadas (sin cambios en el fichero) |
| `10_Herramientas/tests` (referencia de HT-09, HT-03, HT-07, HT-02) | 135 | 135 superadas, 38 subpruebas |
| Sonda de la QA de T-159 (`r01_02_sondas.py -k pb47`) | falla (APTO, APTO; técnico y JSON con «validado») | pasa (BLOQUEADO, APTO_CON_ADVERTENCIAS, APTO_CON_ADVERTENCIAS; ningún entregable con «validado») |
| Goldens (`tests/goldens_ct.py`) | coinciden | coinciden |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 (PB-47 con su preparación completa bloquea) | `test_pb47_informe_de_clase_que_llama_validado_a_un_metodo_documentado_bloquea_g3`; la sonda `r01_02_sondas.py -k pb47` |
| CA-2 (ML-CLUS-001 en DOCUMENTADO sin siembra se entrega) | `test_pb47_corregida_la_declaracion_documentado_la_entrega_pasa`; `test_t159_extremo_a_extremo.py::test_pb47_un_metodo_documentado_no_se_usa_y_la_entrega_lo_declara` (sin cambios) |
| CA-3 (ciclo normal APTO, G3-MET-13 OK) | `test_el_ciclo_simulado_normal_sigue_apto_y_la_comprobacion_ve_las_fichas` (doce tipos); medido además con dos ciclos de los doce tipos y con el backtest de `CLAUDE.md` (13 ciclos: 26 G3V-, todos APTO con G3-MET-13 OK) |
| CA-4 (qué bloquea y qué no) | `test_bloquea_una_madurez_que_el_catalogo_no_da_o_un_metodo_que_no_se_sirve` (14 casos), `test_no_salta_con_frases_que_no_sobredeclaran` (20 casos, entre ellos los ejemplos de `estado_madurez_metodos` de los prompts de los Analistas y «validado por el operador»), `test_sin_catalogo_legible_toda_mencion_bloquea`, `test_textos_de_lleva_el_opp_en_la_ruta_y_lee_el_campo_de_madurez_con_su_metodo`, `test_texto_html_separa_frases_por_etiquetas` |
| CA-5 (formato de HT-09 y dictamen recalculado) | `test_formato_de_hT09_y_severidad_advertencia_sin_extracto`, `test_recalcular_dictamen_y_motivo_como_la_referencia`, `test_g3_met13_localiza_en_la_opcion_y_advierte_de_lo_que_no_se_entrega`, `test_g3_met13_visual_ilegible_falla_cerrado`, `test_una_mencion_repetida_en_la_misma_ruta_se_anota_una_vez` |
| CA-6 (técnico y visual en F7) | `test_un_metodo_no_servido_solo_en_el_tecnico_bloquea_la_entrega_en_f7`, `test_un_visual_que_presenta_un_metodo_como_validado_bloquea_en_f7` |
| CA-7 (PB-47 Superada) | `tests/mapa_plan_pruebas.json` (AUTOMATICA) y `docs/evidencias_pruebas_bloque_a.md` regenerado con `--ejecutar`: «204 de 204 pruebas citadas superadas»; 31 Superada · 27 en parte (antes 30 · 28); PB-47 «Superada» |
| CA-8 (suite, goldens, gates, cuotas) | abajo |

## Los dos fallos de la ejecución completa

- `tests/test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`: esperado mientras el mapa (PB-47 ya
  AUTOMATICA) iba por delante de `docs/evidencias_pruebas_bloque_a.md`. Tras `--ejecutar`, `tests/test_fase4_mapa.py` pasa entero.
- `tests/test_t102_filtro.py::test_r05_h37_sufijo_en_tiempo_lineal`: prueba de tiempo (2,5–2,9 s frente a un tope de 2 s) con la
  máquina a carga 12–16 por otras suites. Repetida sola falla igual **también sobre una exportación de HEAD** (`git archive HEAD`, sin
  T-165): es la carga. Mide `diseno_v6.frase_prohibida`, que T-165 no toca; la QA de T-159 anotó lo mismo.

Repetidas después con el código final (la ejecución completa empezó antes de la excepción «validado por el operador» y de seis
casos nuevos): `tests/test_fase4_mapa.py`, `tests/test_t165_g3_met13.py`, `tests/test_t159_extremo_a_extremo.py` y la sonda
pb47 de T-159 → 81 superadas; goldens, gates y cuotas, igual.

## Falsos positivos medidos

- Ciclo simulado normal, doce tipos, dos semanas (sondeo propio): 4 G3V- APTO, G3-MET-13 OK; la comprobación ve ST-DESC-001,
  RISK-DD-001 y ML-CLUS-001 (servidas) en el técnico y el JSON.
- Backtest de `CLAUDE.md` (`--desde 2024-01-05 --hasta 2024-03-29`, configuración por defecto): 13 ciclos, 26 G3V- APTO, G3-MET-13
  OK en todos.
- ML-CLUS-001 en DOCUMENTADO sin siembra: APTO y se entrega (antes del arreglo del rótulo, el técnico lo habría bloqueado).
- Frases: las 20 de `test_no_salta_…`. Dos frases realistas («umbral validado por el operador» y «tesis validada por el dato de
  empleo», en una frase que también cita ST-DESC-001) bloqueaban en la primera versión; ahora no (lista cerrada de INC-T165-01).

## Regresiones

Mutantes temporales en la copia (restaurados después; `git diff` igual que antes):

| Mutante | Qué falla |
| --- | --- |
| Sin `g3_met13` en `ht09_validar` | `test_pb47_informe_…_bloquea_g3` y `test_un_visual_…_bloquea_en_f7` |
| El rótulo antiguo «N efectivo ML-CLUS-001» siempre | `test_pb47_corregida_…_la_entrega_pasa` y la de T-159 `test_pb47_un_metodo_documentado_no_se_usa_y_la_entrega_lo_declara` |
| Sin `g3_met13_tecnico` en `redaccion.generar` | `test_un_metodo_no_servido_solo_en_el_tecnico_bloquea_la_entrega_en_f7` |

En HEAD (`189ee55`) la sonda de T-159 falla (APTO, APTO y «validado» en el técnico y el JSON) y las pruebas nuevas no se pueden
importar (no existe `ht09.comprobar_madurez`).

## Gate

- Gates ligeros desde la raíz (`for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done`):
  `refs_vivas`, `secrets_scan` y `nfc_check` en verde; `corpus_integridad`: 695 archivos coinciden. Goldens: coinciden.
- Cuotas desde la raíz: ruff **2818** (≤ 2821; antes 2821: se quitan los tres avisos que ya tenía `ht09.py`; `tools/cuotas.txt` no se
  toca, lo baja la sesión coordinadora si quiere) · mypy de A **109** (≤ 109; la misma lista de errores que en HEAD, comparada línea a
  línea).
- `./tools/check_all.sh` completo no se ejecuta en esta copia (otras suites corriendo); sus piezas están arriba.

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t159_extremo_a_extremo.py tests/test_fase4_mapa.py
../../.venv/bin/python tests/goldens_ct.py
(cd ../10_Herramientas && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests)
../../.venv/bin/python -m pytest -q -p no:cacheprovider          # suite completa, en segundo plano
../../.venv/bin/python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --salida /tmp/salida_mock backtest --desde 2024-01-05 --hasta 2024-03-29
cd ../..
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
```
