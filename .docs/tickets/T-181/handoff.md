# Relevo para Claude

Revisar T-181 contra PB-24 y PB-25 en el clon local de trabajo. Los puntos decisivos son el límite temporal de una baja, la imposibilidad de retirar por un simple fallo de conectividad, la distinción entre indicio y retractación confirmada, y la reevaluación cuando sobrevive otra fuente suficiente.

Reproducir con la venv Python 3.12 desde la raíz:

```sh
.venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests/test_t181_fuentes.py
.venv/bin/python .docs/tickets/T-181/mutantes.py
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-24
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-25
```

La rama está en el clon Trabajo-T181. El permiso del operador es exclusivamente local. Pendientes el dictamen independiente, sus posibles correcciones y la integración autorizada.
