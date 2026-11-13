# Directrices para Astra: construir el Bloque B V3

De: Claude, 13-11-2026, por encargo del operador. El diseño está en `decision_claude_c02.md` (esta carpeta); estas directrices dicen **cómo** construirlo.

> **Antes de empezar:** hace falta que el operador asigne la tarea en tu cola (`.docs/tickets/_relevo/cola_astra.md`) y levante la congelación de `bloque_b/`. Sin las dos cosas no se toca nada. La publicación sigue la regla vigente de tu cola: en local hasta que el operador autorice subir.

## 1. Objetivo y cuándo está terminado

Construir en `bloque_b/11_Ejecutor` el diseño V3 como **variante seleccionable** (`diseno: v3`), con la V2.1 intacta por defecto (`diseno: v2`).

Está terminado cuando:
- un N1, un N2 y un N3 simulados terminan ENTREGADA con G3 APTO en V3;
- las mismas peticiones en V2 dan runs, llamadas y paquetes idénticos byte a byte a los de hoy;
- el banco de cuatro variantes (azar, solo código, V2.1 y V3) se ha ejecutado con el simulador y su informe está en el ticket;
- cada ticket de §4 ha pasado QA APTO, con el gate en verde (12/12) y las cuotas sin subir;
- las pruebas de B superan la línea base: hoy 176.

## 2. Lectura mínima

Para cada fase, lee solo esto y el encargo de esa fase, nunca todo el paquete (regla 1 del proyecto):
1. `decision_claude_c02.md` y tu revisión C-02 (`.docs/tickets/T-68/revision_astra.md`).
2. `bloque_b/README - Índice de la entrega del Bloque B V2.1.md`.
3. `bloque_b/08_Arquitectura/Arquitectura del Bloque B - Descripción detallada para LLM - V2.0.md`.
4. Del Documento 0 de B, solo los apartados que toque la fase. Para el plan, 8.3.1 a 8.3.4.
5. Como modelo de cómo se hizo en A, sin importar su código:
   - `bloque_a/11_Ejecutor/bloque_a/diseno_v6.py` y `bloque_a/11_Ejecutor/prompts_v6/`;
   - `.docs/diseno/bloque_a/decision_claude_c01.md`;
   - los tickets T-101 (V6), T-102 (filtro del Sintetizador), T-88 (consumo con hilos) y T-91 (resolución).

## 3. Reglas que no se negocian

- **Corpus congelado intacto.** No se tocan el Documento 0, los prompts V2.0, los esquemas de `06_Plantillas_entregables` ni el manifiesto. Los prompts nuevos van en «bloque_b/11_Ejecutor/prompts_v3/», fuera del corpus.
- **Ningún esquema de contrato cambia.** Si un contrato no encaja, para y pregunta: es una incidencia (`docs/incidencias.md`), no una decisión tuya.
- **Números solo en la configuración:** modelos, topes, lotes, rondas, umbrales y pesos. Si un número no está en el Anexo A o en el Catálogo, va a `config/por_defecto.yaml` marcado `[PROPUESTO]` y a T-57.
- **Mock antes que API.** Todo se valida con `--cliente mock`. La API real, solo en modo sombra y con autorización.
- **Sin mezclar bloques.** No importes código de `bloque_a/`. Lo que reutilices de A (por ejemplo, el filtro de T-102) se copia en B con sus pruebas y una línea de deuda para llevarlo a una biblioteca común más adelante.
- **Nada sale de B.** Evaluación, Vigía, documentadores y seguimiento encargado se quedan en B.
- **Auditoría previa al 100 % en N2 y N3.** No se sustituye por muestreo.
- **Falla cerrado.** Lo que no se puede comprobar no se entrega: se declara.
- **Repositorio público.** Sin secretos ni datos personales.
- **Flujo de trabajo:** cada ticket pasa por planificar → implementar → probar → QA, con las skills de `.agents/skills/`. La QA la hace Claude con un revisor nuevo.
- **Cierre de cada fase:** `./tools/check_all.sh` en verde (12/12) y cuotas de ruff y mypy de B iguales o más bajas.

## 4. Orden de trabajo: un ticket por paso

Cada ticket se abre con `nuevo_ticket.sh` y lleva su número de deuda. No empieces uno hasta que el anterior tenga QA APTO.

| Paso | Qué se construye | Criterio de terminado (binario) |
| --- | --- | --- |
| **B-0 · Medida** | Adaptador «b» en `.docs/scripts/banco_medida.py`, con prerregistro sellado en el registro de experimentos (T-99). Medición por petición y por intento: tokens de entrada y salida, caché escrita y leída, intentos, reparaciones y latencia. Consumo de referencia de redes, India y cobre como fixture. Prueba de «V2.1 sin cambios» | La prueba de V2.1 sin cambios pasa. El banco corre las variantes azar, solo código y V2.1 con el simulador y deja informe y prerregistro |
| **B-1 · Infraestructura** | Caché por prefijo, también en el simulador, con desactivación explícita (corregir que `ttl=""` añade `cache_control`). Reparto determinista de las escrituras compartidas (T-88). Presupuesto reservado antes de cada intento, con salida máxima y reintentos; límite global de peticiones concurrentes; parada en punto de control y reanudación. Lotes para evaluación, mantenimiento y backtests | Dos ejecuciones iguales con varios hilos dan el mismo consumo. Una petición que llega al tope para y se reanuda sin repetir trabajo. Con la caché desactivada no se envía ningún `cache_control` |
| **B-2 · Núcleo y kits** | Derivación mecánica del núcleo común (texto idéntico byte a byte) y de los kits de los analistas de dimensión y del Seleccionador, con el cierre de dependencias de sus playbooks. Prompts V3 del Analista de ámbito con módulos por fase | Prueba de reconstrucción: núcleo más kit dan las mismas secciones que el prompt V2.0. Ninguna referencia entre playbooks queda sin cargar. Cada papel cabe en su tope de tokens de la configuración |
| **B-3 · Código** | Director como máquina de estados, con el plan por la matriz 8.3.1 a 8.3.4, capas, PV1 a PV3, PT30 y PTA, pausas y reanudación idempotente. Admisión del Coordinador por reglas. Curador exacto. Registro de cobertura en HA. **Tabla de obligaciones** de los prompts del Director, el Coordinador y el Curador | Toda dimensión excluida queda en el mapa de cobertura con su motivo (R17). Una prueba falla si alguna obligación de la tabla no tiene dueño. Reanudar dos veces da el mismo resultado |
| **B-4 · Papeles V3** | Los nueve papeles de la decisión, §4, con su firma, detrás de `diseno: v3`: Analista de ámbito, Analista de dimensión, Seleccionador, Prospectiva, Contradictor (cliente propio), Lector de evidencia, Auditor, Sintetizador y Respondedor. Respuestas simuladas para cada uno | N1, N2 y N3 simulados terminan ENTREGADA con G3 APTO. Un sustituto de finalista pasa la crítica antes de entregarse. En N3, el desacuerdo de los dos analistas deja el veredicto más prudente y se declara |
| **B-5 · Sintetizador** | Marcadores de texto y textos sin cifras libres: las cuentas las escribe el código. El filtro frase a frase de T-102, copiado con sus pruebas y adaptado a los entregables de B (informe visual, memorando, mapa por eslabón) | El banco ciego de un revisor cumple los umbrales de INC-T102-01. Ninguna cifra que no esté en el paquete llega a un entregable |
| **B-6 · Medida y exploración** | Exploración sembrada de dimensiones condicionales no activadas. Muestra sembrada de descartes con seguimiento contrafactual. Banco con las cuatro variantes | Informe del banco en el ticket, que dice qué mide el simulador y qué no. Ninguna afirmación de calidad |

## 5. Detalles que suelen fallar

Lo aprendido al construir la V6 de A:
- **Cuentas.** Ningún marcador de cuenta en el texto libre: dos marcadores juntos componen cifras inventadas (T-102, H-42).
- **Orden de los hilos.** Todo lo que se escribe en F1 a F11 o en HA en el orden en que acaban los hilos se ordena antes de escribirlo (T-88).
- **Comentarios en diccionarios.** Un `#` en mitad de un diccionario de varias líneas deja fuera, sin aviso, lo que va detrás (T-88, H-10). Comprueba con una prueba las claves de cada registro.
- **Mutantes.** Las pruebas tienen que matar los mutantes de cada pieza nueva. Para mutar, usa un `git worktree` o una copia completa de `bloque_b`, nunca el árbol principal.
- **Resolución de pronósticos.** Se comprueba frente a la regla de A: fecha común más reciente, frescura por horizonte y festivos (T-91).
- **Vigía.** Comprueba qué parte del «criterio de cambio estructural» es determinista. Si alguna necesita juicio, queda con IA opcional por configuración y declarada.

## 6. Qué entregas en cada ticket

- `README.md`, `analisis-tecnico.md`, `pruebas.md` y los scripts de prueba en el ticket.
- Una entrada en el diario mensual y, si un número es nuevo, su incidencia `[PROPUESTO]` y su línea en T-57.
- En la entrega, di explícitamente:
  - qué no se ha probado;
  - qué cifra es una estimación;
  - qué queda en la deuda.
