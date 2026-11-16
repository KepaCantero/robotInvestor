# T-159 · QA independiente

- **Revisor:** subagente de Claude sin contexto de la implementación (regla `compartida/2026-11-12_claude-puede-hacer-qa`) · **Ronda:** r01 · 16-11-2026
- **Copia revisada:** worktree desechable en el commit `6f3eb2b` (instantánea con T-159 y T-160), con `.venv` enlazado. Sin red ni gasto.

## Reproducción desde limpio

Desde la raíz de la copia (los scripts del revisor están en `revisores/`):

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t159_extremo_a_extremo.py tests/test_fase4_mapa.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py   # 1 falla: H-01
../../.venv/bin/python -m pytest -q -p no:cacheprovider                                    # suite completa, en segundo plano
cd ../..
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar                             # unos 7 min
.venv/bin/python .docs/tickets/T-159/revisores/r01_01_independencia_y_mutantes.py <copia desechable «qa31_…_mut» con bloque_a/ entero>
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
```

| Comprobación | Resultado |
| --- | --- |
| `test_t159_extremo_a_extremo.py` (10) y `test_fase4_mapa.py` | pasan |
| Suite completa de A (`-p no:cacheprovider`, una vez, máquina cargada) | 6752 superadas, 2 omitidas y 1 fallo en 1 h 15 min (carga ~10): `test_t102_filtro.py::test_r05_h37_sufijo_en_tiempo_lineal`, una prueba de tiempo (2,68 s frente a un tope de 2 s). Repetida sola dos veces: pasa una y falla otra con carga 11,8. Es de carga; ni la prueba ni el código que prueba cambian en la instantánea. Una primera ejecución se cortó por el `timeout` del revisor al 99 % sin ningún fallo hasta ahí |
| Evidencias regeneradas en la copia (`--ejecutar`) | «194 de 194 pruebas citadas superadas»; 31 Superada · 27 en parte; el fichero es **idéntico** al de HEAD salvo la línea del commit de la cabecera |
| Independencia del código (r01_01, parte 1) | `git diff HEAD~1 HEAD` del ejecutor y de `10_Herramientas` solo toca `evaluador.py`, `motor/servicio.py` y `motor/operaciones.py` (T-160). Las 10 pruebas de T-159 **pasan con el ejecutor de HEAD~1** (sin T-160): no dependen de ningún cambio de código. La siembra es solo de respuestas simuladas, proveedores de pruebas, la madurez leída por el Motor y `sintesis.construir` (PB-30) |
| Mutantes propios (r01_01, parte 2) | 10 mutantes, 9 muertos; P44b vive y es equivalente en ese escenario (tabla abajo) |
| Mapa del plan: pruebas citadas quitadas entre HEAD~1 y HEAD | ninguna; solo cambian las filas de los 8 (A), PB-32 (T-160), PB-52 y los «no comprueba» de los B nuevos |
| `test_fase4_mapa.py` (PB-02 → PB-08) | no debilita: PB-08 sigue PARCIAL con «no comprueba», así que el caso parametrizado sigue estropeando una fila PARCIAL y espera el mismo mensaje; PB-02 ya es AUTOMATICA y admite «no comprueba» vacío |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` en verde; `corpus_integridad`: 695 archivos coinciden |
| Cuotas | ruff 2825 (≤ 2825 de `tools/cuotas.txt`; el ticket pedía ≤ 2831) · mypy A 109 (≤ 109) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (37 casos clasificados con su motivo) | **no** | Tres clasificaciones no se sostienen: PB-47 no es A (H-01) y PB-25 y PB-46 no son C (H-02). Las otras 34 las he comprobado contra el código (abajo) y se sostienen |
| CA-2 (cada A con prueba que cita su PB y pasa) | sí, con H-01 | 10 pruebas en `tests/test_t159_extremo_a_extremo.py`, todas pasan; los mutantes de cada PB mueren salvo lo dicho en la tabla de mutantes |
| CA-3 (mapa, filas A en AUTOMATICA, el script sin problemas) | sí | `evidencias_plan_a.py`: «67 pruebas del plan, 194 citadas y todas existen · AUTOMATICA 31 … PARCIAL 27» |
| CA-4 (evidencias regeneradas, todas superadas) | sí | regeneradas en la copia, idénticas |
| CA-5 (los B nuevos en INC-T159-01) | **no** | Faltan G3-MET-13 (PB-47), la propagación de la baja de una referencia retractada a F2 (PB-25) y la recepción del CT-19 con la recalificación en F9 (PB-46) (H-01, H-02) |
| CA-6 (suite ≥ 607, gates, ruff ≤ 2831, mypy ≤ 109) | sí | arriba |

### Lo comprobado de cada (A)

| PB | ¿La prueba comprueba la cláusula que faltaba? | Escala reducida |
| --- | --- | --- |
| PB-02 | Sí: exactamente dos opciones, la marginal fuera porque decide su segunda pasada (P02 lo detecta), motivo de «menos de tres» con candidatas, motivo y condición, C03 OK, ningún umbral incumplido | 6 DIV en vez de 7, y la «E = 58» como segunda pasada de media 57,5: no vacía el criterio (la regla que se prueba es la misma) |
| PB-03 | Sí: cero ALT, GRIS, PS3 en el motivo de cada candidata, el técnico la detalla y el visual no la pinta (P03 lo detecta) | Una sola candidata ALT llega al análisis (el universo tiene 2 y una cae en el cribado, sonda de r01_02): basta para la regla «todas fuera por PS3 ⇒ cero opciones», está declarado. El hallazgo del Auditor es del modelo real |
| PB-30 | Sí: C08 bloquea, CT-14, retirada, segundo G3V- APTO, dos G3V-, la cifra fuera de todo entregable (P30 lo detecta). El tiempo ≤ 10 min es de tiempo real | — |
| PB-39 | Sí, el criterio («ningún visual entregado con < 70») en los dos caminos (P39 lo detecta). Lo del Redactor es del modelo real | — |
| PB-41 | Sí: clúster común de los tres tipos, `apuestas_independientes` = clústeres (P41 lo detecta), mismas OPP- y orden en los tres; las cifras (RK) las mira G3-ENT-07 (`redaccion.py`) | El factor común se siembra en el proveedor: declarado |
| PB-44 | Sí: recuento contra F4 y F3 con la invalidada y la descartada dentro y la NO_RESOLUBLE fuera y declarada (P44 lo detecta); mismo dato en los tres entregables; C01 | 9 semanas y no 28 opciones: declarado; se afirma la regla. Véase P44b |
| PB-47 | **No** (H-01) | — |
| PB-67 | Sí: PROPONER_ENVIO_A_B con HT-09 SEGUIMIENTO APTO, paquete, solo el CT-24 al Broker, F3 sin cambios | La sugerencia de N3 solo se comprueba como booleano (H-05) |

### Los (B) nuevos de INC-T159-01

Comprobados en el código: PB-09 (`proxima_ejecucion` solo tiene su definición), PB-13 (nadie lee `presupuesto_uc.rotacion_exploratoria`),
PB-29 (`grado_independencia` fijo a RAIZ, `orquestacion.py`), PB-34/PB-35 (ninguna corrección por fuga en F6; nada cierra un AJU-
EN_SOMBRA), PB-24/PB-20 (sin `FUENTE_RETIRADA` ni CT-21), PB-18 (HT-08 solo `ABRIR` y `CAR`), PB-08 (sin cola) y PB-52 (`Bloque._validar_g3`
llama a `sint.ht09_validar` sin protección). Las diez se sostienen. **PB-52** (sonda de r01_02): con HT-09 caído el ciclo lanza la
excepción y no entrega, no congela, no deja G3V- ni RUN- en F5 ni incidencia; sí deja **24 entradas en F2 y 16 en RC** de un run que
no existe (H-04). El ciclo siguiente, con HT-09 de vuelta, arranca, da APTO y no hereda ninguna opción del ciclo caído; la integridad
de todos los archivos sigue bien. Es B y está bien clasificado; la prueba fija lo que hoy es seguro (nada sale) y tendrá que cambiar
cuando exista el modo degradado.

### PB-25 y PB-46: ¿podrían ser «Superada»?

No. Las dos son **B** (más una parte C), no C:

- **PB-25.** El criterio es «Q recalculada con motivo; baja registrada» y el resultado esperado incluye la retractada «BORRAR con línea
  de baja y propagación a F2». El ejecutor no trata CONTENIDO_CAMBIADO ni RETRACTADA en ningún sitio (`grep` en `bloque_a/*.py`: cero
  apariciones; HT-02 solo se invoca desde la orden `verificar-enlaces` de `cli.py`), y la propagación de una baja es justo la función que
  falta en PB-24 (INC-T159-01). La recalificación de Q es del Documentador (C).
- **PB-46.** El criterio es «FUE- en F6; Q y orden actualizados en F9 con motivo». El CT-19 al Buscador (`Bloque._comunicar_fiabilidad`)
  se crea como RETORNO COMPLETO y nadie lo atiende: no hay llamada al Buscador con él ni F9 escribible en el almacén (`ARCHIVOS` no
  tiene F9). Con el modelo real tampoco se recalificaría nada: falta la función del receptor, no solo el modelo.

## Mutantes (r01_01)

Cada mutante, en una copia desechable de `bloque_a/` (código del ejecutor o la copia de referencia de HT-09 que usa), contra la
prueba de su PB:

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| P02 | HT-03 no recibe la segunda pasada | muerto |
| P03 | PS3 da por buena una invertibilidad falsa | muerto |
| P30 | C08 solo advierte de un CALC- sin artefacto | muerto |
| P39 | C12 solo advierte de un visual por debajo de 70 | muerto |
| P41 | `apuestas_independientes` distinto del número de clústeres | muerto |
| P44 | la nota no declara los NO_RESOLUBLE | muerto |
| P44b | el historial cuenta los contaminados | vivo, **equivalente** en ese escenario: con el simulado ningún PRG lleva `contaminacion_posible`; la exclusión de PA-09 la cubren `test_t66_evaluacion.py::test_pa09_*` |
| P47 | el Motor sirve una ficha DOCUMENTADO | muerto |
| P52 | con HT-09 caído, APTO por defecto | muerto |
| P67 | el C6 no propone el envío | muerto |

9 de 10 muertos y el que vive es equivalente.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | Desde `bloque_a/11_Ejecutor`: `../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47` | PB-47 pasa a «Superada», pero su preparación tiene dos partes y la prueba solo siembra la primera (ML-CLUS-001 en DOCUMENTADO). Con la segunda («un informe de clase que lo describe como validado», sembrable en el Analista simulado igual que en PB-02 y PB-03) los dos G3V- dan **APTO** y el informe técnico y el paquete JSON entregados dicen que el método está «validado». El plan espera BLOQUEADO hasta corregir (G3-MET-13), y el objetivo es que «nada se presente como validado sin estarlo». HT-09 no tiene ninguna comprobación de madurez en el texto (no hay G3-MET-13 en `ht09_validador_g3.py` ni en el ejecutor). El «no comprueba» del mapa lo achaca a que «el simulado no escribe esa palabra», pero lo que falta es la función | PB-47 vuelve a PARCIAL con la causa real en «no comprueba»; G3-MET-13 a INC-T159-01 como B nuevo; la prueba de T-159 se queda (lo que comprueba es cierto) | abierto |
| H-02 | media | Lectura de código: `grep -rn "RETRACT\|CONTENIDO_CAMBIADO" bloque_a/11_Ejecutor/bloque_a` (nada); `orquestacion.py`, `_comunicar_fiabilidad` (el CT-19 nace COMPLETO, sin receptor); `almacen.ARCHIVOS` (sin F9) | PB-25 y PB-46 se clasifican C («solo el modelo real») y la nota sugiere que podrían ser «Superada». Les falta una función del ejecutor (propagación de la baja a F2; recepción del CT-19 y escritura de Q y orden en F9). No deben pasar a «Superada» | Reclasificar las dos como B (con su parte C), corregir la nota de `analisis-tecnico.md` y añadirlas a INC-T159-01 (PB-25 puede remitir a PB-24) | abierto |
| H-03 | baja | `docs/incidencias.md`, INC-T159-01 | Dice «diez casos»; con H-01 y H-02 son trece | Al corregir H-01 y H-02 | abierto |
| H-04 | baja | `-k pb52` en `r01_02_sondas.py` (imprime lo que añade el ciclo caído) | El ciclo que termina con la excepción de HT-09 deja 24 entradas en F2 y 16 en RC de un RUN- que no está en F5. No es inseguro (el ciclo siguiente no las hereda), pero el modo degradado que falte tendrá que cerrarlas o anotarlas | Añadirlo a la descripción de PB-52 en INC-T159-01 | abierto |
| H-05 | baja | `tests/test_t159_extremo_a_extremo.py::test_pb67_…` | La sugerencia de N3 («si la evidencia es antigua») solo se comprueba como booleano; la regla (`seguimiento.py`: material o más de 30 días) no | Afirmar el valor esperado con la fecha de la última actualización de la opción | abierto |

Los scripts de esta ronda están en `revisores/`: `r01_01_independencia_y_mutantes.py` y `r01_02_sondas.py`.

## Veredicto

**NO APTO** · CA-1 y CA-5 no se cumplen: PB-47 se da por «Superada» sin comprobar la mitad de su preparación, que hoy no bloquea
(H-01), y PB-25 y PB-46 no son de «solo modelo real» (H-02), así que tres funciones que faltan no llegan a INC-T159-01. Las otras siete
(A), las diez (B) nuevas, PB-52, la independencia del código, las evidencias y los gates están bien. Para la r02: corregir H-01 a
H-03 (mapa, análisis e incidencia; sin código del ejecutor), regenerar las evidencias (quedarán 30 «Superada» y 28 «en parte» con
T-160) y volver a ejecutar estos scripts.

## Ronda r02

- **Revisor:** el mismo subagente de la r01 · 16-11-2026 · copia: worktree desechable en la instantánea `2d72ceb`, con `.venv` enlazado. Sin red ni gasto.
- **Qué cambió:** solo el mapa (PB-25, PB-46 y PB-47), `analisis-tecnico.md` (sección «Ronda r02»), INC-T159-01 y el estado del README. Ni
  `tests/test_t159_extremo_a_extremo.py`, ni `tests/test_fase4_mapa.py`, ni el código que vigilan (`orquestacion.py`, `sintesis.py`,
  `evaluador.py`, `seguimiento.py`, `motor/servicio.py`, HT-09) cambian desde `6f3eb2b`. El código que sí cambia en la instantánea
  (`cli.py`, `guias.py`, `herramientas/verificador_ids.py`) es de T-161 y de la r02 de T-157, no de este ticket.

### Reproducción

Desde la raíz de la copia:

```bash
.venv/bin/python .docs/scripts/evidencias_plan_a.py                       # comprobación del mapa
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar            # regenerar y comparar con la de HEAD, salvo la cabecera
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase4_mapa.py tests/test_t159_extremo_a_extremo.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py   # 1 falla a propósito (PB-47)
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
```

| Comprobación | Resultado |
| --- | --- |
| Mapa (`evidencias_plan_a.py`) | «67 pruebas del plan, 196 pruebas automáticas citadas y todas existen · AUTOMATICA 30, DOCUMENTAL 1, PARCIAL 28, PENDIENTE_API 7, REQUIERE_USUARIOS 1»; JSON válido |
| Pruebas citadas que se pierden (mapa de `6f3eb2b` frente al de `2d72ceb`, fila a fila) | **ninguna**. Cambian PB-25 y PB-46 (solo «no comprueba»), PB-47 (AUTOMATICA → PARCIAL y «no comprueba») y PB-48 (dos pruebas más, de T-161) |
| `test_fase4_mapa.py` y `test_t159_extremo_a_extremo.py` | 33 superadas |
| Evidencias regeneradas en la copia (`--ejecutar`) | «196 de 196 pruebas citadas superadas»; 30 Superada · 28 en parte; PB-25, PB-46 y PB-47 «Superada en parte»; **idénticas** a las de la instantánea salvo la cabecera (fichero restaurado después) |
| `r01_02_sondas.py` | igual que en la r01: con la preparación completa de PB-47, G3 APTO y «validado» en el técnico y el JSON entregados (lo que ahora dice el mapa); PB-52 y PB-03, iguales |
| `r01_01_independencia_y_mutantes.py` | no se repite: ni las pruebas de T-159 ni el código que vigilan sus mutantes han cambiado desde la r01 (`git diff --stat 6f3eb2b HEAD` vacío en esas rutas) |
| Gates ligeros | `refs_vivas`, `secrets_scan` y `nfc_check` en verde; corpus 695 coinciden; `git diff --check` limpio en el mapa, la incidencia y el ticket |

### ¿Dicen la verdad del código?

| Cambio | Contraste | Veredicto |
| --- | --- | --- |
| PB-47: «G3-MET-13 no existe en HT-09; un informe que llama «validado» a un método DOCUMENTADO pasa como APTO y lo entregado dice «validado»» | Ni `10_Herramientas/ht09_validador_g3.py` ni la copia de referencia del ejecutor tienen una comprobación así; la sonda lo reproduce | cierto |
| PB-25: «el ejecutor no trata CONTENIDO_CAMBIADO ni RETRACTADA; la baja no se propaga a F2» | `grep` en `bloque_a/11_Ejecutor/bloque_a/*.py`: ninguna aparición | cierto (la frase «no se recalcula Q en F9» y después «el recálculo lo hace el Documentador» mezcla la parte B con la C, pero no afirma nada falso) |
| PB-46: «el CT-19 al Buscador se crea COMPLETO y nadie lo atiende; no hay en F9 dónde escribir» | `orquestacion.py`, `_comunicar_fiabilidad`: `tipo_mensaje="RETORNO", estado="COMPLETO"`; `almacen.ARCHIVOS` no tiene F9 | cierto |
| INC-T159-01: trece casos con PB-47, PB-25 y PB-46 | los tres añadidos con el hueco correcto | cierto, con R02-H-06 |
| H-04 y H-05 como observaciones | H-04: las entradas de F2 y RC del ciclo caído no se heredan (sonda); H-05: el criterio de aprobación de PB-67 es «HT-09 SEGUIMIENTO APTO; sin envío automático», y la sugerencia de N3 es del resultado esperado y condicional | aceptable |

### Hallazgos de la r01

| ID | Estado |
| --- | --- |
| H-01 | corregido: PB-47 en PARCIAL con la causa real; G3-MET-13 en INC-T159-01 |
| H-02 | corregido: PB-25 y PB-46 con su función que falta en el mapa y en INC-T159-01 |
| H-03 | corregido en el título (con R02-H-06) |
| H-04, H-05 | observaciones, con su motivo en «Ronda r02» de `analisis-tecnico.md` |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| R02-H-06 | baja | `grep -n "INC-T159-01" docs/incidencias.md` | El título dice «trece casos», pero la frase siguiente sigue diciendo «estos diez no se cierran con una prueba» | «estos trece» | abierto |
| R02-H-07 | baja | `.docs/tickets/T-159/analisis-tecnico.md`, líneas 11 a 15, 33, 46, 47 y 57; `README.md`, «Registro» | La clasificación de arriba sigue diciendo A (8), B (27), C (2), PB-47 A («no dice validado»), PB-25 y PB-46 C, y la «Nota sobre los (C)» sigue sugiriendo moverlas a «Superada». Solo la sección «Ronda r02» del final lo corrige; el registro del README no tiene la línea de la r02 | Marcar en la tabla las tres filas (p. ej. «B (r02)»), tachar o retirar la nota sobre los C y añadir la línea de la r02 al registro | abierto |

Ninguno es crítico, alto ni medio: los dos son de texto y la fuente que manda (mapa, evidencias e incidencia) ya es correcta.

### Veredicto r02

**APTO** · H-01 a H-03 están corregidos y los cambios dicen la verdad del código. El mapa no pierde ninguna prueba citada,
`test_fase4_mapa.py` pasa y las evidencias regeneradas coinciden con las de la instantánea (30 «Superada», 28 «en parte»,
196 de 196). Los gates ligeros están en verde. Quedan dos bajos de texto (R02-H-06 y R02-H-07), que pasan a la deuda o se arreglan
al cerrar. Por encargo, el revisor no cierra el ticket ni toca la deuda.
