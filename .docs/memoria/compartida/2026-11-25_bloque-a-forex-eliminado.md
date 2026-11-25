---
id: compartida/2026-11-25_bloque-a-forex-eliminado
autor: claude
fecha: 2026-11-25
tipo: decision
etiquetas: [bloque_a_forex, gate, cuotas, corpus]
fuente: .docs/tickets/T-204/README.md y la fila T-204 de la deuda técnica
vigencia: vigente
---

## Decisión

El operador, el 25-11-2026: «olvídate del bloque A forex. Elimínalo». Después, ese mismo día: «Elimina el bloque A Forex definitivamente».

- `bloque_a_forex/` ya no existe. Las divisas las cubre el Bloque A general (su Analista de Divisas).
- El gate (`./tools/check_all.sh`) pasa a tener 10 comprobaciones: mypy ×2 y pytest ×2, solo de A y B. `--core` hace 7.
- Las cuotas son ruff 1533 (desde el rebase sobre T-201 y T-203; era 1604 con la base anterior), que cuenta solo A y B, y mypy de A y de B. Las líneas base son A ≥ 607 y B ≥ 174.
- Ahora el corpus congelado tiene 525 archivos.
- `.docs/scripts/pruebas_gate_bloques.py` falla si el Forex vuelve a `check_all.sh`, a `cuotas.txt` o a los scripts que enumeran los bloques.

## Cómo aplicarlo

- **Al citarlo:** en un documento vivo (`CLAUDE.md`, `prompts/`, `docs/`, skills, `.docs/README.md`, `.docs/knowledge/`), una cita a `bloque_a_forex/…` hace fallar `refs-vivas`. Solo vale si la misma línea lleva «T-204». En los registros (tickets, diario, memoria, diseño), las citas antiguas se quedan como estaban.
- **Esta decisión sustituye** a la parte del Forex de `compartida/2026-11-13_codigo-manda-sobre-doc0-a` («se quiere poder probarlo solo con divisas»; T-115). El resto de esa entrada sigue vigente.
- **Constitución:** la enmienda 6 la llevó a la V0.7 el 25-11-2026, por orden del operador («Todo»). Quitó el A Forex de D-20, del cambio 17, del §2 y del §14. Las enmiendas 4 y 5 siguen propuestas, y la numeración provisional de la 5 se corre en uno (INC-T204-01).
- **`.docs/`:** se aplicó la limpieza de lo dedicado al Forex ese mismo día (`.docs/tickets/T-204/limpiar_docs.py --aplicar`, 107 líneas en 80 ficheros; INC-T204-03). Las citas que quedan son registro o evidencia literal.
