# Índice · memoria de Claude

| id | tipo | resumen | vigencia |
| --- | --- | --- | --- |
| claude/2026-11-09_lecciones-marco-c | leccion | Trampas técnicas del marco común de C: huella de esquema, migraciones, versiones, pruebas | vigente |
| claude/2026-11-09_metodo-por-version | convencion | Método que sigo para cada versión del marco y cómo cierro | vigente |
| claude/2026-11-09_lecciones-integracion | leccion | Cómo integrar trabajo de otro agente sin perder cambios | vigente |
| claude/2026-11-10_via-directa-v068 | leccion | T-80/V0.68: reutilizar análisis entre expedientes exige mirar a todos los que lo tienen o lo tuvieron (encargo, caducidad, reanálisis, apartados) y bloquear el reencargo mientras está en juego; un commit con el árbol a medias de otra tarea cuelga el gate: pásalo en un worktree limpio | vigente |
| claude/2026-11-10_t75-embudo | leccion | QA r02 NO APTO: anotar un evento nuevo en el historial (veto de F) cambia lo que leen otros consumidores del historial (contratos.propuesta toma la última anotación hacia PROPUESTA). Al anotar, buscar todos los lectores del historial y cubrir todas las rutas de entrada (pantalla_aprobacion además de autorizar). | vigente |
| claude/2026-11-10_t65-cierre | leccion | T-65 cerrada en la r05 tras cinco rondas: las tolerancias de frescura deben atarse al horizonte y exigir a cada serie un dato posterior a la emisión; una regla nueva de resolución (PS2) hay que marcarla [PROPUESTO] y registrarla como incidencia en la misma ronda (H-27 quedó en T-91). | vigente |
| claude/2026-11-11_t92-filtro-secretos | leccion | Un filtro de secretos que intenta reconocer la forma de una clave falla siempre por algún lado (r02 y r03 de T-92); es más robusto invertir: todo candidato es clave salvo que tenga forma de texto corriente (tramos que son palabras, siglas, años o periodos), con un candidato lineal en regex y la decisión en Python. Y al portar una rama vieja: fusionar sobre lo cerrado después (T-65) y conservar sus reglas. | vigente |
