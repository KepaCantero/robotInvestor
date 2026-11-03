# PROMPT — Fase 6 · Cadena A→B y conexión a robotTrading

> La única fase que toca la frontera entre bloques y sale del repo. Modelo: el más capaz.
> Requisito: Fase 5 verificada en bloque_a (y en forex si se quiere la cadena completa).

---

FASE 6 — Dos piezas, en este orden:

1. Cadena de encargos A→B (dentro de este repo):
   - El paquete JSON de oportunidades del bloque_a trae `paquete_para_bloque_B`; el bloque_b consume encargos. Escribe el conector que toma un paquete real (o de ejemplo) de A y lo registra como entrada en B, respetando los esquemas de AMBOS lados (Fase 3) — sin transformaciones inventadas: si los campos no casan, es una incidencia, no un adaptador creativo.
   - Pasa por una confirmación humana antes de que B arranque un análisis (regla de producto del propietario: nada autónomo sin supervisión, preview→confirm).
2. Conexión al backtester de robotTrading (fuera de este repo, en ~/robotTrading):
   - El ejecutor A emite `senales.csv`, `pronosticos.csv`, `metricas.json` (interfaz diseñada para el ingeniero). Construye en robotTrading el lector que consuma esa salida y la evalúe con el motor determinista existente.
   - Trabaja en ~/robotTrading respetando SUS reglas (su CLAUDE.md/AGENTS.md, su cola en docs/plans/ORDEN_PLANES.md si sigue vigente, sus goldens de conformance). Nada de commits allí sin su protocolo.

Kit de contexto: READMEs de ambos ejecutores, esquemas de encargo de `06_Plantillas_entregables` de A y el mecanismo de entrada de encargos de B (su Documento 0 §frontera con A), y en robotTrading el motor canónico + la suite de conformance.

Entregables: conector A→B con tests de extremo a extremo en mock; lector en robotTrading con sus tests según SU convención; un documento `docs/cadena_A_B.md` con el diagrama real de lo conectado (no el deseado).

Restricciones fijas + commits `fase6:` aquí y SU prefijo en robotTrading.

Criterio de éxito: lanzo un paquete de ejemplo de A y B produce su análisis desde el encargo, todo en mock y con confirmación humana en medio; y robotTrading lee un `senales.csv` generado aquí y lo evalúa sin errores.
