# T-124 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01 · 2026-11-15
- **Copia revisada:** clon desconectado en `fb3ccd4`; lo de T-124 es `tests/goldens_ct.py` (`FLUJOS` y `rutas`), `tests/goldens/bateria_mensajes.json` (ocho casos), los goldens re-congelados (`aceptaciones_rechazos.json`, `formas_flujos_mock.json`, `huellas.json`) con su línea en `REGISTRO.md`, INC-T114-01 y la nota en el registro de T-114.
- **Orden de lectura:** `README.md` → diff de `goldens_ct.py` y de los goldens (`d1ff926..fb3ccd4`) → scripts → al final `analisis-tecnico.md` y `pruebas.md`.
- **Copia desechable para los mutantes:** un clon aparte en el scratchpad, con «qa8_mut» y «qa_f3_mut» en la ruta (los scripts de T-114 exigen lo segundo), restaurado tras cada script y borrado al acabar.

## Reproducción

| Comprobación | Orden (desde la raíz de la copia) | Resultado |
| --- | --- | --- |
| CA-1 | `python .docs/tickets/T-114/revisores/r02_01_mutantes_mensajeria_nuevos.py --confirmar <copia qa_f3_mut>` | «control (copia sin cambios): coincide»; **20 de 20 detectados, vivos: ninguno** (en la r02 de T-114, vivos C01, C02, C03, C04, C08, C09 y C15); 38 s |
| CA-2 | `python .docs/tickets/T-114/revisores/r02_02_formas_y_flujos.py --copia <copia qa_f3_mut>` | (1) control: lo filtrado = golden (220 capturados, 220 guardados); (2) el filtro ya no tira nada que ningún flujo guarde; (5) **0** rutas genéricas en «a veces» estando en todos sus objetos, 28 bien clasificadas (en la r02, 12 de 14 mal); (4) **K01, K02 y K03 detectados** (`goldens_ct.py` código 1). (3) T01 y T02 ahora se ven; T03, T07 y T09 no (ver H-03); 3 min 13 s |
| ¿El re-congelado solo cambia lo que dice su motivo? | `python .docs/tickets/T-124/revisores/r01_01_que_cambia_el_recongelado.py --copia <copia qa8_mut>` | **sin fallos.** (1) En los ocho flujos que T-124 no toca, ninguna ruta perdida, ganada ni con otro tipo, ni emisores o receptores distintos; lo único que cambia es «a veces» → «siempre» en rutas con `<…>` (H-08). En los tres tocados solo se añaden contratos (consulta que escala 2 → 10, informe de aprendizaje 1 → 9, petición ad hoc 2 → 8) y los de antes no pierden nada. (2) Aceptaciones y rechazos: los 362 casos de antes, idénticos; los nuevos son los ocho de la batería. (3) **Con el código de producción de `d1ff926`** (antes de T-123 r02, T-125, T-126 y T-127) y los goldens y `goldens_ct.py` de HEAD, `goldens_ct.py` da «coinciden»: el re-congelado no esconde ningún cambio de lo que emite el ejecutor; todo sale de los cambios de T-124 en las pruebas |
| CA-3 | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py`; suite de A; `git diff d1ff926 fb3ccd4 --stat` | «goldens de contratos: coinciden»; `test_fase3_goldens.py` dentro de la suite completa en verde (ver «Comunes» en `T-127/qa.md`); T-124 no cambia producción (los cambios de producción del commit son de T-123, T-125, T-126 y T-127, y el punto (3) de arriba muestra que no tocan los goldens) |
| Motivo del re-congelado | `tests/goldens/REGISTRO.md` y mensaje del commit | Una línea del 14-11 con los tres ficheros y el motivo (ocho casos, tres flujos enteros por H-07, rutas genéricas por H-08); va en el mismo commit que el cambio de `goldens_ct.py` y la batería, y el mensaje del commit lo cita. ✔ |
| H-10 y H-11 | `awk '/^\*\*INC-T114-01/,/^\*\*INC-T114-02/' docs/incidencias.md`; `.docs/tickets/T-114/README.md` | La línea de las listas cerradas y de `contenido` de CT-23 está en INC-T114-01; la nota de cifras, en el registro de T-114 ✔ |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r02_01 --confirmar`: 20/20 detectados, ningún vivo |
| CA-2 | sí | `r02_02 --copia`: K01, K02 y K03 detectados |
| CA-3 | sí | goldens coinciden; `test_fase3_goldens.py` en verde; sin cambios de producción de T-124 |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `cat .docs/tickets/T-124/pruebas.md` | **Esperado:** el informe de `ri-probar` (suites antes y después, criterio → prueba, regresiones, gate). **Obtenido:** es la plantilla («…», «<Para cada una…>»); lo ejecutado solo está en dos líneas del registro del README | Rellenarlo con lo de arriba | abierto |
| H-02 | baja | `sed -n 35,46p bloque_a/11_Ejecutor/tests/goldens/README.md` y la línea 83 | **Esperado:** el README de los goldens dice qué guarda cada flujo (es lo que define qué ven). **Obtenido:** no se tocó: sigue diciendo «`consulta_que_escala`… CT-03 y el aviso CT-22», «`peticion_ad_hoc`: CT-01 y CT-02», «`informe_de_aprendizaje`: CT-19», y en «Límites» todavía «De los flujos que lanzan un ciclo por dentro… solo se guardan los contratos que el flujo añade. Los del ciclo ya están en los ciclos semanales», justo la frase que H-07 pedía quitar; tampoco dice que las rutas genéricas cuentan una vez por objeto | Actualizar las tres líneas de la lista, quitar la de «Límites» y añadir la regla de H-08 | abierto |
| H-03 | baja | `r02_02 --copia`, apartado 3, cambio T03 | **Esperado** (README, «Límites»: lo que no se ve está dicho). **Obtenido:** que un CT-05 pierda una clase de `presupuesto_por_clase` en un ciclo (T03) sigue sin verse: la ruta genérica `presupuesto_por_clase.<clase>` sigue estando en todos los objetos. Es inherente a escribir la clave como `<clase>` y se parece al límite «claves opcionales mezcladas», pero no está dicho para las claves genéricas | Una línea en «Límites»: con claves `<clase>`/`<id>` no se ve que falte una de ellas en un objeto mientras quede otra | abierto |

## Invariantes

- No cambia código de producción ni el corpus (`tools/corpus_integridad.py` en verde, 695). ✔
- Re-congelado deliberado y con su motivo cierto (comprobado en (1) a (3) de `r01_01`). ✔
- Determinista: `goldens_ct.py` coincide en la copia y en la copia desechable. ✔
- Nada de secretos: `tools/secrets_scan.py` en verde. ✔
- Documentación: README de los goldens desfasado (H-02). ✔ con nota

## Veredicto

**APTO.** Los tres criterios se cumplen con evidencia ejecutada: ningún mutante vivo de los 20 de la mensajería, K01 a K03 detectados y los goldens coinciden sin cambios de producción. El re-congelado solo cambia lo que dice su motivo: con el código de antes de este commit los goldens nuevos coinciden, así que no esconde ninguna regresión del ejecutor. Quedan tres hallazgos bajos (el informe de pruebas sin rellenar, el README de los goldens desfasado y el límite de las claves genéricas sin declarar) que pasan a la deuda con su ID.

**Sin comprobar:** el gate entero (pasó en el commit); los goldens del Bloque A Forex (T-115).
