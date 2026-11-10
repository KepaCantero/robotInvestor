# T-76 · Análisis técnico

## Causa raíz o motivo

P17 y el §9, punto 9, de la Constitución V0.6 piden la cartera sombra pasiva. La QA r01 de la V0.71 encontró cuatro fallos:
- el coste estaba mal prorrateado (H-01);
- el juicio podía adelantarse (H-02);
- había resultados no finitos (H-03);
- el juicio se podía silenciar dejando de comparar (H-04).

## Implementación (V0.71 y ronda r02 en la V0.73)

- **`sombra.py`:**
  - `estado_sombra(entradas, precio, hasta)` devenga el coste por tramos: entre movimientos descuenta unidades con (1 - coste)^(días/365), como el gasto corriente de un fondo.
  - Una retirada se compara en relativo con lo que hay.
  - Los resultados no finitos dan None.
- **`orquestador.py` · `comparar_sombra`:**
  - comprueba la integridad antes de leer;
  - solo admite meses terminados en UTC;
  - el índice de precios del inicio lo fija la primera comparación;
  - O-41 sale cuando el robot pasa a no superar a la sombra.
- **`orquestador.py` · seguimiento:** `comparacion_sombra_pendiente(ahora)` devuelve el mes pendiente, y `barrer()` lo avisa con O-42, uno por mes pendiente.

**Decisiones:**
- En real, robot y sombra se dividen por la misma inflación, así que el veredicto coincide con el nominal. Se informa la cifra real (D-30).
- La sombra no paga impuestos ni comisiones de compra: es el plan pasivo de referencia.

**Límites (H-07 y H-09):**
- El precio del índice y la inflación no se contrastan con K, que no existe aún (T-86).
- `gasto_dia` no está encadenado.
- El capital inicial no se compara con el de la cartera real.
- Vaciar el registro reinicia el plazo, el límite conocido de las cadenas sin ancla externa (T-02).
