---
name: ri-qa
description: Fase 4 de 4 del flujo de trabajo del Robot Investor. Úsala para la revisión independiente de una tarea ya implementada y probada, o cuando pidan «revisa», «haz la QA», «audita»: reproducir desde limpio, intentar romperlo con scripts propios, comprobar los invariantes del sistema, emitir un veredicto binario APTO / NO APTO en docs/tareas/<tarea>/04_qa.md y, si es APTO, cerrar la tarea.
---

# QA independiente de una tarea del Robot Investor

Fase 4 de 4. Antes: `ri-probar`. Si el veredicto es NO APTO, se vuelve a `ri-implementar`.

**Independencia:** la QA la hace un agente que **no** implementó la tarea. Si implementó Claude, revisa Astra, y al revés. Si eso no es posible, la hace un revisor nuevo sin el contexto de la implementación (por ejemplo, un subagente al que solo se le da el plan y el código). Forma tu opinión con el plan y el código antes de leer `02_implementacion.md`, para no heredar los puntos ciegos de quien lo hizo.

## Procedimiento

1. **Reproduce desde limpio.** Haz un clon o una extracción nueva y ejecuta todas las suites y `./tools/check_all.sh`. Ejecuta con `python3 -I` el código que lea archivos descargados o extraídos.
2. **Comprueba los criterios de aceptación** de `01_plan.md` uno a uno, con evidencia (una prueba, una salida o un script).
3. **Intenta romperlo.** Escribe tus propios scripts de ataque en `docs/tareas/<tarea>/revisores/`, numerados y sin sobrescribir los de rondas anteriores (`r01_…`, `r02_…`). Prueba como mínimo:
   - valores límite, cero, negativos, `None`, NaN, infinito y tipos inesperados;
   - repetir la misma operación (idempotencia) y cambiar el orden de las llamadas;
   - la hora justo en el borde de una ventana o de una caducidad;
   - estados guardados antiguos o manipulados (¿lo detecta `integridad()`?);
   - que un fallo a mitad de operación deje el estado intacto.
4. **Comprueba los invariantes del sistema:**
   - ningún camino llega a una orden sin pasar por F y G;
   - no hay LLM en la ruta determinista ni en los controles;
   - los controles nunca se relajan solos;
   - todo falla cerrado y valida antes de mutar;
   - ningún número escrito a mano;
   - ninguna decisión del operador tomada en silencio (deben ser `[PROPUESTO]` y estar en la deuda);
   - nada de secretos ni datos personales o financieros en el repo;
   - documentación al día: LEEME, deuda técnica, y briefing si cambió la arquitectura.
5. **Registra los hallazgos** en `docs/tareas/<tarea>/04_qa.md`. Para cada uno: ID (`H-01`…), gravedad (crítica, alta, media o baja), cómo reproducirlo, qué se esperaba y qué pasó, y una corrección sugerida.
6. **Emite el veredicto:**
   - **APTO**: todos los criterios cumplidos y ningún hallazgo crítico ni alto abierto. Los medios y bajos que no se corrijan pasan a la deuda técnica con su ID.
   - **NO APTO**: en cualquier otro caso.

## Si es NO APTO

Quien implementó corrige cada hallazgo con su prueba de regresión (`ri-implementar` → `ri-probar`). Después, el revisor **vuelve a ejecutar sus propios scripts** de `revisores/`, no solo las pruebas del implementador, y añade una ronda nueva al `04_qa.md`.

## Si es APTO: cerrar la tarea

1. Actualiza la deuda técnica (cierra la T-xx o añade lo pendiente), el LEEME y el briefing si cambió la arquitectura.
2. Escribe en tu carpeta de `memoria/` las lecciones útiles para el futuro y, si sirven a los dos agentes, en `memoria/compartida/`.
3. Commit en `develop` (mensaje en español con prefijo de área, sin `[pendiente QA]`) y push.
4. Mensaje final al operador, en español y breve: qué cambió, el veredicto y el siguiente paso.
5. Los entregables (ZIP, exportaciones) se preparan solo cuando el operador los pide.
