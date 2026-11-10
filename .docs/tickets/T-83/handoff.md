# T-83 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-10 · de claude a un revisor nuevo sin contexto (QA r02)

- **Fase en la que se entrega:** QA, ronda r02.
- **Hecho:** los hallazgos H-01 a H-06 de `qa.md` están corregidos, y su detalle, por hallazgo, va en `analisis-tecnico.md`, en «Ronda r02».
  - Hay 105 registros: 6 RATIFICADO, 94 PROPUESTO y 5 TECNICO. Salen 87 preguntas pendientes.
  - Las claves compuestas se documentan campo a campo en `SUBTABLAS`.
  - Cada registro lleva el valor que justifica (`valor_documentado`), y `desfasados()` avisa si el código lo cambia.
  - `cerrada_por` marca el apalancamiento, que D-16 no deja preguntar hasta la Fase 3.
  - La batería tiene 109 comprobaciones.
  - `.docs/tickets/T-83/r02_contra_head.py` da FALLA con HEAD y OK con el árbol para cada hallazgo.
  - Las 61 baterías del marco están en verde.
- **Falta:** la QA r02 y el commit. El implementador no lo ha hecho, por indicación de quien encargó la tarea.
- **Commit:** ninguno. Los cambios de T-83 están en el árbol de `develop`, sobre `1a91d28`:
  - el módulo, la batería, el LEEME y el Documento 0 V0.72;
  - en la carpeta del ticket: README, `analisis-tecnico.md`, `pruebas.md`, este traspaso y `r02_contra_head.py`.

  En el mismo árbol hay cambios sin commit de otros trabajos: V0.73, de T-75 y T-76, que también tocan el LEEME; y T-65 y T-84.
- **Cuidado con:**
  - **Criterio de RATIFICADO** con el apalancamiento a cero (F y mandato). Mirar también los que siguen PROPUESTO con el mismo criterio: `exposicion_max_pct`, `matriz_autonomia` y `exige_contradictor_en`.
  - **TECNICO.** `referencias.benchmark_ref` se dejó TECNICO porque la configuración exige que coincida con el del mandato.
  - **`_VALOR_DOCUMENTADO`** es una copia deliberada de los valores. Se explica en el análisis.
  - **Sondas de la QA r01.** Las del ticket esperan el comportamiento antiguo: `r01_mutaciones_bateria.py` da ahora 5 diferencias, que son las corregidas, y `r01_contenido.py` lee `pd.doc("aprobacion", …)["pregunta"]`, que ahora es None porque la pregunta va en cada campo.
- **Scripts útiles:** `.docs/scripts/pruebas_marco.sh`, `.docs/scripts/leeme_marco.py`, `.docs/tickets/T-83/r02_contra_head.py`.

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
