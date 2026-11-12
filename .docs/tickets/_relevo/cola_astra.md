# Cola de trabajo de Astra

> **Instrucción expresa del operador, 12-11-2026: TODO EN LOCAL hasta que autorice subirlo.** Las reglas de push de este documento quedan suspendidas. Reclamar, revisar, registrar y hacer commits solo en local; no escribir en GitHub. Ver `.docs/memoria/astra/2026-11-12_solo-local-hasta-autorizacion.md`.

Fuente única del **orden y del estado** de las tareas de Astra desde el 12-11-2026. El detalle de cada tarea está en su encargo o en su ticket; las reglas, en `.docs/tickets/_relevo/2026-11-10_pendientes_para_astra.md` (§0 bis a §3). Si este fichero y el relevo no coinciden en el orden, manda este.

`python3 .docs/scripts/cola_astra.py` dice cuál es la siguiente tarea y comprueba que lo marcado como hecho está de verdad en el repositorio.

**Quién decide las tareas (operador, 12-11-2026):** «A partir de ahora yo te diré qué tareas quiero que realice Astra». Solo el operador añade tareas a esta cola o las retira; Claude no añade ninguna sin que él lo pida. Ese día retiró todas las QA y las implementaciones de tickets (C-24 a C-34) y las dos que Claude había añadido (C-35 y C-36): quedan como `RETIRADA`, sin borrarse, porque de `.docs/` no se borra nada.

## Protocolo, para que no se pierda nada

1. **Al abrir una sesión:** `git pull origin develop` y `python3 .docs/scripts/cola_astra.py`. Si hay una tarea `EN CURSO`, se sigue esa; si no, la primera `PENDIENTE`.
2. **Reclamar antes de empezar.** Cambia su estado a `EN CURSO AAAA-MM-DD` y haz commit y push **solo de este fichero**. Así otra sesión no empieza la misma tarea.
3. **Una tarea, un commit.** Al terminar, en el mismo commit van el entregable, la entrada del diario y el estado `HECHA` en esta tabla. Se sube con `.docs/scripts/commit.sh`, que pasa el gate.
4. **No dejes trabajo sin subir.** Si la sesión se va a cortar (contexto, tiempo), sube lo que tengas como borrador: el entregable a medias, con «BORRADOR, sigue en la próxima sesión» en la primera línea, y en la columna Nota de esta tabla, por dónde ibas. El estado sigue `EN CURSO`.
5. **Si una tarea se bloquea** (necesita una decisión del operador, un contrato con B, un bloque congelado): estado `BLOQUEADA`, el motivo en la Nota y la pregunta en tu entregable. Sigue con la siguiente.
6. **No cambies el orden ni borres filas.** Si una revisión cambia tu opinión sobre una anterior, añade una nota con fecha al final de la anterior.

Las rutas que aún no existen van entre «…» (el gate `refs-vivas` no las exige); al crearlas, pueden quedarse así. Estados: `PENDIENTE`, `EN CURSO AAAA-MM-DD`, `HECHA`, `BLOQUEADA` y `RETIRADA` (el operador la quitó; no se hace). La columna Commit es opcional: el script la busca por el entregable.

## Cola

| # | Tarea | Tipo | Encargo o ticket | Entregable | Estado | Commit | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-01 | Rediseño de A | REVISION | `.docs/diseno/bloque_a/encargo_revision_astra.md` | «.docs/diseno/bloque_a/revision_astra.md» | HECHA | | |
| C-02 | B: evaluación T-68 y rediseño, juntos | REVISION | `.docs/tickets/T-68/encargo_revision_astra.md` y `.docs/diseno/bloque_b/encargo_revision_astra.md` | «.docs/tickets/T-68/revision_astra.md» | HECHA | | Sin tocar `bloque_b/` |
| C-03 | C | REVISION | `.docs/diseno/bloque_c/encargo_revision_astra.md` | «.docs/diseno/bloque_c/revision_astra.md» | HECHA | | |
| C-04 | D | REVISION | `.docs/diseno/bloque_d/encargo_revision_astra.md` | «.docs/diseno/bloque_d/revision_astra.md» | HECHA | | Solo local; subida pendiente de autorización expresa |
| C-05 | E | REVISION | `.docs/diseno/bloque_e/encargo_revision_astra.md` | «.docs/diseno/bloque_e/revision_astra.md» | HECHA | | Solo local; subida pendiente de autorización expresa |
| C-06 | F | REVISION | `.docs/diseno/bloque_f/encargo_revision_astra.md` | «.docs/diseno/bloque_f/revision_astra.md» | PENDIENTE | | Solo diseño; T-74 sigue en espera |
| C-07 | G | REVISION | `.docs/diseno/bloque_g/encargo_revision_astra.md` | «.docs/diseno/bloque_g/revision_astra.md» | PENDIENTE | | |
| C-08 | H | REVISION | `.docs/diseno/bloque_h/encargo_revision_astra.md` | «.docs/diseno/bloque_h/revision_astra.md» | PENDIENTE | | |
| C-09 | I | REVISION | `.docs/diseno/bloque_i/encargo_revision_astra.md` | «.docs/diseno/bloque_i/revision_astra.md» | PENDIENTE | | |
| C-10 | J | REVISION | `.docs/diseno/bloque_j/encargo_revision_astra.md` | «.docs/diseno/bloque_j/revision_astra.md» | PENDIENTE | | |
| C-11 | K | REVISION | `.docs/diseno/bloque_k/encargo_revision_astra.md` | «.docs/diseno/bloque_k/revision_astra.md» | PENDIENTE | | |
| C-12 | M | REVISION | `.docs/diseno/bloque_m/encargo_revision_astra.md` | «.docs/diseno/bloque_m/revision_astra.md» | PENDIENTE | | |
| C-13 | N | REVISION | `.docs/diseno/bloque_n/encargo_revision_astra.md` | «.docs/diseno/bloque_n/revision_astra.md» | PENDIENTE | | Puede usar el prototipo `dashboard/consola_n/` |
| C-14 | Broker Personal | REVISION | `.docs/diseno/broker_personal/encargo_revision_astra.md` | «.docs/diseno/broker_personal/revision_astra.md» | PENDIENTE | | |
| C-15 | SC-9, fiscalidad | REVISION | `.docs/diseno/sc9_fiscalidad/encargo_revision_astra.md` | «.docs/diseno/sc9_fiscalidad/revision_astra.md» | PENDIENTE | | |
| C-16 | SC-3, Motor de cálculo | REVISION | `.docs/diseno/sc3_motor/encargo_revision_astra.md` | «.docs/diseno/sc3_motor/revision_astra.md» | PENDIENTE | | |
| C-17 | SC-10, intermediario | REVISION | `.docs/diseno/sc10_intermediario/encargo_revision_astra.md` | «.docs/diseno/sc10_intermediario/revision_astra.md» | PENDIENTE | | |
| C-18 | SC-7, seguridad | REVISION | `.docs/diseno/sc7_seguridad/encargo_revision_astra.md` | «.docs/diseno/sc7_seguridad/revision_astra.md» | PENDIENTE | | |
| C-19 | Entrada del dinero existente | REVISION | `.docs/diseno/entrada_patrimonio/encargo_revision_astra.md` | «.docs/diseno/entrada_patrimonio/revision_astra.md» | PENDIENTE | | |
| C-35 | Borradores de contratos CT-G-08 0.4.0 y CT-G-24 0.1.0 | REVISION | `.docs/diseno/contratos/README.md` | «.docs/diseno/contratos/revision_astra.md» | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Revisa sobre todo los cuatro puntos `[PROPUESTO]` del README |
| C-20 | Enmienda 4 | REVISION | `.docs/diseno/enmienda_4/encargo_revision_astra.md` | «.docs/diseno/enmienda_4/revision_astra.md» | PENDIENTE | | |
| C-21 | Pasada de coherencia | REVISION | `.docs/diseno/coherencia/encargo_revision_astra.md` | «.docs/diseno/coherencia/revision_astra.md» | PENDIENTE | | La última de diseño |
| C-22 | Enmienda 5, parte 1 | REVISION | `.docs/diseno/enmienda_5/encargo_revision_astra.md` | «.docs/diseno/enmienda_5/revision_astra.md» | PENDIENTE | | |
| C-23 | Enmienda 5, parte 2 | REVISION | `.docs/diseno/enmienda_5/encargo_revision_astra_parte2.md` | «.docs/diseno/enmienda_5/revision_astra_parte2.md» | PENDIENTE | | |
| C-24 | QA de T-94, banco de medida | QA | `.docs/tickets/T-94/` | `.docs/tickets/T-94/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. |
| C-25 | QA de T-95, prototipo de N | QA | `.docs/tickets/T-95/` | `.docs/tickets/T-95/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. `npm install`, `npm test`, `npm run build && npm run e2e` |
| C-26 | QA de T-96, entorno reproducible | QA | `.docs/tickets/T-96/` | `.docs/tickets/T-96/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. |
| C-27 | QA de T-97, marco V0.74 | QA | `.docs/tickets/T-97/` | `.docs/tickets/T-97/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. |
| C-28 | QA r02 de T-83, valores documentados | QA | `.docs/tickets/T-83/` | `.docs/tickets/T-83/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Sobre la V0.74 (T-97 toca `parametros_doc.py`) |
| C-29 | QA r02 de T-84, correcciones c1 | QA | `.docs/tickets/T-84/` | `.docs/tickets/T-84/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. |
| C-30 | T-75, ronda r03 | IMPLEMENTAR | `.docs/tickets/T-75/` | `.docs/tickets/T-75/README.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Sobre la V0.74; la QA la hace otro agente |
| C-31 | T-76, ronda r03 | IMPLEMENTAR | `.docs/tickets/T-76/` | `.docs/tickets/T-76/README.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Después de T-75, sin mezclar |
| C-32 | QA de T-93, Bloque A (H-32 a H-39) | QA | `.docs/tickets/T-93/` | `.docs/tickets/T-93/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Implementó Claude el 12-11-2026 con autorización del operador; los scripts `r04_0x` de T-92 deben dar 0 fallos |
| C-36 | QA de T-99, registro de experimentos | QA | `.docs/tickets/T-99/` | `.docs/tickets/T-99/qa.md` | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Fuera de los bloques; implementó Claude |
| C-33 | T-91, Bloque A | IMPLEMENTAR | «.docs/tickets/T-91/» | «.docs/tickets/T-91/README.md» | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Ídem |
| C-34 | T-88, Bloque A | IMPLEMENTAR | «.docs/tickets/T-88/» | «.docs/tickets/T-88/README.md» | RETIRADA | | Retirada por el operador el 12-11-2026: ya no la hace Astra. Ídem |

Una tarea nueva solo entra si el operador lo pide: Claude la añade con el siguiente número libre, donde él diga, y lo anota en el diario.
