# T-79 · Análisis técnico

## Motivo

GLM construyó en paralelo las siete piezas del kit 2 del marco común de C, de la V0.60 a la V0.66, a partir de la V0.53 del repositorio. El operador las entregó el 10-11-2026 para revisarlas y mejorarlas. El detalle completo está en el Documento 0: `sistema_global/documentos_0/V0.67_Integracion_del_kit_2_de_GLM.md`.

## Evidencia

- **Contenido de las entregas.** Los siete ZIP se compararon por SHA-256: 406 archivos en la V0.66, ninguno perdido y ninguno vuelto a un contenido anterior. Basta con integrar la V0.66.
- **Pruebas.** Desde una extracción limpia con `python3 -I`, la V0.66 pasa sus 56 baterías.
- **Panel (V0.64).** La sonda `marcoC/entrega_claude/V0.67/scripts/r01_panel_v064.py` da 3 hallazgos con la V0.66 (G-02) y ninguno con la V0.67.
- **Vía DIRECTA.** `entrega_claude/V0.67/scripts/pc3_01_via_directa.py` da FALLA: `detectar()` rechaza la vía `DIRECTA` con O-01.

## Implementación

| Archivo | Cambio | Por qué |
| --- | --- | --- |
| `validador/consola.py` | `_diario` valida el tope antes de usarlo (G-02); el tope por defecto sale de `parametros.py` (G-03); `_autonomia` da ROJO si `degradadas` no es un diccionario (QA H-03) | Fallaba abierto; regla 5 del kit |
| `validador/parametros.py` | `n_lineas_diario_ambar: 1000` `[PROPUESTO]`, `PAR-0.4.0` | G-03 |
| `validador/reloj.py` | `estado()` conserva un bloqueo ilegible en su rama de respaldo (QA H-04) | «La foto nunca es más optimista que el reloj» |
| `validador/migraciones.py` y `esquemas_codigo.json` | Esquema V0.67 y MIG-005 (de V0.53 a V0.67, sin cambios en el estado) | El parámetro nuevo cambia el esquema del código |
| `pruebas/pruebas_consola_sistema.py` | Cuatro comprobaciones `r01_` y `r02_` | Regresiones |
| `pruebas/pruebas_comparador_t17.py` y `pruebas_integracion_v053.py` | Versión del PAR, cadenas hasta MIG-005 y nombres al día (QA H-10) | Fijaban el esquema «actual» a la V0.53 |
| `LEEME.md` | Párrafo de la V0.67, lista de ejecución, cifras al día (QA H-07) y deuda renumerada | G-01, G-04 |
| `validador/catalogo_codigos.py` y su batería | Números de deuda T-70 y T-71 | G-04 |

**Decisiones:**
- El valor por defecto del tope lo toma la firma de `panel()` directamente de `parametros.py`. Así `None` sigue siendo inválido (ROJO), como exigía la batería de GLM, y no se debilita ninguna prueba.
- Las notas originales de `entrega_glm/` conservan la numeración de GLM. La tabla de equivalencias está en el §7 del Documento 0.

**Límites:** lo que la pasada de coherencia marca como pendiente (de T-80 a T-86) no entra en este ticket.

**Cómo probarlo:**
- `.docs/scripts/pruebas_marco.sh`
- `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c`
- los scripts de `revisores/` de este ticket
