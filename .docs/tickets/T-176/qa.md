# T-176 · QA independiente

- **Revisor:** claude (subagente revisor nuevo, sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-17
- **Base revisada:** `wip/t176` `68f9b8e` sobre develop `51d68f5`, en un worktree aparte.

## Reproducción desde limpio

Por orden del operador, no se pasa la suite completa ni el gate. Se ejecuta lo siguiente:
- `pytest tests/test_t176_pb36_pb33.py`: 13 pasadas.
- Regresión dirigida, 173 pasadas: `test_t173.py`, `test_fase4_huecos.py` (las tres `test_pb33_…` de T-173), `test_t66_evaluacion.py`, `test_t66_propuestas.py` (sombra de HT-03) y `test_t129_modo_sombra.py`.
- `test_integracion.py`: 15 pasadas.
- Backtest mock del CLAUDE.md (2024-01-05 → 2024-03-29), con el código del worktree y con el de develop `51d68f5`:
  - `senales.csv`, `pronosticos.csv` y `metricas.json` salen idénticos byte a byte;
  - `consumo.csv` solo cambia en la columna de latencia;
  - F6 añade una `NOV-`.
- `ruff` sobre los archivos tocados: 0 errores (la cuota pasa de 2813 a 2812).
- Ataques propios en `revisores/r01_ataques.py` (17 comprobaciones): 11 sin hallazgo y 6 con hallazgo.

## Contraste con el corpus (por sección)

- **Bandas.** Anexo A, fila «Umbrales de elegibilidad»: «Calibrable (±5/trimestre; ±10 total)». Lo confirman 12.2 y la fila P-09 del esquema F10 V3.0. `evaluacion.bandas_f10.P-09` vale `{trimestral: 5, total: 10}` tal cual. P-05 es PENDIENTE_OPERADOR según el esquema F10 (fila P-05 y regla 2). La banda «propuesta» de ±1/±2 no se usa, y eso es correcto: es solo una propuesta para ratificar.
- **Números a mano.** No se ha encontrado ninguno en el código nuevo. `CLAVE_CONFIG_F10` son claves y `min_calibrar` sale de la configuración.
- **F10 sin aprobación.** Ninguna vía nueva escribe en F10:
  - dentro de banda queda un AJU- PROPUESTO;
  - fuera de banda o sin banda, una P3-;
  - comprobado con NaN, inf, bool, None, cadena, componente ausente o erróneo, P-30 y P-11.
- **Youden.** Caso a mano con E = 50, 55, 60, 65 y 70 (seis PRG de cada valor), con acierto en 55, 65 y 70. J vale 0; 0,5; 0,167; 0,667 y 0,333, así que el óptimo es 65 con J = 2/3, y coincide. Los NaN, los inf y las E booleanas no entran. Un `resultado_binario` True cuenta como 1, que es correcto.
- **`ajuste_en_sombra`.** Solo devuelve P-11, también un AJU- antiguo sin `parametro`. HT-03 no cambia (las pruebas de sombra pasan).
- **H5 y T-173.** Una P3- de P-31 elevada sigue ENVIADA en F6, así que `_p31_ya_movida` la sigue bloqueando. Las suites de T-173 pasan.
- **Novedades.** Solo lleva identificadores, estados, celdas, ámbitos y motivos de revocación: no copia el texto libre de las lecciones. Rehacerla la misma semana sin cambios da la misma sección (sin contar `run_id` ni `hasta_seq`). El cambio de año ISO (W53 → W01) sale bien.
- **Observación, sin hallazgo.** La regla 5 del esquema de F6 exige 30 resueltos «en la celda de nivel 1». El estimador del umbral E cuenta los resueltos globales, igual que RK, y lo declara INC-T176-01 `[PROPUESTO]`. Queda para que el operador lo ratifique.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_pb36_umbral_e_y_p05_…`: P3- `fuera de banda` 60 → 48, con F10 intacto y sin CFG- |
| CA-2 | sí | La misma prueba: P-05 `sin banda` y PENDIENTE_OPERADOR, con F10 intacto |
| CA-3 | **no del todo** | Las P3- de P-09 y P-05 se elevan una vez. Pero ahora que se elevan las P3- antiguas, la de P-11 se repite en la cola de HA en cada C5 (H-01) |
| CA-4 | sí (con H-03) | Las pruebas de límite 55, 65, 54 y 66 pasan; un parámetro no CALIBRABLE da ValueError; uno sin banda es tipo 3 |
| CA-5 | sí (con H-04) | Hay un RTR- por trimestre y, con 29 resueltos, no propone nada. Con dos C5 concurrentes salen dos RTR- |
| CA-6 | sí | Las pruebas de `test_pb33_novedades…` y de la semana siguiente pasan; el ataque 8 también |
| CA-7 | sí (lo declarado) | El mapa y las evidencias dicen Superada; ruff 2812. La suite y el gate no se han repetido |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_ataques.py` §5: `recalibrar` fuera de banda (con `banda_total` 0,02) dos C5 seguidos y `elevar_propuestas_tipo3` tras cada uno | Esperado: una P3- de P-11 en la cola de HA (regla 7 de F10, una vez por trimestre por parámetro). Obtenido: **dos** P3 EVAL PENDING_OPERATOR para el mismo objeto, una más cada semana. `recalibrar` nunca deduplicó su P3-; antes solo se acumulaban en F6, y desde T-176 llegan al operador | En `Evaluador.recalibrar`, antes de construir la P3-, devolver la P3- abierta si ya hay una: `abierta = next((a for a in f6 if a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA" and (a.get("parametro") == "P-11" or a.get("objeto") == "P-11 pesos de RK")), None)`; `if abierta: return abierta`. Añadir a la P3- nueva `"parametro": "P-11"` y `"trimestre": trimestre`. Prueba: dos `recalibrar` en semanas consecutivas dejan una P3- en F6 y una entrada P3 en HA | corregido (r02) |
| H-02 | baja | §5: la P3- de P-11 elevada | Esperado: `plan_reversion` (campo del esquema F6 4.7, que también va a HA). Obtenido: None en F6 y en HA | En la P3- de `recalibrar`, añadir `"plan_reversion": "Si se aprueba y aplica, un CFG- nuevo con revierte_a devuelve P-11 a los pesos vigentes (append-only, regla 6 de F10); si se rechaza, no hay nada que revertir"` (el mismo texto que usa `proponer_ajuste`). Comprobarlo en `test_p3_de_p11_tambien_se_eleva` | corregido (r02) |
| H-03 | baja | §4: `proponer_ajuste("P-09","E",48)` en 2026-T2 y `proponer_ajuste("P-09","E",47)` en 2026-T3, con la primera aún ENVIADA | Esperado: no repetir una propuesta abierta del mismo parámetro (como `_p31_ya_movida`: «nunca con una P3 de la celda pendiente»). Obtenido: dos P3- abiertas de P-09·E (48 y 47) en la cola del operador, que se contradicen | En `proponer_ajuste`, cambiar el bucle de duplicados por `for a in mismo: if (a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA") or (a.get("tipo_entrada") == "AJU" and a.get("estado") == "PROPUESTO" and a.get("a") == objetivo): return {...}`, es decir, una P3- abierta del mismo parámetro y componente bloquea **cualquier** objetivo. Registrar en el RTR- `resultado` = id de la abierta. Prueba: el caso de §4 deja una sola P3- y el segundo trimestre devuelve la primera | corregido (r02) |
| H-04 | baja | §6 y §10: dos o ocho instancias de `Evaluador` sobre la misma carpeta, lanzadas a la vez con una barrera | Esperado: una RTR- y una P3- (el almacén promete exclusión entre instancias y procesos). Obtenido: 2 RTR-, y 4 o 5 P3- distintas con ocho `proponer_ajuste` iguales. Comprobar y escribir no es atómico | Envolver en `with self.almacen._transaccion():` (reentrante, como `respuesta_final.py:231`) el cuerpo de `proponer_ajuste`, desde la lectura de F6 hasta el `escribir`; el de `revision_trimestral`, desde la comprobación de `rid` hasta su `escribir`; y el bucle de `Bloque.elevar_propuestas_tipo3`, desde `estado("F6")` hasta el último `escribir`. Prueba: §10 deja una sola P3- | corregido (r02) |
| H-05 | baja | Leer `pruebas_regresion` de cualquier P3-EVAL- nueva | Esperado: según la §6 del Plan V3.0, «Las propuestas de tipo 3 del Evaluador … citan en `pruebas_regresion` los identificadores de esta batería». Obtenido: `["PB-35","PB-36"]`, una lista escrita en el código que no es la batería | Llevar la batería a la configuración, `evaluacion.bateria_regresion: [PB-01, PB-02, PB-06, PB-08, PB-13, PB-18, PB-20, PB-21, PB-22, PB-23, PB-30, PB-31, PB-36, PB-37, PB-39, PB-49]` (§6 del plan, literal), y que `pruebas_regresion` sea esa batería más las específicas de R18 de la tabla de trazabilidad (PB-10, PB-34, PB-35, PB-50). Usarlo en `proponer_ajuste` y en `recalibrar`, quitar `PRUEBAS_REGRESION_AJUSTE` y ajustar la aserción de `test_pb36_…` | corregido (r02) |
| H-06 | baja | §7, segunda parte: una P3-EVAL- con `elevada_via` puesto a un msg_id que no existe y sin entrada en HA | Esperado: la P3- llega a la cola de HA, o se detecta. Obtenido: no se eleva nunca, y `verificar_integridad` no lo ve | En `elevar_propuestas_tipo3`, que estén pendientes las P3-EVAL- que no tengan `elevada_via` **o** que no estén en HA (`… and (not p.get("elevada_via") or p["id"] not in en_ha)`). Prueba: el caso de §7 deja la entrada en HA | corregido (r02) |

Los scripts de ataque están en `revisores/r01_ataques.py`. Se ejecuta con `python .docs/tickets/T-176/revisores/r01_ataques.py` desde la raíz, con el venv activo. Hoy da 11/17; tras las correcciones debe dar 17/17, salvo que H-06 se resuelva de otra forma.

## Veredicto

**NO APTO.**
- El criterio CA-3 no se cumple del todo: la elevación de las P3- antiguas mete en la cola del operador una P3- de P-11 duplicada en cada C5 (H-01, media).
- Hay cinco hallazgos bajos (H-02 a H-06). Por regla del operador se subsanan en este mismo ticket.
- El resto es correcto: el criterio de PB-36 y PB-33, las bandas del Anexo A, que F10 quede intacto, Youden, Novedades y que no haya regresiones en el mock ni en HT-03.
- Siguiente paso: `ri-implementar` corrige H-01 a H-06, cada uno con su prueba de regresión, y luego la QA r02 vuelve a ejecutar `r01_ataques.py`.

## Ronda r02

- **Revisor:** claude (el mismo revisor independiente de la r01) · 2026-11-18
- **Base:** `wip/t176` `ab27e93` (commits `13ba53e` y `ab27e93` sobre `68f9b8e`), en un worktree nuevo.

### Reproducción

- **Mis ataques.** `revisores/r01_ataques.py`, sin modificar (idéntico al de la r01), da **17/17**: los seis hallazgos quedan resueltos.
- **Regresión dirigida, 227 pasadas:**
  - `test_t176_pb36_pb33.py`, con las pruebas `test_r02_…`;
  - `test_t173.py`, `test_fase4_huecos.py`, `test_t66_evaluacion.py`, `test_t66_propuestas.py` y `test_t129_modo_sombra.py`;
  - `test_t65_qa_r01.py` y `test_integracion.py`.
- **Backtest mock** del CLAUDE.md, comparado con develop `51d68f5`. `senales.csv`, `pronosticos.csv` y `metricas.json` salen idénticos byte a byte, y `consumo.csv` también, quitando la columna de latencia.
- **ruff.** `evaluador.py` y `orquestacion.py` pasan de 11 errores (develop) a 10; la prueba nueva tiene 0, y la cuota sigue en 2812. Corrección de la r01: allí escribí «0 errores» por un filtro mal hecho; lo correcto es 11 → 10.
- **Ataques nuevos.** `revisores/r02_ataques.py` da 6/7.

### Correcciones

| Hallazgo r01 | Comprobación | Resultado |
| --- | --- | --- |
| H-01 | `recalibrar` devuelve la P3- abierta de P-11 (por `parametro` o por `objeto`, así que también cubre las antiguas). Con dos semanas seguidas queda una sola P3- en F6 y en HA (ataque r01 §5 y `test_r02_h01_…`) | corregido |
| H-02 | La P3- de P-11 lleva `plan_reversion`, `parametro` y `trimestre`, y HA recibe el mismo `plan_reversion` | corregido |
| H-03 | Una P3- ENVIADA del parámetro y componente bloquea cualquier objetivo, y el RTR- registra su id. P-09·A no queda bloqueado por la de P-09·E. Cuando el operador decide (RECHAZADA), E vuelve a proponer (r02 §2) | corregido |
| H-04 | `proponer_ajuste`, `revision_trimestral` y `elevar_propuestas_tipo3` van en `_transaccion()`, que es reentrante y usa `flock`; `leer` vuelve a cargar dentro del cerrojo. Con 8 hilos sale una sola P3-, y con 2 un solo RTR- | corregido, salvo `recalibrar` (H-07) |
| H-05 | `evaluacion.bateria_regresion` copia literalmente la §6 del plan (16 IDs), y `regresion_r18` copia literalmente la fila R18 de la §5 (PB-10, PB-34, PB-35, PB-36, PB-50). `pruebas_regresion_p3` devuelve las dos listas en orden y sin repetir: 20 IDs. Si la clave falta, se usa `por_defecto.yaml` (la convención de `parametro`); si vale nula, falla cerrado (r02 §3) | corregido |
| H-06 | Una P3- con `elevada_via` pero sin entrada en HA se eleva. Una que ya está en HA no genera otro CT-19 (r02 §4) | corregido |

**Efecto de H-03 sobre el AJU- dentro de banda.** Mientras haya una P3- abierta de P-09·E, tampoco sale un AJU- dentro de banda de ese parámetro y componente. Lo considero **correcto**, por cuatro razones:
- Es la misma regla que `_p31_ya_movida` de T-173: «nunca con una P3 de la celda pendiente».
- Aplica la regla más restrictiva (R23).
- Respeta la regla 7 de F10: un cambio por trimestre y parámetro.
- Evita que un ajuste automático se adelante a la decisión del operador sobre el mismo número, o la contradiga.

Su alcance es exacto: no bloquea otro componente (P-09·A) y se libera en cuanto el operador decide. El coste es que el ejecutor todavía no lee las decisiones del operador, así que P-09·E queda congelado hasta que esa decisión se anote en F6. Está documentado en INC-T176-01 (ronda r02) y en «No entra» del README.

### Hallazgos de la r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | baja | `r02_ataques.py` §1: seis instancias de `Evaluador` sobre la misma carpeta llaman a la vez a `recalibrar` con evidencia fuera de banda (`banda_total` 0,02) | Esperado: una P3- de P-11, porque la deduplicación de H-01 es «comprobar y escribir». Obtenido: 5 o 6 P3- distintas, que después se elevan todas a la cola de HA. La transacción de H-04 no cubre `recalibrar`, y la misma carrera puede duplicar el AJU- EN_SOMBRA | En `evaluador.py`, aplicar a `recalibrar` el mismo patrón que a `proponer_ajuste`: renombrar el cuerpo actual a `_recalibrar(self, as_of, run_id)` y dejar `def recalibrar(self, as_of, run_id=None): with self.almacen._transaccion(): return self._recalibrar(as_of, run_id)`. Prueba: `_a_la_vez(6, lambda i: evs[i].recalibrar("2026-01-02")) == []` y una sola P3- en F6. Lo verifiqué con un parche de prueba que envuelve `recalibrar` en `_transaccion()`: r02 da 7/7 | corregido (ronda de cierre) |

### Veredicto r02

**NO APTO**, pendiente de la ronda de cierre.
- Los seis hallazgos de la r01 están corregidos, y el efecto de H-03 es correcto.
- Queda un bajo, H-07. Por regla del operador se corrige en este mismo ticket.
- Para la ronda de cierre: aplicar la corrección exacta de H-07 con su prueba y volver a pasar `r01_ataques.py` (17/17) y `r02_ataques.py` (debe dar 7/7). Con eso, APTO sin más cambios.

## Ronda de cierre

- **Revisor:** claude (el mismo revisor independiente) · **Base:** `wip/t176` `d44adad`, sobre `ab27e93`, en un worktree nuevo.
- **H-07, corregido.** `recalibrar` envuelve a `_recalibrar` en `self.almacen._transaccion()`, el mismo patrón que `proponer_ajuste`, así que la lectura de F6 y la escritura de la P3- o del AJU- son atómicas. El diff solo toca eso, más la prueba nueva y el mutante M38.
- **Reproducción:**
  - `r02_ataques.py` da 7/7; la §1 deja una sola P3- con seis instancias concurrentes;
  - `r01_ataques.py` da 17/17;
  - `test_t176_pb36_pb33.py`, `test_t66_evaluacion.py`, `test_t65_qa_r01.py` y `test_t66_propuestas.py`: 124 pasadas;
  - ruff de `evaluador.py` sigue igual que en la r02: 3.
- `qa.md` y los scripts de `revisores/` coinciden con los de la r02.

| ID | Estado |
| --- | --- |
| H-01 a H-06 | corregido (r02) |
| H-07 | corregido (ronda de cierre) |

## Veredicto final

**APTO.** Se cumplen los criterios CA-1 a CA-7 y no queda ningún hallazgo abierto. PB-33 y PB-36 quedan «Superada».
