# Pruebas · T-193

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t193_ingesta.py.

La prueba de tiempo usa un reloj controlado. La de concurrencia presenta cuarenta copias y verifica que solo queda una evidencia. Dos mutaciones comprueban el disparador temporal y las dos lecturas necesarias para cerrar.

Un ciclo completo ejecuta el Curador con duración controlada. Comprueba que la orden de apertura se registra en el historial del mismo ciclo. La prueba detectó que la lectura de HT-08 se hacía antes de la ingesta.
