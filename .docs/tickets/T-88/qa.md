# T-88 · QA independiente

## Ronda r01

- **Revisor:** subagente nuevo de Claude, sin contexto de la implementación (regla del operador del 12-11-2026). Opinión formada con el README del ticket y el código antes de leer `analisis-tecnico.md`.
- **Código revisado:** commit `7feb697` de `develop` (la ronda r02 de T-103, que va en el mismo commit, queda fuera de esta QA). Comparación con `7feb697^` en un worktree aparte.
- **Scripts:** `revisores/r01_comun.py` (utilidades), `r01_01` a `r01_05` y `r01_mutar.py` (motor de mutantes, también lo usa T-91). Todos aceptan `--ejecutor RUTA` para lanzarlos contra otra copia; se ejecutan con `.venv/bin/python -I`.

### Reproducción desde limpio

- Worktree limpio de `7feb697` con `PYTHONPATH` apuntando a sus tres ejecutores (el venv instala los bloques en modo editable desde la copia principal): `./tools/check_all.sh` completo **12/12** en 19 min. A **737** passed, A-Forex 68, B 176; ruff 2938 (cuota 2938), mypy A 109, FX 174, B 159; corpus, NFC, YAML, secretos y refs vivas en verde.
- `tests/test_t88_consumo.py`: 5 pruebas, pasan.
- Control con `7feb697^` (`r01_01 --ejecutor <worktree>/bloque_a/11_Ejecutor --rapido`): el fallo original se reproduce. Con los doce perfiles, el F5 da 4 variantes en V5 y 4 en V6 entre 1, 6 y 12 hilos.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r01_01`: con los doce perfiles, 1, 3, 6 y 12 hilos y 3 repeticiones, el `presupuesto` de F5 es idéntico en las 10 ejecuciones de V5 y en las 10 de V6, y también los cierres parciales. Es independiente incluso del número de hilos. `r01_05 R`: con reintentos (AG-03 con dos respuestas no conformes), mismo F5 con 1, 6 y 12 hilos en V5 y V6. `r01_05 K`: con la mitad de las respuestas en la caché de resultados (elegidas por clave, 17 y 10 aciertos), mismo F5 con 1, 6 y 12 hilos en V5 y V6 |
| CA-2 | sí | `r01_01`: V6 con doce perfiles, 29,2188 cargado frente a 29,2190 real. `r01_05`: con reintentos, con aciertos de caché (14,3448 frente a 14,3450) y con una caché de prompts que se pierde (parte P), el total sigue siendo el real. En V5 la diferencia es de 2,9588 UC, la de las llamadas posteriores a F5 (límite declarado); no cambia frente a la base |
| CA-3 | sí | `test_la_prima_solo_es_prudente…` y `r01_05 U`: 50 órdenes distintos de las mismas cargas dan el mismo resumen, `resumen()` repetido no cambia nada y el total tras liquidar es la lectura más la prima real. Prima «solo» de un primer intento con reintentos = la del prefijo, no una por intento (`r01_05 R`) |
| CA-4 | sí | Gate 12/12 desde limpio, cuotas sin subir (ruff baja de 2986 a 2938), A de 719 a 737 con las pruebas nuevas (de T-88, T-91 y T-103) |

### Mutantes (`r01_04_mutantes.py`, sobre otra copia)

Primero las pruebas del ticket y, si sobrevive, la suite entera (M1 a M3) o las suites de presupuesto e integración (`test_integracion`, `test_t65_qa_r01`, `test_t87_agentes`, `test_t92_revision`, `test_v5`, `test_t101_v6`; M4 a M11). Las copias se restauran con `git checkout` dentro del worktree.

| Mutante | Resultado |
| --- | --- |
| M1 vuelta atrás (cada llamada carga su coste real) | detectado (`test_dos_ejecuciones…[v5]`) |
| M2 `liquidar_primas` no hace nada | detectado (`test_v6_el_total_cargado…`) |
| M3 sin la liquidación tras la fase en paralelo | **sobrevive a la suite entera** |
| M4 prefijo sin dividir por los intentos | **sobrevive** (lo detecta `r01_05 R`: 52.322 frente a 26.161 tokens) |
| M5 primera llamada por agente y no por (bolsa, agente) | detectado |
| M6 sin primas «solo», lo real no va a la bolsa común | detectado |
| M7 prima sin descontar la lectura | detectado |
| M8 `resumen()` no liquida | sobrevive; en los ciclos probados es equivalente. Tras la liquidación intermedia, las primas «solo» que quedan son de agentes con un único usuario (COMUN y V6_GLOBAL), y ahí coinciden con la escritura real. Protege flujos futuros |
| M9 cada llamada paga la prima «solo» | **sobrevive** |
| M10 la prima «solo» es la escritura real de la llamada | detectado |
| M11 liquidación sin `sorted` | sobrevive; equivalente (cada bolsa se ajusta por separado) |

Todo lo que cambia lo que ve el control durante el ciclo (M3, M4 y M9) sobrevive: H-04.

### Ataques sin hallazgo

- Determinismo con más hilos (hasta 12) y más perfiles (los doce), V5 y V6: `r01_01`.
- Reintentos y aciertos de la caché de respuestas: `r01_05 R` y `K`.
- Selección y cierres con los presupuestos por defecto (PERIODICO N1 y N2, V5 y V6, doce tipos): iguales que la base (`r01_02`).
- Invariantes: no hay LLM en la contabilidad. Ningún número nuevo escrito a mano: la prima sale de `uc.factor_lectura_cache` y `uc.tokens_entrada_por_uc`. El estado persistido no cambia de forma. Nada de secretos ni datos personales. INC-T88-01 está en `docs/incidencias.md` como `[PROPUESTO]` y T-88 en la deuda técnica.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_03_prima_solo_ampliaciones.py --base <worktree de 7feb697^>/bloque_a/11_Ejecutor`, casos A y B (y `r01_02` para los mínimos por tipo) | **Esperado** (deuda técnica de T-88: «la selección y los pronósticos no cambian»; README: la regla solo cambia «los valores de `presupuesto` en F5»): el control de presupuesto se comporta como antes y solo cambia el reparto.<br>**Obtenido:**<br>– En V5 (el diseño por defecto), la prima «solo» de los prefijos compartidos (AG-10, AG-11, AG-12 y AG-14) suma unos 2,8 UC a cada tipo durante la fase en paralelo. En un ciclo N2 de doce tipos, el presupuesto mínimo que deja pasar todas las llamadas sube, por ejemplo, de 3,00 a 5,78 UC en CRI y de 4,59 a 7,37 en IDX (`r01_02`).<br>– Con los valores por defecto, en una PROFUNDIZACION N3 de los doce tipos (50 / 12 = 4,17 UC por tipo), 9 tipos cierran por presupuesto una fase (refutación o respuesta a objeciones) que la base no cerraba, y RF cierra la refutación en vez de la respuesta a objeciones. 7 tipos piden más ampliaciones AUT que la base (IDX, FON, INM, CRI, ALT y MON, de 0 a 2). **La selección (`top3_por_clase`) cambia**.<br>– Con un override justo por encima del mínimo de la base (CRI 3,054, RF 4,079, DIV 5,269, N2), cierra una fase y cambia la selección en los tres.<br>– Tras liquidar, F5 registra el cierre «presupuesto insuficiente» con un consumo final muy por debajo de lo asignado: FON 3,41 de 4,17 UC, CRI 2,65 de 3,05. La auditoría ve un cierre por presupuesto que el consumo no explica.<br>En V6 el efecto es pequeño (hasta +0,08 UC por tipo) y no cambia nada con los valores por defecto. Ni el README del ticket ni INC-T88-01 declaran esta consecuencia | Que el control no vea un coste que no va a existir. Por ejemplo, durante la fase, cargar cada prefijo compartido a partes iguales entre las bolsas del run que usan ese agente (se sabe de antemano: los tipos del ciclo), o a la bolsa común, y liquidar como ahora. Si se mantiene la regla, declararlo en INC-T88-01 y en la deuda («la prima "solo" puede cerrar fases y cambiar la selección con presupuestos ajustados»). Prueba: PROFUNDIZACION N3 de doce tipos en V5 sin cierres ni selección distinta de los que daría el coste real | abierto |
| H-02 | baja | `r01_05_reintentos_cache_y_unitarias.py U` | **Esperado** (README: «su parte de los tokens escritos de verdad»): cada bolsa paga una parte de los prefijos que usó.<br>**Obtenido:** la liquidación reparte el total de lo escrito en proporción al total de primas «solo», mezclando prefijos de agentes distintos. RV escribe un prefijo propio de 10.000 tokens y comparte otro de 5.000 con RF. RF acaba pagando 3.750 tokens de escritura, cuando su parte del compartido sería 2.500: paga parte del prompt propio de RV. Es determinista y conserva el total, pero no es la parte de RF | Liquidar por agente (o por prefijo): `_primas_solo` y `_primas_reales` con clave `(agente)` y reparto dentro de cada agente. Es igual de determinista. O dejarlo y escribir la convención exacta en INC-T88-01 | abierto |
| H-03 | baja | `r01_05_reintentos_cache_y_unitarias.py P` (cliente simulado que pierde la caché de prompts cada 7 llamadas, V6, 1 hilo) | **Esperado** (README del ticket: «nunca carga menos que la prima real de esa bolsa»; «Cómo falla cerrado: … la prima "solo", que es igual o mayor que la real»).<br>**Obtenido:** si la caché caduca o se pierde a mitad del ciclo, las siguientes llamadas de la bolsa vuelven a escribir, y la prima «solo» solo cuenta la primera. Durante la fase, todas las bolsas cargan menos de lo escrito: MP 14.591 frente a 31.104 tokens, RV 13.939 frente a 27.878, V6_GLOBAL 41.429 frente a 79.791. El total tras liquidar sí es el real. `analisis-tecnico.md` («Límites») lo reconoce para el TTL de la API, pero el README y INC-T88-01 dicen lo contrario | Corregir la afirmación del README y declarar el límite en INC-T88-01. O, si se quiere la prudencia siempre, cargar además durante la fase lo que la llamada escriba por encima del prefijo ya pagado por esa bolsa | abierto |
| H-04 | baja | `r01_04_mutantes.py <copia> --solo=M3,M4,M9` (y la tabla de mutantes) | **Esperado** (como en H-19 y H-29 de T-65: cada parte de la corrección con una prueba que falle sin ella).<br>**Obtenido:** las pruebas fijan el F5 final y el total, pero no lo que carga cada bolsa *durante* el ciclo, que es lo que decide cierres y ampliaciones (H-01). Sobreviven quitar la liquidación tras la fase en paralelo (M3, suite entera), no dividir el prefijo por los intentos (M4) y cobrar la prima «solo» en cada llamada (M9) | Una prueba que fije el consumo por bolsa antes y después de `liquidar_primas` en un ciclo con reintentos (por ejemplo, espiando `cargar_con_prima` como `r01_05 R`) y otra que fije el disponible de una bolsa al entrar en la respuesta a objeciones | abierto |

Observaciones sin hallazgo:
- Con la API real, el total escrito puede variar entre ejecuciones (dos hilos que piden a la vez un prefijo aún no guardado lo escriben los dos). La liquidación reparte ese total en proporción fija, así que el consumo por tipo en modo sombra seguirá cambiando entre ejecuciones lo que cambie el coste real. Es inherente y coherente con INC-T88-01 («el reparto es una convención contable»).
- En vivo, AG-14, AG-16 y AG-28 con búsqueda web suman el uso de las continuaciones `pause_turn` en un solo intento. `cacheados ÷ intentos` sobreestima entonces el prefijo y el control ve una prima mayor. Es prudente y la liquidación lo corrige, pero agrava H-01 en vivo.

### Veredicto

**APTO.** Los cuatro criterios se cumplen, con evidencia propia: el consumo por tipo es determinista con 1 a 12 hilos y los doce perfiles, en V5 y en V6, también con reintentos y con aciertos de la caché de respuestas; el total cargado es el real en V6; el gate da 12/12 desde limpio. No hay hallazgos críticos ni altos.

H-01 (media) es el más importante. La regla `[PROPUESTO]` arregla el registro, pero en la V5 endurece el control de presupuesto durante el ciclo con un coste que no existe (unos 2,8 UC por tipo). Con presupuestos ajustados, como una PROFUNDIZACION N3 de muchos tipos con los valores por defecto, cierra fases y cambia la selección. Conviene corregirlo antes del modo sombra o, si no, declararlo en INC-T88-01. H-01 a H-04 pasan a la deuda técnica con su ID si no se corrigen. El cierre del ticket (estado, deuda, diario y commit) queda para el coordinador: esta ronda solo escribe este archivo y los scripts de `revisores/`.

## Ronda r02

- **Revisor:** subagente nuevo de Claude, sin contexto de la implementación ni de la r01 (solo el plan, el código y los `qa.md`). Opinión formada con el README, el diff de `d1a5a1b` y el código antes de leer «Ronda r02» de `analisis-tecnico.md`.
- **Código revisado:** commit `d1a5a1b` de `develop` (la r01 se revisó en `7feb697`).
  - Comparación con `7feb697^` (antes de T-88) en un worktree aparte.
  - Otra sesión empezó a modificar el árbol principal durante esta QA (`motor/servicio.py`, T-106, desde las 22:41 UTC). Por eso las ejecuciones posteriores se lanzaron contra un worktree limpio de `d1a5a1b` (`--ejecutor`); las anteriores terminaron antes de esa hora.
  - Los worktrees se borraron al acabar. Durante la QA, `develop` avanzó hasta `5642ed0` (T-102 y T-106) sin tocar el código, las pruebas ni los documentos de T-88 y T-91.
- **Scripts nuevos** (todos aceptan `--ejecutor RUTA`; se ejecutan con `.venv/bin/python -I`):
  - `revisores/r02_01_determinismo_fase_y_total.py`: determinismo, también del consumo antes y después de la liquidación de la fase;
  - `r02_02_presupuestos_justos.py`: barrido de presupuestos frente a `7feb697^`;
  - `r02_03_grupos_y_mezcla.py`: CA-6;
  - `r02_04_mutantes.py`: mutantes de la r02, con el motor `r01_mutar.py`.

### Reproducción desde limpio

- Worktree limpio de `d1a5a1b` con `.venv` enlazado y `PYTHONPATH` apuntando a sus tres ejecutores: `./tools/check_all.sh` completo **12/12**. A **740**, A-Forex 68 y B 176; ruff 2938 de 2938; mypy A 109, FX 174 y B 159; corpus, NFC, YAML, secretos y refs vivas en verde.
- `tests/test_t88_consumo.py`: las 5 pruebas pasan. La r02 cambia dos de ellas y no añade ninguna.
- Scripts de la r01, otra vez:
  - `r01_01`: **6/6**. Con los doce perfiles, 1, 3, 6 y 12 hilos y 3 repeticiones, el mismo F5 en V5 y en V6. En V6, 29,2876 UC cargadas frente a 29,2877 reales. En V5 la diferencia es de 2,9589 UC, las llamadas posteriores a F5, como en la r01;
  - `r01_02 --base <7feb697^>`: **10/10**. Con los presupuestos por defecto, los mismos cierres y la misma selección que la base en V5 y V6, N1 y N2;
  - `r01_03 --base <7feb697^>`: **57/59**, como dice `analisis-tecnico.md`. Los dos fallos son de la PROFUNDIZACION N3 de la V5, en RV, y van en la otra dirección. La base cerraba la refutación de RV, que pagaba la caché compartida por llegar primero. HEAD no la cierra y pide dos ampliaciones AUT (autorizadas), así que la selección cambia. En el caso A, RF pide 3 → 0 ampliaciones;
  - `r01_05` y `r01_04` ya no sirven: espían o mutan `cargar_con_prima` con la firma antigua (`TypeError` en `r01_05`). Los sustituyen `r02_03` (partes U y P) y `r02_04`.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r02_01`: con los doce perfiles y 1, 3, 6 y 12 hilos × 3, son idénticos en las 10 ejecuciones de V5 y en las 10 de V6: el `presupuesto` de F5, los cierres y el consumo por tipo justo antes y justo después de la liquidación que sigue a la fase en paralelo. `r02_02`: con presupuestos justos (8 valores de δ por diseño), HEAD da el mismo presupuesto de F5, los mismos cierres y AUT (como conjunto) y la misma selección con 1, 6 y 12 hilos. Ver H-09 para el orden de los cierres |
| CA-2 | sí | `r02_01` y `r01_01`: en V6, 29,2876 UC cargadas frente a 29,2877 reales. Tras liquidar la fase, lo cargado es el coste real de sus llamadas: V5 47,0613 frente a 47,0612 y V6 19,0082 frente a 19,0083 |
| CA-3 | sí | `test_la_liquidacion_reparte_por_grupo_y_conserva_el_total`. Una segunda liquidación no cambia nada: el mutante P11 (no vaciar lo cargado) muere. El total tras liquidar es el real (arriba). La primera frase de CA-3 («cada bolsa carga su prima solo») la sustituye CA-5 |
| CA-4 | sí | Gate 12/12 desde limpio, sin subir cuotas, A 740 (737 + 3 de T-91). La r02 de T-88 no añade pruebas; ver H-08 |
| CA-5 | sí | `r02_02`, V5 N2 con los doce tipos a la vez en su mínimo de la base + δ (δ de −0,4 a +0,4 UC, 8 valores), un hilo: ningún tipo cierra una fase ni pide una AUT que la base no cerrase o pidiese. Hay 3 cierres menos (RF) y 3 tipos con una selección distinta, todos en la dirección declarada. Con los presupuestos por defecto, todo igual que la base (`r01_02`). En la V6 sí aparece un cierre nuevo, pero CA-5 solo habla de la V5: ver H-06 |
| CA-6 | **no** | `r02_03`: la liquidación mezcla prompts de analistas de tipos distintos (H-05) |

### Ataques

- **Lo que ve el control durante la fase** (`r02_01`). En V5, antes de liquidar, los doce tipos han cargado 43,586 UC de 47,061 reales: las escrituras de los agentes compartidos (unos 3,5 UC) no las ve ningún control durante la fase, y al liquidar cada tipo recibe de 0,21 a 0,36 UC. En V6 pasa lo contrario: antes de liquidar, 21,85 UC de 19,01 reales, porque cada analista carga entero el núcleo común (H-06).
- **Bolsas por encima de su límite tras liquidar** (`r02_02`, comprobación 4; el script la marca como FALLO por una diferencia de 0,0001 UC). En V5 hay los mismos casos que en la base: DER con δ de +0,05 a +0,2, por 0,3157 frente a 0,3158 UC; la diferencia es de redondeo y viene de estimaciones previas más bajas que el coste, anteriores a T-88. En V6 el exceso total baja de 3,32 UC (base: sobre todo RV, que pagaba la caché) a 2,21 UC, repartido entre más tipos: 18 casos frente a 19. No es un hallazgo de T-88, pero el control no ve esos excesos (ver H-07).
- **Agentes y grupos** (`r02_03 A`). En el ciclo V6 hay cinco grupos: AG-10, AG-11, AG-26, AG-28 y ANALISTAS. Ningún analista se carga a una bolsa que no sea la suya, y ningún agente compartido carga prima durante la fase.
- **Invariantes:**
  - no hay LLM en la contabilidad;
  - ningún número nuevo: la prima sale de `uc.factor_lectura_cache` y `uc.tokens_entrada_por_uc`;
  - el estado persistido no cambia de forma;
  - INC-T88-01 sigue como `[PROPUESTO]`;
  - nada de secretos ni datos personales;
  - documentación: ver H-07.

### Mutantes (`r02_04_mutantes.py`, sobre otra copia)

Primero `test_t88_consumo.py`. Si sobrevive, las suites de presupuesto e integración de la r01 (`test_integracion`, `test_t65_qa_r01`, `test_t87_agentes`, `test_t92_revision`, `test_v5`, `test_t101_v6`) y, después, los detectores propios (`r02_01 --rapido` y `r02_03 A`).

| Mutante | Resultado |
| --- | --- |
| P1 durante la fase nadie carga prima, tampoco el analista propio | **sobrevive a todo** (suites relacionadas, `r02_01` y `r02_03 A`) |
| P2 vuelta a la r01: todos cargan la prima «solo» durante la fase | **sobrevive a las suites relacionadas**; solo lo detecta `r02_03 A` |
| P3 vuelta a la r01: un único grupo para todos los prefijos | **sobrevive a todo** |
| P4 un grupo por agente (los analistas por separado) | detectado (`test_dos_ejecuciones…[v6]`) |
| P5 la liquidación no descuenta lo ya cargado | detectado (`test_v6_el_total_cargado…`) |
| P6 un grupo sin pesos no va a la bolsa común | detectado (`test_sin_pesos…`) |
| P7 sin la liquidación tras la fase en paralelo | **sobrevive a las suites relacionadas**; lo detecta `r02_01` |
| P8 prefijo sin dividir por los intentos (M4 de la r01) | **sobrevive a todo** (en la r01 lo detectaba `r01_05 R`, que ya no corre) |
| P9 cada llamada tiene prima «solo» (M9 de la r01) | **sobrevive a todo** |
| P10 el analista propio carga su escritura real en vez de la prima «solo» | **sobrevive a las suites relacionadas**; lo detecta `r02_01` |
| P11 la liquidación no vacía lo cargado (una segunda liquidación descuenta otra vez) | detectado (`test_v6_el_total_cargado…`) |
| P12 los pesos son los tokens reales y no la prima «solo» | detectado (`test_dos_ejecuciones…[v5]`) |
| P13 `resumen()` no liquida | detectado (`test_v6_el_total_cargado…`) |

Las dos correcciones de la r02 (P2 para H-01 y P3 para H-02) no tienen ninguna prueba del ticket que falle sin ellas (H-08).

### Estado de los hallazgos de la r01

| ID | Estado tras la r02 |
| --- | --- |
| H-01 (media) | corregido en la V5 (CA-5). En la V6 queda una parte: H-06 |
| H-02 (baja) | corregido entre agentes compartidos, que ya no se mezclan. Dentro del grupo ANALISTAS sigue la mezcla: H-05 |
| H-03 (baja) | `analisis-tecnico.md` lo reconoce («ya no se promete prudencia»), pero el README del ticket sigue prometiéndola: H-07 |
| H-04 (baja) | sigue abierto, ahora con más mutantes vivos: H-08 |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-05 | media | `r02_03_grupos_y_mezcla.py` (partes U, G y P; también con `--ejecutor <worktree de d1a5a1b>`) | **Esperado** (CA-6: «sin mezclar el prompt de un analista con otros tipos»; `analisis-tecnico.md`: «en la V5 cada uno escribe el suyo, que vuelve entero a su tipo»): cada tipo paga su propio prompt entero, y solo se reparte lo compartido de verdad (el núcleo V6 y los agentes compartidos).<br>**Obtenido:** los doce analistas forman un solo grupo, y lo escrito por todos se reparte en proporción a las primas «solo». Así un tipo paga parte del prompt de otro:<br>– U, a mano con la forma de la V6: RV y RF comparten un núcleo de 5.000 tokens; el kit de RV mide 10.000 y el de RF 1.000. RF paga 4.571 tokens, y le tocarían 2.428 (su kit más su parte del núcleo) o 3.500 (el núcleo a medias). Paga 2.143 tokens del kit de RV;<br>– G, ciclo V6 real con los doce tipos: núcleo de 4.695 tokens y kits de 6.783 (MON) a 9.244 (RV). Cada tipo paga o cobra kits ajenos: MON +0,0258 UC, CRI +0,0127, RV −0,0253 y ALT −0,0212; en total 0,157 UC mal repartidas por ciclo;<br>– P, V5 con una caché que se pierde cada 7 llamadas (seis tipos): el analista que vuelve a escribir su prompt no lo paga él. RF, DIV, IDX y FON reescriben el suyo y cobran de 0,41 a 0,47 UC cada uno; RV y MP, que no reescriben, pagan +0,92 y +0,85 UC de prompts ajenos. En la V5 el analista propio no comparte nada con otros tipos, así que la mezcla es entera | Separar en el grupo ANALISTAS lo que se comparte de lo que no: el kit (o, en la V5, el prompt entero) de cada analista en un grupo propio (`"ANALISTA:AG-03"`…), que paga su tipo, y en un grupo aparte solo el núcleo V6 (el primer punto de caché, cuyo tamaño se conoce por los bloques de `system`). Pruebas con U y P. Si se mantiene la regla, cambiar CA-6 y escribir la convención en INC-T88-01 | abierto |
| H-06 | baja | `r02_02_presupuestos_justos.py --base <worktree de 7feb697^>` (V6) y `r01_02` (bolsas en las que HEAD necesita más) | **Esperado** (`analisis-tecnico.md` y docstring de `Bloque._cargar`: el analista propio carga su prompt «como antes de T-88»).<br>**Obtenido:** en la V6, la prima «solo» del analista propio incluye el núcleo común, que antes de T-88 solo escribía el primer analista. Durante la fase, cada tipo carga el núcleo entero: 21,85 UC frente a 19,01 reales (`r02_01`). El mínimo que deja pasar todas las llamadas sube en 10 de los 12 tipos: RF 1,788 → 1,798, IDX 2,739 → 2,795, FON 1,877 → 1,953, INM 1,854 → 1,933 y CRI 1,796 → 1,874. Con presupuestos justos (δ = +0,4), INM cierra la respuesta a objeciones, que la base no cerraba, y cambia su selección. Es el efecto de H-01 de la r01 en la V6, más pequeño. CA-5 solo habla de la V5, pero el efecto no está declarado en INC-T88-01 ni en el README, y la afirmación «como antes de T-88» no es cierta en la V6 | Cargar durante la fase solo el kit del analista propio (lo que escribe aunque el núcleo ya esté guardado) y dejar el núcleo para la liquidación, como los agentes compartidos; va con H-05. O declararlo en INC-T88-01 («en la V6, cada tipo carga el núcleo entero durante la fase; puede cerrar fases con presupuestos justos») | abierto |
| H-07 | baja | `grep -n "prudente\|igual o mayor" .docs/tickets/T-88/README.md`; la fila T-88 de `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | **Esperado** (documentación al día; H-03 de la r01).<br>**Obtenido:**<br>– el «Diseño» del README sigue describiendo la regla de la r01: «cada bolsa paga … su prima solo … Es determinista y prudente: nunca carga menos que la prima real de esa bolsa», y «Cómo falla cerrado: … el control de presupuesto ve la prima solo, que es igual o mayor que la real»;<br>– la deuda técnica dice lo mismo: «Cada tipo paga su prima "como si fuera el único"».<br>Con la r02, en la V5, el control no ve durante la fase unos 3,5 UC de escrituras compartidas: 43,586 cargados frente a 47,061 reales en doce tipos, y de 0,21 a 0,36 UC por tipo. La afirmación de que falla cerrado ya no se cumple. Con los presupuestos probados, ningún tipo acaba por encima de su límite más que en la base (`r02_02`, comprobación 4), pero eso no lo garantiza ningún control | Reescribir «Diseño» y «Cómo falla cerrado» con la regla r02: durante la fase, lectura más la prima del analista propio; lo compartido se ve al liquidar; el control usa la estimación previa, que tampoco incluye escrituras. Actualizar la fila T-88 de la deuda. Si se quiere de verdad fallar cerrado, reservar durante la fase, en cada bolsa, una cota de su parte de lo compartido (por ejemplo, la prima «solo» del agente compartido entre el número de tipos del ciclo) y liquidar como ahora | abierto |
| H-08 | baja | `r02_04_mutantes.py <copia>` (tabla de arriba) | **Esperado** (H-04 de la r01; «nada cuenta como hecho sin tests»): las dos correcciones de la r02 con una prueba que falle sin ellas.<br>**Obtenido:** la r02 no añade pruebas de ciclo, y sobreviven a las suites relacionadas:<br>– P2: volver a la r01, es decir, cobrar la prima «solo» de los agentes compartidos durante la fase. Es lo que corrige H-01 (CA-5);<br>– P3: volver a un único grupo, lo que corrige H-02 (CA-6), porque la prueba unitaria pasa el grupo a mano;<br>– P1: que el analista propio no cargue nada durante la fase;<br>– P7, P8, P9 y P10.<br>Solo `r02_03 A` detecta P2, y solo `r02_01` detecta P7 y P10 | Una prueba de ciclo V5 que fije el consumo por tipo justo antes de la liquidación de la fase (espiando `liquidar_primas`, como `r02_01`): mata P1, P2, P7 y P9. Otra que fije el grupo que llega a `cargar_con_prima` para un analista y para un agente compartido (mata P3). El caso con reintentos de `r01_05 R`, adaptado a la firma nueva, mata P8 | abierto |
| H-09 | baja (anterior a T-88) | `r02_02_presupuestos_justos.py --base …` (línea «orden de `cierres_parciales`»); diagnóstico con 1, 6 y 12 hilos en V6 N2, δ = +0,1 | **Esperado** (objetivo del ticket: un registro de F5 que se reproduzca).<br>**Obtenido:** con presupuestos justos en la V6, `cierres_parciales` de F5 trae los mismos cierres pero en un orden que depende de los hilos, en los 8 valores de δ probados. Las AUT de HA también se escriben en el orden de llegada. El `presupuesto` y la selección sí son idénticos | Ordenar `Presupuesto.cierres` (por clase, fase y motivo) al registrar F5, y las AUT de la fase en paralelo, como ya se hace con las escrituras de F2. O llevarlo a la deuda con este ID | abierto |

### Veredicto

**NO APTO.** CA-6 no se cumple: H-05 (media). La liquidación sigue mezclando el prompt de un analista con otros tipos:
- en la V6, en todos los ciclos (0,157 UC mal repartidas por ciclo de doce tipos);
- en la V5, en cuanto un analista reescribe su prompt (hasta 0,92 UC por tipo con una caché que se pierde).

Por lo demás, la r02 cumple lo que pretendía:
- CA-5: en la V5 no se cierra ninguna fase ni se pide ninguna ampliación que la base no cerrase o pidiese, en un barrido de 8 presupuestos justos;
- CA-1 a CA-4: el consumo por tipo es determinista con 1 a 12 hilos, también antes de la liquidación y con presupuestos justos; el total cargado es el real; el gate da 12/12.

H-06 a H-09 son bajos. H-06 y H-07 conviene resolverlos con H-05; H-08 pide las pruebas que faltan.

Siguiente paso: `ri-implementar` para H-05 (y H-06 a H-08), o, si se mantiene la convención, cambiar CA-6 y declararla en INC-T88-01. Después, el revisor vuelve a ejecutar `r02_01` a `r02_04` en una ronda r03. Esta ronda solo escribe este archivo y los scripts `revisores/r02_*`: el estado del ticket queda para el coordinador.

## Ronda r03

- **Revisor:** subagente nuevo de Claude, sin contexto de la implementación ni de las rondas anteriores (solo el plan, el código y los `qa.md`). Opinión formada con el README, el diff de `0afab6f` y el código antes de leer «Ronda r03» de `analisis-tecnico.md`.
- **Código revisado:** commit `0afab6f` de `develop`, en worktrees limpios (HEAD, `d1a5a1b` de la r02 y `7feb697^` de antes de T-88) creados con `git worktree add` en una carpeta temporal y borrados al acabar. Los mutantes, sobre otra copia completa de `0afab6f` (con `02_System_prompts` y el Catálogo).
- **Scripts nuevos** (aceptan `--ejecutor RUTA`; se ejecutan con `.venv/bin/python -I`):
  - `revisores/r03_01_f5_consumo_y_claves.py`: claves del registro RUN de F5 frente a un control (`--control`) y `Bloque.estado()`;
  - `r03_02_grupos_v5_v6.py`: los grupos de prefijos que llegan de verdad a la liquidación, en V5 (también con una caché que se pierde) y en V6. Sustituye a la parte P de `r02_03`, que con la r03 pasa sin comprobar nada (filtra el grupo ANALISTAS, que en la V5 ya no existe);
  - `r03_03_mutantes.py`: mutantes de la r03 (R1 a R5), con el motor `r01_mutar.py`.

### Reproducción desde limpio

- Worktree limpio de `0afab6f` con `.venv` enlazado y `PYTHONPATH` apuntando a sus tres ejecutores: `./tools/check_all.sh` completo **12/12**. A **1283**, A-Forex 68 y B 176; ruff 2908 de 2908; mypy A 109, FX 174 y B 159; corpus, NFC, YAML, secretos y refs vivas en verde.
- `tests/test_t88_consumo.py`: 11 pruebas (5 + 6 de la r03), pasan.
- Scripts de las rondas anteriores, otra vez contra HEAD:
  - `r01_01`: **6/6**. V6: 29,3067 UC cargadas frente a 29,3069 reales; V5: 2,9588 UC de diferencia (las llamadas posteriores a F5, declarado);
  - `r01_02 --base <7feb697^>`: **10/10**;
  - `r01_03 --base <7feb697^>`: **57/59**, los mismos dos fallos de la r02 en la PROFUNDIZACION N3 de la V5, en la dirección declarada;
  - `r02_01`: **9/9**. Con 1, 3, 6 y 12 hilos × 3, el mismo F5, los mismos cierres y el mismo consumo por tipo antes y después de la liquidación de la fase, en V5 y en V6;
  - `r02_02 --base <7feb697^>`: 7/10, los mismos tres fallos que en la r02 (el exceso de 0,0001 UC de DER por redondeo en la V5, el cierre nuevo de INM con δ = +0,4 en la V6, ya declarado como H-06, y el reparto de los excesos de la V6). El orden de `cierres_parciales` es ahora el mismo con 1, 6 y 12 hilos en V5 y V6 (en la r02 cambiaba en la V6): H-09 corregido;
  - `r02_03`: 4/6. U y G siguen fallando: es la mezcla de kits en la V6, ahora declarada (H-12). En la V5, la mezcla de H-05 ha desaparecido (`r03_02`, abajo);
  - `r02_04 <copia>`: **mueren los 11 mutantes que se aplican** (P1, P2 y P5 a P13), todos con las pruebas del ticket; P3 y P4 ya no se aplican porque la línea del grupo cambió (los sustituyen R1 a R3).

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r02_01` (10 ejecuciones por diseño con 1 a 12 hilos) y `r02_02` (8 presupuestos justos por diseño, 1, 6 y 12 hilos): el mismo `presupuesto` de F5, los mismos cierres en el mismo orden, las mismas AUT y la misma selección |
| CA-2 | sí | `r01_01` y `r02_01`: en V6, 29,3067 UC cargadas frente a 29,3069 reales; tras liquidar la fase, V5 47,0613 frente a 47,0613 y V6 19,0082 frente a 19,0083 |
| CA-3 | sí | `test_la_liquidacion_reparte_por_grupo_y_conserva_el_total` y los mutantes P5, P11 y P13, que mueren |
| CA-4 | sí | Gate 12/12 desde limpio, sin subir cuotas; A sube (6 pruebas nuevas). El gate no ve H-10 |
| CA-5 | sí | `r02_02`, V5: ningún tipo cierra una fase ni pide una AUT que la base no cerrase o pidiese, en 8 presupuestos justos |
| CA-6 | **no, tal como está escrito** | V5, sí: `r03_02 V P` (cada analista es su propio grupo y en él solo pesa su tipo; con una caché que se pierde cada 7 llamadas, cada tipo paga exactamente las reescrituras de su analista, 0 tokens de diferencia). V6, no: `r02_03 U G` siguen mezclando kits (0,157 UC por ciclo de doce tipos; peor, MON +0,0258 UC). La excepción está declarada en INC-T88-01 y en `analisis-tecnico.md`, pero CA-6 no se ha reescrito (H-12) |

### Ataques

- **Determinismo y total** (`r02_01`, `r01_01`, arriba). La r03 no cambia la V6 y en la V5 solo cambia el grupo de los analistas: los resultados coinciden con la r02.
- **Presupuestos justos frente a `7feb697^`** (`r02_02`, V5 y V6): los mismos mínimos por tipo que en la r02 (V5: RV 6,352 → 4,487 y DIV 5,219 → 4,303, en la dirección de CA-5; V6: suben en 10 de 12 tipos, H-06 declarado).
- **Grupos de verdad** (`r03_02`): se guardan `_pesos` y `_reales` justo antes de cada liquidación.
  - V5, doce tipos y seis hilos: 17 grupos (cada analista y cada agente compartido), ninguno «ANALISTAS»; ningún analista se carga a una bolsa ajena;
  - V6: grupos AG-10, AG-11, AG-26, AG-28 y ANALISTAS, como se declara.
- **Registro de F5** (`r03_01`, contra un worktree de `d1a5a1b`): **el registro RUN ha perdido la clave `consumo`** en V5 y en V6 (H-10).
- **Invariantes:**
  - no hay LLM en la contabilidad;
  - ningún número nuevo;
  - INC-T88-01 sigue como `[PROPUESTO]`;
  - nada de secretos ni datos personales;
  - el estado persistido **sí cambia de forma**: F5 pierde `consumo` (H-10), en contra de «Estado persistido: no cambia de forma» del README;
  - documentación: ver H-11.

### Mutantes de la r03 (`r03_03_mutantes.py`, sobre otra copia)

Primero `test_t88_consumo.py`. Si sobrevive, las suites relacionadas (`test_integracion`, `test_t65_qa_r01`, `test_t87_agentes`, `test_t92_revision`, `test_v5`, `test_t101_v6`) y, después, `r03_02`.

| Mutante | Resultado |
| --- | --- |
| R1 vuelta a la r02 (H-05): en la V5 los analistas comparten el grupo ANALISTAS | **sobrevive a las suites relacionadas**; solo lo detecta `r03_02` |
| R2 en la V6 cada analista es su propio grupo | detectado (`test_dos_ejecuciones…[v6]`) |
| R3 un único grupo para todo | detectado (`test_r03_v5_cada_analista_paga_su_prompt…`) |
| R4 vuelta atrás de H-09: `cierres_parciales` en el orden de llegada | **sobrevive a todo** |
| R5 `cierres_parciales` ordenado solo por tipo | **sobrevive a todo** |

R1 sobrevive porque en `test_r03_v5_cada_analista_paga_su_prompt…` ningún analista vuelve a escribir su prompt: sin reescrituras, los pesos «solo» coinciden con lo escrito, y el grupo común reparte lo mismo que un grupo por analista. Las pruebas de la r03 no fijan la corrección de H-05 en la V5.

### Estado de los hallazgos de la r02

| ID | Estado tras la r03 |
| --- | --- |
| H-05 (media) | corregido en la V5 (`r03_02 V P`). En la V6 sigue la mezcla de kits, declarada en INC-T88-01; falta reescribir CA-6 (H-12) y una prueba que fije la corrección en la V5 (H-13) |
| H-06 (baja) | declarado (INC-T88-01, `analisis-tecnico.md` y README). Cerrado |
| H-07 (baja) | a medias: se añade una línea nueva al «Diseño», pero el resto sigue igual (H-11) |
| H-08 (baja) | corregido: los once mutantes P que se aplican mueren con las pruebas del ticket. Aparecen R1, R4 y R5 sin prueba (H-13) |
| H-09 (baja) | corregido en la parte de `cierres_parciales` (`r02_02`: el mismo orden con 1, 6 y 12 hilos). Las AUT de HA siguen en orden de llegada, declarado en `analisis-tecnico.md`. Pero el cambio borra `consumo` de F5 (H-10) |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-10 | **alta** | `r03_01_f5_consumo_y_claves.py --control <worktree de d1a5a1b>/bloque_a/11_Ejecutor` (0/6); `grep -n '# H-09 "consumo"' bloque_a/11_Ejecutor/bloque_a/orquestacion.py` (línea 1812) | **Esperado:** el registro RUN de F5 conserva todas sus claves. Documento 0 del Bloque A, F5: «presupuesto **y consumo**», y 10.3: «El consumo real se registra en F5 y alimenta la calibración de presupuestos del Evaluador». También el README del ticket: «Estado persistido: no cambia de forma».<br>**Obtenido:** la corrección de H-09 puso el comentario `# H-09` en medio de la línea, delante de `"consumo": {k: cons[k] …},`, así que esa entrada quedó comentada. En V5 y V6, el RUN de F5 ya no lleva `consumo`; `d1a5a1b` sí lo llevaba. Además, `Bloque.estado()["ultimos_runs"][*]["uc"]` (orden `bloque-a estado`) sale `None`. Ninguna prueba lo detecta: el gate da 12/12 y A pasa entera. Es justo el registro de consumo que T-88 quiere hacer reproducible | Sacar el comentario de la línea (al final o en una línea propia) para que vuelva `"consumo"`. Añadir una prueba que compruebe las claves del RUN de F5 (al menos `presupuesto`, `cierres_parciales` y `consumo`, con su `uc`) y que `estado()` dé el `uc` del último run | abierto |
| H-11 | baja | `sed -n 25,31p .docs/tickets/T-88/README.md`; fila T-88 (línea 137) de `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | **Esperado** (H-07 de la r02; `analisis-tecnico.md`, r03: «H-07: el README ya no promete prudencia en la V5»).<br>**Obtenido:**<br>– el punto «Regla» del README sigue diciendo que, «durante el ciclo, cada bolsa paga la lectura de lo cacheado más su prima solo», y que «es determinista y prudente: nunca carga menos que la prima real de esa bolsa». Contradice la línea nueva que tiene debajo, «Qué ve el control durante la fase»;<br>– esa línea nueva dice «como antes de T-88», y en la V6 no es así (H-06): cada analista carga ahora el núcleo entero;<br>– la fila T-88 de la deuda sigue diciendo «Cada tipo paga su prima "como si fuera el único"» | Reescribir el punto «Regla» con la regla r02/r03: durante la fase, la lectura más la prima del analista propio; al liquidar, lo escrito por los agentes compartidos (y, en la V6, el núcleo y los kits) por grupos. En la línea nueva, decir «en la V5, como antes de T-88». Actualizar la fila de la deuda | abierto |
| H-12 | baja | `r02_03_grupos_y_mezcla.py U G` (4/6); README, CA-6 | **Esperado** (r02: «si se mantiene la regla, cambiar CA-6 y escribir la convención en INC-T88-01»).<br>**Obtenido:** la convención está en INC-T88-01 y en `analisis-tecnico.md` (hasta unos 0,03 UC por tipo; medido: MON +0,0258 UC, 0,157 UC por ciclo de doce tipos). Pero CA-6 sigue diciendo «sin mezclar el prompt de un analista con otros tipos», y en la V6 no se cumple | Reescribir CA-6: «en la V5, cada analista es su propio grupo; en la V6, los analistas comparten el grupo del núcleo y los kits se reparten con él (INC-T88-01)» | abierto |
| H-13 | baja | `r03_03_mutantes.py <copia> --suite=…` (tabla de arriba) | **Esperado** («nada cuenta como hecho sin tests»): las dos correcciones de la r03 con una prueba que falle sin ellas.<br>**Obtenido:** sobreviven a las suites relacionadas:<br>– R1: volver al grupo común en la V5, que es lo que corrige H-05. `test_r03_v5_…` no lo distingue porque ningún analista reescribe su prompt;<br>– R4 y R5: deshacer o debilitar el orden de `cierres_parciales` (H-09) | En `test_r03_v5_…`, una segunda llamada de AG-04 en RF con escritura real (reescritura del prompt) y comprobar que RV no paga nada de ella. Una prueba que meta cierres en otro orden en `Presupuesto.cierres` y compruebe el orden en F5 (va con la prueba de claves de H-10) | abierto |

### Veredicto

**NO APTO.** H-10 (alta): la r03 borra `consumo` del registro RUN de F5 al comentar por error esa entrada. Es el consumo real que el Documento 0 manda registrar en F5, y ninguna prueba lo detecta. Además, CA-6 no se cumple tal como está escrito en la V6 (H-12, una excepción declarada que falta llevar al criterio).

Lo que la r03 pretendía sí se cumple:
- H-05 corregido en la V5: cada tipo paga exactamente lo que escribe su analista, también con una caché que se pierde;
- H-06 declarado;
- H-08 corregido: los once mutantes P que se aplican mueren con las pruebas del ticket;
- H-09 corregido: los cierres salen en el mismo orden con cualquier número de hilos;
- CA-1 a CA-5 se cumplen.

Siguiente paso: `ri-implementar` para H-10, con su prueba, y para H-11 a H-13, que son pequeños. Después, el revisor vuelve a ejecutar `r03_01` a `r03_03` (y `r02_01`, `r02_02` y `r02_04`) en una ronda r04. Esta ronda solo escribe este archivo y los scripts `revisores/r03_*`: el estado del ticket queda para el coordinador.
