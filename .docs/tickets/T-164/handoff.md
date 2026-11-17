# T-164 · Traspaso

## 2026-11-17 · de claude (implementador) a un revisor (QA r02)

- **Fase en la que se entrega:** QA (r02, tras el NO APTO de la r01)
- **Hecho:** H-01 a H-06 de `qa.md`, con las correcciones exactas de la tabla; ver «Ronda r02» en `analisis-tecnico.md` y en `pruebas.md`.
- **Falta:** la QA r02. Que el revisor vuelva a pasar `revisores/r01_01_excusa.py` (25/25), `r01_02_escritura.py` (6/6), `r01_03_cifras.py` y los mutantes.
- **Commit:** local, «wip local: T-164», sin push. `[pendiente QA]`
- **Cuidado con:** solo se pasaron las pruebas del verificador (57), no la suite completa (por indicación de la sesión
  coordinadora; la de la r01 dio 7528 superadas). `mutantes_t164.py` tiene ahora 20 mutantes; T05 y T13 se rehicieron.

## 2026-11-17 · de claude (implementador) a un revisor nuevo (QA r01)

- **Fase en la que se entrega:** QA
- **Hecho:** H-09 a H-12 corregidos con sus pruebas y H-04 comprobado. El detalle está en `analisis-tecnico.md` y en `pruebas.md`.
- **Falta:** la QA r01. Después, la sesión coordinadora decide el cierre y el push.
- **Commit:** local, «wip local: T-164», sin push. `[pendiente QA]`
- **Cuidado con:**
  - `r01_02_siembra.py` de T-157 lleva fijado el nombre del Documento 0 V5.1 y ya no se ejecuta en develop, porque T-143 trajo
    la V5.2. Lo ejecuté con una copia adaptada (V5.1 → V5.2 y V5.2 → V5.3) y la dejé en `.docs/tickets/T-164/r01_02_siembra_v52.py`, sin tocar el
    original.
  - `docs/auditoria_ids_bloque_a.*` se regeneró en T-164: antes no era lo que develop generaba, por T-143.
    Ver `pruebas.md`, «Informe regenerado».
  - N04 de `r02_02_mutantes.py` sale ROTO a propósito: el texto que mutaba era el defecto de H-09.
  - Mide ruff con los scripts de mutantes terminados. Mientras corren, cada `tests/conftest_mutante_*.py` suma a la cuenta.
- **Scripts útiles:** `.docs/tickets/T-164/mutantes_t164.py` y `.docs/tickets/T-157/revisores/*.py`.
