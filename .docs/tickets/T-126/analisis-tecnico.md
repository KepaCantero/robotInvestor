# T-126 · Análisis técnico

Solo pruebas: `bloque_a/11_Ejecutor/tests/test_t126_pb26_pb48.py`. No cambia código de producción ni el corpus. Medido el 14-11-2026: F7 560 referencias en 23 temáticas, F8 464 en 18, F9 389 en 19; ninguna sin temática válida, ninguna inversión de orden, todos los niveles coherentes con Q.

Límites: PB-26 comprueba el estado de los archivos, no el alta de referencias nuevas (Documentadores, modelo real); PB-48 comprueba que una guía que relaja un control no llega a la elegibilidad, pero el ejecutor no tiene el circuito de guías del Orquestador (CT-18) que registraría el conflicto (INC-T126-01).

Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t126_pb26_pb48.py`.
