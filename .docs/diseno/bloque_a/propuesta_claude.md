# Bloque A: rediseño con menos agentes (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar todavía: el operador está decidiendo la arquitectura de los bloques. Copia en el repositorio del documento que el operador revisó con Claude.

Encargo del operador: revisar «si en la construcción del bloque A también has sido conservador».

## 1. Respuesta corta

Sí. En la revisión de A (T-53) se propuso pasar de 25 agentes a unos 6 papeles de IA con prompts de núcleo común más perfil corto (PA-06 y PA-07). Se aplazó hasta antes del modo sombra con API (T-67), y el trabajo posterior (T-65, T-66 y la auditoría de Astra en T-92) reforzó la estructura de 25 agentes en lugar de cambiarla. Ese trabajo no se pierde: es sobre todo código (contratos, almacén, evaluador, Motor, filtros de seguridad) y sirve igual con menos agentes; lo que cambia son los papeles de IA y sus prompts, que son datos.

Medido ahora con el cliente simulado y los doce perfiles activos: **77 llamadas a 20 agentes y unos 1,66 millones de tokens de entrada por ciclo; el 90 % son prompts de sistema.** Se propone la misma pauta que para B y C:
- **Seis papeles de IA:** Analista de perfil (uno, con kit por tipo de activo), Prospectiva, Contradictor de otro proveedor, Sintetizador, Respondedor de consultas rápidas y Lector de evidencia aislado.
- **El resto, código o servicios comunes:** coordinación, dictamen de G3, curación, auditoría, documentación y evaluación.
- **Primero el filtro barato:** GC1 por código decide qué tipos de activo tienen señal antes de llamar a un agente.

Estimación sin medir: unas 20 llamadas y 300.000–500.000 tokens por ciclo completo. Primero el banco de medida; cada recorte como aspirante frente al diseño actual.

## 2. Lo que hay hoy y lo que cuesta

Ciclo periódico C1 con el cliente simulado, datos sintéticos de ejemplo, as_of 2024-03-29 y los doce perfiles activos (`.docs/scripts/medir_consumo_a.py`, con un YAML que fija `perfiles.activos` a los doce):

| Agente | Modelo | Llamadas | Miles de tokens de entrada |
| --- | --- | --- | --- |
| Doce Analistas de tipo de activo | Sonnet | 24 (2 cada uno) | 593 |
| Hipótesis contrarias (AG-11) | Opus | 19 | 387 |
| Prospectiva (AG-10) | Sonnet | 12 | 291 |
| Curador (AG-12) | Haiku | 12 | 150 |
| Documentador para el Analizador (AG-14) | Sonnet | 6 | 128 |
| Analizador (AG-02) | Opus | 1 | 38 |
| Redactor (AG-17), Orquestador técnico (AG-18), Auditor (AG-19) | Sonnet | 1 cada uno | 21 a 28 |
| **Total** | | **77** | **1.662** |

Solo entrada y a precio de lista (Opus 4 $, Sonnet 2 $, Haiku 0,10 $ por millón; lectura de caché 0,05× y 0,1×; escritura de 1 h 2×): unos 3,9 $ sin caché, 2,3 $ con la caché actual y 2,1 $ cacheando solo lo que se repite. La salida no se mide en simulado.

En la Fase 1 solo está activo el perfil de divisas: 8 llamadas y unos 184.000 tokens por ciclo. Pero **cada perfil que se activa añade su analista con un prompt completo de unos 20.000 tokens, más su prospectiva, su curación y su refutación con Opus.** Además, la integración del Analizador no cambia la selección del top-3, que hace HT-03 por código (T-66, PA-14).

## 3. Dónde fue conservador

1. **Aplazar el cambio de papeles hasta tener llamadas reales.** El banco se puede montar ya con el simulador y datos congelados; entretanto cada corrección se hizo sobre 25 agentes que probablemente no sobrevivan.
2. **Un analista completo por tipo de activo**, cuando lo que cambia entre ellos cabe en un kit corto.
3. **Refutación con Opus por cada finalista, a veces en dos rondas** (19 llamadas por ciclo). A solo decide qué se estudia después; el contraste fuerte debe estar en C y D. En A basta con las finalistas que van a ser encargo.
4. **Agentes para reglas:** dictamen de G3 (ya es código en HT-09), curación, admisión y estimación.
5. **Funciones de otros bloques:** el Evaluador hace lo de I; los Documentadores, lo de K y los registros comunes.

## 4. El rediseño

| Papel | Qué hace | Modelo propuesto | Cuándo se llama | Sustituye a |
| --- | --- | --- | --- | --- |
| **Analista de perfil** | Criba, investiga y propone el encargo para B con el kit del tipo de activo | Sonnet; Haiku en seguimiento ligero | Una vez por tipo que pasa GC1 | Los doce Analistas |
| **Prospectiva** | Escenarios y pronósticos verificables de las finalistas | Sonnet | Una vez por ciclo para todas | Las doce llamadas de Prospectiva |
| **Contradictor** | Ataca la finalista con la evidencia, sin el razonamiento; una regla resuelve las objeciones (ya en T-66) | Otro proveedor si es posible | Solo finalistas que serán encargo, una ronda | Las 19 llamadas con Opus |
| **Sintetizador** | Integración entre tipos e informe en un texto | Sonnet | Una vez por ciclo | Analizador y Redactor |
| **Respondedor de consultas** | Consultas N0 con lo que ya está en memoria | Haiku | Bajo demanda | Parte del Coordinador |
| **Lector de evidencia** | Web y documentos aislado; datos con fuente y fecha | Haiku | Solo con fuentes externas | Buscador, parte del Documentador |

El Curador vuelve como papel de IA solo si la ablación pendiente (PA-14) demuestra que cambia la selección.

**Pasa a código:** GC1 sobre K (PA-04); admisión, prioridad, nivel, presupuesto y colas; dictamen de G3; curación; auditoría por muestreo con IA, por lotes y fuera del ciclo; planificación del Motor (agente solo para cálculos no estándar).

**Sale de A:** evaluación → I; mantenimiento de F7 a F9 → K y registros comunes, por lotes; orquestación → Orquestador del Broker.

**Un ciclo:** ciclo o petición → GC0 y GC1 (código) → un Analista de perfil por tipo con señal → Motor, curación y HT-03 (código) → Prospectiva (una llamada) → Contradictor (finalistas que serán encargo) → top-3 y G3 (código) → Sintetizador → encargos a B y registro (código). Con cuatro tipos con señal y tres encargos, unas 9 llamadas; con doce y seis, unas 20.

## 5. Precisión, consumo y migración

**Precisión.** A decide qué se estudia, no dónde va el dinero: se mide por si sus oportunidades acaban siendo buenas en B, C y D y por si se le escapan las buenas. Ya tiene backtest con fechas de corte, anonimización (PA-09) y ablación por ciclo (PA-14). El banco compara azar, solo código (GC1, Motor, HT-03), diseño actual y rediseño, con su coste.

| Ciclo | Llamadas | Entrada estimada | Hoy (medido) |
| --- | --- | --- | --- |
| Fase 1, solo divisas | 3 o 4 | 50.000–90.000 | 8 llamadas, 184.000 |
| Doce perfiles, cuatro con señal | Unas 9 | 150.000–230.000 | — |
| Doce perfiles, todos con señal | Unas 20 | 300.000–500.000 | 77 llamadas, 1.662.000 |

**El coste deja de crecer con cada perfil que se activa.**

| Paso | Qué se hace | Riesgo |
| --- | --- | --- |
| 0 | Banco de medida con simulador y datos congelados | Ninguno |
| 1 | Caché solo donde se repite, lotes, precios y tope en euros (PA-08) | Ninguno |
| 2 | A código: GC1 sobre K (PA-04), G3, coordinación, curación | Bajo |
| 3 | Núcleo común más kits (PA-07) | Bajo; se mide |
| 4 | Consolidar papeles uno a uno como aspirante (PA-06) | Medio; se mide |
| 5 | Sacar lo que es de I, K y el Orquestador | Ninguno |

## 6. Preguntas para el operador

1. Adelantar PA-06 y PA-07 ahora, empezando por el banco con el simulador.
2. Mientras tanto, las tareas de A del relevo de Astra (T-93, T-91 y T-88) se limitan a lo que sirve en cualquier diseño: código, contratos y seguridad, sin tocar prompts ni papeles.
3. Contradictor en A solo para lo que va a ser encargo.
4. La misma pauta para A, B y C.
