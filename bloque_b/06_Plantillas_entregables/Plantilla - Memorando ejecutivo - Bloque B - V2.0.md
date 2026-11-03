# Plantilla · Memorando ejecutivo · Bloque B · V2.0

> **Bloque B · Robot Investor · V2.0 · actualizado V2.1, 03/11/2026.** Subordinada al Documento 0 del Bloque B, óptima V2.1 (14.4, 8.6 y 8.7.4). Generador: AG-B17. **Una o dos páginas** para la decisión rápida del Broker. Mismas cifras, fechas y candidatos que el informe técnico (HT-09, C20). Sin afirmaciones nuevas.
>
> **Énfasis por horizonte dominante (8.6):** H1 → niveles, catalizadores fechados, liquidez y costes, condiciones para no actuar · H2 → ranking, catalizadores previstos, cambios de expectativas y posicionamiento · H3 → régimen, valoración relativa, escenarios e invalidación · H4 → tesis estructural, ganadores y perdedores, disrupciones, riesgos de valoración · **H5** (décadas) → tesis de transformación, hitos intermedios fechados a 1–5 años y probabilidades solo cualitativas. Ordene los bloques 3–6 según ese énfasis.
>
> Nombre de publicación: `AAAA-MM-DD_memorando_PET-B-AAAA-NNNN.md` en `Memorandos ejecutivos/`. Elimine este recuadro.

---

# Memorando · {{AMBITO_NOMBRE}}

**{{PET_ID}}** · {{REC_ID}} · nivel {{NIVEL}} · {{TIPO_OBJETO}} · horizonte {{HORIZONTE}} · fecha {{FECHA}} · **data_cutoff {{DATA_CUTOFF}}**

## 1. Veredicto
**{{VEREDICTO}}** · relevancia decisional **{{RELEVANCIA}}** · resultado {{RESULTADO}} · siguiente paso **{{SIGUIENTE_PASO}}**

Puertas de viabilidad: PV1 {{PV1}} · PV2 {{PV2}} · PV3 {{PV3}}. {{Si hubo: «Continuación forzada por el Broker tras {{PUERTA}}.»}}

| A · atractivo | E · evidencia | C · convicción |
|---|---|---|
| A = {{A}} | E = {{E}} | C = {{C}} ({{C_LECTURA}}) |

## 2. Tesis en tres frases
{{TESIS_FRASE_1}} {{TESIS_FRASE_2}} {{TESIS_FRASE_3}}

## 3. Cifras decisivas (con fecha y artefacto)
<!-- REPETIR: 2–3 cifras -->
- {{CIFRA}} — {{FECHA_CIFRA}} · {{DAT_O_CALC}} · {{CLASE_CIFRA}}
<!-- FIN REPETIR -->

## 4. Candidatos prioritarios por Bloque C.x
| Bloque | Candidato | Identificador | S | Por qué (una línea) |
|---|---|---|---|---|
<!-- REPETIR: PRIORITARIO_PARA_C -->
| {{BLOQUE_C}} | {{CAND_ID}} {{NOMBRE}} | {{ISIN_O_TICKER}} | S = {{S}} | {{ROL}} |
<!-- FIN REPETIR · si no hay: «Ninguno: …» con el motivo (R21) -->

Secundarios y alternativas: ver el informe técnico, sección 10. Apuestas independientes: {{APUESTAS}}.

## 4 bis. Dónde está el valor en la cadena (entregable 6)
| Eslabón | AE | Cuello (PCB) | Mejor opción del eslabón |
|---|---|---|---|
<!-- REPETIR: eslabones con AE ≥ 60 o cuello material (máximo tres) -->
| {{ESLABON_ID}} {{ESLABON}} | {{AE}} | {{PCB}} {{(material)}} | {{CAND_ID}} {{NOMBRE}} o «sin opciones: motivo» |
<!-- FIN REPETIR · si PV3 no se superó: «Ningún eslabón cualifica (PV3 no superada); opciones indicativas en el entregable 6» -->

## 5. Riesgos principales
<!-- REPETIR: riesgo -->
- {{RIESGO}} — señal temprana: {{SENAL}}
<!-- FIN REPETIR -->

## 6. Disparadores, tramos y condiciones de invalidación
- {{CONDICIONES_ENTRADA_O_TRAMOS_O_DISPARADORES}}
- Invalidación: {{INVALIDACION}}
- Qué cambiaría la conclusión: {{QUE_CAMBIARIA}}

## 7. Tiempo y consumo
{{MINUTOS}} min reales (estimación p80 {{EST_P80}} min) · {{UC}} UC · autorizaciones {{AUTORIZACIONES}} · por capa {{POR_CAPA}}.

Supuestos aplicados por consultas sin respuesta (CT-B-28): {{SUPUESTOS}} o «Ninguno».

---
*No es asesoramiento personalizado. El Broker Personal decide; los candidatos son encargos para los Bloques C.x. Historial: {{CERTIFICACION}}.*
