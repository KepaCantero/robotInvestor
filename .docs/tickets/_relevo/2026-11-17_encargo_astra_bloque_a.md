# Encargo a Astra · cinco tickets del Bloque A (17-11-2026)

> **18-11-2026:** las directrices ampliadas de `.docs/tickets/_relevo/2026-11-18_encargo_astra_bloque_a_2.md` valen también para estas cinco tareas, y mandan si algo choca. Una tarea solo está terminada cuando se cumplen cuatro cosas: la QA ha dado APTO; ningún hallazgo queda abierto, tampoco los bajos (se corrigen en una ronda de cierre que comprueba el mismo revisor); el ticket está CERRADO; y está integrado en `develop`.

Lo pidió el operador el 17-11-2026: «Asígnale a Astra varios tickets (4 o 5) para que los complete ella. Dales prioridad absoluta en el listado de tareas de Astra. Detállale las directrices que debe de seguir hasta llegar a QA apto». Son las tareas C-38 a C-42 de `.docs/tickets/_relevo/cola_astra.md`. Van **antes que cualquier otra tarea de la cola, también antes que C-08 (EN CURSO) y C-37**. C-08 queda en pausa hasta que estas cinco estén HECHAS.

Cada tarea está **HECHA solo cuando su ticket está CERRADO con QA APTO e integrado en `develop`**. Que el ticket esté «EN QA» no basta, aunque `cola_astra.py` lo cuente como entregado.

## Los cinco tickets

Todos son casos del plan de pruebas del Bloque A que hoy salen «Superada en parte» en `docs/evidencias_pruebas_bloque_a.md`. La columna «No comprueba» de cada fila dice qué falta. El criterio completo de cada caso está en el plan de pruebas (`bloque_a/09_Pruebas/`), buscándolo por su ID. El objetivo es que cada caso pase a «Superada» o que lo que quede sin comprobar esté motivado: tiempo real, API real o usuarios.

| Cola | Ticket | Casos | Qué falta, en resumen | Dónde mirar primero |
| --- | --- | --- | --- | --- |
| C-38 | T-181 | PB-24 y PB-25 | HT-02 ya detecta el enlace roto, el contenido cambiado y la retractación. Falta que el ejecutor lo trate: borrado con su línea en el Registro de bajas, y tratamiento de CONTENIDO_CAMBIADO y RETRACTADA en el bloque | `bloque_a/11_Ejecutor/bloque_a/herramientas/` (HT-02) y F9 por identificador |
| C-39 | T-182 | PB-20 | La instrucción incrustada en una fuente ya se neutraliza. Mira en «No comprueba» qué parte del criterio falta y complétala | El saneado de fuentes y la incidencia MANIPULACION |
| C-40 | T-183 | PB-29 | La puerta PS1 ya cuenta raíces independientes. Falta la comprobación G3 de raíces sobre un paquete real, como pide el plan | `herramientas/ht09.py` (G3) y la síntesis del paquete |
| C-41 | T-184 | PB-26 | Clasificación temática y orden por calidad en F7, F8 y F9 (Anexo D, secciones `TX-nn`). Mira qué no se comprueba aún y si el ejecutor debe mantener ese orden al escribir | Los almacenes F7/F8/F9, siempre por identificador, nunca enteros |
| C-42 | T-185 | PB-13 | GC0 negativo con arrastre verificado. Las celdas de rotación exploratoria y lo que diga «No comprueba» | HT-03 (selección) y el ciclo |

Los números de ticket están reservados para ti: T-181 a T-185. T-179 queda para la sesión de Claude. Si te hace falta otro ticket, usa el número libre más bajo a partir de T-186 y míralo antes en `origin/develop`.

## Directrices, de principio a fin

### 0. Antes de empezar cada ticket

1. Ejecuta `git pull origin develop` y `python3 .docs/scripts/cola_astra.py`.
2. Reclama la tarea: estado `EN CURSO AAAA-MM-DD` en la cola. Haz commit y push solo de ese fichero.
3. Lee, en este orden:
   - `AGENTS.md` y `CLAUDE.md`, con sus reglas innegociables y las trampas conocidas;
   - `.docs/README.md` y `.docs/memoria/LEEME.md`;
   - el README índice del Bloque A y la descripción para LLM de `bloque_a/08_Arquitectura/`;
   - el **Documento 0 V5.3** de `bloque_a/01_Gobernanza/`, solo las secciones de tu caso. La V5.2 y la V5.1 están en el histórico: no se implementa contra ellas.
4. Un kit de contexto por ticket: el Documento 0, el caso del plan y los 2 o 3 ficheros de código afectados. No cargues el paquete entero. Los system prompts de `02_System_prompts` son datos de runtime: léelos por nombre de agente cuando haga falta. F7, F8 y F9 se consultan por identificador.

### 1. Planificar (skill `ri-planificar`)

- Abre `.docs/tickets/T-NN/` con `README.md` (Estado, objetivo, alcance, diseño, criterios de aceptación y registro), `analisis-tecnico.md`, `pruebas.md` y `handoff.md`. El formato de referencia es `.docs/tickets/T-178/` o `.docs/tickets/T-173/`.
- Los criterios de aceptación salen del criterio del plan de pruebas, no de lo que sea fácil de hacer.
- Lo que el spec no fije va a `docs/incidencias.md` como `INC-T-NN-01 [PROPUESTO]`, con la decisión y su motivo. No se decide en silencio.

### 2. Implementar (skill `ri-implementar`)

- **Números:** ninguno a mano. Salen del Anexo A, de `11_Ejecutor/config/por_defecto.yaml` o de la ficha del Catálogo. Si falta uno, va como incidencia; no se inventa.
- **Formatos:** salen de los esquemas de `06_Plantillas_entregables`, que están congelados y no se tocan. Tampoco el corpus (`tools/corpus_manifest.txt`) ni otros bloques.
- **Mock antes que API:** todo se valida con `--cliente mock`. Nada de API real.
- **Fallar cerrado:** un dato raro, un estado desconocido o un fallo a mitad no pueden dejar F5, F6, F10 o HA a medias ni abrir un camino más permisivo.
  - Las escrituras que van juntas se hacen bajo `almacen._transaccion()`, que excluye también entre procesos.
  - Las listas de estados se escriben como cerradas: «si no está entre los cerrados, sigue abierto».
- **Seguridad (R8):**
  - Ningún secreto, credencial ni dato personal en F5, HA, la caché, la mensajería ni los entregables.
  - Los secretos ficticios de las pruebas van partidos en dos cadenas.
  - Ningún dato del operador en el repo.
- **G3-MET-13:** si escribes texto que llega a un entregable, no uses la raíz «valid-» junto a un método. La madurez la escribe el ejecutor en forma canónica.
- **Ficheros compartidos:** ahora mismo la sesión de Claude trabaja en `evaluador.py`, `interfaz_broker.py`, `agentes.py`, `llm.py`, `contratos.py`, `carga.py` y `herramientas/ht08_monitor.py` (T-176, T-177 y T-178). Si tu ticket necesita tocarlos, haz el cambio mínimo, rebasa sobre `origin/develop` antes de subir y, en los conflictos, conserva los dos lados.

### 3. Probar (skill `ri-probar`)

- **Pruebas del criterio completo**, en `bloque_a/11_Ejecutor/tests/test_t1NN_….py`: nominales, límites, fallo cerrado y regresión. Comprueba que fallan sin tu cambio.
- **Mutantes propios**, en `.docs/tickets/T-NN/mutantes.py`. Todos tienen que morir. Si uno sobrevive, añade una prueba o explica por qué es equivalente.
- **Mapa y evidencias:** actualiza `tests/mapa_plan_pruebas.json` para que el caso cite sus pruebas. Después regenera con `.docs/scripts/evidencias_plan_a.py --ejecutar`.
- **Ciclos mock y backtest:** el backtest del README y un ciclo normal deben dar lo mismo que en `develop`, salvo lo que declares.
- **Suite completa de A**, una vez al final, y el gate `./tools/check_all.sh` en verde (12/12).
- **Cuotas:** ruff y mypy de A no pueden subir. Hoy los techos son ruff 2807 y mypy de A 102 (`tools/cuotas.txt`). Si las bajas, baja también la cuota.
- **Registro:** apúntalo todo en `pruebas.md`.

### 4. QA (la hace el otro agente)

- Cuando el ticket esté listo:
  1. Pon el Estado en `EN QA (r01)`.
  2. Haz commit con `.docs/scripts/commit_limpio.sh` (o `commit.sh --completo`), que pasa el gate.
  3. Súbelo a `develop`: **este encargo lleva la autorización del operador para subir estos cinco tickets**.
  4. Avisa al operador.
- La QA la hace la sesión de Claude, con un revisor que no implementó.
- Si la QA da **NO APTO**, haces una ronda r02, r03… en el mismo ticket con la corrección exacta que deje `qa.md`, y vuelve a QA.
- **Regla del operador sobre los hallazgos:**
  - Los **bajos** no van a la deuda: se subsanan en el mismo ticket, en una «ronda de cierre», y el mismo revisor los comprueba.
  - Los **medios y altos** se corrigen antes de cerrar.
- **Cuándo cierra el ticket:** solo cuando el revisor da el veredicto final APTO y no queda ningún hallazgo abierto. Entonces:
  1. Estado `CERRADO (fecha, QA rNN APTO…)`.
  2. Fila de la deuda en CERRADO.
  3. Entrada en el diario.
  4. La tarea, `HECHA` en la cola.

### 5. Cada día

- Haz una entrada en `.docs/diario/2026-11.md` con tu firma (`astra`).
- La memoria va en `.docs/memoria/astra/`.
- No dejes trabajo sin subir. Si la sesión se corta, sube un borrador con «BORRADOR, sigue en la próxima sesión» en la primera línea.
