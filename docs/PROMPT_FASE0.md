# PROMPT — Fase 0 · Verificador de consistencia de IDs (bloque_a)

> Pegar tal cual como primer mensaje de una sesión de Claude Code abierta en la raíz
> del repo (`cd ~/robotInvestor && claude`). CLAUDE.md se auto-carga y aporta las
> reglas; este prompt solo define el alcance de la fase. Modelo recomendado para esta
> fase: el más capaz disponible (clase Opus); las fases mecánicas 1–2 bastan con Sonnet.

---

FASE 0 — Verificador de consistencia de IDs del bloque_a. Antes de implementar nada del Motor, quiero poder medir con un comando exactamente qué está desincronizado entre el corpus (V5.1) y el código.

Kit de contexto de ESTA fase (no abras nada más del corpus):
- `bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.md` — solo §1 (reglas R), §5 (archivos F), §6 (contratos CT), §9 (puntuaciones/puertas)
- `bloque_a/04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md`
- `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py` (FICHAS_CATALOGO, CATALOG_VERSION)
- `bloque_a/11_Ejecutor/bloque_a/contratos.py` (ESQUEMAS, canal_permitido)

Prohibido leer F7/F8/F9 enteros: son almacenes indexados, accede por identificador (RF-xxxx, TM-xx).

Entregables:
1. Un verificador (`bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py`, o donde encaje mejor en el diseño existente) que escanee los .md del corpus y el código y emita informe JSON + Markdown con, como mínimo:
   a. Contratos CT-xx citados en los .md vs definidos en Documento 0 §6.1 y en `contratos.py` (citar un CT inexistente = error).
   b. Reglas R1–R27 citadas vs definidas en §1.
   c. Archivos F1–F11 citados vs inventario §5.1, mapeando número→archivo real de `05_Archivos_operativos` por su encabezado H1 (la numeración NO coincide con el nombre).
   d. Fichas del Catálogo V5.0 (encabezados `### [ID]`) vs `FICHAS_CATALOGO` de servicio.py: clasificar cada ficha como IMPLEMENTADO / SOLO_CATALOGO / SOLO_CODIGO / ID_DISTINTO, y señalar las menciones «Catálogo V4.0» en prompts (el skew conocido de 60 vs 81).
   e. Referencias RF-xxxx / TM-xx / TA-xx citadas en prompts y funciones vs entradas existentes en `05_Archivos_operativos`.
2. `docs/auditoria_ids_bloque_a.md`: el informe ya generado + una tabla de decisiones PROPUESTAS para resolver el skew (no las ejecutes todavía).
3. Tests del verificador con un fixture pequeño que contenga al menos un fallo de cada clase (a–e).
4. `pytest -q bloque_a/11_Ejecutor` debe seguir en 58/58.

Restricciones:
- No modificas ningún .md del corpus (son canónicos; los .docx ni tocarlos).
- No toques `bloque_a_forex/` ni `bloque_b/`.
- Ninguna decisión de resolución del skew se aplica en esta fase: cada una se documenta en `docs/incidencias.md` con su porqué.
- Commit con prefijo `fase0:`. Avance registrado en `docs/AVANCE.md`.

Criterio de éxito: lanzo el verificador con un comando y el informe me dice, ficha a ficha y contrato a contrato, qué está desincronizado y por qué — sin que tenga que fiarme de tu palabra: todo dato del informe sale del propio corpus escaneado.

---

## Plantilla para las fases siguientes

Copia este esqueleto cambiando el bloque de contenido del medio (los entregables y el
kit de contexto). Lo que NO cambia nunca: kit de contexto cerrado, F7/F8/F9 por
identificador, corpus .md intocable, sin tocar otros bloques, líneas base de tests
innegociables, decisiones documentadas en incidencias, prefijo de commit de fase.

```text
FASE N — <título>. <una frase de objetivo>.
Kit de contexto: <2-4 rutas exactas>.
Entregables: <concreto y verificable>.
Restricciones: <las fijas + las específicas>.
Criterio de éxito: <un comando que yo pueda lanzar y qué debe mostrar>.
```
