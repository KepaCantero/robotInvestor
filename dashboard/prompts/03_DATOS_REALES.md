# PROMPT 3 — Datos reales: artefactos del ejecutor

> Tercera sesión. Copia primero salidas reales del ejecutor (p. ej. de
> `bloque_a/11_Ejecutor/ejemplos/salida_backtest_simulado/`) a `dashboard/data/`.
> El corpus de los bloques se lee, nunca se modifica. Commit `dashboard:`.

---

Adapta el dashboard (`dashboard/index.html`) para leer datos reales en lugar de
mocks, manteniendo el mismo estilo:

1. Carga estática por artefactos: añade un loader JS que lea, si existen,
   `data/senales.csv`, `data/pronosticos.csv` y `data/metricas.json` (mismos
   esquemas que produce el ejecutor del Bloque A) y pueble KPIs, pipeline,
   feed y control de riesgo desde ahí; si no existen, cae a los mocks y muestra
   el semáforo "MODO MOCK". Parsea el CSV a mano (split por comas respetando
   comillas dobles).
2. Normaliza cada señal al modelo de la UI: opp_id, nombre, direccion
   (LARGO/CORTO), clase, horizonte_principal, prob_interna, riesgo_1a5,
   siguiente_paso (resalta ENVIAR_A_BLOQUE_B como encargo en tránsito).
3. Métricas desde metricas.json: pronósticos totales/resueltos/abiertos, y por
   cada clase|horizonte la tasa de acierto con su IC90 (muestra el intervalo,
   no solo el punto). Advertencias del ciclo en el panel de Control de Riesgo
   en color ámbar.
4. Añade un selector de fecha_asof/run_id (RUN-2026-XXXX) que filtre señales,
   pipeline y feed, con opción "Último run".
5. No añadas servidor ni build: todo debe seguir funcionando abriendo el HTML,
   documentando en un comentario inicial cómo servir la carpeta si el navegador
   bloquea fetch de file:// (p. ej. `python3 -m http.server`).
6. Memoria de aprendizaje (F6): si existe `data/memoria_aprendizaje.json`
   (export del almacén F6), puebla el Panel de Aprendizaje con: lecciones
   (lec_id, ámbito, fuerza, estado VIGENTE/REVOCADA/CADUCADA, caducidad),
   certificados (cert_id, celda, bss, holm_superado, estado) y métricas por
   celda (MET-: acierto con IC90, brier, bss, ece). Si no existe, el panel cae
   a mock y su semáforo del circuito marca "SIN DATOS". Los identificadores y
   estados usan exactamente el vocabulario del esquema F6 del corpus, sin
   sinónimos inventados.

Restricciones que se mantienen: archivo único, sin dependencias externas, UI en
español, la etiqueta de modo (MOCK/ARTIFACTOS) siempre visible y veraz, no se
modifica nada fuera de `dashboard/`.

Criterios de aceptación: con `dashboard/data/` poblado el semáforo cambia a
"ARTIFACTOS" y los KPIs cuadran con los CSV/JSON cargados (verifica tú mismo los
totales contra los archivos, incluida la memoria F6 si está presente); sin la
carpeta, cae limpio a mock; commit
`dashboard: carga de artefactos reales con fallback mock`.
