# Handoff · T-183

Claude revisa los criterios de aceptación del README y reproduce las pruebas con Python 3.12.

`.venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests/test_t183_raices.py`

La identificación de reproducciones sin atribución documental requiere curación. Los registros históricos sin traza de PS1 siguen siendo legibles.

## Ronda r02

Usar los casos de test_t183_raices.py y .venv/bin/python .docs/tickets/T-183/mutantes.py. El registro de incidencias describe las propuestas INC-T183-01 y 02. El mutador del ticket conserva los supuestos del revisor, con puntos de inyección adaptados a las funciones refactorizadas.
