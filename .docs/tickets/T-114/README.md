# T-114 · Fase 3 del Bloque A: goldens de los contratos CT

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor, solo pruebas) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (o Astra, si el operador se lo asigna) |
| Aprobación del operador | aprobada el 2026-11-13: «planifica y ejecuta la fase 3» |
| Deuda técnica | T-114 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Congelar los formatos de los contratos CT-01 a CT-25 del Bloque A en ficheros esperados (goldens) que la suite compara byte a byte, para que un cambio de formato haga saltar una prueba. Es la Fase 3 del plan de fases de `CLAUDE.md` y sigue el prompt `prompts/FASE3_GOLDENS_CONTRATOS.md`.

Precisión de la ronda r02 (QA r01, H-01): «un cambio de formato» es un cambio en lo que los goldens ven, que está escrito en «Qué ve cada golden» de `bloque_a/11_Ejecutor/tests/goldens/README.md`. Lo que no ven está en «Límites» del mismo fichero y de `analisis-tecnico.md`.

## Alcance

- Entra:
  - los goldens del Bloque A, en `bloque_a/11_Ejecutor/tests/goldens/`;
  - el generador y comprobador `bloque_a/11_Ejecutor/tests/goldens_ct.py`;
  - las pruebas `bloque_a/11_Ejecutor/tests/test_fase3_goldens.py`;
  - los esquemas JSON derivados solo del Anexo B, con su ejemplo, para los contratos que tienen campos en el Anexo B (CT-01 a CT-15, CT-22 y CT-23 a CT-25; CT-22 desde la r02, H-02);
  - desde la r02 (H-01): una batería fija de mensajes válidos e inválidos por contrato, con lo que la mensajería hace con cada uno, y las formas de once flujos simulados, con claves anidadas y tipos;
  - el registro de las diferencias entre el Anexo B y el ejecutor (INC-T114-01).
- No entra:
  - cambiar código de producción (`bloque_a/11_Ejecutor/bloque_a/`): si el ejecutor y el Anexo B no coinciden, se congela la diferencia y se registra; no se corrige en silencio (regla 7);
  - tocar el corpus congelado (Documento 0, `06_Plantillas_entregables`): los esquemas derivados viven con las pruebas, no en la entrega;
  - el Bloque A Forex (regla 8): su réplica es T-115;
  - los campos de CT-16 a CT-21: el Anexo B los remite a los prompts de sistema, que son datos de ejecución (regla 1). De ellos se congela el canal, el sobre común y, de los que el ejecutor emite, la forma. De CT-22 el Anexo B solo nombra `tipo` (r02, H-02).

## Diseño

Siete goldens (seis en la primera entrega; `aceptaciones_rechazos.json` es de la r02), todos JSON con claves ordenadas, sangría de un espacio, UTF-8 sin escapes y salto de línea final. La prueba vuelve a generar cada uno y compara el texto exacto.

| Golden | Qué congela | De dónde sale |
| --- | --- | --- |
| `tablas_contratos.json` | `VERSION_CONTRATO`, `ESTADOS`, `CAMPO_ESTADO`, `ESTADOS_ESPECIFICOS`, `CANALES`, `CANALES_V6`, `CAMPOS_MINIMOS`, `CAMPOS_RETORNO` | generado de `contratos.py` |
| `esquemas_respuestas.json` | los esquemas de `ESQUEMAS` (respuestas de los agentes) | generado de `contratos.py` |
| `mensajes_ejemplo.json` | el mensaje completo que `Mensajeria.crear` construye con cada ejemplo del Anexo B (reloj fijo, identificadores deterministas), o la clase del rechazo si el ejecutor no lo admite | generado con el ejecutor |
| `aceptaciones_rechazos.json` (r02) | qué hace `Mensajeria.crear` o `validar` con cada caso de la batería: el mensaje normalizado, o la clase y el motivo del rechazo | generado con el ejecutor |
| `formas_flujos_mock.json` (en la primera entrega, `formas_ciclo_mock.json`, con un solo ciclo y claves de primer nivel) | por flujo simulado, contrato y tipo de mensaje: emisores, receptores, la ruta de cada clave con su tipo JSON y las combinaciones de claves opcionales | generado con el ejecutor y `MockClient` |
| `divergencias_anexo_b.json` | lo que el Anexo B pide y el ejecutor no exige, lo que el ejecutor exige y el Anexo B no nombra, los mensajes de los flujos simulados que no cumplen el esquema derivado y los valores que el Anexo B nombra para un campo y el ejecutor emite en otro | calculado de los esquemas derivados y del ejecutor |
| `huellas.json` | SHA-256 del Documento 0, de los dos esquemas publicados, y de los tres ficheros escritos a mano | calculado |

Tres ficheros escritos a mano (no se generan; los protege `huellas.json`):

- `bateria_mensajes.json` (r02): los casos de la batería. Cada uno parte de un ejemplo del Anexo B o de un cuerpo propio, dice qué cambia y qué se espera de él (ADMITIDO o RECHAZADO).
- `anexo_b_esquemas.json`: un esquema JSON (Draft 2020-12) por contrato y sentido (`CT-NN.ENCARGO`, `CT-NN.RETORNO`), derivado **solo** del Anexo B. Cada uno lleva `"$comment": "derivado del Anexo B del Documento 0 V5.1"`. Reglas de derivación: son obligatorios los campos que el Anexo B nombra sin marcarlos como opcionales o condicionales; las listas cerradas del Anexo B (`A|B|C`) son `enum`; `additionalProperties` queda abierto, porque el §6.2.3 dice que los campos son el mínimo común y el esquema del operador puede ampliarlos. No se añade ningún tipo, patrón ni límite que el Anexo B no diga.
- `anexo_b_ejemplos.json`: un ejemplo por esquema. Donde el Anexo B trae un bloque JSON, es ese bloque con sus marcadores («…», `A|B|C`) sustituidos por un valor válido; donde solo trae la lista de campos, el ejemplo mínimo.

Además, `README.md` (la regla de re-congelado) y `REGISTRO.md` (una línea por re-congelado: fecha, ficheros y motivo) en la carpeta de goldens.

- Contratos CT-G afectados y versión de esquema: ninguno cambia. `VERSION_CONTRATO` sigue en 5.1.
- Estado persistido: no cambia.
- Números y su origen: no hay números nuevos. La fecha del reloj de las pruebas es la `AS_OF` de `conftest.py`.
- Cómo falla cerrado: sin golden, con un golden de más o con una diferencia de un solo byte, la prueba falla y dice qué fichero y qué clave. `goldens_ct.py --update` sin `--motivo` termina con error y no escribe nada. El generador nunca escribe durante las pruebas.
- Decisiones del operador: INC-T114-01. Donde el Anexo B y el ejecutor difieren, el golden congela lo que hay hoy en los dos lados y la lista de diferencias. Decidido el 13-11-2026: manda el código; el Anexo B se corrige en la próxima entrega del Documento 0. INC-T114-02 sigue `[PROPUESTO]`.

Regla de re-congelado (va en el `README.md` de los goldens): solo deliberado, con `python tests/goldens_ct.py --update --motivo "…"`, en el mismo commit que el cambio que lo causa y con el motivo también en el mensaje del commit. Igual que el corpus (`tools/corpus_integridad.py --update`).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| El ciclo simulado no es determinista entre ejecuciones o entre máquinas | Prueba inestable | Se congelan conjuntos ordenados de claves, no el orden ni los valores; se comprueba generando dos veces en la misma sesión (CA-8). Medido el 13-11: dos ciclos, 71 mensajes cada uno, formas idénticas |
| Un golden que no protege (se compara consigo mismo) | Falsa seguridad | Pruebas de mutación dentro de la suite: se cambia un campo del golden y otro del código, y la comparación debe fallar (CA-2) |
| Derivar del Anexo B más de lo que dice | Un esquema inventado pasa por norma | Reglas de derivación escritas arriba; el revisor de QA las contrasta contrato a contrato |
| El golden se regenera por costumbre | Deja de avisar | `--update` exige motivo, deja línea en `REGISTRO.md` y la regla va en el README |
| La suite del Bloque A se alarga | Gate más lento | Un solo ciclo simulado (unos 15 s), compartido por las pruebas del módulo. Desde la r02 son once flujos (unos 25 s de procesador por captura): el módulo los captura una vez, los comparte, y los vuelve a capturar una sola vez para CA-8 |

## Criterios de aceptación (binarios)

1. CA-1: existen los seis goldens y los dos ficheros escritos a mano, y `pytest tests/test_fase3_goldens.py` pasa comparando el texto exacto de cada golden con lo que genera el código.
2. CA-2: al cambiar un campo de cualquiera de los seis goldens, o un campo de `CANALES`, `CAMPOS_MINIMOS`, `CAMPOS_RETORNO` o `ESQUEMAS` en el código, la comparación falla y nombra el fichero; al deshacerlo, pasa.
3. CA-3: `tablas_contratos.json` contiene los 25 contratos, CT-01 a CT-25, y coincide con el §6.1 del Documento 0 en que no falta ni sobra ninguno.
4. CA-4: hay esquema derivado para cada contrato con campos en el Anexo B (CT-01 a CT-15, CT-22 y CT-23 a CT-25, en los sentidos que el Anexo B describe); cada uno es un esquema válido, lleva la marca «derivado del Anexo B» y su ejemplo lo cumple. CT-16 a CT-21 figuran en una lista explícita «sin campos en el Anexo B». (Corregido en la r02, H-02: la primera redacción ponía también CT-22 en esa lista, y el Anexo B nombra su campo `tipo`.)
5. CA-5: el ejemplo publicado del paquete de oportunidades cumple su esquema publicado. El del informe de seguimiento de opción lo cumple **salvo por la clave `x_aviso_ejemplo`**, que su esquema no admite (INC-T114-02, `[PROPUESTO]`): la prueba fija que ese es su único incumplimiento y que sin esa clave lo cumple. (Reescrito en la r02, H-04: la primera redacción decía «los dos ejemplos cumplen sus esquemas», y eso no es cierto ni se puede arreglar sin tocar la entrega, que es corpus congelado.)
6. CA-6: `goldens_ct.py --update` sin `--motivo` termina con error y no cambia ningún fichero; con motivo, regenera y añade una línea a `REGISTRO.md`. Sin opciones, comprueba y termina con código distinto de cero si algo difiere.
7. CA-7: las diferencias entre el Anexo B y el ejecutor están en `divergencias_anexo_b.json`, en INC-T114-01 de `docs/incidencias.md` y en la deuda técnica; una diferencia nueva hace fallar la suite. Incluye la de `tipo` de CT-22, que el ejecutor emite en `tipo_aviso` (r02, H-02).
8. CA-8: generar los goldens dos veces seguidas da el mismo texto.
9. CA-9: `git diff` no muestra ningún cambio en `bloque_a/11_Ejecutor/bloque_a/`, en `bloque_a/01_Gobernanza/` ni en `bloque_a/06_Plantillas_entregables/`.
10. CA-10: `./tools/check_all.sh` 12/12; las cuotas de ruff y mypy no suben; las pruebas recogidas del Bloque A no bajan.
11. CA-11 (r02, H-01): los mutantes del revisor de la r01 (`revisores/r01_01_mutantes_contratos.py` y `r01_03_mutantes_emision.py`) hacen fallar `python tests/goldens_ct.py`, o están declarados uno a uno, con su motivo, en «Límites» del README de los goldens y de `analisis-tecnico.md`.

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| Cada golden generado es igual, byte a byte, al fichero | nominal | CA-1 |
| No hay ficheros de más ni de menos en la carpeta de goldens | fallo cerrado | CA-1 |
| Mutar un valor de cada golden hace fallar la comparación | fallo cerrado | CA-2 |
| Mutar `CANALES`, `CAMPOS_MINIMOS`, `CAMPOS_RETORNO` y `ESQUEMAS` (con `monkeypatch`) cambia lo generado | fallo cerrado | CA-2 |
| Los 25 contratos y solo ellos; coinciden con la tabla del §6.1 | nominal | CA-3 |
| Cada esquema derivado es válido y lleva la marca; su ejemplo lo cumple; un ejemplo sin un campo obligatorio no lo cumple | nominal y límite | CA-4 |
| Lista de contratos sin campos en el Anexo B = CT-16 a CT-21; CT-22 solo con `tipo` | nominal | CA-4 |
| Cada campo de cada esquema está en el párrafo del Anexo B de su contrato (r02, H-06) | regresión | CA-4 |
| `contenido` de CT-23 solo en ENTRANTE (r02, H-05) | límite | CA-4 |
| La batería: cada caso da lo que espera; los 22 cambios de regla de `contratos.py` cambian su resultado (r02, H-01) | fallo cerrado y regresión | CA-11 |
| Los 14 cambios de formato en lo emitido cambian las formas (r02, H-01) | regresión | CA-11 |
| La diferencia de `tipo` de CT-22 está en el golden y desaparece si el ejecutor lo emitiera en `tipo` (r02, H-02) | regresión | CA-7 |
| Ejemplos publicados frente a esquemas publicados | regresión | CA-5 |
| `--update` sin motivo falla y no escribe; con motivo escribe y registra (en una copia temporal) | fallo cerrado | CA-6 |
| Una divergencia añadida al cálculo no coincide con el golden | fallo cerrado | CA-7 |
| Dos generaciones seguidas, mismo texto | regresión | CA-8 |
| Mutación a mano de un golden y del código, con la salida en `pruebas.md` | integración | CA-2 |
| Gate completo | integración | CA-9, CA-10 |

## Scripts

- Crea `bloque_a/11_Ejecutor/tests/goldens_ct.py` (comprobar y re-congelar). Se apunta en la tabla de `.docs/README.md`.
- Usa `.docs/scripts/commit_limpio.sh` para el commit.

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · PLANIFICADO · claude · plan escrito por orden del operador («planifica y ejecuta la fase 3»); se trabaja en una copia aparte mientras corre la QA r02 de T-112
- 2026-11-13 · EN CURSO · claude · implementado en la copia aparte: 51 pruebas del módulo en verde, mutación a mano comprobada, gates ligeros en verde; faltan la suite completa del Bloque A y el gate 12/12, que esperan a que termine la QA r02 de T-112 (una cosa cada vez)
- 2026-11-13 · EN CURSO · claude · decisiones del operador: en INC-T114-01 manda el código del Bloque A (el Documento 0 se escribió antes de construirlo y se modificará); T-115 (Forex) aplazada, no se hace sin orden
- 2026-11-13 · EN QA · claude · informe de pruebas escrito; pendiente la QA
- 2026-11-14 · NO APTO · revisor (QA r01) · dos hallazgos altos: H-01 (20 cambios de formato a la vez no hacen fallar ningún golden: las reglas de valor de la mensajería y los cuerpos que el ciclo semanal no emite quedaban sin congelar) y H-02 (falta la diferencia de `tipo` de CT-22 entre el Anexo B y el ejecutor); H-03 media (deuda sin actualizar) y H-04 a H-06 bajas. Detalle en `qa.md`
- 2026-11-14 · EN QA · claude · ronda r02: batería de aceptaciones y rechazos (golden nuevo), once flujos simulados con rutas anidadas y tipos, CT-22 con su campo del Anexo B y su diferencia medida, `contenido` de CT-23 con condición, prueba «nada inventado» por párrafo, CA-5 reescrito. Detalle en «Ronda r02» de `analisis-tecnico.md`. H-03 (deuda) lo actualiza quien coordina; pendientes el gate 12/12 y la QA r02
- 2026-11-14 · EN QA · claude · al integrar la r02 con la r02 de T-117 se re-congela `formas_flujos_mock.json` (línea del 14-11 en `REGISTRO.md`): en el ciclo V6 simulado dos Analistas dejan de emitir CT-08; no cambia ningún formato
