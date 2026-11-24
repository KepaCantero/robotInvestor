# T-199 · Pruebas

Todo desde `bloque_a/11_Ejecutor`, sin red ni coste, con el `.venv` del proyecto. Máquina de 4 núcleos.

## Recuento

No se añaden ni se quitan pruebas: A sigue con las mismas (el gate exige ≥ 607), A-Forex 68 y B 174. `tests/tiempo_cpu.py` es un módulo auxiliar (no empieza por `test_`).

## Ronda r02 (QA r01 NO APTO: H-01 a H-04)

Carga artificial de la r02: `carga.sh 8 4 1800`, carga de 11,6 a 20 en 4 núcleos (salidas en el espacio temporal de la sesión).

### H-01 · T-165 con tope 12

- `test_t165_g3_met13::test_coste_lineal…`: `largo < 12 * max(corto, 0.02)` con 1 000 → 8 000; el docstring da los umbrales de cuota cuadrática (0,62 frente a 0,8 de `develop`). INC-T199-01 corregida.
- `mutantes.py M14 M15` (re-escaneo de bloques de 120 000 y 160 000), con carga: **los dos MUERTOS**. «ST-DESC-001 implementado»: 0,030 s → 0,398 s (×13,1 > 12) y 0,031 s → 0,436 s (×14,0). Sin carga artificial: ×12,5 y ×14,7.
- `revisores/r01_01_umbral_t165.py 120000 160000`, con carga: razones T-199 de 6,89 / **12,14** / 11,48 (B = 120 000) y 3,86 / **15,86** / **14,43** (B = 160 000). Con el tope 12, los dos mueren. El script marca con «*» su tope antiguo de 16. **B = 120 000 queda cerca del umbral** (12,1–13,6 según la medida): es justo el cuadrático de 0,6 veces el lineal que el tope está pensado para ver.
- `razon_t165.py 1000`, con carga 18–20: peor razón 8,94 con la mínima intercalada (10,75 con una sola medida). Margen sobre el tope 12: 1,34.

### H-02 · ST-INF-001 por recuento

- Nueva `test_fase2_series::test_st_inf_la_busqueda_del_n_minimo_empieza_en_la_aproximacion` (la de `revisores/r01_02`, dentro de la suite). Cuenta las llamadas a `_potencia_t` con `monkeypatch`: como mucho 1 con d = 0,05 y 1e-300, y 20 con d = 0,06. El contador corta a las 50.
- `mutantes.py`: M12 y M13 van contra la prueba nueva y la de tiempo, y se quita la excepción de M13. **M12 MUERTO (4 s)** y **M13 MUERTO (5 s)**: «más de 50 evaluaciones de la potencia (d = 0.05)». M12 tardaba 17 min por tiempo.
- `revisores/r01_03_mutantes_contra.py M12|M13` contra la prueba nueva y `r01_02`: **los dos MUERTOS**.
- La frase del README «Contar operaciones no sirve aquí» se corrige: sirve en ST-INF-001.

### H-03 · Inventario

Orden corregida, con `.wait(` y `Event`:

```
grep -rnE "perf_counter|monotonic|process_time|time\.time|datetime\.now|\.sleep\(|timeout|Barrier|\.join\([0-9]|\.wait\(|Event\b" \
  --include=*.py bloque_a/11_Ejecutor/tests bloque_a_forex/11_Ejecutor/tests bloque_b/11_Ejecutor/tests
```

Salida (sin `tiempo_cpu.py`): A-Forex y B, nada. Cada línea de A está en la tabla del README:
- T-151 y T-154: `timeout` simulado.
- T-147, T-149 y T-150: `falso(url, timeout=None)`.
- T-106: `time_ns`.
- T-87 contratos: `Event`, `wait(10)` ×2 (nueva fila).
- T-178: `Barrier(timeout=3)`.
- T-177: `subprocess timeout=600`, `Barrier(2)` y `wait(timeout=30)`, `join(60/120)`.
- T-174: `Barrier`, `wait(timeout=60)`, `sleep(0.3)` y `join(900)`.
- T-146: `Event` y `wait(600)` (nueva fila).
- T-157 y V51: `subprocess timeout`.
- T-169 y T-176: `Barrier(n)` sin plazo (nueva fila).
- T-87 controles: `proc.wait(30)`.
- T-65: `Event`, `wait(30)` (nueva fila) y `join(60)`.

Ninguna línea queda fuera de la tabla.

### H-04 · T-102 con `medir_cpu`

- Las cuatro pruebas de tiempo de `test_t102_filtro.py` usan `medir_cpu`, con los mismos topes; sale el `import time`. CPU sin carga artificial (carga natural 8), tres pasadas:
  - `textos_largos`: 0,48–0,56 s, tope 2 (×3,6).
  - `r04`: 0,19–0,26 s, tope 2 (×7,7).
  - `r05_h37`: 0,98–1,11 s, tope 2,0 (×1,8).
  - `r06_h45`: 0,09–0,10 s, tope 1,0 (×10).
- Mutantes de retroceso de la QA r01 de T-168 (Q4, Q1, Q2), como M16 a M19 en `mutantes.py`, con carga: **los cuatro MUERTOS**. `textos_largos` da 52,4 s < 2; `r04`, 20,5 s < 2; `r05_h37`, 22,5 s < 2,0; `r06_h45`, 4,75 s < 1,0.

### Todo junto

- `mutantes.py . --originales`, sin carga artificial (carga natural 4–8): las 17 originales pasan y **M01 a M15 están MUERTOS**, con `exit 0`. Con carga 11,6–20: las 17 originales pasan y M14 a M19 están MUERTOS.
- Tanda estrangulada al 10 % con carga 18–19 (la de `r01_05`, más las cuatro de T-102 y la nueva de ST-INF): **17 de 17 pasan** en 186 s.
- Recuento: A suma 1 prueba (la de ST-INF-001); A-Forex y B no cambian.
- ruff: 2806, igual (la corrección de imports de `test_t102_filtro.py` no deja hallazgo nuevo); cuota 2806.

### Gate (r02)

`./tools/check_all.sh`, lanzado con `setsid nohup` y con su log propio (`gate_t199_r02.log`, en el espacio temporal de la sesión), con otros gates en la máquina: **12/12 en verde, `exit 0`**. pytest A 8 360 (una más que en la r01: la de ST-INF-001), A-Forex 68, B 176; ruff 2806 con la cuota 2806; mypy sin cambios.

## CA-1 · Inventario

```
grep -rnE "perf_counter|monotonic|process_time|time\.time|import time|datetime\.now|\.sleep\(|timeout|Barrier|\.join\([0-9]" \
  --include=*.py bloque_a/11_Ejecutor/tests bloque_a_forex/11_Ejecutor/tests bloque_b/11_Ejecutor/tests
```

A-Forex y B: nada (solo `datetime`/`timedelta` de datos). A: las doce pruebas que medían coste, todas pasadas a CPU, y las esperas, que se quedan. La justificación de cada una está en la tabla de `README.md`. Después del cambio, `grep -rn perf_counter` en las tres carpetas de pruebas no encuentra nada.

## Carga artificial

- **Carga** (`.docs/tickets/T-199/carga.sh 8 4 5400`): 8 procesos `while True: pass` y 4 procesos numpy que copian 256 MB en bucle (memoria disputada), durante 90 min. Carga media de 13 a 20 en 4 núcleos.
- **Estrangulamiento** (`.docs/tickets/T-199/estrangular.py 0.1 -- <orden de pytest>`): deja correr el proceso de pytest solo el 10 % del tiempo (SIGSTOP/SIGCONT en ciclos de 100 ms), como una máquina con diez veces más trabajo que núcleos. El tiempo de CPU del proceso no cambia; el de reloj se multiplica por 10.

## CA-2 · Pasan con la máquina cargada

| Prueba | `develop`, con carga (×3) | `develop`, con carga y estrangulada | T-199, con carga | T-199, con carga y estrangulada |
| --- | --- | --- | --- | --- |
| `test_t123…::test_el_coste_es_lineal` | pasa | **falla** | pasa | pasa |
| `test_t92…::test_r02_h17…` | pasa | pasa | pasa | pasa |
| `test_t103…::test_r02_h47…` | pasa | **falla** | pasa | pasa |
| `test_t130_r8::test_h08_coste_lineal` ×3 | pasa | **falla** (`4111`: largo 3,05 s > 3) | pasa | pasa |
| `test_t113…::test_h56…` | pasa | **falla** | pasa | pasa |
| `test_t113…::test_r02_h01_lineal…` | pasa | — | pasa | pasa |
| `test_t113…::test_r02_h01_la_misma_lista…` | — | — | pasa | pasa |
| `test_t165…::test_coste_lineal…` | pasa | — | pasa | pasa |
| `test_t144::test_h03…` | — | — | pasa | — |
| `test_fase2_riesgo::test_la_ficha_mas_cara…` | pasa | pasa | pasa | pasa |
| `test_fase2_series::test_cota_de_cada_parametro_de_tamano` | pasa | — | pasa | — |
| `test_fase2_series::test_st_inf_n_minimo…` | pasa | — | pasa | pasa |

`develop` estrangulada: 4 fallos de 8. T-199 estrangulada y con carga: 12 de 12 en 266 s.

**T-165 en las condiciones del gate.** Solo falla a mitad de la suite (8 266 pruebas en el mismo proceso), así que se reprodujo con 6 millones de objetos vivos, con carga y en 15 medidas de cada unidad de texto (`.docs/tickets/T-199/razon_t165.py 2000` y `… 1000`):

| Medida | Razón máxima | Tope |
| --- | --- | --- |
| `develop` (una medida, 2 000 → 8 000) | **5,97** | 6 |
| mínima de 3 intercaladas, 2 000 → 8 000 | 4,94 | 6 |
| T-199 r01 (mínima de 3 intercaladas, 1 000 → 8 000) | 9,63 | 16 |
| T-199 r02 (ídem, `razon_t165.py 1000` con carga 18–20) | 8,94 | **12** |

## CA-3 · Mutantes, con la máquina cargada

`../../.venv/bin/python ../../.docs/tickets/T-199/mutantes.py . --originales`, con la carga de arriba: las doce originales pasan y los doce mutantes de coste mueren por su aserción de tiempo.

| Mutante | Prueba | Resultado (CPU medida frente al tope) |
| --- | --- | --- |
| M01 R8 re-escanea el prefijo cada 15 600 caracteres | t123 | MUERTO: 41,7 s < 10 |
| M02 ídem, cada 1 200 | t92 | MUERTO: 5,8 s < 2,0 |
| M03 ídem, cada 1 000 | t103 | MUERTO: 16,5 s < 2 |
| M04 ídem, cada 2 000 | t130 | MUERTO: largo 6,8 s < 3,0 |
| M05 H-56: cada nivel vuelve a serializar lo de debajo | t113 h56 | MUERTO: 97,9 s < 5 |
| M06 el camino de la lista como lista (profundidad²) | t113 r02_h01 lineal | MUERTO: 40,7 s < 20 |
| M07 H-01: cada contenedor tantas veces como caminos (2²⁶) | t113 r02_h01 misma lista | MUERTO: 635,8 s < 5 |
| M08 G3-MET-13 re-comprueba el prefijo cada 2 400 | t165 | MUERTO: «no está validado»: 0,047 s → 2,62 s (×56 > 16) |
| M09 H-03 de T-144: un par solo sale cuando salen todos (n²·T) | t144 | MUERTO: 641,9 s < 60 |
| M10 SIM-MC suma de nuevo todas las innovaciones en cada paso | fase2_riesgo | MUERTO: 126,8 s < 30 |
| M11 TEM-DIFF-001: la cota de B se comprueba después del bootstrap | fase2_series (cota B) | MUERTO: «rechazo lento» |
| M12 ST-INF-001: búsqueda desde 2 que en cada paso mira los anteriores (cota²) | fase2_series ST-INF | MUERTO: 589,0 s < 2 |
| M13 ST-INF-001: búsqueda lineal desde 2 | fase2_series ST-INF | r01: VIVO. r02: MUERTO por el recuento (H-02, abajo) |

- **Qué es cada mutante.** M01 a M04 y M08 son el defecto típico de T-102 (H-26, H-37): cada tramo nuevo repasa todo lo anterior. El bloque es fijo, así que el coste es n²; vale la centésima parte del texto más corto de la prueba, unas 50 veces el coste lineal a ese tamaño. M05, M07 y M09 son los defectos históricos que vigilan sus pruebas. M06, M10 y M12 son cuadráticos naturales del código. M11 es el defecto que vigilan las 21 pruebas de `_rapido`: validar después de calcular.
- **Límite declarado (CA-3).** Una prueba de tope absoluto solo ve un cuadrático cuyo coste a su tamaño pase del tope (margen, de tope frente a CPU sin mutar: t123 ×13, t92 ×25, t103 ×12, t113 ×11 y ×4, t144 ×7, SIM-MC ×90). Pasa igual que antes de T-199 y que en T-168. Las de razón (t130, t165) ven cualquier cuadrático que domine.
- **M13** (r01) mostraba ese límite en ST-INF-001: una búsqueda lineal de 2 520 evaluaciones cuesta 0,5 s y cabe en el tope de 2 s. La QA r01 (H-02) vio que no es equivalente y que se mata sin medir tiempo, contando evaluaciones de `_potencia_t`. En la r02 muere (ver «Ronda r02»).

## CA-4 · Lo que protege cada prueba

`git diff` de las pruebas: los mismos tamaños y topes. Solo T-165 cambia: en la r02, ×8 con tope 12, más estricta que `develop` (INC-T199-01; la r01 ponía 16, que la debilitaba: H-01). T-130 conserva ×4 de texto, ×10 de tiempo y 3 s.

## CA-5 · Gate y cuotas

- ruff de los tres ejecutores: 2806 (cuota 2807 → 2806: el I001 de `test_t92_revision.py`). mypy no cambia (solo se tocan pruebas).
- `./tools/check_all.sh`: ver abajo.
- Ciclo mock y backtest: no se repiten, porque no cambia ningún fichero de producción (`git diff --stat` solo lista pruebas, documentos y `tools/cuotas.txt`) y la salida es la misma por construcción.
- Evidencias del plan: `.docs/scripts/evidencias_plan_a.py` da 67 pruebas del plan y 344 citadas, todas existen. El mapa no cita ninguna de las pruebas tocadas y este ticket no tiene caso del plan, así que no se regeneran.

### Gate (r01)

`./tools/check_all.sh` (24-11-2026, máquina sin carga artificial): **12/12 en verde**. pytest A 8 359 pasadas (≥ 607), A-Forex 68, B 176; ruff 2806 frente a la cuota 2806; mypy sin cambios. Después del gate solo cambiaron documentos y scripts de la carpeta del ticket: `tools/refs_vivas.py` y el gate de secretos, repetidos, siguen en verde.
