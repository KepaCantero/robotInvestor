# T-158 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-16 · de claude (sesión del Bloque A, T-158) a claude (sesión coordinadora y revisor nuevo de la QA)

- **Fase en la que se entrega:** QA.
- **Hecho:** guías CT-18 en el ejecutor (`bloque_a/guias.py`), enganche en el ciclo y en `_invocar`, CLI `guia`, configuración `guias_orquestador`, 55 pruebas, PB-48 en AUTOMATICA y documento de evidencias regenerado, incidencia y registro de decisiones.
- **Falta:** la QA con un revisor nuevo; integrar en `develop` (commit local «wip local: T-158», sin push); `./tools/check_all.sh` completo al integrar; si se quiere, bajar la cuota de ruff de `tools/cuotas.txt` a 2828 (no se ha tocado para no chocar con otras sesiones).
- **Commit:** «wip local: T-158» en la copia de trabajo (sin push).
- **Cuidado con:** no se toca `contratos.py` ni los goldens: el esquema del cuerpo CT-18 lo aplica `guias.py` y la mensajería solo el sobre; si T-143 decide meter CT-18 en `CAMPOS_MINIMOS` o en `ESQUEMAS`, cambian `tablas_contratos.json`/`esquemas_respuestas.json` y los casos `CT-18/*` de la batería (hoy con cuerpo `{"guia": "…"}`, ADMITIDOS) pasarían a RECHAZADOS. El detector de conflictos lee texto libre (límites en INC-T126-01). El `.venv` enlazado apunta al paquete de la copia principal: en esta copia, la CLI con `python -m bloque_a.cli` desde `bloque_a/11_Ejecutor`.
- **Scripts útiles:** `.docs/scripts/evidencias_plan_a.py --pb PB-48`, `bloque_a/11_Ejecutor/tests/goldens_ct.py`.
