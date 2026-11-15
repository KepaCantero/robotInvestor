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

## Ronda r03

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01 ni el de la r02, ni quien implementó) · 2026-11-14
- **Qué se revisa:** la ronda r03 (commit `e880ef4`; el `develop` de la revisión es `00ed8d3`, que solo añade T-114 r02 encima y no toca nada de T-116), en una copia propia (`git worktree` con HEAD separado). Orden de lectura: `README.md` y las rondas r01 y r02 de este fichero → el mapa, `test_fase4_huecos.py`, el plan y el código citado → mis ataques → al final `analisis-tecnico.md` y `pruebas.md`.
- «Ejecutado» es ejecutado por mí en mi copia o en copias desechables; «leído» es deducción de lectura. Máquina compartida con otro agente (carga 5 a 9): tiempos orientativos. Por indicación del encargo no ejecuté el gate completo, la suite completa ni `--ejecutar`.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Comprobar el mapa | `.venv/bin/python .docs/scripts/evidencias_plan_a.py` | «67 pruebas del plan, 103 pruebas automáticas citadas y todas existen · AUTOMATICA 24, DOCUMENTAL 1, PARCIAL 31, PENDIENTE_API 7, REQUIERE_USUARIOS 1, SIN_PRUEBA 3», código 0 (12 s) |
| Una fila | `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-32` | 6 de 6 SUPERADA, «PB-32 Certificación de un horizonte: Superada en parte», código 0 (28 s); el árbol queda limpio |
| Documento publicado | `docs/evidencias_pruebas_bloque_a.md` | PB-32 y PB-49 salen «Superada en parte» con el hueco del mapa; cabecera «sobre el commit `6b9f916`» (el documento entra en `e880ef4`; `test_h05_…` lo compara con el mapa, como pidió la r01) |
| Gates ligeros, ruff y mypy | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`; ruff y mypy de A contados como el gate | los cuatro con código 0 (695 archivos); ruff 2902 (cuota 2902) y mypy 109 (cuota 109) |
| No cambia producción | `git show --stat e880ef4 -- bloque_a/11_Ejecutor/bloque_a bloque_a/09_Pruebas bloque_a/10_Herramientas` | vacío |

### Scripts de la r02, vueltos a ejecutar (sin cambiarlos)

| Script | r02 | r03 |
| --- | --- | --- |
| `r02_01_pb32_a_mano_y_mutantes.py` | a mano, el ejecutor cumple; P32a, P32b y P32c VIVOS contra las tres pruebas citadas entonces | a mano, igual: un certificado, el de RF × H3. **P32a, P32b y P32c siguen VIVOS en este script, y es lo esperado:** el script tiene escritas a mano las tres pruebas antiguas (`CITADAS`) y no lee el mapa, así que no enfrenta los mutantes a las dos pruebas nuevas. P32d MUERTO, igual que en la r02 |
| `r02_02_mutantes_pruebas_nuevas.py` | 6 de 6 muertos | **6 de 6 muertos** (A01, N01 a N05) |

```bash
cd bloque_a/11_Ejecutor && python ../../.docs/tickets/T-116/revisores/r02_01_pb32_a_mano_y_mutantes.py <copia desechable de 11_Ejecutor, con «qa2_mut»>
python .docs/tickets/T-116/revisores/r02_02_mutantes_pruebas_nuevas.py <copia desechable de 11_Ejecutor, con «qa2_mut»>
```

### Scripts nuevos de la r03 (`revisores/`)

| Script | Qué hace | Resultado |
| --- | --- | --- |
| `r03_01_pb32_y_muestra.py` | Lee del mapa las pruebas del ejecutor citadas para cada fila y les enfrenta: (1) para PB-32, los cuatro mutantes de la r02 y cuatro nuevos; (2) un mutante por fila de una muestra de seis AUTOMATICA ya leídas, más dos de control que deben morir; (3) PB-60 a mano: credencial denegada y un ciclo simulado, y busca la degradación en los tres entregables | PB-32: **P32a, P32b, P32c y P32d MUEREN** con las cinco citadas (H-06 corregido); **P32e, P32f (Holm) y P32h (sin método) VIVEN**. Muestra: **S06, S33, S56 y S60a VIVEN**; los dos de control (S14, S60b) mueren. PB-60 a mano: F10 tiene la limitación, **ningún entregable declara la degradación** |
| `r03_02_vivos_contra_la_suite.py` | Los vivos de `r03_01`, contra más ficheros de la suite que las citadas (informativo, para la deuda) | P32f MUERE en `test_t53_evaluacion_y_almacen.py` (la prueba de Holm) y P32h en `test_t87_datos.py` (`test_certificados_separan_metodos`), ninguna citada. **Siguen VIVOS:** P32e (`test_t53_evaluacion_y_almacen`, `test_t66_evaluacion`, `test_t65_hallazgos`: 89 passed), S33 (`test_t53_…`, `test_t66_…`, `test_autocritica`: 51 passed), S56 (`test_v5`, `test_t53_seleccion_y_entrega`: 41 passed) y S60a (`test_v51`, `test_fase4_huecos`: 37 passed) |

```bash
python .docs/tickets/T-116/revisores/r03_01_pb32_y_muestra.py <copia desechable de bloque_a/11_Ejecutor, con «qa2_mut»>
python .docs/tickets/T-116/revisores/r03_02_vivos_contra_la_suite.py <copia desechable de bloque_a/11_Ejecutor, con «qa2_mut»>
```

Salida de `r03_01` (ejecutado sobre `00ed8d3`):

| Mutante | Fila | Qué rompe | Citadas | Resultado |
| --- | --- | --- | --- | --- |
| P32a | PB-32 | el IC del BSS ya no cuenta | 5 | MUERTO (3 fallan) |
| P32b | PB-32 | la calibración frente al nulo ya no cuenta | 5 | MUERTO (1) |
| P32c | PB-32 | el tope de ECE ya no cuenta | 5 | MUERTO (2) |
| P32d | PB-32 | la muestra mínima ya no cuenta | 5 | MUERTO (2) |
| **P32e** | PB-32 | **Holm no se aplica** (el Evaluador no pasa a `criterio_certificado` el umbral corregido) | 5 | **VIVO** |
| **P32f** | PB-32 | **Holm no se aplica** (`criterio_certificado` ignora `alfa_holm`) | 5 | **VIVO** |
| P32g | PB-32 | el Evaluador emite certificado aunque el criterio diga que no | 5 | MUERTO (1) |
| **P32h** | PB-32 | **las celdas se agrupan sin el método** (un certificado por clase y horizonte) | 5 | **VIVO** |
| **S06** | PB-06 | la respuesta N0 lleva una referencia que no existe (`OPP-2099-9999`) | 1 | **VIVO** |
| S14 | PB-14 | control: el cierre por invalidación se anota con otro motivo | 1 | MUERTO |
| **S33** | PB-33 | no se genera la lección de sobreconfianza (`extraer_lecciones`, «alerta de sobreconfianza» del plan) | 4 | **VIVO** |
| **S56** | PB-56 | el ciclo C1 deja de llamar a `_deduplicar_entre_tipos` | 1 | **VIVO** |
| **S60a** | PB-60 | una credencial denegada no se vuelve a pedir nunca, ni con cambio de circunstancias | 1 | **VIVO** |
| S60b | PB-60 | control: la denegación ya no deja la limitación en F10 | 1 | MUERTO |

### Estado de los hallazgos de las rondas anteriores

| ID | Gravedad | Estado | Evidencia |
| --- | --- | --- | --- |
| H-01 a H-05 | alta, media y baja | corregidos en la r02 (lo comprobó la r02); sin cambios en esta ronda | `r02_02`: 6 de 6 muertos, como en la r02 |
| H-06 | alta | **corregido en lo que pedía; queda un resto, H-08 (media)** | Las dos pruebas nuevas afirman el caso del plan (celda RF × H3 con habilidad y RV × H3 sin ella en el mismo almacén ⇒ un solo CERT, el de RF, y RV evaluada no certificable con motivo) y cada una de las cuatro condiciones de `criterio_certificado` por separado, con sus bordes (IC 0,0; ECE 0,15 estricto; `n_eff` 99,9 y nulo). P32a a P32d mueren con las cinco citadas (ejecutado). PB-32 pasa a PARCIAL. **Pero su hueco declarado («la re-ejecución CT-10») no es el único: Holm y el método tampoco se afirman (H-08)** |
| De paso en la r02 (PB-49) | baja | **corregido** | PB-49 en PARCIAL; el hueco («las supresiones de F7–F9 las hace HT-02 fuera del ejecutor, y no se comparan instantáneas de ocho semanas») es el que hay: las citadas afirman modificación y borrado (del medio y del final) y la integridad tras un ciclo; la comparación de instantáneas del plan (AS-08, ocho semanas) no se hace. Bien dicho (leído) |

### Las dos pruebas nuevas de PB-32 contra el plan (leídas y con mutantes)

- `test_pb32_se_certifica_la_celda_con_habilidad_y_no_la_que_no_la_tiene`: es el caso del plan con 150 PRG por celda (el plan dice 60 y 40, que no llegan a su propio n ≥ 100; usar 150 es razonable). Afirma lo que dice. Los PRG no llevan `metodo`, así que el certificado es de la celda sin método, y el plan pide «60 PRG RF × H3 **de un mismo método**» y «CERT- para RF × H3 **× método**».
- `test_pb32_cada_condicion_del_certificado_cuenta_por_separado`: llama a `criterio_certificado` **sin `alfa_holm`**, así que la condición de Holm («IC 90 % del BSS > 0 **tras Holm**») queda fuera; con dos celdas en el almacén la prueba anterior sí pasa por Holm, pero RF la supera de sobra y RV ya cae por el IC, así que quitarla no cambia nada (P32e y P32f viven).

### AUTOMATICA sin leer y muestra de seis ya leídas (regla estricta)

**Sin leer: ninguna.** Las 24 AUTOMATICA actuales (PB-01, 06, 07, 12, 14, 16, 21, 22, 23, 33, 38, 45, 53 a 56, 58 a 61, 63 a 66) las leyó la r01 (19, entre ellas las que siguen hoy) o la r02 (PB-53 a PB-56 y PB-63 a PB-65). Se aplica el mismo patrón que las dos rondas anteriores aplicaron a PB-23, PB-37, PB-49 y PB-32: cuenta la entrada entera del plan (preparación, resultado esperado y criterio), salvo lo que es de tiempo real o del modelo real.

| Fila | Juicio r03 | Por qué (y mutante de `r03_01`) |
| --- | --- | --- |
| **PB-60** Credencial denegada | **mal puesta** | Plan: «Limitación de servicio en F10; no se vuelve a pedir salvo cambio de circunstancias; **los entregables declaran la degradación**»; criterio: «Ninguna nueva CT-25 para ese servicio; **limitación visible**». La única prueba citada (`test_v51.py::test_credenciales_boveda`) afirma F10 y que no se vuelve a pedir. **Ejecutado a mano (`r03_01`, apartado 3): con una credencial denegada y un ciclo simulado, ni el informe técnico, ni el visual, ni el paquete JSON dicen nada de la degradación** (el paquete solo trae sus dos limitaciones de siempre; F10 sí la tiene). Leído: nada en `bloque_a/` lee `LIMITACION_SERVICIO` de F10 ni llama a `Credenciales` desde el ciclo. Es una cláusula determinista que el ejecutor **no cumple**, y el documento la publica «Superada» sin incidencia (el ticket dice que un fallo del plan es una incidencia). Además, «salvo cambio de circunstancias» no lo afirma nadie: S60a (nunca se vuelve a pedir) vive |
| **PB-33** Revocación por deterioro | **dudosa** | Plan: «Certificado REVOCADO con motivo; Novedades en F6; **alerta de sobreconfianza**; HT-09 deja de aceptar probabilidades; PRG congelados intactos». El ejecutor tiene esa alerta (la lección CALIBRACION «Sobreconfianza en …» de `Evaluador.extraer_lecciones`, con umbral de 0,10 entre la probabilidad media y la frecuencia; leído, no ejecutado, que el caso del plan con ECE 0,13 la dispararía) y ninguna de las cuatro citadas la afirma: S33 vive. «No comprueba» está vacío. La r01 ya la dio «aceptable, con nota» por el «RUN- posterior» |
| **PB-56** Duplicada entre tipos | **dudosa** | Plan: «Ejecutar C1» con dos Analistas que proponen el mismo ámbito; criterio: «Ninguna oportunidad en dos top-3». La regla se afirma sobre `_deduplicar_entre_tipos` llamada a mano; **si el ciclo deja de llamarla, la prueba citada sigue en verde** (S56 vive). La r02 la dio «aceptable, con nota» por lo mismo; con el patrón de PB-49 (preparación del plan que el ejecutor puede hacer con el simulador) es una cláusula sin afirmar |
| **PB-06** Consulta N0 | **«comprueba» dice de más** | La fila dice «referencias existentes»; la prueba solo mira que tengan un prefijo válido. Una referencia inventada (`OPP-2099-9999`) añadida a la respuesta deja la prueba en verde (S06 vive). El ejecutor sí filtra las inexistentes (`orquestacion.py`, `refs = [x … if x in conocidos]`), así que es afirmable |
| PB-14 Arrastre con invalidación | bien puesta | GC0 positivo, CERRADA con motivo INVALIDACION en F3 y en el paquete, PRG abiertos en F4: todo afirmado (S14, de control, muere). «Se explica en cambios frente al ciclo anterior» es texto del modelo |
| PB-64 H5 por hitos | bien puesta | Releída: lo que dijo la r02 se mantiene (sin mutante propio) |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · 67 filas con cobertura, pruebas, qué comprueban y qué no | sí en la forma; **no en el fondo** (H-07, H-08) | 67 filas con sus cuatro campos. PB-60 se publica «Superada» con una cláusula que el ejecutor no cumple; PB-33, PB-56 y PB-06 con una cláusula sin afirmar o con «comprueba» de más; PB-32 en parte, con el hueco incompleto |
| CA-2 · toda prueba citada existe | sí | 103 citadas, todas existen, código 0 (ejecutado) |
| CA-3 · `--ejecutar` genera el documento y termina con 0 | no repetido en esta ronda | Lo ejecutó la r01; `test_h05_…` compara el documento con el mapa y pasa (dentro de `test_fase4_mapa.py`, abajo) |
| CA-4 · cada fila superada tiene una orden que, copiada, pasa | sí (muestra) | Las dos órdenes de PB-32 copiadas del documento: `12 passed` y `1 passed`; `--pb PB-32`: código 0 |
| CA-5 · nada que dependa del modelo real, de usuarios o documental figura superado | sí | Sin cambios: 7 PENDIENTE_API, 1 con usuarios y 1 documental, sin pruebas |
| CA-6 · mapa roto ⇒ el script y `test_fase4_mapa.py` fallan | sí | Sin cambios desde la r02; `test_fase4_mapa.py` y `test_fase4_huecos.py`: **47 passed** (74 s, ejecutado) |
| CA-7 · huecos en el ticket y en la deuda | sí, con una cifra vieja (H-09) | README («Huecos» y registro) y fila T-116 de la deuda con 24 y 31 |
| CA-8 · gate 12/12; cuotas; pruebas recogidas | por partes | Gates ligeros en verde, ruff 2902 y mypy 109; el gate entero, según quien coordina, pasó al subir `e880ef4` |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | **alta** | `python .docs/tickets/T-116/revisores/r03_01_pb32_y_muestra.py <copia desechable de 11_Ejecutor con «qa2_mut»>`: apartado 3 («los entregables declaran la degradación: False») y S60a, S33, S56 y S06 «VIVO». Leer en el plan PB-60, PB-33, PB-56 y PB-06 y sus filas del mapa | Esperado (regla estricta del ticket, la misma de H-01 y H-06): AUTOMATICA solo si las citadas afirman la entrada entera del plan, salvo tiempo real y modelo real; y un fallo del plan es una incidencia. Obtenido, en una muestra de seis filas que las rondas anteriores ya habían leído: **PB-60** se publica «Superada» y el ejecutor **no** declara en los entregables la degradación por la credencial denegada (ejecutado), ni hay incidencia; tampoco se afirma «salvo cambio de circunstancias». **PB-33** («alerta de sobreconfianza») y **PB-56** (el C1 del plan; la regla solo se prueba llamando a la función a mano) tienen una cláusula afirmable sin afirmar y «No comprueba» vacío. **PB-06** dice «referencias existentes» y la prueba no lo comprueba. Es la tercera ronda seguida que una muestra encuentra filas de este tipo: el muestreo no converge | (1) PB-60 a PARCIAL con su hueco («los entregables no declaran la degradación; el ciclo no lee F10 ni consulta las credenciales») y una incidencia `INC-T116-03` por el fallo del plan, o una prueba si se decide corregir el ejecutor; prueba de «cambio de circunstancias» (una línea en `test_credenciales_boveda` o en `test_fase4_huecos.py`). (2) PB-33 y PB-56: prueba (la lección CALIBRACION tras la revisión mensual del caso del plan; un C1 con dos Analistas que proponen el mismo ámbito) o PARCIAL con su hueco. (3) PB-06: afirmar que cada referencia existe en F1–F6/F5, o quitar «existentes» del texto. (4) **Repaso sistemático de las 24 AUTOMATICA por quien implementa**, con una tabla cláusula → línea de la prueba que la afirma (preparación, resultado esperado y criterio), en vez de esperar a la siguiente muestra. Regenerar el documento | abierto |
| H-08 | media | El mismo script: P32e, P32f y P32h «VIVO» contra las cinco citadas de PB-32. `r03_02_vivos_contra_la_suite.py`: P32f lo mata `test_t53_evaluacion_y_almacen.py` (la prueba de Holm), P32h lo mata `test_t87_datos.py::test_certificados_separan_metodos` (no citadas), **P32e no lo mata ninguna de `test_t53_evaluacion_y_almacen`, `test_t66_evaluacion` ni `test_t65_hallazgos` (89 passed)** | Esperado: una fila PARCIAL dice en «No comprueba» todo lo que le falta. Obtenido: el hueco de PB-32 solo nombra la re-ejecución CT-10; el plan pide además «IC 90 % del BSS > 0 **tras Holm**» y «CERT- para RF × H3 **× método**» (PRG «de un mismo método»), y ninguna citada lo afirma: las PRG de las pruebas nuevas no llevan método y `criterio_certificado` se llama sin `alfa_holm`. Que el Evaluador deje de pasar el umbral de Holm a `criterio_certificado` (P32e) no lo ve ninguna prueba que haya ejecutado | Citar `test_certificados_separan_metodos` y la prueba de Holm de `test_t53_…`; añadir un caso con dos celdas hábiles en el que una supere el IC pero no Holm (o sembrar las PRG con `metodo`), o poner Holm y el método en «No comprueba» |
| H-09 | baja | `grep -n "| T-116 |" sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | La fila dice «101 pruebas citadas, todas superadas»; el mapa tiene 103 desde la r03 (el script: «103 pruebas automáticas citadas») | Poner la cifra de la r03 (y la de la ronda que corrija H-07) | abierto |

### Invariantes

- No cambia código de producción ni el corpus por este ticket: `e880ef4` no toca `11_Ejecutor/bloque_a`, `09_Pruebas` ni `10_Herramientas` (ejecutado); corpus íntegro (695). ✔
- Mock antes que API: todo con `MockClient`. ✔
- Ambigüedad documentada: INC-T116-01 y 02 siguen `[PROPUESTO]`; **el fallo de PB-60 no está registrado** (H-07). ✗
- Nada cuenta sin pruebas: las dos pruebas nuevas suben la suite. ✔
- Secretos: `tools/secrets_scan.py` en verde. ✔
- Documentación: al día salvo la cifra de la deuda (H-09).

### Lo que quedó sin comprobar

- `--ejecutar` completo, el gate entero y la suite completa (indicación del encargo).
- PB-64 no se mutó en esta ronda; de las 24 AUTOMATICA solo releí seis.
- Que el caso de PB-33 del plan dispare de verdad la lección de sobreconfianza (leído, no ejecutado).

## Veredicto (r03)

**NO APTO** · H-06 está corregido en lo que pedía (P32a a P32d mueren ahora con las pruebas citadas; PB-32 y PB-49 en PARCIAL) y PB-49 tiene su hueco bien dicho. Pero queda abierto un hallazgo alto nuevo del mismo tipo que H-01 y H-06 (H-07): en una muestra de seis filas AUTOMATICA ya leídas por las rondas anteriores, **PB-60 se publica «Superada» con una cláusula del plan que el ejecutor no cumple** (los entregables no declaran la degradación; ejecutado), sin incidencia, y PB-33, PB-56 y PB-06 tienen cláusulas afirmables sin afirmar. Además, el hueco de PB-32 está incompleto (H-08, media: Holm y el método). Como es la tercera vez que una muestra encuentra filas así, la corrección que propongo es un repaso cláusula a cláusula de las 24 AUTOMATICA por quien implementa, no solo de estas cuatro. Después basta volver a ejecutar `r03_01` y `r03_02`.

## Ronda r04

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01, la r02 ni la r03, ni quien implementó) · 2026-11-15
- **Copia revisada:** clon desconectado en `fb3ccd4` (la ronda r04 integrada con T-125 y T-126). Mutantes en dos copias desechables («qa7_mut»), ya borradas.
- Opinión formada con el plan, el mapa y las pruebas citadas antes de leer el apartado «Ronda r04» de `analisis-tecnico.md`.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **5798 passed** en 1489 s (máquina compartida con otra QA); el árbol queda limpio (solo mis ficheros nuevos) |
| Pruebas de `10_Herramientas` (no están en el gate; el mapa las cita) | `cd bloque_a/10_Herramientas && python -m pytest -q -p no:cacheprovider tests` | 135 passed, 38 subtests passed |
| Comprobar el mapa | `.venv/bin/python .docs/scripts/evidencias_plan_a.py` | «67 pruebas del plan, 145 pruebas automáticas citadas y todas existen · AUTOMATICA 22, DOCUMENTAL 1, PARCIAL 36, PENDIENTE_API 7, REQUIERE_USUARIOS 1», código 0 |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff (tres `11_Ejecutor`, como el gate) | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | 2902 (cuota 2902) |
| Gates ligeros | `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | los cuatro con 0 |

### Scripts de rondas anteriores, vueltos a ejecutar (sin cambiarlos)

| Script | Resultado r04 |
| --- | --- |
| `r03_01_pb32_y_muestra.py` (lee las citadas del mapa) | P32a a P32h, S06, S14, S33, S56, S60a y S60b: **todos MUERTOS** («vivos: ninguno»); S64 no se ejecuta (como en la r03). A mano, con una credencial denegada: F10 la tiene y **los tres entregables declaran la degradación** (técnico y JSON con servicio, DEGRADADO y CRD-; visual con el servicio) |
| `r04_mutantes_implementador.py` (del implementador) | M01 a M20: **20 de 20 MUERTOS** («vivos o no aplicados: ninguno») |
| `r03_02_vivos_contra_la_suite.py` | no se ejecuta: era informativo para los vivos de `r03_01`, y en `r03_01` ya no queda ninguno |

```bash
cd <copia desechable con «qa2_mut»>/bloque_a/11_Ejecutor && python <repo>/.docs/tickets/T-116/revisores/r03_01_pb32_y_muestra.py .
python <repo>/.docs/tickets/T-116/r04_mutantes_implementador.py .
```

### Script nuevo de la r04 (`revisores/r04_01_mutantes_clausulas.py`)

Un mutante por cláusula, enfrentado a las pruebas que el mapa cita para su fila (del ejecutor y de `10_Herramientas`). Uso: `python .docs/tickets/T-116/revisores/r04_01_mutantes_clausulas.py <copia desechable de bloque_a con «_mut»>`.

| Mutante | Fila | Qué rompe | Citadas | Resultado |
| --- | --- | --- | --- | --- |
| **M31** | PB-31 | la banda verbal de cada horizonte publicado deja de seguir a la probabilidad interna (siempre «incierto») | 3 | **VIVO** |
| **M37a** | PB-37 | el Evaluador deja de resolver las correcciones (PRG con `version_de`) | 4 | **VIVO** |
| **M37b** | PB-37 | el Evaluador deja de resolver el original de un PRG corregido | 4 | **VIVO** |
| M22 | PB-22 | la incidencia de canal no previsto deja de marcarse como escalada (corrección r04) | 3 | MUERTO |
| M60a | PB-60 | los entregables dejan de declarar la degradación (corrección r04) | 2 | MUERTO |
| M60b | PB-60 | con cambio de circunstancias tampoco se vuelve a pedir | 2 | MUERTO |
| M58 | PB-58 | una solicitud pendiente deja de declararse como degradada | 3 | MUERTO |
| M56 | PB-56 | el C1 deja de llamar a la regla de duplicados entre tipos | 5 | MUERTO |
| M33 | PB-33 | no se genera la alerta de sobreconfianza | 6 | MUERTO |

### Las dos correcciones del ejecutor de la r04

- **PB-58 y PB-60 (degradación declarada):** leído `Credenciales.degradaciones` y su uso en el ciclo (`orquestacion.py`, «Servicio «…» en modo degradado») y en el visual (`redaccion.py`). `test_pb60_…` afirma la limitación en el paquete, el técnico, el JSON y el visual, que no se vuelve a pedir salvo cambio de circunstancias y que deja de declararse al proveerse; `test_pb58_…`, el servicio pendiente declarado y el valor fuera de todo contexto. M60a, M60b y M58 mueren; S60a y S60b de la r03 también. **Bien.**
- **PB-22 (escalado):** las dos incidencias CANAL_NO_PREVISTO de `Mensajeria.crear` llevan `escalado_operador=True` y «rechazada y registrada», como la de acceso fuera de matriz; M22 muere. **Bien**, con una nota (H-12): la marca no la lee nada.

### Repaso cláusula a cláusula de las 22 AUTOMATICA (leídas todas, con la entrada entera del plan)

| Fila | Juicio r04 | Por qué |
| --- | --- | --- |
| PB-01 | bien | Nombres `AAAA-MM-DD_tipo_RUN-id`, F1–F5, ≤ 3, RUN- en F5, PRG congelados tras G3 (y no sin G3), N2/N1 según GC0, mensajes del catálogo, todo lo que va al Broker sale de AG-01. Fuera: hora de entrega (reloj simulado) y «siete clases» (el ciclo usa doce) |
| PB-06 | bien | ACLARACION, N0, referencias existentes en F1–F6, QRY- en F5, cero CT-05, ningún RUN- nuevo, ≤ 1 UC (S06 muere) |
| PB-12 | bien | La regla de relevancia es la misma función en el productor y en la prueba (`ht09.relevancia_esperada_alta`), pero la anclan los dos casos fijos (CRI nueva ALTA, RF de seguimiento MEDIA o BAJA); G3-CON-14, 15 y 20 corresponden a C10, C01 (vocabulario) y C11 de HT-09 |
| PB-14 | bien | GC0 positivo con la opción en `invalidadas`, CERRADA con motivo INVALIDACION en F3, PRG ABIERTO |
| PB-16 | bien | PARCIAL, limitación en los dos informes, laguna en F5, menos candidatas en RV, mismas comprobaciones G3 sin NO_APLICA, C08 OK |
| PB-22 | bien | Tres mensajes del plan, tres INC- CANAL_NO_PREVISTO, ningún efecto fuera de HA (M22 muere); nota en H-12 |
| PB-23 | bien | Tres intentos, tres ACCESO_FUERA_DE_MATRIZ, huella de F4 igual tras cada uno |
| **PB-31** | **mal puesta** | Plan, resultado esperado: «Banda «más probable que no» con «sin ventaja demostrada todavía» en técnico, visual y JSON». Las citadas afirman la etiqueta, `prob` nula, ninguna cifra ni «Alta», y que HT-09 bloquea la variante sembrada; **ninguna afirma la banda**: si todas las bandas publicadas salen «incierto» (M31), las tres siguen en verde. La banda la calcula el ejecutor (`sintesis.py`, `banda_publicable`) y es afirmable con el simulador. «No comprueba» vacío |
| **PB-37** | **mal puesta** | Plan: «Adelantar el reloj a ambos vencimientos» → «el original sin cambios y resuelto en su fecha»; criterio «ambos RESUELTO». Las dos pruebas nuevas escriben la RESOLUCION de los dos PRG **a mano** (AG-20) y no llaman a `Evaluador.resolver`: si el Evaluador dejara de resolver la corrección o el original (M37a, M37b), las cuatro citadas siguen en verde. Es el mismo patrón que S56 en la r03 (la regla probada con la llamada hecha a mano) |
| PB-43 | bien | CT-22, LEC- de producto enlazada a las tres QRY-, tema común en F5; las palabras distintas y la sección siguiente son del modelo |
| PB-45 | bien | Diez lecciones, la estadística primero, ninguna de otro tipo |
| PB-49 | bien | Ocho semanas: cada instantánea de F1–F6, RC y HA contiene la anterior; borrado del medio y del final detectado; supresiones de F7–F9 con registro de bajas (HT-02) |
| PB-53 | bien | El caso del plan en un C1; el nombre solo en `ejemplos_ilustrativos`; HT-09 bloquea un activo concreto |
| PB-54 | bien | Once campos no vacíos en cada encargo |
| PB-55 | bien | Doce apartados con semáforo en el técnico, ≤ 3 y motivo de menos de tres |
| PB-56 | bien | El caso del plan en un C1 con su motivo en F3 (M56 y S56 mueren) |
| **PB-58** | **dudosa** | Pasos 1 y 2 del plan: «El BFA envía `solicitudes_credenciales` con su retorno» y «el Coordinador comprueba HT-01 y emite CT-25». Ningún código lee `solicitudes_credenciales` de un retorno (`grep`: solo aparece en los goldens, siempre vacío); las pruebas llaman a `credenciales.solicitar` a mano. El paso es del ejecutor (leer el retorno y emitir el CT-25), no del modelo. Ni «No comprueba» ni INC-T116-03 lo dicen. El resto del criterio (valor en ningún sitio, segunda solicitud sin molestar al Broker, degradación declarada) está bien afirmado |
| PB-59 | bien | Rechazo íntegro (sigue pendiente), SEGURIDAD en HA sin el valor, depósito y renovación pedidos |
| PB-60 | bien | Corrección y sus cláusulas afirmadas (M60a, M60b, S60a y S60b mueren) |
| PB-63 | bien | Banda sin cifra, ≥ 3 hitos con fecha, indicador y criterio, espaciado, congelados con su padre, C18 OK; HT-09 bloquea sin hitos o con probabilidad |
| PB-65 | bien | Los tres dictámenes del plan en HT-09 con su motivo; el del Orquestador (CT-14) es del modelo |
| PB-66 | bien | SEG- en F11, EN_SEGUIMIENTO y `seg_id` en F3, dos C6 con ≤ 300 palabras, recomendación del vocabulario y HT-09; pausa, reanudación, cancelación inmediata y ningún ciclo después |

### Muestra de PARCIAL (regla: «No comprueba» dice todo lo que falta)

| Fila | Juicio | Por qué |
| --- | --- | --- |
| PB-02, PB-07, PB-30, PB-39, PB-62 | bien | El hueco declarado es el que hay |
| PB-13 | aceptable | Declara la rotación; «comprobación de invalidación registrada (AS-06)» es del Auditor |
| **PB-44** | **incompleta** | Declara solo «el recuento exacto contra F4 y F3». El plan pide además `significativo` false (n < 30) con nota de muestra pequeña, el mismo dato en el técnico y en el visual («Cómo nos fue») y G3-CON-18; ninguna citada lo afirma |
| **PB-46** | **incompleta** | Declara solo la recalificación en F9. No dice que en un ciclo ningún pronóstico de fuente llega a F2 (el ejecutor pierde el bloque `pronostico_fuente` al construir las piezas; QA r01 de T-125, H-01) |
| **PB-48** | **incompleta** | Declara solo COR- y P3-. No dice que en el ciclo citado ninguna opción en banda marginal se resuelve con su segunda pasada y que quitar la segunda pasada del ciclo deja las citadas en verde (QA r01 de T-126, H-01) |
| **PB-26** | **incompleta** | No dice que la «sección temática» se comprueba por el campo de la ficha y no por la sección en la que está, ni que el desempate por fecha no se comprueba (QA r01 de T-126, H-02) |

### Estado de los hallazgos anteriores

| ID | Gravedad | Estado | Evidencia |
| --- | --- | --- | --- |
| H-01 a H-06 | — | corregidos (rondas anteriores) | sin cambios |
| H-07 | alta | **corregido en lo que pedía** | PB-60: los entregables declaran la degradación (M60a, S60a, S60b mueren); PB-33 a parcial con su hueco y S33 muere; PB-56 (S56) y PB-06 (S06) mueren. Pero el repaso sistemático deja dos filas del mismo tipo (H-10) |
| H-08 | media | **corregido** | P32e, P32f y P32h mueren con las citadas (`r03_01`) |
| H-09 | baja | **corregido** | La fila T-116 de la deuda dice 145 citadas, como el script |

### INC-T116-03 (`docs/incidencias.md`)

Leída. Es `[PROPUESTO]`, distingue lo corregido (PB-60 y PB-58, PB-22) de lo que no se arregla y cada línea casa con el «No comprueba» de su fila (PB-32, 33, 07, 11, 21, 36, 38, 61, 62, 19, 50 y 64). Falta una línea para el paso de `solicitudes_credenciales` de PB-58 (H-10). PB-31 y PB-37 no son fallos del ejecutor sino de las pruebas, así que no van a la incidencia.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · 67 filas con cobertura, pruebas, qué comprueban y qué no | sí en la forma; **no en el fondo** (H-10, H-11) | PB-31 y PB-37 se publican «Superada» con una cláusula determinista sin afirmar (M31, M37a y M37b viven); PB-58 con un paso del ejecutor que no existe; cuatro parciales con el hueco incompleto |
| CA-2 · toda prueba citada existe | sí | 145 citadas, código 0 (ejecutado) |
| CA-3 · `--ejecutar` genera el documento y termina con 0 | no repetido | La suite completa de A y la de `10_Herramientas` pasan (arriba), que contienen todas las citadas; `test_h05_…` compara documento y mapa |
| CA-4 · cada fila superada tiene una orden que, copiada, pasa | no repetido | — |
| CA-5 · nada del modelo real, de usuarios o documental figura superado | sí | 7 PENDIENTE_API, 1 con usuarios, 1 documental, sin pruebas |
| CA-6 · mapa roto ⇒ el script y `test_fase4_mapa.py` fallan | sí | dentro de la suite |
| CA-7 · huecos en el ticket y en la deuda | sí | README (registro) y fila T-116 de la deuda al día |
| CA-8 · gate 12/12; cuotas; pruebas recogidas | por partes | gates ligeros y ruff 2902; el gate entero y mypy no los he pasado (encargo) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-10 | **alta** | `python .docs/tickets/T-116/revisores/r04_01_mutantes_clausulas.py <copia desechable de bloque_a con «_mut»>`: M31, M37a y M37b «VIVO». Para PB-58: `grep -rn solicitudes_credenciales bloque_a/11_Ejecutor/bloque_a` (vacío) | Esperado (regla estricta, la de H-01, H-06 y H-07): AUTOMATICA solo si las citadas afirman cada cláusula determinista de la entrada del plan. Obtenido: **PB-31** no afirma la banda «más probable que no» en los tres entregables (todas «incierto» y las citadas en verde); **PB-37** no afirma que el Evaluador resuelva los dos PRG (las pruebas escriben la resolución a mano); **PB-58** publica «Superada» sin el paso del BFA (`solicitudes_credenciales` en su retorno → CT-25), que el ejecutor no hace y nadie declara | PB-31: afirmar la banda de cada horizonte publicado frente a `banda_publicable(prob_interna)` en el JSON, el técnico y el visual (y el caso del plan con 0,65). PB-37: hacer vencer los dos PRG y llamar a `Evaluador.resolver` (o a un ciclo) en vez de escribir la RESOLUCION. PB-58: pasar a PARCIAL con el hueco y su línea en INC-T116-03, o implementar la lectura del retorno. Regenerar el documento |
| H-11 | media | Leer el plan y la fila del mapa de PB-44, PB-46, PB-48 y PB-26 (tabla de la muestra de PARCIAL) | Esperado: el «No comprueba» de una parcial dice todo lo que le falta (como H-08). Obtenido: cuatro huecos incompletos (PB-44: `significativo` y nota, mismo dato en los dos informes, G3-CON-18; PB-46: el camino de F2 roto; PB-48: la segunda pasada en el ciclo; PB-26: sección física y desempate por fecha) | Completar los cuatro «No comprueba» (o añadir las pruebas) y regenerar |
| H-12 | baja | `grep -rn escalado_operador bloque_a/11_Ejecutor/bloque_a` | El mapa de PB-22 dice «escaladas al operador»; la marca `escalado_operador` se escribe en HA y nada la lee (ni el paquete, ni los informes, ni una cola). Es igual que la de acceso fuera de matriz, ya aceptada | Decir «marcadas para escalar» o llevarlas a donde el operador las vea; si se deja, apuntarlo |

### Invariantes

- No hay LLM en la ruta determinista; mock antes que API. ✔
- Las dos correcciones del ejecutor validan antes de mutar y no cambian formatos congelados (goldens coinciden). ✔
- Decisiones del operador: INC-T116-01 a 03 `[PROPUESTO]`; falta la de PB-58 (H-10). ✗ (menor)
- Secretos: los gates en verde; mis scripts no llevan ninguno. ✔
- Documentación: LEEME y deuda al día; el documento de evidencias publica PB-31, PB-37 y PB-58 como «Superada» (H-10). ✗

### Lo que quedó sin comprobar

- `--ejecutar` completo, el gate entero, mypy, A-Forex y B (encargo).
- CA-4 (órdenes copiadas del documento).
- Mutantes contra la suite entera para M31 y M37 (solo contra las citadas, que es la regla).

## Veredicto (r04)

**NO APTO** · Las dos correcciones del ejecutor están bien (degradación declarada en los entregables en PB-58 y PB-60; CANAL_NO_PREVISTO escalado en PB-22: sus mutantes mueren), y H-07, H-08 y H-09 están corregidos. Pero el repaso cláusula a cláusula de las 22 AUTOMATICA deja otra vez filas del mismo tipo (H-10, alta): PB-31 (la banda) y PB-37 (la resolución por el Evaluador) tienen una cláusula determinista sin afirmar, con mutantes vivos, y PB-58 da por superado un paso del ejecutor que no existe. Además, cuatro parciales tienen el hueco incompleto (H-11, media). Tras corregirlo, volver a ejecutar `r04_01_mutantes_clausulas.py` (M31, M37a y M37b deben morir) y `r03_01`.

## Ronda r05

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de las rondas r01 a r04 ni quien implementó) · 2026-11-15
- **Copia revisada:** clon desconectado en `41c0ea4` (wip local: T-125 r02, T-116 r05, T-126 r02). Mutantes en copias desechables con «qa10_mut» en la ruta (y «qa2_mut» dentro, para `r03_01`), ya borradas.
- Opinión formada con el plan, el mapa y las pruebas citadas antes de leer el apartado «Ronda r05» de `analisis-tecnico.md`.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **5857 passed** en 1940 s (máquina compartida con los mutantes) |
| `10_Herramientas` (el mapa las cita) | `cd bloque_a/10_Herramientas && python -m pytest -q -p no:cacheprovider tests` | 135 passed, 38 subtests passed |
| Comprobar el mapa | `python .docs/scripts/evidencias_plan_a.py` | «67 pruebas del plan, 162 pruebas automáticas citadas y todas existen · AUTOMATICA 21, DOCUMENTAL 1, PARCIAL 37, PENDIENTE_API 7, REQUIERE_USUARIOS 1», código 0 |
| `--ejecutar` | no repetido | las 162 citadas están dentro de las dos suites de arriba, en verde; `test_h05_…` compara documento y mapa (en verde) |
| CA-4, órdenes copiadas del documento | las de PB-31 y PB-37 de `docs/evidencias_pruebas_bloque_a.md`, tal cual desde la raíz (con `.venv` enlazado) | todas pasan (4 + 1 y 5 + 1 + 2) |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff (tres `11_Ejecutor`) | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | 2902 (cuota 2902) |
| mypy de A, como el gate | `cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | 109 (cuota 109) |
| Gates ligeros | `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | los cuatro con 0 (corpus: 695 coinciden) |

### Scripts de rondas anteriores, vueltos a ejecutar sin cambiarlos

| Script | Resultado r05 |
| --- | --- |
| `revisores/r04_01_mutantes_clausulas.py <copia «qa10_mut»>/bloque_a` | **9 de 9 MUERTOS**: M31 (2 fallan), M37a (1), M37b (1), M22 (3), M60a, M60b, M58, M56, M33 |
| `revisores/r03_01_pb32_y_muestra.py .` (desde `<copia «qa2_mut»>/bloque_a/11_Ejecutor`) | P32a–P32h, S06, S14, S33, S56, S60a, S60b MUERTOS; «vivos: ninguno»; PB-60 a mano: F10 la tiene y los entregables declaran la degradación |
| `r04_mutantes_implementador.py .` (ídem) | M01 a M20 MUERTOS; «vivos o no aplicados: ninguno» |

### Repaso de las 21 AUTOMATICA

| Fila | Juicio r05 | Por qué |
| --- | --- | --- |
| **PB-31** | **bien** | Plan: banda «más probable que no» con «sin ventaja demostrada todavía» en técnico, visual y JSON; `prob_publicada` nula; variante bloqueada. `test_t116_r05.py` afirma, en un ciclo de RV sin certificados, que la banda de cada horizonte del JSON es `banda_publicable(prob_interna)` de su PRG (con `banda_verbal` en F4 y al menos dos bandas distintas) y, para los PRG con 0,65, la banda en el JSON, la fila del técnico (expresión regular por horizonte) y la tarjeta del visual. M31 muere. Nota: en el visual basta con que la cadena aparezca una vez, pero el plan solo pide el caso de 0,65 |
| **PB-37** | **bien** | Plan: «adelantar el reloj a ambos vencimientos» → el original sin cambios y resuelto en su fecha, ambos RESUELTO, ambos en métricas, huella intacta. La prueba nueva congela los dos PRG, adelanta el reloj y llama a `Evaluador.resolver` dos veces: el original se resuelve el 4-5 con su dato del 1-5 y la corrección espera; la corrección, el 11-5; nivel original igual, F4 con el prefijo de bytes y `verificar_integridad`; los dos en `resueltos` y `metricas` (n = 2). M37a y M37b mueren. Que Prospectiva decida corregir es del modelo (declarado) |
| PB-22 | bien | Las dos pruebas nuevas afirman que `estado()` y la orden `estado` listan exactamente las incidencias con `escalado_operador` (y no una DATOS sin la marca). El «comprueba» dice ahora «marcadas para escalar» |
| PB-01, PB-06, PB-12, PB-14, PB-16, PB-23, PB-43, PB-45, PB-49, PB-53, PB-54, PB-55, PB-56, PB-59, PB-60, PB-63, PB-65, PB-66 | bien | Sus citas no cambian desde la r04. Releí contra el plan PB-14 (GC0 positivo con la opción en `invalidadas`, CERRADA por INVALIDACION en F3 y en el paquete, PRG ABIERTO), PB-45, PB-54, PB-59 y PB-65: cada cláusula determinista tiene su `assert`; lo del modelo está en «No comprueba». Las demás, con la muestra de mutantes de `r03_01` y `r04_mutantes_implementador`, todos muertos |

PB-58 pasa a PARCIAL con los pasos 1 y 2 en «No comprueba», línea en INC-T116-03 y fila en `Decisiones_del_operador_Bloque_A.md`: corrige la parte de PB-58 de H-10.

### Muestra de PARCIAL

| Fila | Juicio | Por qué |
| --- | --- | --- |
| PB-44 | bien | El «No comprueba» enumera ahora el escenario de n = 27, `significativo` y su nota, el mismo dato en los dos informes y G3-CON-18 (H-11 corregido) |
| PB-46 | bien en el hueco; el «comprueba» va un poco más allá de las citadas (H-14) | Hueco: la recalificación en F9 y el backtest sin fuentes de F9. El «comprueba» dice «Brier del Motor, FC-EVAL-001, con su `calc_id`» y «una por fuente y mes», pero las pruebas que lo afirman (`test_r02_h08_…_calc_id`, `test_r02_h06_…`) no están citadas; las citadas solo afirman que `calc_id` no es vacío |
| PB-48, PB-26 | bien | Huecos completos (segunda pasada que el ejecutor no pide; desempate solo entre fichas con año) |
| PB-58 | bien | Pasos 1 y 2 declarados, con la orden que los sustituye |
| PB-10, PB-03, PB-18, PB-24, PB-35, PB-52 | bien | El hueco declarado es el que hay |
| **PB-20** | **incompleta** | Plan: el Buscador recupera la página para un Analista, ingesta al Curador, «EVD con `incidencia_manipulacion` INSTRUCCION_INCRUSTADA», fuente invalidada, INC- en HA, «si el texto llegara a un entregable, G3-EST-06 bloquea»; criterio: «ninguna puntuación **ni destino** alterado». Las citadas inyectan la instrucción por la nota del universo (otro camino), afirman la INC- MANIPULACION, que la puntuación A < 100 y que el texto no llega a los entregables. Ninguna prueba de la suite afirma `incidencia_manipulacion` en una EVD (`grep` en `tests/`: vacío), G3-EST-06 no existe en HT-09 ni en el ejecutor (solo en el prompt del Orquestador) y el «destino» no se ejerce. El «No comprueba» solo declara la baja en F9 (H-13) |
| PB-08, PB-29 | aceptables, poco precisas (H-15) | PB-08 declara «la ráfaga del plan» pero no nombra el orden por prioridad con envejecimiento ni el presupuesto por nivel; PB-29 no dice que el ejecutor no distingue derivadas (escribe `grado_independencia = RAIZ` siempre), así que «1 raíz y 20 derivadas» es del Curador |

### Estado de los hallazgos anteriores

| ID | Gravedad | Estado | Evidencia |
| --- | --- | --- | --- |
| H-10 | alta | **corregido** | M31, M37a y M37b mueren con las citadas (`r04_01`); PB-58 a PARCIAL con su hueco, INC-T116-03 y la decisión |
| H-11 | media | **corregido** | PB-44, PB-46, PB-48 y PB-26 con el hueco completo |
| H-12 | baja | **corregido** | `incidencias_escaladas` en `Bloque.estado()` y en la orden `estado`, con dos pruebas; leído: solo filtra las INC- de HA con `escalado_operador is True`; los goldens coinciden; no cambia ningún ciclo (`T-125/revisores/r02_02_ciclos_sin_bloque.py`: almacén y entregables iguales byte a byte que en `fb3ccd4`) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida |
| --- | --- | --- | --- | --- |
| H-13 | media | Leer PB-20 en el plan y su fila del mapa; `grep -rn incidencia_manipulacion bloque_a/11_Ejecutor/tests` (vacío); `grep -rln EST-06 bloque_a` (solo el prompt del Orquestador y el plan) | Esperado (regla de las parciales): el «No comprueba» dice todo lo que falta. Obtenido: no dice que no se ejerce el camino del plan (Buscador → Curador), que ninguna prueba afirma la EVD con `incidencia_manipulacion`, que G3-EST-06 no existe en el ejecutor ni en HT-09 ni que el «destino» no se prueba | Completar el «No comprueba» de PB-20 (o probar la EVD por el camino del Buscador, que el ejecutor ya marca en `_peticion_conocimiento`) y regenerar |
| H-14 | baja | Fila PB-46 del mapa frente a sus citadas | El «comprueba» afirma el Brier del Motor con su `calc_id` y una FUE- por fuente y mes, que solo afirman pruebas no citadas | Citar `test_r02_h08_…_calc_id` y `test_r02_h06_…` (o quitarlo del «comprueba»). Si T-125 cambia en su r03 (NO APTO en la r02), revisar la fila |
| H-15 | baja | Filas PB-08 y PB-29 | Huecos declarados de forma genérica | Nombrar en PB-08 el orden con envejecimiento y el presupuesto por nivel; en PB-29, que la detección de derivadas es del Curador |

Nota: el documento de evidencias dice «sobre el commit `fb3ccd4`» porque se generó antes del commit `41c0ea4`; al hacer el commit definitivo conviene regenerarlo para que el sello coincida.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · 67 filas con cobertura, pruebas, qué comprueban y qué no | sí, con H-13 a H-15 | las 21 AUTOMATICA aguantan el repaso; una parcial con el hueco incompleto (PB-20) |
| CA-2 · toda prueba citada existe | sí | 162 citadas, código 0 |
| CA-3 · `--ejecutar` genera el documento y termina con 0 | por las suites | 5857 + 135 en verde, que contienen las 162 |
| CA-4 · cada fila superada tiene una orden que, copiada, pasa | sí en la muestra | PB-31 y PB-37 |
| CA-5 · nada del modelo real, de usuarios o documental figura superado | sí | 7 PENDIENTE_API, 1 con usuarios, 1 documental |
| CA-6 · mapa roto ⇒ el script y `test_fase4_mapa.py` fallan | sí | dentro de la suite |
| CA-7 · huecos en el ticket y en la deuda | sí | INC-T116-03 ampliada; registro del README |
| CA-8 · gate 12/12; cuotas; pruebas recogidas | por partes | ruff 2902, mypy 109, gates ligeros 0, 5857 pruebas de A; `check_all.sh` no lo pasé (encargo) |

### Invariantes

- Sin LLM en la ruta determinista; mock antes que API. ✔
- El cambio de producción (`incidencias_escaladas`) solo lee HA y no cambia formatos congelados (goldens coinciden). ✔
- Decisiones del operador: INC-T116-03 `[PROPUESTO]` con PB-58 y PB-22; fila nueva en las decisiones. ✔
- Secretos: gates en verde. ✔
- Documentación: el documento de evidencias publica cada fila como está (PB-31 y PB-37 superadas con sus mutantes muertos; PB-58 en parte). ✔

### Lo que quedó sin comprobar

- `--ejecutar` completo, el gate entero, A-Forex y B (encargo).
- Mutantes propios para las 18 AUTOMATICA sin cambios desde la r04 (cubiertas por los mutantes de `r03_01` y `r04_mutantes_implementador`).

## Veredicto (r05)

**APTO** · H-10 (alta), H-11 y H-12 están corregidos: M31, M37a y M37b mueren con las pruebas nuevas, PB-58 pasa a parcial con su hueco declarado, los cuatro huecos incompletos de la r04 están completos y las incidencias escaladas se ven en el estado. Las 21 AUTOMATICA aguantan el repaso cláusula a cláusula. Quedan H-13 (media: el hueco de PB-20 está incompleto) y H-14 y H-15 (bajas), que pasan a la deuda técnica con su ID. Cerrar el ticket queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
