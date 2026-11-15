# T-129 · Análisis técnico

- No cambia código de producción: el cliente real (`llm.AnthropicClient`) ya envía solo `model`, `max_tokens`, `system`, `messages`, `metadata`, `tools` y, si se activa, `output_config`; las pruebas lo fijan.
- `max_tokens` máximo de la configuración: 12 000, sin streaming; por debajo del umbral a partir del cual el SDK exige streaming.
- Decisiones `[PROPUESTO]` en INC-T129-01: tarifa aparte; sin respaldo automático a otro modelo ante un rechazo (`fallbacks`); sin fijar el esfuerzo (`effort`) hasta el banco real.
- La cota superior supone toda la salida hasta `max_tokens`; en un modelo real la salida suele quedar lejos, así que la cifra real debería estar entre las dos.
- Precios de la caché: la escritura es la de 1 hora porque `llm.cache_ttl` es «1h»; entre ciclos semanales la caché caduca, así que cada ciclo paga su escritura.
