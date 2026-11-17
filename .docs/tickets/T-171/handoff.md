# T-171 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-17 · de claude (implementador) a un revisor nuevo (QA r01)

- **Fase en la que se entrega:** QA.
- **Hecho:** detector de `guias.py` por estructura para H-18 y H-19 (`analisis-tecnico.md`), pruebas en
  `bloque_a/11_Ejecutor/tests/test_t171_guias.py`, INC-T126-01 (viñeta T-171), fila de la deuda técnica y `pruebas.md`.
- **Falta:** la QA. Commit local, sin push (lo integra la sesión coordinadora).
- **Commit:** el de «wip local: T-171 … [pendiente QA]» sobre `origin/develop` `a9210c0`; el juego reservado está en el commit
  anterior (`45064cd`), hecho antes de tocar el detector.
- **Cuidado con:**
  - `.docs/tickets/T-171/reservado_t171.py` lo escribió el implementador conociendo la QA r04: su 0 es optimista. Un juego
    reservado del revisor es la medida honrada.
  - `ALCANCE_PARTE` solo acota si el control del núcleo es el objeto directo (para no romper el ejemplo del prompt 4.5). Es la
    decisión que más conviene atacar. El objeto se busca tras quitar los complementos de alcance que van delante («Comprueba en RV la segunda pasada» se detecta: lo encontré al escribir este traspaso y está en el juego propio); quedan otras posiciones (el control como sujeto, «La segunda pasada se hace en RV», da NOMBRA_CONTROL por el verbo, no por el alcance).
  - `_otra_accion` cuenta como acción cualquier palabra tras «y» que no abra un sintagma nominal ni sea un plural: los
    sustantivos singulares sin determinante dan falso positivo (declarado).
  - Los mutantes M45, M46, M47 y M51 de T-161 no aplican sobre el código nuevo (sus líneas cambiaron); `mutantes_t171.py` los
    lleva con la misma intención (M45b…) sin tocar el script de T-161.
- **Scripts útiles:** `.docs/tickets/T-171/mutantes_t171.py <copia qa29_…_mut> [IDs]`, `.docs/tickets/T-161/revisores/*`,
  `.docs/tickets/T-161/medir_detector.py`.
