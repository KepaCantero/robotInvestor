# T-66 · Aplicar las propuestas de T-53 al Bloque A y darlo por terminado

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a |
| Planifica · implementa · QA | claude · claude (orquestación) y un segundo agente (evaluación) · un revisor nuevo sin contexto |
| Aprobación del operador | Aprobada el 2026-11-10: «Quiero que apliques todas las propuestas que consideres oportunas ahora mismo y demos por finalizado el bloque A». Los valores que decide el operador van como `[PROPUESTO]` hasta T-57 |
| Deuda técnica | T-66 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Aplicar al ejecutor del Bloque A las propuestas de la revisión T-53 (`.docs/tickets/T-53/propuestas.md`) que se pueden programar y probar ya, sin otro proveedor de IA, sin K y sin llamadas reales a la API. Las demás quedan con su motivo y su destino. Con eso, el Bloque A se da por terminado en su fase de diseño y revisión, y queda listo para conectarse en la Fase 1.

## Alcance

**Entra** (por área de archivos, sin solapes):

| Propuesta | Qué se hace | Quién · archivos |
| --- | --- | --- |
| PA-01 | Perfiles activos por configuración (`perfiles.activos`, `[PROPUESTO]`: solo `DIV`). F10 P-02 nace de ahí. Un tipo no activo que se pide devuelve `NO_ESTIMABLE` y se declara | claude · `orquestacion.py`, YAML, `tests/conftest.py` |
| H-06 (T-65) | Si no queda ningún tipo que analizar (pausados o no activos), el run se cierra sin redactar, PARCIAL y con sus limitaciones | claude · `orquestacion.py` |
| PA-05 (técnica) | El Contradictor (AG-11) recibe la afirmación verificable y la evidencia, sin la tesis, el mecanismo, el pre-mortem ni las dimensiones. Una objeción fuerte solo queda resuelta si la respuesta del Analista cita evidencia verificable **y** el Contradictor lo confirma en una contrarréplica (prompt de Contrarias, §5). El veredicto lo calcula una regla y tiene efecto: «refutada» no es elegible; «frágil» pasa a confianza `especulativo` y relevancia ALTA | claude · `orquestacion.py`, `sintesis.py`, `contratos.py`, `mock_respuestas.py` |
| PA-09 | `backtest.anonimizar: auto` (sí con un modelo real, no con el simulado). Todo PRG de backtest hecho con un modelo real antes de su fecha de corte lleva `contaminacion_posible: true` | claude marca (`orquestacion.py`, `llm.py`) · el segundo agente lo excluye (`evaluador.py`) |
| PA-10 | `aprendizaje.solo_endurecer: true` (`[PROPUESTO]`). Siguen siendo automáticos degradar H5, revocar certificados y endurecer. Emitir un certificado (habilita probabilidades numéricas) queda como `PROPUESTO` hasta que el operador lo aprueba por CT-04 (`aprobar_certificados`). La recalibración de pesos nunca pasa sola a producción | segundo agente (`evaluador.py`) · claude (CT-04 en `orquestacion.py`) |
| PA-03 (parte) | Muestra efectiva: los certificados usan `n_eff` con un efecto de diseño por conglomerados de fecha y un bootstrap por fechas, no la n nominal | segundo agente (`motor/evaluacion.py`, `evaluador.py`) |
| PA-14 | Ablación determinista en cada ciclo: top-3 sin las objeciones de AG-11 y top-3 de una referencia simple (señal compuesta). Se registra cuántos puestos cambia cada variante (F5 y registro del run) | claude · `orquestacion.py` |
| PA-21 | El Analista puede dar su propia probabilidad por horizonte (`probabilidades_propias`, opcional). Se guarda en F4 (`prob_analista`) y el Evaluador mide su Brier frente al de Prospectiva | claude (esquema y F4) · segundo agente (métrica) |

**No entra, y por qué:**

| Propuesta | Motivo | Destino |
| --- | --- | --- |
| PA-02 | Es la conexión de A con el resto y exige una enmienda (contrato de encargo a A) | Al conectar A en la Fase 1 |
| PA-03 (torneo) | Las preguntas fijas por par y la atribución por agente viven en SC-4 | Con SC-4 (PA-15) |
| PA-04 | Depende de K y de las 6 fichas FX (T-54) | T-54 |
| PA-05 (otro proveedor) | Proveedor, clave y coste son del operador | T-57 |
| PA-06 y PA-07 | Retirar agentes y recortar prompts exige validar cada recorte como aspirante frente al titular con llamadas reales, y cambia el corpus congelado | Ticket propio antes del modo sombra con API |
| PA-08 | Hacen falta los precios reales por modelo y el tope en euros del operador | Antes del modo sombra con API; tope en T-57 |
| PA-11 y PA-12 | Columnas del Anexo A, traslado a SC-1 y referencia con datos de €STR (K) | T-57 y K |
| PA-13, PA-15 a PA-20 | Fase 1 avanzada o Fase 2 (N, SC-3, SC-4, auditor de otro proveedor, radar, lotes, compartir entre copias) | Su fase |

## Diseño

- **Contratos:** cambian los esquemas internos de A, sin versión global:
  - `FINALISTA` gana `probabilidades_propias` (opcional);
  - `RESPUESTA_OBJECIONES` gana `evidencia_citada` (opcional);
  - aparece la fase `CONTRARREPLICA` de AG-11;
  - CT-04 admite `aprobar_certificados`.

  No cambia ningún CT-G.
- **Estado persistido:**
  - F4 gana `contaminacion_posible` y `prob_analista` (campos nuevos y opcionales; lo antiguo sigue siendo válido).
  - F6 admite `CERT` con estado `PROPUESTO` y la entrada `CERT_APROBACION`.
  - Sin migración: los registros antiguos no tienen los campos, y se leen como `false` y `null`.
- **Números nuevos** (todos en `config/por_defecto.yaml`, con su pregunta para T-57):
  - `perfiles.activos`: [DIV] (PA-01). Pregunta: «¿En qué tipos de inversión busco?»
  - `aprendizaje.solo_endurecer`: true (PA-10). Pregunta: «¿Ajustes automáticos solo prudentes?»
  - `llm.fecha_corte_conocimiento` (PA-09). Es técnico y se revisa al cambiar de modelo.
  - Los umbrales del veredicto de Contrarias (PA-05).
- **Cómo falla cerrado:**
  - Sin contrarréplica, la objeción fuerte sigue abierta.
  - Un certificado sin aprobar no habilita probabilidades.
  - Ante la duda sobre la contaminación, se marca.
  - Un tipo no activo no se analiza: se declara.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Las pruebas existentes cuentan con los 12 tipos activos | Fallan por el valor por defecto nuevo | La configuración de pruebas activa los 12 tipos; hay pruebas propias para el valor por defecto |
| El simulado de AG-11 decidía con las dimensiones del Analista | Cambian las objeciones del simulado | El simulado decide con la evidencia recibida; se revisan las pruebas que dependan de ello |
| `n_eff` deja sin certificado casos que antes lo tenían | Pruebas de certificados en rojo | Datos de prueba con fechas independientes; es el comportamiento correcto |
| Dos agentes en paralelo | Conflictos al juntar | Archivos repartidos sin solapes; el YAML, por secciones distintas |

## Criterios de aceptación (binarios)

1. CA-1: cada propuesta aplicada tiene al menos una prueba que falla sin ella.
2. CA-2: las suites y el gate completo quedan en verde, y la línea base de A sube.
3. CA-3: cada propuesta no aplicada tiene su motivo y su destino en este README y en la deuda técnica.
4. CA-4: el Documento 0 no se toca. Los cambios de comportamiento quedan en el README del ejecutor y en `docs/incidencias.md` (INC-T66-xx).

## Plan de pruebas

`tests/test_t66_propuestas.py` (claude) y `tests/test_t66_evaluacion.py` (segundo agente): una prueba nominal y una de fallo cerrado por propuesta, más las regresiones de lo que cambie.

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN CURSO · plan escrito; reparto de archivos entre claude y un segundo agente
- 2026-11-10 · EN QA · implementado y juntado (claude + segundo agente); A con 172 pruebas; gate 12/12
