# T-134 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude; no es el revisor de la r03 de T-125) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `197aaca` (instantánea para QA de T-131 r02, T-133 y T-134). Mutantes en una copia desechable extraída con `git archive` dentro del scratchpad («qa14_mut»), ya borrada.
- **Orden de lectura:** README → diff de `evaluador.py` (`_finito`, `_prob_valida`, `_numero_finito`, `RE_FECHA_ISO`, `variables_nivel`, `Evaluador.__init__`, `pronosticos_de_fuentes`) y de `orquestacion.py` (`_tipo_con_pronostico_fuente`) → `test_t134_r03_t125.py` → la ronda r03 de `T-125/qa.md` y sus scripts `r03_0*.py` → mis scripts → al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Desde `bloque_a/11_Ejecutor` de la copia, con el intérprete del repositorio (`py`) y `QA_TMP` en el scratchpad.

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| CA-2 · `r03_02` de la r03 de T-125, tal cual | `QA_TMP=<tmp> py ../../.docs/tickets/T-125/revisores/r03_02_fechas_variables_y_numeros.py` | abajo |
| CA-2 · `r03_03`, tal cual | `QA_TMP=<tmp> py ../../.docs/tickets/T-125/revisores/r03_03_ciclo_tras_desbordamiento.py` | **C1 COMPLETO** con el umbral de 400 cifras (antes, `OverflowError`); integridad `True`; C2 COMPLETO |
| CA-2 · `r03_04` (mutantes), tal cual | — | ya no se puede ejecutar: sus textos de M02, M03, M07–M09 y M14 han cambiado en el código (el script exige que aparezcan una vez). M12 y M14 adaptados en mi script 2 |
| Mi script 1 | `QA_TMP=<tmp> py ../../.docs/tickets/T-134/revisores/r01_01_enteros_fechas_y_configuracion.py` | **58 ok, 3 fallos** (H-19) |
| Mi script 2 (mutantes) | desde la raíz: `py .docs/tickets/T-134/revisores/r01_02_mutantes.py <copia «qa14_mut»>/bloque_a` | **14 de 15 muertos**; vivo T13, equivalente |
| Ciclo con un año 0000 | dos ciclos con el cliente simulado (Analista parcheado como en `r03_02`): C1 el 2026-04-03 con una pieza sana y otra con `fecha_emision` «0000-01-01»; C2 en `AS_OF` | C1 COMPLETO y el bloque del año 0000 **entra en F2**; C2 COMPLETO, con la incidencia «Fiabilidad de las fuentes no calculada en este ciclo: date not yet supported on Timestamps which are outside the range of Python's standard library» (H-19) |
| Suite, goldens, gates y cuotas | comunes (ver «Comunes» en `T-131/qa.md`, ronda r02) | 6048 passed; goldens coinciden; ruff 2838; mypy 109; gates ligeros en verde |

### `r03_02` otra vez

| Bloque | r03 de T-125 | Ahora | Juicio |
| --- | --- | --- | --- |
| N02a | cifras de ancho completo, árabes orientales y devanagari, y «2026-07-01-05:00» se leían y eran registrables | las cuatro: `ValueError` y rechazo en el alta; siguen leyéndose «+14:00», 9999-12-31, 0001-01-01 y el espacio Unicode delante | H-16 corregido |
| N02b | la fecha en ancho completo quedaba tal cual en F2 y contaba | nada en F2, no cuenta | H-16 corregido |
| N03b | texto «cierre» → la variable «c» registrable; número 5 → `TypeError` | **igual**, porque el script llama a `motivo_pronostico_fuente_no_registrable` con la lista en crudo; por el ciclo no se llega: el Bloque no se crea con una lista mal formada (mi script 1, E5) | H-17 corregido en el ciclo; la función sigue sin validar su argumento explícito (observación) |
| N04a | `OverflowError` con 10^400 en umbral, rango y probabilidad | los tres rechazados con su motivo | H-14 corregido |
| N04b | el ciclo entero caía | **COMPLETO**; el bloque, rechazado en HA; ninguna incidencia de desbordamiento | H-14 corregido |
| N04c | `fiabilidad_fuentes` caía y se perdía la FUE- de la fuente sana | FUE- de REF-RF-0001 | H-15 corregido |
| N01, N03a, N03c, N03d, N05 | correctos | iguales | correcto |

### Mi script 1

| Bloque | Qué | Obtenido | Juicio |
| --- | --- | --- | --- |
| E1 | alta con 24 valores raros: enteros de 400 y 4 000 cifras (positivos y negativos, en umbral, rango y probabilidad), `1e-400`, NaN y ±inf, listas anidadas (también de 400 niveles), dict, rango de 3, enteros enormes en variable, dirección, ref_id, serie y fechas | 23 rechazados con su motivo y ninguna excepción; `[10^300, 10^301]` (representable) registrable | correcto |
| E2 | 21 fechas «ISO» raras: hora 24, segundo 60, mes 13, 29-02 de 2026, zona +24:00, +99:99 y solo con horas, fracción de 13 cifras, coma decimal, semana, ordinal, signo, NUL, años 0000, 0001, 1677, 2262 y 9999, espacio ideográfico | 20 bien; **«0000-01-01» se lee** (pandas admite el año 0) y como emisión es **registrable**, pero `Timestamp.date()` lanza `NotImplementedError` | H-19 |
| E3 | un ciclo con las 45 piezas raras por finalista | PARCIAL solo porque la Curación (AG-12) se queda sin presupuesto (declarado, R16); ningún bloque raro en F2; lo registrado se relee igual en JSON; `pronosticos_de_fuentes` sin excepción | correcto |
| E4 | F2 con todos los bloques raros junto a uno sano | `pronosticos_de_fuentes` y `fiabilidad_fuentes` lanzan `NotImplementedError` por la emisión «0000-01-01» y se pierde el sano | H-19 |
| E5 | `variables_nivel` = «cierre», 5, `[]`, `[""]`, `["  "]`, `["cierre", 5]`, `[["cierre"]]`, dict, `True` | `ValueError` al crear el Bloque en los nueve; `[" Cierre "]` admite «cierre» | correcto |

### Mutantes (mi script 2, contra `test_t134_r03_t125.py`, `test_t125_r03.py`, `test_t125_r02.py` y `test_t125_fiabilidad_fuentes.py`)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| T01, T02 | `_finito` da True con un desbordamiento · no lo captura | MUERTOS |
| T03, T04 | `_numero_finito` y `_prob_valida` vuelven a `math.isfinite` | MUERTOS |
| T05, T06 | `RE_FECHA_ISO` con `\d` · zona también sin hora | MUERTOS |
| T07, T08, T09 | el Evaluador no valida `variables_nivel` · admite un texto · admite textos vacíos | MUERTOS |
| T10, T11, T12 | `math.isfinite` en el umbral y el rango de `pronosticos_de_fuentes` y en el rango del alta | MUERTOS |
| M12, M14 | (r03 de T-125, adaptados) el C5 sin `run_id` · el alta con la lista por defecto | **MUERTOS** (antes vivos: H-18) |
| T13 | el alta del ciclo con la lista sin validar | VIVO · equivalente: el Evaluador ya la validó al crear el Bloque |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_t134_r03_t125.py` y las pruebas de T-125 dentro de la suite completa: 6048 passed |
| CA-2 | sí | `r03_02` y `r03_03` ya no reproducen H-14 a H-16, y H-17 no se reproduce por el ciclo (N03b llama a la función con la lista en crudo, ver arriba); `r03_04` no aplica al código nuevo y sus M12 y M14, adaptados, mueren |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | suite, goldens, ruff, mypy y gates ligeros en verde |

## Hallazgos de la r03 de T-125

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-14 (media) | **corregido** | N04a, N04b, `r03_03`; E1; T01–T04 y T12 mueren |
| H-15 (baja) | **corregido** | N04c; T10 y T11 mueren |
| H-16 (baja) | **corregido** | N02a, N02b; T05 y T06 mueren |
| H-17 (baja) | **corregido** | E5; T07–T09 mueren |
| H-18 (baja) | **corregido** | M12 y M14 mueren |

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-19 | baja | mi script 1, E2 («0000-01-01») y E4; el ciclo con un año 0000 de la tabla de reproducción | **Esperado** (INC-T125-01: falla por pronóstico, no por run; H-12 y H-15: un bloque raro no hace perder la FUE- de las demás fuentes). **Obtenido:** «0000-01-01» cumple `RE_FECHA_ISO` y pandas lo lee (año 0 proleptico), así que como `fecha_emision` (anterior al objetivo) el alta lo **registra en F2** desde la respuesta del Analista; después `pronosticos_de_fuentes` hace `str(emision.date())` para la clave y `Timestamp.date()` lanza `NotImplementedError` (fuera de lo que admite `datetime.date`). El C5 lo captura y deja «Fiabilidad de las fuentes no calculada en este ciclo», pero se pierde la FUE- de **todas** las fuentes en cada ciclo mientras el bloque siga en la ventana (`fiabilidad_fuentes.ventana_meses`). Es la clase de H-12 y H-15, por una fecha en vez de un número; el ciclo no cae | En `_fecha_de_calendario`, rechazar lo que `datetime.date` no admite (p. ej., `t.year < 1` o intentar `t.date()` y capturar `NotImplementedError` como fecha no legible), y añadir `NotImplementedError` a lo que captura `_campos_pronostico_fuente`; prueba con «0000-01-01» en la emisión, en el alta y en un F2 ya escrito | abierto |

Observación sin gravedad: `motivo_pronostico_fuente_no_registrable(…, variables_nivel_cfg)` no valida la lista que recibe (un texto se recorre letra a letra); todos sus llamadores le pasan `variables_nivel(cfg)` o `None` (que usa la de por defecto, validada), así que hoy no se llega.

Los scripts de ataque están en `revisores/` (`r01_01_enteros_fechas_y_configuracion.py`, `r01_02_mutantes.py`).

## Invariantes

- Sin LLM en la ruta: alta, resolución y FUE- son código. ✔
- Falla cerrado y valida antes de mutar: sí con números enormes, NaN, infinitos, tipos raros y fechas no ISO (el ciclo ya no cae a mitad); **no** del todo con el año 0000, que entra en F2 y luego impide calcular la FUE- (H-19, baja). ✔ con reserva
- Números a mano: ninguno nuevo; `variables_nivel` sigue en la configuración, ahora validada. ✔
- Decisiones del operador: ninguna nueva. ✔
- Secretos y datos personales: gates en verde; mis scripts no llevan ninguno ni identificadores de modelo. ✔
- Documentación: README del ticket, análisis y pruebas al día. ✔

## Lo que no comprobé

- El gate completo (`./tools/check_all.sh`), B (encargo).
- Otros caminos del ciclo con números o fechas del modelo fuera del bloque `pronostico_fuente` (p. ej., los de Prospectiva), salvo lo que recorre un ciclo simulado.
- Un F4 manipulado con un nivel de referencia de 400 cifras (`_rentabilidad_serie` usa `math.isfinite` directamente): lo escribe el código, no el modelo, y la cadena de huellas lo detectaría.

## Veredicto

**APTO** · Los tres criterios se cumplen (CA-3 sin el gate entero) y los cinco hallazgos de la r03 de T-125 están corregidos con sus pruebas: un entero de 400 o 4 000 cifras ya no tumba el ciclo ni la FUE-, las cifras no ASCII y la zona sin hora no se leen, `variables_nivel` mal formada falla al crear el Bloque y las dos conexiones del ciclo tienen prueba (M12 y M14 mueren; 14 de 15 mutantes muertos, el vivo es equivalente). Queda **H-19 (baja)**: una emisión «0000-01-01» entra en F2 y hace perder la FUE- de todas las fuentes en los ciclos siguientes (con incidencia, sin tumbar el ciclo). Sin críticos ni altos: H-19 pasa a la deuda técnica con su ID (o se corrige antes de cerrar: es una línea en `_fecha_de_calendario`). El cierre (estado, deuda, diario, memoria y commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
