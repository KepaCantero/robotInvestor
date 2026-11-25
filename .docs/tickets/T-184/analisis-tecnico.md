# Análisis técnico · T-184

El comando alta-referencias incorpora un lote JSON revisado por el custodio en un solo catálogo. Valida identificadores, sección, enlace, fecha y Q. El lote se publica de una vez y comprueba si otro escritor modificó el fichero.

## Ronda r02

El alta comparte la rúbrica de puntos con el mantenimiento y consulta la misma configuración de niveles. La CLI resuelve la fecha y el registro de bajas del almacén indicado en la invocación. Todos los controles ocurren antes de publicar. Los catálogos se mantienen en disco si se produce un error en el lote o si otra sesión ha publicado entretanto. Véase INC-T184-01 para las reglas del formato.
