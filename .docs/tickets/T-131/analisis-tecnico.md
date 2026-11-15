# T-131 · Análisis técnico

- `comprobar_datos_a.py` usa el mismo `ProveedorCSV` que el ejecutor, así que rechaza lo mismo que rechazaría un ciclo (columnas, fechas con zona, cabeceras repetidas…). `DatosInvalidos` es subclase de `DatosNoDisponibles`: se captura primero.
- El umbral de «anticuado» sale de `ps2_antiguedad_maxima_dias` del horizonte pedido (H3 por defecto, el del ciclo semanal), sin número nuevo. H1 en el ejecutor se cuenta en sesiones; el script cuenta días naturales (más estricto): se dice en la ayuda del script si hiciera falta afinarlo.
- `borrador_anexo_b.py` no edita a mano el borrador: lo genera desde `divergencias_anexo_b.json` y tres incidencias (INC-T116-01, INC-T114-02 y las fases de CT-06). La propuesta por defecto, por la decisión del operador, es marcar como opcional lo que el ejecutor no exige; lo que deba ser obligatorio de verdad se cambiaría en el código, con re-congelado de los goldens.

## Ronda r02 (QA r01)

- `comprobar_datos_a.py` usa `ProveedorCSV.cierres()` (el que usa el ciclo), no `serie()`, que no valida las filas. Un dato malo posterior a as_of no cuenta, como en el ciclo (T-65, QA r03, H-21): el caso «fechas duplicadas» del revisor repite las tres últimas filas, que son de 2026 con as_of en 2024, y da OK con razón; con repetidas dentro del rango da INVALIDO.
- H1 en sesiones con `calendario._sesiones_entre` y `ps2_festivos`, como el ejecutor.
- `borrador_anexo_b.py`: incluye los «(raíz)» que no son de lotes ni están ya en «admite que falte», los campos de cada elemento de los lotes y el motivo del rechazo, los cambios de tipo, tres apartados nuevos en el §1 y, para los retornos internos, la propuesta de describir los campos de `ESQUEMAS`.
