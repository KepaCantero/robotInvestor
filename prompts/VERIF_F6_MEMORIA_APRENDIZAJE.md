# PROMPT — Auditoría F6: ¿la memoria de aprendizaje existe en el ejecutor?

> Sesión de SOLO LECTURA: nada se implementa aquí. Los huecos se documentan como
> incidencias y su implementación será un prompt-fase futuro. Ejecutable en
> cualquier momento tras `00_ENTORNO.md` (no depende del orden de fases).

---

AUDITA si la Memoria de aprendizaje (F6) del corpus está implementada de verdad en
los ejecutores, o si es solo esquema sobre papel. Cada punto se verifica con un
comando real; nada se da por supuesto. La sesión no modifica ni una línea del
corpus ni del ejecutor: solo lectura, greps y ciclos mock.

1. Kit de contexto cerrado (solo esto; localiza el archivo por NOMBRE, no por
   numeración F, que cambia entre bloques):
   - `bloque_x/05_Archivos_operativos/Memoria de aprendizaje (esquema …).md`
   - La sección de aprendizaje del Documento 0 del bloque (sección 12 en Bloque A).
   - System prompt del Evaluador (AG-20) y del Orquestador técnico del bloque.
   - `bloque_x/11_Ejecutor/`: `evaluador.py`, `almacen.py`, `orquestacion.py`,
     `prompts.py`, `seguimiento.py`.

2. Por cada bloque (A, A-Forex, B) verifica y anota EVIDENCIA (archivo:línea o
   salida de comando) de cinco capacidades:
   a. ESCRITURA — ¿algún módulo escribe entradas LEC-, MET-, RES- o CERT- en un
      almacén persistente?
      `grep -rn "LEC-\|CERT-\|MET-" bloque_x/11_Ejecutor --include="*.py"`
      ¿Dónde persisten y se conservan entre runs, o se recalculan de cero?
   b. INYECCIÓN — ¿el extracto por ámbito (máximo 10 lecciones por fuerza +
      «Novedades», vía HT-06 en Bloque A) se inyecta en el contexto de los
      encargos?
      `grep -rn "memoria\|aprendizaje\|extracto\|leccion" bloque_x/11_Ejecutor --include="*.py"`
   c. PROPIETARIO ÚNICO — ¿solo el Evaluador escribe en F6, o hay más escritores?
   d. CICLO REAL — ejecuta un ciclo mock del bloque (ver comando en su README de
      `11_Ejecutor`) y examina los artefactos de salida: ¿hay rastro de lecciones
      o métricas por celda más allá de `metricas.json`? ¿`metricas.json` sale de
      un almacén F6 acumulado o se calcula solo sobre la ventana del backtest?
   e. CADUCIDAD — ¿algún código aplica la caducidad obligatoria de lecciones y el
      límite de 10 vigentes por ámbito, o es regla solo documental?

3. Matriz de veredicto (3 bloques × 5 capacidades), cada celda con estado
   IMPLEMENTADO · PARCIAL · SOLO ESQUEMA y su evidencia.

4. Cada hueco → incidencia nueva en `docs/incidencias.md` (INC-xxx) con el hueco
   exacto y la evidencia. NADA se implementa en esta sesión.

5. Registra el veredicto en `docs/AVANCE.md` (una línea, fecha + estado por
   bloque). Si tocas docs, commit con prefijo `infra:`.

Criterio de éxito: la matriz completa con evidencia verificable en las 15 celdas,
una INC por cada hueco encontrado, y `git status` sin cambios ni en corpus ni en
ejecutores.
