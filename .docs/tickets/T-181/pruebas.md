# Pruebas del 21-11-2026

- Python 3.12.6. Las once pruebas específicas pasan. Incluyen la CLI en modo informe y aplicación, retractación del editor de F8 con el verificador HTTP real y transporte simulado, y comprobación de F2 persistido al final del comando.
- PB-24 cubre retirada, aviso al Curador, reintento, lectura al corte, revisión con y sin respaldo alternativo en F3 y bajas en CT-21. Un fallo de conectividad del servicio de archivo conserva la referencia.
- PB-25 cubre recálculo de Q con motivo, rechazo de revisión obsoleta, reparación desde una copia idéntica, indicio sin confirmar y retractación confirmada.
- Los ocho mutantes propios provocan fallos de aserción. Se ejecutan en una copia temporal. La versión anterior carece del módulo y no recoge la nueva prueba.
- Comparación con 9ce57b2. El ciclo del 05-06-2026 entrega el mismo resumen al normalizar las rutas de salida. Backtest semanal en modo mock del 03-07 al 25-12-2026, 26 ciclos, 18 señales, 6 pronósticos y 4 resueltos. Los CSV de señales y pronósticos y el JSON de métricas son idénticos byte a byte. En el CSV de consumo solo varía el tiempo de ejecución. No se ha medido rentabilidad con un modelo real.
- Evidencias regeneradas con el servidor HTTP de prueba en la interfaz local. El plan recoge 349/349 pruebas automáticas citadas superadas, incluidos PB-24 y PB-25. Pasaron también las 337 pruebas de los scripts del repositorio.
- Suite completa del ejecutor A dentro de la comprobación general del repositorio: 8369 pruebas superadas. Ruff 2807 y mypy de A 102, dentro de las cuotas de la versión de partida.
- La comprobación general del repositorio pasó los doce controles, sin omisiones.
