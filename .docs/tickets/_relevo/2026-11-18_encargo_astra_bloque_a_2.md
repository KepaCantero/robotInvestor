# Encargo a Astra · otros cinco tickets del Bloque A (18-11-2026)

Lo pidió el operador el 18-11-2026: «aprovecha para crearle unas tareas nuevas a Astra. Dale otros 5 tickets relacionados con la implementación del bloque A. Dale las directrices para que haga exactamente lo que haces tú hasta pasar la QA en apto. Las correcciones de los hallazgos bajos también. […] Quiero que las finalice completamente».

Son las tareas C-43 a C-47 de `.docs/tickets/_relevo/cola_astra.md`. Van **después de C-38 a C-42**, que son las del encargo del 17-11-2026 (`.docs/tickets/_relevo/2026-11-17_encargo_astra_bloque_a.md`), y **antes que cualquier otra tarea de la cola**.

Las directrices de este documento valen **para las diez tareas, de C-38 a C-47**. Desarrollan las del 17-11 y, si algo choca, mandan estas.

## Qué significa «terminada»

Una tarea solo está HECHA cuando se cumplen las cinco cosas:

1. La QA del otro agente ha dado **APTO**.
2. **Ningún hallazgo** de la QA queda abierto, tampoco los bajos. Se corrigen todos en el mismo ticket.
3. El revisor ha comprobado esas correcciones y ha dado el **veredicto final APTO**.
4. El ticket está **integrado en `develop`** con el gate en verde (12/12).
5. El ticket, la deuda, el diario y la cola dicen **CERRADO o HECHA**.

«EN QA» no es terminada. Un APTO con bajos abiertos tampoco. Nada se aplaza a la deuda.

## Los cinco tickets

Son casos del plan de pruebas del Bloque A que hoy salen «Superada en parte» en `docs/evidencias_pruebas_bloque_a.md`. La columna «No comprueba» de cada fila dice qué falta (resumido abajo; manda el fichero regenerado), y el criterio completo está en el plan (`bloque_a/09_Pruebas/`), buscando por su ID. El objetivo es que el caso pase a «Superada» o que lo que quede sin comprobar esté motivado (tiempo real, API real o usuarios).

| Cola | Ticket | Casos | Qué falta, en resumen | Dónde mirar primero |
| --- | --- | --- | --- | --- |
| C-43 | T-188 | PB-11 y PB-62 | La lección de producto (LEC-) que no genera el Evaluador (INC-T116-03): en PB-11, la que compara las ideas enviadas con las descartadas cuando haya muestra; en PB-62, la de la consulta recurrente (el aviso CONSULTA_RECURRENTE ya sale) | El Evaluador y la CT-23. T-161 y T-171 fijaron que las lecciones de PRODUCTO no llegan a los agentes de control: no lo deshagas |
| C-44 | T-189 | PB-10, PB-17 y PB-21 | PB-10: que F10 cambie solo en P-02 (el CT-04 guarda la lista global de horizontes en P-03 aunque rechace ALT×H1; INC-T116-01). PB-17: CPI y EAC en la AUT- (INC-T116-02) y una ampliación autorizada dentro de un ciclo completo. PB-21: el tipo de dato protegido (clave API, IBAN) en la incidencia (INC-T116-03), sin escribir nunca el valor | CT-04, la autorización de ampliación y R8. T-177 rehízo R8 y las credenciales: léelo antes |
| C-45 | T-191 | PB-52 | El modo degradado de HT-09 (INC-T159-01): con HT-09 caído hoy el ciclo acaba en excepción; tiene que terminar con CT-14 al Orquestador, G3 manual con su etiqueta y el RUN- y la incidencia en el historial. El de HT-01 ya se prueba | HT-09, el Orquestador y cómo se declara una entrega PARCIAL |
| C-46 | T-192 | PB-34 y PB-35 | PB-34: registrar en F6 la corrección y el recálculo tras detectar la fuga, como entrada nueva. PB-35: cerrar el AJU- EN_SOMBRA como CONFIRMADO o REVERTIDO con la decisión documentada con DM-HLN (INC-T159-01) | El Evaluador. T-176 hizo la recalibración (AJU- y P3-EVAL-) y T-173 la DM-HLN: construye encima |
| C-47 | T-193 | PB-18 | En HT-08: el disparo por tiempo de ingesta (> 2 × objetivo) con su objetivo de configuración, cero duplicados en F2, la vuelta al objetivo y la orden ORD- de cierre tras dos lecturas con cola 0 y ρ < 0,30 (INC-T159-01). Los números, del Anexo A o la configuración; si no están, incidencia `[PROPUESTO]` | El monitor HT-08 y `carga.py`. T-178 hizo el caso de instancia única |

Los números T-188, T-189, T-191, T-192 y T-193 están reservados para ti. T-190 ya está usado. Si necesitas otro ticket, usa el número libre más bajo a partir de T-194, mirándolo antes en `origin/develop`.

## El ciclo completo de cada ticket

### 0. Al empezar

1. `git pull origin develop` y `python3 .docs/scripts/cola_astra.py`.
2. Reclama la tarea (`EN CURSO AAAA-MM-DD` en la cola) con un commit de solo ese fichero, y súbelo.
3. Lee:
   - `AGENTS.md`, `CLAUDE.md`, `.docs/README.md` y `.docs/memoria/LEEME.md`;
   - el README índice y la descripción para LLM del Bloque A;
   - del Documento 0 V5.3 (`bloque_a/01_Gobernanza/`), solo las secciones de tu caso.
4. Haz un kit de contexto por ticket: el Documento 0, el caso del plan, los tickets anteriores que tocaron lo mismo y los 2 o 3 ficheros de código afectados. Los almacenes F7, F8 y F9 se leen por identificador, nunca enteros.

### 1. Planificar (`ri-planificar`)

- Abre `.docs/tickets/T-NN/` con:
  - `README.md` (Estado, objetivo, alcance, diseño, criterios de aceptación numerados y registro);
  - `analisis-tecnico.md`, `pruebas.md` y `handoff.md`.
  - Modelos: `.docs/tickets/T-176/` o `.docs/tickets/T-178/`.
- Los criterios de aceptación salen del criterio del plan de pruebas.
- Lo que el spec no fije va a `docs/incidencias.md` como `INC-T-NN-01 [PROPUESTO]`, con la decisión y su motivo.

### 2. Implementar (`ri-implementar`)

- **Números y formatos.** Ningún número a mano: sale del Anexo A, de `config/por_defecto.yaml` o de su ficha. Esquemas y corpus congelados: no se tocan.
- **Primero el mock.** Todo se prueba antes con el cliente simulado (`--cliente mock`).
- **Fallar cerrado.**
  - Las escrituras que van juntas, bajo `almacen._transaccion()`, que excluye también entre procesos.
  - Las listas de estados, cerradas: lo que no está en la lista de cerrados sigue abierto.
  - Un fallo a mitad no deja F5, F6, F10 ni HA a medias.
- **R8.** Ningún secreto ni dato personal en almacenes, caché, mensajería ni entregables. En las pruebas, los secretos ficticios van partidos en dos cadenas.
- **G3-MET-13.** El texto que escribe el ejecutor no usa la raíz «valid-» junto a un método.

### 3. Probar (`ri-probar`)

- **Pruebas del criterio completo**: nominales, límites, fallo cerrado, concurrencia si hay escrituras y regresión. Comprueba que fallan sin tu cambio.
- **Mutantes** en `.docs/tickets/T-NN/mutantes.py`: todos muertos o explicados como equivalentes.
- **Mapa y evidencias**: actualiza `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json` y regenera las evidencias con `.docs/scripts/evidencias_plan_a.py --ejecutar`.
- **Ciclos y backtest**: un ciclo mock y el backtest del README dan lo mismo que en `develop`, salvo lo declarado.
- **Suite completa de A** y `./tools/check_all.sh`, los dos en verde (12/12).
- **Cuotas** (`tools/cuotas.txt`): ruff y mypy de A no pueden subir. Si bajan, se baja también la cuota.

### 4. Pedir la QA

1. Pon el Estado del README en `EN QA (r01)`.
2. Haz commit de tu trabajo con `.docs/scripts/commit_limpio.sh "mensaje" ficheros…`. Ese script pasa el gate en una copia limpia y sube a `develop`; este encargo lleva la autorización del operador para subir estos diez tickets.
3. Avisa al operador de que el ticket está listo para QA.

La QA la hace la sesión de Claude, con un revisor que no implementó.

### 5. Las rondas hasta el APTO

- **NO APTO:** haces la ronda r02, r03… en el mismo ticket.
  - Corrige **todos** los hallazgos con la corrección exacta del `qa.md`; si te apartas, explícalo en el `analisis-tecnico.md`.
  - Cada hallazgo lleva su prueba de regresión.
  - Trae antes al ticket el `qa.md` y los scripts `revisores/` de la QA.
  - Vuelve a pasar los scripts del revisor.
  - Pon el Estado en `EN QA (rNN: QA rMM NO APTO)` y vuelve al paso 4.
- **APTO con hallazgos bajos (o medios):** no se cierra. Haces una **ronda de cierre** en el mismo ticket con esas correcciones, cada una con su prueba. Estado: `EN QA (ronda de cierre de la QA rNN)`. El mismo revisor las comprueba.
- **APTO sin ningún hallazgo abierto:** el revisor da el veredicto final y pasas al paso 6.

### 6. Cerrar e integrar

1. README: `CERRADO (fecha, QA rNN APTO…)`.
2. Fila de la deuda (`sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`): CERRADO.
3. Entrada en `.docs/diario/2026-11.md`, firmada `astra`.
4. La tarea, `HECHA` en la cola.
5. Rebasa sobre `origin/develop`. En conflictos de documentación (deuda, diario, incidencias, evidencias), conserva los dos lados. Las evidencias se regeneran, no se fusionan a mano.
6. Haz el commit con `commit_limpio.sh`, con todos los ficheros del ticket. Comprueba después que `git status` está limpio y que `develop` coincide con `origin/develop`.

## Si algo se tuerce

- **Una decisión del operador:** si la tarea la necesita, márcala `BLOQUEADA` en la cola con la pregunta, y sigue con la siguiente.
- **Gate en rojo en `commit_limpio.sh`:** lee el log del gate que indica el propio script, corrige y vuelve a lanzar. No subas nada con el gate en rojo.
- **Push rechazado:** rebasa sobre `origin/develop` y vuelve a subir.
- **Sesión cortada:** sube el trabajo como borrador, con «BORRADOR, sigue en la próxima sesión» en la primera línea del README del ticket.
