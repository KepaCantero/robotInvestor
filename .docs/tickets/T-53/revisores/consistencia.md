# Revisión de coherencia especificación ↔ código · Bloque A (V5.1 / ejecutor «V1.2»)

Revisor independiente · 09/11/2026 · alcance: `/home/claude/repo/bloque_a/` (solo lectura; no se ha modificado ningún archivo del repositorio).
Scripts de apoyo en `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/rev_a_bloque/consistencia/scripts/`.

**Abreviaturas.** D0 = `01_Gobernanza/Documento 0 … V5.1.md` (las líneas citadas son de ese archivo). EJ = `11_Ejecutor/`. PKG = `11_Ejecutor/bloque_a/`. YAML = `11_Ejecutor/config/por_defecto.yaml`.
**Corpus congelado** (comprobado en `tools/corpus_manifest.txt`, 695 entradas): las carpetas 01–10, el README índice y 99_Histórico. **No** están congeladas: todo `11_Ejecutor/` (código, YAML, `tests/MAPA_PLAN_DE_PRUEBAS.md`, README del ejecutor). Ojo: `PKG/herramientas/referencia/*.py` debe ser copia byte a byte de `10_Herramientas/*.py` (`tests/test_unitarias.py:27-31`), así que tocar HT-03 o HT-09 toca el corpus.

## Resumen

28 desajustes: 1 de gravedad alta, 12 media y 15 baja. Los más importantes:

- **CS-01 (alta):** el ejecutor no hace caso del `horizonte_principal` ni de la `justificacion_horizonte` que declara el Analista. Elige él el horizonte y, si no encaja, cambia la naturaleza de la inversión. Así la regla de adecuación de 8.3 (C17 de HT-09) no puede fallar nunca.
- **CS-02:** los estados de CT-23/24/25 se contradicen dentro del propio D0, y el código pisa el estado común de retorno.
- **CS-03:** HT-08 trata como «con estado» a los cinco Analistas nuevos (AG-21 a AG-25).
- **CS-04:** el ejecutor manda en CT-06 valores de `fase` que no existen ni en el D0 ni en los prompts.
- **CS-05:** las bandas que se publican son 3, no las 5 del Anexo A.
- **CS-07:** dato nuevo sobre una trampa conocida. Las 21 fichas V5.0 **no** responden `METODO_NO_IMPLEMENTADO`, sino `OPERACION_SIN_FICHA` y sin alternativa.
- **CS-09:** el YAML valora `PLAN_STD` en 0,1 UC; el Anexo A dice 1 UC.
- **CS-10 y CS-11:** hay números del Anexo A escritos a mano en el código. Además, F10 solo publica 9 de los 44 parámetros.

### Comprobaciones sin desajuste (verificadas)

- **Agentes.**
  - `CatalogoPrompts` encuentra el prompt correcto de los 25 agentes. El H1 y el código AG de la cabecera coinciden en todos los casos.
  - No hay prompts duplicados.
  - Los prompts que no usa ningún agente son el Marco común (se usa como respaldo) y los 10 MC-xx (módulos del Motor, que no son agentes; el ejecutor no los carga).
  - Hay 25 fichas de funciones, una por agente (cruce por H1).
- **Propiedad de archivos.** Todas las llamadas a `almacen.escribir` (89 en total) usan el propietario de 5.1: F1 y F3 AG-02; F2 AG-12; F4 AG-10 (alta) y AG-20 (resolución); F5 y F11 AG-01; F6 AG-20; F10 AG-01 y OPERADOR; RC AG-13; HA AG-18. Ningún archivo se escribe por otra vía. Ver CS-22 para un matiz.
- **Canales.** `CANALES` (`PKG/contratos.py:39-66`) coincide con la tabla 6.1 en emisores y receptores de CT-01 a CT-25. La única excepción es el origen AG-16 de CT-25 (CS-13).
- **Tablas de horizontes.** `TABLA_HORIZONTES` y `NATURALEZAS` (`PKG/configuracion.py:33-49`) coinciden celda a celda con 8.3 (D0 l. 496-524).
- **HT-03.** Los pesos de 9.1, los umbrales de 9.2, RK 0,45/0,35/0,20 y los márgenes de 9.6 en `10_Herramientas/ht03_puntuaciones.py:57-81` coinciden con el D0. Las copias de `PKG/herramientas/referencia/` son idénticas (comprobado con `cmp`).
- **Escala de riesgo.** La escala 1-5 de RISK-DD-001 (`PKG/motor/operaciones.py:175-190`) coincide con la ficha del Catálogo (l. 694).
- **Valores del YAML que sí coinciden con el Anexo A:**
  - presupuestos N0 1, N1 5, N2 18, N3 50 y ciclo ≤ 240;
  - +25 %; 8 candidatas; 5 finalistas; GC1 0,75; GC0 1,5 σ y 10 %;
  - muestra 30/100; ECE 0,15; IC 90 %;
  - CT-23: 4 h, 24 h, 3 mensajes y 3 consultas en 8 semanas;
  - CT-25: 72 h, 7 días y 3 recordatorios;
  - frecuencias de CT-24 y orientativas;
  - C6: 2 / 5 / 0,5 UC;
  - hitos H5 a 12, 30 y 54 meses (cumplen «≤ 12» y «≤ 24 entre hitos»);
  - referencias de 8.4;
  - methodology_version 5.1.
- **Pruebas.** Todas las funciones `test_*` que cita el mapa existen (55 funciones, que dan 58 casos con la parametrización). La que se cita de `10_Herramientas` también existe (`test_seguimiento_envio_a_b`).

---

## Desajustes

### CS-01 · Alta · El horizonte principal y la naturaleza los decide el ejecutor, no el Analista; la regla de adecuación de 8.3 no puede fallar

**Dónde:**
- D0 8.3, l. 515-526: «Cada opción declara su `naturaleza_inversion` y su horizonte principal… fuera del rango… sin justificación → `BLOQUEADO`».
- D0 7.3 F2, l. 376: lo hace el Analista.
- Marco común de los Analistas, l. 37, y prompt de RV, l. 39 y 224: piden `naturaleza_inversion`, `horizonte_principal` y `justificacion_horizonte`.
- Código, `PKG/sintesis.py:201-206`:
  ```python
  nat = f.get("naturaleza_inversion") if … in NATURALEZAS else NATURALEZA_POR_DEFECTO.get(c, "CICLICA")
  hp = next((h for h in prefer if h in hz and naturaleza_coherente(nat, h)), None)
  if hp is None:
      hp = next((h for h in prefer if h in hz), sorted(hz)[0]); nat = naturaleza_para(hp)
  ```
  `sintesis.py:231` fija `"justificacion_horizonte": None`. El esquema `FINALISTA` (`PKG/contratos.py:257-298`) ni siquiera incluye `horizonte_principal`.

**Qué dice cada parte.** El D0 y los prompts dicen que el Analista declara el horizonte principal y que HT-09 bloquea lo incoherente. El código descarta el horizonte del Analista, lo elige con `horizonte_principal_preferente` (YAML l. 143) y, si ninguno cuadra, cambia la naturaleza para que cuadre. HT-09 C17 nunca ve un caso incoherente, y PB-65 solo se cumple en las pruebas unitarias de HT-09. El README del ejecutor (§9 bis) lo cuenta («si ninguno lo es, se ajusta la naturaleza»), pero no hay incidencia en `docs/incidencias.md`.

**Manda:** el D0.

**Corrección (código):**
- añadir `horizonte_principal` y `justificacion_horizonte` a `FINALISTA`;
- usar los valores del Analista y dejar que HT-09 dictamine;
- reservar el valor por defecto para cuando falte, y declararlo como limitación;
- registrar la decisión en `docs/incidencias.md`.

No toca el corpus.

### CS-02 · Media · Estado de CT-23/24/25: el D0 se contradice y el código pisa el estado común de retorno

**Dónde:**
- D0 6.2.6, l. 337: «el estado de su objeto… va en un campo propio (`estado_consulta`, `estado_seguimiento`, `estado_credencial`) y no sustituye al estado común de retorno».
- D0 Anexo B, l. 912, 921 y 927: los retornos usan `"estado":"RESPONDIDA|PARCIAL|VENCIDA"`, `"estado":"ACTIVO|…"` y `"estado":"PROVISTA|…"`.
- Prompt del Coordinador, l. 865-868: también usa `estado`.
- Código:
  - `PKG/contratos.py:22-26` y `:88` (`CAMPOS_RETORNO` con `estado`);
  - `PKG/seguimiento.py:65`: `crear("CT-24", …, r, …, estado="COMPLETO")` con `r["estado"]="ACTIVO"`;
  - `PKG/interfaz_broker.py:93` y `:224`, igual para CT-23 y CT-25.

  Como `Mensajeria.crear` hace `msg.update(cuerpo)` después de fijar `estado` (`contratos.py:187-190`), el estado común `COMPLETO` queda sobrescrito por el del objeto. El comentario de `contratos.py:22-23` reconoce la ambigüedad («el ejecutor admite ambos»), pero no hay incidencia.

  Además, el código admite `RECIBIDA` en CT-23 (`contratos.py:24`), un valor que no está en el D0.

**Manda:** el D0, 6.2.6 (es la regla). El Anexo B debe alinearse con ella.

**Corrección:**
- Documentación (corpus): usar `estado_consulta`, `estado_seguimiento` y `estado_credencial` en el Anexo B del D0 y en los ejemplos del prompt del Coordinador.
- Código: mover el estado del objeto a esos campos y validar `estado` solo contra `ESTADOS`.

### CS-03 · Media · HT-08 trata como agentes «con estado» a los cinco Analistas nuevos

**Dónde:**
- D0 4.5, l. 257: «Los agentes sin estado pueden ejecutarse en paralelo: AG-03 a AG-09, **AG-21 a AG-25**, AG-12…».
- Código, `PKG/herramientas/ht08_monitor.py:11-12`: `SIN_ESTADO = {"AG-03",…,"AG-09","AG-10",…,"AG-17"}`, sin AG-21 a AG-25. En `evaluar_instancias` (l. 47-57), un agente que no está en `SIN_ESTADO` solo genera `CAR-` y nunca una `ORD-` de apertura.

**Qué dice cada parte.** El D0 permite el escalado de IDX, FON, DER, MON y TCV. El código lo impide.

La lista de Analistas está repetida en cuatro sitios: `contratos.py:28`, `prompts.py:78`, `mock_respuestas.py:30` y `ht08_monitor.py:11`. Este último se quedó sin actualizar en V5.0.

**Manda:** el D0.

**Corrección (código):** construir `SIN_ESTADO` a partir de `contratos.ANALISTAS` más AG-10 a AG-17, y añadir una prueba con AG-21. No toca el corpus.

### CS-04 · Media · CT-06: el ejecutor envía valores de `fase` que no existen

**Dónde:**
- D0 Anexo B CT-06, l. 886: `fase` ∈ CRIBADO | INVESTIGACION | PROFUNDIZACION | SEGUIMIENTO.
- Marco común, l. 13, y prompt de RV, l. 15: la misma lista.
- Código:
  - `PKG/orquestacion.py:530`: `fase = "CRIBADO_E_INVESTIGACION" if nivel in ("N2","N3") else "REVISION_VIGENTES"`;
  - `PKG/orquestacion.py:732`: `"fase": "RESPUESTA_OBJECIONES"`.

  Solo `seguimiento.py:188` usa un valor válido (`SEGUIMIENTO`).

**Qué dice cada parte.** Los prompts, que son datos en tiempo de ejecución, reciben fases que no conocen.

**Manda:** el D0.

**Corrección (código):**
- `CRIBADO` o `INVESTIGACION` según la etapa;
- la revisión del arrastre como `CRIBADO` con `foco` de revisión;
- la respuesta a objeciones dentro de `INVESTIGACION`, o pedir al operador que amplíe el Anexo B (tipo 3, corpus).

### CS-05 · Media · Bandas verbales: se publican 3 en lugar de 5, y hay dos tablas distintas en el mismo módulo

**Dónde:**
- D0 Anexo A, l. 820: cinco bandas (Muy probable 80-95 · Más probable que no 60-75 · Incierto 45-55 · Poco probable 25-40 · Muy poco probable 5-20).
- Esquema JSON del paquete, `$defs.vista_horizonte.banda`: las cinco.
- Prompt de Prospectiva, l. 237: «Los huecos entre bandas… se asignan a la banda más cercana a 50 %».
- Código:
  - `PKG/evaluador.py:57-64` (`banda_publicable`, que usan `sintesis.py:164` y `:182`): solo «más probable que no / incierto / poco probable», con el comentario «esquema JSON del paquete, V4.0–V5.0: tres valores», que es falso para el esquema vigente;
  - `evaluador.py:26`: `BANDAS` (Incierto desde 0,45), sin usar e incoherente con `banda_de` (`evaluador.py:39-51`, Incierto si p > 0,40);
  - `banda_de` manda 0,21-0,24 a `MUY_POCO_PROBABLE`, en contra de la regla de prudencia del prompt.

**Qué dice cada parte.** Una probabilidad interna de 0,85 se publica como «más probable que no», y una de 0,15 como «poco probable».

**Manda:** el D0, el esquema y el prompt.

**Corrección (código):**
- una sola tabla de bandas leída del YAML (añadir una clave `bandas_verbales`);
- `banda_publicable` con los cinco valores;
- borrar `BANDAS`.

No toca el corpus.

### CS-06 · Media · Pronósticos H5: los hitos los fabrica el ejecutor, y a Prospectiva se le exige una probabilidad que el D0 prohíbe

**Dónde:**
- D0 Anexo A, l. 820 («salvo en H5, donde solo se registra la banda») y l. 846.
- D0 Anexo B CT-12, l. 896: la respuesta de Prospectiva trae «en H5, banda cualitativa y hitos HIT- con fecha, indicador y criterio».
- Prompt de Prospectiva, l. 89 y 125: los hitos se construyen por backcasting.
- Código:
  - `PKG/contratos.py:331-334`: el esquema `PROSPECTIVA` exige `prob_interna` (0,05-0,95) en todo pronóstico, H5 incluido, y no tiene campos `banda` ni `hitos`;
  - `PKG/orquestacion.py:697`: la instrucción pide «probabilidad interna (0,05–0,95)» sin excepción para H5;
  - `PKG/sintesis.py:143-165`: el ejecutor descarta la probabilidad y genera tres hitos mecánicos (rentabilidad del indicador a 12, 30 y 54 meses, con horizonte «H4»), sin usar los de Prospectiva.

**Manda:** el D0.

**Corrección (código):**
- esquema `PROSPECTIVA` con `banda` y `hitos` obligatorios en H5 y sin `prob_interna`;
- usar los hitos del agente, y dejar los mecánicos solo como respaldo declarado.

No toca el corpus.

### CS-07 · Media · Dato nuevo sobre una trampa conocida: las 21 fichas V5.0 no responden `METODO_NO_IMPLEMENTADO`

**Dónde:**
- `CLAUDE.md` (trampas): «Las 21 fichas nuevas V5.0… responden `METODO_NO_IMPLEMENTADO` con alternativa».
- Catálogo V5.0, l. 19: un DOCUMENTADO «responde `RECHAZADO` con motivo `METODO_NO_IMPLEMENTADO` y, si existe, ofrece la alternativa».
- Código, `PKG/motor/servicio.py:301-302`:
  ```python
  motivo = "METODO_NO_IMPLEMENTADO" if ficha in FICHAS_CATALOGO else "OPERACION_SIN_FICHA"
  ```
  `FICHAS_CATALOGO` (l. 25-34) solo tiene las 60 del índice V4.0 y `ALTERNATIVAS` (l. 35-38) no incluye ninguna V5.0.

  Ejecución real (script `motor_fichas_nuevas.py`): `FON-DISC-001 → RECHAZADO OPERACION_SIN_FICHA, alternativa None`; `FX-BRK-001 → RECHAZADO METODO_NO_IMPLEMENTADO`.

  Además, la frase de la trampa «el ejecutor implementa las 60» es inexacta: el ejecutor *conoce* 60 identificadores e *implementa* 17.

**Manda:** el Catálogo.

**Corrección:**
- Código: añadir las 21 fichas a `FICHAS_CATALOGO` (o leer el índice del Catálogo V5.0) y darles su alternativa del núcleo.
- Documentación no congelada: corregir la trampa de `CLAUDE.md`.

### CS-08 · Baja · El Motor entrega cifras con 3 fichas que el Catálogo da por DOCUMENTADO, y el README las cuenta mal

**Dónde:**
- Catálogo, l. 126, 135 y 141: ACC-ERP-001, FX-MOM-001 y REI-CAP-001 figuran como «Documentado».
- Catálogo, l. 23: «14 IMPLEMENTADO».
- README índice §5: «14 fichas implementadas; las 67 restantes responden "método no implementado"».
- Código, `PKG/motor/servicio.py:206-224`: `IMPLEMENTADAS` tiene 17 fichas, esas tres incluidas, que se sirven con normalidad.

El README del ejecutor (§9.3) lo reconoce, pero contradice la semántica de DOCUMENTADO del Catálogo («no entrega cifras citables»). En la práctica se rechazan 64, no 67.

**Manda:** el Catálogo.

**Corrección:** una de dos.
- Código: rechazar esas tres fichas con `METODO_NO_IMPLEMENTADO`.
- Corpus: promoverlas en el Catálogo (cambio deliberado) y corregir el README índice.

### CS-09 · Media · Valor en UC de un cálculo PLAN_STD

**Dónde:**
- D0 Anexo A, l. 823: «1 UC ≈ una llamada de agente de tamaño medio… **o un cálculo PLAN_STD**».
- F10, P-18: lo mismo.
- YAML, l. 124: `motor_por_plan: {PLAN_MIN: 0.02, PLAN_STD: 0.1, PLAN_EXT: 0.5}`, que usa `PKG/motor/servicio.py:298`.

**Qué dice cada parte.** El código valora un PLAN_STD en una décima parte de lo que dice el Anexo A. Esto falsea el consumo en F5 y los presupuestos. Es un número del Anexo A con régimen Operador.

**Manda:** el D0.

**Corrección (YAML):** `PLAN_STD: 1.0`, y reescalar MIN y EXT con criterio documentado. Si se mantiene, abrir una incidencia. No toca el corpus.

### CS-10 · Media · Números de reglas escritos a mano en el código

Los literales siguientes deberían salir del Anexo A, vía YAML o F10. En los casos marcados con (≠), además, no coinciden con el Anexo A.

| Literal en el código | Anexo A / fuente | Valor |
|---|---|---|
| `PKG/orquestacion.py:860`: `edad <= lim[h] + (2 if h == "H1" else 0)` (≠) | PS2, l. 816: H1 1 día (Operador) | En la práctica H1 tolera 3 días |
| `PKG/configuracion.py:53`: `ANTIGUEDAD_PS2 = {"H1": 1, …, "H5": 90}` | PS2, l. 816 | Igual, pero en el código y no en el YAML |
| `PKG/orquestacion.py:822`: `>= 2` raíces A/B o primaria A | PS1, l. 817 (Operador) | Igual, en el código |
| `PKG/evaluador.py:26`, `:39-64`, `:54` (bandas y probabilidades 0,85…0,15) | Bandas, l. 820 (Calibrable) | Ver CS-05 |
| `PKG/evaluador.py:292`: `len(v) >= 20 and … < 0.5` | Degradación H5, l. 847 (Calibrable) | Igual, en el código |
| `PKG/evaluador.py:422-434`: `delta = 0.05`, bandas `0.05` / `0.15`; `:429`, pesos RK de respaldo `{0.45, 0.35, 0.20}` | Pesos RK ±0,05 / ±0,15, l. 814 | Igual, en el código |
| `PKG/orquestacion.py:1359` (`weeks=4`) y `:1368` (`>= 3`) | Pregunta repetida, l. 832 (Calibrable) | Igual, en el código; CT-23 sí usa el YAML |
| `PKG/orquestacion.py:535`: `[:2]` celdas de rotación | Rotación exploratoria 20 % del presupuesto de cribado, l. 809 | (≠) Criterio distinto; `presupuesto_uc.rotacion_exploratoria` (YAML l. 114) **no se lee nunca** |
| `PKG/evaluador.py:173`: `{"replicas": 200, "simulaciones": 200}` | YAML `evaluacion.bootstrap_replicas` / `simulaciones_ece: 2000` | (≠) Ignora el YAML |
| `PKG/sintesis.py:112`: `{"H1": 5, "H2": 20, "H3": 126, "H4": 252, "H5": 2520}` | YAML `horizontes` | Duplica el YAML; si este cambia, divergen |
| `PKG/sintesis.py:291` (VERDE si n ≥ 2 o RK ≥ 70), `:79-84` (E < 70, RK ≥ 65), `:240` (E ≥ 70 ⇒ «probable») | Sin respaldo en el Anexo A; contradicen prompts (CS-17) | Inventados |
| `PKG/orquestacion.py:843`: `umbral_rho 0.7`, `ventana_semanas 104` | Ficha ML-CLUS-001 (CS-18) | 0,7 coincide; 104 no |
| `PKG/orquestacion.py:129`: `"SAB 06:00"` | Anexo A l. 803 solo dice «sábado» | Ver CS-16 |

**Manda:** el D0 (y la regla 2 del proyecto).

**Corrección (código y YAML):**
- llevar cada número a YAML o F10 con referencia a su fila del Anexo A;
- quitar el +2 de PS2 o documentarlo como incidencia.

No toca el corpus.

### CS-11 · Media · Parámetros del Anexo A fuera del YAML, F10 casi vacía y regímenes de F10 incompletos en el código

**Dónde:**
- **Umbrales y pesos.** Los umbrales de elegibilidad, GC2, los pesos de RK y los pesos de A/E/T/M/P no están en el YAML. Salen de `10_Herramientas/ht03_puntuaciones.py:57-81` (corpus) y solo se pueden sobrescribir con una clave oculta `_parametros_ht03` (`PKG/orquestacion.py:107`). Pasa lo mismo con `_tabla_horizontes` (`configuracion.py:144`). Los valores coinciden con el D0, pero la regla 2 del proyecto pide YAML.
- **F10.** El D0, l. 797, dice que los parámetros «se publican en F10». El esquema F10 (`05_Archivos_operativos/Configuración y parámetros… V3.0.md`, l. 57-100) define P-01 a P-44. `PKG/orquestacion.py:129-137` solo da de alta 9: P-01, 02, 03, 09, 11, 17, 29, 30 y 32. Comprobado en ejecución: `F10 keys: ['P-01','P-02','P-03','P-09','P-11','P-17','P-29','P-30','P-32']`. Además, `P-30` tiene como respaldo `"4.0"` (l. 136 y 147).
- **Regímenes en el código.**
  - `PKG/almacen.py:38-40`: `PARAMETROS_CALIBRABLES` no incluye P-35, P-36, P-39, P-40 ni **P-42** (degradación H5), que el esquema F10 marca CALIBRABLE. Por tanto AG-20 no podría aplicar la degradación (ver CS-12).
  - `PARAMETROS_SERVICIO` no incluye P-38 ni P-44. La limitación por credencial se escribe con `param_id` `SRV-…` (`interfaz_broker.py:241`).

**Manda:** el D0 y el esquema F10.

**Corrección (código):**
- mover a YAML una sección `parametros_ht03` explícita;
- dar de alta en F10 los 44 parámetros con su régimen;
- completar `PARAMETROS_CALIBRABLES` y `PARAMETROS_SERVICIO` según el esquema F10.

No toca el corpus.

### CS-12 · Media · La degradación de H5 se calcula pero no se aplica, y el mapa da PB-64 por «Superada»

**Dónde:**
- D0 12.2 y Anexo A, l. 847: la aplicabilidad baja un escalón.
- Plan de pruebas, PB-64 (l. 871-881): «Ajuste registrado en F6 y F10».
- Código: `PKG/evaluador.py:291-293` devuelve `"degradar": True/False`. Ningún módulo lo lee: el único consumidor de `estado_h5` es `seguimiento.py:314`, y solo para el estado del pronóstico. No se escribe nada en F6 ni en F10, y `_tabla_horizontes` no se actualiza.
- `EJ/tests/MAPA_PLAN_DE_PRUEBAS.md` (sección V5.1): «PB-64 Estado de los H5 por hitos | Parcial | `test_estado_h5_por_hitos` | **Superada**».

**Manda:** el D0 y el plan.

**Corrección:**
- Código: aplicar la degradación (F6 con evidencia y F10 P-31) y añadir P-42 a los calibrables.
- Mapa (no congelado): PB-64 como «Parcial: degradación no implementada», no como «Superada».

### CS-13 · Media · Las dudas para el Broker y las solicitudes de credenciales de los agentes no se recogen nunca; falta el canal de origen AG-16 → Coordinador

**Dónde:**
- D0 Anexo B, l. 855: campos comunes de retorno `consultas_broker` y `solicitudes_credenciales`.
- D0 7.9.1-7.9.2 (l. 438-439), 7.10.1 (l. 447) y 6.1 CT-25 (l. 324: «en origen: Analizador, o el Buscador de Fuentes Avanzadas directamente → Coordinador»).
- Código: `grep consultas_broker|solicitudes_credenciales` en PKG no da ninguna coincidencia de lectura. CT-23 y CT-25 solo se disparan desde la línea de comandos (`cli.py`, `interfaz_broker.enviar` y `solicitar`). `CANALES["CT-25"]` (`contratos.py:65`) solo modela Coordinador ↔ Broker.

**Qué dice cada parte.** El D0 describe un flujo agente → Analizador (filtro) → Coordinador → Broker. En el ejecutor ese flujo no existe, y el README del ejecutor no lo declara como limitación.

**Manda:** el D0.

**Corrección (código):** leer esos campos en los retornos de CT-05 y CT-06 y en el de AG-16, filtrar en AG-02 y pasarlos a `ConsultasBroker` y `Credenciales`. Mientras tanto, declararlo en el README del ejecutor y en una incidencia. No toca el corpus.

### CS-14 · Baja · `CAMPOS_MINIMOS` y los esquemas de respuesta no recogen todo el Anexo B

**Dónde:** `PKG/contratos.py:68-88`, frente al D0 Anexo B (l. 857-941). Campos que faltan en la validación:

| Contrato | Falta |
|---|---|
| CT-01 | `fecha_objetivo`, `nivel_forzado`, `referencia_previa` |
| CT-03 | Encargo: `contexto`, `urgencia`. Retorno: `escalado` |
| CT-04 | No tiene ninguna entrada |
| CT-23 | `preguntas`, `plazo_respuesta`, `punto_control` |
| CT-24 | Solo exige `accion`; el alta no exige `opp_id` ni `frecuencia` |
| CT-25 | Encargo: `herramienta`, `urgencia`. Retorno: `credencial_ref`, `caducidad` |
| `DICTAMEN_G3` (l. 378-382) | `comprobaciones`; el `enum` excluye `APTO` |
| `REFUTACION` | No exige `evidencia` |
| `INFORME_CLASE` | No exige `senales_para_otras_clases` ni `descartadas_relevantes` |

CT-11, CT-12 y CT-13 van agrupados (`piezas`, `encargos`, `peticiones`). Los elementos sí llevan los campos del Anexo B, pero la validación no lo comprueba. Varios de estos campos se rellenan en `interfaz_broker.py` y `seguimiento.py`, aunque no se validan.

**Manda:** el D0, Anexo B.

**Corrección (código):** completar `CAMPOS_MINIMOS` y `CAMPOS_RETORNO`. Es el objetivo de la Fase 3, «esquemas congelados para los CT».

### CS-15 · Baja · CT-22: nombre del campo de tipo y valores distintos en el D0, los prompts y el código

**Dónde:**
- D0 Anexo B, l. 904: «En CT-22, `tipo` admite además `CONSULTA_RECURRENTE` y `DECISION_SEGUIMIENTO`».
- Prompt del Evaluador, l. 98: `"tipo_aviso":"DECISION|VALORACION|RESULTADO_COMUNICADO|PREGUNTA_REPETIDA|CONSULTA_RECURRENTE|DECISION_SEGUIMIENTO"`.
- Prompt del Coordinador, l. 393: `tipo_aviso: PREGUNTA_REPETIDA`.
- Código: usa `"tipo": "PREGUNTA_REPETIDA"` (`orquestacion.py:1369`) y `"tipo": "DECISIONES_BROKER"` (`:1427`, un valor que no existe en el prompt), pero `"tipo_aviso"` en `interfaz_broker.py:164` y `seguimiento.py:133`.

**Manda:** el D0 para el nombre del campo. Los prompts lo contradicen.

**Corrección:**
- Corpus: alinear el D0 y los prompts en un solo nombre.
- Código: un solo campo y valores del `enum` del Evaluador (`DECISION` en lugar de `DECISIONES_BROKER`).

### CS-16 · Baja · `dia_hora_entrega` de CT-04: el ejecutor lo interpreta como hora de ejecución

**Dónde:**
- D0 Anexo A, l. 803: «ejecución el sábado, entrega el lunes 07:00».
- Anexo B CT-04, l. 880: `"dia_hora_entrega":"LUN 07:00"`.
- Código:
  - `PKG/orquestacion.py:1419`: P-01 = `periodicidad · dia_hora_entrega`, con respaldo `'SAB 06:00'`;
  - `PKG/herramientas/ht05_planificador.py:54-57`: `proxima_ejecucion(…, dia_hora="SAB 06:00")`, que trata ese valor como la hora de **ejecución**;
  - `orquestacion.py:129`: el valor inicial de P-01 inventa «SAB 06:00».

**Qué dice cada parte.** Si el Broker envía «LUN 07:00» como pide el Anexo B, el ciclo se ejecutaría el lunes a las 07:00, cuando debería entregarse a esa hora.

**Manda:** el D0.

**Corrección (código):** separar `dia_hora_ejecucion` (decisión del ejecutor, en el YAML) de `dia_hora_entrega` (servicio, P-01).

### CS-17 · Media · El semáforo, el `siguiente_paso_sugerido` y la confianza del código contradicen los prompts del Analizador y del Redactor

**Dónde:**

| Regla | Qué dice el prompt | Qué hace el código |
|---|---|---|
| Semáforo | Analizador, l. 419: «VERDE (≥ 1 opción con E ≥ 70 y A ≥ 65), ÁMBAR (… inciertas o marginales), GRIS (ninguna)» | `sintesis.py:291`: `"VERDE" if n >= 2 or rk_max >= 70 else "AMBAR"` |
| `siguiente_paso_sugerido` | Analizador, l. 443: `ENVIAR_A_BLOQUE_B` exige «E ≥ 70, sin objeción moderada abierta, catalizador dentro del horizonte» | `sintesis.py:79-84`: `PROFUNDIZAR_EN_A` si ALTA y E < 70; si no, `ENVIAR_A_BLOQUE_B` si RK ≥ 65. Puede proponer el envío al Bloque B con E entre 60 y 69 |
| Confianza | Redactor, l. 168: la barra de confianza usa E ≥ 80 / 65-79 / 60-64 | `sintesis.py:240`: `confianza = "probable" if E >= 70 else "especulativo"`, una tercera regla distinta |

El D0 (14.2, 7.8) solo da criterios cualitativos.

**Manda:** el prompt del Analizador (AG-02 es el dueño de F5 Selección, y el ejecutor «calcula» en su nombre).

**Corrección (código):** implementar las reglas del prompt con umbrales en el YAML. Si se prefieren las del código, el cambio toca el corpus (prompts).

### CS-18 · Baja · Clústeres de exposición: el umbral de correlación y la ventana no coinciden entre prompt, Catálogo y código

**Dónde:**
- Prompt del Analizador, l. 431: «misma apuesta si… su correlación es ≥ 0,6… (umbral inicial, calibrable)».
- Catálogo, ML-CLUS-001 (l. 677-679): «corte en ρ = 0,7 por defecto; Entradas mínimas ≥ 1 año diarios o ≥ 3 años semanales; ventana (1 año diario)».
- Código:
  - `PKG/orquestacion.py:841-843`: pide 2 años con `umbral_rho 0.7` y `ventana_semanas 104`;
  - `PKG/motor/servicio.py:125-130`: semanal, 104 semanas, y solo avisa si hay menos de 52 semanas.

**Qué dice cada parte.** El prompt dice 0,6 y el Catálogo y el código 0,7. Además, el código usa 2 años semanales, por debajo del mínimo de 3 años semanales del Catálogo, sin declararlo.

**Manda:** el Catálogo para el método. El prompt contradice al Catálogo.

**Corrección:**
- Corpus: alinear el prompt con el Catálogo.
- Código: 3 años semanales (o 1 año diario) y parámetros en el YAML.

### CS-19 · Baja · El mapa de pruebas está desfasado respecto del plan V3.0

**Dónde:** `EJ/tests/MAPA_PLAN_DE_PRUEBAS.md`.
- Título: «Mapa del Plan de pruebas V2.0»; l. 5: «Cobertura de las **52** pruebas del … V3.0». El plan (`09_Pruebas/Plan de pruebas… V3.0.md`) tiene **67** (PB-01 a PB-67).
- PB-53 a PB-57 (l. 728-791 del plan: frontera A/B, encargo completo, doce tipos, duplicada entre tipos, estrategias nuevas) no aparecen por su identificador. La sección V5.0 del mapa describe aspectos sin PB.
- La fila PB-12 dice «validación con el esquema JSON **V4.0**».
- La fila PB-13 cita el «Anexo A **V5.0**».
- 8 pruebas existentes no figuran por nombre: `test_casos_de_control_de_las_fichas`, `test_cli_backtest_y_estado`, `test_herramientas_de_referencia_sin_divergencia`, `test_ht05_fechas`, `test_mock_determinista_y_uc`, `test_referencias_reales_se_cargan_con_cualquier_version`, `test_score_rk_identico_a_ht03` y `test_sintetico_determinista`. Algunas aparecen descritas en prosa.

**Manda:** el plan.

**Corrección (documentación no congelada):** rehacer el mapa contra las 67 pruebas. Ver también CS-12 para PB-64.

### CS-20 · Baja · El Anexo A y el esquema F10 no coinciden en régimen ni en inventario (dentro del corpus)

**Dónde:**
- D0 Anexo A, l. 820: «Bandas verbales y probabilidad interna… | **Calibrable**». El esquema F10, P-33 (l. 89), dice «**OPERADOR**».
- Las filas del Anexo A «Escala de riesgo 1–5» (l. 821, Calibrable), «Presupuesto del mantenimiento continuo (C4)» (l. 829), «Relevancia decisional MEDIA / BAJA» (l. 833) y «Valores de liquidez» (l. 834) no tienen P-xx en el esquema F10.

**Manda:** el D0.

**Corrección (corpus, cambio deliberado):** corregir P-33 y añadir los cuatro parámetros al esquema F10.

### CS-21 · Baja · Versiones rancias: contratos en los prompts y textos del ejecutor (dato nuevo sobre INC-001)

**Dónde:**
- 22 ejemplos JSON de los prompts llevan `"version_contrato":"4.0"`: 12 en el Coordinador y 1-2 en el Analizador, Auditor, Buscador, Curador, Documentadores, Evaluador, Orquestador y Redactor (2). Solo 4 llevan "5.1". Sin embargo, el D0 (l. 855), el propio prompt del Coordinador (l. 96) y `contratos.py:20` dicen «5.1».
- `PKG/prompts.py:47`: el bloque que se **envía a todos los agentes en cada llamada** dice «Ejecutor programático del Bloque A (**V1.1**)».
- `PKG/prompts.py:68`: dice «Documento 0 **V5.0**».
- YAML, l. 1 («V1.1») y l. 98 («Anexo A del Documento 0 óptima V5.0»).

**Manda:** el D0.

**Corrección:**
- Corpus: ejemplos de los prompts.
- Código y YAML: cadenas de versión; puede ir junto con INC-001.

### CS-22 · Baja · El Evaluador escribe en RC suplantando al Motor y a Prospectiva

**Dónde:**
- D0 5.1, l. 279: el propietario de RC es AG-13, con «cada servicio… con artefacto reproducible».
- Código, `PKG/evaluador.py:117-123`: el módulo Evaluador hace `almacen.escribir("RC", "AG-13", {…, "solicitante": "AG-10", "operacion": {"method_id": "RI-TB", "ficha_id": "FC-EVAL-001", …}})` sin pasar por `Motor.servir`.

**Qué dice cada parte.** La reserva de escritura se cumple solo porque el autor se declara AG-13. El cálculo lo hace el Evaluador (AG-20) y se atribuye a AG-10.

**Manda:** el D0 (R6).

**Corrección (código):** calcular RI-TB con `self.motor.servir(…, "AG-20")`.

### CS-23 · Baja · Se cita un archivo de prueba inexistente

**Dónde:** `PKG/herramientas/__init__.py:4`: «la prueba `test_herramientas.py` comprueba que no divergen». Ese archivo no existe; la prueba real es `EJ/tests/test_unitarias.py:27` (`test_herramientas_de_referencia_sin_divergencia`).

**Corrección (código):** corregir el comentario.

### CS-24 · Baja · Parámetros del Anexo A sin ninguna implementación ni limitación declarada

| Parámetro | Situación |
|---|---|
| GC0 «dato macro con sorpresa > 1 desviación típica» (l. 810) | No aparece ni en el código ni en el YAML (`grep sorpresa` vacío) |
| Muestreo de auditoría «10 % consultas N0» (l. 827) | `orquestacion.py:1251-1259` solo muestrea AD_HOC; las consultas C3 no se auditan |
| «Respuesta esperada en 72 h» de CT-25 | YAML l. 165, `respuesta_esperada_horas`, no se lee nunca |
| Rotación exploratoria del 20 % | Ver CS-10 |
| Presupuesto C4 (l. 829) | No hay clave en el YAML |

**Corrección (código y YAML, o README del ejecutor):** implementarlos o declararlos como limitación.

### CS-25 · Baja · El cliente simulado no respeta el umbral GC1 que recibe

**Dónde:**
- YAML, l. 196: `umbral_senal_gc1: 0.75`, que se envía en el mensaje (`orquestacion.py:547`).
- `PKG/mock_respuestas.py:144`: `umbral = 0.55` fijo para el cribado normal; `:140` usa 0,75 fijo para el exploratorio.

Las pruebas «automáticas» de GC1 no ejercitan el valor configurado.

**Corrección (código):** usar `msg["umbral_senal_gc1"]`.

### CS-26 · Baja · Nombres de agentes: archivos, H1 y D0 no coinciden; las fichas no siempre citan su código AG

**Dónde:**
- **Prompts.**

  | Agente | Nombre en el D0 (4.2) y en el H1 | Nombre del archivo |
  |---|---|---|
  | AG-04 | «Analista de Renta Fija» | «… Renta Fija **y Crédito**» |
  | AG-07 | «Analista de Activos Inmobiliarios Cotizados» | «Analista Inmobiliario y de Infraestructuras» |
  | AG-09 | «Analista de Capital Privado y Activos Alternativos» | «Analista de Alternativos y Mercados Privados» |

  Las fichas de `03_Funciones` siguen el mismo patrón. El cargador lo resuelve con alias (`prompts.py:22`, `:25`, `:27`), así que hoy funciona.
- **AG-14.** El H1 del prompt y de la ficha dice «Documentador para el Analizador **de Tendencias de Inversión**»; el D0 4.2 dice «Documentador para el Analizador».
- **Fichas sin su código AG** en todo el texto: Prospectiva, Contrarias, Analizador, Auditor, Buscador, Curador, Documentadores, Evaluador y Orquestador (10 de 25).

**Corrección (corpus, opcional):** renombrar o añadir el código. Si no, dejarlo anotado como trampa conocida junto a «numeración F ≠ nombre».

### CS-27 · Baja · Esquemas JSON: patrones de identificador y versión no coinciden entre sí

**Dónde:**
- Esquema del paquete: `run_id` / `opp_id` / `prg_id` con `^…-[0-9]{4}-[0-9]{4,}$`.
- Esquema de seguimiento: `[0-9]{4,6}`. Un `OPP-2026-1234567` vale en el paquete y no en el seguimiento.
- El archivo «Esquema JSON - Paquete de oportunidades - **V5.0**.json» declara `$id …:paquete-oportunidades:**5.1**` y su descripción dice «Versión óptima V5.0».

**Corrección (corpus):** unificar los patrones.

### CS-28 · Baja · Decisiones del ejecutor sin respaldo en el D0

**Dónde:**
- YAML, l. 107: `ampliacion_max_autorizable: 0.50` (+50 % de tope), que usa `orquestacion.py:190`. El D0 (10.3, Anexo A l. 824) solo fija el +25 % sin autorización.
- HT-08 dimensiona con `c = ⌈cola/(umbral·0,75)⌉` y `instancias_max = 8` (`ht08_monitor.py:16`, `:49`). El prompt del Orquestador (l. 403) dice `c = ⌈λ/(μ·ρ_obj)⌉` con ρ_obj = 0,75 (ley de Little). Además, el criterio «tiempo > 2× el objetivo» (Anexo A, l. 825) no se evalúa.

**Corrección:** registrarlo en `docs/incidencias.md` y llevar los números al YAML. No toca el corpus.

---

## Evidencia reproducible

Scripts en `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/rev_a_bloque/consistencia/scripts/`:

| Script | Qué hace |
|---|---|
| `agentes_prompts.py` | Resuelve el prompt de AG-01 a AG-25 con `CatalogoPrompts` y comprueba el H1, el código AG, los huérfanos y los duplicados |
| `dump_schema.py` | Lista los `required`, `enum` y `pattern` de los esquemas JSON |
| `motor_fichas_nuevas.py` | Llama a `Motor.servir` con FON-DISC-001 y FX-BRK-001 (motivo de rechazo) y vuelca las claves de F10 y el valor de PLAN_STD |

Archivos auxiliares en la misma carpeta:
- `catalogo_estado.txt`: estado de las 81 fichas.
- `tests_existentes.txt` y `tests_mapa.txt`: cruce del mapa con las pruebas.
