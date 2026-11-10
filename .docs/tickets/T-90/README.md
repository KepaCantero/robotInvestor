# T-90 · Bloque B: declarar la nota excluida por fechas posteriores al corte (H-01 de la QA de T-64)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO, 10-11-2026) |
| Pieza | bloque_b |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | No necesaria: corrección técnica de robustez y trazabilidad. El operador pidió el 2026-11-10 «sigue con el resto de la deuda que no dependa de mí» |
| Deuda técnica | T-90 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

La QA de T-64 (H-01, baja) vio que una nota de un especialista con fechas de fuente posteriores al corte se excluía con `continue`: no dejaba limitación ni incidencia, y la afirmación desaparecía del informe sin rastro. Debe excluirse, porque en backtest sería una fuga, pero declarándolo, con el especialista y la dimensión.

## Alcance

- **Entra:** `bloque_b/11_Ejecutor/bloque_b/orquestacion.py`, en el bucle de notas del informe dimensional, y una prueba nueva.
- **No entra:** el resto del Bloque B, que espera su revisión con el operador (T-68).

## Diseño

La nota se sigue excluyendo. Ahora, además, se añade a `estados_degradados` del paquete la entrada «Dn: nota de AG-… excluida por fechas de fuente posteriores al corte o incoherentes (fuga de información)». Ese apartado ya llega al paquete y al informe técnico («Estados degradados»).
- **Contratos y estado:** no cambian. La entrada nueva es una cadena más de una lista que ya existe.
- **Números:** ninguno.
- **Cómo falla cerrado:** la nota no entra ni en el expediente (F2) ni en el informe, y queda declarada.

## Criterios de aceptación (binarios)

1. CA-1: con una nota de fechas posteriores al corte, la nota no está en F2 ni en el paquete, y `estados_degradados` del paquete la declara.
2. CA-2: la prueba falla con el código anterior y la suite de B y el gate pasan.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t90_nota_fuera_de_corte.py::test_nota_posterior_al_corte_se_excluye_y_se_declara` | regresión | CA-1, CA-2 |

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · corrección y prueba (falla con HEAD: `estados_degradados` vacío)
- 2026-11-10 · CERRADO · QA r01 APTO. Al cerrar se corrigen H-01 (motivo propio para las fechas incompletas o ilegibles, que ya no se rotulan como fuga) y H-02 (cuántas notas se excluyeron por dimensión y especialista), con una prueba nueva, y H-03 (documentación). La suite de B queda en 176
- 2026-11-10 · CERRADO · después de cerrar: la corrección de H-01 añadió un error de mypy en B (160, frente a una cuota de 159), visto al pasar el gate de T-83. Se tipa `f_` y la cuenta vuelve a 159
