# T-62 · Pruebas de Astra

Ejecutor B, fecha simulada 2025-01-31, encargo de redes eléctricas en Europa. Cada variante usa un estado temporal nuevo y el mismo ejemplo. Se introduce una objeción fuerte sobre el retraso de los transformadores.

| Caso | Resultado esperado y verificado |
| --- | --- |
| Tesis global abierta | PA5 bloquea. El veredicto es VIGILAR. Cada encargo emitido incluye el motivo en el contexto del sector. |
| Eslabón de transformadores, abierto | PA5 pasa. El sector conserva INVERTIR_ESCALONADO. Cuatro de los doce encargos reciben la advertencia; los ocho restantes quedan fuera de su alcance. |
| TESIS con eslabon_id frente a ESLABON con ese mismo identificador | Ambas formas producen el mismo alcance. Los paquetes completos pasan el esquema JSON congelado. |
| Objeción resuelta por el Director | La caja conserva la respuesta y el estado resuelto. |
| Identificador desconocido, ausente o mal tipado | La petición termina bloqueada con motivo, sin entrega de encargos. |
| Exposición secundaria y candidatos adicionales | Se fuerza una asignación secundaria en renta fija y un ranking corto. El aviso llega también a las opciones añadidas por cobertura y una objeción fuerte abierta las limita a secundarias. |

En la base 0a865bb, siete de las ocho variantes fallaron y el control de la tesis global conservó VIGILAR. Una comprobación posterior mostró que a las cajas de ese control les faltaba el argumento de la objeción global. Se añadió la regresión y se verificó la corrección.

Reproducción desde la raíz con el entorno del proyecto:

```sh
python -m pytest -q bloque_b/11_Ejecutor/tests/test_objecion_eslabon.py
.docs/scripts/gate.sh --completo
.docs/scripts/pruebas_marco.sh
```

El marco se ejecutó en una copia temporal por los ejemplos que algunas pruebas escriben. Se verificaron 50 suites.

Resultado completo: A 58, Forex 68, B 142 (134 previas y ocho nuevas). Los doce controles del repositorio pasaron, sin omisiones. Al exigir también el motivo global en la caja, las ocho variantes fallaron en la base anterior. Las ocho pasan con la corrección. Se verificó de nuevo el conjunto de ocho después de añadir la comprobación explícita de PC5 para expuestos, ajenos y casos resueltos. La cuota de Ruff baja de 3488 a 3485.
