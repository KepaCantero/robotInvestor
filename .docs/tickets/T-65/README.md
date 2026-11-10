# T-65 · Hallazgos bajos de la QA de T-53 y resto técnico de T-53 (Bloque A)

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a |
| Planifica · implementa · QA | claude · claude · el otro agente (Astra) o un revisor nuevo sin contexto |
| Aprobación del operador | No necesaria: es una corrección técnica. Los valores que decide el operador van como `[PROPUESTO]` en `bloque_a/11_Ejecutor/config/por_defecto.yaml` y se listan abajo para T-57 |
| Deuda técnica | T-65 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (y H-20 y H-21 de la fila T-67) |

## Objetivo

Cerrar los hallazgos bajos que dejó la QA de T-53 en el Bloque A (H-07 a H-17), dos bajos de la QA de T-66 (H-20 y H-21) y el resto técnico de T-53 (CA-14 resto, CA-15, CS-08, CS-10 resto, CS-11, CS-18, CS-19, CS-23), antes de conectar A en la Fase 1. Sin llamadas reales a la API, sin otro proveedor y sin tocar el corpus congelado.

Fuentes: `.docs/tickets/T-53/qa.md`, `.docs/tickets/T-53/analisis-tecnico.md`, `.docs/tickets/T-53/revisores/codigo.md`, `.docs/tickets/T-53/revisores/consistencia.md`, `.docs/tickets/T-66/README.md` y `.docs/tickets/T-66/qa.md`.

## Alcance, punto por punto

Todas las rutas de código son relativas a `bloque_a/11_Ejecutor/`. Las pruebas nuevas están en `tests/test_t65_hallazgos.py` (TH) y `tests/test_t65_resto_t53.py` (TR); la de H-11, en `.docs/scripts/prueba_refs_vivas.py`.

| Punto | Qué pasaba | Qué se hace (o por qué no, y adónde va) | Prueba |
| --- | --- | --- | --- |
| H-06 | Todo el alcance pausado: el run redactaba y caía en el esquema | **Ya hecho en T-66** (el run se cierra sin redactar, PARCIAL y con sus limitaciones). Comprobado en el código (`orquestacion.py`, «no queda ningún tipo que analizar») | `test_t66_propuestas.py::test_h06_todo_pausado_no_redacta_ni_falla_en_el_esquema` |
| H-07 | `fijar_bandas` escribía la tabla de bandas en una variable global del módulo | La tabla vive en el `Evaluador` (`self.bandas`) y la síntesis usa la de su instancia; las funciones del módulo usan siempre la del Anexo A. `fijar_bandas` pasa a `validar_bandas`, que valida y devuelve, sin efectos | TH `test_h07_*` |
| H-08 | `A_profundizar: 65` sin origen; los valores del YAML repetidos como literales en el código | `A_profundizar` (y el resto del semáforo y el siguiente paso) quedan `[PROPUESTO]` con su pregunta. Nuevo `configuracion.parametro(cfg, "seccion.clave")`: valor de la configuración recibida o, si falta, de `por_defecto.yaml`; si tampoco está, `KeyError` (falla cerrado). Sustituye los `.get(clave, literal)` de números de configuración del paquete | TH `test_h08_*` |
| H-09 | Las decisiones de INC-T53-01 a 05 no estaban marcadas `[PROPUESTO]` en la configuración | Marcadas en `por_defecto.yaml` junto a su clave (01 en `parametros_ht03`, 02 en PS2, 03 en `ece_revocacion`, 04 en la degradación de H5, 05 en `seleccion` y `presentacion`). `docs/incidencias.md` no se toca (fuera del alcance de este ticket): la lista para T-57 está abajo | TH `test_h09_*` |
| H-10 | (a) el paquete en memoria seguía con `estado_g3` favorable tras bloquear; (b) el C6 bloqueado en backtest iba a otra carpeta que la redacción; (c) `DatosInvalidos` se declaraba como «sin datos» y sin incidencia | (a) se quita `estado_g3` del paquete bloqueado; (b) una sola función `carpeta_bloqueados` para la redacción y el C6; (c) motivo propio («datos HT-01 inválidos») e incidencia `DATOS` en HA | TH `test_h10_*` |
| H-11 | `refs_vivas` dejaba de revisar todas las carpetas `revisores/` | Se quita la excepción general. Para no dar falsos rotos en los informes: una cita con argumentos (`script.sh --opcion`) se comprueba por su primera palabra, se quita el sufijo de líneas (`archivo.py:10-20`) y una ruta de paquete Python (`bloque_a/…` dentro de `11_Ejecutor/`) cuenta como viva. El script está en `tools/refs_vivas.py` (no en `.docs/scripts/`); su prueba, en `.docs/scripts/prueba_refs_vivas.py` | `.docs/scripts/prueba_refs_vivas.py` |
| H-12 | Dos `Bloque` compartían la tabla de horizontes | **Ya hecho en T-53** (QA r02: copia propia de la configuración y `_tabla_base`) | `test_t53_seleccion_y_entrega.py::test_h12_dos_bloques_con_la_misma_configuracion_no_comparten_la_tabla_de_horizontes` |
| H-13 | La degradación de H5 registraba `fecha_efecto` = as_of + 1 y se aplicaba en el mismo ciclo | `efecto_desde` y `fecha_efecto` = as_of, con la nota «se aplica desde este ciclo» | TH `test_h13_*` |
| H-14 | Ninguna prueba llegaba a la rama «fichas del Motor rechazadas» | Prueba que fuerza un RECHAZADO de una ficha del lote (`monkeypatch` de `Motor.servir`) y comprueba la laguna y el estado PARCIAL | TH `test_h14_*` |
| H-15 | Un símbolo con cierres a 0 o fechas duplicadas vaciaba su tipo; los negativos no se declaraban | HT-01 rechaza las series con cierres ≤ 0 y con fechas duplicadas como `DatosInvalidos`; el cribado excluye y declara el símbolo ante `DatosInvalidos` o cualquier error del proveedor para ese símbolo (salvo la fuga de información, que sigue cortando) | TH `test_h15_*` |
| H-16 | Un finalista con poca historia hacía rechazar ML-CLUS-001 entero | Se excluyen del cálculo los proxies con menos de `clusteres.min_semanas_proxy` rendimientos semanales en la ventana, se declaran como limitación y cada uno queda en un clúster propio; los demás se agrupan | TH `test_h16_*` |
| H-17 | `ps2_festivos` no se validaba; el lunes de Pascua no estaba | Se valida al crear el `Bloque` (claves conocidas, booleanos y lista de «MM-DD» válidos; si falta, error claro). Nueva clave `lunes_de_pascua` (`[PROPUESTO]`: false, igual que hoy); el valor lo fija el operador en T-57 | TH `test_h17_*` |
| H-20 | Un contenedor de objeciones de F3 que no es una lista contaba como «sin objeciones» | Un contenedor que no es lista ni `None` cuenta como una fuerte abierta («contenedor mal formado en F3») | TH `test_h20_*` |
| H-21 | Incidencias R9 de la contrarréplica sin `run_id`, una por cita, y saneado del texto propio | `_contenido_evidencia` recibe el `run_id`; una incidencia por (fuente, run); se sanea solo lo externo: las REF- y las piezas de origen desconocido. Las piezas del código (AG-13), de los Analistas y de AG-14/AG-16 (ya saneadas al entrar) llegan como están | TH `test_h21_*` |
| CA-14 resto | Sesiones por horizonte duplicadas, zona de interés ±5 %, tasa base 0,5 y recorte, umbral C6 0,05 con σ NaN | Las sesiones salen de `horizontes` y de `calendario` (5 sesiones por semana, 21 por mes, mismos valores que antes); zona de interés y confianza en `presentacion` (`[PROPUESTO]`); tasa base (ventana, mínimo de ventanas, valor sin historia y recorte) en `tasa_base` (`[PROPUESTO]`, técnico); en C6, sin σ semanal el delta cuenta como material y se declara (falla cerrado) | TR `test_ca14_*` |
| CA-15 | F5 cambiaba el orden de `participantes` y los `msg_id` del paralelo dependían de los hilos | `participantes` ordenados por agente. Los mensajes creados dentro del análisis paralelo de un tipo llevan un contador propio de ese tipo (`MSG-<TIPO>-AAAA-nnnnnn`), así que no dependen del orden de los hilos. El orden de `cache_resultados.jsonl` no se toca: se busca por clave y su contenido coincide | TR `test_ca15_*` |
| CS-08 | El Motor servía 3 fichas que el Catálogo da por DOCUMENTADO | ACC-ERP-001, FX-MOM-001 y REI-CAP-001 se rechazan con `METODO_NO_IMPLEMENTADO` (manda el Catálogo); el código se conserva. Las alternativas que apuntaban a ellas dejan de ofrecerse. Ningún camino del ciclo las usa. Promoverlas exige cambiar el Catálogo: revisión del corpus con el operador | TR `test_cs08_*` |
| CS-10 resto | Rotación exploratoria de 2 celdas fijas; 200 réplicas en la evaluación de la resolución; PS1, bandas de recalibración de RK y pregunta repetida con números en el código | Las réplicas y simulaciones salen de `evaluacion`; el número de celdas de rotación pasa a `seleccion.rotacion_exploratoria_celdas` (`[PROPUESTO]`); PS1, recalibración de RK y pregunta repetida a la configuración con su P-xx. **No se hace:** traducir el «20 % del presupuesto de cribado» (P-07) a celdas exige un coste por celda que no está en el Anexo A → T-57 (con la revisión del corpus) | TR `test_cs10_*` |
| CS-11 | Parámetros de HT-03 en una clave oculta; regímenes de F10 incompletos; P-30 con respaldo «4.0»; F10 con 9 de 44 parámetros | Sección explícita `parametros_ht03` en el YAML (iguales a HT-03 del corpus, con prueba de igualdad); se completan `PARAMETROS_CALIBRABLES` (P-35, P-36, P-39, P-40) y `PARAMETROS_SERVICIO` (P-34, P-38, P-44); P-30 sale de `methodology_version`. **No se hace:** dar de alta en F10 los 44 parámetros (muchos con valor `PENDIENTE_OPERADOR`) → T-83 y T-57 (con PA-11 de T-67) | TR `test_cs11_*` |
| CS-18 | El código pedía 2 años semanales para ML-CLUS-001; el Catálogo pide ≥ 3 años semanales | La ventana sale de `clusteres.ventana_semanas`, que pasa a 156 (Catálogo) y fija también el inicio de los datos. **No se hace:** el prompt del Analizador dice ρ ≥ 0,6 y el Catálogo 0,7; alinearlo es editar el corpus → revisión del corpus con el operador | TR `test_cs18_*` |
| CS-19 | El mapa de pruebas estaba desfasado frente al plan V3.0 | Rehecho: título, 67 pruebas, PB-53 a PB-57, versiones de PB-12 y PB-13, PB-33 y PB-64 con sus pruebas, y las pruebas de T-53, T-66 y T-65 | TR `test_cs19_*` |
| CS-23 | `herramientas/__init__.py` citaba una prueba inexistente | Corregido (`test_unitarias.py::test_herramientas_de_referencia_sin_divergencia`) | TR `test_cs23_*` |

## Correcciones de la QA r01 (NO APTO, `qa.md`)

Pruebas en `bloque_a/11_Ejecutor/tests/test_t65_qa_r01.py` (QR); las de H-01, H-02 y H-03 fallan con b699d4f.

| Hallazgo | Qué se hace (o por qué no, y adónde va) | Prueba |
| --- | --- | --- |
| H-01 (media) | `valor_en` valida solo el cierre que devuelve, y `cierres` solo el rango pedido: un cierre malo antiguo, fuera de la ventana, no importa. Si el precio de un símbolo no se puede leer, el símbolo se excluye, se declara y deja una incidencia `DATOS` (antes quedaba sin precio en silencio) | QR `test_r01_h01_*` (3) |
| H-02 (media) | Cualquier error al leer el CSV (vacío, binario, codificación) es `DatosInvalidos` del símbolo: se excluye y se declara, y el ciclo de los demás tipos sigue | QR `test_r01_h02_*` |
| H-03 (media) | `pruebas.md` ya no cita el log de `.docs/scripts/.logs/` con forma de ruta | gate `refs-vivas` en una copia limpia (`pruebas.md`) |
| H-04 | `fijos` exige «MM-DD» con dígitos ASCII y sin espacios (`re.fullmatch`), además de una fecha real | QR `test_r01_h04_*` |
| H-05 | Pasan a `parametro()`: `seguimiento.frecuencias` y `frecuencia_orientativa_dias`, `uc.motor_por_plan`, `max_tokens.por_defecto`, el texto de GC0, el suelo de la bolsa COMÚN (`presupuesto_uc.fraccion_minima_comun`, nuevo, `[PROPUESTO]` técnico), la tasa base de los hitos H5 y los «10 días hábiles» de `regla_fallback` y de `NO_RESOLUBLE`. Quedan literales algorítmicos (redondeo de la probabilidad de Prospectiva a 0,05, familias de la señal compuesta), anotados en los límites de `analisis-tecnico.md` | QR `test_r01_h05_*` (2) |
| H-06 | `refs_vivas` comprueba, en una orden, el script y cada argumento con forma de ruta del repo | `.docs/scripts/prueba_refs_vivas.py` (8 casos; con el script de b699d4f, 7/8) |
| H-07 | Los proxies de ML-CLUS-001 se eligen por solape: en orden determinista (más semanas primero) entran los que mantienen ≥ `min_semanas_proxy` semanas comunes con los ya elegidos; los demás se declaran | QR `test_r01_h07_*` |
| H-08 | Pruebas de efecto con otro valor en la configuración para la pregunta repetida, la recalibración de RK (paso y bandas) y PS1 (la regla pasa a `Bloque._ps1`) | QR `test_r01_h08_*` (3) |
| H-09 | `docs/incidencias.md`: INC-T53-02 a 05 marcadas `[PROPUESTO]` (hasta T-57); INC-T53-04 ya no dice «pendiente en T-53» y recoge H-13; INC-T53-02 recoge la validación y `lunes_de_pascua` | lectura |
| H-10 | **No se hace:** el consumo por tipo de F5 con hilos (`presupuesto.<tipo>.consumido`) no es de T-65 y pide asignar en orden determinista el consumo de las llamadas compartidas entre hilos. **Destino: deuda técnica** (fila nueva o dentro de T-65 restante, la abre el coordinador), antes de conectar A en la Fase 1 | — |
| H-11 | El texto de la limitación usa coma decimal («tasa base 0,5 por defecto») | QR `test_r01_h11_*` |

## Diseño

- **Contratos CT-G:** ninguno. Los esquemas internos de A no cambian.
- **Estado persistido:** sin migración. F10 y F6 llevan las mismas claves; cambia solo el valor de `efecto_desde`/`fecha_efecto` (H-13) en las degradaciones nuevas. Los `msg_id` de los mensajes del paralelo cambian de forma (CA-15); no se guardan como clave en ningún archivo F.
- **Números nuevos o movidos** (todos en `config/por_defecto.yaml`):
  - `calendario: {sesiones_por_semana: 5, sesiones_por_mes: 21}`: técnico (convención de mercado).
  - `tasa_base: {ventana_anios: 3, min_ventanas: 5, sin_historia: 0.5, recorte: [0.05, 0.95]}`: técnico `[PROPUESTO]`.
  - `presentacion: {zona_interes: 0.05, confianza_probable_E: 70}`: `[PROPUESTO]` (INC-T53-05).
  - `senales: {ventana_anios: 3, margen_dias: 30}`: la ventana del lote de fichas que ya estaba en el código.
  - `clusteres.ventana_semanas: 156` (Catálogo, ML-CLUS-001) y `clusteres.min_semanas_proxy: 52` `[PROPUESTO]`.
  - `ps1.raices_min: 2` (Anexo A, P-14), `pregunta_repetida: {veces: 3, semanas: 4}` (P-26), `evaluacion.recalibracion_rk: {paso: 0.05, banda_trimestral: 0.05, banda_total: 0.15}` (P-11).
  - `seleccion.rotacion_exploratoria_celdas: 2` `[PROPUESTO]`; `seguimiento.min_semanas_sigma: 6`.
  - `ps2_festivos.lunes_de_pascua: false` `[PROPUESTO]`.
  - `parametros_ht03`: copia explícita de los valores de HT-03 (Anexo A); una prueba exige que coincidan con el corpus.
- **Cómo falla cerrado:** una clave numérica que falta en la configuración y en `por_defecto.yaml` lanza `KeyError`; `ps2_festivos` mal formado impide crear el `Bloque`; un símbolo con datos inválidos se excluye y se declara; sin σ semanal, el delta del C6 es material; un contenedor de objeciones mal formado es una fuerte abierta; las fichas DOCUMENTADO no dan cifras.
- **Decisiones del operador usadas como `[PROPUESTO]`** (para T-57; la fila de la deuda la actualiza el coordinador):
  1. Semáforo y siguiente paso: `E_verde 70`, `A_verde 65`, `E_enviar 70`, `A_profundizar 65`. Pregunta: «¿Con qué solidez mínima (E) y atractivo mínimo (A) se propone enviar una opción al Bloque B o seguir estudiándola?» (INC-T53-05).
  2. Confianza «probable» con E ≥ 70 y zona de interés ±5 % del minigráfico (INC-T53-05).
  3. H1 de PS2 en sesiones hábiles y la lista de festivos, ahora con `lunes_de_pascua` (INC-T53-02).
  4. `ece_revocacion` 0,12 (INC-T53-03).
  5. «Limitado → No» de H5 como propuesta de tipo 3 (INC-T53-04).
  6. Diversidad con tres opciones del mismo clúster (`diversidad_margen_rk`, INC-T53-01).
  7. `seleccion.rotacion_exploratoria_celdas` 2 frente al 20 % de P-07; `clusteres.min_semanas_proxy` 52; `tasa_base` (técnico).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Cambiar la ventana de ML-CLUS-001 (104 → 156 semanas) | Otros clústeres en algunas fechas y, con ellos, otra diversidad del top-3 | Suite completa antes y después; si cambia una prueba, se analiza y se anota en `pruebas.md` |
| `parametro()` sustituye muchos `.get(…, literal)` | Un error de ruta deja una clave sin leer | Las pruebas de configuración recorren todas las rutas usadas en el paquete contra `por_defecto.yaml` |
| Validar cierres > 0 en HT-01 | Una serie de niveles que puede ser negativa (tipos, diferenciales) deja de servir | Hoy el pipeline calcula rentabilidades como cociente: con niveles negativos no tienen sentido. Esas series deben llegar como índice de rentabilidad total; se declara en el README del ejecutor |
| Otro agente trabaja en `sistema_global/` y en `.docs/tickets/T-80/` | El gate `refs-vivas` puede fallar por sus archivos | No se tocan; si el gate falla por ellos, se anota en `pruebas.md` |

## Criterios de aceptación (binarios)

1. CA-1: cada punto de la tabla marcado como hecho tiene al menos una prueba que falla sin la corrección (comprobado quitando la corrección).
2. CA-2: cada punto ya hecho cita la prueba existente que lo demuestra, y esa prueba pasa.
3. CA-3: cada punto no hecho (o hecho en parte) tiene su motivo y su destino en este README.
4. CA-4: ningún número nuevo se escribe en el código: sale de `por_defecto.yaml`, y los del operador llevan `[PROPUESTO]`.
5. CA-5: la suite de `bloque_a` pasa entera y sube de 201; el gate completo da 12/12 (o, si falla, solo por archivos ajenos a este ticket, con la evidencia).
6. CA-6: no se toca `sistema_global/`, `bloque_b/`, `bloque_a_forex/`, `.docs/memoria/`, el diario ni la deuda técnica; el corpus congelado no cambia.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t65_hallazgos.py` (H-07 a H-21) | regresión y fallo cerrado | CA-1, CA-4 |
| `test_t65_resto_t53.py` (CA-14 a CS-23) | regresión, límite y fallo cerrado | CA-1, CA-4 |
| `.docs/scripts/prueba_refs_vivas.py` | regresión del gate | CA-1 |
| Pruebas de H-06 y H-12 ya existentes | regresión | CA-2 |
| Suite completa de `bloque_a` y `.docs/scripts/gate.sh --completo` | integración | CA-5 |
| Mutaciones: quitar cada corrección y ver fallar su prueba | regresión | CA-1 |

## Scripts

- Usa `.docs/scripts/nuevo_ticket.sh` y `.docs/scripts/gate.sh` con `--completo`.
- Crea `.docs/scripts/prueba_refs_vivas.py` (prueba del gate `refs-vivas`). Falta apuntarlo en la tabla de scripts de `.docs/README.md` (fuera del alcance de este ticket; lo hace el coordinador).

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · PLANIFICADO · claude · plan punto por punto; tarea técnica, sin aprobación del operador
- 2026-11-10 · EN CURSO · claude · implementación en `bloque_a/` y `tools/refs_vivas.py`
- 2026-11-10 · EN QA · claude · ver `pruebas.md`
- 2026-11-10 · QA r01 NO APTO (H-01 a H-03 medios; H-04 a H-11 bajos)
- 2026-11-10 · EN CURSO · claude · correcciones de la r01: H-01 a H-09 y H-11 corregidos con su prueba; H-10 a la deuda técnica
- 2026-11-10 · EN QA · claude · pendiente de la r02; ver `pruebas.md`
