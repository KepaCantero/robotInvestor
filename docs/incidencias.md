# Incidencias del spec

Decisiones y ambigüedades detectadas durante la implementación. Cada entrada: qué dice
el spec (o dónde calla), qué decisión se tomó, y por qué. Nada se decide en silencio.

---

**INC-001 · 2026-11-03 · Versión del ejecutor sin subir en pyproject.** El README V5.1
(§3 y §5) declara "ejecutor V1.2" (subcomandos seguimiento/consulta-broker/credencial,
F11, H5), pero `11_Ejecutor/pyproject.toml` mantiene `version = "1.1.0"`. El código
entregado ES el V1.2 (los subcomandos existen y los 58 tests pasan); solo la cadena de
versión quedó sin bump. Decisión: se deja tal cual pendiente de confirmar con el
propietario de la entrega; no se corrige en silencio porque una versión en el paquete
instalado (`bloque-a --version` / metadata) diría 1.1.0.

**INC-002 · 2026-11-03 · Igual patrón en bloque_a_forex.** El README V1.1 del Bloque A
Forex declara "V1.1" (subcomandos seguimiento/consulta-broker/credencial incluidos, 68
tests) pero su `pyproject.toml` declara `version = "1.0.0"`. Mismo tratamiento que
INC-001: documentado, sin corregir en silencio.

**INC-003 · 2026-11-03 · python-docx es dependencia implícita de bloque_b.**
`bloque_b/redaccion.py::md_a_docx` genera los .docx con pandoc o, en su defecto,
python-docx — pero ni `dependencies` ni `optional-dependencies` del pyproject declaran
`python-docx`. Sin él (ni pandoc), el mapa de eslabones .docx se omite con una
limitación declarada (degradación elegante) y 3 tests fallan porque exigen el .docx.
Solución de entorno aplicada: `pip install python-docx` en el venv del proyecto
(documentado en CLAUDE.md). Corregir el pyproject upstream queda pendiente de confirmar
con el propietario de la entrega.

**INC-T53-01 · 2026-11-09 · Diversidad con tres opciones del mismo clúster (Bloque A, D0 9.6.3).** El D0 dice
«no más de dos opciones del mismo clúster» y, a continuación, que la tercera cede su puesto a otra de otro clúster
«si su RK está a ≤ 10 puntos». No dice qué pasa si no hay ninguna a ≤ 10 puntos. HT-03 publica las tres con la
concentración declarada (`excepcion: True`). Decisión: se deja como está y se pregunta al operador (revisión T-53),
porque cambiarlo toca la herramienta de referencia del corpus y es una regla de selección.

**INC-T53-02 · 2026-11-09 · Antigüedad de los datos en H1 (Bloque A, Anexo A, PS2).** El Anexo A dice «H1: 1 día» y
el código toleraba 3 días naturales. Decisión: H1 se cuenta en sesiones hábiles (el dato del viernes vale el lunes)
y el resto de horizontes sigue en días naturales, para no relajar H2–H5. Los límites pasan a
`ps2_antiguedad_maxima_dias` en la configuración. Ampliación (QA de T-53, H-04): las sesiones descuentan los cierres habituales de mercado (`ps2_festivos`, [PROPUESTO]: Viernes Santo y 1-1, 24-12, 25-12, 26-12 y 31-12), para que el dato de la última sesión real valga tras un festivo. El calendario por mercado (por ejemplo, el 4 de julio en EE. UU.) queda para el perfil de cada tipo de activo; T-57 fija la lista.

**INC-T53-03 · 2026-11-09 · Umbral de revocación de certificados por calibración (Bloque A).** El código revoca un
certificado si el ECE llega a 0,12, pero ese número no figura en el Anexo A (que solo fija `ece_max` 0,15 para
conceder). Decisión: se mantiene 0,12 como `evaluacion.ece_revocacion` y queda para que lo fije el operador (T-57).

**INC-T53-04 · 2026-11-09 · Degradación de H5 de «Limitado» a «No» (Bloque A, D0 12.2 frente al esquema F10).** El
D0 la describe como automática; el esquema de F10 (P-31) exige un cambio de tipo 3 para cualquier paso hacia «No».
Decisión (R23, la más restrictiva): «Sí → Limitado» se aplica sola y «Limitado → No» queda como propuesta de tipo 3.
La degradación se registra en F6 y F10, pero todavía no cambia la tabla que usa el ejecutor (`aplicabilidad` lee
`_tabla_horizontes`, no F10): pendiente en T-53.

**INC-T53-05 · 2026-11-09 · Siguiente paso, semáforo y confianza (Bloque A).** El código usaba reglas propias,
distintas de las del prompt del Analizador (6.15.5 y 6.16) y del Redactor. Decisión: el semáforo y el
`siguiente_paso_sugerido` siguen ya al prompt del Analizador, con los umbrales en la configuración. La `confianza`
(E ≥ 70 «probable») se deja como está: el prompt del Redactor la usa solo para la barra visual y alinearla cambia el
esquema del paquete; queda para la revisión con el operador.

**INC-T66-01 · 2026-11-10 · Efecto de una «tesis frágil» (Bloque A, PA-05).** La propuesta PA-05 de T-53 pedía que
una tesis frágil, según la regla de Contrarias, pasara a confianza «especulativo» y relevancia ALTA. El Anexo A
(control C10 de HT-09) no tiene ese disparador de ALTA: forzarla genera una advertencia en cada ciclo. Decisión
`[PROPUESTO]`: se aplica solo la confianza «especulativo», y la relevancia sigue la regla del Anexo A. Añadir
«tesis frágil» como disparador de ALTA exige editar el Anexo A y HT-09 (corpus): queda para la revisión de
documentación con el operador.

**INC-T66-02 · 2026-11-10 · Quién resuelve una objeción fuerte (Bloque A, PA-05).** Antes la declaraba resuelta el
propio Analista acusado. Decisión `[PROPUESTO]`: queda resuelta solo si se cumplen las dos condiciones:
- la respuesta del Analista cita evidencia verificable (fuentes de sus piezas, cálculos CALC- o referencias REF- registradas);
- el Contradictor lo confirma en una contrarréplica (§5 de su prompt, que el ejecutor no implementaba).

Sin contrarréplica, la objeción sigue abierta.
