# Plantilla · Informe de seguimiento · Bloque B · V2.1

> **Bloque B · Robot Investor · V2.1 · 03/11/2026.** Subordinada al Documento 0 del Bloque B, óptima V2.1 (R34, 7.13, 14.8; Anexos B.13 y B.14; archivo F11). Un informe por **ciclo N1-SEG** de un seguimiento encargado por el Broker (CT-B-29). Dirección del ciclo: **AG-B02 Director**; generador: **AG-B17 Redactor** (CT-B-20, tipo `CICLO`).
>
> **Instrucciones de uso (se eliminan del entregable):**
> 1. **Breve: una página.** Sin afirmaciones nuevas (R9); los cambios llevan su evidencia.
> 2. El seguimiento encargado **no es el Vigía**: el Vigía solo compara señales con umbrales sobre las REC-B entregadas y emite alertas (R32); el ciclo de seguimiento lo encarga el Broker, re-lee las dimensiones clave y las señales pedidas, actualiza la Biblioteca y **recomienda**, pero **no inicia ningún análisis profundo**: si recomienda reactivarlo, propone la petición (`peticion_sugerida`) y el Broker decide.
> 3. Controles: G3 determinista con el **perfil reducido CIC** de HT-09 (`validar_informe_seguimiento`) y auditoría por muestreo (20 %, Anexo A).
> 4. Registro: entrada `CIC` en F11 (ciclo, semáforo, recomendación, próximo ciclo); F1 `CICLO_SEGUIMIENTO`; F6 actualizada con lo verificado; evento al Evaluador.
> 5. Nombre de publicación: `AAAA-MM-DD_informe-seguimiento_SEG-B-AAAA-NNNN_cNN.md` y `.json` en `Informes de seguimiento/`.

---

# Informe de seguimiento · {{AMBITO_NOMBRE}} [objeto.ambito]

**{{SEG_ID}}** · ciclo {{CICLO_ID}} · {{RUN_ID}} · fecha {{FECHA}} · **data_cutoff {{DATA_CUTOFF}}** · objeto {{REC_ID}} / {{MKT_ID}}

**Semáforo: {{VERDE | AMBAR | ROJO}}** · recomendación **{{MANTENER_VIGILANCIA | REACTIVAR_ANALISIS_PROFUNDO | PROPONER_PASAR_A_C | CANCELAR_SEGUIMIENTO}}** · próximo ciclo {{PROXIMO_CICLO}}.

{{RESUMEN}} [resumen]

## Qué ha cambiado

| Dimensión | Antes | Ahora | Importancia | Evidencia |
|---|---|---|---|---|
<!-- REPETIR: que_ha_cambiado -->
| {{DIM}} | {{ANTES}} | {{AHORA}} | {{ALTA / MEDIA / BAJA}} | {{CLM-B}} |
<!-- FIN REPETIR · si no hay: «Sin cambios materiales desde el ciclo anterior» -->

## Señales y disparadores

| Señal o disparador | Valor | Umbral | Estado |
|---|---|---|---|
<!-- REPETIR: senales y disparadores (origen BROKER | PLAN) -->
| {{SIG_ID}} {{NOMBRE}} / {{DISPARADOR}} ({{ORIGEN}}) | {{VALOR}} | {{UMBRAL}} | {{NORMAL / PROXIMO / ALCANZADO · NO_ALCANZADO}} |
<!-- FIN REPETIR -->

## Candidatos entregados

| Candidato | Eslabón | Cambio | Estado |
|---|---|---|---|
<!-- REPETIR: candidatos -->
| {{CAND_ID}} | {{ESLABON_ID}} | {{CAMBIO}} | {{VIGENTE / ALERTA / INVALIDADO}} |
<!-- FIN REPETIR · si el objeto es un ámbito nuevo: «Sin candidatos entregados (línea base)» -->

Biblioteca F6: {{MKT_ID}} {{VERSION}} · dimensiones {{DIMENSIONES}}. Alertas del Vigía incluidas: {{ALR-B …}} o «ninguna».

**Recomendación: {{RECOMENDACION}}.** {{MOTIVO}} {{Si REACTIVAR_ANALISIS_PROFUNDO: «Petición sugerida: nivel {{NIVEL}}, alcance {{ALCANCE}}, estimación p80 {{MIN}} min (el Broker decide).»}} {{Si PROPONER_PASAR_A_C: «Candidatos propuestos para C: {{CAND-B …}}.»}}

Tiempo {{MINUTOS}} min · {{UC}} UC. {{Supuestos aplicados: …}} {{Limitaciones: …}}

---
*El bloque no ha iniciado ningún análisis profundo. No es una recomendación personal.*
