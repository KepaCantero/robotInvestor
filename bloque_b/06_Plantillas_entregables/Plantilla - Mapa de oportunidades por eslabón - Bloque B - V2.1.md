# Plantilla · Mapa de oportunidades por eslabón de la cadena de valor · Bloque B · V2.1

> **Bloque B · Robot Investor · V2.1 · 03/11/2026.** Subordinada al Documento 0 del Bloque B, óptima V2.1 (secciones 8.7, 8.7.4, 9.12, 9.13, 14.6; Anexo B.16). **Entregable 6.** Compositor del contenido: **AG-B02 Director del Análisis de Mercado** (campo `mapa_cadena_valor` del paquete de síntesis, compuesto en F7 sin afirmaciones nuevas a partir del despliegue estructural de AG-B03, el radar de emergentes de AG-B24 y la selección de AG-B12). Generador del documento: **AG-B17 Redactor y Diseñador de Informes** (CT-B-20, tipo `SINTESIS`).
>
> **Instrucciones de uso (se eliminan del entregable):**
> 1. Sustituya cada `{{MARCADOR}}` por el campo del paquete indicado entre corchetes `[mapa_cadena_valor.…]`. Los bloques `<!-- REPETIR: … -->` se repiten por elemento; si no hay ninguno se deja la frase de «sin elementos» indicada (R21: menos es legítimo y se explica).
> 2. **No añada afirmaciones** que no estén en el paquete (R9). Toda cifra lleva su `DAT-B` o `CALC-B`; PCB, AE y S se reconstruyen con el anexo de datos (entregable 5, hojas `Eslabones`, `Opciones_eslabon` y `Emergentes`) y con HT-03.
> 3. **Orden de los eslabones:** descendente por AE; los eslabones con cuello **material** (PCB ≥ 30 y al menos dos indicadores en rojo) se marcan «cuello material».
> 4. **Mejores opciones por eslabón** (9.13): hasta cinco por eslabón (N1: tres, y solo en el eslabón crítico), **adicionales al top-N por tipo y sin duplicarlo**; solo eslabones con AE ≥ 60 o con cuello material. Cada opción supera PC1–PC4 y tiene S ≥ 50. Las opciones que no están en el top-N de su tipo y obtienen PRIORITARIO_PARA_C generan su propio encargo C.x (`origen_seleccion = MEJORES_POR_ESLABON`).
> 5. **Si PV3 no se superó** (ningún eslabón cualifica): el entregable se emite igualmente con el desglose, las métricas, el PCB y el AE de cada eslabón, y las opciones se marcan «indicativas (PV3 no superada)» **sin PRIORITARIO_PARA_C**, o se escribe «sin opciones invertibles que superen los filtros» con el motivo.
> 6. **Emergentes:** el PEM **ordena, no recomienda**. Un emergente solo entra en una tabla de opciones si su vía de exposición es invertible (`COTIZADA_DIRECTA`, `MATRIZ_COTIZADA`, `ETF_O_FONDO`) y el instrumento supera PC1–PC4; en otro caso pasa a la vigilancia del plan de seguimiento.
> 7. La fecha de corte (`data_cutoff`) es la misma que la de los otros cinco entregables (HT-09, G3B-CON-01 y G3B-ENT-11).
> 8. Nombre de publicación: `AAAA-MM-DD_mapa-eslabones_PET-B-AAAA-NNNN.md` en `Mapas por eslabón/`, con copia `.docx` obtenida por **conversión fiel** del Markdown (pandoc o python-docx) y el JSON `mapa_cadena_valor` (`…_mapa-eslabones_….json`).
> 9. Aviso legal obligatorio al final (17.8 del Documento 0).

---

# Mapa de oportunidades por eslabón · {{AMBITO_NOMBRE}} [ambito.nombre]

**{{PET_ID}}** [pet_id] · {{REC_ID}} [rec_id] · nivel {{NIVEL}} [estrategia.nivel] · {{TIPO_OBJETO}} [ambito.tipo_objeto] · horizonte principal {{HORIZONTE}} [estrategia.horizonte_dominante] · fecha {{FECHA}} · **data_cutoff {{DATA_CUTOFF}}** [mapa_cadena_valor.data_cutoff]

Entregable 6 del Bloque B para el Broker. Veredicto del ámbito: **{{VEREDICTO}}** [veredicto.valor]. Puertas de viabilidad: PV1 {{PV1}} · PV2 {{PV2}} · PV3 {{PV3}} [capas.puertas_viabilidad]. {{CONTINUACION_FORZADA}} [capas.continuacion_forzada] (si la hubo: «Continuación forzada por el Broker tras {{PUERTA}}»). {{SUPUESTOS}} [supuestos_aplicados] (si los hay: «Supuestos aplicados por consultas sin respuesta: …»).

## 1. Alcance del desglose

Nivel de detalle {{NIVEL_DETALLE}} [mapa_cadena_valor.nivel_detalle] · eslabón crítico {{ESLABON_CRITICO}} [mapa_cadena_valor.eslabon_critico] · {{N_ESLABONES}} eslabones analizados. Profundidad por nivel (Anexo A): N1 macro-eslabones y el eslabón crítico · N2 hasta sub-eslabón en los eslabones relevantes · N3 hasta actividad e insumo crítico.

| Omitido | Motivo |
|---|---|
<!-- REPETIR: mapa_cadena_valor.omisiones -->
| {{ESLABON_OMITIDO}} | {{MOTIVO_OMISION}} |
<!-- FIN REPETIR · si no hay: «Ninguna omisión» -->

## 2. Árbol de la cadena

Árbol jerárquico (HT-04) con, en cada nodo, su nivel, su AE, su PCB y la marca de cuello material.

```
{{ESL_ID}} {{ESL_NOMBRE}} [{{NIVEL}}] · AE {{AE}} · PCB {{PCB}} {{· CUELLO MATERIAL}}
   └─ {{ESL_ID_HIJO}} {{ESL_NOMBRE_HIJO}} [sub|actividad|insumo] · AE {{AE}} · PCB {{PCB}}
```

## 3. Eslabones (orden descendente por AE)

<!-- REPETIR: mapa_cadena_valor.eslabones (orden AE descendente) -->
### {{ESLABON_ID}} · {{ESLABON_NOMBRE}} {{· cuello material}}

{{DESCRIPCION}} Papel del ámbito: {{PAPEL_AMBITO}} (ES | CONSUME | ALIMENTA). Nivel: {{NIVEL_ESLABON}} {{(padre ESL-…)}}.

| Métrica | Valor |
|---|---|
| Tamaño | {{TAMANO}} {{UNIDAD}} ({{FECHA}}; {{DAT-B}}) o «—» |
| Crecimiento anual | {{CRECIMIENTO}} % |
| Margen típico (bruto / operativo) · ROIC | {{MARGEN_BRUTO}} / {{MARGEN_OPERATIVO}} · {{ROIC}} |
| Poder de negociación · HHI de proveedores | {{PODER}} · {{HHI}} |
| Concentración por país | {{PAIS}} {{CUOTA}} |
| Capacidad · utilización · plazo de entrega | {{CAPACIDAD}} · {{UTILIZACION}} · {{PLAZO_SEMANAS}} semanas |
| Sustitutos | {{SUSTITUTOS}} |
| Actores principales | {{ACTOR}} ({{CUOTA}}; cotizado sí/no) … |
| Cuello de botella | sí/no · severidad {{SEV}} (1–5) · persistencia {{PERS}} (1–5) · relevancia para el valor {{REL}} (1–5) · **PCB = {{PCB}}** {{(material)}} · causa {{CAUSA}} · {{CALC-B}} |
| Indicadores del cuello | {{INDICADOR}} = {{VALOR}} ({{VERDE/AMBAR/ROJO}}; {{DAT-B}}) … |
| Señal de resolución | {{SENAL_RESOLUCION}} |
| Atractivo del eslabón | **AE = {{AE}}** · crecimiento {{}} (20) · margen/ROIC {{}} (20) · poder de negociación {{}} (15) · cuello {{}} (20) · expectativas invertidas {{}} (15) · sustitución invertida {{}} (10) · {{CALC-B}} |

**Mejores opciones del eslabón** (hasta cinco; adicionales al top-N por tipo, sin duplicarlo; 9.13)

| Rango | Candidato | Ticker / ISIN | Tipo | Rol en el eslabón | Pureza al eslabón | S (IC 90 %) | Veredicto | Motivo | Riesgos clave |
|---|---|---|---|---|---|---|---|---|---|
<!-- REPETIR: opciones del eslabón (rango ascendente) -->
| {{RANGO}} | {{CAND_ID}} {{NOMBRE}} | {{TICKER_O_ISIN}} | {{TIPO_ACTIVO}} | {{ROL}} | {{PUREZA}} | {{S}} ({{IC_INF}}–{{IC_SUP}}) | {{PRIORITARIO_PARA_C / SECUNDARIO / indicativa (PV3 no superada)}} | {{MOTIVO}} (en el top-N de su tipo / añadida por cobertura del eslabón) | {{RIESGOS}} |
<!-- FIN REPETIR · si no hay: «Sin opciones: {{sin_opciones_motivo}}» (p. ej., «el eslabón no es atractivo ni tiene un cuello material», «sin opciones invertibles que superen los filtros») -->

**Emergentes, startups y spin-offs del eslabón** (radar de AG-B24; el PEM ordena, no recomienda)

| Nombre | Tipo | Financiación conocida | Tecnología o ventaja | Señales de tracción | Vía de exposición | PEM | Riesgos |
|---|---|---|---|---|---|---|---|
<!-- REPETIR: emergentes del eslabón (PEM descendente) -->
| {{EMG_ID}} {{NOMBRE}} | {{STARTUP / SCALE_UP / SPIN_OFF_UNIVERSITARIO / SPIN_OFF_CORPORATIVO / SALIDA_A_BOLSA_RECIENTE}} | {{IMPORTE}} M{{DIVISA}} · {{ULTIMA_RONDA}} · {{FECHA}} ({{EVD-B}}) o «no publicada» | {{TECNOLOGIA}} | {{SENALES}} | {{COTIZADA_DIRECTA / MATRIZ_COTIZADA / ETF_O_FONDO / FUTURA_SALIDA_A_BOLSA / NO_INVERTIBLE_HOY}} ({{INSTRUMENTO}}; {{CAND-B o «fuera de filtros»}}) | {{PEM}} | {{RIESGOS}} |
<!-- FIN REPETIR · si no hay: «El radar no ha identificado emergentes con información verificable en este eslabón» -->
<!-- FIN REPETIR eslabones -->

## 4. Síntesis

{{SINTESIS}} [mapa_cadena_valor.sintesis]: dónde se captura el valor, qué eslabones evitar y por qué, y qué cambiaría el mapa (señal de resolución del cuello). Los eslabones sin opciones lo dicen y explican por qué (R21).

## 5. Trazabilidad

Cifras: {{DAT-B …}} · cálculos PCB, AE, S y PEM: {{CALC-B …}} (MC-B07; HT-03 los reconstruye) · fichas del Catálogo aplicadas: VC-DESG-001, VC-BOT-001{{, EMG-PEM-001}} · anexo de datos: hojas `Eslabones`, `Opciones_eslabon`, `Emergentes`.

---
*Mapa de oportunidades por eslabón del Bloque B: activos que el análisis ha estudiado; no son recomendaciones personales. El Broker Personal decide; los candidatos prioritarios son encargos para los Bloques C.x. Historial: {{CERTIFICACION}}.*
