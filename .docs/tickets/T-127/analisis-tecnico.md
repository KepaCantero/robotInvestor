# T-127 · Análisis técnico

## Causa raíz o motivo

- **T-119 H-10 (media).** La r02 de T-119 cerró la frontera con el Bloque B (1.6) con reglas exactas: un mínimo de
  componentes y el rechazo de clones idénticos. Lo de al lado seguía abierto: copias que difieren en 1e-9 no son
  «idénticas»; un componente con el 99,9999 % del peso hace del agregado su cifra; y la dispersión (mínimo, cuartiles,
  máximo) de pocos componentes es la lista de sus cifras (con 3, mínimo, mediana y máximo; con hasta 5, los cinco
  estadísticos; con 6, más el agregado ponderado). La justificación del mínimo de 3 de INC-T119-01 («con dos, el mínimo y
  el máximo son las dos cifras individuales») no cubría el caso de 3. Además, `ambito_es_red` lo declaraba el
  solicitante sin ninguna comprobación. Al revisarlo aparecieron dos casos de la misma familia que la QA no midió: los
  covenants de REI-LEV-001 se agregan sobre los componentes que los declaran (2 en el caso de control: sus holguras eran
  las de esas dos sociedades) y el *staking* y la concentración de CHR-TOKEN-001 sobre los tokens que los declaran (1 en
  el caso de control: eran los de TKA).
- **T-119 H-11 (baja).** `_firma_tipos` serializaba con JSON, que escribe igual una tupla que una lista (y no llama a
  `default` para ellas): la tupla, que la ficha rechaza, salía de la caché de la lista.
- **T-121 H-07 (baja).** CT-10 decidía CONVENCION_DISTINTA si la huella de la sección en `por_defecto.yaml` cambiaba y el
  valor guardado no «cubría» todas las claves del fichero (`_cubre`). Una clave nueva del fichero dejaba de estar cubierta
  aunque la ficha no la leyera. Y la premisa de `_cubre` («de ahí toma `parametro` lo que falta») no es cierta para una
  sección leída entera: `parametro` no mezcla una sección encontrada con la del fichero; solo toma del fichero una ruta
  que no encuentra.
- **T-121 H-08 (baja).** Tres criterios de día: MON e IDX pasaban una fecha con zona a UTC; TCV tomaba los diez primeros
  caracteres (el día local); FON fallaba con zonas mezcladas (`ValueError` de pandas).
- **T-121 H-09 (baja, heredado).** FON-DISC-001 comparaba la fecha de NAV con hora contra la última de «fechas» a
  medianoche.

## Evidencia

Scripts del revisor, desde la raíz de la copia (`.venv` enlazado al del repositorio): ver `pruebas.md`, tabla «Scripts del
revisor». Antes de T-127: `r02_01` 0/5, `r02_02` 11/12, `r01_02` 8/11 (A2, A2b, A5), `r01_03` 36/37 con tres líneas
«DISTINTO» por zona horaria, `r01_01` «día del corte con hora rechazado: 20» (los 20, de FON-DISC-001 `fecha_nav`).

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_p2.py` (H-10): `FRONTERA_B` y `ESTADISTICOS_ORDEN`, dentro de los
    `UMBRALES` de las tres fichas (la petición no los cambia: «umbrales fijos»); `redes_propias` en los de CHR-TOKEN-001.
    Ayudantes nuevos: `_grupos_casi_iguales` (cercanía en todos los datos a la vez, |a − b| ≤ tol·máx(|a|, |b|), `None` solo
    igual a `None`, grupos por componentes conexas de `scipy.sparse.csgraph`), `_sin_clones` con tolerancia (mismo mensaje
    de la r02 más «a menos del 1 %…»), `_sin_dominio` (regla (1, k) sobre valores absolutos, comparando la proporción),
    `_orden` y `_limitacion_orden`. FIR-CRED-001: dominancia sobre la deuda. REI-LEV-001: dominancia sobre GAV, deuda,
    EBITDA, gastos financieros y FFO; dispersión solo con 7 o más; covenants con el mínimo de la ficha (3) y sus holguras
    con 7 o más. CHR-TOKEN-001: la «propia red» se comprueba contra `redes_propias`; dominancia sobre capitalización y FDV
    en un sector; *staking* y concentración con 2 tokens no dominados; dispersión con 7 o más. Casos de control: S3 declara
    covenants y TKB *staking* y concentración (para que los subconjuntos lleguen al mínimo); las comprobaciones de la
    dispersión con 3 componentes y 2 tokens pasan a comprobar que no se entrega, y las del *staking* y los covenants, sus
    valores nuevos calculados a mano.
  - `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py`: `_marcado` y `_firma_tipos` (H-11); `_ConfiguracionLeida.respaldos`
    y `anotar_respaldo`, `_respaldo_en` y la regla de `no_reproducidas` de `reejecutar` (H-07); se retira `_cubre`.
  - `bloque_a/11_Ejecutor/bloque_a/configuracion.py` (H-07): `parametro`, cuando no encuentra una ruta y la toma de
    `por_defecto.yaml`, llama a `cfg.anotar_respaldo(ruta)` si la configuración lo tiene (un `dict` normal no). No cambia
    ningún valor devuelto.
  - `bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py` (H-08): `sin_zona` y `dia`, el criterio único.
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_reales.py`, `fichas_mon_idx.py`: usan `dia` (misma semántica que antes).
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_tcv.py` (H-08): `_fecha` y `_corte` usan `dia`; un texto con hora se lee
    entero (antes, sus diez primeros caracteres): una zona horaria cuenta y un texto con basura tras la fecha se rechaza.
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_fon_der.py` (H-08 y H-09): `_fecha` pasa una fecha con zona a UTC sin zona;
    `_hasta_corte_peticion` compara con `dia`; FON-DISC-001 compara la fecha de NAV por día (también la antigüedad) y el
    mensaje nombra la fecha de corte de la ficha.
  - Pruebas que fijaban el comportamiento anterior (cada cambio con su comentario «T-127»):
    `tests/test_t119_r02.py` (`test_h01_chr_token_un_solo_token_solo_si_el_ambito_es_la_propia_red`: la red servida es
    Bitcoin con BTC, no «red TKA»); `tests/test_t119_p2.py` (`test_la_envoltura_rechaza_resultados_no_finitos_y_traduce_excepciones`
    pasa a FIR-CRED-001, porque con 3 componentes REI-LEV-001 ya no calcula la dispersión;
    `test_rei_lev_oraculo_independiente_con_pandas`: 3 de 9 con covenants y la limitación nueva;
    `test_rei_lev_covenants_incumplidos_y_sin_covenants` y `test_r02_h02_rei_lev_incumple_quien_falla_uno_solo_de_los_dos_covenants`:
    las holguras se comprueban con 7 sociedades, `_con_cuatro_mas`, y «en incumplimiento» con 3 y con 7);
    `tests/test_t121_hallazgos.py` (`valor_parcial` pasa de CONVENCION_DISTINTA a ERROR_ORIGINAL, ver H-07; las tres
    aserciones sobre `_cubre` se sustituyen por otras sobre `respaldos`).
  - Nuevas: `tests/test_t127_hallazgos.py` (41 pruebas) y `.docs/tickets/T-127/revisores/impl_mutantes.py`.
  - Documentación: `docs/incidencias.md` (INC-T127-01 nueva; INC-T119-01 corregida en su sitio; INC-T121-01 anotada),
    `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (§5, una fila), `bloque_a/11_Ejecutor/README.md`
    (una frase en «Fichas del Motor»).
- **Decisiones tomadas y desviaciones del plan:**
  - H-10: se combina lo que sugería la QA en lugar de elegir una sola vía, porque cada vía cierra una de las tres
    rutas medidas: la tolerancia cierra los casi clones, la dominancia el peso casi total y el mínimo de orden la
    dispersión de pocos componentes. Subir el mínimo de componentes no habría resuelto las dos primeras. El 1 % y el 95 %
    son `[PROPUESTO]`; el 7 está derivado (`len(ESTADISTICOS_ORDEN) + 2`). La lista de redes es la del perfil PERF-CHR.
  - H-10, alcance ampliado a los subconjuntos (covenants, *staking*, concentración): son la misma fuga, y dejarlos abiertos
    habría dejado la regla a medias. Obliga a tocar dos casos de control (sus datos, no lo que comprueban: siguen
    verificando el impacto en FFO, la proporción en incumplimiento con y sin estrés, el *staking* real y la concentración
    ponderados, ahora con dos tokens).
  - H-11: se marca el tipo de los contenedores en lugar de rechazar tuplas en la forma de la petición: no cambia lo que se
    sirve ni a quién, solo cuándo sale algo de la caché. Un `numpy.float64` sigue siendo un `float` y una clave que no es
    de JSON sigue sin firmarse (la prueba de la r02 de T-119 sigue igual).
  - H-07: se sigue la sugerencia de la QA («registrar las rutas hoja que la ficha toma de `por_defecto.yaml`»), pero se
    registran al re-ejecutar, no al servir: con los mismos datos, parámetros y configuración guardada, las lecturas son las
    mismas, y así el artefacto no cambia de forma. Consecuencia declarada: un valor guardado incompleto en una clave que la
    ficha no usa ya no da CONVENCION_DISTINTA (`valor_parcial` de T-121), porque la ficha no toma nada del fichero.
  - H-08: se toma el criterio de la Fase 2 (UTC), como sugería la QA, y no el rechazo de las fechas con zona: el ciclo no
    las produce y rechazarlas sería más cambio.
- **Límites conocidos:**
  - La regla de H-10 cierra lo que se obtiene en **una** petición. Restar dos peticiones que difieren en un componente,
    rellenos diseñados para que un estadístico de orden caiga en un emisor concreto (con 7 o más) o compensaciones entre
    componentes que se anulan en una suma (por ejemplo, FFO de signo contrario) no se pueden distinguir de datos reales
    con un cálculo; quedan en el Registro de cálculos (una entrada por petición). Declarado en INC-T127-01.
  - Lo que el solicitante llame «BTC» con los datos de otro token queda con ese nombre en el Registro: la lista fija de
    redes impide declarar como red un token cualquiera, no falsear los datos.
  - Mutante equivalente: S02 (*staking* con un solo token) no muere porque un token es siempre el 100 % de su subconjunto y
    la dominancia ya lo rechaza; la condición del mínimo queda por claridad (y por si el 95 % llega a 1).
  - `impl_mutantes.py` de T-121 tenía dos mutantes sobre `_cubre` (A04 y A05), que ya no existe: ese script los dará por
    no aplicados.
  - REI-NAV-001 (T-112) entrega una fila por sociedad con su identificador; su ficha pide «prima/descuento agregado y su
    dispersión». Fuera del alcance (la QA lo apuntó «para que conste»); queda anotado en INC-T127-01 para un ticket propio.
- **Comandos exactos para probarlo** (desde la raíz del repositorio, con `.venv`):
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q tests/test_t127_hallazgos.py tests/test_t119_r02.py tests/test_t119_p2.py tests/test_t121_hallazgos.py`
  - `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_02_cache.py bloque_a/11_Ejecutor` y los demás de la tabla de `pruebas.md`
  - `.venv/bin/python .docs/tickets/T-127/revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/t127_mut`

## Ronda r02 (QA r01: H-01, H-02, H-03)

### Causa raíz

- **H-01 (alta).** La regla de casi clones comparaba los **datos** del cálculo (importes). Las cifras que agrega cada ficha
  son cocientes (DD y PD; LTV, ICR; FDV/CM, inflación por unidad de oferta…) que no dependen del tamaño: un emisor copiado
  con todos sus importes por 1,02^i difiere un 2 % en cada dato, no es casi clon, y el agregado de sus copias es su cifra
  exacta. La dominancia tampoco saltaba (cada copia pesa poco).
- **H-02 (media).** La dominancia miraba el **peso** de cada componente en la base de ponderación, no su **aportación** a la
  cifra agregada. Con rellenos de cifra nula (PD 0, deuda neta 0), un componente con el 30 % del peso aporta el 100 % de la
  media, y la media dividida por su peso (que conoce quien pide) es su cifra.
- **H-03 (baja).** Un estadístico de orden es, por definición, la cifra de un componente.

### Implementación

- `bloque_a/11_Ejecutor/bloque_a/motor/fichas_p2.py` (y, desde T-128, `motor/frontera_b.py`, adonde se mueven las funciones
  comunes sin cambiarlas; `fichas_p2` las importa con los mismos nombres):
  - `_etiquetas_casi_iguales` (el grupo de cada componente; `_grupos_casi_iguales` cuenta los grupos, como antes).
  - `_sin_copias_a_escala(cifras, que, minimo, tol)` (H-01): agrupa los componentes por sus cifras individuales con la
    tolerancia de clon y cierre transitivo, rechaza si hay menos de `minimo` grupos y devuelve el grupo de cada uno. Cifras:
    FIR-CRED-001, las seis de `_merton_medidas` (DD, PD, DD y PD reales, diferencial, triángulo); REI-LEV-001, LTV, ICR, deuda
    neta/EBITDA, vencimientos/deuda, sobrecoste/deuda, FFO/GAV y los covenants (`ltv_max`, `icr_min` o ausentes);
    CHR-TOKEN-001 (sector), FDV/CM, inflación neta, desbloqueos por ventana, *staking* real y concentración (o ausentes).
  - `_sin_dominio(..., grupos)`: con grupos, el peso es el del grupo (`_por_grupo`).
  - `_orden(..., distintos)`: los 7 de los estadísticos de orden son grupos distintos; también en los covenants de REI-LEV y
    en el *staking* y la concentración de CHR-TOKEN (el subconjunto cuenta grupos y su dominancia es por grupos).
  - `_aportacion_maxima(num, den, tol, cero)` y `_concentradas` (H-02): para una cifra agregada Σnum/Σden, la mayor parte de
    Σ|num| que aporta un componente junto con los que tienen su misma cifra num/den a menos de la tolerancia de clon (sin
    cierre transitivo: un vecindario por componente, para que una nube de cifras reales no se junte en una cadena). Una
    cifra sin definir (den = 0) es solo la suya. Un agregado nulo a la tolerancia de la ficha da 0.
  - FIR-CRED-001: si alguna media ponderada (DD, PD, diferencial, triángulo y, con `mu: historico`, DD y PD reales) pasa del
    95 %, **se rechaza** (`_rechazo_concentradas`; el mensaje nombra la cifra, no el componente).
  - REI-LEV-001: LTV, ICR y deuda neta/EBITDA, **rechazo**; vencimientos a 24 meses e impacto en FFO, **`null`** y limitación
    (`_limitacion_concentradas`).
  - CHR-TOKEN-001 (sector): FDV/CM, inflación neta y desbloqueos de cada ventana, **`null`** y limitación; *staking* real y
    concentración, igual dentro de `parcial`. La propia red no pasa por estas reglas (es su token).
  - Casos de control de CHR-TOKEN-001 con datos nuevos (comprueban lo mismo): «sin dilución» como la propia red (Bitcoin,
    BTC; dos tokens sin dilución tienen las mismas cifras y se rechazan); en el método, TKB quema 4e7 (antes 2,4e7) y
    desbloquea 2,4e7 (antes 2e7). Comentario «T-127 r02» en cada cambio.
- Decisiones y desviaciones (INC-T127-01, «Ronda r02», `[PROPUESTO]`):
  - H-01 por las **cifras**, no por los datos normalizados (la segunda opción de la QA): los datos se pueden variar sin
    cambiar las cifras (en FIR-CRED, el reparto corto/largo con el mismo punto de impago, `test_h01_las_copias_se_comparan_por_sus_cifras_no_por_sus_datos`).
  - Un grupo de copias **no** rechaza por sí solo (como hacen los casi clones de datos): cuenta como un componente. Así un
    sector real con dos componentes de cifras casi iguales no se rechaza entero si quedan bastantes distintos.
  - H-02 con la aportación (la segunda opción de la QA) y vecindarios de la misma cifra, en lugar de «un mínimo de
    componentes informativos» (rellenos casi nulos, pero no nulos, lo esquivan) o «rechazar rellenos de cifra nula o
    idéntica» (no distingue un relleno de un componente real sin riesgo). Rechazo o `null` según la cifra: rechazo donde la
    cifra es la de la ficha (FIR-CRED; los cocientes de REI-LEV, como la dominancia de peso), `null` donde es un
    subconjunto o donde las cifras reales se quedan en su cota (vencimientos, CHR-TOKEN).
  - H-03: declarado; quitar el mínimo y el máximo no lo resuelve (la mediana con n impar es la cifra de un componente).
- Pruebas existentes cambiadas por el comportamiento nuevo (comentario «T-127 r02»; ninguna se debilita):
  - `test_t119_p2.py::test_chr_token_borde_de_la_ventana_y_desbloqueos_pasados`: a 20 días solo desbloqueaba TKA (su
    cifra); se añade TKC con un desbloqueo el mismo día y la ventana sigue probando su borde (19 no, 20 sí, 30 con TKB).
  - `test_t119_p2.py::test_chr_token_oraculo_con_fracciones_exactas`: ventanas 31, 33 y 200 (antes 20: solo TKA).
  - `test_t119_p2.py::test_fir_cred_limites_del_dominio_que_se_admiten`: la volatilidad 10 de un emisor hacía su PD (≈ 100 %)
    más del 95 % de la media; ahora se comprueba ese rechazo y, con los demás de riesgo alto, que la volatilidad 10 entra.
  - `test_t127_hallazgos.py::test_h10_staking_y_concentracion_de_un_solo_token_o_dominados_no_se_calculan`: el tercer token
    tenía el mismo *staking* real que TKA (4 % − 1 % = 8 % − 5 %); nominal 4,5 %.
- Límites conocidos: los de INC-T127-01 («Lo que sigue sin poder impedirse»); mutante equivalente E11 (con
  `tokens_minimos_sector` = 2, un subconjunto de un solo grupo pesa el 100 % y lo rechaza la dominancia por grupos, con el
  mismo mensaje).
- Comandos (desde la raíz de la copia, con `.venv` enlazado):
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t127_r02.py tests/test_t127_hallazgos.py tests/test_t119_p2.py tests/test_t119_r02.py`
  - `.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor`
  - `git show fb3ccd4:bloque_a/11_Ejecutor/bloque_a/motor/fichas_p2.py > <scratchpad>/antes/fichas_p2.py` y
    `.venv/bin/python .docs/tickets/T-127/revisores/impl_r02_mutantes.py bloque_a/11_Ejecutor <scratchpad>/t127r02_mut --antes <scratchpad>/antes/fichas_p2.py`
