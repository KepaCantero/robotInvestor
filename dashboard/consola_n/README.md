# Consola N · prototipo

Prototipo de la consola del operador (Bloque N) del Robot Investor: las siete pantallas de la propuesta de diseño (`.docs/diseno/bloque_n/propuesta_claude.md`) con **datos de ejemplo**. No está conectado al robot; ninguna cifra es de nadie ni es una recomendación. Ticket: `.docs/tickets/T-95/`.

## Qué enseña

| Pantalla | Pregunta | Qué se puede probar |
| --- | --- | --- |
| Inicio | ¿Va todo bien y qué espera de mí? | Cifra principal frente a la cartera sombra con su rango («todavía no se sabe» si cruza el cero), cinco comprobaciones, decisiones por vencimiento, largo plazo sin cifra diaria |
| Decisiones | ¿Qué apruebo? | Cifras de F, riesgo en euros de M, plan base; importe tecleado al céntimo, un solo uso, caducidad; aumentar con código y espera; bloqueo el día en que se tocó un límite; explicación del Broker que se retira si cita una cifra que no está en pantalla |
| Carteras | ¿Qué tengo? | Tabla de posiciones (AG Grid), gráfico con entrada, stop y rango de H (Lightweight Charts), vender con un toque, pantalla contra la venta de pánico en el largo plazo, declarar una operación hecha fuera del robot |
| Avisos | ¿Qué no he visto? | Prioridades y canal de cada una; acusar no borra |
| Informes | ¿Aporta el robot? | Embudo de abstención, robot frente a sombra, atribución por etapa con rangos, intervenciones del operador, revisión anual |
| Salud | ¿Funciona el robot? | Latido, presupuesto de IA, estado por bloque, sellos de datos; botón para simular que la API no responde |
| Configuración | ¿Cambio algo? | Bajar el riesgo se aplica; subirlo se convierte en una decisión con fricción |

El kill-switch está siempre arriba: activarlo es un toque; reactivar el robot pide código.

## Stack

React 18, TypeScript, Vite 5, Tailwind CSS 3, shadcn/ui (componentes copiados en `src/componentes/ui/`, con Radix), TanStack Query 5 (datos de la API), Zustand 5 (estado de la interfaz), Lightweight Charts 4 y AG Grid Community 32.

## Estructura

| Carpeta | Qué hay |
| --- | --- |
| `src/api/puerto.ts` | Lo único que las pantallas saben de la API. La consola real cambiará `simulada.ts` por el Orquestador sin tocar las pantallas |
| `src/api/simulada.ts`, `datos_ejemplo.ts` | API en memoria con datos de ejemplo. Vuelve a comprobar todo lo que comprueba la pantalla: la consola informa, no protege |
| `src/logica/` | Reglas puras y probadas: veredicto del rango, fricción asimétrica, comprobación de cifras, semáforo y formato español |
| `src/config/prototipo.ts` | Parámetros del prototipo, todos [PROPUESTO] |
| `src/pantallas/` | Las siete pantallas |
| `pruebas/unit/`, `pruebas/e2e/` | Vitest (29 pruebas) y Playwright (12) |

## Comandos

```bash
cd dashboard/consola_n
npm install
npm run dev            # http://localhost:5173
npm run typecheck
npm test               # unitarias
npm run build && npm run e2e   # navegador (usa vite preview en el puerto 4173)
npm run build:pagina   # un solo fichero en dist-pagina/consola_n.html, para publicarlo como página
```

## Lo que falta para la consola de verdad

Cerrar el diseño de N con la revisión de Astra; tipos generados de los esquemas reales en lugar de `src/api/tipos.ts`; la API del Orquestador; autenticación con segundo factor real (T-01) y canal de avisos fuera del chat (T-41); servirla desde el propio robot en una red privada (SC-7).

## Herramientas para quien desarrolle en su ordenador

Para trabajar en esta carpeta con Claude Code en local, estos servidores MCP ayudan: shadcn (añadir componentes), Playwright (probar en el navegador), Context7 (documentación al día de las librerías) y Figma (si las pantallas se diseñan allí). No hacen falta para usar el prototipo.
