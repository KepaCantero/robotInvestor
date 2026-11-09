# Implementación · Astra · 9 de noviembre de 2026

El origen fue el trabajo local del Bloque B sobre c83b211. Se comprobó que la revisión 104f4c8 conservaba la base de los archivos afectados. Se incorporaron los cambios después de reproducir los fallos con las pruebas nuevas.

| Archivos del ejecutor | Cambio |
| --- | --- |
| bloque_b/orquestacion.py | Resolución booleana estricta, ficha del candidato en el encargo, alcance de la respuesta por agente y aceptación del matiz débil. |
| bloque_b/backtest.py | Identificación del símbolo sin serie, conservación del horizonte del resto y resultado de certificación por tipo. |
| bloque_b/evaluador.py | Cálculo compartido para certificar con ventanas de rendimiento (inicio, fin] sin solapamiento y con ambas métricas disponibles. |
| tests/test_v21_capas_consultas_seguimiento.py y tests/test_objecion_candidato.py | Efectos de las objeciones en la entrega completa y en el candidato correspondiente. |
| tests/test_datos_backtest.py y tests/test_certificacion_ranking.py | Cobertura de precios ausentes, observaciones sin fecha, ventanas consecutivas y periodos superpuestos. |
| ejemplos/comparar_critico.py y ejemplos/casos_critico/ | Ensayo pareado reproducible y tres casos manuales con su guía separada. |
| README.md | Interpretación de los intervalos y uso de los ejemplos. |

Ajustes de integración: orden de importaciones, anotación de tipos y fijación del valor de la variable capturada en la prueba pareada. Se redujeron las cuotas globales de Ruff de 3490 a 3488 y de mypy para B de 160 a 159 conforme a la medición del control oficial. Se conservaron las cuotas de A y Forex.

## Cómo comprobar el cambio

Desde la raíz, con el entorno del proyecto activo:

```sh
python -m pytest -q bloque_b/11_Ejecutor/tests
./tools/check_all.sh
(cd bloque_b/11_Ejecutor && PYTHONPATH=. python ejemplos/comparar_critico.py)
```

## Límites

Una respuesta bien tipada puede contener una afirmación sin justificar. Los ensayos con respuestas simuladas miden cómo circulan los datos. La eficacia del crítico real sigue abierta. El muestreo estadístico evita volver a usar el mismo intervalo de rentabilidad; periodos disjuntos aún pueden pertenecer al mismo régimen de mercado. Los registros históricos ya emitidos conservan su contenido. Los CSV corruptos con errores de formato quedan fuera del caso de archivo ausente o sin observaciones.
