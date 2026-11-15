# T-134 · Análisis técnico

- `evaluador.py`: `_finito` (usado por `_prob_valida` y `_numero_finito`; el Evaluador ya no llama a `math.isfinite` directamente sobre el umbral), `RE_FECHA_ISO` con cifras ASCII y zona solo tras la hora, `variables_nivel(cfg)` validada en `Evaluador.__init__` y usada en el alta y en `pronosticos_de_fuentes`; el parámetro de `motivo_pronostico_fuente_no_registrable` se llama `variables_nivel_cfg` para no ocultar la función.
- `orquestacion.py`: el alta en F2 llama a `variables_nivel(self.cfg)`.
- Una clave nula en la configuración es una clave ausente (`parametro`): falla con `KeyError`, como el resto.
