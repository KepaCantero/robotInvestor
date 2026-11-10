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
