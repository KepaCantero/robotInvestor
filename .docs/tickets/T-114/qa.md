# T-114 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude) · **Ronda:** r01 · 2026-11-13 y 14
- Orden de lectura: `README.md` del ticket → `goldens_ct.py`, los goldens, `test_fase3_goldens.py` y `contratos.py` → mis ataques → al final `analisis-tecnico.md` y `pruebas.md`.
- Lo que digo «ejecutado» lo he ejecutado yo en mi copia; lo que digo «leído» es deducción de lectura.

## Ronda r01

### Reproducción desde limpio

Copia propia (`git worktree` en `2ff0630`, HEAD separado; lo de los tres tickets es `git diff ab95d41 HEAD`). Python del `.venv` del repositorio. La máquina se compartía con otros cuatro trabajos: los tiempos son orientativos.

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite del Bloque A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **3811 passed in 684 s**; el árbol queda limpio (ningún golden ni documento reescrito) |
| Comprobador | `python tests/goldens_ct.py` | `goldens de contratos: coinciden`, código 0 (8 s) |
| Corpus | `python tools/corpus_integridad.py` | 695 archivos coinciden, código 0 |
| Refs, secretos, NFC | `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | los tres en verde |
| ruff (como el gate) | `ruff check --output-format=concise` sobre los tres `11_Ejecutor`, `wc -l` | 2902 (cuota 2902) |
| mypy (como el gate) | `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a`, `wc -l` | 109 (cuota 109) |

No ejecuté `tools/check_all.sh` completo (indicación del encargo). CA-10 queda comprobado por partes; el implementador tampoco lo ha pasado todavía (`pruebas.md`). **Es condición de cierre.**

### Mis scripts (`revisores/`)

| Script | Qué hace | Resultado |
| --- | --- | --- |
| `r01_01_mutantes_contratos.py` | 40 mutantes de `contratos.py` (canales, campos mínimos y de retorno, `ESQUEMAS`, `Mensajeria.crear` y `validar`) contra `python tests/goldens_ct.py`; con `--suite`, además contra pruebas de la suite | 39 aplicados: 21 detectados por los goldens, 18 no |
| `r01_02_goldens_determinismo_y_update.py` | Determinismo (cuatro procesos con `PYTHONHASHSEED` distinto, otra zona horaria), `--update` sin motivo, con motivo, mutación de la última hoja de cada uno de los ocho JSON, BOM, fichero de más | 24 de 24 comprobaciones bien |
| `r01_03_mutantes_emision.py` | 11 cambios de formato en los cuerpos que el ejecutor **emite** (no en `contratos.py`) | 1 detectado por los goldens, 10 no |
| `r01_04_supervivientes_suite_completa.py` | Los supervivientes aplicados a la vez y la suite completa una sola vez | 23 a la vez: los goldens siguen diciendo «coinciden»; la suite, 3 fallos de 3811 |

```bash
python .docs/tickets/T-114/revisores/r01_01_mutantes_contratos.py <copia desechable>
python .docs/tickets/T-114/revisores/r01_02_goldens_determinismo_y_update.py <copia desechable>
python .docs/tickets/T-114/revisores/r01_03_mutantes_emision.py <copia desechable>
python .docs/tickets/T-114/revisores/r01_04_supervivientes_suite_completa.py <copia desechable> \
  M18,M20,M22,M23,M24,M25,M27,M28,M32,M33,M38,M39,M40 E02,E03,E04,E05,E06,E07,E08,E09,E10,E11
```

### Criterios de aceptación

| Criterio | Cumple | Evidencia (ejecutada salvo que diga otra cosa) |
| --- | --- | --- |
| CA-1 · seis goldens y dos ficheros a mano; la suite compara el texto exacto | sí | Suite en verde (51 pruebas del módulo dentro de las 3811); `goldens_ct.py` código 0; un BOM, un salto de línea o un fichero de más dan código 1 (`r01_02`) |
| CA-2 · cambiar un campo de un golden o de `CANALES`, `CAMPOS_MINIMOS`, `CAMPOS_RETORNO` o `ESQUEMAS` hace fallar la comparación y nombra el fichero | sí | `r01_02`: la última hoja de cada uno de los ocho JSON, mutada, da código 1 y nombra fichero y línea (los dos escritos a mano se ven por `huellas.json`). `r01_01`: M01 a M09, M11 y M12 (canales, `ANALISTAS`, campos mínimos y de retorno, su orden, tres esquemas) detectados |
| CA-3 · los 25 contratos, y coinciden con el §6.1 | sí | 25 filas `CT-` en el §6.1 del Documento 0 y 25 claves `CT-01` a `CT-25` en `tablas_contratos.json` |
| CA-4 · esquema derivado por contrato con campos en el Anexo B, válido, con la marca y con ejemplo que lo cumple; CT-16 a CT-22 «sin campos» | sí, con una inexactitud (H-02) | 32 esquemas y 32 ejemplos. Contrasté **todos** con el Anexo B, campo a campo (ver abajo). CT-22 sí tiene un campo nombrado en el Anexo B |
| CA-5 · los dos ejemplos publicados cumplen sus esquemas | no al pie de la letra; desviación declarada | El del informe de seguimiento no cumple por `x_aviso_ejemplo` (INC-T114-02, `[PROPUESTO]`, en la deuda y en el registro de decisiones). La prueba congela que ese es el único incumplimiento. El corpus no se puede tocar: lo acepto como desviación declarada (H-04) |
| CA-6 · `--update` sin motivo falla y no escribe; con motivo regenera y registra; sin opciones, código distinto de 0 si algo difiere | sí | `r01_02`: `--update`, `--motivo ""`, `"   "` y `"\t\n"` → código 2 y ningún byte cambiado aunque haya un golden roto; con motivo, regenera y añade una sola línea (un salto de línea en el motivo se aplana); sin diferencias no toca el registro; sin opciones, código 1 y no escribe |
| CA-7 · las diferencias entre el Anexo B y el ejecutor están en el golden, en INC-T114-01 y en la deuda; una nueva hace fallar la suite | **no del todo** (H-02) | Lo que hay está bien medido y congelado (22 claves por contrato y 4 del ciclo). Falta una diferencia real: CT-22 |
| CA-8 · generar dos veces da el mismo texto | sí | Cuatro procesos con `PYTHONHASHSEED` 0, 1, 12345 y aleatorio dan los seis goldens idénticos entre sí y al congelado; también con `TZ=Pacific/Kiritimati` y `LC_ALL=C` |
| CA-9 · ningún cambio en `11_Ejecutor/bloque_a/`, `01_Gobernanza/` ni `06_Plantillas_entregables/` | sí | `git diff --stat ab95d41 HEAD` sobre esas carpetas (y `02_System_prompts`, `09_Pruebas`, `10_Herramientas`): solo `diseno_v6.py`, que es de T-117. Corpus íntegro (695) |
| CA-10 · gate 12/12; cuotas sin subir; pruebas sin bajar | sí por partes; gate entero pendiente | 3811 passed; ruff 2902; mypy 109; gates ligeros en verde |

### Los esquemas derivados frente al Anexo B

Leí el Anexo B entero (122 líneas) y volqué los 32 esquemas con sus campos, obligatorios y listas cerradas. Contratos contrastados: los 18 (CT-01 a CT-15 y CT-23 a CT-25), en los dos sentidos donde los hay.

- **Nada inventado:** todo campo de todo esquema está nombrado en el párrafo o bloque de su contrato. Ningún tipo, patrón ni límite añadido; `additionalProperties` abierto.
- **Nada obligatorio que el Anexo B haga opcional, ni al revés,** en lo que el Anexo B dice expresamente: `alcance.pregunta` (CT-01), `motivo` y `texto` (CT-04), `foco` (CT-06), `fecha_corte` (CT-09: «obligatoria en evaluaciones y backtesting», condicional), `referencia_ingenua` (CT-09), `revision_seguimiento` (CT-06), `contenido` (CT-23), `aviso` (CT-24) y `seg_id`/`opp_id` solo con `SEGUIMIENTO` (CT-05, con `if/then`).
- **Listas cerradas:** las 28 coinciden valor a valor, acentos incluidos («método», «tesis frágil»).
- **Lo que falta o queda flojo** (H-02 y H-05): el campo `tipo` de CT-22; `contenido` de CT-23 «solo en ENTRANTE» queda como opcional sin condición (en CT-05 la misma clase de condición sí se codificó); los esquemas de retorno exigen todos los campos también cuando el retorno es `RECHAZADO` (el Anexo B prevé en CT-09 un retorno rechazado con `ACLARACION_REQUERIDA`, que no cumpliría su esquema).

### ¿Protegen de verdad los goldens?

**Sí lo que dicen los criterios; no todo lo que dice el objetivo.** El objetivo del ticket es «que ningún cambio de formato pase sin que salte una prueba», y el README de los goldens repite «si un formato cambia, una prueba falla».

Lo que ven (`r01_01`, 21 de 39): todo cambio en `CANALES`, `CANALES_V6`, `ANALISTAS`, `CAMPOS_MINIMOS`, `CAMPOS_RETORNO`, `ESTADOS_ESPECIFICOS` y `ESQUEMAS`; y en `crear`, lo que cambia el mensaje de un ejemplo (presupuesto y limitaciones por defecto, estado por defecto, ancho del `msg_id`, un campo nuevo en el sobre, el texto de un rechazo, exigir o no los campos mínimos).

Lo que no ven:

| Mutante | Cambio de formato | Goldens | Suite completa |
| --- | --- | --- | --- |
| M23, M24 | CT-01 admite `tipo` SEGUIMIENTO; admite `prioridad` URGENTE | no | no |
| M25 · M26 | CT-01 admite el horizonte H6 · pierde H5 | no | no · no en 257 pruebas de contratos (M26 no entró en la pasada completa) |
| M27 | **CT-02 admite una entrega con `estado_g3` BLOQUEADO** | no | no |
| M28 · M29 | CT-05 queda exento de `run_id`/`query_id` · CT-23 deja de estarlo | no | no · no en 257 pruebas (M29 no entró en la pasada completa) |
| M32 | no se comprueba el `estado` de un retorno | no | no |
| M38 | se admite un tercer `tipo_mensaje` | no | no |
| M40 | CT-01 no comprueba que `alcance` sea un objeto | no | no |
| M20, M22 | el cuerpo puede pisar campos reservados del sobre; estados de objeto contradictorios ya no se rechazan | no | no |
| M18 | la traza de mensajes pierde `tipo_mensaje` | no | no |
| M21, M30, M31, M33, M39 | formato del `msg_id` del Broker, comprobación de credenciales, estado específico de CT-23/24/25, versión del contrato, `msg_id` externo en el cuerpo | no | **sí** (otras pruebas de la suite) |
| E03, E04 | clave nueva **dentro** de cada encargo de CT-12 y dentro de `resumen` de CT-02 | no | no |
| E05 | `top3_por_clase` de CT-02 pasa de listas a un número | no | no |
| E06 a E11 | cuerpos que el ciclo semanal no emite: CT-03 (`urgencia` renombrada), CT-16, CT-22, CT-24 (sin `proximo_ciclo`), CT-25 (sin `herramienta`), CT-23 (`respuestas` renombrada) | no | no |
| E02 | `lecciones` de CT-06 pasa de identificadores a objetos | no | sí (la prueba de PB-45 de T-116) |
| E01 | clave nueva de primer nivel en el CT-06 del ciclo | **sí** | — |

Pasada conjunta (`r01_04`): con 23 mutantes aplicados a la vez, `goldens_ct.py` dice «coinciden» y la suite completa da **3 fallos de 3811**, atribuidos uno a uno a E02, M33 y M39 (comprobado por separado). Los otros **20 cambios de formato pasan a la vez por los goldens y por toda la suite.**

Por qué: (1) las reglas de valor de `validar` (listas de CT-01, `estado_g3` de CT-02, contratos exentos de `run_id`, tipos de mensaje) están escritas en el código y no en las tablas que se congelan; los ejemplos solo prueban el camino que se admite, y solo tres rechazos; (2) `formas_ciclo_mock.json` guarda las claves de primer nivel de 8 tipos de mensaje de un ciclo semanal V5: ni claves anidadas, ni tipos de los valores, ni los cuerpos que emiten la consulta, la decisión, el seguimiento, las credenciales, la consulta al Broker o el ciclo V6. La parte (2) está en «Límites conocidos» del análisis técnico, pero no en el README de los goldens ni en la deuda; la parte (1) no está en ningún sitio.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | La orden de `r01_04` de arriba (unos 11 min): `goldens_ct.py` rc=0 y «3 failed, 3808 passed». Uno a uno: `r01_01 … --solo M27` y `r01_03 … --solo E10` → «NO DETECTADO» | Esperado (objetivo del ticket y README de los goldens): un cambio de formato de un contrato hace fallar una prueba. Obtenido: 20 cambios de formato a la vez no hacen fallar nada, entre ellos que CT-02 admita una entrega con G3 BLOQUEADO (M27), que CT-01 admita valores fuera de sus listas (M23 a M25) y que el ejecutor deje de emitir un campo de CT-24 o CT-25 (E09, E10). Los criterios CA-1 y CA-2 se cumplen tal como están escritos; lo que no se cumple es lo que el ticket dice conseguir | (a) Un golden nuevo de **rechazos**: una batería fija de mensajes inválidos por contrato (valor fuera de lista, campo reservado pisado, sin `run_id`, estado no válido, tipo de mensaje desconocido) con «admitido» o la clase y el motivo del rechazo; (b) capturar formas también de una consulta, una decisión CT-04, un alta y un ciclo de seguimiento, una solicitud y respuesta de credencial, una consulta al Broker y un ciclo V6; (c) guardar las rutas de claves anidadas y el tipo JSON de cada valor, no solo las claves de primer nivel. Como mínimo, y si (b) y (c) se aplazan: decir en `tests/goldens/README.md` y en la deuda qué queda sin congelar, y corregir la frase del objetivo | abierto |
| H-02 | **alta** (criterio CA-7) | `grep -n "CT-16 a CT-22" "bloque_a/01_Gobernanza/Documento 0"*.md` → «En CT-22, `tipo` admite además `CONSULTA_RECURRENTE` y `DECISION_SEGUIMIENTO`»; `grep -n '"tipo_aviso"' bloque_a/11_Ejecutor/bloque_a/interfaz_broker.py bloque_a/11_Ejecutor/bloque_a/seguimiento.py` | Esperado (CA-7): las diferencias entre el Anexo B y el ejecutor están en el golden, en INC-T114-01 y en la deuda. Obtenido: falta una. El Anexo B nombra el campo `tipo` de CT-22 con esos dos valores; el ejecutor los emite en `tipo_aviso` (`interfaz_broker.py:207`, `seguimiento.py:137`) y usa `tipo` para `DECISIONES_BROKER` y `PREGUNTA_REPETIDA`. El ticket, el golden (`contratos_sin_campos_en_el_anexo_b`) e INC-T114-01 dicen que el Anexo B no da campos de CT-16 a CT-22 | Añadir `CT-22.ENCARGO` a los esquemas derivados (`tipo`, lista abierta), su ejemplo, la diferencia en INC-T114-01 y en el golden, y sacar CT-22 de la lista «sin campos»; re-congelar con motivo. Para ver la diferencia en el golden hace falta capturar un CT-22 real (H-01 b) | abierto |
| H-03 | media | `sed -n 163p sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | La fila T-114 de la deuda sigue en «PLANIFICADO» con el ticket EN QA, y no recoge los límites conocidos del análisis técnico (8 de 25 contratos observados, primer nivel, sin tipos) | Poner el estado y los límites en la deuda | abierto |
| H-04 | baja | `README.md` del ticket, CA-5, frente a `test_ca5_el_ejemplo_de_seguimiento_cumple_su_esquema_salvo_la_clave_de_aviso` | El criterio escrito («los dos ejemplos cumplen sus esquemas») no se cumple; la desviación está en el análisis técnico y en INC-T114-02, pero el criterio del README sigue igual | Reescribir CA-5 en el README con la salvedad y la referencia a INC-T114-02 | abierto |
| H-05 | baja | Volcar `anexo_b_esquemas.json`: `CT-23.ENCARGO` y los `.RETORNO` | (a) `contenido` «solo en ENTRANTE» no lleva condición, y `seg_id`/`opp_id` de CT-05 sí: dos reglas de derivación para el mismo caso; (b) los retornos exigen todos sus campos también con `estado` RECHAZADO o SIN_RESULTADO | Codificar la condición de CT-23 con `if/then` o decir en el `$comment` por qué no; anotar (b) en el README de los goldens como límite de la derivación | abierto |
| H-06 | baja | Leer `test_ca4_los_campos_de_cada_esquema_estan_en_el_anexo_b` | La prueba «nada inventado» busca cada nombre de campo en **todo** el Anexo B, no en el párrafo de su contrato: un campo de CT-09 puesto por error en CT-10 pasaría. (Mi contraste a mano no encontró ninguno) | Trocear el Anexo B por contrato (`**CT-NN`) y buscar en su trozo | abierto |

### Invariantes (punto 4 de la skill)

- No cambia código de producción ni corpus. ✔ (ejecutado)
- Todo formato sale de un artefacto mecánico: los goldens se generan del código y se comparan byte a byte; lo escrito a mano va con huella. ✔
- Re-congelar solo es deliberado: sin motivo no escribe; la regla está en el README y en `.docs/README.md`. ✔
- Ambigüedad documentada: INC-T114-01 (decidida por el operador) e INC-T114-02 (`[PROPUESTO]`). Falta CT-22 (H-02).
- Secretos: `tools/secrets_scan.py` en verde. ✔
- Documentación al día: `docs/AVANCE.md`, `.docs/README.md` y el README del ejecutor, sí; la deuda, no (H-03).

### Fuera del ticket (para la deuda; no cuenta en el veredicto)

- M27 enseña que **ninguna prueba de la suite** falla si `Mensajeria.validar` admite un CT-02 con `estado_g3` BLOQUEADO. La entrega pasa antes por G3 en el orquestador, así que no es un camino abierto hoy; pero la última barrera del contrato no tiene prueba.

## Veredicto

**NO APTO** · Quedan dos hallazgos altos abiertos. H-02: el criterio CA-7 no se cumple del todo (falta la diferencia de CT-22 entre el Anexo B y el ejecutor, y el ticket parte de que el Anexo B no nombra campos de CT-22). H-01: los goldens protegen las tablas y los esquemas, que es lo que piden CA-1 y CA-2, pero 20 cambios de formato a la vez pasan por ellos y por toda la suite, en contra del objetivo declarado. Lo demás es sólido: generación determinista, re-congelado solo con motivo, esquemas derivados fieles al Anexo B, sin tocar producción ni corpus. Tras la corrección vuelvo a ejecutar `r01_01` a `r01_04`. **Además, condición de cierre:** `./tools/check_all.sh` 12/12, que en esta ronda no ha ejecutado nadie.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01 ni quien implementó) · 2026-11-14
- **Qué se revisa:** la ronda r02 de T-114, commit `00ed8d3` (`develop`), en una copia propia (`git worktree` con HEAD separado). Orden de lectura: `README.md` del ticket y la r01 de este fichero → `goldens_ct.py`, `test_fase3_goldens.py`, los goldens y `contratos.py` → mis ataques → al final `analisis-tecnico.md` y `pruebas.md`.
- «Ejecutado» es ejecutado por mí en mi copia o en copias desechables; «leído» es deducción de lectura. Máquina de 4 núcleos compartida con otro agente (carga 5 a 9 durante la ronda): los tiempos son orientativos.
- Por indicación del encargo no ejecuté `tools/check_all.sh` completo ni la suite completa del Bloque A (los dos pasaron 12/12 al subir el commit, según quien coordina).

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Comprobador | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | `goldens de contratos: coinciden`, código 0 (38 s con la máquina cargada) |
| Corpus, refs, secretos, NFC | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | los cuatro con código 0 (695 archivos del corpus) |
| ruff y mypy (como el gate) | `ruff check --output-format=concise` sobre los tres `11_Ejecutor` y `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a`, contados con `wc -l` | 2902 (cuota 2902) y 109 (cuota 109) |
| Producción y corpus sin tocar | `git diff --stat 3fc54d5 00ed8d3 -- bloque_a/11_Ejecutor/bloque_a bloque_a/01_Gobernanza bloque_a/06_Plantillas_entregables`, y commit a commit | 12 ficheros de `11_Ejecutor/bloque_a`, todos de otros tickets: `6b9f916` (T-113 r02 y T-120: `contratos.py`, `diseno_v6.py`, `evaluador.py`, `ht06_indice.py`, `llm.py`, `fichas_mon_idx.py`, `orquestacion.py`), `2b9c8d9` (T-119: `fichas_p2.py`, `servicio.py`) y `ebadb7d` (T-118 y T-117 r02: `diseno_v6.py`, cuatro de `motor/`, `orquestacion.py`). **`00ed8d3` y `e880ef4` no tocan ninguna de las tres carpetas.** `01_Gobernanza` y `06_Plantillas_entregables`: sin cambios |

### Scripts de la r01, vueltos a ejecutar (sin cambiarlos, en copias desechables `qa_f3_mut_*` extraídas de `00ed8d3`)

| Script | r01 | r02 (esta ronda) |
| --- | --- | --- |
| `r01_01_mutantes_contratos.py` | 39 aplicados: 21 detectados, 18 no | **39 de 39 aplicados detectados** (`goldens_ct.py` código 1); M10 sigue sin aplicarse (su texto aparece dos veces en `contratos.py`), como en la r01. «no detectados por lo ejecutado: ninguno» |
| `r01_03_mutantes_emision.py` | 1 detectado, 10 no | **11 de 11 detectados** (E01 a E11, `goldens_ct.py` código 1) |
| `r01_02_goldens_determinismo_y_update.py` | 24 de 24 bien | **26 de 26 bien** (hay tres JSON más que en la r01): cuatro procesos con `PYTHONHASHSEED` 0, 1, 12345 y aleatorio dan los siete goldens idénticos entre sí y al congelado; también con `TZ=Pacific/Kiritimati` y `LC_ALL=C`; `--update` sin motivo (cuatro variantes) da 2 sin escribir; la última hoja de cada uno de los diez JSON, mutada, da 1 (los tres a mano por `huellas.json` o porque la batería queda mal escrita); BOM y fichero de más dan 1; la carpeta queda intacta |
| `r01_04_supervivientes_suite_completa.py` | 23 a la vez: goldens «coinciden»; suite, 3 fallos | **no ejecutado**: corre la suite completa (unos 11 min sin carga) y la máquina estaba a carga 8–9 con el gate de otro agente; el encargo lo permite. Lo que mide ya lo dicen `r01_01` y `r01_03` uno a uno |

### Scripts nuevos de la r02 (`revisores/`)

| Script | Qué hace | Resultado |
| --- | --- | --- |
| `r02_01_mutantes_mensajeria_nuevos.py` | 20 mutantes **nuevos** de `Mensajeria.crear` y `validar` (no los de la r01), medidos en proceso con una copia del módulo contra los cuatro goldens que no dependen de los flujos; los que no cambian nada se confirman con `goldens_ct.py` entero en una copia desechable (`--confirmar`) | 13 detectados; **vivos C01, C02, C03, C04, C08, C09 y C15** (H-09) |
| `r02_02_formas_y_flujos.py` | (1) captura los once flujos sin el filtro de contratos y comprueba que, filtrados, dan el golden; (2) lista lo que el filtro tira y ningún flujo guardado tiene; (3) doce cambios sobre los mensajes capturados; (5) clasificación de las rutas con clave genérica; (4) con `--copia`, tres mutantes del código del ejecutor contra `goldens_ct.py` entero | (1) control: igual al golden (220 mensajes capturados, 182 guardados). (2) **CT-05 de los ciclos ad hoc: `tipo` AD_HOC y `alcance.pregunta`, `regiones`, `tematicas`, `activos_concretos`; CT-06: `foco` como objeto (`foco.pregunta`, `foco.regiones`); CT-15: `historial_aciertos.por_horizonte…`: nada de eso está en ningún flujo guardado** (H-07). (3) T01 a T03 no se ven (H-08); T07 y T09 no se ven y están declarados; los otros siete se ven. (5) **12 de las 14 rutas con clave genérica están en todos sus objetos y el golden las pone en «a veces»** (H-08). (4) **K01, K02 y K03: `goldens_ct.py` código 0, no detectados** |
| `r02_03_motivo_del_recongelado.py` | Deshace en una copia solo el cambio de T-117 r02 que cita la línea del 14-11 de `REGISTRO.md` (el umbral de GC1 que el encargo CT-06 comunica) y compara las formas con el golden | **1 diferencia: los emisores de CT-08 del ciclo V6 vuelven a incluir AG-04 y AG-25. El motivo es cierto** y «no cambia ningún formato» también |

```bash
python .docs/tickets/T-114/revisores/r02_01_mutantes_mensajeria_nuevos.py --confirmar <copia desechable con «qa_f3_mut»>
python .docs/tickets/T-114/revisores/r02_02_formas_y_flujos.py --copia <copia desechable con «qa_f3_mut»>
python .docs/tickets/T-114/revisores/r02_03_motivo_del_recongelado.py <copia desechable con «qa_f3_mut»>
```

### Estado de los hallazgos de la r01

| ID | Gravedad | Estado | Evidencia |
| --- | --- | --- | --- |
| H-01 | alta | **corregido** (con dos restos nuevos, H-07 y H-08, y siete mutantes nuevos vivos en la mensajería, H-09, todos de gravedad menor) | `r01_01` y `r01_03`: ver la tabla de arriba (ejecutado). La batería (362 casos) congela las reglas de valor que la r01 vio pasar, y las formas de once flujos ven claves anidadas, tipos y los cuerpos que el ciclo semanal no emite. El README dice qué ve cada golden y lo que no |
| H-02 | alta | **corregido** | `CT-22.ENCARGO` en los esquemas derivados (`tipo`, obligatorio por la regla de derivación, con sus dos valores en `examples`) y su ejemplo; la diferencia medida en el golden (`tipo_aviso` con CONSULTA_RECURRENTE y DECISION_SEGUIMIENTO, y dos avisos sin `tipo`); `contratos_sin_campos_en_el_anexo_b` = CT-16 a CT-21; INC-T114-01 la recoge (leído y ejecutado: el esquema admite `tipo` PREGUNTA_REPETIDA y rechaza un aviso sin `tipo`) |
| H-03 | media | **corregido** | Fila T-114 de la deuda: «EN QA (14-11-2026, ronda r02 …)» con los límites conocidos (leído) |
| H-04 | baja | **corregido** | CA-5 reescrito con la salvedad de `x_aviso_ejemplo` e INC-T114-02 (leído) |
| H-05 | baja | **corregido** | `contenido` de CT-23 con `if`/`then`/`else`: SALIENTE sin `contenido` y ENTRANTE con él cumplen; SALIENTE con él y ENTRANTE sin él no (ejecutado). Los 15 esquemas de retorno dicen en su `$comment` que no juzgan un RECHAZADO (leído) |
| H-06 | baja | **corregido** | `campos_fuera_de_su_parrafo` busca en el párrafo del contrato: `semilla` (de CT-09) en CT-10, `fuerza` (de CT-13) dentro de las preguntas de CT-23, `urgencia` en CT-07 y `tema` en CT-22 se detectan; con los esquemas actuales, ninguno (ejecutado). Queda, sin importancia, que CT-16 a CT-22 comparten párrafo |

### Lo que se ha atacado en esta ronda

- **CT-22 en los esquemas derivados** (leído contra el Anexo B, ejecutado con `jsonschema`): el Anexo B dice «En CT-22, `tipo` admite además `CONSULTA_RECURRENTE` y `DECISION_SEGUIMIENTO`». El esquema tiene solo ese campo, obligatorio (misma regla que en los demás contratos: nombrado y no marcado como opcional), sin tipo, sin `enum` y con los dos valores en `examples`; el sentido es ENCARGO (el canal AG-01 → AG-20 es de ida). **Dice lo que dice el Anexo B y nada más.**
- **La batería** (leída entera por su lista de casos; diez casos leídos con su cuerpo y su resultado): los nombres, el `que` y el `espera` coinciden con lo que construye cada caso; donde el ejecutor se aparta del Anexo B el `que` lo dice («la mensajería no la aplica», «el Anexo B lo reserva a ENTRANTE y la mensajería lo admite»). No encontré casos mal escritos. Lo que sí falta es registrar esas diferencias (H-10).
- **Determinismo**: `r01_02` (cuatro procesos con `PYTHONHASHSEED` 0, 1, 12345 y aleatorio; otra zona horaria y `LC_ALL=C`): idénticos. Además, `test_fase3_goldens.py` en dos procesos, con `PYTHONHASHSEED=0` y `PYTHONHASHSEED=987654`: **102 passed** las dos veces, en 155 s y 143 s de reloj con la máquina a carga 9 (el implementador midió 92 s sin carga). Es aceptable para el gate; es el fichero más lento del módulo porque captura dos veces los once flujos.
- **Producción y corpus**: ver «Reproducción». **No cambia producción ni corpus por este ticket.**
- **`REGISTRO.md`, línea del 14-11 de la integración**: el motivo es cierto (`r02_03`, ejecutado). La otra línea del 14-11 (la de la r02) también: el `diff` de `mensajes_ejemplo.json` es el ejemplo nuevo de CT-22 y el corrimiento de `msg_id` y hora de los que van detrás (leído); `divergencias_anexo_b.json` y `huellas.json` cambian por CT-22, CT-23 y los `$comment`; `aceptaciones_rechazos.json` y `formas_flujos_mock.json` son nuevos. `tablas_contratos.json` y `esquemas_respuestas.json` no cambian, y no se anotan.

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | media | `python .docs/tickets/T-114/revisores/r02_02_formas_y_flujos.py --copia <copia con «qa_f3_mut»>`: apartado 2 y mutantes K01 y K02 (`goldens_ct.py` código 0) | Esperado (objetivo del ticket tras la r01: lo que los goldens no ven está en «Límites»). Obtenido: `peticion_ad_hoc`, `consulta_que_escala` e `informe_de_aprendizaje` lanzan ciclos cuyos contratos el filtro de `FLUJOS` tira (38 mensajes) porque «los del ciclo ya están en los ciclos semanales» (`analisis-tecnico.md`, «Decisiones»). **No lo están**: el CT-05 de un ciclo ad hoc lleva `tipo` AD_HOC (valor de una lista cerrada del Anexo B que ningún flujo guardado emite: solo PERIODICO y SEGUIMIENTO) y un `alcance` con `pregunta`, `regiones`, `tematicas` y `activos_concretos`; su CT-06 lleva `foco` como objeto (en los flujos guardados `foco` es siempre nulo; es campo del Anexo B); el CT-15 de un ciclo con pronósticos resueltos lleva `historial_aciertos.por_horizonte`. Que el ejecutor mande el CT-05 de una petición ad hoc con `tipo` PERIODICO (K01) o sin `alcance.pregunta` (K02) no lo ve ningún golden, y no figura en «Límites» del README ni del análisis | Guardar todos los contratos (`TODOS`) también en esos tres flujos (las formas se agrupan por flujo, así que no se mezclan con las del ciclo semanal), o al menos CT-05, CT-06 y CT-15; si no, decirlo en «Límites» y quitar la frase de «Decisiones» |
| H-08 | baja | El mismo script: apartado 5, cambios T01 a T03 («NO SE VE») y mutante K03 (`goldens_ct.py` código 0) | Esperado (README: «en dos grupos: las que están en todos los objetos que podrían llevarlas y las que solo en algunos»). Obtenido: en `rutas()`, una clave genérica (`<clase>`, `<id>`) suma una vez por cada clave real del objeto, así que con más de un tipo de activo la cuenta pasa del número de objetos y la ruta cae en «a veces» aunque esté en todos: **12 de las 14 rutas con clave genérica** (`resumen.top3_por_clase.<clase>` de CT-02, `nivel_por_clase.<clase>`, `presupuesto_por_clase.<clase>` y `delta_gc0.<clase>` de CT-05, `paquete_sintesis.clases.<clase>` de CT-15, `nivel_por_clase.<clase>` de CT-17). Consecuencia: que uno de los dos CT-02 del ciclo V5 salga con `top3_por_clase` vacío (K03), o un CT-05 con `nivel_por_clase` vacío (T02), no cambia el golden. No está entre los límites declarados (que hablan de claves **opcionales**) | En `rutas()`, contar cada ruta una sola vez por objeto (`cuenta` solo en la primera clave real que da esa ruta genérica); re-congelar con motivo. O declararlo en «Límites» |
| H-09 | baja | `python .docs/tickets/T-114/revisores/r02_01_mutantes_mensajeria_nuevos.py --confirmar <copia con «qa_f3_mut»>` → «vivos: …» | Esperado (README, «Qué ve»: los datos protegidos (R8), los campos comunes, el estado propio, las listas de CT-01, CT-02 con `entregables` y `resumen`). Obtenido, con `goldens_ct.py` entero: no se ven **C01 a C03** (el examen R8 deja fuera `limitaciones`, `autoevaluacion`, `presupuesto` o `consumo`: un retorno con una clave en su `limitaciones`, que escribe el agente, pasaría), **C04** (un `run_id` vacío pasa por `validar`), **C08** (en CT-23 a CT-25, un estado común COMPLETO en el cuerpo con PARCIAL por su sitio ya no se trata como contradictorio), **C09** (CT-01 admite `horizontes` como texto: `""` pasa) y **C15** (CT-02 admite `resumen` como lista). La batería solo prueba un tipo erróneo por campo y datos protegidos en cuerpo, clave, lista y `run_id` | Casos nuevos: una clave en `limitaciones` y en `autoevaluacion` de un retorno y en `presupuesto`/`consumo`; `via: validar` con `run_id` vacío; CT-23 retorno con `estado` PARCIAL por su sitio, COMPLETO en el cuerpo y el campo propio; `horizontes: ""` y `resumen: []`. O declarar en «Límites» qué partes de esas reglas no se congelan |
| H-10 | baja | `aceptaciones_rechazos.json`: los 18 casos `…fuera_de_la_lista_del_anexo_b` (de 10 contratos) y `CT-23/saliente_con_contenido`, `CT-23/entrante_sin_contenido` (ADMITIDO); `awk '/INC-T114-01/,/INC-T114-02/' docs/incidencias.md` | Esperado (CA-7: las diferencias entre el Anexo B y el ejecutor están en el golden de divergencias, en INC-T114-01 y en la deuda). Obtenido: la batería congela que la mensajería admite valores fuera de las listas cerradas del Anexo B (CT-03, CT-05, CT-06, CT-07, CT-08, CT-09, CT-14, CT-23, CT-24 y CT-25) y que no aplica la condición de `contenido` de CT-23, pero ni `divergencias_anexo_b.json` ni INC-T114-01 lo dicen (solo las fases de CT-06, porque el ciclo las emite). Leído: algunas las aplica otra capa (`accion` y `frecuencia` de CT-24 en `Seguimientos.procesar`; `tipo` y `modo` de CT-23 en `ConsultasBroker.enviar`) y otras ninguna (`urgencia` de CT-03 pasa tal cual de `Bloque.consulta` al mensaje); no está medido | Una línea en INC-T114-01: qué listas y condiciones del Anexo B no aplica la mensajería y, de ellas, cuáles aplica otra capa y cuáles ninguna (para la próxima entrega del Documento 0) |
| H-11 | baja | `README.md` del ticket, CA-1 y CA-2 | CA-1 dice «existen los seis goldens y los dos ficheros escritos a mano» y CA-2 «cualquiera de los seis goldens»; desde la r02 son siete y tres (`bateria_mensajes.json`), como dice el propio «Diseño» | Actualizar las cifras de CA-1 y CA-2 |

### Criterios de aceptación

| Criterio | Cumple | Evidencia (ejecutada salvo que diga otra cosa) |
| --- | --- | --- |
| CA-1 · los goldens y los ficheros a mano existen y la suite compara el texto exacto | sí (con la cifra vieja del texto, H-11) | Siete generados y tres a mano; `goldens_ct.py` código 0; `test_fase3_goldens.py`: 102 passed (dos veces) |
| CA-2 · cambiar un golden o una tabla del código hace fallar la comparación y nombra el fichero | sí | `r01_02`: la última hoja de cada JSON, mutada, da código 1 y nombra fichero y línea (los tres escritos a mano, a través de `huellas.json` o de la batería mal escrita). `r01_01`: los mutantes de tablas y esquemas, detectados |
| CA-3 · CT-01 a CT-25, como el §6.1 | sí | `tablas_contratos.json` no cambia en la r02 (REGISTRO); la r01 lo contrastó |
| CA-4 · esquema derivado por contrato con campos en el Anexo B, válido, con marca y ejemplo; CT-16 a CT-21 sin campos | sí | 33 esquemas y 33 ejemplos, todos con la marca; CT-22 con `tipo`; `contratos_sin_campos_en_el_anexo_b` = CT-16 a CT-21; nada fuera del párrafo de su contrato (H-06) |
| CA-5 · ejemplos publicados frente a sus esquemas, con la salvedad de INC-T114-02 | sí | Criterio reescrito (H-04); su prueba, en `test_fase3_goldens.py` |
| CA-6 · `--update` sin motivo falla y no escribe; con motivo escribe y registra | sí | `r01_02`: `--update`, `--motivo ""`, `"   "` y `"\t\n"` → código 2 sin escribir; con motivo regenera y añade una sola línea; sin diferencias no toca el registro |
| CA-7 · las diferencias Anexo B ↔ ejecutor en el golden, en INC-T114-01 y en la deuda; una nueva hace fallar la suite; incluida la de CT-22 | sí en lo que mide el cálculo de divergencias (CT-22 incluida); con un resto sin registrar (H-10, baja) | `divergencias_anexo_b.json` e INC-T114-01 (leído); una diferencia nueva cambia el golden (pruebas de CA-7) |
| CA-8 · dos generaciones, el mismo texto | sí | `r01_02` (cuatro semillas de hash, otra zona horaria y otra configuración regional) y dos procesos de `test_fase3_goldens.py` con `PYTHONHASHSEED` distinto: 102 passed las dos veces |
| CA-9 · nada en `11_Ejecutor/bloque_a/`, `01_Gobernanza/` ni `06_Plantillas_entregables/` | sí | `00ed8d3` no toca esas carpetas; lo que hay entre `3fc54d5` y `00ed8d3` es de T-113, T-117, T-118, T-119 y T-120 |
| CA-10 · gate 12/12, cuotas, pruebas recogidas | por partes | Gates ligeros en verde; ruff 2902 y mypy 109. El gate entero y la suite, según quien coordina, en verde al subir `00ed8d3`; no los repetí |
| CA-11 · los mutantes de `r01_01` y `r01_03` hacen fallar `goldens_ct.py` o están declarados uno a uno | **sí** | `r01_03`: 11 de 11 detectados; `r01_01`: 39 de 39 aplicados detectados (ejecutado). No queda vivo ninguno de los mutantes de la r01 |

### Invariantes

- No cambia código de producción ni el corpus (ejecutado, ver «Reproducción»). ✔
- Todo formato sale de un artefacto mecánico: los goldens se generan del código y se comparan byte a byte; lo escrito a mano va con huella. ✔
- Re-congelar solo es deliberado: sin motivo no escribe (`r01_02`); las dos líneas del 14-11 de `REGISTRO.md` llevan un motivo cierto (`r02_03` y lectura del `diff`). ✔
- Ambigüedad documentada: INC-T114-01 (decidida: manda el código) e INC-T114-02 `[PROPUESTO]`; queda el resto de H-10. ✔ con nota
- Secretos: `tools/secrets_scan.py` en verde (los datos protegidos de la batería son ficticios). ✔
- Documentación: README de los goldens y análisis al día salvo H-07, H-08 y H-11; la deuda, al día (H-03). ✔ con nota

### Lo que quedó sin comprobar

- `r01_04` (suite completa con los 23 mutantes a la vez), el gate entero y la suite completa: por la carga de la máquina y por indicación del encargo.
- CT-07 y CT-14 siguen sin forma emitida (límite declarado); no intenté un cliente simulado a medida.
- No contrasté otra vez campo a campo los 32 esquemas que la r01 ya contrastó; sí el nuevo de CT-22 y el cambio de CT-23.

## Veredicto (r02)

**APTO** · Los dos hallazgos altos de la r01 están corregidos: los 39 mutantes aplicables de `contratos.py` y los 11 de lo emitido hacen fallar ahora `goldens_ct.py` (ejecutado), y CT-22 tiene su campo del Anexo B, su esquema derivado y su diferencia con el ejecutor congelada y registrada. Los medios y bajos de la r01 también (H-03 a H-06). Los once criterios se cumplen (CA-10 por partes; el gate entero lo dio en verde quien coordina al subir `00ed8d3`). Generación determinista, re-congelado solo con motivo y motivos ciertos en `REGISTRO.md`, sin tocar producción ni corpus. Quedan abiertos un hallazgo medio y cuatro bajos, todos de alcance de lo que los goldens ven, que pasan a la deuda con su ID: **H-07** (media: los contratos de los ciclos ad hoc que el filtro tira —CT-05 con `tipo` AD_HOC, CT-06 con `foco`, CT-15 con historial— no los ve ningún golden ni lo dice «Límites»), H-08 (rutas con clave genérica mal clasificadas), H-09 (siete mutantes nuevos de la mensajería vivos, entre ellos tres del examen R8), H-10 (diferencias de la batería sin registrar en INC-T114-01) y H-11 (cifras de CA-1 y CA-2).

Este revisor no cierra el ticket ni toca la deuda, el diario, la memoria ni el registro: lo hace quien coordina (cierre, deuda con H-07 a H-11, commit).
