# T-141 · Análisis técnico

- Cruces: cada símbolo es numerador / denominador en «unidades por euro» (`CRUCES`); EURUSD=X es directamente USD/EUR.
- Un tipo que falta (festivo de alguna plaza) o un cruce no positivo o no finito se quita de esa fecha, no se inventa.
- `fecha_publicacion` es la misma fecha: el BCE publica a las 14:15 CET, antes del cierre que usa el ciclo semanal.
- La URL del BCE es la única red del script; las pruebas no usan red.
