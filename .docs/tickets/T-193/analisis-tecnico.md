# Análisis técnico · T-193

HT08 mide duración e intensidad de ingesta y registra órdenes de apertura y cierre. F2 comprueba el hash y guarda la evidencia dentro de la misma transacción.

### Ronda r02

El monitor dimensiona la capacidad según las llegadas y los tiempos de servicio de la ventana. La carga se compara con los umbrales configurados y cada orden conserva sus métricas y su regla. Después de ampliar, cada lectura con servicio del Curador deja en HA la medida frente al objetivo, incluso al cerrar la última instancia adicional.
