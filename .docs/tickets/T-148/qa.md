# T-148 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó Claude) · **Ronda:** r01 · 2026-11-15
- **Copia:** git worktree en el scratchpad con HEAD `f197bc5` (T-148 ya integrado con T-146) y `.venv` enlazado. Sin red, sin la API y sin coste. Opinión formada con el README, el diff de HEAD y `consumo.py` (`ReservaLlamada`, `Presupuesto`, `Contabilidad.uc_de`) antes de leer `analisis-tecnico.md`. T-146 no se revisa aquí (está en su ronda r02); lo que de él afecta a T-148 va en «Observaciones».

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez | **6338 passed** en 24 min 8 s; exit 0 |
| `pytest -q tests/test_t148.py tests/test_t145.py …` | en verde (218 con los de T-147 y T-144) |
| ruff · mypy de A · gates ligeros · goldens | 2838 · 109 · en verde · coinciden (102 passed) |
| `medir_consumo_a.py <tmp>/m_div` y `<tmp>/m_12 2024-03-29 --config <doce.yaml>` (`perfiles: {activos: [los doce]}`), luego `estimar_coste_ciclo_a.py` por defecto, `--con-t146` y `--sin-t146` | divisas: **28,04** (presupuesto 46,08) con y sin la opción, `--sin-t146` 28,04 (69,62); 12 tipos: **46,08** por presupuesto, **por llamadas 268,48** y `--sin-t146` **248,02** (el README dice 267,71 y 250,11: H-02). Dos medidas seguidas de los 12 tipos dan el mismo multiconjunto de llamadas y las mismas cifras; también midiendo con el código de `b0046a1` |
| `T-145/revisores/r01_01_amplificacion_contrarreplica.py <tmp> <tmp>/m_div --n 120,150,170 --salida real --k 1` (y `--reparar-papel contrarreplica --modo cota`, con N = 60 también) | todos los escenarios por debajo de la cota: el ciclo cuesta 1,42–2,78 USD frente a 28,04; la contrarréplica, como mucho 1,26 USD (su cota, 7,64). Con T-146 las N grandes se cortan por presupuesto antes de la contrarréplica |
| `T-145/revisores/r01_03_comprobar_datos_bordes.py <tmp>` | fallos: 0 (las historias inválidas, con su aviso) |
| `T-145/revisores/r01_04_mutantes.py <copia «t147_mut»>` con sus pruebas · la misma lista con `tests/test_t148.py` añadido a `PRUEBAS` (copia del script en el scratchpad) | 5 muertos y 7 vivos (como antes) · **12 de 12 muertos** |
| `.docs/tickets/T-147/mutantes.py <copia «t147_mut»>` | grupo T-148: **8 de 8 muertos** (M25–M32) |

## Integración con T-146 (lo que pidió la coordinación)

- **El tope del encargo (S4b) es el que admite `ReservaLlamada`.** `r01_01` A busca, con la reserva del código, el mayor mensaje que sale en cada bolsa vacía con la ampliación máxima: bolsa de un tipo, tope 310 123 tokens y admitido 310 096; COMÚN con un tipo, 4 167 901 y 4 167 860; COMÚN con 12, 3 190 123 y 3 190 077 (con la herramienta de búsqueda, algo menos: sus UC reservadas). Cubre y es ajustado (a menos del 0,01 %). La COMÚN del estimador (240 − 5·n) no es menor que la del ciclo en N1 o N2. Coincide con la fórmula de `uc_de` (0,5·entrada/8 000 + 0,5·salida/1 500) y con `limite_maximo` (base × 1,5).
- **`--sin-t146` y `--con-t146`.** Por defecto y con `--con-t146` dan lo mismo (solo los límites); `--sin-t146`, la cota de antes con su desglose. Las dos a la vez se aceptan y manda `--sin-t146` sin aviso (H-03).
- **Las cifras.** 28,04 (divisas) y 46,08 (12 tipos) se reproducen. 46,08 = 360 UC × 0,128 USD/UC (Opus): el tope del ciclo con la ampliación máxima. Las cifras secundarias de los 12 tipos no (H-02).
- **Lo que no se cumple:** la salida de los 12 tipos dice que, con T-146, el presupuesto acota también lo que lee cada búsqueda, y no es así (H-01).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_h01_*` (con el tope de `ReservaLlamada`); `r01_01` A; `T-145/r01_01` por debajo en todos sus escenarios |
| CA-2 | **no** (12 tipos) | Divisas: la salida dice «salvo lo que lee cada búsqueda (S5)» y el peso (0,40 USD por cada 1 000 tokens) coincide con `test_h02_…`. Con los 12 tipos, la línea de la cota dice «con T-146, el presupuesto acota también lo que lee cada búsqueda», y `r01_01` C muestra que una petición admitida cuya búsqueda lee deja la bolsa por encima de su límite (H-01). `--estado`: los tipos salen de P-02 (`r01_01` D) |
| CA-3 | sí | `T-145/r01_04` 12 de 12 con `test_t148.py`; M25–M32 muertos; mutantes propios Q12–Q15 (`T-147/revisores/r01_03_mutantes_qa.py --ticket T-148`), 4 de 4 muertos |
| CA-4 | sí | `T-145/r01_03` sin fallos; `test_h05/h06/h07` en verde |
| CA-5 | sí, con matiz | `--con-t146` da solo los límites; la tabla está en el README, en INC-T129-01 y en §7 de las decisiones del operador, pero dos de sus cifras no se reproducen (H-02) |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media (rompe CA-2) | `.venv/bin/python -I .docs/tickets/T-148/revisores/r01_01_tope_y_cota_con_t146.py <tmp>/m_div <tmp>/m_12 <doce.yaml> <tmp>` (caso C) y `estimar_coste_ciclo_a.py <tmp>/m_12 --config <doce.yaml>` | Esperado (CA-2 y la decisión del operador, «salvo lo que lee cada búsqueda»): la cota no promete cubrir lo que lee cada búsqueda. Obtenido: cuando manda la cota por presupuesto (12 tipos), la salida dice «con T-146, el presupuesto acota también lo que lee cada búsqueda», y el README («ninguna bolsa supera su límite… acota también lo que lee cada búsqueda»), el docstring de `cota_ciclo` e INC-T129-01 dicen lo mismo. No es así: `ReservaLlamada` reserva la entrada medida, la salida y las UC de las búsquedas, pero no lo que leen, que la API cobra como entrada de la misma petición; con la bolsa llena hasta su peor caso, una petición con cinco búsquedas que leen 8 000 tokens cada una la deja **+2,31 UC** por encima de su límite (22,50). Pasa lo mismo con un tokenizador peor que 1,35 (T-146, QA r01, H-04). Así, «solo los límites» no es una cota del ciclo: falta lo que leen las búsquedas de la última petición de cada bolsa (sin tope, porque lo que lee una búsqueda no lo tiene) | Mientras T-146 no reserve una lectura por búsqueda: decir también con T-146 «salvo lo que lee cada búsqueda (en la última petición de cada bolsa) y lo que la entrada pase del margen 1,35» y quitar la frase de la salida, del README, del docstring y de INC-T129-01; si T-146 r02 reserva la lectura (su H-04), sumar a la cota ese margen por petición y citarlo. Prueba: la frase no sale cuando hay búsquedas | abierto |
| H-02 | baja | `medir_consumo_a.py <tmp>/m_12 2024-03-29 --config <doce.yaml>` y `estimar_coste_ciclo_a.py <tmp>/m_12 --config <doce.yaml> [--sin-t146]` | Esperado: las cifras de la tabla del README, de `pruebas.md` («Integración con T-146») e INC-T129-01. Obtenido: por llamadas **268,48** (dice 267,71) y `--sin-t146` **248,02** (dice 250,11). Es determinista (dos medidas iguales) y sale igual midiendo con el código de `b0046a1`, así que la cifra publicada se midió con otra medida. La cota que manda (46,08) no cambia | Volver a medir y poner las cifras con la orden y la configuración exactas (`doce.yaml`) en `pruebas.md` | abierto |
| H-03 | baja | `estimar_coste_ciclo_a.py <tmp>/m_div --sin-t146 --con-t146`; lectura de `LLAMADAS_DEL_CICLO` | (a) Las dos opciones a la vez se aceptan y manda `--sin-t146` en silencio (deberían excluirse: `add_mutually_exclusive_group`). (b) `LLAMADAS_DEL_CICLO` sigue poniendo AG-20, AG-18 y AG-19 con bolsa `None` (fuera del presupuesto), cuando con T-146 pagan de la COMÚN (lo dice el docstring de `cota_ciclo`): por eso S4b no acota sus encargos en la cota por llamadas. Es más holgado, no un error de la cota, pero la tabla describe el código de antes. (c) Quedan textos de antes de T-146: el punto S4b de INC-T129-01 sigue diciendo que el tope es `Bloque._estimar_uc` con 417 167 tokens (el punto siguiente lo corrige), el CA-1 del README habla de `_estimar_uc` y el comentario de la cota por presupuesto en el estimador cita `Presupuesto.puede` | Grupo excluyente para las dos opciones; con `con_t146`, AG-18/19/20 en la COMÚN (o un comentario que diga por qué se dejan fuera); poner al día el punto S4b de INC-T129-01 (310 123 tokens, la reserva de T-146) y el comentario | abierto |

## Observaciones sobre T-146 que afectan a T-148

- **T-146 r01 H-04 (lectura de las búsquedas y margen del tokenizador sin reservar) y H-03 (C5 con escala):** son la causa de H-01. Si la r02 de T-146 cambia la reserva, la cota «con T-146» de este estimador tiene que seguirla.
- **T-146 r01 H-01 (factor observado):** solo encoge lo que admite la reserva, así que el tope S4b sigue siendo una cota por encima.
- **Escala y N3:** el tope S4b y los límites suponen un ciclo C1 en N1 o N2 sin escala (S3). Con `nivel_forzado`, una profundización (N3) o un `presupuesto_override`, las bolsas de un tipo pueden pasar de 27 UC (con N3 y un solo tipo, hasta 75); la línea de órdenes no lo permite hoy en un C1, así que no es un hallazgo, pero la cota no vale para esos ciclos.

Scripts de esta ronda: `revisores/r01_01_tope_y_cota_con_t146.py` y, para los mutantes, `.docs/tickets/T-147/revisores/r01_03_mutantes_qa.py --ticket T-148`.

No comprobado: el gasto real con la API (sin red ni coste); `./tools/check_all.sh` entero.

## Veredicto

**NO APTO** · H-01 (media) rompe el CA-2: con los 12 tipos, la salida afirma que la cota cubre lo que lee cada búsqueda, y una petición con búsquedas que leen deja su bolsa por encima del límite. El resto de la integración con T-146 es correcto (el tope de S4b coincide con `ReservaLlamada`, `--con-t146` y `--sin-t146` hacen lo dicho, 28,04 y 46,08 se reproducen). La corrección es de texto y una prueba; en la r02 se vuelve a pasar `r01_01` (caso C y la salida de los 12 tipos) y se corrigen H-02 y H-03, o pasan a la deuda.
