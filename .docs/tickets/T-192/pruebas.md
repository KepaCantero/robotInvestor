# Pruebas · T-192

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t192_evaluacion.py.

Se introduce una base calculada al día siguiente en un ciclo mock y se comprueba el recálculo posterior. Dos ordenaciones emparejadas de cuatro fechas prueban confirmación y reversión con DM-HLN e idempotencia.

## Ronda r02

La comparación usa la configuración del proyecto y pares con varianza. Trece fechas de tres pronósticos superan el mínimo de 30; nueve quedan por debajo. La prueba de umbral usa un p real del orden de 0,027. Con umbral 0,10 revierte por DM-HLN y con 0,01 por IC medio inferior, tal como dicta la regla con un único objetivo. En F4 se comprueban por separado la fecha de cálculo y la del dato. Hay un tercer pronóstico limpio para asegurar que la comparación del soporte de métricas del día no resulta vacía. Se ensayan un C5 sin histórico y la recuperación de un fallo de escritura en HA. La ronda r01 falla las ocho primeras regresiones; ambos guiones funcionales de Claude terminan con cero fallos en r02.

El script original r01 mató M01 a M12. M13 y M14 dejaron de coincidir con el código al cambiar el parámetro de reversión y la unidad del mínimo; el ejecutor del ticket porta ambos a las expresiones nuevas. Detectó los catorce operadores y los dos controles propios. La suite específica tiene once pruebas. Los guiones funcionales de Claude, ejecutados sin cambios, informaron cero fallos en la sombra y en el recálculo.

## PB-34 · Revisión de la primera publicación · 26-11-2026

En `c4f2d1b`, un pronóstico H1 con base 100 y valor 110 al vencimiento se resolvía en +0,10. Al añadir una revisión a 90 para la misma observación, HT-01 rechazaba las dos publicaciones como duplicadas. El pronóstico pasaba de ABIERTO a NO_RESOLUBLE pese a disponer de la primera edición. Además, al recalcular RI-TB, una observación anterior a la emisión pero publicada después entraba en la muestra. Se reproducían siete ventanas donde al emitir solo se conocían seis, con y sin índice y con cesta.

`test_resolver_con_ediciones_visibles` recorre HT-01 CSV, la resolución de AG-20, F4 y la lectura posterior de las puntuaciones. En el vencimiento aún no se ha publicado el dato. Con ambas ediciones visibles y las filas del archivo en orden inverso, se obtiene +0,10, resultado binario 1 y Brier 0,09. Dos valores de una misma primera edición o una primera edición inválida impiden resolver. Las consultas ordinarias de HT-01 conservan su regla de duplicados. `test_tasa_historica_solo_con_publicaciones_conocidas` mide los tres recorridos de RI-TB con la configuración por defecto. Las seis ventanas conocidas son favorables y producen la probabilidad recortada de 0,95.

Antes de corregir, fallaban la resolución con dos ediciones distinguibles y los tres recorridos de RI-TB. El control de los duplicados verdaderos ya pasaba. Tras corregir, pasan los seis casos nuevos, incluido el control adicional de la primera edición inválida. En las pruebas vecinas seleccionadas de T-65 r04, T-91, T-92 y las unitarias pasaron 82 casos. Los datos son CSV locales construidos para la prueba.

La suite completa de T-192 pasó sus 17 pruebas. Los guiones funcionales de Claude `r02_ataques_sombra.py` y `r03_ataques_fuga.py` terminaron con cero fallos.
