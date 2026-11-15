# T-147 · Bloque A: R8 en la petición al Bloque B y validación de la cadena A→B; comprobación de datos por clases

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/cadena_b.py`, `bloque_a/contratos.py`, `tests/test_t147.py`, `tests/test_t142_cadena_b.py`, `README.md`); `.docs/scripts/cadena_a_b.py`, `comprobar_datos_a.py`, `descargar_datos_bce.py`; `docs/incidencias.md` (INC-T123-01, INC-T142-01, INC-T53-02) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; las decisiones nuevas van como `[PROPUESTO]` |
| Deuda técnica | T-147 (número reservado; la fila la pone la sesión coordinadora: esta copia no toca la deuda) |

## Objetivo

Corregir los hallazgos de la QA r01 de T-142 (`.docs/tickets/T-142/qa.md`) y de la QA r01 de T-141 (`.docs/tickets/T-141/qa.md`) antes del modo sombra: que el Broker no envíe al Bloque B una petición con datos protegidos (R8), que A detecte correos y claves en texto, que la petición solo lleve valores del Anexo B.1 del Bloque B y que una errata en `--clases` no dé un verde.

## Alcance

- Entra: T-142 H-01 a H-05; T-141 H-01 a H-04.
- No entra: el Bloque B (solo se lee su Documento 0, B.1, y su detector para comparar); la deuda técnica; el presupuesto (T-146); T-142 H-06 (la fila de la deuda la cierra la coordinación).

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| T-142 H-02 (media): el Broker no comprueba R8; A no detecta un correo ni `api_key=…` | `construir_peticion` pasa la petición por `contratos.contiene_credenciales` (el filtro de `Mensajeria.validar`) y, si encuentra algo, `ErrorCadenaB("DATOS_PROTEGIDOS")` con los campos y sin el dato: no se escribe, no se envía y no hay CT-04. R8 (`secretos_en_texto`, y con él `contenido_sensible` y `contiene_credenciales`) gana `RE_CORREO` y `RE_ASIGNACION_CLAVE` (INC-T123-01) |
| T-142 H-01 (media): `tipos_secundarios` sin validar | Se validan contra su definición en `$defs/opcion` del esquema del Bloque A (lista de los doce, sin repetir): `ENTRADA_B_INVALIDA` |
| T-142 H-03 (media): `cadena_b.peticion` sin validar | `ENUMERACIONES_B1` (las de B.1: `nivel`, `prioridad`, perfil), `RE_IDIOMA` (como «es-ES») y claves y símbolos sin espacios: `CONFIGURACION_CADENA_B` |
| T-142 H-04 (baja): la sonda arrastra `x_clave_universo` | Se quita del encargo copiado; solo la pone la tabla |
| T-142 H-05 (baja): mutante `muta_paquete` vivo | `test_no_muta_el_paquete` usa una copia propia del paquete, sin la extensión, y comprueba que el encargo es otro objeto |
| T-141 H-01 (media): `--clases XXX` da «0 de 0 OK» y código 0 | `choices` con los doce tipos (`configuracion.CLASES`), `nargs="+"`, y código 2 si el universo filtrado queda vacío |
| T-141 H-02 (baja): docstring del BCE | Fijación de las 14:15 (CET), publicada hacia las 16:00 (CET); el «cierre» es esa fijación; qué pasa con un ciclo antes de las 16:00 |
| T-141 H-03 (baja): respuestas raras | `leer` valida todo antes de escribir (columnas, monedas, fechas repetidas, fechas, series vacías); se escribe en una carpeta temporal y se mueve al final; mensajes y código 1 en vez de trazas |
| T-141 H-04 (baja): TARGET frente a `ps2_festivos` | Documentado como pregunta para T-57 en INC-T53-02, sin cambiar la configuración |

- Contratos y esquemas: ninguno cambia (los goldens de contratos coinciden). La petición CT-B-01 sigue con los campos de B.1.
- Estado persistido: no cambia.
- Números: ninguno nuevo en la ruta de decisión. Los de R8 (64 y 63 de RFC 5321; 6, 12 y 16 caracteres del valor de una clave) llevan su motivo en `contratos.py` y en INC-T123-01 (`[PROPUESTO]`); el 6 es el del detector del Bloque B.
- Falla cerrado: todo lo nuevo termina en `ErrorCadenaB` con código, en `SystemExit(2)` del script o en código 1 sin escribir nada.

## Criterios de aceptación (binarios)

1. CA-1 (H-02): una petición con un correo, `api_key=…`, `token: <clave>` o un IBAN en cualquier texto del encargo falla con `DATOS_PROTEGIDOS`, sin reproducir el dato, con y sin correspondencia; `cadena_a_b.py` no la escribe, no llama al Bloque B ni emite CT-04.
2. CA-2 (H-02): R8 detecta las formas de la QA (correo, `api_key=`) y las formas parecidas de la lista, y no marca ninguno de los falsos positivos de la lista; ningún hallazgo nuevo en todo lo que R8 mira en un ciclo simulado de los doce tipos, en su estado y entregables, en los prompts, las plantillas y los goldens; `tests/goldens_ct.py` coincide.
3. CA-3 (H-01, H-03, H-04): `tipos_secundarios` y la configuración fuera del esquema de A o de B.1 fallan cerrado; los valores de B.1 se aceptan; las enumeraciones coinciden con el bloque JSON de B.1; la sonda no lleva clave.
4. CA-4 (T-141 H-01): `--clases` con una clase que no existe, en minúsculas o vacía termina con 2; un universo sin símbolos de la clase, con 2; `--clases DIV` sigue en 0.
5. CA-5 (T-141 H-02, H-03): las respuestas raras de `r03_respuestas_raras.py` terminan con 1 y no escriben nada; la normal escribe las seis series; el docstring dice 16:00 (CET).
6. CA-6: los scripts de los revisores de T-142 (`r01`, `r02`, `r03`) y T-141 (`r03`) dan lo esperado; los mutantes de `.docs/tickets/T-147/mutantes.py` (grupo T-147) mueren; ruff ≤ 2838 y mypy A ≤ 109.

## Plan de pruebas

| Prueba (`tests/test_t147.py` salvo que se diga) | Tipo | Criterio |
| --- | --- | --- |
| `test_h02_la_peticion_con_datos_protegidos_falla_cerrado`, `test_h02_el_script_no_escribe…` | fallo cerrado, integración | CA-1 |
| `test_h02_r8_detecta…`, `test_h02_r8_falsos_positivos…`, `test_h02_ni_un_falso_positivo…` (ciclo de 12 tipos, prompts, goldens) | nominal, límite, regresión | CA-2 |
| `test_h01_…`, `test_h03_…`, `test_h04_…`; `test_t142_cadena_b.py::test_no_muta_el_paquete` | fallo cerrado, regresión | CA-3 |
| `test_t141_h01_…` | fallo cerrado | CA-4 |
| `test_t141_h02_…`, `test_t141_h03_…` | fallo cerrado, nominal | CA-5 |
| revisores y mutantes | regresión | CA-6 |

## Scripts

`.docs/scripts/cadena_a_b.py`, `comprobar_datos_a.py` y `descargar_datos_bce.py` (cambian); `.docs/tickets/T-147/mutantes.py` (nuevo: mutantes de T-147, T-144 y T-148).

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · claude · plan, implementación y pruebas en la copia `t147` (sin commit)
- 2026-11-15 · EN QA · claude · pendiente de QA por un agente que no implementó
