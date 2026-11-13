# T-93 · Bloque A: hallazgos H-32 a H-39 de la QA r04 de T-92

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO, 12-11-2026) |
| Pieza | `bloque_a/11_Ejecutor` (un solo bloque) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (regla del operador del 12-11-2026) |
| Aprobación del operador | Toca código de un bloque: autorizado el 2026-11-12 («haz todo», tras proponer que Claude lo implementara y Astra hiciera la QA). Era la tarea C-32 de la cola de Astra; pasa a ser su QA |
| Deuda técnica | T-93 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los hallazgos medios y bajos que dejó la QA r04 de T-92 (`.docs/tickets/T-92/qa.md`, «Ronda r04»), sobre todo los dos que la QA pedía antes del modo sombra con API: una clave «sk-» que se colaba en la cinta grabada detrás de ciertos escapes (H-32) y un almacén anterior a los sellos que se corrompía con la última línea cortada (H-34).

## Alcance

- Entra:
  - **H-32** (media): R8 ve la clave detrás de `\uXXXX`, `\b`, `\f`, `\"`, `\\`, `\xNN` y `%XX`, y `contenido_sensible` recorre los conjuntos;
  - **H-33** (media): las URL de prensa financiera en minúsculas, los códigos de cotización, las fechas de 8 cifras válidas, las siglas largas y el CamelCase no son claves;
  - **H-34** (media): en un almacén anterior a los sellos, la última línea cortada se aparta;
  - **H-35** (baja): un corte a mitad de un carácter UTF-8 se aparta como cualquier otro;
  - **H-36** (baja): declarar en «Límites» las colas que no se detectan;
  - **H-37** (baja): un plazo de CT-23 numérico o booleano se rechaza, y un `date` vence al terminar su día;
  - **H-38** (baja): un plazo guardado por la versión anterior que ya no se lee no bloquea `vencer()`: la consulta vence con una incidencia;
  - **H-39** (baja): el recuento que faltaba en `pruebas.md` de T-92 y la prueba de regresión de la medianoche inexistente.
- No entra: prompts, papeles de los agentes o cualquier cosa que dependa del rediseño de A (pregunta 2 de su propuesta); el Bloque B y la interfaz de encargos.

## Diseño

- Contratos: ninguno cambia. Estado persistido: ninguno cambia de forma (el almacén lee igual lo que ya había).
- Números: ninguno nuevo de configuración; los patrones de texto son reglas de forma, como los de T-92.
- Fallo cerrado: un registro sellado truncado sigue siendo un fallo de integridad; solo se aparta la última línea **sin sello**. Un plazo que no se lee vence (el análisis sigue con el supuesto declarado), como pedía la QA, en lugar de parar el ciclo.

## Criterios de aceptación (binarios)

1. CA-1: los tres scripts de la QA r04 (`.docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py`, `.docs/tickets/T-92/revisores/r04_02_almacen_corte.py` y `.docs/tickets/T-92/revisores/r04_03_plazos_iso.py`) dan 0 fallos.
2. CA-2: la detección de claves reales no baja: todos los formatos de `r04_01` caso 1 iguales que en la r04 (los residuos de H-36, también).
3. CA-3: las 37 pruebas nuevas de `tests/test_t93_hallazgos.py` pasan, y la mayoría fallan con el código anterior.
4. CA-4: la suite de A pasa entera (476) y el gate da 12/12, con ruff y mypy de A por debajo de su cuota.
5. CA-5: no cambia ningún fichero fuera de `bloque_a/11_Ejecutor`, salvo la documentación, las cuotas y la cola.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `r04_01`, `r04_02` y `r04_03` contra el código nuevo | Regresión de la QA | CA-1 y CA-2 |
| `tests/test_t93_hallazgos.py` | Nominal, límites y fallo cerrado | CA-3 |
| Las pruebas nuevas contra HEAD sin el cambio | Regresión | CA-3 |
| Suite de A y gate | Regresión | CA-4 |

## Registro

- 2026-11-12 · EN QA · H-32 a H-39 corregidos; 37 pruebas nuevas (A 476)
- 2026-11-12 · CERRADO · QA r01 APTO (revisor nuevo sin contexto): CA-1 a CA-5 cumplidos (CA-2 con reservas), sin críticos ni altos. H-40 (media, regresión de R8 con escapes dobles) y H-41 a H-46 (bajos) pasan a T-103
