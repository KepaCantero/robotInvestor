# Pruebas · Bloque B · Astra

## Comparación

Sobre la base 104f4c8, B pasó sus 118 pruebas originales. Con las pruebas nuevas y el código original, 12 de los 16 casos seleccionados fallaron y cuatro controles pasaron. Con la corrección pasaron los 16. Se ejecutó con Python 3.12.9 y datos simulados. La dependencia de Anthropic estaba instalada; el SDK falso y la prueba sin clave permiten validar su interfaz localmente.

| Criterio del plan | Evidencia |
| --- | --- |
| 1. Cierre booleano y efecto en la tesis | test_resolucion_de_objecion_fuerte_exige_booleano, test_objecion_fuerte_sobre_la_tesis_en_la_entrega. En el original los textos y el entero 1 cerraban la objeción. |
| 2. Alcance de la respuesta y entrega con un matiz | Los tres casos de test_objecion_candidato.py fallaron en el original. Verifican respectivamente la ficha y el límite individual, el cruce indebido de identificadores y la entrega con una sola objeción débil. |
| 3. Precios ausentes o vacíos | Ambas variantes de test_una_serie_sin_precios_no_trunca_los_otros_rankings fallaron en la fecha final de la evaluación original. Verifican el aviso y el rendimiento de otra empresa. |
| 4. Ventanas comparables | test_certificado_cuenta_periodos_sin_solapar y test_backtest_solo_seleccion. Se verificó el criterio en los dos puntos de entrada. Los periodos consecutivos pueden compartir el precio de frontera. |
| 5. Ejemplos | Dos ejecuciones independientes del par simulado dieron JSON idéntico. Los tres pares posibles de casos manuales difieren en una sola línea. La evaluación humana de las respuestas de dos IA queda pendiente. |

## Reproducción

Activar el entorno del proyecto en una copia de trabajo. Para reproducir la comparación negativa en una copia desechable, conservar las pruebas nuevas y restaurar en **esa copia** las versiones de orquestacion.py, backtest.py y evaluador.py de 104f4c8. Ejecutar el mismo subconjunto antes y después de incorporar el código:

```sh
python -B -m pytest -p no:cacheprovider -q bloque_b/11_Ejecutor/tests -k 'objecion_fuerte or objecion_individual or seleccionador_no_puede or solo_matiz or trunca or certificado_cuenta or backtest_solo_seleccion' --tb=short
python -B -m pytest -p no:cacheprovider -q -rs bloque_b/11_Ejecutor/tests
./tools/check_all.sh
(cd bloque_b/11_Ejecutor && PYTHONPATH=. python -B ejemplos/comparar_critico.py)
```

Para comprobar el marco global se usó una copia temporal de sistema_global/marco_comun_c, ya que algunas suites escriben ejemplos junto al código. El ejecutor comprobó tanto el código de salida de cada script como la línea final «TODAS LAS PRUEBAS PASAN». Se ejecutaron pruebas/ejecutar_pruebas.py y los 49 scripts pruebas/pruebas_*.py, 50 en total. Las pruebas de la tarea no modifican el marco global.

## Resultados finales · 9 de noviembre de 2026

- Control oficial en la copia temporal de la integración: 12 ejecutados, 12 pasaron, 0 omitidos. Corpus de 695 archivos íntegro.
- A: 58 pruebas. A Forex: 68. B: 133 frente a 118 en la misma base antes del traslado.
- Segunda ejecución sobre el ejecutor B del clon de destino: 133 pasaron, 0 omitidas. Hubo 65 avisos de obsolescencia de NumPy en una prueba anterior al cambio; también estaban en la ejecución inicial.
- Cuotas medidas por el controlador del repositorio: Ruff 3488; mypy A 135, Forex 174, B 159.
- En los ejemplos se usó solo el cliente simulado, sin credenciales ni consultas externas. No se incluyeron datos BCE.
- Revisión independiente de Claude pendiente. No se ha emitido el veredicto de QA.
