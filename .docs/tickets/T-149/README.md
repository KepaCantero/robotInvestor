# T-149 · Bloque A: hallazgos de las QA r01 de T-144 y T-147 (copias en rejillas no decimales, mensajes sin datos R8, BCE, mutantes y G3 antes de encargar)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/motor/frontera_b.py`, `bloque_a/cadena_b.py`, `README.md`, `tests/test_t149.py`, `tests/test_t144.py`, `tests/test_t147.py`); `.docs/scripts/cadena_a_b.py` y `descargar_datos_bce.py`; `docs/incidencias.md` (INC-T127-01 y INC-T142-01, rondas T-149); `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (fila de las fichas con componentes) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; las decisiones nuevas van como `[PROPUESTO]` |
| Deuda técnica | T-149 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la pone la sesión coordinadora) |

## Objetivo

Cerrar los hallazgos abiertos de las QA r01 de T-144 (`.docs/tickets/T-144/qa.md`) y de T-147 (`.docs/tickets/T-147/qa.md`) y responder a su observación O-01 (¿se encarga al Bloque B con G3 BLOQUEADO?) antes del modo sombra.

## Alcance

- Entra: T-144 H-01 (media) y H-02 (baja); T-147 H-01, H-02 y H-03 (bajas); la pregunta O-01 de la QA de T-147.
- No entra: los límites de R8 ya declarados en INC-T123-01 (la «@» codificada, `Authorization: Basic`, un `token:` de solo letras); el cálculo de la amplitud con copias (T-144 H-05, del operador); `consumo.py`, `orquestacion.py`, `agentes.py`, `llm.py`, `estimar_coste_ciclo_a.py` y las pruebas de T-145, T-146 y T-148 (otra ronda); el Bloque B.

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| T-144 H-01: copias en rejillas que no son potencias de 10 o con un precio suelto sin redondear | `_paso_de_precio`: después de la mayor potencia de 10, la mayor rejilla de `REJILLAS_PRECIO` más gruesa en la que está la serie (2·10⁻ᵈ, 5·10⁻ᵈ, 25·10⁻ᵈ y 1/2ᵏ hasta 1/256); una serie está en una rejilla si lo está el 90 % de sus precios; el de cada precio es el mayor del de su serie y el de su década (`_paso_por_decada`, cifras significativas). Lo que no se cierra, declarado en INC-T127-01 «Ronda T-149» |
| T-144 H-02: Q08, Q09 y Q10 viven | Pruebas en el borde de la cota (`tests/test_t144.py`) |
| T-147 H-01: el detalle de dos errores copia el dato | `ErrorCadenaB` limpia su detalle (`sin_datos_protegidos`): cada dato que R8 reconoce, sustituido; si queda alguno, el detalle entero cambia por un aviso. Los mensajes de `jsonschema`, antes de recortarlos. `cadena_a_b.py`, lo que imprime |
| T-147 H-02: dos trazas en la descarga del BCE | Repetidas sobre la fecha convertida; destino comprobado antes de descargar; `OSError` al escribir: mensaje y 1 |
| T-147 H-03: Q02, Q03, Q05 y Q07 viven | Pruebas en `tests/test_t147.py` (los ficheros que fija el script del revisor) |
| O-01: encargos con G3 BLOQUEADO | El diseño lo prohíbe (7.3: «BLOQUEADO impide la entrega»; el Broker recibe el paquete en CT-02, que exige G3 favorable): `construir_peticion` falla cerrado con `ENTREGA_BLOQUEADA_G3` y `cadena_a_b.py` no envía nada sin entrega (`sin_envio`, código 1) |

- Contratos y esquemas: no cambian (goldens coinciden). Código de error nuevo: `ENTREGA_BLOQUEADA_G3`.
- Estado persistido: no cambia.
- Números: `REJILLAS_PRECIO` de `motor/frontera_b.py` (múltiplos 25, 5, 2; denominador 256; 90 %), `[PROPUESTO]` con su motivo en el código y en la incidencia; los estados G3 son los de CT-02 y del esquema (una prueba lo comprueba).
- Falla cerrado: un paso más grueso solo agrupa más (la amplitud no se sirve); sin entrega no hay encargo; un detalle que no se puede limpiar se omite.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Rejillas más gruesas agrupan series distintas | Amplitud no servida en índices de verdad | Medido con 300 semillas (`medir_copias.py`): índices y rentabilidad total, 0 salvo con un paso del 1 % del precio (límite declarado) |
| El coste de `_paso_de_precio` crece | Índices grandes más lentos | Filas candidatas solo donde la potencia llega; n = 2000, T = 2520: ~6 s (cota de la prueba, 60 s) |
| El texto de los mutantes del revisor cambia | Su script no corre | Las líneas que mutan se conservan tal cual |

## Criterios de aceptación (binarios)

1. CA-1 (T-144 H-01): `.docs/tickets/T-144/revisores/r01_01_copias_otras_rejillas.py` con 0 hallazgos (las seis vías A agrupadas y sin amplitud; B, 0 de 100); 0 falsos positivos en `test_h01_series_distintas_*` de T-144 y T-149; límites que quedan, declarados.
2. CA-2 (T-144 H-02): Q08, Q09 y Q10 muertos con `r01_03_mutantes_qa.py --ticket T-144`.
3. CA-3 (T-147 H-01): `T-147/revisores/r01_01_r8_y_peticion.py` con 0 hallazgos (C2 a C5 en verde) y `cadena_a_b.py` sin el dato en `resumen.json` ni en lo que imprime.
4. CA-4 (T-147 H-02): `T-147/revisores/r01_02_bce_y_clases.py` con 0 hallazgos; fecha repetida sin ceros y destino fichero: código 1, mensaje, sin traza y sin escribir.
5. CA-5 (T-147 H-03): Q02, Q03, Q05 y Q07 muertos con `r01_03_mutantes_qa.py --ticket T-147`.
6. CA-6 (O-01): con G3 BLOQUEADO o sin `estado_g3` favorable no sale ninguna petición (librería y script), y con APTO o APTO_CON_ADVERTENCIAS sí.
7. CA-7: mutantes de `.docs/tickets/T-147/mutantes.py` muertos; suite completa de A en verde; ruff ≤ 2838, mypy A ≤ 109; `refs_vivas`, `secrets_scan`, `nfc_check`, `corpus_integridad` (695) en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t149.py::test_h01_*` (rejillas, paso, fracción, década, falsos positivos, límites declarados) | nominal, límite, regresión | CA-1 |
| `test_t144.py::test_t149_*` (borde de la cota) | límite, regresión de mutantes | CA-2 |
| `test_t149.py::test_h01_*` de la cadena B (campos, tipos, configuración, símbolo, script) | fallo cerrado, regresión | CA-3 |
| `test_t149.py::test_h02_*` (BCE) | fallo cerrado, regresión | CA-4 |
| `test_t147.py::test_t149_*` | límite, regresión de mutantes | CA-5 |
| `test_t149.py::test_g3_*` | fallo cerrado, integración (script con `_cli` simulado) | CA-6 |
| revisores, mutantes, suite completa, gates | regresión | CA-7 |

## Scripts

`.docs/tickets/T-149/medir_copias.py` (falsos positivos y copias de la regla de niveles; `--modulo` mide otra versión de `frontera_b.py`); los del revisor de T-144, T-147, T-142 y T-141; `.docs/tickets/T-147/mutantes.py`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · claude · plan, implementación y pruebas en la copia `t149` (commit local)
- 2026-11-15 · EN QA · claude · pendiente de QA por un agente que no implementó
