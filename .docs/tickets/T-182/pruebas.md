# Pruebas · T-182

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t182_procedencia.py.

Los dos casos fallaron antes de la corrección. Con el cambio pasan los dos y las once regresiones de T-181.

## QA r02

Con Python 3.12 pasan los seis casos del ticket, con pruebas directas de los patrones defensivos, prosa de mercado, corte histórico y la publicación de los ficheros de un ciclo real con cliente simulado. Se reprodujo primero el fallo de la frase del Brent. El corpus HTML tenía comentarios internos de plantilla, por lo que se prueba también que la entrega ordinaria se publica. El script original `revisores/r01_mutantes.py` detectó las 11 alteraciones. Para contrastar H-01 a H-03 se usaron casos controlados de entradas y salidas en la suite, sin inyectar acciones sobre sistemas reales. La fuente confirmada y la atribución pendiente se comprueban por separado.
