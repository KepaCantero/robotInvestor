# Pruebas · T-183

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t183_raices.py.

El caso original con 20 reproducciones llegaba a superar PS1 antes de la corrección. Tras ella, todas las derivadas apuntan a la misma EVD, incluso si se reciben en orden inverso.

## Ronda r02

El revisor r01 reprodujo ocho fallos en su lote de doce casos. Tras la corrección, once de los doce pasan en su versión original. La preparación de a04, que busca una CLM nueva sin evidencias_ps1, deja de encontrarla porque el flujo ya escribe la traza vacía. El caso histórico equivalente se construye expresamente en test_g3_compara_paquete_historicos_y_fecha. El caso de dos ciclos retira una fuente y comprueba el recuento de las afirmaciones y la entrega posterior.

Integración con T-181. M3 calcula el PS1 conjunto de cada opción y lo atribuye erróneamente a todas sus afirmaciones. Si una afirmación aparece en varias opciones, el mutante la da por respaldada cuando cualquiera de ellas supera PS1. Usa las evidencias raíz vigentes después de enlazar los documentos. La prueba distingue una afirmación sin corroboración suficiente dentro de una opción que sí la tiene.
