# Ejemplo de salida de un backtest simulado (Bloque A Forex)

Regenerado el 03/11/2026 con el ejecutor `bloque_a_forex` actualizado V1.1 (Documento 0 del Bloque A Forex V1.1; cada opción lleva `naturaleza_inversion` y `horizonte_principal`, y el paquete `supuestos_declarados`):

```
bloque-a-forex --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --estado ./estado --salida ./salida backtest --desde 2026-07-03 --hasta 2026-09-25 --frecuencia semanal
```

**Atención:** se usó el cliente simulado (`mock`) y datos sintéticos (tipos de cambio, índices de cestas y estrategias,
una volatilidad implícita y tipos de interés `TIPO-<ISO>`). Las señales salen de reglas deterministas de prueba, no de un
modelo de lenguaje: sirven para ver los **formatos**, **no** para valorar la capacidad predictiva del bloque. Los niveles
de los pares sintéticos derivan con el tiempo y no se parecen a los reales.

Contenido:

| Archivo | Qué es |
|---|---|
| `senales.csv` | Una fila por opción publicada y fecha: segmento, tipo de opción, par y dirección (o composición, o vista de volatilidad), indicador de seguimiento y si la tesis espera que suba (`indicador_sube`), tipo de rentabilidad y divisa de medición, carry, horizontes, puntuaciones y riesgo |
| `pronosticos.csv` | Todos los PRG-FX- congelados (también los de finalistas no publicadas, `en_informe = False`), con la probabilidad del paseo aleatorio (0,5), la del forward, el cambio que descontaba el forward, la resolución y las puntuaciones de Brier frente a ambas referencias |
| `metricas.json` | Métricas por segmento × horizonte (Brier, BSS frente al paseo aleatorio, Brier y acierto del forward, ECE, DM-HLN), certificados y consumo |
| `consumo.csv` | Llamadas, tokens y UC por ciclo (coste vacío: no hay precios configurados) |
| `entregables_ultima_semana/` | Informe técnico (Markdown), informe visual (HTML autocontenido) y paquete JSON (esquema del Bloque A Forex, actualizado V1.1) del último ciclo |

Las 13 fechas terminaron con dictamen G3 «APTO»; 29 de los 78 ciclos de segmento quedaron en arrastre verificado (N1). Sin encargos de seguimiento (CT-24) ni H5 activado: esas funciones se ilustran en `tests/test_v11.py`. El estado completo del bloque (F1–F6, F10, RC, HA) no se incluye por
tamaño; se regenera con la orden anterior en algo más de un minuto.
