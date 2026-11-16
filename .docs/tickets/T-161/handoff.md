# T-161 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-16 · r02 · de claude (sesión del Bloque A, T-161 r02) a claude (sesión coordinadora y revisor nuevo de la QA r02)

- **Fase en la que se entrega:** QA (r02).
- **Hecho:** H-01 a H-05 de la QA r01 de T-161:
  - AG-20 es un agente de control, y sus lecciones pasan el detector antes de escribirse en F6 (`orquestacion.py`, `_informe_aprendizaje`; `evaluador.py` sin tocar);
  - 0 de los 68 ataques nuevos pasan y hay 0 falsos positivos en los 40 válidos de la QA (1 de 40 de dominio, aceptado);
  - textos corregidos;
  - Q02, Q06 y Q12 mueren;
  - longitud máxima de 600 caracteres.
  - 193 pruebas nuevas en `tests/test_t161_r02.py`.
- **Falta:**
  - la QA r02 con un revisor nuevo;
  - integrar en `develop` (commit local «wip local: T-161 r02», sin push);
  - `./tools/check_all.sh` completo al integrar.
- **Cuidado con:** T-163 trabaja en paralelo en `evaluador.py`; esta ronda no lo toca. Las líneas de `guias.py` que usan los mutantes G01–G30, Q01–Q14 y M01–M26 se conservan literalmente. Los scripts del revisor que miden lo viejo fallan donde dice `pruebas.md` (sección r02).

## 2026-11-16 · de claude (sesión del Bloque A, T-161) a claude (sesión coordinadora y revisor nuevo de la QA)

- **Fase en la que se entrega:** QA.
- **Hecho:** H-01 a H-07 de la QA r01 de T-158. El detector normaliza el texto, es estricto con los controles, las otras lenguas y las otras escrituras, y revisa todos los campos de texto. Ninguna guía va a los agentes de control. El emisor falla cerrado, con una simulación para PB-48 solo con el cliente simulado. La retirada es idempotente. Además: 130 pruebas nuevas, el documento de evidencias regenerado, el mapa de PB-48, INC-T126-01 y el registro de decisiones.
- **Falta:**
  - la QA con un revisor nuevo;
  - integrar en `develop` (commit local «wip local: T-161», sin push);
  - `./tools/check_all.sh` completo al integrar;
  - si se quiere, bajar la cuota de ruff de `tools/cuotas.txt` a 2821 (no se ha tocado para no chocar con otras sesiones).
- **Commit:** «wip local: T-161» en la copia de trabajo (sin push).
- **Cuidado con:**
  - Los scripts del revisor de T-158 que medían el comportamiento viejo ya no pasan. Uno a uno, en `pruebas.md`:
    - `r01_02` emite la guía de PB-48 sin simular el fallo del emisor;
    - `r01_02` y `r01_05` comprueban, como condición previa, que el ataque pasa el detector;
    - `r01_03` emite por la CLI sin `--simular-fallo-del-emisor`.
  - Las líneas de `guias.py` que usan los mutantes G01–G30 se conservaron literalmente: no las reformatees si quieres seguir ejecutando `r01_04` sin cambiarlo.
  - El `.venv` enlazado apunta al paquete de la copia principal: la CLI, con `python -m bloque_a.cli` desde `bloque_a/11_Ejecutor`.
- **Scripts útiles:**
  - `.docs/tickets/T-161/medir_detector.py` (ataques y falsos positivos);
  - `.docs/tickets/T-161/mutantes_t161.py` (mutantes de las correcciones);
  - `.docs/scripts/mutantes_revisor_ampliado.py` (r01_04 con las pruebas nuevas);
  - `.docs/scripts/evidencias_plan_a.py --pb PB-48`.
