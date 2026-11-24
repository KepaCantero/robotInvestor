# T-198 · QA

## Ronda r01 · 2026-11-24 · claude (revisor independiente: no implementó T-198)

**Veredicto: NO APTO** (3 medios y 4 bajos; ninguno crítico ni alto).

### Reproducción desde limpio

- Worktree nuevo sobre `wip/t198` (`f7c3df5`, un commit sobre `origin/develop` `6045913`); la copia del implementador no se ha tocado.
- `tests/test_t198_buscador_ct19.py`: 20 superadas. **Sin el cambio fallan**: con `almacen.py` y `orquestacion.py` de `6045913` (copia aparte), 19 de 20 fallan; la que pasa es `test_ca7_el_ct19_al_buscador_conserva_sus_campos`, de regresión del cuerpo, que debe pasar en los dos.
- Vecinas: T-125 (tres suites), `test_t134_r03_t125.py` y las 15 suites que tocan sellos o integridad del almacén (`test_unitarias`, `test_integracion`, `test_t53…`, `test_t92…`, `test_t93…`, `test_fase4_huecos`, …): **548 superadas**, ningún fallo.
- `mutantes.py` del implementador sobre una copia: **34 de 34 muertos** (confirmado).
- Ciclo mock con la configuración por defecto (`revisores/r01_ciclo_mock.sh`, `--as-of 2026-06-05 ciclo`) en develop y en T-198: rc 0 los dos; paquete JSON e informe visual idénticos byte a byte; el técnico difiere solo en la ruta de la carpeta temporal; `sellos_integridad.json` gana la clave F9; ningún `F9_registro_fuentes.jsonl` (no hay FUE-). El backtest no lo repito: en backtest no hay FUE- (T-125) y el implementador lo comparó.
- ruff: `fiabilidad_f9.py` y la prueba nueva limpios; el gate da ruff 2807 y mypy A 102 (cuotas 2807 y 102: no suben).
- Compatibilidad con el PR 3 de Astra (`origin/astra/encargos-bloque-a-c38-c47`): el código de T-198 se aplica sin conflictos sobre esa rama (`orquestacion.py` se fusiona solo; `referencias.py` y `mantenimiento_fuentes.py` no se tocan) y las 20 pruebas pasan encima. Solo chocan los documentos generados o de lista (`evidencias_pruebas_bloque_a.md`, `incidencias.md`, deuda, cola de Astra): se resuelven al fusionar regenerando y juntando líneas.
- Gate del implementador (`scratchpad/gate_t198.log`): no terminó (H-07).

### Diseño frente al Documento 0

Un F9 de la instancia **no contradice** el Documento 0: F9 es de AG-16 (5.1, tabla de archivos; R6) y F7–F9 son «bases vivas» que su propietario recalifica (5.1, punto 2; 12.5: el Buscador «la incorpora a su calidad en F9»). El corpus congelado sigue intacto (gate corpus-integridad en verde; Q del corpus sin cambios, afirmado en CA-1). Es una decisión de lugar sin precedente en el corpus y está declarada `[PROPUESTO]` en INC-T198-01. Ojo: el PR 3 de Astra añade otras dos formas de cambiar F9 en la instancia (HT-02 reescribe y borra fichas con `publicar`/`borrar_ficha`, y `F9_bajas.md` en la carpeta del almacén), y eso da pie a H-01.

### Hallazgos

| ID | Gravedad | Qué |
| --- | --- | --- |
| H-01 | media | Una FUE- que ya no se puede atender bloquea para siempre todas las demás y deja una incidencia en cada ciclo |
| H-02 | baja | La migración «sin sello y sin archivo → se sella vacío» vale para todos los archivos, no solo para F9: borrar HA, F4 o F6 junto con su sello ya no falla cerrado |
| H-03 | baja | `fecha_ct19` sale del `timestamp` del mensaje sin comprobarlo: puede quedar en F9 una fecha posterior a as_of |
| H-04 | media | La parte «sin fuga» (solo lo conocible en as_of) no tiene prueba que la mate en la escritura ni en el ciclo: 3 mutantes vivos |
| H-05 | baja | Campos y casos sin afirmar: `metrica`, el filtro por `tipo_afirmacion` y el cerrojo del ciclo entre dos procesos (3 mutantes vivos) |
| H-06 | baja | Documentación: prefijo `FMD-` no declarado; «todo en una transacción» es un cerrojo sin vuelta atrás |
| H-07 | media | El gate no ha llegado a 12/12: el del implementador se cortó en pytest de A (CA-7 sin evidencia) |

#### H-01 (media) · Una FUE- envenenada bloquea la fiabilidad de todas las fuentes, para siempre

- **Reproducir:** `revisores/r01_ataques.py::test_r01_una_fue_envenenada_no_bloquea_a_las_demas`. Dos FUE- (A y B) en F6; después la fuente B deja de estar en F9 (`por_id` devuelve None, como tras una baja de R19, un borrado de HT-02 del PR 3 o una versión nueva de F9 sin esa ficha). Tres ciclos de `_comunicar_fiabilidad`.
- **Esperado:** A se atiende; B queda declarada una vez.
- **Pasa:** F9 vacío y 3 incidencias. `por_comunicar` mete en cada CT-19 todas las FUE- sin atender; `comprobar_ct19` es todo o nada; B nunca cuadra, así que ni A ni ninguna FUE- futura llega nunca a F9 y cada ciclo crea un CT-19 nuevo, reescribe `comunicado_ct19` en F6 y anota otra incidencia en HA. El todo o nada tiene sentido ante un mensaje hostil, pero en el ciclo el mensaje lo construye el propio ejecutor desde F6, así que lo único que puede fallar es justo esto: que una fuente ya no esté en F9.
- **Corrección:** en `_comunicar_fiabilidad`, antes de crear el CT-19, separar las FUE- cuyo `ref_id` ya no es fuente de F9 (`fuente_de_opinion_registrada`): no van en el CT-19 y dejan **una** incidencia DATOS cada una, con una marca durable en HA (p. ej. `fue_no_atendible: <fue_id>`) que `por_comunicar` excluye, para que no se repita. Las demás se envían y se atienden. `atender_ct19` sigue siendo todo o nada para un mensaje que llega de fuera. Declararlo en INC-T198-01, también la interacción con las bajas y borrados de F9 del PR 3.
- **Prueba de regresión:** la de arriba (A en F9 y una sola incidencia en tres ciclos), y que la FUE- de B no vuelve a salir en el CT-19 siguiente.

#### H-02 (baja) · La migración del sello vale para cualquier archivo

- **Reproducir:** `python .docs/tickets/T-198/revisores/r01_sello_generico.py bloque_a/11_Ejecutor`. Borra el archivo de HA (o F4, o F6) y quita su clave de `sellos_integridad.json`.
- **Esperado:** fallo de integridad, como en develop (`ValueError: … el final de HA difiere del sello`).
- **Pasa:** con T-198 el almacén abre con HA vacío, `verificar_integridad()` da todo bien y la historia desaparece sin aviso. `nuevos = [a for a in ARCHIVOS if a not in sellos and not exists]` no se limita a F9, que es lo único que dice el plan («un almacén sellado antes de T-198 abre y sella F9 vacío»). Es baja porque el sello no lleva clave y en develop forjar su valor es igual de fácil; pero amplía, sin decirlo, un camino de fallo cerrado a archivos que no lo necesitan.
- **Corrección:** `ARCHIVOS_NUEVOS = {"F9"}` (los añadidos después del sellado) en `almacen.py`, y `nuevos = [a for a in ARCHIVOS_NUEVOS if a not in sellos and not (self.carpeta / ARCHIVOS[a]).exists()]`.
- **Prueba de regresión:** en `test_t198_buscador_ct19.py`, el script hecho prueba: para HA, F4 y F6, archivo borrado y sello quitado, `Almacen(carpeta)` lanza `ValueError`; y la de CA-6 sigue pasando para F9.

#### H-03 (baja) · `fecha_ct19` del mensaje sin comprobar

- **Reproducir:** `revisores/r01_ataques.py::test_r01_fecha_ct19_no_puede_ser_posterior_a_as_of`: un CT-19 que cuadra con F6 pero con `timestamp` 2099-01-01 se atiende y deja `fecha_ct19: 2099-01-01` en F9, que el Buscador ve en sus CT-07.
- **Esperado:** `FiabilidadNoAtendible` o la fecha de as_of.
- **Corrección:** en `comprobar_ct19` (recibe `as_of`), exigir que `timestamp` sea una fecha ISO no posterior a as_of; o escribir siempre `fecha_ct19 = str(as_of)[:10]`, que en el ciclo es lo mismo.
- **Prueba de regresión:** la de arriba, y que un `timestamp` que no es fecha tampoco pasa.

#### H-04 (media) · Lo «sin fuga» no está protegido por las pruebas

- **Reproducir:** `python .docs/tickets/T-198/revisores/r01_mutantes.py <copia de 11_Ejecutor>`. Siguen vivos:
  - R1: `_registrados` lee F2 con `as_of=None`: `pronosticos_registrados` cuenta pronósticos registrados después de as_of;
  - R2: `atender_ct19` lee F6 con `as_of=None`: se atendería en as_of una FUE- escrita después;
  - R5: en `_peticion_conocimiento`, `anotar_candidatas(self.almacen, None, …)`: el CT-07 del ciclo enseña fiabilidad posterior a as_of.
- **Esperado:** CA-5 dice «antes de la fecha de la entrada, tampoco (sin fuga)» y el alcance, «solo lo conocible en as_of»; la ausencia de fuga es un invariante del sistema. Solo se prueba en la llamada directa a `anotar_candidatas` (M24).
- **Corrección:** tres pruebas: (a) un PRONOSTICO_FUENTE en F2 con fecha posterior a as_of no cuenta en `pronosticos_registrados`; (b) una FUE- escrita en F6 con fecha posterior a as_of no se atiende en as_of (`FiabilidadNoAtendible`, «no está en F6»); (c) en un ciclo con as_of anterior a una entrada de F9, el CT-07 al Buscador no lleva `fiabilidad_medida`. Añadir R1, R2 y R5 a `mutantes.py`.
- **Prueba de regresión:** las tres, con R1, R2 y R5 muertos.

#### H-05 (baja) · Campos y casos sin afirmar

- **Mutantes vivos** (`r01_mutantes.py`): R3 `metrica` a None; R6 cuenta cualquier afirmación con bloque `pronostico_fuente`, no solo las PRONOSTICO_FUENTE; R4 `_comunicar_fiabilidad` sin `_transaccion` (dos procesos a la vez crean dos CT-19, uno no cuadra porque F6 ya anota el otro y deja una incidencia de más). CA-3 promete «tampoco con dos procesos a la vez» y solo lo prueba en `atender_ct19`.
- **Corrección:** en CA-1, `e["metrica"] == f6[fue_id]["metodo"]`; un CLM con `pronostico_fuente` y otro `tipo_afirmacion` no cuenta; dos bloques sobre la misma carpeta llaman a `_comunicar_fiabilidad` a la vez (barrera): un solo CT-19, una entrada por fuente y ninguna incidencia. Añadir R3, R4 y R6 a `mutantes.py`.
- **Prueba de regresión:** esas tres, con R3, R4 y R6 muertos.

#### H-06 (baja) · Documentación

- El identificador `FMD-AAAA-nnnn` de las entradas de F9 es un prefijo nuevo que no está en el Documento 0 ni en INC-T198-01. **Corrección:** declararlo en INC-T198-01 (y en la tabla de archivos del README del ejecutor).
- El docstring de `atender_ct19`, el del módulo, el README del ticket («Todo en una transacción del almacén») e INC-T198-01 hablan de transacción, pero `_transaccion` es un cerrojo sin vuelta atrás: si el almacén falla en la segunda escritura de F9, la primera queda escrita (`revisores/r01_ataques.py::test_r01_fallo_a_mitad_se_recupera_sin_duplicar`: 1 entrada tras el fallo; el ciclo siguiente completa la otra sin duplicar, almacén íntegro). El comportamiento es correcto; el texto no. **Corrección:** «bajo el cerrojo del almacén; si falla a mitad, lo ya escrito queda y el ciclo siguiente completa el resto sin duplicar».
- **Prueba de regresión:** la de fallo a mitad, llevada a `test_t198_buscador_ct19.py`.

#### H-07 (media) · Gate sin terminar

- **Reproducir:** `scratchpad/gate_t198.log` acaba en `>>> pytest bloque_a (base >= 607)` (última escritura 09:52) y a las 10:26 no hay ningún proceso que escriba en él (los dos `check_all.sh` vivos son de T-199 y T-194). Nueve gates en verde (corpus, NFC, YAML, secretos, refs, ruff 2807, mypy 102 / 174 / 159); las tres pytest no tienen resultado. Es la cuarta ejecución que no termina (`pruebas.md`: «Pendiente: 12/12»).
- **Esperado:** CA-7 y la regla 9 del proyecto: gate 12/12 antes de cerrar.
- **Corrección:** volver a pasar `./tools/check_all.sh` completo en la ronda r02 (con las correcciones) con un log propio, sin otras sesiones sobre el mismo log, y dejar el 12/12 y los recuentos de A, A-Forex y B en `pruebas.md`. Por mi parte, 548 pruebas de A (T-198, T-125 y las 15 suites de sellos e integridad del almacén) pasan; no sustituye a la suite completa.
- **Prueba de regresión:** el propio gate.

### Lo que sí está bien (con evidencia)

- CA-1 a CA-7 cubiertos por las 20 pruebas, salvo lo señalado en H-01, H-04 y H-05. Datos hostiles en `fuentes` (None, textos, listas, `fue_id` no texto, todo None): fallan cerrado sin escribir (`r01_ataques.py`, 6 casos). Dos ciclos seguidos con FUE-: una entrada, ninguna incidencia, almacén íntegro.
- Números: solo `fiabilidad_fuentes.ventana_meses` de la configuración; los puntos son los de la FUE-. R8 y G3-MET-13: ningún «valid…» en F9 (CA-7). Ninguna prueba antigua cambiada; el mapa (PB-46 PARCIAL) y las evidencias son honestos: el «No comprueba» dice que la Q, el nivel y el orden siguen siendo del modelo, y PB-46 sigue «Superada en parte».

### Scripts del revisor (`revisores/`)

- `r01_ataques.py` (pytest, desde `bloque_a/11_Ejecutor`): H-01, H-03, fallo a mitad, datos hostiles, dos ciclos. Hoy: 2 en rojo (H-01, H-03), 8 en verde.
- `r01_sello_generico.py <11_Ejecutor>`: H-02 (rc 1 en T-198, rc 0 en develop).
- `r01_mutantes.py <copia de 11_Ejecutor>`: 9 mutantes; 3 muertos, 6 vivos (H-04 y H-05).
- `r01_ciclo_mock.sh <develop> <T-198> <python> <carpeta>`: ciclo mock en los dos y comparación.

### Para la ronda r02

El implementador corrige H-01 a H-07, cada uno con su prueba. El revisor vuelve a pasar los cuatro scripts de `revisores/` (todos deben dar verde: `r01_ataques.py` sin rojos, `r01_sello_generico.py` rc 0, `r01_mutantes.py` 9 de 9) además de `mutantes.py` y el gate 12/12.

## Ronda r02 · 2026-11-24 · claude (mismo revisor)

**Veredicto: APTO, pendiente de la ronda de cierre de tres bajos (H-08, H-09, H-10), que verificaré yo.** Los siete hallazgos de la r01 están corregidos, cada uno con su prueba, y no queda ningún medio ni alto.

Sobre `e436b87` (r02, encima de `f7c3df5`). Mis scripts de la r01 vienen en el commit sin cambios (comparados byte a byte con mi copia).

### Reproducción

- `tests/test_t198_buscador_ct19.py`: 29 pruebas (35 casos) más `revisores/r01_ataques.py` (10): **45 superadas**. **Sin la corrección fallan**: con `almacen.py`, `orquestacion.py` y `fiabilidad_f9.py` de `f7c3df5`, fallan las 10 que prueban código nuevo (H-01 ×2, H-02, H-03 ×7). Las de H-04 y H-05 pasan también con el código de la r01, como debe ser: solo añaden pruebas, para matar R1–R6.
- `revisores/r01_sello_generico.py`: rc 0 (HA, F4 y F6 fallan cerrado). `revisores/r01_mutantes.py`: **9 de 9 muertos** (antes 3).
- `mutantes.py` (48) sobre una copia: **47 de 48 muertos**. Sigue vivo **M12** (`atender_ct19` sin cerrojo), que en la r01 murió. Pasado solo 8 veces (`revisores/r02_m12_repetido.py`), muere 8 de 8. La prueba de concurrencia de CA-3 lo mata según la carga de la máquina (H-10).
- Ciclo mock (`revisores/r01_ciclo_mock.sh`) en develop y en la r02: paquete JSON e informe visual idénticos; el técnico difiere solo en la ruta temporal; ningún F9 sin FUE-.
- ruff 2807 y mypy 102 / 174 / 159 en el gate (no suben).

### Correcciones de la r01

| Hallazgo | ¿Corregido? | Evidencia |
| --- | --- | --- |
| H-01 (media) | Sí | `apartar_no_atendibles` antes del CT-19, marca durable `fue_no_atendible` en HA que `por_comunicar` excluye. `test_r02_h01_…` (×2), mi `test_r01_una_fue_envenenada…` en verde, M35–M37 muertos. Cuatro ciclos con B fuera: una sola marca, A en F9, almacén íntegro (`r02_ataques.py::test_r02_la_marca_es_unica_en_varios_ciclos`). Pero abre H-08 |
| H-02 (baja) | Sí | `ARCHIVOS_NUEVOS = ("F9",)`; `test_r02_h02_…`, M38 muerto, mi script con rc 0 |
| H-03 (baja) | Sí, con la otra opción | Ver «La desviación de H-03» |
| H-04 (media) | Sí | R1, R2 y R5 muertos con las tres pruebas nuevas (CA-1 reforzada, `test_r02_h04_…` ×2) |
| H-05 (baja) | Sí | R3, R4 y R6 muertos; la prueba de dos bloques pone una barrera dentro de `por_comunicar`, así que no depende de la carga |
| H-06 (baja) | Sí | `FMD-` declarado (INC-T198-01, docstring, README); «cerrojo, sin vuelta atrás» en lugar de «transacción»; `test_r02_h06_…` |
| H-07 (media) | Sí | `scratchpad/gate_t198_r02.log`, sobre `e436b87` con el árbol limpio: 12 de 12 en verde y `rc 0` (pytest A 8394, A-Forex 68, B 176; ruff 2807; mypy 102 / 174 / 159) |

### La desviación de H-03

El implementador **valida** el `timestamp` (ISO 8601, fecha que existe en el calendario, no posterior a as_of) en lugar de escribir siempre as_of. **Vale**, y es la primera de las dos correcciones que propuse:
- un mensaje de fuera con una fecha imposible se rechaza, en vez de pasar con otra fecha;
- el CT-19 del ciclo siempre pasa: `Reloj.ahora()` da la fecha de as_of con su zona (`r02_ataques.py::test_r02_el_timestamp_del_ciclo_pasa`);
- 2099, el día siguiente, «ayer», 30 de febrero, None y un número se rechazan.

La hora no se comprueba («T25:00» pasa el patrón), pero solo se usa la fecha. No es un hallazgo.

### Hallazgos nuevos

| ID | Gravedad | Qué |
| --- | --- | --- |
| H-08 | baja | Un ciclo con F9 ilegible marca todas las FUE- como no atendibles para siempre |
| H-09 | baja | INC-T198-01 pone `F9_bajas.md` del PR 3 entre las causas de «ya no es de F9», y con el código del PR 3 no lo es |
| H-10 | baja | M12 (sin cerrojo en `atender_ct19`) solo muere si la carrera se da: la prueba de CA-3 depende de la carga |

#### H-08 (baja) · Un F9 ilegible quema todas las FUE-

- **Reproducir:** `revisores/r02_ataques.py::test_r02_f9_ilegible_un_ciclo_no_quema_las_fue`. Dos FUE- válidas. Un ciclo con `referencias.fichas["F9"]` vacío, que es lo que deja `Referencias` cuando el archivo de F9 no está (por ejemplo, `rutas.archivos_operativos` mal puesto en el YAML del operador: `localizar` devuelve la ruta inexistente y se cargan cero fichas). Después, F9 vuelve.
- **Esperado:** las dos FUE- se atienden en cuanto F9 vuelve.
- **Pasa:** las dos quedan marcadas `fue_no_atendible` en el primer ciclo y F9 queda vacío para siempre. Antes de la r02 solo se reintentaba; ahora un fallo pasajero de lectura borra para siempre la señal de aprendizaje de todas las fuentes.
- **Corrección:** en `apartar_no_atendibles`, si F9 no tiene ninguna ficha cargada (`not referencias.fichas.get("F9")`), no marcar ninguna. Dejar una incidencia DATOS sin marca («F9 no se pudo leer; las FUE- se reintentan») y no crear CT-19 ese ciclo. Declararlo en INC-T198-01.
- **Prueba de regresión:** la de arriba, llevada a `test_t198_buscador_ct19.py`, y un mutante que quite esa guarda.

#### H-09 (baja) · INC-T198-01 cita `F9_bajas.md` como causa

- INC-T198-01 (r02) dice que una FUE- se aparta si su fuente sale de F9 por «el registro de bajas `F9_bajas.md` del PR 3 de Astra». En la rama del PR 3 (`origin/astra/encargos-bloque-a-c38-c47`), `retirar_por_manipulacion` solo añade una línea a `F9_bajas.md`: la ficha sigue en `Referencias.fichas`, `por_id` la devuelve y `fuente_de_opinion_registrada` da True. Esa FUE- no se aparta: se envía y se atiende. Solo la apartan un borrado de HT-02 (`borrar_ficha` y `publicar`) o una versión nueva de F9 sin la ficha.
- **Corrección:** quitar `F9_bajas.md` de esa lista en INC-T198-01, o, si se quiere apartar también lo retirado, decirlo y dejarlo para la fusión con el PR 3 (consultar `retiradas_f9(as_of)` cuando exista), con una línea en el handoff.
- **Prueba de regresión:** es un cambio de texto. Si se elige apartar lo retirado, una prueba en la fusión con el PR 3: una FUE- de una fuente en `F9_bajas.md` se aparta con su marca.

#### H-10 (baja) · M12 vive con la máquina cargada

- **Reproducir:** `mutantes.py` en una copia con la máquina ocupada (otros tres gates en marcha): `M12 sin transacción: VIVO` (47 de 48). Solo (`revisores/r02_m12_repetido.py <copia> 8`), muere 8 de 8. `test_ca3_dos_instancias_a_la_vez…` pone la barrera antes de `atender_ct19`, así que sin el cerrojo los cuatro hilos solo chocan si coinciden por azar entre la lectura y la escritura.
- **Corrección:** hacer la carrera determinista, como ya hace la prueba de H-05: una barrera con plazo dentro de la sección crítica (envolver `fiabilidad_f9.atendidas` con monkeypatch), para que sin el cerrojo todos lean lo pendiente antes de que nadie escriba, y con el cerrojo el plazo venza sin bloquear.
- **Prueba de regresión:** `mutantes.py` con M12 muerto con carga, y `r02_m12_repetido.py` con 0 vivos.

### Scripts del revisor, ronda r02

- `r02_ataques.py` (pytest, desde `bloque_a/11_Ejecutor`): H-08 en rojo; marca única en cuatro ciclos y timestamp del ciclo en verde.
- `r02_m12_repetido.py <copia> [N]`: H-10.
- Los de la r01, sin cambios: todos en verde.

### Para la ronda de cierre

Corregir H-08, H-09 y H-10 con sus pruebas. Lo verifico yo: `r02_ataques.py` en verde, `mutantes.py` 100 % muerto (con M12 y el mutante de H-08), `r01_*` en verde, y el gate 12/12 si cambia código.

## Ronda de cierre · 2026-11-24 · claude (mismo revisor)

**Veredicto final: APTO, sin nada abierto.** Los diez hallazgos (H-01 a H-10) están corregidos, cada uno con su prueba de regresión.

Revisión sobre `9071019`, encima de `e436b87`. El commit trae mis `qa.md` y `revisores/` sin cambios: los comparé byte a byte con mi copia.

| Hallazgo | Corrección | Evidencia |
| --- | --- | --- |
| H-08 (baja) | En `apartar_no_atendibles`: si F9 no tiene ninguna ficha cargada, no marca ninguna FUE-, no hay CT-19, queda una incidencia DATOS sin marca y se reintenta en el ciclo siguiente. Si `referencias` falta, la guarda también salta: falla cerrado | Mi `r02_ataques.py::test_r02_f9_ilegible…` en verde, y llevado a la suite (`test_r02_f9_ilegible_un_ciclo_no_quema_las_fue`); M43 y M44 muertos |
| H-09 (baja) | INC-T198-01 dice ahora lo que hace el código: una fuente en `F9_bajas.md` del PR 3 conserva su ficha y su FUE- se atiende. Lo decidió el coordinador y queda para revisar al fusionar el PR 3 | Texto leído en `docs/incidencias.md` (línea de la ronda r02) |
| H-10 (baja) | Barrera con plazo dentro de la sección crítica (tras `atendidas`) en `test_ca3_dos_instancias_a_la_vez…` | Con la máquina cargada (carga 8–15 en 4 núcleos, otros gates en marcha), `revisores/r02_m12_repetido.py` da 0 vivos en 8 pasadas, y `mutantes.py` mata M12 |

Comprobaciones:
- **Pruebas:** `tests/test_t198_buscador_ct19.py`, `revisores/r01_ataques.py` y `revisores/r02_ataques.py`: 49 superadas.
- **Sellos:** `r01_sello_generico.py` da rc 0.
- **Mutantes:** `r01_mutantes.py` 9 de 9 muertos; `mutantes.py` **50 de 50 muertos**. Las dos baterías se pasaron con la máquina cargada.
- **Lint y tipos:** ruff limpio en `fiabilidad_f9.py` y en la prueba; mypy sin errores en `fiabilidad_f9.py`.
- **Regresiones:** el cambio de código es solo la guarda de H-08, que actúa únicamente con FUE- pendientes y F9 vacío. Ciclo mock y backtest no cambian: sin FUE- no se entra en la guarda.
- **Gate:** no se repite en esta ronda (lo decidió el coordinador: solo cambian una condición y las pruebas). El último gate completo es el de `e436b87` (12/12, `rc 0`), y la integración lo vuelve a pasar.

Queda al operador, sin bloquear: las decisiones `[PROPUESTO]` de INC-T198-01, sobre todo cuál de las dos fórmulas del criterio 2 manda si se quiere que el ejecutor recalcule Q. PB-46 sigue «Superada en parte», por motivo declarado.
