# Relevo para un chat nuevo · estado al 11-11-2026

De: Claude. Para cualquier chat nuevo de Claude (del operador o de un compañero) y para quien llegue al proyecto. Resume el estado del Robot Investor a 11-11-2026, dónde está cada cosa y cómo se trabaja. Lo detallado está en los ficheros que se citan: **léelos solo cuando la tarea los pida** (regla 1 de `CLAUDE.md`).

## 1. Cómo arrancar

1. `git pull origin develop`. Al escribir esto, el último commit es `d5c3531` o uno posterior.
2. Lee, en este orden: `CLAUDE.md`, `.docs/README.md`, `.docs/memoria/LEEME.md` y el `INDICE.md` de `.docs/memoria/compartida/` y de tu carpeta (`claude/`).
3. Lee este relevo entero y la historia del proyecto (`.docs/knowledge/05_historia-del-proyecto.md`): todo lo hecho del 3 al 11-11-2026, con el marco común de C versión a versión y el trabajo sobre A y B. Si la tarea es de diseño, lee también `.docs/diseno/README.md` y `.docs/diseno/decisiones_operador.md`.
4. **Nada se pierde:** si un fichero se modificó o se borró, su versión anterior sigue en el historial de git (`git log --follow -- <ruta>` y `git show <commit>:<ruta>`). Los mensajes de commit cuentan qué se hizo en cada paso.
5. Pregunta al operador qué quiere hacer hoy. No retomes nada por tu cuenta: lo pendiente está en el §6.

## 2. El proyecto en cinco líneas

El Robot Investor es un sistema de inversión personal por bloques. A busca oportunidades, B elige activos, C analiza a fondo y D compara. Después, E dimensiona, F controla el riesgo (código, sin IA), G ejecuta y concilia, H vigila la salida, I evalúa frente a una cartera sombra pasiva, J aprende sin engañarse, K da los datos, M mira el riesgo de cartera y N es la consola del operador. Por encima están el Broker Personal (el asesor que habla con el operador) y los servicios comunes SC-1 a SC-11. La brújula (P17) es batir a la cartera sombra pasiva, en neto y por euro. Más en `.docs/knowledge/01_que-es-el-robot-investor.md`.

## 3. Quién hace qué

| Quién | Papel |
| --- | --- |
| El operador | Decide. Se le habla en español y de **usted**. Ratifica la Constitución y cada decisión marcada `[PROPUESTO]`. |
| Claude | Propone diseños, planifica e implementa. Escribe su memoria solo en `.docs/memoria/claude/` y `compartida/`. |
| Astra (OpenAI) | Revisa de forma independiente y hace la QA de lo que implementa Claude (y al revés). Entra por `AGENTS.md`. |
| Compañeros del operador | Cada uno tiene su propia copia con su propio dinero (D-47). Por eso en el repositorio no hay nada personal. |

## 4. Reglas que no se rompen

- **El repositorio es público:** sin secretos (solo en `.env`, cargado por `.docs/scripts/common.sh`) y sin datos personales ni financieros de nadie. El nombre del operador no se escribe en ficheros del repositorio.
- **Nunca se borra nada de `.docs/`:** lo viejo se marca.
- **`bloque_b/` está congelado.** Tampoco se toca el código de ningún bloque, del marco común (`sistema_global/marco_comun_c/`) ni de la Constitución sin autorización expresa del operador.
- **No autorizados aún:** T-14, T-30 y las dos fechas de K, aunque se propusieron. Construir bloques nuevos tampoco, hasta cerrar su diseño.
- **Las decisiones del operador** se marcan `[PROPUESTO]` hasta que las ratifica, y van a la deuda técnica.
- **Flujo de cuatro fases** (planificar, implementar, probar y QA), con la QA hecha por el agente que no implementó: `.docs/knowledge/02_flujo-de-trabajo.md` y las skills `ri-*`.
- **Gate del repositorio:** `./tools/check_all.sh` en verde (12/12) antes de cerrar nada.
- Nada de lo que produce el proyecto es asesoramiento legal, fiscal ni de inversión.

## 5. Estado al 11-11-2026

### Constitución y decisiones

- **Constitución V0.6** ratificada (`sistema_global/constitucion/Constitucion_Global.md`).
- **Enmienda 4** propuesta, pendiente de la revisión de Astra: veinte puntos (`.docs/diseno/enmienda_4/`).
- **Enmienda 5, parte 1:** borrador que redacta en la Constitución las ocho decisiones de la tanda 1 (nueve cambios, D-48 a D-56, numeración provisional), en `.docs/diseno/enmienda_5/`. La parte 2 (veintiocho cambios, 52 a 79, y D-57 a D-84, todo [PROPUESTO]) está en borrador desde el 11-11-2026 (`propuesta_parte2_claude.md`), con una casilla vacía por cambio para lo que digan las revisiones de Astra.
- **Tanda 1 de decisiones aceptada** el 11-11-2026 (`.docs/diseno/decisiones_operador.md`):
  1. pauta común de A, B y C con banco de medida;
  2. Contradictor de otro proveedor de IA;
  3. largo plazo en paralelo a la Fase 1, con los perfiles de fondos fuera del tope de bloques;
  4. asimetría de F;
  5. registro de experimentos desde la Fase 1;
  6. informes con rangos;
  7. territorio fiscal común (falta que el operador designe al asesor);
  8. dos intermediarios (falta que el operador elija las entidades).
- **Tandas 2 a 5 pendientes** (parámetros, antes de la Fase 2, antes del dinero real y Fase 4). Están en `.docs/diseno/coherencia/propuesta_claude.md`, §8. Se deciden en la sesión única T-57, cada una con su valor por defecto.

### Código

| Pieza | Estado |
| --- | --- |
| `bloque_a/` (V5.1) | Corregido y auditado (T-53, T-66, T-92); T-93 implementado por Claude, QA sin asignar. 476 pruebas. Pendientes técnicos: T-88 y T-91 |
| `bloque_a_forex/` | Fuera del Robot Investor (D-20). 68 pruebas |
| `bloque_b/` (V2.1) | Congelado. Evaluado en T-68 y con un rediseño propuesto, ambos a la espera de Astra. 176 pruebas |
| `sistema_global/marco_comun_c/` (V0.74) | Código de referencia de la Fase 1, 62 suites, todo en simulado. La V0.74 (T-97, EN QA) alinea los valores por defecto con la tanda 2 |
| `.docs/scripts/banco_medida.py` (T-94) | Banco de medida: A frente a azar y momento, con prerregistro, rangos y coste. 10 pruebas. EN QA |
| `dashboard/consola_n/` (T-95) | Prototipo navegable de la consola N con datos de ejemplo (React, TypeScript, Vite, Tailwind, shadcn/ui, TanStack Query, Zustand, Lightweight Charts y AG Grid). 29 pruebas unitarias y 12 de navegador. EN QA. Su README explica cómo arrancarlo |
| `tools/requisitos_entorno.txt` y `.docs/scripts/preparar_entorno.sh` (T-96) | Versiones fijadas del entorno y script que crea el `.venv` con ellas. EN QA |
| `dashboard/prompts/` | Kit de un panel anterior al rediseño. Se conserva; no es la consola N |

### Diseño: 23 propuestas a la espera de Astra

Todas en `.docs/diseno/<carpeta>/propuesta_claude.md`, con su `encargo_revision_astra.md`. El índice es `.docs/diseno/README.md` y el orden de revisión, el §0 bis de `2026-11-10_pendientes_para_astra.md` (en esta carpeta):

1. A
2. B (con `.docs/tickets/T-68/`)
3. C
4. D
5. E
6. F
7. G
8. H
9. I
10. J
11. K
12. M
13. N
14. Broker Personal
15. SC-9 (fiscalidad)
16. SC-3 (Motor de cálculo)
17. SC-10 (intermediario)
18. SC-7 (seguridad)
19. Entrada del dinero existente
20. Enmienda 4
21. Pasada de coherencia
22. Enmienda 5, parte 1
23. Enmienda 5, parte 2

La pasada de coherencia reúne las doce incoherencias halladas, los servicios pequeños, las fases, los dieciséis contratos nuevos y las tandas de decisiones.

### Plantillas del operador

En blanco en `.docs/plantillas_operador/`: ficha de restricciones, inventario del patrimonio, preguntas al asesor fiscal y carta de instrucciones. Se rellenan **fuera del repositorio**.

### Cola de Astra

**Desde el 12-11-2026 solo el operador decide qué tareas hace Astra** («A partir de ahora yo te diré qué tareas quiero que realice Astra»). La cola con su estado está en `.docs/tickets/_relevo/cola_astra.md` y se consulta con `python3 .docs/scripts/cola_astra.py`; el operador abre cada sesión de Astra con el mensaje de `.docs/tickets/_relevo/arranque_astra.md`.

- **Le quedan las 23 revisiones de diseño** (C-01 a C-23), en el orden natural de los bloques.
- **Retiradas por el operador** el 12-11-2026, sin borrarse (estado `RETIRADA`): todas las QA de tickets (T-83, T-84, T-93, T-94, T-95, T-96, T-97 y T-99) y las implementaciones (T-75, T-76, T-91 y T-88). Quién hace esas QA, y si se hacen, lo decide el operador.
- Claude no añade tareas a la cola sin que el operador lo pida.

## 6. Lo siguiente (a elegir con el operador)

1. **Esperar las revisiones de Astra.** Llevar al operador cada discrepancia con una decisión ya tomada.
2. **Enmienda 5, parte 2:** borrador hecho; falta rellenar sus casillas con las revisiones de Astra. Después, la ratificación punto por punto y la Constitución V0.7, aplicada en un ticket con el gate.
3. **Los contratos nuevos** (pasada de coherencia, §6), antes que el código. Luego, la construcción de la Fase 1, con el banco de medida y datos reales de K (T-86) como primer paso.
4. **Mientras tanto, sin tocar código:**
   - la tanda 2 está contestada (11-11-2026): las decisiones de arquitectura E1 a E8 están en `.docs/diseno/decisiones_operador.md`; los parámetros son perfil del operador y no están en el repositorio. Quedan seis discrepancias entre los diseños y el marco común (cuestionario, §8), que se corrigen en un ticket con autorización;
   - que el operador rellene sus plantillas (la ficha antes de la cuenta de demostración);
   - compartir el prototipo de N con su equipo para recoger opiniones.

## 7. Cómo trabaja Claude aquí

- **Propuesta de diseño:**
  1. documento en Claude Docs del operador (esqueleto, abrirlo y una sección por llamada);
  2. copia en `.docs/diseno/<carpeta>/propuesta_claude.md`, sin el nombre del operador;
  3. `encargo_revision_astra.md`;
  4. fila en `.docs/diseno/README.md`;
  5. puesto en la cola del relevo;
  6. diario;
  7. commit.
- **Tarea de código:**
  1. fila T-NN en la deuda técnica (`sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`);
  2. `.docs/scripts/nuevo_ticket.sh T-NN "título" pieza`;
  3. plan con criterios binarios;
  4. implementar;
  5. `pruebas.md`;
  6. estado EN QA y aviso a Astra en el relevo.
- **Diario:** una entrada por tema y día, arriba del todo de `.docs/diario/AAAA-MM.md`, con el formato de `.docs/README.md`.
- **Commit:** `.docs/scripts/commit_limpio.sh "mensaje" fichero1 fichero2 …`, solo con ficheros (no carpetas). Las líneas finales del mensaje van en la variable `GIT_TRAILERS`. Tarda entre 15 y 20 minutos porque pasa el gate completo en una copia limpia: se lanza en segundo plano y se espera a que termine. Sube a `develop`.
- **Mensajes en español** con prefijo de área: `docs:`, `infra:`, `dashboard:`, `motor:`…
- Los parámetros nuevos son `[PROPUESTO]` y salen de configuración, nunca a mano.

## 8. Lecciones prácticas

- Desde la sesión en la nube solo se llega a los registros de paquetes y a GitHub. Para datos de la web se usa la búsqueda web; el registro web de shadcn no responde, así que sus componentes se escriben a mano en `src/componentes/ui/`.
- El prototipo de N se publica como una página de un solo fichero: `npm run build:pagina` en `dashboard/consola_n/`.
- En las pruebas de navegador, las fuentes de Google no cargan sin red. Se ignora solo ese error.
- En un clon nuevo, crea el entorno con `.docs/scripts/preparar_entorno.sh` (T-96): sin las versiones fijadas, `arch` 9.0.0 hace fallar las cuotas de mypy.
- `commit_limpio.sh` falla si se le pasa una carpeta. Hay que listar los ficheros, por ejemplo con `git ls-files -o --exclude-standard <carpeta>`.
- Cifras con datos sintéticos y cliente simulado solo prueban la tubería; el informe del banco lo avisa en su primera línea.
