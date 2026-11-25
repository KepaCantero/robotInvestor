# T-121 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01 · 2026-11-14
- **Copia revisada:** `git worktree` con HEAD separado en `63d6ae9` («wip local: integrar T-119 r02 y T-121»), encima de `1455b03` (T-123) y `c25fb8b` (T-122). El código de T-121 está en `63d6ae9` junto con la r02 de T-119; lo he atribuido por los comentarios «T-121» del diff y por el `README.md` de cada ticket.
- **Orden de lectura:** `README.md` y `.docs/tickets/T-118/qa.md` → diff de `servicio.py`, `fichas_fon_der.py`, `fichas_mon_idx.py`, `fichas_tcv.py` y `fichas_series.py` → mis scripts → solo al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Todo desde la raíz de la copia con `.venv` enlazado al del repositorio (`ln -s /home/user/robotinvestor/.venv .venv`), salvo donde se indica. Lo marcado «leído» lo he deducido leyendo el código; el resto, ejecutándolo.

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Scripts de la QA r01 de T-118, sin modificar | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_01_h09_fecha_corte.py` · `r01_03_h11_ct10_configuracion.py` · `r01_04_h12_configuracion.py` | **60/60** · **34/34** · **47/47**. En `r01_01` bloque 2 solo se sirven, con el corte en la víspera, IDX-REB-001 (`/evento/fecha_efectividad`), MON-EXP-001 (`/reuniones[]`) y REI-LEV-001 (vencimientos): ninguna de las 14 |
| Fuzz de `servir` y `reejecutar` (T-118) | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_05_h13_h14_fuzz.py` | Ver CA-3 y CA-4 (bloques 1 y 3) |
| Mutantes de H-06 | `python .docs/tickets/T-118/revisores/r01_07_mutantes.py <copia «qa2_mut»>/bloque_a/11_Ejecutor --solo M05,M38,M50,M68,M78` | **5 muertos, 0 vivos** (cada uno con su prueba `test_h09_m05_…`, `test_h10_m38_…`, `test_h11_m50_…`, `test_h12_m68_…`, `test_h13_m78_…[9]`) |
| H-04 campo a campo (mío) | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_01_h04_campo_a_campo.py` | 22 fichas de IDX, FON, DER, MON y TCV; 67 casos de control (los de DER y FON-TD no llevan fechas). 206 peticiones; ver CA-1 |
| CT-10 (mío) | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_02_h01_ct10.py` | **8/11**: ver CA-2 y H-07 |
| Bordes de la fecha de corte (mío) | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_03_h04_bordes.py` | 36/37 (el que falla es un caso mal planteado por mí: FON-FLOW-001 mensual con la última fecha corrida un día rompe la frecuencia, no es un defecto). Ver H-08 |
| Casos de control (mío) | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_04_casos_control.py` | `verificar_casos_control`: **67 de 67 superados** (66 fichas con caso de control en `CASOS_CONTROL` + AUD-REX-001), 70 s. Las 14 restantes de los 80 manejadores no tienen casos en `CASOS_CONTROL` (sus pruebas van en la suite) |
| Ciclo V5 antes y después | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_06_regresion_ciclo.py <export de 00ed8d3>/bloque_a/11_Ejecutor bloque_a/11_Ejecutor <carpeta>` («antes» = `00ed8d3`, el ancestro común con `develop`, sin T-121, T-122, T-123 ni la r02 de T-119) | 57 ficheros en los dos; **56 idénticos byte a byte**, `consumo.csv` igual salvo latencias; RC del ciclo: 129 SERVICIO, iguales. «Sin diferencias fuera de los campos nuevos del RC, su cadena y las latencias» |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && ../../.venv/bin/python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| Gates ligeros | `tools/corpus_integridad.py` · `refs_vivas.py` · `secrets_scan.py` · `nfc_check.py` | Los cuatro en verde (corpus: 695 archivos) |
| ruff y mypy, contados como el gate | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` · `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | **2902** (cuota 2902) · **109** (cuota 109) |
| Suite de A | `cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q` (una sola vez, al final, para los cuatro tickets) | Ver «Suite» al final |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-04) | sí | `r01_01_h04`: en los 67 casos de control, sin corte y con el corte en la fecha más tardía de sus `valores`, **mismo resultado** (0 diferencias). Por cada ruta con fechas, la aparición más tardía corrida a D + 1 con el corte en D: 103 pruebas, 98 rechazadas (81 por «posterior a la fecha de corte»; 17 por otra regla de la ficha que salta antes: periodo de MON-REAL, `conocible_desde` de TCV-SLOPE, efectividad anterior al anuncio) y **5 servidas, todas fechas futuras por naturaleza**: `evento/fecha_efectividad` de IDX-REB-001, `reuniones[]` de MON-EXP-001 y `eventos_comparables[]/fecha_efectividad` de IDX-REB-001 (este último: un comparable con anuncio y efectividad posteriores al corte se sirve pero queda fuera del estudio, que sale igual que sin él: comprobado en `r01_03` bloque 2). El dato del día del corte con hora (`D 23:59:59`, `DT23:59:59.999`) se sirve en los tres módulos; los 20 rechazos «con hora» del barrido son de otras reglas o de H-09. En `r01_01` (T-118), ninguna de las 14. Ninguna excepción escapa y cada llamada deja una entrada en RC. Los bloques opcionales que los casos de control no traen (historia de MON-YLD, decisiones de MON-EXP, precios de IDX-CONC…) los he leído en el diff, no los he atacado con un script mío (los cubren las pruebas y los 55 mutantes del implementador, que no he vuelto a ejecutar) |
| CA-2 (H-01) | sí, con H-07 | `r01_03` (T-118) bloque 5: ERROR_ORIGINAL con la configuración vigente igual, con la clave leída cambiada (E 60→68), con otra clave de la sección y con otra sección. `r01_02` mío: con `por_defecto.yaml` cambiado en la clave leída y el valor guardado completo, ERROR_ORIGINAL (A1); sin `configuracion_usada`, sin la sección leída en el registro o con el Motor original sin la sección (tomada del fichero) y el fichero cambiado, CONVENCION_DISTINTA (B1–B3). Pero si `por_defecto.yaml` **gana una clave** en una sección leída (aunque ninguna ficha la lea), un error real vuelve a CONVENCION_DISTINTA (A2, A2b, A5): H-07 |
| CA-3 (H-02) | sí | `r01_05` (T-118) bloque 1: **5 758 llamadas** (cada campo de la petición, los argumentos `solicitante`, `run_id` y `msg_id`, la petición entera y los elementos y claves de `datos`, con ~45 valores raros, entre ellos `"\ud800"`, generadores, claves tupla, referencias circulares y 3 000 niveles) en SIM-MC, REI-CAP, DEC-VOI y FX-BRK: **0 escapes**, exactamente una entrada en RC por llamada, y el RC de 5 758 entradas se reabre con la cadena íntegra (en la r01 de T-118: 104 escapes). Bloque 2: el rechazo por anidamiento empieza justo en 33 niveles en todos los sitios |
| CA-4 (H-03) | sí | `r01_05` (T-118) bloque 3, **8/8**: de 124 artefactos alterados (en la r01 de T-118, 33 escapaban), 74 NO / ERROR_REEJECUCION, 16 NO / ERROR_ORIGINAL, 5 NO / DATOS_DISTINTOS, 15 SI, 11 excepciones **declaradas** (3 «sin los valores en línea», 4 «ficha sin manejador», 4 «no es un servicio») y 3 alteraciones que el script no llega a escribir en el Almacén; **0** excepciones de clase declarada fuera de los cuatro casos documentados; toda re-ejecución que termina deja su entrada REEJECUCION |
| CA-5 (H-05) | sí | `r01_04` (T-118): **47/47**; con H5 en 60 meses, REG-HMM-001 pasa a 260 |
| CA-6 (H-06) | sí | `r01_07 --solo M05,M38,M50,M68,M78`: 5 muertos, 0 vivos |
| CA-7 | sí, salvo el gate entero (suite: 5663 en verde) | Casos de control: 67/67. Ruff 2902 y mypy 109 (no suben). Corpus, referencias, secretos y NFC en verde. Goldens sin cambios. Ciclo V5 sin diferencias. No he vuelto a ejecutar `impl_mutantes.py` (55 mutantes del implementador). La suite completa, abajo. `./tools/check_all.sh` entero no lo he lanzado (por instrucción) |

## Hallazgos de origen (QA r01 de T-118)

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (media) | corregido, con un resto (H-07, baja) | Arriba, CA-2 |
| H-02 (baja) | corregido | CA-3: 0 escapes en 5 758 llamadas |
| H-03 (baja) | corregido | CA-4 |
| H-04 (media) | corregido | Arriba, CA-1; bordes de zona horaria en H-08 |
| H-05 (baja) | corregido | `r01_04` 47/47 |
| H-06 (baja) | corregido | `r01_07` 5/5 muertos |

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | baja | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_02_h01_ct10.py` (casos A2, A2b y A5) | **Esperado:** con el registro completo guardado en el artefacto, una cifra alterada es ERROR_ORIGINAL aunque `por_defecto.yaml` cambie en algo que la ficha no lee. **Obtenido:** si el fichero **gana una clave** en una sección leída (`parametros_ht03.clave_nueva`, `parametros_ht03.umbrales.Z`, `horizontes.H6`), el artefacto bueno se reproduce SI, pero el alterado da NO / CONVENCION_DISTINTA en DEC-VOI-001 y en RISK-VAR-001: `_cubre(valor, defecto_actual)` es falso y la huella ha cambiado. Quitar una clave o cambiar un valor sí da ERROR_ORIGINAL (A1, A3). Es la regla declarada en el README («cuando la sección guardada no trae todas las claves del fichero y su huella ha cambiado»), pero INC-T121-01 afirma que «tras la sesión T-57… un artefacto con la sección entera guardada sigue pudiendo dar ERROR_ORIGINAL», y eso deja de ser cierto en cuanto T-57 añada una clave a `horizontes`, `parametros_ht03` o `evaluacion`. `coincide` sigue en NO y el diagnóstico nombra la sección, por eso es baja | Registrar en la lectura las rutas hoja que la ficha toma de `por_defecto.yaml` (no solo la sección) y decidir CONVENCION_DISTINTA solo si alguna de ellas falta en el valor guardado; o, como mínimo, completar INC-T121-01 con este caso para T-57 | abierto |
| H-08 | baja | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_03_h04_bordes.py` (bloque 1, «coherencia entre módulos») | **Esperado:** la misma regla de día en las tres familias. **Obtenido:** con zonas horarias cada módulo decide distinto. Un dato `(D+1)T00:30+14:00` (día D+1 en su hora local, día D en UTC) con el corte en D: MON-YLD-001 lo **sirve** (`fichas_mon_idx._dia` pasa a UTC), TCV-CDS-001 y FON-FLOW-001 lo rechazan (TCV toma los diez primeros caracteres; FON da `ValueError` de pandas con zonas mezcladas). Un dato `DT23:00-05:00` con el corte en D: MON lo rechaza, TCV lo sirve. Un corte `DT23:00-05:00` deja pasar en MON y TCV un dato fechado en D + 1. Solo con fechas con zona, que el ciclo no produce (el corte sale de `as_of.date()`); el margen es de un día | Una sola función de día para los tres módulos (la de la Fase 2), con la misma convención para el dato y para el corte; o rechazar fechas con zona en los datos en línea | abierto |
| H-09 | baja (heredado de T-106, no lo introduce T-121) | `r01_01_h04_campo_a_campo.py`, línea «día del corte con hora rechazado» | **Esperado:** INC-T121-01: «el dato del día del corte se sirve, también con hora». **Obtenido:** en FON-DISC-001, una `fecha_nav` del último día de `fechas` con hora (`2023-01-06T23:59:59`) se rechaza: «fecha de NAV posterior a la fecha de corte», porque la ficha compara con hora contra su propia «fecha de corte» (la última de `fechas`, a medianoche). No es una fuga (rechaza de más) y el mensaje confunde las dos fechas de corte | Comparar por día también ahí, o renombrar en el mensaje la fecha de la ficha | abierto |

## Suite

`cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q -p no:cacheprovider` (una sola vez, en la copia `63d6ae9`, común a T-119 r02, T-121, T-122 y T-123): **5663 passed** en 23 min 43 s, código de salida 0 (línea base 607).

## Veredicto

**APTO.**

Los siete criterios se cumplen (CA-2 con el resto que describe H-07; CA-7 sin el gate entero, que no he lanzado por instrucción) y no queda ningún hallazgo crítico ni alto. Los seis hallazgos de la QA r01 de T-118 están corregidos, con evidencia mía: los scripts de aquella QA pasan sin modificar (60/60, 34/34, 47/47 y 8/8, con **0 escapes en 5 758 llamadas** a `servir` y **0 excepciones no declaradas en 124 artefactos** alterados), los cinco mutantes de H-06 mueren, y en H-04 el barrido campo a campo de las 22 fichas de la Fase 1 solo deja pasar fechas futuras por naturaleza (efectividad anunciada, reuniones y la efectividad de un comparable, que además no entra en el cálculo). La distinción entre fechas observadas y futuras no deja colarse información: un dato observado disfrazado de fecha futura (un comparable con anuncio y efectividad posteriores al corte) queda fuera del estudio, y las reuniones y la efectividad no llevan cifras. El ciclo V5 da lo mismo que antes (56 de 57 ficheros byte a byte) y los casos de control siguen superados (67/67).

Quedan tres bajos, que se corrigen o pasan a la deuda con su ID: **H-07** (CT-10: una clave nueva en `por_defecto.yaml` vuelve a dar CONVENCION_DISTINTA a un error real; conviene resolverlo o declararlo antes de la sesión T-57), **H-08** (zonas horarias tratadas distinto en los tres módulos) y **H-09** (heredado: `fecha_nav` con hora en FON-DISC-001).

**Condición de cierre:** `./tools/check_all.sh` 12/12 en el commit.

**Sin comprobar:** el gate entero; `impl_mutantes.py` del implementador (55 mutantes) no lo he vuelto a ejecutar, así que los bloques opcionales de H-04 que los casos de control no traen (historias, decisiones, precios, encuestas…) los he verificado leyendo el diff y por sus pruebas, no con un ataque mío; el `r01_07` completo (los 72 mutantes de T-118), solo los cinco de H-06; la suite de B; datos y modelo reales (fuera del alcance). Tiempos medidos en una máquina compartida con otras dos suites en marcha.

Este revisor no cierra el ticket ni toca la deuda, el diario ni la memoria: lo hace quien encargó la QA.
