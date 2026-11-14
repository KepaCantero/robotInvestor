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
