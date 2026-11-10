# T-65 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-10 · de claude a la QA r03

- **Fase en la que se entrega:** QA (r03).
- **Hecho:**
  - H-12 a H-15 de la QA r02, con sus pruebas en `bloque_a/11_Ejecutor/tests/test_t65_qa_r02.py` y en `.docs/scripts/prueba_refs_vivas.py`.
  - A tiene 300 pruebas y `mutaciones.py` detecta 57 de 57.
  - Las sondas r01_01, r01_04, r01_06 y r02_01 a r02_03 dan 0 hallazgos.
  - Gate completo 12/12 desde una copia limpia.
- **Falta (coordinador):** el commit de la r03.
- **Cuidado con:**
  - Una referencia de comparación mala deja fuera del ciclo los tipos que la usan; no se pasan a pronósticos sin referencia.
  - `Close` junto a `Adj Close` se rechaza; qué columna debe mandar no se ha decidido.

## 2026-11-10 · de claude a la QA r02

- **Fase en la que se entrega:** QA (r02).
- **Hecho:**
  - H-01 a H-09 y H-11 de la QA r01, con sus pruebas en `bloque_a/11_Ejecutor/tests/test_t65_qa_r01.py`.
  - A tiene 285 pruebas; `mutaciones.py` detecta 50 de 50; las sondas r01_01 y r01_04 dan 0 hallazgos.
  - Gate completo en una copia limpia: ver `pruebas.md`.
- **Falta (coordinador):**
  - H-10 a la deuda técnica.
  - Commit de lo de la r02, junto con `qa.md` y `revisores/` de la QA.
  - Lo anotado en la sección anterior, salvo `docs/incidencias.md`, que ya está hecho (H-09).
- **Cuidado con:**
  - `valor_en` valida solo el cierre que devuelve, y `cierres` solo el rango pedido.
  - ML-CLUS-001 elige los proxies por solape, en orden determinista.

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
