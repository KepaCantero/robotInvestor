# Ejecutor programático del Bloque B (`bloque_b` V1.1 · metodología 2.1)

Bloque B · Robot Investor · V2.0 · actualizado V2.1, 03/11/2026 · subordinado al Documento 0 del Bloque B, óptima V2.1.

Implementa el Bloque B como programa Python:

- Los **24 agentes** se invocan con su system prompt íntegro (V2.1: AG-B24, Analista de Emergentes, Startups y Spin-offs).
- Las **capas 0–4** (fases F0–F10) con las **puertas de viabilidad PV1–PV3** reales: si una puerta no se supera, el análisis se detiene y entrega un **informe de parada**; el Broker puede **forzar la continuación** en 7 días.
- La **puerta de tiempo real**: PT30 previa y en ejecución sobre el acumulado, y PTA, con estimación por capa y la opción `HASTA_PV2`. La puerta persiste puntos de control y se reanuda con `autorizar`.
- Las **consultas del bloque al Broker** (CT-B-28): filtro del Director, BLOQUEANTE con punto de control y pausa, NO_BLOQUEANTE con supuesto declarado, límites por nivel y aportes del Broker.
- Los **seguimientos encargados** (CT-B-29, archivo F11): alta, modificación, pausa, reanudación, cancelación y ciclos N1-SEG con informe de seguimiento; distintos del Vigía.
- La **política de autorización automática** del Broker.
- La **bóveda simulada** de credenciales.
- Los archivos **F1–F6, F10, F11, RC y HA**: append-only, con cadena de hash y matriz de escritura.
- Los **seis entregables** (V2.1: mapa de oportunidades por eslabón, con desglose, PCB, AE, mejores opciones por eslabón y radar de emergentes) con G3 (HT-09, 107 comprobaciones) en dos pasadas; el informe de parada y el de seguimiento con los perfiles reducidos PAR y CIC.
- El horizonte **H5** (décadas) con hitos `HITO_H5` y probabilidades cualitativas.
- El **Vigía**, el **Evaluador** y un **backtest de rankings de candidatos** sin anticipación.

Este README está pensado para el ingeniero que hará el backtesting. **Si la sintaxis de este README difiere de la del Runbook, manda este README** (Runbook, nota inicial); las diferencias están en la sección 5.3.

> Todo lo que trae el paquete es **ficticio**:
> - los universos de `config/universos/`;
> - las series sintéticas;
> - las respuestas del cliente simulado;
> - las salidas de `ejemplos/`.
>
> Sirve para probar el mecanismo, no para juzgar la capacidad del bloque (sección 10).

## 1. Instalación

```bash
cd vB/11_Ejecutor
pip install -e .                       # o: pip install -r requirements.txt  (Python ≥ 3.10)
python -m pytest -q tests              # 118 pruebas, cliente simulado, sin red ni clave (≈ 4 min)
bloque-b --help                        # o: python -m bloque_b.cli --help
```

- **Dependencias:** `anthropic`, `jsonschema`, `numpy`, `pandas`, `PyYAML` y `openpyxl`. La opcional `yfinance` solo sirve en modo vivo y nunca en backtest.
- **Rutas:** el ejecutor busca el resto del paquete en la carpeta padre de `11_Ejecutor`:
  - `02_System_prompts`
  - `05_Archivos_operativos` (F7, F8, F9 y FM)
  - `06_Plantillas_entregables` (esquema del Anexo B y plantilla del informe visual)
- **Copia .docx del entregable 6:** por conversión fiel del Markdown con `pandoc` si está en el PATH; si no, con `python-docx` (encabezados, párrafos y tablas). Si no hay ninguno, se declara la limitación.

  Si mueve el ejecutor, exporte `BLOQUE_B_RAIZ=/ruta/a/vB` o fije `rutas.raiz_paquete` en el YAML.
- **Herramientas de referencia:** HT-02, 03, 07, 08, 09, 10 y 11 están en `bloque_b/herramientas/referencia/`. Son copias literales de `10_Herramientas` y una prueba comprueba que no divergen. Si cambia una herramienta, cópiela.

## 2. Clientes de modelo y prompts

| `--cliente` | Uso | Notas |
|---|---|---|
| `mock` (por defecto) | Pruebas y backtest de la parte determinista | Respuestas deterministas generadas a partir del encargo y válidas frente a los esquemas mínimos. Tokens estimados y caché de prompts simulada |
| `anthropic` | Uso real | Lee `ANTHROPIC_API_KEY` del entorno; la clave nunca se guarda (R10). Detalle debajo de la tabla |
| `replay` | Reproducibilidad | `--replay grabacion.jsonl --replay-modo grabar` envuelve el cliente de `BLOQUE_B_CLIENTE_BASE` (por defecto `anthropic`) y graba cada respuesta. `reproducir` las devuelve exactamente: un backtest con el modelo real se repite sin coste |

Detalle del cliente `anthropic`:

- El system prompt va en bloques con `cache_control` (TTL 1 h) y gestiona `pause_turn`.
- La búsqueda web (`web_search_20260318`) solo se ofrece a AG-B18, AG-B19 y AG-B20, en modo vivo. **Nunca** se ofrece en backtest.
- Los modelos por agente están en `config/por_defecto.yaml`. Compruebe los identificadores en la documentación de Anthropic antes de usarlos.

**Prompts.** Para cada agente se busca `System prompt - <Nombre> - Bloque B - Versión óptima V<x.y>.md` en `02_System_prompts`:

- La búsqueda es **por nombre**: tolera NFC/NFD, mayúsculas y cualquier sufijo de versión, y toma la versión más alta.
- AG-B18 admite el alias «Documentador para el Analizador de Mercados».
- El prompt se envía íntegro, seguido de un bloque fijo de interfaz con el ejecutor (`prompts.BLOQUE_EJECUTOR`).

Si falta un prompt:

| Agente | Qué se usa | Registro |
|---|---|---|
| Especialistas (AG-B03…B11) | Marco común de los Analistas de dimensión | Modo degradado declarado |
| Cualquier otro, con `mock` o `replay` | Marcador | Las pruebas no dependen del contenido de los prompts: usan una carpeta vacía |
| Cualquier otro, con `anthropic` | Error | Se detiene la ejecución |

`bloque-b estado` informa de cada agente: CARGADO, DEGRADADO o AUSENTE.

## 3. Configuración

Se usa `config/por_defecto.yaml`, sobre el que se fusiona el YAML que pase con `--config`. Claves principales:

| Clave | Qué controla |
|---|---|
| `modelos`, `max_tokens`, `llm` | Modelo por agente, reintentos, caché, búsqueda web (agentes y tipo) |
| `uc` | Conversión de tokens en UC (Anexo A: 1 UC ≈ 8 000 tokens de entrada y 1 500 de salida; la lectura de caché pesa 0,1) |
| `reloj` | `tipo: auto` (simulado con `mock`/`replay`, real con `anthropic`), `real` o `simulado`; `factor_simulado` y `sigma_ruido` |
| `puerta_tiempo` | Umbral (30), tope automático (240; nunca más de 480), recordatorio (24 h), caducidad (7 días), `modelo` (sobrescribe parámetros de HT-08) |
| `politica_autorizacion` | Política inicial (vacía). En servicio se cambia con `decision` (CT-B-04 → F10) |
| `marco_invertibilidad`, `top_n`, `horizontes_sesiones` | Marco 2.7, top-N por nivel y sesiones por horizonte (H1 5, H2 21, H3 63, H4 252, H5 1260) |
| `capas` (V2.1) | Plazo para forzar la continuación (7 días) y hitos H5 mínimos (3) |
| `consultas_broker` (V2.1) | Límites por nivel (N1 1 · N2 3 · N3 6 · N1-SEG 1), bloqueantes máximos, plazos (4 h y 48 h), recordatorio y criterio de consulta recurrente |
| `seguimientos` (V2.1) | Máximo de activos (25), objetivo y UC por ciclo, línea base, recordatorio sin fecha de fin, días por frecuencia |
| `motor` | Réplicas bootstrap, perturbación de pesos, simulaciones de Monte Carlo, bloque del bootstrap, ventana de correlaciones |
| `auditoria` | Muestreo del Auditor por nivel (V2.1: PARADA 30 %, N1-SEG 20 %). `en_backtest: false` evita el coste del Auditor LLM; G3 se aplica siempre |
| `evaluacion` | Muestras mínimas, condiciones de certificado, recalibración en sombra |
| `backtest` | Frecuencia por defecto y `fecha_corte_modelo` (aviso de fuga por conocimiento) |
| `datos_sinteticos.semilla` | Semilla de las series sintéticas (14) |

**Ámbitos** (`config/ambitos_ejemplo.yaml`):

- Clave → nombre, nombre llano, tipo de objeto, incluye/excluye, región, tipos de activo y horizonte.
- Indicador y referencia (símbolos HT-01).
- Cadena y, opcionalmente, `cadena_llana`: el nombre sin jerga de un eslabón para el informe visual.

En F0 el Director elige la clave. La petición puede fijarla con `objeto.clave_universo` (o, desde el Bloque A, con `paquete_para_bloque_B.x_clave_universo`). Hay 10 ámbitos de ejemplo que cubren los 12 tipos de activo.

## 4. Datos (HT-01), universos y punto en el tiempo

### 4.1 Series

`--datos CARPETA` lee un CSV por símbolo, `<SIMBOLO>.csv`:

- Cabecera `fecha,apertura,maximo,minimo,cierre,volumen` o, como mínimo, `fecha,cierre`. También se aceptan los alias `date`, `close`, `adj close` y `valor`.
- Columna opcional `fecha_publicacion`: la fila solo es visible cuando `fecha_publicacion ≤ as_of`. Sirve para series macro publicadas con retraso o revisadas.
- Los indicadores, referencias y series auxiliares usan el mismo formato.

Sin `--datos` se generan series sintéticas en memoria (2021-01-04 → 2026-10-30) con factor común por grupo y regímenes de deriva. Respetan las altas y bajas de los universos de ejemplo. `bloque-b generar-sinteticos --salida DIR` las escribe en CSV.

**Guardia anti-fuga:**

- Con una fecha de corte activa (`--as-of`, o cada fecha del backtest), ningún proveedor devuelve observaciones posteriores.
- Pedirlas lanza `FugaDeInformacion`.
- Cada cálculo del Motor queda en RC con su fecha de corte y la huella de los datos.

### 4.2 Universos (HT-11)

`config/universos/universo_<TIPO>.csv` contiene una fila por instrumento e instantánea. Las columnas comunes y las de filtro de cada tipo están en `10_Herramientas/README.md` (HT-11). Para que no haya sesgo de supervivencia ni de anticipación:

- `fecha_alta`, `fecha_baja` y `fecha_dato` hacen que el universo de cada fecha incluya **solo lo que cotizaba y lo que se sabía entonces**.
- Los instrumentos dados de baja después siguen en el universo de su fecha.
- Su rentabilidad posterior se valora al último precio disponible (tratamiento de bajas declarado).
- La columna `ambitos` (lista con «;») une el instrumento con las claves de ámbito.

**Para backtesting real:**

- Sustituya los universos por instantáneas históricas, como constituyentes de índices en cada fecha o listas de ETF por categoría con su fecha de alta.
- Sustituya las series por precios ajustados.

Los universos de ejemplo están marcados como ilustrativos; algunos ISIN de renta variable son reales, pero los datos no.

### 4.3 Archivos operativos y reconstrucción en una fecha

- F1–F6, F10, F11 (`F11_registro_seguimientos.jsonl`, propiedad de AG-B01), RC y HA se guardan en `--estado` (JSONL append-only). Cada entrada lleva `_fecha`, que es la fecha de corte en que se conoció.
- `leer(archivo, as_of)` solo devuelve lo conocible en esa fecha. Por eso un backtest sobre un estado con historia no ve lecciones, fichas de Biblioteca ni resultados futuros.
- `verificar_integridad()` recalcula la cadena de hash.
- Los puntos de control (`estado/puntos_control/CKP-*.json`) llevan una huella SHA-256: uno alterado no se reanuda.

## 5. Uso

### 5.1 Opciones globales

Van antes del subcomando:

```
--config YAML   --cliente mock|anthropic|replay   --replay ARCHIVO   --replay-modo grabar|reproducir
--datos CARPETA --estado DIR (./estado_bloque_b)   --salida DIR (./entregables)   --as-of AAAA-MM-DD   --boveda ARCHIVO
```

La salida de todos los subcomandos es JSON por stdout, integrable con n8n.

### 5.2 Subcomandos (Documento 0, 18.4)

```bash
# Petición (CT-B-01). Si la puerta de tiempo la detiene, devuelve estado EN_PAUSA con aut_id, opciones y recomendación
bloque-b --estado ./estado --salida ./ENT analizar --json ejemplos/peticiones/peticion_redes_bloque_a.json

# Decisión del Broker sobre la autorización pendiente (CT-B-05): reanuda desde el punto de control
bloque-b --estado ./estado autorizar --aut AUT-B-2026-0001 --opcion CONTINUAR [--minutos 70] \
         --decidido-por BROKER|USUARIO_VIA_BROKER [--motivo TEXTO]
#   --opcion CONTINUAR | VERSION_30_MIN | DIVIDIR_EN_FASES | HASTA_PV2 | CANCELAR

bloque-b --estado ./estado consulta "¿Por qué quedó fuera del top-5?" --contexto REC-B-2026-0001   # N0 (CT-B-03)
bloque-b --estado ./estado decision --json ejemplos/decision_ejemplo.json   # CT-B-04: decisiones, resultados, valoraciones
bloque-b --estado ./estado decision --json ejemplos/politica.json           # política de autorización automática (F10)
bloque-b --estado ./estado decision --json ejemplos/credencial_ejemplo.json # respuesta de CT-B-06: estado y alias, nunca la clave
#   V2.1: decision también admite {"forzar_continuacion": {pet_id, puerta PV1|PV2, motivo}} y
#         {"decision_seguimiento": {seg_id, ciclo_id, decision MANTENER|REACTIVAR_PETICION|PASAR_A_C|CANCELAR|SIN_DECISION}}
bloque-b --estado ./estado vigia                        # ronda del Vigía (fase F11) con la fecha de corte (en la V2.0 era «seguimiento»)

# V2.1 · seguimientos encargados (CT-B-29, archivo F11)
bloque-b --estado ./estado --salida ./ENT seguimiento alta --json ejemplos/seguimiento_ejemplo.json
bloque-b --estado ./estado seguimiento modificar --seg SEG-B-2026-0001 --json cambios.json
bloque-b --estado ./estado seguimiento pausar|reanudar|cancelar --seg SEG-B-2026-0001 [--motivo TEXTO]
bloque-b --estado ./estado --salida ./ENT seguimiento ciclo --seg SEG-B-2026-0001    # ciclo N1-SEG manual
bloque-b --estado ./estado --salida ./ENT seguimiento pendientes                     # ciclos vencidos (agenda HT-05)
bloque-b --estado ./estado seguimiento listar                                        # estado, próximos ciclos, recordatorios

# V2.1 · consultas del bloque al Broker y aportes (CT-B-28)
bloque-b --estado ./estado consulta-broker listar [--pet PET-B-…]
bloque-b --estado ./estado --salida ./ENT consulta-broker responder --cns CNS-B-… --respuesta TEXTO [--forzar-continuacion] [--motivo TEXTO]
bloque-b --estado ./estado consulta-broker aporte --json ejemplos/aporte_ejemplo.json
bloque-b --estado ./estado --salida ./ENT consulta-broker revisar                    # vence plazos y aplica supuestos
bloque-b --estado ./estado evaluar                      # resuelve PRG-B vencidos, métricas, lecciones, modelo de tiempos (F12)
bloque-b --estado ./estado estado [--pet PET-B-…] [--config]
bloque-b --estado ./estado verificar-enlaces [--max-fichas N] [--con-red [--aplicar]]
bloque-b --estado ./bt --salida ./bt_out backtest --peticion PET.json --desde 2023-01-01 --hasta 2024-12-31 \
         [--frecuencia mensual|semanal|diaria] [--solo-seleccion]
bloque-b generar-sinteticos --salida ./datos_sinteticos [--semilla N]
```

### 5.3 Diferencias con la sintaxis prevista en el Runbook

| Punto | Runbook | Este ejecutor |
|---|---|---|
| Subcomandos y opciones de los ejemplos | Los diez subcomandos de 18.4 | Iguales, con un cambio de significado: `seguimiento` gestiona desde la V2.1 los seguimientos encargados (CT-B-29) y la ronda del Vigía pasa a `vigia`. Se añade `consulta-broker` (CT-B-28). El Documento 0 V2.1 (18.4) aún no lista `vigia` ni `consulta-broker` |
| `verificar-enlaces` | Sin `--aplicar` no modifica nada | Además, por defecto **no usa la red**: solo lee y cuenta las fichas. Para el barrido real de HT-02 hace falta `--con-red`, y `--aplicar` solo surte efecto con `--con-red`. `--max-fichas N` limita el barrido |
| `backtest` | Sin opciones detalladas | `--peticion --desde --hasta [--frecuencia] [--solo-seleccion]` |
| Opciones adicionales | — | `--as-of` (simular una fecha), `--boveda` (archivo de bóveda simulada), `--semilla` (generar-sinteticos), `--replay`, `--replay-modo` |
| Condición `minutos_p80_min` de la política (POL-3) | Prevista | Admitida por HT-08, junto con `minutos_max` |

## 6. Qué hace una petición

| Tramo | Contenido |
|---|---|
| Tramo (capa) | Contenido |
|---|---|
| F0 (0) | Admisibilidad: activo individual, asesoramiento personal, tiempo real, datos sensibles, ámbito indeterminado o fuera de alcance; las instrucciones incrustadas se neutralizan (R12). Plan del Director (AG-B02) por capas, estrategia y pesos (HT-03), horizonte principal y secundarios (aplicabilidad por tipo de objeto y de activo, H1–H5), universos (HT-11), GC0 y estimación HT-08 por capa → **PT30 previa** |
| F1 (1) | Reconocimiento y mapa del mercado (AG-B03) y prueba de viabilidad del Director → **PV1** (HT-03 `evaluar_pv1`) |
| F2L (2) | Dimensiones **líderes** de la matriz en paralelo; desglose jerárquico de la cadena (AG-B03 `desglose_cadena`; PCB y AE con HT-03 y el Motor, fichas VC-DESG-001 y VC-BOT-001) |
| F3P (2) | Tesis provisional con autorrefutación, A y E provisionales → **PV2** (si solo falla E, consulta BLOQUEANTE `CONFIRMACION_SUPUESTO`) |
| F2R (3) | Resto de dimensiones y radar de emergentes de **AG-B24** (PEM con HT-03, registrado por el Motor MC-B07) |
| F3 (3) | Integración, componentes de A, E y C con PA1–8 y veredicto provisional |
| F5 (3) | Selección por tipo: cribado, asignación de eslabón, S con IC por bootstrap, diversidad 9.7, PC1–8, GC1–GC3, **mejores opciones por eslabón** (AG-B12 + Motor + HT-03) → **PV3** |
| F4 (4) | Proyecciones, escenarios (bootstrap por bloques) y pronósticos (AG-B13; con H5, hitos `HITO_H5`) |
| F6 (4) | Refutación del ámbito y de los finalistas, incluidas las opciones por eslabón (AG-B14) |
| F7 (4) | Síntesis, veredicto final, `mapa_cadena_valor`, consultas y supuestos, lista profesional, paquete para el Bloque C y plan de seguimiento |
| F8 (4) | Cierre de las consultas NO_BLOQUEANTES (supuesto aplicado); G3 sobre el paquete (HT-09); Auditor (AG-B22) si toca; AUTC-B |
| F9 (4) | Redacción de los seis entregables (AG-B17; entregable 6 en Markdown, .docx y JSON), HT-07 ≥ 70, G3 de fidelidad, AUTS-B |
| F10 (4) | Entrega en las carpetas ENT, registros F1–F6 (por capa), agenda del Vigía y biblioteca F6 (desglose y radar) |

**Puertas de viabilidad.** Una puerta no superada detiene el análisis: el Director compone el paquete de parada, el Redactor el informe de parada (G3 perfil PAR, auditoría por muestreo del 30 %), la REC-B queda `DETENIDO_EN_PUERTA` (veredicto DESCARTAR o VIGILAR) y la petición `DETENIDA_EN_PUERTA` con su punto de control. El Broker puede forzar la continuación en 7 días con `decision` (`forzar_continuacion`) o al responder una consulta; tras PV2 forzada, F4 es cualitativo y F5 indicativo. Si PV3 no se supera, se entrega sin selección completa (VIGILAR como máximo) con opciones «indicativas (PV3 no superada)» en el entregable 6.

**Consultas al Broker.** Los agentes proponen dudas en `consultas_propuestas`; el Director descarta las que tocan datos sensibles y las que resuelve la memoria, agrupa y decide el modo; el Coordinador las registra (CNS-B en F1, copia en `ENT/Consultas al Broker/`). Una BLOQUEANTE pausa la petición (`EN_PAUSA_CONSULTA`) en un punto de control; una NO_BLOQUEANTE sigue y, al llegar a F8 sin respuesta, aplica el supuesto, que figura en todos los entregables.

Tras cada tramo se guarda un punto de control. En ejecución se proyecta el consumo más el p80 restante, corregido por la desviación observada:

- Si un análisis estimado en ≤ 30 min va a superarlos, salta la **PT30**.
- Si ya autorizado va a superar lo autorizado + max(10 %, 5 min), salta la **PTA**.

En cualquiera de los dos casos se para en un punto seguro y se registra una AUT-B con:

- justificación (siempre, R20);
- lo hecho hasta ahora;
- estimación p50/p80 en minutos y UC;
- cinco opciones con su recomendación (V2.1: `HASTA_PV2` cuando PV2 está pendiente).

Entonces:

1. Se aplica la **política automática** de F10: la primera regla que cubre el caso, con tope efectivo min(tope, 480). Si autoriza, se registra `AUTORIZACION_AUTOMATICA_NOTIFICADA` y se sigue.
2. Si ninguna regla la cubre, la petición queda **EN_PAUSA** hasta `autorizar`. Hay un recordatorio a las 24 h y la autorización caduca a los 7 días.
3. Un **N3 pedido expresamente** (`nivel: N3` o `alto_impacto`) queda autorizado de entrada (240 min). Un límite del Broker (`limite.minutos`) prevalece.

Efecto de cada opción de `autorizar`:

| Opción | Efecto |
|---|---|
| CONTINUAR | Autoriza `--minutos` o, si no se indica, consumido + p80 restante |
| VERSION_30_MIN | Recorta según la propuesta de HT-08 (profundidad, top-N, tipos, refutación) y declara el alcance reducido (R23); el resultado es PARCIAL |
| DIVIDIR_EN_FASES | La fase 1 entrega ámbito y veredicto (como mucho VIGILAR, sin selección), con los entregables `_fase1`. Abre una AUT-B nueva para la fase 2 (selección, refutación, encargos), que se autoriza igual y entrega `_fase2` |
| HASTA_PV2 | Autoriza solo las capas 0–2; tras PV2 superada, nueva AUT-B para las capas 3–4 (si PV2 no se supera, informe de parada sin más consumo) |
| CANCELAR | Deja un resumen N0 en la salida; lo hecho queda registrado |

**Reloj de la puerta:**

- Con el cliente real, los minutos son de pared.
- Con `mock` y `replay`, cada tramo «dura» su p50 del modelo × `factor_simulado` × ruido lognormal con semilla. Así la puerta se prueba sin esperar: con el factor 1,0, el ejemplo N2 de tres tipos se detiene en PT30; con 0,3 no se detiene.

## 7. Entregables

Se escriben en `--salida`, con el nombre `AAAA-MM-DD_<clave>_<PET-B>[_faseN].<ext>`:

| Carpeta | Archivo |
|---|---|
| `Informes técnicos Broker/` | Informe técnico (Markdown, 16 secciones) |
| `Informes visuales Usuario/` | Informe visual (HTML autocontenido, accesible, adaptable; legibilidad Fernández-Huerta ≥ 70; sin identificadores de valores) |
| `Paquetes JSON/` | Paquete de análisis de mercado (valida contra el esquema del Anexo B de `06_Plantillas_entregables`) |
| `Memorandos ejecutivos/` | Memorando |
| `Anexos de datos/` | Anexo XLSX (HT-10) y sus CSV (V2.1: hojas `Eslabones`, `Opciones_eslabon`, `Emergentes`) |
| `Mapas por eslabón/` | Entregable 6 (V2.1): Markdown, copia .docx y JSON `mapa_cadena_valor` |
| `Informes de parada/` | Informe de parada (Markdown y JSON `informe_parada`) cuando el análisis se detiene en PV1 o PV2 |
| `Informes de seguimiento/` | Informe de cada ciclo de un seguimiento encargado (`…_SEG-B-id_cNN`, Markdown y JSON) |
| `Consultas al Broker/` | Copia de cada consulta saliente (CT-B-28) |

Además:

- `AAAA-MM-DD_entrega_<PET-B>.json` es la respuesta CT-B-02 resumida.
- `Alertas/` guarda las del Vigía.

Si G3 da BLOQUEADO, no se entrega: la petición queda BLOQUEADO_AUDITORIA con el motivo en HA. Las comprobaciones G3B que quedan manuales están en `10_Herramientas/README.md`.

## 8. Backtest

Para cada fecha de corte (fin de mes, viernes o día hábil), la fecha actual pasa a ser esa:

- HT-01 con guardia.
- F1–F6 filtrados por fecha.
- Universos en punto del tiempo.
- Búsqueda web desactivada.
- Prompts con la instrucción de no usar conocimiento posterior.

En cada fecha se ejecuta uno de estos modos:

- **Completo** (por defecto): la petición entera con los agentes. Si F10 no tiene política, se registra `POL-BT-1`, que autoriza automáticamente hasta 480 min, para que el backtest no se detenga.
- **`--solo-seleccion`**: solo la parte determinista, HT-11 → Motor (plan MIN) → HT-03. Sin agentes y sin coste de modelo; sirve para estudiar el ranking por sí solo.

Al final, la fecha avanza hasta el último dato disponible:

- se mide la rentabilidad posterior de cada candidato en el horizonte de la petición;
- se resuelven los PRG-B vencidos (solo en modo completo).

### 8.1 Archivos

| Archivo | Columnas / contenido |
|---|---|
| `rankings.csv` | `fecha_asof, pet_id, cand_id, tipo_activo, simbolo, nombre, S, en_top_n, rango, veredicto` (candidato); `veredicto_ambito, A, E, C` (solo modo completo); `fecha_fin_horizonte, evaluable, rent_fwd` (rentabilidad del instrumento hasta el fin del horizonte); `fecha_precio_final` (fecha del cierre utilizado) y `dias_desfase_precio_final` (días naturales desde ese cierre hasta el vencimiento: 0 si coinciden, ambos campos vacíos si no se pudo evaluar); `rent_fwd_universo` (media equiponderada del universo cribado: referencia del ranking, 9.11); `rent_fwd_referencia_ambito` (referencia del ámbito) |
| `series_ranking.csv` | Por fecha y tipo: `n_top_elegidos` (seleccionados originalmente), `n_top_evaluados` (con puntuación y rentabilidad, igual a `n_top`) y `n_top_sin_precios` (sin rentabilidad observable para el periodo). Se muestra el recuento aun cuando no pueda calcularse la comparación. Otras columnas: `fecha_fin_horizonte, n_universo, n_top, rent_top, rent_universo, exceso_vs_universo, rent_referencia_ambito, exceso_vs_referencia_ambito, ic_rango` (Spearman entre S y la rentabilidad posterior relativa al universo) |
| `pronosticos.csv` | PRG-B de ámbito y de ranking: `prg_id, pet_id, tipo, fecha_emision, fecha_resolucion, tipo_activo, banda, probabilidad_interna, estado, acierto, relativa, exceso, ic_rango, brier` |
| `consumo.csv` | Por ejecución: llamadas, tokens de entrada, salida, escritura y lectura de caché, búsquedas web y UC |
| `metricas.json` | Por tipo: `n_rankings`, exceso medio del top-N frente al universo y frente a la referencia del ámbito con IC 90 % (bootstrap), tasa de acierto, IC de rango medio con IC 90 %, `certificable` (n ≥ 30 y ambos IC por encima de 0). También la evaluación de pronósticos (celdas, Brier, BSS), los certificados, el consumo total y las advertencias |
| `entregables_ultima_fecha/` | Los seis entregables de la última fecha (modo completo) |

Para comparar la selección con el universo evaluable, `metricas.json` muestra dos medias por tipo de activo. Cada periodo pesa lo mismo. Los excesos son diferencias de rentabilidad expresadas como fracción (0,01 equivale a un punto porcentual).

| Periodos incluidos | Número de periodos | Exceso medio frente al universo |
|---|---|---|
| Todos los evaluables | `n_rankings` | `exceso_medio_top_n_vs_universo` |
| Evaluables con todos los elegidos evaluados | `n_rankings_seleccion_completa` | `exceso_medio_top_n_vs_universo_seleccion_completa` |

Si solo hay periodos parciales, la segunda fila tiene recuento 0 y media nula (`null`). Si un tipo carece de periodos evaluables, sus recuentos por fecha se consultan en `series_ranking.csv`. La certificación sigue su criterio de ventanas sin solapamiento.

**Comparación con el azar.** En ambos modos, cada fila de `series_ranking.csv` compara la selección original con grupos del mismo tamaño, fecha y tipo de activo. El sorteo toma los admitidos por HT-03 en aquella fecha, incluidas las alternativas. Conserva sus límites de subclúster, emisor de renta fija, índice replicado y las incompatibilidades por correlación aplicadas al seleccionar. Las rentabilidades se miden en el mismo horizonte, con igual peso por activo. Si falta la rentabilidad de algún admitido se informa `universo_incompleto`: quitarlo después de conocer la historia alteraría el sorteo.

Si las combinaciones caben en `evaluacion.bootstrap_replicas` (1.000 por defecto), se examinan todas. En otro caso se sortean ese número de grupos uniformemente, sin repetir activos dentro de un grupo. La semilla depende del ámbito, fecha, tipo y horizonte. Se descartan los grupos que incumplen las reglas. `azar_metodo`, `azar_estado`, `azar_grupos_examinados` y `azar_grupos_validos` indican cómo se obtuvo la comparación. `azar_pct_superado` es el porcentaje de grupos válidos que rindieron estrictamente menos que el robot. `azar_pct_empate` informa los empates por separado. Si no hay comparación, ambos quedan vacíos. En `metricas.json`, `azar_pct_superado_medio` da el mismo peso a cada periodo comparable y `n_periodos_azar` indica cuántos entran. Es una medida descriptiva, independiente de la certificación.

### 8.2 Recomendaciones para el backtest

- **Solapamiento.** Use una frecuencia coherente con el horizonte: con H4 (252 sesiones) y frecuencia mensual los rankings se solapan, y los IC por bootstrap simple son optimistas (`metricas.json` lo avisa). La certificación submuestrea las ventanas con exceso e IC de rango válidos, por orden de fecha de cierre, y admite ventanas consecutivas que comparten el precio de cierre. `certificacion_ranking` muestra el número retenido, el mínimo configurado y los dos intervalos del 90 % sobre esa muestra. Las medias e intervalos descriptivos siguen usando todas las fechas. El submuestreo evita reutilizar periodos de rentabilidad; puede persistir dependencia entre periodos distintos.
- **Fuga por conocimiento del modelo.** Con el cliente real, empiece después de `backtest.fecha_corte_modelo`. Si el periodo empieza antes, el resultado lleva una advertencia.
- **Coste.** Grabe con `--cliente replay --replay-modo grabar` y repita con `reproducir`.
- **Herramientas por separado.** Compare el modo completo con `--solo-seleccion` para separar lo que aportan los agentes (veredictos, refutación, rasgos) de lo que aporta la selección determinista.
- **Coste medido en simulación.** Con el cliente simulado, una petición N2 de tres tipos consume ≈ 25 UC y 22 llamadas, con ≈ 300 000 tokens de escritura de caché en la primera petición. Con el modelo real los tokens de salida serán mayores; mida con `consumo.csv`.

## 9. Credenciales (R10) y datos personales (R11)

- **Dónde vive la clave.** El Broker deposita la clave en la bóveda, en `BLOQUE_B_BOVEDA_<ALIAS>` o en un archivo con permisos 600 (`--boveda`).
- **Qué ven los agentes.** Los agentes y el Coordinador solo ven el alias y el estado: `PROVISTA_EN_BOVEDA`, `SIN_CREDENCIAL` o `DESACTIVADO_PAGO`. La respuesta de CT-B-06 (`decision --json`) solo admite `cred_id`, `estado`, `credencial_ref`, `caducidad` y `restricciones`.
- **Mensajes con claves.** Cualquier mensaje o entrada con aspecto de clave se rechaza íntegro, con una incidencia Crítica que no reproduce la clave. Lo mismo pasa con los datos personales: correo, IBAN, DNI/NIE o teléfono.
- **Prueba.** Una prueba barre todos los archivos del estado y de la salida en busca de una clave trampa.

## 10. Limitaciones y advertencias

- **Datos sintéticos y cliente simulado.** Las métricas de `ejemplos/backtest_simulado` no dicen nada de la capacidad del bloque. El simulado responde de forma determinista y sensible a la entrada, pero no razona. Componentes A/E/C, rasgos y objeciones son ruido con semilla.
- **Fuga por conocimiento del modelo.** El aviso en el prompt y la búsqueda desactivada no impiden que el modelo «sepa» lo que pasó después de la fecha. Solo un periodo posterior a su fecha de corte elimina esa fuga.
- **Universos de ejemplo.** Son pequeños (6–10 instrumentos por tipo). Con universos así, el IC de rango es muy ruidoso.
- **Referencias F7/F8/F9.** Se cargan las reales de `05_Archivos_operativos`. En backtest solo se ofrecen referencias publicadas hasta el año de la fecha de corte; la fecha exacta de publicación no siempre está en la ficha.
- **Datos fundamentales.** No hay proveedor histórico de fundamentales. Las dimensiones D8–D9 se apoyan en las métricas de precio del Motor y en los juicios de los agentes, declarados como tales.
- **V2.1 con el cliente simulado.** El desglose de la cadena, los indicadores de cuello, el radar de emergentes (nombres «simulados» o «ilustrativos») y las consultas son respuestas sintéticas: prueban el mecanismo (puertas, consultas, seguimientos, entregable 6), no la calidad del análisis. La asignación de eslabón usa la del Seleccionador o, si falta, una regla determinista.
- **Certificados.** Los de probabilidad no se emiten: falta implementar el IC 90 % del BSS, el ECE frente a su nulo y Holm. Quedan como «candidatos».
- **Madurez.** Hasta un backtest con datos reales, los componentes se declaran «implementados», no «validados» (R26).

## 11. Decisiones de diseño

- **Cálculo determinista.** Puntuaciones, veredicto, S, ranking, puertas, relevancia y tiempo los calculan HT-03, HT-08 y HT-09. Los agentes aportan componentes (múltiplos de 10, NA o NE), juicios y textos. Una respuesta no conforme se reintenta una vez y después degrada de forma declarada.
- **Segunda pasada de G3.** La pasada sobre los entregables (fidelidad) es determinista (HT-09 + HT-07). Si la legibilidad no llega a 70, el informe visual se rehace con textos de reserva sencillos.
- **Selección.** Se puntúa S una sola vez sobre todo el universo cribado (plan STD; EXT en N3). Los encargos C.x solo se emiten para el top-N.
- **Filtros.** Un filtro de invertibilidad no verificable por falta de dato excluye con `DATOS_INSUFICIENTES`. Un vehículo colectivo fuera de FON se excluye con «se asigna a FON» (2.6, regla 2).
- **Riesgo 1–5.** Escala por volatilidad anualizada del indicador: < 5 % → 1; < 10 % → 2; < 20 % → 3; < 35 % → 4; resto → 5. Se suma 1 si la caída máxima a un año supera el 40 %.
- **Reglas de tiempo y autorización.** Fase 1 de un análisis dividido: veredicto acotado a VIGILAR. Política del backtest POL-BT-1 hasta 480 min.
- **Datos sintéticos.** La semilla 14 se eligió para que el ejemplo muestre un INVERTIR_ESCALONADO con prioritarios.
- **Archivos.** JSONL append-only con cadena de hash, en lugar de una base de datos. La vista de una fecha se reconstruye filtrando por `_fecha`.

## 12. Estructura

```
11_Ejecutor/
  pyproject.toml, requirements.txt, README.md
  config/por_defecto.yaml, ambitos_ejemplo.yaml, universos/universo_<TIPO>.csv (12)
  bloque_b/
    cli.py            subcomandos
    entorno.py        configuración, almacén, reloj, HT-01, bóveda, cliente, prompts, Motor, universos
    orquestacion.py   Coordinador: admisión, capas 0–4 (F0–F10), puertas PV1–PV3, parada y continuación forzada, puerta de tiempo, autorizar, consultas al Broker
    sintesis.py       veredicto, paquete (Anexo B), mapa_cadena_valor, lista profesional, plan de seguimiento, G3 (F8)
    redaccion.py      seis entregables, informe de parada y de seguimiento, .docx del entregable 6, HT-07, G3 de fidelidad, entrega (F9–F10)
    motor.py          Motor de cálculo: métricas, S con IC, escenarios, sensibilidades, Spearman, Brier
    agentes.py, prompts.py, llm.py, mock_respuestas.py, contratos.py
    almacen.py        F1–F6, F10, F11, RC, HA
    referencias.py    índice de F7/F8/F9/FM
    seguimiento.py    seguimientos encargados (CT-B-29, F11, ciclos N1-SEG)
    vigia.py, evaluador.py, broker.py, backtest.py
    herramientas/     ht01_datos.py, boveda.py, referencia/ (copias de 10_Herramientas)
  tests/              118 pruebas (pytest)
  ejemplos/
    peticiones/       una petición por ámbito de ejemplo (la de redes viene del Bloque A) y `peticion_parada_pv1.json` (V2.1: parada en PV1)
    politica.json, decision_ejemplo.json, credencial_ejemplo.json, seguimiento_ejemplo.json, aporte_ejemplo.json
    salida_simulada/  analizar → PT30 → autorizar → seis entregables (con consulta NO_BLOQUEANTE y supuesto), Vigía, consulta, decisión, estado,
                      seguimiento (alta, ciclo, listado), consultas y aporte del Broker, parada en PV1 (respuestas/, ENT/, estado/)
    backtest_simulado/ solo_seleccion/ (24 fechas) y completo/ (3 fechas)
    generar_ejemplos.sh  regenera las dos carpetas anteriores
```

### Objeciones y ejemplos de contraste

Una objeción fuerte sobre la tesis que sigue abierta bloquea la recomendación de invertir. Para un candidato, limita su prioridad. Cada respuesta se aplica a los identificadores del encargo de ese agente. El seleccionador recibe las fichas de los candidatos objetados. Un cierre requiere un valor booleano verdadero y una respuesta; los matices débiles se registran como aceptados.

Si faltan precios de un símbolo, el backtest lo indica en las advertencias y evalúa los que tienen precios. Para ensayar la refutación, desde este directorio se puede ejecutar `PYTHONPATH=. python ejemplos/comparar_critico.py`. Los tres casos de lectura manual tienen su guía en [ejemplos/casos_critico/guia.md](ejemplos/casos_critico/guia.md).
