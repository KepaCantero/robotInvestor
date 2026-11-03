<!-- PLANTILLA · Informe de seguimiento de opción (ciclo C6) · Bloque A Forex V1.1 (03/11/2026) · Documento 0 Forex V1.1, 7.11 y 14.4.
Lo genera AG-17 Redactor a partir del JSON `informe_seguimiento_opcion` (Anexo B) que le entrega el Analizador; lo valida HT-09
(`validar_seguimiento`, S01–S06, y longitud ≤ 300 palabras) y lo entrega AG-01 Coordinador por CT-24.
Archivo: `Informes de seguimiento/AAAA-MM-DD_informe-seguimiento_RUN-FX-id.md` (y `.json` con el mismo nombre base).
Reglas: una pantalla, ≤ 300 palabras; no cambia ningún valor del JSON; dice siempre qué moneda sube y cuál baja; la recomendación
es una propuesta para el Broker (R4), nunca una orden; sin instrumentos, niveles de entrada ni tamaños (R21).
Un ciclo «sin novedad» (`sin_novedad: true`) usa solo las secciones marcadas con [SN]. Elimine estos comentarios al generar. -->

# Informe de seguimiento de opción · {{seg_id}} · ciclo {{ciclo}}   [SN]

**{{fecha}}** · `{{opp_id}}` · {{par_o_composicion}} {{direccion}} · segmento {{segmento}} · horizonte principal {{horizonte_principal}} ({{naturaleza_inversion}}) · `{{run_id}}`   [SN]

**{{nombre_llano}}** — {{sube_baja_llano}}   [SN]

**Semáforo:** {{VERDE: la tesis mejora | ÁMBAR: sin cambio material o señales mixtas | ROJO: la tesis se deteriora o se acerca una invalidación}}   [SN]

<!-- Si sin_novedad = true: una sola frase y la recomendación. -->
**Sin novedad.** {{una frase: el movimiento del indicador desde el ciclo anterior y que nada material ha cambiado}}   [SN]

**Qué ha cambiado:** {{2–4 hechos: tipo de cambio y rentabilidad total, carry, posicionamiento, bancos centrales, datos o evidencia nueva}}

**Señales de interés del encargo:** {{señal → estado (activada / no activada, con el nivel actual y su fecha)}}

**Invalidación:** {{condición → distancia (porcentaje de la distancia inicial) o ACTIVADA}}

**Catalizadores:** {{evento, fecha, estado: pendiente / ocurrido / aplazado}}

**Puntuaciones (HT-03):** T {{T}} · E {{E}} · A {{A}} · RK {{RK}} ({{variacion_RK con signo}}) · {{elegible / no elegible}} (umbrales 9.2)

**Pronósticos abiertos:** {{PRG-FX-, horizonte, estado; en H5: hitos cumplidos / resueltos y próximo hito con su fecha}}

**Recomendación: {{MANTENER_VIGILANCIA | PROPONER_ENVIO_A_B | CERRAR | PROPONER_CANCELACION}}.** {{motivo en una o dos frases}}   [SN]
<!-- Si PROPONER_ENVIO_A_B: «Se adjunta el encargo para el Bloque B actualizado (paquete_para_bloque_B del JSON).» y, si sugerir_profundizacion_N3 = true, «Se sugiere una profundización N3 antes del envío.»
     Si CERRAR: motivo de cierre (invalidación verificada, objetivo alcanzado u horizonte vencido).
     Si PROPONER_CANCELACION: «La vigilancia ya no aporta valor (n ciclos sin novedad); la cancelación la decide el Broker.» -->

**Supuestos declarados:** {{supuesto (CNS-FX-) y efecto si fuera falso}}   <!-- solo si hay consultas CT-23 sin respuesta -->

**Limitaciones:** {{servicio degradado por credencial ausente, datos sin fecha, informe transversal reutilizado…}}   <!-- solo si las hay -->

*La decisión es siempre del Broker. Este informe no es asesoramiento personalizado.*   [SN]
