# T-206 · QA

## Ronda r01 · 2026-11-25 · revisor independiente (claude, sin el contexto de la implementación)

**Veredicto: APTO pendiente de la ronda de cierre.** Los seis hallazgos son bajos. Ninguno deja una INC- con un tipo fuera del esquema en un camino real del ejecutor, pero ninguno se puede dejar abierto (regla del operador). La ronda de cierre la verifica este revisor, con los scripts de `revisores/`.

**Qué se revisó.** El commit `d633efee` (rama `wip/t206`), un solo commit sobre `d11662ff` (`git merge-base wip/t206 origin/develop`). El trabajo se hizo en copias propias (`git worktree --detach`), sin tocar la copia del implementador. No hay caso del plan de pruebas: es deuda técnica sin PB.

### 1. Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t206_tipo_incidencia.py` | 35 superadas |
| Los ocho ficheros de pruebas que cambian y diecisiete vecinos (almacén, F9, broker, cola, carga, cuotas, mapa, integración; 25 ficheros) | 646 superadas, 0 fallos |
| Las pruebas nuevas sobre el código de `d11662ff` (los cuatro módulos de develop y, para que importe, los nombres nuevos con el comportamiento de develop) | 24 fallan y 11 pasan. Las 11 que pasan comprueban lo que ya era cierto: los 7 tipos se escriben, el enumerado frente al esquema, el sitio único, el lector y la deduplicación de F9 con un HA antiguo. Coincide con `pruebas.md` (25/10); la diferencia es que en esta sustitución el enumerado está en `almacen.py` |
| Los ocho ficheros de pruebas antiguos que cambian, sobre el código de develop con la misma sustitución | 207 superadas: el lector acepta las INC- de antes, así que siguen valiendo para un almacén antiguo |
| `mutantes.py` del implementador | 19 muertos, M4 vivo (declarado equivalente: no lo es, ver H-02) |
| Equivalencia con develop (`.docs/tickets/T-201/equivalencia.sh <copia> d11662ff`, sobre la base nueva) | 89 ficheros por lado, ninguno distinto tras normalizar, EQUIVALENTE, testigo sin puntos ciegos |
| ruff (medida del gate) | 2735, con cuota 2735. Los doce ficheros `.py` que cambian tienen los mismos hallazgos que en la base (0, 0, 2, 7 y 0 en los de pruebas) |
| mypy de A (medida del gate) | 67, con cuota 67 (las 6 de `orquestacion.py` son de antes) |
| corpus-integridad, nombres-nfc, secrets, refs-vivas | OK |
| Gate completo del implementador (`gate_t206.log`) | 12/12, pero sobre el árbol de antes del rebase (ruff 2797 con cuota 2797): ver H-01 |
| Fusión con T-205 (`wip/t205`: `seguimiento.py`, `test_t205_clase_seguimiento.py`, `test_t201_cuotas.py`) | El código fusiona sin conflicto; `test_t205`, `test_t206` y `test_t201_cuotas`: 101 superadas. T-205 escribe sus INC- con OTRO y `campo_afectado`, compatible con el enumerado. Solo chocan los añadidos al final de `docs/incidencias.md`, de la deuda y del diario (texto, se resuelve juntando las dos entradas) |
| Fusión con el PR 3 de Astra (`astra/encargos-bloque-a-c38-c47`, `2d99af69`) | El código fusiona sin conflicto (`orquestacion.py`, `interfaz_broker.py`); su única incidencia nueva es HERRAMIENTA. `test_t206` sobre el árbol fusionado: 35 superadas. Los conflictos de documentos (`cola_astra.md`, evidencias, incidencias, deuda) ya los tiene el PR 3 con develop sin T-206 |

### 2. Criterios de aceptación

| Criterio | Estado | Evidencia |
| --- | --- | --- |
| CA-1 enumerado = 4.8, un solo módulo, todas las llamadas con un tipo del enumerado | Cumple | `test_ca1_*`; búsqueda propia de todas las llamadas y de toda escritura de `tipo_entrada` INC del paquete (solo `almacen.py`) |
| CA-2 un tipo de fuera falla cerrado sin escribir nada | Cumple salvo un objeto hostil | `test_ca2_*`; `revisores/r01_01_ataques.py` §1 (NaN, infinito, bytes, dict, bool, ancho completo, cero ancho: rechazados). Una subclase de `str` con `==` permisivo pasa y escribe DATOS (H-02) |
| CA-3 los ocho caminos: OTRO con `categoria` DATOS; conservan objeto, severidad, tratamiento y marcas | Cumple el tipo y, por el diff, la conservación; la conservación no está probada | `test_ca3_*`; diez mutantes propios vivos (H-05) |
| CA-4 HA antiguo: se abre, el lector reconoce las antiguas y las nuevas «y solo esas», deduplicación de F9, `estado` | Cumple salvo «solo esas» | `test_ca4_*`; `r01_01` §4 (HA antiguo abierto, ampliado y reabierto íntegro; reescribir a mano el tipo de una antigua se detecta). El lector toma por de datos una SEGURIDAD con `categoria` DATOS (H-03) |
| CA-5 ciclo mock por defecto, equivalencia, suite, cuotas, gate 12/12 | Cumple salvo el gate sobre el commit final | `test_ca5_*`; `revisores/r01_03_ciclo_mock.sh` (CLI, configuración por defecto, cierre negativo en EURUSD=X y HA con DATOS antiguas: OK); equivalencia propia; cuotas propias; gate de antes del rebase (H-01) |

### 3. Preguntas del encargo

- **¿Admite el esquema de HA el campo `categoria`?** Sí. El esquema (`Historial de auditorías (esquema V2.0).md`) es una tabla en Markdown, no un esquema cerrado: no dice en ningún sitio que no se admitan otros campos, y las INC- del ejecutor ya llevan campos que 4.8 no nombra (`detalle`, `run_id`, `fue_no_atendible`, `leccion_id`, `fragmento`; T-205 añade `fase`, `opp_id`, `f3_seq_clase`). No hay un esquema JSON de HA en el corpus ni en `06_Plantillas_entregables`. La regla 4 (el campo y el tipo, nunca el valor) se cumple: `categoria` lleva la categoría. No es hallazgo.
- **¿Se debilita alguna de las pruebas antiguas?** No en lo que importa. `tipo == "DATOS"` pasa a `es_incidencia_de_datos`, que acepta las dos formas, así que esas pruebas ya no distinguen DATOS de OTRO + `categoria`. Eso lo cubren ahora las ocho `test_ca3_*`, que exigen OTRO y `categoria` DATOS camino a camino, y el fallo cerrado, que hace caer cualquier vuelta a DATOS (M12 a M19 muertos). Las negativas (`test_r02_h12_referencia_sana_no_cambia_nada`) quedan más estrictas. El número de pruebas no cambia. El lector es algo más ancho de lo declarado (H-03), y eso sí afecta a lo que aceptan.
- **¿Las INC- con DATOS de almacenes existentes se abren y se sellan bien?** Sí: `test_ca4_*` y `r01_01` §4 (abrir, verificar, añadir una nueva, reabrir; y la manipulación del tipo de una antigua rompe la cadena). El ciclo mock por la CLI sobre un almacén con dos antiguas termina y deja el almacén íntegro (`r01_03`).
- **¿Algún informe contaba por tipo DATOS?** No. Ningún módulo del paquete, ni `.docs/scripts/`, `tools/` o `dashboard/`, filtra o cuenta INC- por `tipo`. Los lectores van por marcas (`leccion_id`, `peticion_huerfana`, `reserva_huerfana`, `fue_no_atendible`, `escalado_operador`). Lo único que cambia es la etiqueta en `estado`: las escaladas nuevas de datos salen como OTRO y la vista no enseña `categoria`, así que el operador ya no ve que son de datos (H-06). No cambia ninguna cifra. A-Forex y B no escriben DATOS.
- **¿Choca con T-205 o con el PR 3?** En el código, no (ver la tabla de arriba). Solo hay conflictos de texto en los ficheros que todos amplían al final.
- **El límite declarado (`Almacen.escribir`).** Es hallazgo (H-04): el ejecutor no tiene hoy ningún camino así, pero el invariante «toda INC- de HA lleva un tipo del esquema» depende de que nadie la monte a mano, y la prueba estática no lo vigila.
- **El gate de antes del rebase.** No basta (H-01). El rebase cambió la base (T-203: 39 ficheros, cuota de ruff 2797 → 2735) y después solo se repitieron 3 + 6 ficheros de pruebas: faltan dos de los ocho que cambian (`test_t65_hallazgos.py`, `test_t65_qa_r03.py`; en esta QA pasan), la suite completa de A, A-Forex y B y mypy de A-Forex y B sobre el commit final.

### 4. Invariantes

- Números: ninguno nuevo. Decisiones: INC-T206-01 `[PROPUESTO]` en `docs/incidencias.md` y citada en la fila T-206 de la deuda. Correcto.
- Corpus y esquemas congelados: intactos (corpus-integridad OK; el esquema de HA no se toca).
- R8 y regla 4 de HA: el error de `TipoIncidenciaNoAdmitido` cita el tipo (cortado a 40) y no el detalle (`test_ca2_el_rechazo_…`); `categoria` no lleva valores.
- G3-MET-13: no lo toca (ningún texto de madurez cambia).
- `mapa_plan_pruebas.json`: sin cambios, correcto (sin PB). `docs/evidencias_pruebas_bloque_a.md`: solo cambia el commit de la cabecera, que es el de antes del rebase (`358576c3`) y no la base del commit (`d11662ff`): va con H-01.
- Ciclo mock y backtest iguales a develop: sí, con la equivalencia propia sobre `d11662ff`.
- Concurrencia: no hay escritura nueva, y el rechazo va antes de `nuevo_id`. `r01_01` §5: cuatro procesos que alternan incidencias de datos con rechazos dejan 40 INC- con ids contiguos (`INC-2026-0001` a `0040`), ningún contador gastado y el almacén íntegro.

### 5. Mutantes propios (`revisores/r01_02_mutantes.py`)

Primero `test_t206`; si sobrevive, también los ocho ficheros que cambian y las vecinas del broker (`test_t174`, `test_t93`).

25 mutantes: **14 muertos, 1 equivalente y 10 vivos** (salida en `revisores/r01_02_mutantes.txt`).

| Mutante | Resultado |
| --- | --- |
| Q1 `_incidencia_interna` valida después de gastar el contador; Q2 el error es un `ValueError` genérico; Q4 la comprobación normaliza mayúsculas y espacios | muertos (etapa 1) |
| Q3 el mensaje repite el tipo | equivalente: `_comprobar_tipo_incidencia` no recibe el detalle; el mutante estaba mal planteado |
| Q5 sin `isinstance` (el M4 del implementador) | **vivo**: H-02 |
| Q6 severidad por omisión de `incidencia_de_datos` (la usan los dos caminos del broker) | **vivo**: H-05 |
| Q7 a Q10 (`incidencia_de_datos` pierde objeto, severidad pedida o marcas; otra `categoria`); Q11 y Q12 (el lector toma cualquier categoría o cualquier OTRO); Q13 (C2 sin alcance pierde `escalado_operador`) | muertos (etapa 1) |
| Q14 C2 sin alcance pierde su `tratamiento`; Q15 plazo ilegible cambia de `objeto` | **vivos**: H-05 |
| Q16, Q18, Q20, Q22 y Q24: cambia la severidad de la referencia inválida, de los datos inválidos de un símbolo, del CT-19 no atendido, de F9 sin fichas y de la fuente que ya no es de F9 | **vivos**: H-05 |
| Q21 el pronóstico no registrable pierde `run_id`; Q25 la fuente que ya no es de F9 pierde su `tratamiento` | **vivos**: H-05 |
| Q17, Q19 y Q23 (pierden `run_id` los datos inválidos, el CT-19 no atendido y F9 sin fichas) | muertos (etapa 2, por las pruebas antiguas) |

### 6. Hallazgos

#### H-01 · baja · El gate 12/12 no es del commit que se integra

- **Cómo se reproduce.** `gate_t206.log` mide ruff con cuota 2797, la de antes de T-203; el commit `d633efee` está sobre `d11662ff`, con cuota 2735. `pruebas.md` dice que tras el rebase solo se repitieron 63 + 150 pruebas.
- **Esperado.** CA-5: `./tools/check_all.sh` 12/12 sobre el commit que se integra. **Encontrado:** 12/12 sobre otro árbol.
- **Corrección.** Pasar `./tools/check_all.sh` completo sobre el commit final, ya rebasado sobre el develop en el que entra (después de T-205 si entra antes), guardar el log, citarlo en `pruebas.md` (cifras de ruff, mypy ×3 y pytest ×3) y regenerar `docs/evidencias_pruebas_bloque_a.md` sobre esa base, para que la cabecera cite la base real.
- **Prueba de regresión.** El propio log 12/12 del commit final.

#### H-02 · baja · El fallo cerrado se salta con una subclase de `str`, y M4 no es equivalente

- **Cómo se reproduce.** `revisores/r01_01_ataques.py` §1: `class T(str)` con `__eq__` que devuelve siempre True y valor `"DATOS"` pasa `isinstance(tipo, str)` y `tipo in TIPOS_INCIDENCIA`, y queda en HA una INC- con `tipo` DATOS. Con M4 (sin `isinstance`), un objeto cualquiera con `__eq__` permisivo también pasa y se escribe (comprobado: la INC- se escribe y el contador avanza). Ninguna prueba lo mata: M4 y el Q5 propio siguen vivos.
- **Esperado.** CA-2: cualquier tipo fuera del enumerado falla cerrado. **Encontrado:** pasa un valor hostil; `mutantes.py` declara M4 equivalente sin serlo.
- **Corrección.** En `_comprobar_tipo_incidencia`, `if type(tipo) is not str or tipo not in TIPOS_INCIDENCIA:` (el tipo exacto, no `isinstance`). Añadir al parametrizado de `test_ca2_un_tipo_fuera_del_esquema_falla_cerrado_sin_escribir_nada` los dos objetos (subclase de `str` permisiva con valor DATOS y objeto permisivo) y quitar M4 de `EQUIVALENTES` en `mutantes.py`.
- **Prueba de regresión.** Los dos casos nuevos; M4 muerto; `r01_01` §1 sin HALLAZGO.

#### H-03 · baja · `categoria` DATOS se admite con cualquier tipo y el lector la cuenta

- **Cómo se reproduce.** `r01_01` §2: `incidencia("SEGURIDAD", "…", "AG-18", categoria="DATOS")` se escribe, y `es_incidencia_de_datos` la da por incidencia de datos.
- **Esperado.** CA-4: el lector reconoce las antiguas (DATOS) y las nuevas (OTRO + `categoria` DATOS) «y solo esas»; la decisión de cómo se escribe una de datos está en un único sitio (`incidencia_de_datos`). **Encontrado:** una SEGURIDAD cuenta como de datos, y cualquier llamador puede marcar de datos otro tipo por `**extra`.
- **Corrección.** `es_incidencia_de_datos`: `tipo == CATEGORIA_DATOS or (tipo == TIPO_INCIDENCIA_DATOS and categoria == CATEGORIA_DATOS)`. En `incidencia`, antes de `nuevo_id`: si `extra` trae `categoria` y no es la pareja (`TIPO_INCIDENCIA_DATOS`, `CATEGORIA_DATOS`), `TipoIncidenciaNoAdmitido`, sin escribir nada.
- **Prueba de regresión.** En `test_ca4_el_lector_no_toma_otras_entradas_por_de_datos`, `{"tipo_entrada": "INC", "tipo": "SEGURIDAD", "categoria": "DATOS"}` → False; una prueba de fallo cerrado byte a byte para `incidencia("SEGURIDAD", …, categoria="DATOS")` y para `incidencia("OTRO", …, categoria="OTRA")`; `r01_01` §2 sin HALLAZGO.

#### H-04 · baja · `Almacen.escribir` admite una INC- con un tipo fuera del esquema (límite declarado)

- **Cómo se reproduce.** `r01_01` §3: `escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": …, "tipo": "DATOS", …})` se escribe. La prueba estática de CA-1 solo mira las llamadas a `incidencia` y `_incidencia_interna`.
- **Esperado.** Objetivo del ticket: toda INC- que escribe el ejecutor en HA lleva un tipo del esquema, con el fallo cerrado en el único punto por el que pasa toda escritura. **Encontrado:** el invariante depende de que nadie monte una INC- a mano.
- **Corrección.** En `Almacen._comprobar_reserva`, para `archivo == "HA"` y `tipo_entrada == "INC"`, devolver el motivo si el `tipo` no pasa la misma comprobación (con H-02 y H-03: tipo exacto `str` del enumerado, y `categoria` solo en la pareja OTRO/DATOS). `escribir` ya rechaza sin escribir nada (y para AG-18 en HA sin incidencia recursiva). Ajustar `test_t198_buscador_ct19.py::test_r02_h02_…`, que escribe una INC- sin tipo para probar el sellado, con un tipo del esquema (no cambia lo que prueba). Las INC- antiguas de las pruebas de CA-4 y de `r01_03` se montan como las dejaba el ejecutor anterior, sin pasar por la comprobación (por ejemplo, con un ayudante de prueba que desactive la comprobación con `monkeypatch` solo mientras monta el almacén antiguo).
- **Prueba de regresión.** `escribir` de una INC- con DATOS, sin tipo, con `None` y con otras mayúsculas: `EscrituraFueraDeReserva` y ficheros iguales byte a byte; las de CA-4 siguen pasando; `r01_01` §3 sin HALLAZGO.

#### H-05 · baja · CA-3 «conservan su objeto, severidad, tratamiento y marcas» no tiene prueba en casi ningún camino

- **Cómo se reproduce.** Diez mutantes propios vivos tras las dos etapas (tabla de arriba): la severidad de los siete caminos que la fijan o la heredan (Q6, Q16, Q18, Q20, Q22, Q24), el `tratamiento` de la revisión C2 sin alcance y de la fuente que ya no es de F9 (Q14, Q25), el `objeto` del plazo ilegible (Q15) y el `run_id` del pronóstico no registrable (Q21).
- **Esperado.** CA-3: los ocho caminos conservan su objeto, severidad, tratamiento y marcas. **Encontrado:** las `test_ca3_*` comprueban el tipo, la categoría y alguna marca, pero no esos campos, y las pruebas antiguas tampoco. Por qué es baja y no media: el código de los ocho sitios solo cambia el nombre de la función (comprobado con el diff: fuera del literal, ningún argumento cambia), así que hoy se conservan; lo que falta es la prueba que lo mantenga.
- **Corrección.** En cada `test_ca3_*`, comparar objeto, severidad, tratamiento y `run_id` (y `escalado_operador`, `fue_no_atendible` donde los lleva) con los valores de develop: broker C2 sin alcance (AG-01, Material, «revisar a mano el alcance de la revisión C2 de CNS-…», escalada); plazo ilegible (AG-01, Material, «registrada»); referencia inválida (la referencia, Operativa, «tipo de activo PARCIAL y declarado», run); datos inválidos (el símbolo, Operativa, «símbolo excluido y declarado como laguna del tipo», run); CT-19 no atendido (AG-16, Operativa, «registrada», run); pronóstico no registrable (el origen, Menor, «registrada», run); F9 sin fichas (AG-16, Operativa, «sin marca; reintento en el ciclo siguiente», run); fuente fuera de F9 (AG-16, Operativa, «declarada una vez; excluida de los CT-19 siguientes», run, marca). Añadir los diez mutantes a `mutantes.py`.
- **Prueba de regresión.** Los diez mutantes muertos con `test_t206` sola (`revisores/r01_02_mutantes.py`).

#### H-06 · baja · Documentación y vista `estado`: «DATOS» sin actualizar y la categoría no se ve

- **Cómo se reproduce.** `bloque_a/11_Ejecutor/README.md` (consultas al Broker, CT-23): «se da por vencida con una incidencia DATOS en HA»; `orquestacion.py`, comentario de la línea 405: «con incidencia DATOS». `Bloque.estado()["incidencias_escaladas"]` muestra `tipo` y no `categoria`: la escalada nueva de la revisión C2 sin alcance sale como OTRO, y el operador deja de ver que es un problema de datos (antes salía DATOS). INC-T206-01 dice que la categoría «se conserva», pero no en la vista del operador.
- **Esperado.** Documentación al día, y que lo que la decisión conserva llegue al operador. El motivo de no tocar el comentario (el rebase del PR 3) no se sostiene: el PR 3 no cambia esas líneas ni las de `estado` (sus trozos de `orquestacion.py` en la base son 366–371 y 2324–2338; el comentario está en la 401 y `estado` en la 2382).
- **Corrección.** README: «con una incidencia de datos en HA (OTRO con `categoria` DATOS; las de antes de T-206, DATOS)». Comentario de la 405: «con una incidencia de datos». En `estado`, añadir `categoria` a cada escalada solo cuando la INC- la lleva (las demás quedan igual y la secuencia mock no cambia).
- **Prueba de regresión.** `test_ca4_el_estado_del_operador_…` exige `categoria` DATOS en la nueva y ninguna `categoria` en la antigua; una prueba que lea el README y `orquestacion.py` y no encuentre «incidencia DATOS»; la equivalencia con develop sigue EQUIVALENTE.

### 7. Scripts de esta ronda (`revisores/`)

- `r01_01_ataques.py` (salida en `r01_01_ataques.txt`): tipos hostiles, lector, escritura genérica, HA antiguo y manipulado, cuatro procesos. Con `d633efee`: 4 HALLAZGO (H-02, H-03 ×2, H-04). Uso desde `bloque_a/11_Ejecutor`: `../../.venv/bin/python ../../.docs/tickets/T-206/revisores/r01_01_ataques.py`.
- `r01_02_mutantes.py` (salida en `r01_02_mutantes.txt`): 25 mutantes propios en dos etapas, en una copia desechable (`QA_DESDE=Qn` retoma). Uso: `../../.venv/bin/python ../../.docs/tickets/T-206/revisores/r01_02_mutantes.py .`.
- `r01_04_equivalencia.txt`: salida de la equivalencia con develop sobre `d11662ff`.
- `r01_03_ciclo_mock.sh <copia>` (salida en `r01_03_ciclo_mock.txt`): ciclo y `estado` por la CLI con la configuración por defecto, un cierre negativo y un HA con DATOS antiguas. Con `d633efee`: OK.

En la ronda de cierre: los tres scripts sin HALLAZGO ni mutante vivo no equivalente, `mutantes.py` del implementador sin vivos, la equivalencia con develop y el log del gate 12/12 del commit final.

## Ronda de cierre de la QA r01 · 2026-11-25 · revisor independiente (claude)

**Veredicto: APTO en el código, con un hallazgo bajo de texto abierto (H-07).** Los seis hallazgos de la r01 quedan corregidos y verificados con mis scripts. H-07 es una sola afirmación falsa en las evidencias del ticket. No toca código ni pruebas. Por la regla del operador (nada abierto), se corrige antes de integrar, y la verifico yo.

**Qué se revisó.** El commit `1544b0a3`, encima de `786ad26a` (el commit de la r01 rebasado sobre `6c8910c1`, develop con T-205). Lo comprobé con `git range-diff`: el rebase solo cambia el contexto de `docs/incidencias.md` y de la deuda. Lo revisé en mi worktree, con una copia desechable aparte para los mutantes.

### Comprobaciones

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t206_tipo_incidencia.py` | 52 superadas |
| Ocho ficheros que cambian y vecinas (`test_t174`, `test_t93`, `test_t205`, `test_t201_cuotas`, `test_t203_cuotas`, `test_fase4_mapa`, `test_t53`, `test_t178`, `test_t196`, `test_t200`, `test_unitarias`) | 514 superadas |
| `mutantes.py` del implementador | 41 de 41 muertos, M4 incluido (`revisores/rc_05_mutantes_impl.txt`) |
| `revisores/r01_01_ataques.py` | 0 HALLAZGO, 16 OK (`rc_01_ataques.txt`) |
| `revisores/r01_02_mutantes.py` | 24 muertos en la etapa 1 y Q3 vivo, que es el equivalente ya declarado (`rc_02_mutantes.txt`). Lo he repetido dos veces solo: vive. Ver H-07 |
| `revisores/r01_03_ciclo_mock.sh` | OK (`rc_03_ciclo_mock.txt`) |
| Equivalencia con develop (`equivalencia.sh <copia> 6c8910c1`) | 89 ficheros por lado, ninguno distinto tras normalizar, EQUIVALENTE, testigo sin puntos ciegos (`rc_04_equivalencia.txt`) |
| ruff, mypy de A, corpus, nfc, secrets, refs-vivas | 2735 (cuota 2735) y 67 (cuota 67); los demás OK |
| Gate `gate_t206_cierre.log` | 12/12, sobre `ea534285`, con 8629 pruebas de A, 68 de A-Forex y 176 de B. `ea534285` y `1544b0a3` tienen el mismo padre (`786ad26a`) y solo se diferencian en `pruebas.md`: el gate vale para el código final |

### Adaptaciones de mis scripts (`cierre_adaptacion_revisores.diff`)

He comprobado que el diff declarado es exactamente el diff real entre mi copia de la r01 y la del commit. Las tres adaptaciones mantienen lo que se quería comprobar:
- **`r01_01` §2.** Ahora da por bueno el rechazo, siempre que deje los ficheros iguales byte a byte. Es la corrección que pedía H-03. El lector se prueba con la entrada montada a mano, que es lo que había que comprobar.
- **`r01_01` §4 y `r01_03`.** La comprobación se desactiva solo mientras se monta el almacén antiguo, y se restaura en un `finally` (en `r01_03`, en un proceso aparte del ciclo). §3, que prueba que `escribir` rechaza, sigue corriendo sin el parche. `test_ca4_un_ha_antiguo_…` comprueba además que la comprobación vuelve a estar activa.
- **`r01_02`, Q4 y Q5.** Solo cambia el anclaje a `type(tipo) is not str`. Las mutaciones siguen siendo las mismas.

### Correcciones de la r01

| Hallazgo | Corrección | Verificación |
| --- | --- | --- |
| H-01 | Gate 12/12 sobre el código final. Evidencias regeneradas, con `786ad26a` en la cabecera, que es el padre del commit | Log leído; ver la fila del gate |
| H-02 | `type(tipo) is not str` y dos casos hostiles en el parametrizado de CA-2 | M4, M4b y Q5 muertos; `r01_01` §1 OK |
| H-03 | `categoria` solo en la pareja OTRO + DATOS. Se rechaza antes de pedir el id, también una subclase o `None`. El lector exige la pareja o la DATOS antigua | M21 a M26, Q11 y Q12 muertos; `r01_01` §2 OK |
| H-04 | `_comprobar_reserva` valida tipo y categoría de toda INC- de HA. En `test_t198` la INC- de sellado lleva OTRO, y sigue probando el sellado | M27 y M28 muertos; `r01_01` §3 OK. He revisado que ningún otro camino del paquete escribe una INC- con `escribir`, y que las INC- de T-205 (OTRO con `campo_afectado`) pasan (`test_t205` en verde) |
| H-05 | `_conserva` compara en las ocho `test_ca3_*` objeto, severidad, tratamiento, `run_id`, `escalado_operador` y `fue_no_atendible` con los valores de develop | Mis diez Q vivos, muertos en la etapa 1 |
| H-06 | README y comentario corregidos. `estado` añade `categoria` solo si la INC- la lleva. Una prueba busca «incidencia DATOS» en el README y en el código | M29 y M30 muertos. La equivalencia no cambia: en el camino normal ninguna escalada lleva categoría |

### H-07 · baja · Las evidencias de la ronda de cierre dicen que Q3 muere

- **Cómo se reproduce.** `pruebas.md` («Ronda de cierre»: «25 muertos en la etapa 1, 0 vivos (Q3 también muere)») y `evidencia_r01_02_cierre.txt` («Q3 … MUERTO (etapa 1)»). Con `1544b0a3`, Q3 vive en la etapa 1 en tres ejecuciones mías: la del script completo y dos de Q3 solo. Es lo esperable: `_comprobar_tipo_incidencia` no recibe el detalle, y el mutante solo repite el tipo en el mensaje, que todas las pruebas siguen aceptando. Es el equivalente declarado en la r01.
- **Esperado.** Evidencias honestas: Q3 vivo y equivalente. **Encontrado:** se da por muerto. Lo más probable es una muerte espuria de esa ejecución, por ejemplo dos ejecuciones de mutantes a la vez en la misma copia.
- **Corrección.** En `pruebas.md`, la fila de `r01_02`: «25 mutantes: 24 muertos en la etapa 1 y Q3 vivo (equivalente, declarado en el script), 0 vivos no equivalentes». Sustituir `evidencia_r01_02_cierre.txt` por una ejecución limpia, una sola a la vez en la copia, que dará la misma salida que `revisores/rc_02_mutantes.txt`. `analisis-tecnico.md` y `handoff.md` no la repiten.
- **Prueba de regresión.** La salida nueva de `r01_02_mutantes.py`, que tiene que coincidir con `rc_02_mutantes.txt`.

Con H-07 corregido, T-206 queda **APTO sin nada abierto**. No hace falta repetir el gate, porque es un cambio solo de texto.

## Verificación de H-07 · 2026-11-25 · revisor independiente (claude)

**Qué se revisó.** El commit `d426614e`, encima de `1544b0a3`. Solo cambia texto del ticket: no toca `bloque_a/`, `docs/`, `sistema_global/` ni `tools/`. El gate, los mutantes y la equivalencia de la ronda de cierre siguen valiendo.

- **`pruebas.md`.** La fila de `r01_02` dice ahora «24 muertos en la etapa 1 y Q3 vivo, equivalente; 0 vivos no equivalentes». Explica la muerte espuria y remite a `revisores/rc_02_mutantes.txt`. Es correcto.
- **`evidencia_r01_02_cierre.txt`.** Es idéntica, byte a byte, a `revisores/rc_02_mutantes.txt`. Es correcto.
- **`qa.md` y `revisores/rc_01` a `rc_05`.** Entran en el commit tal como los dejé.
- **Queda un resto de H-07 en `handoff.md`.** El traspaso de la ronda de cierre (línea 19, «Resultado») sigue diciendo «`r01_02`: 25 muertos».
- **Corrección de mi propio `qa.md`.** En la ronda de cierre escribí que `handoff.md` no repetía la afirmación. Me equivoqué: busqué «Q3» y la frase de `handoff.md` no lo nombra. Lo corrijo aquí.
- **Corrección pendiente.** En `handoff.md`, línea 19: «`r01_02`: 24 muertos y Q3 vivo, equivalente (0 vivos no equivalentes)». Es un cambio solo de texto y no hace falta repetir ninguna comprobación.

**Veredicto: APTO.** El código y las pruebas no tienen nada abierto. H-07 queda cerrado cuando se corrija esa línea de `handoff.md`. Con eso, T-206 queda APTO sin nada abierto, y lo puede confirmar el coordinador con un `grep "25 muertos" .docs/tickets/T-206/handoff.md` vacío.

**Cierre de H-07 (coordinador, 25-11-2026).** Corregida la línea 19 de `handoff.md` con el texto exacto del revisor; `grep "25 muertos" .docs/tickets/T-206/handoff.md` sale vacío, que es la condición que fijó el revisor. T-206 queda APTO sin nada abierto.
