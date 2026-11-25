# Handoff · T-191

Claude revisa los criterios de aceptación del README y reproduce las pruebas con Python 3.12.

`.venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests/test_t191_degradado.py`

El modo manual no acredita que se hayan ejecutado los controles de la herramienta caída. El resultado seguro es un bloqueo justificado.

## Ronda r02

Reproducir con `.venv/bin/python .docs/tickets/T-191/mutantes.py` y las pruebas T-159/T-191. El caso nominal antiguo de r01_ataques.py sustituye todo el control por un RuntimeError genérico: ahora debe parar el ciclo. Para reproducir una caída en ese guion usar ht09.HerramientaNoDisponible, conservando intactos los casos de integridad y permisos. En el mapa PB-52 sigue parcial por las comprobaciones B manuales.
