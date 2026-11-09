# T-63 · Evidencia de pruebas de Astra

Pruebas simuladas con corte 2025-01-31, petición de redes eléctricas y la misma advertencia sobre retrasos.

| Respuesta a la objeción fuerte | Registro y caja del sector |
| --- | --- |
| «Los plazos han vuelto al nivel anterior», sin cita | Abierta, VIGILAR. La caja y el informe explican que falta una referencia verificable. |
| La misma frase con una cita inventada | Abierta, VIGILAR. El identificador no se presenta como fuente válida. |
| La misma frase citando un dato registrado en otra petición | Abierta, VIGILAR. El dato ajeno tampoco se ofrece en el catálogo al agente. |
| La misma frase citando un dato registrado en esta petición | Resuelta, INVERTIR_ESCALONADO en este ejemplo. La fuente queda en la objeción, el contexto del sector de cada caja y la fila correspondiente del informe técnico. |

Antes del cambio se ejecutaron los tres casos iniciales: sin cita, cita inventada y cita registrada. Los tres fallaron. Los dos primeros permitían el cierre. El tercero falló al intentar usar el catálogo de fuentes que el ejecutor todavía no facilitaba.

Las diez comprobaciones de test_evidencia_objecion.py cubren los cuatro recorridos y seis límites: lista vacía, identificador suelto, cita mezclada con una entrada inválida, texto en blanco, respuesta de tipo incorrecto y cita repetida. Los casos anteriores del candidato y del eslabón, con cita expresa en el caso positivo, comprueban que la referencia también llega a sus encargos a C.

## Reproducción desde la raíz

```sh
python -m pytest -q bloque_b/11_Ejecutor/tests/test_evidencia_objecion.py
python -m pytest -q bloque_b/11_Ejecutor/tests/test_objecion_candidato.py bloque_b/11_Ejecutor/tests/test_objecion_eslabon.py
.docs/scripts/gate.sh --completo
.docs/scripts/pruebas_marco.sh
```

Para reproducir el fallo original, usar el código de 666f4a9 en una copia temporal y añadir las pruebas nuevas. No se hicieron llamadas a un modelo real. El caso positivo únicamente acredita que se citó una referencia reconocida.

Resultado final: 152 pruebas del ejecutor B frente a las 142 de T-62; 58 de A y 68 de Forex. Pasaron los doce controles del repositorio sin fallos ni omisiones. Pasaron también las 50 suites del marco global, ejecutadas en copia temporal. Ruff bajó de 3485 a 3482 y mypy B mantuvo su cuota. QA independiente pendiente.
