# Pruebas · T-182

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t182_procedencia.py.

Los dos casos fallaron antes de la corrección. Con el cambio pasan los dos y las once regresiones de T-181.

## QA r02

Con Python 3.12 pasan los seis casos del ticket, con pruebas directas de los patrones defensivos, prosa de mercado, corte histórico y la publicación de los ficheros de un ciclo real con cliente simulado. Se reprodujo primero el fallo de la frase del Brent. El corpus HTML tenía comentarios internos de plantilla, por lo que se prueba también que la entrega ordinaria se publica. El script original `revisores/r01_mutantes.py` detectó las 11 alteraciones. Para contrastar H-01 a H-03 se usaron casos controlados de entradas y salidas en la suite, sin inyectar acciones sobre sistemas reales. La fuente confirmada y la atribución pendiente se comprueban por separado.

### Regresión de la frase sobre el oro

En `c4f2d1b`, dos ciclos simulados de RV con el mismo corte (5 de junio de 2026) y estados separados dieron resultados distintos. «El oro sirve de refugio frente a caídas bursátiles a corto plazo» llegó al informe. «El oro actúa como refugio frente a caídas bursátiles a corto plazo», frase del prompt del Analista de Materias Primas (§ sobre el oro), produjo G3-EST-06 en HA y BLOQUEADA en F5. El contrato G3-EST-06 del Orquestador exige un imperativo dirigido a un sistema o IA.

R9 y G3 comprueban el sujeto contiguo a «actúa como». Un determinante, un sustantivo financiero y sus posibles calificativos permiten reconocer el uso declarativo con independencia del complemento del verbo. La regresión incluye oro, franco suizo, liquidez y bono soberano, distintos complementos, mayúsculas y espacios. Comprueba el saneamiento, el dictamen G3 y la presencia literal de la frase del oro en el informe técnico entregado. El caso del imperativo del Orquestador sigue en la misma prueba.
