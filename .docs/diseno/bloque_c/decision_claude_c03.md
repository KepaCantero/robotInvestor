# Bloque C: decisión de Claude sobre la revisión C-03 de Astra y diseño de construcción

De: Claude, 15-11-2026. Responde a la revisión de Astra `revision_astra.md` (base `6a6cad5`) sobre mi propuesta `propuesta_claude.md`, ambas en esta carpeta, por encargo del operador: «analízalas y evalúalas una por una y decide qué incluir y qué excluir; incluye mejoras adicionales; guarda la información para cuando empecemos a construir cada bloque».

Estado: **DISEÑO ESTABLECIDO**, a falta de las decisiones del operador del §6. No se construye hasta que el operador lo ordene. Al construir, este documento manda sobre la propuesta donde la corrige.

## 1. Resumen

- **Se acepta la revisión entera.** Los siete veredictos de Astra son «de acuerdo con cambios», y los siete cambios se adoptan. Ninguno contradice la propuesta; la hacen más estricta.
- **Tres correcciones a mi propuesta:**
  - **N1 deja de ser un sobre invertible.** El Documento 0 del marco (§1) exige Contradictor antes de llegar a D. N1 es una criba: su sobre lleva `alcance: CRIBA` y D no lo usa para invertir. Para invertir hace falta N2 como mínimo.
  - **Las cifras de consumo (llamadas por nivel y coste por sobre) se retiran como compromisos.** Quedan como estimaciones sin medir; se miden con los kits construidos y se presupuesta por expediente, no por llamada.
  - **Citar evidencia no resuelve una objeción.** Lo propuse por analogía con A (T-66), pero allí la objeción era estructural. En C, una objeción semántica se resuelve por prueba determinista si existe, y si no, por revisión independiente.
- **C se construye como en A y B:** núcleo común más kits, con la mayor parte en código y variantes seleccionables comparadas en un banco.
- **Nueve ideas nuevas** (§4), casi todas aprendidas en la V6 de A y la V3 de B. Las más útiles:
  - la matriz campo → dato → método → validación → política si falta, que hace ejecutable el hallazgo 4 de Astra;
  - el sobre sin cifras libres;
  - el contrato de reutilización con envoltura nueva.

## 2. Veredictos de Astra

| Decisión | Astra | Claude | Cómo se aplica |
| --- | --- | --- | --- |
| Un Analista con kits | De acuerdo con cambios | **Se acepta** | Un kit es un **paquete verificable**, no un texto. Lleva el esquema del cuerpo especializado, los métodos del Motor, las fuentes de K, los casos adversos, los criterios de abstención y su versión. Un perfil pasa a ACTIVO solo después de su banco propio (idea 6). Si el banco lo justifica, se admiten instancias especializadas del mismo papel. |
| Cuatro papeles | De acuerdo con cambios | **Se acepta** | Son funciones, no un número fijo de llamadas. Reparaciones, varios documentos y rondas de objeción suman llamadas, todas con su tope en la configuración. Si falla el revisor (el Contradictor o un analista independiente), el análisis **no se degrada** a una revisión propia: el sobre queda sin revisión y no se puede invertir con él. |
| Tasa base Q y vista exterior | De acuerdo con cambios | **Se acepta** | El Motor calcula la tasa base sobre una cohorte y un horizonte **definidos antes de ver el resultado**, y los registra en el artefacto antes de calcular. Da el tamaño efectivo y la incertidumbre. Ser clase Q no basta para que una historia sea tasa base: sin cohorte, datos y método, `NO_ESTIMABLE`. |
| Combinación N3 y objeciones | De acuerdo con cambios | **Se acepta** | Solo se combinan pronósticos del **mismo evento y horizonte**. Las tesis incompatibles no se promedian: se conservan como escenarios y la divergencia se declara y baja el tope de confianza. Los pesos se congelan y se estiman fuera de muestra. Mientras haya poca muestra, pesos iguales, sin que eso dé confianza alta. |
| Niveles y carteras | De acuerdo con cambios | **Se acepta** | El nivel sale de importe, incertidumbre y **daño potencial**, por reglas de la configuración. N1 es criba (§1). Un N0 reutilizado no se salta la revisión de una decisión nueva: si cambió algo material, hace falta otra revisión. La vía sistemática de J conserva sus propios controles. |
| Orden DIV, IDX/FON, RV | De acuerdo con cambios | **Se acepta** | C-DIV primero, después C-IDX y C-FON (largo plazo en paralelo, L0) y C-RV como segundo perfil de verdad distinto antes de congelar CT-G-02 1.0.0. Una excepción al contador de bloques no lo es a los controles de seguridad. |
| No repetir B | De acuerdo con cambios | **Se acepta** | Se reutiliza la evidencia de B **identificada y vigente**, con la cobertura que B declara. Las conclusiones de B no se toman como dato. C revisa lo material para su propia tesis y repite lo invalidado. |

## 3. Hallazgos de Astra

| # | Hallazgo | Decisión | Cómo se aplica |
| --- | --- | --- | --- |
| 1 | Reutilización con contexto completo | **Se acepta** | La clave del registro de análisis vigentes (SC-5, T-87) lleva instrumento, vía, dirección, horizonte, mandato, versión del encargo, sello de K, kit, modelo, método, evidencia, informe del revisor y caducidad. Cualquier cambio invalida **solo las partes afectadas** (idea 3). Reutilizar no reenvía el sobre viejo: se emite uno nuevo que pasa R-01 a R-14 de `validar_encargo.py` y cita el original. En SC-4, ese pronóstico no cuenta como observación nueva. |
| 2 | Resolución sustantiva de objeciones | **Se acepta** | Tres estados distintos: `ABIERTA`, `RESUELTA_PRUEBA` (una comprobación determinista, con su identificador) y `RESUELTA_REVISION` (revisión independiente), más `ACEPTADA_OPERADOR`. Si cambia el sobre, la revisión se ata al hash final y se revalida. Una cita irrelevante es un caso adverso del banco. |
| 3 | Alcance por nivel | **Se acepta** | Corrección de §1: N1 es `CRIBA`. La validación final de SC-6 se repite tras la combinación de N3 y tras cualquier corrección, no solo antes del Contradictor. Quitar el Contradictor de algún nivel invertible exigiría aprobación expresa del operador; no se propone. |
| 4 | Prerrequisitos reales de C-DIV | **Se acepta** | Antes de construir C-DIV se escribe su matriz campo → dato → método → validación → política si falta (idea 1). Un dato material ausente impide promover el sobre, pero nunca para los controles de las posiciones que ya existen. Lo que K o SC-3 no tengan se declara y se pide a su bloque; no se improvisa en C. |
| 5 | Independencia y agregación | **Se acepta** | Se mide la correlación de errores entre analistas (misma evidencia, mismos supuestos) en el banco. El número de modelos no suma observaciones de calibración. Contra la contaminación (que el modelo reconozca el episodio), validación hacia delante con casos posteriores a su fecha de corte y una prueba de reconocimiento antes de usar un caso histórico. |
| 6 | Consumo no demostrado | **Se acepta** | Presupuesto por expediente, con salida máxima, reintentos, herramientas y rondas, reservado antes de cada intento (como B-1). La métrica es el **coste por sobre utilizable**. Las cifras de §7 de la propuesta quedan como estimaciones. N0 declara el coste de K y del Motor. |
| 7 | Perfil completo y conocimiento versionado | **Se acepta** | El esquema del cuerpo especializado y sus métodos existen antes de ACTIVO. El kit no carga toda la biblioteca: recupera referencias concretas por identificador (F7 a F9 de A son el modelo) y guarda su versión en el sobre. |

**Preguntas de la propuesta.** Se toman las respuestas de Astra a las seis. En la 4, el C-DIV del otro modelo, si se comparte, es material para contrastar con el banco; no bloquea el esqueleto ni se presume validado.

## 4. Ideas nuevas

1. **Matriz de cada perfil como fichero, comprobada por una prueba.** Una tabla por perfil con campo del sobre → dato de K → método de SC-3 → validación → política si falta (rechazo, parcial declarado o `NO_ESTIMABLE`). Una prueba falla si un campo obligatorio del cuerpo especializado no tiene fila, o si su método no existe en el Motor. Es la «tabla de obligaciones» de B aplicada a C.
2. **Sobre sin cifras libres (lección de T-102).** El Analista escribe el texto con marcadores de identificador (`{motor:ART-…}`, `{k:…}`) y nunca una cifra suelta. El código sustituye los marcadores por los valores del artefacto y un filtro frase a frase quita y declara cualquier cifra que no venga de un marcador. Así P3 («toda cifra del Motor») se cumple por construcción.
3. **Invalidación por dependencias, no por fechas.** Cada parte del sobre guarda de qué datos y artefactos depende. Cuando K publica una revisión o caduca un dato, solo se rehacen las partes que dependían de él. Es lo que hace barato el N0 y responde al hallazgo 1.
4. **Banco de tres variantes desde el principio.** Los mismos encargos con: solo tasa base (código puro, sin IA), C con un modelo y C con revisor de otro proveedor. Brier, cobertura de los intervalos, daño evitado y coste por sobre utilizable, con incertidumbre emparejada. Como en B, un empate por falta de potencia se declara como «todavía no se sabe».
5. **Torneo de pronósticos en sombra.** Mientras no haya dinero real, C emite y congela en SC-4 sub-pronósticos de 12 meses o menos sobre candidatos que B ya entregó. Se resuelven solos con la regla de A (T-91: fecha común, frescura por horizonte, festivos) y dan muestra de calibración antes de invertir.
6. **Activación de perfiles por banco, en la configuración.** Cada perfil tiene un estado (`BORRADOR`, `ASPIRANTE`, `ACTIVO`) y solo un ACTIVO produce sobres invertibles. Pasar de ASPIRANTE a ACTIVO exige su banco y la ratificación del operador, y se registra en el registro de experimentos (T-99).
7. **Lector de evidencia aislado, como en B.** Sin herramientas de escritura, sin cartera y con esquema cerrado: devuelve datos con fuente, fecha de publicación y etiqueta. Lo que lee no puede cambiar instrucciones (texto de terceros como datos). Se reutiliza el diseño de AG-B25.
8. **Consumo determinista y tope del prompt por papel (lecciones de T-88 y B-1).** Caché por prefijo con el núcleo común primero, reparto determinista de las escrituras compartidas, listas ordenadas antes de escribirlas y un tope de tokens del prompt por papel vigilado por una prueba.
9. **Variante seleccionable y vuelta atrás.** Cada pieza nueva se activa sola en la configuración y primero corre en sombra. Así un perfil o un papel que empeora el banco se apaga sin tocar código.

## 5. Diseño para construir

### Papeles de IA

| Papel | Qué hace | Cuándo | Modelo por defecto (`[PROPUESTO]`, lo decide el banco) |
| --- | --- | --- | --- |
| Lector de evidencia | Datos de documentos, con fuente y fecha, esquema cerrado | Solo si hay documentos | Haiku |
| Analista | Clase de referencia, desvío del caso, supuestos, invalidez medible, escenarios, probabilidad con plazo y criterio, con marcadores | Siempre salvo N0 | Sonnet; Opus como aspirante en N3 |
| Analista independiente | El mismo papel con otro modelo, sin ver el primero | N3 | Otro modelo o proveedor |
| Contradictor | Escenarios de fallo y revisión de la clase de referencia, sin ver el razonamiento | N2 y N3 (y N1 si el operador lo pide) | Otro proveedor cuando exista (decisión 2 de la tanda 1); hasta entonces, el mismo, declarado |

### Código

- **Orquestador:** nivel por reglas, presupuesto por expediente, llamadas, reanudación.
- **Registro de análisis vigentes (SC-5):** clave completa e invalidación por dependencias.
- **K:** datos con sello de corte.
- **Motor (SC-3):** tasa base con cohorte prerregistrada, estrés, factores, costes, liquidez y escenarios.
- **SC-6:** valida el sobre, una vuelta al Analista y después escala, también tras combinar y tras corregir.
- **Combinación N3:** por regla, solo del mismo evento.
- **Estados de las objeciones** (hallazgo 2).
- **Filtro de cifras libres** (idea 2).

### Orden de construcción, un ticket por paso

| Paso | Qué | Terminado cuando (binario) |
| --- | --- | --- |
| C-0 · Medida | Adaptador «c» del banco (`banco_medida.py`) y prerregistro; variante «solo tasa base» | El banco corre la variante de código puro con el simulador y deja informe |
| C-1 · Esqueleto | Orquestador de C, niveles, presupuesto por expediente, registro de vigentes con invalidación por dependencias, estados de objeción, filtro de cifras | Un N0, un N1 (`CRIBA`) y un N2 simulados de un perfil de prueba terminan con sobre válido en SC-6; reutilizar emite sobre nuevo que pasa R-01 a R-14 |
| C-2 · C-DIV | Matriz del perfil, kit, esquema del cuerpo especializado y casos adversos | Ningún campo sin fila en la matriz; banco de C-DIV ejecutado; perfil en ASPIRANTE |
| C-3 · Largo plazo | C-IDX y C-FON, casi todo código | Ídem, con comisiones, diferencia con el índice, réplica, domicilio y traspasabilidad del Motor |
| C-4 · C-RV | Segundo perfil distinto | Banco de C-RV; CT-G-02 listo para congelar 1.0.0 (lo congela el operador) |
| C-5 · Resto | Los demás perfiles, cuando una cartera los necesite | Cada uno con su matriz y su banco |

## 6. Qué decide el operador

1. Ratificar este diseño (sustituye a las preguntas 1, 3 y 5 de la propuesta, ya respondidas por Astra y aceptadas).
2. Si se comparte el C-DIV del otro modelo (D-02).
3. Las reglas de nivel (importe, incertidumbre y daño) y el presupuesto por expediente, `[PROPUESTO]` para T-57.
4. Cada paso de ACTIVO de un perfil.

## 7. Qué no se hace

- No se cambian la Constitución ni el marco común (`sistema_global/marco_comun_c/`) sin autorización. Los cambios a CT-G-02 o a los validadores pasan por su ticket.
- No se quita el Contradictor de ningún nivel invertible.
- No se afirma calidad ni coste sin medirlos: el simulador mide flujo y consumo; la calidad, el modo sombra con la API real.
