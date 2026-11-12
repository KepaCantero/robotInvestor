# T-101 · Bloque A V6: rediseño con núcleo común, kits y menos papeles de IA (aspirante)

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r02) |
| Pieza | `bloque_a/11_Ejecutor` (código vivo, fuera del corpus congelado) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (regla del operador del 12-11-2026) |
| Aprobación del operador | 2026-11-12: «analiza su revisión y decide si merece la pena tomar en consideración los cambios [...] También aprovecha para sumar alguna idea nueva [...] quiero que empieces a crear (en este caso sería modificar lo que ya existe) e implementar el bloque A completo» |
| Deuda técnica | T-101 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`; recoge PA-04, PA-06 y PA-07 (T-67) y la revisión C-01 de Astra |

## Objetivo

Construir en el ejecutor el Bloque A rediseñado: el de la propuesta de Claude (`.docs/diseno/bloque_a/propuesta_claude.md`), con los cambios de la revisión C-01 de Astra (`revision_astra.md`) que acepta la decisión de Claude (`decision_claude_c01.md`) y sus ideas nuevas. Se construye como **diseño V6 seleccionable** (`diseno: v6`), aspirante frente a la V5, por la decisión 1 de la tanda 1. Con el simulador se miden el flujo y el consumo; la calidad, en el modo sombra con la API real (Fase 5).

## Alcance

- **Entra** (todo con `diseno: v6`; con `v5`, el comportamiento y las 476 pruebas de hoy no cambian):
  1. **Analista de perfil:** núcleo común (el marco común V5.0 sin marcadores) más el kit del tipo de activo (identidad, §6, ejemplo de la §11 y, si la configuración lo pide, la §10), derivados al cargar los prompts V5.0. Caché por prefijo: el núcleo se comparte entre los doce analistas.
  2. **GC1 por código** antes del analista, con:
     - un catálogo mínimo de señales por perfil;
     - paso marcado de los ámbitos sin señal medible;
     - una rotación exploratoria sembrada para medir los falsos negativos.
  3. **Prospectiva una vez por ciclo,** en lotes por tamaño, con control de cobertura por identificador: un encargo que falta se pide una vez más en un lote aparte y, si sigue faltando, queda sin pronóstico declarado, nunca como pronóstico negativo.
  4. **Contradictor solo de la selección provisional y sus sustitutas** (A-01):
     - el orden es selección provisional, crítica y selección final;
     - una sustituta pasa la misma crítica;
     - lo que no se ha podido criticar no se entrega;
     - cliente propio para el segundo proveedor, cuando exista.
  5. **Sintetizador (AG-26),** después de G3, sobre el paquete validado: integración y textos en una llamada, y la segunda pasada de HT-09 valida el resultado. La integración previa a G3 es determinista.
  6. **Lector de evidencia (AG-28)** para CT-07 y CT-08 en el ciclo, y **Respondedor de consultas (AG-27)** para las consultas N0 de CT-03. Los tres prompts nuevos son cortos y viven en `11_Ejecutor/prompts_v6/`.
  7. **A código:** la curación (la IA queda opcional para la ablación), el dictamen G3 (sin llamar a AG-18) y el informe del Evaluador (las lecciones deterministas siguen).
  8. **Auditor por muestreo sembrado.**
  9. **Registro de cobertura** del embudo en HA y **muestreo de descartes,** con seguimiento contrafactual en el Evaluador.
  10. **Coste completo** por llamada (intentos y latencia) y **tope del tamaño de los prompts** por papel en la configuración, vigilado por una prueba.
  11. **Banco:** comparación de V5 y V6 con el simulador (llamadas, tokens, caché y coincidencia de la selección), en `.docs/scripts/`.
- **No entra:**
  - el corpus congelado (Documento 0, prompts V5.0, esquemas de `06_Plantillas_entregables`) y su re-congelado;
  - cambiar el diseño por defecto a la V6, que espera al banco con la API real;
  - mover funciones a I, K o al Orquestador del Broker;
  - contratar el segundo proveedor;
  - A-Forex y B.

## Diseño

- **Selección del diseño:** clave `diseno` (`v5` por defecto) y sección `v6` en `config/por_defecto.yaml`. Cada pieza tiene su interruptor para comparar un cambio cada vez.
- **Contratos:** ningún esquema cambia. Los mensajes CT se siguen registrando con los mismos identificadores. Matriz de propietarios en el §5 de `decision_claude_c01.md`.
- **Estado persistido:**
  - las entradas nuevas en HA: `COB-` (cobertura y muestra de descartes) y `CTF-` (contrafactual);
  - ningún archivo cambia de propietario;
  - los runs anteriores se leen igual.
- **Números:** todos salen de la configuración y son `[PROPUESTO]`, salvo los ya ratificados:
  - encargos por lote de Prospectiva;
  - rondas de sustitución;
  - celdas de exploración de GC1;
  - descartes muestreados;
  - fracción del Auditor;
  - topes de prompt.

  Van a la deuda (T-57).
- **Cómo falla cerrado:**
  - una candidata sin crítica no se entrega;
  - un ámbito sin señal no se descarta, pasa marcado;
  - un encargo de Prospectiva omitido queda sin pronóstico y declarado;
  - el Sintetizador no puede cambiar la selección, las puntuaciones ni las fechas (solo se toman sus textos), y HT-09 valida después.

## Criterios de aceptación (binarios)

1. CA-1: con `diseno: v5`, las 476 pruebas del bloque pasan sin cambios en sus expectativas.
2. CA-2: el prompt de un analista V6 es el núcleo más el kit. Con el kit completo, núcleo más kit contiene exactamente las secciones del prompt V5.0 original. El núcleo es idéntico para los doce analistas.
3. CA-3: en un ciclo V6 con varios tipos, Prospectiva se llama una vez por lote (no una por tipo) y cada encargo tiene resultado o queda declarado sin pronóstico.
4. CA-4: el Contradictor solo recibe opciones de la selección provisional o sustitutas. Si cae la mejor y entra la cuarta, la cuarta se critica antes de salir, y una opción sin crítica no se entrega.
5. CA-5: el Sintetizador se llama una vez, después de G3. Si devuelve una selección o unas cifras distintas, se ignoran, y la segunda pasada de HT-09 valida el paquete final.
6. CA-6: GC1 por código: el analista recibe como mucho `max_candidatas` ámbitos con señal, más la exploración y los ámbitos sin señal medible, todos marcados.
7. CA-7: el registro de cobertura da, para cada candidata del run, hasta qué fase llegó y por qué se quedó; los descartes muestreados se resuelven en el contrafactual cuando vence su horizonte.
8. CA-8: un ciclo V6 con los doce perfiles hace menos llamadas y lee menos tokens de entrada, con caché y sin ella, que el V5 con el simulador (cifras en `pruebas.md`), sin afirmar nada sobre la calidad. *(Reformulado el 12-11-2026 tras la QA r01, H-02: decía «lee más caché», pero la V6 lee menos caché porque envía menos tokens; su proporción de lectura es del 56 % frente al 66 % de la V5.)*
9. CA-9: el gate da 12/12, con A ≥ 476 más las pruebas nuevas, sin subir las cuotas de ruff ni mypy; no cambia el corpus.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Las 476 pruebas de hoy con `diseno: v5` | Regresión | CA-1 |
| `tests/test_t101_v6.py`: kits y núcleo | Unitaria | CA-2 |
| `tests/test_t101_v6.py`: ciclo V6 completo con el simulador (doce perfiles) | Integración | CA-3 a CA-7 |
| Sustitución forzada: el simulador refuta la mejor candidata | Límite | CA-4 |
| Omisión forzada de Prospectiva y Sintetizador que intenta cambiar la selección | Fallo cerrado | CA-3, CA-5 |
| `.docs/scripts/comparar_disenos_a.py` | Banco | CA-8 |
| `./tools/check_all.sh` | Gate | CA-9 |

## Registro

- 2026-11-12 · ABIERTO · creado con nuevo_ticket.sh, a petición del operador
- 2026-11-12 · EN QA · V6 implementada (`diseno: v6`, la V5 por defecto): 39 pruebas nuevas, A 515 en verde; ruff 3019 → 2987, mypy de A 114 → 109; banco con el simulador en `pruebas.md` (56 llamadas frente a 89 y 41 % de los tokens de entrada en dos ciclos con los doce perfiles)
- 2026-11-12 · NO APTO · QA r01 (revisor nuevo sin contexto, commit `16aa49e`): CA-7 y CA-8 sin cumplir; H-01, H-02, H-03, H-04, H-05 y H-11 medios; H-06 a H-10 bajos
- 2026-11-12 · EN QA · Ronda r02: corregidos H-01 a H-11 (CA-8 reformulado y registrado, H-02); 23 pruebas nuevas (62 en `test_t101_v6.py`, A 538)
