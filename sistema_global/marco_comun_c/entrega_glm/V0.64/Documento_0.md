# Documento 0 — panel con el estado del sistema (V0.64) — GLM, pendiente de revisión

## 1. Problema y alcance

El panel de la consola (`consola.panel`) mira la integridad, los datos de K, el presupuesto, los avisos y las decisiones pendientes, pero no dice nada de lo más grave: si el kill-switch está activo, qué carteras están degradadas, si el reloj del sistema está bloqueado o sin contrastar, o si el diario está bloqueado o lleva demasiadas líneas sin un punto de control. El operador que solo mira el panel puede no enterarse de que el sistema ha dejado de operar (§6 de la Constitución: la consola es la vista del operador). Entra en esta versión:

- `consola.panel(o, ahora, reloj=None, diario=None, lineas_diario_ambar=1000)`: los dos parámetros son opcionales; sin ellos el panel sale como hoy (las cinco comprobaciones de siempre) más los dos apartados nuevos que no dependen de ellos, «kill_switch» y «autonomia»;
- la comprobación «kill_switch»: ROJO si `o.kill` no es None, con el actor, el motivo y el instante; VERDE si no (y si hubo rearmes, menciona el último);
- la comprobación «autonomia»: ÁMBAR si hay carteras en `o.degradadas`, con cuáles, a qué nivel efectivo están (`o.nivel(cartera)`), por qué y desde cuándo; VERDE si no;
- la comprobación «reloj», solo si se pasa `reloj`: ROJO si `reloj.bloqueo` no es None (con el código y el motivo); ÁMBAR si aún no se ha contrastado, si hace falta otro contraste o si no se puede confirmar el contraste; VERDE si no. Para saber si falta el contraste NO se llama a `reloj.ahora()` (cambiaría su estado): `reloj.py` estrena un método de solo lectura `estado()` (el único cambio fuera de `consola.py`);
- la comprobación «diario», solo si se pasa `diario`: ROJO si el diario está bloqueado (lee `diario._roto`); ÁMBAR si el diario lleva más de 1.000 líneas desde el último PUNTO (el número sale de `diario._n`; el umbral es el valor por defecto del parámetro `lineas_diario_ambar`, [PROPUESTO]); VERDE si no;
- la comprobación «migracion», solo si la última entrada de `o.limites["entradas"]` es una MIGRACION: una línea VERDE informativa «migrado a este código el … (MIG-…)».

Queda fuera: cualquier cambio en el Orquestador, en G/H/F/E/D o en el resto de la infraestructura T-03; un método público para el estado del diario (se propone como deuda T-63, no se implementa aquí: la pieza manda leer los privados `_roto` y `_n` y anotar la propuesta); el contenido de la consola más allá del panel (la cola y los avisos no cambian); los umbrales nuevos no van a una fila D nueva: van a la D-09 que ya existe (umbrales de la consola).

## 2. Diseño

**Todo en `consola.py` (y una función en `reloj.py`).** La consola sigue siendo de solo lectura: las comprobaciones nuevas leen atributos y llaman a métodos que no mutan (`o.nivel`, `Reloj.estado`), cada una dentro de su propio `try` para que un `reloj` o un `diario` imposibles no salgan disparando (fallan cerrado a ROJO), y todo el conjunto dentro del `try` de `panel`, que sigue devolviendo ROJO si algo se escapa. El `nivel` global del panel sigue siendo el peor de todas las comprobaciones (`_peor`).

**El orden del panel.** Las comprobaciones de siempre salen igual que hoy (integridad, datos, presupuesto, avisos, decisiones) y detrás van las nuevas, en este orden: kill_switch, autonomia, reloj (solo con `reloj`), diario (solo con `diario`) y migracion (solo si toca). Sin `reloj` ni `diario` el panel es el de hoy más kill_switch y autonomia: `pruebas_consola.py`, que mira las comprobaciones por nombre, no cambia.

**Kill-switch y rearmes.** `o.kill` es None o `{"motivo", "actor", "ahora"}`: con kill activo, el motivo del ROJO lleva los tres («kill-switch activo (OPERADOR): … desde 2026-11-06T09:00:00+00:00»); si el objeto no es un diccionario legible, ROJO igualmente con lo que se pueda imprimir (falla cerrado). VERDE cuando no hay kill; si `o.rearmes` no está vacío, el motivo menciona el último rearme («sin kill-switch activo; último rearme …») — el `ahora` de `o.rearmes[-1]`.

**Autonomía.** `o.degradadas` es un diccionario cartera → `{"motivo", "ahora"}`. Con cualquiera, ÁMBAR listando cada cartera con su nivel efectivo (`o.nivel(cartera)`, que devuelve L1 aunque la configuración diga otra cosa), su motivo y su instante, ordenado por nombre para que el panel sea determinista; sin ninguna, VERDE.

**El reloj y `Reloj.estado()`.** El método nuevo de `reloj.py` es de solo lectura: no toca `_ancla`, `_ultima`, `_suelo`, `_contraste`, `bloqueo` ni `incidentes`, y no lee la pared (no avanza nada): devuelve `{"bloqueo": copia o None, "contrastado": bool, "segundos_desde_contraste": float o None, "incidentes": n}`. Los segundos salen del monótono menos el monótono del último contraste bueno; si el monótono no da un número finito o da un valor por detrás del contraste, `segundos_desde_contraste` es None (no se puede afirmar nada: la consola lo trata como «hace falta comprobar el contraste», ÁMBAR). Nunca lanza: si algo inesperado falla, devuelve la foto prudente (`contrastado: False`, segundos None), que la consola pinta ÁMBAR (o ROJO si hay `bloqueo`). La consola combina: ROJO si `reloj.bloqueo` no es None (con su código y motivo); ÁMBAR si `contrastado` es False, si los segundos son None o si pasan de `reloj.max_sin_contraste_s` (el tope del propio reloj, sin constantes nuevas); VERDE si no.

**El diario.** La consola lee dos privados del `Diario`: `_roto` (None o el motivo del bloqueo: DI-05, DI-06 u otra marca) y `_n` (el número de la última línea, que `punto()` deja en 1: son las líneas desde el último PUNTO). Es privado y se lee desde la consola porque la consola es parte del sistema (lo anota esta pieza y propone en la deuda T-63 un método público `estado()` del diario para no depender de los privados). ROJO con `_roto` truthy (el motivo lleva la marca), ÁMBAR con `_n` por encima del umbral (por defecto 1.000, [PROPUESTO], como valor por defecto de `lineas_diario_ambar` y así no hay constantes nuevas en mayúsculas en `consola.py`), VERDE si no. Si lo que llega no es un `Diario` (un texto, un número, otro objeto sin esos atributos) o `_n` no es un entero de verdad (bool incluido), la comprobación sale ROJO «diario ilegible»: nunca se pinta VERDE un diario del que no se puede leer el estado.

**La última migración.** Las entradas de `o.limites["entradas"]` van pareadas con `o.limites["historial"]` (misma longitud, `ref` igual al `tipo`, lo exige `_limites_ok`), y la anotación de una MIGRACION lleva el instante en el `ahora` del historial y los identificadores en la entrada (`"migraciones"`: la lista de MIG-…). Si la última entrada es una MIGRACION, línea VERDE «migrado a este código el {ahora} ({MIG-…})»; si la entrada está ahí pero no se puede leer el instante o los identificadores, ROJO (falla cerrado); si la última entrada no es una MIGRACION, no hay línea.

**Números.** Un único valor nuevo: el umbral de líneas del diario, 1.000 [PROPUESTO] como valor por defecto de `lineas_diario_ambar` (va a la fila D-09, umbrales de la consola). No hay códigos nuevos ni constantes nuevas en mayúsculas: `consola.py` no estrena ninguna (el esquema del código no cambia y no hay migración) y `reloj.py` solo estrena un método.

## 3. Reglas y comprobaciones

No hay códigos nuevos: el panel reutiliza los existentes y hace visibles los estados que ya producían códigos. La batería exige lo que el diseño manda en cada caso.

| Código | Qué exige la batería | Efecto comprobado |
| --- | --- | --- |
| RL-01 | un salto de la pared respecto al monótono (`Fuentes`) bloquea el reloj | la comprobación «reloj» sale ROJO con el código y el motivo, y el panel entero ROJO |
| RL-04 (visible) | reloj sin contrastar, rearmado, o con el contraste pasado de `max_sin_contraste_s` | la comprobación «reloj» sale ÁMBAR pidiendo el contraste, sin leer `ahora()` |
| DI-06 (visible) | un cambio por fuera del diario (`cotizaciones`) y la operación siguiente que lo para | la comprobación «diario» sale ROJO con la marca y el resto del panel sigue calculado |
| DI-05 (visible) | `_roto` con otra marca | el motivo del ROJO lleva la marca del bloqueo |
| O-26 (visible) | kill-switch activo (`activar_kill_switch`) | «kill_switch» ROJO con actor, motivo e instante y el panel entero ROJO |
| O-19 (visible) | una cartera degradada con su aviso sin acusar | el panel es ROJO hasta acusar el aviso y ÁMBAR después (autonomia); «autonomia» sale ÁMBAR en ambos casos |
| MG-01 a MG-04 (visibles) | una migración real (`a_010_v045` → `migrar`) | la línea VERDE informativa con el instante y los MIG; sin migración no hay línea |

No se cambia ninguna regla existente y ninguna prueba antigua se toca: `pruebas_consola.py` pasa sin cambios y no hay códigos ni constantes nuevas (el umbral del diario es un parámetro, así que el esquema del código no cambia y no hay migración).

## 4. Códigos, API, pruebas y revisión independiente

Funciones nuevas o cambiadas: `consola.panel(o, ahora, reloj=None, diario=None, lineas_diario_ambar=1000)` (firma nueva: los dos primeros parámetros como hoy) con los ayudantes privados `_add_seguro` (lo imposible ROJO sin salir del panel), `_kill`, `_autonomia`, `_reloj`, `_diario` y `_migracion`; en `reloj.py`, el método nuevo `Reloj.estado()` de solo lectura (el único cambio fuera de `consola.py`). Nada más: sin cambios en el Orquestador, en G/H/F/E/D, en el diario ni en la persistencia.

Batería nueva: `pruebas/pruebas_consola_sistema.py`, 42 comprobaciones, ~2 s (límite de la pieza: 3 minutos). Determinista: dos ejecuciones dan la misma salida byte a byte (comprobado antes de entregar). Pruebas antiguas que cambiaron: ninguna (las 53 anteriores pasan sin tocarlas; el lote completo son 54 baterías, 0 con fallos, ver `salida_pruebas.txt`).

Defectos encontrados al montar la batería (ninguno de producto; el sistema se comportó como el diseño manda en cada caso):

- **h01 (constatación, fijada por la batería):** degradar una cartera emite el aviso O-19 y `PRIORIDAD_AVISO` lo marca de prioridad ALTA: con una cartera degradada y el aviso sin acusar, el panel es ROJO por «avisos» y ÁMBAR por «autonomia»; acusado el aviso (la degradación sigue), queda ÁMBAR por «autonomia». La batería exige las dos cosas: así el color del panel nunca esconde una cartera degradada.
- **h02 (del montaje, sin cambio):** la provocación DI-06 del patrón de `pruebas_reloj_t03` (añadir a mano un aviso mal formado) rompe además el cálculo del resto del panel: `avisos_pendientes` se queda sin la clave `acuse` y `panel` responde el ROJO único de siempre. La batería provoca el DI-06 con una mutación que el resto del panel no lee (`cotizaciones`), para poder exigir que la comprobación «diario» salga ROJO **con el resto del panel calculado**. El ROJO único ante un aviso roto es el comportamiento de hoy (el `try` de `panel`) y no se cambia en esta pieza.

La revisión independiente se hace después, en otra conversación (prompt de la sección 9 de las directrices); sus hallazgos se recogerán en `revision.md`. El revisor debería mirar, además de lo suyo, una propiedad que la batería podría exigir y no exige (por ejemplo, que «reloj» siga ROJO tras `degradar_por_reloj`, o la comprobación «diario» con un diario con clave).

## 5. Límites y deuda técnica

- La consola muestra, no arregla: el panel dice ROJO/ÁMBAR con el motivo, pero rearmar el reloj, reabrir el diario, acusar avisos y restablecer niveles siguen siendo acciones del operador por sus métodos de siempre.
- «reloj» solo sale si el llamador pasa el reloj, y «diario» solo si pasa el diario: sin ellos el panel no puede decir nada de ellos (no los adivina).
- La comprobación «diario» lee dos privados del `Diario` (`_roto` y `_n`): la consola es parte del sistema y la pieza lo anota; la deuda **T-63** (nueva) propone un método público `estado()` del diario para no depender de los privados.
- El umbral de líneas del diario (1.000, [PROPUESTO]) es el valor por defecto de `lineas_diario_ambar` y va a la fila **D-09**, que ya existe (umbrales de la consola): no hay fila D nueva.
- La línea «migracion» solo mira la ÚLTIMA entrada del registro de límites: una migración seguida después de un CAMBIO del operador no se muestra (es informativa del código actual, por diseño de la pieza).
- Los segundos del contraste salen del monótono: si el monótono va por detrás del contraste o no da un número finito, `estado()` devuelve None y la consola pinta ÁMBAR (no se puede afirmar nada), nunca VERDE.
- Filas de deuda que cambian: T-63 nueva; D-09 recoge el umbral nuevo. El fichero `Deuda_tecnica.md` no viaja en el ZIP y su contenido va resumido en `notas_deuda.md` de esta entrega.
