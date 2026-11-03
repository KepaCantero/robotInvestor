# Avance del proyecto

| Fecha | Fase | Entrada | Estado |
|---|---|---|---|
| 2026-11-03 | — | Proyecto creado: entrega V5.0 copiada íntegra (351 archivos, 25 MB), git `develop` con commit baseline, CLAUDE.md (protocolo), docs/ (AVANCE + incidencias) | ✅ Hecho |
| 2026-11-03 | — | Entorno: venv `.venv` (Python 3.12.15 de ~/.local/bin), ejecutor instalado `pip install -e ".[pruebas]"` + `arch` | ✅ Hecho |
| 2026-11-03 | — | **Fix NFD→NFC**: los 191 nombres de archivo copiados estaban en NFD (artefacto macOS) y rompían 1 test (AG-21..25); renormalizados a NFC, contenidos ya eran NFC | ✅ Hecho |
| 2026-11-03 | — | Línea base verificada: **45/45 tests en verde** y backtest mock end-to-end (13 ciclos, 368 señales, 282 pronósticos resueltos, entregables JSON por semana, aviso de fuga por conocimiento operativo) | ✅ Hecho |
| 2026-11-03 | — | **Actualización a V5.1** (cambios propietario A1–A4): CT-23 consulta al Broker, CT-24 seguimiento encargado + ciclo C6 + F11 + informe de seguimiento, CT-25 credenciales con bóveda HT-01, H5 décadas con hitos HIT- y `horizonte_principal` obligatorio. Sincronización: 16 archivos nuevos, 4 renombrados (README y Documento 0 → V5.1), 169 modificados; NFC re-aplicado (195 renames en staging). Ejecutor V1.2: **58/58 tests** + mock end-to-end (361 señales, 507 pronósticos, 336 resueltos) y subcomandos `seguimiento`/`consulta-broker`/`credencial` verificados | ✅ Hecho |
| 2026-11-03 | — | **Monorepo de 3 bloques**: `git mv` del Bloque A a `bloque_a/` (historial conservado, 363 renames) + añadir `bloque_a_forex/` (entrega V1.1, 342 archivos, ejecutor `bloque-a-forex`) y `bloque_b/` (entrega V2.1, 561 archivos, ejecutor `bloque-b` con puerta de 30 minutos, Vigía y backtest de rankings). Los tres ejecutores instalados en el mismo venv. **Líneas base verificadas: A 58/58 · A-Forex 68/68 · B 118/118** (B necesitó `python-docx`, sin él 3 tests fallan porque el .docx del mapa de eslabones degrada con elegancia — INC-003) | ✅ Hecho |
| 2026-11-03 | — | **Quality gates transplantados de robotTrading**: `tools/check_all.sh` con 12 gates **12/12 en verde** — corpus canónico congelado por hash (695 archivos, re-congelado solo deliberado `--update-corpus` + motivo en el commit, espejo de los goldens de conformance), nombres NFC, yaml-configs, secrets (allowlist manual: 2 fixtures verificados), refs-vivas (antídoto planes rancios, con allowlist de entregables futuros), cuotas ratchet ruff 3490 / mypy 135+174+160 (solo bajan; andamiaje temporal sin-deuda), pytest ×3 con número base comprobado. Pre-commit instalado (fixers SOLO sobre docs/prompts/tools/CLAUDE.md — los fixers tocaron 7 ejemplos entregados en la primera pasada y se REVERTIERON; detect-secrets con baseline de 48 hallazgos auditados falsos: fixtures y huellas hex sintéticas) | ✅ Hecho |

## Pendiente

- Fase 0: verificador de consistencia de IDs + resolución del skew V4.0↔V5.0 (Catálogo V5.0 = 81 fichas vs `servicio.py` = 60 de V4.0; prompts MC citan V4.0).
- Fases 1–6 según tabla de CLAUDE.md.

## Notas de entorno

- Python 3.12.15 en `~/.local/bin/python3.12` (el del sistema es 3.9, insuficiente).
- `arch` es dependencia opcional (`[garch]`): sin ella, 1 test falla. Ya instalada en el venv.
- El mock genera `senales.csv`, `pronosticos.csv`, `metricas.json`, `consumo.csv` — la interfaz pensada para el backtester de robotTrading (Fase 6).
