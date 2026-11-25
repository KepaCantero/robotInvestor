# Pruebas · T-184

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t184_altas.py.

Treinta altas distribuidas en tres catálogos temporales. Incluye empates de Q, fechas diferentes, marca D y rechazo atómico de un lote inválido.

## Regresión de la ronda r02

`test_b01` incorpora 30 fichas de las cuatro calidades sobre copias de los F7, F8 y F9 entregados. Recorre las tres secciones afectadas, comprueba el seguimiento de nivel D, la ubicación, el orden y el estado del enlace. `test_b02` a `test_b10` cubren el rechazo atómico, bajas, fechas, enlaces, repetición, concurrencia, fuentes únicas y tipología. Los casos adicionales ejercitan la rúbrica, los umbrales configurables, las bajas del almacén y los desempates de días y años.

El archivo independiente r01 se conserva íntegro. Al ejecutarlo en r02 pasan 19 de 23 casos. Las cuatro entradas positivas de b01, b07, b08 y b09 carecen del desglose obligatorio de H-04 y el alta se rechaza antes de la comprobación pretendida. Sus equivalentes mantenidos en la suite aportan los campos obligatorios y ejercitan esos caminos. Los mutantes r01 apuntaban a expresiones literales de la implementación antigua. La versión r02 de `mutantes.py` conserva sus 14 hipótesis con anclajes actuales y añade tres comprobaciones.
