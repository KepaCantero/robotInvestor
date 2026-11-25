# T-201 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-25 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho:** H-01 a H-04 corregidos, cada uno con su prueba (tabla en `analisis-tecnico.md`, «Ronda r02»).
  - **H-01:** `comparar.py` normaliza solo las rutas, las dos latencias por su nombre exacto (`latencia_s`, `tiempo_respuesta_s`) y la columna `latencia_s` de `consumo.csv`, y los resúmenes encadenados; ningún instante. `equivalencia.sh` lanza el testigo `sensibilidad.py`.
  - **H-02:** el caso de flotantes de `acierto_direccional`.
  - **H-03:** el mensaje de `ruta` («… o es null») y sus tres límites.
  - **H-04:** las cifras de `referencia/` con las dos medidas.
- **Comprobado:** 38 pruebas en `tests/test_t201_cuotas.py`; `revisores/r04_mutantes.py`, ver `pruebas.md`; equivalencia EQUIVALENTE y «puntos ciegos: ninguno» (también con `revisores/r02_sensibilidad_equivalencia.py`).
- **No se toca:** el defecto de `b_agente`, que va a un ticket propio.
- **Commit:** «T-201 r02: …», encima de `67a52fd0`, sin push.

## 2026-11-24 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - La cuota de mypy de A baja de 102 a 67 y la de ruff de 2806 a 2797, sin cambiar ningún comportamiento.
  - Los envoltorios de HT-02, HT-03, HT-07 y HT-09 importan la copia por su ruta de paquete solo para mypy (`TYPE_CHECKING`). Así se quitan sus `import-not-found` y los 19 `attr-defined` de sus usos, también en ficheros que no se tocan.
  - Se corrigen los errores de tipos de `seguimiento.py`, `configuracion.py`, `backtest.py`, `motor/servicio.py`, `motor/operaciones.py` y `motor/evaluacion.py`.
  - 35 pruebas en `tests/test_t201_cuotas.py` y una prueba de equivalencia de salidas frente a `origin/develop` (`equivalencia.sh` + `comparar.py`), en lugar de mutantes.
- **Lo que queda fuera:**
  - Los 53 errores de `herramientas/referencia/`, que son deuda del corpus (decisión del operador del 16-11-2026). El objetivo de T-201 cambió por eso; ver el README.
  - Las 6 líneas de `orquestacion.py`, que está en la PR 3 de Astra y en T-196.
  - Los `import-untyped`, que lleva T-202.
  - `yfinance`, que es un extra opcional sin instalar.
- **Cuidado con:**
  - **El único cambio observable** es el mensaje del `TypeError` de `configuracion.ruta` cuando falta la clave.
  - **`b_agente`** conserva su defecto silencioso (AG-03), anotado como observación en INC-T201-01.
  - **La equivalencia** (r01) normalizaba rutas, latencias, instantes y resúmenes encadenados. La QA r01 vio que eso escondía cambios de dominio (H-01); desde la r02, solo rutas, las dos latencias y los resúmenes (`pruebas.md`).
  - **`tools/cuotas.txt`** lo bajan también T-202 y T-203: el conflicto se resuelve al integrar.
- **Commit:** local en `wip/t201`, sin push.
- **Scripts útiles:** `.docs/tickets/T-201/equivalencia.sh .` (desde la raíz de la copia, unos 75 s).
