# T-145 · QA independiente

- **Revisor:** revisor nuevo (subagente de Claude sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-15
- Copia git `qa18` sobre `6df54b3` (desconectada), intérprete del repositorio. Sin red, sin API y sin servicios de pago: el
  cliente real (`llm.AnthropicClient`), con un SDK falso local.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A (`pytest -q -p no:cacheprovider`, una vez) | **6131 passed** (21 min 15 s); 6092 + las 39 de `test_t145.py` |
| `tests/goldens_ct.py` | coinciden |
| ruff (los tres ejecutores, desde la raíz) | **2838** (cuota ≤ 2838) |
| mypy A (como el gate) | **109** (cuota ≤ 109) |
| `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | en verde (695 archivos del corpus) |
| `medir_consumo_a.py` + `estimar_coste_ciclo_a.py`, solo divisas / 12 tipos | 0,86 · 4,58 · **19,54** (68,29 por presupuesto) / 2,98 · 56,79 · **166,56** (233,18): las del README |
| T-140 `r01_01` (div / 12) | 9,81 / 79,33 USD, por debajo de 19,54 / 166,56 |
| T-140 `r01_02` (div, div C12, 12, 12 C12) | 4,57 · 5,04 · 36,02 · 36,53 USD, por debajo |
| T-140 `r01_03 <contratos de T-136>` | 14 falsos positivos (fila de 8, declarada); los negativos que quedan, todos en INC-T123-01 |
| T-140 `r01_04` | 19 ok, 0 fallos |
| `contraste_cota.py` (div) | ningún encargo alargado pasa del supuesto S4 |
| `mutantes_t145.py` (copia desechable `qa18_mut_impl`) | **19 de 19 muertos** |
| `borrador_anexo_b.py --comprobar` | 0 (el borrador coincide con lo que genera) |
| `./tools/check_all.sh`, B | no lanzados (instrucción del encargo) |

## Recuento de llamadas de un ciclo C1 (código leído, no el script)

`orquestacion.py` (`ciclo`, `_analizar_clase`, `_peticion_conocimiento`, `_refutacion`, `_registrar_evidencia_clase`,
`_integrar`, `_validar_g3`, `_redactar`, `_auditar`, `_informe_aprendizaje`) y `agentes.py` / `llm.py`:

- **Por tipo (N2):** cribado 1; peticiones de conocimiento ≤ `seleccion.peticiones_conocimiento_por_clase` (el bucle corta
  al llegar al máximo; CT-07 a AG-16, si no a AG-14, ambos con búsqueda); prospectiva 1 (si hay finalistas con GC3);
  refutación 1 (solo N2/N3); respuesta a objeciones 1 (si hay fuertes o moderadas); contrarréplica 1 (si el Analista da
  una fuerte por resuelta con evidencia citable); curación 1 (N2/N3 con piezas). N1 hace menos. Coincide con `LLAMADAS_POR_TIPO`.
- **Por ciclo:** AG-20 ≤ 1 (solo con pronósticos resueltos); AG-02 1; AG-18 ≤ 2 (`_validar_g3` corta en el segundo intento);
  AG-17 ≤ 2 (una sola reescritura por C12); AG-19 ≤ 1. Ni el Evaluador, ni la síntesis, ni `redaccion.generar` llaman a un
  modelo. Coincide con `LLAMADAS_DEL_CICLO`.
- **Por llamada:** `1 + llm.reintento_reparacion` intentos; en un agente con búsqueda, cada intento hasta
  `1 + max_continuaciones_pause_turn` peticiones (un turno que sigue en `pause_turn` corta sin reparación). La reparación
  reenvía `r.texto` (solo la última respuesta de ese intento) y hasta 15 errores de ≤ 300 caracteres más «respuesta
  truncada por max_tokens» (16 en el peor caso; el script cuenta 15: unos 85 tokens de diferencia, despreciable). La
  continuación reenvía el contenido pausado, con los bloques de la búsqueda (fuera, S5). Coincide con `peor_llamada`.

## Hallazgo declarado por el implementador: el presupuesto en UC no corta antes de la llamada

**Confirmado.** `_invocar` compara `_estimar_uc` (encargo/3,6 + 1500, sistema como lectura, 2500 de salida, un solo
intento) con lo disponible y carga lo real después; AG-18, AG-19 y AG-20 se llaman sin `presupuesto`; `Contabilidad.uc_de`
no cuenta `busquedas_web`; `_cargar` carga la escritura de caché de los agentes compartidos como lectura hasta
`liquidar_primas`. En mi escenario con salida `max_tokens` (`r01_01 --n 20`), la bolsa DIV acaba en 27,53 UC con
asignado 18, sin ampliación (límite 22,5), y no se registra ninguna incidencia: solo se ve en el resumen del run (F5).
**Alcance:** cada bolsa se pasa como mucho una llamada (después `puede` niega todas), pero esa llamada puede ser grande: la
petición de conocimiento se estima como una petición y hace hasta 8 con 40 búsquedas, y una reparación nunca se vuelve a
comprobar. El gasto que el operador autoriza sale de la cota, no del presupuesto, así que no rompe la autorización; sí
quita valor a la cota por presupuesto y al control del Anexo A. No se corrige aquí (encargo); falta un ticket (H-07).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | suite completa 6131 passed (incluye `test_t145.py`, `test_t140.py` con su cambio, `test_t12*`, `test_t13*`, `test_t141_datos_bce.py`); goldens coinciden |
| CA-2 | sí | `test_h01_…` en verde; `r01_01` y `r01_02` de T-140 por debajo de 19,54 y 166,56 en todos sus escenarios. Con H-01: el total aguanta en todos mis escenarios, pero S4 no se cumple llamada a llamada |
| CA-3 | sí | `r01_03` de T-140: 0 en las filas con año o fecha delante; «tarjeta, caducidad y otra» y «dos con su caducidad» al 100 %; lo demás, declarado. `r01_02` (mío): 0 fallos |
| CA-4 | sí | `r01_04` de T-140: 19 ok; `r01_03` (mío): 10 de 10 |
| CA-5 | sí | `mutantes_t145.py`: 19 de 19 muertos (los vivos de mis mutantes, en H-04) |
| CA-6 | sí | ruff 2838, mypy A 109 |

## Dos casos de `test_t140.py` que cambian

`«2027 <tarjeta>»` y `«<tarjeta> 1999»` dejan de detectarse. **Justificado:** con cinco grupos de cuatro cifras, «año +
tarjeta» y «año + cuatro niveles que pasan Luhn» tienen la misma forma, y lo segundo marcaba del 5 al 8 % de las filas de
tabla; lo mismo con el año detrás. Es una decisión `[PROPUESTO]`, declarada en INC-T123-01 con las tasas, comentada en la
prueba y probada en `test_t145.py`; no se debilita en silencio. Las formas corrientes (caducidad MMAA detrás, dos o tres
tarjetas, con guiones o espacio duro, con CVV de tres cifras) siguen al 100 %.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | Desde `bloque_a/11_Ejecutor`: `python -I ../../.docs/tickets/T-145/revisores/r01_01_amplificacion_contrarreplica.py <tmp> <carpeta de medir_consumo_a> --n 120,150,170 --salida real --k 1 [--reparar-papel contrarreplica]`. Respuestas válidas y de largo ≤ `max_tokens`: el Analista escribe una afirmación larga con fuente propia (en modo vivo cualquier fuente es citable), el Contradictor da N objeciones fuertes cortas y el Analista las da todas por resueltas citándola | **Esperado (S4):** el encargo de cada llamada ≤ lo medido + la salida máxima de las anteriores, «copiada una vez»: 53 746 tok en la contrarréplica. **Obtenido:** `_refutacion` copia el contenido de cada evidencia citada en cada objeción (crece con N·K·L): con N=150 la contrarréplica se admite con **196 239 tok** (3,65 veces) y cuesta **2,48 USD** a la tarifa real (cota de esa llamada: 2,07); con N=170 la corta la estimación previa del presupuesto. El total del ciclo queda en 1,4–3,9 USD (cota 19,54): la cifra aguanta por la holgura de S2 y porque la estimación previa usa el encargo real, no por S4. La cota por presupuesto usa la misma S4 para «la última llamada de cada bolsa», que tampoco acota | Acotar el encargo de las llamadas con bolsa por lo que deja pasar `_estimar_uc` (encargo ≤ 3,6·(2·T_e·límite máximo − 1500) caracteres, y su peor caso con reparaciones y continuaciones), o modelar la contrarréplica y la respuesta como producto (objeciones × evidencia); y escribir en S4 que el reparto se apoya en el presupuesto. Prueba: este escenario | abierto |
| H-02 | baja | Leer S5 en la salida de `estimar_coste_ciclo_a.py` | La cota elegida (por llamadas) no cuenta lo que lee cada búsqueda, que se cobra como entrada y que cada continuación de `pause_turn` reenvía (hasta 5 búsquedas × 4 peticiones por intento en AG-14/AG-16). Está declarado, pero la cifra se presenta como «cota superior» y es la de la petición de conocimiento, la llamada más cara por tipo (3,22 USD en solo divisas) | Un margen por búsqueda declarado (`[PROPUESTO]`, para afinar con el modo sombra) o llamar a la cifra «cota salvo lo que lee la búsqueda» | abierto |
| H-03 | baja | `orquestacion.ciclo`: `activas = f10["P-02"] or perfiles_activos(cfg)` | La cota cuenta los tipos de `perfiles_activos(cfg)`; si un CT-04 cambió los tipos activos en F10 (P-02), el ciclo analiza otros y la cota no lo sabe | Leer P-02 del estado si se pasa, o fallar cerrado / avisar si difiere | abierto |
| H-04 | baja | `python .docs/tickets/T-145/revisores/r01_04_mutantes.py <copia con «_mut»>` | Vivos 7 de 12, todos en `estimar_coste_ciclo_a.py`: R01 (la integración no lee el cribado), R04 (sin el suelo de COMÚN), R05 (solo el reparto todo N2), R06 (sin la última llamada de cada bolsa), R07 (sin la prima de caché), R08 (S3 admite una llamada de más; la prueba añade tres), R09 (precio por UC sin la lectura). La cota por presupuesto no tiene ninguna prueba de su cifra | Pruebas con cifras esperadas de `cota_presupuesto` y de sus términos, del encargo de la integración y del borde de S3 (una llamada de más) | abierto |
| H-05 | baja | `python -I .docs/tickets/T-145/revisores/r01_03_comprobar_datos_bordes.py <tmp>` | Una historia anterior a la ventana cuyo último cierre es inválido («n/d», negativo, fechas repetidas) da ANTIGUO con la fecha de ese dato inválido y sin aviso; el docstring dice que un dato malo antiguo lleva aviso | Validar la historia (`cierres(simbolo, None, as_of)`) también en esa rama y poner el aviso, o decirlo en el docstring | abierto |
| H-06 | baja | `.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`, §1, «Lo que el Anexo B deja abierto» | Dice que `coincide` (CT-10) e `independiente` (CT-11) tomen «los valores que usa el ejecutor (los de `esquemas_respuestas.json`)», pero ninguno de los dos está en ese golden: CT-10 lo sirve el Motor (`motor/servicio.py`), como dice ahora la entrada nueva. Texto anterior a T-145, en el mismo §1 que corrige H-05 de T-140 | Citar `motor/servicio.py` para `coincide` y el código de CT-11 para `independiente` | abierto |
| H-07 | baja | `grep -n "T-145" sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | El README del ticket dice «T-145 en la deuda técnica», y no hay fila; el hallazgo del presupuesto «va en otro ticket», que no existe (solo INC-T129-01, «queda para decidir»); en INC-T129-01, «Límites del estimador» sigue diciendo que no cuenta reparaciones (sí desde T-140) | Fila de T-145 y un ticket (o fila de deuda) para el presupuesto que no corta; actualizar esa viñeta | abierto |

Observación sin hallazgo: la forma declarada «cuatro números y la fecha MMDD detrás» llega al 9,2 % con precios dentro
del rango de Mastercard (2221–2720) y una hora HHMM (`r01_02`), por encima del 7,1 % y el 5,2 % que da INC-T123-01 para
niveles y oro; su techo es 1/10 (Luhn) por la fracción de meses válidos. Conviene dar el techo en la incidencia.

## Scripts de esta ronda (`revisores/`)

- `r01_01_amplificacion_contrarreplica.py`: cliente real con SDK falso; respuestas válidas que amplían la contrarréplica; barre N (H-01).
- `r01_02_r8_series.py`: R8 en filas de 5 a 12 grupos, cabeceras de años, tres tarjetas, separadores, series de 200 000 grupos (0,3 s) y repetición: 0 fallos.
- `r01_03_comprobar_datos_bordes.py`: bordes de la ventana, archivo vacío, datos futuros, historia inválida, H1: 10 de 10 (H-05).
- `r01_04_mutantes.py`: 12 mutantes del revisor; 5 muertos, 7 vivos (H-04).

## Invariantes

Sin LLM en la ruta determinista (los cambios son de R8, de scripts de `.docs/` y de pruebas); R8 falla cerrado donde se
declara; ningún número a mano nuevo en producción (los de la cota salen de la configuración y la tarifa; 15 y 300 son los
del código de `agentes.py`); decisiones como `[PROPUESTO]` en INC-T123-01 e INC-T129-01; sin secretos (tarjetas generadas
en tiempo de ejecución o partidas); sin identificadores de modelo en los scripts del revisor. Documentación: H-07.

## Veredicto

**APTO** · los seis criterios se cumplen con evidencia y no hay hallazgos críticos ni altos. La cifra que se dará al
operador (19,54 USD con solo divisas y 166,56 con los 12 tipos) cubre todo lo que he podido construir, con mucho margen;
H-01 (media) muestra que su derivación no es una cota llamada a llamada y debe corregirse antes de afinar la cota con el
modo sombra. H-01 a H-07 pasan a la deuda técnica con su ID.
