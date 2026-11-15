# T-131 · Análisis técnico

- `comprobar_datos_a.py` usa el mismo `ProveedorCSV` que el ejecutor, así que rechaza lo mismo que rechazaría un ciclo (columnas, fechas con zona, cabeceras repetidas…). `DatosInvalidos` es subclase de `DatosNoDisponibles`: se captura primero.
- El umbral de «anticuado» sale de `ps2_antiguedad_maxima_dias` del horizonte pedido (H3 por defecto, el del ciclo semanal), sin número nuevo. H1 en el ejecutor se cuenta en sesiones; el script cuenta días naturales (más estricto): se dice en la ayuda del script si hiciera falta afinarlo.
- `borrador_anexo_b.py` no edita a mano el borrador: lo genera desde `divergencias_anexo_b.json` y tres incidencias (INC-T116-01, INC-T114-02 y las fases de CT-06). La propuesta por defecto, por la decisión del operador, es marcar como opcional lo que el ejecutor no exige; lo que deba ser obligatorio de verdad se cambiaría en el código, con re-congelado de los goldens.
