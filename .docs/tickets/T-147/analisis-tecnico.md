# T-147 · Análisis técnico

## Causa raíz

- **T-142 H-02.** `cadena_b.construir_peticion` validaba el encargo contra el esquema de A, pero la petición no pasaba por R8: el Broker de la cadena no es un agente ni usa `Mensajeria`, así que nada miraba lo que salía. Además R8 de A (`contratos.secretos_en_texto`) solo conocía el par JSON `"api_key": "…"`, claves «sk-», AWS, `Bearer`, claves privadas, IBAN, tarjetas y DNI: ni correos ni asignaciones fuera de JSON.
- **T-142 H-01.** `tipos_secundarios` se iteraba sin validar (un texto se troceaba en letras).
- **T-142 H-03.** La configuración solo se comprobaba presente, no dentro de las enumeraciones de B.1.
- **T-142 H-04.** La rama sin clave copiaba el encargo tal cual, con la extensión que trajera.
- **T-142 H-05.** El fixture del ciclo es de módulo y las pruebas anteriores dejaban la extensión en el paquete compartido.
- **T-141 H-01.** `--clases` sin `choices` y `all([])` es `True`.
- **T-141 H-03.** `descargar_datos_bce.py` no validaba nada antes de escribir y escribía símbolo a símbolo.

## Evidencia (antes → después)

| Script | Antes | Después |
| --- | --- | --- |
| `T-142/revisores/r01_ataques_peticion.py --trabajo <dir>` | 27 OK · 14 OBS (41 casos) | **36 OK · 4 OBS** (40 casos: el envío a B de la petición con correo ya no existe porque no se construye). Las 4 OBS son observaciones de la QA, no hallazgos: `horizonte_principal` fuera de `horizontes` (lo debe impedir el esquema de A), una entrada que no es objeto (se ignora) y dos del Bloque B (admite `N9` y tipos en letras: ya no le llegan) |
| `T-142/revisores/r02_cadena_doce_tipos.sh` | 30 enviables, 2 enviadas | igual: 30 enviables, 2 enviadas, ENTREGADA y válidas, 2 RET |
| `.docs/scripts/cadena_a_b.py --sonda-sin-correspondencia` | 3 enviables, 1 enviada | igual (OPP-2024-0002, ENTREGADA, válida, RET-2024-0001); la sonda sigue elegida por B como `divisas_materias_primas` |
| `T-142/revisores/r03_mutantes.py` (copia `t147_mut`) | 9 de 10 muertos (`muta_paquete` vivo) | ver `pruebas.md` |
| `T-141/revisores/r03_respuestas_raras.py <dir>` | trazas en 4 casos, carpeta a medias, repetida resuelta en silencio | 8 casos raros con código 1 y 0 CSV; la normal, 6 CSV |
| `comprobar_datos_a.py --clases XXX` / `div` | «0 de 0 OK», código 0 | código 2 (argparse) |

## Implementación

- `bloque_a/11_Ejecutor/bloque_a/cadena_b.py`: `ENUMERACIONES_B1`, `RE_IDIOMA`, `RE_SIN_ESPACIOS`; `_valores_de_la_peticion`; validación de `tipos_secundarios` con `errores_entrada_b(…, "opcion/properties/tipos_secundarios")` (el validador se cachea por definición); `encargo.pop(x_clave_universo)`; R8 al final con `contiene_credenciales`.
- `bloque_a/11_Ejecutor/bloque_a/contratos.py`: `RE_CORREO`, `NOMBRES_CLAVE_FUERTES`, `NOMBRES_CLAVE_GENERICOS`, `RE_ASIGNACION_CLAVE`, `RE_VALOR_GENERICO`, `_asignaciones_de_clave`; `secretos_en_texto` los usa en el texto y en el texto sin escapes, como el resto.
- `bloque_a/11_Ejecutor/tests/test_t142_cadena_b.py`: `test_no_muta_el_paquete` reforzado (comentado «T-147»).
- `bloque_a/11_Ejecutor/README.md`: códigos de `ErrorCadenaB`.
- `.docs/scripts/cadena_a_b.py`: docstring y la sonda pasa los mismos filtros (si falla, se anota en el resumen).
- `.docs/scripts/comprobar_datos_a.py`: `choices=CLASES`, `nargs="+"`, universo vacío → 2 (y el borde de T-148 H-05, ver T-148).
- `.docs/scripts/descargar_datos_bce.py`: `RespuestaBCE`, `leer`, `escribir` (carpeta temporal y `os.replace`), docstring de las 16:00.
- `docs/incidencias.md`: INC-T123-01 (formas nuevas de R8, falsos positivos medidos, límites, A frente a B para T-57), INC-T142-01 (ronda T-147), INC-T53-02 (TARGET frente a `ps2_festivos`, pregunta para T-57).

**Decisiones `[PROPUESTO]`.** (1) Cualquier correo es un dato protegido, también el de una empresa o de un dominio de ejemplo (el detector no sabe de quién es). Consecuencia en modo vivo: una respuesta con búsqueda cuyo resultado trae un correo de contacto se descarta entera (`llm.AnthropicClient.generar` mira los bloques de la búsqueda con `contenido_sensible`); se medirá en el modo sombra. (2) Asignaciones: con un nombre de credencial inequívoco basta un valor de 6 caracteres (el mínimo del detector del Bloque B) con una cifra o un signo, o 12 letras, para no marcar «contraseña: obligatoria»; con los nombres genéricos (`token`, `secret`, `secreto`) el valor tiene que parecer una clave (16 o más, letras y cifras), para no marcar «token: Uniswap»; las direcciones «0x…» son públicas. (3) La opción no se valida entera contra `$defs/opcion`: el paquete en memoria del ciclo lleva campos internos (`metodo` en los horizontes, puertas booleanas) que no cumplen el esquema; se valida solo lo que entra en la petición.

**Límites conocidos.** No se detecta un correo con la «@» codificada (`%40`, `@`), con una parte local de más de 64 caracteres pegada a otra palabra, ni una clave bajo un nombre que no está en las listas («key:», «clave:») o con un valor de menos de 6 caracteres. Los detectores de A y B siguen sin cubrir lo mismo (INC-T123-01, pregunta para T-57). T-142 H-06 (fila de la deuda) no se toca aquí.

## Comandos

```bash
cd bloque_a/11_Ejecutor
PY=/home/user/robotinvestor/.venv/bin/python
$PY -m pytest -q -p no:cacheprovider tests/test_t147.py tests/test_t142_cadena_b.py
$PY tests/goldens_ct.py
cd ../..   # raíz de la copia, con .venv enlazado
.venv/bin/python .docs/tickets/T-142/revisores/r01_ataques_peticion.py --trabajo <dir>
bash .docs/tickets/T-142/revisores/r02_cadena_doce_tipos.sh .venv/bin/python <dir>
.venv/bin/python -I .docs/tickets/T-141/revisores/r03_respuestas_raras.py <dir>
.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <dir> --sonda-sin-correspondencia
.venv/bin/python .docs/tickets/T-147/mutantes.py <copia con «t147_mut»> --ticket T-147
```
