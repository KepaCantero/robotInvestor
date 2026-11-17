# T-190 · Bloque A: hallazgos bajos de la QA r01 de T-152 (umbral por arriba, trazas de cadena_a_b, referencias y erratas)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (sin QA, por orden del operador) |
| Pieza | bloque_a (11_Ejecutor: `tests/test_t150.py`; en `bloque_a/motor/frontera_b.py`, solo un comentario); `.docs/scripts/cadena_a_b.py`; `docs/incidencias.md` (INC-T127-01 e INC-T142-01, rondas T-190); textos de `.docs/tickets/T-152/` |
| Planifica · implementa · QA | claude · claude · **sin QA** (orden del operador: los bajos no pasan por QA) |
| Aprobación del operador | 2026-11-16: «Haz T-190 también y el resto de hallazgos que pudieran salir. Si son bajos no los pases por QA. Corrígelos tú.» |
| Deuda técnica | T-190 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar H-01 a H-03 de la QA r01 de T-152 (`.docs/tickets/T-152/qa.md`, veredicto APTO).

## Alcance

- Entra:
  - H-01: el umbral del desplazamiento se fija también por arriba; U2 deja de ser equivalente y se corrigen los textos que lo afirmaban.
  - H-02: las cuatro trazas de `cadena_a_b.py`.
  - H-03: la referencia a un commit que no está en ninguna rama, y las erratas.
  - De las observaciones: O-01, el primer tramo de la prueba del borde, que tiene un precio con q/p del 2 % exacto; y O-02, el límite de los pasos grandes, que depende del par.
- No entra:
  - cambiar el umbral (decidido por el operador);
  - O-03, un falso positivo de una semilla dentro del límite declarado;
  - O-04: el detalle de `ENTRADA_B_INVALIDA` copia el valor ya limpio de R8, y viene de T-149;
  - los otros bloques, el marco común, la Constitución y el corpus.

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| H-01 | `test_t190_h01_el_umbral_tambien_se_fija_por_arriba` usa semillas del revisor. En [0,48, 0,9], la copia truncada se agrupa con el 2 % y no con el 2,1 % o más. En [0,4905, 0,9] pasa al revés. Mutantes U2 (4 %), U5 (2,1 %) y U6 (`<` estricto) en `T-152/mutantes.py`. Los textos de T-152 que daban U2 por equivalente quedan con una nota de corrección. El límite nuevo, que una serie que cruza el 2 % se desplaza a medias, va a INC-T127-01 |
| H-02 | `cadena_a_b.py`. Un JSON o un YAML anidados sin fin (`RecursionError`) se tratan como ficheros que no se leen. `_escribir` escribe en un temporal y lo mueve al final. `_json` usa los escapes de JSON si el texto no se codifica en UTF-8, tanto al escribir como al imprimir. Una petición que no cabe en un nombre de fichero queda en `no_enviadas` (o en la sonda) como `PETICION_NO_ESCRITA`, sin la ruta |
| H-03 | `pruebas.md` de T-152 cita `32af7fe`. Se corrigen las dos frases de la primera versión en `analisis-tecnico.md`, el número de pruebas (24, en el análisis y en el diario) y el comentario de T-150 en `frontera_b.py` |

- Contratos, esquemas y estado: no cambian. Código nuevo: `PETICION_NO_ESCRITA`, un motivo de `no_enviadas` del resumen del script, no de la librería.
- Números: ninguno nuevo.
- Falla cerrado: lo que no se lee o no se escribe no se envía. El límite nuevo de H-01 **no** falla cerrado: una copia sin agrupar cuenta como serie distinta. Queda declarado.

## Criterios de aceptación (binarios)

1. CA-1 (H-01): U2, U5 y U6 muertos. Ningún texto de T-152 afirma la equivalencia sin la nota.
2. CA-2 (H-02): las cuatro formas del revisor (`T-152/revisores/r01_03_formas_qa.py`) terminan sin traza, y las pruebas nuevas fallan con el `cadena_a_b.py` de antes.
3. CA-3 (H-03): ninguna referencia a `4e39324` fuera del `qa.md` del revisor, y las erratas corregidas.
4. CA-4: `T-190/mutantes.py` sin vivos. `T-152/mutantes.py`, `mutantes_heredados.py` y `T-149/revisores/r01_02_mutantes_qa.py`, como antes (solo vive X02, el casi equivalente conocido). Gate en verde.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · EN CURSO · claude · implementación y pruebas (sin QA, por orden del operador)
- 2026-11-16 · CERRADO · claude · sin QA por orden del operador (hallazgos bajos); ningún hallazgo nuevo
