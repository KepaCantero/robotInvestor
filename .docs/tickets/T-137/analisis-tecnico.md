# T-137 · Análisis técnico

- `contratos.py`: `_forma_de_fecha` (mes 01–12 o año 19xx/20xx: calendario, no umbral) y el reparto de series largas de grupos de 4 en tarjetas desde el principio o desde el final.
- `evaluador.py`: `_fecha_de_calendario` comprueba que la fecha da fecha de calendario (`date()`), sin años límite escritos a mano.
- `estimar_coste_ciclo_a.py`: `estimar(…, reparaciones)`; con una reparación se reenvía el intento anterior entero (todas sus continuaciones).
- `comprobar_datos_a.py`: ventana del ciclo y campo `aviso`.
- `borrador_anexo_b.py`: `RETORNOS_DEL_MOTOR`.
- Pruebas de T-136 que cambian por decisión: la fila de 8 números admite hasta un 1 % (dos tarjetas válidas seguidas) y la cota de las continuaciones paga su `max_tokens` y reenvía lo generado.
