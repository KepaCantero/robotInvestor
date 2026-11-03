# Prompts del dashboard — robotInvestor

Kit de prompts para construir el **dashboard multi-agente** con estética de piso de
trading isométrico pixel-art (modo oscuro + LED dorado), a partir de la imagen de
referencia del propietario (diorama de trading floor: rótulos LED de departamentos,
puntos de estado verdes, relojes de sesiones de mercado, mini-gráficos).

Prompts listos para pegar en sesiones de **Claude Code** abiertas en la raíz del repo
(`CLAUDE.md` se auto-carga). Todo el trabajo de estos prompts vive dentro de
`dashboard/`: **no se toca el corpus de los bloques** en ninguna sesión de este kit.

## Orden de ejecución

| # | Archivo | Qué hace | Modelo recomendado |
|---|---|---|---|
| 1 | `01_DASHBOARD_V1.md` | v1 completa: HTML único autocontenido con datos mock realistas, todo el estilo LED dorado y panel de F6 (aprendizaje) | el más capaz |
| 2 | `02_REFINO_PIXEL_LED.md` | Refino visual: scanlines, suelo isométrico, avatares pixel-art, mesas 3D | Sonnet |
| 3 | `03_DATOS_REALES.md` | Cargar `senales.csv` / `pronosticos.csv` / `metricas.json` / `memoria_aprendizaje.json` reales con fallback a mock | el más capaz |

## Reglas fijas del kit (van dentro de cada prompt, no las quites)

- Un único `dashboard/index.html` autocontenido: sin build, sin frameworks, sin
  dependencias externas, funciona offline con doble clic (regla del proyecto:
  mock antes que API).
- UI completa en español; los datos simulados siempre etiquetados
  «MODO MOCK · DATOS SIMULADOS».
- Los agentes, bloques y campos mostrados son los reales del repo
  (`02_System_prompts/`, `senales.csv`, `metricas.json`): no se inventan roles ni
  métricas que no existan en los artefactos.
- Commits con prefijo `dashboard:`; avance registrado en `docs/AVANCE.md`.

## Referencia de estilo (tokens extraídos de la imagen)

| Elemento | Valor |
|---|---|
| Fondo | `#0b0d12` (azul-negro) |
| Paneles | `#14161d`, `#1a1d26` |
| Acento LED | `#f5c860` / `#e8b84a` con borde 1-2px + glow dorado |
| Rótulos LED | Panel negro, texto blanco MAYÚSCULAS, letter-spacing ≥ 0.12em |
| Positivo/activo | `#4ade80` con punto pulsante |
| Negativo/error | `#f87171` |
| Advertencia | `#e8b84a` |
| Secundario | `#8b93a7` |
| Tipografía | Números en mono; etiquetas mayúsculas tipo LED (pixel font solo rótulos) |
| Formas | Esquinas casi rectas (0-4px), sin glassmorphism, solo glows sobre negro |
