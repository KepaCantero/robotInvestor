# T-61 · QA independiente

- **Revisor:** Claude, que no implementó el cambio (lo implementó Astra). · **Ronda:** r01 · **Fecha:** 2026-11-09

Revisé primero el plan y el código. Solo después leí `analisis-tecnico.md` y `pruebas.md`, para no heredar los puntos ciegos de quien lo implementó.

## Reproducción desde limpio

- **La rama en una copia limpia** (worktree de `origin/astra/bloque-b-objeciones-y-evaluacion`, con `PYTHONPATH` apuntando a su propio ejecutor para no usar el paquete instalado): **134 pruebas de B en verde**, frente a las 118 de la línea base.
- **Las pruebas nuevas contra el código anterior** (el de `develop` antes de la rama): **13 fallan y 26 pasan**. Las pruebas de regresión detectan, por tanto, los fallos que corrigen.
- **Ejemplo del crítico** (`ejemplos/comparar_critico.py`): dos ejecuciones sin red dan una salida idéntica.
- **Los tres casos manuales** solo difieren en la línea del dato del fabricante.
- **Después de fusionar**, en `develop`: `.docs/scripts/gate.sh` con `--completo` y `.docs/scripts/pruebas_marco.sh` (resultado en el registro del ticket).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| 1. Solo un `True` booleano cierra una objeción fuerte | sí | Pruebas de Astra, y `r01` punto 8: «true», `1`, una respuesta vacía, un no-dict y una respuesta ajena no cierran |
| 2. La ficha llega al seleccionador, que solo responde por sus candidatos; un matiz débil no bloquea | sí | `test_objecion_candidato.py`. En el código, cada lista de respuestas se aplica solo a sus objeciones, y las débiles se aceptan aparte (nunca se envían a los agentes) |
| 3. Una serie ausente o vacía no trunca las demás | sí | Pruebas con archivo ausente, sin observaciones y de cero bytes. `DatosNoDisponibles` se trata de forma explícita y cualquier otro error se propaga: falla cerrado |
| 4. Los periodos solapados no cuentan dos veces | sí | `r01`, puntos 1 a 7: basura descartada, duplicados una vez, encadenadas todas, semanales a 4 semanas 1 de cada 4, independiente del orden y sin certificar con excesos negativos. Selección voraz por fin más temprano, que no depende de los resultados |
| 5. Ejemplos reproducibles sin red | sí | Dos ejecuciones idénticas |

## Invariantes

Se cumplen todos:
- no hay ningún camino a órdenes (B no ejecuta);
- los cambios son deterministas y no meten ningún LLM en los controles;
- los controles se endurecen, no se relajan: cerrar una objeción es ahora más difícil y la certificación más exigente;
- falla cerrado;
- los números salen de la configuración de evaluación, con los mismos valores por defecto que antes;
- no se decide nada del operador;
- no hay secretos ni datos personales: los casos del crítico usan datos ficticios;
- la documentación está al día (README del ejecutor, deuda y ticket).

Las cuotas de ruff y de mypy de B bajan.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `tools/cuotas.txt` | La línea base de pruebas de B debería proteger las nuevas; seguía en 118 | Subir `pytest_bloque_b` (a 141 tras la r02, también en `CLAUDE.md` y en `ri-probar`) | corregido por el revisor en la r02 |
| H-02 | baja | `README.md` de este ticket | La revisión de B con el operador (D-42, regla 9 del §14) no tiene ticket propio; T-61 se presenta como aportación a T-53, que es la revisión de A | Abrir T-62, «Revisión del Bloque B con el operador» | corregido por el revisor (fila en la deuda) |
| H-03 | baja | `evaluador.metricas` | Dentro de una celda se descartan también las ventanas solapadas de peticiones distintas, que podrían ser independientes. Es conservador: puede retrasar un certificado, nunca adelantarlo | Ninguna ahora; revisarlo con el operador en T-62 si los certificados tardan demasiado | abierto, a la deuda (T-62) |
| H-04 | baja | `.docs/memoria/compartida/2026-11-09_bloque-b-objeciones-y-evaluacion.md` | `vigencia: histórica` no es uno de los valores del protocolo de memoria | Usar `vigente`, `sustituida por …` o `caduca …` | abierto, para Astra (la carpeta y la entrada son suyas) |

## Veredicto

**APTO.** Se cumplen los cinco criterios, no queda ningún hallazgo crítico ni alto y las regresiones están demostradas contra el código anterior. Rama fusionada en `develop` por avance rápido.

---

# Ronda r02 · cobertura y comparación con el azar

- **Revisor:** Claude · **Fecha:** 2026-11-09 · **Rama:** `astra/bloque-b-backtesting-cobertura-y-azar` (commit `ddfc734`, sobre la rama de la r01)

## Reproducción desde limpio

- **Copia limpia** con `.docs/scripts/qa_rama.sh` (base: la rama de la r01): se puede fusionar por avance rápido y **B pasa 141 pruebas** con el código de la rama (antes, 134).
- **Ataques propios** en `revisores/r02_ataques_azar.py`: 12 comprobaciones en verde. Cubren:
  - el universo sin selección o incompleto: sin precio, con NaN o infinito, o con un elegido ajeno;
  - la enumeración exacta: 15 grupos, 14/15 superados y 1/15 empatado;
  - el muestreo determinista con semilla de texto, que no depende de `PYTHONHASHSEED`;
  - los descartes por índice replicado y por emisor en RF.
- **Después de fusionar**, en `develop`: `.docs/scripts/gate.sh` con `--completo` y `.docs/scripts/pruebas_marco.sh` (resultado en el registro del ticket).

## Lo que pedía el traspaso

| Punto | Cumple | Evidencia |
| --- | --- | --- |
| El universo del sorteo se fija en la fecha de selección, con los admitidos por HT-03 | sí | `universo_azar` toma `top_n`, `alternativas` y `resto_secundarios` de la selección de esa fecha, en los dos modos (en el completo lo guarda en F3 al entregar). Las rentabilidades solo se usan después para medir |
| Mismo tamaño y mismas restricciones que la selección original | sí, con H-06 | Índice replicado, correlación con la misma tesis, subclúster y emisor en RF: las reglas de `ht03.seleccionar` tal como lo llaman hoy B y el backtest |
| Empates y periodos con precios ausentes | sí | Los empates se cuentan aparte (la propia selección empata consigo misma en el modo exacto). Si falta un precio del universo, estado `universo_incompleto`, sin porcentaje: falla cerrado |
| Recuentos de elegidos y evaluados, y desfase del último cierre | sí | `n_top_elegidos`, `n_top_evaluados`, `n_top_sin_precios`, `fecha_precio_final` y `dias_desfase_precio_final` en los CSV. Media aparte de los periodos con selección completa |
| Las optimizaciones conservan los resultados | sí | Vencimientos calculados una vez por fecha, una sola lectura de F3 y pesos racionales en el bootstrap (`calcular_S` ya trabaja en fracciones exactas). Las pruebas anteriores siguen en verde |

## Invariantes

Se cumplen todos:
- B no tiene camino a órdenes;
- es determinista y no usa LLM;
- falla cerrado;
- las semillas se derivan del ámbito, la fecha, el tipo y el horizonte, sin números escritos en el código;
- no hay datos personales ni secretos;
- el README del ejecutor está al día.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección | Estado |
| --- | --- | --- | --- | --- | --- |
| H-05 | baja | `backtest.py`: `comparar_azar(..., ent.cfg["evaluacion"]["bootstrap_replicas"], ...)` | El número de grupos del sorteo reutiliza el parámetro de réplicas del bootstrap. Está documentado, pero según D-45 cada parámetro nuevo lleva su propio valor por defecto y su pregunta | `evaluacion.grupos_azar`, con 1.000 por defecto | abierto, a la deuda (T-62) |
| H-06 | baja | `revisores/r02_ataques_azar.py`, punto 8 | `comparacion_azar` lee las reglas de diversidad de `PARAMETROS_POR_DEFECTO` y siempre aplica el límite de subclúster. Coincide con cómo se llama hoy a HT-03 (sin parámetros y sin `ambito_es_subcluster`), pero dejaría de coincidir si la selección se llamara con parámetros propios o con un ámbito que sea un subclúster | Guardar en `universo_azar` las reglas efectivas de la selección | abierto, a la deuda (T-62) |
| H-07 | baja | `handoff.md` de este ticket | Las mejoras de backtesting son una tarea nueva, posterior a T-61, pero no tienen ticket propio | Ninguna ahora (se revisan aquí como r02); en adelante, un `T-NN` por tarea | anotado |

## Veredicto

**APTO.** Se cumple todo lo que pedía el traspaso y no queda ningún hallazgo crítico ni alto. Rama fusionada en `develop` por avance rápido.

