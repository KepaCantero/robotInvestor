# Relevo para Astra · tareas pendientes al 10-11-2026

De: Claude. Para: Astra. Lo pide el operador el 10-11-2026: **que Astra trabaje hasta completar todas las tareas pendientes y que todas pasen su QA (APTO)**. Este documento dice qué hacer, en qué orden, con qué reglas y cómo se repite cada ronda hasta el APTO. El detalle de cada hallazgo está en el `qa.md` de su ticket; aquí solo se resume.

## 0. Antes de empezar (obligatorio)

1. `git pull origin develop` y `git log --oneline -8`. Los últimos commits de Claude son `7b775cc` (V0.73), `476f163` (T-75 detenida), `0bcefbc` (T-76 detenida y r02 de T-83), `5fe0c20` (T-65 r04), `2e4c510` (T-84 c1) y el del cierre de T-65 con este relevo.
2. Lee `AGENTS.md`, `CLAUDE.md`, `.docs/README.md`, `.docs/memoria/LEEME.md` y el `INDICE.md` de `.docs/memoria/compartida/`.
3. Para cada tarea, lee **solo** su ticket (`.docs/tickets/T-NN/`) y su fila en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`. No leas el repositorio entero.
4. Antes de cada tarea, `git pull`: Claude puede estar subiendo cosas a la vez.

## 0 bis. Fuera de tu alcance hasta nuevo aviso (operador, 11-11-2026)

El operador va a discutir con Claude la arquitectura del Bloque B y de los demás bloques antes de construir nada más. Hasta que lo dé por cerrado:
- **No toques `bloque_b/`** ni sus tickets, ni abras tareas nuevas del Bloque B. Claude está evaluándolo; es solo lectura y medición, sin cambios.
- **No abras las tareas que dependen de esa arquitectura:** T-87 (SC-5), T-81 (SC-4 mínimo), T-82 (escalera de verificación y CT-G-17), T-74 (controles de F) y T-73 (perfil inversor). En el §3.6 quedan marcadas como «en espera».
- **Excepción, y tus primeras tareas: revisar las propuestas de diseño de Claude en el orden natural de los bloques (operador, 11-11-2026: «ordena a Astra que evalúe las propuestas siguiendo el orden natural de los bloques»).** Son solo lectura, medición y opinión: no se escribe nada en ningún bloque ni en el marco común. Índice de las propuestas en `.docs/diseno/README.md`. Una revisión por bloque, con su entregable y su commit, y en este orden, antes que el resto de tus tareas:
  1. **A**, el rediseño: `.docs/diseno/bloque_a/encargo_revision_astra.md`.
  2. **B**, la evaluación de T-68 y el rediseño juntos: `.docs/tickets/T-68/encargo_revision_astra.md` y `.docs/diseno/bloque_b/encargo_revision_astra.md`.
  3. **C**: `.docs/diseno/bloque_c/encargo_revision_astra.md`.
  4. **D**: `.docs/diseno/bloque_d/encargo_revision_astra.md`.
  5. **E**, que comparte objetivo con D: `.docs/diseno/bloque_e/encargo_revision_astra.md`.
  6. **F**: `.docs/diseno/bloque_f/encargo_revision_astra.md`. T-74 sigue en espera: la revisión es solo de diseño.
  7. **G**: `.docs/diseno/bloque_g/encargo_revision_astra.md`.
  8. **H**: `.docs/diseno/bloque_h/encargo_revision_astra.md`.
  9. **I**: `.docs/diseno/bloque_i/encargo_revision_astra.md`.
  10. **Enmienda 4** a la Constitución, al final porque toca los diseños anteriores: `.docs/diseno/enmienda_4/encargo_revision_astra.md`.

  Si Claude añade propuestas de más bloques (J, K, M, N), van en su orden natural antes de la enmienda 4.

  Si al revisar un bloque ves algo que cambia tu opinión sobre uno anterior, añádelo como nota al final de la revisión anterior, con fecha, en lugar de reescribirla.
- [PROPUESTO] hasta que el operador lo decida (pregunta 2 de la propuesta de A): mientras no cierre el diseño de A, en T-93, T-91 y T-88 cambia solo lo que sirve en cualquier diseño (código, contratos y seguridad), sin tocar prompts ni papeles de los agentes.
- **Sí sigues con:**
  - las del marco: T-83, T-84, T-75 y T-76;
  - las del Bloque A: T-93, T-91 y T-88.
- Si una de las tuyas te obliga a cambiar un contrato con el Bloque B (CT-B-…) o la interfaz de encargos A→B, para y pregúntale al operador.

## 1. Reglas que no cambian

- **Rondas hasta el APTO (sustituye la regla anterior de una sola ronda; operador, 10-11-2026: «Quiero que Astra trabaje hasta completar todas las tareas y que pasen las QAs»).** Cada tarea sigue este ciclo hasta que su QA dé APTO:
  1. Implementar o corregir los hallazgos de la ronda anterior. Se corrigen todos: críticos, altos, medios y bajos. Solo pasa a la deuda, con su ID, lo que de verdad no se pueda hacer en la tarea, y se explica por qué.
  2. Probar: baterías, LEEME y gate (§2), y que cada prueba nueva falle con el código anterior.
  3. Commit de la ronda, con el ticket EN QA (ronda rNN).
  4. QA independiente de la ronda: veredicto en `qa.md`, en su sección «Ronda rNN».
  5. Si sale NO APTO: commit del `qa.md` y de las sondas, y vuelta al paso 1 con la ronda siguiente. **No se detiene la tarea ni se espera al operador.**
  6. Si sale APTO: la tarea se cierra (CERRADO en el ticket, RESUELTO en la deuda) y se pasa a la siguiente.
- **La QA la hace siempre un revisor que no implementó esa ronda.**
  - Si Astra implementó o corrigió, la QA la hace un revisor nuevo sin contexto: otra sesión o subagente de Astra que no vio la implementación, o Claude si el operador lo pone.
  - Cada ronda lleva un revisor nuevo, que reproduce todo desde limpio y no se fía del informe del implementador.
  - Si implementó Claude, la QA la puede hacer Astra directamente.
  - Si esa QA da NO APTO y Astra corrige, la ronda siguiente la revisa otro revisor nuevo.
- **Aviso al operador sin parar.** Si un mismo hallazgo vuelve en tres rondas seguidas, o una corrección rompe algo que ya estaba bien, escribe una nota corta en el diario y en tu mensaje al operador. Después sigue.
- **Decisiones del operador:** no se le preguntan. Valor por defecto marcado `[PROPUESTO]`, en simulado, y anotado en la fila T-57 de la deuda.
- **Lo único que sí espera al operador:**
  - un cambio de los controles (F, G, kill-switch, niveles de autonomía) o de un contrato CT-G-xx, que necesita su aprobación del plan por escrito;
  - una pieza nueva, que necesita una conversación de diseño con él.

  En esos casos escribe el plan o las preguntas de diseño en el ticket, pídeselo y **sigue con las demás tareas mientras esperas**.
- **Repositorio público:** nada de secretos ni de datos personales o financieros. Los secretos solo en `.env`, que no se sube.
- **Nunca se borra nada en `.docs/`:** lo viejo se marca CERRADO o SUSTITUIDO. Escribe memoria solo en `.docs/memoria/astra/` y `compartida/`.
- **Si el proxy o una política deniega algo:** se informa al operador; no se busca otra vía.
- **Al terminar cada tarea:**
  - ticket con su estado;
  - fila de la deuda;
  - Documento 0;
  - una entrada en el diario: `.docs/scripts/diario.sh "Título" astra`, rellenando sus cuatro apartados;
  - una entrada en la memoria: `.docs/scripts/memoria.sh astra <tema> <tipo> "<resumen>" --autor astra`;
  - y, si cambia la versión del marco, `CLAUDE.md`, `sistema_global/README.md` y el LEEME del marco.

## 2. Cómo se prueba y se sube

- **Marco común de C:**
  - todas las baterías: `.docs/scripts/pruebas_marco.sh`, que debe dar 61 o más y 0 fallos;
  - el LEEME contra el disco: `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c`, que debe dar «SIN DIFERENCIAS».
- **Gate:** `.docs/scripts/gate.sh --completo` debe dar 12/12. Hoy da A 326, A-Forex 68 y B 176.
- **Subir con el árbol limpio:** `.docs/scripts/commit.sh "mensaje" rutas… --completo`.
- **Subir con el árbol con cambios a medias de otra tarea:** usa `.docs/scripts/commit_limpio.sh "mensaje" ruta…`.
  - Hace una copia de HEAD con solo esas rutas y pasa allí las pruebas del marco, su LEEME y el gate completo.
  - Después sube las copias probadas.
  - Autor y líneas finales: `GIT_AUTOR_NOMBRE`, `GIT_AUTOR_EMAIL` y `GIT_TRAILERS` de tu `.env`.
- **Si cambia una constante en mayúsculas, `CONFIG_DEFECTO`, un atributo del Orquestador o un parámetro, cambia el esquema del código.** Pasos, desde `sistema_global/marco_comun_c`:
  1. `../../.venv/bin/python validador/migraciones.py --registrar-esquema V0.xx`, sin `-I`.
  2. Añadir `ESQUEMA_V0_xx` y una `Migracion(...)` nueva en `validador/migraciones.py`. La última hoy es MIG-009 (`_sin_cambios`).
  3. Actualizar los anclajes:
     - `pruebas/pruebas_integracion_v053.py`: esquema actual, última MIG y cadenas de MIG;
     - `pruebas/pruebas_comparador_t17.py`: `VERSION_PARAMETROS`, si cambia `parametros.py`;
     - `pruebas/pruebas_catalogo_codigos.py`: número de avisos, si añades códigos O-xx.
- **Patrones del Orquestador** (`validador/orquestador.py`):
  - `@_seguro` solo restaura el reloj si la operación se rechaza;
  - se valida antes de mutar;
  - se devuelve `_r(...)` o `_no(codigo, motivo)`;
  - los registros encadenados usan `_anota`, `_historial_ok` y `*_ok()` dentro de `integridad()`.
- **Que cada prueba nueva falle con el código anterior:** cambia el fichero por su versión de HEAD (`git show HEAD:ruta > ruta`), comprueba que la prueba falla y restáuralo.

## 3. Orden de trabajo

### 3.1 T-83 · QA r02 (la hace Astra; implementó Claude)

- **Qué es:** `validador/parametros_doc.py` documenta como datos los valores por defecto (D-45): estado, fuente, justificación y pregunta del cuestionario de T-57.
- **Commit:** `0bcefbc`.
- **Ronda r02:** corrige los seis hallazgos de la r01 (H-01 a H-06, en `.docs/tickets/T-83/qa.md`). La batería pasa de 62 a 109 comprobaciones.
- **Qué revisar:**
  - **H-01:** `apalancamiento_max` de F y del mandato es RATIFICADO por D-16 y D-45, sin pregunta.
  - **H-02:** las claves compuestas se documentan campo a campo (20 campos).
  - **H-05:** `valor_documentado` y `desfasados()`.
  - **H-06:** `preguntas_pendientes()` falla cerrado.
  - Que ningún otro valor ratificado por la Constitución siga como PROPUESTO.
- **Pruebas:**
  - `.docs/tickets/T-83/r02_contra_head.py` debe dar FALLA con HEAD~ (la V0.72 de `dd96e19`) y OK con el árbol, en los seis hallazgos.
  - La sonda `r01_contenido.py` de la r01 lee la pregunta de `aprobacion` como texto. Ahora va campo a campo, así que hay que adaptarla.
- **Salida:** veredicto en `.docs/tickets/T-83/qa.md`, con el título «Ronda r02».
  - Si sale APTO, la tarea se cierra.
  - Si sale NO APTO, Astra corrige (r03) y la QA de la r03 la hace un revisor nuevo de Astra. Así hasta el APTO (§1).

### 3.2 T-84 · QA r02 de las correcciones c1 (la hace Astra; implementó Claude)

- **Qué es:** la revisión de la V0.63, la semana simulada de GLM.
- **Qué corrige la ronda c1:** los hallazgos de la r01 (`.docs/tickets/T-84/qa.md`; resumen en `analisis-tecnico.md`):
  - H-01: `pruebas/pruebas_semana.py` no ejercitaba el Reloj que decía ejercitar;
  - H-02, H-03 y H-07: huecos de batería (ahora `semana` tiene 176 comprobaciones y `reloj_t03`, 80);
  - H-06: `validador/diario.py` borra al abrir los temporales huérfanos;
  - H-08: nota en `entrega_glm/V0.63/revision.md`.
- **Estado de partida:** el agente de c1 se paró mientras pasaba el gate final, y Claude lo subió en `2e4c510` con `commit_limpio.sh`: baterías del marco, LEEME y gate 12/12 sobre una copia limpia. Repite tú esas comprobaciones al empezar la QA.
- **Desviaciones declaradas que hay que juzgar:**
  - la de H-01: contrasta en cada paso porque la máquina va por detrás del intermediario;
  - H-04 llevado a la deuda: el Reloj no da instantes hasta un `comprobar_estado` bueno, lo que cambia el contrato de `Reloj`.
- **Salida:** «Ronda r02» en `qa.md`. Si sale NO APTO, sigue el mismo ciclo que T-83 hasta el APTO.
- **H-04 de la deuda:** el Reloj no da instantes hasta un `comprobar_estado` bueno. Va con T-84 si su QA lo exige; si no, queda en la deuda.

### 3.3 T-75 · Ronda r03 (implementa Astra; la QA la hace otro agente)

- **Qué es:** el embudo visible y la alarma de sequía, en el marco V0.73.
- **Autorizada por el operador** (10-11-2026). Sigue el ciclo del §1 hasta el APTO.
- **Pendientes** (detalle en `.docs/tickets/T-75/qa.md`, «Ronda r02»):
  - **H-09 (media):** el veto de F solo se anota si el informe que veta llega directo a `autorizar()`. Por `pantalla_aprobacion()`, el camino normal del operador, sale O-06 y no se anota nada.
    - *Sugerencia:* un único punto común que anote el veto, llamado desde las dos rutas.
  - **H-10 (media, regresión):** `contratos.propuesta()` toma la última anotación que llega a PROPUESTA. Tras un veto es la de F, y la CT-G-06 sale con F como emisor, `ct.validar()` da CT-03 y cambia el `event_id`.
    - *Sugerencia:* que `propuesta()` ignore las anotaciones de veto (motivo `MOTIVO_VETO_F`), o anotar el veto fuera de la cadena que lee `propuesta()`.
    - Añade una prueba que valide la CT-G-06 después de un veto.
    - Antes de cambiar nada, busca todos los lectores del historial del expediente.
  - **H-11 (baja):** el veto se anota en una llamada rechazada que no adelanta `ultimo_ahora`, porque `@_seguro` restaura el reloj. Una operación posterior con una hora anterior queda desordenada en el historial. Hay que decidir una de dos cosas y probarla: que esa anotación adelante el reloj, o que no se anote en un rechazo.
  - **H-12 (baja, documentación):**
    - en el LEEME, las filas de `orquestador.py`, `consola.py` y `parametros.py` y el registro de prefijos deben llegar hasta O-42;
    - en el LEEME, la línea «Comprobado en el embudo…»;
    - en el Documento 0 V0.70, los §2 a §5 (V0.73, MIG-009 y el recuento);
    - en la deuda, los dos límites del análisis técnico;
    - en `pruebas.md`, el resultado de las baterías y del gate.
  - **H-13 (baja):** el docstring de `embudo()` dice que un expediente revalidado no suma, y con otro sobre cuenta 2. Corrige el texto o la cuenta.
  - **H-14 (baja):** sin inversiones, un sistema 1 µs más joven que 60 días ya juzga la sequía. Usa la comparación de borde correcta.
- **Sondas:** las de la QA están en `sistema_global/marco_comun_c/entrega_claude/V0.70/qa/`. La r02 es `r02_sondas_embudo_sequia.py`, y sus 5 sondas que marcan deben pasar a OK.

### 3.4 T-76 · Ronda r03 (implementa Astra; la QA la hace otro agente)

- **Qué es:** la cartera sombra pasiva, en el marco V0.73.
- **Autorizada por el operador** (10-11-2026). Sigue el ciclo del §1 hasta el APTO.
- **Ojo:** toca el mismo `validador/orquestador.py` que T-75. Hazlas una detrás de otra, sin mezclar. Si las dos cambian el esquema, puede ir todo en una sola versión del marco (V0.74, con MIG-010), como se hizo en la V0.73. Cada ticket lleva su propia QA.
- **Pendientes** (detalle en `.docs/tickets/T-76/qa.md`, «Ronda r02»):
  - **H-10 (media):** el mes se valora en el instante en que se compara, no a su cierre. Entran los movimientos, el coste de la sombra y el `gasto_dia` posteriores al cierre. Ejemplo: una retirada el día 2 con el mes comparado el día 3 da SUPERA a un robot que pierde y calla el O-41.
    - *Sugerencia:* `estado_sombra(..., hasta=cierre del mes en UTC)` con solo las entradas anteriores o iguales al cierre, y los costes de análisis hasta el cierre.
    - Declara en el contrato de `comparar_sombra` que `robot_valor_eur` y `precio_indice` son los del cierre del mes.
  - **H-11 (baja):** `iniciar_sombra(1e200, 1e-200)` deja unidades infinitas y la sombra inservible. Hay que rechazarlo antes de anotar, y comprobar que el resultado es finito.
  - **H-12 (baja):** `iniciar_sombra` y `movimiento_sombra` leen el registro antes de comprobar su integridad. Hay que poner `_sombra_precheck` primero. Además, `barrer()` con el registro tocado no debe callar: tiene que saltar el kill-switch o el O-13, no quedar en silencio el O-42.
  - **H-13 (baja):** el O-42 salta en el mismo instante del fin de mes.
    - Añade un plazo de gracia como parámetro `[PROPUESTO]` en `parametros.py` y en la fila T-57.
    - Avisa de todos los meses pendientes.
    - Sube la prioridad a ALTA si lo que falta es el mes de juicio.
  - **H-14 (baja):** sobreviven cuatro mutantes. Hacen falta pruebas que los maten:
    - el mes del inicio en hora local;
    - el O-42 del mes en curso;
    - una tolerancia absoluta en lugar de la relativa de H-06;
    - quitar el `isfinite` de `estado_sombra`.
  - **H-15 (baja, documentación):**
    - en el Documento 0 V0.71, los §2 a §5;
    - en el LEEME, el punto de la sombra («coste devengado por tramos», O-41 al pasar a no superarla, O-42);
    - en la deuda, los límites H-07 y H-09 y el valor del robot sin contraste;
    - en `pruebas.md`, el resultado de las baterías y del gate.
  - **H-16 (baja):** MIG-009 reinterpreta en silencio las comparaciones de la V0.71. La V0.71 no llegó a operar. Basta con declararlo en la migración y en el Documento 0, o hacer que la migración lo deje explícito.
- **Sondas:** en `sistema_global/marco_comun_c/entrega_claude/V0.71/qa/`, las de la r02 son `r02_sondas_calculo.py`, `r02_sondas_juicio.py` y `r02_sondas_migracion.py`.

### 3.5 T-65 · Cerrada

- **Estado:** CERRADA el 10-11-2026 tras la QA r05 APTO. La línea base de A es ahora 326.
- **Pendiente:** sus cuatro hallazgos bajos (H-26 a H-29) pasan a la tarea nueva T-91 de la deuda. Ver §3.6.
- **Ya puedes tocar** `bloque_a/`.

### 3.6 Resto de la deuda técnica

Cuando estén cerradas las tareas del 3.1 al 3.4, sigue con estas, una cada vez, en el orden de la tabla y con el mismo ciclo hasta el APTO.
- Para cada una: si no tiene ticket, créalo con `.docs/scripts/nuevo_ticket.sh T-NN "Título" <pieza>`. Escribe el plan con la skill de planificar.
- Las que necesitan al operador:
  - escribe en el ticket el plan, o las preguntas de diseño, con valores `[PROPUESTO]`;
  - pídele su aprobación;
  - mientras tanto, pasa a la siguiente;
  - cuando responda, vuelve a esa tarea y sigue el ciclo.

| Tarea | Qué es | Qué hace falta antes |
| --- | --- | --- |
| T-91 | Bloque A: H-26 a H-29 de la QA r05 de T-65 (festivos de PS2 en la resolución de H1; fechas distintas de proxy y referencia; regla de PS2 sin marcar `[PROPUESTO]` ni registrar en `docs/incidencias.md`; documentación y mutantes vivos) | Ninguna; es técnica. La regla de H-27 se marca `[PROPUESTO]` y va a T-57 |
| T-93 | Bloque A: hallazgos medios y bajos de la QA r04 de T-92 (integración de tu auditoría; R8 con escapes, falsos positivos con URL de prensa, almacén anterior con la última línea a medias…) | Ninguna; es técnica. Corregir H-32 y H-34 antes del modo sombra con API. Tu rama `astra/bloque-a-integridad-y-evidencia` ya está integrada en develop como T-92 (salvo `preparar-encargo-b`): no la fusiones |
| T-88 | Bloque A: `presupuesto.consumido` de F5 cambia entre ejecuciones iguales con varios hilos | Ninguna; es técnica |
| T-87 | SC-5 con su registro de análisis compartido (sale de T-80) | Pieza nueva: diseñarla con el operador antes del plan; **en espera** de la discusión de arquitectura (§0 bis) |
| T-81 | SC-4 mínimo (tesis congeladas, torneo de pronósticos, calibración) | Pieza nueva: diseñarla con el operador, junto con PA-03 y PA-15 de T-67; **en espera** de la discusión de arquitectura (§0 bis) |
| T-82 | Escalera de verificación y ficha de bloque CT-G-17 | Pieza nueva y contrato nuevo: diseño y aprobación del operador; **en espera** de la discusión de arquitectura (§0 bis) |
| T-74 | Controles de F que faltan (volumen, liquidez, exposición compartida…) | Cambia F y el contrato CT-G-08: el operador aprueba el plan por escrito; **en espera** de la discusión de arquitectura (§0 bis) |
| T-73 | Perfil inversor en SC-1 | La estructura se puede planificar; los valores, en T-57; **en espera** de la discusión de arquitectura (§0 bis) |
| T-70, T-71 | Choques de los códigos O-00 y O-01 | Son de la Fase 2: renombrar exige migrar diarios ya escritos. Haz solo el plan, y pregunta al operador si las adelanta |

## 4. Qué entregar al operador

- **Al cerrar cada tarea con APTO:** un mensaje corto en español con:
  - la tarea;
  - cuántas rondas hicieron falta;
  - el commit;
  - lo que se pasó a la deuda y por qué.
- **Cuando haga falta su aprobación o una conversación de diseño:** un mensaje con lo que necesitas y dónde está el plan.
- **Al terminar todo:** una tabla con cada tarea, su estado final y su último commit.

La tarea está terminada cuando todas las del §3 tienen QA APTO, o cuando lo único que les falta es la aprobación o el diseño del operador.

Sin recapitular los pasos.
