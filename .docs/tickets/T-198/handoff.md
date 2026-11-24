# T-198 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-24 · de claude (implementador) a QA (el agente que no implementó)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - El Buscador (AG-16) atiende el CT-19 FIABILIDAD_FUENTES: `fiabilidad_f9.atender_ct19` comprueba el mensaje entero contra F6 y F9 y, si cuadra, deja una entrada `FIABILIDAD_MEDIDA` por fuente en F9 de la instancia (archivo nuevo del almacén, propietario AG-16). Sin duplicados (también entre procesos) y con reintento en el ciclo siguiente si no cuadra (incidencia DATOS en HA).
  - El Buscador ve esa fiabilidad en sus búsquedas: las fuentes de F9 de un CT-07 llevan `fiabilidad_medida` si la tienen.
  - 20 pruebas en `tests/test_t198_buscador_ct19.py`; mutantes en `mutantes.py`; mapa y evidencias de PB-46 (sigue PARCIAL, con el «No comprueba» nuevo).
- **Falta:** la QA. Commit local, sin push.
- **Cuidado con:**
  - PB-46 no pasa a «Superada»: la Q, el nivel y el orden de F9 los recalcula el Buscador con el modelo real, y el prompt (6.3, n / (n + 30) sobre S por bandas) y el esquema de F6 (k = 20) no dan la misma puntuación del criterio 2 (INC-T198-01). El ejecutor guarda los puntos del Evaluador y `recalificacion_q: PENDIENTE`.
  - El almacén gana un archivo (F9). Un almacén sellado antes de T-198 sella F9 vacío al abrir (`sellos_integridad.json` gana la clave); si `F9_registro_fuentes.jsonl` existe sin sello, falla cerrado.
  - En el primer ciclo tras T-198, un almacén con FUE- antiguas las reenvía en un CT-19 nuevo y las atiende (nunca se atendieron); su `comunicado_ct19` en F6 pasa a ser el nuevo.
  - `referencias.py` y `mantenimiento_fuentes.py` (Astra, T-181, T-183 y T-184) no se tocan. En `orquestacion.py`: el import (`from . import fiabilidad_f9, respuesta_final`), `_comunicar_fiabilidad` (cambia su firma a `(as_of, run_id)`) y una línea tras `para_clase` en `_peticion_conocimiento`.
- **Scripts útiles:** `.docs/tickets/T-198/mutantes.py <copia de bloque_a/11_Ejecutor>`; `.docs/scripts/evidencias_plan_a.py --pb PB-46`.
