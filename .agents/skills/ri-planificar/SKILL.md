---
name: ri-planificar
description: Fase 1 de 4 del flujo de trabajo del Robot Investor (planificar → implementar → probar → QA). Úsala antes de construir o cambiar cualquier bloque, contrato, esquema, versión del marco común de C o documento de arquitectura, o cuando pidan «planifica», «diseña», «cómo lo haríamos». Deja un plan con criterios de aceptación y plan de pruebas en docs/tareas/.
---

# Planificar una tarea del Robot Investor

Fase 1 de 4. Después viene `ri-implementar`. Visión de conjunto: `docs/flujo_de_trabajo.md`.

Esta skill la usan dos agentes (Claude y Astra) sobre el mismo repositorio. Escribe todo en español y deja cada resultado en un archivo del repo, nunca solo en la conversación: el otro agente tiene que poder continuar sin preguntarte.

## 1. Carga el contexto mínimo

No leas el repositorio entero (regla 1 de `CLAUDE.md`, válida para cualquier agente).

1. Memoria: `memoria/LEEME.md`, el `INDICE.md` de `memoria/compartida/` y el de tu propia carpeta. Abre solo las entradas que toquen la tarea.
2. Constitución global (`sistema_global/constitucion/Constitucion_Global.md`): solo las secciones afectadas.
3. El Documento 0 de la pieza (`sistema_global/documentos_0/` o el del bloque).
4. La deuda técnica (`sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`): busca el ID de la tarea (T-xx) y lo que dependa del operador.
5. Si es tu primera sesión: el briefing (`sistema_global/seguimiento/Briefing_de_arranque.md`).

## 2. Clasifica la tarea

| Tipo | Qué exige antes del plan |
| --- | --- |
| Bloque o pieza sin construir | Conversación de diseño (brainstorming) con el operador. Nunca se planifica en solitario. |
| Revisión o mejora de los bloques A o B | Revisión con el operador antes de conectarlos al resto. |
| Cambio de la Constitución o de los controles (F, G, kill-switch, niveles de autonomía) | El operador aprueba el plan por escrito. |
| Versión del marco, corrección, pruebas, documentación | El agente planifica y sigue. |

## 3. Reglas del operador que condicionan cualquier plan

- A y B analizan todo tipo de activo. Todo bloque es núcleo general + perfiles; hoy solo el perfil C-DIV (divisas) es específico. La Fase 1 se queda en divisas.
- Las decisiones de perfil y técnicas del operador están aplazadas hasta completar la arquitectura (T-57). No preguntes por ellas: usa un valor por defecto marcado `[PROPUESTO]`, en simulado, y apúntalo en la deuda técnica.
- Todo lo que dependa del operador va a la deuda técnica.
- Ante una ambigüedad de la especificación: pregunta o registra una incidencia en `docs/incidencias.md`. No decidas en silencio.
- Una tarea toca un solo bloque (regla 8), salvo la interfaz de contratos entre bloques.
- Ningún número se escribe a mano: cada umbral sale de la configuración o del Documento 0.

## 4. Escribe el plan

Crea `docs/tareas/<AAAA-MM-DD>_<pieza>_<tema>/01_plan.md` con la plantilla `plantilla_plan.md` de esta carpeta. Si es una versión nueva del marco, el Documento 0 de esa versión se escribe antes que el código y el plan lo enlaza.

Un buen plan permite a otro agente implementar sin preguntar: dice qué cambia, qué no, cómo se sabrá que está bien y qué podría salir mal.

## 5. Puerta de salida (todas en verde para pasar a implementar)

- [ ] Criterios de aceptación binarios (se cumplen o no) y plan de pruebas escritos.
- [ ] Cambios de contrato o de estado persistido identificados (versión de esquema y migración si aplica).
- [ ] Decisiones del operador marcadas `[PROPUESTO]` y apuntadas en la deuda técnica.
- [ ] Aprobación del operador anotada en el plan si el tipo de tarea la exige.
- [ ] Asignados quién implementa y quién hace QA, que deben ser agentes distintos.
- [ ] Si otro agente implementará: entrada de traspaso en `memoria/compartida/` (tipo `traspaso`).
