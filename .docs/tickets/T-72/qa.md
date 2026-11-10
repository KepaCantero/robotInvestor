# T-72 · QA independiente

- **Revisor:** Claude, como revisor nuevo sin el contexto de la implementación (solo el plan, el código y el diff) · **Ronda:** r01 · 10-11-2026

## Ronda r01

### Qué se revisó

El trabajo de T-72 (V0.69) se revisó sin commit en el árbol de trabajo. Durante la revisión otra sesión lo dejó en el commit `61d3973` («pendiente de QA»), con el mismo contenido. La base de comparación es `8d74622` (V0.68).

Cambian:

- `sistema_global/marco_comun_c/validador/reloj.py`
- `sistema_global/marco_comun_c/validador/diario.py`
- `sistema_global/marco_comun_c/validador/consola.py`
- `sistema_global/marco_comun_c/pruebas/pruebas_reloj_diario_t72.py` (nueva)
- `sistema_global/marco_comun_c/pruebas/pruebas_consola_sistema.py`
- `sistema_global/marco_comun_c/LEEME.md`
- `sistema_global/documentos_0/V0.69_Estado_del_diario_y_tolerancias_del_reloj.md`
- `CLAUDE.md`, `sistema_global/README.md`, el briefing y la deuda (filas T-72 y T-85)

Origen: H-05 y H-06 de `.docs/tickets/T-79/qa.md`.

### Reproducción desde limpio

- **Baterías del marco:** `.docs/scripts/pruebas_marco.sh` da «58 pasan, 0 fallan». La batería nueva tiene 24 comprobaciones, como dicen el LEEME y el ticket.
- **LEEME frente al disco:** `.docs/scripts/leeme_marco.py` da «SIN DIFERENCIAS (0)».
- **Gate:** `./tools/check_all.sh` sobre un worktree limpio de `61d3973` da 12/12.
- **Esquema:** `persistencia.esquema_actual()` es `9eade73e…94cd8` en `8d74622` y en el árbol: no cambia.
  - `reloj.py`, `diario.py` y `consola.py` no están en el esquema.
  - `estado_diario()` y `_tol` no entran en `vars(o)` del Orquestador, así que el estado guardado tampoco cambia.
- **La batería nueva sobre el código de la V0.68** (copia de `8d74622` con la batería y la prueba de consola nuevas): falla. Tres FALLA de solo lectura y un AttributeError en `_tol`. Se confirma que «falla con la V0.68».
- **Las pruebas de `8d74622` sobre el código nuevo:**
  - `pruebas_reloj_t03.py`, `pruebas_consola.py`, `pruebas_consola_sistema.py` y `pruebas_robustez_t03.py` dan en el árbol la misma salida que en HEAD (quitando los tiempos).
  - La única que falla es `diario_ilegible_es_rojo` en la versión vieja de `pruebas_consola_sistema.py`. Su `DiarioFalso` sin `estado_diario()` sigue siendo ROJO, pero con el motivo «no da su estado» en lugar de «número de líneas». Es el ajuste que declara el Documento 0 (§3) y está justificado.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Sonda r01_03, 136 comprobaciones sin hallazgos. Cubre: un cambio por fuera (un valor, NaN, una lista hecha tupla, otro orden de claves, un atributo nuevo o quitado); el fichero con una línea añadida, en otro inodo con los mismos bytes o quitado; otro Diario que escribe en los mismos ficheros; todo ello también con clave. En cada caso la foto dice «no sincronizado», el panel es ROJO, mirar no bloquea y la operación siguiente da DI-06 con el mismo motivo. |
| CA-2 | sí | Sonda r01_04: un espía registra cada atributo que la consola pide al objeto `diario`, y solo pide `estado_diario`. En `consola.py`, `_roto` y `_n` solo aparecen en la docstring. |
| CA-3 | sí, en lo que dice | Las tres tolerancias son propiedades sin setter: `setattr`, `delattr` y `object.__setattr__` se rechazan, y escribir en `__dict__` no tiene efecto. Con NaN en `_tol`, en cualquier posición, no hay instantes ni VERDE y el reloj no lanza (sonda r01_02). Con otros valores privados no vale lo mismo: ver H-01 y H-02. |
| CA-4 | sí | 58 de 58 baterías y gate 12/12. |

### Comportamiento con tolerancias sanas: idéntico al de antes

La sonda r01_01 carga el `reloj.py` de `8d74622` y el del árbol y los ejecuta en paralelo con las mismas fuentes simuladas.

- **Casos:** los bordes exactos de cada tolerancia (salto, deriva desde el ancla, suelo, desfase y contraste), con 0 y con ±0,001 y ±2⁻²⁰ a cada lado, más 4.000 secuencias aleatorias (semilla 20261110).
- **Resultado:** 33.452 comparaciones del resultado, del estado interno y de `estado()`, sin ninguna diferencia.
- **La sonda detecta los cambios:** si `_dentro` usa `<` en lugar de `<=`, salen diferencias en el borde exacto del desfase.

`_suma` da el mismo número que la resta de antes (0 + a + (−b) = a − b en IEEE).

### `estado_diario()`: lo que se comprobó sin hallazgo

- **Es de solo lectura:** el `__dict__` entero del Diario, el Orquestador, y los bytes, el inodo, el tamaño y el mtime del diario y del estado quedan iguales. Tres fotos seguidas dan lo mismo.
- **Coincide con la operación siguiente** en todos los escenarios de r01_03:
  - limpio, tras operar, `punto()` y tras el punto;
  - un cambio por fuera que luego se deshace, que vuelve a estar sincronizado (la operación también lo acepta);
  - los mismos bytes reescritos en el sitio: el diario no se distingue del bueno, y la operación tampoco lo distingue (es el límite de la V0.49: dispositivo, inodo y tamaño);
  - reabrir después de un DI-06, con una línea a medias o con una OP sin RES;
  - después de un DI-01;
  - los bloqueos DI-05 (`OSError`, operación interrumpida) y DI-06 (los tres motivos de `ROTOS_DI06`).

  En cada uno, «operativo» quiere decir que la operación siguiente no da DI-05 ni DI-06, y «bloqueado X» que da X.
- **Encaja con el resto del Diario:**
  - `__getattr__`: el método es de la clase, así que no pasa por `__getattr__` ni se anota.
  - `__setattr__`: no se puede reasignar.
  - Copias: `copy.copy` y `copy.deepcopy` dan un Orquestador sin foto, y el panel lo pinta ROJO, como en HEAD.
  - Clave: la foto no la expone.
- **DI-05:** la foto no puede prever un fallo de escritura, como un disco lleno. Por eso promete «sincronizado» y no «la escritura irá bien». El Documento 0 lo dice bien («las mismas dos comprobaciones… antes de dar DI-06»).

### La consola: lo que se comprobó sin hallazgo

Sonda r01_04:

- **Fotos raras:** 20 fotos dan siempre no VERDE y sin excepción. Entre ellas:
  - `None`, una lista o un texto en lugar de la foto;
  - un dict vacío, o uno cuyo `get` lanza;
  - `bloqueo` con `False`, `{}`, `0` o un texto;
  - `sincronizado` con `1`, `"True"` o un objeto que dice ser igual a todo;
  - `lineas` con `True`, `2.0`, `0`, `-1`, `"2"` o NaN, o ausentes.
- **`estado_diario` mal formado:** si no es invocable, o es una propiedad que lanza, el panel es ROJO.
- **El resto del panel no cambia:** los niveles son iguales en HEAD y en el árbol en 12 escenarios: sin reloj ni diario; reloj contrastado, caducado o sin contrastar; diario limpio, con 3 líneas y topes 2 y 3, con tope NaN, bloqueado, como texto o como Orquestador; y todo junto. Solo cambia el texto del bloqueo, que ahora lleva el código.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | Sonda r01_02, tabla: `r._tol` con `inf`, `1e308`, `10**400` o `Decimal("Infinity")` en una posición (tocando lo privado) | **Esperado** (Documento 0 §2: «una tolerancia rota bloquea o no da instantes»): ninguna tolerancia rara deja pasar. **Obtenido:** solo fallan cerrado NaN y lo que no se compara. En el contraste, un infinito o un número enorme da instantes diez días después del contraste, sin pedir otro, y el panel lo pinta VERDE: el síntoma de H-06 de T-79, con `inf` en lugar de NaN. En el salto, se acepta un salto de una hora; en el desfase, contrastar con una referencia que va un día por detrás o por delante. Negativos, cero, bool, texto y None fallan cerrado. | Las propiedades validan `_tol` con la misma regla que el constructor (finito y en (0, TOPE]) y, si no la cumple, devuelven NaN; o `_dentro` exige `math.isfinite(tope)`. Añadir la regresión con `inf` | abierto |
| H-02 | baja | Sonda r01_02: `r._tol = None`, `()` o `(2.0,)`; o `10**400` en el salto o en el desfase | **Esperado** (CA-3 y Documento 0: «el reloj sigue sin lanzar»; docstring del módulo: «nada lanza»): un código RL. **Obtenido:** `ahora()`, `contrastar()` y `comprobar_estado()` lanzan `TypeError` o `IndexError`. Con `10**400`, `_suma` lanza `OverflowError` fuera del `try` de `_dentro`. El panel sí queda ROJO. | Leer `_tol` dentro de un `try` en las propiedades (NaN si falla) y que `_suma` recoja `OverflowError` (NaN) | abierto |
| H-03 | baja (anterior a la V0.69, viene de T-03) | `Reloj(max_sin_contraste_s=1e12)` o `1e308`, contrastar una vez y dejar pasar un año (sonda r01_02, final) | **Esperado:** como el salto y el desfase, que tienen tope (`TOPE_SALTO_S`, `TOPE_DESFASE_S`: «tolerancias mayores desactivarían las comprobaciones»), un contraste que desactiva la comprobación se rechaza. **Obtenido:** se acepta, `ahora()` da instantes un año después y el panel pinta VERDE. Es el riesgo de la fila T-85 («un reloj sin contraste que parece contrastado») por la vía pública. `pruebas_reloj_t03.py` tiene `salto_que_desactiva` y `desfase_que_desactiva`, pero no la del contraste, y `pruebas_robustez_t03.py` acepta las dos salidas. | Un tope para `max_sin_contraste_s` como `[PROPUESTO]` (es un número nuevo), con la prueba `contraste_que_desactiva`. Puede ir a la deuda | abierto, a la deuda |
| H-04 | baja | Sonda r01_04, apartado 3: un diario cuya foto dice `operativo: False` con `bloqueo: None`, `sincronizado: True` y `lineas: 2` | **Esperado:** no VERDE, porque la foto dice que no está operativo. **Obtenido:** VERDE; `_diario` no mira `operativo`. El `Diario` real nunca da esa foto (`operativo = bloqueo is None and sincronizado`), así que solo afecta a un diario falso o a una versión futura | Exigir también `e.get("operativo") is True` en `_diario` | abierto |
| H-05 | baja | `.docs/tickets/T-72/pruebas.md` y `.docs/tickets/T-72/analisis-tecnico.md` en `61d3973` | **Esperado:** el informe de pruebas (`ri-probar`) y el análisis técnico rellenos. **Obtenido:** son las plantillas vacías. Lo mismo que H-02 de T-79 | Rellenarlos | abierto |
| H-06 | baja | Docstrings de `validador/diario.py` y `validador/reloj.py` | **Esperado:** la API pública al día, como la docstring del reloj lista `estado()` (V0.64). **Obtenido:** la de `diario.py` no menciona `estado_diario()` y la de `reloj.py` no dice que las tolerancias son de solo lectura | Una línea en cada docstring | abierto |

Observaciones que no son hallazgos:

- **Un `Diario` a medio construir** (`Diario.__new__(Diario)`): `estado_diario()` lanza `AttributeError`, porque lee `_roto` antes de su `try`. No se llega a él por `crear` ni por `abrir`, y el panel lo pinta ROJO.
- **Coste del panel:** con un estado grande, la foto calcula la huella del estado entero. Es el riesgo que el ticket ya declara.

### Invariantes

- **Ningún camino a una orden sin pasar por F y G:** no se toca el Orquestador, ni F, ni G.
- **Sin LLM** en el reloj, el diario ni la consola.
- **Los controles no se relajan solos.** Con tolerancias sanas, el reloj se comporta exactamente como en HEAD (r01_01). La consola es más estricta que antes: el diario desincronizado pasa a ROJO.
- **Falla cerrado y valida antes de mutar:** sí en todo lo revisado, salvo H-01 a H-04, que solo se alcanzan tocando lo privado (H-01 y H-02), con una configuración absurda (H-03) o con un diario falso (H-04).
- **Números a mano:** ninguno nuevo. H-03 pediría uno, como `[PROPUESTO]`.
- **Decisiones del operador:** ninguna tomada en silencio.
- **Secretos y datos personales:** ninguno en el diff.
- **Documentación:**
  - El LEEME, `CLAUDE.md`, `sistema_global/README.md`, el briefing y las filas T-72 y T-85 de la deuda («EN QA») cuadran con el código.
  - Las cifras son 58 suites y 24 comprobaciones.
  - El Documento 0 se pasa de general en «una tolerancia rota» (H-01 y H-02).

### Veredicto

**APTO.** Se cumplen los cuatro criterios de aceptación y los seis hallazgos son bajos; ninguno es crítico, alto ni medio.

- **Comportamiento:** con tolerancias sanas, el reloj hace exactamente lo mismo que en la V0.68. `estado_diario()` es de solo lectura, no lanza con un `Diario` real y coincide con la operación siguiente en todos los escenarios probados. El esquema y el estado guardado no cambian.
- **Qué corregir antes de cerrar:** H-05 y H-06 se corrigen en minutos. H-01, H-02 y H-04 son correcciones de pocas líneas, con su regresión.
- **Qué pasa a la deuda:** lo que no se corrija ahora, con su ID; H-03 encaja en una fila propia del reloj.

Esta QA no cierra la tarea. El encargo de la revisión prohíbe tocar otros ficheros, hacer commit y escribir en la memoria. Pasar el ticket a CERRADO, poner las filas T-72 y T-85 de la deuda en RESUELTO, la entrada del diario, la memoria y el commit quedan para quien coordina.

### Sondas de la ronda r01

Están en la carpeta entrega_claude/V0.69/qa del marco (otra sesión las dejó en el commit `f481903` mientras se escribía este informe). Se ejecutan desde `sistema_global/marco_comun_c` con `python3 -I` (el uso está en la cabecera de cada una):

- **r01_01_reloj_diferencial.py:** el reloj de HEAD y el del árbol en paralelo, en los bordes exactos y en 4.000 secuencias aleatorias. Recibe como argumento la ruta del marco de HEAD.
- **r01_02_tolerancias_raras.py:** venenos en cada posición de `_tol`, `_tol` mal formado, la vía pública y el constructor (H-01 a H-03). Sale con 1 mientras queden H-01 a H-03.
- **r01_03_estado_diario_oraculo.py:** la foto frente a la operación siguiente en 33 escenarios, con y sin clave (CA-1).
- **r01_04_consola_foto.py:** el espía de atributos, las fotos raras y el panel de HEAD frente al del árbol (CA-2 y H-04). Recibe como argumento la ruta del marco de HEAD.
