# T-132 · Análisis técnico

- `ruff check --fix` sobre los ocho ficheros: 55 corregidos, 5 quedan (no automáticos). Ninguna importación quitada se usaba desde otro módulo (comprobado con `grep` de los `from … import` de esos módulos).
- `dt.UTC` es el alias de `dt.timezone.utc` desde Python 3.11; el entorno es 3.12.
