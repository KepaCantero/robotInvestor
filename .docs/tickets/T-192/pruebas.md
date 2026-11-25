# Pruebas · T-192

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t192_evaluacion.py.

Se introduce una base calculada al día siguiente en un ciclo mock y se comprueba el recálculo posterior. Dos ordenaciones emparejadas de cuatro fechas prueban confirmación y reversión con DM-HLN e idempotencia.

## Ronda r02

La comparación usa la configuración del proyecto y pares con varianza. Trece fechas de tres pronósticos superan el mínimo de 30; nueve quedan por debajo. La prueba de umbral usa un p real del orden de 0,027. Con umbral 0,10 revierte por DM-HLN y con 0,01 por IC medio inferior, tal como dicta la regla con un único objetivo. En F4 se comprueban por separado la fecha de cálculo y la del dato. Hay un tercer pronóstico limpio para asegurar que la comparación del soporte de métricas del día no resulta vacía. Se ensayan un C5 sin histórico y la recuperación de un fallo de escritura en HA. La ronda r01 falla las ocho primeras regresiones; ambos guiones funcionales de Claude terminan con cero fallos en r02.

El script original r01 mató M01 a M12. M13 y M14 dejaron de coincidir con el código al cambiar el parámetro de reversión y la unidad del mínimo; el ejecutor del ticket porta ambos a las expresiones nuevas. Detectó los catorce operadores y los dos controles propios. La suite específica tiene once pruebas. Los guiones funcionales de Claude, ejecutados sin cambios, informaron cero fallos en la sombra y en el recálculo.
