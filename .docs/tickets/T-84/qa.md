# T-84 · QA independiente

- **Revisor:** Claude, como revisor nuevo sin el contexto de la pieza (la V0.63 la escribió GLM; su revisión independiente se había dado por renunciada en `sistema_global/marco_comun_c/entrega_glm/V0.63/revision.md`). Formé la opinión con el Documento 0 de GLM, el código de `pruebas/pruebas_semana.py`, `validador/diario.py`, `validador/reloj.py` y `validador/persistencia.py` antes de leer las notas de entrega.
- **Ronda:** r01 · 2026-11-10 · revisado sobre `develop` (`c4d0c5a` y `c306132`: entre los dos no cambia ninguna de las cuatro piezas).
- **Qué se revisa:** la pieza V0.63 (la semana simulada) y los dos huecos que GLM dejó señalados (G-05 y PC3-09 del Documento 0 de la V0.67): un segundo corte en el diario firmado y un arranque con el reloj por detrás del estado. No hay implementación nueva que aprobar.

## Ronda r01

### Reproducción desde limpio

- **Lote del marco en el árbol de trabajo:** `.docs/scripts/pruebas_marco.sh` da «59 pasan, 0 fallan».
- **Copia limpia:** un `git worktree` de `c306132` en el scratchpad, quitado al terminar. Todas las `pruebas/pruebas_*.py` con `/home/claude/repo/.venv/bin/python -I -B` (resultado en la sección de abajo, «Reproducción en la copia limpia»).
- **Determinismo:** dos ejecuciones seguidas de `pruebas/pruebas_semana.py` dan la misma salida byte a byte (123 comprobaciones, «TODAS LAS PRUEBAS PASAN», unos 8 s de reloj y 3,4 s de CPU).
- **Sondas de esta ronda** (en la carpeta V0.63_revision de entrega_claude del marco, sin rastrear en git; todas con `python3 -I` desde el marco):
  - r01_mutaciones_semana.py: 27 mutaciones dirigidas sobre diario, reloj, persistencia y la propia batería, cada una en una copia temporal del marco (nunca en el repositorio). Opciones `--doradas` (también la dorada de la V0.66), `--resto` (siete baterías de T-03 y la jornada) y `--todas` (todas las baterías).
  - r02_segundo_corte_firmado.py: el hueco 1 de GLM (27 comprobaciones).
  - r03_reloj_detras_del_estado.py: el hueco 2 de GLM (17 comprobaciones, 3 hallazgos).
  - r04_reloj_huecos_sin_bateria.py: dos propiedades del reloj que ninguna batería fija (2 comprobaciones). La sonda no es vacía: cae con cada una de las dos mutaciones.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · la semana prueba de verdad lo que dice: reloj, diario, puntos de control, reinicios y determinismo | **no**, en la parte del reloj | r01: la semana caza las 7 mutaciones de diario y persistencia que dice cubrir (D02, D04, D05, D07, P05, P06). Deja vivas las 7 del reloj que dice cubrir (R01, R02, R03, R05, R07, R08 y R09) y las 2 de la propia batería (S01 y S02). La dorada de la V0.66 no caza ninguna de las 27 (H-01, H-02 y H-03) |
| CA-2 · hueco 1 de GLM: un segundo corte en el diario firmado, tras un primer corte y su recuperación, falla cerrado, sin perder ni duplicar operaciones y sin aceptar un diario alterado | sí | r02: 27 de 27. El barrido abarca 50 posiciones de corte en dos pasos, uno de ellos con 10 líneas. Se cumplen la réplica independiente del estado esperado, un OP con su RES y sin repeticiones, y la idempotencia byte a byte. También se recupera de un corte dentro de la reescritura que limpia, de un corte a mitad del RES que completa abrir y de tres cortes dentro del punto firmado. Los diarios alterados dan DI-02 y una línea falsificada sin salto final se descarta sin aplicarse. La semana sigue hasta el final idéntica al gemelo. Queda un resto: H-06 |
| CA-3 · hueco 2 de GLM: con el reloj detrás del estado, nada da instantes anteriores y todo falla cerrado | sí, con H-04 y H-05 | r03: con 1 día, 1 h o 5,5 s de atraso, RL-02 bloquea el reloj y ni `contrastar` ni `ahora` dan instante. Con 5 s o 4 s, nunca sale un instante anterior al del estado y se opera sin O-16. `degradar_por_reloj` a través del diario firmado usa el instante del estado y la degradación queda anotada. Rearmar sin corregir la hora da RL-01. Si se olvida `comprobar_estado`, el Reloj sí da un instante anterior, pero el Orquestador lo rechaza con O-16 y G no envía nada (H-04). El instante de guardado puede retroceder (H-05) |
| CA-4 · la batería y el lote completo pasan desde limpio | sí | Lote 59/59 y copia limpia (abajo); semana determinista |

### Resultado de las mutaciones (r01)

«Se espera» es CAZAR cuando el Documento 0 de la V0.63 (§1 a §3) o el LEEME dicen que la semana lo prueba, y FUERA cuando es robustez que la semana no pretende cubrir. «Otras» son las baterías del marco que la cazan (`--resto`; para R04, R06 y S01, `--todas`).

| ID | Se espera | Semana | Dorada | Otras | Qué rompe |
| --- | --- | --- | --- | --- | --- |
| D01 | FUERA | viva | viva | firma_t03 | abrir acepta cualquier firma en las líneas |
| D02 | CAZAR | **cazada** | viva | firma_t03 | las líneas no se firman con clave |
| D03 | FUERA | viva | viva | diario_t03 | DI-04 desactivado |
| D04 | CAZAR | **cazada** | viva | diario_t03, jornada | tras una línea a medias se pierde la última operación entera |
| D05 | CAZAR | **cazada** | viva | diario_t03, robustez_t03, jornada | la línea cortada no se limpia |
| D06 | FUERA | viva | viva | diario_t03, firma_t03, robustez_t03 | una línea rota en medio se trunca en silencio |
| D07 | CAZAR | **cazada** | viva | diario_t03, firma_t03, jornada | el punto no guarda el estado |
| D08 | FUERA | viva | viva | diario_t03, reloj_t03, reloj_diario_t72 | DI-06 desactivado |
| D09 | FUERA | viva | viva | diario_t03 | una OP sin RES en medio se acepta |
| D10 | FUERA | viva | viva | diario_t03, jornada | la OP pendiente se aplica sin anotar su RES |
| R01 | CAZAR | **viva** | viva | reloj_t03 | `comprobar_estado` nunca da RL-02 |
| R02 | CAZAR | **viva** | viva | reloj_t03 | `comprobar_estado` no fija el suelo |
| R03 | CAZAR | **viva** | viva | reloj_t03 | instantes por debajo del suelo |
| R04 | FUERA | viva | viva | **ninguna** (ver abajo) | `contrastar` da la referencia, no el mayor |
| R05 | CAZAR | **viva** | viva | reloj_t03, robustez_t03, reloj_diario_t72 | RL-03 desactivado |
| R06 | FUERA | viva | viva | **ninguna** (ver abajo) | sin el control de salto entre dos lecturas |
| R07 | CAZAR | **viva** | viva | reloj_t03, reloj_diario_t72 | `Reloj.ahora()` no da nunca un instante |
| R08 | CAZAR | **viva** | viva | reloj_t03, reloj_diario_t72 | `ahora()` sin contraste |
| R09 | CAZAR | **viva** | viva | reloj_t03, robustez_t03 | `contrastar` no lee el reloj: devuelve la referencia |
| P01 | FUERA | viva | viva | persistencia_t03, robustez_t03 | PE-02 desactivado |
| P02 | FUERA | viva | viva | firma_t03, robustez_t03 | PE-06 desactivado |
| P03 | FUERA | viva | viva | firma_t03, robustez_t03 | la firma del estado no cubre el estado |
| P04 | FUERA | viva | viva | persistencia_t03 | cargar sin `integridad()` |
| P05 | CAZAR | **cazada** | viva | las siete | volcar pierde un atributo |
| P06 | CAZAR | **cazada** | viva | firma_t03, robustez_t03 | volcar con clave no firma |
| S01 | CAZAR | **viva** | viva | ninguna | el corte del miércoles no corta nada |
| S02 | CAZAR | **viva** | viva | ninguna | la máquina no llama a `comprobar_estado` |

Lo que la semana caza del diario y de la persistencia, lo caza bien: cae en el paso exacto (el arranque del martes, el `miercoles_libre`, el arranque del jueves). Lo FUERA lo cubren las baterías de T-03, con dos excepciones en el reloj (H-07). La dorada no caza nada de esto: es lo esperado, porque fotografía el gemelo en memoria.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | r01 con `--solo R05,R07,R08,R09` | **Esperado:** dicen que la semana ejercita el Reloj el Documento 0 de la V0.63 (§2: «es el único origen de instantes»; §3: RL-03 y RL-04 «implícitos») y el LEEME («con el instante saliendo SIEMPRE del `Reloj`»). Si el Reloj se rompe, la semana debería caer. **Obtenido:** la semana pasa entera con estas mutaciones: `ahora()` no da nunca un instante (R07), da instantes sin contraste (R08), `contrastar` no lee el reloj y devuelve la referencia (R09) o no compara con ella (R05). Hay dos causas en la `Maquina` de la batería. (1) `instante()` llama a `contrastar` en cada paso, nunca a `Reloj.ahora()`, que es lo que usaría la marcha real. (2) `pasar()` lleva la pared y la `hora_datos` del intermediario exactamente al mismo segundo, así que `max(pared, referencia)` es siempre la referencia y el desfase siempre 0. El instante de la semana es la hora del intermediario simulado, con o sin Reloj. Por lo mismo, «los instantes nunca bajan» es una tautología, porque las fuentes solo avanzan. El Reloj sí está probado en `pruebas_reloj_t03.py` y en `pruebas_reloj_diario_t72.py`. Lo que falta es la prueba de integración que la pieza dice ser | En la `Maquina`: `instante()` con `reloj.ahora()`, y `contrastar` solo al arrancar y cuando `ahora()` pida RL-04. Un desfase fijo de unos segundos entre la pared y la `hora_datos`, distinto según el día (por ejemplo −2 s y +3 s, dentro de los 5 s), con una comprobación de que el instante de cada paso es el mayor de los dos. Las mutaciones R05, R07, R08 y R09 de r01 como regresión. Si no se cambia la batería, corregir el Documento 0 y el LEEME: hoy dicen más de lo que se prueba | abierto |
| H-02 | baja | r01 con `--solo R01,R02,R03,S02`; r03, B9 | **Esperado:** el Documento 0 dice que la batería lo afirma («RL-02 (implícito)»). **Obtenido:** el reloj nunca arranca detrás del estado, así que `comprobar_estado` puede no dar RL-02 (R01), no fijar el suelo (R02), el suelo puede no aplicarse (R03) o la llamada puede quitarse (S02), y la semana pasa igual. Es el hueco 2 que señaló GLM. Además, `arrancar` e `instante()` comprueban con `assert`. Un RL-02 tumba la batería con un AssertionError sin contarse como FALLA, y con `python -O` la comprobación desaparece (B9). El producto se porta bien (CA-3) | Contar los resultados de `comprobar_estado` y `contrastar` con `h.chk`, no con `assert`. Añadir una mañana con el reloj atrasado: RL-02, `degradar_por_reloj` a través del diario y rearme. r03 sirve de base | abierto |
| H-03 | baja | r01 con `--solo S01` | **Esperado:** el corte del miércoles se recupera porque hubo corte (§3: «DI-02 (implícito): la última línea a medias se ignora y se limpia»). **Obtenido:** con `cortar()` sin efecto la semana pasa igual, y ninguna otra batería lo nota. La batería solo exige `ab["ok"]`: no mira `linea_incompleta` ni que el fichero quede limpio. Además, el corte solo añade un trozo de la última línea detrás de un RES completo. No deja nunca una OP sin su RES, y la semana no corta nunca el diario firmado. Ese es el hueco 1 que señaló GLM, y r02 lo cubre: el producto se porta bien (CA-2) | Exigir `ab["linea_incompleta"] is True` y que, después, el diario acabe en salto de línea. Añadir un corte «sin RES» y un segundo corte en el diario firmado, por ejemplo C1 y C2 de r02 en el jueves | abierto |
| H-04 | baja | r03, B8 | **Esperado:** el docstring de `reloj.py` dice que `ahora()` no da nunca un instante anterior al último del estado y que un reinicio «vuelve a exigir contrastar y `comprobar_estado`». **Obtenido:** con un `Reloj` nuevo y sin llamar a `comprobar_estado`, `contrastar` y `ahora` dan un instante una hora anterior al último del estado. Solo exige el contraste. El fallo queda cerrado más abajo: el Orquestador lo rechaza con O-16 y deshace todo, y G no envía nada (G-06). Llamar después a `comprobar_estado` da RL-02, pero tarde | El Reloj no da instantes (RL-04, «sin comprobar el estado») hasta que un `comprobar_estado` vaya bien. Otra opción es recibir el estado al construirse. Regresión: B8 | abierto |
| H-05 | baja | r03, B10 | **Esperado:** el instante con que se guarda el estado (`guardado_en`) no retrocede, y un reloj detrás de él no da instantes anteriores. **Obtenido:** `comprobar_estado` solo mira `ultimo_ahora`. La semana hace el punto de la noche 2 minutos después de la última operación, así que un reloj 60 s detrás del `guardado_en` arranca sin RL-02 y da un instante anterior. `Diario.punto()`, `crear` y `persistencia.volcar` aceptan cualquier instante bien escrito, también uno de 2020, anterior a `ultimo_ahora` y al `MINIMO` del reloj: el estado se guarda y se vuelve a cargar con un `guardado_en` que retrocede. Hoy el `guardado_en` no decide nada, porque solo lo usan las migraciones como dato | `punto()` (y `crear`) rechazan un instante anterior a `ultimo_ahora` o al `guardado_en` del estado anterior. `abrir` expone el `guardado_en`, y `comprobar_estado` lo toma también como suelo | abierto |
| H-06 | baja | r02, C4 (nota final) | **Esperado:** un corte dentro de una escritura atómica no deja basura. **Obtenido:** si el proceso muere después de escribir el temporal y antes del `os.replace`, queda un `.diario-*.tmp` en la carpeta del diario. Lo mismo pasa con `.estado-*.tmp` en `persistencia.guardar`, porque el `finally` no corre con el proceso muerto. Nadie los borra después. Cada uno puede ocupar tanto como el diario o el estado (hasta `MAX_BYTES`). No afecta a la recuperación | `abrir` (o el arranque) borra los `.diario-*.tmp` y `.estado-*.tmp` de esa carpeta, o al menos los cuenta en `estado_diario()` para que la consola avise | abierto |
| H-07 | baja (pruebas del marco, anterior a la V0.63) | r01 con `--todas --solo R04,R06`; r04 | **Esperado:** cada propiedad documentada del Reloj tiene una prueba que cae si se rompe. **Obtenido:** ninguna de las baterías del marco caza estas dos mutaciones. R04: `contrastar` da «el mayor de los dos», según su docstring, y nadie comprueba el caso del reloj por delante de la referencia. R06: sin el control de salto entre dos lecturas, solo queda el de deriva desde el ancla, que tras un día de marcha ya tolera 2 + 0,0005 × 86 400 = 45 s; un salto de 10 s pasaría sin RL-01. El código actual cumple las dos (r04 en verde) | Llevar los dos casos de r04 a `pruebas_reloj_t03.py` | abierto |
| H-08 | baja | Documento 0 de la V0.63, §4; LEEME, entrada de la V0.63 | **Esperado:** lo que la pieza promete, la batería lo exige. **Obtenido:** el «determinista: dos ejecuciones dan la misma salida byte a byte» es cierto (lo reproduje), pero lo comprobó GLM a mano: la batería no lo exige. La dorada de la V0.66 fija el recorrido del gemelo, no la salida ni el gemelo con diario. Tampoco sirve como red el `revision.md` de la V0.63, que la da por «renunciada»: esta QA la sustituye | Al aplicar esta QA, citar T-84 en el `revision.md` de la V0.63 y en G-05 y PC3-09. Si se quiere fijar el determinismo, una comprobación que ejecute `main()` dos veces y compare la salida | abierto |

### Sin hallazgo en lo comprobado

- **Diario firmado, segundo corte (r02):**
  - Primer corte vivo en `jueves_stop` y otro en `viernes_kill`, con media línea RES.
  - Segundo corte en `jueves_conciliar` (2 líneas) y en `viernes_rearmar` (10 líneas: acusar avisos, conciliar y rearmar), en cada línea al principio, un byte dentro, a la mitad, justo antes del salto y justo después: 9 y 41 posiciones.
  - En todas, `abrir` funciona y da el estado de una réplica independiente: el estado guardado más las k operaciones cuya OP quedó entera, aplicadas a mano. El diario reescrito tiene k OP, cada una con su RES, sin repetidas. Una segunda apertura no cambia ni el estado ni el fichero. Sin pérdida, el estado es el del gemelo en memoria.
  - Corte dentro de la reescritura que limpia la línea cortada (C4) y corte a mitad del RES que `abrir` completa al recuperar (C5): la siguiente apertura recupera con la operación aplicada una sola vez.
  - Corte dentro del punto firmado de la noche del jueves (C6): tras anotar el PUNTO, tras guardar el estado y con media línea PUNTO. Se recupera el estado del gemelo y el punto se rehace.
  - Alterados tras los dos cortes (C3): un byte de una RES del medio; una OP falsificada completa con salto final, con firma inventada o firmada con otra clave; una OP del medio cambiada con su hash rehecho. Todos dan DI-02 sin tocar el fichero. Una OP falsificada sin salto final se toma por corte, se descarta y no se aplica.
  - La semana sigue hasta el final con todos los cortes. Las posiciones, el kill-switch, el rearme y la degradación quedan sin duplicar, y el diario firmado final es idéntico al gemelo e íntegro.
- **Límite conocido, no nuevo:** un recorte limpio del último par OP-RES se acepta sin aviso y esa operación se pierde. r02 lo informa como INFO. Lo documenta `diario.py` y está en la deuda (T-03: falta «el ancla monótona o la bóveda contra el truncado y el retroceso», Fase 3). Esa operación sí había vuelto al llamador.
- **Reloj detrás del estado (r03):**
  - RL-02 con 1 día, 1 h y 5,5 s de atraso, tanto con el intermediario de acuerdo con la máquina como con el intermediario en hora.
  - Con 5 s y 4 s, el instante es el del estado (el suelo), nunca uno anterior, y se opera a través del diario sin O-16.
  - `degradar_por_reloj` a través del diario firmado: las carteras en L1 con el instante del estado, anotado e íntegro al reabrir.
  - Rearmar sin corregir la hora: RL-01 y ningún instante. Con 6 s de atraso y rearmado: el instante del estado.
- **Respaldo del Orquestador:** los 42 métodos `@_seguro` del Orquestador llaman a `_ahora`, y un `RelojRetrocede` restaura todo el estado (O-16). Esto respalda H-04.

### Reproducción en la copia limpia

- **Copia:** un `git worktree` de `c306132` (develop) en el scratchpad, con las cuatro sondas copiadas. Quitado al terminar con `git worktree remove`.
- **Baterías:** las 59 `pruebas/pruebas_*.py` con `/home/claude/repo/.venv/bin/python -I -B`: **59 pasan, 0 fallan**.
- **Sondas:**
  - r02: «TODO FALLA CERRADO»;
  - r03: «FALLA CERRADO (CON HALLAZGOS)», que son H-04 y H-05;
  - r04: «LAS DOS PROPIEDADES SE CUMPLEN».
- **Semana:** dos ejecuciones idénticas byte a byte.
- **R04 y R06 con `--todas`:** contra las 58 baterías restantes, ninguna las caza. `pruebas_via_directa_t80.py` queda apartada porque ya falla en la copia parcial del marco, que solo lleva validador, pruebas, esquemas y LEEME; no toca el reloj.
- **Gates:** `tools/refs_vivas.py` y `tools/secrets_scan.py` en verde con este ticket. No ejecuté `./tools/check_all.sh` entero: la pieza no toca los bloques, y la QA no cambia código ni documentos rastreados.

### Veredicto

**NO APTO** · El producto falla cerrado en los dos huecos de GLM: un segundo corte en el diario firmado y un arranque con el reloj por detrás del estado. No hay hallazgos críticos ni altos. Pero la pieza V0.63 no cumple CA-1: la semana no ejercita el Reloj que dice ejercitar (H-01, media). Siete mutaciones del reloj que el Documento 0 y el LEEME dan por cubiertas pasan la semana y la dorada, y lo mismo pasa con las dos mutaciones de la propia batería (H-02 y H-03).

**Siguiente paso:** quien mantenga la batería corrige H-01 a H-03 en `pruebas/pruebas_semana.py`. Lo más barato es adoptar r02 y r03 como pasos de la semana, y la `Maquina` con `ahora()` y un desfase. Después se vuelve a pasar r01 (deben quedar cazadas R01 a R03, R05, R07 a R09, S01 y S02) y se abre la ronda r02 de esta QA. H-04 a H-07 son de producto o de las baterías de T-03. Si no se corrigen ahora, pasan a la deuda con su ID (T-84/H-0n). Los ficheros de V0.63_revision siguen sin rastrear en git: los añade quien haga el commit.
