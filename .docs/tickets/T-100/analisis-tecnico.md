# T-100 · Análisis técnico

## Causa raíz

- **T-76 H-17:** `movimiento_sombra` no tenía identificador, así que cada declaración era un movimiento nuevo. El resto de lo que declara G en el marco lleva `event_id`.
- **T-76 H-19:** `barrer()` avisaba del registro roto, pero luego calculaba lo pendiente igual y no activaba el kill-switch.
- **T-75 H-15:** en `embudo()`, el reinicio del veto estaba después del `continue` que se salta lo anterior al periodo.
- **Mutantes (T-75 H-17, T-76 H-18):** faltaban regresiones para el borde del cierre, los costes, el juicio por el último mes pendiente, el mes de inicio en UTC, `isfinite`, el empate y `reloj_firme` en la pantalla.

## Implementación

- **`orquestador.py`:**
  - `movimiento_sombra(..., ref=None)`: `ref` debe ser texto no vacío (si no, O-01). Se busca un APORTE o RETIRADA con la misma `ref`: si tiene el mismo tipo e importe, O-02 (ok, duplicado, sin cambios); si no, aviso O-03, kill-switch y O-03. La entrada guarda `ref`.
  - `barrer()`: con `sombra_ok()` falso, aviso O-13, `_activar_kill` y `falta = None`.
  - `embudo()`: `nuevo_analisis` se calcula para cada anotación. Si es anterior al periodo, borra el veto antes del `continue`; dentro del periodo, después de contar la anotación, como antes.
- **`migraciones.py`:** solo la descripción de MIG-011 (H-20).
- **`catalogo_codigos.py`:** texto de O-03.

**Decisiones:**
- El esquema del código no cambia, porque `parte_de_codigo()` solo cuenta constantes. Por eso no hay MIG-012.
- Contenido igual es tipo e importe; el precio y el instante pueden diferir entre quienes declaran, y vale la primera declaración.
- Un conflicto de referencia activa el kill-switch, por coherencia con `_duplicado` (§11).

**Límites:** ver el §5 del Documento 0 de la V0.76.
