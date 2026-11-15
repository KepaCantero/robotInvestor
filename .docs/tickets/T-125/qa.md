# T-125 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no implementó T-125) · **Ronda:** r01 · 2026-11-15
- **Copia revisada:** clon desconectado en `fb3ccd4` (incluye `df4a60a`, el commit de T-125). Mutantes en una copia desechable aparte («qa7_mut»), ya borrada.
- Opinión formada con el plan (PB-46), el Documento 0 (12.2, 12.5, 13.3, rúbrica de F9), los esquemas de F2 (3, reglas 2–4 y 8; 4.1) y F6 (4.5) y el código, antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

| Qué | Orden (desde `bloque_a/11_Ejecutor`) | Resultado |
| --- | --- | --- |
| Pruebas del ticket | dentro de la suite completa de A | en verde (ver la suite en `T-116/qa.md`, ronda r04) |
| Goldens de contratos | `python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff (tres `11_Ejecutor`, como el gate) | `ruff check --output-format=concise … \| wc -l` desde la raíz | 2902 (cuota 2902) |
| Gates ligeros | `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | los cuatro con 0 |
| Ataques | `QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r01_01_ataques_fiabilidad.py` | abajo |
| Camino de entrada a F2 | `QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r01_03_camino_de_entrada_a_f2.py` | abajo (H-01) |
| Mutantes | desde la raíz: `python .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia desechable de bloque_a con «_mut»>` | abajo |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · dos fuentes de 25, FUE- con la fórmula, la hábil > 10 y la otra < 10 | sí | `test_pb46_dos_fuentes_…`; K03 y K14 mueren. A mano (A8): BSS 0 da 10 puntos; una fuente que siempre falla con 0,99 da 0 |
| CA-2 · en un ciclo, la FUE- en F6 con el `msg_id` del CT-19 a AG-16 | sí, **solo con F2 sembrado a mano** | `test_pb46_las_fue_quedan_…` (K02 muere). Pero en un ciclo de verdad F2 nunca recibe un pronóstico de fuente (H-01) |
| CA-3 · una vez al mes; sin muestra, nada | sí, con un matiz (H-06) | K04 y K10 mueren. A4: con dos ciclos en junio, la fuente que llega a `n_min` a mitad de mes espera a julio |
| CA-4 · no vencidos, mal formados o sin dato no cuentan; las cuatro direcciones | **no** | Una fecha objetivo con zona horaria (ISO válido) lanza `TypeError` y tumba el C5 entero en cada ciclo (H-02). Además, dos casos de la prueba pasan por otro motivo: «fuera de ventana» (2020) y «no ha vencido» (2026-12-31) caen por falta de datos o por la antigüedad del cierre, no por la regla que dicen probar: K05 y K07 viven (H-07) |
| CA-5 · sin pronósticos de fuentes el ciclo no cambia; goldens, ruff, mypy, gate | sí en lo comprobado | goldens y ruff, arriba; mypy y el gate no los he pasado (encargo) |

## Ataques (`revisores/r01_01_ataques_fiabilidad.py`, ejecutado)

| Ataque | Obtenido | Juicio |
| --- | --- | --- |
| A1 · la pieza entra en F2 cuando su fecha objetivo ya pasó (resultado conocido al registrarla) | 5 de 5 cuentan | H-03 |
| A2 · `ref_id` arbitrario («cualquier cosa», «OPP-2026-0001», «REF-9999») | tres FUE- con esos `ref_id` | H-04 |
| A3 · el mismo pronóstico de la fuente en dos afirmaciones de texto distinto | n = 10 en vez de 5 | H-05 |
| A4 · dos ciclos en junio; REF-0002 llega a 5 resueltos entre los dos | junio: solo REF-0001; julio: REF-0001 y REF-0002 | H-06 |
| A5 · probabilidades 0, 1, NaN, inf, −0,2, «0.7», 70, `[0.7]`, `True` | fuera; 1e-9 y 0,999999999 cuentan; sin declarar → 0,7 | correcto (falla cerrado) |
| A6 · fechas | con hora, cuenta; objetivo = `as_of`, cuenta; 30 de febrero, número, fuera de ventana, objetivo > `as_of`, objetivo = emisión: fuera; **con zona horaria: `TypeError`** | H-02 |
| A6b/A6c · una sola pieza con zona horaria dentro de un ciclo | el ciclo acaba COMPLETO, pero `evaluacion` = `{"error"}`, ninguna FUE- (tampoco la de la fuente sana) e incidencia HERRAMIENTA «Evaluador no disponible»; un mes después, otra vez | H-02 |
| A7 · determinismo (mismo escenario, dos almacenes) | idénticos | correcto |
| A8 · extremos | siempre 0,99 y falla: BSS −2,92, puntos 0; siempre 0,5: BSS 0, puntos 10 | correcto |
| A9 · `prob_sin_declarar` frente a la banda «más probable que no» | 0,7 frente a 0,65 de `bandas_verbales` | H-08 |

## Camino de entrada a F2 (`revisores/r01_03_camino_de_entrada_a_f2.py`, ejecutado)

Con el cliente simulado parcheado para que el Analista devuelva en cada afirmación un bloque `pronostico_fuente` completo y el Curador las clasifique como PRONOSTICO_FUENTE (lo más que puede hacer el modelo real): «ciclo COMPLETO · CLM en F2: 12 · clasificadas PRONOSTICO_FUENTE: 12 · **con bloque pronostico_fuente: 0** · pronósticos de fuentes que ve el Evaluador: 0». Leído: `_f_analistas` construye cada pieza con cinco claves fijas (`afirmacion`, `fuente`, `direccion`, `extracto`, `origen`; `orquestacion.py`, línea 882), y las piezas del Buscador y del momentum tampoco llevan el bloque (líneas 885 y 958); la línea nueva de T-125 (`clm["pronostico_fuente"] = dict(p["pronostico_fuente"])`, 1265) no se alcanza nunca. K01 (borrarla) vive.

## Mutantes (`revisores/r01_02_mutantes.py`, contra las 12 pruebas de `test_t125_fiabilidad_fuentes.py`)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| K01 | el alta en F2 deja de guardar `pronostico_fuente` | **VIVO** (H-01) |
| K02 | la FUE- no anota el `msg_id` del CT-19 | MUERTO |
| K03 | sin contracción n / (n + k) | MUERTO |
| K04 | sin «una vez al mes» | MUERTO |
| K05 | sin ventana de 24 meses | **VIVO** (H-07) |
| K06 | sin el control de antigüedad del cierre (H2) | **VIVO** (H-07) |
| K07 | cuenta pronósticos no vencidos | **VIVO** (H-07; el proveedor recorta en `as_of`, así que no hay fuga, pero la regla no tiene prueba) |
| K08 | admite emisión = objetivo | **VIVO** (baja, dentro de H-07) |
| K09 | probabilidad sin declarar 0,5 | MUERTO |
| K10 | `n_min` uno menos | MUERTO |
| K11 | puntos sin acotar a [0, 20] | **VIVO** (H-07) |
| K12 | admite probabilidad 0 y 1 | **VIVO** (H-07) |
| K13 | «dentro» con bordes abiertos | **VIVO** (H-07) |
| K14 | referencia ingenua fija en 0,4 | MUERTO |

Resumen: 6 de 14 muertos (K02, K03, K04, K09, K10, K14), 8 vivos.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_03_camino_de_entrada_a_f2.py`; leer `orquestacion.py` 880–890 y 955–960; K01 de `r01_02` | Esperado (README, Diseño: «el registro de evidencia guarda ahora ese bloque cuando la pieza lo trae»; Doc. 0 12.5): un pronóstico explícito de una fuente que devuelve un agente llega a F2 y el Evaluador lo mide. Obtenido: **ninguna pieza puede traer el bloque**; el ejecutor reconstruye cada pieza con claves fijas y lo pierde, también con el modelo real. Fuera de las pruebas (que siembran F2 a mano), ningún ciclo produce nunca una FUE-. El análisis técnico lo atribuye al cliente simulado («con el cliente simulado no se generan piezas PRONOSTICO_FUENTE»), y el mapa de PB-46 solo declara como hueco la recalificación en F9 | Copiar `pronostico_fuente` (y `tipo_afirmacion`) de la afirmación del Analista y de la referencia del Buscador a la pieza, validado (H-02, H-04) y con su prueba de extremo a extremo (cliente simulado parcheado, como `r01_03`); o, si se decide no hacerlo ahora, declararlo como hueco en el mapa (PB-46), en INC-T125-01 y en el análisis, sin atribuirlo al simulador |
| H-02 | media | `r01_01`, A6, A6b y A6c | Esperado (CA-4; docstring: «uno mal formado o sin dato se omite»): la pieza se omite. Obtenido: `fecha_objetivo` con zona («2025-06-02T10:00:00+05:00») lanza `TypeError: Cannot compare tz-naive and tz-aware timestamps`; `Bloque.ciclo` lo recoge como «Evaluador no disponible», el resultado del C5 del run se pierde (`evaluacion = {"error"}`, sin FUE- de ninguna fuente) y, como F2 es append-only y la ventana es de 24 meses, se repite en cada ciclo. Hoy no llega por H-01; en cuanto se conecte, sí | En `_campos_pronostico_fuente`, normalizar a fecha sin zona (`tz_convert(None)` o quedarse con la fecha) o rechazar la pieza; envolver cada pieza para que una sola no tumbe las demás; prueba con zona, con `Z` y con hora |
| H-03 | media | `r01_01`, A1 | Esperado (F2, regla 4: «`conocible_desde` … es el filtro anti-fuga»; Doc. 0 12.2: sin fuga): solo cuentan los pronósticos registrados antes de conocerse su resultado. Obtenido: una pieza que entra en F2 después de su fecha objetivo cuenta igual; un agente que cita «como predijo X» solo lo que acertó infla la fiabilidad de esa fuente. No está en INC-T125-01 | Contar solo las CLM cuya alta en F2 (o `conocible_desde` de su evidencia) sea anterior a la fecha objetivo; decisión `[PROPUESTO]` en INC-T125-01 y prueba |
| H-04 | media | `r01_01`, A2 | Esperado (valida antes de mutar): el `ref_id` es el de una fuente registrada de F9 (o, al menos, la fuente de la evidencia de la pieza). Obtenido: FUE- para «cualquier cosa», «OPP-2026-0001» y «REF-9999», que se comunican al Buscador por CT-19 | Exigir que `ref_id` exista en F9 (`Referencias.por_id`) y coincida con la fuente de la pieza; prueba |
| H-05 | baja | `r01_01`, A3 | Esperado (R10, contar raíces): un mismo pronóstico de la fuente cuenta una vez. Obtenido: dos afirmaciones de texto distinto con el mismo bloque dan n = 10 en vez de 5 (la deduplicación de CLM es por texto) | Deduplicar por (`ref_id`, `serie_ht01`, `fecha_objetivo`, `umbral_o_rango`, `direccion`, `fecha_emision`) |
| H-06 | baja | `r01_01`, A4 | INC-T125-01 dice «una FUE- por fuente y mes»; el código hace «una tanda por mes»: si hay alguna FUE- del mes, no calcula ninguna más, y una fuente que llega a `n_min` después espera al mes siguiente | Comprobar el periodo por `ref_id`, o decir en INC-T125-01 que es una tanda mensual |
| H-07 | baja | K05 a K08 y K11 a K13 de `r01_02` viven | En `test_pb46_no_se_resuelve_…` el caso «fuera de ventana» (objetivo 2020) cae porque los datos sintéticos empiezan en 2022, y el de «no ha vencido» (2026-12-31) por la antigüedad del cierre: ninguna de las dos reglas tiene prueba. Tampoco la antigüedad, los bordes de «dentro», el tope de puntos ni el rechazo de 0 y 1 | Casos con datos dentro de la ventana y un día fuera; objetivo `as_of` + 1 con cierre fresco; cierre de hace 4 días; valor justo en el borde del rango; p = 0 y 1; fuente que siempre falla (puntos 0) |
| H-08 | baja | `config/por_defecto.yaml`, `fiabilidad_fuentes.prob_sin_declarar` | El comentario dice 0,7 «más probable que no», y la banda «más probable que no» de `bandas_verbales` tiene `prob_interna` 0,65. Además, la FUE- sale con `calc_id: null`, cuando el esquema de F6 (4.5) lo nombra y las demás métricas del Evaluador pasan por el Motor (FC-EVAL-001) | Usar la `prob_interna` de la banda (o explicar en INC-T125-01 por qué 0,7) y pasar el cálculo por el Motor o decir por qué no |

## Invariantes

- Sin LLM en la ruta: la FUE- y el CT-19 son deterministas. ✔
- Falla cerrado y valida antes de mutar: **no del todo** (H-02 tumba el C5; H-04 acepta cualquier `ref_id`). ✗
- Números: los de la fórmula salen de la configuración (k, neutro y máximo citan el esquema de F6; el resto `[PROPUESTO]`). ✔, con la nota de H-08.
- Decisiones del operador: las `[PROPUESTO]` están en INC-T125-01, salvo el trato del registro tardío (H-03). ✗ (menor)
- Secretos y datos personales: nada (los gates en verde). ✔
- Documentación: el análisis atribuye al simulador lo que es del ejecutor (H-01). ✗

## Lo que no comprobé

- mypy y el gate completo (`check_all.sh`), por el encargo; A-Forex y B.
- Que el Buscador use la FUE- (fuera del ejecutor).

## Veredicto

**NO APTO** · H-01 (alta): la función nueva no se alcanza en ningún ciclo, porque el ejecutor pierde el bloque `pronostico_fuente` al construir las piezas, y la documentación lo atribuye al cliente simulado. CA-4 no se cumple (H-02: una fecha con zona tumba el C5 en cada ciclo). Tras la corrección, volver a ejecutar `r01_01`, `r01_02` y `r01_03`.
