# T-83 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-10 · de claude a astra (o un revisor nuevo sin contexto)

- **Fase en la que se entrega:** QA.
- **Hecho:**
  - módulo `sistema_global/marco_comun_c/validador/parametros_doc.py`, con 85 claves documentadas: 4 RATIFICADO, 77 PROPUESTO y 4 TECNICO;
  - batería `sistema_global/marco_comun_c/pruebas/pruebas_parametros_doc_t83.py`, con 62 comprobaciones;
  - LEEME del marco y Documento 0 `sistema_global/documentos_0/V0.72_Valores_por_defecto_documentados.md`;
  - las 61 baterías del marco en verde y `leeme_marco.py` sin diferencias.
- **Falta:**
  - la QA;
  - el commit, que no lo ha hecho el implementador por indicación de quien encargó la tarea;
  - las filas de la deuda técnica (T-83 y la nota de PC3-07), que no se tocaron por la misma indicación.
- **Commit:** ninguno todavía. Los cambios están en el árbol de trabajo de `develop`: el LEEME modificado y cuatro rutas nuevas, la carpeta del ticket incluida.
- **Cuidado con:**
  - **Estados.** Revisar a mano el estado y la fuente de cada registro, sobre todo:
    - `nivel_autonomia` como RATIFICADO (§6 con D-45);
    - `autoria_c` y `autoria_contradictor` como PROPUESTO;
    - los cuatro TECNICO.
  - **Redacción.** Las justificaciones y preguntas: la batería solo comprueba su forma.
  - **Fuentes.** «Deuda D-xx» es la tabla de pendientes del operador de la deuda técnica, no la Constitución.
  - **Mypy de B.** El gate completo falla en `mypy bloque_b` (160 > 159), pero eso ya pasa con HEAD (`99160b3`, T-90) y no viene de esta tarea.
- **Scripts útiles:** `.docs/scripts/pruebas_marco.sh`, `.docs/scripts/leeme_marco.py`, `.docs/scripts/gate.sh`.
