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
