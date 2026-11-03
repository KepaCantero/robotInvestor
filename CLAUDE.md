# robotInvestor — Robot Investor multi-bloque (A · A Forex · B)

Monorepo con los tres bloques del sistema Robot Investor, implementados con Claude Code
como desarrollador. Cada entrega es la **fuente de verdad** de su bloque; este archivo es
el protocolo de trabajo común.

| Carpeta | Bloque | Entrega | Ejecutor (comando) | Línea base tests |
|---|---|---|---|---|
| `bloque_a/` | Buscador de oportunidades (12 tipos de activo) | V5.1 (03-11-2026) | `bloque-a` | 58 |
| `bloque_a_forex/` | Buscador de oportunidades de divisas | V1.1 (03-11-2026) | `bloque-a-forex` | 68 |
| `bloque_b/` | Selección de activos por mercado (encargos del Bloque A) | V2.1 (03-11-2026) | `bloque-b` | 118 |

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
5. **Nada cuenta como hecho sin tests.** Líneas base: A 58, A-Forex 68, B 118. Ninguna
   fase puede dejar su suite por debajo. Cada contrato/ficha nueva añade sus pruebas.
6. **F7/F8/F9 (y equivalentes) son almacenes indexados**, no contexto: se accede por
   identificador (RF-xxxx, TM-xx…), nunca se cargan enteros (7.000–11.000 líneas).
7. **Ante ambigüedad del spec, se pregunta o se documenta como incidencia**
   (`docs/incidencias.md`), no se decide en silencio.
8. **No mezclar bloques en una misma fase** salvo la interfaz de encargos (A→B), que es
   la única frontera que se toca por los dos lados y con esquemas congelados de ambos.

## Trampas conocidas de los corpus (auditadas 03-11-2026)

- **Versiones cruzadas en bloque_a:** los prompts MC citan "Catálogo V4.0"; el catálogo
  entregado es V5.0 (81 fichas); el ejecutor implementa las 60 del índice V4.0
  (`bloque_a/…/motor/servicio.py`, `CATALOG_VERSION = "4.0"`). Las 21 fichas nuevas V5.0
  (IDX, FON, DER, MON, TCV) están DOCUMENTADAS sin código y responden
  `METODO_NO_IMPLEMENTADO` con alternativa. → Fase 0 de bloque_a.
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

Avance registrado en `docs/AVANCE.md`.

## Comandos

```bash
# venv único del proyecto (Python 3.12, ~/.local/bin/python3.12)
source .venv/bin/activate
pip install -e bloque_a/11_Ejecutor -e bloque_a_forex/11_Ejecutor -e bloque_b/11_Ejecutor
pip install arch openpyxl python-docx         # opcionales que usan los tests (B necesita python-docx para sus entregables .docx)

pytest -q bloque_a/11_Ejecutor        # 58
pytest -q bloque_a_forex/11_Ejecutor  # 68 (≈5 min: backtests simulados)
pytest -q bloque_b/11_Ejecutor        # 118

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
