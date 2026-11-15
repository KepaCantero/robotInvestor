# T-148 · Bloque A: la contrarréplica en la cota del coste y bajos de la QA r01 de T-145

| Campo | Valor |
| --- | --- |
| Estado | EN CURSO (r02: QA r01 NO APTO) |
| Pieza | bloque_a (estimador de coste): `.docs/scripts/estimar_coste_ciclo_a.py`, `comprobar_datos_a.py`, `borrador_anexo_b.py`; `.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`; `bloque_a/11_Ejecutor/tests/test_t148.py`, `tests/test_t145.py`; `docs/incidencias.md` (INC-T129-01); `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (§7) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; las decisiones nuevas van como `[PROPUESTO]` |
| Deuda técnica | T-148 (número reservado; la fila la pone la sesión coordinadora) |

## Objetivo

Que la cifra de coste que autoriza el operador sea una cota también llamada a llamada (QA r01 de T-145, H-01: el supuesto S4 no se cumple en la contrarréplica) y corregir los seis bajos.

## Alcance

- Entra: H-01 a H-07 de `.docs/tickets/T-145/qa.md`; la variante «con T-146 integrado» de la cota por presupuesto (aviso de la coordinación del 15-11-2026).
- No entra: el código del presupuesto (`consumo.py`, `agentes.py` y el presupuesto de `orquestacion.py` los lleva T-146 en otra copia); la deuda técnica.

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| H-01 (media): S4 no acota la contrarréplica (ni la respuesta a objeciones) | **S4b**: su encargo crece con objeciones × evidencias; el único tope del código es la estimación previa del presupuesto (`Bloque._estimar_uc` ≤ el límite de la bolsa con la ampliación máxima). Esos dos papeles llevan lo medido más ese tope (417 167 tokens en la bolsa de un tipo); en toda llamada con bolsa, el encargo es como mucho ese, aunque S4 dé más. La última llamada de cada bolsa, igual |
| H-02 (baja): lo que lee cada búsqueda | La cifra es «cota salvo lo que lee cada búsqueda» y la salida da su peso por cada 1 000 tokens leídos por búsqueda (lectura en su petición y en cada continuación posterior del intento) |
| H-03 (baja): tipos de F10 frente a `perfiles_activos` | `--estado`: los tipos salen de F10 (P-02), como en `Bloque.ciclo`; sin él, la salida avisa |
| H-04 (baja): mutantes vivos R01, R04–R09 | Pruebas con las cifras a mano en `test_t148.py` |
| H-05 (baja): historia antigua con el último cierre inválido | ANTIGUO con el aviso del dato inválido (y el docstring lo dice) |
| H-06 (baja): §1 del borrador del Anexo B | Cita `motor/servicio.py` para `coincide` y `Bloque._registrar_evidencia_clase` para `independiente`; borrador regenerado (`--comprobar` da 0; en la base daba 1: el borrador no estaba al día con T-145) |
| H-07 (baja): INC-T129-01 «Límites del estimador» desfasada | Al día, con la ronda T-148 |
| Con T-146 integrado (coordinación) | `--con-t146` (`cota_ciclo(…, con_t146=True)`): la cota por presupuesto son solo los límites de las bolsas; si la configuración da `presupuesto_uc.uc_por_busqueda`, su precio por UC entra en el máximo |

- Números: ninguno nuevo en el ejecutor. En el estimador, `TOKENS_FIJOS_ESTIMACION` (1 500) y `SALIDA_ESTIMACION` (2 500) son los de `orquestacion._estimar_uc` (una prueba los compara con el código).
- Falla cerrado: tipos fuera de los doce o repetidos, estado inexistente (no se crea) y llamadas medidas de más: `SystemExit`.

## Coste de un ciclo C1 (tarifa del 15-11-2026)

`medir_consumo_a.py` + `estimar_coste_ciclo_a.py`, sin red ni coste; cifras «salvo lo que lee cada búsqueda»:

| Tipos activos | Suelo | Cota (código con T-146) | Cota de antes de T-146 (`--sin-t146`, más holgada) | Por cada 1 000 tokens leídos por búsqueda |
| --- | --- | --- | --- | --- |
| Solo divisas | 0,86 USD | **28,04 USD** (por llamadas; por presupuesto, 46,08) | 28,04 USD (por presupuesto, 69,62) | +0,40 USD |
| Los 12 tipos | 2,98 USD | **46,08 USD** (por presupuesto; por llamadas, 267,71) | 250,11 USD (por presupuesto; por llamadas, 267,71) | +4,80 USD |

**Integración con T-146 (15-11-2026, al llevar este ticket al árbol principal).** T-148 se hizo en una copia sin T-146 y suponía la estimación previa `_estimar_uc` (mensaje / 3,6 + 1 500, 2 500 de salida), que T-146 quitó. Se adapta: (1) el tope del encargo de S4b es el de `consumo.ReservaLlamada` (la entrada × `presupuesto_uc.reserva.factor_tokens_entrada` y, como poco, `salida_minima_tokens` de salida en el límite de la bolsa), y la prueba lo comprueba contra la reserva del código (`test_h01_el_tope_del_encargo_es_el_de_la_reserva_del_codigo`); (2) la cota con T-146 es la de por defecto (`--con-t146` se acepta y da lo mismo; `--sin-t146`, la de antes); (3) las UC de una búsqueda salen de `uc.uc_por_busqueda_web`, la clave real de T-146, y ese ajuste va en la cota, no en `limites`; (4) M27 de `T-147/mutantes.py` apunta al texto nuevo. Las cifras de arriba son las de esta versión; las de antes (31,50 y 275,77 sin T-146, 46,08 con él) eran con la estimación previa.

En T-145 eran 19,54 y 166,56: suben porque la respuesta a objeciones y la contrarréplica ya no se suponen acotadas por S4. Con T-146 integrado, la cota por presupuesto (todo pasa por él y ninguna bolsa supera su límite) acota también lo que lee cada búsqueda si el presupuesto lo carga; con los 12 tipos manda ella.

## Criterios de aceptación (binarios)

1. CA-1 (H-01): el encargo de la respuesta y de la contrarréplica es lo medido más el tope del presupuesto, calculado a mano; el tope está ajustado a `_estimar_uc` (un mensaje del tope no cabe; uno del 99 %, sí); la cota de la contrarréplica pasa de lo que obtuvo la QA (encargo 222 410 tokens, 5,04 USD) y `r01_01` del revisor queda por debajo en todos sus escenarios.
2. CA-2 (H-02, H-03): la salida dice «salvo lo que lee cada búsqueda» y su peso coincide con la cuenta a mano; con `--estado` los tipos son los de P-02.
3. CA-3 (H-04): los mutantes R01–R12 de `T-145/revisores/r01_04_mutantes.py` mueren con las pruebas fijadas en ese script más `test_t148.py` (una copia del script con `test_t148.py` en `PRUEBAS`: `mutantes_revisor_ampliado.py` no entiende una lista en varias líneas); los del grupo T-148 de `.docs/tickets/T-147/mutantes.py`, también.
4. CA-4 (H-05 a H-07): el aviso de la historia antigua; el borrador cita lo correcto y `--comprobar` da 0; INC-T129-01 al día.
5. CA-5: `--con-t146` da solo los límites; tabla en este README, en INC-T129-01 y en §7 de las decisiones del operador; ruff ≤ 2838 y mypy A ≤ 109.

## Plan de pruebas

| Prueba (`tests/test_t148.py`) | Tipo | Criterio |
| --- | --- | --- |
| `test_h01_…` (cuatro) | nominal, límite, regresión | CA-1 |
| `test_h02_…`, `test_h03_…` | nominal, fallo cerrado | CA-2 |
| `test_h04_r01…` a `test_h04_r09…` | regresión (mutantes) | CA-3 |
| `test_h05_…`, `test_h06_…`, `test_h07_…` | regresión, documentación | CA-4 |
| `test_con_t146_…`; `test_t145.py` (cambia una igualdad, comentada) | nominal | CA-5 |

## Scripts

`.docs/scripts/estimar_coste_ciclo_a.py` (`--estado`, `--con-t146`), `comprobar_datos_a.py`, `borrador_anexo_b.py`; `.docs/tickets/T-145/revisores/r01_01_…`, `r01_03_…` y `r01_04_mutantes.py` (del revisor); `.docs/tickets/T-147/mutantes.py --ticket T-148`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · claude · plan, implementación y pruebas en la copia `t147` (sin commit); aviso de la coordinación sobre T-146 incorporado (`--con-t146`)
- 2026-11-15 · EN QA · claude · pendiente de QA por un agente que no implementó
