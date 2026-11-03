# PROMPT 1 — Dashboard v1: piso de trading multi-agente

> Primera sesión del kit. Entrega `dashboard/index.html` completo con datos mock.
> No toques nada fuera de `dashboard/`. Commit con prefijo `dashboard:` y línea en
> `docs/AVANCE.md`.

---

Actúa como diseñador front-end senior especializado en dashboards financieros con
estética retro-terminal / pixel-art. Construye un dashboard web de una sola página
para un sistema multi-agente de inversión llamado "robotInvestor", con la estética
exacta de un piso de trading isométrico nocturno en pixel-art: modo oscuro con
acentos dorados tipo LED. Todo el trabajo queda en `dashboard/index.html`.

ESTILO VISUAL (obligatorio):
- Fondo general #0b0d12; paneles #14161d/#1a1d26 con esquinas casi rectas
  (border-radius 0-4px, look pixel).
- Componente firma "rótulo LED": panel negro, borde dorado #f5c860 de 1-2px con
  box-shadow dorado (glow), texto blanco en MAYÚSCULAS con letter-spacing >= 0.12em.
- Estados: verde #4ade80 (activo/positivo, con punto pulsante), rojo #f87171
  (error/negativo), ámbar #e8b84a (advertencia/en espera), gris #8b93a7 (secundario).
- Números en fuente monoespaciada; etiquetas en mayúsculas tipo LED. Aceptable una
  fuente pixel/retro (p. ej. "Silkscreen" o "VT323") solo para rótulos, con fallback.
- Toque isométrico sutil: rejilla de suelo en perspectiva como fondo del hero y/o
  marcos de tarjeta con bisel 3D ligero. Nada de glassmorphism ni sombras difusas
  grises: solo glows dorados/verdes sobre negro.

ARQUITECTURA QUE REPRESENTA (datos reales del proyecto):
El sistema tiene 3 bloques que colaboran en cadena:
1) "BLOQUE A — BUSCADOR DE OPORTUNIDADES" (V5.1): 12 analistas por tipo de activo
   (Renta Variable, Renta Fija, Divisas, Cripto, Materias Primas, Inmobiliario,
   Alternativos, Derivados, Fondos, Monetarios, Índices, Tipos de Interés) +
   agentes horizontales (Analizador de Tendencias, Motor de Cálculo, MC-01..10,
   Auditor, Curador de Evidencia, Redactor).
2) "BLOQUE A FOREX — MESA DE DIVISAS" (V1.1): 8 analistas de segmento (G10 núcleo,
   G10 materias primas y escandinavas, Emergentes Asia/EMEA/LatAm, Bancos
   Centrales, Estrategias y Cestas, Posicionamiento y Flujos, Prospectiva).
3) "BLOQUE B — SELECCIÓN DE ACTIVOS" (V2.1): Director del Análisis de Mercado,
   12 analistas de dimensión (Demanda, Estructura Sectorial, Finanzas y Valoración,
   Macro y Ciclo, Oferta y Costes, Regulación, Tecnología, Flujos y Sentimiento,
   Prospectiva, Sostenibilidad, Emergentes), Motor de Cálculo y Seleccionador
   de Activos.
Flujo: A y A-Forex detectan oportunidades y emiten "encargos" → B estudia el
mercado y selecciona activos → salida para un backtester externo.

LAYOUT DEL DASHBOARD:
1. Header: rótulo LED principal "ROBOTINVESTOR · PISO DE TRADING MULTI-AGENTE",
   reloj en vivo (Europe/Madrid), indicador de ciclo (SEMANAL · LUN 07:00) y
   semáforo de modo (MOCK vs API REAL).
2. Barra de sesiones de mercado (relevante para la mesa Forex): Sídney, Tokio,
   Londres, Nueva York con estado abierto/cerrado calculado por hora real y
   punto verde/rojo pulsante.
3. Fila de KPIs globales (monospace, verde/rojo según signo): señales vigentes,
   encargos emitidos A→B, pronósticos resueltos, tasa de acierto global con IC90,
   horizonte principal dominante.
4. Tres tarjetas-departamento grandes (una por bloque), cada una con:
   rótulo LED con su nombre, versión del bloque, estado (● OPERANDO / EN ESPERA /
   ERROR), agentes activos/total, mini-gráfico de línea con la actividad por run,
   y 3-4 métricas propias:
   - Bloque A: señales nuevas del último run, top oportunidad (nombre, dirección
     LARGO/CORTO, prob_interna), distribución por tipo de activo.
   - A-Forex: pares/ámbitos bajo seguimiento, oportunidad cambiaria top.
   - Bloque B: encargos recibidos, activos seleccionados, última decisión del
     Seleccionador.
5. Sección "CADENA DE ENCARGOS" (pipeline visual): A → B con tarjetas pequeñas de
   encargos en tránsito (opp_id, ámbito, siguiente_paso, vigencia) animadas
   moviéndose de izquierda a derecha entre mesas.
6. "MONITOREO EN VIVO": feed tipo terminal (fondo negro, texto verde) con eventos
   de agentes: "[14:02] RUN-2026-0013 · Analista de Criptoactivos → señal nueva
   OPP-2026-0041 (CRI|H2, prob 0.65, ENVIAR_A_BLOQUE_B)".
7. "CONTROL DE RIESGO" (panel del Auditor/Evaluador): riesgo_1a5 de las señales
   vigentes, Brier/BSS por clase|horizonte (p. ej. CRI|H2), advertencias del
   último ciclo (texto en ámbar).
8. "PANEL DE APRENDIZAJE" (F6, la memoria del sistema): lecciones nuevas,
   revocadas y caducadas del último ciclo (LEC- con ámbito clase|horizonte y
   fuerza), top lecciones vigentes por ámbito, drift de calibración por celda
   (Brier/BSS con IC90) y certificados CERT- emitidos con su estado. Nuevas en
   verde, revocadas en rojo, drift en ámbar. Incluye un semáforo del circuito:
   "extracto de lecciones inyectado en el último encargo: SÍ/NO".

DATOS:
- Todo con datos mock realistas y coherentes entre sí (señales con campos reales:
  fecha_asof, run_id, clase, tipo_activo, opp_id, nombre, direccion, horizontes,
  horizonte_principal, prob_interna, riesgo_1a5, siguiente_paso; métricas estilo
  metricas.json: pronósticos totales/resueltos/abiertos, tasa de acierto con
  IC90 de Wilson, brier, bss, ece; lecciones F6 con lec_id LEC-2026-XXXX, ámbito
  clase|horizonte, fuerza 0-1, estado VIGENTE/REVOCADA/CADUCADA y caducidad).
  Prohibido inventar rentabilidades reales:
  los números son de ciclo simulado y el header debe decir "MODO MOCK · DATOS
  SIMULADOS".
- Los eventos del feed y los KPIs se actualizan en intervalos (setInterval) para
  que parezca vivo.

RESTRICCIONES TÉCNICAS:
- Un único archivo dashboard/index.html autocontenido: HTML + CSS + JS vanilla,
  sin build, sin frameworks ni dependencias externas (gráficos de línea dibujados
  en canvas o SVG a mano). Debe abrirse con doble clic.
- UI completa en español. Responsive: 3 columnas en desktop, apilado en móvil.
- Accesibilidad razonable: contraste AA en textos, aria-labels en indicadores.
- No crees nada fuera de la carpeta dashboard/.

CRITERIOS DE ACEPTACIÓN:
- Al abrir dashboard/index.html se reconocen al instante los tres departamentos
  con sus rótulos LED dorados y puntos de estado.
- El feed en vivo agrega eventos cada pocos segundos y el pipeline de encargos
  se anima.
- El panel de aprendizaje muestra lecciones nuevas/revocadas del último ciclo y
  el drift de calibración por celda, con el semáforo del circuito visible.
- Cero dependencias externas; funciona offline.
- Commit `dashboard: v1 del dashboard multi-agente (mock, HTML único)` y línea
  en docs/AVANCE.md.
