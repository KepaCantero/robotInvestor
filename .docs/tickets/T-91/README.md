# T-91 · Bloque A: resolución de pronósticos con los festivos de PS2 y las series alineadas (H-26 a H-29 de la QA r05 de T-65)

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `bloque_a/11_Ejecutor` (`evaluador.py`, `calendario.py`, `sintesis.py`, `backtest.py`) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (regla del operador del 12-11-2026) |
| Aprobación del operador | 2026-11-12: está en el orden de tareas obligatorias para evaluar el Bloque A por separado |
| Deuda técnica | T-91 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los cuatro hallazgos bajos de la QA r05 de T-65 (`.docs/tickets/T-65/qa.md`, «Ronda r05») antes del modo sombra con API. Así la resolución de los pronósticos:
- no pierde muestra en los cierres de dos días;
- mide el suceso pronosticado sobre la misma ventana en las dos series;
- deja la regla escrita donde se congela.

## Alcance

- Entra:
  - **H-26:** `motivo_no_fresca` y `bases_cesta` cuentan las sesiones de H1 con los festivos de `ps2_festivos`, con la misma función que PS2 (ahora en `calendario.py`);
  - **H-27:** si proxy y referencia (o los miembros de la CESTA) acaban en fechas distintas, todos se miden hasta la más antigua; la regla, `[PROPUESTO]` en INC-T91-01, con su pregunta para T-57;
  - **H-28:** el criterio y la regla de respaldo que se congelan en cada PRG nuevo dicen la regla; `pronosticos.csv` saca `fecha_dato_proxy` y `fecha_dato_referencia`; el README del ejecutor recoge la regla y corrige lo de `fecha_publicacion`;
  - **H-29:** pruebas para las tres partes de la corrección de H-24 que sobrevivían a mutaciones.
- No entra: el plazo de NO_RESOLUBLE (`evaluacion.dias_habiles_no_resoluble`), que sigue en días hábiles sin festivos, ni los PRG ya congelados, que conservan su texto.

## Diseño

- Contratos: ninguno. `pronosticos.csv` gana dos columnas al final; las anteriores siguen en su sitio.
- Estado persistido: no cambia de forma. Los PRG nuevos llevan otro texto en `criterio_resolucion` y `regla_fallback`.
- Números: ninguno nuevo; se usan `ps2_antiguedad_maxima_dias` y `ps2_festivos` del Anexo A y de la configuración.
- Cómo falla cerrado: una serie que no sirve sigue dejando el pronóstico en espera. Si, al medir hasta la fecha común, una serie no tiene dato posterior a la emisión, también espera.

## Criterios de aceptación (binarios)

1. CA-1: los casos de Navidad y Pascua de `r05_01` F (último dato antes del cierre) se resuelven con H1, y sin festivos no.
2. CA-2: con la referencia parada dentro de la tolerancia, proxy y referencia se miden hasta la misma fecha, y la CESTA mide sus miembros hasta la más antigua.
3. CA-3: el criterio congelado y el README dicen la regla; `pronosticos.csv` lleva las dos fechas.
4. CA-4: las mutaciones (a), (b) y (c) de H-29 tienen una prueba que falla.
5. CA-5: el gate da 12/12, sin subir cuotas.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t91_resolucion.py` | Regresión, límite y fallo cerrado | CA-1 a CA-4 |
| Suites de resolución y evaluación (`test_t65_*`, `test_t92_*`, integración) | Regresión | CA-5 |
| `./tools/check_all.sh` | Gate | CA-5 |

## Registro

- 2026-11-12 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-12 · EN QA · H-26 a H-29 corregidos; 10 pruebas nuevas
