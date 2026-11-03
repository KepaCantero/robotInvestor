# PROMPT — Fase 2 · Fichas restantes por prioridad (bloque_a)

> Sesión de implementación mecánica. Modelo: Sonnet. Requisito: Fase 1 verificada.

---

FASE 2 — Continuar con las fichas que el verificador de la Fase 0 clasifique como SOLO_CATALOGO y que no se hicieron en la Fase 1, EN ORDEN de prioridad del Catálogo (P0 primero, luego P1; P2+ solo si el propietario lo pide expresamente).

Kit de contexto: el mismo de la Fase 1 (Catálogo V5.0, operaciones.py, servicio.py, test_unitarias.py) + la tabla de estado de la Fase 1 en docs/AVANCE.md.

Reglas adicionales de esta fase:
- Trabaja por FAMILIAS completas (termina una familia antes de abrir la siguiente): menos contexto que cambiar, menos errores.
- Si una ficha P0 depende de otra P1, respeta el orden de dependencia y documéntalo.
- Las fichas «Implementado (heredado)» no se reescriben: se verifica que el comportamiento existente cumple la ficha y, si no, se documenta la discrepancia en docs/incidencias.md sin cambiar el código en esta fase.
- Cada sesión de esta fase puede cerrarse por familia: mejor 3 sesiones pequeñas y verificadas que una grande.

Entregables y criterio de éxito: iguales que la Fase 1 (tests crecen, cero fallos, tabla actualizada, `fase2:`).

Restricciones fijas: corpus .md intocable; otros bloques intactos; nada en silencio.
