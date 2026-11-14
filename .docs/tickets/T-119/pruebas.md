# T-119 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t119_p2.py` (nuevo) | — | 1171 |
| `tests/test_t119_motor.py` (nuevo) | — | 130 |
| Suite completa de A (`pytest -q bloque_a/11_Ejecutor`) | 3693 | **4994** en verde (14 min 46 s) |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `test_t119_p2.py::test_casos_de_control` y `test_cada_caso_de_control_puede_fallar`; `test_t119_motor.py::test_los_casos_de_control_de_las_diez_se_superan_y_quedan_en_rc`; `promover_fichas_catalogo.py` | 33 casos de control en 10 fichas, todos superados y registrados en RC; cada uno falla con las cifras movidas una millonésima |
| CA-2 | `test_t119_motor.py::test_cada_caso_de_control_se_sirve_por_ct09_queda_en_rc_y_se_reejecuta_por_ct10`, `test_ct10_detecta_…`, `test_ya_no_queda_ninguna_ficha_documentada`, `test_una_ficha_p2_degradada_en_el_catalogo_deja_de_servirse`; `test_t106_motor.py::test_el_motor_sirve_exactamente_lo_que_el_catalogo_da_por_implementado` | Sí: 80 manejadores, los 80 servibles, y AUD-REX-001 por CT-10; los 33 casos se re-ejecutan con coincidencia `SI` |
| CA-3 | `test_t119_p2.py`: `test_*_rechazos` de cada ficha, `test_dominio_de_cada_parametro` (y `test_todos_los_parametros_tienen_prueba_de_dominio`), `test_cota_superior_de_cada_parametro_de_tamano`, `test_cota_superior_de_cada_lista_de_datos`, `test_ningun_umbral_se_cambia_desde_la_peticion`, `test_un_parametro_no_declarado_se_rechaza`, `test_una_serie_de_ht01_no_se_ignora_en_silencio` | Sí |
| CA-4 | `test_t119_p2.py`: hojas hostiles, bloques ausentes, magnitud, fecha de corte por ficha y por bloque; `test_t119_motor.py`: `test_ninguna_excepcion_escapa_del_servicio_y_nada_no_finito_se_sirve`, `test_un_manejador_que_falla_o_da_no_finitos_es_un_rechazo`, `test_un_dato_posterior_a_la_fecha_de_corte_…`, `test_umbrales_parametros_no_declarados_y_semillas`, `test_mismo_resultado_en_dos_procesos` | Sí |
| CA-5 | Oráculos de `test_t119_p2.py` (ver abajo); `.docs/tickets/T-119/revisores/impl_p2_mutantes.py` | 124 mutantes, ninguno vivo |
| CA-6 | `promover_fichas_catalogo.py --aplicar --etiqueta "ejecutor, casos de control registrados (T-119)"` con las diez fichas; `tools/corpus_integridad.py --update` | 10 promovidas, ninguna sin superar; §1.3 con 81 IMPLEMENTADO y ninguna en DOCUMENTADO; el diff del Catálogo solo toca la madurez (10 filas del §4, 10 líneas de ficha y el §1.3); corpus re-congelado (695 archivos) |
| CA-7 | Ver «Gate» | Sí |

## Oráculos independientes

| Ficha | Otra vía |
| --- | --- |
| FIR-CRED-001 | Sistema de Merton en dos dimensiones con `scipy.optimize.fsolve` y `scipy.stats.norm`; diferencial como rendimiento de la deuda (V − E) menos r; T = 0,5, 1 y 3 |
| FX-BEER-001 | Diseño DOLS fila a fila, covarianza de Newey-West con bucles e IC; ADF de los residuos recalculado con su rezago por AIC; valores críticos publicados |
| CMD-REAL-001 | pandas, `scipy.stats.percentileofscore` y `theilslopes`; cuantil de costes expandiendo cada tramo en unidades de producción |
| REI-LEV-001 | pandas, con nueve componentes |
| CHR-ONCHAIN-001 | pandas (`rolling`, `std`) con medias de 1, 90 y 365 días |
| CHR-TOKEN-001 | Fracciones exactas (`fractions.Fraction`) |
| PRV-PME-001 y PRV-CF-001 | TIR por el método de la secante y, con flujos anuales, como raíz de un polinomio (`numpy.roots`); Takahashi-Alexander con otra recurrencia |
| ALT-HF-001 | MCO por ecuaciones normales, Newey-West con bucles y R², con y sin desuavizado; ACC-FACT-001 con los mismos datos |
| ALT-AUC-001 | Ventas repetidas por efectos fijos de pieza y de año; hedónico por ecuaciones normales |

## Mutantes

`.docs/tickets/T-119/revisores/impl_p2_mutantes.py`, en una copia desechable (`…/scratchpad/p2_mut`): 124 mutantes de fórmulas, cotas y reglas de rechazo.

- Primera pasada (119): vivo uno, N20 (la cota de componentes, 500 → 501): la prueba de la cota leía el umbral del propio módulo. Corrección: `test_las_cotas_de_tamano_salen_de_las_incidencias` fija cada cota con su número.
- Segunda pasada (124, con cinco más sobre lo corregido): **ninguno vivo**. De los 83 con casos de control, 74 mueren ya ante ellos y 9 solo ante las pruebas (el IC, el HAC, los adelantos del DOLS y el valor crítico de FX-BEER-001; el borde del percentil de costes; la referencia ingenua de ALT-HF-001; y el orden y los pares del mismo año de ALT-AUC-001). Los 41 de reglas y cotas mueren ante las pruebas.

## Regresiones adaptadas

Tres pruebas anteriores daban por hecho que quedaba una ficha DOCUMENTADO, o que `ESTRICTAS` solo tenía las dos fases:
- `test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion` y `test_t65_resto_t53.py::test_cs08_no_se_ofrece_como_alternativa_una_ficha_que_no_se_sirve` usaban CHR-ONCHAIN-001 como ficha no servible. Ahora la ponen a mano en `DOCUMENTADAS_CON_CODIGO` y comprueban la misma regla (`METODO_NO_IMPLEMENTADO` y alternativa solo si se sirve).
- `test_t112_motor.py::test_son_las_35_fichas_de_la_fase_2_y_estan_en_el_catalogo` compara `ESTRICTAS` con `FASE1 | FASE2 | P2`.

Ninguna prueba se ha quitado.

## Gate

Comprobaciones pedidas, desde la raíz de la copia de trabajo (el gate completo `./tools/check_all.sh` no se ha lanzado: la máquina es compartida; lo pasa quien integre):

| Comprobación | Resultado |
| --- | --- |
| `pytest -q` de `test_t119_p2.py`, `test_t119_motor.py`, `test_fase2_*.py`, `test_t112_motor.py`, `test_t106_*.py`, `test_t87_contratos.py`, `test_t65_resto_t53.py` y `test_unitarias.py` | 3586 en verde (4 min 42 s) |
| Suite completa de A | 4994 en verde |
| `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | 2902 (cuota 2902); los ficheros nuevos, sin incidencias |
| `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | 109 (cuota 109); `fichas_p2.py`, sin incidencias |
| `tools/corpus_integridad.py` | Íntegro, 695 archivos |
| `tools/refs_vivas.py` · `tools/secrets_scan.py` · `tools/nfc_check.py` | En verde los tres |

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_t119_p2.py tests/test_t119_motor.py
cd ../..
.venv/bin/pytest -q bloque_a/11_Ejecutor
.venv/bin/python -I -B .docs/tickets/T-119/revisores/impl_p2_mutantes.py <carpeta desechable>
```

## Ronda r02 (QA r01: NO APTO)

| Suite | Antes (r01) | Después (r02) |
| --- | --- | --- |
| `tests/test_t119_p2.py` | 1171 | 1191 (pruebas `test_r02_h02_*`, que matan los mutantes de H-02) |
| `tests/test_t119_motor.py` | 130 | 130 |
| `tests/test_t119_r02.py` (nuevo) | — | 21 |
| Suite completa de A | 5258 (QA r01, con T-118 integrado) | **5497** en verde, con T-121 (21 min 34 s) |

### Hallazgo → prueba → script del revisor (sin modificar)

| Hallazgo | Prueba | Script: antes → después |
| --- | --- | --- |
| H-01 | `test_t119_r02.py::test_h01_*` (mínimos fijos; REI-LEV con 1 y 2 componentes; una petición por emisor; clones con 10, 3 y 2 componentes; un solo clon entre distintos; el clon de FIR-CRED por los datos del modelo; un token solo con `ambito_es_red`; REI-NAV con uno; los casos de control de las cuatro, superados) | `r01_08_frontera_b.py`: 11/15 → el script original se detiene en la línea 83 con `KeyError: 'limitaciones'`: imprime `r['limitaciones']` de la respuesta de CHR-TOKEN-001 con un token, que ahora es un RECHAZO y no lleva ese campo. Con una copia que solo cambia ese acceso por `r.get('limitaciones')` (en la impresión y en la comprobación; ninguna otra línea): **14/14** (REI-LEV con un componente y con una petición por emisor, RECHAZADO; FIR-CRED con 10 copias, RECHAZADO; CHR-TOKEN con un token de sector, RECHAZADO). El bloque 3 (dispersión con dos componentes) ya no tiene nada que comprobar: con dos, REI-LEV rechaza |
| H-02 | `test_t119_p2.py::test_r02_h02_*` | `r01_09_mutantes.py`: 62 muertos y 12 vivos (8 no equivalentes) → **71 muertos y 4 vivos** (Q50, Q53, Q60 y Q73, los que el revisor dio por equivalentes o redundantes); Q83 ya se aplica y muere; Q28 sigue sin aplicarse (su texto no está en el módulo). Los 8 del hallazgo, muertos |
| H-03 | `test_h03_dos_tir_no_es_sin_tir`, `test_h03_la_rejilla_es_un_umbral_fijo` | `r01_03_oraculos_b.py`: 102/103 → **103/103** |
| H-04 | — (documentación) | INC-T119-01, «Ronda r02» |
| H-05, H-09 | `test_h05_h09_lo_que_no_se_calcula_se_declara_en_la_entrega` | `r01_03` (LN-PME) y `r01_02_oraculos_a.py`: 280/280 → **280/280** |
| H-06 | `test_h06_la_cache_no_entrega_…`, `test_h06_la_firma_distingue_…` | `r01_04_hostiles.py`: 474 «tipo raro servido», entre ellos el `Decimal` servido desde la caché → **97**, ninguno desde la caché (los que quedan son campos que la ficha no usa con esos parámetros y opcionales con None, como en la r01) |
| H-07 | `test_t121_hallazgos.py::test_h02_argumentos_de_la_llamada_que_no_son_texto` (solicitante de 3 000 niveles, circular, sustituto Unicode, lista) | `r01_04_hostiles.py`: 70 excepciones escapadas (60 del proveedor de pruebas del script, que no tiene `cierres`, y 10 `RecursionError` con el solicitante anidado) → **60**, todas del proveedor del script (`AttributeError: 'Proveedor' object has no attribute 'cierres'`), ninguna de `servicio.py` ni de las fichas. Resultado del script: 4/5 (la que falla es esa, la misma que el revisor descartó en la r01); 35 659 llamadas, una entrada en RC por llamada, nada no finito, la más lenta 0,4 s |
| H-08 | `test_h08_un_cambio_de_configuracion_en_caliente_no_sale_de_la_cache` | `r01_06_corte_cotas_config.py`: 113/114 → **114/114** |

Otros scripts de la r01, de nuevo: `r01_01_casos_ct09_ct10.py` **37/37** (los 33 casos servidos, CT-10 = SI, misma huella en dos procesos); `r01_05_catalogo.py --desechable <carpeta>` **29/29** (el Catálogo se reproduce byte a byte); `r01_07_merton_barrido.py` **3/3** (1 657 de 1 800 combinaciones servidas, como en la r01).

### Mutantes de las correcciones de la r02

`.docs/tickets/T-119/revisores/impl_r02_mutantes.py bloque_a/11_Ejecutor <carpeta desechable>`: 13 mutantes (sin rechazo de clones en las tres fichas; sin mínimo o con mínimo 2 en REI-LEV; un token de sector; el clon distinguido por el id; REI-NAV con uno; la TIR con dos soluciones; las dos advertencias; la caché sin firma de tipos y sin configuración) frente a `test_t119_r02.py`, `test_t119_p2.py` y `test_t119_motor.py`: **13 muertos, ninguno vivo**.

### Gate

El mismo que el de T-121 (misma rama y mismo árbol): ver `.docs/tickets/T-121/pruebas.md`, «Gate». ruff 2902 (cuota 2902), mypy 109 (cuota 109), corpus íntegro (695), refs, secretos y NFC en verde, goldens de contratos sin cambios.
