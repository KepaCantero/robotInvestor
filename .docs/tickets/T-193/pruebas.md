# Pruebas · T-193

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t193_ingesta.py.

La prueba de tiempo usa un reloj controlado. La de concurrencia presenta cuarenta copias y verifica que solo queda una evidencia. Dos mutaciones comprueban el disparador temporal y las dos lecturas necesarias para cerrar.

Un ciclo completo ejecuta el Curador con duración controlada. Comprueba que la orden de apertura se registra en el historial del mismo ciclo. La prueba detectó que la lectura de HT-08 se hacía antes de la ingesta.

## Ronda r02

El reloj controlado permite distinguir el borde estricto, las llegadas de la ventana, la duración media, el dimensionado y el cierre de una sola instancia tras lecturas libres consecutivas. Un segundo ciclo comprueba el CAR- de recuperación en HA. Las pruebas con la configuración modificada hacen observable cada parámetro y un objetivo inválido impide construir el bloque.

El script r01 presupone que todas las salidas de HT-08 son órdenes y accede a `accion` también en las lecturas de recuperación. La revisión solicita añadir CAR-, que carece de ese campo. La prueba de regresión comprueba ambos tipos por separado. Para los analistas sin objetivo se aplica la opción de escalado por cola expresamente admitida en H-05. El programa de mutación r02 porta los once cambios del revisor a la versión configurable del monitor y añade dos comprobaciones propias. Primero debe pasar el código original, y un error de ejecución del mutante no cuenta como detección.
