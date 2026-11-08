# Documento 0 — T-44, reducción parcial declarada a mano (V0.41) — GLM, pendiente de revisión

## 1. Problema y alcance

Hoy un registro CT-G-14 vinculado a una POSICION solo puede ser un cierre total (RM-06: «el cierre manual
debe ser total (una reducción parcial la hace G con reducir; declararla a mano no está implementado)»).
Si el operador vende una parte a mano fuera del sistema (en el intermediario, con un CT-G-14), no lo puede
declarar: la conciliación ve una discrepancia de CANTIDAD y degrada la cartera, y el operador se ve empujado
a cerrar la posición entera o a dejar una discrepancia sin explicar. Es la deuda T-44
(Deuda_tecnica.md, fila T-44: «Hoy solo se declaran cierres totales; una venta parcial a mano es una
discrepancia»).

Entra en esta versión: declarar a mano una reducción parcial de una posición ABIERTA o EN_REVISION,
siguiendo el patrón de T-12 (primero el stop nuevo por lo que queda, después se retira el viejo, para que
la posición nunca quede sin protección), con dos reglas nuevas (RM-07 en la parcial y RM-12 sobre el valor
mínimo del resto según la política de F) y el contraste completo de G contra el intermediario. La posición
se queda en su estado (ABIERTA o EN_REVISION), la reducción queda anotada en `reducciones` con
`"manual": True`, y la conciliación y H funcionan (la conciliación vigila además que los stops retirados
estén cancelados, §2 punto 5).

Queda fuera: la reducción parcial a mano de una posición REDUCIENDO (sigue igual que antes: a media
reducción el cierre manual es del resto del intermediario y termina el cierre); el cierre total (no cambia
ni una línea); la reducción iniciada por el sistema (G con `reducir`, T-12, no cambia); la consola del
operador (`contratos.registro_manual` solo envuelve el mensaje y no necesita cambios); `vigilancia` (no
necesita cambios) y `conciliar` (solo añade el control de los stops retirados, ver §2 punto 5). T-43 (lo que
quedó de T-12) y D-11 (ratificar los
valores de la política de F) siguen como estaban.

## 2. Diseño

El flujo es el mismo que el de un cierre manual, con una rama nueva en cada módulo:

1. **manual_g.py (`_validar_plano`, rama POSICION).** Cuando la posición no está REDUCIENDO y
   `cantidad < p["cantidad"]` (más allá de la tolerancia de 1e-6), es una reducción parcial manual y se
   añaden las reglas de la nueva `_parcial_manual`:

   - exige `proteccion_ref`: el stop nuevo que el operador ya colocó en el intermediario por lo que queda
     (si falta, RM-07);
   - exige que lo que queda, `p["cantidad"] - cantidad`, valga en euros al menos `valor_min_eur` de la
     política de F. Para eso el ctx de `validar_manual` lleva `valor_min_restante_eur`, ya calculado por el
     Orquestador (ver punto 4). Si el resto no lo cumple, RM-12: «una reducción parcial no puede dejar un
     resto por debajo del valor mínimo de F: ciérrala entera»;
   - el resto se valora con el `precio` del propio registro (el precio real de la venta del operador, que
     G contrasta contra el intermediario): `resto = (p["cantidad"] - cantidad) * precio`, en la divisa de
     cotización del instrumento;
   - si `valor_min_restante_eur` no llega (None, no numérico, negativo) o el resto no se puede valorar
     (un producto que desborda a infinito), RM-12: no se puede verificar el mínimo, se rechaza la parcial
     y se pide el cierre entero (falla cerrado);
   - una parcial con `cantidad <= 1e-6` se rechaza con RM-06 (no es una reducción; el cierre total se
     declara con la cantidad exacta);
   - si `cantidad > p["cantidad"] + 1e-6`, sigue siendo RM-06, con texto nuevo: «se declara más cantidad de
     la que tiene la posición: el cierre total es con la cantidad exacta»;
   - el texto de RM-06 y la cabecera del módulo se actualizan (RM-12 nueva). Una posición REDUCIENDO
     conserva la regla de antes (solo la cantidad que queda en el intermediario, RM-06).

   La cantidad declarada del registro es SIEMPRE lo que el operador vendió (igual que el cierre total
   declara la venta entera); lo que queda es `p["cantidad"] - cantidad`.

2. **ejecucion_g.py (`declarar_manual`, rama POSICION).** Si la posición no está REDUCIENDO y lo declarado
   es una parcial (el mismo criterio: `p["cantidad"] - cantidad > TOL`), G lo contrasta con el intermediario
   en la nueva `_declarar_parcial`, en este orden:

   - la orden `proteccion_ref` debe estar ACEPTADA, ser de tipo STOP, del lado contrario a la posición
     (VENTA en un LARGO, COMPRA en un CORTO), del mismo instrumento y vía de acceso que la posición, con
     cantidad igual a lo que queda y precio igual a `p["stop_precio"]`; si no, G-10;
   - el neto del intermediario en ese instrumento debe ser exactamente lo que queda, medido EN EL SENTIDO
     DE LA POSICIÓN (`neto * signo`, con `signo = +1` en un LARGO y `-1` en un CORTO, como hace `_reducir`):
     así un giro completo de la posición no cuadra; si no, G-10;
   - los dos contrastes de cantidad (stop nuevo y neto) son ABSOLUTOS: `_cuadra_abs(x, y) = abs(x - y) <= TOL`
     con el TOL = 1e-6 del módulo, la misma medida que aplican después TOL_Q del Orquestador, la conciliación
     (CANTIDAD con TOL = 1e-6 y `tolerancia_conciliacion_rel` = 0.0) y su control de protección, y el mismo
     control absoluto que usa el cierre total para su neto (G-10); una banda relativa daría por buena una
     parcial que la conciliación inmediata reportaría como discrepancia kill-switch (revisión T-44, hallazgo 1);
   - si alguno de los stops viejos de la posición (los de `p["protecciones"]`) ya se ejecutó o se ejecutó
     en parte, G-10: ese cambio lo concilia H (H-01), no lo explica la venta declarada;
   - solo después cancela los stops viejos (`_stops_de`, salvo el nuevo) con el mismo bucle de 3 intentos
     del cierre total y, además, reconsultando tras cada cancelación (no se fía de la respuesta: comprueba
     que el stop de verdad se fue, como hace `_cerrar`); si alguno sigue vivo, G-10 y no se registra nada
     (la posición no queda nunca sin su stop viejo antes de tiempo ni con dos stops sin explicar);
   - el cierre total no cambia ni una línea.

3. **orquestador.py (`registrar_manual`, rama POSICION parcial).** Antes de mutar, `_reglas_manual` ya lo
   validó (RM-01/RM-04/RM-05/RM-06/RM-07/RM-11/RM-12, O-03 por orden usada). Después, todo de una vez:

   - `p["protecciones_anteriores"] += p["protecciones"]` sin repetidos;
   - `p["protecciones"] = [proteccion_ref]`;
   - añade `proteccion_ref` y `ref_intermediario` a `self.ordenes_usadas` (ninguno puede estar ya, lo
     garantiza O-03);
   - añade a `p["reducciones"]` un elemento `{"n", "cantidad" (lo vendido), "desde", "restante",
     "manual": True, "orden_id": ref_intermediario, "terminada_en": ahora, "motivo"}`;
   - resta lo vendido a `p["cantidad"]`;
   - anota con `self._anota_pos(p, p["estado"], p["estado"], "OPERADOR", ahora, "reducción parcial manual
     declarada (CT-G-14): <motivo>", ref_intermediario)`: la anotación lleva el hash del estado nuevo
     (`_estado_pos`) y la posición se queda en su estado (ABIERTA o EN_REVISION). El registro queda además
     en `self.manuales` y en `self.eventos`, como cualquier CT-G-14.

   Con esto `o.integridad() == []` y `o.posicion_integra(pid)` siguen en verde: la única anotación nueva
   cuadra con el estado mutado (lo comprueba la batería en el caso bueno, en EN_REVISION y en las dos
   parciales seguidas).

4. **El mínimo de F convertido (`_valor_min_restante`, nuevo método del Orquestador).** La política de F
   fija `valor_min_eur` en euros, pero lo que queda se valora en la divisa de cotización del instrumento
   (el precio del registro y el stop están en esa divisa). El Orquestador — que sí conoce la política
   (`cfg["politica_f"]`) y el último tipo de cambio conocido (`ultima_foto` de G, la misma fuente que usa
   T-33 para valorar las LIBRES) — entrega en el ctx el mínimo YA convertido a la divisa de cotización:
   `valor_min_restante_eur = valor_min_eur / fx`, con `fx = tipo_cambio(self.divisa(instrumento),
   self.ultima_foto)`. Si la política no tiene un `valor_min_eur` utilizable, o no hay tipo de cambio
   válido (foto ausente, fx <= 0, no finito), devuelve None y manual_g rechaza la parcial con RM-12
   (falla cerrado: sin poder valorar el resto, lo prudente es cerrarla entera). El nombre del campo es el
   de las directrices; su unidad es la divisa de cotización, y así está documentado en los dos módulos.

5. **Conciliación: un control nuevo; H: sin cambios.** Tras una parcial correcta por G, el Orquestador tiene
   la cantidad nueva, el stop vivo nuevo en `p["protecciones"]` (cantidad exacta, precio de la posición, lado
   y vía correctos) y los stops viejos cancelados en el intermediario: todas las comprobaciones de
   `conciliar` pasan tal cual y H vigila la posición igual que antes (el stop nuevo está en
   `p["protecciones"]`, así que ni H-01 (no hay stops ejecutados) ni H-07 (la conciliación está limpia) se
   disparan). Pero por el camino directo (`o.registrar_manual` sin G) nadie cancela los stops viejos en el
   intermediario (límite de T-32): la mutación los saca de `p["protecciones"]` y los guarda en
   `p["protecciones_anteriores"]`, que ni `_stops_de` ni `conciliar` miraban — un stop viejo vivo habría
   quedado invisible para la conciliación, un estado imposible o visible antes de T-44 (revisión T-44,
   hallazgo 2, gravedad alta). `conciliar` comprueba ahora, para todas las posiciones y antes de la rama
   CERRADA, que cada stop de `p["protecciones_anteriores"]` esté CANCELADA en el intermediario; si sigue
   vivo (ACEPTADA), a medias (PARCIAL) o se ejecutó (EJECUTADA), PROTECCION_HUERFANA («el stop retirado X no
   está cancelado (estado)»), tipo que ya está en TIPOS_KILL. El control va antes del «continue» de
   STOP_EJECUTADO para que la ejecución fuera de control de un stop retirado no pueda quedar explicada como
   cierre propio, y `_stops_de` no cambia (el camino por G y `_reducir` conservan su semántica exacta). El
   patrón de T-12 se mantiene: quien declara por el camino directo retira antes el stop viejo (como hace G
   por el suyo) y la conciliación queda limpia; si no lo retira, la conciliación lo ve. Lo verificado en la
   batería: la conciliación limpia tras la parcial (por G, y por el Orquestador con el viejo retirado), tras
   dos parciales y tras el cierre total posterior; el stop viejo vivo del hallazgo se reporta con
   PROTECCION_HUERFANA; y una pasada de H sin incidencias.

6. **Batería nueva (`pruebas/pruebas_manual_t44.py`, 47 comprobaciones).** Parte de una posición abierta en
   L1 (la misma `abierta_l1` de `pruebas_manual.py`) con una política de F con `valor_min_eur` bajado a
   20.0 [solo para la prueba; el valor oficial es 100.0, D-11], porque con la posición de prueba (100 EURUSD
   a 1,10 = 110 EUR) y el mínimo oficial no cabría ninguna parcial. Cubre el caso bueno (por G y por el
   Orquestador), todos los rechazos de G (G-10) y del Orquestador (O-01 con RM-01/RM-06/RM-07/RM-12), una
   posición REDUCIENDO, el duplicado (O-03), dos parciales seguidas, el cierre total posterior, la
   simetría CORTO (el operador compra a mano; cazó el defecto del neto con signo, ver §4), una pasada de
   H sin incidencias y las cinco regresiones de la revisión independiente: los desfases de la parcial se
   miden en absoluto (3e-5 fuera de banda → G-10 con el stop por lo declarado y con el stop por lo real;
   5e-7 dentro de la banda → aceptada con la conciliación inmediata limpia) y los stops retirados son
   visibles para la conciliación (stop viejo vivo tras el registro directo → PROTECCION_HUERFANA;
   retirado antes, patrón de T-12 → conciliación limpia).

7. **Pruebas antiguas que cambian (mínimo, ver §4).** La comprobación `cierre_parcial_RM06` de
   `pruebas_manual.py` esperaba RM-06 para un cierre parcial: con T-44 esa declaración es una reducción
   parcial sin stop nuevo y ahora la rechaza RM-07 (comportamiento nuevo, más preciso). Se cambia a
   RM-07 con nombre nuevo y se añade una que sigue exigiendo RM-06 cuando la cantidad supera la posición.
   Lo mismo ocurre con `M9_declaracion_rechazada_no_quita_el_stop` de `pruebas_reduccion.py` (una parcial
   sin stop declarada sobre una posición ya reducida): pasa de RM-06 a RM-07, conservando lo que esa
   comprobación protege (el rechazo llega antes de tocar el intermediario y el stop sigue vivo).

## 3. Reglas y comprobaciones

| Código (regla o aviso) | Qué comprueba | Efecto |
| --- | --- | --- |
| RM-06 (texto nuevo) | Se declara más cantidad de la que tiene la posición (`cantidad > p["cantidad"] + 1e-6`); el cierre total es con la cantidad exacta. También una reducción parcial con `cantidad <= 1e-6` | Rechazo del registro (O-01), sin tocar nada |
| RM-07 (ampliada) | Una reducción parcial (T-44) exige declarar el stop nuevo que el operador ya colocó por lo que queda, igual que una entrada exige el suyo | Rechazo del registro (O-01) |
| RM-12 (nueva) | Lo que queda (`p["cantidad"] - cantidad`) valorado con el precio del registro no llega al mínimo de F convertido (`valor_min_restante_eur`), o no se puede valorar (mínimo o tipo de cambio ausente, producto que desborda) | Rechazo del registro (O-01): «ciérrala entera» |
| RM-01 a RM-05, RM-08 a RM-11 | Sin cambios: forma, emisor, instantes, vínculo, coincidencia, mandato, LIBRE y envoltura | Como antes |
| O-03 | La orden ejecutada o el stop nuevo ya están registrados en el Orquestador (duplicado) | Rechazo con O-03 |
| O-13 | El expediente o la posición vinculados no son íntegros | Kill-switch y rechazo, como antes |
| G-10 (ampliado) | En la parcial: el stop nuevo no es un stop vivo por lo que queda (estado, tipo, lado, instrumento, vía, cantidad o precio, con contraste de cantidad ABSOLUTO con el TOL de G), el neto no queda exactamente en lo que queda en el sentido de la posición (mismo contraste absoluto), un stop viejo ya saltó o no se pudo cancelar de verdad (reconsulta tras cada intento) | G no registra nada y el intermediario queda como estaba (los stops viejos solo se cancelan cuando todo lo demás ha cuadrado) |
| PROTECCION_HUERFANA (ampliada) | La conciliación comprueba que cada stop que una posición ya retiró (`protecciones_anteriores`, T-44) esté CANCELADA en el intermediario; si sigue vivo, a medias o se ejecutó, lo reporta | Discrepancia de la clase kill-switch (el tipo ya estaba en TIPOS_KILL): G informa y el Orquestador degrada |
| O-01/O-06/O-10/O-25 y el resto de códigos | Sin cambios | Como antes |

## 4. Códigos, API, pruebas y revisión independiente

Funciones nuevas o cambiadas:

- `validador/manual_g.py`: nueva `_parcial_manual(reg, p, ctx)` (las reglas RM-06/RM-07/RM-12 de la
  parcial; nunca lanza: la envuelve el try de `validar_manual`); `_validar_plano` deriva a ella en la rama
  POSICION cuando `p["estado"] != "REDUCIENDO"` y `cantidad < p["cantidad"] - 1e-6`; el docstring de
  `_validar_manual` documenta la clave nueva del ctx (`valor_min_restante_eur`); cabecera del módulo con
  RM-12 y textos de RM-06/RM-07 actualizados.
- `validador/ejecucion_g.py`: nueva `_declarar_parcial(o, registro, plano, p, broker, ahora)`; `declarar_manual`
  (rama POSICION) deriva a ella cuando la posición no está REDUCIENDO y `p["cantidad"] - cantidad > TOL`
  (el cierre total queda intacto); los contrastes de cantidad de la parcial (stop nuevo y neto) usan la
  comparación absoluta `_cuadra_abs` con el TOL del módulo (revisión T-44, hallazgo 1); `conciliar` añade el
  control de los stops retirados (`protecciones_anteriores` deben estar CANCELADA; si no,
  PROTECCION_HUERFANA — revisión T-44, hallazgo 2); errores del intermediario → G-01 (sin conexión) o G-10
  (lo declarado no cuadra), nunca se registra nada a medias.
- `validador/orquestador.py`: `registrar_manual` (rama POSICION) con la mutación de la parcial descrita en
  §2 punto 3; `_reglas_manual` añade `"valor_min_restante_eur"` al ctx de `validar_manual` (None si no hay
  posición vinculada); nuevo método `_valor_min_restante(ins)` (el mínimo de F convertido; nunca lanza).

Batería nueva: `pruebas/pruebas_manual_t44.py`, 47 comprobaciones (validador puro: 9; camino bueno por G:
9; camino bueno por el Orquestador: 3, incluidas las dos regresiones del hallazgo 2; rechazos y estado del
Orquestador: 8; rechazos y contraste de G: 10, incluidas las tres regresiones del hallazgo 1, una de ellas
de aceptación dentro de la banda; comprobar_manual sin efectos: 2; secuencias y simetría CORTO: 6).
Determinista: dos ejecuciones consecutivas producen la misma
salida. Con el código de V0.40 la batería no es vacua: falla enseguida (la parcial acaba en RM-06 y el caso
bueno no llega a registrarse).

Pruebas antiguas que cambian (2 ficheros, 3 líneas de comprobaciones):

- `pruebas/pruebas_manual.py`: `cierre_parcial_RM06` pasa a `cierre_parcial_sin_stop_RM07` (espera RM-07 en
  lugar de RM-06) y se añade `cierre_de_mas_sigue_RM06` (cantidad 150 > 100 sigue en RM-06). Por qué es
  correcto lo nuevo: la declaración de una parte es ahora una reducción parcial y su defecto específico es
  no llevar el stop nuevo (RM-07, la regla que la directriz pide); RM-06 queda para lo que de verdad no
  cabe (más de lo que hay) y para la parcial sin cantidad positiva. La comprobación protege lo mismo (el
  rechazo y el estado intacto) con la regla nueva.
- `pruebas/pruebas_reduccion.py`: `M9_declaracion_rechazada_no_quita_el_stop` espera RM-07 en lugar de
  RM-06 por lo mismo (la posición ya reducida a 60 y la declaración de 30 sin stop nuevo): lo que protege
  la comprobación —el rechazo llega antes de que G consulte o toque el intermediario y el stop
  redimensionado sigue vivo— no cambia.

Revisión independiente: ejecutada (sección 7 de las directrices, en otra conversación, con el prompt «Prompt
para el revisor — V0.41») con resultado de dos hallazgos, ambos corregidos (detalle completo en `revision.md`):

| # | Gravedad | Dónde | Defecto | Arreglo | Regresiones |
| --- | --- | --- | --- | --- | --- |
| 1 | media | `ejecucion_g._declarar_parcial` | Los contrastes de cantidad (stop nuevo y neto) eran relativos (`_cuadra`, 1e-6·max(1,\|y\|)) mientras toda la cadena posterior mide absoluto (TOL_Q del Orquestador, conciliar con TOL=1e-6 y tolerancia relativa 0.0, control de protección, y el cierre total con su control absoluto): una parcial con desfase de 3e-5 se registraba con OK y la conciliación inmediata reportaba kill-switch | Comparación absoluta `_cuadra_abs` (`abs(x - y) <= TOL`) en los dos contrastes | `G_desfase_lo_declarado_G10`, `G_desfase_lo_real_G10`, `G_desfase_dentro_de_la_banda_consistente` |
| 2 | alta | `ejecucion_g.conciliar` (con `orquestador.registrar_manual`) | Los stops que la parcial retira (`protecciones_anteriores`) eran invisibles para `_stops_de` y `conciliar`; por el camino directo (sin G) nadie los cancela: un stop viejo vivo quedaba fuera de todo control y la conciliación lo daba limpio | `conciliar` exige que cada stop retirado esté CANCELADA; si no, PROTECCION_HUERFANA (kill-switch), antes del «continue» de STOP_EJECUTADO y sin tocar `_stops_de` | `directo_stop_viejo_vivo_lo_ve_la_conciliacion`, `directo_con_el_viejo_retirado_concilia_limpio` |

Los tres ficheros del revisor (`hallazgo_t44_1_conciliacion_tras_parcial_con_desfase.py`,
`hallazgo_t44_2_stop_viejo_vivo_invisible_a_conciliacion.py` y `sondas_t44_revisor.py`) quedan intactos byte
a byte en la raíz de `marcoC/`; los dos primeros FALLABAN (exit 1) contra la versión entregada y dan OK tras
la corrección. El auto-repaso previo a la entrega se conserva abajo.

Auto-repaso del paso 6, con una corrección real: la sonda de la
simetría CORTO destapó que `_declarar_parcial` comparaba el neto del intermediario (con signo) contra lo
que queda (sin signo) —en un corto, −60 frente a 60, G-10 indebidamente—; corregido midiendo el neto en el
sentido de la posición (`neto * signo`, el mismo criterio de `_reducir`), de modo que un giro completo de la
posición tampoco cuadra (fail-open evitado), y fijado en la batería con tres comprobaciones CORTO
(`parcial_en_corto_ok`, `parcial_en_corto_stop_y_conciliacion`, `parcial_en_corto_resto_minimo_RM12`). Los
demás caminos repasados: no hay mutación antes de validar (`_reglas_manual` y `_valor_min_restante` son de
solo lectura; las mutaciones van después de todas las comprobaciones), nada lanza hacia fuera (la
`_parcial_manual` está bajo el try de `validar_manual`; `declarar_manual` captura `ConexionPerdida` → G-01
y cualquier otra excepción → G-10; `comprobar_manual` nunca lanza), y los casos frontera están en la
batería (cantidad exacta ± tolerancia, parcial sin cantidad positiva, resto justo por debajo del mínimo,
precio cero, precio que desborda, sin tipo de cambio, duplicado, REDUCIENDO).

Número de baterías que pasan: 39 ejecuciones (el bucle de la sección 0: `pruebas/ejecutar_pruebas.py` + las
38 baterías de `pruebas/pruebas_*.py`, incluida la nueva), todas terminan en «TODAS LAS PRUEBAS PASAN» y
sin ninguna línea FALLA.

## 5. Límites y deuda técnica

- La reducción parcial a mano solo existe para posiciones ABIERTA o EN_REVISION. En REDUCIENDO el registro
  manual sigue siendo el cierre del resto del intermediario (regla de antes, RM-06): mezclar una parcial a
  mano con una reducción de G a medias dejaría dos criterios de cantidad sobre el mismo intermediario.
- El resto se valora con el precio del propio registro, no con el mercado del momento: es el precio que G
  contrasta contra el fill real del intermediario (G-10 si no cuadra), y usar otro precio añadiría una
  fuente no verificable al mínimo de F. Si el mercado se movió después de la venta, el mínimo se mide al
  precio de la venta, que es el dato que el operador declara y el intermediario confirma.
- El mínimo del resto no es un control nuevo de F: es el `valor_min_eur` de la política (D-11, valor
  oficial 100.0 [PROPUESTO]) aplicado a lo que queda, convertido con el último tipo de cambio de la última
  foto de G. Sin foto o sin tipo para esa divisa, la parcial se rechaza (RM-12) y el camino prudente es el
  cierre entero, que no deja resto que valorar.
- `registrar_manual` llamado directamente (sin G) sigue sin contrastar el intermediario (limitación ya
  anotada de T-32): las comprobaciones del intermediario son de `declarar_manual`/`_declarar_parcial`.
  El Orquestador, por su lado, valida forma, reglas, duplicados e integridad igual para ambos caminos.
  Lo que la cadena garantiza desde la revisión es la visibilidad y la misma medida: `conciliar` vigila los
  stops retirados (`protecciones_anteriores` deben estar CANCELADA; si no, PROTECCION_HUERFANA) y los
  contrastes de cantidad de la parcial son absolutos con el TOL de G, la misma banda que aplican TOL_Q del
  Orquestador y la conciliación, de modo que una parcial que G da por buena no puede llevar una discrepancia
  inmediata.
- La anotación de la reducción manual lleva `manual: True` y el `orden_id` de la venta declarada; los stops
  retirados quedan en `protecciones_anteriores`, como en una reducción de G. No hay un registro aparte de
  «quién colocó el stop nuevo»: el CT-G-14 del operador lo declara y G lo verifica vivo en el intermediario.
- Filas de deuda que cambian: **T-44 queda RESUELTO** («RESUELTO en V0.41: CT-G-14 vinculado a una POSICION
  admite la reducción parcial declarada a mano con el stop nuevo por lo que queda (RM-07) y el mínimo de F
  para el resto (RM-12); G lo contrasta y la conciliación queda limpia»). La fila T-12 decía «quedan T-43
  y T-44»: queda T-43. Ninguna fila D nueva (el `valor_min_eur` aplicado al resto es el de D-11, ya abierta).
