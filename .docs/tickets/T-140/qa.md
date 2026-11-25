# T-137 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `b16089e` (instantánea para QA de T-137). El `contratos.py` de T-136 (`HEAD~1`) para comparar, y los mutantes en una copia desechable del scratchpad («qa15_mut»), ya borrada. Sin llamadas a la API ni a servicios de pago: el cliente real se probó con un SDK falso local.
- **Nota:** en el repositorio este ticket pasa a llamarse T-140 (otra sesión subió antes un T-137); aquí se conserva el nombre de la copia.
- **Orden de lectura:** README → diff de `contratos.py`, `evaluador.py`, `estimar_coste_ciclo_a.py`, `comprobar_datos_a.py`, `borrador_anexo_b.py` y de las dos pruebas cambiadas → `llm.py` (`AnthropicClient.generar`), `agentes.py` (reparación), `orquestacion.py` (`_invocar`, presupuesto, peticiones de conocimiento, contrarréplica, reescritura de AG-17), `motor/servicio.py` y `ht01_datos.py` → QA de T-136, T-131 r02 y T-134 → INC-T123-01 → mis scripts → al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

`py` = el intérprete del repositorio. `<doce>`/`<div>`: carpetas de `medir_consumo_a.py` en el scratchpad (con `perfiles.activos` de los 12 tipos en un YAML aparte, y por defecto).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A (una vez) | `cd bloque_a/11_Ejecutor && py -m pytest -q -p no:cacheprovider` | **6060 passed** (26 min) |
| Goldens | `py tests/goldens_ct.py` | coinciden |
| ruff · mypy A | órdenes del encargo | **2838** · **109** (iguales a las cuotas) |
| Gates ligeros | `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | en verde (695 archivos del corpus) |
| Tabla del README | `medir_consumo_a.py` + `estimar_coste_ciclo_a.py`, 12 tipos y solo divisas | **2,98–56,79 USD (240 búsquedas)** y **0,86–4,58**: coincide |
| CA-2 · T-136 `r01_02_cota_por_peticion.py` | `py -I … <doce> --config <doce.yaml>` y `… <div>` | la cota cubre A (25,19 / 2,11) y es igual a B (56,79 / 4,58) |
| CA-2 · T-136 `r01_01_iban_tarjetas_formas.py` | `py -I … <contratos.py de T-136>` | 25 ok, 1 fallo: la fila de 8 números (19/3000), declarada en INC-T123-01; tarjetas junto a otro número 50/50 |
| T-131 `r02_01_ventana_del_ciclo_y_borrador.py` | `py -I …` | **13 ok, 0 fallos** |
| T-134 `r01_01_enteros_fechas_y_configuracion.py` | `QA_TMP=<tmp> py …` desde `bloque_a/11_Ejecutor` | **61 ok, 0 fallos** (H-19 corregido) |
| Mi script 1 | `py -I .docs/tickets/T-140/revisores/r01_01_cota_ciclo_real.py <tmp> [--config <doce.yaml>]` desde `bloque_a/11_Ejecutor` | 12 tipos: **79,18 USD** con las llamadas condicionales al máximo (+39 %); solo divisas: **8,85** (+93 %) (H-01) |
| Mi script 2 | `py -I .docs/tickets/T-140/revisores/r01_02_peor_caso_con_cliente_real.py <tmp> [--config <doce.yaml>] [--forzar-c12]` desde `bloque_a/11_Ejecutor` | cliente real + corte de presupuesto: 12 tipos **36,02**; solo divisas **4,57**, y con la reescritura de AG-17 **5,04 > 4,58** (H-01) |
| Mi script 3 | `py -I .docs/tickets/T-140/revisores/r01_03_tarjetas_series_largas.py <contratos.py de T-136>` | filas con un año o una fecha MMDD y cuatro niveles de índice: **5–8 %** marcadas (T-136: 0) (H-02); falsos negativos no declarados (H-03) |
| Mi script 4 | `py -I .docs/tickets/T-140/revisores/r01_04_ventana_fechas_y_borrador.py <tmp>` | **17 ok, 2 fallos** (H-04, H-05) |
| Mi script 5 (mutantes) | `py .docs/tickets/T-140/revisores/r01_05_mutantes.py <copia «qa15_mut»>` | **15 de 19 muertos**; vivos T06, T07, K04, V02 (H-06) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_t137.py` (12) y las vecinas dentro de la suite completa: 6060 passed |
| CA-2 | sí | T-136 `r01_02`: cubre A, igual a B; `r01_01`: tarjetas junto a otro número 50/50, lo que falla está declarado; `r01_03` de T-136: C03 y C12 mueren (`test_c03_…`, `test_c12_…`; confirmado con mis mutantes T03–T05) |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | suite, goldens, cuotas y gates ligeros en verde |

## Hallazgos de las QA anteriores

| ID | Estado | Evidencia |
| --- | --- | --- |
| T-136 H-01 (media) | **corregido lo que pedía** (cada petición con su `max_tokens`, la salida reenviada y la reparación); queda H-01 de esta ronda | T-136 `r01_02`; K01–K03 mueren |
| T-136 H-02 (media) | **corregido**, con un coste (H-02 y H-03 de esta ronda) | mi script 3 [3]: tarjeta + MMAA, año delante y dos tarjetas: 2000/2000 |
| T-136 H-03 (baja) | declarado en INC-T123-01 | — |
| T-136 H-04 (baja) | **corregido** | `test_c03_…`, `test_c12_…` |
| T-131 H-05 (media) | **corregido** | mi script 4 [1]–[2]: en el borde de la ventana (2023-05-31 dentro, 2023-05-30 fuera) el script y el ciclo dicen lo mismo; cero y fecha repetida antiguos: OK con aviso |
| T-131 H-06 (baja) | **corregido en la tabla**; queda el §1 (H-05) | mi script 4 [6] |
| T-134 H-19 (baja) | **corregido** | mi script 4 [5]: «0000-…» con y sin hora y zona da `ValueError`; 0001, 9999, 1677 y 2262 se leen; T-134 `r01_01` 61/61 |

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | mis scripts 1 y 2 (órdenes de arriba) | **Esperado** (README «Cota superior»; docstring del estimador): una cifra que el ciclo real no puede superar, salvo lo que dice que no incluye (lo leído por cada búsqueda y los reintentos del SDK). **Obtenido:** la cota suma el peor caso de **las llamadas que hizo el cliente simulado**, y varias llamadas del ciclo dependen de la respuesta del modelo y el simulado no las dispara: las peticiones de conocimiento CT-07/CT-08 (hasta `seleccion.peticiones_conocimiento_por_clase` por tipo, a AG-14/AG-16 **con búsqueda**: el simulado hace 6 de 12 con los 12 tipos y 0 de 1 con divisas), la contrarréplica CT-13 de AG-11 (una por tipo: 7 de 12, y 0 de 1) y la reescritura de AG-17 cuando G3 bloquea por legibilidad (C12). Con el método del estimador, al máximo: **79,18 USD** (12 tipos, +39 %) y **8,85** (divisas, +93 %). Y no es solo teórico: pasando el peor caso por el **cliente real** (`AnthropicClient` con un SDK falso que declara la entrada ×1,35 como escritura y `max_tokens` de salida, `pause_turn` hasta el máximo y una reparación) y por el **corte de presupuesto UC** de `_invocar`, solo divisas da 4,57 y, con la reescritura de AG-17 que pide un texto real por debajo de Fernández-Huerta 70, **5,04 USD > 4,58** (la bolsa COMÚN con un solo tipo tiene 222 UC y no corta). Con los 12 tipos el presupuesto sí corta (36,02 por ese camino), así que ni 56,79 ni 79,18 son el máximo real: lo que de verdad acota el ciclo es el presupuesto UC (más las búsquedas, que no cuentan en UC), y el estimador no lo usa. Además, con la cota «toda la entrada como escritura», el propio presupuesto se agotaría antes de llegar a las 77 llamadas | Añadir a la cota las llamadas condicionales hasta sus topes del código (peticiones por tipo, una contrarréplica por tipo, una reescritura de AG-17) o, mejor, calcular la cota con los topes del presupuesto (`presupuesto_uc` por bolsa con sus ampliaciones, al peor precio por UC de los agentes de cada bolsa, más la última llamada que se pasa y las búsquedas); en todo caso, decir en el README, en la salida del script e INC-T129-01 que la cifra es «sobre las llamadas del ciclo simulado». Conviene antes de pedir al operador que autorice gasto con la tabla | abierto |
| H-02 | media | mi script 3 [1] | **Esperado** (INC-T123-01, T-136: «cinco o más números de cuatro cifras seguidos son una fila de tabla»; T-137 declara solo la fila de 8 al 0,6 %). **Obtenido:** una fila de cinco números con un año (o una fecha MMDD o MMAA) en un extremo y cuatro números del rango de una red de pago se marca como tarjeta cuando esos cuatro pasan Luhn: «año + cuatro cierres trimestrales» de un índice entre 4000 y 5999 (S&P 500 o Euro Stoxx 50 de 2021–2024): **7,5 %**; con el año al final 8,2 %; fecha MMDD delante 8,2 %; año y cuatro precios del oro (1800–2700, prefijo de Mastercard) 5,2 %; con guiones 7,3 %; T-136: 0 en todos. Es la clase de falso positivo de H-02 de T-130 (bloquea la respuesta del agente sin reparación: `agentes.invocar` corta con «respuesta bloqueada por R8»), no declarada, y `test_c12_…` solo prueba filas de 4000–5999 sin fecha, en las que la regla nueva no puede disparar | Pedir más que «forma de fecha» a lo que sobra (p. ej., MMAA solo detrás de la tarjeta y con un año de caducidad plausible respecto a as_of, el año solo delante) y medirlo con filas de este tipo; declarar en INC-T123-01 la tasa real con filas «año + niveles»; prueba con esas filas | abierto |
| H-03 | baja | mi script 3 [2] | **Obtenido:** 0 de 2000 detectadas: «año <tarjeta> MMAA», «MMAA <tarjeta> año», «<tarjeta> MMAA <tarjeta>», dos tarjetas cada una con su caducidad y «<tarjeta> MMAA PIN» (PIN que no empieza por 01–12, 19 o 20). Con T-136 tampoco se detectaban (no es regresión de esta ronda), pero T-130 sí (ventanas) e INC-T123-01 solo declara «una tarjeta seguida de un número que no es una fecha» | Probar todos los desplazamientos de una ventana de 4 grupos (o de varias) y exigir que el resto sea fecha u otra tarjeta; o declarar los casos en INC-T123-01 | abierto |
| H-04 | baja | mi script 4 [3] | **Esperado** (docstring: FALTA = «no hay archivo», ANTIGUO = el último cierre es demasiado antiguo). **Obtenido:** un símbolo con archivo y datos que acaban antes de la ventana (último cierre en 2022, as_of 2026-06-30) sale **FALTA** con «HT-01: sin datos de EURUSD=X en el rango», sin fechas; antes de T-137 salía ANTIGUO con su último cierre. El ciclo también lo excluye (el resultado es correcto, la etiqueta no). Además `desde`, `filas` y `mayor_hueco_dias` son ahora los de la ventana y el docstring no lo dice | Si la ventana sale vacía, leer la historia hasta as_of y dar ANTIGUO con la última fecha; decir en el docstring que las cifras son de la ventana | abierto |
| H-05 | baja | mi script 4 [6]; `borrador_correccion_anexo_b.md`, §1 | El §1 sigue diciendo «Retornos internos (CT-06 a CT-14) … la respuesta de cada agente se valida con los esquemas de `ESQUEMAS`», que contradice las filas nuevas de CT-09 y CT-10 (los sirve el Motor). El texto del cambio de tipo es ahora genérico («admitir el tipo que envía el ejecutor»): ya no es falso, pero no dice cuál | «CT-06 a CT-14 salvo CT-09 y CT-10» en el §1 (y matizar INC-T114-01) | abierto |
| H-06 | baja | mi script 5 (mutantes) | Viven: **K04** (`main` sin pasar `reintento_reparacion`: la cifra del README bajaría a 25,19 sin que falle ninguna prueba), **V02** (ventana con `max` en vez de `min`: pierde los 30 días de margen de `senales`; ninguna prueba en ese tramo), **T06** (mes «00» como MMAA) y **T07** (meses 13–19 como fecha; solo se prueba «9999») | Pruebas: `main` con una configuración que tenga `reintento_reparacion`; un dato malo entre 3 años y 3 años + 30 días; «<tarjeta> 0028» y «<tarjeta> 1500» no se marcan | abierto |

### Las dos expectativas cambiadas

- `test_t136_coste.py` (`test_h01_…`): la cifra esperada sube a la suma petición a petición. Está justificada: es la corrección de H-01 de T-136 y la prueba es más exigente, no menos (K02 y K03 mueren).
- `test_t136_r8.py` (`test_h02_filas_…`): de «ninguna fila de 8 marcada» a «como mucho 50 de 5000». Es un debilitamiento deliberado y declarado (0,6 % medido; 19/3000 en `r01_01` de T-136, 14/2000 en mi script), a cambio de detectar dos tarjetas seguidas. Aceptable como decisión, pero la prueba no mira las filas de 5 con un año, que es donde está el coste grande (H-02).

## Invariantes

- Sin LLM en la ruta: R8, la comprobación de datos, el estimador y el borrador son código. ✔
- Falla cerrado y valida antes de mutar: «0000-01-01» ya no entra en F2 (`ValueError` en el alta y al leer un F2 antiguo); la comprobación no da OK a nada que el ciclo rechace en su ventana. R8 marca de más (H-02, fallo cerrado) y de menos en formas raras (H-03). ✔ con reserva
- Números a mano: la ventana sale de `senales` y `tasa_base`; `_forma_de_fecha` usa el calendario (mes 01–12, años 19xx/20xx), no umbrales. ✔
- Decisiones del operador: INC-T123-01 al día con la regla nueva, pero sin la tasa de H-02 ni los casos de H-03. ✔ con reserva
- Secretos y datos personales: `secrets_scan.py` en verde; mis scripts generan las tarjetas al azar con Luhn y no llevan identificadores de modelo. ✔
- Documentación: README del ticket, INC-T123-01 y el borrador al día; la tabla de coste hay que revisarla con H-01. ✔ con reserva

## Lo que no comprobé

- El gate completo (`./tools/check_all.sh`), B (encargo).
- Los precios, la página de la herramienta de búsqueda y si un `messages.create` que vence por `timeout_s` y el SDK reintenta se cobra (el estimador lo deja fuera como «reintentos del SDK por errores de red»; un tiempo agotado no es un error de red).
- Una cota rigurosa con el presupuesto UC (H-01): mi script 2 recorre un solo camino del peor caso, no el máximo sobre todos los órdenes posibles.
- Los tokens del mensaje de errores de una reparación (hasta 15 errores de 300 caracteres): la cota no los cuenta; los absorbe el margen de 1,35 de la entrada, que está pensado para el tokenizador.

## Veredicto

**APTO** · Los tres criterios se cumplen (CA-3 sin el gate entero, por instrucción): suite completa 6060 passed, goldens, cuotas y gates ligeros en verde, y los siete hallazgos de las QA de T-136, T-131 r02 y T-134 quedan corregidos o declarados (H-19 y H-05 de T-131 con prueba en el borde). No hay críticos ni altos. Quedan dos **medios**: **H-01**, la «cota superior» solo acota las llamadas que hizo el cliente simulado: faltan las que dependen de la respuesta del modelo, y con solo divisas un camino que pasa por el cliente real y por el presupuesto llega a 5,04 USD frente a 4,58; y **H-02**, la regla nueva de R8 marca como tarjeta del 5 al 8 % de las filas «año + cuatro niveles de índice». Y cuatro bajos (H-03 a H-06). Pasan a la deuda técnica con su ID. Conviene corregir H-01 antes de pedir al operador que autorice gasto con la tabla del README, y H-02 antes del modo sombra con textos reales. El cierre (estado, deuda, diario, memoria y commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
