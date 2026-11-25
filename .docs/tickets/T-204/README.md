# T-204 · Eliminar el Bloque A Forex del repositorio

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (25-11-2026, QA r03 APTO y dos rondas de cierre verificadas, sin hallazgos abiertos) |
| Pieza | Repositorio: gate y herramientas (`tools/`), scripts de `.docs/scripts/` y documentos vivos. Ningún código de A ni de B |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | 25-11-2026: «olvídate del bloque A forex. Elimínalo». Ampliada ese día: «Elimina el bloque A Forex definitivamente» y «Haz esas tres cosas. Te doy mi consentimiento» (Constitución, `.docs/` e historial de git; el historial lo limpia él después de integrar) |
| Deuda técnica | T-204 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (sigue al último paso pendiente de T-54) |

## Objetivo

Quitar del repositorio `bloque_a_forex/` y todo lo que depende de él, sin romper nada más, y que no pueda volver al gate sin que una prueba falle.

## Alcance

- **Entra:**
  - el borrado de `bloque_a_forex/` (317 archivos);
  - el gate: `tools/check_all.sh` (mypy y pytest del Forex fuera; quedan 10 comprobaciones), `tools/cuotas.txt` (fuera `mypy_bloque_a_forex` y `pytest_bloque_a_forex`; ruff 2806 → 1604), `tools/corpus_integridad.py` y el manifiesto re-congelado (705 → 525 archivos), `tools/refs_vivas.py` (bloque retirado) y `tools/requisitos_entorno.txt`;
  - los scripts: `.docs/scripts/preparar_entorno.sh` y `.docs/scripts/qa_rama.sh`;
  - la prueba nueva `.docs/scripts/pruebas_gate_bloques.py`, más casos en `prueba_refs_vivas.py`;
  - los documentos vivos:
    - `CLAUDE.md`, `prompts/`, `docs/AVANCE.md`, `docs/incidencias.md` (INC-002 fuera) y la skill `ri-probar`;
    - el prompt del panel (`dashboard/prompts/01_DASHBOARD_V1.md`) y `.secrets.baseline`;
    - en `sistema_global/` (la Constitución, aparte, con la enmienda 6): el README, el briefing, las decisiones del Bloque A, la deuda (T-115 fuera; T-54, T-96, T-103, T-105, T-120 y T-199 reescritas) y el Documento 0 V0.75;
  - en `.docs/`, notas en `.docs/README.md` y en `.docs/knowledge/01_que-es-el-robot-investor.md`, y una entrada de memoria nueva.
- **No entra:**
  - el código, las pruebas, la configuración y el corpus de `bloque_a/` y `bloque_b/`. B no tiene nada del Forex (INC-T204-04);
  - `sistema_global/marco_comun_c/`, que no cita el bloque, solo divisas (`fx`);
  - `99_Historico*`;
  - el historial de git, que lo hace el operador;
  - la rama `wip/t202`, que se ajustará al integrar.
- **Ampliación del operador, aplicada el 25-11-2026 por orden suya («Todo»), en la r02b de la coordinación:**
  - la Constitución: la «enmienda 6» la lleva a la V0.7 (INC-T204-01). El parche está en `enmienda4_constitucion.patch`, lo genera `generar_enmienda.py`, y es la 6 porque la 4 y la 5 son propuestas pendientes;
  - la limpieza de `.docs/` con `limpiar_docs.py --aplicar`: 107 líneas en 80 ficheros (INC-T204-03). En la r03 se devolvieron a su texto cuatro líneas de evidencia (H-11).

  En la r01, el sistema de permisos de la sesión de Claude bloqueó las dos escrituras, y Claude no lo sorteó. Las preparó para que se aplicaran después.

## Inventario y clasificación

Leyenda: (a) se borra · (b) se reescribe · (c) histórica, se marca sin borrar · (d) no se toca.

| Sitio | Qué cita | Clase |
| --- | --- | --- |
| `bloque_a_forex/` | El bloque entero (317 archivos) | (a) |
| `tools/check_all.sh` | `EJECUTORES`, `PAQUETES`, YAML, mypy, pytest y la cabecera | (b) |
| `tools/cuotas.txt` | `mypy_bloque_a_forex=174`, `pytest_bloque_a_forex=68` (fuera); ruff (recalculada) | (a)/(b) |
| `tools/corpus_manifest.txt` | 180 huellas del Forex (re-congelado) | (a) |
| `tools/corpus_integridad.py`, `tools/refs_vivas.py`, `tools/requisitos_entorno.txt` | El Forex como raíz o bloque, y el comentario de arch | (b) |
| `.docs/scripts/preparar_entorno.sh`, `.docs/scripts/qa_rama.sh` | El ejecutor y el paquete del Forex | (b) |
| `.secrets.baseline` | Dos ficheros del Forex | (a) |
| `CLAUDE.md` | Tabla, línea base, trampa INC-002, flujo, plan de fases, gate, comandos | (b) |
| `AGENTS.md` | Nada (no nombra bloques, líneas base ni «12/12») | (d) |
| `prompts/` (00, README, FASE0, 1, 3, 4, 6, VERIF_F6), `dashboard/prompts/01_DASHBOARD_V1.md` | El Forex como bloque; «12/12», «tres suites» | (b) |
| `.agents/skills/ri-probar/SKILL.md` | «A-Forex ≥ 68» | (b) |
| `docs/AVANCE.md` | Fila del monorepo (03-11) y frase de T-115 | (c) (marca T-204) y (b); fila nueva de T-204 |
| `docs/incidencias.md` | INC-002 (solo Forex) y su mención en INC-001 | (a) |
| `sistema_global/constitucion/` | Cinco menciones (cuatro del A Forex; P-10 solo de B Forex) | (b) con la enmienda 6 (V0.7), aplicada en la r02b (INC-T204-01) |
| `sistema_global/README.md`, `Briefing_de_arranque.md`, `Decisiones_del_operador_Bloque_A.md`, `documentos_0/V0.75_…` | El A Forex como bloque existente o como pieza que no se toca | (b) |
| Deuda técnica | T-115 (solo Forex) | (a) |
| Deuda técnica | T-54 | (d), igual que D-20 |
| Deuda técnica | T-96, T-103, T-105, T-120 y T-199 | (b) |
| Deuda técnica | T-204 | fila nueva |
| `sistema_global/marco_comun_c/`, `V0.01_…`, `V0.03_…`, cuestionario | Divisas (`fx`) o B Forex | (d) |
| `bloque_a/` | «Divisas (Forex)», fichas FX, `tests/goldens/README.md` (T-115) | (d): el encargo prohíbe tocar A |
| `bloque_b/` | README V2.1 y dos fichas de F8 (origen) | (d): corpus congelado; sin enumerado del contrato A→B (INC-T204-04) |
| `.docs/README.md`, `.docs/knowledge/01_…` | Índices vivos | (c): nota y fila marcadas con T-204 |
| `.docs/tickets/`, `diario/`, `memoria/`, `diseno/` | Unas 300 líneas en 147 ficheros | (a)/(b) lo dedicado al Forex, con `limpiar_docs.py` (107 líneas en 80 ficheros, r02b); (c) el resto, como registro (`refs-vivas` lo exime) (INC-T204-03) |
| `.github/workflows/python-package.yml` | Nada | (d) |

## Diseño

- **Gate.**
  - `EJECUTORES` y `PAQUETES` quedan con A y B. El bucle de mypy recorre `"${!PAQUETES[@]}"` (antes, `0 1 2` fijos) y pytest usa `EJECUTORES[0]` y `EJECUTORES[1]`.
  - Son 10 comprobaciones: corpus, NFC, YAML, secretos, refs-vivas, ruff, mypy ×2 y pytest ×2. Con `--core` son 7.
  - Ruff se mide como el gate (`--output-format=concise … | wc -l`) sobre A y B: 1604, donde antes 2806 eran 1204 del Forex más 1602, y cada medida suma 2 líneas de resumen. La cuota baja a 1604.
  - mypy de A y de B y las líneas base no cambian.
- **Corpus.** `--update-corpus` en el mismo commit. Solo desaparecen las 180 líneas de `bloque_a_forex/`: antes del re-congelado, `corpus_integridad.py` daba solo esas 180 como «ELIMINADO».
- **refs-vivas.** El Forex no vuelve a las raíces válidas. Es un bloque retirado: su cita es ruta muerta salvo en los registros de `.docs/` o en una línea marcada con «T-204» (INC-T204-02). Las demás rutas de la misma cita se siguen comprobando.
- **Prueba que impide que vuelva** (`.docs/scripts/pruebas_gate_bloques.py`):
  - **Sin el Forex:** `check_all.sh`, `cuotas.txt`, `preparar_entorno.sh`, `qa_rama.sh`, `corpus_integridad.py` y `requisitos_entorno.txt` no lo nombran (`forex`, `fx`, `_fx`, sin distinguir mayúsculas). El detector se prueba con las formas de develop y con palabras que no deben saltar.
  - **El gate real:** `check_all.sh` se ejecuta en una raíz temporal con ruff, mypy y pytest falsos que anotan con qué se les llama. Da 10 de 10 (7 con `--core`) y llama a mypy y pytest justo sobre A y B. Una prueba menos que la línea base de un bloque hace fallar ese bloque.
  - **Las listas:** `preparar_entorno.sh` instala justo los ejecutores del gate y `qa_rama.sh` prueba justo sus paquetes. Las cuotas son de bloques que existen.
  - **refs-vivas:** ejecuta `prueba_refs_vivas.py`.

  Lo ejecuta `pruebas_scripts.sh`; la línea base pasa de 399 a 432 en la r01 y a 449 en la r02.
- **Bloque B.** No acepta nada propio del Forex. El `origen.tipo` del paquete de B es `BLOQUE_A | LIBRE`; no hay rutas, esquemas ni pruebas que lean ficheros del Forex. Su suite sigue en 174 o más.
- **Números.** Ninguno nuevo. 1604 sale de la medida del gate.
- **Falla cerrado.** Si el Forex vuelve a nombrarse en el gate o en sus scripts, `pruebas_gate_bloques.py` falla, y con ella `pruebas_scripts.sh`, que llaman `commit.sh` y `commit_limpio.sh`. Una cita viva sin marca hace fallar `refs-vivas`.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| El `.venv` compartido conserva `bloque-a-forex` instalado en modo editable | Nada en el gate: `pip freeze --exclude-editable` no lo cuenta | Se va solo al recrear el `.venv` con `preparar_entorno.sh` |
| Ramas abiertas que miden el Forex (`wip/t202`) | Conflicto en `cuotas.txt` y `check_all.sh` al integrar | Aviso del encargo: se ajusta al integrar |
| La Constitución y `.docs/` citaban el Forex | Texto desfasado | Enmienda 6 y limpieza aplicadas en la r02b (INC-T204-01 y 03) |

## Criterios de aceptación (binarios)

1. CA-1: `bloque_a_forex/` no existe y ningún ejecutor, prueba o configuración de A o de B lo usa.
2. CA-2: `check_all.sh` no nombra el Forex, ejecuta 10 comprobaciones (7 con `--core`) sobre A y B y pasa en verde. `cuotas.txt` no tiene líneas del Forex y ruff baja a lo que mide (1604); desde la r02 lo fija una prueba (H-07).
3. CA-3: el corpus se re-congela en el mismo commit, y solo cambian las 180 huellas del Forex.
4. CA-4: `refs-vivas` está en verde sin añadir nada a `tools/refs_allowlist.txt`. Una cita viva al Forex sin la marca T-204 lo hace fallar.
5. CA-5: hay una prueba en `.docs/scripts/` que falla si el Forex vuelve a `check_all.sh` o a `cuotas.txt`, y falla con la versión de develop.
6. CA-6: `pruebas_scripts.sh` está en verde, con la línea base subida a 449 (432 en la r01) y ninguna prueba quitada. La suite de B tiene 174 o más, y ninguna prueba de B se quita.
7. CA-7: `CLAUDE.md`, la skill `ri-probar`, `.pre-commit-config.yaml` y los prompts vivos dicen dos bloques, 10/10 y las líneas base y cifras reales (A ≥ 607, B ≥ 174, 43 hallazgos de `.secrets.baseline`); `docs/AVANCE.md` no da por aplicada la enmienda. `AGENTS.md` no necesita cambios.
8. CA-8: la fila T-204 de la deuda, con su origen en la orden del operador del 25-11-2026, y el ticket en EN QA.
9. CA-9 (r02): el parche de la Constitución y `limpiar_docs.py` quedan listos y coherentes: «enmienda 6» sin choque de numeración declarado (H-02), y la limpieza no toca la marca T-204, los resultados de gates y suites, los encargos ni las citas «…» (H-03).

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_gate_bloques.py`: sin Forex en el gate y en sus scripts; el detector | regresión | CA-2, CA-5 |
| `pruebas_gate_bloques.py`: el gate real con herramientas falsas (10, 7 con `--core`, líneas base por bloque) | integración, límite | CA-2 |
| `pruebas_gate_bloques.py`: cuotas, `preparar_entorno.sh` y `qa_rama.sh` frente a la lista del gate | regresión | CA-1, CA-2 |
| `prueba_refs_vivas.py`: 21 casos del bloque retirado (18 de la r01 y 3 de la r02, H-06) | regresión, límite | CA-4 |
| Las mismas pruebas con los scripts de develop | regresión (fallan sin el cambio) | CA-4, CA-5 |
| `.docs/tickets/T-204/mutantes.py` (36 mutantes) y los 10 del revisor (`r02_mutantes_revisor.py`) | robustez | CA-2, CA-4, CA-5 |
| r02: `pruebas_gate_bloques.py`, pruebas `test_h01` a `test_h08` (AVANCE, parche, `limpiar()`, líneas base, secretos y pre-commit, cuota de ruff = medida, INC-T204-04) | regresión | CA-2, CA-6, CA-7 |
| `./tools/check_all.sh` completo y `pruebas_scripts.sh` | regresión | CA-2, CA-3, CA-6 |

## Scripts

- Usa `.docs/scripts/pruebas_scripts.sh`, `.docs/scripts/memoria.sh` y `./tools/check_all.sh --update-corpus`.
- Crea `.docs/scripts/pruebas_gate_bloques.py`, `.docs/tickets/T-204/mutantes.py` y `.docs/tickets/T-204/limpiar_docs.py`. El último lo aplicó la coordinación con `--aplicar` (r02b); sin opciones dice qué cambiaría.
- r02: `.docs/tickets/T-204/generar_enmienda.py` (genera el parche; `--comprobar` dice si el guardado es el de ahora) y `.docs/tickets/T-204/r02_mutantes_revisor.py` (los mutantes del revisor con Q1 adaptado al código nuevo).

## Registro

- 2026-11-25 · PLANIFICADO · claude · orden del operador «olvídate del bloque A forex. Elimínalo»; inventario y clasificación
- 2026-11-25 · EN CURSO · claude · ampliación del operador («Elimina el bloque A Forex definitivamente»; «Haz esas tres cosas. Te doy mi consentimiento»): Constitución, `.docs/` e historial (este último, del operador). El sistema de permisos bloquea la Constitución y la limpieza de `.docs/`: se dejan propuestas (INC-T204-01 y 03)
- 2026-11-25 · EN QA (r01) · claude · gate 10/10, `pruebas_scripts.sh` 432, 29 mutantes muertos; commit local
- 2026-11-25 · QA r01 NO APTO · revisor · H-01 a H-03 medios, H-04 a H-08 bajos (`qa.md`)
- 2026-11-25 · EN QA (r02: QA r01 NO APTO) · claude · los ocho hallazgos corregidos con su prueba; `pruebas_scripts.sh` 449; 36 mutantes propios y 10 del revisor muertos; scripts del revisor en verde; gate 10/10 (`gate_t204_r02.log`); commit local
- 2026-11-25 · r02b · coordinación · por orden del operador («Todo»): aplicadas la enmienda 6 (V0.7) y la limpieza de `.docs/` (107 líneas en 80 ficheros)
- 2026-11-25 · QA r02 NO APTO · revisor · H-09 y H-10 medios, H-11 y H-12 bajos
- 2026-11-25 · EN QA (r03: QA r02 NO APTO) · claude · H-09 a H-12 corregidos con su prueba; `pruebas_scripts.sh` 455; 38 mutantes propios y 10 del revisor muertos; scripts r01 y r02 del revisor en verde; marco 62/62; gate 10/10 (`gate_t204_r03.log`); commit local
- 2026-11-25 · QA r03 APTO pendiente de ronda de cierre · revisor · H-13 (bajo) y una observación sobre `test_h02`
- 2026-11-25 · EN QA (ronda de cierre de la QA r03) · claude · H-13 y la observación corregidos; rebase sobre `origin/develop` (`d11662ff`, T-201 y T-203): ruff 1533 (medida de A y B), mypy A 67 y B 159, líneas base A 607 y B 174; `pruebas_scripts.sh` 455; gate 10/10 (`gate_t204_cierre.log`); commit local
- 2026-11-25 · QA r03, ronda de cierre: APTO con H-14 (bajo) · revisor
- 2026-11-25 · EN QA (ronda de cierre de la QA r03) · claude · cierre 2: rebase sobre `6c8910c1` (T-205); H-14: `RE_EVIDENCIA` sin distinguir mayúsculas y con el recuento «A-Forex N, B N», y 5 casos en `test_h03`; la limpieza de los tickets llegados con el rebase está propuesta (5 líneas), porque el sistema de permisos bloqueó `--aplicar`; `r04_02` da 0; `pruebas_scripts.sh` 460; 41 mutantes; gate 10/10 (`gate_t204_cierre2.log`); commit local
- 2026-11-25 · segunda ronda de cierre verificada · APTO sin nada abierto (`qa.md`).
- 2026-11-25 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`; después, la limpieza del historial (autores y `bloque_a_forex/`).
