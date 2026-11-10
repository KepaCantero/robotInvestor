# Documento 0 — pruebas doradas (V0.66 pos-revisión) — GLM

## 1. Problema y alcance

Las baterías comprueban lo que se les dice que compruebe. Cuando se integren piezas nuevas (las del fin
de semana, las de este kit), un cambio de comportamiento que ninguna prueba mira pasará sin que nadie lo
vea: un aviso más, otra cantidad, una cartera que ya no se degrada o un código distinto en un paso. La
pieza 7 del kit 2 (V0.66) añade **pruebas doradas**: una foto fija de lo que hace cada paso de la jornada
(`pruebas/pruebas_jornada.py`) y de la semana (`pruebas/pruebas_semana.py`), que avisa de cualquier
diferencia; la acepta o la rechaza una persona, a propósito y por escrito (con `--regenerar`, y cada
regeneración se explica en el Documento 0 de la pieza que la hizo, con la lista de diferencias aceptadas).

Entra en esta versión: el módulo `pruebas/doradas.py` (el resumen de un paso, los gemelos de los dos
recorridos, el texto JSON de la foto, el generador de ficheros y el comparador con su informe), las dos
fotos (`pruebas/doradas/jornada.json` y `pruebas/doradas/semana.json`) y la batería
`pruebas/pruebas_doradas.py`. Queda fuera: cualquier cambio en `validador/` (la pieza no toca código,
esquemas ni configuración), el Orquestador y las pruebas antiguas (ninguna se borra ni se debilita), y
las filas de deuda (la pieza no abre ni resuelve ninguna: no corrige ningún defecto real del marco).

## 2. Diseño

Todo en `pruebas/`; nada en `validador/`. Cuatro piezas:

- **`resumen(resultado, o)`** — la foto de UN paso, en dos mitades:
  - `resultado`: una copia limpia del resultado del paso. Se quitan los textos de `motivo` (cualquier
    clave `motivo`, a cualquier profundidad: son los que cambian demasiado). La única otra excepción son
    las listas bajo la clave `acciones`, que se proyectan a `{condicion, codigo, expediente, ok, posicion,
    regla}` — lo que la jornada y la semana ya exigen de ellas en sus ESPERADO (regla, codigo, condicion)
    más `ok`, `posicion` y `expediente`, que ninguna prueba mira (hallazgo 1 de la revisión independiente:
    sin ellos, una regresión que cambiara el `ok` o la `posicion` informados de una acción de H pasaba en
    silencio por todo el lote; las acciones no llevan `senal`, `perdida_pct`, `nivel` ni
    `aviso_registrado`). Los `float` se redondean a 6 decimales y los no
    finitos se representan como los textos `"NaN"`, `"Infinity"` y `"-Infinity"` (una foto es JSON
    estricto, sin NaN). Un anidado más profundo que 60 niveles [PROPUESTO] se representa como el texto
    `"(...)"` (por ahí pasan las mutaciones de 500 niveles del generador de robustez; así el resumen
    tampoco desborda la pila). Un `set` o un `frozenset` (su orden varía entre procesos) y una clave que
    colisiona tras `str()` (p. ej. `1` y `"1"`) salen como el texto `"ILEGIBLE"`: nunca un orden que
    dependa del proceso ni una entrada fundida en silencio (observaciones 1 y 2 de la revisión).
    Criterio declarado: el resto se queda — `ok`, `codigo`, los
    identificadores (`ganador`, `posicion_id`, `orden_id`, `stop_id`, `encargo`, `ref`, `senal`…), las
    cantidades redondeadas y también el `detalle` de la conciliación, porque lleva la cifra explicada y
    cambia poco; si un día cambia, la diferencia se ve y una persona decide.
  - `estado`: del Orquestador, y leyendo, sin cambiar nada: el estado de cada expediente
    (`o.expedientes` → `{id: estado}`), el de cada posición con su cantidad (`{id: {estado, cantidad}}`),
    los códigos de los avisos sin acusar **ordenados y con duplicados** (dos O-19 son dos avisos: la
    semana los tiene el viernes), el nivel efectivo de cada cartera (`o.nivel` sobre las carteras de
    `o.cfg["nivel_autonomia"]` más las de `o.degradadas`, ordenadas), si hay kill-switch (`o.kill` no es
    None) y el número de rearmes (`len(o.rearmes)`). Cada bloque va en su propio `try`: lo ilegible se
    representa con el texto `"ILEGIBLE"` y el resumen nunca lanza (falla cerrado).
- **Los gemelos** — `foto_jornada(pasos=None, observar=None)` y `foto_semana(pasos=None, observar=None)`
  recorren con UN Orquestador en memoria y SU intermediario los mismos pasos de las baterías: en la
  jornada, `pasos()` de `pruebas_jornada.py` sobre `nuevo(CFG)` y su `broker()` (el gemelo `g` de la
  batería; el diario, los cortes y los reinicios son infraestructura de la batería y no cambian el estado
  del Orquestador). En la semana, `pasos_semana()` de `pruebas_semana.py` con la clase `Maquina` de la
  propia batería: los mismos deltas entre pasos, las noches de 120 s y los arranques de la mañana con
  reloj nuevo (`comprobar_estado` y `contrastar`), de modo que la secuencia de instantes es la misma que
  la de la batería; sin diario (el punto de control y el reinicio tampoco cambian el estado). Tras cada
  paso, `resumen(resultado, o)`; la foto es la lista `{"paso", "resultado", "estado"}` paso a paso. El
  gancho opcional `observar(nombre, resultado, o)` se llama antes del resumen (lo usa la batería para
  comprobar que resumir no cambia nada, y que observar no perturba la foto).
- **Las fotos** — `texto_foto(foto)` es `json.dumps(..., ensure_ascii=False, indent=2, sort_keys=True,
  allow_nan=False)` más el salto de línea final: claves ordenadas e indentado, para que las diferencias
  se lean bien, e independiente del orden de los diccionarios, de la carpeta y de la máquina (las listas
  conservan su orden, que es semántico: el de las acciones de H). `generar_fotos(carpeta=None)` escribe
  `jornada.json` y `semana.json` en `pruebas/doradas/` (o en la carpeta que se le dé, que es como la
  batería comprueba la regeneración en una carpeta temporal). Los ficheros entregados se generaron con el
  mismo código que ejecuta la batería, sin azar ni reloj del sistema.
- **El comparador** — `comparar_fotos(antigua, nueva)` empareja los pasos por posición (y señala si el
  nombre del paso o el número de pasos cambian) y baja recursivamente por `resultado` y `estado`; cada
  diferencia es `{"camino", "antes", "después"}` con el camino completo
  (por ejemplo `paso[4] (ejecutar).estado.posiciones.POS-EXP-0001.cantidad`) y los dos valores; una clave
  que aparece o desaparece se informa con el texto `"(ausente)"` en el lado que le toca. `describe()`
  los pinta en una línea por diferencia: `camino: antes -> después`, que es lo que imprime la batería al
  fallar.

`pruebas/pruebas_doradas.py` sin argumentos regenera las dos fotos en memoria y las compara con las
entregadas (falla con el informe de diferencias si no cuadran); con `--regenerar` reescribe las fotos de
`pruebas/doradas/`. Eso solo se hace a propósito: cada regeneración se explica en el Documento 0 de la
pieza que la hizo, con la lista de diferencias aceptadas (lo recuerda también `notas_briefing.md`).

## 3. Reglas y comprobaciones

La pieza no añade códigos de resultado ni de aviso (no toca `validador/` ni el Orquestador: no hay reglas
nuevas ni cambios en reglas existentes). Lo que fija es la batería `pruebas/pruebas_doradas.py`, con **17
comprobaciones** (la pieza pide al menos 12):

| Comprobación | Qué demuestra |
| --- | --- |
| `las_dos_fotos_regeneradas_coiniden_byte_a_byte_con_las_entregadas` | Las fotos de `pruebas/doradas/` son las que el código de hoy produce: si no, falla con el informe de diferencias |
| `la_foto_de_la_jornada_tiene_un_resumen_por_paso_en_el_orden_del_recorrido` | 15 entradas, los nombres y el orden de `pasos()` de la jornada |
| `la_foto_de_la_semana_tiene_un_resumen_por_paso_en_el_orden_del_recorrido` | 31 entradas, los nombres y el orden de `pasos_semana()` |
| `regenerar_en_carpeta_temporal_da_el_mismo_fichero_dos_veces_y_el_mismo_que_en_memoria` | Dos regeneraciones en una carpeta temporal dan los mismos bytes, y los mismos que en memoria: la carpeta no influye. Ahí mismo se ejercitan `leer_foto()` (con y sin carpeta) y el parámetro `recorridos` con un subconjunto (observación 3 de la revisión) |
| `el_mismo_recorrido_dos_veces_da_la_misma_foto` | Determinismo a nivel de objeto: dos gemelos completos, la misma lista |
| `un_precio_distinto_en_una_copia_del_recorrido_se_detecta` | Una copia de la ruta con 1,05 en vez de 1,16 en el paso de vigilancia cambia la foto y el comparador lo ve (acciones H-10 por H-01 y la posición cerrada) |
| `el_informe_nombra_el_paso_el_camino_y_los_valores_de_antes_y_despues` | Las líneas del informe llevan el paso, el camino y `antes -> después` |
| `el_comparador_senala_el_camino_exacto_de_un_cambio_de_estado_provocado` | Tres cambios provocados en una copia de la foto (cantidad, clave ausente, código) salen con su camino exacto y solo esos tres |
| `los_resumenes_no_llevan_textos_de_motivo` | Ninguna clave «motivo» a cualquier profundidad en las dos fotos |
| `el_resumen_no_cambia_el_orquestador_ni_el_resultado_en_ningun_paso` | En los 46 pasos de los dos recorridos, el volcado de `persistencia` y una copia profunda del resultado son iguales antes y después de resumir |
| `observar_no_perturba_la_foto` | Recorrer con el gancho de observación da la misma foto que recorrer sin él |
| `el_resumen_aguenta_resultados_raros_sin_lanzar_y_es_determinista` | None, número, texto, listas y diccionarios vacíos, NaN e infinitos, «acciones» que no son lista, anidado a 500 niveles y un ciclo: no lanza, dos llamadas dan lo mismo y el texto es JSON estricto. También un `set`, un `frozenset` anidado y un diccionario con claves que colisionan tras `str()` (`1`, `"1"`, `True`): salen `"ILEGIBLE"`, fijado |
| `el_redondeo_a_seis_decimales_y_los_no_finitos_son_lo_que_la_foto_promete` | 1/3 y 0,12345675 salen redondeados; NaN, Infinity y -Infinity como texto; enteros, booleanos y None tal cual (fija la promesa que los recorridos de hoy no ejercitan) |
| `el_resumen_aguenta_un_orquestador_roto_sin_lanzar_y_falla_cerrado` | Expedientes None, avisos en diccionario, posición sin diccionario, nivel que lanza y rearmes None: «ILEGIBLE» donde toca; un kill falsy que no es None (0, «») cuenta como activo (solo `None` lo apaga) y uno que lanza sale «ILEGIBLE»; dos llamadas dan lo mismo |
| `las_fotos_son_json_valido_ordenado_e_indentado_y_sin_nan` | El texto entregado es exactamente el volcado ordenado e indentado de lo que dice, y JSON estricto (sin NaN ni infinitos) |
| `las_cantidades_de_las_fotos_no_superan_seis_decimales` | Todo float de las dos fotos cumple `x == round(x, 6)` |
| `la_foto_marca_los_puntos_de_giro_conocidos_de_los_dos_recorridos` | Las fotos documentan el comportamiento conocido (kill y rearme, degradación, cierres, cantidades): no son la foto de nada |

## 4. Códigos, API, pruebas y revisión independiente

Funciones nuevas, todas en `pruebas/doradas.py` (nada en `validador/`):

- `resumen(resultado, o) -> dict` — la foto de un paso: `{"resultado": …, "estado": …}`. Nunca lanza.
- `foto_jornada(pasos=None, observar=None) -> list` — el gemelo en memoria de la jornada, resumen por paso.
- `foto_semana(pasos=None, observar=None) -> list` — el gemelo en memoria de la semana, con la misma
  secuencia de instantes (clase `Maquina` de `pruebas_semana.py`), resumen por paso.
- `texto_foto(foto) -> str` — JSON con claves ordenadas, indentado 2, sin NaN, con salto final.
- `generar_fotos(carpeta=None, recorridos=("jornada", "semana")) -> dict` — escribe las fotos; devuelve
  `{recorrido: ruta}`.
- `leer_foto(recorrido, carpeta=None)` — la foto entregada como estructura.
- `comparar_fotos(antigua, nueva) -> list` — las diferencias `{"camino", "antes", "después"}`.
- `describe(diferencias) -> list` — las mismas, una línea por diferencia: `camino: antes -> después`.

Constantes públicas: `CARPETA_FOTOS`, `PROFUNDIDAD_TOPE` (60 [PROPUESTO]), `DECIMALES` (6), `ILEGIBLE`,
`AUSENTE`, `CORTADO` y `FOTOS` (el registro de recorridos). Sin cambios en el esquema del código (ninguna
constante nueva en `validador/`: los módulos de `persistencia.MODULOS_ESQUEMA` quedan como estaban), sin
configuración nueva y sin tocar el Orquestador.

Batería nueva: `pruebas/pruebas_doradas.py`, **17 comprobaciones**, determinista, ~5,5 s, sin azar ni reloj
del sistema; acepta `--regenerar` (reescribe las fotos de `pruebas/doradas/`). **Ninguna prueba antigua
se debilita** (la de la semana gana la constante `CFG_SEMANA` a nivel de módulo, misma cfg, una línea
movida: hallazgo 2 de la revisión); el lote completo queda en **55 baterías, 0 con fallos**
(`salida_pruebas.txt`, regenerada tras la corrección).

Defectos encontrados por el propio desarrollo y el autorrepaso (corregidos aquí, con su comprobación):

- `defecto_01` — un `o.avisos` que no es una lista (o es un texto) salía en la foto como lista vacía
  `[]`, en silencio. Ahora el bloque entero sale `ILEGIBLE` (falla cerrado); lo fija la comprobación del
  Orquestador roto con `_O_Avisos_Raros`.
- `defecto_02` — los estados de expediente y de posición y los niveles salían crudos del resumen: un valor
  no JSON (NaN, un objeto) llegaría hasta `texto_foto` y la haría lanzar. Ahora pasan todos por la misma
  limpieza que el resultado.
- `defecto_03` (sonda S1) — quitar el redondeo no cambiaba ninguna foto: los recorridos de hoy solo
  llevan cantidades exactas a 6 decimales. La promesa estaba sin fijar; la fija la comprobación unitaria
  vía `resumen` (1/3, 0,12345675, NaN, ±Infinity), y la sonda S1 ya la caza.

Revisión independiente: **ejecutada el 10 de noviembre de 2026 y aplicada aquí (V0.66 pos-revisión)**;
los tres hallazgos, sus correcciones y las regresiones quedan en `revision.md` de esta carpeta y el
informe íntegro del revisor en `informe_revision_independiente_V0.66.md` (las dos sondas adversariales,
en `entrega_glm/revisores/`). No-vacuidad demostrada con las
sondas de `entrega_glm/V0.66/sondas_no_vacuidad_v066.py`: cinco mutaciones de `doradas.py` en una copia
del árbol (S1 sin redondeo, S2 con «motivo», S3 kill fijo a False, S4 comparador vacío, S5 claves sin
ordenar) y la batería cae en las cinco, en las comprobaciones que tocan (repetidas por el revisor: LAS
CINCO CAZADAS).

## 5. Límites y deuda técnica

- La foto es del **gemelo en memoria** de cada recorrido: el diario, los cortes, los reinicios y los
  puntos de control son infraestructura de las baterías y no cambian el estado del Orquestador, así que
  no entran en la foto (lo que sí entra es la misma secuencia de instantes de la semana, noches incluidas).
- Del resultado se quita solo lo que cambia demasiado (los «motivo»), más la proyección de las «acciones»
  a sus seis campos (§2); el «detalle» de la conciliación se queda a propósito, porque lleva la cifra
  explicada y cambia poco. Consecuencia declarada: una diferencia
  de comportamiento solo se ve si cambia algo que el resumen guarda; lo que solo cambia un texto de
  «motivo» no la verá la foto (lo ven las baterías que exigen esos textos).
- La comprobación «el resumen no cambia nada» mira el volcado de `persistencia` y una copia del resultado:
  es el estándar del propio marco (las baterías gemelas usan el mismo patrón); un efecto lateral sobre un
  atributo fuera del volcado no se vería (observación 4 de la revisión, aceptada).
- Por encima de `PROFUNDIDAD_TOPE`, el comparador trabaja con valores ya cortados: dos fotos distintas
  solo más allá de 60 niveles darían `"(...)" == "(...)"`. Hoy inalcanzable desde los resultados del marco
  y declarado [PROPUESTO] (observación 5 de la revisión).
- **Regeneración del 10 de noviembre de 2026 (revisión independiente, hallazgo 1), aceptada a propósito.**
  Las acciones de la foto pasan de la proyección `(regla, codigo, condicion)` a los seis campos
  `{condicion, codigo, expediente, ok, posicion, regla}`. Diferencias aceptadas, contadas sobre las fotos
  con el propio comparador: **2 pasos cambiados, uno por recorrido** — `vigilar_objetivo` (jornada) y
  `jueves_stop` (semana), que son los únicos con acciones no vacías de las dos fotos (una acción cada uno:
  H-10 y H-01); cada acción gana `ok`, `posicion` y `expediente` (null aquí), sin cambiar nada más.
  Los otros pasos que llevan la clave «acciones» la llevan vacía y no cambian. Las dos fotos siguen
  siendo 15 y 31 pasos, con los mismos puntos de giro y los dos O-19 del viernes.
- Las fotos ligan el comportamiento actual de los DOS recorridos entregados; un recorrido nuevo o un paso
  nuevo pedirá regenerar sus fotos (con `--regenerar`) y explicarlo. La foto no sustituye a las baterías:
  las 55 siguen pasando por su cuenta.
- El comparador empareja pasos por posición: si una pieza añadiera o quitara un paso, todas las parejas
  siguientes saldrían descuadradas en el informe (es lo que pasa, y se ve; afinar el emparejamiento no
  valía la complejidad).
- **Deuda: ninguna fila nueva** (la pieza no corrige ningún defecto del marco y la pieza 7 no propone
  deuda). Las filas T-64 a T-69 de la pasada de coherencia siguen sin resolver, igual que las anteriores.
