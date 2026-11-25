# T-97 · QA independiente

- **Revisor:** revisor nuevo sin contexto (Claude) · **Ronda:** r01 · **Fecha:** 15-11-2026
- **Base revisada:** `origin/develop` en `a8e0f29` (marco V0.76). El commit de T-97 es `5d03192` (V0.74). Después, V0.75 (`89e78e7`) y V0.76 (`3583c52`) solo tocaron lo de T-97 en tres sitios: MIG-011 encadenada detrás de MIG-010, `PRIORIDAD_AVISO` con O-44 y la prueba `MIG010_en_la_cadena…`, que ahora admite que MIG-010 no sea la última. `control_f.py` no ha cambiado desde T-97, y `_gasto_anio`, `tolerancia_tipo_k`, `_v074` y `_f_al_enviar` tampoco. Lo de la V0.74 sigue cumpliendo hoy lo que cumplía.
- **Independencia:** me formé la opinión con el README del ticket, el §8 del cuestionario, el Documento 0 de la V0.74, el LEEME y el código. Leí `analisis-tecnico.md` y `pruebas.md` al final, y no cambiaron ninguna conclusión.

## Reproducción desde limpio

Hice un worktree nuevo desde `origin/develop` en el scratchpad, con el `.venv` del proyecto enlazado y `PYTHONPATH` apuntando a los tres ejecutores del worktree. Así los paquetes de los bloques, instalados en modo editable, se importan del worktree y no del árbol principal (lo comprobé con `bloque_a.__file__`). Usé dos worktrees auxiliares más: `5d03192^` (código de la V0.73) y `5d03192` (código de la V0.74), solo para generar estados guardados de verdad y para comparar F con el de la V0.73. Al terminar, eliminé los tres.

| Orden | Resultado |
| --- | --- |
| `.docs/scripts/pruebas_marco.sh` | **62 pasan, 0 fallan** (2 min 45 s) |
| `python3 -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c` | **sin diferencias** (62 órdenes, 62 baterías en disco; `pruebas_tanda2_t97.py` ejecuta 49, y el LEEME cita 49) |
| `./tools/check_all.sh` (una vez, en el worktree) | **12/12** (corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff 2831/2831, mypy A 109, FX 174 y B 159 dentro de cuota, y pytest A 6557, FX 68 y B 176 por encima de la línea base); exit 0 |
| Scripts del revisor (`revisores/r01_*.py`, con `python3 -I`) | ver abajo: todos pasan salvo los que reproducen H-02 |

Scripts de esta ronda (en `revisores/`):

- `r01_genera_estado_v073.py`: genera, **con el código de la V0.73**, un estado guardado auténtico (esquema `2bcc76b8…` = `ESQUEMA_V0_73`). Lleva valores personalizados (importe del día de 30.000 €, pérdida semanal de 4.000 €, tolerancia de 0,2 y tope diario de 40 €), un expediente AUTORIZADA pendiente de enviar y un gasto. Con `v074`, genera lo mismo con el código de la V0.74 (esquema `27fc8408…`) y las claves nuevas también personalizadas.
- `r01_migracion_v073.py`: CA-7 sobre esos estados, idempotencia, estados manipulados y la cadena V0.74 → V0.76. 22/22.
- `r01_f_bordes_y_solo_endurece.py`: bordes de F-14 y F-16 y una **prueba de propiedad contra el F de la V0.73** (4.000 casos aleatorios + 500 de carteras grandes). Todas pasan; muestra H-04.
- `r01_tope_anual.py`: CA-2 con 20.000 € y 100 €, y los bordes del tope anual. 19/19; muestra H-01 y H-07.
- `r01_tipo_cambio_divisas.py`: CA-6 con un sello de K **con una fuente EURSEK de verdad**, construido por el camino normal de K. 20/20; muestra H-03.
- `r01_envio_semana.py`: el camino real del Orquestador al enviar la orden (`_f_al_enviar`). 3/3.
- `r01_pantalla_aprobacion.py`: la pantalla de aprobación del operador. **2 fallos = H-02.**
- `r01_mutantes.py`: 28 mutantes sobre una copia desechable de `sistema_global` (ruta con `_mut`).

Uso, desde la carpeta con los worktrees (las rutas son las del marco de cada worktree):

```bash
python3 -I r01_genera_estado_v073.py <marco V0.73> estado_v073.json
python3 -I r01_genera_estado_v073.py <marco V0.74> estado_v074.json v074
python3 -I r01_migracion_v073.py <marco de hoy> estado_v073.json estado_v074.json
python3 -I r01_f_bordes_y_solo_endurece.py <marco de hoy> <marco V0.73>
python3 -I r01_tope_anual.py <marco de hoy>
python3 -I r01_tipo_cambio_divisas.py <marco de hoy>
python3 -I r01_envio_semana.py <marco de hoy>
python3 -I r01_pantalla_aprobacion.py <marco de hoy>
python3 -I r01_mutantes.py <copia del marco con _mut> <marco V0.73> estado_v073.json estado_v074.json
```

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `sistema_global/documentos_0/V0.74_Valores_por_defecto_de_la_tanda_2.md` existe, y el `LEEME.md` del marco lo cita (línea 29, entrada de la V0.74). |
| CA-2 | sí | `r01_tope_anual.py`, con una foto de 20.000 €: el tope sale en 100 € (`_gasto_anio`). Con 90 € gastados este año, un encargo de 10 € se admite (100 € justos) y uno de 0,01 € más se rechaza con O-43 sin mutar el estado (`Arnes.rechaza`); uno de 25 €, también. Al registrar el gasto que llega a 100 €, sale el aviso O-43 de prioridad ALTA, sin acusar, y se puede acusar. Con el tope agotado, una foto de G (rutina sin IA) sigue registrándose, y ningún encargo entra (un coste 0 no es válido por esquema, E-01: no sirve para esquivar el tope). Sin foto ni capital declarado, O-43. Las reservas de varios encargos vivos cuentan. El capital declarado sirve sin foto, y con foto manda la foto (de 20.000 € a 10.000 €: frena; con 1.000.000 €: 5.000 €). El año natural UTC no arrastra el anterior, también con una Nochevieja en hora local. El aviso sale al **llegar** al tope, como dice el plan. Cuando el tope está comprometido o falta capital no sale ningún aviso: es H-01. |
| CA-3 | sí | `r01_f_bordes_y_solo_endurece.py`: con 20.000 € y 4.500 € ya invertidos, F-14 deja 500,00 € (REDUCIDO a 500 €); 500 € justos pasan y 500,01 € reducen; con 5.000 € ya invertidos, el límite es 0 y no se aprueba nada; 25 % de 20.000,04 € = 5.000,01 € pasa; con 200.000 € los dos límites coinciden en 50.000 €. Con 1.000.000 €, el límite es 45.500 € y el resultado es **idéntico al del F de la V0.73** en 500 casos aleatorios de carteras grandes. Un capital de 0, negativo, NaN, infinito, None o en texto da F-01 VETA. |
| CA-4 | sí | Con 20.000 € y 800 € (4 %) perdidos en la semana, trading veta y táctica abre. En el borde exacto, cada cartera veta en su porcentaje (800 €, 1.000 € y 1.000 €) y abre con un céntimo menos. Con varias carteras a la vez y una pérdida del 4,5 %, solo veta trading. Por el camino real del envío (`r01_envio_semana.py`): autorizada con 50.000 € y la semana al 5,4 % (2.700 € < 5.000 €), la orden no sale (O-06, F-16); al 4,8 % sale; con 1.000.000 € sale como en la V0.73. |
| CA-5 | sí | Fuera del ticket (T-98, en la deuda). `alerta_perdida_pct` sigue en −5,0 y `pruebas_vigilancia_t49.py` pasa (73). |
| CA-6 | sí | `r01_tipo_cambio_divisas.py`, con un sello de K que trae EURSEK: EUR/USD al 0,6 % → O-29, citando USD y no SEK; EUR/SEK al 0,6 % → pasa; al 3,1 %, los dos se rechazan, uno a uno y juntos (el motivo cita los dos). Bordes: USD al 0,49 % pasa y al 0,51 % no; SEK al 2,99 % pasa y al 3,01 % no; al −0,6 %, USD también se rechaza. Divisas no listadas (SEK, NOK y una inventada) reciben el 3 % general, igual que una lista vacía; SEK declarada principal se endurece. Una divisa en minúsculas en la foto no entra (O-01). |
| CA-7 | sí | `r01_migracion_v073.py` sobre un estado **guardado con la V0.73 de verdad**: la cadena es `MIG-010, MIG-011` y `integridad()` sale vacía. Recibe las ocho claves con su valor (0,5; None; USD, GBP, JPY y CHF; 0,005; 25; 4; 5 y 5) y conserva todos los valores personalizados de `cfg` y de la política (ninguna otra clave cambia); `CFG-0.12.0`; el gasto y los expedientes se conservan. `_v074` es idempotente. Un estado tocado sin rehacer la huella da PE-02, y con la huella rehecha, MG-02. Un estado de hoy disfrazado de V0.74 tampoco pasa (MG-02). Un estado **guardado con la V0.74 de verdad** migra solo con MIG-011, con `cfg` idéntica e integridad vacía. La autorización hecha con la V0.73 ya no vale tras migrar (O-05: vuelve a F y al operador): es la regla de la V0.46 para las migraciones que cambian la configuración, y falla cerrado. |
| CA-8 | sí | `parametros_doc.faltan() == []` y `desfasados() == []`. Las ocho claves están como `PROPUESTO`, con fuente `Deuda T-97`/`V0.74`, justificación, pregunta y `valor_documentado` correcto. `pruebas_parametros_doc_t83.py` da 109. |
| CA-9 | sí | 62 baterías en verde, LEEME sin diferencias y gate del repositorio 12/12 en el worktree limpio. |
| CA-10 | sí | `git show --stat 5d03192` no toca ningún archivo de `bloque_a/`, `bloque_b/` ni `sistema_global/constitucion/`. |

## Invariantes

- **Ninguna orden sin F y G:** no hay rutas nuevas hacia una orden. `_f_al_enviar` vuelve a pasar F-16 con el capital de la autorización (comprobado por el camino real). Mutante M06 (enviar sin capital): las baterías del marco no lo matan y `r01_envio_semana.py` sí (ver H-08).
- **Sin LLM en la ruta determinista:** todo lo de T-97 es aritmética y comparaciones; no hay importaciones nuevas.
- **Los controles nunca se relajan solos:** la prueba de propiedad contra el `control_f.py` de la V0.73, con la misma política en euros y porcentajes aleatorios válidos (0,01–100), no da **ningún** caso en que el F de hoy apruebe más cantidad o deje de vetar lo que vetaba (4.000 casos, 224 endurecen). Fuera de F-14, F-16 y F-11 los controles son idénticos; F-11 solo pasa de OK a VETA, porque el resto aprobado es menor. La política no admite un porcentaje NaN, infinito, negativo, cero, booleano o en texto (F veta). MIG-010 solo añade claves (`setdefault`) y nunca deja las principales más laxas que la general. Los porcentajes solo pueden endurecer porque F aplica `min()` con el euro. Matiz en H-05: el cortacircuito global sigue solo en euros.
- **Falla cerrado y valida antes de mutar:** el rechazo O-43 llega antes de cualquier escritura (comprobado con `Arnes.rechaza`). Con un capital no válido al enviar, F-01 VETA; sin capital, no se admite ningún encargo con coste; una configuración mala no arranca. Matiz bajo en H-03: con un `dict` en `divisas_principales` no arranca, pero con TypeError en vez de ValueError.
- **Ningún número a mano:** los valores nuevos están en `CONFIG_DEFECTO`/`POLITICA_DEFECTO`, documentados en `parametros_doc.py` con `[PROPUESTO]`. Los literales de `_v074` son el «valor de partida literal» que exige una migración, como en las anteriores, y M24/M25 confirman que un cambio en ellos se detecta (con el script del revisor en M25, ver H-08). Las cotas de validación (tope anual ≤ 10 %, como mucho 30 divisas, % ≤ 100) siguen la convención de `_valida_config`; el 10 % lo cita el Documento 0.
- **Decisiones del operador:** la lista de divisas principales y los valores están en `[PROPUESTO]` y en la deuda (T-97). Dos desviaciones respecto a las opciones recomendadas no están en la deuda: H-06.
- **Secretos y datos personales:** ninguno en el código revisado ni en los scripts del revisor (datos simulados; el perfil del operador sigue fuera del repositorio).
- **Documentación:** el LEEME coincide con el disco; el Documento 0 de la V0.74 existe; la deuda tiene T-97 (EN QA) y T-98. Hay un comentario desfasado en el cortacircuito (H-05).

## Mutantes (`r01_mutantes.py`, 28)

Los 28 mueren. 26 los matan ya las baterías del marco (`pruebas_tanda2_t97.py`, `pruebas_parametros_doc_t83.py`, `pruebas_control_f_t22.py` y `pruebas_migraciones_t03.py`). Los otros dos **sobreviven a las baterías del marco** y solo los matan los scripts del revisor:

- **M06** (`_f_al_enviar` pasa `None` como capital: al enviar no se repite el % semanal): lo mata `r01_envio_semana.py`.
- **M25** (MIG-010 deja el % semanal de trading de los estados migrados en 100): lo mata `r01_migracion_v073.py`.

Los dos son caminos de un control de F sin prueba propia en el marco (H-08).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_tope_anual.py`, apartados A y B (las líneas «avisos O-43 tras rechazar…») | Esperado: el catálogo define O-43 como «tope anual agotado **o comprometido, o sin foto de G para calcularlo**», con efecto AVISO y prioridad ALTA. Obtenido: al rechazar un encargo porque el tope está comprometido o porque no hay capital, solo se devuelve el código al emisor y `avisos` no recibe nada (0 avisos). El aviso solo sale cuando el gasto registrado **llega** al tope. Con 96 € gastados de 100 y encargos que reservan 5 €, todos se rechazan, el gasto nunca llega a 100 y el operador no se entera en lo que queda de año. Una copia nueva en L0/L1 sin capital declarado no analiza nada, también sin aviso. Sigue el patrón de O-08, pero O-08 se reinicia cada día y este dura hasta el 1 de enero. No relaja ningún control: falla cerrado. | En `emitir_encargo`, al rechazar con O-43, emitir también el aviso O-43 con un motivo fijo por año y causa («comprometido», «sin capital»), para que la deduplicación de `_aviso` no lo multiplique. Añadir la prueba. | abierto |
| H-02 | media | `r01_pantalla_aprobacion.py` (cartera de 20.000 €) | Esperado: la pantalla de aprobación (V0.40, «las cifras de la §8 con las que F decidió») enseña los límites que F aplicó: 5.000 € al día (25 %) y 1.000 € en la semana (5 % en táctica). Obtenido: `limite_dia_eur = 50000.0` y `limite_semana_eur = 5000.0`, los de euros, porque `pantalla_aprobacion` lee `importe_max_dia_eur` y `perdida_semana_max_eur` de la política. El operador aprueba viendo límites diez y cinco veces más laxos que los reales. F ya aplicó los buenos, así que no pasa ninguna orden de más, pero es información de control falsa en la pantalla del operador. | Mostrar el límite efectivo: el del informe (el `limite` de F-14, en euros, y el de F-16 semanal), o `min(euros, % × capital de la autorización)`, y separar los dos si se quiere. Ajustar `pruebas_pantalla_f.py` con un caso de cartera pequeña. | abierto |
| H-03 | baja | `r01_tipo_cambio_divisas.py`, línea «HALLAZGO H-03» | Esperado: «una configuración mala no arranca» con ValueError, como el resto de `_valida_config`. Obtenido: con `divisas_principales: ["USD", {"x": 1}]`, `set()` se evalúa antes que `isinstance` y lanza `TypeError: unhashable type`. Falla cerrado: no arranca, y `persistencia.montar` captura cualquier excepción (PE-04). | Comprobar `all(isinstance(x, str) …)` antes de `len(set(…))`. | abierto |
| H-04 | baja | `r01_f_bordes_y_solo_endurece.py`, línea «HALLAZGO H-04» | Esperado: «con una pérdida del 4 % en la semana, trading no abre». Obtenido: con 7.777,77 € de capital y una pérdida de 311,1108 € (el 4 % exacto en decimal), `4.0 / 100 * cap` da 311,11080000000004 y F-16 deja abrir, por 4·10⁻¹⁴ €. F-08 ya tenía el mismo patrón antes de T-97. | Calcular el límite como `pct * cap / 100` y redondearlo a céntimos (o comparar con una tolerancia relativa), en F-08, F-14 y F-16 a la vez. | abierto |
| H-05 | baja | Lectura de `orquestador.py` (`registrar_cartera`, comentario T-40, y `rearmar`) | Esperado: el comentario dice que el cortacircuito global «salta con el mismo umbral en el que F-16 empieza a vetar». Obtenido: desde la V0.74, con una cartera pequeña F-16 veta antes (4 % o 5 % del capital), mientras el cortacircuito y la comprobación del rearme siguen solo en euros (5.000 €). No relaja nada respecto a la V0.73, pero el comentario ya no es verdad, y no está decidido si el cortacircuito también debe ir en %. | Corregir el comentario y anotar en la deuda, como `[PROPUESTO]`, si el cortacircuito de la semana debe usar el mismo mínimo (es una decisión del operador: endurecería). | abierto |
| H-06 | baja | `README.md` (cambios de alcance) frente a la deuda T-97 y el Documento 0 de la V0.74 | Esperado: toda desviación de la opción recomendada que contestó el operador está en la deuda como pendiente suya. Obtenido: el largo plazo conserva el 2 % diario de F-08, cuando F1 recomendaba «sin límite diario»; la excepción de F2 («en el largo plazo la orden puede llegar a la aportación del mes aunque supere el 10 %») no está implementada ni en el «No entra». Las dos están solo en el README o en `analisis-tecnico.md`; la deuda T-97 solo cita el benchmark y T-98. Las dos son prudentes (no relajan). | Añadir las dos a la deuda como pendientes del operador `[PROPUESTO]` y al §4 del Documento 0. | abierto |
| H-07 | baja | `r01_tope_anual.py`, apartado C (dos gastos tras llegar al tope → 2 avisos sin acusar) | Esperado: un aviso O-43 por agotamiento, que «no se multiplica» (`_aviso` deduplica por motivo). Obtenido: el motivo lleva el gasto acumulado («100.00 de 100.00», «100.50 de 100.00»…), así que cada gasto posterior crea otro aviso ALTA sin acusar. Cada uno bloquea el rearme del kill-switch hasta que se acusa. | Motivo fijo por año («tope anual de 2026 agotado») y el importe en otro campo, o deduplicar por código y año. | abierto |
| H-08 | baja | `r01_mutantes.py`: M06 y M25 sobreviven a las baterías del marco | Esperado: cada camino nuevo de F tiene su prueba en el marco. Obtenido: ninguna batería del marco prueba `_f_al_enviar` con el % semanal (solo `controles_de_contexto` suelto), ni el valor de partida de MIG-010 para trading y largo plazo. Una regresión que relaje F al enviar, o en las copias migradas, pasaría el gate. | Llevar a `pruebas_tanda2_t97.py` los casos de `r01_envio_semana.py` (envío al 5,4 % → O-06 F-16) y comprobar en MIG-010 los cuatro porcentajes. | abierto |

## Veredicto

**APTO.** Se cumplen los diez criterios (CA-5, fuera del ticket por diseño y en T-98) y no queda ningún hallazgo crítico ni alto: ningún camino relaja F respecto a la V0.73 (comprobado contra su propio código), ninguna orden pasa de más, MIG-010 no pierde ni pisa estado, y todo lo nuevo falla cerrado.

Quedan abiertos, para la deuda técnica con su ID:

- **Medios:** H-01 (O-43 no avisa al operador cuando rechaza porque el tope está comprometido o falta capital) y H-02 (la pantalla de aprobación enseña los límites en euros y no los que aplicó F).
- **Bajos:** H-03 (TypeError en lugar de ValueError en `divisas_principales`), H-04 (borde exacto del % en coma flotante, compartido con F-08), H-05 (cortacircuito solo en euros y comentario desfasado), H-06 (dos desviaciones de F1 y F2 fuera de la deuda), H-07 (O-43 repetido en cada gasto) y H-08 (M06 y M25 sobreviven a las baterías del marco).

Según las restricciones de esta ronda, el revisor no cierra el ticket, no toca la deuda ni el diario y no hace commit: el cierre (`ri-qa`, «Si es APTO») queda para quien coordine.
