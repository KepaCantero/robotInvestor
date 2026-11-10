# T-87 · Correcciones A1–A8, agentes y procedencia de evidencia

Sobre `bc90534` se reprodujeron los ocho hallazgos anteriores con un SDK en memoria, un catálogo real y datos locales. La comparación negativa ejecutó las pruebas nuevas sobre una extracción del bloque anterior: **14 fallos**. En la rama corregida pasan esas **14 pruebas**. Durante el desarrollo pasaron además los 109 casos conjuntos de integración, selección T-53 y propuestas T-66. El resumen global del ticket recoge la validación del árbol final.

| ID | Comportamiento corregido | Evidencia |
| --- | --- | --- |
| A1 | La caché de resultados separa cliente, modelo, prompt completo, instrucciones, herramientas, esquema y límite de salida; la semilla separa los simulados. Replay siempre consulta o escribe su propia cinta. No se reutilizan las claves antiguas de resultados. | Una llamada real simulada después de una mock sí llega al SDK. Cambiar el prompt o límite invalida el acierto; la repetición idéntica sí acierta. |
| A2 | Se comprueban encargo, respuesta, contexto y bloques del SDK antes de reenvío o persistencia. Un turno sensible queda sin texto con el uso incurrido y un motivo genérico en HA y en replay. | Marcador ficticio en JSON, texto libre, JSON incompleto, y valor truncado antes de la comilla de cierre. Un solo intento, sin marcador en cinta, HA ni caché. No se emplearon secretos reales. |
| A3 | Replay conserva stop_reason, truncada y rechazo; la lectura de cintas antiguas deriva los dos indicadores del motivo de parada. Las cintas nuevas distinguen el esquema y límite de salida. | Truncamiento en grabación y reproducción, cinta del formato anterior, y petición de otra longitud contra una cinta nueva. |
| A4 | Un rechazo o una pausa que agota sus continuaciones cierran el intento como PARCIAL aunque el texto fuera un JSON válido. Los turnos truncados pueden seguir la política de reparación. | Casos pause_turn, refusal y max_tokens junto al control end_turn. |
| A5 | El documentador/Buscador solo puede devolver las referencias documentales ofrecidas en backtest. La misma regla alcanza las afirmaciones del analista antes de la refutación y al escribir F2. Para una ficha que solo acredita año, se usa el 31 de diciembre como primera fecha segura y se deja nula la fecha exacta de publicación. Los canales sin fecha siguen siendo catálogo. | Se rechaza una ficha real de 2023 para junio de 2000. Una ficha solo fechada en 2025 no se ofrece el 30 de diciembre y sí el 31. |
| A6 | El límite máximo de ampliación autorizada incluye el margen automático y las autorizaciones anteriores; la comprobación y el ajuste de la bolsa comparten bloqueo. | Con base de 10 UC, ya consumidas 12,5, las 5 adicionales se deniegan y 2,5 se conceden. Un cobro real puede exceder la estimación; no se ha introducido un tope monetario ni tarifas. |
| A7 | Un error final del SDK produce PARCIAL, deja una incidencia saneada, conserva el uso conocido de continuaciones anteriores y permite cerrar el RUN. El texto de la excepción no se remite al modelo. | Fallo persistente de transporte con dos clases: ciclo PARCIAL, registro F5 e incidencia HA. |
| A8 | Los identificadores CALC se comprueban contra un servicio aceptado de RC, el corte y la tabla del símbolo. Una fuente HT-01 debe coincidir con la opción y su observación efectiva al corte. Al analista se le suministra la observación normalizada para que pueda citarla; una frase libre sin contraste conserva a lo sumo estado PENDIENTE y no sirve para PS1 ni por sí sola para cerrar una objeción. | Cálculo inexistente, símbolo ajeno, referencia no ofrecida y texto inventado junto a un símbolo auténtico. Control positivo con observación contrastada. |

**Reproducción.** Desde la raíz, con las dependencias del proyecto:

```sh
python -B -m pytest -p no:cacheprovider -q bloque_a/11_Ejecutor/tests/test_t87_agentes.py
```

**Límites de la revisión.** No se observa el coste facturado de una solicitud que falla sin devolver usage; sí los tokens que el SDK alcanzó a devolver. Las cintas históricas no guardaban el límite de generación ni el esquema y solo pueden reproducirse bajo su identidad antigua. Las nuevas protecciones no limpian archivos antiguos ni prueban la verdad semántica de una afirmación bibliográfica. Reducir perfiles o evaluar la calidad de un modelo real corresponde a las decisiones de T-66 y T-57.
