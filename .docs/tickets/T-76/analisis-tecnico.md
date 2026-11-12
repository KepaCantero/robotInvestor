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

## Ronda r03 (V0.75)

- **H-10:** `comparar_sombra` valora al cierre del mes en UTC (`cierre` = el primer instante del mes siguiente menos 1 µs). Usa solo las entradas con `ahora <= cierre` y el coste de análisis `_costes_analisis_desde(inicio, cierre)`. El valor del robot, el precio del índice y la inflación son los del cierre, y así lo dice el docstring.
- **H-11:** `iniciar_sombra` y `movimiento_sombra` rechazan con O-01 unas unidades `importe / precio` no finitas. El motivo dice «no finito», distinto del de una retirada mayor.
- **H-12:** los dos métodos llaman primero a `_sombra_precheck()` (O-13 con kill-switch). `barrer()` avisa con O-13 si `sombra_ok()` es falso.
- **H-13:** `comparaciones_sombra_pendientes(ahora, gracia_dias)` da `primero`, `faltan` y `juicio`. Un mes cuenta cuando han pasado `i_dias_gracia_comparacion_sombra` días (5, `[PROPUESTO]`) desde su cierre. `barrer()` avisa con O-42 o, si `juicio`, con O-44 (ALTA), con el número de meses en el motivo. Sigue sin repetirse en cada barrido.
- **H-14:** regresiones para los cuatro mutantes:
  - el mes de inicio en UTC en el borde;
  - `comparacion_sombra_pendiente` no salta en el último instante del mes;
  - la tolerancia relativa con 1e-9 unidades;
  - `estado_sombra` con un resultado infinito da None.
- **H-15:** Documento 0 V0.71 y V0.75, LEEME y deuda al día. Los límites están en T-86 y T-02.
- **H-16:** la descripción de MIG-009 declara que las comparaciones de la V0.71 se conservan como históricas, con sus reglas.

**Decisiones:**
- En real, robot y sombra se dividen por la misma inflación, así que el veredicto coincide con el nominal. Se informa la cifra real (D-30).
- La sombra no paga impuestos ni comisiones de compra: es el plan pasivo de referencia.

**Límites (H-07 y H-09):**
- El precio del índice, la inflación y el valor del robot que declara I no se contrastan con K, que no existe aún (T-86). La primera comparación fija el índice de precios del inicio.
- `gasto_dia` no está encadenado.
- El capital inicial no se compara con el de la cartera real.
- Vaciar el registro reinicia el plazo, el límite conocido de las cadenas sin ancla externa (T-02).
