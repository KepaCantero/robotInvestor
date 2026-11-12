---
id: claude/2026-11-12_decorador-al-insertar-metodo
autor: claude
fecha: 2026-11-12
tipo: leccion
etiquetas: [marco, edicion, decoradores]
fuente: commit 89e78e7 (marco V0.75, T-75 H-09), sistema_global/marco_comun_c/validador/orquestador.py
vigencia: vigente
---

Al añadir `_anotar_veto_f` en `orquestador.py` lo puse justo antes de `pantalla_aprobacion`, debajo de su línea `@_seguro`. El decorador pasó al método nuevo, que deshacía su propia anotación, y `pantalla_aprobacion` se quedó sin protección atómica. La prueba de regresión lo cazó antes del commit.

- **Por qué importa:** en el marco, `@_seguro` es lo que hace atómica cada operación y fija el reloj. Si cambia de método en silencio, se pierde la atomicidad sin que falle nada a la vista.
- **Cómo aplicarlo:** al insertar un método antes de otro, busca las líneas de decorador de este (`@...`) e inserta por encima de ellas. Después, revisa con `grep -n -B1 "def <nuevo>"` que el nuevo no ha heredado ningún decorador.
