# Ejemplo de salida de un backtest simulado

Generado con:

```
bloque-a --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --estado ./estado --salida ./salida backtest --desde 2026-07-03 --hasta 2026-09-25 --frecuencia semanal
```

**Atención:** se usó el cliente simulado (`mock`) y precios sintéticos. Las señales salen de reglas deterministas de prueba, no de un modelo de lenguaje: sirven para ver los **formatos** de `senales.csv`, `pronosticos.csv`, `metricas.json` y `consumo.csv` y los tres entregables, **no** para valorar la capacidad predictiva del bloque.

Regenerado el 02/11/2026 con el Ejecutor V1.1 (Documento 0 óptima V5.0): doce tipos de activo, universo de ámbitos con indicador de seguimiento, `senales.csv` con las columnas `tipo_activo`, `subtipo`, `ambito` e `indicador_seguimiento_simbolo` (más el alias obsoleto `proxy_backtest` al final) y paquete JSON con `ambito`, `indicador_seguimiento`, `invertibilidad` y el encargo para el Bloque B, sin vehículos.


Migración de formato V5.1: al paquete JSON histórico se le añadió la naturaleza coherente con el horizonte principal mediante la regla del ejecutor. Los valores analíticos y la fecha de la ejecución son los originales.

Migración de formato T-91 (12-11-2026): `pronosticos.csv` gana al final las columnas `fecha_dato_proxy` y `fecha_dato_referencia`, vacías en este ejemplo porque se generó antes de que la resolución guardara la fecha de cada serie. El resto de los valores son los originales.
