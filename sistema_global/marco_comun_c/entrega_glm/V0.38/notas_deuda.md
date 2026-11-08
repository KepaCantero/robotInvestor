# Notas de deuda — V0.38 (tope a las operaciones LIBRES)

La pieza cierra la fila T-33 de la tabla T y abre una fila nueva en la tabla D. Ninguna otra fila cambia.

## Tabla T (texto nuevo de la cuarta columna de filas existentes)

- T-33: «RESUELTO en V0.38: tope diario por cartera a las LIBRES declaradas (CT-G-14): el importe de cada LIBRE se valora en euros con la última foto de G y se registra aparte (`self.libres` del Orquestador); si la suma del día de la cartera supera `libres_tope_dia_eur` o hay LIBRES sin poder valorar en euros, avisa O-37 (prioridad ALTA) y degrada la cartera a L1; el registro se acepta igual (con `tope_libres_superado`) y F-14 cuenta las LIBRES en el importe del día de la cuenta (batería `pruebas/pruebas_libres_t33.py`, 37 comprobaciones)»

## Tabla D (filas nuevas: qué debe decidir el operador, dónde se usa y valor de partida [PROPUESTO])

- D-32 | Fijar el tope diario por cartera de las operaciones LIBRES declaradas fuera del sistema; decidir también que una LIBRE que no se puede valorar en euros (sin foto de G, sin divisa conocida o sin tipo de cambio) cuenta como tope superado y degrada la cartera | Clave `libres_tope_dia_eur` de la configuración del Orquestador (CFG-0.8.0); se comprueba al registrar un CT-G-14 LIBRE (aviso O-37 y degradación) y en la actividad que el Orquestador entrega a F (`importe_dia_eur`, recorte de F-14) | 2.000 € por cartera y día [PROPUESTO]
