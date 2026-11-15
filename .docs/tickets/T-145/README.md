# T-145 · Bloque A: hallazgos de la QA r01 de T-140 (cota de coste de un ciclo real, filas de tabla con fecha delante, falsos negativos de tarjetas, comprobación de datos, borrador, mutantes)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/contratos.py`, `tests/test_t145.py`, `tests/test_t140.py`); `.docs/scripts/estimar_coste_ciclo_a.py`, `comprobar_datos_a.py`, `borrador_anexo_b.py`; `.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`; `docs/incidencias.md` (INC-T123-01, INC-T129-01, INC-T114-01) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; las decisiones nuevas van como `[PROPUESTO]` |
| Deuda técnica | T-145 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Corregir los hallazgos de la QA r01 de T-140 (`.docs/tickets/T-140/qa.md`): que la cota del coste de un ciclo sea una cota antes de pedir al operador que autorice gasto con ella (H-01), que R8 no marque filas de tabla con una fecha delante (H-02) y los cuatro bajos.

## Alcance

- Entra: H-01 a H-06 de la QA r01 de T-140.
- No entra: cambiar cómo el presupuesto en UC decide si llama (el hallazgo nuevo de H-01 se documenta, no se corrige); la V6 (la cota falla cerrado con `diseno: v6`); la deuda técnica; la cadena A→B (otra sesión).

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| H-01 (media): la «cota superior» solo acotaba las llamadas del ciclo simulado | `cota_ciclo`: la menor de dos cotas con supuestos declarados (S1–S5). **Por llamadas:** las que el código de un C1 de la V5 puede hacer como mucho (`LLAMADAS_POR_TIPO`: cribado, petición de conocimiento, prospectiva, refutación, respuesta, contrarréplica y curación; `LLAMADAS_DEL_CICLO`: aprendizaje, integración, dos dictámenes G3, redacción y reescritura, auditoría), cada una en su peor caso petición a petición y con la salida máxima de las llamadas que puede leer en su encargo. **Por presupuesto:** el presupuesto del ciclo con la ampliación máxima al peor precio por UC, más lo que el presupuesto deja pasar (la última llamada de cada bolsa, la caché cargada como lectura, AG-18/19/20 y las búsquedas). La cifra de T-140 queda como «peor caso de las llamadas medidas» y la salida dice que no es una cota |
| H-01 (hallazgo nuevo): el presupuesto no corta antes de la llamada | Documentado en el análisis y en INC-T129-01; la cota por presupuesto lo cuenta. No se cambia el ejecutor |
| H-02 (media): filas «año o fecha MMDD + cuatro niveles» marcadas (5–8 %) | En cinco o más grupos de cuatro cifras, la serie entera se reparte en tarjetas, cada una seguida, si acaso, de su caducidad MMAA; lo que sobra solo va detrás y un año ya no es fecha (`_forma_de_caducidad`, `_tarjetas_de_la_serie`) |
| H-03 (baja): falsos negativos | Se detectan «tarjeta, caducidad y otra tarjeta» y «dos tarjetas cada una con su caducidad». Declarados en INC-T123-01: lo que va delante de la tarjeta, la tarjeta seguida de un año y el PIN tras la caducidad |
| H-04 (baja): FALTA en vez de ANTIGUO | Sin datos en la ventana, el último dato de la historia: ANTIGUO con su fecha; sin datos, FALTA. El docstring dice que `desde`, `filas` y `mayor_hueco_dias` son de la ventana |
| H-05 (baja): §1 del borrador | «Retornos internos (CT-06 a CT-08 y CT-11 a CT-14)» y una entrada propia «Retornos del Motor (CT-09 y CT-10)», derivadas de los mismos conjuntos que las filas; INC-T114-01 matizado; borrador regenerado |
| H-06 (baja): mutantes vivos K04, V02, T06, T07 | Pruebas en `test_t145.py` (`main` con `reintento_reparacion` de la configuración, dato malo en el margen de `senales`, meses 00 y 13–19) |

- Contratos CT-G afectados: ninguno. Estado persistido: no cambia.
- Números: todos de la configuración (`llm`, `busqueda_web`, `max_tokens`, `presupuesto_uc`, `uc`, `seleccion.peticiones_conocimiento_por_clase`) y de la tarifa; los límites del mensaje de reparación (15 errores de 300 caracteres) son los del código de `agentes.py`.
- Cómo falla cerrado: la cota se niega (`SystemExit`) con `diseno: v6`, con un ciclo medido que llama a un agente más veces de las que prevé la tabla y sin tarifa de un modelo. R8 marca de más antes que de menos solo donde está declarado.
- Decisiones como `[PROPUESTO]`: la regla nueva de R8 (INC-T123-01) y la definición de la cota (INC-T129-01).

## Coste de un ciclo semanal C1 (tarifa del 15-11-2026, USD)

| Tipos activos | Llamadas (medidas · máximo) | Suelo | Peor caso de las llamadas medidas (T-140; no es cota) | Cota superior del ciclo (T-145) |
| --- | --- | --- | --- | --- |
| Solo divisas (configuración actual) | 8 · 14 | 0,86 | 4,58 | **19,54** (por llamadas; hasta 40 búsquedas; por presupuesto, 68,29) |
| Los 12 tipos (`perfiles.activos` con los doce, en un YAML aparte) | 77 · 91 | 2,98 | 56,79 | **166,56** (por llamadas; hasta 480 búsquedas; por presupuesto, 233,18) |

Supuestos (los imprime el script): S1 tokens ≤ 1,35 veces los del simulador; S2 cada petición en su peor caso (toda la entrada como escritura de caché, `max_tokens` de salida, cada reparación y continuación reenviando lo generado); S3 el número de llamadas de las tablas (C1 de la V5, nivel N2); S4 el encargo de cada llamada, lo medido más la salida máxima de las llamadas que puede leer, copiada una vez; S5 fuera: lo que lee cada búsqueda, reintentos del SDK, tarifa de contexto largo y el texto de ciclos anteriores más allá de lo medido desde un estado vacío. Contraste: los caminos del revisor quedan por debajo (solo divisas: 8,85 y 9,81 con `r01_01`, 4,57 y 5,04 con `r01_02`; los 12 tipos: 79,18 y 79,33, y 36,02 y 36,53).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La cota es muy holgada (S4 suma salidas máximas que en la práctica no llegan) | El operador ve una cifra alta | Se dan también el suelo y el peor caso de las llamadas medidas; la cota se puede afinar con el modo sombra |
| La tabla de llamadas se queda vieja si cambia `orquestacion.py` | Cota por debajo del real | El script falla cerrado si el ciclo medido hace más llamadas de un agente de las previstas; `test_h01_la_tabla_…` fija el número |
| R8 deja de ver una tarjeta con un año delante o detrás | Un dato de tarjeta podría pasar | Declarado; las formas corrientes (caducidad detrás, dos tarjetas, CVV) se detectan |

## Criterios de aceptación (binarios)

1. CA-1: `tests/test_t145.py` en verde, y `tests/test_t140.py` (con su cambio comentado «T-145»), `test_t12*`, `test_t13*`, `test_t141_datos_bce.py` y `goldens_ct.py` sin fallos.
2. CA-2 (H-01): la cota supera el peor camino por el cliente real con la reescritura de AG-17 (`test_h01_la_cota_cubre_…`, que además pasa la cifra de T-140) y los escenarios de `r01_01` y `r01_02` del revisor, con solo divisas y con los 12 tipos.
3. CA-3 (H-02/H-03): `r01_03_tarjetas_series_largas.py`: 0 falsos positivos en las filas con año o fecha delante; detectados «tarjeta, caducidad y otra tarjeta» y «dos tarjetas con su caducidad»; lo demás, declarado.
4. CA-4 (H-04/H-05): `r01_04_ventana_fechas_y_borrador.py` sin fallos.
5. CA-5 (H-06): `mutantes_t145.py`: todos los mutantes muertos.
6. CA-6: ruff ≤ 2838, mypy A ≤ 109.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_h01_la_tabla_de_llamadas_del_ciclo` | nominal | CA-2 |
| `test_h01_la_cota_cubre_el_peor_camino_con_el_cliente_real` | integración, regresión | CA-2 |
| `test_h01_el_presupuesto_se_pasa_y_la_cota_por_presupuesto_lo_cuenta` | integración | CA-2 |
| `test_h01_falla_cerrado` | fallo cerrado | CA-2 |
| `test_h01_peor_llamada_reenvia_y_paga_cada_peticion` | límite | CA-2 |
| `test_h02_…`, `test_h03_…` | regresión, límite | CA-3 |
| `test_h04_…`, `test_h05_…` | regresión | CA-4 |
| `test_h06_…` | regresión (mutantes) | CA-5 |

## Scripts

`.docs/scripts/estimar_coste_ciclo_a.py` (cambia), `medir_consumo_a.py` (se usa), `comprobar_datos_a.py` y `borrador_anexo_b.py` (cambian). En el ticket: `mutantes_t145.py` (mutantes), `contraste_cota.py` (supuesto S4 contra el método del revisor) y `medir_filas_r8.py` (tasas de R8 en filas con la fecha detrás).

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado (sin commit: lo hace quien coordina)
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto: el recuento de llamadas coincide con el código y ningún escenario supera la cota); hallazgos (H-01 media, H-02 a H-07 bajos) en T-148
