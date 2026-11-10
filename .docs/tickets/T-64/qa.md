# T-64 · QA independiente (T-62, T-63 y T-64)

- **Revisor:** Claude, que no implementó ninguna de las tres tareas. Astra las implementó.
- **Ronda:** r01, 10-11-2026.
- **Alcance:** las tres ramas apiladas: `astra/t62-objeciones-eslabon` (666f4a9), `astra/t63-evidencia-objeciones` (76cdc40) y `astra/t64-fechas-evidencia` (123ff92). Todas salen de `0a865bb`. Se revisan juntas porque T-64 contiene a las otras dos.
- **Script de ataques:** `revisores/r01_ataques_cierre_objeciones.py`. Es una prueba de pytest: se copia a `bloque_b/11_Ejecutor/tests/` y se ejecuta con el `PYTHONPATH` apuntando al ejecutor de la copia.

## Reproducción desde limpio

- `.docs/scripts/qa_rama.sh`, con la rama `astra/t64-fechas-evidencia`, la sacó en una copia limpia y ejecutó la suite de B contra su código, comprobando que `bloque_b.__file__` sale de la copia. Resultado: **167 passed**, frente a 141 en `develop`. Una vez fusionado con `develop`, B tiene 174.
- **Fusión simulada con `develop`:** el código de B no choca. Los conflictos están solo en seguimiento: el diario, las incidencias, la deuda y las cuotas.
- Tras fusionar en `develop`, el gate completo da 12/12 (ver «Fusión»).

## Criterios de aceptación

| Ticket | Criterio | Cumple | Evidencia |
| --- | --- | --- | --- |
| T-62 | La misma objeción, a la tesis o a un eslabón, llega a los candidatos expuestos con su motivo y su estado | sí | `test_objecion_eslabon.py` de Astra; ataque a11: los candidatos expuestos llevan el aviso con `x_eslabon_id` y `x_resuelta: false`, y quedan con `objecion_fuerte_sin_resolver` |
| T-62 | Un eslabón desconocido o ambiguo se rechaza de forma explícita | sí | Ataque a09: la petición queda BLOQUEADO_AUDITORIA, sin entregables |
| T-63 | Sin cita, con una cita inventada o mal formada, la fuerte sigue abierta | sí | Ataques a02: una buena y una inventada, una cadena, una lista vacía y un dict, y ninguna cierra. Ataque a04: `resuelta` con «true», 1 o None no cierra |
| T-63 | Las moderadas y las débiles conservan sus reglas | sí | Ataque a10 |
| T-64 | El cierre exige una fecha de incidente válida y un hecho citado posterior, disponible al corte | sí | Ataque a05: incidente con hora sin zona, futuro, texto o número, y no cierra. Ataque a06: una fuente con `conocible_desde` posterior al corte no se ofrece y no cierra. `test_fechas_evidencia.py` de Astra |
| T-64 | Un cierre anterior al control temporal no se entrega | sí | `test_reanudar_cierre_heredado_sin_fechas` |
| Todos | El contrato de salida y las pruebas de T-61 se mantienen | sí | 167 pruebas de B en verde |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | Ataque a07: una nota de un especialista con `conocible_desde` posterior al corte | **Esperado:** la nota se excluye, porque en backtest sería una fuga, y se declara. **Obtenido:** `orquestacion.py`, en el bucle de notas del informe dimensional, la salta con `continue`. No queda ninguna limitación ni incidencia, y la afirmación desaparece del informe sin rastro | Declarar la exclusión en `limitaciones` o como incidencia, con el especialista y la dimensión | abierto (a la deuda, T-64) |
| H-02 | baja | `tools/cuotas.txt` de la rama | La línea base de B se quedó en 118 (la de su base): no sube a 167 con las 26 pruebas nuevas | Resuelto al fusionar: `pytest_bloque_b=174` (las de la rama más las de `develop`) | corregido |
| H-03 | baja | Fila T-62 de la deuda en `develop` frente a la de la rama | Las dos usaban T-62 para cosas distintas: la «Revisión de B con el operador» en `develop` y el alcance por eslabón en la rama | Resuelto al fusionar: la rama conserva T-62 a T-64, y la revisión de B pasa a **T-68**, con las referencias vivas actualizadas | corregido |

**Observaciones sin hallazgo:**
- Un eslabón desconocido bloquea la petición entera, no solo esa objeción. Es lo que pide el plan («rechazo explícito») y falla cerrado. Si resulta demasiado estricto con un modelo real, se puede revisar en T-68.
- Hoy solo son citables las notas fechadas de los especialistas. Los DAT y los cálculos del Motor no traen fechas de fuente, así que no se ofrecen como referencia para cerrar una fuerte. Es conservador y coherente con T-64.

## Sin hallazgo en lo comprobado

- **Una cita duplicada** cierra una sola vez y queda deduplicada en `x_evidencia_respuesta` (a03).
- **Una objeción fuerte a un candidato** sigue la misma regla de fechas que la de un eslabón (a08).
- **Control:** con una nota fechada válida y un incidente anterior, la fuerte se cierra (a01).
- **Las referencias** se filtran por petición y por fecha de corte (`_referencias_contraste`), y las fechas sin zona no fijan el día.

## Veredicto

**APTO** para T-62, T-63 y T-64. Los criterios de aceptación de los tres tickets se cumplen, y la regla de cierre de las objeciones fuertes no se relaja en ningún ataque. H-02 y H-03 se corrigen al fusionar. H-01 es bajo y pasa a la deuda técnica.

## Fusión

Las tres ramas se fusionan en `develop` en un solo merge, porque T-64 contiene a las otras dos. Tras fusionar, el gate completo da 12/12, con B en 174.
