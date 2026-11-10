# Notas de briefing — V0.66 (pruebas doradas)

**Qué es.** Las baterías comprueban lo que se les dice que compruebe; las pruebas doradas guardan una foto
fija de lo que hace cada paso de la jornada y de la semana y avisan de cualquier diferencia. La foto vive
en `pruebas/doradas/jornada.json` y `pruebas/doradas/semana.json`; la batería es
`pruebas/pruebas_doradas.py` (17 comprobaciones) y el aparato, `pruebas/doradas.py`.

**Cómo se usa.**

- La batería completa (`corre_baterias.py`) y la pieza la corren sin argumentos: regeneran las dos fotos
  en memoria, las comparan con las entregadas y, si algo cambió, fallan con el informe de diferencias —
  una línea por diferencia: `camino: antes -> después` (el camino llega hasta la clave, por ejemplo
  `paso[4] (ejecutar).estado.posiciones.POS-EXP-0001.cantidad`).
- `python3 pruebas/pruebas_doradas.py` a mano hace lo mismo.
- `python3 pruebas/pruebas_doradas.py --regenerar` **reescribe** las fotos de `pruebas/doradas/`.

**Cuándo está permitido regenerar.** Solo a propósito, y cada regeneración se explica en el Documento 0
de la pieza que la hizo, con la lista de diferencias aceptadas (el propio comando lo recuerda al acabar).
Flujo cuando la batería dorada cae tras integrar una pieza:

1. Leer el informe: qué paso, qué camino y qué valores cambiaron.
2. Decidir si el cambio es el previsto. Si lo es, `--regenerar` y escribir en el Documento 0 de la pieza
   la lista de diferencias aceptadas. Si no lo es, es un defecto: no regenerar.
3. Repetir la batería completa: las 55 baterías, 0 con fallos.

**Qué mira la foto y qué no.** Del resultado de cada paso: `ok`, `codigo`, las acciones como
`(condicion, codigo, expediente, ok, posicion, regla)`, las cantidades redondeadas a 6 decimales y los
identificadores — sin los
textos de `motivo`, que cambian demasiado. Del estado: expedientes, posiciones con su cantidad, avisos
sin acusar (códigos ordenados, con duplicados), niveles por cartera, kill-switch y rearmes. No mira los
textos de «motivo» ni lo que no cambia el estado (el diario, los cortes y los reinicios de las baterías).

**Datos.** Todo simulado y determinista: sin azar, sin reloj del sistema; dos ejecuciones dan las mismas
fotos byte a byte, en cualquier carpeta y máquina. Las fotos entregadas se generaron con el mismo código
que ejecuta la batería.
