# PROMPT — Fase 5 · Modo sombra con API real (un bloque por sesión)

> La primera sesión donde se gasta dinero. Modelo: el más capaz. Requisito: Fase 4 verificada.
> El propietario debe tener ANTHROPIC_API_KEY exportada y haber aprobado el gasto de la sesión.

---

FASE 5 — Ejecutar el primer ciclo semanal REAL de un bloque en modo sombra (sin entrega al Broker): mide calidad analítica, consumo y coste real antes de confiar en nada.

ANTES de gastar un céntimo:
1. Verifica los identificadores de modelo de `11_Ejecutor/config/por_defecto.yaml` contra la página de modelos de Anthropic (context7 puede traer la doc; si hay duda, la lista oficial de la web manda). Los configs traen `claude-*-5-5` sin verificar por el propio paquete.
2. Rellena `precios_por_millon` (hoy null a propósito) con la tarifa vigente publicada. Anota fuente y fecha en docs/incidencias.md.
3. Presupuesto de la sesión acordado con el propietario por escrito: el ciclo completo medido en mock es ≈50 llamadas / ≈44 UC el primero y ≈14/7 los siguientes — espera salidas más largas con el modelo real.
4. `fecha_corte_modelo` actualizada según la doc del modelo elegido: un backtest anterior a esa fecha solo vale con su aviso de fuga.

Ejecución:
- Un ciclo semanal completo con `--cliente anthropic`, salida a un directorio aparte (p. ej. `sombra_<fecha>/`), y registro de consumo.csv y metricas.json.
- Guarda la grabación (`--replay-modo grabar` si está disponible) para poder reproducir la sesión sin coste.
- Nada se envía al Broker ni al Bloque B. Es modo sombra del plan de despliegue (Fase 3 del README del bloque).

Después: informe en `docs/sombra_<bloque>_<fecha>.md` con coste real, UC reales vs medidas, incidencias de la tubería, y una valoración HONESTA de la calidad analítica de las salidas (¿las oportunidades tienen sentido o son relleno?). El objetivo de esta fase es medir, no aprobar.

Restricciones fijas + commits `fase5:` (el material de sombra generado, si pesa, fuera del git — .gitignore).

Criterio de éxito: hay un documento con el coste real por ciclo y puedo reproducir la sesión con el replay sin gastar nada.
