# Plan de la noche del 15 al 16-11-2026 · terminar de implementar el Bloque A

Lo pidió el operador el 15-11-2026: tareas autónomas, solo para acabar de implementar el Bloque A. Cada tarea es un ticket que pasa por las cuatro fases y no cuenta como hecha sin su QA APTO. Si la QA deja hallazgos medios o altos, van a un ticket nuevo que se hace la misma noche. Desde el 16-11, por decisión del operador, los bajos no abren ticket ni se aplazan a la deuda: se subsanan en el mismo ticket antes de cerrarlo (ronda de cierre), y el mismo revisor comprueba esos arreglos. El número de agentes no tiene tope (el operador lo quitó el 15-11): van a la vez los que no se crucen en sus ficheros. Lo que limita es el uso de la API, que, si salta, los para todos. No se tocan otros bloques.

**Fuera del plan:**
- el modo sombra, porque falta la clave de la API;
- el Bloque B, que es de Astra;
- A-Forex;
- T-152, T-153 y T-155, que son de la otra sesión de Claude;
- la versión de los pyproject (INC-001), que necesita una decisión.

## 0. Lo que ya está en marcha

1. **T-143.** Documento 0 V5.2 con el Anexo B corregido, en la r02 (la QA r01 dio NO APTO por tres afirmaciones falsas). Después vienen la QA r02, el commit con el corpus y los goldens recongelados y el 696 de `CLAUDE.md`.
2. **T-156.** Rango de `cobro_posible_desde` y una prueba de F9 por lista. Queda su QA.

## 1. Fase 0: verificador de consistencia de IDs

3. **T-157 · El verificador** (`prompts/FASE0_VERIFICADOR_IDS.md`). Es el único entregable de fase del Bloque A que no existe todavía: `tools/refs_allowlist.txt` lo reserva como `bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py`. Recorre el corpus y el código (CT, R, F, RF, fichas…) y emite un informe en JSON y en Markdown. Con pruebas, y quitando su línea de la allowlist.

## 2. Funciones que el ejecutor no tiene

Salen de INC-T116-03, INC-T126-01, INC-T116-01 e INC-T116-02, y cada una deja a medias un caso del plan de pruebas. Van ordenadas por lo que pesan en el control del sistema:

4. **T-158 · CT-18 (PB-48).** Las guías de mejora del Orquestador: ante una guía que contradice una regla, se registra el conflicto (COR-), se escala (P3-) y manda la norma más restrictiva.
5. **PB-32.** Una re-ejecución CT-10 coincidente antes de emitir un certificado de horizonte.
6. **PB-50 y PB-64.** Un horizonte que pierde frente a la referencia con significación (DM-HLN) pasa de «Sí» a «Limitado», con su CFG- de P-31. Los estados de los H5 por hitos se publican en F6 y en los entregables.
7. **PB-07.** La respuesta final por CT-03, con referencias, cuando termina el análisis escalado.
8. **PB-61.** Una respuesta tardía del Broker que invalida un supuesto abre una revisión C2.
9. **PB-38.** La opción que se queda fuera del top-3 por una objeción fuerte sin resolver aparece en el informe técnico como alternativa documentada.
10. **PB-36.** La recalibración del umbral E (P-09) y de P-05. La propuesta P3- fuera de banda va a la cola de HA.
11. **PB-33.** La sección «Novedades» de F6.
12. **PB-11 y PB-62.** Las lecciones de producto: enviadas frente a descartadas, y la consulta recurrente.
13. **PB-58.** Pasos 1 y 2: el Buscador envía `solicitudes_credenciales` en el mantenimiento C4 y el Coordinador emite el CT-25.
14. **PB-19.** Con un agente de instancia única saturado: reordenar por prioridad, avisar al Coordinador de los plazos y proponer un cambio de tipo 3 si se repite.
15. **PB-10, PB-17 y PB-21:**
    - el CT-04 que cambia solo P-02 (INC-T116-01);
    - CPI y EAC en la AUT- (INC-T116-02);
    - el tipo de dato protegido en la incidencia.

## 3. Pruebas de lo que ya existe

16. Entre los 37 casos «Superada en parte» de `docs/evidencias_pruebas_bloque_a.md`, los que solo necesitan una prueba del comportamiento que ya hay. Por ejemplo PB-02, PB-13, PB-18, PB-30, PB-39, PB-41, PB-44, PB-47, PB-52 y PB-67: se revisa uno a uno. Al acabar se regeneran las evidencias con `.docs/scripts/evidencias_plan_a.py --ejecutar`. Lo que siga «en parte» queda con su motivo.

## 4. Calidad

17. **Bajar mypy de A** (cuota 109) y ruff en `bloque_a/11_Ejecutor` (2831), con correcciones seguras que no cambien el comportamiento, como en T-132. Las cuotas solo bajan.

## 5. Cierre

18. **Al terminar cada tarea:** se regeneran las evidencias del plan de pruebas y se ponen al día `docs/AVANCE.md` y el diario.
19. **Relevo final** en este fichero: qué se cerró, qué queda y lo que necesita al operador.

## Orden

Primero 1, 2 y 3. Después de la 4 a la 15, por ese orden, varias a la vez si sus ficheros no se cruzan. La 16 y la 17 van en los huecos. Una noche no da para todo: lo que no se termine queda aquí con su estado.
