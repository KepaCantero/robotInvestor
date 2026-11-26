# Pruebas · T-188

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t188_producto.py.

Ciclo real del ejecutor con cliente mock, dos decisiones, avance del reloj y lección en F6. El segundo caso atraviesa tres consultas desde análisis distintos.

El 26 de noviembre se reprodujeron dos preguntas distintas en los mismos tres análisis. La entrega anterior generaba dos avisos pero guardaba una sola lección. La prueba exige ambas lecciones, comprueba qué consultas sustentan cada una y verifica la entrega a sus destinatarios. La muestra sintética de 30 oportunidades por grupo atraviesa ahora el ciclo completo del Evaluador con la configuración de entrega.

El programa de mutaciones del ticket detectó las dos alteraciones deliberadas. Las cuatro suites T-181, T-182, T-188 y T-192 pasaron sus 67 pruebas juntas en Linux con Python 3.12.
