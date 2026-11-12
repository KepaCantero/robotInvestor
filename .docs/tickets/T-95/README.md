# T-95 · Prototipo de la consola N con datos de ejemplo

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `dashboard/consola_n/` (fuera de los bloques y del marco común) |
| Planifica · implementa · QA | claude · claude · sin asignar (el operador decide quién, 12-11-2026) |
| Aprobación del operador | aprobada el 2026-11-11: elige «Prototipo de la consola N» para el dashboard que le pide su equipo, con el stack que le pasan (React, TypeScript, Vite, Tailwind CSS, shadcn/ui, TanStack Query, Zustand, Lightweight Charts y AG Grid) |
| Deuda técnica | T-95 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Ver y usar las siete pantallas de la propuesta de N (`.docs/diseno/bloque_n/propuesta_claude.md`, §4 y §6) antes de cerrar su diseño, con el stack web que propone el equipo del operador. Es un prototipo: datos de ejemplo detrás de una API simulada, sin conexión con el robot.

## Alcance

- Entra:
  - las siete pantallas: inicio, decisiones, carteras, avisos, informes, salud y configuración;
  - lo que define a N: cifra principal frente a la cartera sombra con rango y «todavía no se sabe»; semáforo con cinco comprobaciones que sale en rojo si no se puede calcular; fricción asimétrica (reducir con un toque; aprobar con importe tecleado al céntimo, un solo uso y caducidad; aumentar con segundo factor y espera, nunca el día en que se tocó un límite); pantalla contra la venta de pánico sin bloquearla; avisos con acuse que no borra; explicación del Broker que solo se muestra si cada cifra de su texto está en la pantalla; kill-switch siempre a la vista; declaración de operaciones hechas fuera del robot;
  - una API simulada (puerto) que se pueda cambiar por la real sin tocar las pantallas;
  - una versión de un solo fichero para publicarla como página con enlace.
- No entra:
  - conexión con el robot, autenticación real, segundo factor real ni canal de avisos fuera del chat (T-01, T-41);
  - cambiar nada de los bloques, del marco común ni de la Constitución;
  - el kit `dashboard/prompts/` (otro panel, anterior al rediseño), que se conserva tal cual.

## Diseño

- Contratos: ninguno. Los tipos de la API simulada imitan lo que N leería (CT-G-08 de F, la cifra de I, el riesgo en euros de M, el rango de H), marcados como tipos del prototipo; cuando el diseño se cierre se generarán de los esquemas reales (regla 3).
- Estado persistido: ninguno. El estado de la sesión vive en memoria (Zustand); recargar vuelve a los datos de ejemplo.
- Números: todos los datos son de ejemplo y lo dice una franja fija en todas las pantallas. Los parámetros de fricción (espera para aumentar riesgo, caducidad de una aprobación) son [PROPUESTO], en un único fichero de configuración del prototipo.
- Cómo falla cerrado: si una consulta a la API falla, la pantalla lo dice y el semáforo pasa a rojo; nunca muestra cifras viejas como actuales. Una explicación con una cifra que no está en la pantalla no se muestra.
- Decisiones del operador usadas como [PROPUESTO]: las seis preguntas del §9 de la propuesta de N, con su valor propuesto.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Tomar los datos de ejemplo por reales | Decisiones sobre cifras inventadas | Franja «Prototipo · datos de ejemplo» fija en todas las pantallas; nombres de activos genéricos |
| El prototipo se convierte en la consola sin cerrar el diseño | Construir antes de decidir | Vive en `dashboard/`, no en un bloque; la consola de verdad tendrá su ticket cuando N esté cerrado |
| Peso de las dependencias | Repositorio pesado | `node_modules/` fuera del repositorio; solo el código y el `package-lock.json` |
| Fricción mal hecha | Aprobar un aumento de riesgo sin querer | Pruebas unitarias de la regla y de navegador del flujo completo |

## Criterios de aceptación (binarios)

1. CA-1: `npm run build` y `npm run typecheck` terminan sin errores.
2. CA-2: las siete pantallas se abren desde el menú y por su enlace (`#inicio`, `#decisiones`…), sin errores en la consola del navegador.
3. CA-3: la cifra principal dice «todavía no se sabe» cuando el rango incluye el cero (prueba unitaria y de navegador).
4. CA-4: una aprobación solo se habilita con el importe tecleado al céntimo, vale una vez y caduca; un aumento de riesgo pide además código y espera, y se bloquea el día en que se tocó un límite (unitarias y navegador).
5. CA-5: reducir riesgo y el kill-switch se hacen con un toque; vender a mano en caída una posición de largo plazo muestra antes la caída aceptada, la real, el coste de salir y el plan base, y deja vender con un toque más.
6. CA-6: una explicación del Broker con una cifra que no está en la pantalla no se muestra (unitaria).
7. CA-7: acusar un aviso no lo borra; queda en el historial.
8. CA-8: si la API simulada falla, el semáforo sale en rojo y la pantalla lo dice.
9. CA-9: se ve bien en el móvil (unos 400 px) y en tema claro y oscuro.
10. CA-10: no cambia ningún fichero de los bloques, del marco común ni de la Constitución, y el gate del repositorio sigue en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Veredicto de la cifra principal con rango a cada lado del cero | Unitaria | CA-3 |
| Reglas de fricción: importe exacto, un solo uso, caducidad, segundo factor, espera, día de límite | Unitaria | CA-4 |
| Comprobación de cifras de la explicación (formatos español: 1.234,56 €, 2,5 %) | Unitaria | CA-6 |
| Semáforo con una comprobación imposible de calcular | Unitaria | CA-8 |
| Recorrido de las siete pantallas y consola sin errores | Navegador (Playwright) | CA-2 |
| Aprobar una orden y aumentar riesgo de punta a punta | Navegador | CA-4 |
| Venta en caída del largo plazo y kill-switch | Navegador | CA-5 |
| Acusar un aviso | Navegador | CA-7 |
| API simulada en fallo | Navegador | CA-8 |
| Capturas a 400 px y 1.280 px, claro y oscuro | Navegador | CA-9 |
| `git status` de bloques, marco y Constitución; `./tools/check_all.sh` | Regresión | CA-10 |

## Scripts

`npm run dev`, `build`, `build:pagina` (un solo fichero), `typecheck`, `test` y `e2e`, descritos en `dashboard/consola_n/README.md`.

## Registro

- 2026-11-11 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-11 · EN CURSO · claude · plan escrito; implementa claude, QA astra cuando termine sus revisiones de diseño
- 2026-11-11 · EN QA · claude · prototipo listo: 29 pruebas unitarias y 12 de navegador en verde; publicado como página privada del operador. Espera la QA de Astra
