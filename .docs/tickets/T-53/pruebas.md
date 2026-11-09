# T-53 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`bloque_a/11_Ejecutor/tests`) | 58 | 117 (`test_t53_seleccion_y_entrega.py`: 32, 14 de ellas de la QA · `test_t53_evaluacion_y_almacen.py`: 27) |
| Herramientas de referencia (`bloque_a/10_Herramientas/tests`) | 135 | 135, sin cambios en las pruebas y en verde con HT-03 y HT-09 corregidas |
| Bloque A Forex y Bloque B | 68 · 141 | 68 · 141 (no se tocan) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1: cada corrección tiene una prueba que falla sin ella | Las dos baterías nuevas. Ver «Regresiones» |
| CA-2: suites en verde y línea base subida | 117 en A; `tools/cuotas.txt` sube `pytest_bloque_a` a 117; gate completo |
| CA-3: cada hallazgo no corregido, con su motivo | `analisis-tecnico.md`, sección «Lo que no se corrige aquí» |
| CA-4: propuestas presentadas al operador | `propuestas.md` y la conversación del 9-11-2026 |

## Regresiones

- **`test_t53_seleccion_y_entrega.py`:** se ejecutó contra el código anterior (copia limpia de `develop` en 63a376d, con `PYTHONPATH` apuntando a ella). Fallan 14 de 18. Las 4 que pasan son controles a propósito:
  - la sustitución legítima de una vigente;
  - tres hitos distintos;
  - la entrega apta;
  - PS2 un lunes con el dato del viernes.
- **`test_t53_evaluacion_y_almacen.py`:** el segundo agente revirtió cada corrección por separado en una copia y ejecutó sus pruebas. Los 14 casos fallan sin la corrección y pasan con ella.
- **Reproducción:** los scripts del revisor de código (`revisores/scripts_codigo/`) ya no reproducen los defectos. La excepción es `ca_ece_cero.py`, que solo evalúa la expresión antigua; con el Evaluador real, un ECE de 0 no se revoca.

## Regresiones de la QA r01 (H-01 a H-05)

- Las 13 pruebas nuevas se ejecutaron contra `8562d1e`: fallan 10; las 3 que pasan son controles (un sábado normal, más de una sesión) y el uso del horizonte del Analista, ya corregido en `8562d1e`.
- `revisores/scripts_qa/r08b_mutaciones_ronda2.sh` revierte cada corrección por separado: las 8 mutaciones hacen fallar su prueba.

## Gate

Se ejecutó `.docs/scripts/gate.sh` con `--completo` antes del commit. El resultado queda en `.docs/scripts/.logs/`. La lista de archivos del corpus se volvió a congelar a propósito solo por las dos copias de HT-03 y HT-09 en `10_Herramientas`.
