# T-92 · QA independiente

## Ronda r01

- **Revisor:** revisor nuevo sin contexto de la implementación (Claude, subagente de QA) · **Ronda:** r01 · 10-11-2026
- **Código revisado:** `c7127dc` (rama local `claude/t92-auditoria-astra`, sobre develop `dae70df`); comparaciones con `dae70df` (develop) y `76b90e6` (rama de Astra).
- Opinión formada con el README del ticket y el código antes de leer `analisis-tecnico.md`.

### Reproducción desde limpio

```bash
git -C /home/claude/repo worktree add --detach /tmp/claude-0/t92r01 c7127dc
ln -s /home/claude/repo/.venv /tmp/claude-0/t92r01/.venv
W=/tmp/claude-0/t92r01
export PYTHONPATH=$W/bloque_a/11_Ejecutor:$W/bloque_a_forex/11_Ejecutor:$W/bloque_b/11_Ejecutor
cd $W && .docs/scripts/gate.sh --completo        # 12/12: A 386, FX 68, B 176 (log .docs/scripts/.logs/gate_20261110_221747.log)
# scripts de ataque (todos con python -I; comprueban que bloque_a se importa de la copia)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_01_cesta_bases.py $W/bloque_a/11_Ejecutor          # 6 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_02_almacen.py $W/bloque_a/11_Ejecutor              # 2 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_03_contratos.py $W/bloque_a/11_Ejecutor            # 8 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_04_plazos_y_literales.py $W/bloque_a/11_Ejecutor   # 2 fallos
```

Además: `test_t92_revision.py` copiado a la rama de Astra (`76b90e6`) da 13 fallos y 4 aprobados (17 pruebas, no 16); los scripts `rama_02` y `rama_03` ya no encuentran falsos positivos en el corpus (`*.md`), y un barrido propio de los `*.json` del bloque tampoco.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 43 `test_t87_*` + 17 `test_t92_revision.py` = 60 recogidas, todas en verde dentro de las 386 del gate |
| CA-2 | sí | Gate en verde con T-53, T-65 (r01–r04) y T-66; solo cambian `test_r03_h16_…` y `test_r04_h24_…`, con su motivo (D02) |
| CA-3 | sí | 12/12; `pytest_bloque_a=386` en `tools/cuotas.txt`; ruff 3109→3077, mypy A 123→115 |
| CA-4 | **no** | H-01 tiene prueba pero la corrección es incompleta (H-07: URLs y nombres de archivo con `sk-` tras «/» o espacio). La parte de «sin literales de respaldo» de H-05 no tiene una prueba que falle con la rama (la del tope pasa en `76b90e6`, como reconoce `pruebas.md`) |
| CA-5 | sí | INC-T92-01 en `docs/incidencias.md` como `[PROPUESTO]` y en la fila T-57 de la deuda |

### Lo que se comprobó y está bien

- **T-65 no se deshace:** frescura por serie y horizonte en cada pata (proxy, referencia y cada miembro de la CESTA, vía `motivo_no_fresca`); la degradación de H5 escribe `fecha_efecto` = `as_of` y `estado(F10, as_of)` la incluye (dos degradaciones el mismo día componen); `DOCUMENTADAS_CON_CODIGO` sigue rechazada (`test_fichas_documentadas_con_codigo_siguen_sin_cifras_citables`, falla en la rama); `autorizar_hasta_tope` lee los dos números con `parametro()`. No encuentro `cfg.get(…, número)` nuevos traídos por la fusión (ver H-09 para el literal que sí entra).
- **D02 (fuga):** la composición de la CESTA se congela al emitir con `conocido_el` = emisión; un miembro que deja de publicar después ya no se quita (supervivencia); el que ya estaba parado al emitir queda fuera por PS2. Base posterior, `True`, NaN, inf, 0, texto, lista o dict vacío, miembro desconocido y ruta fuera de la carpeta dan `DatosNoDisponibles`. Un PRG antiguo sin `bases_cesta` se resuelve con la cesta reconstruida al corte de la emisión.
- **Almacén:** registro intermedio cambiado, sello alterado o no JSON, línea no objeto y línea añadida al final se detectan al abrir y en la instancia viva; un `OSError` al guardar el sello deshace el registro; tres procesos × 40 escrituras dejan 120 registros con la cadena íntegra.
- **CT-01:** `msg_id` externo con formas raras (salto de línea, minúsculas, vacío, entero, inyección) se rechaza; reserva FALLIDA sin el texto del error; reconciliación con motivo e incidencia en HA.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-06 | **alta** | `r01_01_cesta_bases.py`, casos 1a–1c y 2. Miembro Y de la CESTA con último cierre conocido al emitir `-50` (o con la fecha de la emisión duplicada) | **Esperado:** como en develop y T-65 (H-15, H-21, H-25), un cierre ≤ 0 o una fecha repetida nunca se convierte en cifra: el miembro queda fuera al emitir (se sabía al emitir) o la CESTA no sirve. **Obtenido:** `_base_conocida` lee `serie()["cierre"].iloc[-1]` sin `_validar_cierres` y solo descarta 0 o no finito: `bases_cesta` congela `{"Y": {"valor": -50.0}}` (o 200, la última de las dos filas duplicadas, según el orden del CSV) y el PRG queda **RESUELTO, OCURRIDO, `rent_referencia` = −1,05**. Ese resultado entra en Brier, métricas y certificados (R13). En develop (`dae70df`) el mismo dato da una CESTA de +10 % sin Y. Además, `_rentabilidad_serie` acepta una base congelada negativa (caso 3, «valor negativo», da −2,1) | En `_base_conocida`, validar el último tramo como `valor_en` (`_validar_cierres` sobre las filas de la fecha máxima, con `conocido_el`), de modo que `DatosInvalidos` deje al miembro fuera al emitir. En `_rentabilidad_serie`, rechazar `v0 <= 0` (no solo `== 0`). Pruebas de regresión: cierre negativo y fecha duplicada al emitir, y base congelada negativa | abierto |
| H-07 | media | `r01_03_contratos.py`, caso 5, y `contenido_sensible("https://www.reuters.com/technology/sk-hynix-posts-record-quarterly-profit-2024-10-24/")` → `True`; igual con `…/sk-innovation-to-merge-with-sk-enmove` y `Fuente: sk-telecom-annual-report-2023.pdf` | **Esperado:** H-01 corregido: ningún texto corriente pasa por clave. **Obtenido:** el límite izquierdo `(?<![A-Za-z0-9_-])` no excluye «/», el espacio ni el inicio, y con `(?i)` vale «SK-». Una URL de resultados de búsqueda web sobre SK Hynix, SK Telecom… hace que `AnthropicClient.generar` (que pasa R8 a todos los bloques de contenido) devuelva `contenido_sensible` y el turno entero quede PARCIAL. A la vez hay falsos negativos: `OPENAI_KEY_sk-…` y `key-sk-…` no se detectan | Hacer la rama `sk-` sensible a mayúsculas (`(?-i:…)`) y exigir forma de clave: p. ej. al menos un dígito y una mayúscula en el cuerpo (`sk-(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Z])[A-Za-z0-9_-]{20,}`) o los prefijos conocidos (`sk-ant-`, `sk-proj-`, `sk-live-`…), sin depender del carácter anterior. Pruebas con las tres URLs y con los dos falsos negativos | abierto |
| H-08 | media | `r01_03_contratos.py`, casos 1a–1c | **Esperado:** el `msg_id` estable del Broker identifica un único mensaje. **Obtenido:** el externo (`MSG-AAAA-N+`) y el interno (`nuevo_id("MSG")` → `MSG-AAAA-NNNNNN`) comparten espacio de nombres. Un CT-01 sin `msg_id` puede recibir un número que el Broker ya usó (y al revés): `procesar_una_vez` lo rechaza con «msg_id reutilizado con contenido distinto» y el registro de mensajes tiene dos mensajes distintos con el mismo `msg_id`. Falla cerrado (no repite efectos), pero rechaza una petición legítima y rompe la trazabilidad que C3 quiere dar | Separar los espacios: guardar la clave del acuse como `BROKER:<id>` y exigir al Broker un formato propio (p. ej. `MSG-B-AAAA-N`), o que `nuevo_id` salte los números ya presentes en `acuses.sqlite3`. Ajustar el README del ejecutor (dice «formato `MSG-AAAA-NNNNNN`», el mismo que el interno) | abierto |
| H-09 | media | `r01_04_plazos_y_literales.py`, caso 2; `orquestacion.py`, `_observacion_ht01` | **Esperado:** ningún número escrito a mano en la ruta determinista (regla 2 de `CLAUDE.md`). **Obtenido:** `"favorable" if senal >= 0.5 else "contraria"` (A8, traído de la rama). Esa dirección decide en `_filtrar_evidencia` si la pieza del Analista que cita HT-01 queda `_sin_contraste`, es decir, si cuenta como raíz en PS1 (GC2). El 0,5 no está en `por_defecto.yaml` (solo existe en el mock). Menor: `ajustar_configuracion` repite como respaldo el literal de P-01 `"SEMANAL · SAB 06:00 · entrega LUN 07:00"` que ya está en `_inicializar_f10` | Leer el umbral de una clave de la configuración (p. ej. `senales.umbral_direccion_observacion`, `[PROPUESTO]` con incidencia y a T-57) y la P-01 de partida de una constante única | abierto |
| H-10 | media | `r01_02_almacen.py`, caso 1 con `KeyboardInterrupt` (o una caída del proceso entre el `fsync` del registro y el `replace` del sello) | **Esperado:** un fallo a mitad deja el estado intacto (ri-qa). **Obtenido:** `escribir` solo deshace con `except Exception`: con `KeyboardInterrupt`, `SystemExit` o un `kill`, el registro queda en el fichero y el sello no; el almacén ya no abre («el final de F5 difiere del sello»). La única salida es borrar sellos y marca de formato, que es justo lo que H-02 quería impedir (H-11) | `except BaseException` para el truncado. Para las caídas reales, un registro de intención (sello «pendiente» con `n+1` antes de escribir), y al abrir: si el fichero tiene exactamente un registro más que el sello, con la cadena íntegra y la intención anotada, se completa el sello o se trunca ese registro, con incidencia en HA. Documentar la recuperación en el README | abierto |
| H-11 | baja | `r01_02_almacen.py`, caso 2: truncar el final de F5 y borrar `sellos_integridad.json` **y** `formato_almacen.json` | **Esperado:** no se vuelve a sellar en silencio un almacén ya sellado. **Obtenido:** abre y sella `['uno', 'dos']`. Es el límite declarado en `analisis-tecnico.md`, pero la marca vive en un fichero aparte tan fácil de borrar como el sello | Llevar la marca dentro de los propios registros (p. ej. `_formato: 1` en cada entrada escrita con sellos): si alguna entrada la tiene y falta el sello, se falla cerrado | abierto |
| H-12 | baja | `r01_03_contratos.py`, caso 2 (HA no escribible durante `reconciliar`) | **Esperado:** validar antes de mutar: si no queda la incidencia, no se libera. **Obtenido:** la reserva se borra (estado DESCONOCIDO) y la incidencia no se escribe: liberación sin rastro | Escribir la incidencia antes del `DELETE` (o en la misma transacción lógica) y borrar solo si se escribió | abierto |
| H-13 | baja | `r01_03_contratos.py`, caso 3 | **Esperado:** repetir el `msg_id` devuelve la misma respuesta. **Obtenido:** la primera trae `Timestamp` y tupla; la repetida, `str` y lista (`json.dumps(default=str)`) | Normalizar la respuesta (ida y vuelta por JSON) también en la primera llamada | abierto |
| H-14 | baja | `r01_01_cesta_bases.py`, casos 3 («fecha basura») y 5 | **Esperado:** un PRG con datos corruptos espera o queda NO_RESOLUBLE sin afectar a los demás. **Obtenido:** `pd.Timestamp(base["fecha"])` lanza `DateParseError`, que `resolver()` no captura: se cae toda la resolución de C5 (también la del PRG sano). Solo con un F4 escrito por fuera (los sellos lo detectan), de ahí la gravedad | En `_rentabilidad_serie`, convertir la fecha con `try` y elevar `DatosNoDisponibles` | abierto |
| H-15 | baja | `r01_04_plazos_y_literales.py`, caso 1 | **Esperado:** un plazo CT-23 del Broker con solo fecha («2026-06-08») vale todo ese día, como en develop. **Obtenido:** `_instante` lo convierte en las 00:00 del 8-6 y `vencer` lo da por VENCIDO el 8-6 a las 09:00 (un día antes que develop). Regla nueva sin incidencia | Si el plazo no trae hora, tomar el final del día (o exigir hora y rechazarlo al enviar), y documentarlo | abierto |
| H-16 | baja | Lectura de documentos | Documentación desalineada: (a) `.agents/skills/ri-probar/SKILL.md` pasa a «A ≥ 244» (valor de la rama), debe ser 386; (b) el README del ejecutor titula «Operación del Bloque A tras T-87» y enlaza «.docs/tickets/T-87/handoff.md» (ruta que no existe en develop; nota del coordinador para el gate refs-vivas), que no existe (en develop T-87 es SC-5; el traspaso está en `auditoria_astra/handoff.md`), y da el formato `MSG-AAAA-NNNNNN` cuando el código admite `MSG-AAAA-N+`; (c) CA-1 y `pruebas.md` hablan de 16 pruebas en `test_t92_revision.py` (son 17) y de «12 fallan» en la rama (fallan 13) | Corregir los tres puntos | abierto |

### Invariantes

- **F y G antes de una orden:** no se toca ningún camino de órdenes (Bloque A no emite órdenes). Sin cambios.
- **Sin LLM en la ruta determinista ni en los controles:** se cumple. R8 y R21 son expresiones regulares y la evaluación es numérica.
- **Los controles no se relajan solos:** se cumple. A6 endurece el tope; la degradación de H5 sigue sin revertirse sola.
- **Falla cerrado y valida antes de mutar:** **no del todo.** H-06 (una base inválida se convierte en cifra), H-10 (un fallo a mitad no deja el estado intacto), H-12 y H-14.
- **Ningún número escrito a mano:** **no.** H-09.
- **Ninguna decisión del operador en silencio:** INC-T92-01 está `[PROPUESTO]` y en T-57. D02 (cambia la regla de T-65) está razonada en el ticket. H-15 es una regla nueva sin incidencia.
- **Sin secretos ni datos personales:** el gate de secretos pasa. Las claves de prueba van partidas (`"s" + "k-"`).
- **Documentación:** la fila T-92 de la deuda y CLAUDE.md están al día (386). Lo pendiente está en H-16.

### Veredicto

**NO APTO.** H-06 es alto: con un cierre negativo o una fecha duplicada en un miembro al emitir, la CESTA congelada resuelve un pronóstico con una cifra falsa. Eso deshace para la CESTA la regla de T-65 de que un cierre inválido nunca se convierte en cifra, y el resultado entra en las métricas y los certificados. CA-4 no se cumple: H-01 está corregido solo en parte (H-07) y la parte de literales de H-05 no tiene una prueba que falle con la rama. Para la r02, quien implementó corrige al menos H-06 a H-10 con su regresión. El revisor vuelve a ejecutar `revisores/r01_*.py`: deben dar 0 fallos, salvo los casos que se acepten como límite documentado y pasen a la deuda con su ID.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación ni de la QA r01 (Claude, subagente de QA) · **Ronda:** r02 · 10-11-2026
- **Código revisado:** `6f02e11` (rama local `claude/t92-auditoria-astra`); comparaciones con `c7127dc` (r01), `dae70df` (develop) y `76b90e6` (rama de Astra).

### Reproducción desde limpio

```bash
git -C /home/claude/repo worktree add --detach /tmp/claude-0/t92r02 6f02e11
ln -s /home/claude/repo/.venv /tmp/claude-0/t92r02/.venv
W=/tmp/claude-0/t92r02
export PYTHONPATH=$W/bloque_a/11_Ejecutor:$W/bloque_a_forex/11_Ejecutor:$W/bloque_b/11_Ejecutor
cd $W && .docs/scripts/gate.sh --completo        # 12/12: A 401, FX 68, B 176 (log .docs/scripts/.logs/gate_20261110_225429.log)
# sondas de la r01 (python -I; comprueban que bloque_a se importa de la copia)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_01_cesta_bases.py $W/bloque_a/11_Ejecutor          # 1 fallo (1c)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_02_almacen.py $W/bloque_a/11_Ejecutor              # 1 fallo (2, H-11)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_03_contratos.py $W/bloque_a/11_Ejecutor            # se corta en el caso 1 (MensajeInvalido: formato MSG-BRK)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_04_plazos_y_literales.py $W/bloque_a/11_Ejecutor   # 0 fallos
# sondas nuevas de la r02
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_01_r8_sk.py $W/bloque_a/11_Ejecutor                # 10 fallos (develop: 3, los falsos positivos de siempre)
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_02_almacen_recuperacion.py $W/bloque_a/11_Ejecutor # 4 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_03_contratos.py $W/bloque_a/11_Ejecutor            # 0 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_04_bases_plazos_umbral.py $W/bloque_a/11_Ejecutor  # 7 fallos
```

Además, `test_t92_revision.py` de la r02 (32 pruebas):
- copiado sobre `c7127dc`, fallan 14 y pasan 18: fallan las de H-06, H-08, H-09, H-10 (dos), H-12, H-13, H-14 (tres), H-15 y H-07 (tres casos);
- copiado sobre `76b90e6`, fallan 27 y pasan 5, como dice `pruebas.md`.

### Sondas de la r01: ¿es correcta la explicación del ticket?

- **`r01_01`, caso 1c: sí.** Con la r02, el miembro Y (cierre −50 al emitir) ya no se congela: `bases_cesta` = `{X}` y el PRG se resuelve con X (`rent_referencia` = 0,1). Es lo mismo que hace develop. El H-06 de la r01 aceptaba las dos salidas («queda fuera al emitir o la CESTA no sirve»), y el 1c pedía solo la segunda. Lo que importa se cumple: ninguna base inválida llega a ser una cifra (casos 1a, 1b, 2 y 3 en verde, y `r02_04` caso 1 con cinco formas de cierre inválido).
- **`r01_02`, caso 2: sí.** Es H-11: quien borra a la vez el final, los sellos y la marca reescribe la carpeta, y eso solo se detecta con una copia o una firma externas. El límite está declarado en `analisis-tecnico.md` y en el ticket. Como hallazgo bajo, pasa a la deuda al cerrar.
- **`r01_03`: sí, pero se corta en el caso 1 y no ejecuta los casos 2 a 5.** Los casos 2 a 4 se repiten en `r02_03` con el formato nuevo y salen todos en verde. El caso 5 (R8) se cubre con más alcance en `r02_01`.

### Estado de H-06 a H-16

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-06 | **corregido** | `_base_conocida` pasa la fecha máxima por `_validar_cierres`, con el mismo tramo que `valor_en`. Un cierre negativo, 0, no numérico, infinito o con la fecha repetida al emitir deja fuera al miembro y el resto sigue. Un cierre malo anterior a la base no deja fuera a un miembro sano. `_rentabilidad_serie` rechaza `v0 <= 0` (`r02_04`, casos 1, 1b y 1c; `r01_01`, casos 1a, 1b, 2 y 3). La prueba falla con `c7127dc` |
| H-07 | **corregido lo pedido, pero con una regresión: H-17 (alta)** | Las URL y los nombres con `sk-hynix-…` ya no se toman por clave, y `OPENAI_KEY_sk-…` sí se detecta. Pero el patrón nuevo deja de detectar claves reales que develop y la r01 detectaban (H-17). No hay retroceso catastrófico: entradas adversarias de ~1 MB tardan ≤ 0,13 s (`r02_01`, caso 4) |
| H-08 | **corregido** | `MSG-BRK-AAAA-N{1,12}`. Ningún identificador interno, con o sin ámbito de las 12 clases, empieza por `MSG-BRK-`. Se rechazan las formas raras (`r02_03`, casos 1a a 1c) |
| H-09 | **corregido; queda H-23 (baja)** | `parametro(cfg, "senales.umbral_favorable")`, sin literal de respaldo (`r01_04`, caso 2). El valor no se valida y no está en T-57 |
| H-10 | **corregido en el caso pedido; quedan H-19 (media), H-20 (baja) y H-21 (baja)** | `except BaseException` en `escribir`. Con una muerte real del proceso (`os._exit` entre el registro y el sello, en otro proceso), el almacén abre en lo sellado, aparta el registro y anota la incidencia (`r02_02`, caso 1). También funciona si el registro cortado está en HA (caso 5). No acepta registros manipulados, porque todo lo que pasa del sello se aparta, pero puede sacar de la cadena registros confirmados (H-19) |
| H-11 | límite declarado (baja) | Aceptado como límite. Pasa a la deuda al cerrar (hoy la fila T-92 de la deuda no lo nombra) |
| H-12 | **corregido** | Si HA falla, la reserva sigue FALLIDA. Tras reconciliar, el mismo `msg_id` se procesa. Un COMPLETADO no se reconcilia (`r02_03`, casos 2a a 2c) |
| H-13 | **corregido** | La primera respuesta y la repetida son idénticas, también con `Timestamp`, tupla y NaN (`r02_03`, caso 3) |
| H-14 | **corregido** | Diez formas ilegibles de la fecha (texto, entero enorme, lista, dict, NaN, «NaT», mes 13, 1e30, bytes, `True`) dan `DatosNoDisponibles` (prueba y `r02_04`, caso 2) |
| H-15 | **corregido en el caso pedido; queda H-22 (baja)** | «2026-06-08» sigue abierto a las 23:59 de Madrid y vence a las 00:00 del día siguiente (`r01_04`, caso 1; `r02_04`, caso 3). Falla en los días de cambio de hora y con fechas escritas sin ceros a la izquierda (H-22) |
| H-16 | **corregido** | `ri-probar` con A ≥ 401; el README enlaza a `auditoria_astra/handoff.md` (existe) y al ticket; los recuentos de `pruebas.md` (32; 27/5 en la rama) coinciden con lo reproducido |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 43 `test_t87_*` y 32 `test_t92_revision.py`, en verde dentro de las 401 del gate |
| CA-2 | sí | T-53, T-65 (r01 a r04) y T-66 en verde; solo cambian, con su motivo, las dos pruebas de la regla de la CESTA que sustituye D02 |
| CA-3 | sí | Gate 12/12; `pytest_bloque_a=401` |
| CA-4 | **no** | Las pruebas fallan con la rama de Astra (27/5), pero la corrección de H-01 (R8 `sk-`, ronda r02 por H-07) relaja el control respecto a develop (H-17) |
| CA-5 | sí | INC-T92-01 en `docs/incidencias.md` como `[PROPUESTO]` y en la fila T-57 |

### Lo que se comprobó y está bien

- **T-65 no se deshace.** Se mantienen:
  - la frescura por serie y horizonte;
  - la fecha de efecto de H5 en el mismo ciclo;
  - `DOCUMENTADAS_CON_CODIGO` rechazada;
  - el tope con los dos números de la configuración (`test_t65_h05_…` falla en la rama de Astra).
- **Ningún literal nuevo de la r02.** Revisé las líneas añadidas desde develop. Los literales que quedan son de antes (`plazo_horas`, `4 if BLOQUEANTE else 24`, en develop) o constantes lógicas (p = 1,0 sin dato en Holm).
- **Rendimiento de `RE_SECRETO`:** es lineal. Dentro del tramo perezoso nunca hay un segundo inicio válido, porque la clase del tramo está dentro de la del límite izquierdo.
- **Los cierres de la base en otros caminos:** la referencia que no es CESTA y el proxy se congelan con `valor_en`, que ya valida. Una CESTA congelada vacía (`{}`) no resuelve, que es lo correcto.

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-17 | **alta** | `r02_01_r8_sk.py`, casos 1 y 1b. Claves con la forma real: cuerpo base64url aleatorio con «-» y «_», `sk-ant-api03-…AA` (la forma del proveedor del propio sistema), `sk-proj-…` y `sk-svcacct-…`. Ejemplo fijo: `sk-ant-api03-` seguido de un cuerpo aleatorio (ejemplo fijo de la sonda, omitido aquí para el gate de secretos; nota del coordinador) | **Esperado:** H-07 quita falsos positivos sin relajar R8: toda clave que develop detecta se sigue detectando («los controles nunca se relajan solos», «nada de secretos»). **Obtenido:** no se detectan 160 de 5000 claves Anthropic, 141 de 5000 `sk-proj-` y 137 de 5000 `sk-svcacct-` (≈3 %), cuando develop y la r01 detectan las 5000. La causa es que el tramo perezoso `[A-Za-z0-9-]*?` no cruza «_», y el tramo de 16 sin guion tiene que empezar antes del primer «_». En esos casos `contenido_sensible` deja pasar la clave al proveedor del LLM, a la cinta y a F5. Además siguen sin detectarse `key-sk-…` y `…/sk-…` (falsos negativos que la r01 señaló). Las pruebas de H-07 usan cuerpos fijos (`'A' * 24`, `'C7' * 12`), y por eso no lo ven | No basta con añadir «_» al tramo perezoso: en `(?<![A-Za-z0-9./-])` un «_» abre un inicio válido detrás de otro, y la búsqueda se vuelve cuadrática (128 KB de `_sk-` repetido tarda 68 s, un DoS con contenido web). Dos pasos: (1) candidato lineal `sk-[A-Za-z0-9_-]{20,}`, con `finditer` y el límite izquierdo que se decida; (2) en Python, es clave si el candidato empieza por un prefijo conocido (`sk-ant-`, `sk-proj-`, `sk-svcacct-`, `sk-live-`…) o tiene un tramo `[A-Za-z0-9_]{16}`. Regresión: 5000 claves aleatorias con semilla fija por formato (0 sin detectar), las URL de H-07 y una prueba de tiempo con `_sk-` repetido |  abierto |
| H-18 | media | `r02_01_r8_sk.py`, casos 2 y 2b: `Mensajeria.crear("CT-03", …, {"pregunta": "Uso esta clave:\n" + clave})` | **Esperado:** el mensaje se rechaza íntegro (R8), como en develop. **Obtenido:** se crea. `contiene_credenciales` (sobre de mensajes, CT-23 del Broker y salidas de los agentes en `agentes.py`) busca en el volcado JSON, donde el salto de línea es `\\n`. Con eso, el límite izquierdo ve una «n» y la clave no cuenta. Igual con tabulador y CRLF. `contenido_sensible`, sobre el texto crudo, sí la detecta. Viene de la r01 (H-01), no de la r02 | Que `contiene_credenciales` recorra la estructura y busque en cada cadena cruda, como `contenido_sensible`, o que el límite izquierdo admita una secuencia de escape (`(?<=\\[nrt])`). Regresión con `\n`, `\t` y `\r\n` delante de la clave en un CT-03 |  abierto |
| H-19 | media | `r02_02_almacen_recuperacion.py`, casos 2 y 3. (2) Sello de F5 devuelto a `[1, hash_1]` con tres registros confirmados, p. ej. al restaurar `sellos_integridad.json` de una copia anterior. (3) En una instancia viva, alguien añade al final de F5 un registro con la cadena bien calculada | **Esperado:** un proceso que muere entre el registro y el sello deja como mucho **un** registro sin sellar por fichero (cada `escribir` es registro más sello bajo el cerrojo). Más de uno es manipulación o un sello viejo, y debe fallar cerrado como en la r01. Una recuperación siempre deja rastro. **Obtenido:** (2) abre y aparta a `*.no_confirmado.jsonl` dos registros **confirmados** (`dos`, `tres`). La cadena operativa los pierde (en F4 sería una RESOLUCION; en F10, una degradación de H5), y solo queda una incidencia «Operativa». (3) `leer` y `verificar_integridad` aplican la recuperación en silencio: borran el registro del fichero, `verificar_integridad()` devuelve `True` y no queda ninguna incidencia, porque `_recuperadas` solo se vuelca en `__init__`. Con la r01, los dos casos fallaban cerrado. Respuesta a la pregunta del encargo: no sirve para aceptar registros manipulados, pero sí para sacar de la cadena registros confirmados | Recuperar solo si sobra exactamente un registro (mejor aún con una marca de intención `n+1` escrita antes del registro, como proponía la r01) y fallar cerrado en cualquier otro caso. Fuera de `__init__` (instancia viva, `verificar_integridad`), no reescribir: lanzar el fallo de integridad o, como mínimo, escribir la incidencia en el momento. Regresión con los dos casos |  abierto |
| H-20 | baja | `r02_02_almacen_recuperacion.py`, caso 4: F5 con un registro sin sellar y F6 manipulado | **Esperado:** validar antes de mutar: si la apertura falla, no se toca nada. **Obtenido:** `Almacen()` lanza «Fallo de integridad en F6», pero F5 ya se ha reescrito y su registro ya está apartado | Dos fases en `__init__`: primero se validan todos los ficheros y se calcula qué hay que recuperar; después se reescribe |  abierto |
| H-21 | baja | `r02_02_almacen_recuperacion.py`, caso 6: `KeyboardInterrupt` en `temporal.unlink(...)` del `finally` de `_guardar_json`, ya sustituido el sello | **Esperado:** el almacén sigue abriendo (lo que H-10 quería). **Obtenido:** el sello ya dice `n+1`, `escribir` trunca el registro y el almacén no abre («el final de F5 difiere del sello»). La ventana es muy pequeña | En `_guardar_json`, que la limpieza del temporal tras un `replace` correcto no propague, o en `escribir`, que no trunque si el sello en disco ya incluye el registro |  abierto |
| H-22 | baja | `r02_04_bases_plazos_umbral.py`, caso 3 | **Esperado:** un plazo de solo fecha vale todo ese día en Madrid. **Obtenido:** el final del día se calcula como 00:00 + 24 h − 1 µs en tiempo absoluto. El 29-3-2026 (día de 23 h) vence a la 01:00 del 30, una hora tarde, y el 25-10-2026 (día de 25 h) vence a las 23:00 del 25, una hora antes. La detección por `len == 10` no reconoce «2026-6-8» ni «20260608», que vencen a las 00:00 (caso 3b; «8/6/2026» se lee como 6 de agosto, igual que en develop) | Tomar las 00:00 locales del día siguiente (fecha + 1 día, localizada) y reconocer la fecha sola al interpretarla (`dt.date.fromisoformat` o un patrón `^\d{4}-\d{2}-\d{2}$`), rechazando lo que no sea ISO |  abierto |
| H-23 | baja | `r02_04_bases_plazos_umbral.py`, caso 4; fila T-57 de la deuda | **Esperado:** un parámetro `[PROPUESTO]` se valida al leerlo y figura en la deuda (T-57) para que lo decida el operador. **Obtenido:** `senales.umbral_favorable` acepta NaN (todo «contraria»), `True`, −1, 7 y «0.5». No figura en T-57 ni en ninguna incidencia | Validar que es un número finito en [0, 1] (no booleano) y añadirlo a la lista de T-57 con su valor de partida |  abierto |
| H-24 | baja | Lectura de documentos | Documentación de la r02 incompleta. (a) La fila T-92 de la deuda dice «EN QA r01». (b) `analisis-tecnico.md` no recoge el diseño de la r02: la recuperación de una escritura no confirmada y sus límites, el nuevo formato `MSG-BRK-` y la regla del plazo de solo fecha. (c) H-11 «pasa a la deuda», pero la fila T-92 aún no lo nombra (se puede hacer al cerrar) | Corregir los tres puntos |  abierto |

### Invariantes

- **F y G antes de una orden:** sin cambios. El Bloque A no emite órdenes.
- **Sin LLM en la ruta determinista ni en los controles:** se cumple.
- **Los controles no se relajan solos:** **no.** R8 detecta menos claves que en develop (H-17 y H-18).
- **Falla cerrado y valida antes de mutar:** **no del todo.** H-19 (un sello viejo saca de la cadena registros confirmados, sin rastro en la instancia viva), H-20 y H-21.
- **Ningún número escrito a mano:** se cumple (H-09 corregido). Falta validar el valor nuevo (H-23).
- **Ninguna decisión del operador en silencio:** INC-T92-01 en T-57. `senales.umbral_favorable` está `[PROPUESTO]`, pero no en T-57 (H-23). La regla de H-15 vuelve a la de develop.
- **Sin secretos ni datos personales:** `tools/secrets_scan.py` sin hallazgos, también con las sondas `r02_*` (las claves se arman en tiempo de ejecución).
- **Documentación:** README del ejecutor, `CLAUDE.md` (401) y `ri-probar` al día. Lo pendiente está en H-24.

### Veredicto

**NO APTO.** H-06 a H-16 están corregidos con su regresión, que falla con `c7127dc`, y las explicaciones de las sondas `r01_01` (1c) y `r01_02` (2) son correctas. Pero la corrección de H-07 introduce H-17, que es **alto**: R8 deja de detectar alrededor del 3 % de las claves con la forma real del proveedor del propio sistema (y de OpenAI), que develop detectaba todas. Eso relaja un control de seguridad, y por eso CA-4 no se cumple.

Para la r03:
- corregir H-17 sin volver a los falsos positivos de H-01 ni introducir una búsqueda cuadrática;
- corregir H-18 y H-19 (medios), o justificar que pasen a la deuda.

Los bajos (H-11 y H-20 a H-24) pueden pasar a la deuda con su ID. El revisor de la r03 vuelve a ejecutar `revisores/r01_*.py` y `r02_*.py`.

## Ronda r03

- **Revisor:** revisor nuevo sin contexto de la implementación ni de las QA r01 y r02 (Claude, subagente de QA) · **Ronda:** r03 · 10-11-2026
- **Código revisado:** `5a56c9c` (rama local `claude/t92-auditoria-astra`); comparaciones con `6f02e11` (r02) y `dae70df` (develop).

### Reproducción desde limpio

```bash
git -C /home/claude/repo worktree add --detach /tmp/claude-0/t92r03 5a56c9c
ln -s /home/claude/repo/.venv /tmp/claude-0/t92r03/.venv
W=/tmp/claude-0/t92r03
export PYTHONPATH=$W/bloque_a/11_Ejecutor:$W/bloque_a_forex/11_Ejecutor:$W/bloque_b/11_Ejecutor
cd $W && .docs/scripts/gate.sh --completo        # 12/12: A 420, FX 68, B 176 (log .docs/scripts/.logs/gate_20261110_232228.log)
# sondas anteriores (python -I; comprueban que bloque_a se importa de la copia)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_01_cesta_bases.py $W/bloque_a/11_Ejecutor          # 1 fallo (1c)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_02_almacen.py $W/bloque_a/11_Ejecutor              # 1 fallo (2, H-11)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_03_contratos.py $W/bloque_a/11_Ejecutor            # se corta en el caso 1 (MensajeInvalido: MSG-BRK)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_04_plazos_y_literales.py $W/bloque_a/11_Ejecutor   # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_01_r8_sk.py $W/bloque_a/11_Ejecutor                # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_02_almacen_recuperacion.py $W/bloque_a/11_Ejecutor # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_03_contratos.py $W/bloque_a/11_Ejecutor            # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_04_bases_plazos_umbral.py $W/bloque_a/11_Ejecutor  # 1 fallo (3, 29-3)
# sondas nuevas de la r03
.venv/bin/python -I .docs/tickets/T-92/revisores/r03_01_r8_dos_pasos.py $W/bloque_a/11_Ejecutor          # 18 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r03_02_almacen_recuperacion.py $W/bloque_a/11_Ejecutor  # 0 fallos (4 INFO)
.venv/bin/python -I .docs/tickets/T-92/revisores/r03_03_plazos_umbral.py $W/bloque_a/11_Ejecutor         # 0 fallos (INFO de formas)
```

`test_t92_revision.py` de la r03 (51 pruebas), copiado sobre `6f02e11`: de las 17 nuevas (`-k r02_`) fallan 15 y pasan 2. Pasan `test_r02_h17_r8_sin_retroceso_cuadratico` (la r02 ya era lineal) y `test_r02_h23_…[None]` (sin el parámetro ya fallaba con `KeyError`). Todas las demás, de H-17 a H-23, fallan con la r02. `pruebas.md` no da este recuento (H-31).

### Sondas anteriores: ¿son correctas las explicaciones del ticket?

- **`r01_01` (1c), `r01_02` (2) y `r01_03` (1):** sí, por lo mismo que en la r02. Es la regla de develop para un miembro inválido al emitir, el límite H-11 y el formato `MSG-BRK-` (H-08).
- **`r02_04`, caso 3: sí.** La sonda envía la consulta el 5-6 (`AS_OF`). `vencer("2026-03-29T22:00Z")` lee F5 a esa fecha y la consulta aún no existe, así que devuelve `[]`; el 5-6 sí la vence (`r03_03`, caso 1b). Con la consulta enviada el 2-3, los cinco bordes (día normal, 29-3 de 23 h, 25-10 de 25 h, víspera del cambio y 31-12) son exactos al microsegundo (`r03_03`, caso 1).

### Estado de H-17 a H-24

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-17 | **corregido en lo principal; queda H-25 (alta)** | En contexto normal se detectan 4000 de 4000 claves en cada formato: `ant-api03`, `ant-admin01`, `proj`, `svcacct`, `admin`, la clásica de 48, hexadecimal 32 y `or-v1-` + 64 hexadecimales (`r03_01`, caso 1). Las 79 líneas del corpus del Bloque A con «sk-» dan 0 falsos positivos (develop da 6). La peor entrada adversaria de hasta 1 MB tarda 0,48 s. Pero siguen sin detectarse `key-sk-…` y `…/sk-…`, que H-17 nombraba, y además la clave tras un `\n` dentro de un texto JSON (H-25) |
| H-18 | **corregido en estructuras; el mismo mecanismo sigue en el texto JSON (H-25)** | `contiene_credenciales` detecta la clave tras `\n`, `\t`, CRLF, U+2028, NUL o NBSP, también en claves de dict, listas, tuplas y sets (`r03_01`, casos 2 y 2b). Falla con `bytes` (H-26) y con un `\n` literal, de barra y n (H-25) |
| H-19 | **corregido para un fichero; queda H-27 (media)** | Con dos registros por encima del sello en un fichero, falla cerrado. Una instancia viva no recupera: un registro forjado no se lee, `verificar_integridad` da False y la escritura se rechaza (`r03_02`, casos 5a a 5c). Sí acepta un registro sin sello en **cada uno** de varios ficheros (H-27) |
| H-20 | **corregido** | `r02_02`, caso 4, y la prueba de la r03: si otro fichero no valida, no se reescribe nada |
| H-21 | **corregido** | Con una muerte real (`os._exit`) tras guardar el sello, el registro se conserva (`r03_02`, caso 1). Con Ctrl-C en el fsync del registro, en `json.dump` del sello, en el `replace` o en el `unlink` posterior, la instancia viva, el disco y el sello coinciden y el almacén abre (caso 7). Con escritura y apertura a la vez desde dos procesos (150 escrituras y 60 aperturas), no hay recuperaciones falsas (caso 8) |
| H-22 | **corregido; quedan bajos (H-30)** | «2026-06-08», «2026-6-8», «20260608» y «2026/06/08» valen todo el día local, también los días de cambio de hora; una hora explícita no se alarga (`r03_03`, casos 1 y 2) |
| H-23 | **corregido** | Se aceptan 0, 1 y `np.float64`. Fallan cerrado NaN, ±inf, `True`, `False`, −0,01, 1,01, «0.5», `None`, `[0.5]`, `Decimal` y `np.int64`. La señal igual al umbral es «favorable» (`r03_03`, caso 4). Está en T-57 |
| H-24 | **corregido; queda H-31 (baja)** | Fila T-92 «EN QA r03» con el límite H-11; T-57 con `umbral_favorable`; el diseño de r02 y r03 en `analisis-tecnico.md` |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 43 `test_t87_*` y 51 `test_t92_revision.py`, en verde dentro de las 420 del gate |
| CA-2 | sí | T-53, T-65 (r01 a r04) y T-66 en verde. La r03 solo toca `almacen.py`, `contratos.py`, `interfaz_broker.py`, `llm.py` y el umbral de `orquestacion.py` |
| CA-3 | sí | Gate 12/12; `pytest_bloque_a=420` en `tools/cuotas.txt`, `CLAUDE.md` y `ri-probar` |
| CA-4 | **no** | Las pruebas existen y fallan con la rama de Astra y con la r02. Pero la corrección de H-01 sigue relajando R8 respecto a develop con la forma de clave del proveedor del propio sistema (H-25). Es el mismo criterio por el que la r02 no lo dio por cumplido |
| CA-5 | sí | INC-T92-01 `[PROPUESTO]` en `docs/incidencias.md` y en la fila T-57 |

### Lo que se comprobó y está bien

- **T-65 y las rondas anteriores no se deshacen:**
  - las sondas `r01_*` y `r02_*` siguen en verde, salvo los casos explicados arriba;
  - la r03 no toca la evaluación, la CESTA, el Motor ni el presupuesto.
- **Sin números a mano nuevos.** Los literales añadidos son constantes de la regla y no parámetros de política:
  - el 20 del candidato viene de develop;
  - el 16 del tramo es de la r02;
  - el intervalo [0, 1] es la escala de HT-03;
  - 1 µs marca el final del día.
- **Todo el Bloque A pasa por la función común.** No queda ningún uso de `RE_SECRETO` en `bloque_a/` fuera de `secretos_en_texto`. Forex y B tienen sus propios patrones, sin cambios.
- **El cerrojo cubre la apertura.** `__init__` recupera dentro de `_transaccion()`, así que un proceso que abre nunca aparta el registro de otro que está escribiendo (`r03_02`, caso 8).
- **Recuperación idempotente.** Reabrir no repite la recuperación ni la incidencia, y el almacén sigue siendo escribible (`r03_02`, casos 2 y 2b). Si el proceso muere a mitad de la recuperación, al reabrir abre en lo sellado y el registro sigue apartado (caso 3).
- **Un registro forjado nunca entra en la cadena:**
  - en una instancia viva, falla cerrado;
  - al reabrir, se aparta con incidencia.

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-25 | **alta** | `r03_01_r8_dos_pasos.py`, casos 1b, 2 (`'\\n'`), 2d y 2e. Por ejemplo, `contenido_sensible(json.dumps({"nota": "clave:\n" + clave}))` con `clave` = `"s"+"k-"` + `ant-api03-` + 93 caracteres base64url + `AA`; o `ReplayClient(..., "grabar", base)` con un cliente base que devuelve ese texto | **Esperado** (criterio de la r02 para H-17): toda clave con la forma del proveedor del propio sistema que develop detecta se sigue detectando; H-17 citaba ya `key-sk-…` y `…/sk-…`. **Obtenido:** `RE_CANDIDATO_SK` conserva el límite izquierdo `(?<![A-Za-z0-9./-])`, que ya no hace falta para los falsos positivos de H-01 y H-07, porque eso lo decide ahora `_es_clave_sk`. Con ese límite, no se detecta ninguna clave `sk-ant-…` ni `sk-proj-…` en estos casos: <br>(a) detrás de «/», «-» o «.» (`https://…/keys/sk-…`, `OPENAI-KEY-sk-…`, `config.sk-…`: 0 de 200 cada uno; develop, 200 de 200); <br>(b) detrás de un escape `\n` o `\t` dentro de un texto JSON, donde el límite ve la «n» o la «t». Las respuestas de los agentes son texto JSON, así que una clave en su propia línea dentro de una cadena pasa por `respuesta_segura` y por la comprobación de `AnthropicClient` (texto y `model_dump`), y **la grabadora la escribe en la cinta** (caso 2e). Develop la descarta. Después, `contiene_credenciales(datos)` bloquea los datos ya interpretados, pero la cinta ya la tiene. Lo mismo vale para un campo del contexto que sea JSON serializado: va al proveedor | Que el límite izquierdo no deje escapar claves con forma inequívoca:<br>1. Para un candidato con prefijo de proveedor (`ant-`, `proj-`, `svcacct-`, `admin-`), que no haya límite izquierdo o que solo excluya letras y cifras que no formen un escape `\n`, `\t`, `\r`, `\"` o `\/`. Por ejemplo, mirar en Python el carácter anterior y los dos anteriores.<br>2. En `contenido_sensible(str)`, si el texto se puede leer como JSON, revisar también la estructura leída.<br><br>Regresión: clave `ant-api03` aleatoria tras `/`, `-`, `.`, `\\n` y `\\t`; una grabación de `ReplayClient` con esa respuesta; las líneas de H-01 y H-07 y el corpus en 0 | abierto |
| H-26 | media | `r03_01`, casos 1 (UUID, `lf-`, hexadecimales con «-», minúsculas con «_», `token_urlsafe(16)`), 1c y 2b (`bytes`) | **Esperado:** R8 no detecta menos claves que develop. **Obtenido:** no se detecta ninguna `sk-` + UUID v4 en minúsculas ni `sk-lf-` + UUID (Langfuse), ni las hexadecimales con «-» cada 8, ni las minúsculas con cifras y «_» cada 10 (0 de 4000 en cada caso; develop, 4000). Tampoco el 1,4 % de `sk-` + `token_urlsafe(16)` (55 de 4000, la forma de LiteLLM). Tampoco el prefijo en mayúsculas `SK-` (develop es insensible a mayúsculas) ni una clave en un valor `bytes`. `_es_clave_sk` solo acepta un tramo de 16 sin separador o mayúsculas mezcladas con cifras, y la prueba de H-17 genera cuerpos con mayúsculas y cifras casi siempre, así que no lo ve. No son claves del proveedor del sistema | En `_es_clave_sk`, contar como clave también:<br>- un cuerpo con forma de UUID o de hexadecimal agrupado (`[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}`, tramos hexadecimales con cifras);<br>- un candidato con al menos un tramo de 8 que mezcle letras y cifras.<br><br>Además: candidato insensible a mayúsculas y `bytes` decodificados en `_textos`. Regresión con generadores por formato que incluyan cuerpos solo en minúsculas | abierto |
| H-27 | media | `r03_02`, caso 9: F5 y F6 con un registro **confirmado** cada uno por encima de un `sellos_integridad.json` restaurado de una copia dos escrituras atrás | **Esperado:** cada `escribir` es registro más sello bajo un único cerrojo, así que una muerte del proceso deja como mucho UN registro sin sello **en todo el almacén**. Más de uno es un sello viejo o una manipulación, y debe fallar cerrado (como pedía H-19). **Obtenido:** abre y saca de la cadena los dos registros confirmados, F5 = `['uno']` y F6 = `['m1']`, con una incidencia «Operativa» por fichero. Con un sello de N escrituras atrás repartidas en N ficheros, se apartan N registros confirmados (por ejemplo, una RESOLUCION de F4 y una degradación de F10) | En `__init__`, si `_por_recuperar` tiene más de una entrada, fallo de integridad sin reescribir nada. Regresión con dos ficheros |  abierto |
| H-28 | baja | `r03_01`, caso 3: `Descarga: sk-hynix_3Q24_earnings_release.pdf`, `sk-Hynix-Q3-2024-Earnings-Presentation.pdf`, `sk-innovation-2024Q4-results-presentation`, `sk-biopharm_FY2023_annual_report_EN.pdf` | **Esperado:** el nombre de un fichero de relación con inversores no es una clave. **Obtenido:** la regla «mayúsculas y cifras» los toma por clave, y el encargo o la respuesta quedan PARCIAL sin llamar al modelo. Detrás de «/» no pasa (por el límite de H-25), y el corpus actual da 0 | Pedir que la mezcla de mayúsculas y cifras esté dentro de un mismo tramo de 8 o más (`3Q24` y `FY2023` no llegan), en lugar de en toda la cola. Regresión con estos cuatro textos |  abierto |
| H-29 | baja | `r03_02`: (a) caso 3, muerte tras reescribir el fichero y antes de la incidencia; (b) caso 4, línea final a medio escribir | **Esperado:** toda recuperación deja rastro en HA, y una escritura cortada a mitad de línea, por ejemplo por un corte de corriente, se trata como no confirmada. **Obtenido:** (a) el registro queda apartado, pero no hay incidencia en HA (0), y al reabrir ya no hay nada que recuperar; (b) el almacén no abre (`JSONDecodeError`) y hay que repararlo a mano. Falla cerrado, que es el lado seguro | (a) Anotar la incidencia antes de reescribir el original, o, al abrir, anotar una si existe un `*.no_confirmado.jsonl` sin su incidencia. (b) Si la última línea no acaba en «\n», no se puede leer y está por encima del sello, apartarla como no confirmada |  abierto |
| H-30 | baja | `r03_03`, casos 2 y 3 | **Esperado:** un plazo de CT-23 que no sea una fecha ISO ni una fecha y hora completas se rechaza (como sugería H-22). **Obtenido:** se acepta e interpreta en silencio: «2026» da el 1-1-2026 a las 23:59:59, «2026-06» el 1-6, y «8 June 2026» o «June 8, 2026» vencen a las 00:00 de ese día, 24 h antes que «2026-06-08». Con `zona_horaria: America/Santiago`, el plazo «2026-09-05» hace que `enviar` lance `ValueError` (las 00:00 del 6-9 no existen) | Admitir solo `^\d{4}-\d{1,2}-\d{1,2}$`, `^\d{8}$` o una fecha y hora completas; rechazar el resto. Usar `tz_localize(…, nonexistent="shift_forward")` |  abierto |
| H-31 | baja | Lectura de documentos | (a) `pruebas.md` (r03) no dice cuántas pruebas nuevas fallan con `6f02e11` (son 15 de 17, arriba). (b) El README del ejecutor sigue diciendo «se apartan los registros sin confirmar», en plural, y no dice que una instancia viva falla cerrado hasta que se reabre. (c) «Límites» de `analisis-tecnico.md` no recoge que un sello restaurado de una sola escritura atrás no se distingue de una muerte del proceso y aparta un registro confirmado (`r03_02`, caso 6) | Completar los tres puntos |  abierto |

### Invariantes

- **F y G antes de una orden:** sin cambios. El Bloque A no emite órdenes.
- **Sin LLM en la ruta determinista ni en los controles:** se cumple. R8 es una expresión regular más Python.
- **Los controles no se relajan solos:** **no.** R8 detecta menos claves que develop, también con la forma del proveedor del sistema (H-25 y H-26).
- **Falla cerrado y valida antes de mutar:** se cumple salvo H-27. Con varios ficheros por encima del sello, el almacén muta en lugar de fallar.
- **Ningún número escrito a mano:** se cumple.
- **Ninguna decisión del operador en silencio:**
  - `umbral_favorable` e INC-T92-01 están en T-57;
  - la interpretación de formas de fecha no ISO (H-30) es baja.
- **Sin secretos ni datos personales:** `tools/secrets_scan.py` sin hallazgos, también con las sondas `r03_*` y este `qa.md` (las claves se arman en tiempo de ejecución).
- **Documentación:**
  - al día: la fila T-92 con el límite H-11, T-57, INC-T92-01, `CLAUDE.md` (420) y `por_defecto.yaml` (`umbral_favorable` `[PROPUESTO]`);
  - pendiente: H-31.

### Veredicto

**NO APTO.** La r03 corrige bien H-19 a H-24. El almacén ya no pierde registros confirmados por una sola escritura cortada, no acepta forjados, abre tras un Ctrl-C en cualquier punto y es correcto con dos procesos. El plazo y el umbral también están bien. H-17 está corregido en el caso principal: las claves en texto plano, ahora el 100 %.

Pero queda un hallazgo **alto**, H-25. Con el criterio que la r02 fijó para H-17 (toda clave que develop detecta se sigue detectando), R8 sigue sin ver las claves `sk-ant-…` detrás de «/», «-», «.» o de un escape `\n` o `\t` dentro de un texto JSON. Es justo la forma de las respuestas de los agentes, y con ella la clave llega a la cinta grabada. Parte de esto ya lo nombraba H-17 (`key-sk-…`, `…/sk-…`), y la r03 conservó a propósito el límite izquierdo que lo causa, aunque `_es_clave_sk` ya lo hace innecesario. La corrección es pequeña y está acotada.

Para la r04:
- corregir H-25 con su regresión;
- corregir H-26 y H-27 (medios) o justificar que pasen a la deuda con su ID;
- H-28 a H-31 (bajos) pueden pasar a la deuda.

El revisor de la r04 vuelve a ejecutar `revisores/r01_*.py`, `r02_*.py` y `r03_*.py`.

## Ronda r04

- **Revisor:** revisor nuevo sin contexto de la implementación ni de las QA r01 a r03 (Claude, subagente de QA) · **Ronda:** r04 · 11-11-2026
- **Código revisado:** `1230cc3` (rama local `claude/t92-auditoria-astra`); comparaciones con `5a56c9c` (r03) y `dae70df` (develop).

### Reproducción desde limpio

```bash
git -C /home/claude/repo worktree add --detach /tmp/claude-0/t92r04 1230cc3
ln -s /home/claude/repo/.venv /tmp/claude-0/t92r04/.venv
W=/tmp/claude-0/t92r04
export PYTHONPATH=$W/bloque_a/11_Ejecutor:$W/bloque_a_forex/11_Ejecutor:$W/bloque_b/11_Ejecutor
cd $W && .docs/scripts/gate.sh --completo        # 12/12: A 439, FX 68, B 176 (log .docs/scripts/.logs/gate_20261110_235545.log)
# sondas anteriores (python -I; comprueban que bloque_a se importa de la copia)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_01_cesta_bases.py $W/bloque_a/11_Ejecutor          # 1 fallo (1c)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_02_almacen.py $W/bloque_a/11_Ejecutor              # 1 fallo (2, H-11)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_03_contratos.py $W/bloque_a/11_Ejecutor            # se corta en el caso 1 (MSG-BRK, H-08)
.venv/bin/python -I .docs/tickets/T-92/revisores/r01_04_plazos_y_literales.py $W/bloque_a/11_Ejecutor   # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_01_r8_sk.py $W/bloque_a/11_Ejecutor                # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_02_almacen_recuperacion.py $W/bloque_a/11_Ejecutor # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_03_contratos.py $W/bloque_a/11_Ejecutor            # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r02_04_bases_plazos_umbral.py $W/bloque_a/11_Ejecutor  # 1 fallo (3, 29-3)
.venv/bin/python -I .docs/tickets/T-92/revisores/r03_01_r8_dos_pasos.py $W/bloque_a/11_Ejecutor          # 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r03_02_almacen_recuperacion.py $W/bloque_a/11_Ejecutor  # 0 (caso 9 ya falla cerrado)
.venv/bin/python -I .docs/tickets/T-92/revisores/r03_03_plazos_umbral.py $W/bloque_a/11_Ejecutor         # 1 fallo (2a, por H-30)
# sondas nuevas de la r04
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py $W/bloque_a/11_Ejecutor  # 11 fallos (2b y 2c: H-32)
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_02_almacen_corte.py $W/bloque_a/11_Ejecutor   # 2 fallos (1: H-35; 5: H-34)
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_03_plazos_iso.py $W/bloque_a/11_Ejecutor      # 4 fallos (3b: H-37; 4: H-38)
```

`test_t92_revision.py` de la r04 (70 pruebas), copiado sobre `5a56c9c` y ejecutado con ese código: de las 20 nuevas (`-k r03_`) fallan 16 y pasan 4. Las 4 que pasan ya funcionaban en la r03:
- `h25[\n]`: salto de línea real, que es H-18;
- `h25[_]`: el límite izquierdo de la r03 no excluía «_»;
- `h28[SK-Hynix-Q3-…]`: el candidato de la r03 distinguía mayúsculas;
- `h30[mañana]`: `pd.Timestamp` ya la rechazaba.

Fallan con la r03 todas las demás de H-25 a H-30. `pruebas.md` no da este recuento (H-39). Con `r04_02` sobre la r03, el corte de la última línea abre en 2 de 321 bytes (r04: 312) y el almacén anterior con la línea cortada no abre (r04 sí abre, H-34).

### Sondas anteriores: ¿son correctas las explicaciones del ticket?

- **`r01_01` (1c), `r01_02` (2), `r01_03` (1) y `r02_04` (3): sí.** Por lo mismo que en las r02 y r03: la regla de develop para un miembro inválido al emitir, el límite H-11, el formato `MSG-BRK-` (H-08) y la consulta que el 29-3 aún no existe.
- **`r03_03`: no del todo.** El README dice que da 0 fallos, pero da 1 (caso 2a): esa sonda esperaba que «2026-6-8» y «2026/06/08» valieran todo el día, y la r04 los rechaza a propósito (H-30, «solo ISO 8601»). El fallo es correcto, pero la explicación tendría que figurar en el README (H-39).
- **`r03_01` y `r03_02`: 0 fallos, correcto.** El caso 9 de `r03_02` (dos ficheros por encima del sello) ahora falla cerrado.

### Estado de H-25 a H-31

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-25 | **corregido en los casos citados; el mismo mecanismo sigue con otros escapes (H-32)** | 200 de 200 claves `ant-api03` detrás de «/», «-», «.», «_», `key-`, «=», ««», «“», NBSP, «—», tabulador, «(» y «`» (`r04_01`, caso 2). Los escapes JSON `\n`, `\t`, `\r` y `\/` se sustituyen. Siguen sin verse `\uXXXX`, `\b`, `\f`, `%XX` y `\xNN` (H-32) |
| H-26 | **corregido; queda un residuo bajo (H-36)** | 4000 de 4000 en cada formato (`r04_01`, caso 1): UUID en minúsculas y mayúsculas, `lf-`, hexadecimal con «-», minúsculas con «_», solo minúsculas, `SK-`. Con `token_urlsafe(16/24/32)` no se escapa ninguna de 50 000 en cada caso. Detecta `bytes`, `bytearray` y `bytes` dentro de un dict |
| H-27 | **corregido** | Registros sin sello en dos ficheros fallan cerrado sin tocar nada: `r03_02` caso 9, `r04_02` caso 2a (línea cortada en F5 y registro sin sello en F6) y la prueba, que falla con la r03 |
| H-28 | **corregido para las formas en mayúsculas; quedan las minúsculas (H-33)** | Los cuatro nombres de fichero de la r03 ya no son clave. «q2», «fy2023» o «1q24» en minúsculas, que es como van en las URL, siguen siéndolo |
| H-29 | **corregido para un corte en un carácter ASCII; quedan H-34 y H-35** | Con el último registro cortado en cada uno de sus 321 bytes, abre en lo sellado, aparta el resto, anota una sola incidencia y sigue escribiendo en 312 casos; la r03 solo en 2. Los 9 que no abren son cortes a mitad de un carácter UTF-8 de varios bytes (H-35). En un almacén anterior a los sellos la línea cortada no se aparta (H-34). (a) está en «Límites» |
| H-30 | **corregido para textos; quedan H-37 y H-38** | Se rechazan «2026», «2026-06», «8 June 2026», «June 8, 2026», «2026-6-8», «2026/06/08», «08/06/2026», «2026-06-08T09», «mañana», fechas imposibles, semana ISO y día ordinal. Se aceptan la fecha, `AAAAMMDD`, la fecha con hora, «Z», `+0200` y nanosegundos. En Madrid los bordes del 29-3 (23 h) y del 25-10 (25 h) son exactos. En Santiago, el 5-9 (sin medianoche) vence a las 23:59:59,999999 −04 sin lanzar; las 00:30 inexistentes pasan a la 01:00 −03; el día de 23 h y el de 25 h acaban bien (`r04_03`, casos 1 y 2). La medianoche inexistente no tiene prueba de regresión (H-39) |
| H-31 | **corregido; se repite el mismo hueco en la r04 (H-39)** | `pruebas.md` da el recuento contra la r02. El README del ejecutor está en singular y nombra la instancia viva. «Límites» recoge el sello restaurado |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 43 `test_t87_*` y 70 de `test_t92_revision.py` (113), en verde dentro de las 439 del gate |
| CA-2 | sí | T-53, T-65 (r01 a r04) y T-66 en verde. La r04 solo toca `almacen.py`, `contratos.py` (R8), `interfaz_broker.py` (CT-23) y `llm.py`. La única prueba anterior que cambia es un parámetro de H-22 («2026-6-8»), retirado por H-30 |
| CA-3 | sí | Gate 12/12; `pytest_bloque_a=439` en `tools/cuotas.txt`, `CLAUDE.md` y `ri-probar`; ruff baja a 3072 |
| CA-4 | sí | Las pruebas de H-01 a H-05 no cambian desde la r02, que comprobó que fallan con la rama de Astra. La relajación de R8 frente a develop con la forma de clave del proveedor ya solo queda con escapes poco frecuentes (H-32, media). En texto plano, tras cualquier separador o con los escapes JSON de una cadena con saltos de línea, la detección es del 100 % |
| CA-5 | sí | INC-T92-01 `[PROPUESTO]` en `docs/incidencias.md` y en la fila T-57 |

### R8: ¿es razonable el equilibrio?

**Sí.** Invertir la regla (todo es clave salvo lo que tiene forma de texto) es el diseño correcto para un filtro de secretos:
- **Formatos reales de clave:** recall del 100 % en todos los que se han probado (Anthropic, OpenAI proj, svcacct y admin, la clásica, UUID, hexadecimal, `token_urlsafe`, base64url, mayúsculas, `bytes`, claves y valores de dict), igual que develop. Lo que no se detecta son formas que ningún proveedor usa (H-36).
- **Falsos positivos frente a develop:** 0 de 106 líneas del corpus del Bloque A con «sk-» (develop marca 6), y los textos de H-01, H-07 y H-28 pasan.
- **Tiempo:** la peor entrada adversaria de 1 MB tarda 0,47 s.
- **Lo que queda:**
  - un falso negativo realista pero poco frecuente: la clave pegada a un escape que no es `\n`, `\t`, `\r` ni `\/` (H-32);
  - los nombres en minúsculas de las URL de prensa financiera, que son falsos positivos. Fallan cerrado y con incidencia (H-33).

### Lo que se comprobó y está bien

- **T-65 y las rondas anteriores no se deshacen:**
  - las sondas `r01_*`, `r02_*` y `r03_*` siguen en verde, salvo los casos explicados;
  - el diff de r03 a r04 no toca la evaluación, la CESTA, el Motor ni el presupuesto.
- **Almacén:**
  - un único registro sin sello en todo el almacén se aparta con incidencia;
  - dos fallan cerrado sin reescribir nada (`r04_02`, caso 2a);
  - un registro completo sin sello con otra línea cortada encima falla cerrado (2b);
  - una basura sin salto de línea en un fichero vacío se aparta y no entra en la cadena (2c);
  - la validación previa se mantiene con una línea cortada (2d);
  - una instancia viva falla cerrado ante una línea cortada (3a) y al reabrir se recupera (3b);
  - con una muerte real del proceso (`os._exit`) antes del sello, el registro se aparta (4);
  - con Ctrl-C en cualquier punto y con dos procesos a la vez, sigue bien (`r03_02`, casos 7 y 8).
  - Ningún registro manipulado entra en la cadena en ningún caso, y ningún confirmado se pierde, salvo en H-34 (un almacén anterior a los sellos) y en el límite declarado del sello restaurado.
- **Sin números a mano nuevos.** Las longitudes de `RE_TRAMO_TEXTO` (15 letras, 6 siglas, 4 cifras) son constantes de la forma del texto, no parámetros de política. Las horas por defecto de `_plazo` (4 y 24) vienen de develop y T-92 no las toca.

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-32 | media | `r04_01`, casos 2b y 2c. Por ejemplo, `contenido_sensible(json.dumps({"nota": "la clave «" + clave + "»"}))` con `ensure_ascii` por defecto, y `clave` una `ant-api03` armada en tiempo de ejecución; o la misma respuesta grabada con `ReplayClient(..., "grabar", base)` | **Esperado:** ningún escape delante de la clave la oculta (es el mecanismo de H-25). **Obtenido:** 0 % detectado, frente al 100 % de develop, cuando delante va un escape JSON `\uXXXX` («, “, NBSP, —, emoji), `\b` o `\f`, un `%XX` de URL (`key%3D…`, `%20`) o un `\xNN` de `repr`. El límite izquierdo ve la última cifra o letra del escape. La grabadora escribe la clave en la cinta (2c). Los datos ya leídos sí se bloquean (`contiene_credenciales(json.loads(…))`). `contenido_sensible` tampoco entra en los `set` (un valor `set` con NBSP delante no se detecta; `contiene_credenciales` sí). **Media y no alta:** ningún componente del Bloque A escribe JSON con `ensure_ascii` (todos los `json.dumps` del bloque usan `ensure_ascii=False`), los modelos no suelen escapar lo que no es ASCII, y una clave del propio sistema tendría que llegar ya escapada en un contexto | En la segunda variante de `secretos_en_texto`, sustituir también `\\u[0-9a-fA-F]{4}`, `\\x[0-9a-fA-F]{2}`, `\\[bf"\\]` y `%[0-9A-Fa-f]{2}`; que `contenido_sensible` recorra los `set`. Regresión con los diez casos de 2b y la cinta de 2c | abierto (puede ir a la deuda) |
| H-33 | media | `r04_01`, caso 3b | **Esperado:** el nombre de una URL de prensa financiera no es una clave (lo que buscaba H-07). **Obtenido:** se toman por clave 12 de 12 textos reales de este tipo: <br>- URL en minúsculas con códigos de periodo o de producto: `…/sk-hynix-q2-profit-jumps-…`, `…-record-q3-profit-…`, `sk-telecom-5g-…`, `hbm3e`, `fy2023`, `1q24`; <br>- fechas `AAAAMMDD`; códigos de 6 o 7 cifras (KRX `000660`, MarketScreener `SK-TELECOM-CO-LTD-6496057`); <br>- siglas de más de 6 letras (`SK-HYNIX-QUARTERLY-…`) y CamelCase. <br>La r03 no marcaba los que van detrás de «/»; develop los marca todos. Un Analista que cite la URL de Reuters sobre los resultados de SK Hynix pierde la respuesta entera (PARCIAL, con incidencia). El corpus actual da 0. Falla cerrado y queda declarado, y la prioridad es el recall: por eso es media | Admitir en `RE_TRAMO_TEXTO` los códigos de periodo en minúsculas (`[a-z]{1,2}[0-9]{1,4}`, `[0-9][a-z][0-9]{0,2}`, `[0-9]{4}[a-z][0-9]{1,2}`) y las fechas de 8 cifras que sean una fecha válida. Regresión con los 12 textos y las claves de `r04_01` caso 1 | abierto (puede ir a la deuda) |
| H-34 | media | `r04_02`, caso 5: un almacén anterior a los sellos (sin `sellos_integridad.json` ni `formato_almacen.json`) con la última línea a medio escribir | **Esperado:** se aparta como en un almacén sellado, o no abre, como en la r03 y en develop. **Obtenido:** abre y sella los registros buenos, pero la rama de la línea parcial está dentro de `if not legado` y la línea se queda en el fichero. La siguiente escritura (confirmada y sellada) se pega a esa línea, y al reabrir el almacén no abre (`JSONDecodeError`): el registro confirmado queda fuera de la cadena hasta repararlo a mano. Solo se da en la migración, con un almacén que develop ya no podía abrir | En `_actualizar`, aplicar también en modo `legado` el apartado de la línea parcial, o fallar cerrado si hay una. Regresión con el caso 5 | abierto (puede ir a la deuda) |
| H-35 | baja | `r04_02`, caso 1: corte del último registro en cada byte, con texto en español | **Esperado:** cualquier corte se aparta (H-29). **Obtenido:** en 9 de 321 cortes, los que caen a mitad de un carácter UTF-8 de varios bytes («ñ», ««», «—»), `read_text` lanza `UnicodeDecodeError` y el almacén no abre. Falla cerrado | Leer en bytes, separar la última línea antes de decodificar y tratar como parcial la que no decodifica | abierto |
| H-36 | baja | `r04_01`, caso 1 (INFO) | **Esperado:** R8 no detecta menos claves que develop. **Obtenido:** no se detectan las colas hechas solo de tramos con forma de texto: el 2,25 % de 5 grupos de 4 mayúsculas y cifras (estilo licencia), el 0,35 % de 4 grupos base32 de 7 en minúsculas y el 100 % de los grupos de 8 letras minúsculas. No es la forma de ningún proveedor conocido y es el precio aceptado de la regla | Declararlo en «Límites» de `analisis-tecnico.md` | abierto |
| H-37 | baja | `r04_03`, caso 3 | **Esperado:** «solo ISO 8601» (H-30) también para lo que no es texto. **Obtenido:** un plazo numérico 20260608 (por ejemplo, un JSON del operador por la CLI) se lee como nanosegundos de 1970. La consulta BLOQUEANTE queda VENCIDA al enviarla y el análisis sigue con el supuesto, en lugar de pausar (R26). Develop lanzaba `TypeError` al vencer. Un `date` o un `datetime` a medianoche vencen al empezar el día, 24 h antes que el texto «2026-06-08» | Rechazar en `_instante` los números y los booleanos; tratar un `date` como el texto de la fecha | abierto |
| H-38 | baja | `r04_03`, caso 4: un CNS ENVIADA en F5, guardado por develop (que guardaba el plazo tal cual) con «2026-6-8», «8/6/2026» o una hora con zona en texto | **Esperado:** las consultas ya guardadas siguen venciendo. **Obtenido:** `vencer()` lanza `ValueError` al releer ese plazo. El ciclo la llama en F0 (`orquestacion.py`, `self.consultas.vencer(instante)`) sin capturarlo, así que no corre ningún análisis hasta que se cierre esa consulta a mano. Solo se crean consultas desde la CLI del operador | Ser estricto al recibir el plazo (en `enviar`) y tolerante al releer lo guardado; o, si no se puede leer, anotar una incidencia y vencer la consulta | abierto |
| H-39 | baja | Lectura de documentos y pruebas | (a) La sección «Sondas» del README dice que `r03_03` da 0 fallos y da 1 (2a, por H-30). (b) `pruebas.md` (r04) no dice cuántas pruebas nuevas fallan con `5a56c9c` (son 16 de 20, arriba): es el mismo hueco que H-31 (a). (c) La segunda mitad de H-30 (medianoche inexistente) no tiene prueba de regresión | Completar los tres puntos | abierto |

### Invariantes

- **F y G antes de una orden:** sin cambios. El Bloque A no emite órdenes.
- **Sin LLM en la ruta determinista ni en los controles:** se cumple.
- **Los controles no se relajan solos:** se cumple. R8 detecta menos que develop solo en H-32 y H-36, que son una decisión de diseño declarada en el ticket y no un cambio en tiempo de ejecución. Se recomienda cerrar H-32 pronto.
- **Falla cerrado y valida antes de mutar:**
  - se cumple en el almacén sellado;
  - H-34 es la excepción (un almacén anterior abre y después se corrompe);
  - H-37 relaja una pausa BLOQUEANTE con una entrada mal formada.
- **Ningún número escrito a mano:** se cumple.
- **Ninguna decisión del operador en silencio:** `umbral_favorable` e INC-T92-01 están en T-57 como `[PROPUESTO]`. La regla de texto de R8 está documentada en `analisis-tecnico.md`.
- **Sin secretos ni datos personales:** `tools/secrets_scan.py` sin hallazgos, con las sondas `r04_*` y este `qa.md` (las claves se arman en tiempo de ejecución).
- **Documentación:**
  - al día: la fila T-92 «EN QA r04» con el límite H-11, T-57, INC-T92-01, `CLAUDE.md` y `ri-probar` (439), el README del ejecutor y `por_defecto.yaml` (`umbral_favorable` `[PROPUESTO]`);
  - pendiente: H-39.

### Veredicto

**APTO.** Se cumplen CA-1 a CA-5 y no queda ningún hallazgo crítico ni alto.
- **H-25 a H-31 están corregidos, con su prueba,** que falla con la r03 (16 de 20).
- **R8 está bien resuelto:** el 100 % de las claves con forma real, como develop, en texto, tras cualquier separador, con los escapes de una cadena JSON con saltos de línea, en `bytes` y en estructuras. Tiene 0 falsos positivos en el corpus y es lineal.
- **El almacén no deja entrar un registro manipulado** y recupera un corte real en casi todos los bytes.
- **CT-23 solo acepta ISO 8601** y trata bien los cambios de hora y las medianoches que no existen.

Los hallazgos nuevos son medios (H-32 a H-34) y bajos (H-35 a H-39), y pasan a la deuda con su ID al cerrar. Se recomienda corregir H-32 y H-34 antes del modo sombra con API: son pocas líneas cada uno.
