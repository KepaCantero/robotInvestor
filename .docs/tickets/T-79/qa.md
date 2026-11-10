# T-79 · QA independiente

- **Revisor:** un revisor nuevo, sin contexto de la implementación (subagente Claude). Formé mi opinión con el plan, las directrices del kit 2, el Documento 0 y el diff antes de mirar `analisis-tecnico.md` y `pruebas.md`. Los dos resultaron ser la plantilla vacía (H-02).
- **Ronda:** r01 · 2026-11-10 · commit revisado `250ddb7` (rama `develop`); base anterior del marco `df6a0da` (V0.53).

## Ronda r01

### Reproducción desde limpio

- **Clon limpio:** `git clone /home/claude/repo` en el scratchpad y `git checkout 250ddb7`. El código de la V0.53 lo saqué con `git archive df6a0da sistema_global/marco_comun_c`, para las pruebas de migración.
- **Baterías del marco:** ejecuté cada `pruebas/ejecutar_pruebas.py` y `pruebas/pruebas_*.py` con `/home/claude/repo/.venv/bin/python -I` y un plazo de 400 s cada una.
  - Resultado: **56 de 56** con «TODAS LAS PRUEBAS PASAN».
  - La más lenta es `pruebas_robustez_validadores.py`, con 18 s. `pruebas_migraciones_t03.py` tarda 1 s.
- **`.docs/scripts/pruebas_marco.sh` en el clon:** «Marco común de C: 56 pasan, 0 fallan», sin avisos de baterías que falten en el LEEME.
- **Gate `./tools/check_all.sh` en el clon:** con el `.venv` enlazado temporalmente y `RUFF_CACHE_DIR` y `MYPY_CACHE_DIR` fuera del clon. Resultado: **12/12**.
  - corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas en verde.
  - ruff 3102 (cuota 3109); mypy A 123/123, FX 174/174 y B 159/159.
  - pytest: A 201, FX 68 y B 174.
- **Scripts de la pasada de coherencia:**
  - Los ocho `entrega_glm/V0.65/scripts/pc2_0*.py` dan «RESULTADO PC2-0n: FALLA», como declara la entrega.
  - `entrega_claude/V0.67/scripts/pc3_01_via_directa.py` da FALLA: `detectar()` devuelve O-01 por la vía. Comprobé en `validador/orquestador.py`, en `detectar()`, que el rechazo es por `via_entrada` y no por el actor ni por los identificadores.
- **Limpieza:** clon y extracción borrados. El repositorio principal sigue en `250ddb7`, sin cambios (`git status` vacío).

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · la V0.66 contiene las seis anteriores, sin pérdidas ni vueltas atrás | sí, con límites | Los ZIP no están en el repositorio, así que verifiqué lo que sí está. Los 107 ficheros del manifiesto SHA-256 de la V0.62 siguen en disco, y entre ese manifiesto y el de la V0.66 solo cambian `consola.py` y `reloj.py`, que son las piezas V0.63 y V0.64. Contra el manifiesto de la V0.66, en el disco de la V0.67 solo difieren los nueve ficheros que declara el Documento 0. `git diff --diff-filter=DR df6a0da 250ddb7` sobre el marco está vacío: no se borra ni se renombra nada. `esquemas_codigo.json` solo añade la entrada de la V0.67, sin líneas quitadas, y frente a la V0.53 solo difiere en `n_lineas_diario_ambar` y `VERSION_PARAMETROS` |
| CA-2 · 56 baterías en el repositorio y gate 12/12 | sí | Las salidas de la reproducción |
| CA-3 · cada corrección tiene una prueba que falla con la V0.66 | sí, para las correcciones de código | Script r01_regresiones_fallan_sin_correccion.py, en copias del marco. Al deshacer G-02 cae `r01_umbral_nan_inf_o_bool_es_rojo`. Al deshacer G-03 cae `pruebas_consola_sistema.py` (con KeyError en la comprobación del tope por defecto) y `parametros_versionados` de T-17. Sin MIG-005 caen `hay_camino_desde_V0_45_hasta_este_codigo` y `v067_esquema_actual_y_MIG005_sin_cambios`. G-01, G-04, G-05 y G-06 son documentales: G-04 no tiene una prueba que falle con la numeración de GLM, porque la batería del catálogo solo compara el catálogo consigo mismo |
| CA-4 · deuda de GLM sin choques, y lo pendiente de la pasada con su fila | sí, con H-01 | La deuda técnica tiene 84 filas `T-NN`, sin ningún número repetido. T-60 a T-68 son las del repositorio; T-69 a T-78 son las de GLM renumeradas; T-80 a T-84 son las nuevas. `catalogo_codigos.py`, su batería y `consola.py` citan T-70, T-71 y T-72 con el mismo sentido que la deuda. Todo lo que la tabla PC3 marca como pendiente tiene su fila, pero la tabla no recoge todos los requisitos de la Fase 1 que añaden las enmiendas 2 y 3 (H-01) |

### Correcciones de Claude, comprobadas

- **G-02 (`consola._diario`):** el tope se valida antes de leer el diario. Un `bool`, un valor que no sea `int` o un tope menor que 1 dan ROJO. Comprobé también los topes 10³⁰ y 1, y el borde real: con el tope igual a `_n`, VERDE; con `_n - 1`, ÁMBAR; después de `punto()`, VERDE.
- **G-03 (`parametros.py`):** `n_lineas_diario_ambar` vale 1000, marcado `[PROPUESTO]`, con `PAR-0.4.0`. `PARAMETROS` sigue siendo de solo lectura: intentar escribir en él da TypeError.
- **MIG-005:** la migración `_sin_cambios`, con `cambia` vacío, enlaza `ESQUEMA_V0_53` con `ESQUEMA_V0_67`. El esquema registrado se recalcula igual que el del código.
- **Un estado guardado por la V0.53 se carga y se migra bien.** Lo comprueba r01_migracion_v053_a_v067.py (80 comprobaciones en verde), con estados generados por el código real de la V0.53. Son cuatro estados (sencillo, con el kill-switch activo, con una cartera degradada y firmado), además de dos diarios.
  - Sin migrar, la carga da PE-08.
  - `migrar` aplica solo `["MIG-005"]`. Solo cambian `limites` (una entrada MIGRACION añadida al final), `ultimo_ahora` y `huella_config`. El kill-switch, los rearmes, las degradaciones, la configuración, los expedientes y las posiciones quedan iguales.
  - El estado migrado queda íntegro y se vuelve a cargar. Migrarlo otra vez no hace nada.
  - Un estado firmado no migra sin su clave ni con otra clave.
  - Un estado de la V0.53 tocado no migra: con la huella sin rehacer da PE-02; con la configuración tocada y la huella rehecha también se rechaza.
  - Un diario con operaciones después de su punto da MG-06 y no toca los ficheros. Con un punto previo, `migrar_ficheros` lo deja abrible y conserva lo operado.
- **MIG-005 respeta `PROHIBIDAS`.** `PROHIBIDAS` es idéntica a la de la V0.53. Probé registros hostiles entre la V0.53 y la V0.67 que tocan `kill`, `cfg.nivel_autonomia`, el límite de pérdida o `rearmes`, declarándolo o sin declararlo, y uno que borra `expedientes` sin declararlo: todos dan MG-04.
- **Pruebas antiguas que cambian:** `pruebas_comparador_t17.py` solo actualiza el PAR esperado. `pruebas_integracion_v053.py` conserva todo lo que comprobaba sobre la V0.53 y MIG-004, alarga las cadenas esperadas con MIG-005 y añade `v067_esquema_actual_y_MIG005_sin_cambios`. Ninguna comprobación se debilita, aunque quedan dos nombres desfasados (H-10).

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | r01_pc3_cobertura.py, más el cotejo con la tabla «Reparto por fases de la enmienda 2» del §14 y con el §15 de la Constitución V0.6 | **Esperado:** que el §5 del Documento 0 recorra todo lo que la Fase 1 gana con las enmiendas 2 y 3 (G-06). **Obtenido:** faltan, sin fila ni clasificación: (a) «bases de datos del mundo para divisas y las del propio robot» (Fase 1 del reparto; D-38 y cambio 34); (b) «prueba de instrucciones a pequeña escala» por código de SC-4 (Fase 1 del reparto), que PC3-04 no menciona; (c) D-42 y cambio 38, ratificados el 8-11, después de la V0.4: núcleo y perfiles desde el primer día y valores `[PROPUESTO]` en simulado; deja además sin revisar la fila 14 de la V0.65, «FUERA DE FASE 1»; (d) D-34, segunda mitad, «los límites duros de F y el kill-switch no los fija un modelo», que es un invariante vigente y no cabe en «FUERA DE FASE 1» como lo deja PC3-10; (e) D-47 y cambio 42, del que PC3-08 solo cubre las migraciones, sin «nada personal en el repositorio» ni «copias sin datos compartidos»; (f) D-37 (cambio 33) y D-40 (cambio 36: historial exportable), sin fase asignada en la tabla. El adaptador de A y B a CT-G sí lo cubre la fila 30 de la V0.65 | Añadir las filas PC3-12 en adelante, con su estado y su deuda (o «—» si cumple), y revisar la fila 14 de la V0.65 a la luz de D-42 | abierto |
| H-02 | media | Abrir `.docs/tickets/T-79/pruebas.md` y `.docs/tickets/T-79/analisis-tecnico.md` | **Esperado:** las salidas de `ri-implementar` (paso 6) y de `ri-probar` (casilla «`pruebas.md` escrito»), como en T-60 a T-66. **Obtenido:** las dos son la plantilla sin rellenar («…», «<Causa raíz…>»). El contenido está repartido por el Documento 0 | Rellenarlas antes de cerrar: suites antes y después, CA→prueba, las regresiones con la prueba de que fallan sin su corrección (las de CA-3 sirven) y el gate | abierto |
| H-03 | baja | r01_panel_otros_caminos.py, apartado 1: `o.degradadas` a `None`, `[]`, `0`, `""` o `set()`; también un estado guardado sin firma con `degradadas=None` y la huella rehecha, que `cargar` acepta | **Esperado:** ROJO, como hacen `_kill` con `o.kill` y G-02 con el tope; el docstring dice «lo que falle es ROJO». **Obtenido:** «autonomia» y el panel entero en VERDE («autonomía plena»), mientras `o.nivel()` lanza TypeError con `None`, e «integridad» también sale VERDE. Contradice el «único fallo es G-02» de G-05 | En `_autonomia`, exigir `isinstance(o.degradadas, dict)` y, si no lo es, ROJO; regresión con los cinco valores. Valorar que `integridad()` o `montar` comprueben el tipo | abierto |
| H-04 | baja | r01_panel_otros_caminos.py, apartado 2: `r.bloqueo = "RL-01 escrito a mano"`; o un bloqueo válido con `r.incidentes = None` | **Esperado:** `Reloj.estado()` dice que el reloj está bloqueado; su docstring promete que «la foto nunca es más optimista que el reloj». **Obtenido:** la rama de respaldo devuelve `bloqueo: None`. El panel no se engaña, porque lee `reloj.bloqueo` antes, pero otro consumidor de `estado()` sí | En el `except` exterior, conservar un bloqueo no nulo (por ejemplo `{"codigo": "?", "motivo": repr(...)}`), o calcular `bloqueo` antes y fuera del `try` de `incidentes` |  abierto |
| H-05 | baja | r01_panel_otros_caminos.py, apartado 6: abrir un Diario, operar con `d.orquestador.detectar(...)` (por fuera del diario) y pintar el panel con `diario=d` | **Esperado:** no VERDE, porque la siguiente operación del diario dará DI-06. **Obtenido:** VERDE «diario operativo (1 línea(s)…)», y la siguiente operación devuelve DI-06 | Dentro de T-72 (método público de solo lectura del diario), comparar `_huella_viva(o)` con `_huella` y la identidad del fichero sin mutar nada, y pintar ROJO si difieren |  abierto |
| H-06 | baja (anterior a la V0.64, viene de T-03) | r01_panel_otros_caminos.py, apartado 4: `r.max_sin_contraste_s = float("nan")` después de construir el reloj, y diez días sin contraste | **Esperado:** pedir otro contraste. **Obtenido:** `ahora()` sigue dando instantes y el panel pinta VERDE «contrastado hace 864000 s». El constructor valida la tolerancia, pero el atributo es público | Comparar con `not (s <= tope)` en `ahora()` y en `_reloj`, o hacer las tolerancias de solo lectura | abierto, a la deuda |
| H-07 | baja | r01_leeme_frente_al_disco.py: ejecuta cada batería y compara sus comprobaciones con las que cita el LEEME | **Esperado:** las cifras del LEEME coinciden con el disco. **Obtenido:** la fila de la tabla de `pruebas_consola_sistema.py` dice 42 y se ejecutan 44 (el punto «Comprobado» sí dice 44). Esto es de esta versión. Hay además siete desfases heredados de la V0.53, que ya estaban en `df6a0da`: `pruebas_cortacircuito_t40.py` 27/29, `pruebas_diario_t03.py` 56/57, `pruebas_extremo.py` 42/44, `pruebas_libres_t33.py` 37/39, `pruebas_manual_t44.py` 47/52, `pruebas_migraciones_t03.py` 94/96 y `pruebas_propuesta.py` 73/74. La lista de «Cómo se ejecuta» sí coincide con el disco: 56 de 56 | Corregir la fila de la tabla a 44 y, de paso, los siete heredados. El script puede ir a `.docs/scripts/` como comprobación repetible | abierto |
| H-08 | baja | `git show df6a0da:sistema_global/marco_comun_c/LEEME.md`, `git show a6ceb76:…` y `git show 250ddb7:…`, buscando `python3 pruebas/pruebas_reduccion_t43.py` | **Esperado:** G-01 dice que la lista «perdió en la V0.60 dos baterías que sí estaban en la V0.53» y que la V0.67 las devuelve. **Obtenido:** ya faltaban en la V0.53 del repositorio (`df6a0da`), así que GLM partió de una lista que ya no las tenía. Las devolvió `a6ceb76` (T-60), antes de este ticket. El commit `250ddb7` no las añade | Corregir G-01 en el Documento 0 y la frase de cabecera de la V0.67 en el LEEME | abierto |
| H-09 | baja | `ls sistema_global/marco_comun_c` | **Esperado:** las sondas de los revisores de GLM con las demás, en `entrega_glm/revisores/` o en `entrega_glm/V0.6x/`, como las de la V0.66. **Obtenido:** siete scripts sueltos en la raíz del marco (`sondas_revisor_v060.py`, `_v061`, `_v062` y `hallazgo_1…4_revision_v060_*.py`) que el LEEME no indexa. Se ejecutan y cierran | Moverlos a `entrega_glm/revisores/` y ajustar las citas de `entrega_glm/V0.60/` y `V0.61/`, o dejar constancia en el LEEME | abierto |
| H-10 | baja | `pruebas/pruebas_integracion_v053.py` | **Esperado:** cada nombre dice lo que comprueba. **Obtenido:** `esquema_V0_53_registrado_y_es_el_del_codigo` ya no comprueba que sea el del código (lo hace la comprobación nueva), y `desde_V0_50_la_cadena_es_MIG003_y_MIG004` ahora también exige MIG-005. No debilita nada | Renombrar a `esquema_V0_53_registrado_y_MIG004_en_la_cadena` y `desde_V0_50_la_cadena_es_MIG003_MIG004_y_MIG005` | abierto |

Los scripts de ataque de esta ronda van en `revisores/` dentro de este ticket.

### Sin hallazgo en lo comprobado

- **V-15 (`validar_sobre.py`):**
  - Sin permiso, o con `False`, `1`, `1.0`, `"true"`, `"True"`, `"1"`, `b"1"`, `[True]`, `{"x": 1}`, NaN, infinito, una subclase de `int` o `numpy.bool_(True)`, se rechaza con V-15, tanto con valor 5 como con `NO_ESTIMABLE`. Solo `True` habilita.
  - No muta el sobre y es determinista.
  - Es coherente con `mandato_ok` (`is True`) y con `CONFIG_OBLIGATORIA`, que exige un `bool`.
  - Con el permiso en `True`, los valores 0, -1, NaN, infinito, texto, `bool`, `None` y 0,5 se rechazan. 1e308 pasa el sobre, pero eso es anterior a la V0.60 y lo topan F (`apalancamiento_max` ≤ 100) y SC-1 (≤ 10).
- **`catalogo_codigos.py` y su batería** (r01_v15_y_catalogo.py), en copias del marco:
  - la batería falla con un código nuevo sin catalogar;
  - falla con un código catalogado que no existe;
  - falla con el mismo código en otro módulo;
  - falla si al LEEME le falta la línea del prefijo RL.
  - La batería no es vacía. Las 282 entradas son los 281 pares que cita el LEEME más E-06, retirado con su motivo.
- **`Reloj.estado()` y el panel**, por caminos que no repiten la sonda de Claude ni la batería:
  - el panel es determinista con reloj y diario;
  - no muta el reloj (ni el suelo, ni la última lectura, ni los incidentes);
  - no muta el diario ni escribe en sus ficheros (mismo SHA-256 antes y después);
  - el panel sobre el Diario, que actúa como proxy, es igual al panel sobre su Orquestador;
  - con un monótono que retrocede no da VERDE (da ÁMBAR, y el `ahora()` siguiente bloquea con RL-01);
  - una cartera inventada en `degradadas` da ROJO;
  - tras migrar desde la V0.52, la línea de migración dice «MIG-004, MIG-005», y una lista de IDs rara da ROJO.
- **Invariantes:**
  - **Falla cerrado:** se cumple en todo lo revisado, salvo H-03 a H-06.
  - **Números:** el único número nuevo de producto (1000) está en `parametros.py` con `[PROPUESTO]`. Las comparaciones `tope < 1` y `n < 1` son estructurales. Según D-45, el parámetro nuevo debería llegar con su justificación y su pregunta del cuestionario; queda cubierto por la fila general T-83, pero convendría citarlo en ella.
  - **Determinismo:** r01_determinismo.py ejecuta dos veces ocho baterías (las cinco nuevas del kit 2, la del catálogo y las dos que cambian) y la salida es idéntica, quitando los segundos. Solo se usa `random.Random(semilla)`, sin reloj del sistema.
  - **Nada personal ni secreto** en lo que añade `250ddb7`: solo aparece una ruta del entorno de GLM, `/home/z/my-project/…`, en un `generar_pasada.py`, sin datos personales.
  - **Ningún camino hacia una orden sin F y G:** los cambios del kit no tocan el Orquestador, ni F, ni G.
  - **Sin LLM** en la ruta determinista.
- **Documentación:** `CLAUDE.md` y `sistema_global/README.md` citan la V0.67 y 56 suites. El briefing está al día en lo que cambia. La lista de ejecución del LEEME coincide con el disco: 56 de 56.

### Veredicto

**APTO.** Se cumplen los cuatro criterios de aceptación (CA-1 con la verificación limitada a los manifiestos y a git, porque los ZIP no están en el repositorio) y no queda abierto ningún hallazgo crítico ni alto. Las correcciones de código tienen una regresión que falla sin ellas. Un estado de la V0.53 migra a la V0.67 sin tocar nada prohibido, y MIG-005 rechaza los registros hostiles.

Antes de cerrar, H-02 (rellenar `pruebas.md` y `analisis-tecnico.md`) y H-07 en su parte nueva (el 42 de la tabla) se corrigen en minutos. H-01, y H-03 a H-10 si no se corrigen ahora, pasan a la deuda técnica con su ID. H-03, H-04 y H-05 encajan en T-72 o en una fila propia del panel; H-01, en la próxima versión de la pasada de coherencia.

### Scripts de la ronda r01

En la carpeta `revisores/` de este ticket, todos con `python3 -I` y con la ruta del marco como argumento (el uso está en la cabecera de cada uno):

- r01_leeme_frente_al_disco.py: la lista de ejecución y las comprobaciones citadas, frente al disco.
- r01_migracion_v053_a_v067.py: estados y diarios genuinos de la V0.53 migrados con la V0.67, y registros hostiles frente a `PROHIBIDAS`.
- r01_panel_otros_caminos.py: el panel de la V0.64 y `Reloj.estado()` (H-03 a H-06).
- r01_v15_y_catalogo.py: los permisos de V-15 y la no vacuidad de la batería del catálogo.
- r01_regresiones_fallan_sin_correccion.py: CA-3; deshace cada corrección en una copia.
- r01_determinismo.py: dos ejecuciones de las baterías nuevas y de las que cambian.
- r01_pc3_cobertura.py: cobertura de PC3 frente a D-28 a D-47, los cambios 26 a 42 y la Fase 1 del reparto (H-01).

## Correcciones tras la r01 (Claude)

| ID | Qué se hizo | Estado |
| --- | --- | --- |
| H-01 | Filas PC3-12 a PC3-17 en el Documento 0; la fila 14 de la V0.65 queda superada por D-42 (PC3-14) | corregido |
| H-02 | `pruebas.md` y `analisis-tecnico.md` escritos | corregido |
| H-03 | `_autonomia` da ROJO si `degradadas` no es un diccionario. Regresión `r02_degradadas_ilegible_es_rojo`, que falla con `250ddb7` | corregido |
| H-04 | `Reloj.estado()` conserva un bloqueo ilegible. Regresión `r02_estado_del_reloj_conserva_un_bloqueo_ilegible`, que falla con `250ddb7` | corregido |
| H-05 | A T-72 (un `Diario.estado()` que detecte el desfase) | a la deuda |
| H-06 | A T-85 | a la deuda |
| H-07 | Las ocho cifras, al día. La comprobación queda en `.docs/scripts/leeme_marco.py`: «SIN DIFERENCIAS (0)» | corregido |
| H-08 | G-01 corregido en el Documento 0 y en la cabecera del LEEME | corregido |
| H-09 | Se dejan en la raíz, porque las notas de la V0.60 y la V0.61 los citan allí, y el LEEME lo explica | aceptado, documentado |
| H-10 | Renombradas `esquema_V0_53_registrado_y_MIG004_en_la_cadena` y `desde_V0_50_la_cadena_es_MIG003_MIG004_y_MIG005` | corregido |

Con el veredicto APTO de la r01 y estas correcciones, el ticket queda CERRADO.
