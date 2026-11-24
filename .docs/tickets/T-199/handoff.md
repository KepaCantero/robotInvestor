# T-199 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-24 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho (cada hallazgo con su prueba, detalle en `pruebas.md`, «Ronda r02»):**
  - H-01: T-165 con tope 12 sobre 1 000 → 8 000; M14 y M15 (bloques de 120 000 y 160 000) mueren; INC-T199-01 y el docstring, corregidos.
  - H-02: prueba nueva por recuento de `_potencia_t` en `test_fase2_series.py`; M12 y M13 mueren en segundos; sin la excepción de M13.
  - H-03: `.wait(` y `Event` en la búsqueda; filas nuevas de T-87 contratos, T-146, T-65 (`wait(30)`) y de las barreras sin plazo y los `timeout` simulados.
  - H-04: las cuatro de T-102 con `medir_cpu`, mismos topes y su margen en el README; M16 a M19 (Q4, Q1, Q2 de T-168) mueren.
- **Cuidado con:** M14 (B = 120 000) queda cerca del umbral de 12 (12,1–13,6). Es el cuadrático de 0,6 veces el lineal, justo el que el tope está pensado para ver. `r05_h37` de T-102 tiene el menor margen de la suite (×1,8, el tope de T-168, que no se sube).
- **Commit:** «T-199 r02: …» en `wip/t199`, encima de `d1d7ac4`, sin push.

## 2026-11-24 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:** inventario de las tres suites (`README.md`). Doce pruebas de A pasan a tiempo de CPU sin recolector, con el módulo nuevo `tests/tiempo_cpu.py`. Las dos de razón usan además la mínima de tres medidas intercaladas. Los topes no cambian, salvo T-165: ×8 de texto con tope ×16 (INC-T199-01). Las esperas a hilos y subprocesos se quedan, cada una justificada. Producción no se toca.
- **Pruebas:** con carga artificial y con estrangulamiento del proceso, más 13 mutantes de coste (`mutantes.py`; resultados en `pruebas.md`).
- **Cuidado con:**
  - Las pruebas de tope absoluto solo detectan un cuadrático cuyo coste a ese tamaño pase del tope. Es el límite declarado de CA-3, el mismo de T-168. Los mutantes M01 a M04 y M08 usan bloques de re-escaneo de la centésima parte del texto, unas 50 veces el coste lineal.
  - M13 (búsqueda lineal desde 2 en ST-INF-001) vivía «a propósito» (2 520 evaluaciones caben en 0,5 s). Corregido en la r02 (QA r01, H-02): no era equivalente y ahora lo mata un recuento.
  - M09, M10 y M12 tardan minutos: son los defectos de verdad (n²·T, horizonte², cota²).
- **Commit:** «wip local: T-199» en la rama `wip/t199`, sin push.
