# Notas de deuda — V0.60 (robustez de los seis validadores de mensajes)

La pieza no abre deuda nueva y no cierra ninguna: es una batería nueva de robustez sobre los seis validadores
que quedaron fuera de V0.37, y los dos defectos reales que aparecieron están resueltos —el defecto_01 (el
permiso de apalancamiento ajeno en `validar_sobre`) se corrigió y fijó con su prueba, y los cuatro hallazgos
de la revisión independiente eran de cobertura y documentación, corregidos con las regresiones r01–r04—, así
que no dejan fila.

- **Tabla T (pendientes de deuda técnica):** ninguna fila nueva, ninguna modificada. `Deuda_tecnica.md` queda
  intacto.
- **Tabla D (decisiones del operador):** ninguna fila nueva. La pieza no añade ningún valor de configuración
  ni de parámetros: no hay constantes nuevas en `validador/` (los ADMITE_*, las tablas `_MIN_ITEMS` y los
  predicados de excepciones viven dentro de la batería, que no está en `MODULOS_ESQUEMA`), el esquema del
  código sigue siendo V0.53 y `version_config` no cambia. Nada que ratificar.
- **Anotado para una pieza futura** (sugerencia del revisor, no es deuda formal): distinguir en el informe
  entre `autoria_c`/`autoria_contradictor` AUSENTES (None, legítimo) y MAL FORMADAS (hoy una lista se queda
  sin comprobación de coherencia en silencio, porque `diversidad()` la trata como desconocida; fijado con
  r02 y sin camino práctico, porque el Orquestador valida su configuración con `_autoria_ok`). Sería una
  decisión de contrato (una regla C nueva o el estrechamiento de C-11), no de esta pieza.
- **Observación para el revisor** (no es deuda): las excepciones por diseño de la batería están codificadas
  en predicados que describen lo que cada validador lee (`_afecta_sobre`, `_afecta_encargo`,
  `_calendario_afecta`) y en las tablas de mínimos `_MIN_ITEMS`, extraídas de los esquemas. Si una pieza
  futura cambia lo que un validador consulta o los mínimos de un esquema, la batería habrá que ajustarla; el
  ajuste sería señal del cambio, no un debilitamiento. Los predicados tienen granularidad gruesa en algunas
  ramas: con los fixtures y la semilla actuales no produce fallos espurios.
