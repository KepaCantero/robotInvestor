---
id: claude/2026-11-09_metodo-por-version
autor: claude
fecha: 2026-11-09
tipo: convencion
etiquetas: [metodo, versiones, cierre]
fuente: docs/flujo_de_trabajo.md; historial de commits de sistema_global/marco_comun_c
vigencia: vigente
---

El método de cada versión del marco común de C, que el flujo de cuatro fases generaliza:

1. Documento 0 de la versión antes del código (en Claude Docs: primero el esqueleto, después una sección por llamada).
2. Código y pruebas.
3. Revisor independiente en segundo plano, con scripts numerados `revNN`.
4. Cada hallazgo se corrige con una prueba de regresión.
5. Se vuelven a ejecutar los scripts del revisor.
6. Se actualizan el LEEME, la deuda técnica y el briefing.
7. ZIP en `/home/claude/out/`, probado desde una extracción limpia con `python3 -I`. Solo cuando el operador lo pide o para un kit.
8. Exportación del Documento 0.
9. Copia al repo, README y CLAUDE.md, `./tools/check_all.sh`, commit (autor `Claude <noreply@anthropic.com>`) y push a `develop`.
10. Mensaje final breve en español con el siguiente paso y el modelo y nivel recomendados.
