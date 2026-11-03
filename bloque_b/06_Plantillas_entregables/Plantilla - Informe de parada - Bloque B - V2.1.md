# Plantilla · Informe de parada · Bloque B · V2.1

> **Bloque B · Robot Investor · V2.1 · 03/11/2026.** Subordinada al Documento 0 del Bloque B, óptima V2.1 (R21, R33, 7.10, 7.11, 14.7; Anexo B.15). Compositor del paquete de parada: **AG-B02 Director** (cuando PV1 o PV2 no se superan y el Broker no ha forzado la continuación). Generador: **AG-B17 Redactor** (CT-B-20, tipo `PARADA`). Lo entrega el Coordinador por CT-B-02 **en lugar de los seis entregables**.
>
> **Instrucciones de uso (se eliminan del entregable):**
> 1. **Breve: dos páginas como máximo.** Legibilidad apta para el Broker (HT-07). No incluye candidatos, encargos C.x ni pronósticos congelados.
> 2. Sustituya cada `{{MARCADOR}}` por el campo de `informe_parada` indicado entre corchetes. Sin afirmaciones nuevas (R9); cada motivo lleva su evidencia (CLM-B, DAT-B o CALC-B) y su etiqueta epistémica (R16).
> 3. «Por qué no merece seguir» tiene **de tres a seis puntos** (7.11, punto 1).
> 4. Controles: G3 determinista con el **perfil reducido PAR** de HT-09 (`validar_informe_parada`), comprobación de fidelidad y autorización de salida del Orquestador; auditoría experta por muestreo (30 %, Anexo A).
> 5. Registro: REC-B en F3 con `resultado_del_analisis = DETENIDO_EN_PUERTA` y veredicto DESCARTAR (sugerencia descartar) o VIGILAR (sugerencia seguimiento); F1 con la entrada `PUERTA_VIABILIDAD` y la entrega; F6 solo con lo verificado (como mínimo, fecha y motivo de la parada).
> 6. Nombre de publicación: `AAAA-MM-DD_informe-parada_PET-B-AAAA-NNNN.md` y `.json` en `Informes de parada/`.

---

# Informe de parada · {{AMBITO_NOMBRE}} [ambito.nombre]

**{{PET_ID}}** · {{REC_ID}} · {{RUN_ID}} · fecha {{FECHA}} · **data_cutoff {{DATA_CUTOFF}}** · tipo de objeto {{TIPO_OBJETO}} · horizonte principal {{HORIZONTE}}

**Resultado: DETENIDO_EN_PUERTA en {{PUERTA}} (capa {{CAPA}}).** [puerta, capa] Sugerencia del bloque: **{{SUGERENCIA}}** [sugerencia] · veredicto registrado {{VEREDICTO_REGISTRADO}} [veredicto_registrado].

## 1. Por qué no merece seguir

<!-- REPETIR: 3–6 puntos [por_que_no_merece_seguir] -->
- {{PUNTO}}
<!-- FIN REPETIR -->

| Criterio | Clase | Detalle | Evidencia | Etiqueta |
|---|---|---|---|---|
<!-- REPETIR: motivos -->
| {{SIN_INVERTIBILIDAD / ALERTA_GRAVE / BIBLIOTECA_DESCARTAR / MATERIALIDAD / YA_DESCONTADO / SIN_MECANISMO / A_PROVISIONAL / E_PROVISIONAL / TESIS_REFUTADA}} | {{ELIMINATORIO / DEBILIDAD / UMBRAL}} | {{DETALLE}} | {{CLM-B / DAT-B / CALC-B}} | {{[HECHO] / [INTERPRETACIÓN] / [ESPECULACIÓN]}} |
<!-- FIN REPETIR -->

Regla aplicada: PV1 se detiene con un criterio eliminatorio o con dos debilidades; PV2, si A provisional < 50, E provisional < 50 o la tesis no sobrevive a la autorrefutación (si solo falla E, antes se consulta al Broker por CT-B-28; 7.10).

## 2. Qué lo cambiaría

<!-- REPETIR: que_lo_cambiaria -->
- {{CONDICION_OBSERVABLE}} (nivel de valoración, dato, catalizador, aparición de instrumentos invertibles)
<!-- FIN REPETIR -->

## 3. Sugerencia

**{{DESCARTAR | PONER_EN_SEGUIMIENTO}}**. {{Si PONER_EN_SEGUIMIENTO: «Seguimiento propuesto (CT-B-29): frecuencia {{FRECUENCIA}}; señales: {{SENALES}}; disparadores: {{DISPARADORES}}.»}} [seguimiento_propuesto]

## 4. Lo que ya se sabe

<!-- REPETIR: lo_que_ya_se_sabe -->
- {{HECHO_VERIFICADO}}
<!-- FIN REPETIR -->

Puntuaciones provisionales: A {{A}} · E {{E}} [puntuaciones_provisionales] (o «no calculadas (la parada es anterior a la capa 2)»). Tiempo {{MINUTOS}} min · {{UC}} UC · por capa {{capa 0: … min, capa 1: … min, …}} [tiempo_consumo.por_capa_min].

**Forzar la continuación:** posible hasta el {{POSIBLE_HASTA}} (7 días; CT-B-04 o CT-B-28) desde el punto de control {{CHECKPOINT_ID}}; estimación del resto p80 {{ESTIMACION_RESTO}} min. No se rebaja ningún umbral (R33): si se fuerza tras PV2, F4 se reduce a escenarios cualitativos y F5 a un universo indicativo sin ranking completo, salvo petición expresa. [forzar_continuacion]

{{Si hay supuestos: «Supuestos aplicados por consultas sin respuesta: {{CNS-B}}: {{SUPUESTO}}.»}} [supuestos_aplicados]

---
*Informe de parada del Bloque B: no es una recomendación personal. No genera candidatos, encargos C.x ni pronósticos congelados (7.11).*
