# T-63 · Causa y corrección

En 666f4a9 el cierre se basaba en texto y un booleano. El Director y el Seleccionador reciben ahora un catálogo de referencias trazables de la misma petición, reconstruido a la fecha de corte a partir de F2 y de los cálculos de escenarios y de puntuación identificados en el estado y registrados en RC. Se incluye una descripción para elegir la referencia.

La respuesta cita mediante evidencia_nueva, campo previsto por el prompt del Seleccionador. Una cadena suelta, una lista vacía, una entrada de tipo incorrecto, una referencia de otra petición o texto en blanco no acreditan un cierre fuerte. Se conserva el texto recibido y, cuando se intentó cerrar sin citas verificables, el motivo de la incertidumbre. Las citas repetidas se presentan una vez. En el paquete se guardan como x_evidencia_respuesta; el campo evidencia pertenece al argumento original.

Se modificaron la recepción de las respuestas en orquestacion.py, la preparación de las cajas en sintesis.py y la tabla del informe técnico en redaccion.py. Los casos positivos de T-61 y T-62 ahora citan una referencia del encargo. El esquema congelado permite estas extensiones. El cambio se aplica al procesar respuestas; no se recalifican retrospectivamente las entregas guardadas ni se inspecciona la veracidad de la fuente.
