# T-206 · Traspaso

Este fichero solo existe si el trabajo cambia de manos. Hay una sección por traspaso, con la más reciente arriba.

## 2026-11-25 · de claude (implementador, ronda de cierre) a la QA r01 (el mismo revisor)

- **Fase en la que se entrega:** ronda de cierre de la QA r01, que dio APTO pendiente de cierre con H-01 a H-06, todos bajos.
- **Hecho:** rebase sobre `6c8910c1`, con T-205, y los seis hallazgos corregidos tal como dice el `qa.md`, cada uno con su prueba. La tabla está en `analisis-tecnico.md`, «Ronda de cierre».
  - H-02: tipo exacto `str`.
  - H-03: `categoria` solo en la pareja OTRO con DATOS, y el lector la exige.
  - H-04: `_comprobar_reserva` comprueba toda INC- de HA.
  - H-05: `_conserva` en las ocho `test_ca3_*` y los diez mutantes en `mutantes.py`.
  - H-06: README, comentario y `categoria` en `estado`.
  - H-01: gate completo sobre el commit de cierre y evidencias regeneradas.
- **Resultado:**
  - `test_t206`: 52 casos;
  - `mutantes.py`: 41 muertos y ningún equivalente;
  - `r01_01`: 0 HALLAZGO;
  - `r01_02`: 24 muertos y Q3 vivo, equivalente (0 vivos no equivalentes);
  - `r01_03`: OK;
  - equivalencia con develop: EQUIVALENTE;
  - gate: en `pruebas.md`.
- **Cuidado con:**
  - Tus scripts de `revisores/` se adaptaron en tres puntos donde tu corrección choca con su montaje: el rechazo de §2, el HA antiguo de §4 y de `r01_03`, y el anclaje de Q4 y Q5. El diff exacto está en `cierre_adaptacion_revisores.diff`, y las comprobaciones no cambian.
  - `revisores/` y `qa.md` estaban sin commit en esta copia. Entran ahora en el commit de cierre.
  - La cabecera de las evidencias cita `786ad26a`, el commit r01 rebasado y padre del de cierre, porque el script toma HEAD.
- **Commit:** «T-206 cierre: …», local, sin push.

## 2026-11-25 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - `Almacen.incidencia` y `_incidencia_interna` fallan cerrado ante un tipo fuera del enumerado de 4.8 del esquema de HA, con `TipoIncidenciaNoAdmitido`. Lo hacen antes de pedir el identificador, así que no escriben nada.
  - Los ocho sitios que escribían DATOS escriben OTRO con `categoria` DATOS, a través de `incidencia_de_datos`.
  - `es_incidencia_de_datos` reconoce las INC- de antes y las de ahora.
  - Hay 35 pruebas en `tests/test_t206_tipo_incidencia.py`. Ocho ficheros de pruebas que miraban `tipo == "DATOS"` usan ahora el lector.
  - Hay 20 mutantes: 19 muertos y uno equivalente, M4, explicado en `mutantes.py`.
- **Falta:** la QA. Es un commit local en `wip/t206`, sin push.
- **Cuidado con:**
  - Las decisiones `[PROPUESTO]` de INC-T206-01: OTRO y no HERRAMIENTA, el campo `categoria` y el lector doble.
  - El límite declarado: `Almacen.escribir`, la escritura genérica, no comprueba el tipo de una INC- montada a mano. Ningún módulo lo hace, y la prueba estática solo cubre `incidencia` y `_incidencia_interna`.
  - `orquestacion.py` e `interfaz_broker.py` solo cambian en el literal, `incidencia("DATOS", ` → `incidencia_de_datos(`, con la misma longitud. El PR 3 de Astra, ahora parado, también los cambia. `seguimiento.py` no se toca: lo cambia T-205, que usa OTRO.
  - Sin el cambio, el módulo de pruebas ni siquiera importa. Con los nombres nuevos sustituidos en la propia prueba, fallan 25 de los 35 casos, como se ve en `pruebas.md`. Los 10 que pasan comprueban lo que ya era cierto antes o lo que aporta la sustitución: cada tipo del esquema se escribe, el enumerado frente al esquema, el lector y la deduplicación de F9 con un HA antiguo.
- **Scripts útiles:**
  - `.docs/tickets/T-206/mutantes.py`;
  - `.docs/tickets/T-201/equivalencia.sh <copia> origin/develop`, que compara la secuencia mock con develop.
