# T-64 · Qué fechas existen

El esquema de F2 describe fecha_fenomeno o periodo_datos, fecha_publicacion, fecha_recuperacion y conocible_desde. El campo conocible_desde contempla retrasos o embargos. En la ruta de análisis dimensional del ejecutor, el alta de EVD en orquestacion.py escribe recuperacion y conocible_desde con la fecha del análisis. Esa ruta no obtiene la fecha del hecho ni la de publicación del documento. El almacén añade por separado su fecha de escritura (_fecha).

El catálogo de T-63 consulta el estado de F2 a la fecha de corte: Almacen.leer filtra _fecha. Después entrega descripciones de referencias y el cierre comprueba los identificadores. Ninguno de estos dos pasos compara el día del hecho con el día del incidente ni verifica conocible_desde de la evidencia. La objeción tampoco dispone hoy de una fecha estructurada del incidente. La lectura de precios CSV en HT-01 tiene un filtro opcional de publicación propio; es un recorrido distinto.

**Siguiente cambio propuesto.** Para objeciones sobre un hecho fechado, conservar las fechas verificables al ingresar la fuente y registrar la fecha del incidente. Antes de mostrar una fuente al agente, respetar la primera disponibilidad y el corte del expediente. Para cerrar la objeción, verificar que la observación documenta el periodo relevante. Si falta la fecha, mantener abierta la objeción hasta aclararla. Quedan por acordar el tratamiento de periodos y eventos del mismo día. La fecha por sí sola no prueba que el informe hable de la misma incidencia.

## Corrección aplicada

La normalización y la elegibilidad temporal de EVD, DAT y CALC se comparten en fechas_evidencia.py. El catálogo F2/RC sigue filtrado por petición y por el día de registro, y comprueba también las fechas de la fuente. Una observación anterior puede estar en el catálogo como antecedente; se descarta para el cierre si su día no supera el del incidente. Los tiempos ISO con zona se convierten al día de la zona del expediente. Los periodos en texto, valores ausentes, inválidos o sin zona horaria cuando incluyen una hora no se convierten en fechas inventadas.

En la entrada dimensional se conservan las fechas declaradas en las notas con fuente fechada. El flujo de prueba produce observaciones sintéticas explícitamente fechadas. El crítico proporciona fecha_incidente, y la síntesis copia la fecha del incidente, los días de cada referencia admisible y el motivo al aviso de la empresa. Se protege la reanudación posterior a F6 si el expediente contiene un cierre fuerte antiguo sin constancia temporal. El cambio no demuestra la veracidad del contenido ni autentica las fechas declaradas por la fuente.

El control se aplica a la evidencia para el contraste de B. Los lectores de precios, los certificados históricos y las reglas de inversión de los demás bloques quedan fuera del alcance.
