# Relevo para un chat nuevo · estado al 13-11-2026

De: Claude. Para el chat nuevo de Claude que continúa el trabajo del 12 y 13-11-2026 (Bloque A: Motor Fase 1 y 2, V6, deuda técnica; diseño del Bloque B V3). **Este documento basta para arrancar.** Lo demás se lee solo cuando la tarea lo pida (regla 1 de `CLAUDE.md`). El relevo anterior (`2026-11-11_relevo_nuevo_chat.md`, misma carpeta) describe el sistema global, la Constitución y las 23 propuestas de diseño; consúltelo solo si la tarea es de esa parte.

## 1. Cómo arrancar (barato en tokens)

1. `git pull origin develop`. Último commit al escribir esto: `3a5fbfe` (o posterior: Astra puede haber subido tickets de C-37).
2. Lea este relevo. `CLAUDE.md` ya llega cargado. Lea `.docs/memoria/claude/INDICE.md` solo por las filas que toquen la tarea.
3. **No retome nada por su cuenta.** Pregunte al operador qué quiere hacer. Lo pendiente está en el §6.

## 2. Reglas que no se rompen (las del §4 del relevo del 11-11, resumidas)

- Al operador se le habla **en español y de usted**. Decide él; las decisiones nuevas van `[PROPUESTO]` y a T-57 (deuda técnica).
- **Repositorio público:** sin secretos (solo `.env`) ni datos personales. **El nombre del operador nunca se escribe en ficheros.** Claves falsas en pruebas, partidas (`"sk-" + "ant-…"`) para que no salte el gate `secrets`.
- **De `.docs/` no se borra nada:** lo viejo se marca.
- **No tocar** bloques, marco común (`sistema_global/marco_comun_c/`) ni la Constitución sin autorización expresa. Autorizado ahora: Bloque A (implementación completa, orden del 13-11) y `bloque_b/` **solo para Astra en C-37**.
- Los documentos de trabajo del operador en Claude son privados: no se leen salvo que la tarea lo exija y sus plantillas no se copian al repo.
- **QA por un revisor nuevo sin contexto** (skill `ri-qa`, con un agente nuevo). Solo el operador decide las tareas de Astra.
- **Una cosa cada vez:** nada de QA ni gates en paralelo (cargan la máquina y consumen el límite).
- **Límite semanal del operador:** él pidió parar al 94 %. El porcentaje exacto no se ve desde la sesión; si el aviso de límite aparece, avise y pregunte antes de lanzar algo caro (QA, gate completo). Se reinicia el lunes 16-11-2026 a las 21:00 CET.

## 3. Cómo se trabaja (lo práctico)

- **Gate:** `./tools/check_all.sh` (12/12). **Commit siempre con** `.docs/scripts/commit_limpio.sh "mensaje" ficheros…`: pasa el gate completo en una copia limpia (unos 30 min), hace commit de lo probado y sube. Lista de ficheros: `mapfile -d '' -t F < <(git ls-files -z -m -o --exclude-standard)`.
- Mensajes en español con prefijo (`motor:`, `docs:`…) y las dos líneas finales `Co-Authored-By` y `Claude-Session` que indique el sistema.
- Si el remoto rechaza el push (Astra subió algo): `git rebase origin/develop` y volver a subir.
- **Cuotas** (`tools/cuotas.txt`, solo bajan): ruff 2902 (se cuenta como el gate: `ruff check --output-format=concise … | wc -l`, no con `grep -c`), mypy A 109, FX 174, B 159. Pruebas: A 3693 recogidas (línea base del gate 607), FX 68, B 174.
- **Corpus:** si se cambia el Catálogo, `tools/corpus_integridad.py --update` en el mismo commit y con el motivo.
- Tickets: `.docs/tickets/T-NN/` (README, analisis-tecnico, pruebas, qa, revisores/). Incidencias: `docs/incidencias.md`. Diario: `.docs/diario/2026-11.md` (la entrada más nueva arriba). Deuda: `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`.

## 4. Lecciones de estas sesiones (no repetirlas)

- **Nunca** encadenar `open(p,"w")` y `open(p).read()` en una expresión: vació `diseno_v6.py` (se recuperó con `git show HEAD:<ruta>`).
- Los **mutantes** se hacen en una copia o `git worktree`, nunca en el árbol principal.
- Un `#` a media línea en un diccionario de varias líneas puede dejar fuera una clave sin aviso (T-88 H-10): probar las claves de cada registro.
- Todo lo que escriben varios hilos se **ordena** antes de escribirlo (T-88).
- Filtros por regex sobre texto libre no convergen: frase a frase, con listas de K, y las cifras las escribe el código.
- Al insertar un método antes de otro decorado, el decorador pasa al nuevo: insertar por encima del decorador.
- Una caché debe incluir en su clave todo lo que cambia el resultado (la fecha de corte faltaba: T-112 r02).
- No comparar semillas con un `set`: una no hashable rompe `servir`.

## 5. Estado al 13-11-2026

### Bloque A (`bloque_a/11_Ejecutor`)

| Ticket | Qué | Estado |
| --- | --- | --- |
| T-88 | Consumo determinista con hilos | CERRADO |
| T-91 | Resolución de pronósticos (fecha común, frescura por horizonte, festivos) | CERRADO |
| T-101 | Diseño V6 aspirante (`diseno: v6`), V5 por defecto | CERRADO |
| T-102 | Filtro del Sintetizador V6 (operador: «umbrales y sin cifras libres») | CERRADO |
| T-106 | Motor Fase 1: 21 fichas V5.0 (IDX, FON, DER, MON, TCV) | CERRADO |
| **T-112** | **Motor Fase 2: 35 fichas P0/P1 en `motor/fichas_series.py`, `fichas_riesgo.py`, `fichas_valoracion.py`, `fichas_reales.py` + AUD-REX-001 (CT-10). Catálogo: 71 IMPLEMENTADO, 10 DOCUMENTADO (las P2)** | **EN QA: r02 hecha (commit `ea52b1e`), QA r02 pendiente de la orden del operador.** Detalle en `.docs/tickets/T-112/analisis-tecnico.md` («Ronda r02») e INC-T112-01/02 |
| **T-113** | **Toda la deuda técnica de A (T-104, T-107, T-108, T-109, T-110), 57 pruebas nuevas** | **EN QA: QA r01 pendiente de la orden del operador** (commit `3a5fbfe`). INC-T113-01 |

Claves del Motor (`motor/servicio.py`): `MODULOS_FASE1/2`, `ESTRICTAS = FASE1 | FASE2` (sin no finitos), `ACEPTA_SEMILLA`, `SOLICITANTES_FICHA` (BIB-MET-001 solo AG-18 y AG-20), `SERVICIOS_CT10 = {"AUD-REX-001"}`, `_contexto` (añade configuración y fecha de corte a `ent`), `_error_de_forma`; `MemoryError`/`RecursionError` → RECHAZADO; `DOCUMENTADAS_CON_CODIGO` vacío. Script de promoción: `.docs/scripts/promover_fichas_catalogo.py`.

### Bloque B

- Diseño V3 cerrado (T-68): `.docs/diseno/bloque_b/decision_claude_c02.md` (9 papeles de IA; Director, Coordinador, Curador, Orquestador y Evaluador pasan a código; nada sale de B).
- Directrices para Astra: `.docs/diseno/bloque_b/directrices_astra.md` (pasos B-0 a B-6, un ticket cada uno, empezando por T-111).
- Asignado como **C-37** en `.docs/tickets/_relevo/cola_astra.md`, después de C-08 (en curso). Congelación de `bloque_b/` levantada solo para eso; publicación de sus tickets autorizada. **Claude hace la QA de cada ticket de C-37** cuando Astra lo suba.

### Decisiones del operador vigentes

- T-102: «Umbrales y sin cifras libres».
- 12-11: autoriza promover en el Catálogo las fichas que superen sus casos de control (con re-congelado del corpus).
- 13-11: «continuamos con la implementación del bloque A»; «Corrige toda la deuda técnica».
- Fuente de datos históricos reales: **sin decidir**. API real: más adelante, con clave y autorización de gasto.

## 6. Pendiente (no empezar sin orden)

1. **QA r02 de T-112** y **QA r01 de T-113** (caras: un revisor nuevo cada una, una detrás de otra).
2. Para terminar A, decisiones del operador primero:
   - GC1: señal y umbral por tipo (Claude propone valores, el operador confirma; hoy `v6.gc1.senal_por_perfil` vacío);
   - fuente de datos históricos reales;
   - Fase 3: esquemas congelados (goldens) de los contratos CT;
   - Fase 4: plan de pruebas de 67 casos (`bloque_a/09_Pruebas/`);
   - backtest de evaluación y modo sombra con API (necesita clave y autorización de gasto);
   - las 10 fichas P2 (opcional).
3. QA de los tickets de C-37 (Bloque B V3) a medida que Astra los suba.
