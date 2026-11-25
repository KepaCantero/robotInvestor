# T-206 · Bloque A: el tipo DATOS de las incidencias de HA no está en el esquema

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (25-11-2026, QA r01 APTO y rondas de cierre verificadas, sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/almacen.py`; el literal del tipo en `interfaz_broker.py` (2), `orquestacion.py` (4) y `fiabilidad_f9.py` (2) |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | No hace falta: es deuda técnica sin decisión nueva. Lo que el esquema no fija lo decide el agente por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`), en INC-T206-01 `[PROPUESTO]` |
| Deuda técnica | T-206 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (origen: implementador de T-205, 25-11-2026) |

## Objetivo

Que toda incidencia (INC-) que escribe el ejecutor en HA tenga un `tipo` del esquema de HA V2.0. Hoy ocho sitios escriben DATOS, que el esquema no admite, y `Almacen.incidencia` admite cualquier tipo.

## Fuentes

- Esquema de HA V2.0 (`bloque_a/05_Archivos_operativos/Historial de auditorías (esquema V2.0).md`):
  - 4.8, la línea de INC-: `inc_id`, `tipo` (SEGURIDAD · MANIPULACION · CANAL_NO_PREVISTO · ACCESO_FUERA_DE_MATRIZ · HERRAMIENTA · ESCRITURA · OTRO), `severidad`, `objeto`, `campo_afectado` (sin el valor), `tratamiento` y `escalado_operador`;
  - 3.1, append-only;
  - 3.4, en una incidencia se registran el campo y el tipo, nunca el valor.
- Documento 0 V5.3, §17.5 («continuidad segura»: la herramienta caída es el ejemplo de modo degradado) y §17.4 (manipulación). No hay caso del plan de pruebas: es deuda técnica sin PB.

## Alcance

- **Entra:**
  - `almacen.TIPOS_INCIDENCIA`, el enumerado de 4.8 en un solo sitio, con la cita del esquema;
  - `Almacen.incidencia` y `_incidencia_interna` fallan cerrado con `TipoIncidenciaNoAdmitido` ante un tipo de fuera, antes de pedir el identificador;
  - `Almacen.incidencia_de_datos`, que escribe OTRO con `categoria` DATOS;
  - `almacen.es_incidencia_de_datos`, que reconoce las INC- de datos de antes y de después;
  - los ocho sitios pasan de `incidencia("DATOS", …` a `incidencia_de_datos(…`, que tiene la misma longitud, y sus argumentos no cambian;
  - las pruebas existentes que buscaban `tipo == "DATOS"` pasan a `es_incidencia_de_datos`.
- **No entra:**
  - `seguimiento.py`: lo cambia T-205, en `wip/t205`, y allí ya usa OTRO;
  - reescribir las entradas antiguas de HA, que es append-only;
  - ~~validar `Almacen.escribir` genérico~~: entra en la ronda de cierre de la QA r01 (H-04); ver `analisis-tecnico.md`, «Ronda de cierre».
  - tocar más de `orquestacion.py` e `interfaz_broker.py` que el literal. El PR 3 de Astra, ahora parado, también cambia esos ficheros, y así su rebase es fácil.

## Diseño

- **Contratos y esquemas:** ninguno cambia. HA es un esquema en Markdown y no hay un esquema JSON de HA en el corpus. Las pruebas hacen uno con los campos de 4.8 para validar con jsonschema.
- **Estado persistido:** HA sigue igual, append-only. Las INC- nuevas de datos llevan `tipo` OTRO y `categoria` DATOS. Las antiguas no se tocan.
- **Números:** ninguno.
- **Cómo falla cerrado:** con un tipo que no está en la tupla (texto con otro valor, otras mayúsculas, espacios o un valor que no es texto), se lanza `TipoIncidenciaNoAdmitido` (subclase de `ValueError`) antes de `nuevo_id`. No se escribe la entrada, ni el contador de INC-, ni el sello. El mensaje del error cita el tipo y no el detalle. Si `incidencia_de_datos` recibe otra `categoria`, lanza `TypeError` sin escribir.
- **Decisiones `[PROPUESTO]` (INC-T206-01):**
  - OTRO, y no HERRAMIENTA, en los ocho sitios;
  - el campo `categoria` en vez de `campo_afectado` o del `detalle`;
  - el lector que admite las dos formas.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Un llamador que no se ha visto usa otro tipo y ahora falla | El ciclo cae donde antes escribía un tipo inválido | Una prueba lee el paquete entero (AST) y comprueba cada `incidencia(…)` y `_incidencia_interna(…)`; hoy usan CANAL_NO_PREVISTO, HERRAMIENTA, MANIPULACION, OTRO, SEGURIDAD, ACCESO_FUERA_DE_MATRIZ y ESCRITURA |
| Un lector que filtra por `tipo == "DATOS"` deja de ver las nuevas | Se pierde una deduplicación | No hay ninguno en el ejecutor. `fiabilidad_f9.no_atendibles` lee la marca `fue_no_atendible` sin mirar el tipo. Pruebas con un HA antiguo |
| Rebase del PR 3 de Astra y de T-205 | Conflictos | Cambio de un token por línea, con la misma longitud, sin tocar `seguimiento.py` |

## Criterios de aceptación (binarios)

1. **CA-1:**
   - el enumerado del código es el de 4.8 del esquema de HA, en el mismo orden;
   - está escrito en un solo módulo (`almacen.py`);
   - cada llamada del paquete a `incidencia` o a `_incidencia_interna` usa un tipo del enumerado y ninguna escribe DATOS.
2. **CA-2:**
   - un tipo fuera del enumerado (DATOS, vacío, None, otras mayúsculas, espacios, un número, una lista o una tupla) hace fallar cerrado `incidencia` y `_incidencia_interna` con un error propio;
   - no se escribe nada: los ficheros del almacén quedan iguales byte a byte y el contador de INC- no se gasta;
   - cada tipo del enumerado se escribe.
3. **CA-3:** los ocho caminos (dos de `interfaz_broker.py`, cuatro de `orquestacion.py` y dos de `fiabilidad_f9.py`) escriben una sola INC- con `tipo` OTRO y `categoria` DATOS, conforme al esquema JSON de la INC-. Conservan su objeto, severidad, tratamiento y marcas (`fue_no_atendible`, `escalado_operador`, `run_id`).
4. **CA-4:** con un HA antiguo con INC- de `tipo` DATOS:
   - el almacén se abre íntegro;
   - `es_incidencia_de_datos` reconoce las antiguas y las nuevas, y solo esas;
   - la deduplicación de `fiabilidad_f9` sigue excluyendo la FUE- marcada antes de T-206;
   - `estado` muestra las escaladas antiguas y las nuevas.
5. **CA-5 (regresión):**
   - un ciclo mock con la configuración por defecto y un dato inválido solo deja tipos del esquema;
   - la secuencia mock de T-201 (backtest del README, ciclo, petición, consulta, seguimiento, evaluar y estado) da lo mismo que en develop byte a byte;
   - la suite de A pasa sin fallos y con 607 pruebas o más;
   - ruff ≤ 2797 y mypy de A ≤ 67;
   - `./tools/check_all.sh` da 12/12.

## Plan de pruebas

| Prueba (`tests/test_t206_tipo_incidencia.py`) | Tipo | Criterio |
| --- | --- | --- |
| `test_ca1_…` (enumerado frente al esquema, un solo sitio, lectura estática de las llamadas) | nominal, regresión | CA-1 |
| `test_ca2_un_tipo_fuera_del_esquema_falla_cerrado_sin_escribir_nada` (10 casos), `…_el_rechazo_es_un_error_propio…`, `…_cada_tipo_del_esquema_se_escribe` (7), `…_la_de_datos_no_admite_otra_categoria` | fallo cerrado, límite | CA-2 |
| `test_ca3_…` (los ocho caminos, por separado) | nominal | CA-3 |
| `test_ca4_…` (HA antiguo, lector, deduplicación de F9, `estado`) | migración, compatibilidad | CA-4 |
| `test_ca5_ciclo_mock_por_defecto_…`, equivalencia de T-201, suite de A, gate | regresión, integración | CA-5 |
| Pruebas existentes que miraban DATOS (8 ficheros) | regresión | CA-3, CA-4 |
| Mutantes propios (`mutantes.py`) | robustez de las pruebas | todos |

No hay escritura nueva que pueda competir con otra. La comprobación del tipo no tiene estado y va antes de `nuevo_id` y de `escribir`, que no cambian. Por eso no hace falta una prueba de concurrencia nueva. Las de `escribir` siguen en la suite.

## Scripts

- `.docs/tickets/T-201/equivalencia.sh` (reutilizado, sin cambios);
- `.docs/scripts/evidencias_plan_a.py --ejecutar`;
- `.docs/tickets/T-206/mutantes.py` (nuevo).

## Registro

- 2026-11-25 · ABIERTO · claude · encargo con el defecto que encontró el implementador de T-205
- 2026-11-25 · PLANIFICADO · claude · fuentes: esquema de HA 4.8 y Documento 0 §17. Búsqueda de llamadores y lectores
- 2026-11-25 · EN CURSO · claude · `almacen.py`, los ocho literales y las pruebas que miraban DATOS
- 2026-11-25 · EN QA (r01) · claude · 35 pruebas nuevas; 20 mutantes (19 muertos y 1 equivalente); equivalencia con develop; commit local
- 2026-11-25 · EN CURSO (cierre) · claude · QA r01 APTO pendiente de la ronda de cierre (H-01 a H-06, bajos): rebase sobre `6c8910c1` (T-205); los seis corregidos con su prueba
- 2026-11-25 · EN QA (ronda de cierre de la QA r01) · claude · 52 casos en `test_t206`; 41 mutantes propios muertos, sin equivalentes; los tres scripts del revisor sin HALLAZGO ni vivos; gate 12/12 sobre el commit final; commit local «T-206 cierre: …»
- 2026-11-25 · rondas de cierre verificadas (H-01 a H-07) · APTO sin nada abierto (`qa.md`).
- 2026-11-25 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
