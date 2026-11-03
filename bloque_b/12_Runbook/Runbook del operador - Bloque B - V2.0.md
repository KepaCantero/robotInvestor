# Runbook del operador — Bloque B

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

> **Para quién es este documento.** Para el operador humano: la persona que instala, configura, pone en marcha, vigila, mantiene y despliega el Bloque B, y que actúa por cuenta del Broker Personal cuando este es una persona o un sistema que necesita apoyo técnico. Los agentes tienen sus system prompts; este runbook es tu manual. No repite lo que los prompts regulan: te dice qué hacer en cada situación y dónde mirar. No es fuente de gobernanza: ante discrepancia, manda el Documento 0 (jerarquía de 0.2).
>
> **Sobre la sintaxis de los comandos.** Los subcomandos del ejecutor son los fijados en el Documento 0 (18.4): `analizar`, `autorizar`, `consulta`, `decision`, `seguimiento`, `evaluar`, `estado`, `verificar-enlaces`, `backtest`, `generar-sinteticos`; desde la V2.1, `seguimiento` gestiona los **seguimientos encargados** por el Broker (CT-B-29, archivo F11) y el ejecutor añade `vigia` (la ronda del Vigía, que en la V2.0 se lanzaba con `seguimiento`) y `consulta-broker` (consultas del bloque al Broker y aportes, CT-B-28). Las opciones que aparecen en los ejemplos son las previstas; si el README de `11_Ejecutor` fija otra sintaxis, manda el README.

---

## 1. Panorama en una página

- **Qué hace**: bajo petición del Broker, analiza en profundidad un ámbito (sector, temática, mercado geográfico, segmento, estrategia o eslabón de cadena) y selecciona los mejores activos concretos por tipo de activo, con un encargo para cada Bloque C.x. Entrega seis piezas: informe técnico, informe visual, paquete JSON, memorando, anexo de datos y **mapa de oportunidades por eslabón** de la cadena de valor (entregable 6). Analiza **por capas** (0–4) con puertas de viabilidad PV1–PV3: si una capa muestra que no merece seguir, se detiene y entrega un **informe de parada**. Puede preguntar al Broker (CT-B-28) y ejecuta los **seguimientos periódicos** que el Broker encargue (CT-B-29).
- **Qué no hace**: nada sin petición o encargo de seguimiento del Broker; ni asesora al usuario, ni conoce su cartera, ni valora un activo individual en profundidad, ni usa datos en tiempo real o de pago no autorizados, ni ve claves API.
- **Quién es quién**: 24 agentes en cuatro planos (V2.1: AG-B24, Analista de Emergentes, Startups y Spin-offs). Tu interlocutor operativo en el bloque es el **Coordinador** (AG-B01, interfaz con el Broker) y, para calidad, tiempo y carga, el **Orquestador** (AG-B21, dueño de HA). El **Evaluador** (AG-B23) aprende y vigila (Vigía).
- **Dónde mirar**: F1 (todo lo que pasa con cada petición, incluidas puertas, paradas y consultas al Broker), F11 (seguimientos encargados y sus ciclos), HA (calidad, tiempo, incidencias, cola de tipo 3), F5 (lo aprendido, modelo de tiempos, certificados), F10 (configuración vigente), ENT (entregables).
- **La regla que más te afectará**: la **puerta de 30 minutos**. Si un análisis va a durar más de 30 minutos (estimación p80) o más de lo autorizado, se detiene en un punto de control seguro y pide autorización con una justificación, salvo que la política automática del Broker lo cubra; aun entonces, la justificación se registra y se notifica.

## 2. Instalación

### 2.1 Requisitos

| Elemento | Requisito |
|---|---|
| Sistema | Linux o macOS (Windows con WSL); Python ≥ 3.10 |
| Paquete del bloque | Carpeta completa `vB` (01_Gobernanza … 11_Ejecutor); el ejecutor lee prompts, plantillas, esquemas y F7–F9 desde la carpeta padre |
| Dependencias | Las de `11_Ejecutor/requirements.txt` (cliente de la API de Anthropic, validación JSON, cálculo numérico, YAML, generación de XLSX) |
| Clave de la API del modelo | Variable de entorno del sistema (nunca en archivos del bloque); solo para el cliente real |
| Almacenamiento | Directorio de estado persistente para F1–F6, F10, RC y HA (JSONL append-only) y directorio ENT; copia de seguridad diaria |
| Bóveda de HT-01 | Un gestor de secretos o almacén cifrado al que solo accede la capa de ejecución de HT-01 (sección 7) |
| Red | Acceso de salida a las fuentes gratuitas de F9 y a la API del modelo; en backtest, sin búsqueda web |

### 2.2 Pasos

```bash
cd vB/11_Ejecutor
pip install -e .                       # o: pip install -r requirements.txt
export BLOQUE_B_RAIZ="$(cd .. && pwd)"  # si mueves el ejecutor fuera del paquete
python -m pytest -q tests              # batería automática con el cliente simulado (sin red ni clave)
bloque-b generar-sinteticos --salida ./datos_sinteticos   # datos de prueba
bloque-b --cliente mock --datos ./datos_sinteticos --estado ./estado_prueba estado
```

**Verificación de la instalación**: la batería pasa; `estado` muestra 24 agentes con prompt cargado (ninguno en modo degradado), F10 con `methodology_version` 2.1 y la política de autorización vacía; `verificar-enlaces` sin `--aplicar` recorre F7–F9 sin modificar nada.

### 2.3 Modelos por agente

El YAML del ejecutor asigna un modelo a cada agente. Recomendación de arranque (compruébala con la documentación vigente del proveedor antes de usar el cliente real): modelo de mayor capacidad para el Director (AG-B02), el Seleccionador (AG-B12), Contrarias (AG-B14), el Auditor (AG-B22) y el Evaluador (AG-B23); modelo intermedio para especialistas, Prospectiva, Redactor, Documentadores, Buscador y Orquestador; modelo rápido para el Coordinador en N0 y el Curador. El Motor (AG-B16) es determinista en el ejecutor; su agente solo planifica peticiones de cálculo no estándar.

## 3. Configuración

### 3.1 Qué configura cada uno

| Qué | Quién | Cómo |
|---|---|---|
| Parámetros de servicio (política de autorización automática, tope de autorización automática ≤ 480 min, criterios de nivel AUTO, objetivos de tiempo por nivel, marco de invertibilidad, top-N, idioma) | Broker | CT-B-04 → Coordinador → F10 (régimen SERVICIO) |
| Parámetros calibrables (pesos, umbrales, matriz, caducidades, modelo de tiempos) | Evaluador, dentro de bandas | Automático, con sombra; tú solo vigilas (sección 10) |
| Parámetros del operador (umbral de 30 min, margen de la PTA, certificados, antigüedad de datos, conectores de pago, retención, numeración C.x) | Tú | Propuesta de tipo 3 aprobada y publicada (sección 10.5) |
| Ejecutor (modelos, rutas, zona horaria, modo vivo o backtest, precios por millón de tokens para estimar coste) | Tú | YAML del ejecutor |

### 3.2 Configuración inicial recomendada

1. **Política de autorización automática**: por defecto **ninguna** (todas las ampliaciones son manuales). Mantenla así las primeras semanas para observar las justificaciones. Después, propón al Broker reglas acotadas, por ejemplo: `POL-1` autorizar hasta 60 min si el origen es una oportunidad del Bloque A con siguiente paso ENVIAR_A_BLOQUE_B; `POL-2` autorizar hasta 90 min si la relevancia es ALTA; `POL-3` elegir «dividir en fases» si el p80 supera 120 min.
2. **Tope absoluto**: 240 min (inicial). Súbelo solo si las peticiones N3 lo exigen con frecuencia.
3. **Marco de invertibilidad**: el minorista europeo por defecto (UCITS con KID, mercados regulados, EUR). Cámbialo solo por petición del Broker.
4. **Conectores**: solo gratuitos. Los que requieren registro o clave gratuita quedan en `SIN_CREDENCIAL` hasta que el Broker los provea (sección 7).
5. **Zona horaria e idioma**: los del Broker (por defecto Europe/Madrid, es-ES).

### 3.3 Ejemplo de configuración de la política (CT-B-04)

```json
{"configuracion":{"politica_autorizacion":[
   {"regla_id":"POL-1","condicion":{"origen":"BLOQUE_A","siguiente_paso_A":"ENVIAR_A_BLOQUE_B","nivel":["N2"]},"accion":"AUTORIZAR_HASTA","minutos":60},
   {"regla_id":"POL-2","condicion":{"relevancia":"ALTA","nivel":["N2","N3"]},"accion":"AUTORIZAR_HASTA","minutos":90},
   {"regla_id":"POL-3","condicion":{"minutos_p80_min":120},"accion":"ELEGIR_OPCION","opcion":"DIVIDIR_EN_FASES"}],
  "tope_autorizacion_automatica_min":240}}
```

```bash
bloque-b --estado ./estado decision --json politica.json
bloque-b --estado ./estado estado --config      # comprueba POL-1…3 en F10 y el CFG-B registrado
```

Las reglas se evalúan en orden; se aplica la primera que cubre el caso. Un campo que no corresponde al régimen de servicio (p. ej., el umbral de 30 minutos) se rechaza con motivo y no se escribe.

## 4. Puesta en marcha

1. **Madurez documental**: Documento 0, 23 system prompts, funciones, esquemas de archivos, plantillas de entregables, herramientas, ejecutor, objetivos, plan de pruebas y este runbook presentes y en versión V2.0.
2. **Batería automática** (modalidad AUTO del plan de pruebas): ejecutada y aprobada; resultados en la sección 5 del plan.
3. **Piloto con datos sintéticos**: tres peticiones declaradas como ficticias (un N1 libre, un N2 desde un `paquete_para_bloque_B` y un N3 con PT30), con el cliente real; revisa F1, HA y ENT de extremo a extremo. Un piloto con incidencias Críticas o Materiales abiertas bloquea la puesta en marcha.
4. **Propuesta de activación (tipo 3)**: piezas y versiones, resultado del piloto, riesgos y plan de reversión. La apruebas o la rechazas.
5. **Publicación**: estado inicial limpio (F1–F6, RC y HA vacíos; F10 con el volcado del Anexo A; F7–F9 y FM tal como se entregan).
6. **Verificación posterior**: tras las cinco primeras peticiones reales, revisión de canales, matriz de escritura y tiempos estimados frente a reales.

Hasta superar la batería y el backtesting de rankings con datos reales, los componentes se declaran **documentados** o **implementados**, nunca **validados** (R26).

## 5. Operación de peticiones

### 5.1 Enviar una petición (CT-B-01)

Las peticiones las envía el Broker. Si actúas por él (pruebas, soporte), usa un archivo JSON con los campos de B.1:

```json
{"pet_ref_broker":"BRK-2026-118","origen":"LIBRE",
 "objeto":{"descripcion":"Empaquetado avanzado de semiconductores en Europa y Asia","tipo_objeto_sugerido":"CADENA_DE_VALOR",
   "ambito":{"incluye":"OSAT, sustratos, equipos de empaquetado","excluye":"diseño de chips","region":"GLB"}},
 "tipos_activo_admitidos":["RV","FON","RF"],"horizontes":["H3","H4"],
 "preguntas":["¿Persistirá el cuello de botella más allá de 2027?","¿Qué empresas europeas capturan valor?"],
 "nivel":"AUTO","limite":{"minutos":null,"uc":null},"prioridad":"NORMAL",
 "marco_invertibilidad":{"perfil":"MINORISTA_UE_DEFECTO","divisa_base":"EUR","ucits_requerido":true},"top_n":null,"alto_impacto":false,"idioma_usuario":"es-ES"}
```

```bash
bloque-b --cliente anthropic --datos DATOS --estado ./estado --salida ./ENT analizar --json peticion.json
```

**Una buena petición ahorra tiempo**: ámbito delimitado (incluye/excluye), tipos de activo admitidos, horizonte, preguntas concretas y, si viene del Bloque A, el `paquete_para_bloque_B` completo. No pidas un activo único (se devolverá con el Bloque C.x adecuado) ni consejo personal (se rechazará).

### 5.2 Ciclo de vida y dónde mirar

| Estado (F1) | Qué significa | Qué haces |
|---|---|---|
| RECIBIDA → ADMITIDA / RECHAZADA | Admisibilidad | Si RECHAZADA, lee el motivo y la reformulación propuesta |
| PLANIFICADA | Plan y estimación p50/p80 hechos | Revisa nivel y estimación en el acuse |
| EN_PAUSA_AUTORIZACION | p80 > 30 min (o > límite PERS) y la política no cubre | Decide (sección 6) |
| EN_CURSO | Ejecución por fases | `bloque-b estado --pet PET-B-…` muestra fase, minutos, UC y proyección |
| EN_PAUSA_PUNTO_CONTROL | Proyección de exceso en ejecución (PT30 o PTA) | Decide (sección 6) |
| EN_AUDITORIA | G3 y auditoría previa (F8) | Espera; un bucle largo es la auditoría trabajando |
| AUTORIZADA → ENTREGADA | Autorización de salida y entrega | Entregables en ENT; resumen en CT-B-02 |
| BLOQUEADO_AUDITORIA | Tres vueltas sin convergencia en algo material | Lee las opciones del CT-B-02 (sección 9) |
| CADUCADA · CANCELADA · DIVIDIDA | Sin respuesta en 7 días · cancelada · por fases | Lo hecho queda registrado y reutilizable |
| EN_PAUSA_CONSULTA (V2.1) | Consulta BLOQUEANTE al Broker pendiente (plazo 4 h) | Que el Broker responda: `consulta-broker responder` (sección 8 bis) |
| DETENIDA_EN_PUERTA (V2.1) | No superó PV1 o PV2; informe de parada entregado | Lee el informe; el Broker puede **forzar la continuación** en 7 días (sección 6 bis) |

### 5.3 Entregables

En `ENT/` con nombre `AAAA-MM-DD_tipo_PET-B-id`: `Informes técnicos Broker/` (pieza principal), `Informes visuales Usuario/`, `Paquetes JSON/`, `Memorandos ejecutivos/`, `Anexos de datos/`, `Mapas por eslabón/` (entregable 6: Markdown, copia .docx y JSON `mapa_cadena_valor`); además `Informes de parada/`, `Informes de seguimiento/` (`…_SEG-B-id_cNN`) y `Consultas al Broker/`. Comprueba en la portada del informe técnico el resultado del análisis (CONCLUYENTE, PARCIAL, NO_CONCLUYENTE, BLOQUEADO), las puertas de viabilidad, la continuación forzada si la hubo, los **supuestos aplicados** por consultas sin respuesta, las reservas de auditoría y los estados degradados. Recuerda: los candidatos PRIORITARIO_PARA_C son encargos para los Bloques C.x, no recomendaciones al usuario.

### 5.4 Paralelismo

Puedes lanzar varias peticiones a la vez: cada una tiene su propio Director, su plan y su puerta de tiempo, y ninguna usa conclusiones de otra en curso. Si dos peticiones son idénticas, la segunda se vincula a la primera. Si observas colas (sección 9), el Orquestador abre instancias de los agentes sin estado.

## 6. Autorizaciones (puerta de 30 minutos)

### 6.1 Cómo leer una solicitud (CT-B-05, AUT-B)

1. **Justificación**: qué aporta el tiempo adicional (dimensiones, tipos de activo, validaciones), qué incertidumbres reduce y **qué podría cambiar** (p. ej., «VIGILAR → INVERTIR_ESCALONADO»), y qué se perdería sin él. Si es genérica («para mayor rigor»), es un defecto: anótalo; el Auditor revisa estas justificaciones por muestreo.
2. **Lo hecho**: fases cerradas y conclusiones provisionales que ya pueden darse.
3. **Estimación nueva**: p50 y p80 hasta el final.
4. **Opciones**: continuar · versión ≤ 30 min (qué se recorta y el E y el veredicto máximos alcanzables) · dividir en fases · **avanzar hasta PV2** (`HASTA_PV2`, V2.1: solo capas 0–2, que suelen caber en 30 min; con el resultado de PV2 se vuelve a decidir) · cancelar. La estimación viene **por capa** y sobre el acumulado.
5. **Recomendación del bloque** y si la política la cubría.

### 6.2 Cómo decidir

| Situación | Opción razonable |
|---|---|
| La incertidumbre pendiente puede cambiar el veredicto o los prioritarios y la decisión del Broker es relevante | Continuar |
| Basta con una primera lectura o el plazo es corto | Versión ≤ 30 min (el alcance se recorta y se declara; los controles no) |
| Interesa el veredicto del ámbito ya y la selección después | Dividir en fases |
| No está claro que el ámbito merezca un análisis largo | Avanzar hasta PV2 (`HASTA_PV2`): si PV2 no se supera, recibes el informe de parada sin más consumo |
| La petición ha perdido interés | Cancelar (recibes un resumen de lo hecho) |

```bash
bloque-b --estado ./estado autorizar --aut AUT-B-2026-0004 --opcion CONTINUAR --minutos 70 --decidido-por BROKER
bloque-b --estado ./estado autorizar --aut AUT-B-2026-0005 --opcion DIVIDIR_EN_FASES --decidido-por USUARIO_VIA_BROKER
bloque-b --estado ./estado autorizar --aut AUT-B-2026-0006 --opcion HASTA_PV2 --decidido-por BROKER
```

El análisis se reanuda desde el punto de control: no se repite lo hecho. Sin respuesta, HT-05 envía un recordatorio a las 24 h y la petición caduca a los 7 días.

### 6.3 Reglas que no puedes saltarte

- El umbral de 30 minutos y el margen de la PTA (+10 % o +5 min) son parámetros del operador: se cambian solo por tipo 3, nunca por mensaje.
- Un N3 solicitado expresamente viene autorizado hasta el tiempo indicado (o 240 min), pero su justificación se registra igualmente.
- La versión ≤ 30 min **nunca** omite la validación G3 ni, en N2/N3, la auditoría previa: si el tiempo no da, el bloque recorta alcance o propone dividir.

### 6 bis. Puertas de viabilidad, informe de parada y continuación forzada (V2.1)

- **PV1** (fin de la capa 1): se detiene con un criterio eliminatorio (sin instrumentos invertibles, alerta grave de integridad, ficha de la Biblioteca con DESCARTAR sin cambio material) o con dos debilidades (materialidad, ya descontado, tesis sin mecanismo). **PV2** (fin de la capa 2): A o E provisional < 50 o tesis que no sobrevive a la autorrefutación (si solo falla E, antes llega una consulta al Broker). **PV3** (capa 3): si ningún eslabón cualifica, se entrega sin selección completa (VIGILAR como máximo) y el entregable 6 explica por qué.
- **Informe de parada** (`Informes de parada/`): por qué no merece seguir, qué lo cambiaría, sugerencia (DESCARTAR o PONER_EN_SEGUIMIENTO), lo que ya se sabe y el tiempo por capa. No trae candidatos.
- **Forzar la continuación** (solo el Broker, dentro de 7 días; nunca tras PV3): por CT-B-04 o respondiendo a una consulta. No se rebaja ningún umbral; los entregables lo declaran.

```bash
# CT-B-04 con {"forzar_continuacion": {"pet_id": "PET-B-2026-0009", "puerta": "PV1", "motivo": "tesis diferencial conocida"}}
bloque-b --estado ./estado --salida ./ENT decision --json forzar.json
# o al responder una consulta de confirmación tras PV2
bloque-b --estado ./estado --salida ./ENT consulta-broker responder --cns CNS-B-2026-0012 --respuesta "Seguid" --forzar-continuacion
```

Si observas paradas que luego resultan injustificadas, el Evaluador las mide como falsos negativos de las puertas (12.7) y propone ajustar umbrales dentro de bandas.

## 7. Credenciales

### 7.1 Principio

El bloque **solicita**; el Broker **provee**; la clave va **directamente a la bóveda de HT-01** por el canal seguro del ecosistema; los agentes solo conocen un **alias** (`credencial_ref`). Ninguna clave pasa por un mensaje, un archivo del bloque, un registro, un entregable, una conversación con un agente ni un orquestador externo.

### 7.2 Procedimiento

1. Llega una CT-B-06 (CRED-B en F1) con proveedor, finalidad, alcance (solo lectura), duración, alternativa y degradación sin clave, y urgencia (`BLOQUEA_PETICION` o `MEJORA_CALIDAD`).
2. Valora con el Broker si se provee: ¿es gratuita?, ¿el valor informativo es recurrente?, ¿hay alternativa pública suficiente? Las fuentes de pago no se solicitan sin tu autorización previa (tipo 3).
3. El Broker (o tú, con su autorización) da de alta la clave en el gestor de secretos de la bóveda con un **alias** acordado (p. ej., `alias-flujos-01`), con permisos de solo lectura y fecha de caducidad. Esta operación se hace con la herramienta de administración de la bóveda, **fuera** del ejecutor y de los agentes.
4. El Broker responde por CT-B-06 con estado `PROVISTA_EN_BOVEDA`, alias, caducidad y restricciones. El Coordinador comprueba el estado del alias en HT-01 y el conector pasa a `ACTIVO` en F10.
5. Revocación o rotación: se hace en la bóveda; el conector vuelve a `SIN_CREDENCIAL` y el bloque degrada y declara.

### 7.3 Si una clave aparece donde no debe

Es una **incidencia Crítica**: el mensaje se rechaza íntegro, la clave no se reproduce en ningún registro, el Orquestador abre INC-B y el Coordinador avisa al Broker. Tú: **revoca la clave en el proveedor de inmediato**, emite una nueva por la bóveda, comprueba con un barrido (búsqueda de la cadena en F1–F11, RC, HA, ENT y registros del sistema) que no quedó copia y documenta el cierre en HA.

## 8. Consultas, decisiones y alertas

```bash
bloque-b --estado ./estado consulta "¿Por qué la emisión X quedó como alternativa y no en el top-5?" --contexto REC-B-2026-0007
bloque-b --estado ./estado decision --json decisiones_PET-B-2026-0007.json   # CT-B-04: ENVIADO_A_C, EN_VIGILANCIA, DESCARTADO, valoraciones
bloque-b --estado ./estado vigia                                              # ronda del Vigía con fecha de corte de hoy (V2.0: «seguimiento»)
```

- **Consultas**: aclaración, dato, método o estado se responden en N0 (< 2 min) con referencias; si dice que una dimensión de la Biblioteca está caducada, tenlo en cuenta. Contraste y profundización devuelven una **propuesta de petición** (nivel, alcance, estimación): el bloque no la inicia por sí mismo.
- **Decisiones**: registran qué candidatos se enviaron a qué Bloque C.x; no cambian el análisis ni su evaluación. Si el Broker conoce la valoración de un Bloque C.x sobre un candidato, comunícala: es la mejor señal de la calidad de la selección.
- **Alertas del Vigía** (CT-B-07, comando `vigia`): REVISION (MEDIA), INVALIDACION_PROBABLE (ALTA, con petición N1 sugerida) e INVALIDACION_CONFIRMADA (ALTA). Ninguna abre un análisis: si el Broker quiere reanalizar, envía una petición nueva.

### 8 bis. Consultas del bloque al Broker y aportes (CT-B-28, V2.1)

El bloque puede **preguntar** al Broker (aclaración de alcance, dato o documento, preferencia o criterio, confirmación de un supuesto). Solo el Coordinador envía, tras el filtro del Director; cada consulta trae su **supuesto** si no hay respuesta. Límites por petición: N1 1 · N2 3 · N3 6 (bloqueantes: 1; N3: 2). Plazos: BLOQUEANTE 4 h (la petición queda `EN_PAUSA_CONSULTA`); NO_BLOQUEANTE hasta el inicio de F8 o 48 h. Al vencer, se aplica el supuesto y **todos** los entregables lo declaran. El Broker puede además enviar aportes en cualquier momento: el alcance y las preferencias vinculan; los datos y documentos se re-verifican (R31). Nunca incluyas claves, datos personales ni la cartera: el mensaje se rechaza íntegro.

```bash
bloque-b --estado ./estado consulta-broker listar                                   # pendientes y cerradas, con plazo y supuesto
bloque-b --estado ./estado --salida ./ENT consulta-broker responder --cns CNS-B-2026-0012 --respuesta "Solo bonos con calificación pública"
bloque-b --estado ./estado consulta-broker aporte --json aporte.json                # {"pet_id"|"seg_id", "naturaleza": ALCANCE|PREFERENCIA|DATO|DOCUMENTO, "contenido"}
bloque-b --estado ./estado --salida ./ENT consulta-broker revisar                   # vence plazos y aplica supuestos (HT-05)
```

### 8 ter. Seguimientos encargados (CT-B-29, archivo F11, V2.1)

Distintos del Vigía: solo existen si el Broker los **encarga**, se pueden modificar, pausar, reanudar y **cancelar en cualquier momento**, y cada ciclo (N1-SEG, objetivo < 10 min, ≈ 5 UC) entrega un **informe de seguimiento** de una página con semáforo (VERDE, AMBAR, ROJO) y recomendación (MANTENER_VIGILANCIA, REACTIVAR_ANALISIS_PROFUNDO, PROPONER_PASAR_A_C, CANCELAR_SEGUIMIENTO). Un ciclo **nunca** inicia un análisis profundo: si recomienda reactivarlo, propone la petición y el Broker decide. Máximo 25 activos; sin fecha de fin, recordatorio cada 6 meses.

```bash
bloque-b --estado ./estado seguimiento alta --json encargo.json        # {"objeto": {"tipo": "AMBITO_ANALIZADO", "rec_id": "REC-B-…"}, "frecuencia": {"tipo": "MENSUAL"}, "motivo": …}
bloque-b --estado ./estado seguimiento modificar --seg SEG-B-2026-0001 --json cambios.json
bloque-b --estado ./estado seguimiento pausar --seg SEG-B-2026-0001
bloque-b --estado ./estado seguimiento reanudar --seg SEG-B-2026-0001
bloque-b --estado ./estado seguimiento cancelar --seg SEG-B-2026-0001 --motivo "ya no interesa"
bloque-b --estado ./estado --salida ./ENT seguimiento ciclo --seg SEG-B-2026-0001   # ciclo manual
bloque-b --estado ./estado --salida ./ENT seguimiento pendientes                    # ciclos vencidos (lo que programa HT-05)
bloque-b --estado ./estado seguimiento listar                                       # estado, próximos ciclos y recordatorios
# decisión posterior del Broker sobre un ciclo: decision --json con {"decision_seguimiento": {"seg_id", "ciclo_id", "decision": MANTENER|REACTIVAR_PETICION|PASAR_A_C|CANCELAR|SIN_DECISION}}
```

## 9. Incidencias

| Síntoma | Dónde mirar | Diagnóstico probable | Acción |
|---|---|---|---|
| Petición en EN_PAUSA_AUTORIZACION que nadie decide | F1 (AUT-B), recordatorio de HT-05 | El Broker no recibió o no atendió CT-B-05 | Reenvía la solicitud; decide si estás autorizado; a los 7 días caduca sin coste adicional |
| Muchas PT30 en peticiones N2 | F1, F5 (MOD-B), HA (AVT-B) | Modelo de tiempos sesgado al alza o planes demasiado amplios | Revisa la cobertura del p80 en F5; si < 75 % o > 90 %, pide al Evaluador la reestimación; revisa el criterio AUTO |
| G3 BLOQUEADO repetido | HA (G3V-B, comprobaciones que fallan) | Defecto sistemático de un agente o de una plantilla | Guía del Orquestador; si es estructural, tipo 3 |
| BLOQUEADO_AUDITORIA | HA (AUD-B, vueltas, hallazgos) | Material sin converger en tres vueltas | Lee las opciones del CT-B-02 (petición nueva con otro alcance, N3, aceptar lo entregable con reserva si procede); nunca se edita lo bloqueado |
| HT-09 caído | HA (`modo` MANUAL) | Herramienta no disponible | El Orquestador valida manualmente y lo etiqueta; nunca APTO por defecto. Restablece la herramienta y relanza |
| Conector sin datos o fuente sin acceso | F10 (conectores), limitaciones del paquete | Caída, cambio de API o credencial caducada | El bloque degrada y declara; repara el conector o renueva la credencial |
| Instrucción incrustada detectada | F2 («Alertas de procedencia»), HA (INC-B MANIPULACION) | Fuente maliciosa o contaminada | Comprueba que no se ejecutó nada; el Buscador degrada o borra la fuente; registra el cierre |
| Datos personales en una petición | F1 (`MENSAJE_RECHAZADO`), HA | El Broker envió cartera o perfil | Recuerda al Broker la regla; no reenvíes el contenido |
| Clave fuera de la bóveda | HA (INC-B Crítica) | Error del Broker o fuga | Sección 7.3 |
| Colas por encima del umbral | HA (CAR-B, ORD-B) | Ráfaga de peticiones | Comprueba que el Orquestador abrió instancias de agentes sin estado; los de instancia única (Coordinador, Orquestador, Auditor, Evaluador) reordenan su cola; si se repite, tipo 3 |
| Vigía consume demasiado | HA (CAR-B de AG-B23) | > 150 REC-B vigentes o > 40 % del tiempo del Evaluador dos meses | Aprueba o rechaza la propuesta de tipo 3 de instancia propia del Vigía |
| Certificado revocado | F5 (CERT-B), Novedades | Deterioro de la habilidad | Nada que hacer: los entregables vuelven a bandas verbales; revisa en el trimestre |
| Fuga de información en una métrica | F5 (`comprobacion_fuga` FALLIDA) | Serie con revisiones o fecha mal declarada | Ningún ajuste ni certificado sobre ella; corrige la declaración de datos y deja recalcular |
| Enlaces rotos en masa | HA (MAN-B), HT-02 | Cambio de web de un emisor | Los Documentadores y el Buscador reparan o borran con registro; verifica el Registro de bajas |
| Mensaje por un canal no previsto | HA (INC-B CANAL_NO_PREVISTO) | Configuración o prompt defectuoso | Corrige la configuración del ejecutor; si viene de un prompt, guía o tipo 3 |
| Conflicto entre normas | HA (CNF-B) | Guía o parámetro en contradicción con el Documento 0 | Se aplica la regla más restrictiva; resuelve actualizando los documentos de forma coordinada |

**Escalados que te llegan siempre**: incidencias Críticas (seguridad, frontera, cifra inventada), propuestas de tipo 3, bloqueos por auditoría recurrentes, conflictos de normas y la revisión trimestral.

## 10. Mantenimiento

### 10.1 Diario

- `bloque-b estado`: peticiones en pausa, colas, incidencias abiertas.
- Revisa INC-B nuevas en HA y las autorizaciones pendientes en F1.
- Copia de seguridad del directorio de estado (los registros son append-only: una copia diaria permite restaurar sin pérdida).

### 10.2 Semanal

- `bloque-b verificar-enlaces` (barrido de HT-02, domingo): por defecto no modifica; los propietarios de F7–F9 deciden reparar, degradar o borrar.
- `bloque-b evaluar`: resolución de pronósticos y rankings vencidos (si no está programado).
- Revisa «Novedades» de F5, F7, F8 y F9.

### 10.3 Mensual

- Paquetes de mantenimiento del conocimiento (MAN-B en HA): cobertura ≥ 20 referencias verificadas por área, salud de enlaces ≥ 95 %, lagunas.
- Modelo de tiempos (MOD-B en F5): cobertura del p80 entre 75 % y 90 %.
- Revisión de sobreconfianza del Evaluador y del criterio de separación del Vigía.
- Barrido de claves trampa o de patrones de clave en archivos y registros (sección 7.3).

### 10.4 Trimestral (revisión programada, 18.2)

Con el Orquestador y el Evaluador: calibración y certificados; rendimiento de los rankings por playbook y horizonte; modelo de tiempos y **uso de la puerta de tiempo** (frecuencia, decisiones del Broker, política aplicada, desviaciones); carga y cuellos de botella; salud del conocimiento; separación del Vigía; ajustes en sombra (confirmar o revertir); cola de tipo 3; cuadro de mando de los objetivos (documento «Objetivos del Bloque B - Versión óptima V2.0», sección 6). Queda en HA como TRI-B.

### 10.5 Cambios de tipo 3

1. Llega una propuesta P3-B (del Orquestador, del Auditor o del Evaluador) con evidencia, impacto, pruebas de regresión y plan de reversión.
2. Comprueba que cita las pruebas de la batería de regresión del plan de pruebas (sección 7).
3. Aprueba o rechaza con motivo (queda en HA).
4. Si apruebas: actualiza de forma coordinada el Documento 0 y los prompts afectados, publica el valor en F10 (si es un parámetro), ejecuta la regresión y registra sus resultados en la sección 5 del plan de pruebas. Sin regresión registrada, el cambio no es vigente.
5. Un cambio mayor de metodología (2.x → 3.0) revoca los certificados vigentes.

### 10.6 Retención

F1–F6, RC y HA se conservan indefinidamente; artefactos del Motor y anexos de datos, 5 años; extractos de contenido externo, mínimos. Las únicas supresiones permitidas son las bajas de referencias de F7–F9 (con línea en el Registro de bajas) y la retención.

## 11. Despliegue

### 11.1 Entornos

| Entorno | Uso | Cliente | Datos | Búsqueda web |
|---|---|---|---|---|
| Pruebas | Batería automática, desarrollo | Simulado | Sintéticos | No |
| Preproducción | Piloto, regresión con modelo real | Anthropic o repetición | Reales gratuitos | Sí (solo agentes de conocimiento) |
| Producción | Peticiones del Broker | Anthropic | Reales gratuitos | Sí (solo agentes de conocimiento) |
| Backtest | Evaluación histórica de rankings y pronósticos | Anthropic o repetición | Históricos con «conocible desde» | **No** (fuga de información) |

### 11.2 Ejecución como servicio y tareas de fondo

- El ejecutor es un **proceso por petición** (CLI) o un **trabajador** de larga vida, según el despliegue. En ambos casos el estado vive en el directorio de estado (no en memoria) y los puntos de control permiten reanudar tras un reinicio.
- Las tareas de fondo se programan con el planificador del sistema (cron o temporizadores de systemd), **nunca** como análisis: `vigia` según las frecuencias del Vigía (al menos diaria), `evaluar` diaria, `verificar-enlaces` semanal (domingo); desde la V2.1, además `seguimiento pendientes` (al menos diaria: solo ejecuta los ciclos que el Broker encargó) y `consulta-broker revisar` (cada hora: vence plazos y aplica supuestos). HT-05 dentro del bloque decide qué toca en cada ronda.
- Secretos: la clave del modelo en una variable de entorno del servicio; las claves de proveedores de datos solo en la bóveda de HT-01.
- Registros del sistema: sin contenido de mensajes sensibles; rotación; los registros del bloque son F1–F11, RC y HA.

### 11.3 Actualizaciones y reversión

1. Nueva versión de prompts, herramientas o ejecutor → regresión mínima del plan de pruebas en preproducción.
2. Despliegue con el número de versión en F10 (`methodology_version` solo cambia si cambia la metodología).
3. Las peticiones en curso terminan con la versión con que empezaron.
4. Reversión: reinstala la versión anterior; los registros append-only no se tocan; si cambió un parámetro, la reversión es un CFG-B nuevo con `revierte_a`.

### 11.4 n8n como orquestador externo opcional

**Qué es y qué no es.** n8n puede usarse como **capa de integración externa** que mueve los mensajes del Broker al ejecutor y de vuelta, y que programa tareas de fondo. **No modela los agentes** del bloque, no reparte encargos, no decide autorizaciones, no ve claves y no es un canal nuevo: los 23 agentes, sus contratos internos (CT-B-08 a CT-B-27), sus puertas y sus archivos viven dentro del ejecutor. Para el Documento 0, n8n es parte del **transporte** entre el Broker y el Coordinador (CT-B-01 a CT-B-07); toda validación de esquema, idempotencia, seguridad y registro la hace el ejecutor.

**Formas de llamar al ejecutor como servicio.**

| Opción | Cómo | Cuándo |
|---|---|---|
| A · Línea de comandos | Nodo de ejecución de comandos de n8n en la misma máquina (o por SSH) que invoca `bloque-b <subcomando> --json <archivo>` y lee la salida JSON | Despliegue simple, un solo servidor |
| B · Envoltorio HTTP | Un servicio HTTP mínimo del operador delante del ejecutor que traduce cada ruta a un subcomando (p. ej., `POST /peticiones` → `analizar`; `POST /autorizaciones/{aut_id}` → `autorizar`; `POST /consultas` → `consulta`; `POST /decisiones` → `decision`; `GET /peticiones/{pet_id}` → `estado`) y responde con el JSON del ejecutor | Varios servidores, n8n en otra máquina. **El envoltorio no forma parte del Documento 0**: es infraestructura del operador; si se quiere como componente del bloque, es un cambio de tipo 3 |

**Patrón asíncrono obligatorio.** Un análisis puede durar de minutos a horas y detenerse en un punto de control. Por eso: (1) n8n envía la petición y recibe el **acuse en dos tiempos**: de inmediato, el acuse de recepción (PET-B, estado `RECIBIDA` o rechazo motivado) y, tras F0, el acuse de admisión con nivel, estimación p80 (calculada por el Coordinador con HT-08 sobre el grafo del Director), `requiere_autorizacion` y `aut_id`; (2) n8n **no espera** el resultado en la misma ejecución: o consulta el estado periódicamente (`estado`), o el envoltorio llama a un webhook de n8n cuando hay un mensaje saliente para el Broker (CT-B-02, CT-B-03, CT-B-05, CT-B-06, CT-B-07); (3) cada mensaje lleva su `msg_id`: si n8n reintenta, el ejecutor no duplica (idempotencia).

**Flujos de ejemplo.**

1. *Petición*: webhook del Broker → validación mínima de forma (sin interpretar contenido) → `analizar` → devolver el acuse al Broker.
2. *Mensajes salientes*: webhook «mensaje saliente» del envoltorio (o sondeo de `estado`) → enrutar según el contrato: CT-B-05 a la bandeja de autorizaciones del Broker; CT-B-02 con las rutas de ENT; CT-B-07 como alerta; CT-B-28 como consulta al Broker con su plazo; CT-B-29 de vuelta con el informe de seguimiento; CT-B-06 como tarea para el Broker de dar de alta la clave **en la bóveda** (n8n solo transporta el aviso, nunca la clave).
3. *Respuesta del Broker a una autorización*: webhook → `autorizar` con `aut_id`, opción y `decidido_por`.
4. *Tareas de fondo*: disparadores programados de n8n que llaman a `vigia` (diario), `seguimiento pendientes` (diario), `consulta-broker revisar` (cada hora), `evaluar` (diario) y `verificar-enlaces` (domingo). Es equivalente a cron.

**Reglas para n8n (no negociables).**

- **Nunca** programa ni dispara `analizar` sin un CT-B-01 del Broker (R5), ni da de alta un seguimiento sin un CT-B-29 del Broker (R35). Ningún disparador temporal ni ninguna alerta del Vigía puede convertirse en una petición automática: la petición sugerida por una alerta solo se envía si el Broker la confirma.
- **Nunca** decide autorizaciones: la política automática vive en F10 y la aplica el Coordinador. n8n solo transporta la decisión del Broker.
- **Nunca** maneja claves de proveedores de datos: el alta de credenciales se hace en la bóveda de HT-01. No guardes claves de datos en las credenciales de n8n ni las pases en nodos.
- **No** transforma el contenido de los contratos (más allá de envolverlo): cualquier campo añadido que altere límites o destinos se trata como tipo 3 y el ejecutor no lo aplica.
- **No** conserva contenido sensible: desactiva o limita el guardado de datos de ejecución en n8n, o purga periódicamente; las peticiones no deben contener datos personales y, si llegan, el ejecutor las rechaza íntegras, pero n8n no debe archivarlas.
- **No** llama a los agentes ni a la API del modelo directamente: solo al ejecutor.
- Tiempos de espera largos y reintentos con el mismo `msg_id`; alertas de n8n si un mensaje saliente no se entrega.

**Comprobación al integrar n8n**: repite con n8n en medio las pruebas PB-B-E2E-01, PB-B-E2E-19, PB-B-PT-01, PB-B-PT-09, PB-B-CRD-02, PB-B-CRD-03, PB-B-CTR-03 y PB-B-ADV-14 del plan de pruebas. Si alguna falla solo con n8n, el defecto está en la integración, no en el bloque.

## 12. Checklist rápido

- [ ] Instalación verificada (batería AUTO aprobada; 24 prompts cargados; F10 con versión 2.1).
- [ ] Política de autorización acordada con el Broker (o vacía de forma deliberada) y tope revisado.
- [ ] Bóveda operativa; ningún alias activo sin caducidad; barrido de claves limpio.
- [ ] Tareas de fondo programadas (`vigia`, `seguimiento pendientes`, `consulta-broker revisar`, `evaluar`, `verificar-enlaces`) y ninguna tarea que dispare `analizar`.
- [ ] Consultas al Broker sin plazos vencidos olvidados; peticiones `DETENIDA_EN_PUERTA` revisadas con el Broker antes de 7 días.
- [ ] Seguimientos encargados revisados (activos, pausados > 6 meses, sin fecha de fin).
- [ ] Copias de seguridad diarias del directorio de estado.
- [ ] Autorizaciones pendientes atendidas (ninguna a punto de caducar sin decisión consciente).
- [ ] INC-B abiertas revisadas; Críticas cerradas con evidencia.
- [ ] Cola de tipo 3 al día; regresiones registradas para lo aprobado.
- [ ] Revisión trimestral convocada con el dossier del Orquestador y del Evaluador.

## 13. Relación con el resto de la arquitectura

- **Broker Personal**: único interlocutor; tú das soporte a su relación con el bloque (política, credenciales, decisiones), nunca le sustituyes en sus decisiones sin su autorización.
- **Bloque A**: sus oportunidades llegan solo como `paquete_para_bloque_B` dentro de una petición del Broker; el contraste (qué se confirmó y qué se refutó) vuelve al Broker en el informe técnico, que puede trasladarlo al Bloque A.
- **Bloques C.x**: reciben del Broker los `paquete_para_bloque_C` de los candidatos que él elija. Mientras el operador no fije la numeración definitiva del Bloque C, se usa C.1 RV … C.12 TCV.
- **Fondo metodológico**: compartido por el ecosistema; el Documentador para el Director es su custodio en el bloque y los cambios se proponen, no se aplican desde el bloque.
