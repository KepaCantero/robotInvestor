# Análisis técnico · T-192

La resolución contrasta la fecha del cálculo de la tasa base y sus datos con la emisión. La base con información futura se excluye. C5 reconstruye RI-TB con el corte original, registra cálculo y puntuaciones corregidas en F6 y conserva F4. La sombra congela pares de RK por opción y fecha en F5 y los compara al terminar la ventana con resultados admisibles.

## Ronda r02

El cierre de sombra usa el número de pronósticos pareados para el mínimo del Anexo A. La serie diaria de IC sirve como entrada de la DM-HLN. Las predicciones sin valor observado, horizonte o sentido conocido se omiten. F6 conserva el resultado del AJU según §4.6. Cada fuga de tasa base deja una incidencia y cada corrección tiene una comunicación COR al Orquestador. Un C5 posterior repara una comunicación interrumpida sin volver a corregir F4 o F6.
