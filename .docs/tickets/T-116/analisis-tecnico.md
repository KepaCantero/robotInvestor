# T-116 · Análisis técnico

## Causa raíz o motivo

El mapa de cobertura del plan de pruebas (`tests/MAPA_PLAN_DE_PRUEBAS.md`, del 3-11-2026) era anterior a casi todo lo construido después y marcaba como automáticas filas cuyas pruebas solo comprueban parte del criterio de aprobación. La Fase 4 pide el resultado real de cada prueba del plan con un comando que lo repita.

## Evidencia

- Mapa antiguo: 34 automáticas. Con la regla estricta, 13 pasan a parciales.
- QA r01 (NO APTO): cuatro filas que el mapa nuevo seguía dando por automáticas (PB-21, PB-23, PB-37 y PB-49) tenían una cláusula determinista sin afirmar; el mutante A01 del revisor, que guarda en F4 una escritura rechazada, dejaba en verde la prueba citada por PB-23.

## Implementación

- Archivos y por qué:
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: fuente de verdad, legible por máquina, de qué prueba cubre qué.
  - `.docs/scripts/evidencias_plan_a.py`: comprueba el mapa, ejecuta lo citado y regenera el documento.
  - `docs/evidencias_pruebas_bloque_a.md`: generado; no se edita.
  - `tests/test_fase4_mapa.py` (mantiene el mapa y el documento al día) y `tests/test_fase4_huecos.py` (cláusulas del plan que nadie afirmaba).
- Decisiones tomadas:
  - **Regla estricta:** una fila es `AUTOMATICA` solo si sus pruebas afirman todo el criterio, salvo lo que solo existe con tiempo real o con el modelo real. Una cláusula que el ejecutor podría comprobar y nadie afirma la deja en `PARCIAL`.
  - **Las herramientas cuentan** (`bloque_a/10_Herramientas/tests`), aunque no estén en el gate del repositorio: el script las ejecuta desde su carpeta.
  - **Un hueco que revela una diferencia con el plan no se arregla:** se registra (INC-T116-01 e INC-T116-02) y la fila queda parcial.
  - **`--runxfail`:** una prueba citada marcada como fallo esperado cuenta por lo que hace.
- Desviaciones del plan del ticket: ninguna de alcance. La ronda r02 añade pruebas en vez de rebajar las cuatro filas, salvo PB-37, que baja a parcial porque el ejecutor no tiene una operación de corrección de un pronóstico.
- Límites conocidos:
  - el documento refleja el commit sobre el que se generó; `test_h05…` falla si el mapa cambia sin regenerarlo, pero no vuelve a ejecutar las pruebas;
  - las 29 filas parciales siguen teniendo su hueco, dicho en «No comprueba»;
  - con el cliente simulado se valida la tubería, no la calidad analítica (R22);
  - el script lee el plan por sus cabeceras `### PB-NN · …`; otra forma lo detiene con un error.
- Comandos exactos para probarlo, desde la raíz y con el `.venv`:
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py` (comprueba; 0 si está bien);
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-23`;
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` (unos 3 minutos);
  - `cd bloque_a/11_Ejecutor && python -m pytest -q tests/test_fase4_mapa.py tests/test_fase4_huecos.py`.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 (alta) cuatro filas automáticas con una cláusula sin afirmar | Pruebas nuevas para PB-21, PB-23 y PB-49 con el caso del plan; PB-37 con la corrección como PRG nuevo, y la fila baja a parcial. Repasadas las ocho automáticas que el revisor no leyó: se añaden pruebas a PB-54 y PB-64 y se cita `test_principal_en_celda_no` en PB-65; PB-32, PB-53, PB-55, PB-56 y PB-63 se mantienen | `test_pb21_…`, `test_pb23_…`, `test_pb37_…`, `test_pb49_…` (2), `test_pb54_…`, `test_pb64_…` |
| H-02 (media) `--pb` daba 0 con una prueba saltada o `xfail` | `--pb` da 1 si alguna citada no se supera; las pruebas se lanzan con `--runxfail` | `test_h02_una_prueba_citada_no_superada_nunca_da_un_cero` |
| H-03 (baja) cabeceras del plan que no se reconocen | `leer_plan` se detiene si una cabecera `PB-` no casa con el patrón; `comprobar` exige título y criterio | `test_h03_…` (5) |
| H-04 (media) documentación | Este análisis; fila de la deuda en EN QA con las cifras; fila de la Fase 4 en `docs/AVANCE.md` | — |
| H-05 (baja) nada avisa si el mapa cambia sin regenerar | La tabla del documento se compara con el mapa | `test_h05_el_documento_publicado_coincide_con_el_mapa` |

Resultado tras la r02: 26 automáticas, 29 parciales, 7 pendientes de la API, 3 sin prueba, 1 con usuarios y 1 documental; 101 pruebas citadas, las 101 superadas.

Fuera del ticket, a la deuda (T-120): un IBAN escrito con espacios no se detecta como dato sensible, y el máximo de 10 lecciones por encargo está escrito en el código y no en la configuración.
