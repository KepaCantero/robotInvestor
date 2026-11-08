# Revisión independiente — V0.41 (reducción parcial declarada a mano)

Estado: **revisión ejecutada y dos hallazgos corregidos** (sección 7 de las directrices). La revisión se hizo
en otra conversación, con el ZIP de la pieza ya en verde y el prompt «Prompt para el revisor — V0.41 (copiar y
pegar)», sin el historial de la pieza. El revisor verificó contra el código real, no contra lo que declara la
entrega: (1) las 39 ejecuciones del bucle de la sección 0 en verde, con la batería nueva en las 42
comprobaciones anunciadas y dos ejecuciones con salida idéntica; (2) la no-vacuidad (la batería T-44 contra el
código de V0.40 falla en 7 comprobaciones, y las pruebas antiguas de la V0.41 contra el código de V0.40 fallan
solo en los dos cambios explicados: `cierre_parcial_sin_stop_RM07` y `M9_declaracion_rechazada_no_quita_el_stop`);
(3) el diff V0.40 → V0.41, que toca solo los ficheros declarados, con `conciliar`, H y
`contratos.registro_manual` intactos y `version_config` en CFG-0.8.0 (TOL_Q = 1e-6 coincide con el TOL de G y
con el umbral de `manual_g`); (4) el cierre falla cerrado en todos los casos sondeados (mínimo sin foto, divisa
sin tipo de cambio, contexto `valor_min_restante_eur` corrupto, precio 0 o negativo, precio que desborda,
cantidades 10**400, cantidad 0 o negativa, resto justo en el mínimo, orden de G, O-03 sobre los tres tipos de
stop, bordes del criterio «parcial», REDUCIENDO, CORTO, EN_REVISION, dos parciales seguidas, cierre total
posterior, integridad y ausencia de dobles conteos); y (5) cinco sospechas investigadas y descartadas sin
camino dañino (divergencia de 1 ulp en el borde del criterio «parcial» —la 4ª rama de `manual_g` la rechaza
con RM-06—, subdesborde del mínimo a 0.0 en `_valor_min_restante`, instrumento cotizado en EUR sin foto,
mensaje «a media reducción…» dentro de la banda de 3e-14, apunte manual sin las claves de las reducciones de G).

Resultado: **dos hallazgos reproducibles (1 ALTA y 1 MEDIA), ambos corregidos**. Tras la corrección: el bucle de
la sección 0 entero en verde (`ejecutar_pruebas.py` + las 38 baterías de `pruebas/pruebas_*.py`, 39 ejecuciones,
ninguna línea FALLA); la batería nueva queda en **47 comprobaciones** (5 regresiones nuevas) y determinista
(dos ejecuciones, diff vacío); los catorce scripts de hallazgos de las cinco revisiones (`hallazgo_1..6` de la
V0.37, `hallazgo_t33_1..3` de la V0.38, `hallazgo_t40_1..2` de la V0.39, `hallazgo_v40_1` de la V0.40 y los dos
de esta) dan OK; las nueve sondas adversariales del revisor de V0.40 (`sondas_revisor_v040.py`) cierran todas y
las cuatro sondas del revisor de esta pieza (`sondas_t44_revisor.py`) terminan sin error. Los tres ficheros del
revisor quedan intactos byte a byte en la raíz de `marcoC/` y se ejecutan desde ahí.

## Hallazgos

| # | Gravedad | Fichero y función | Defecto | Script | FALLA antes | Arreglo | Regresión | OK después |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | media | `validador/ejecucion_g.py` — `_declarar_parcial` (llamada desde `declarar_manual`, rama POSICION) | El contraste de la cantidad del stop nuevo y el del neto del intermediario usaban `_cuadra` (tolerancia relativa 1e-6·max(1, \|y\|)), mientras que toda la cadena posterior mide en absoluto: TOL_Q = 1e-6 del Orquestador, la conciliación (CANTIDAD con TOL = 1e-6 y `tolerancia_conciliacion_rel` = 0.0 por defecto) y su control de protección (1e-6 absoluto); el cierre total, además, sí rechaza el desfase equivalente (control del neto absoluto, G-10). Una declaración que difiere del relleno real hasta en 1e-6·max(1, restante) se registraba con OK y la conciliación inmediata — sin ningún otro evento — reportaba discrepancia kill-switch (CANTIDAD, o PROTECCION y CANTIDAD con el stop por lo que queda real), contradiciendo el punto 4 del diseño («tras una parcial correcta la cantidad esperada es la nueva, el stop vivo nuevo es exacto y los viejos están cancelados») y asignando a G-10 justo ese caso («lo declarado no cuadra con el intermediario»). Escenario: posición de 100 EURUSD; el intermediario ejecuta una venta de 40.0 y el operador declara 40.00003 (3e-5, dentro de las bandas relativas 4e-5 y 6e-5) con el stop por 59.99997: G respondía OK, libros 59.99997 y conciliar CANTIDAD («Orquestador 59.99997, intermediario 60.0») | `hallazgo_t44_1_conciliacion_tras_parcial_con_desfase.py` | `caso 1: G=OK libros=59.99997 conciliar=[CANTIDAD]` y `caso 2: G=OK … [PROTECCION, CANTIDAD]` → FALLA (exit 1) | Los dos contrastes de cantidad pasan a la comparación ABSOLUTA `abs(x − y) <= TOL` (nueva `_cuadra_abs` junto a `_cuadra`, con el TOL = 1e-6 del propio módulo, el mismo umbral de la conciliación); sin banda relativa, el desfase de 3e-5 cae en G-10 antes de registrar nada — por el contraste del neto si el stop va por lo declarado y por el contraste del stop si va por lo que queda real — y la parcial dentro de la banda (5e-7) sigue aceptándose con la conciliación inmediata limpia | `G_desfase_lo_declarado_G10`, `G_desfase_lo_real_G10` y `G_desfase_dentro_de_la_banda_consistente` en `pruebas/pruebas_manual_t44.py` | OK |
| 2 | alta | `validador/ejecucion_g.py` — `conciliar` (con `validador/orquestador.py`, `registrar_manual` rama parcial T-44, y `_stops_de`) | La mutación de la parcial saca los stops viejos de `p["protecciones"]` y los guarda en `p["protecciones_anteriores"]`, pero ni `_stops_de` ni `conciliar` leían `protecciones_anteriores`: los controles de stop huérfano solo recorren `p["protecciones"]` más los identificadores R{n}-S de las reducciones de G. La garantía del diseño («los viejos están cancelados», punto 4) solo la produce el camino por G (`_declarar_parcial` los cancela antes de registrar, G-10 si no puede); por el camino directo (`o.registrar_manual` sin G — camino propio de la batería) nadie toca el intermediario: el stop viejo seguía ACEPTADA cubriendo 100 cuando los libros decían 60 y la conciliación lo declaraba limpio. Antes de T-44 ese estado era inaccesible o visible (el cierre total mantiene los stops en `p["protecciones"]`, que `conciliar` sí recorre). Escenario: posición de 100 EURUSD (stop de la entrada ORD-EXP-0001-S-1, VENTA 100 a 1.05); el operador vende 40 a mano, coloca MAN-STOP-2 (VENTA 60 a 1.05) y registra la parcial directamente en el Orquestador: conciliar daba ok=True con el stop viejo vivo; al cruzar 1.05 el stop se ejecuta fuera de todo control, el intermediario queda plano y la conciliación solo descubría entonces PROTECCION + CANTIDAD (kill-switch), tras la venta incontrolada | `hallazgo_t44_2_stop_viejo_vivo_invisible_a_conciliacion.py` | `conciliar: [] \| ok: True` con el stop viejo aún ACEPTADA; al cruzar 1.05 se ejecuta fuera de control → FALLA (exit 1) | `conciliar` comprueba ahora los stops de `p["protecciones_anteriores"]` de todas las posiciones (antes de la rama CERRADA): un stop retirado debe estar CANCELADA; si sigue vivo (ACEPTADA), a medias (PARCIAL) o se ejecutó (EJECUTADA), PROTECCION_HUERFANA («el stop retirado X no está cancelado (estado)»), tipo ya presente en TIPOS_KILL (kill-switch). El control va ANTES del «continue» de STOP_EJECUTADO para que la ejecución fuera de control de un stop retirado no pueda quedar explicada como cierre propio, y `_stops_de` no cambia (el camino por G y `_reducir` conservan su semántica exacta). El estado del hallazgo sigue siendo posible por el camino directo (límite anotado de T-32: el Orquestador no contrasta el intermediario), pero vuelve a ser VISIBLE, como antes de T-44; el camino por G lo sigue impidiendo (los cancela con reconsulta antes de registrar) | `directo_stop_viejo_vivo_lo_ve_la_conciliacion` (el estado del hallazgo: la conciliación lo ve) y `directo_con_el_viejo_retirado_concilia_limpio` (el operador retira el viejo antes de declarar, patrón de T-12: conciliación limpia) en `pruebas/pruebas_manual_t44.py` | OK |

La numeración coincide con la del fichero: el informe del revisor enunció primero el hallazgo 2 (el ALTA) y
después el 1 (el MEDIA), pero los scripts llevan la numeración contraria y aquí manda la de los ficheros, como
en las piezas anteriores.

## Notas de la revisión

- Solo cambia `validador/ejecucion_g.py` (los dos arreglos: `_cuadra_abs` y los dos contrastes de
  `_declarar_parcial`; el bucle de stops retirados en `conciliar`). `validador/orquestador.py`,
  `validador/manual_g.py`, la consola y las 38 baterías anteriores quedan exactamente como estaban. La batería
  `pruebas/pruebas_manual_t44.py` añade las 5 comprobaciones de regresión (42 → 47) y la documentación de la
  entrega se actualiza con las cifras (`Documento_0.md`, esta `revision.md`, `LEEME.md`, `notas_briefing.md` y
  `salida_pruebas.txt`).
- Ninguna prueba antigua se debilita: las 38 baterías anteriores pasan sin tocar ni una línea, y las dos
  diferencias que el revisor ya había explicado como cambios de comportamiento de la pieza
  (`cierre_parcial_sin_stop_RM07` y `M9_declaracion_rechazada_no_quita_el_stop`) siguen igual.
- El revisor dejó constancia de cinco sospechas investigadas y descartadas sin camino dañino; ninguna requiere
  cambio: la divergencia de ~1 ulp en el borde del criterio «parcial» entre G y `manual_g`/Orquestador la
  rechaza la 4ª rama absoluta de `manual_g` con RM-06; el subdesborde del mínimo a 0.0 en `_valor_min_restante`
  exige una configuración absurda y coincide en la práctica con el mínimo verdadero; un instrumento cotizado en
  EUR sin foto calcula el mínimo con fx = 1.0 (coherente con la fuente declarada de T-33 para LIBRES); el
  mensaje «a media reducción…» dentro de la banda de 3e-14 es un rechazo correcto y cosmético; y los apuntes
  manuales en `reducciones` sin las claves de las reducciones de G no tienen ningún lector que las exija.
- Verificación tras los arreglos: los dos scripts del revisor en OK (exit 0); el bucle de la sección 0 completo
  (39 ejecuciones) sin ninguna línea FALLA; la batería nueva determinista (dos ejecuciones, misma salida); los
  doce scripts de hallazgos de las piezas anteriores en OK; las nueve sondas de V0.40 cierran y las cuatro
  sondas de esta pieza terminan sin error.
