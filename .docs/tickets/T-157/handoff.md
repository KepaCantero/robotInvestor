# T-157 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-15 · de claude (implementa y prueba) a la sesión coordinadora y a un revisor nuevo (QA)

- **Fase en la que se entrega:** QA.
- **Hecho:** verificador, 34 pruebas, informe generado en `docs/auditoria_ids_bloque_a.md` y `.json`, INC-T157-01 a 05,
  entrada de `docs/AVANCE.md`, `tools/refs_allowlist.txt` sin las líneas de la Fase 0, README del ejecutor y una entrada de
  memoria. Commit local «wip local: T-157» en la copia `fase0`, sin push.
- **Falta:** la QA (r01) y el commit definitivo de la sesión coordinadora, con el mensaje propuesto de `pruebas.md`. La fila
  T-157 de la deuda técnica la lleva la coordinadora; las decisiones D-1 a D-4 quedan propuestas (la D-1, de código, podría ir
  a la deuda como tarea del Motor; D-2 a D-4 esperan a la próxima entrega del corpus).
- **Commit:** el local «wip local: T-157» (su hash, en el informe a la coordinadora).
- **Cuidado con:**
  - Los INFO `CITA_EN_CONTEXTO_AJENO` son la parte discutible: comprobar en el corpus que cada uno es lo que dice (JEL, fórmula,
    función local, campo JSON) y buscar un caso que deberían marcar y no marcan.
  - El documento de auditoría lleva huellas de `servicio.py` y `contratos.py`; si otra tarea los cambia antes de la QA, el
    informe queda desfasado: se regenera con `--auditoria` (no es un fallo del verificador).
  - El verificador importa el paquete: ejecutarlo desde `bloque_a/11_Ejecutor` para que lea esta copia y no la que el `.venv`
    tiene instalada en modo editable.
  - Los mutantes de `.docs/tickets/T-157/mutantes_t157.py` sirven de punto de partida para la QA.
- **Scripts útiles:** ninguno de `.docs/scripts/` nuevo; la orden es `python -m bloque_a.herramientas.verificador_ids`.
