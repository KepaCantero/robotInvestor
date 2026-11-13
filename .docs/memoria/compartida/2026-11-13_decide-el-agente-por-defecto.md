---
id: compartida/2026-11-13_decide-el-agente-por-defecto
autor: claude
fecha: 2026-11-13
tipo: regla
etiquetas: [operador, decisiones, propuesto]
fuente: sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md
vigencia: vigente
---


## Regla

Dicha por el operador el 13-11-2026: «todo lo que dependa de una decisión mía prefiero que tomes la decisión por mí por defecto ya que soy inexperto en el campo. Eso sí, me gustaría que recopilases todos los parámetros/variables/decisiones importantes que son exclusivas de mi elección por si en el futuro quiera modificar alguna de ellas».

## Cómo se aplica

- Ante una decisión de método, de umbral, de alcance de una tarea o de prioridad, el agente elige la opción que recomendaría, sigue trabajando y no espera respuesta.
- Cada decisión importante se apunta en `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`: qué se decidió, el valor, quién lo decidió (el operador o el agente por defecto), dónde vive y cómo se cambia. El operador puede cambiar cualquiera después.
- En el código y en las incidencias, lo decidido así se sigue marcando `[PROPUESTO]`, para distinguirlo de lo que el operador ha dicho él mismo.
- Sustituye, para el Bloque A, a la costumbre anterior de dejar la decisión pendiente y esperar (relevos del 11 y del 13-11-2026, «decide él»).

## Límites (interpretación de Claude, por prudencia)

Se sigue preguntando antes de actuar cuando la decisión:

- gasta dinero o usa una credencial (la API real, un proveedor de datos de pago);
- no se puede deshacer o sale del repositorio (borrar, publicar fuera, enviar órdenes);
- cambia la Constitución, los controles (F, G, kill-switch, niveles de autonomía) o una entrega congelada (Documento 0, plantillas);
- reparte trabajo a Astra: sus tareas las decide el operador.

El operador dijo la regla hablando del Bloque A. Para otras piezas es un buen punto de partida, pero conviene confirmarlo la primera vez.
