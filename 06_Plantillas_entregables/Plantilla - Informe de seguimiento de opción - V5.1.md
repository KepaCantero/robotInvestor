# Plantilla — Informe de seguimiento de opción

**Bloque A · Robot Investor · Versión óptima V5.1 · 03/11/2026 (nueva)** · Subordinada al Documento 0 óptima V5.1 (7.11, 14.4, Anexo B `informe_seguimiento_opcion`).

> **Uso.** Entregable del **ciclo C6** (seguimiento encargado de opción). Uno por ciclo y encargo `SEG-`. Lo genera **AG-17 Redactor y Diseñador de Informes** a partir de la revisión de seguimiento que le entrega el Analizador (CT-15), lo valida **HT-09** (perfil SEGUIMIENTO) y lo entrega **AG-01 Coordinador** al Broker por **CT-24**; se guarda en `Informes de seguimiento/{{FECHA}}_informe-seguimiento_{{RUN_ID}}.md`, junto a su JSON (`.json`, esquema `Esquema JSON - Informe de seguimiento de opción - V5.1`, ejemplo en `Ejemplo - Informe de seguimiento de opción - V5.1.json`).
>
> **Reglas.**
> 1. **Breve**: una pantalla, **≤ 300 palabras**. Un ciclo **sin novedad** produce solo el bloque A (pocas líneas).
> 2. **Mismos valores que el JSON**, que es la fuente de verdad. No se calcula nada al redactar (R7): las puntuaciones las reconstruye HT-03.
> 3. **Una sola recomendación** (7.11.4): `MANTENER_VIGILANCIA` · `PROPONER_ENVIO_A_B` (solo si la opción vuelve a ser elegible según 9.2 con las puntuaciones actualizadas y no tiene objeciones fuertes abiertas; con el `paquete_para_bloque_B` actualizado y, si la evidencia es antigua o el cambio es material, la sugerencia de profundizar en N3) · `CERRAR` (invalidación verificada, objetivo alcanzado o vencimiento del horizonte) · `PROPONER_CANCELACION` (la vigilancia ya no aporta valor). La decisión es del Broker (R4).
> 4. **Semáforo** con forma y palabra, no solo color: 🟢 Verde (la tesis mejora) · 🟡 Ámbar (sin cambio material o señales mixtas) · 🔴 Rojo (la tesis se deteriora o se acerca una invalidación).
> 5. **R13**: sin certificado, bandas y «sin ventaja demostrada todavía»; en H5, solo banda y estado de los hitos.
> 6. Nunca se congelan pronósticos nuevos en un ciclo C6; nunca se rellena un top-3 (R27).

---

## A. Cabecera y conclusión (siempre)

# Seguimiento de opción · {{SEG_ID}} · ciclo {{CICLO}}

**{{NOMBRE}}** (`{{OPP_ID}}`, {{TIPO_ACTIVO}}) · {{FECHA}} · `{{RUN_ID}}` · horizonte principal **{{HORIZONTE_PRINCIPAL}}**

**Semáforo:** {{SEMAFORO}} · **Recomendación:** **{{RECOMENDACION}}** — {{MOTIVO}}

<!-- Si sin_novedad = true: escribir «Sin novedad.» delante del semáforo y terminar aquí (ir a E). -->

## B. Qué ha cambiado desde el ciclo anterior

<!-- REPETIR: CAMBIO -->
- {{CAMBIO}}
<!-- FIN REPETIR -->

**Señales de interés del encargo.** {{SENAL}}: {{ESTADO_SENAL}}; …

## C. Tesis bajo vigilancia

| Puntuaciones (HT-03) | T | E | A | RK | Variación RK | Elegible (9.2) |
|---|---|---|---|---|---|---|
| Actual | {{T}} | {{E}} | {{A}} | {{RK}} | {{VARIACION_RK}} | {{ELEGIBLE}} |

**Invalidación.** {{CONDICION}} — distancia {{DISTANCIA}} {{ACTIVADA}}; …

**Catalizadores.** {{EVENTO}} ({{FECHA_CATALIZADOR}}): {{ESTADO_CATALIZADOR}}; …

**Pronósticos abiertos.** `{{PRG_ID}}` ({{HORIZONTE}}): {{ESTADO_PRG}}{{HITOS_H5}}; …

> Instrucción: para un H5, el estado es `EN_CURSO_CONFORME`, `DESVIADO` o `INVALIDADO` y se listan sus hitos `HIT-` con fecha y estado (pendiente, cumplido, fallado).

## D. Si la recomendación es `PROPONER_ENVIO_A_B`

**Encargo para el Bloque B actualizado** (ámbito, tesis, horizonte principal, pronósticos, criterios de selección sugeridos, métricas clave y preguntas): ver `paquete_para_bloque_B` del JSON. {{SUGERENCIA_N3}}

## E. Supuestos, limitaciones y aviso

**Supuestos declarados** (consultas al Broker sin respuesta, CT-23): {{SUPUESTO}} (`{{CNS_ID}}`); …

**Limitaciones.** {{LIMITACIONES}}

_Esto no es una recomendación personal; la decisión es del Broker Personal._

---

## Ejemplo ficticio (sin novedad)

> **EJEMPLO FICTICIO.**

# Seguimiento de opción · SEG-2026-9007 · ciclo 4

**Descuento de los fondos cerrados británicos de infraestructuras** (`OPP-2026-9110`, FON) · 2026-11-30 · `RUN-2026-9171` · horizonte principal **H3**

**Sin novedad.** Semáforo 🟡 Ámbar. Recomendación: **MANTENER_VIGILANCIA** — el descuento se mueve dentro de su banda normal y el próximo catalizador (NAV trimestrales) es el 31 de enero.

_Esto no es una recomendación personal; la decisión es del Broker Personal._
