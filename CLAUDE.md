# robotInvestor — Bloque A (Buscador de Oportunidades de Inversión)

Proyecto: implementar el Bloque A V5.0 (25 agentes LLM + Motor determinista) descrito en
este paquete, con Claude Code como desarrollador. La entrega V5.0 (02-11-2026) es la
**fuente de verdad**; este archivo es el protocolo de trabajo que la acompaña.

Lectura mínima obligatoria antes de tocar código:
1. `README - Índice de la entrega y registro de la reforma V5.0.md` (mapa del paquete)
2. `08_Arquitectura/Arquitectura del Bloque A - Descripción detallada para LLM - V4.0.md` (89 líneas, resumen denso)
3. `01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.0.md` (950 líneas — la constitución: R1–R25, CT-01..CT-22, Anexo A/B)

## Reglas del proyecto (innegociables)

1. **Una fase = un kit de contexto.** Cada sesión trabaja con Documento 0 + los 2-3
   documentos de su fase. Prohibido intentar "leer todo el paquete". Los 36 system
   prompts de `02_System_prompts` son **datos en runtime** (el ejecutor los carga por
   nombre de agente), no material de implementación que haya que memorizar.
2. **Los números nunca a mano.** Presupuestos, tolerancias, semillas, umbrales y pesos
   salen del Anexo A del Documento 0 → `11_Ejecutor/config/por_defecto.yaml`, o de la
   ficha correspondiente del Catálogo. Si un número no está ahí, no se escribe en código.
3. **Todo formato sale de un artefacto mecánico.** Esquemas JSON del Anexo B y de
   `06_Plantillas_entregables` + sus ejemplos son la definición; el código se valida
   contra ellos (jsonschema), nunca al revés.
4. **Mock antes que API.** Toda funcionalidad nueva se valida primero con
   `--cliente mock` (coste cero, reproducible). La API real solo en modo sombra.
5. **Nada cuenta como hecho sin tests.** El ejecutor arranca con 45 tests verdes;
   ninguna fase puede dejarlos por debajo. Cada contrato/ficha nueva añade sus pruebas.
6. **F7/F8/F9 son almacenes indexados**, no contexto: se accede por identificador
   (RF-xxxx, TM-xx, fondo_entry_NNN), nunca se cargan enteros (7.200–11.300 líneas).
7. **Ante ambigüedad del spec, se pregunta o se documenta como incidencia**
   (`docs/incidencias.md`), no se decide en silencio.

## Trampas conocidas del corpus (detectadas en la auditoría del 03-11-2026)

- **Versiones cruzadas V4.0/V5.0:** los prompts MC citan "Catálogo V4.0"; el catálogo
  entregado es V5.0 (81 fichas); el ejecutor implementa las 60 del índice V4.0
  (`bloque_a/motor/servicio.py`, `CATALOG_VERSION = "4.0"`). Las 21 fichas nuevas V5.0
  (familias IDX, FON, DER, MON, TCV — los 5 tipos de activo nuevos) no tienen código y
  hoy responden `METODO_NO_IMPLEMENTADO` con alternativa.
- **Numeración F ≠ nombre de archivo:** F7 = "Documentación para el Analizador…",
  F8 = "Documentación para el Motor…", F9 = "Registro de Fuentes…", FM = "Fondo
  metodológico…". Verificar siempre el H1 del archivo en `05_Archivos_operativos`.
- **Identificadores de modelo sin verificar:** `config/por_defecto.yaml` usa
  `claude-opus-5-5`/`claude-sonnet-5-5`/`claude-haiku-5-5` y el propio paquete exige
  comprobarlos en la página de modelos de Anthropic antes de usar la API real.
- **Referencias con estado PENDIENTE_BARRIDO** (RF-0035, RF-0550, RF-0555): confirmar
  con `bloque-a verificar-enlaces` en el primer barrido, no asumirlas válidas.

## Plan de fases

| Fase | Contenido | Kit de contexto |
|---|---|---|
| 0 | Verificador de consistencia de IDs (CT/R/F/RF/fichas) + resolver skew V4.0↔V5.0 | Documento 0, Catálogo V5.0, `servicio.py` |
| 1 | Implementar las 21 fichas V5.0 (IDX, FON, DER, MON, TCV) | Catálogo V5.0, `motor/operaciones.py` |
| 2 | Fichas restantes DOCUMENTADO por prioridad P0/P1 | Ídem, por familias |
| 3 | Esquemas congelados (goldens) para CT-01..CT-22 | Anexo B, `contratos.py` |
| 4 | Ejecutar el plan de 57 pruebas y registrar evidencias | `09_Pruebas/Plan V3.0` |
| 5 | Modo sombra real con API (ciclo semanal, sin entrega al Broker) | `11_Ejecutor/README.md`, config |
| 6 | Conexión con el backtester de robotTrading (`senales.csv`, `pronosticos.csv`, `metricas.json`) | Los 3 CSV de interfaz del README del ejecutor |

Avance registrado en `docs/AVANCE.md`.

## Comandos

```bash
cd 11_Ejecutor
source ../.venv/bin/activate          # venv del proyecto (Python 3.12, ~/.local/bin/python3.12)
pip install -e ".[pruebas]"
pytest -q                             # línea base: 45 pasando

# Ciclo simulado sin coste (crea estado_bloque_a/ y entregables/, ignorados por git)
bloque-a --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --salida /tmp/salida_mock backtest --desde 2024-01-01 --hasta 2024-03-31
```

## Convenciones

- Rama única `develop`, commits directos, mensajes en español con prefijo de área
  (`data:`, `fase0:`, `motor:`, `contratos:`, `test:`).
- Los `.md` son canónicos; los `.docx` son copias de consulta — nunca se editan.
- `99_Historico_V3.0` es solo referencia: prohibido implementar contra él.
