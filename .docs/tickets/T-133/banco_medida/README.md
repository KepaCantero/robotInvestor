# T-133 · Banco de medida: hallazgos abiertos de la QA r03 de T-94

> La carpeta `.docs/tickets/T-133/` guarda la copia antigua de un ticket del Bloque A que se renumeró a T-136 (ver su README). Este ticket, el T-133 de la deuda («Banco de medida (T-94): hallazgos abiertos de la QA r03»), vive en esta subcarpeta para no mezclarse con aquella.

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r02 APTO, 16-11-2026) |
| Pieza | `.docs/scripts/banco_medida.py` y sus pruebas (fuera de los bloques y del marco común) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «Después del T-97 quiero que sigas terminando los tickets que se han generado de los hallazgos de estos tickets» |
| Deuda técnica | T-133 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los hallazgos medios y bajos que dejó la QA r03 de T-94 (`.docs/tickets/T-94/qa.md`, «Ronda r03»).

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| H-21 (media) | La regla de adopción por variante del registro (T-99) ya no deja adoptar por repetición. Además, el prerregistro guarda la **huella del contenido** de los datos y del universo (`huella_datos`), así que unos datos cambiados son otra variante. |
| H-22 (baja) | La fuente del experimento es `cliente + huella de los datos + huella del universo`, no la ruta: los mismos datos copiados en otra carpeta son el mismo experimento. |
| H-23 (media) | `verificar`, sin `--registro`, comprueba contra el registro del agente (`RI_AGENTE`), no contra el que cita `experimento.json`. Avisa si la carpeta cita otro, y compara `dentro_del_maximo` con el registro. El sello y el ancla son de T-99. |
| H-24 (media) | La muestra de fechas sin solape se elige primero y solo se evalúa dentro de ella. Una apuesta de una fecha fuera de la muestra ya no deja «repetida» a otra de dentro. El informe da `plantilla`: selecciones totales y en la muestra. |
| H-25 (baja) | Una selección NEUTRAL no gasta ventana en `fechas_sin_solape`. Que la muestra se calcule con el titular y que una fila sin `fecha_fin` tenga un día de ventana es lo diseñado, y está documentado. |
| H-26 (baja) | `consumo.csv`: rechaza decimales en los recuentos, columnas obligatorias que faltan y columnas repetidas, y declara las opcionales ausentes. |
| H-27 (baja) | El mínimo de fechas efectivas de un experimento es el de A (10). Con 5 salían un 17,0 % y un 15,4 % de veredictos firmes sin habilidad. |
| H-28 (baja) | Pruebas que matan S04 (la muestra solo al titular), N19 (grupos por fecha y clase) y C01 (fechas sin ceros). |
| H-29 (baja) | `VERSION` 0.4.0, el docstring y el índice de scripts. |

## Criterios de aceptación (binarios)

1. CA-1: `pruebas_banco_medida.py` en verde, con una prueba por hallazgo (`test_t133_*`), y `pruebas_scripts.sh` por encima de su línea base.
2. CA-2: los scripts de las QA de T-94 (`revisores/r03_00_todos.sh`, si existe, o los `r03_*`) no dan defectos nuevos; lo que cambie por diseño se explica en `analisis-tecnico.md`.
3. CA-3: la simulación nula de T-94 (`.docs/tickets/T-94/nula_r03.py`) sigue calibrada: veredictos firmes sin habilidad por debajo del 15 %.
4. CA-4: gate 12/12, sin cambiar bloques, marco común ni Constitución.

## Registro

- 2026-11-15 · EN QA · correcciones de H-21 a H-29 en el banco 0.4.0, con sus pruebas
- 2026-11-15 · NO APTO · QA r01 (revisor nuevo, base `bdeb3d8`, gate 12/12): CA-2 (datos cambiados abrían otro experimento), H-01 a H-03 medios, H-04 a H-09 bajos; sin altos
- 2026-11-15 · EN QA · Ronda r02 (banco 0.5.0): datos como variante, huella de lo que A lee, verificar con avisos, informe con la plantilla, consumo estricto, nivel ≥ 0,90
- 2026-11-16 · CERRADO · QA r02 APTO (revisor nuevo, base `e08081e`, gate 12/12): CA-1 a CA-4; H-01 a H-04 y H-09 corregidos; restos y H-10 a H-17 (un medio y bajos) a la deuda como T-170
