# T-147 · Pruebas

Copia `t147` (base `dd166b3`), intérprete `/home/user/robotinvestor/.venv/bin/python`, sin red, sin API y sin servicios de pago. No se lanzó `./tools/check_all.sh` ni la suite completa de A (instrucción de la coordinación).

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t147.py` (nuevo) | — | 96 pasan |
| `tests/test_t142_cadena_b.py` | 30 | 30 pasan (una reforzada, comentada «T-147») |
| R8 vecinas (`test_t92_revision`, `test_t93_hallazgos`, `test_t103_r8_y_bajos`, `test_t120…`, `test_t122…`, `test_t123_r02`, `test_t123_r8…`, `test_t130_r8`, `test_t136_r8`, `test_t140`) con `test_t142_cadena_b` | — | 369 pasan |
| Vecinas pedidas: `test_t12*`, `test_t13*`, `test_t14*`, `test_fase2_*`, `test_fase3_goldens.py` (incluye `test_t144`, `test_t147` y `test_t148`) | — | **3061 pasan**, 0 fallan (5 min 57 s) |
| `python tests/goldens_ct.py` | coinciden | coinciden |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_h02_la_peticion_con_datos_protegidos_falla_cerrado` (4 datos × 3 campos × con y sin correspondencia), `test_h02_el_script_no_escribe_ni_devuelve_ct04…` (`cadena_a_b.main` con un ciclo de mentira: `no_enviadas` con DATOS_PROTEGIDOS, sin petición escrita, sin llamar a B ni CT-04), `test_h02_la_peticion_limpia_se_sigue_construyendo` |
| CA-2 | `test_h02_r8_detecta_correos_y_asignaciones_de_clave` (15 formas), `test_h02_r8_falsos_positivos_de_las_formas_nuevas` (19 textos), `test_h02_el_correo_se_detecta_aunque_lleve_escapes_de_json`, `test_h02_ni_un_falso_positivo_en_el_ciclo_simulado_de_los_doce_tipos` (todo lo que R8 mira en el ciclo, más de mil textos, y lo que el ciclo escribe), `test_h02_ni_un_falso_positivo_en_los_prompts_ni_en_los_goldens`; `goldens_ct.py` |
| CA-3 | `test_h01_tipos_secundarios_…` (7 inválidos, 4 válidos), `test_h03_las_enumeraciones_son_las_del_anexo_b1_del_bloque_b`, `test_h03_configuracion_fuera_de_b1_falla_cerrado` (11 casos × con y sin correspondencia), `test_h03_peticion_que_no_es_una_tabla`, `test_h03_valores_de_b1_se_aceptan`, `test_h04_sonda_sin_correspondencia_quita_la_clave_previa`, `test_t142_cadena_b.py::test_no_muta_el_paquete` |
| CA-4 | `test_t141_h01_clases_que_no_existen_fallan` (XXX, div, DIV + RENTA, vacía), `test_t141_h01_universo_sin_simbolos_de_la_clase_falla`, `test_t141_h01_una_clase_que_existe_sigue_en_verde` |
| CA-5 | `test_t141_h03_respuestas_raras_no_escriben_nada` (10 casos; lo que ya había en la carpeta se queda), `test_t141_h03_respuesta_normal_escribe_las_seis_series`, `test_t141_h02_el_docstring_dice_cuando_se_publica` |
| CA-6 | scripts de los revisores y mutantes (abajo) |

## Scripts de los revisores (antes → después)

| Script | Antes (QA) | Después |
| --- | --- | --- |
| `T-142/revisores/r01_ataques_peticion.py --trabajo <dir>` | 27 OK · 14 OBS | 36 OK · 4 OBS (las cuatro, observaciones de la QA: ver `analisis-tecnico.md`) |
| `T-142/revisores/r02_cadena_doce_tipos.sh` | código 0; 30 enviables, 2 enviadas | igual |
| `.docs/scripts/cadena_a_b.py --sonda-sin-correspondencia` | código 0; 1 enviada | igual |
| `T-142/revisores/r03_mutantes.py <copia t147_mut>` | 9 muertos, 1 vivo (`muta_paquete`) | **10 de 10 muertos** |
| `T-141/revisores/r03_respuestas_raras.py <dir>` | 4 trazas, carpeta a medias, repetida en silencio | normal: código 0, 6 CSV; los 8 raros: código 1 y 0 CSV |
| `T-145/revisores/r01_02_r8_series.py` (R8 de tarjetas, que también toca `secretos_en_texto`) | 0 fallos | 0 fallos (200 000 grupos en 0,41 s) |
| `T-141/revisores/r01_contraste_fred.py`, `r02_festivos_y_huecos.py` | — | no se ejecutan: necesitan red y los datos descargados; no prueban nada de lo que cambia (H-04 queda como pregunta) |

Coste de los patrones nuevos (textos de 200 000 caracteres hechos para el peor caso: «a»×200 000 + «@», «x@» + «a.»×100 000, «api_key=»×50 000…): de 0,03 a 0,15 s.

## Regresiones (mutantes)

`.docs/tickets/T-147/mutantes.py <copia t147_mut> --ticket T-147`: **16 de 16 muertos** (sin R8 en la petición, sin validar `tipos_secundarios`, sin enumeraciones de B.1, idioma sin validar, claves con espacios, la sonda arrastra la clave, R8 sin correos, R8 sin asignaciones, cualquier valor de 6 con un nombre fuerte, sin excluir «0x…», correo de imagen «@2x», `--clases` sin `choices`, universo vacío en verde, BCE con fechas repetidas, con una serie vacía y sin una moneda). Con el código de la base (`dd166b3`, `git archive` en una carpeta desechable), `test_t147.py` da 67 fallos y 1 error de 96 (pasan los falsos positivos y los casos válidos, como debe ser). `T-142/revisores/r03_mutantes.py` en la copia: **10 de 10 muertos** (antes, `muta_paquete` vivo). Las copias desechables se borraron al acabar.

## Cuotas y gates ligeros

ruff de los tres ejecutores desde la raíz: **2838** (cuota 2838); mypy de A como el gate: **109** (cuota 109). `tools/secrets_scan.py` sin hallazgos, `refs_vivas.py` todas vivas, `nfc_check.py` NFC, `corpus_integridad.py` 695 íntegros. Los nombres de credencial de las pruebas van partidos en dos cadenas (`PW`, `AK`) y los correos y el IBAN de prueba también.

## Comandos

```bash
cd bloque_a/11_Ejecutor; PY=/home/user/robotinvestor/.venv/bin/python
$PY -m pytest -q -p no:cacheprovider tests/test_t147.py tests/test_t142_cadena_b.py
$PY -m pytest -q -p no:cacheprovider tests/test_t12*.py tests/test_t13*.py tests/test_t14*.py tests/test_fase2_*.py tests/test_fase3_goldens.py
$PY tests/goldens_ct.py
cd ../..   # con .venv enlazado al del repositorio
.venv/bin/python .docs/tickets/T-142/revisores/r01_ataques_peticion.py --trabajo <dir>
bash .docs/tickets/T-142/revisores/r02_cadena_doce_tipos.sh .venv/bin/python <dir>
.venv/bin/python .docs/tickets/T-142/revisores/r03_mutantes.py <copia t147_mut>
.venv/bin/python -I .docs/tickets/T-141/revisores/r03_respuestas_raras.py <dir>
.venv/bin/python .docs/tickets/T-147/mutantes.py <copia t147_mut> --ticket T-147
/home/user/robotinvestor/.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
(cd bloque_a/11_Ejecutor && /home/user/robotinvestor/.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a | wc -l)
```
