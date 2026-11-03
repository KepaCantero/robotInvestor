# BLOQUE B — Analizador de Mercados y Seleccionador de Activos Candidatos · Versión óptima V2.1

**Robot Investor · Entrega del 03/11/2026 (actualización V2.1) · es-ES.** Sustituye al paquete V1.3 del propietario (31/10/2026). Ese paquete se conserva intacto en `99_Historico_V1.3`.

---

## 1. Qué hace el Bloque B

El Bloque B trabaja **solo bajo petición del Broker Personal**: una petición por propuesta, analizada de forma individual e independiente, y varias pueden ejecutarse en paralelo. Normalmente la propuesta procede del Bloque A o del Bloque A Forex.

Cada petición tiene dos partes:

1. **Análisis en profundidad del ámbito.** El ámbito puede ser un sector o subsector, una temática, un mercado geográfico, un segmento de una clase de activo, una estrategia o factor, o un eslabón de una cadena de valor. El análisis tiene la máxima exhaustividad y recorre **12 dimensiones**:
   1. definición del mercado;
   2. demanda y tamaño;
   3. oferta y costes;
   4. cadena de valor y competencia;
   5. tecnología;
   6. regulación y geopolítica;
   7. macro y ciclo;
   8. economía del sector;
   9. valoración y expectativas descontadas;
   10. flujos y sentimiento;
   11. sostenibilidad;
   12. riesgos y escenarios.

   El análisis termina en una tesis falsable, escenarios y proyecciones trazables, y un veredicto: `INVERTIR`, `INVERTIR_ESCALONADO`, `VIGILAR` o `DESCARTAR`.
2. **Selección de los mejores activos concretos** del ámbito para cada tipo de activo aplicable: empresas, ETF y fondos, bonos, ETC y futuros, REIT, criptoactivos… El bloque construye el universo invertible, lo criba y ordena los candidatos con una puntuación S cuantitativa e intervalos de incertidumbre. Para cada candidato prepara un **encargo para el Bloque C.x** de su tipo de activo. Los Bloques C.1…C.12 hacen después la valoración individual profunda.

**La estrategia de análisis cambia** según tres factores: el tipo de objeto (6 tipos), los tipos de activo implicados (12) y el horizonte. Esos tres factores determinan los pesos y la profundidad de cada dimensión, qué especialistas se activan, qué perfiles de cálculo usa el Motor y qué *playbook* de selección se aplica.

## 2. Tiempo, coste y autorización

| Nivel | Objetivo de tiempo | Uso típico |
|---|---|---|
| N1 Rápido | ≤ 10 min | Primera lectura |
| N2 Estándar | ≤ 30 min | Análisis completo habitual |
| N3 Exhaustivo | > 30 min | Requiere autorización |
| Personalizado | Lo fija el Broker | Tiempo o coste decididos por el Broker |

**Puerta de 30 minutos.** El bloque estima la duración antes de empezar y la vuelve a proyectar mientras trabaja. Si va a superar 30 minutos, **se detiene en un punto de control** y notifica al Broker:
- **Justificación argumentada:** qué aporta el tiempo adicional y qué se perdería sin él.
- **Opciones:**
  - continuar;
  - hacer una versión de 30 minutos o menos;
  - dividir el análisis en fases;
  - cancelar.

El Broker o el usuario deciden. El Broker también puede fijar una **política de autorización automática**. En ese caso la justificación se genera y se registra igualmente. No hay techo de coste, pero sí registro completo de tiempo y consumo.

## 3. Arquitectura: 24 agentes en 4 planos

- **P1 Interfaz:** Coordinador de Peticiones y Consultas. Es el único agente que habla con el Broker y gestiona:
  - las autorizaciones;
  - las claves API: las pide al Broker y van a la bóveda de herramientas, nunca al contexto de un agente;
  - las alertas del Vigía.
- **P2 Análisis:**
  - el Director del Análisis de Mercado;
  - **nueve especialistas por dimensión**: Estructura y competencia; Demanda y adopción; Oferta, costes y cadena de suministro; Tecnología; Regulación y geopolítica; Macro y ciclo; Finanzas y valoración; Flujos y sentimiento; Sostenibilidad y riesgos;
  - el **Analista de Emergentes, Startups y Spin-offs** (AG-B24, nuevo en V2.1): radar de empresas emergentes, startups, scale-ups, spin-offs universitarios y corporativos, salidas a bolsa recientes y SPAC, con su vía de exposición para el inversor;
  - el **Seleccionador de Activos**, con 12 *playbooks* de selección y las mejores opciones por eslabón de la cadena de valor;
  - Prospectiva y escenarios;
  - Hipótesis contrarias (equipo rojo sobre la tesis y sobre los candidatos);
  - Curador de evidencia;
  - **Motor de Cálculo Avanzado de Mercados**: propio del bloque, con los módulos MC-B01…MC-B10 y 106 fichas de cálculo;
  - Redactor.
- **P3 Conocimiento:** dos Documentadores y el Buscador de Fuentes Avanzadas.
- **P4 Calidad, aprendizaje y seguimiento:**
  - Orquestador técnico: validación G3 determinista, control de tiempo y autorizaciones;
  - Auditor: auditoría experta **previa a la salida**, obligatoria en N2 y N3;
  - Evaluador: pronósticos, evaluación de rankings, certificados y el **Vigía** de recomendaciones ya entregadas.

**Tareas de fondo permitidas:** vigilancia, evaluación y mantenimiento de referencias. **Nunca** se lanzan análisis nuevos sin petición.

## 4. Entregables (seis por análisis, más el informe de parada y el de seguimiento)

1. **Informe técnico exhaustivo** para el Broker.
2. **Informe visual** para el usuario novato (HTML).
3. **Paquete JSON**, con `candidatos_por_tipo`, `paquete_para_bloque_C` y `plan_de_seguimiento`.
4. **Memorando ejecutivo** de 1–2 páginas.
5. **Anexo de datos y cálculos** en XLSX y CSV, con todas las cifras, fuentes y artefactos.
6. **Mapa de oportunidades por eslabón de la cadena de valor** (nuevo en V2.1): por cada eslabón, sus métricas, si es cuello de botella (puntuación PCB), su atractivo (AE), una tabla con las mejores opciones invertibles y una subtabla de emergentes, startups y spin-offs con su vía de exposición. El informe visual del usuario incluye una versión simplificada de estas tablas.

Además:
- **Informe de parada**, cuando el análisis no supera una de sus puertas: explica por qué no merece seguir y qué lo cambiaría.
- **Informe de seguimiento**, en cada ciclo de un seguimiento periódico encargado por el Broker.

## 5. Inventario

| Carpeta | Contenido |
|---|---|
| `01_Gobernanza` | **Documento 0 V2.0**, especificación única del bloque: reglas R1–R32, matriz de estrategia, 12 *playbooks*, puntuaciones A/E/C/S y veredictos, puerta de 30 minutos, contratos CT-B-01…27, parámetros y precisiones operativas, esquemas JSON y taxonomías |
| `02_System_prompts` | 35 archivos: 24 agentes, 10 módulos del Motor y el Marco común de los Analistas de dimensión; cada prompt termina su base de conocimientos con un «Inventario de competencias» |
| `03_Funciones` | 24 fichas de funciones, tareas y cometidos |
| `04_Motor_conocimiento_y_catalogo` | Catálogo de cálculos (112 fichas, con desglose de la cadena de valor, cuellos de botella, potencial de emergentes, curvas S a décadas, hitos H5 y evaluación de puertas), perfiles de estrategia PERF-B y de selección SEL, y mapa de conocimientos |
| `05_Archivos_operativos` | **Referencias verificadas** (sección 6), Fondo metodológico compartido y esquemas de F1–F6 (F6 es la Biblioteca de mercados), F10, F11 (seguimientos encargados), RC y HA |
| `06_Plantillas_entregables` | Plantillas de los seis entregables y de los informes de parada y de seguimiento, esquema JSON y ejemplo que lo valida, capturas del informe visual |
| `07_Objetivos` | 152 objetivos medibles |
| `08_Arquitectura` | **Imagen de la arquitectura** (PNG y SVG) y descripción detallada para LLM |
| `09_Pruebas` | Plan de pruebas: 204 pruebas y 88 comprobaciones G3 (G3B-…) |
| `10_Herramientas` | HT-02, HT-03, HT-07, HT-08, HT-09, HT-10 y HT-11 (148 pruebas superadas) |
| `11_Ejecutor` | **Ejecutor Python** `bloque_b` (comando `bloque-b`), con la puerta de 30 minutos y puntos de control reales, política automática, bóveda simulada, cinco entregables, Vigía, evaluación y backtest de rankings. Incluye README para el ingeniero, ejemplos y 118 pruebas superadas |
| `12_Runbook` | Runbook del operador: instalación, operación, autorizaciones, credenciales, incidencias, despliegue y uso opcional de n8n como orquestador externo |
| `99_Historico_V1.3` | Paquete original del propietario, sin cambios |

Los archivos .md son los documentos canónicos; los .docx son copias de consulta.

## 6. Referencias verificadas (02–03/11/2026)

| Archivo | Áreas | Fichas | Mínimo por área |
|---|---|---|---|
| F7 Documentación para el Analizador de Mercados (TB-01…23) | 23 | 618 | 21 |
| F8 Documentación para el Motor de Cálculo Avanzado de Mercados (TMB-01…14) | 14 | 410 | 25 |
| F9 Registro de Fuentes para el Analizador de Mercados (TFB-01…19, fuentes gratuitas) | 19 | 443 | 20 |

Todas las fichas están verificadas por búsqueda web, ordenadas por calidad Q y clasificadas por área. Las fichas reutilizadas de los Bloques A conservan su ID; las nuevas llevan el prefijo MBA-, MBM- o MBF-.

Muchas fichas se confirmaron a través de páginas índice: bibliografías, listas de lecturas, RePEc y directorios oficiales. Figuran como `VERIFICADO_BUSQUEDA` y están pendientes de completar en el primer barrido automático.

## 7. Qué se ha conservado del V1.3 y qué ha cambiado

**Se conserva**, integrado y con nombres funcionales:
- las 12 dimensiones;
- el despliegue estructural de la cadena de valor;
- la máquina de proyecciones;
- la tesis falsable con hipótesis competidoras;
- el etiquetado epistémico;
- la auditoría previa a la salida;
- la regla de invertibilidad;
- las fichas de familia;
- los *playbooks* por horizonte;
- las fichas de régimen y de lección;
- el protocolo de discrepancias;
- el mapa de cobertura de oportunidades;
- REC-B y CT-B-xx.

**Cambia:**
- Topología: de 7 agentes con un Analizador monolítico se pasa a 23 agentes especializados.
- Motor propio en lugar del compartido «en transición».
- Selección de activos concretos.
- Puerta de 30 minutos.
- Credenciales gestionadas por el Broker.
- Aprendizaje medible con pronósticos congelados y evaluación de rankings.
- Biblioteca de mercados reutilizable.
- Referencias verificadas: antes no había ninguna; ahora hay 1 471.
- Ejecutor con pruebas.

**Se elimina** la estela de adendas, decisiones D-xx, «elementos en transición» y «estado de configuración».

## 8. Cómo probarlo

Las instrucciones están en `11_Ejecutor/README.md`. Con el cliente simulado se comprueba la tubería completa:
- puerta de 30 minutos y reanudación;
- los cinco entregables;
- validación G3 y legibilidad;
- Vigía;
- backtest de rankings sin *look-ahead*.

**No se mide capacidad analítica.** Para eso hacen falta ejecuciones con la API real y un backtest con datos históricos.

## 9. Decisiones pendientes del operador

1. Ratificar la numeración C.1…C.12 de los Bloques C, en el orden de los tipos de activo del Bloque A.
2. Ratificar los pesos iniciales de la matriz de estrategia, de las puntuaciones A, C y S, y de los *playbooks*. Son calibrables por el Evaluador.
3. Ratificar los umbrales de los veredictos:
   - INVERTIR: A ≥ 65, E ≥ 60, C ≥ 65.
   - Candidato prioritario: S ≥ 65 y extremo inferior del IC 90 % ≥ 55.
4. Fijar la política de autorización automática del Broker (por defecto no hay ninguna, salvo el tope absoluto de 240 minutos).
5. Revisar los parámetros de F10 marcados `PENDIENTE_OPERADOR`.


## 10. Actualización V2.1 (03/11/2026)

| Petición del propietario | Cómo queda |
|---|---|
| Tablas con las mejores opciones por eslabón de la cadena de valor, para el Broker y también en el informe del usuario | Entregable 6 «Mapa de oportunidades por eslabón»; tablas simplificadas en el informe visual |
| Conocimientos completos en cada agente | Auditoría de los 35 prompts de este bloque, con lo que faltaba añadido y un «Inventario de competencias» al final de cada base de conocimientos. La misma auditoría se ha hecho en los Bloques A y A Forex |
| Máxima profundidad profesional, emergentes, desglose de la cadena y cuellos de botella | Lista de comprobación profesional de 22 ítems del Director; agente nuevo AG-B24; desglose jerárquico macro-eslabón → sub-eslabón → actividad → nodo crítico; método cuantitativo de cuellos de botella con 11 indicadores y puntuación PCB; referencias nuevas TB-23 (40) y TFB-19 (24) |
| Análisis por capas; no seguir si una capa no se supera | Capas 0–4 con puertas PV1, PV2 y PV3. Si una no se supera, el análisis se detiene y entrega un informe de parada. El Broker puede forzar la continuación |
| Consultas de cualquier índole al Broker | Contrato CT-B-28, bloqueante (pausa en un punto de control) o no bloqueante (sigue con un supuesto declarado); el Broker también puede aportar información en cualquier momento |
| Proyecciones a distintos horizontes | H1 días · H2 semanas · H3 meses · H4 años · **H5 décadas**, con hitos intermedios verificables y horizonte principal declarado |
| Seguimiento periódico a elección del Broker y cancelable | Contrato CT-B-29 y archivo F11: alta, modificación, pausa o cancelación; cada ciclo es un análisis ligero de menos de 10 minutos con informe de seguimiento |

**Pruebas:** 148 en las herramientas y 118 en el ejecutor, todas superadas.
