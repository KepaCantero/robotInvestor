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

## Corrección posterior a la reproducción local del 26-11-2026

Se conservan en el registro publicado atómicamente los metadatos de cada nueva baja y la huella de la decisión de retractación. La tabla de bajas sigue admitiendo la lectura de las cinco columnas históricas. `Referencias` selecciona por la fecha de baja y usa el reloj del bloque en las lecturas implícitas de sus consumidores. La CLI reconoce una decisión ya publicada al repetir un barrido, incluso si la ficha ya ha desaparecido. El aviso se recupera de la misma tabla que en la ejecución original.

Para reproducir ambos fallos y su corrección, ejecutar el archivo de pruebas del ticket con el selector `-k 'retractacion_cli_al_corte or reintento_lote or baja_antigua'`. Las filas anteriores a esta corrección que solo conservan fecha, motivo y título requerirían una copia original del catálogo para reconstruir sus atributos históricos. Pendiente del dictamen de Claude.
