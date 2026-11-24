# T-200 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-24 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho:**
  - H-01 está corregido con la doble comprobación de `revisores/r03_correccion_propuesta.diff`.
  - Hay una prueba de regresión equivalente a r05 en `test_t200.py`.
  - M7 y M9 están adaptados, y M10 y M11 son nuevos: 11 mutantes, todos muertos.
  - r05 sale con 0 y r04 no deja fugas.
  - En r06, Q5 y Q6 siguen vivos: son los equivalentes.
  - Comentario de `_acuses`, README (Diseño, CA-5), análisis y pruebas actualizados.
- **Cuidado con:** Q3 de r06 ya no se aplica: su texto lleva la sangría de la r01 y el `assert` del script lo detiene. No se
  ha cambiado el script del revisor; Q3 está como M11 en `mutantes.py`.
- **Commit:** «T-200 r02: …», encima de `4b33dbc8`, sin push.

## 2026-11-24 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:** `Mensajeria._acuses` crea, comprueba y migra la tabla de acuses en una sola transacción `BEGIN IMMEDIATE`; si
  algo falla, cierra la conexión (la transacción se deshace) y relanza el mismo error. Cuatro pruebas (cinco casos) en
  `bloque_a/11_Ejecutor/tests/test_t200.py`, nueve mutantes muertos en `mutantes.py`.
- **Falta:** la QA. Commit local en `wip/t200`, sin push.
- **Cuidado con:**
  - La prueba de concurrencia lanza 8 procesos `python -c` que importan `bloque_a`; cada ronda espera a que los 8 digan
    «listo» y entonces les da la orden a la vez. Con develop falla 10 de 10 ejecuciones en los dos casos (nuevo y antiguo).
  - Se eligió `BEGIN IMMEDIATE` y no `almacen._transaccion()`: motivo en `analisis-tecnico.md` («Decisiones»). Un
    `BEGIN DEFERRED` no vale con un almacén antiguo (M2).
  - La prueba de `wip/t196` que llama a `mensajeria._acuses().close()` antes de su prueba de hilos no se ha tocado.
  - Sin caso del plan: el mapa y las evidencias no cambian.
- **Scripts útiles:** `.docs/tickets/T-200/mutantes.py`.
