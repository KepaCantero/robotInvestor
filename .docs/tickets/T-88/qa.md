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
