---
id: compartida/2026-11-09_revision-bloque-a
autor: claude
fecha: 2026-11-09
tipo: estado
etiquetas: [bloque_a, T-53, qa]
fuente: .docs/tickets/T-53/
vigencia: sustituida por compartida/2026-11-10_bloque-a-terminado
---

**Estado del Bloque A tras T-53 (9-11-2026).**
- El ejecutor (`bloque_a/11_Ejecutor/`) está corregido frente a su Documento 0 V5.1. Línea base: 117 pruebas.
- QA r01: NO APTO; r02: APTO. Las medias, H-01 a H-05 y H-12, están corregidas con pruebas de regresión. El ticket está cerrado.
- `Bloque` trabaja con una copia propia de la configuración. No vuelvas a escribir en el dict del llamador.
- Las propuestas PA-01 a PA-21 (`propuestas.md`) **no se han aplicado**. Las decide el operador, y cada una tendrá su ticket.
- Pendiente técnico: la fila T-65 de la deuda técnica.

**Cómo aplicarlo:**
- No conectes A a C ni a B hasta que el operador haya visto las propuestas (D-42).
- Todo umbral nuevo va a `config/por_defecto.yaml` con `[PROPUESTO]`.
- Las copias de HT-03 y HT-09 en `10_Herramientas/` y en el ejecutor deben seguir idénticas: si cambias una, copia la otra y vuelve a congelar el corpus a propósito.
