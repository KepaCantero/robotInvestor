# T-76 · QA independiente

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación · **Ronda:** r01 · 2026-11-10
- **Objeto:** commit `c306132` (marco común de C V0.71, cartera sombra pasiva). Su código coincide byte a byte con el que se revisó antes del commit. Solo difería la fila de la deuda, que el commit añade.

## Reproducción desde limpio

- **Copia limpia:** un `git worktree` de `c4d0c5a` con el cambio de T-76 aplicado en una carpeta temporal fuera del repo, y quitado al terminar.
  - `.docs/scripts/pruebas_marco.sh`: **60 pasan, 0 fallan**.
  - `pruebas/pruebas_sombra_t76.py`: 45 comprobaciones, todas pasan.
- **LEEME contra disco:** `.docs/scripts/leeme_marco.py` sobre `sistema_global/marco_comun_c`: «SIN DIFERENCIAS (0)», y `pruebas_sombra_t76.py` ejecuta las 45 que cita.
- **Gate:** `./tools/check_all.sh` sobre la copia limpia: **12 pasan, 0 fallan**.
- **Sondas del revisor:** tres scripts con prefijo r01 en la carpeta de QA de la V0.71, dentro de la entrega de Claude del marco. No están en git. Se ejecutan con `python3 -I` desde `sistema_global/marco_comun_c` e imprimen CONFIRMADO o NO en cada sonda:
  - las sondas del cálculo (S1 a S14);
  - las de fallo cerrado, actores e integridad (F1 a F13);
  - las del diario, la persistencia y MIG-008 (D1 a D5). D3 genera un estado genuino de V0.70 con el código de `c4d0c5a`, extraído con `git archive`.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1: la sombra nace el primer día con el mismo capital y replica cada aporte y retirada | sí, con reservas | Batería: `el_primer_dia_*`, `un_aporte_*`, `G_tambien_*`. F1 y F2: ninguna entrada rara ni ningún actor ajeno pasa, y ningún rechazo cambia el estado. Reservas: el capital no se contrasta con la cartera real (F13) y el precio de cada movimiento es libre (S11): H-07 |
| CA-2: cada mes, el robot neto de costes de análisis e impuestos frente a la sombra neta de su coste, en nominal y en real | **no** | El coste de la sombra está mal prorrateado y puede dar la vuelta al veredicto (S1, S1b, S2, S3): H-01. Con valores finitos enormes se guarda un NaN (S9): H-03 |
| CA-3: antes de 24 meses no se juzga; a los 24, O-41 si no la supera | **no** | El juicio «a los 24 meses» puede llegar con 23 meses y una hora (S4, S4b, S5): H-02. Si I no compara, no hay O-41 ni ningún otro aviso (F4, F5): H-04 |
| CA-4: los rechazos no cambian el estado y el registro tocado se detecta (O-13 con kill-switch) | sí, con reservas | F1, F10 y D4: los rechazos son atómicos y el estado tocado se detecta al cargar (O-13 con kill-switch). `integridad()` ve el toque en todos los casos de F7. Reservas: algunos toques se rechazan con O-00, O-01 u O-02 sin O-13 (F7): H-05. Vaciar o recortar el registro no se detecta (F8): H-09 |
| CA-5: guardar, cargar y MIG-008; 60 baterías; gate 12/12 | sí, con reservas | D1: el diario reproduce la sombra y sus O-41. D3: un estado genuino de V0.70 se rechaza sin migrar (PE-08), migra con `["MIG-008"]` con la sombra vacía y la integridad limpia, y después se inicia la sombra. 60/60 baterías. Gate 12/12 sobre la copia limpia. Reserva: tras una comparación con NaN no se guarda ni sigue el diario (D2): H-03 |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **media** | Sondas S1, S1b, S2 y S3. Inicio de 1 000 EUR. En el mes 23 se aportan 1 000 000 EUR y se compara al día siguiente con el robot en 1 000 000 EUR | **Esperado:** cada euro paga el coste de los días que estuvo en la sombra, unos 9,6 EUR en total. **Obtenido:** `estado_sombra` cobra `valor_bruto × 0,20 % × días desde el inicio / 365`, así que el aporte de la víspera paga más de dos años de coste: 4 130,84 EUR. La sombra queda en 996 869 EUR en vez de unos 1 000 990, y un robot que pierde 1 000 EUR frente a ella da **SUPERA**. Al revés, una retirada borra el coste ya devengado: pasa de 3 956,85 a 4,13 EUR (S2). Además, el coste se recalcula al precio de hoy: con el índice a 300 se cobra el triple que a 100 (S3). El veredicto se puede mover con movimientos legítimos | Devengar el coste por tramos, entre cada dos entradas, sobre las unidades de cada tramo, y acumularlo (o restarlo en unidades) en lugar de recalcularlo sobre el valor final. Añadir pruebas de regresión con un aporte y una retirada justo antes de comparar |
| H-02 | **media** | Sondas S4, S4b, S5 y S5b. Inicio el 2026-11-30T23:00Z, y cada mes se compara el día 1 a las 00:00 | **Esperado:** se juzga «tras 24 meses» (§9 punto 9, D-27), y un mes se compara cuando ya ha terminado. **Obtenido:** el mes 2026-12 se compara una hora después del inicio. **PROPONER_PASIVA** llega el 2028-11-01, con 23 meses y una hora. El mes del inicio sale del texto local (`ini["ahora"][:7]`), mientras que el «no del futuro» usa UTC. Con un inicio a las 2026-11-30T20:00-05:00, el mes 1 se compara en el mismo instante. El mismo instante escrito en +01:00 cambia el calendario | Usar UTC en todo. Exigir que el mes comparado esté cerrado (`ahora` en el mes siguiente o después). Juzgar por el tiempo transcurrido desde el inicio, o fijar y documentar la regla de meses naturales cerrados. Añadir pruebas en el borde (inicio a fin de mes, husos con desfase) |
| H-03 | **media** | Sondas S9, S9b y D2. `comparar_sombra("2026-12", 1000, 1e308, …)`, o un inicio con `iniciar_sombra(1e200, 1e-200, …)` | **Esperado:** un cálculo que no da números finitos se rechaza sin tocar nada. **Obtenido:** OK con `sombra_eur = NaN`, y el NaN se anota en el registro. Después `pe.volcar` lanza ValueError («valores que JSON no guarda tal cual: ['sombra']»). Con el diario, la operación siguiente y el punto de control dan DI-06: el estado ya no se puede guardar. Con una inflación diminuta (S9c) se aceptan valores reales de 1e308 y una inflación acumulada de −100 % | Antes de `_anota_sombra`, comprobar que todos los números de `est` y `cmp_` (y las unidades de `estado_sombra`) son finitos, y si no, rechazar con O-01. Valen el mismo control `pe._solo_json` o `math.isfinite` sobre el resultado |
| H-04 | **media** | Sondas F4 y F5. Se compara hasta el mes 23 y luego `barrer()` siete meses después | **Esperado:** «I compara cada mes» y «si tras 24 meses no la supera» (P17, §9 punto 9). O-41 no se puede silenciar. **Obtenido:** si I deja de comparar, no hay O-41 ni ningún aviso de comparación atrasada. `barrer()` solo da O-10. El mes 24 se puede comparar un año tarde, con los días de coste de entonces y el veredicto que convenga a la fecha elegida | Que `barrer()` avise (con su código y su prioridad) cuando falte la comparación de un mes ya cerrado pasado un plazo `[PROPUESTO]`, y en especial la del mes de juicio. Opcionalmente, rechazar o marcar las comparaciones muy tardías |
| H-05 | baja | Sonda F7. Se quita `ahora` del INICIO o `mes` de una comparación, o se cambia un `tipo`, y se llama a `comparar_sombra` o `iniciar_sombra` | **Esperado:** registro tocado, O-13 y kill-switch, como dice el documento. **Obtenido:** O-00, O-01 u O-02 sin kill-switch, porque las comprobaciones que leen el registro van antes de `_sombra_precheck()`. `integridad()` sí lo ve, y el siguiente punto de decisión lo para | Llamar a `_sombra_precheck()` antes de leer `self.sombra` en los tres métodos |
| H-06 | baja | Sonda S10. Inicio de 1 000 EUR a un precio de 1e12, es decir, 1e-9 unidades. Retirada de 2 000 EUR | **Esperado:** O-06. **Obtenido:** OK, y la sombra vale −1 000 EUR. La tolerancia es absoluta en unidades (`-1e-9`) | Usar una tolerancia relativa a las unidades compradas, o en euros |
| H-07 | baja | Sondas S7, S11, F9 y F13 | Lo que entra en la comparación no se contrasta con nada. G registra una retirada a 50 y un aporte a 100 en el mismo instante: neto 0 EUR, y la sombra pierde la mitad (S11). El índice de precios del inicio cambia en cada mes (S7). El capital inicial es cualquiera, sin relación con la cartera real (F13). `gasto_dia` no está encadenado ni validado, y un coste negativo inyectado en memoria regala un millón al robot sin que `integridad()` lo vea (F9). Parte está en el alcance de T-86, pero el documento no lo declara | Fijar el índice de precios del inicio en la entrada INICIO. Rechazar dos precios distintos en el mismo instante. Ignorar o rechazar costes negativos. Declarar en el Documento 0 y en la deuda (T-86) lo que queda por contrastar |
| H-08 | baja | Lectura de documentos y sondas S6, S8, S12 y F6 | Lo documentado no coincide del todo con lo que hace el código. `pruebas.md` y `analisis-tecnico.md` del ticket son todavía las plantillas: la fase 3 no tiene informe y el «gate 12/12» de CA-5 no tiene evidencia. El LEEME y CA-3 dicen «O-41 una vez», pero sale uno por mes mientras no la supere (F6, 3 avisos en los meses 24 a 26). No se dice que el veredicto en real es siempre el mismo que en nominal, porque los dos valores se dividen por el mismo factor (S8). Tampoco que la sombra no paga impuestos ni comisiones de compra (S12), ni que se cuentan los costes de todo el día del inicio, también los anteriores al inicio (S6, criterio conservador). No se anota qué índice de inflación se usa ni su fuente (Constitución, convenciones: «con el índice de inflación que fije el operador … y su fuente») | Rellenar `pruebas.md` y `analisis-tecnico.md`. Ajustar el LEEME, el Documento 0 y CA-3. Declarar las convenciones. Añadir el índice y la fuente a la comparación (o dejarlo en T-86) |
| H-09 | baja | Sonda F8 | Con el registro vaciado del todo, `sombra_ok()` da verdadero y se puede iniciar otra vez, con lo que el reloj de 24 meses vuelve a cero. Recortando la última comparación, el mes 24 se vuelve a comparar con otros números. Es el límite conocido de toda cadena sin ancla externa (el diario lo detecta con DI-06 y la persistencia con su huella), y lo mismo pasa con SC-5 | Dejarlo como límite declarado en la deuda: anclar la cabeza `SOMBRA` fuera, en la Fase 3 |

**Lo que se intentó y no se rompió:**
- Entradas con NaN, inf, bool, texto, None, listas, enteros enormes o complejos en los tres métodos: todas se rechazan sin cambiar el estado (F1).
- Actores ajenos, mal escritos o en minúsculas (F2).
- Comparar dos veces, hacia atrás o saltándose un mes (F3).
- O-41 sale uno por mes y sin duplicarse (F6).
- La retirada excesiva no cambia nada (F10).
- `informe_sombra()` devuelve copias (F11).
- Con la configuración rota, O-13 y kill-switch (F12).
- Vaciar la sombra exactamente y comparar después (S13).
- Bordes de año en `meses_entre` (S14).
- Reproducción determinista por el diario (D1).
- Carga de un estado con la sombra tocada: O-13 y kill-switch (D4).
- El esquema V0.71 registrado y actual (D5).
- O-41 en el catálogo y en `PRIORIDAD_AVISO` (ALTA).
- `PAR-0.7.0`, con los dos `[PROPUESTO]` en T-57.

## Veredicto

**NO APTO** · Hay cuatro hallazgos medios confirmados:
- H-01: el coste de la sombra está mal prorrateado y el veredicto se puede dar la vuelta con movimientos legítimos.
- H-02: el juicio de los 24 meses puede llegar con 23 meses y una hora, y el mes se compara antes de cerrarse.
- H-03: un cálculo no finito se anota y deja el estado sin poder guardarse ni seguir el diario.
- H-04: O-41 se silencia si I no compara, y nada avisa del retraso.

H-05 a H-09 son bajos: se corrigen en la misma ronda o pasan a la deuda con su ID. En la ronda r02 el revisor volverá a ejecutar sus sondas r01.

---

## Ronda r02

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación ni de la r01 · **Ronda:** r02 · 2026-11-10
- **Objeto:** la V0.73 del marco, revisada en el árbol de trabajo sobre `1a91d28`. Durante la revisión se hizo el commit `7b775cc`: su código de T-76 coincide con el revisado (sin diferencias en `sombra.py`, `orquestador.py` ni `migraciones.py` entre `7b775cc` y lo revisado). Lo revisado: `validador/sombra.py`, `validador/orquestador.py` (`iniciar_sombra`, `movimiento_sombra`, `comparar_sombra`, `comparacion_sombra_pendiente`, `_mes_utc`, el O-42 de `barrer`, `sombra_ok`), `validador/migraciones.py` (MIG-009), el catálogo (O-42) y los documentos del ticket. El árbol lleva también cambios a medias de T-65, T-75, T-83 y T-84, que no se revisan aquí.

### Reproducción

- `.docs/scripts/pruebas_marco.sh` sobre el árbol de trabajo: **61 pasan, 0 fallan** (con los cambios ajenos a medias incluidos).
- `pruebas/pruebas_sombra_t76.py`: 55 comprobaciones, todas pasan. `.docs/scripts/leeme_marco.py` sobre esa batería y `pruebas_integracion_v053.py`: «SIN DIFERENCIAS (0)».
- Gate `./tools/check_all.sh` sobre el árbol de trabajo (con los cambios ajenos a medias): **12 pasan, 0 fallan** (A 326, A-Forex 68, B 176). No se hizo copia limpia: el cambio de T-76 está sin commit y mezclado en los mismos ficheros con el de T-75.
- **Sondas r01:** ya no corren tal cual, y es lo esperado: comparan cada mes el día 28 del propio mes, que la V0.73 rechaza (H-02). Sus casos se rehacen, con fechas válidas, en las sondas nuevas.
- **Sondas r02:** tres scripts con prefijo r02 en la misma carpeta de QA de la V0.71, en la entrega de Claude del marco (no están en git). Se ejecutan con `python3 -I` desde `sistema_global/marco_comun_c` e imprimen FALLA o BIEN en cada sonda:
  - cálculo (C1 a C10): el devengo contra un cálculo independiente (un fondo con valor liquidativo (1 − c)^años y participaciones compradas y vendidas al precio de cada movimiento), meses terminados en UTC y no finitos;
  - juicio (J1 a J12): O-41, O-42, comparaciones atrasadas, integridad antes de leer, índice del inicio y los límites H-07 y H-09;
  - migración (M1 a M6): diario, volcado, esquema V0.73 y MIG-009 desde un estado genuino de V0.71 generado con el código de `c306132` (extraído con `git archive` a una carpeta temporal).
- **Mutaciones** (en una copia temporal, ya borrada): diez cambios de una línea en el código corregido, cada uno contra `pruebas_sombra_t76.py`. La batería mata seis y deja vivos cuatro (H-14).

### Estado de los hallazgos de la r01

| ID | Estado en la r02 | Evidencia |
| --- | --- | --- |
| H-01 | **corregido** | C1: aportes y retiradas en fechas distintas, con 29 de febrero de 2028, otro huso y tres movimientos en el mismo instante: código y referencia coinciden a 1e-9. C2: con coste 0, sombra = bruto exactamente. C4: la retirada total neta de coste se acepta y deja 0; un 1e-9 más o los 1 000 EUR brutos, O-06. C5 (el caso S1): el aporte de la víspera paga 9,62 EUR, igual que la referencia, y el robot que pierde 990 EUR da PROPONER_PASIVA. C7: el coste es la misma proporción a cualquier precio |
| H-02 | **corregido** | C8 y C8b: el mes del inicio y el mes terminado se toman en UTC, también con −01:00 y +01:00 en el borde de mes y de año (31 dic 23:59:59.999999 no, 1 ene 00:00Z sí). C8c (el caso S4): el juicio llega a los 731 días. Pero la batería no protege el huso (H-14) |
| H-03 | **corregido en la comparación** | C9: precio 1e308, robot 1e308 o inflación 1e-300 dan O-01 y el estado se vuelca. Queda el inicio con unidades infinitas (H-11) |
| H-04 | **en parte** | J1, J3 y J4: O-42 no salta antes de que termine el mes en UTC, no se repite en cada barrido y se puede poner al día comparando varios meses seguidos. Pero el juicio aún se mueve según cuándo se compare (H-10), y el aviso no tiene plazo ni sube de prioridad (H-13) |
| H-05 | **en parte** | J7: `comparar_sombra` da O-13 con kill-switch en los siete toques probados. `iniciar_sombra` y `movimiento_sombra` todavía leen el registro antes de comprobarlo (H-12) |
| H-06 | **corregido** | C10: retirar el doble con precio 1e12 da O-06; casi todo, OK. La batería no lo protege (H-14) |
| H-07 | en parte, como límite | J8: el índice de precios del inicio ya no cambia (50 en vez de 100, O-01; 100 entero, OK). Siguen como límite: la primera comparación elige el índice (J8b), I declara sin contraste el valor del robot y el precio del índice, que deciden el juicio (J9 y J9b), y `gasto_dia` no está encadenado (aunque `registrar_gasto` rechaza un coste negativo, J11). Es aceptable como límite de la Fase 1 simulada hasta K (T-86), pero solo si está declarado donde se mira. Hoy solo lo está en `analisis-tecnico.md`, que además no cita el valor del robot (H-15) |
| H-08 | **en parte** | J6: O-41 en el mes 24 y otra vez en el 27, tras un SUPERA en el 26, y ninguno en los meses 25 y 28. J6b: un solo O-41 si ya iba por debajo antes del plazo. Los informes del ticket están rellenos. La documentación sigue desfasada (H-15) |
| H-09 | límite, sin declarar | J10: vaciar el registro deja la integridad limpia y permite iniciar otra vez. Es aceptable como límite conocido de las cadenas sin ancla (T-02), pero no está en la deuda (H-15) |

**Lo que se intentó y no se rompió:**
- O-42: ni antes del fin de mes en UTC ni con la hora local de otro huso (J1). Uno por barrido y, tras un acuse, uno más (J4).
- Ponerse al día con tres meses seguidos en el mismo instante (J3).
- Los rechazos de `comparar_sombra` (mes sin terminar, índice del inicio distinto, no finito) no cambian el estado (J12).
- El diario reproduce la sombra, sus dos O-41 y sus dos O-42 (M1). Volcar y cargar con el esquema V0.73 (M2).
- El esquema V0.73 es el actual y está en `esquemas_codigo.json`, y MIG-009 va de V0.71 a V0.73 (M3).
- Un estado genuino de V0.71 con 25 comparaciones y dos O-41 se rechaza sin migrar (PE-08) y migra con `["MIG-009"]`. Después: integridad limpia, el informe lee las 25 comparaciones antiguas, `barrer` da O-42 y la siguiente comparación funciona sin repetir el O-41 (M4 y M5).

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-10 | **media** | Sondas J5 y J5c. Inicio de 100 000 EUR. Meses 1 a 23 comparados a tiempo. Al cierre del mes 24 (2028-11), el robot vale 99 000 y la sombra unos 99 585. El 2028-12-02 se retiran 50 000 EUR (`movimiento_sombra`). El 2028-12-03, I compara 2028-11 con el valor del robot al cierre del mes | **Esperado:** la comparación del mes 24 es la del mes 24. El veredicto no depende de lo que pasó después del cierre ni del día en que I compare. **Obtenido:** `comparar_sombra` valora la sombra en el instante de la comparación (`estado_sombra(L, precio, a)`), con todos los movimientos hasta ese instante, y cuenta el `gasto_dia` hasta ese día. Con la retirada, la sombra queda en 49 585 y el robot que pierde da **SUPERA**, sin O-41. Con un aporte de 50 000 en vez de la retirada (J5c), un robot que gana (101 000) da **PROPONER_PASIVA** y un O-41 falso. Con la H-02 corregida esto pasa siempre: la comparación de un mes llega, a la fuerza, después de su cierre. El contrato no dice a qué instante corresponden `robot_valor_eur` y `precio_indice`, mientras que `inflacion_mes` es «del mes». Si se leen como valores del momento, ponerse al día (J3) da varias comparaciones con los mismos datos y el juicio del mes 24 se hace con los de un mes posterior. Es el resto de la r01 H-04 («el veredicto que convenga a la fecha elegida») | Valorar la sombra al cierre del mes comparado: solo las entradas con `ahora` hasta el fin de mes en UTC, el coste devengado hasta ese instante y `gasto_dia` hasta el último día del mes. Declarar en la docstring, en el Documento 0 y en el LEEME que el valor del robot, el precio del índice y la inflación son los del cierre del mes. Añadir J5 y J5c como pruebas de regresión | abierto |
| H-11 | baja | Sonda C9b. `iniciar_sombra(1e200, 1e-200, "OPERADOR", …)` | **Esperado:** O-01, porque las unidades no son finitas (la misma regla de la H-03). **Obtenido:** OK con `unidades = inf`. Después, toda comparación da O-01 y todo aporte da O-06 con el motivo «la retirada es mayor que lo que tiene la sombra». La sombra queda inservible y no se puede reiniciar (O-02), así que O-42 saldrá cada mes para siempre. La batería lo da por bueno (`… ["ok"] or True` en `resultados_no_finitos_no_se_anotan_H03`) | En `iniciar_sombra`, exigir que `importe / precio` sea finito (o pasar la entrada por `estado_sombra`). En `movimiento_sombra`, distinguir «no finito» de «retirada mayor» en el motivo |
| H-12 | baja | Sonda J7. Con el registro tocado (por ejemplo, sin `ahora` en el INICIO, o con `entradas` vaciadas o borradas), se llama a `iniciar_sombra` o `movimiento_sombra`. Sonda J7b: se cambia el `mes` de una comparación y se llama a `barrer` | **Esperado:** O-13 con kill-switch, como en `comparar_sombra` (la r01 H-05 pedía los tres métodos). **Obtenido:** `iniciar_sombra` da O-02 («ya iniciada») sin kill-switch en cinco toques. `movimiento_sombra` da O-06 («no iniciada») con las entradas vaciadas, y O-00 sin la clave. `barrer` no da O-42 ni O-13: `comparacion_sombra_pendiente` se traga el error y devuelve None. El siguiente punto de decisión lo para (`integridad()` da `['SOMBRA']`) | Llamar a `_sombra_precheck()` al principio de `iniciar_sombra` y `movimiento_sombra`. En `barrer`, si `sombra_ok()` es falso, avisar en vez de callar |
| H-13 | baja | Sondas J2 y J3 | **Esperado:** O-42 avisa de un retraso real, y más fuerte si lo que falta es el juicio. **Obtenido:** salta a las 00:00:00 del día 1, en el mismo instante en que termina el mes y antes de que I haya podido comparar. Habrá un O-42 casi cada mes, y el operador se acostumbrará a ignorarlo. Con tres meses sin comparar, solo avisa del primero (lo que falta se ve al ir comparando, pero el análisis dice «uno por mes pendiente»). Además es MEDIA, no se reitera y no sube de prioridad cuando el que falta es el mes de juicio, de modo que el juicio solo queda «avisado» con un MEDIA | Un plazo `[PROPUESTO]` (unos días tras el cierre, a T-57) antes de O-42. ALTA cuando el mes que falta es el de juicio o uno posterior. Decir en el motivo cuántos meses faltan. Ajustar el texto del análisis |
| H-14 | baja | Mutaciones contra `pruebas_sombra_t76.py` | **Esperado:** cada corrección de la r01 tiene una regresión que la protege. **Obtenido:** sobreviven cuatro mutantes. (1) Volver a `mes_ini = ini["ahora"][:7]`: la H-02 en otro huso no tiene prueba. (2) O-42 con `sig <= _mes_utc(ahora)`, que avisa del mes en curso: no se prueba que no salte antes de tiempo. (3) Volver a la tolerancia absoluta `u > unidades + 1e-9`: la prueba de la H-06 usa 1e-8 unidades y no distingue. (4) Quitar el `isfinite` de `estado_sombra` | Añadir C8 (husos en el borde), J1 (O-42 a las 23:59:59 y a las 00:00 en UTC) y C10 (1e-9 unidades y retirar el doble) como pruebas, y una prueba de `estado_sombra` con un resultado infinito |
| H-15 | baja | Lectura de documentos | **Esperado:** Documento 0, LEEME, ticket y deuda dicen lo que hace la V0.73. **Obtenido:** (1) Las secciones 2 a 4 del Documento 0 de la V0.71 siguen con la V0.71: el coste está «prorrateado por días», el mes es «nunca un mes futuro» (no «terminado»), no aparecen O-42 ni MIG-009, y dice 45 comprobaciones y 60 baterías. La sección 5 lista H-01 a H-04 como pendientes y, justo después, dice que están corregidos. (2) El punto «Comprobado en la cartera sombra pasiva» del LEEME dice «neta de su coste prorrateado», «nunca del futuro» y «O-41 una vez», y no nombra O-42. (3) Los límites H-07 y H-09 no están en la deuda: la fila T-76 sigue con el texto de la r01, y ni T-86 ni T-02 los recogen. Entre los límites no figura el valor del robot que declara I. (4) `pruebas.md` no da el resultado de las baterías ni del gate de la V0.73. (5) CA-5 dice «60 baterías» (hoy 61) | Actualizar el Documento 0 (secciones 2 a 5), el LEEME y la fila T-76. Llevar los límites a T-86 (precio, inflación y valor del robot sin contraste con K y G) y a T-02 (ancla de la cabeza `SOMBRA`). Anotar el resultado de las baterías y del gate en `pruebas.md` |
| H-16 | baja | Sondas M5b y M6. Estados genuinos de V0.71 migrados con MIG-009 | **Esperado:** MIG-009 «sin cambios en el estado» deja las comparaciones antiguas con el mismo sentido. **Obtenido:** se leen bien (M4), pero la V0.73 las interpreta con sus reglas nuevas sin decirlo. Si la V0.71 anotó índices del inicio distintos (100 y 101), la V0.73 fija en silencio el de la primera comparación. Con un inicio escrito en hora local (2026-12-01T00:30+01:00), la V0.71 contó el mes 1 desde 2026-12 y la V0.73 cuenta desde 2026-11 en UTC, así que el registro pasa de `meses` 1 a 3. Las comparaciones antiguas llevan además el coste antiguo y pueden ser de meses sin terminar. Pesa poco: la V0.71 no llegó a operar | Decirlo en la descripción de MIG-009 y en el Documento 0 (las comparaciones de la V0.71 se conservan como históricas, con sus reglas). O hacer que MIG-009 rechace un estado de V0.71 con comparaciones incoherentes con la V0.73 |

**Observaciones sin hallazgo:**
- El coste se devenga por días/365, así que un año bisiesto cobra 366/365 del coste anual (C3: 2,0055 EUR por 1 000 EUR). Es una convención defendible, pero conviene declararla.
- Una inflación diminuta (1e-5 frente a 1e300) se acepta con una inflación acumulada de −100 % (C9). No cambia el veredicto, porque real y nominal coinciden.
- Con la sombra vaciada del todo se sigue comparando (C4b), y es correcto.

### Veredicto r02

**NO APTO** · Un hallazgo medio confirmado:
- H-10: el mes se valora en el instante de la comparación, no a su cierre. Un movimiento legítimo entre el cierre y la comparación da la vuelta al juicio de los 24 meses, a favor o en contra del robot, y puede callar el O-41 o darlo sin motivo.

H-01, H-02, H-03 (en la comparación) y H-06 están corregidos. H-04, H-05, H-07 y H-08 lo están en parte. H-07 y H-09 son aceptables como límites de la Fase 1 simulada si se declaran en la deuda (H-15). H-11 a H-16 son bajos: se corrigen en la ronda siguiente o pasan a la deuda con su ID. En la r03, el revisor volverá a ejecutar sus sondas r02, y J5 y J5c deben dar BIEN.

---

## Ronda r03

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación ni de las rondas r01 y r02 · **Ronda:** r03 · 2026-11-12
- **Objeto:** la V0.75 del marco en el commit `89e78e7`. Lo revisado: `validador/sombra.py`; en `validador/orquestador.py`, `iniciar_sombra`, `movimiento_sombra`, `comparar_sombra`, `comparaciones_sombra_pendientes`, `comparacion_sombra_pendiente`, `_sombra_precheck`, `sombra_ok`, `informe_sombra`, `barrer` y `_costes_analisis_desde`; `validador/parametros.py`, `validador/parametros_doc.py`, el catálogo (O-41, O-42 y O-44), `validador/migraciones.py` (MIG-009 y MIG-011), la batería `pruebas/pruebas_sombra_t76.py`, los Documentos 0 de la V0.71 y la V0.75, el LEEME, las filas T-76, T-86, T-02 y T-57 de la deuda y los documentos del ticket. Contrastado con la Constitución, §9 punto 9 (D-22, D-27 y D-30), P17 y las convenciones de D-30.

### Reproducción

- **Copia limpia:** un `git worktree` de `89e78e7` en una carpeta temporal fuera del repo, quitado al terminar.
  - `.docs/scripts/pruebas_marco.sh`: **62 pasan, 0 fallan**.
  - `pruebas/pruebas_sombra_t76.py`: 74 comprobaciones, todas pasan.
  - `.docs/scripts/leeme_marco.py` sobre `sistema_global/marco_comun_c`: «SIN DIFERENCIAS (0)».
- **Código antiguo:** la copia del repositorio es superficial (9 commits) y no tiene `c306132` (V0.71) ni `7b775cc` (V0.73). Se trajeron con `git fetch --depth=80` de `develop` a un repositorio «bare» en una carpeta temporal, sin tocar el `.git` del proyecto. `5d03192` (V0.74) sí está.
- **Con el código de la V0.74 y la batería de la V0.75:** fallan las dos regresiones de H-10 y la de H-11, y la batería se para en la línea 187 con un AssertionError. Lo dice `pruebas.md`, aunque la causa no es que «falten las funciones nuevas»: la V0.74 acepta el inicio con unidades infinitas y el `iniciar_sombra` siguiente da O-02.
- **Sondas r03:** cinco scripts en `.docs/tickets/T-76/revisores/`. Se ejecutan con `python3 -I` desde la raíz del repo, con la ruta del marco como argumento opcional, e imprimen FALLA o BIEN en cada sonda:
  - `r03_01_cierre_plazos_juicio.py` (A1 a A12): el mes valorado a su cierre contra una referencia independiente (un fondo con valor liquidativo (1 − c)^años), movimientos y costes de análisis en el último microsegundo y en el primer instante del mes siguiente, en UTC y en ±01:00 y ±05:00, febrero bisiesto, cambio de año, plazo de gracia exacto, mes de juicio y siguientes, ponerse al día y repetición de O-42 y O-44. **0 FALLA de 18.**
  - `r03_02_fallo_cerrado_registro.py` (F1 a F9): NaN, inf, None, bytes, bool, complejos, enteros enormes, un float que miente al compararse, meses y actores mal escritos, reloj hacia atrás, idempotencia, diez toques del registro en los tres métodos y en `barrer()`, volcado tocado, fallo a mitad de operación y prioridades. 6 FALLA de 19: F2 y F2b (H-17), F3b y F3c (H-19), F9b (H-18) y F3d, que mide el límite declarado T-02.
  - `r03_03_migraciones_v071_v073_v074.py` (M1 a M7): estados genuinos de la V0.71, la V0.73 y la V0.74, generados con su propio código, con 24 comparaciones, un movimiento tras el cierre del mes 24 y un O-42 sin acusar, migrados a la V0.75; además, el diario. Para la copia superficial se le indica el repositorio con `R03_GIT_DIR`. 3 FALLA de 16: M4 en la V0.73 y en la V0.74 (observación) y M6 (H-20).
  - `r03_04_mutantes.py`: 31 mutantes de una línea en una copia temporal, cada uno contra la batería. **Mueren 21 y viven 10** (H-18).
  - `r03_05_rejecuta_r02.py`: vuelve a ejecutar las sondas r02.
- **Sondas r02, otra vez:**
  - `r02_sondas_calculo.py`: todo BIEN salvo C4b, que es el comportamiento correcto que la r02 ya anotó como observación, y C5. C5 calcula su referencia en el instante de la comparación y no al cierre: con la H-10 corregida, la diferencia es la esperada y el veredicto, PROPONER_PASIVA, es el correcto.
  - `r02_sondas_juicio.py` sin cambios: J1 y J3 dan FALLA y J4 se para, porque esperan O-42 en el mismo instante del cierre (antes del plazo de gracia de la H-13). Con `r03_05_rejecuta_r02.py juicio --sin-gracia`, que pone a 0 la gracia por defecto solo en ese proceso, corren enteras:
    - **J5, J5c y J5b dan BIEN**, como pedía la r02;
    - J1, J2, J4, J6, J6b, J7, J8, J11 y J12 dan BIEN;
    - J3 da FALLA porque ahora hay un O-42 cada vez que crece el número de meses pendientes, que es lo que pedía la H-13;
    - J7b da FALLA porque no mira el O-13 que ahora sale;
    - las cuatro LIMITE siguen, como estaba declarado.
  - `r02_sondas_migracion.py`: M1 da BIEN. M2 y M3 dan FALLA porque el esquema actual ya es el de la V0.75, y es lo esperado. M4 a M6 no corren en la copia superficial; sus casos se repiten, con la V0.73 y la V0.74 además, en `r03_03`.
- **Gate:** `./tools/check_all.sh --core` sobre la copia limpia (ver «Gate» abajo). El gate completo pasó 12/12 en el commit, según el registro del ticket; no se repitió, porque otro revisor trabaja a la vez.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1: la sombra nace con el mismo capital y replica cada aporte y retirada al precio de su momento | sí, con reservas | Batería (`el_primer_dia_*`, `un_aporte_*`, `G_tambien_*`). A1, A1b y A4: cada movimiento entra en el mes de su instante en UTC, y el valor coincide con la referencia a 1e-6. F1: ninguna entrada rara pasa ni cambia el estado. Reserva: el mismo movimiento declarado dos veces se replica dos veces (H-17) |
| CA-2: cada mes, el robot neto de costes de análisis e impuestos frente a la sombra neta de su coste, en nominal y en real | sí | A3: la sombra se valora al cierre aunque I compare 29 días tarde, igual que la referencia al cierre (999 694,95, frente a 999 534,57 si se valorara en el instante de la comparación). A2: los costes de análisis cuentan hasta el último microsegundo del mes, y no desde el primer instante del siguiente. A4: ponerse al día con tres meses en el mismo instante valora cada uno a su cierre. A11: el juicio del mes 24 es el mismo comparado el 1-12-2028, el 20-12-2028 o el 1-6-2029 |
| CA-3: antes de 24 meses no se juzga; a los 24, O-41 al pasar a no superarla; si la supera, nada | sí | A7: EN_PLAZO hasta el 23; en los meses 24 a 29, O-41 en el 24, el 26 y el 29, y ninguno en el 25, el 27 y el 28. A7b: el mes 24 es 2028-11, con 755 días desde el inicio. A8 y A9c: O-44 (ALTA) en cuanto vence la gracia del mes de juicio, aunque falten meses anteriores; se reitera y escala como los ALTA |
| CA-4: los rechazos no cambian el estado, y el registro tocado se detecta (O-13 con kill-switch) | sí, con reservas | F1, F1b a F1d, F2c y F8: ningún rechazo ni fallo a mitad de operación cambia el estado. F3: diez toques en los tres métodos dan O-13 con kill-switch, y `barrer()` avisa con O-13. F4: un volcado tocado da PE-02. Reservas: con el registro roto, `barrer()` sigue avisando de lo pendiente con los datos tocados, y no activa el kill-switch (H-19) |
| CA-5: guardar, cargar y MIG-008; 62 baterías; gate 12/12 | sí | M1 a M5: los estados genuinos de la V0.71 (`["MIG-009", "MIG-010", "MIG-011"]`), de la V0.73 (`["MIG-010", "MIG-011"]`) y de la V0.74 (`["MIG-011"]`) se rechazan sin migrar (PE-08), migran con la integridad limpia, conservan sus 24 comparaciones, dan O-44, se ponen al día y se vuelcan y cargan con el esquema V0.75. M7: el diario reproduce la sombra, O-44 y O-41. 62/62 baterías. Gate: ver abajo |

### Estado de los hallazgos de la r02

| ID | Estado en la r03 | Evidencia |
| --- | --- | --- |
| H-10 | **corregido** | J5, J5c y J5b de la r02, con la gracia a 0: BIEN. A1, A3, A4 y A11: la sombra, su coste y los costes de análisis van hasta el último microsegundo del mes en UTC; lo posterior no cambia el veredicto. Docstring, Documento 0 y LEEME dicen que el valor del robot, el precio y la inflación son los del cierre. Faltan regresiones para el coste hasta el cierre y para el borde exacto (H-18) |
| H-11 | **corregido** | C9b de la r02: O-01 al iniciar con 1e200 / 1e-200. La batería lo protege (mutantes M19 y M20, muertos). Un movimiento no finito da O-01 con su motivo |
| H-12 | **corregido** | F3: O-13 con kill-switch en `iniciar_sombra`, `movimiento_sombra` y `comparar_sombra` con los diez toques; `barrer()` avisa con O-13 (mutantes M15 a M18, muertos). Queda lo de la H-19 |
| H-13 | **corregido** | A6: el aviso sale justo a los 5 días del cierre en UTC, no 1 µs antes, también escrito en ±01:00. A8: el número de meses que faltan va en el motivo, y O-44 sale en ALTA si falta el mes de juicio o uno posterior. A9: tres meses sin comparar con barridos diarios dan tres O-42, uno cada vez que crece el número, y ninguno repetido; tras el acuse vuelve a avisar. El parámetro es `[PROPUESTO]`, pero no está en la fila T-57 (H-21) |
| H-14 | **corregido** | Los cuatro mutantes de la r02 mueren (M24, M23 con el plazo de gracia, M25 y M21). Viven otros (H-18) |
| H-15 | **corregido** | Documentos 0 de la V0.71 (secciones 2 a 5) y de la V0.75, LEEME, filas T-76, T-86 y T-02 y `pruebas.md` dicen lo que hace la V0.75. Quedan la fila T-57 (H-21) y MIG-011 (H-20) |
| H-16 | **corregido** | La descripción de MIG-009 declara que las comparaciones de la V0.71 se conservan como históricas, con sus reglas (M2 en la V0.71). No se dice lo mismo de MIG-011 para la V0.73 y la V0.74 (H-20) |

**Lo que se intentó y no se rompió:**
- Bordes de mes y de año, en UTC y en otros husos: movimientos (A1 y A1b), costes de análisis (A2), inicio (A5b y A12), comparación en el último microsegundo del mes y un microsegundo después (A10) y febrero bisiesto (A5).
- Plazo de gracia exacto (A6), mes de juicio y siguientes (A7), O-42 frente a O-44 al ponerse al día (A8 y A8b), repetición y acuse (A9 y A9b), y reiteración y escalado del ALTA (A9c).
- Valores raros en los tres métodos (F1), meses mal escritos, incluidos los dígitos de ancho completo (F1b), y actores con variantes (F1c).
- Reloj hacia atrás (F1d), repetir o saltarse meses (F2c), fallo a mitad de la anotación (F8), informe con copias (F7), prioridades en el catálogo y en `PRIORIDAD_AVISO` (F6), y un resultado no finito en la comparación (F9).
- Migración de estados genuinos de la V0.71, la V0.73 y la V0.74 (M1 a M5) y el diario (M7).

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-17 | **media** | Sondas F2 y F2b. Inicio de 100 000 EUR. G declara un aporte de 50 000 EUR el 2026-12-10 a las 10:00, y el operador declara el mismo aporte (o G lo reenvía tras un corte) | **Esperado:** «los mismos aportes y retiradas que la cartera real» (§9 punto 9). Un movimiento repetido no se cuenta dos veces, como el resto de lo que declara G en el marco, que lleva `event_id` y da O-02 si se repite (por ejemplo, `registrar_manual`). **Obtenido:** `movimiento_sombra` no tiene identificador del movimiento ni detecta duplicados, y el docstring invita a dos actores a declarar el mismo hecho («la declara el operador (o G, que ve el movimiento en el intermediario)»). Tres declaraciones iguales dan tres aportes (F2). Con uno repetido, un robot que vale lo mismo que la cartera real (150 750 EUR, +0,5 %) frente a una sombra de 199 191 EUR da **PROPONER_PASIVA** y un O-41 falso en el mes 24 (F2b). Una retirada repetida da el error contrario. No se puede deshacer, y ningún límite declarado lo recoge | Dar a `movimiento_sombra` una referencia obligatoria del movimiento en el intermediario (o un `event_id`): la misma referencia con el mismo contenido da O-02 (duplicado), y con otro contenido, O-03. Añadir F2 y F2b como regresiones. Si no se corrige ahora, declararlo en el Documento 0 y llevarlo a la deuda (con G y T-86: contrastar los movimientos de la sombra con los de la cartera real) |
| H-18 | baja | `r03_04_mutantes.py` y sonda F9b | **Esperado:** cada regla nueva de la V0.75 tiene una regresión que la protege. **Obtenido:** viven 10 de 31 mutantes. Ocho cambian el comportamiento, y las sondas r03 los detectan: M02 (coste de la sombra hasta la comparación, no hasta el cierre: A1, A3, A4 y A11), M03 (costes de análisis hasta la comparación: A2), M04 (sin el último microsegundo del mes: A1 y A5), M05 (cierre 1 µs tarde: A1, A2 y A4), M09 y M12 (el juicio por el primer mes pendiente, o lo pendiente contado desde la primera comparación: O-42 en vez de O-44, A8 y A8b), M13 (lo pendiente desde el mes de inicio local: A12) y M22 (sin el `isfinite` de `comparar`: F9). Además, `resultados_no_finitos_no_se_anotan_H03` ya no prueba nada: su inicio (1e200 / 1e-200) lo rechaza ahora la H-11, y la prueba toma la rama `{"codigo": "O-01"}` sin llamar a `comparar_sombra` (F9b). Los otros dos son casi equivalentes: M30 (año de 366 días; la batería solo acota el coste) y M29 (juicio en nominal con `>=`: solo cambia el empate, que no se prueba) | Añadir como pruebas A1, A2, A3, A8, A12 y F9 (y reescribir la regresión H-03 con un inicio válido y `robot` 1e308 con inflación 1e10 / 1e-300). Fijar el coste contra un cálculo de referencia y probar el empate (robot neto igual a la sombra en el mes 24: PROPONER_PASIVA) |
| H-19 | baja | Sondas F3b y F3c. Con el INICIO retrasado a 2020-01-01 en el registro, `barrer("2027-01-10…")`. Con el importe del INICIO tocado, `barrer("2026-12-10…")` | **Esperado:** con el registro roto, `barrer()` avisa con O-13 y no saca conclusiones de él (su propio motivo dice «no se puede comparar ni avisar de lo pendiente»). **Obtenido:** avisa con O-13 y, a continuación, con un O-44 (ALTA) de «83 mes(es) sin comparar desde 2020-02», calculado con el registro tocado. Con otro toque (J7b de la r02, un mes de 2099), lo pendiente desaparece en silencio. Además, `barrer()` no activa el kill-switch, mientras que los tres métodos que escriben sí. CA-4 se cumple por esos tres métodos y por el siguiente punto de decisión, y `integridad()` da `["SOMBRA"]` | En `barrer()`, si `sombra_ok()` es falso, no calcular lo pendiente. Decidir y documentar si el barrido activa el kill-switch, como `_sombra_precheck()`, o solo avisa |
| H-20 | baja | Sondas M1, M2 y M6. Un estado genuino de la V0.73 o la V0.74 en el que se retiraron 50 000 EUR tras el cierre del mes 24 y luego se comparó (el caso de la H-10) | **Esperado:** como en MIG-009 (H-16), la migración dice que las comparaciones antiguas se conservan con sus reglas. **Obtenido:** migra bien y conserva la comparación antigua del mes 24, **SUPERA** sin O-41, valorada con la regla de la V0.73 (en el instante de la comparación). Con la V0.75 sería PROPONER_PASIVA. La descripción de MIG-011 dice solo «sombra valorada al cierre del mes … el estado guardado no cambia», y el Documento 0 de la V0.75 solo habla de las comparaciones de la V0.71. Además (M4, observación), los O-42 antiguos sin acusar siguen vivos junto al O-44 nuevo, aunque el mes ya se haya comparado. Pesa poco: la V0.73 y la V0.74 no llegaron a operar | Añadir a la descripción de MIG-011 y al Documento 0 de la V0.75 que las comparaciones de la V0.73 y la V0.74 se conservan como históricas, valoradas en el instante de la comparación |
| H-21 | baja | Lectura de la deuda y de `parametros_doc.py` | **Esperado:** todo `[PROPUESTO]` está en la deuda, en la sesión de decisiones T-57, como los otros dos de la sombra («Añadidas por T-76 (marco V0.71): … `i_indice_sombra` … `i_coste_anual_sombra_pct`»). **Obtenido:** `i_dias_gracia_comparacion_sombra` (5 días, `[PROPUESTO]`) no aparece en el documento de la deuda fuera de la fila T-76, que desaparecerá al cerrarse. Sus fuentes en `parametros_doc.py` son «Deuda T-76» y «V0.75», no T-57 (aunque el comentario de `parametros.py` sí cita T-57). La pregunta para el cuestionario sí existe | Añadir el plazo de gracia a la fila T-57 («Añadidas por T-76 (marco V0.75): …») y, si procede, «Deuda T-57» a sus fuentes |

**Observaciones sin hallazgo:**
- `comparaciones_sombra_pendientes(ahora, gracia_dias)` acepta una gracia negativa o 0 sin quejarse, y con NaN, None o un texto devuelve None. Solo lee, y `barrer()` usa siempre el parámetro.
- Un O-44 (ALTA) sin acusar se sigue reiterando y escalando aunque I ya haya comparado el mes. Es la regla general de los ALTA (CT-G-16): lo cierra el acuse del operador.
- F3d: reescribir el registro con sus huellas recalculadas no se detecta. Es el límite declarado en T-02.
- Invariantes de la skill:
  - no hay LLM en la ruta;
  - nada se decide solo: O-41 y O-44 proponen y avisan;
  - todo falla cerrado y valida antes de mutar (F1 y F8);
  - el único número nuevo (5 días) sale de `PARAMETROS` y está documentado como `[PROPUESTO]`;
  - no hay secretos ni datos personales en lo revisado;
  - la sombra no da órdenes, así que F y G no aplican.

### Gate

- `./tools/check_all.sh --core` sobre la copia limpia de `89e78e7`: **8 pasan, 0 fallan** (corpus, configuración y pytest de los tres bloques; B 176), en 12 min.
- El gate completo (12/12) pasó en el commit, según el registro del ticket y `commit_limpio.sh`; no se repitió, como se pidió. La r03 no cambia código, así que no hace falta otro gate para el veredicto.
- Baterías del marco: 62/62 (`pruebas_marco.sh`), y LEEME contra disco sin diferencias.

### Veredicto r03

**APTO** · Se cumplen los cinco criterios de aceptación, y no hay hallazgos críticos ni altos abiertos. H-10 a H-16 están corregidos.

Queda abierto H-17 (medio): un movimiento repetido se cuenta dos veces. No hace fallar CA-1, porque cada movimiento real se replica, pero puede mover el juicio de los 24 meses. Se recomienda corregirlo antes de que la sombra reciba movimientos de G de verdad.

H-17 y los bajos H-18 a H-21, si no se corrigen, pasan a la fila T-76 de la deuda con su ID: H-17 con G y T-86; H-20 y H-21, de documentación.
