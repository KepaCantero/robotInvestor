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

## Ronda r02 (QA r01: H-01 a H-12)

Copia `t165r02` (HEAD `3d685ed`). Sin red ni gasto. El contenedor se reinició dos veces; la suite completa se relanzó una vez con
el código final.

| Suite | Antes (r01) | Después (r02) |
| --- | --- | --- |
| `tests/test_t165_g3_met13.py` | 47 | **162** superadas |
| Bloque A completa | — | 7297 recogidas: **7294 superadas, 2 omitidas, 1 fallo** (`test_fase4_mapa::test_h05`, el documento de evidencias, que iba por detrás del mapa: tras `--ejecutar`, pasa) en 41 min |
| Banco del revisor `r01_01` (105 casos) | 62 fallan (40 escapes, 20 falsos positivos, H-09 y el tiempo) | **0 fallan** |
| Extremo a extremo `r01_02` (14 casos) | fallaban los `test_escapa_*` y `test_fp_*` de H-01 a H-07 | **13 pasan**. El que falla (`guion_no_separable`) es un ValueError del propio script (su tupla no tiene el tercer elemento); con la misma siembra, a mano: F6 BLOQUEADO, opciones retiradas, nada entregado con la frase |
| Ciclos normales `r01_03` (10 ciclos, V5, V6 y solo DIV) | 20 G3V-, G3-MET-13 OK | 20 G3V-, G3-MET-13 OK; entregables **idénticos** a los de la r01 (`diff -r` sin diferencias, con la ruta de trabajo normalizada) |
| Sonda pb47 de T-159 y `tests/test_t159_extremo_a_extremo.py` | pasan | pasan |
| Mutantes (`r02_mutantes.py`, 31: los nueve vivos de la r01 y 22 de las reglas nuevas) | r01: 9 vivos | **0 vivos** |
| Bancos nuevos (`r02_bancos_frases.py`) | — | banco 1 (usado para ajustar): legítimas que bloquean 1 de 20, falsas que pasan 0 de 15 (antes del ajuste, 5 de 20 y 0 de 15). Banco 2 (sin ajustar): **1 de 15 y 0 de 10** |
| Goldens | coinciden | coinciden |

### Hallazgo → prueba

| Hallazgo | Pruebas del ticket |
| --- | --- |
| H-01 | `test_r02_bloquea[h01_*]` (datos, mercado, evidencia, fuentes) y `test_r02_no_salta[h01_*]` (las seis personas); mutante N01 |
| H-02 | `test_r02_bloquea[h02_*]`, `test_r02_pb47_declarado_y_luego_afirmado_bloquea`, `test_r02_h11_html[…<p>…</p><p>…]`; N02, N03 |
| H-03 | `test_r02_bloquea[h03_*]`, `test_r02_no_salta[h07_validacion_pendiente, h07_no_supero]`; N04 a N06 |
| H-04 | `test_r02_bloquea[h04_*]`, `test_r02_h04_una_parcial_ambigua_falla_cerrado`; N07 a N09 |
| H-05 | `test_r02_json` (11 formas), `test_r02_json_registro_dentro_de_una_opcion_lleva_su_opp`; N10 |
| H-06 | `test_r02_h06_v6_con_ml_clus_documentado_se_entrega`, `test_r02_h06_el_riesgo_sin_calculo_del_motor_no_cita_risk_dd`; N19, N20 |
| H-07 | `test_r02_no_salta` (negaciones y prosa financiera, 38 frases); N11 a N13, N21, N22 |
| H-08 | `test_r02_h08_una_declaracion_en_otra_celda_o_linea_vale` |
| H-09 | `test_r02_h09_el_extracto_no_lleva_otra_opcion`; N14 |
| H-10 | `test_r02_h10_coste_lineal` (tiempo de CPU; 4 veces más texto, menos de 6 veces más tiempo) y `r01_01::test_tiempo_lineal_…` |
| H-11 | `test_r02_bloquea[h11_*]`, `test_r02_h11_html`; N15 a N18 |
| H-12 | `test_r02_m01_…`, `m03`, `m09`, `m12`, `m13`, `m14`, `m15`, `m20` y `m32`; límites en INC-T165-01 |

### Gates y cuotas

Gates `refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (695) en verde. ruff **2813** (≤ 2813) y mypy A **109** (≤ 109).
Evidencias regeneradas con `--ejecutar`: «204 de 204 pruebas citadas superadas»; 31 Superada · 27 en parte; PB-47 «Superada»; `tests/test_fase4_mapa.py` 23 superadas.

## Ronda r03 (QA r02: H-13 a H-27), enfoque estructural

Copia `t165r03` (sobre `origin/develop` `c728c91` tras el rebase; base de comparación: la r02 con la QA r02, `a5a9a65`). Sin red
ni gasto (cliente simulado).

| Suite o script | r02 | r03 |
| --- | --- | --- |
| `tests/test_t165_g3_met13.py` | 162 (las reglas de la r02) | **110** superadas (reescrita: reglas A, B y C, ámbito, JSON, canonización, anotación, grafías, coste, HTML y extremo a extremo; las 115 de lectura de la r02 dejan de tener sentido) |
| `tests/test_t159_extremo_a_extremo.py` | 10 | 10 superadas (PB-30: la expresión del aviso admite «el control G3») |
| Bloque A completa | 7294 superadas | 7494 recogidas: **7490 superadas, 2 omitidas, 2 fallos** en 43 min, los dos de `tests/test_fase4_mapa.py` (el mapa citaba pruebas renombradas y el documento de evidencias iba por detrás). Corregido el mapa de PB-47 y regeneradas las evidencias: `test_fase4_mapa.py` **23 superadas**. Suite ≥ 607 |
| `revisores/r02_01` (71) | 36 madurez falsas: 35 pasaban | **0 escapes**: los 36 `test_escapa_*` y los 8 `test_control_bloquea` bloquean; la prueba de coste pasa. Fallan 15, todos por el **cambio de expectativa** de la r03: 9 `test_fp` (S1–S5 ya no bloquean, pasan; fallan D1–D7 y P1–P2: la raíz junto a una ficha), 2 `test_fp_pb47` (F1, F2: ficha no servida sin su forma canónica) y 4 `test_control_ok` («no validado», «sin validar», «la OPEP validó…») |
| `revisores/r02_02` (10 ciclos) | 5 escapes y 3 falsos positivos | **0 escapes** (N1, N2, N3, N4, J3 y PB-47 «otra cosa rechazada» bloquean); S1 «Hemos comprobado con…» y la lectura del conjunto ya no retiran ni bloquean; falla 1, D2 «ninguna ficha del Catálogo está validada» (cambio de expectativa) |
| `revisores/r01_01` (105) | 0 fallos | 62 pasan; **1 escape**: E04 «VOL-GARCH-001 es un método verificado y probado» (sinónimos, H-18: límite declarado). Los otros 42 fallos son cambios de expectativa: 19 `test_fp` (prosa con la raíz y declaraciones «pendiente de ser validado»), 7 `test_control_ok`, 12 ejemplos de `estado_madurez_metodos` de los prompts (en texto libre llevan «no validado»; en JSON no son la forma canónica; en el flujo real los reescribe el ejecutor), 3 de PB-47 declarado en prosa o en una tabla y el de la frase larga (36 KB de «no está validado,»: ahora bloquea, en milisegundos) |
| `revisores/r01_02` (14 ciclos) | 13 | 7 pasan. Fallan: `guion_no_separable` (el ValueError del propio script, como en la r02), 2 de prosa financiera (retira o bloquea: cambio de expectativa) y 4 de `estado_madurez_metodos` sembrado (control y tres formas): **no se retiran porque el ejecutor reescribe el campo** y lo que dijo el modelo no llega a ningún sitio (decisión «se ignora», INC-T165-01) |
| `revisores/r01_03` (10 ciclos, 20 G3V-) | G3-MET-13 OK | G3-MET-13 OK en los 20 y **dictámenes iguales**. Entregables: cambian solo por la forma canónica (abajo); el visual, **idéntico** (no cita fichas) |
| `r02_mutantes.py` corregido (H-24), sobre la r02 (`git archive a5a9a65`) | se paraba en N13 | **31 de 31 muertos** en una sola pasada (N13 y N17 también) |
| `r03_mutantes.py` (23), sobre la r03 (`git archive`) | — | primera pasada: 21 muertos, vivos R12 (grafías «_» y «.»: solo las cubría la búsqueda con espacios) y R17 (canonización: solo se probaba la función); pruebas añadidas (`ml_super_001`, `ML.SUPER.001`; el campo del prompt sembrado de extremo a extremo) y **R12 y R17 mueren**: 0 vivos |
| `revisores/r02_03_mutantes.py` (9) | 2 vivos (X05, X07) | 8 no aplican (sus expresiones no existen en la r03); **X07 muere** (`test_el_tecnico_es_un_ambito_y_la_ruta_es_la_linea_del_parrafo`); 0 vivos |

### Cambios en los entregables del ciclo normal (`diff` r02 → r03, 10 ciclos, ruta de trabajo normalizada)

Recuento de líneas distintas, con los números y los OPP- normalizados (todo lo demás, idéntico; el visual, idéntico):

```
198 < **Valoración.** Precio en el percentil N de sus últimos tres años (ST-DESC-N).
198 > **Valoración.** Precio en el percentil N de sus últimos tres años (ST-DESC-N [madurez: IMPLEMENTADO]).
198 < **Riesgos.** … riesgo sintético **N/N** (RISK-DD-N).
198 > **Riesgos.** … riesgo sintético **N/N** (RISK-DD-N [madurez: IMPLEMENTADO]).
198 <      "valoracion": "Precio en el percentil N de sus últimos tres años (ST-DESC-N).",
198 >      "valoracion": "Precio en el percentil N de sus últimos tres años (ST-DESC-N [madurez: IMPLEMENTADO]).",
 10 < **Apuestas independientes: N** (N efectivo ML-CLUS-N: N).
 10 > **Apuestas independientes: N** (N efectivo ML-CLUS-N [madurez: IMPLEMENTADO]: N).
 10 > - Madurez de los métodos citados (R22; la escribe el ejecutor desde el Catálogo): ML-CLUS-001 [madurez: IMPLEMENTADO]; RISK-DD-001 [madurez: IMPLEMENTADO]; ST-DESC-001 [madurez: IMPLEMENTADO].
 10 >  "x_madurez_metodos": { "ST-DESC-001": "IMPLEMENTADO" }      (y la coma de «estado_g3» que lo precede)
```

### Falsos positivos medidos (`r03_bancos_frases.py`, Catálogo real)

| Banco | Legítimas que bloquean | Falsas que pasan |
| --- | --- | --- |
| Banco 3 sin la raíz «valid-» (nuevo, sin ajustar) | **0 de 30** | 0 de 15 |
| Banco 3 con la raíz en otro sentido (nuevo, sin ajustar) | 15 de 15 (por construcción) | — |
| Bancos 1 y 2 de la r02 (implementador) | 19 de 35, todas con la raíz | 4 de 25 (sinónimos) |
| `r01_01` del revisor (prosa, controles y ejemplos de los prompts) | 30 de 39, todas con la raíz | 1 de 36 (sinónimos) |
| `r02_01` del revisor | 13 de 18, todas con la raíz | 0 de 33 |

Ninguna frase legítima sin la raíz bloquea en ningún banco. El coste del falso positivo es la opción (F6 la retira) o el run (fuera
de una opción). En los ciclos simulados normales la raíz no aparece (solo «invalidación», que no cuenta).

### Hallazgo → prueba

| Hallazgo | Pruebas del ticket (`tests/test_t165_g3_met13.py`) | Mutantes |
| --- | --- | --- |
| H-13, H-14, H-15, H-26 | `test_en_el_mismo_texto_la_palabra_cuenta_en_todo_el` | R01 |
| H-16 | `test_bloquea[ML-CLUS-001: documentado, no se sirve]`, `test_pb47_corregida_la_declaracion_con_la_forma_canonica_la_entrega_pasa` | R07 |
| H-17, H-23 | `test_h17_otro_campo_de_la_misma_opcion…`, `test_en_el_mismo_texto…` (título, tabla transpuesta, dos párrafos), `test_html` | R04 |
| H-18 | `test_no_salta[Hemos comprobado…, Riesgo verificado…]` | — |
| H-19 | `test_anotar_madurez`, `test_el_ciclo_simulado_normal_sigue_apto_y_lleva_la_madurez_canonica` (declaración R22 canónica) | R18–R20 |
| H-20 | `test_json_bloquea` (16 formas), `test_json_canonico_no_salta`, `test_canonizar_madurez…`, `test_el_campo_de_madurez_que_pide_el_prompt…` | R10, R11, R17 |
| H-21 | `test_una_ficha_con_otra_grafia_se_reconoce`, `test_una_ficha_desconocida…`, `test_lo_que_no_es_una_ficha` | R12, R13 |
| H-22 | `test_coste_lineal_en_una_frase_larga_y_en_muchas_fichas_por_parrafo` (CPU; 2000 → 8000: menos de ×6) | R14 |
| H-24 | `r02_mutantes.py` ejecutado entero | — |
| H-25 | `git ls-files .venv` vacío; `git check-ignore -v .venv` → `.gitignore:10:.venv` | — |
| H-27 | X05 no aplica; X07: `test_el_tecnico_es_un_ambito_y_la_ruta_es_la_linea_del_parrafo` | `r02_03` X07 |
| Lectura antes de anotar | `test_una_ficha_no_servida_que_el_modelo_pone_en_el_tecnico_se_lee_antes_de_anotar` | R21 |
| Literales del ejecutor | `test_la_limitacion_sin_historia…`, `test_los_textos_del_ejecutor_no_dicen_validacion`, `test_el_riesgo_sin_calculo_del_motor_no_cita_risk_dd` | R22, R23 |

CA-1 a CA-8 siguen cubiertos por las mismas pruebas de extremo a extremo (CA-2 con la declaración en forma canónica; CA-4 con las
reglas de la r03).

### Gates y cuotas

`refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (695) en verde; el corpus no se toca. ruff **2813** (≤ 2813) y mypy A **109** (≤ 109). Evidencias regeneradas con `--ejecutar`: «204 de 204 pruebas citadas superadas»; 31 Superada · 27 en parte; PB-47 «Superada». No se ha ejecutado `./tools/check_all.sh` entero (sin push; lo hace el commit a `develop`).

### Comandos

Los de `analisis-tecnico.md`, ronda r03, y:

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider .     # suite completa de A
cd ../.. && git archive a5a9a65 bloque_a | tar -x -C <copia_r02> && .venv/bin/python .docs/tickets/T-165/r02_mutantes.py --copia <copia_r02>
.venv/bin/python .docs/tickets/T-165/revisores/r02_03_mutantes.py --copia <copia_r03>
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
```

## Ronda r04 (QA r03: H-28 a H-32)

Copia `t165r03`, con la QA r03 traída de `c6a2867`. Tras la pausa del operador, rebasada sobre `origin/develop` `b9c71d2` (T-143 y
T-167) sin conflictos; la suite completa se ejecutó después del rebase. Sin red ni gasto.

| Suite o script | r03 | r04 |
| --- | --- | --- |
| `tests/test_t165_g3_met13.py` | 110 | **126** superadas (16 de la r04) |
| `tests/test_t159_extremo_a_extremo.py` y `revisores/r03_02` | 10 y 44 | 164 superadas con la de T-165 (`r03_02`: **0 fallos**, también V1a–V1c y M1–M3) |
| Bloque A completa | 7490 | Una ejecución tras el rebase (la anterior la cortó el reinicio del contenedor): 7602 recogidas, **7578 superadas, 2 omitidas y 22 fallos** en 40 min, todos de `test_t145.py` (4) y `test_t148.py` (18): el estimador de coste (`.docs/scripts/estimar_coste_ciclo_a.py`) no preveía la reescritura R22 de AG-02 y AG-17 (S3: «el ciclo medido llama más veces de las previstas a AG-02»). Añadidas a `LLAMADAS_DEL_CICLO` (con la clave `redaccion.reescrituras_r22`) y corregidos los recuentos de las dos pruebas (7 + 9 llamadas del ciclo): `test_t145.py` + `test_t148.py` **64 superadas**. Suite ≥ 607 |
| `revisores/r03_03` (9) | 5 fp, 1 escape, H-29 y H-31 fallaban | **4 pasan**: `test_escapa[raiz_con_tilde]` (H-30), `test_fp_ruta_de_salida_con_la_raiz` (H-29), `test_esquema_nombre_llano…` (H-31) y el límite de sinónimos. Fallan 5 por construcción: `test_fp_lectura_del_conjunto` (2) y `test_fp_sintetizador_v6…` siembran la raíz también en la reescritura, que persiste y bloquea (lo pedido: «se bloquea solo si persiste»); `test_fp_informe_de_clase` (2) siembran la raíz dentro de una opción, que se retira (sin reescritura dentro de una opción, decisión de la ronda). Las versiones del ticket que siembran como el simulado (solo en la primera respuesta) entregan |
| `revisores/r03_01` (corpus) | Fondos se retiraría (1 de 12); el paquete V5.0, OK | Igual: lo de dentro de una opción no cambia. Las líneas de los prompts que piden la raíz las cubren ahora la regla R22 de las instrucciones y la reescritura |
| Ciclos normales `r01_03` (10) | G3-MET-13 OK | G3-MET-13 OK, **dictámenes iguales**. Diferencias con la r03 (abajo): solo la limitación R22 reescrita en los 8 ciclos V5 y el consumo |
| Cadena A→B (`cadena_a_b.py`) | rc 0 | **rc 0**: 1 entrega válida del Bloque B y 1 vuelta registrada (antes del rebase; T-143 y T-167 no tocan el código) |
| `r03_mutantes.py` (35: R01–R23 de la r03, con las expresiones nuevas, y R24–R35 de la r04) | 23 muertos | **35 de 35 muertos** |
| `revisores/r02_03_mutantes.py` | X07 muerto, 8 no aplican | igual: 0 vivos |

### Diferencias de los entregables (r03 → r04, 10 ciclos, ruta de trabajo normalizada)

```
 10 < Consumo del RUN (hasta la redacción): N llamadas, N UC (LLM N, Motor N); tokens …
 10 > Consumo del RUN (hasta la redacción): N llamadas, N UC (LLM N, Motor N); tokens …     (V5: una llamada más, la reescritura)
  8 > - Métodos usados (RN): su madurez la escribe el ejecutor junto a cada ficha.             (técnico, V5)
  8 >   "Métodos usados (RN): su madurez la escribe el ejecutor junto a cada ficha.",           (JSON, V5)
```

Ejemplo (`v5_12tipos_2026_0`): «70 llamadas, 56.3518 UC» → «71 llamadas, 57.1169 UC». El visual no cambia.

### Hallazgo → prueba (`tests/test_t165_g3_met13.py`) y mutante

| Hallazgo | Prueba | Mutantes |
| --- | --- | --- |
| H-28 regla en las instrucciones | `test_h28_la_regla_r22_va_en_las_instrucciones_de_los_que_redactan` | R24, R27 |
| H-28 reescritura de la integración (el simulado escribe la R22 del prompt) | `test_h28_la_declaracion_r22_del_analizador_se_reescribe_y_el_ciclo_entrega` (y RC del Motor sin la raíz) | R25, R34 |
| H-28 si persiste | `test_h28_si_la_raiz_persiste_tras_la_reescritura_el_run_se_bloquea` (una sola reescritura) | — |
| H-28 Redactor V5 y Sintetizador V6 | `test_h28_el_redactor_y_el_sintetizador_se_reescriben[v5, v6]` | R26 |
| H-28 lagunas | `test_h28_una_laguna_del_analista_con_la_raiz_no_se_transcribe_al_paquete` | R32 |
| H-28 «semanas válidas» | `test_la_limitacion_sin_historia…` (la limitación entera, con la tilde de H-30 bloquearía) | R35 |
| H-29 | `test_h29_una_carpeta_de_salida_con_la_raiz_no_bloquea` | R28 |
| H-30, H-32 | `test_h30_h32_la_tilde_y_los_sustantivos_que_faltaban`, `test_h30_inválido_no_es_la_raiz` | R30, R31 |
| H-31 | `test_h31_un_campo_con_maxlength_no_se_anota_y_el_esquema_sigue_valido` | R29 |
| Sugerencia: lo descartado en HA | `test_lo_que_el_modelo_dijo_de_la_madurez_queda_en_ha` | R33 |

### Gates y cuotas

`refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (**696**, el de T-143) en verde; `por_defecto.yaml` parsea. ruff **2813** (≤ 2813) y mypy A **109** (≤ 109). Evidencias regeneradas con `--ejecutar` tras el rebase: «204 de 204 pruebas citadas superadas»; 31 Superada · 27 en parte; PB-47 «Superada». No se ha ejecutado `./tools/check_all.sh` entero.

### Comandos

Los de la r03 y de `analisis-tecnico.md`, ronda r04.

## Ronda r05 (QA r04: H-33 a H-37)

QA r04 traída de `003a062`. Rebasada al final sobre `origin/develop` `d72526c` (T-162 y T-169): el único conflicto, el documento
de evidencias, se resolvió con el de develop y se regeneró. Sin red ni gasto.

| Suite o script | r04 | r05 |
| --- | --- | --- |
| `tests/test_t165_g3_met13.py` | 126 | **139** superadas (13 de la r05) |
| T-145, T-148, T-113, T-159 y T-165 juntas | — | 315 superadas antes de las dos últimas pruebas; tras ellas, 139 de T-165 y 64 de T-145 + T-148 |
| Bloque A completa (una vez, tras el rebase) | 7578 + 22 corregidos | 7678 recogidas: **7675 superadas, 2 omitidas y 1 fallo** en 42 min: `test_fase4_mapa::test_h05` (el documento de evidencias, que tras el conflicto del rebase iba por detrás). Regeneradas las evidencias: `test_fase4_mapa.py` **23 superadas** |
| `revisores/r04_01` (12) | 4 fallaban (H-33 a H-36) | **10 pasan**. Fallan 2, por expectativa: `test_limite_fondos_ejemplo_del_corpus_retira_la_opcion` (con H-34 ya no se retira, como anticipaba el revisor) y `test_reescritura_sigue_la_configuracion[2]` (siembra la raíz también en la respuesta reescrita y espera que persista; desde la r05 el simulado obedece la reescritura; la misma comprobación con un modelo que no obedece, `test_la_reescritura_sigue_la_configuracion_con_un_modelo_que_no_obedece[0, 2]`, pasa) |
| `revisores/r03_03` (9) | 5 fallaban por construcción | **9 pasan** (Fondos, catalizador, R22 del Analizador, PS5 y Sintetizador V6, con el simulado que obedece) |
| Ciclos normales `r01_03` (10), salida nueva `ciclos_r05_impl` | G3-MET-13 OK | G3-MET-13 OK y dictámenes iguales; frente a la r04 solo cambia el consumo (instrucciones más largas) |
| Cadena A→B | rc 0 | **rc 0**: 1 entrega válida y 1 vuelta |
| `r03_mutantes.py` (43: R01–R35 y R36–R43 de la r05) | 35 de 35 | 42 de 43 en la primera pasada; vivo R40 (la bolsa de la reescritura); con `test_h34_…paga_de_la_bolsa_del_tipo`, **muere: 43 de 43** |
| `revisores/r02_03_mutantes.py` | 0 vivos | 0 vivos (X07 muere) |

### Hallazgo → prueba (`tests/test_t165_g3_met13.py`) y mutante

| Hallazgo | Prueba | Mutantes |
| --- | --- | --- |
| H-33 | `test_h33_todas_las_instrucciones_cuyo_texto_llega_al_paquete_llevan_la_regla[v5, v6]`, `test_h33_la_objecion_del_contradictor_con_la_raiz_se_reescribe_y_no_retira_la_opcion` | R36–R38 |
| H-34 | `test_h34_el_ejemplo_de_fondos_del_corpus_se_reescribe_y_no_retira_opciones`, `test_h34_si_la_raiz_persiste_en_el_informe_de_clase_la_opcion_se_retira`, `test_h34_…paga_de_la_bolsa_del_tipo`; `test_t145`/`test_t148` (9 llamadas por tipo) | R39, R40 |
| H-35 | `test_h35_una_laguna_del_analista_con_la_raiz_llega_con_la_palabra_cambiada`, `test_h35_la_carencia_llega_al_broker[…]` | R41, R32 |
| H-36, H-37 | `test_h36_h37_la_reescritura_repite_la_instruccion_y_lleva_las_frases`, `test_h37_frases_con_raiz_tiene_tope` | R42, R43 |
| El simulado obedece | `test_el_simulado_obedece_la_reescritura`, `test_la_reescritura_sigue_la_configuracion_con_un_modelo_que_no_obedece[0, 2]` | — |

### Gates y cuotas

`refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (696) en verde. ruff **2813** (≤ 2813) y mypy A **109** (≤ 109). Evidencias regeneradas con `--ejecutar` tras el rebase: «211 de 211 pruebas citadas superadas» (develop sumó las de T-162 y T-169); 32 Superada · 26 en parte; PB-47 «Superada». No se ha ejecutado `./tools/check_all.sh` entero.

## Ronda r06 (QA r05: H-38 a H-40)

QA r05 traída de `7fb1fb2`. Rebasada sobre `origin/develop` `a9210c0` (T-161 y T-164); el único conflicto, el documento de
evidencias, se resolvió con el de develop y se regeneró. Sin red ni gasto.

| Suite o script | r05 | r06 |
| --- | --- | --- |
| `tests/test_t165_g3_met13.py` | 139 | **145** superadas (6 de la r06) |
| T-165, T-159, T-145, T-148 y T-113 juntas (antes del rebase) | — | **325 superadas** |
| Bloque A completa (una vez, tras el rebase; la primera la cortó la pausa del operador) | 7675 | 7896 recogidas: **7893 superadas, 2 omitidas y 1 fallo** en 44 min: `test_fase4_mapa::test_h05` (el documento de evidencias, por detrás tras el conflicto del rebase). Regeneradas las evidencias: `test_fase4_mapa.py` **23 superadas** |
| `revisores/r05_01` (6) | 3 fallaban | **6 pasan** |
| `revisores/r04_01` (12) | 10 | 10 pasan; los mismos 2 por expectativa de la r05 (Fondos ya no se retira; `sigue_la_configuracion[2]` siembra también la respuesta reescrita y el simulado la obedece) |
| `revisores/r03_03` (9) | 9 | **9 pasan** |
| Ciclos normales `r01_03` (10), salida nueva `ciclos_r06_impl` | OK | G3-MET-13 OK y dictámenes iguales; frente a la r05 solo cambia el consumo (la frase nueva de la regla: p. ej. 57,17 → 57,29 UC, las mismas 71 llamadas) |
| Cadena A→B | rc 0 | **rc 0**: 1 entrega válida y 1 vuelta |
| `r03_mutantes.py` (46) | 43 de 43 | **46 de 46 muertos** |
| `revisores/r02_03_mutantes.py` | 0 vivos | 0 vivos |

### Hallazgo → prueba y mutante

| Hallazgo | Prueba (`tests/test_t165_g3_met13.py`) | Mutantes |
| --- | --- | --- |
| H-40 | `test_h40_con_la_raiz_en_la_primera_respuesta_de_cada_agente_que_redacta_el_ciclo_entrega_sin_perder_opciones[v5, v6]` (siembra la raíz en cada texto libre de la primera respuesta de todo agente fuera de la exclusión; un solo G3V- de F6, sin retiradas, G3-MET-13 OK; cada agente sembrado se reescribe), `test_h40_todo_agente_que_no_esta_en_la_exclusion_pasa_por_la_reescritura` (también «AG-99»; la clase de la propia llamada), `test_h40_no_quedan_llamadas_sueltas_a_reescribir_r22` | R25, R26, R38, R39, R40, R42 |
| H-38 | `test_h38_los_campos_de_madurez_no_disparan_la_reescritura`; `test_lo_que_el_modelo_dijo_de_la_madurez_queda_en_ha` con el simulado obediente | R44 |
| H-39 | la INC con `frases_r22` en la prueba de H-40; `test_h39_la_regla_tambien_pide_no_calificar_la_fiabilidad` | R45, R46 |
| Estimador | `test_t145`/`test_t148` (filas derivadas de la exclusión) | — |

### Gates y cuotas

`refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (696) en verde. ruff **2813** (≤ 2813) y mypy A **109** (≤ 109). Evidencias regeneradas con `--ejecutar` tras el rebase: «211 de 211 pruebas citadas superadas»; 32 Superada · 26 en parte; PB-47 «Superada». No se ha ejecutado `./tools/check_all.sh` entero.

## Ronda de cierre de la QA r06

| Prueba | Resultado |
| --- | --- |
| `test_cierre_r06_la_reescritura_que_no_cabe_en_la_bolsa_no_se_pide[1.5-False, 50.0-True]` (bolsa justa para la primera llamada, 1,5 UC, y no para la reescritura; y bolsa de sobra) | pasan: sin reescritura ni cierre parcial y con la INC «sin reescribir… decide G3-MET-13»; con bolsa, se reescribe. Sin la corrección (mutante R47) falla el primer caso |
| `test_t165_g3_met13.py` + `test_t145.py` + `test_t148.py` | **211 superadas** (147 de T-165) |
| `revisores/r06_01` (9) y `revisores/r05_01` (6) | **9 y 6 pasan** |
| Ciclos normales (10), salida nueva `ciclos_r07_impl` | G3-MET-13 OK, dictámenes iguales y entregables **idénticos** a los de la r06 |
| `r03_mutantes.py` (47, con R47) | **47 de 47 muertos** |
| Cuotas | ruff **2813** (≤ 2813) y mypy A **109** (≤ 109) |
