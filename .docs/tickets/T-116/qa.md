# T-116 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude) · **Ronda:** r01 · 2026-11-13
- Orden de lectura: `README.md` del ticket → el script, el mapa, las pruebas y el plan → mis ataques → al final `analisis-tecnico.md` y `pruebas.md`.
- Lo que digo «ejecutado» lo he ejecutado yo en mi copia; lo que digo «leído» es deducción de lectura.

## Ronda r01

### Reproducción desde limpio

Copia propia (`git worktree` en `2ff0630`, HEAD separado; lo de los tres tickets es `git diff ab95d41 HEAD`). Python del `.venv` del repositorio (enlace `.venv` en la raíz de la copia, borrado al acabar). Máquina compartida con otros cuatro trabajos: los tiempos son orientativos.

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite del Bloque A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **3811 passed in 684 s**; el árbol queda limpio |
| Comprobar el mapa | `.venv/bin/python .docs/scripts/evidencias_plan_a.py` | «67 pruebas del plan, 94 pruebas automáticas citadas y todas existen · AUTOMATICA 27, DOCUMENTAL 1, PARCIAL 28, PENDIENTE_API 7, REQUIERE_USUARIOS 1, SIN_PRUEBA 3», código 0 (3 s) |
| Una fila | `… evidencias_plan_a.py --pb PB-22` (y PB-04, PB-99) | PB-22: 3 SUPERADA, «Superada», código 0 (18 s); PB-04: «Pendiente API», código 0; PB-99: «no está en el plan», código 1 |
| Ejecutar todo | `… evidencias_plan_a.py --ejecutar`, en una copia desechable para no reescribir el documento | «escrito docs/evidencias_pruebas_bloque_a.md · 94 de 94 pruebas citadas superadas», código 0 (3 min 13 s). **El documento regenerado es idéntico al del repositorio** salvo el identificador del commit |
| Dos órdenes copiadas del documento | las dos de PB-12 y las dos de PB-33, pegadas tal cual desde la raíz | `1 passed`, `2 passed`, `4 passed`, `1 passed` |
| Corpus, refs, secretos, NFC | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | los cuatro en verde (695 archivos del corpus) |
| ruff y mypy (como el gate) | — | 2902 (cuota 2902) y 109 (cuota 109) |

No ejecuté `tools/check_all.sh` completo (indicación del encargo). CA-8 queda comprobado por partes; el implementador tampoco lo ha pasado todavía (`pruebas.md`). **Es condición de cierre.**

### Mis scripts (`revisores/`)

| Script | Qué hace | Resultado |
| --- | --- | --- |
| `r01_01_filas_automaticas_a_mano.py` | Ejecuta PB-21, PB-23, PB-45, PB-49 y PB-06 como dice el plan, no como las pruebas citadas | El ejecutor cumple PB-21, PB-23 y PB-49; ver H-01 y «Fuera del ticket» |
| `r01_02_ataques_script.py` | 27 ataques al script en una copia desechable: mapa roto, prueba inexistente, que falla, saltada, xfail, plan con una PB de más | 20 fallan cerrado; ver H-02 y H-03 |
| `r01_03_mutantes_huecos.py` | 26 mutantes en el código que cubren las ocho pruebas de `test_fase4_huecos.py`, y uno (A01) contra la prueba que el mapa cita para PB-23 | 23 de 26 muertos; A01 vivo (H-01) |

```bash
cd bloque_a/11_Ejecutor && python ../../.docs/tickets/T-116/revisores/r01_01_filas_automaticas_a_mano.py
python .docs/tickets/T-116/revisores/r01_02_ataques_script.py <copia desechable>
python .docs/tickets/T-116/revisores/r01_03_mutantes_huecos.py <copia desechable>
```

### Criterios de aceptación

| Criterio | Cumple | Evidencia (ejecutada salvo que diga otra cosa) |
| --- | --- | --- |
| CA-1 · el mapa tiene las 67 pruebas del plan y cada fila dice su cobertura, sus pruebas, qué comprueban y qué no | sí en la forma; **no en el fondo en cuatro filas** (H-01) | 67 filas, PB-01 a PB-67, con los cuatro campos. Pero en PB-21, PB-23, PB-37 y PB-49 «comprueba» dice más de lo que afirman las pruebas citadas, y «no_comprueba» está vacío o incompleto |
| CA-2 · toda prueba citada existe | sí | Script sin opciones: 94 citadas, todas existen, código 0. Una citada inexistente, con parámetro o un fichero sin prueba: código 1 (`r01_02`) |
| CA-3 · `--ejecutar` genera el documento con las 67 filas y termina con 0 | sí | 94 de 94 superadas, código 0; documento idéntico al del repositorio |
| CA-4 · cada fila «Superada» o «Superada en parte» tiene una orden que, copiada, pasa | sí (muestra) | Cuatro órdenes de dos filas, copiadas del documento: pasan. `--pb PB-22`: pasa |
| CA-5 · ninguna fila que dependa del modelo real, de usuarios o de una revisión documental figura como superada | sí | Las 7 `PENDIENTE_API`, la de usuarios y la documental no llevan pruebas y salen con su rótulo; las AUTOMATICA que tienen una parte del modelo real (PB-07, PB-45, PB-58, PB-61) la declaran en «No comprueba» |
| CA-6 · citar una prueba que no existe, quitar un PB o dejar una parcial sin su hueco hace fallar el script y `test_fase4_mapa.py` | sí | `r01_02`: los tres casos dan código 1 con su mensaje; `test_ca6_un_mapa_estropeado_se_detecta` (11 casos) pasa en la suite |
| CA-7 · los huecos están en el ticket y en la deuda técnica | sí, con la deuda desfasada (H-04) | Sección «Huecos» del README y fila T-116 de la deuda (PB-26, PB-48, PB-46, INC-T116-01 y 02). La fila sigue diciendo «PLANIFICADO… Pendiente: ejecutar y generar el documento» |
| CA-8 · gate 12/12; cuotas sin subir; pruebas recogidas sin bajar | sí por partes; gate entero pendiente | 3811 passed (3744 con T-114 + 16 + 8 + 43 de T-117); ruff 2902, mypy 109; gates ligeros en verde |

### Muestreo del mapa contra el plan (regla: «prohibido marcar por leído o parecido»)

Leí el criterio de aprobación del plan y las pruebas citadas de 28 filas: las 7 que pedía el encargo (PB-10, 16, 17, 22, 33, 45, 59), otras 14 AUTOMATICA (PB-01, 06, 07, 12, 14, 21, 23, 37, 38, 49, 58, 60, 61, 66) y 7 que no son automáticas (PB-02, 13, 52, 67 y las tres sin prueba). En total, 19 de las 27 AUTOMATICA. Cinco filas las ejecuté además a mano como dice el plan. No leí PB-32, PB-53 a PB-56 ni PB-63 a PB-65.

| Fila | Cobertura | Juicio | Por qué |
| --- | --- | --- | --- |
| PB-10 | PARCIAL | bien puesta | La prueba nueva afirma el rechazo de la celda, el de `umbral_E`, qué cambia en F10 (P-02 y P-03) y que HA no tiene incidencia de escritura. El hueco (P-03) está declarado e INC-T116-01 existe. Mutantes H01 a H03 mueren |
| PB-16 | AUTOMATICA | bien puesta | Mismas comprobaciones de G3 (F6 y F7) con y sin presupuesto, y limitación en los dos informes. El ejecutor no tiene resultado `NO_APLICA`: la afirmación fuerte es la igualdad de las listas (mutante H04 muere) |
| PB-17 | PARCIAL | bien puesta | AUTORIZADA y dos DENEGADA con su AUT- y motivo; consumo real en F5; CPI y EAC declarados como hueco (INC-T116-02). Mutantes H05 a H09 mueren |
| PB-22 | AUTOMATICA | bien puesta | Los tres mensajes del plan, tres INC- y solo cambian HA, contadores y sellos. Mutantes H10 a H13 mueren |
| PB-33 | AUTOMATICA | aceptable, con nota | Estado, motivo y fecha de efecto afirmados (H14 a H16 mueren). «G3-CON-10 bloquea probabilidades posteriores» se apoya en HT-09 con un certificado no vigente hecho a mano; el «RUN- posterior» del plan no se ejecuta de extremo a extremo |
| PB-45 | AUTOMATICA | bien puesta | Diez como máximo, la estadística primero, ninguna de otro tipo (H19 a H21 mueren). Comprobé que la aplicación no se ve con el cliente simulado (probabilidades iguales con y sin lección): es del modelo real, como dice la fila |
| PB-59 | AUTOMATICA | bien puesta | Incidencia en HA sin el valor, valor ausente de todos los ficheros del estado y de la traza (H23 a H26 mueren) |
| PB-01, 07, 12, 14, 38, 58, 60, 61, 66 | AUTOMATICA | bien puestas | Las pruebas citadas afirman cada cláusula determinista; lo que es de tiempo real o del modelo está en «No comprueba» |
| PB-06 | AUTOMATICA | aceptable, con nota | «≥ 1 referencia por afirmación» se afirma como «hay referencias y tienen prefijo válido»; la fila dice «referencias existentes» y la prueba no comprueba que existan (yo sí: las 6 existen) |
| **PB-21** | AUTOMATICA | **mal puesta** | El plan: CT-04 con una clave API y un IBAN en el comentario; criterio: «búsqueda del valor en todos los archivos: cero coincidencias». Las pruebas citadas envían un CT-03 con una clave, sin IBAN, y buscan solo en el fichero de HA; `test_credenciales_boveda` es el caso de CT-25. Ejecutado a mano, el ejecutor cumple el caso del plan |
| **PB-23** | AUTOMATICA | **mal puesta** | El plan: tres intentos (Analizador en F4, Prospectiva escribe una resolución, Evaluador modifica la afirmación) y «hash de F4 sin cambios». La prueba citada hace dos de los tres (el tercero es una escritura en F10) y no compara F4 antes y después: el mutante A01, que **guarda** en F4 la escritura rechazada del Analizador, deja la prueba en verde. Ejecutado a mano, el ejecutor cumple los tres |
| **PB-37** | AUTOMATICA | **mal puesta** | El plan: Prospectiva corrige un PRG congelado (PRG nuevo con `version_de`), se adelanta el reloj y «ambos RESUELTO». Ninguna prueba de la suite usa `version_de` (`grep -rn version_de tests/`: nada); las dos citadas comprueban que alterar el fichero rompe la cadena y que un arrastre no anula los PRG. No lo he ejecutado a mano |
| **PB-49** | AUTOMATICA | **mal puesta** | Criterio: «cero entradas modificadas **o borradas**» en ocho semanas simuladas. Las pruebas citadas afirman que una entrada modificada se detecta y que todo está íntegro tras dos ciclos; el borrado no se afirma. Ejecutado a mano, el ejecutor detecta el borrado de una entrada del medio y de la última |
| PB-02, 13, 52, 67 | PARCIAL | bien puestas | El hueco que declaran es el que hay |
| PB-26, 46, 48 | SIN_PRUEBA | bien puestas | — |

La propia regla del ticket manda a PARCIAL estos cuatro casos: es lo que hizo con PB-02 («el caso sembrado del plan no se ejecuta de extremo a extremo»).

### ¿Afirman las ocho pruebas nuevas lo que dicen?

Sí. 23 de 26 mutantes mueren. Los tres vivos no desmienten a las pruebas: H17 y H18 (revocar solo por BSS o solo por calibración) sobreviven porque la celda de la prueba incumple las dos condiciones a la vez y cada una tiene su prueba propia entre las citadas; H22 (lecciones caducadas) no es lo que la prueba dice afirmar.

### Ataques al script

| Ataque | Resultado |
| --- | --- |
| Mapa truncado, vacío o con una lista | código 1 (traza de Python, no un mensaje: feo pero cerrado) |
| Prueba citada inexistente, con parámetro, o un fichero entero | código 1, «la prueba citada no existe» |
| Falta un PB, sobra un PB, `pruebas` como texto, `comprueba` nulo, parcial sin hueco | código 1 |
| Plan con una PB-68 bien escrita; PB-22 renombrada | código 1 |
| Prueba citada que falla; con error en la fixture; fichero con error de sintaxis | `--pb`: «FALLA», código 1 |
| **Prueba citada saltada (`skip`) o `xfail` que falla** | `--pb`: «No ejecutada», **código 0** (H-02). `--ejecutar` sí da 1 en ese caso (leído: `fallan` incluye todo lo que no es SUPERADA) |
| **Prueba citada `xfail` que pasa (XPASS)** | «Superada», código 0 (H-02) |
| **Plan con «### PB-68 - …» (guion) o «### PB-100 · …»** | código 0: la PB nueva no se ve (H-03) |
| Plan con PB-22 sin criterio de aprobación | script: código 0; lo detecta `test_ca1…` en la suite, no el script (H-03) |
| Una PARCIAL pasa a AUTOMATICA; una PENDIENTE_API pasa a AUTOMATICA citando una prueba cualquiera | código 0. Es el límite del diseño: el script no puede saber si una fila dice la verdad; por eso importa H-01 |
| Prueba citada vaciada | «Superada», código 0 (mismo límite) |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | Leer en el plan el criterio de PB-21, PB-23, PB-37 y PB-49 y las pruebas que cita `tests/mapa_plan_pruebas.json`. Para PB-23: `python .docs/tickets/T-116/revisores/r01_03_mutantes_huecos.py <copia> --solo A01` → `VIVO`. Para PB-37: `grep -rn "version_de" bloque_a/11_Ejecutor/tests bloque_a/10_Herramientas/tests` → nada | Esperado (regla estricta del ticket y del prompt de la fase): AUTOMATICA solo si las pruebas comprueban todo el criterio; una cláusula que el ejecutor puede comprobar y nadie afirma va a PARCIAL. Obtenido: cuatro filas AUTOMATICA con una cláusula determinista sin afirmar, y `docs/evidencias_pruebas_bloque_a.md` las publica como «Superada» («comprueban todo el criterio»): PB-21 (ni CT-04, ni IBAN, ni búsqueda en todos los archivos), PB-23 (dos de los tres intentos; F4 no se compara), PB-37 (el caso del plan, `version_de` y «ambos RESUELTO», no se ejercita en ninguna prueba), PB-49 (el borrado no se afirma). Son 4 de las 19 AUTOMATICA que leí (hay 27) | O bien pasar las cuatro a PARCIAL con su hueco en «no_comprueba» y regenerar el documento (quedarían 23 y 32), o bien añadir las cuatro pruebas: las de PB-21, PB-23 y PB-49 están casi escritas en `r01_01_filas_automaticas_a_mano.py` y el ejecutor las pasa; la de PB-37 hay que escribirla. Conviene repasar con el mismo criterio las 8 AUTOMATICA que no leí (PB-32, PB-53 a PB-56 y PB-63 a PB-65) | abierto |
| H-02 | media | `python .docs/tickets/T-116/revisores/r01_02_ataques_script.py <copia>`: casos «SALTADA», «xfail que falla» y «xfail que pasa» | Esperado (README: «Una prueba que no se ejecuta deja la fila como "No ejecutada", nunca como superada» y el script falla cerrado): código distinto de 0 si una prueba citada no se ejecuta. Obtenido: `--pb` imprime «No ejecutada» y termina con **0** (solo mira `FALLA`); y un `xfail` que pasa cuenta como SUPERADA, así que una fila puede figurar «Superada» con una prueba marcada como fallo esperado | En `--pb`, devolver 1 si algún resultado no es SUPERADA (como hace `--ejecutar`); tratar XPASS y `xfail` como «NO EJECUTADA» o rechazar en `comprobar` las pruebas citadas con esas marcas; un caso en `test_fase4_mapa.py` | abierto |
| H-03 | baja | Mismo script: casos «PB-68 con guion», «PB-100», «PB-22 sin criterio» | Esperado: una prueba nueva del plan, o una sin criterio, hace fallar el script. Obtenido: `leer_plan` solo reconoce `### PB-NN · …` con dos cifras; una cabecera con otro separador o con tres cifras se ignora y el script dice «67 pruebas del plan». Un PB sin criterio lo ve la suite, no el script. El plan es corpus congelado por huella, lo que limita el riesgo | Contar aparte las cabeceras `### PB-` y exigir que todas casen con el patrón; exigir título y criterio en `comprobar` | abierto |
| H-04 | media | `sed -n 165p sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`; `cat .docs/tickets/T-116/analisis-tecnico.md`; `grep -n "T-116\|Fase 4" docs/AVANCE.md` | Documentación al día. Obtenido: (a) `analisis-tecnico.md` es la plantilla sin rellenar; (b) la fila T-116 de la deuda dice «PLANIFICADO… Pendiente: ejecutar y generar el documento», cuando el ticket está EN QA y el documento existe; (c) `docs/AVANCE.md` no tiene fila de la Fase 4 (sí la de la Fase 3) | Rellenar el análisis técnico (decisiones: regla estricta, herramientas fuera del gate, límites del script), poner la deuda en EN QA con las cifras finales y añadir la fila de la Fase 4 a `docs/AVANCE.md` | abierto |
| H-05 | baja | `git log -1 --format=%h -- docs/evidencias_pruebas_bloque_a.md` frente a la línea 3 del documento | El documento dice «sobre el commit `7c649df`» y entra en el commit `2ff0630`. Entre los dos no cambia código ni pruebas (`git diff --stat 7c649df 2ff0630`: solo tickets y el documento), así que el contenido vale; pero el documento se regenera por norma y no hay nada que avise si el mapa o la suite cambian sin regenerarlo | Una prueba en `test_fase4_mapa.py` que compare la tabla del documento con el mapa (filas, cobertura y textos), sin ejecutar nada | abierto |

### Invariantes (punto 4 de la skill)

- No cambia código de producción ni corpus: `git diff --stat ab95d41 HEAD -- bloque_a/11_Ejecutor/bloque_a` solo muestra `diseno_v6.py` (T-117); el plan y `10_Herramientas` no cambian; corpus íntegro (695). ✔
- Mock antes que API: todo con `MockClient`; las filas del modelo real no se marcan. ✔
- Ambigüedad documentada, no decidida en silencio: INC-T116-01 e INC-T116-02 `[PROPUESTO]`, en la deuda y en el registro de decisiones. ✔
- Nada cuenta sin pruebas: 24 pruebas nuevas; la suite sube. ✔
- Secretos: `tools/secrets_scan.py` en verde; las claves de las pruebas son ficticias. ✔
- Documentación al día: **no** (H-04).

### Fuera del ticket (para la deuda; no cuentan en el veredicto)

- **Un IBAN escrito con espacios no se detecta.** `python …/r01_01_filas_automaticas_a_mano.py`, apartado PB-21: un CT-04 cuyo comentario lleva solo «ES91 2100 0418 4502 0005 1332» se admite (APLICADA) y el IBAN queda en `F5_historial_analisis.jsonl`; sin espacios se rechaza. El caso del plan pasa porque la clave API del mismo comentario hace rechazar el mensaje entero. Es un defecto de R8 en `contratos.contiene_credenciales`, anterior a estos tickets, y es justo lo que una prueba fiel de PB-21 habría sacado a la luz. Tampoco se detecta un número de tarjeta con espacios.
- `Evaluador.lecciones_vigentes(…, max_n: int = 10)`: el 10 del Anexo A está escrito en el código y no en `por_defecto.yaml` (regla 2).

## Veredicto

**NO APTO** · Queda un hallazgo alto abierto (H-01): el mapa y el documento de evidencias dan por «Superada» cuatro filas (PB-21, PB-23, PB-37 y PB-49) cuyas pruebas citadas no afirman una cláusula determinista del criterio del plan, contra la regla estricta del propio ticket y del prompt de la fase. El resto está bien: el script, el documento y las ocho pruebas nuevas hacen lo que dicen, y los criterios CA-2 a CA-8 se cumplen. La corrección es corta: reclasificar las cuatro filas (o añadir sus pruebas), regenerar el documento, y de paso H-02 y H-04. Después vuelvo a ejecutar `r01_01`, `r01_02` y `r01_03`.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01 ni quien implementó) · 2026-11-14
- **Qué se revisa:** las correcciones de la r01 (`git diff 94c6193 HEAD`, en una copia propia: `git worktree` con HEAD separado en `08862e8`). Orden de lectura: `README.md` y la r01 de este fichero → código, mapa, pruebas y plan → al final `analisis-tecnico.md` y `pruebas.md`.
- «Ejecutado» es ejecutado por mí en mi copia; «leído» es deducción de lectura. Máquina compartida con otros trabajos: tiempos orientativos.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite del Bloque A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **3957 passed in 1672 s**; el árbol queda limpio |
| Comprobar el mapa | `.venv/bin/python .docs/scripts/evidencias_plan_a.py` (en la copia desechable, por `r01_02`) | «67 pruebas del plan, 101 pruebas automáticas citadas y todas existen · AUTOMATICA 26, DOCUMENTAL 1, PARCIAL 29, PENDIENTE_API 7, REQUIERE_USUARIOS 1, SIN_PRUEBA 3», código 0 |
| Gates ligeros, ruff y mypy | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`; ruff y mypy de A contados como el gate | los cuatro en verde (695 archivos del corpus); ruff 2902 (cuota 2902) y mypy 109 (cuota 109) |

No ejecuté `tools/check_all.sh` completo ni `evidencias_plan_a.py --ejecutar` (indicación del encargo: máquina compartida). El documento publicado dice «sobre el commit `94c6193`» y `test_h05_el_documento_publicado_coincide_con_el_mapa` (en la suite) lo compara con el mapa.

### Scripts de la r01, vueltos a ejecutar

| Script | r01 | r02 |
| --- | --- | --- |
| `r01_01_filas_automaticas_a_mano.py` | el ejecutor cumple PB-21, PB-23 y PB-49 a mano | igual: PB-21 (clave e IBAN: rechazado, cero coincidencias en archivos), PB-23 (tres intentos rechazados, huella de F4 sin cambios, tres incidencias), PB-49 (borrar la del medio o la última: lo detecta). Sigue igual lo de fuera del ticket (un IBAN solo, con espacios, se admite: ahora es T-120 en la deuda) |
| `r01_02_ataques_script.py` | 20 de 27 fallan cerrado | **prueba saltada: «No ejecutada», código 1; `xfail` que falla: «FALLA», código 1** (H-02); **«### PB-68 - …», «### PB-100 · …» y «PB-2X»: «cabeceras de prueba que no se reconocen», código 1; PB-22 sin criterio: código 1** (H-03). Un `xfail` que pasa sale «Superada» con código 0: con `--runxfail` la marca se ignora y la prueba cuenta como una normal que pasa, lo que es correcto. Siguen dando 0, como límite declarado del diseño: una PARCIAL o una PENDIENTE_API cambiada a AUTOMATICA y una prueba citada vaciada |
| `r01_03_mutantes_huecos.py` | 23 de 26 muertos; A01 vivo | H01 a H26: igual (23 muertos; H17, H18 y H22 vivos por los motivos de la r01). **A01 sigue «VIVO» en este script porque el script solo lo enfrenta a la prueba antigua** (`test_almacen_reserva_integridad_y_as_of`); contra las dos que el mapa cita ahora para PB-23, **muere** (`r02_02`) |

### Scripts nuevos de la r02 (`revisores/`)

| Script | Qué hace | Resultado |
| --- | --- | --- |
| `r02_01_pb32_a_mano_y_mutantes.py` | PB-32 como dice el plan (celda RF × H3 con habilidad y celda RV × H3 sin ella) y cuatro mutantes de `criterio_certificado` contra las tres pruebas del ejecutor que el mapa cita para PB-32 | A mano el ejecutor cumple (un certificado, el de RF). **Tres de los cuatro mutantes viven** (H-06) |
| `r02_02_mutantes_pruebas_nuevas.py` | A01 de la r01 contra las dos pruebas de PB-23, y cinco mutantes nuevos contra las pruebas de PB-21, PB-23, PB-37 y PB-54 | **6 de 6 muertos** |

```bash
cd bloque_a/11_Ejecutor && python ../../.docs/tickets/T-116/revisores/r02_01_pb32_a_mano_y_mutantes.py <copia desechable de 11_Ejecutor>
python .docs/tickets/T-116/revisores/r02_02_mutantes_pruebas_nuevas.py <copia desechable de 11_Ejecutor>
```

### Estado de los hallazgos de la r01

| ID | Gravedad | Estado | Evidencia |
| --- | --- | --- | --- |
| H-01 | alta | **corregido en las cuatro filas que señalaba; queda una de las que la r01 no leyó (H-06)** | PB-21: prueba nueva con el CT-04 del plan, clave e IBAN, búsqueda en todos los archivos y en la mensajería (N05 muere). PB-23: los tres intentos, huella de F4 tras cada uno, tres incidencias (A01, N01 y N02 mueren). PB-37: pasa a PARCIAL con su hueco («ambos en métricas»), y la prueba nueva afirma `version_de`, la entrada original byte a byte y «ambos RESUELTO» (N03 muere). PB-49: el borrado del medio y del final se afirma. El documento publicado dice lo mismo que el mapa |
| H-02 | media | **corregido** | `r01_02`: saltada y `xfail` que falla dan código 1; `test_h02_…` en la suite |
| H-03 | baja | **corregido** | `r01_02`: las tres cabeceras mal escritas y el PB sin criterio dan código 1; tres pruebas `test_h03_…` |
| H-04 | media | **corregido** | `analisis-tecnico.md` relleno (48 líneas); la deuda dice «EN QA, ronda r02»; `docs/AVANCE.md` tiene la fila de la Fase 4 (leído) |
| H-05 | baja | **corregido** | `test_h05_el_documento_publicado_coincide_con_el_mapa` compara las 67 filas del documento con el mapa |

### Las siete pruebas nuevas contra el criterio del plan (leídas y con mutantes)

| Fila | Cobertura | Juicio | Por qué |
| --- | --- | --- | --- |
| PB-21 | AUTOMATICA | bien puesta | El caso del plan tal cual (CT-04, clave API e IBAN en el comentario), incidencia SEGURIDAD con el campo y sin el valor, nada en F5 y cero coincidencias en todos los archivos y en la traza. Nota: el rechazo lo provoca la clave; el IBAN con espacios, solo, no se detecta (T-120) |
| PB-23 | AUTOMATICA | bien puesta | Los tres intentos del plan, la huella de F4 comparada tras cada uno y tres ACCESO_FUERA_DE_MATRIZ |
| PB-37 | PARCIAL | bien puesta | Afirma «PRG nuevo con `version_de`», «hash de la entrada original intacto» y «ambos RESUELTO» sobre el Almacén; el hueco («ambos en métricas» y que no hay una operación de corrección en Prospectiva) está declarado |
| PB-49 | AUTOMATICA | **dudosa (baja, dentro de H-06)** | El borrado ya se afirma. Pero la propia fila declara en «No comprueba» que «no se comparan instantáneas de ocho semanas», que es la preparación del plan y algo que el ejecutor puede hacer con el cliente simulado: con la regla del ticket, una fila AUTOMATICA solo deja fuera lo que es de tiempo real o del modelo real |
| PB-54 | AUTOMATICA | bien puesta | Los once campos del plan, presentes y no vacíos en cada encargo del ciclo (N04 muere) |
| PB-64 | AUTOMATICA | aceptable, con nota | 20 hitos al 40 %, degradación (F6 y F10 en las otras pruebas citadas) y ningún CERT de H5. Que no haya certificado de H5 es casi estructural (un PRG de H5 no tiene probabilidad interna): la afirmación es correcta pero difícil de romper |
| PB-65 | AUTOMATICA | bien puesta | Los tres casos del plan en HT-09; el dictamen del Orquestador (modelo real) está en «No comprueba» |

### Las AUTOMATICA que la r01 dejó sin leer, con la regla estricta (leídas)

| Fila | Juicio | Por qué |
| --- | --- | --- |
| **PB-32** | **mal puesta** (H-06) | El plan: 60 PRG de RF × H3 con habilidad y 40 de RV × H3 sin ella ⇒ CERT- para RF (n ≥ 100, IC 90 % del BSS > 0 tras Holm, calibración no rechazada con ECE < 0,15, CT-10 coincidente) y **ninguno para RV**; criterio: «un certificado; G3-CON-10 PASA en RF y bloquearía en RV». Las pruebas citadas certifican una celda con habilidad y rechazan una con muestra insuficiente; **ninguna afirma que una celda sin habilidad o mal calibrada no se certifica**, ni la re-ejecución CT-10 |
| PB-53 | bien puesta | La propuesta de una empresa se retira antes de entregar, HT-09 bloquea un activo concreto y la ficha de finalista no admite vehículos |
| PB-55 | bien puesta | Doce tipos, tres opciones como máximo y motivo si hay menos, doce apartados en el HTML |
| PB-56 | aceptable, con nota | La regla de duplicados se afirma sobre `_deduplicar_entre_tipos` (RF y TCV) y HT-09 bloquea los tres tipos de duplicado; el caso del plan (dos Analistas, RV e IDX, en un C1 entero) no se ejecuta de extremo a extremo |
| PB-63 | bien puesta | H5 solo con banda y ≥ 3 hitos congelados con su padre; HT-09 bloquea un H5 sin hitos o con probabilidad numérica |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí en la forma; **no en el fondo en una fila** (H-06) | 67 filas con sus cuatro campos; PB-32 dice «comprueban todo el criterio» y no es así |
| CA-2 | sí | 101 citadas, todas existen, código 0 |
| CA-3 | no repetido en esta ronda | La r01 lo ejecutó; el implementador declara 101 de 101. `test_h05_…` comprueba el documento contra el mapa |
| CA-4 | sí (por la r01 y `--pb`) | `r01_02`: `--pb PB-22` «Superada», código 0 |
| CA-5 | sí | Sin cambios respecto de la r01; el mapa sigue con 7 PENDIENTE_API, 1 con usuarios y 1 documental sin pruebas |
| CA-6 | sí | `r01_02`: los tres casos, código 1; `test_fase4_mapa.py` en la suite |
| CA-7 | sí | README («Huecos») y fila T-116 de la deuda, ya al día; T-120 recoge lo de fuera del ticket |
| CA-8 | por partes; el gate entero, pendiente | Ver «Reproducción» |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-06 | **alta** | `cd bloque_a/11_Ejecutor && python ../../.docs/tickets/T-116/revisores/r02_01_pb32_a_mano_y_mutantes.py <copia desechable de 11_Ejecutor>` → P32a, P32b y P32c `VIVO`. Leer el criterio de PB-32 en el plan y las cuatro pruebas que cita el mapa | Esperado (regla estricta del ticket; es el mismo defecto que H-01, en una de las filas que la r01 pidió repasar): AUTOMATICA solo si las pruebas citadas afirman todo el criterio. Obtenido: PB-32 figura AUTOMATICA y el documento la publica «Superada», pero quitar de `criterio_certificado` la condición del IC del BSS (P32a), la de la calibración frente al nulo (P32b) o el tope de ECE (P32c) deja en verde las tres pruebas del ejecutor citadas: nadie afirma «ninguno para RV × H3» (una celda sin habilidad no se certifica). En toda la suite, P32a lo mata una prueba no citada (`test_t66_evaluacion.py::test_pa03_minimo_de_conglomerados_desde_la_configuracion`); **P32b y P32c no los mata ninguna** de `test_t66_evaluacion`, `test_t53_evaluacion_y_almacen`, `test_t65_hallazgos`, `test_t87_datos` ni `test_unitarias` (ejecutado). La certificación es el control de R13 que abre la publicación de probabilidades. A mano, el ejecutor cumple. De paso (baja): PB-49 es AUTOMATICA con un hueco propio del ejecutor declarado en «No comprueba» | Añadir a `test_fase4_huecos.py` la prueba de PB-32 (está casi escrita en `r02_01`: celda con habilidad y celda sin ella en el mismo almacén ⇒ un solo CERT, el de RF; y un caso mal calibrado) y citarla, o pasar PB-32 a PARCIAL con su hueco; pasar PB-49 a PARCIAL o comparar instantáneas en un backtest de ocho semanas; regenerar el documento | abierto |

### Invariantes

Sin cambios respecto de la r01: no cambia código de producción por este ticket ni el corpus; todo con `MockClient`; INC-T116-01 y 02 siguen `[PROPUESTO]`; sin secretos (las claves de las pruebas son ficticias y partidas); documentación al día (H-04 corregido).

## Veredicto (r02)

**NO APTO** · Los cinco hallazgos de la r01 están corregidos en lo que decían, las siete pruebas nuevas afirman lo que dicen (6 mutantes de 6 mueren, A01 incluido) y el script falla cerrado donde antes no. Pero al repasar con la regla estricta las AUTOMATICA que la r01 dejó sin leer aparece otra fila del mismo tipo que H-01: **PB-32** se publica como «Superada» sin que ninguna prueba citada afirme que una celda sin habilidad o mal calibrada no se certifica (H-06, alta por la misma razón que H-01: evidencia que dice más de lo que las pruebas afirman, y aquí sobre el control R13). La corrección es corta: una prueba (o reclasificar PB-32 y PB-49 a PARCIAL) y regenerar el documento. Después basta volver a ejecutar `r02_01` y `r02_02`.

Lo que no comprobé: `--ejecutar` completo y el gate entero; PB-55, PB-56, PB-53 y PB-63 están leídas, no mutadas; las demás AUTOMATICA (las 19 de la r01) no las releí.

Este revisor no cierra el ticket ni toca la deuda, el diario o la memoria.
