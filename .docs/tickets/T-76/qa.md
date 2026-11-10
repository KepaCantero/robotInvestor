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
