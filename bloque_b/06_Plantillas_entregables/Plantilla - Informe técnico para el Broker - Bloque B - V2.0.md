# Plantilla · Informe técnico para el Broker · Bloque B · V2.0

> **Bloque B · Robot Investor · V2.0 · actualizado V2.1, 03/11/2026.** Subordinada al Documento 0 del Bloque B, óptima V2.1 (secciones 7.9–7.13, 8, 9, 11, 14 y 14.1; Anexos A y B). Generador: **AG-B17 Redactor y Diseñador de Informes**, a partir del paquete de síntesis autorizado (CT-B-20). El informe técnico es la **pieza principal** de los seis entregables: dice lo mismo que el memorando, el informe visual, el paquete JSON, el anexo de datos y el mapa de oportunidades por eslabón (entregable 6), con la máxima profundidad.
>
> **Instrucciones de uso (se eliminan del entregable):**
> 1. Sustituya cada `{{MARCADOR}}` por el campo del paquete indicado entre corchetes `[ruta.json]`. Los bloques `<!-- REPETIR: … -->` se repiten por elemento y se eliminan si no hay ninguno, dejando la frase de «sin elementos» indicada.
> 2. **No añada afirmaciones** que no estén en el paquete (R9). Toda cifra lleva su `DAT-B` o `CALC-B` y su clase (determinista, estimación estadística, juicio experto); toda afirmación, su etiqueta [HECHO], [INTERPRETACIÓN] o [ESPECULACIÓN] (R16).
> 3. Las probabilidades numéricas solo aparecen si hay certificado (R13); si no, bandas verbales y la leyenda «sin ventaja demostrada».
> 4. La fecha de corte (`data_cutoff`) es la misma en los seis entregables; HT-09 lo comprueba en segunda pasada (G3B-CON-01) y comprueba que los eslabones, sus opciones y los candidatos coinciden con el entregable 6 (G3B-ENT-11).
> 4 bis. **V2.1:** el análisis avanza por **capas 0–4** con puertas **PV1–PV3** (7.10); si PV1 o PV2 no se superan, este informe **no se emite** y se entrega el informe de parada (`Plantilla - Informe de parada - Bloque B - V2.1.md`). Todo candidato lleva `eslabon_id`; las consultas al Broker (CT-B-28) y los **supuestos aplicados** se declaran en la sección 3.5; la continuación forzada, en la portada.
> 5. Nombre de publicación: `AAAA-MM-DD_informe-tecnico_PET-B-AAAA-NNNN.md` (y PDF) en `Informes técnicos Broker/`.
> 6. Aviso legal obligatorio al final (sección 17.8 del Documento 0).

---

# Informe técnico · {{AMBITO_NOMBRE}} [ambito.nombre]

## 1. Portada

| Campo | Valor |
|---|---|
| Petición | {{PET_ID}} [pet_id] · referencia del Broker {{PET_REF_BROKER}} |
| Ejecuciones | {{RUN_IDS}} [run_ids] (más de una si hubo punto de control y reanudación o fases) |
| Análisis registrado | {{REC_ID}} [rec_id] · ficha de la Biblioteca {{MKT_ID}} [ambito.mkt_id] |
| Nivel | {{NIVEL}} [estrategia.nivel] · plan de cálculo {{PLAN_CALCULO}} |
| Tipo de objeto | {{TIPO_OBJETO}} [ambito.tipo_objeto] {{RECLASIFICACION}} [origen.reclasificacion] |
| Horizonte dominante | {{HORIZONTE}} [estrategia.horizonte_dominante] · solapamientos {{HORIZONTES}} |
| Fecha del informe · fecha de corte | {{FECHA}} [fecha] · **data_cutoff {{DATA_CUTOFF}}** [data_cutoff] |
| Resultado del análisis | {{RESULTADO}} [veredicto.resultado_del_analisis] (CONCLUYENTE · PARCIAL · NO_CONCLUYENTE · BLOQUEADO; DETENIDO_EN_PUERTA solo en el informe de parada) |
| Capas y puertas de viabilidad | capas ejecutadas {{CAPAS}} · PV1 {{PV1}} · PV2 {{PV2}} · PV3 {{PV3}} [capas.puertas_viabilidad] · continuación forzada {{CONTINUACION_FORZADA}} [capas.continuacion_forzada] o «No» |
| Supuestos aplicados | {{SUPUESTOS}} [supuestos_aplicados] (consultas CT-B-28 sin respuesta) o «Ninguno» |
| Horizontes secundarios | {{HORIZONTES_SECUNDARIOS}} (H1–H5; H5 = décadas, con hitos intermedios) |
| Validación G3 · auditoría previa | {{DICTAMEN_G3}} · {{AUDITORIA}} (vueltas, muestreo) |
| Reservas de auditoría | {{RESERVAS}} [reservas_auditoria] o «Ninguna» |
| Estados degradados | {{ESTADOS_DEGRADADOS}} [estados_degradados] o «Ninguno» (credenciales ausentes, fuentes sin acceso, alcance reducido por la puerta de tiempo) |
| Metodología | {{METODOLOGIA}} [methodology_version] |

## 2. Resumen ejecutivo

**Veredicto del ámbito: {{VEREDICTO}}** [veredicto.valor] · horizonte {{HORIZONTE}} · relevancia decisional **{{RELEVANCIA}}** · siguiente paso **{{SIGUIENTE_PASO}}** · reversibilidad {{REVERSIBILIDAD}}.

| Puntuación | Valor | Lectura |
|---|---|---|
| A · Atractivo del ámbito | A = {{A}} | {{A_LECTURA}} |
| E · Calidad de la evidencia | E = {{E}} | {{E_LECTURA}} |
| C · Convicción | C = {{C}} | {{C_LECTURA}} (alta ≥ 70 · media 50–69 · baja < 50); tope C ≤ E + 10 |
| RF · Refutación · RE · Robustez entre escenarios | RF = {{RF}} · RE = {{RE}} | Veredicto de Contrarias: {{VEREDICTO_TESIS}} |

**Tesis en tres frases.** {{TESIS_3_FRASES}}

**Cuatro evaluaciones separadas** (un mercado extraordinario con expectativas descontadas no es una oportunidad bursátil):

| Evaluación | Conclusión |
|---|---|
| Atractivo del mercado | {{EV_MERCADO}} |
| Calidad del ámbito | {{EV_CALIDAD}} |
| Atractivo bursátil | {{EV_BURSATIL}} |
| Accesibilidad | {{EV_ACCESIBILIDAD}} |

**Candidatos prioritarios por Bloque C.x** [veredicto.prioritarios_por_bloque_C]:

| Bloque | Candidato | Identificador | S (IC 90 %) | Por qué |
|---|---|---|---|---|
<!-- REPETIR: candidato PRIORITARIO_PARA_C -->
| {{BLOQUE_C}} | {{CAND_ID}} {{NOMBRE}} | {{ISIN_O_TICKER}} | S = {{S}} ({{IC_INF}}–{{IC_SUP}}) | {{ROL_EN_TESIS}} |
<!-- FIN REPETIR · si no hay: «Ningún candidato prioritario: …» con el motivo (R21) -->

**Condiciones de entrada / tramos / disparadores** (según el veredicto): {{CONDICIONES}}
**Qué cambiaría la conclusión:** {{QUE_CAMBIARIA}}
**Apuestas independientes:** {{APUESTAS}} [apuestas_independientes] — grupos: {{GRUPOS_APUESTAS}}

## 3. Petición, origen, estrategia, tiempo y autorizaciones

### 3.1 Petición
- Ámbito pedido y delimitación final: **incluye** {{INCLUYE}} · **excluye** {{EXCLUYE}} · región {{REGION}}.
- Tipos de activo admitidos por el Broker: {{TIPOS_ADMITIDOS}} · aplicables tras el encuadre: {{TIPOS_APLICABLES}}.
- Marco de invertibilidad: {{MARCO}} (por defecto, minorista europeo, UCITS, EUR; 2.7).
- Preguntas del Broker y `preguntas_para_B` del Bloque A, con su respuesta:

| Pregunta | Origen | Respuesta | Referencias |
|---|---|---|---|
<!-- REPETIR: respuesta [respuestas_preguntas] -->
| {{PREGUNTA}} | {{ORIGEN}} | {{RESPUESTA}} | {{REFS}} |
<!-- FIN REPETIR -->

### 3.2 Origen (`paquete_para_bloque_B`) — herencia no es evidencia (R31)
- Oportunidad del Bloque A: {{OPP_ID_A}} [origen.opp_id_A] · tipo de opción y reclasificación: {{RECLASIFICACION}}.
- **Confirmado** (re-verificado con fuentes propias): {{CONFIRMADO}}
- **Refutado**: {{REFUTADO}}
- **Sin verificar**: {{SIN_VERIFICAR}}

### 3.3 Estrategia aplicada (matriz 8.3)
Perfil del Motor {{PERFIL_MOTOR}} · playbooks {{PLAYBOOKS}} · tipos materiales para el modulador {{TIPOS_MATERIALES}}.

| Dimensión | Peso efectivo | Profundidad | Especialista | Tratada en | Exclusión / motivo |
|---|---|---|---|---|---|
<!-- REPETIR: D1…D12 -->
| {{DIM}} {{DIM_NOMBRE}} | {{PESO}} | {{PROF}} | {{ESPECIALISTA}} | {{PROF_TRATADA}} | {{EXCLUSION}} |
<!-- FIN REPETIR -->

Desviaciones del Director sobre la matriz (±5 puntos con justificación): {{DESVIACIONES}} o «Ninguna».

### 3.4 Tiempo, consumo y autorizaciones (R20)
- Estimación previa: p50 {{EST_P50}} min · **p80 {{EST_P80}} min** · real **{{MINUTOS}} min** · consumo **{{UC}} UC** · reloj {{RELOJ}}.
- Tiempo por fase: {{POR_FASE}}
- **Tiempo por capa (V2.1):** {{POR_CAPA}} [tiempo_consumo.por_capa_min] frente a la estimación por capa {{EST_POR_CAPA}}; opción `HASTA_PV2` si se autorizó.
- Autorizaciones de la puerta de tiempo: {{AUTORIZACIONES}} (AUT-B: puerta, momento, justificación, opción elegida, quién decidió) · puntos de control: {{CHECKPOINTS}}.

### 3.5 Puertas de viabilidad y consultas al Broker (7.10, 7.12)
| Capa | Puerta | Resultado | Criterios evaluados | Momento |
|---|---|---|---|---|
<!-- REPETIR: capas.registro -->
| {{CAPA}} | {{PV1 / PV2 / PV3}} | {{SUPERADA / NO_SUPERADA / FORZADA}} | {{CRITERIOS}} | {{FECHA_HORA}} |
<!-- FIN REPETIR -->

| CNS-B | Tipo | Modo | Pregunta (lenguaje claro) | Estado | Respuesta o supuesto aplicado | Efecto |
|---|---|---|---|---|---|---|
<!-- REPETIR: consultas_broker -->
| {{CNS_ID}} | {{TIPO}} | {{BLOQUEANTE / NO_BLOQUEANTE}} | {{PREGUNTA}} | {{RESPONDIDA / SUPUESTO_APLICADO / …}} | {{RESPUESTA_O_SUPUESTO}} | {{SIN_CAMBIO / SUPUESTO_CAMBIADO}} |
<!-- FIN REPETIR · si no hay: «Sin consultas al Broker en esta petición» -->

## 4. Régimen de referencia
{{RGM_ID}} · estado de confianza **{{ESTADO_REGIMEN}}** · variables dominantes: {{VARIABLES}}.
Relaciones apoyadas como estables y su naturaleza (histórica observada con ventana, o causal demostrada con mecanismo): {{RELACIONES}}.

## 5. Las doce dimensiones
<!-- REPETIR: dimensión [dimensiones] (las excluidas, con motivo, momento y condición de reapertura) -->
### {{DIM}} · {{DIM_NOMBRE}} — {{PROF_TRATADA}} · {{ESPECIALISTA}}
**Pregunta central:** {{PREGUNTA_CENTRAL}}

<!-- REPETIR: nota -->
- {{ETIQUETA}} {{AFIRMACION}} — {{CLASE_CIFRA}} · {{EVIDENCIAS_CALCULOS}}
<!-- FIN REPETIR -->

**Conclusión parcial:** {{CONCLUSION}}
**Confianza:** {{CONFIANZA}} — a favor: {{FACTORES_FAVOR}}; en contra: {{FACTORES_CONTRA}}.
**Lagunas:** {{LAGUNAS}} · **Discrepancias (DSC-B):** {{DISCREPANCIAS}}
<!-- FIN REPETIR -->

## 6. Despliegue estructural de la cadena de valor (8.7)
**Alcance:** {{ALCANCE_DESPLIEGUE}} (N1: eslabón crítico · N2: eslabones relevantes · N3: cadena completa).

### 6.1 (4a) Mapa de la cadena y desglose jerárquico (8.7.1)
Desglose macro → sub → actividad → insumo con identificadores ESL- (ficha VC-DESG-001); el detalle completo por eslabón está en el **entregable 6** («Mapa de oportunidades por eslabón»), que este informe resume.

| Eslabón (ESL-) | Nivel | Papel del ámbito | Participantes | Concentración (HHI) | Margen aprox. | Captura de valor | PCB | AE | Cuello material | Opciones |
|---|---|---|---|---|---|---|---|---|---|---|
<!-- REPETIR: eslabón [mapa_cadena_valor.eslabones] -->
| {{ESLABON_ID}} {{ESLABON}} | {{macro / sub / actividad / insumo}} | {{PAPEL}} (es · consume · alimenta) | {{PARTICIPANTES}} | {{CONCENTRACION}} | {{MARGEN}} | {{CAPTURA}} | {{PCB}} | {{AE}} | {{sí / no}} | {{N_OPCIONES}} |
<!-- FIN REPETIR -->

### 6.2 (4b) Actores establecidos y emergentes (radar de AG-B24, 8.7.3)
| Actor | Eslabón | Tipo | Vía de exposición | PEM | Evidencia |
|---|---|---|---|---|---|
| {{ACTOR}} {{EMG_ID}} | {{ESLABON_ID}} | establecido · STARTUP · SCALE_UP · SPIN_OFF_UNIVERSITARIO · SPIN_OFF_CORPORATIVO · SALIDA_A_BOLSA_RECIENTE | COTIZADA_DIRECTA · MATRIZ_COTIZADA · ETF_O_FONDO · FUTURA_SALIDA_A_BOLSA · NO_INVERTIBLE_HOY | {{PEM}} (ordena, no recomienda; EMG-PEM-001) | {{EVIDENCIA}} |

### 6.3 (4c) Vigilancia tecnológica (0–2, 2–5, 5+ años)
| Horizonte | Avance | Madurez | Etiqueta | Implicación |
|---|---|---|---|---|
| {{H_ANOS}} | {{AVANCE}} | {{MADUREZ}} | {{ETIQUETA}} | {{IMPLICACION}} |

### 6.4 (4d) Cuellos de botella y perdedores sistemáticos (VC-BOT-001)
PCB = round(100 · severidad · persistencia · relevancia / 125); cuello **material** si PCB ≥ 30 y al menos dos indicadores en rojo (9.12; HT-03 lo reconstruye).

| Eslabón | Causa | Severidad · persistencia · relevancia | PCB | Indicadores (estado) | Señal de resolución | Favorecidos | Perjudicados | Perdedores sistemáticos | Reflejo en tesis y escenarios |
|---|---|---|---|---|---|---|---|---|---|
| {{ESLABON_ID}} | {{CAUSA}} | {{SEV}} · {{PERS}} · {{REL}} | {{PCB}} | {{INDICADORES}} | {{SENAL}} | {{FAVORECIDOS}} | {{PERJUDICADOS}} | {{PERDEDORES}} | {{REFLEJO}} |

### 6.5 (4e) Efectos de segundo y tercer orden
- {{ETIQUETA}} **{{PREGUNTA}}** {{RESPUESTA}} (invertible: {{INVERTIBLE}})

## 7. Máquina de proyecciones (8.8)
Activada: {{ACTIVADA}} · motivo de exclusión: {{MOTIVO_EXCLUSION_PROY}}.

| Etapa | Contenido | Resultado | Artefactos |
|---|---|---|---|
| {{ETAPA}} | {{CONTENIDO}} | {{RESULTADO}} | {{CALC}} |

**Premisas falsables** (sin premisa no hay cifra):

| Premisa | Valor | Fuente | Sensibilidad | Invalidación |
|---|---|---|---|---|
| {{PREMISA}} | {{VALOR}} | {{FUENTE}} | {{SENSIBILIDAD}} | {{INVALIDACION}} |

**Brecha de expectativas (DCF inverso):** {{BRECHA}}

## 8. Escenarios, sensibilidades, robustez y pronósticos
| Escenario | Premisas | Régimen | Probabilidad o banda | Resultado frente a la referencia | Disparadores |
|---|---|---|---|---|---|
<!-- REPETIR: base · favorable · adverso -->
| {{ESCENARIO}} | {{PREMISAS}} | {{REGIMEN}} | {{PROB_O_BANDA}} | {{RESULTADO_REF}} | {{DISPARADORES}} |
<!-- FIN REPETIR -->

Robustez entre escenarios: **RE = {{RE}}**. Probabilidades numéricas: solo con frecuencia histórica, implícita de mercado con su fuente o certificado; en otro caso, bandas (protocolo cuantitativo, 8.8).

**Sensibilidades**

| Variable | Base | Rango | Efecto | Artefacto |
|---|---|---|---|---|
| {{VARIABLE}} | {{BASE}} | {{BAJO}} – {{ALTO}} | {{EFECTO_BAJO}} / {{EFECTO_ALTO}} | {{CALC}} |

**Pronósticos congelados (F4, R14)**

| PRG-B | Tipo | Afirmación | Horizonte | Resolución | Criterio | Referencia | Banda |
|---|---|---|---|---|---|---|---|
| {{PRG_ID}} | AMBITO · RANKING · HITO_H5 | {{AFIRMACION}} | {{H}} | {{FECHA_RES}} | {{CRITERIO}} | {{REFERENCIA}} (HITO_H5: RI-LIN) | {{BANDA}} |

Con horizonte principal **H5** (décadas): probabilidades solo cualitativas y **al menos tres hitos intermedios** verificables a 1–5 años (HITO_H5, fichas DIF-H5-001 y FC-HITO-001) que permiten evaluar la tesis antes de su horizonte.

## 9. Tesis, hipótesis competidoras y su cierre (R15)
**Tesis falsable:** {{TESIS}}
**Mecanismo:** {{MECANISMO}}

| Premisa | Evidencia | Comprobación | Horizonte | Invalidación |
|---|---|---|---|---|
| {{PREMISA}} | {{EVIDENCIA}} | {{COMPROBACION}} | {{H}} | {{INVALIDACION}} |

| Hipótesis | Naturaleza | Discriminante | Indicador anticipado | Estado | Evidencia |
|---|---|---|---|---|---|
| {{HIP_ID}} {{ENUNCIADO}} | {{NATURALEZA}} | {{DISCRIMINANTE}} | {{INDICADOR}} | confirmada · debilitada · indeterminada · invalidada | {{EVIDENCIA}} |

**Steelman de la tesis contraria:** {{STEELMAN}}

## 10. Selección de activos (F5)
<!-- REPETIR: tipo de activo aplicable [candidatos_por_tipo] -->
### 10.x {{TIPO}} · {{TIPO_NOMBRE}} ({{PLAYBOOK}} → Bloque {{BLOQUE_C}})
- **Universo:** {{TAMANO}} activos ({{TAMANO_INVERTIBLE}} invertibles) a {{FECHA_UNIVERSO}} · fuentes: {{FUENTES}} · método: {{METODO}} (punto en el tiempo, sin sesgo de supervivencia).
- **Exclusiones por motivo:** {{EXCLUIDOS_POR_MOTIVO}} · destacadas: {{EXCLUSIONES_DESTACADAS}}.
- **Traducción de los rasgos de la tesis a métricas (9.5.6):** {{TRADUCCION}}.
- **Referencia:** ámbito {{REF_AMBITO}} · ranking {{REF_RANKING}}.

| Rango | Candidato | Identificador | Eslabón | S | IC 90 % S | IC 90 % rango | PE | QL | VA | MO | RI | LA | CO | Pureza | Puertas | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
<!-- REPETIR: candidato del top-N -->
| {{RANGO}} | {{CAND_ID}} {{NOMBRE}} | {{ISIN}} | {{ESLABON_ID}} | {{S}} | {{IC_S}} | {{IC_RANGO}} {{FRONTERA}} | {{PE}} | {{QL}} | {{VA}} | {{MO}} | {{RI}} | {{LA}} | {{CO}} | {{PUREZA}} | {{PUERTAS_NO_OK}} | {{VEREDICTO_CAND}} |
<!-- FIN REPETIR -->

**Alternativas:** {{ALTERNATIVAS}} · **sustituciones por diversidad (9.7):** {{SUSTITUCIONES}} · **menos de N:** {{MENOS_DE_N}}

**Opciones añadidas por cobertura de eslabón (9.13, PV3):** {{OPCIONES_ESLABON}} (adicionales al top-N; `origen_seleccion = MEJORES_POR_ESLABON`) o «Ninguna». Si PV3 no se superó: «PV3 no superada: opciones indicativas, sin PRIORITARIO_PARA_C».

#### Ficha de cada candidato del top-N
<!-- REPETIR: ficha -->
**{{CAND_ID}} · {{NOMBRE}}** ({{TIPO_INSTRUMENTO}}, {{MERCADO}}, {{DIVISA}}) — {{VEREDICTO_CAND}}, S = {{S}}
- Rol en la tesis: {{ROL_EN_TESIS}}
- Pureza: {{PUREZA_METRICA}} = {{PUREZA_VALOR}} ({{PUREZA_FUENTE}}, {{PUREZA_METODO}})
- Señales de alerta: {{ALERTAS}} · exposición compartida: {{EXPOSICION_COMPARTIDA}}
- Objeciones y respuestas: {{OBJECIONES}}
- Motivo de SECUNDARIO (si aplica): {{MOTIVO_SECUNDARIO}}
<!-- FIN REPETIR -->
<!-- FIN REPETIR · tipos no aplicables: tabla «Tipo · motivo» -->

| Tipo no aplicable | Motivo |
|---|---|
| {{TIPO}} | {{MOTIVO}} |

## 11. Refutación y registro de contraste adversarial (F6)
Realizada por {{REALIZADA_POR}} (AG-B14 en N2/N3; autorrefutación en N1) · veredicto sobre la tesis **{{VEREDICTO_TESIS}}** · sobre los candidatos {{VEREDICTO_CANDIDATOS}}.

| Objeción | Objeto | Fuerza | Argumento | Qué la resolvería | Respuesta | Estado |
|---|---|---|---|---|---|---|
| {{OBJ_ID}} | {{OBJETO}} | {{FUERZA}} | {{ARGUMENTO}} | {{RESOLVERIA}} | {{RESPUESTA}} | aceptada · resuelta · incertidumbre abierta |

**Pre-mortem:** {{PRE_MORTEM}}

## 12. Mapa de cobertura de oportunidades (8.7)
- **Oportunidades directas:** {{DIRECTAS}}
- **Oportunidades indirectas:** {{INDIRECTAS}}
- **Perdedores sistemáticos y exposiciones a evitar** (nunca recomendación de venta): {{PERDEDORES}}
- **Investigado:** {{INVESTIGADO}}
- **Excluido con motivo:** {{EXCLUIDO}}
- **Vigilancia informativa:** {{VIG_INFORMATIVA}} · **vigilancia pre-salida a bolsa:** {{VIG_PRE_SALIDA}} · **emergentes no invertibles hoy** (EMG-B): {{EMERGENTES_VIGILANCIA}}

## 13. Plan de seguimiento (Vigía, B.11)
Vigente hasta {{VIGENTE_HASTA}} · frecuencia {{FRECUENCIA}} · régimen de referencia {{RGM}}.

| Señal | Serie HT-01 | Fluctuación | Revisión | Invalidación | Dirección | Cambio estructural | Afecta a |
|---|---|---|---|---|---|---|---|
| {{SIG_ID}} {{NOMBRE}} | {{SERIE}} | {{MIN}} – {{MAX}} | {{REV}} | {{INV}} | {{DIR}} | {{CRITERIO}} | {{AFECTA}} |

Condiciones de invalidación del ámbito: {{INV_AMBITO}} · de los candidatos: {{INV_CANDIDATOS}} · catalizadores: {{CATALIZADORES}} · pronósticos a resolver: {{PRG_RESOLVER}}.
El Vigía avisa al Broker por el Coordinador; nunca abre un análisis nuevo (R32). Un **seguimiento encargado** (CT-B-29, ciclos N1-SEG con informe de seguimiento, archivo F11) solo existe si el Broker lo encarga y es distinto del Vigía.

## 14. Limitaciones, lagunas, discrepancias abiertas y qué no sabemos
- **Limitaciones:** {{LIMITACIONES}}
- **Lagunas por dimensión:** {{LAGUNAS}}
- **Discrepancias abiertas:** {{DISCREPANCIAS}}
- **Qué podría salir mal:** {{RIESGOS}} (con mecanismo y señal temprana)
- **Lo que no sabemos:** {{LO_QUE_NO_SABEMOS}}
- Vocabulario: riesgo · incertidumbre · ignorancia · ambigüedad (8.9).

### 14 bis. Lista de comprobación profesional (8.10)
| Ítem | Estado | Dónde se trata o por qué no aplica |
|---|---|---|
<!-- REPETIR: lista_profesional -->
| {{ITEM}} | {{TRATADO / NO_APLICABLE / LAGUNA}} | {{REFERENCIA_O_MOTIVO}} |
<!-- FIN REPETIR -->

## 15. Historial de aciertos
Ventana {{VENTANA}} · ámbitos: {{HIST_AMBITOS}} · rankings: {{HIST_RANKINGS}} · **certificación: {{CERTIFICACION}}** (sin certificado: «sin ventaja demostrada todavía», R13).

## 16. Anexos de evidencia, cálculos y metodología
- Afirmaciones y evidencias (CLM-B → EVD-B), declaraciones de datos (DAT-B) y discrepancias (DSC-B): {{TRAZAS}}
- Artefactos del Motor reproducibles (CALC-B, con semilla y fecha de corte): {{ARTEFACTOS}} — detalle en el anexo de datos (hoja «Artefactos»).
- Fechas de los datos críticos: {{FECHAS_DATOS}}
- Metodología: Documento 0 del Bloque B V2.0; HT-03 (puntuaciones y ranking), HT-08 (tiempo), HT-09 (G3), HT-10 (anexo), HT-11 (universos).
- Preguntas sugeridas para consultas N0: {{PREGUNTAS_SUGERIDAS}}

---
*Análisis del Bloque B (Robot Investor). No constituye asesoramiento personalizado ni una recomendación de inversión: el Bloque B no conoce la cartera ni el perfil del inversor. El Broker Personal decide; los candidatos son encargos para los Bloques C.x, no valoraciones individuales. data_cutoff {{DATA_CUTOFF}}.*
