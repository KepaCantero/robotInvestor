# T-99 · Análisis técnico

## Motivo

La Constitución (§9, punto 17) exige corregir por número de intentos (Sharpe deflactado, probabilidad de sobreajuste), y la propuesta de J lo resume en «cada intento cuenta». El banco de medida (T-94) ya sellaba un prerregistro por ejecución, pero suelto en la carpeta de salida: no había un sitio común que contara los intentos de una misma idea ni impidiera elegir el resultado después.

## Implementación

- `.docs/scripts/registro_experimentos.py` (nuevo, solo biblioteca estándar): clase `Registro` con `prerregistrar`, `intento`, `resultado`, `experimento`, `resumen`, `adoptable` y `verificar`; `RegistroError` para todo lo que no admite; línea de órdenes (`prerregistrar`, `intento`, `resultado`, `ver`, `verificar`). Cada escritura relee y verifica la cadena antes de anexar y hace `fsync`.
- `.docs/scripts/banco_medida.py` (0.2.0): opciones `--registro`, `--experimento` y `--max-variantes`; prerregistro en el registro con la huella del prerregistro del banco; un intento por ejecución, con la huella de sus parámetros como variante; resultado «fallido» si el titular no llega a ejecutarse; `veredicto_conjunto`. Llamado desde código sin `registro`, no anota nada (lo usan las pruebas unitarias).
- `.docs/diseno/contratos/`: borrador de CT-G-24 con la forma exacta de las anotaciones (y el de CT-G-08, aparte).

## Decisiones y límites

- El registro está en el repositorio porque es del proyecto; no guarda datos de ningún usuario.
- La cadena de huellas detecta la manipulación, pero no la impide: quien tenga el fichero puede reescribirlo entero con una cadena nueva. Para eso está git (cada anotación nueva llega en un commit) y, cuando exista, la firma de SC-5.
- La regla «el intento empezó después del prerregistro» compara instantes ISO en UTC: quien pase `ahora` a mano tiene que usar el mismo formato.

## Comandos

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_registro_experimentos.py
```

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_banco_medida.py
```

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_borradores_contratos.py
```
