# T-103 · Bloque A: regresión de R8 con escapes dobles (H-40) y bajos H-41 a H-46 de la QA r01 de T-93

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r02) |
| Pieza | `bloque_a/11_Ejecutor` (un solo bloque) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (regla del operador del 12-11-2026) |
| Aprobación del operador | 2026-11-12: el orden de tareas obligatorias para evaluar el Bloque A por separado («Cómo quedaría entonces las tareas obligatorias para implementar el bloque A?»); la QA r01 de T-93 pedía H-40 antes del modo sombra con API |
| Deuda técnica | T-103 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (H-40 a H-46 de T-93) |

## Objetivo

Corregir la regresión de seguridad que dejó T-93 en R8 (una clave detrás de un escape doble ya no se veía, H-40) y los bajos H-41 a H-46 de la misma QA, antes del modo sombra con API.

## Alcance

- Entra:
  - **H-40** (media): `RE_ESCAPES` toma el tramo de barras entero y añade los escapes largos de `ascii()`, los octales, `%uXXXX` y los `%25…` de una URL codificada dos veces;
  - **H-41** (baja): una cola de cuatro o más tramos de solo cifras cuenta como clave; lo que sigue sin verse se declara;
  - **H-42** (baja): si el último registro de un archivo del almacén no acaba en «\n», `escribir` lo antepone;
  - **H-43** (baja): un CNS sin `plazo_respuesta` vence con una incidencia DATOS, como H-38;
  - **H-44** (baja): `contiene_credenciales` recorre `frozenset`;
  - **H-45** (baja): se declaran los falsos positivos con cifra y unidad;
  - **H-46** (baja): documentos (`Reloj`, «Límites» y las reglas de plazo de CT-23 en el README del ejecutor).
- No entra: ampliar `RE_TRAMO_TEXTO` para H-45 (cada ampliación quita recall, como mostró H-41); prompts y papeles; Bloque B.

## Diseño

- Contratos: ninguno cambia. Estado persistido: no cambia de forma; el almacén lee igual lo que ya había y solo añade el salto de línea que faltaba antes del registro nuevo.
- Números: «cuatro o más tramos» de H-41 es una regla de forma de R8, como las de `RE_TRAMO_TEXTO` (no es un parámetro de negocio del Anexo A).
- Cómo falla cerrado: R8 sigue detectando de más antes que de menos (un falso positivo deja el resultado PARCIAL con incidencia); una consulta que no se puede leer vence con su supuesto declarado y una incidencia.

## Criterios de aceptación (binarios)

1. CA-1: los casos 1, 1b, 2 (los cuatro enumerados) y 3 de `r01_01_r8_escapes.py` se detectan, y el script da 0 fallos.
2. CA-2: los casos 1 y 2 de `r01_02_almacen_legado.py` y el 3b de `r01_03_plazos_tipos.py` pasan (0 fallos en ambos scripts).
3. CA-3: `r04_01_r8_regla_texto.py` de T-92 sigue con 0 fallos (recall de los formatos de proveedor y 0 de 12 textos de H-33).
4. CA-4: las pruebas nuevas fallan sin la corrección y pasan con ella.
5. CA-5: el gate da 12/12, A ≥ 607 más las nuevas, sin subir cuotas.

### Ronda r02 (QA r01 NO APTO)

6. CA-6 (H-47): R8 es lineal: `contenido_sensible` y `contiene_credenciales` con 100.000 barras tardan menos de 2 s entre los dos, y `r01_02_r8_rendimiento.py` da 0 fallos.
7. CA-7 (H-48): un registro con U+2028, U+2029 o U+0085 se vuelve a leer en el almacén, la cinta y la caché de resultados; `r01_03_almacen_cortes.py` da 0 fallos.
8. CA-8 (H-49, H-50): la prueba de `frozenset` falla sin él, y tres tramos de cifras de 20 caracteres o más son clave.
9. CA-9 (H-50 a H-52): lo que sigue sin verse y los falsos positivos nuevos están en «Límites».

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t103_r8_y_bajos.py` | Regresión | CA-1, CA-2, CA-4 |
| Scripts del revisor de T-93 (`r01_01`, `r01_02`, `r01_03`) y `r04_01` de T-92 | Regresión | CA-1 a CA-3 |
| `./tools/check_all.sh` | Gate | CA-5 |

## Registro

- 2026-11-12 · ABIERTO · creado con nuevo_ticket.sh, tras la QA r01 APTO de T-93
- 2026-11-12 · EN QA · H-40 a H-46 corregidos o declarados; 23 pruebas nuevas
- 2026-11-12 · NO APTO · QA r01 (revisor nuevo sin contexto): H-48 alto (el almacén no vuelve a abrir con U+2028), H-47 medio (R8 cuadrático con muchas barras), H-49 a H-52 bajos
- 2026-11-12 · EN QA · Ronda r02: H-47 a H-50 corregidos, H-50 a H-52 declarados; 8 pruebas nuevas
