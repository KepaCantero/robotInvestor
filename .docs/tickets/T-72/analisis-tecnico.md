# T-72 · Análisis técnico

## Causa raíz o motivo

- **H-05 de la QA de T-79.** La consola leía los privados `_roto` y `_n` del `Diario`. No tenía cómo saber que el estado del Orquestador había cambiado por fuera del diario hasta que la operación siguiente daba DI-06.
- **H-06.** Las tolerancias del `Reloj` eran atributos públicos que se podían cambiar después de construirlo. Además, se comparaban con `>`, y con NaN esa comparación es falsa, así que el reloj seguía dando instantes.

## Evidencia

- Sondas de la QA de T-79.
- La batería nueva, que falla con el código de la V0.68.
- Las sondas de la QA r01 en `entrega_claude/V0.69/qa/`.

## Implementación

- **`validador/diario.py`:** `Diario.estado_diario()`, con las mismas comprobaciones que `_sin_cambios_por_fuera`, pero sin bloquear.
- **`validador/consola.py`:** `_diario` usa esa foto y comprueba también `operativo`. El tope de contraste se compara con `not s <= tope`.
- **`validador/reloj.py`:** `_tol` privado, propiedades que validan su tope (`_tol_i`), y `_dentro` y `_suma`, que nunca lanzan.
- **Pruebas:** `pruebas/pruebas_reloj_diario_t72.py`, nueva; `pruebas/pruebas_consola_sistema.py`, con el diario falso con `estado_diario()`.
- **Decisiones:**
  - `estado_diario` se llama así, y no `estado`, para no ocultar un atributo del Orquestador con ese nombre (el `Diario` pasa al Orquestador todo lo que no tiene).
  - El tope de `max_sin_contraste_s` no se fija aquí: es un número nuevo y va a T-89.
- **Límites conocidos:** H-03 (T-89).
- **Comandos:**
  - `python3 -I pruebas/pruebas_reloj_diario_t72.py`;
  - `.docs/scripts/pruebas_marco.sh`.
