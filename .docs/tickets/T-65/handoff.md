# T-65 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-10 · de claude a la QA (Astra o un revisor nuevo)

- **Fase en la que se entrega:** QA.
- **Hecho:**
  - H-07 a H-21 y el resto técnico de T-53, según la tabla del `README.md`. H-06 y H-12 ya estaban hechos y citan su prueba.
  - `bloque_a` pasa de 201 a 265 pruebas, y las 39 mutaciones se detectan.
- **Falta:**
  - El commit lo hace el coordinador; este ticket no lo hace.
  - Para el coordinador, fuera del alcance de este ticket:
    - la fila T-65 de la deuda técnica y la lista para T-57 (está en el `README.md`);
    - la línea de `prueba_refs_vivas.py` en la tabla de scripts de `.docs/README.md`;
    - en `docs/incidencias.md`: INC-T53-02 ahora con `lunes_de_pascua`, e INC-T53-04 aplicada en el mismo ciclo;
    - la nota de CS-08 en la trampa de `CLAUDE.md`: 17 fichas con código, de las que se sirven 14;
    - la línea base de A en `CLAUDE.md` y en `tools/cuotas.txt` (`pytest_bloque_a=265`; ruff puede bajar a 3083).
- **Commit:** ninguno (lo hace el coordinador).
- **Cuidado con:**
  - `tools/refs_vivas.py` está fuera de `bloque_a/`. Se tocó porque el encargo autoriza arreglar el script de H-11 (lo situaba en `.docs/scripts/`).
  - `clusteres.ventana_semanas` pasa de 104 a 156.
  - HT-01 rechaza ahora los cierres ≤ 0.
  - `parametro()` cae en `por_defecto.yaml` cuando una configuración parcial no trae la clave.
- **Scripts útiles:**
  - `python3 .docs/tickets/T-65/mutaciones.py [filtro]`;
  - `python3 .docs/scripts/prueba_refs_vivas.py [script]`;
  - `.docs/scripts/gate.sh` con `--completo`.
