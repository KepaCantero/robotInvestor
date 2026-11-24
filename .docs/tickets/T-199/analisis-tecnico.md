# T-199 · Análisis técnico

## Causa raíz

- **El fallo del 18-11-2026.** El log del gate (el `commit_limpio_gate_20261118_122103.log` de la carpeta de logs local de `.docs/scripts`, que no se sube) solo guarda el resumen: 1 fallo de 8 266, en la prueba de T-165, a los 52 min de suite. Esa prueba ya medía `process_time` desde su r06, así que no fue el reloj: fue el margen. Compara 2 000 y 8 000 unidades de texto (lineal: ×4) con un tope de ×6, y una sola medida de cada tamaño.
- **Reproducido.** Con 6 millones de objetos vivos en el proceso (como a mitad de suite) y la máquina cargada (8 procesos de CPU y 4 de copia de memoria en 4 núcleos, carga ≈ 18), 15 medidas de la prueba de `develop` dan razones de 1,8 a **5,97**. Con la máquina libre y el mismo montón: 2,0 a 5,6. Tres efectos:
  1. El recolector de basura: una pasada de la generación 2 recorre todo lo vivo en el proceso, que depende de las pruebas anteriores, no del texto. Cae en uno de los tamaños y no en el otro.
  2. La carga compartida: con la caché y la memoria disputadas, el tiempo de CPU también sube, y más en el texto largo (232 KB) que en el corto.
  3. Una sola medida de 20–150 ms por tamaño: cualquier ráfaga entra entera en la razón.
- **Las otras once.** Medían `perf_counter` (reloj). Con la carga de esta máquina pasan solas (los topes absolutos tienen de 5 a 200 veces de margen), pero el reloj cuenta el tiempo en que el proceso espera la CPU: con más carga que la de hoy, o una pausa de la máquina virtual, caen sin que el código haya cambiado. Es lo que T-168 vio con `test_r05_h37` (2,4–2,9 s frente a 2 s).

## Por qué CPU y no contar operaciones

El encargo da tres caminos: CPU, contar operaciones o dejarla. Contar llamadas no ve los defectos que vigilan estas pruebas: el retroceso de una expresión regular ocurre dentro de una sola llamada a `re`, un bucle numpy n²·T es una llamada por tramo y un repaso del prefijo hace una llamada por bloque, cada una más cara. Un contador tendría que medir caracteres recorridos dentro de `re`, y eso no existe sin cambiar producción. `process_time` mide justo lo que importa (el trabajo del proceso) y no cuenta la espera.

`process_time` suma todos los hilos del proceso. OpenBLAS podría repartir una operación en 4 hilos y contar 4 veces: medido, ninguna de estas pruebas lo hace (CPU ≈ reloj sin carga: T-144 9,8 s frente a 10,1 s; SIM-MC 0,30 frente a 0,32).

## Implementación

- `bloque_a/11_Ejecutor/tests/tiempo_cpu.py` (nuevo, no lo recoge pytest: no empieza por `test_`):
  - `medir_cpu()`: gestor de contexto; para el recolector (si estaba activo) y lo vuelve a activar en `finally`; deja los segundos de CPU en `m.segundos`.
  - `cpu(f)`: lo mismo para una función.
  - `minimos_intercalados(f, g, repeticiones=3)`: a, b, a, b, a, b; la mínima de cada una.
- Pruebas de tope absoluto (diez, más las 21 de `_rapido`): `perf_counter` → `medir_cpu`/`cpu`, mismo tope y mismo tamaño.
- Pruebas de razón:
  - `test_t130_r8::test_h08_coste_lineal`: mínima de tres intercaladas; mismos tamaños (50 000 y 200 000) y topes (×10 y 3 s).
  - `test_t165_g3_met13::test_coste_lineal…`: mínima de tres intercaladas, 1 000 → 8 000 unidades, tope ×16 en la r01 (×12 en la r02), el suelo de 0,02 s de antes (INC-T199-01). Con 2 000 → 8 000 y la mínima intercalada, la razón con carga llegó a 4,94: el margen sobre el tope de 6 quedaba en 1,2. Con ×8, la máxima medida es 9,63 (margen 1,66) y un cuadrático da ×64.
- `test_t92_revision.py`: además, la línea en blanco que ruff pedía entre los imports de `test_r03_h26_formatos_genericos` (I001, ya estaba). Cuota de ruff 2807 → 2806.
- Corpus: ninguno de los diez ficheros, ni el nuevo, está en `tools/corpus_manifest.txt` (solo lo están las pruebas de `10_Herramientas`).

## Coste en la suite

El de las pruebas de razón sube: T-165 de 1,5 s a unos 3,6 s de CPU (tres medidas de cada tamaño) y T-130 de 0,6 s a 1,8 s. El resto, igual.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Causa | Corrección | Prueba |
| --- | --- | --- | --- |
| H-01 (media) | «El mismo exponente» solo vale para una potencia pura de n. El defecto real es b·n + a·n²: con ×8 y tope 16 hacía falta un cuadrático de 1,33 veces el lineal para fallar (`develop`: 0,8) | tope 12: ×1,5 de lo lineal, falla desde 0,62 | M14 y M15 mueren; `r01_01` con B = 120 000 y 160 000; `razon_t165.py 1000` con carga: 8,94 < 12 |
| H-02 (baja) | M13 no es equivalente: cuesta hasta 2 520 evaluaciones por contraste, pero cabe en el tope de tiempo | prueba nueva que cuenta `_potencia_t` (`monkeypatch`, sin tocar producción) | M12 y M13 mueren por el recuento; `r01_03` contra `r01_02` y la prueba nueva |
| H-03 (baja) | la orden no buscaba `.wait(` ni `Event` | orden corregida; filas nuevas en el inventario | la salida de la orden, cubierta línea a línea |
| H-04 (baja) | T-102 medía CPU con el recolector activo | `medir_cpu` en las cuatro, mismos topes | M16–M19 (retroceso Q4, Q1, Q2 de T-168) mueren con carga |
