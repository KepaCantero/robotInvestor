# robotInvestor — Robot Investor multi-bloque (A · A Forex · B)

Monorepo con los tres bloques del sistema Robot Investor, implementados con Claude Code
como desarrollador. Cada entrega es la **fuente de verdad** de su bloque; este archivo es
el protocolo de trabajo común.

| Carpeta | Bloque | Entrega | Ejecutor (comando) | Línea base tests |
|---|---|---|---|---|
| `bloque_a/` | Buscador de oportunidades (12 tipos de activo) | V5.1 (03-11-2026) | `bloque-a` | 439 |
| `bloque_a_forex/` | Buscador de oportunidades de divisas | V1.1 (03-11-2026) | `bloque-a-forex` | 68 |
| `bloque_b/` | Selección de activos por mercado (encargos del Bloque A) | V2.1 (03-11-2026) | `bloque-b` | 174 |

Por encima de los bloques, `sistema_global/` contiene la Constitución global del Robot Investor
(`sistema_global/constitucion/Constitucion_Global.md`, fuente de verdad de todo el sistema), el código
de referencia de la Fase 1 (`sistema_global/marco_comun_c/`, V0.73, 61 suites propias fuera de los gates
de los bloques), un Documento 0 por pieza y la deuda técnica y el briefing de arranque
(`sistema_global/README.md` es su índice). No forma parte del corpus congelado.

**Trabajo entre agentes (desde el 9-11-2026).** El repo lo trabajan Claude y Astra (OpenAI), con las
mismas reglas (Astra entra por `AGENTS.md`). Flujo planificar → implementar → probar → QA con una skill por
fase en `.agents/skills/` (`.claude/skills` es un enlace a esa carpeta); la QA la hace el agente que no
implementó (`.docs/knowledge/02_flujo-de-trabajo.md`). Espacio de trabajo en `.docs/` (índice y reglas en
`.docs/README.md`): tickets `.docs/tickets/T-NN/` con el ID de la deuda técnica, diario mensual, scripts,
conocimiento y memoria indexada. Al empezar se leen `.docs/README.md`, `.docs/memoria/LEEME.md` y los índices;
Claude escribe solo en `.docs/memoria/claude/` y en `.docs/memoria/compartida/`. **Lo repetible se automatiza:**
antes de hacer algo a mano se mira `.docs/scripts/`, y lo que se vaya a repetir se guarda ahí como script
(secretos solo en `.env`, vía `.docs/scripts/common.sh`) para no gastar otra vez los mismos tokens.

Cada bloque mantiene internamente la estructura numerada de la entrega
(`01_Gobernanza` … `11_Ejecutor` [+ `12_Runbook` en B], `99_Historico…`).

Lectura mínima obligatoria antes de tocar el código de un bloque:
1. El README índice de ese bloque (`bloque_x/README - Índice….md`).
2. `bloque_x/08_Arquitectura/…Descripción detallada para LLM….md` (resumen denso).
3. `bloque_x/01_Gobernanza/Documento 0 - Protocolo maestro….md` (la constitución del
   bloque: reglas R, contratos CT, archivos F, ciclos, horizontes, Anexos A/B).

Flujo entre bloques: el Bloque A (y el Forex) detectan ámbitos y emiten **encargos**;
el Bloque B recibe el encargo, estudia el mercado y elige los activos. El ejecutor A
emite `senales.csv` / `pronosticos.csv` / `metricas.json` pensados para un backtester
externo (robotTrading). En V5.1/V1.1 ambos A comparten: CT-23 consulta al Broker,
CT-24 seguimiento encargado (ciclo C6, F11), CT-25 credenciales con bóveda en HT-01,
H5 décadas con hitos HIT- y `horizonte_principal` obligatorio (HT-09 C17–C19).

## Reglas del proyecto (innegociables)

1. **Una fase = un kit de contexto.** Cada sesión trabaja con el Documento 0 del bloque
   afectado + los 2-3 documentos de su fase. Prohibido intentar "leer todo el paquete".
   Los system prompts de `02_System_prompts` son **datos en runtime** (el ejecutor los
   carga por nombre de agente), no material de implementación que haya que memorizar.
2. **Los números nunca a mano.** Presupuestos, tolerancias, semillas, umbrales y pesos
   salen del Anexo A del Documento 0 del bloque → `11_Ejecutor/config/por_defecto.yaml`,
   o de la ficha correspondiente del Catálogo. Si un número no está ahí, no se escribe
   en código.
3. **Todo formato sale de un artefacto mecánico.** Esquemas JSON de `06_Plantillas_entregables`
   + sus ejemplos son la definición; el código se valida contra ellos (jsonschema),
   nunca al revés.
4. **Mock antes que API.** Toda funcionalidad nueva se valida primero con
   `--cliente mock` (coste cero, reproducible). La API real solo en modo sombra.
5. **Nada cuenta como hecho sin tests.** Líneas base: A 439 (desde T-92), A-Forex 68, B 174 (desde T-64), 10-11-2026. Ninguna
   fase puede dejar su suite por debajo. Cada contrato/ficha nueva añade sus pruebas.
6. **F7/F8/F9 (y equivalentes) son almacenes indexados**, no contexto: se accede por
   identificador (RF-xxxx, TM-xx…), nunca se cargan enteros (7.000–11.000 líneas).
7. **Ante ambigüedad del spec, se pregunta o se documenta como incidencia**
   (`docs/incidencias.md`), no se decide en silencio.
8. **No mezclar bloques en una misma fase** salvo la interfaz de encargos (A→B), que es
   la única frontera que se toca por los dos lados y con esquemas congelados de ambos.
9. **Una fase no cierra sin `./tools/check_all.sh` en verde (12/12)** y con las cuotas
   (si se tocaron) más bajas que como se encontraron.

## Trampas conocidas de los corpus (auditadas 03-11-2026)

- **Catálogo del Bloque A:** los prompts MC congelados citan "Catálogo V4.0"; el catálogo entregado es V5.0
  (81 fichas). Desde T-92 (auditoría de Astra, C6) el despacho CT-09 reconoce las 81
  (`bloque_a/11_Ejecutor/bloque_a/motor/servicio.py`, `CATALOG_VERSION = "5.0"`). Hay 17 manejadores, pero
  solo 14 dan cifras citables: las tres con código que el Catálogo da por «Documentado»
  (`DOCUMENTADAS_CON_CODIGO`, T-65 CS-08) se rechazan, y VOL-GARCH-001 depende de `arch`. Una ficha conocida sin
  manejador responde `METODO_NO_IMPLEMENTADO`; una ajena al catálogo, `OPERACION_SIN_FICHA`. Una alternativa
  solo se anuncia si se sirve. → Fase 0 de bloque_a.
- **Versión sin subir en pyprojects (INC-001/002):** `bloque_a/11_Ejecutor` declara
  1.1.0 (README dice V1.2); `bloque_a_forex/11_Ejecutor` declara 1.0.0 (README dice
  V1.1). El código entregado ES el de la versión del README. No corregir en silencio.
- **Numeración F ≠ nombre de archivo** (p. ej. F7 = "Documentación para el
  Analizador…"). Verificar siempre el H1 del archivo en `05_Archivos_operativos`.
- **Identificadores de modelo sin verificar:** los `config/por_defecto.yaml` usan
  `claude-opus-5-5`/`claude-sonnet-5-5`/`claude-haiku-5-5` y cada paquete exige
  comprobarlos en la página de modelos de Anthropic antes de usar la API real.
- **macOS NFD:** las carpetas extraídas de entregas pueden traer nombres NFD que rompen
  las comparaciones NFC del código. Al recargar una entrega, renormalizar siempre
  (hecho en las tres cargas actuales).

## Plan de fases (por bloque; orden A → A-Forex → B en lo transversal)

| Fase | Contenido | Kit de contexto |
|---|---|---|
| 0 (bloque_a) | Verificador de consistencia de IDs (CT/R/F/RF/fichas) + resolver skew V4.0↔V5.0 | Documento 0, Catálogo V5.0, `servicio.py` |
| 1 (bloque_a) | Implementar las 21 fichas V5.0 (IDX, FON, DER, MON, TCV) | Catálogo V5.0, `motor/operaciones.py` |
| 2 (bloque_a) | Fichas restantes DOCUMENTADO por prioridad P0/P1 | Ídem, por familias |
| 3 (ambos A) | Esquemas congelados (goldens) para los contratos CT | Anexo B, `contratos.py` |
| 4 (todos) | Ejecutar los planes de pruebas y registrar evidencias (A: 67 · A-Forex: 86 · B: 204) | `09_Pruebas/` de cada bloque |
| 5 (todos) | Modo sombra real con API (ciclo semanal, sin entrega al Broker) | `11_Ejecutor/README.md` + config de cada bloque |
| 6 (A→B) | Cadena de encargos A→B real y conexión al backtester de robotTrading (`senales.csv`, `pronosticos.csv`, `metricas.json`) | READMEs de ejecutores + esquemas de encargo |

Avance registrado en `docs/AVANCE.md`. Los prompts paste-ready de cada fase viven en
`prompts/` (empezando por `prompts/00_ENTORNO.md`, que verifica venv, dependencias y
MCPs); no reinventar su contenido: se pegan tal cual.

## Calidad (gates transplantados de robotTrading)

**`./tools/check_all.sh` es EL gate del repo. Una fase no cierra sin él en verde (12/12).**
Flags: `--core` (rápido: corpus+config+tests), `--strict` (corta al primer fallo, CI),
`--update-corpus` (re-congelado del corpus, ver abajo).

| Gate | Qué protege |
|---|---|
| corpus-integridad | El corpus canónico congelado por hash (695 archivos: prompts, catálogo, esquemas, referencias…). Adaptación de los goldens de conformance: **re-congelar solo es deliberado** — `--update-corpus` en el MISMO commit que el cambio y con el motivo en el mensaje. Nada silencioso. |
| nombres-nfc | Lección macOS pagada 2×: nombres NFD rompen tests que en Linux pasan. |
| yaml-configs | Los 3 `por_defecto.yaml` parsean. |
| secrets | Repo público: patrones reales con allowlist explícita (`tools/secrets_allowlist.txt`, solo cadadas verificadas a mano). |
| refs-vivas | Rutas citadas en CLAUDE.md/prompts/docs existen — antídoto contra planes rancios. Entregables futuros: `tools/refs_allowlist.txt` (quitar la línea al aterrizar la fase). |
| ruff, mypy ×3 | **Cuotas (ratchet): solo bajan.** El código entregado no era limpio (ruff 3490, mypy A 135 / FX 174 / B 160); las cuotas congelan el estado y cada fase debe dejarlas más bajas si toca el paquete. Al llegar a 0, la línea se borra y el gate se vuelve estricto. Andamiaje temporal — política sin-deuda. |
| pytest ×3 | Líneas base innegociables: A ≥ 439 · FX ≥ 68 · B ≥ 174 (el gate comprueba el NÚMERO, no solo el exit code: quitar tests no pasa). |

**Pre-commit** (`.venv/bin/pre-commit install`): check-yaml, merge-conflicts,
debug-statements, detect-secrets con `.secrets.baseline` (48 hallazgos auditados como
falsos el 03-11: fixtures de tests y huellas hex de salidas simuladas — verificados a
mano). Los fixers de espacios SOLO tocan lo nuestro (`docs/`, `prompts/`, `tools/`,
`CLAUDE.md`): el paquete entregado ni un espacio se le toca.

**Procesos heredados de robotTrading además de los gates:** veredictos binarios con
umbral duro (ya llegan en el diseño G3/HT-09 del corpus); bench propio ANTES de adoptar
la receta de otro repo (lección NautilusTrader: prometía 10×, dio 0.26–1.05×); si algún
día hay sesiones paralelas de agentes: clústeres disjuntos de archivos y solo el
propietario (o una sesión coordinadora) hace commit.

## Comandos

```bash
# venv único del proyecto (Python 3.12, ~/.local/bin/python3.12)
source .venv/bin/activate
pip install -e bloque_a/11_Ejecutor -e bloque_a_forex/11_Ejecutor -e bloque_b/11_Ejecutor
pip install arch openpyxl python-docx         # opcionales que usan los tests (B necesita python-docx para sus entregables .docx)

pytest -q bloque_a/11_Ejecutor        # 439
pytest -q bloque_a_forex/11_Ejecutor  # 68 (≈5 min: backtests simulados)
pytest -q bloque_b/11_Ejecutor        # 174

# Ciclo simulado sin coste (ejemplo bloque_a; los demás análogos, ver su README)
cd bloque_a/11_Ejecutor
bloque-a --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --salida /tmp/salida_mock backtest --desde 2024-01-05 --hasta 2024-03-29
```

## Convenciones

- Rama única `develop`, commits directos, mensajes en español con prefijo de área
  (`data:`, `infra:`, `fase0:`, `motor:`, `contratos:`, `test:`).
- Los `.md` son canónicos; los `.docx` son copias de consulta — nunca se editan.
- `99_Historico*` es solo referencia: prohibido implementar contra él.
