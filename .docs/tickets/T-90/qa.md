# T-90 · QA independiente

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación (subagente) · **Ronda:** r01 · **Fecha:** 2026-11-10
- **Objeto:** el cambio sin commit en `bloque_b/11_Ejecutor/bloque_b/orquestacion.py` (bucle de notas de `_f2_dims`) y la prueba nueva test_t90_nota_fuera_de_corte.py de las pruebas del ejecutor de B. Origen: H-01 de `.docs/tickets/T-64/qa.md`.

## Reproducción desde limpio

| Paso | Comando | Resultado |
| --- | --- | --- |
| Prueba nueva con el código anterior (copia limpia de HEAD `c4d0c5a` con `git worktree add --detach`, solo la prueba copiada) | `.venv/bin/pytest -q bloque_b/11_Ejecutor/tests/test_t90_nota_fuera_de_corte.py` | **1 failed**: `AssertionError: []` (`estados_degradados` vacío). La prueba detecta la regresión |
| Sonda S1 con el código anterior (misma copia) | sonda r01 con `RI_EJECUTOR_B` apuntando a la copia | falla solo `S1.declaradas_por_dim` (`[]`): sin la corrección la exclusión no deja rastro |
| Suite de B en el repo de trabajo | `.venv/bin/pytest -q bloque_b/11_Ejecutor` | **175 passed**, 1 aviso (pandas), 408 s |
| Gate completo sobre la copia limpia de HEAD + los dos archivos de B (sin los cambios de otros agentes en `sistema_global/`) | `.docs/scripts/gate.sh --completo` | RESULTADO_GATE |

La copia limpia se retiró al terminar con `git worktree remove`.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · la nota fuera de corte no está en F2 ni en el paquete, y `estados_degradados` del paquete la declara | sí | Prueba del implementador (pasa) y sondas S1, S2 y S6: ninguna nota con la marca de la sonda y fechas inválidas aparece entre los CLM de F2 ni en `dimensiones[].notas` del paquete; cada dimensión afectada aparece en `estados_degradados` con su especialista («D2: nota de AG-B04 excluida…»), y la fila «Estados degradados» de la portada del informe técnico la lleva completa |
| CA-2 · la prueba falla con el código anterior; la suite de B y el gate pasan | sí | Primera fila de la reproducción (falla con HEAD); suite de B 175/175; gate RESULTADO_GATE_CORTO |

## Ataques (sondas en revisores/ de este ticket: r01_comun.py y r01_sondas.py)

Ejecución: `.venv/bin/python` sobre r01_sondas.py (opcionalmente con `RI_EJECUTOR_B=<ejecutor de B>` para otra copia). Cada sonda lanza una petición completa (redes eléctricas, N2, cliente simulado) y añade notas a los informes dimensionales de todos los especialistas y del Director.

| Sonda | Qué ataca | Resultado |
| --- | --- | --- |
| S1 | Cinco notas en cuatro dimensiones: futura (2099), incoherente (publicación antes del hecho), ilegible («ayer»), conocible un día después del corte, y dos válidas (una en el borde exacto `conocible_desde == as_of`) | OK: solo las dos válidas llegan a F2 y al paquete; D2, D4, D8 y D9 declaradas con especialista; texto completo en el informe técnico y sus 40 primeros caracteres en la portada (G3B-ENT-09); G3 APTO en las dos pasadas; sin duplicados; la EVD de la válida conserva sus fechas |
| S2 | Formas raras de `fechas`: `None`, texto, lista, solo un campo, hora sin zona, campos en la raíz y futuros, números | OK: ninguna entra en F2 ni en el paquete, las siete dimensiones quedan declaradas, sin excepciones. Ver H-01 sobre la redacción |
| S3 | Dos notas excluidas del mismo especialista en la misma dimensión | Se excluyen las dos, pero el paquete deja una sola entrada en singular. Ver H-02 |
| S4 | Una nota excluida en D2 | OK, declarada |
| S5 | Determinismo: dos ejecuciones idénticas | OK: mismos `estados_degradados`, mismo orden (el de `ht03.DIMENSIONES`, no el de llegada de los hilos) y misma fila en el informe técnico |
| S6 | Una nota futura en cada una de las 12 dimensiones (máximo de entradas distintas, porque se deduplican por dimensión y especialista) | OK: ENTREGADA, G3 de fidelidad sin fallos; la fila mide 1310 caracteres y empieza en el 887, dentro de la portada de 4000 que exige G3B-ENT-09 |
| S7 | Entrega sin notas inválidas | OK: ninguna declaración T-90 (las notas válidas no se ven afectadas); margen de la portada para unas 29 declaraciones |

Revisión de código (sin script):
- La entrada solo interpola la dimensión (`d`, del vocabulario de `ht03.DIMENSIONES`) y el especialista (fijado por el ejecutor, nunca por el agente), así que el texto de la nota no llega a `estados_degradados`: no hay vía para inyectar contenido del LLM ni para disparar G3B-EST-06.
- `sintesis.py` deduplica con `dict.fromkeys` (orden estable) y la reanudación que repita F2 no duplica entradas. `limitaciones` nunca queda vacía (`sintesis.py`, valor por defecto), así que G3B-TMP-04 («estados degradados sin limitación») no salta.
- El `continue` sigue antes de crear la EVD y el CLM y antes de añadir la pieza a la ingesta del Curador (CT-B-15): la nota no deja rastro en F2 ni en lo que se envía a AG-B15. Falla cerrado como antes.
- La otra exclusión por fechas, en `_referencias_contraste` (CLM con fechas inválidas), opera sobre entradas que ya no pueden existir por este camino; no necesita declaración propia.
- Invariantes: no toca F ni G, ni el LLM en la ruta determinista, ni números; no hay decisiones del operador ni secretos.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | Sonda S2 (D6: solo `fecha_publicacion`; D7: hora sin zona; D1: `fechas: None`) | Esperado: la declaración distingue una fuga (fecha posterior al corte) de unas fechas incompletas o ilegibles. Obtenido: todas se declaran «…posteriores al corte o incoherentes (fuga de información)». El encargo de `_f2_dims` pide a los especialistas «Omite lo desconocido», así que una nota que lo cumpla con fechas parciales se excluye (comportamiento previo de T-64, correcto por falla cerrado) y además se rotula como fuga, lo que engaña al lector del informe técnico | Que `fechas_de_fuente` (o una variante) devuelva el motivo y el texto diga «posteriores al corte (fuga de información)» o «incompletas o ilegibles» según el caso | abierto |
| H-02 | baja | Sonda S3 | Esperado: saber cuántas afirmaciones desaparecieron. Obtenido: dos notas excluidas de AG-B04 en D2 dejan una sola entrada, «nota de AG-B04 excluida…», por la deduplicación de `estados_degradados` | Agrupar por dimensión y especialista y declarar el número («2 notas de AG-B04 excluidas…»); la entrada sigue siendo determinista y deduplicable | abierto |
| H-03 | baja | Leer pruebas.md y analisis-tecnico.md de este ticket | Esperado: el informe de la fase 3 (suite antes/después, CA → prueba, regresión y gate) y el análisis técnico. Obtenido: las dos plantillas sin rellenar con el ticket en EN QA. Además, la fila T-64 de `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` sigue diciendo que queda H-01 «en `limitaciones` o como incidencia», cuando la corrección lo declara en `estados_degradados` | Rellenar pruebas.md (las evidencias de esta QA sirven) y analisis-tecnico.md, y actualizar la fila T-64 al cerrar | abierto |

## Veredicto

**APTO** · los dos criterios se cumplen con evidencia propia (la prueba falla con el código anterior; suite de B 175/175; gate RESULTADO_GATE_CORTO sobre copia limpia) y ningún hallazgo crítico, alto ni medio. H-01, H-02 y H-03 son bajos: pasan a la deuda técnica con su ID si no se corrigen. El cierre del ticket (estado, deuda, diario, commit) queda para quien coordina, fuera del alcance de esta revisión.
