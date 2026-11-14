# T-114 · Análisis técnico

## Causa raíz o motivo

Los formatos de los contratos CT del Bloque A vivían solo en el código (`bloque_a/contratos.py`) y en el Anexo B del Documento 0. Un cambio en una tabla de canales, en un campo mínimo o en un esquema de respuesta podía pasar sin que fallara ninguna prueba. La Fase 3 del plan de fases pide congelarlos en goldens comparados byte a byte, antes de la cadena A→B (Fase 6), que se apoya en ellos.

## Evidencia

- Antes de T-114 no había ningún fichero esperado de contratos: `grep -rn golden bloque_a/11_Ejecutor tools` no daba nada.
- Con los goldens, cinco mutaciones hechas a mano en una copia desechable se detectan (salida en `pruebas.md`, «Mutación a mano»).
- Al derivar los esquemas del Anexo B y medir con el ejecutor aparecieron diferencias que nadie tenía listadas: INC-T114-01 y INC-T114-02 en `docs/incidencias.md`.

## Implementación

- Archivos nuevos y por qué:
  - `bloque_a/11_Ejecutor/tests/goldens_ct.py`: genera el texto de cada golden, lo compara con el congelado y re-congela con motivo. Es a la vez módulo de las pruebas y orden de línea.
  - `bloque_a/11_Ejecutor/tests/test_fase3_goldens.py`: 51 pruebas, agrupadas por criterio de aceptación.
  - `bloque_a/11_Ejecutor/tests/goldens/`: seis goldens generados, dos ficheros escritos a mano (`anexo_b_esquemas.json`, 32 esquemas; `anexo_b_ejemplos.json`, 32 ejemplos), `README.md` con la regla de re-congelado y `REGISTRO.md`.
- Archivos cambiados: `docs/incidencias.md` (INC-T114-01 y 02), la deuda técnica (T-114 y T-115), `.docs/README.md` (tabla de scripts), `bloque_a/11_Ejecutor/README.md` (una línea en la estructura) y `docs/AVANCE.md`.
- No cambia: nada de `bloque_a/11_Ejecutor/bloque_a/`, del Documento 0 ni de `06_Plantillas_entregables`.
- Decisiones tomadas:
  - Los esquemas derivados viven con las pruebas y no en `06_Plantillas_entregables`, que es corpus congelado de la entrega.
  - Las diferencias con el Anexo B se **miden con el ejecutor**, no se deducen de las tablas: se crea el mensaje del ejemplo con `Mensajeria.crear` y se repite quitando cada campo obligatorio. Motivo: las tablas engañan; por ejemplo, `CAMPOS_MINIMOS["CT-02"]` no se aplica a la entrega, que es un retorno y tiene su comprobación propia en `validar`.
  - Del ciclo simulado se congelan formas (emisores, receptores, claves y valores de las listas cerradas), no mensajes enteros: los textos del simulador pueden cambiar sin que cambie un formato.
  - Los ejemplos del Anexo B se envían por el primer canal del contrato; el retorno vuelve por él si el canal lo admite. Los campos del sobre que el Anexo B pone en el cuerpo (`run_id`, `query_id`, `presupuesto`, `consumo`) se pasan por su sitio, como hace el ejecutor.
- Desviaciones del plan:
  - CA-5 decía que los dos ejemplos publicados cumplen sus esquemas. El del informe de seguimiento no lo cumple por la clave `x_aviso_ejemplo` (INC-T114-02). La prueba congela el hecho: ese es el único incumplimiento y sin la clave lo cumple. No se toca la entrega.
  - `divergencias_anexo_b.json` usa las claves `el_ejecutor_rechaza_el_ejemplo_del_anexo_b`, `el_ejecutor_admite_que_falte` y `el_ejecutor_exige_y_el_anexo_b_no_nombra`, más precisas que las dos que nombraba el plan.
  - `formas_ciclo_mock.json` añade `valores_de_listas_cerradas`: así se ve que CT-06 emite fases que el Anexo B no lista.
- Límites conocidos (los de la primera entrega; los vigentes están en «Ronda r02»):
  - Los esquemas derivados solo llegan al primer nivel de campos, y a un segundo nivel donde el Anexo B trae un bloque JSON. No fijan tipos.
  - El ciclo simulado emite 8 de los 25 contratos por la mensajería (CT-02, 05, 06, 08, 11, 12, 13 y 15). De los demás se congelan las tablas y el mensaje de ejemplo, no una forma observada.
  - Los retornos internos (CT-06 a CT-14) no pasan por `Mensajeria`: su formato real lo fijan los esquemas de `ESQUEMAS`, congelados en `esquemas_respuestas.json`.
  - CT-16 a CT-22 no tienen cuerpo congelado: el Anexo B no da sus campos.
  - El Bloque A Forex queda para T-115.
- Comandos exactos para probarlo, desde `bloque_a/11_Ejecutor` y con el `.venv` del proyecto:
  - `python -m pytest -q tests/test_fase3_goldens.py` (51 pruebas, unos 20 s);
  - `python tests/goldens_ct.py` (comprueba; 0 si coincide, 1 si difiere);
  - `python tests/goldens_ct.py --update` (debe terminar con 2 y no escribir nada).

## Ronda r02 (14-11-2026)

Corrige los hallazgos de la QA r01 (`qa.md`, «Ronda r01»). No cambia código de producción, ni el Documento 0, ni `06_Plantillas_entregables`: solo pruebas, goldens, su generador y documentación.

### Causa de H-01

Los goldens de la primera entrega veían las tablas y los esquemas, que era lo que pedían CA-1 y CA-2, pero dos clases de formato quedaban fuera:

- **Las reglas de valor de la mensajería.** Las listas de CT-01, el G3 de CT-02, los contratos exentos de `run_id`, los tipos de mensaje, la normalización del estado de CT-23 a CT-25 y el `msg_id` externo están escritos dentro de `Mensajeria.crear` y `validar`, no en las tablas. Los ejemplos solo recorrían el camino que se admite.
- **Lo que el ejecutor emite.** Solo se guardaban las claves de primer nivel de un ciclo semanal V5.

### Qué cambia

| Hallazgo | Cambio | Prueba |
| --- | --- | --- |
| H-01 a | Golden nuevo `aceptaciones_rechazos.json`. Sale de `bateria_mensajes.json`, un fichero de datos escrito a mano con 362 casos (145 admitidos y 217 rechazados), protegido por `huellas.json`. Cada caso parte de un ejemplo del Anexo B o de un cuerpo propio, dice qué cambia y qué se espera de él. El golden guarda el mensaje normalizado o la clase y el motivo del rechazo. Cada caso usa un almacén nuevo, así que añadir un caso no cambia los demás | `test_h01_la_bateria_cubre_los_25_contratos…`, `…las_reglas_de_valor_estan_en_la_bateria`, `…un_caso_mal_escrito_es_un_error…`, `…la_copia_sin_cambios_de_contratos_da_el_golden` y `…un_cambio_en_las_reglas_de_la_mensajeria_cambia_el_golden` (22 cambios de una línea de `contratos.py`, aplicados a una copia del módulo) |
| H-01 b y c | `formas_flujos_mock.json` sustituye a `formas_ciclo_mock.json`. Once flujos en vez de un ciclo, y de cada tipo de mensaje la ruta de cada clave con su tipo JSON y las combinaciones de claves opcionales de primer nivel. El ejecutor emite 20 contratos por la mensajería; se ven 18 (faltan CT-07 y CT-14) | `test_h01_los_flujos_cubren_los_contratos_que_el_ejecutor_emite`, `…las_rutas_llevan_claves_anidadas_tipos_y_combinaciones`, `…un_cambio_en_lo_que_el_ejecutor_emite_cambia_las_formas` (14 cambios sobre los mensajes capturados, entre ellos E02 a E11 del revisor) |
| H-02 | `CT-22.ENCARGO` en los esquemas derivados, con `tipo` obligatorio y lista abierta (los dos valores, en `examples`), y su ejemplo. La lista «sin campos en el Anexo B» pasa a CT-16 a CT-21. `divergencias_anexo_b.json` gana `valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro`, medido con los mensajes de los flujos. INC-T114-01 corregida y ampliada | `test_ca4_de_ct16_a_ct22_el_anexo_b_solo_nombra_el_tipo_de_ct22`, `test_ca7_el_tipo_de_ct22_que_el_ejecutor_emite_en_tipo_aviso_esta_congelado` |
| H-04 | CA-5 del README reescrito con su salvedad (INC-T114-02) | — (documentación) |
| H-05 | `contenido` de CT-23 con `if`/`then`/`else`. Los retornos: el Anexo B no dice qué lleva un retorno RECHAZADO o SIN_RESULTADO, así que no se inventa; se declara en el `$comment` de los 15 esquemas de retorno y en el README de los goldens | `test_ca4_el_contenido_de_ct23_solo_va_en_entrante`, `test_ca4_los_retornos_declaran_que_el_anexo_b_no_describe_el_retorno_rechazado` |
| H-06 | La prueba «nada inventado» busca cada campo, anidados incluidos, en el párrafo de su contrato (`parrafos_anexo_b`, `campos_fuera_de_su_parrafo`) | `test_ca4_los_campos_de_cada_esquema_estan_en_el_parrafo_de_su_contrato`, `test_ca4_un_campo_de_otro_contrato_se_detecta` |
| H-03 | No se toca la deuda (la actualiza quien coordina). El texto propuesto va en el informe de entrega | — |

Además: si un fichero escrito a mano está roto (un esquema, un ejemplo o un caso de la batería), `python tests/goldens_ct.py` termina con 1 y dice por qué en una línea, sin traza (`test_un_fichero_a_mano_roto_se_dice_sin_traza`).

### Archivos

- Nuevos: `tests/goldens/bateria_mensajes.json` (a mano), `tests/goldens/aceptaciones_rechazos.json` y `tests/goldens/formas_flujos_mock.json` (generados).
- Borrado: `tests/goldens/formas_ciclo_mock.json` (lo sustituye `formas_flujos_mock.json`).
- Cambiados:
  - `tests/goldens_ct.py`: batería, flujos, rutas, la medida nueva de divergencias, los párrafos del Anexo B;
  - `tests/test_fase3_goldens.py`: de 51 a 102 pruebas;
  - `tests/goldens/anexo_b_esquemas.json` y `anexo_b_ejemplos.json`: CT-22, CT-23 y los `$comment` de los retornos (33 esquemas y 33 ejemplos);
  - `tests/goldens/divergencias_anexo_b.json`, `mensajes_ejemplo.json` y `huellas.json`, re-congelados con motivo (línea del 14-11 en `REGISTRO.md`); `tablas_contratos.json` y `esquemas_respuestas.json` no cambian;
  - `tests/goldens/README.md`: tabla de ficheros, «Qué ve cada golden» y «Límites»;
  - `docs/incidencias.md`: INC-T114-01;
  - el README del ticket y `pruebas.md`.

### Decisiones

- **`espera` en cada caso de la batería.** El golden dice lo que el ejecutor hace; `espera` dice lo que quien escribió el caso creía que hacía. Si no coinciden, el golden lo lista y una prueba falla. Así un re-congelado no puede tapar una regla que cambió sin querer.
- **Los flujos reutilizan las llamadas de las pruebas existentes** (`test_integracion.py`, `test_v51.py`, `test_t101_v6.py`), con `MockClient`. La auditoría se activa también en modo backtest para ver CT-16 y CT-17.
- **De los flujos que lanzan un ciclo por dentro** (consulta que escala, petición ad hoc) solo se guardan los contratos que el flujo añade. Los del ciclo ya están en los ciclos semanales.
- **Las claves que son datos se escriben genéricas** (`<clase>`, `<id>`): si no, el golden cambiaría cada vez que el simulador eligiera otra opción.
- **Los mensajes de un mismo flujo, contrato y tipo se resumen juntos**, con las combinaciones de claves opcionales de primer nivel aparte. Guardar cada forma entera por separado multiplicaba el tamaño del golden sin ver mucho más.
- **`tipo` de CT-22 es obligatorio en el esquema derivado.** El Anexo B lo nombra sin marcarlo como opcional; es la misma regla que en los demás contratos. La lista es abierta («admite además»), así que no hay `enum`.
- **Los 22 cambios de `contratos.py` dentro de la suite** se aplican a una copia del módulo escrita en una carpeta temporal. Si el texto original deja de estar en `contratos.py`, la prueba falla y pide actualizar el cambio. Es el precio de tener dentro de la suite los mutantes que la r01 encontró vivos.

### Lo que se ha visto de paso (no se corrige: manda el código)

- **CT-02 como ENCARGO.** La regla «entrega solo con G3 aprobado» se aplica al retorno. Un CT-02 con tipo de mensaje ENCARGO y `estado_g3` BLOQUEADO se admite (caso `CT-02/como_encargo_con_g3_bloqueado`). El ejecutor siempre emite CT-02 como retorno, así que hoy no es un camino abierto.
- **Un retorno RECHAZADO de CT-03 sin sus campos se rechaza:** el ejecutor exige los campos de retorno sea cual sea el estado común.
- **La mensajería no mira tipos** fuera de CT-01 y CT-02: `piezas`, `encargos` o `peticiones` con un texto en vez de una lista se admiten.
- **CT-25 con un campo `valor`** cuyo texto no tiene forma de clave lo admite la mensajería. Lo rechaza `Credenciales.responder`, antes de crear el mensaje.
- **Los cuatro avisos CT-22 no llevan el mismo campo:** dos usan `tipo` y dos `tipo_aviso` (INC-T114-01).

### Mutantes del revisor, antes y después

Ejecutados en una copia desechable con los scripts de `revisores/`, sin cambiarlos.

| Script | r01 | r02 |
| --- | --- | --- |
| `r01_01_mutantes_contratos.py` (40; 39 aplicables, M10 no se aplica porque su texto aparece dos veces) | 21 detectados por `goldens_ct.py`, 18 no | **39 de 39 detectados** |
| `r01_03_mutantes_emision.py` (11) | 1 detectado, 10 no | **11 de 11 detectados** |
| `r01_02_goldens_determinismo_y_update.py` | 24 de 24 bien | 27 de 27 bien (hay tres ficheros JSON más); cuatro procesos con `PYTHONHASHSEED` distinto dan los siete goldens idénticos |
| `r01_04_supervivientes_suite_completa.py` (los 23 a la vez) | `goldens_ct.py` decía «coinciden»; la suite, 3 fallos de 3811 | `goldens_ct.py` rc=1; la suite, 42 fallos de 3876 (39 en `test_fase3_goldens.py`) |

No queda vivo ninguno de los mutantes del revisor.

### Límites conocidos (r02)

Son los de «Límites» de `bloque_a/11_Ejecutor/tests/goldens/README.md`. Sustituyen a los de la primera entrega:

- **Contratos que ningún flujo emite:** CT-07, CT-09, CT-10, CT-14, CT-18, CT-20 y CT-21.
  - CT-09, CT-10, CT-18, CT-20 y CT-21 no los emite el ejecutor por la mensajería en ningún caso.
  - CT-07 y CT-14 sí, pero no con las respuestas de `MockClient`. Verlos pediría un cliente simulado a medida; no se ha hecho para no fabricar un flujo que ninguna prueba existente ejercita.
  - De los siete se congelan las tablas, el mensaje de ejemplo, el canal y la regla de `run_id`.
- **Los retornos internos (CT-06 a CT-14)** no pasan por `Mensajeria`: se congela su esquema de `ESQUEMAS`, no una respuesta vista.
- **Los valores** de un mensaje emitido no se guardan: solo claves y tipos, y los valores de los campos con valores nombrados en el Anexo B.
- **Tipos y claves opcionales anidadas mezclados:** si una clave anidada opcional deja de emitirse en un caso y sigue en otro del mismo grupo, o un valor «`null|string`» deja de ser nulo en un solo caso, el resumen no cambia. En el primer nivel sí se ve.
- **Ramas que el simulador no recorre** (G3 con advertencias, presupuesto agotado, consulta bloqueante vencida).
- **Reglas fuera de la mensajería** (`Bloque.decision`, `Credenciales.responder`, `ConsultasBroker.enviar`) y **los patrones del detector de datos protegidos**: tienen sus pruebas propias.
- **La batería es amplia, no exhaustiva:** una regla nueva que solo afecte a un mensaje que ningún caso construye no cambia el golden.
- **Los esquemas derivados** llegan al primer nivel, y a un segundo donde el Anexo B trae un bloque JSON. No fijan tipos. No juzgan un retorno RECHAZADO o SIN_RESULTADO.
- El Bloque A Forex queda para T-115.

### Comandos

Desde `bloque_a/11_Ejecutor`, con el `.venv` del proyecto:

- `python -m pytest -q tests/test_fase3_goldens.py` (102 pruebas);
- `python tests/goldens_ct.py` (0 si coincide, 1 si difiere o no se puede generar);
- `python tests/goldens_ct.py --update` (2, y no escribe nada).

Los mutantes, en una copia desechable cuya ruta contenga `qa_f3_mut`:

```bash
python .docs/tickets/T-114/revisores/r01_01_mutantes_contratos.py <copia>
python .docs/tickets/T-114/revisores/r01_03_mutantes_emision.py <copia>
python .docs/tickets/T-114/revisores/r01_02_goldens_determinismo_y_update.py <copia>
```
