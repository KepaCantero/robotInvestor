# T-150 · Bloque A: hallazgos bajos de la QA r01 de T-149 (dos datos pegados, limpiar antes de recortar, el resumen sin R8, copias truncadas, BCE y ficheros que no se leen)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/cadena_b.py`, `bloque_a/motor/frontera_b.py`, `README.md`, `tests/test_t150.py`, `tests/test_t149.py`, `tests/test_t144.py`); `.docs/scripts/cadena_a_b.py` y `descargar_datos_bce.py`; `docs/incidencias.md` (INC-T127-01 y INC-T142-01, rondas T-150) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | no necesaria (corrección de hallazgos bajos); 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; lo nuevo va como `[PROPUESTO]` |
| Deuda técnica | T-150 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; no se toca aquí) |

## Objetivo

Cerrar los hallazgos bajos H-01 a H-06 y las observaciones O-01, O-04, O-05 y O-06 de la QA r01 de T-149 (`.docs/tickets/T-149/qa.md`, veredicto APTO), con los scripts del revisor (`.docs/tickets/T-149/revisores/r01_0*.py`) terminando con 0.

## Alcance

- Entra: H-01 (`sin_datos_protegidos` con dos datos pegados), H-02 (`_cli` de `cadena_a_b.py` recorta antes de limpiar), H-03 (pruebas de las limpiezas de los mutantes N21 y N27), H-04 (un `opp_id` con un correo en `resumen.json`), H-05 (copias truncadas en IDX-CONC-001, o su declaración) y O-01 (nombrar las tablas de paso por tramo de precio), H-06 y O-05 (BCE: `TIME_PERIOD` vacío, `IncompleteRead`, el mensaje de un traslado a medias, un destino que es un enlace roto), O-04 y O-06 (`cadena_a_b.py` con un `paquete_json` o un `--config-a` que no se leen).
- No entra: los límites del detector de R8 (INC-T123-01; O-03: lo que el detector no ve pegado a una letra); la atomicidad entre ficheros del traslado del BCE (límite declarado en T-149); la amplitud con copias (T-144 H-05, del operador); `consumo.py`, `orquestacion.py`, `agentes.py`, `llm.py`, `estimar_coste_ciclo_a.py`, `test_t145.py`, `test_t146_presupuesto.py` y `test_t148.py` (otra revisión); los otros bloques, el marco común de C, la Constitución y el corpus congelado; la fila de la deuda.

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| H-01 | `sin_datos_protegidos` sustituye **tramos**: cada aparición de cada dato que ve el detector es un intervalo del texto original; los que se solapan o se tocan se unen y cada unión se sustituye una vez (`_sin_tramos`). La comprobación final (aviso entero si queda algo) no cambia |
| H-02 | `_cli`: `sin_datos_protegidos(r.stderr)[-2000:]` (y lo mismo con el stdout que no es JSON, a 1000); `main` vuelve a limpiar lo que imprime |
| H-03 | Dos pruebas en `tests/test_t149.py` (el fichero que fija el script de mutantes del revisor): el correo junto al carácter 200 de un mensaje de `jsonschema` (N21) y un `FalloEjecutor` con datos que `main` imprime (N27) |
| H-04 | Todo lo que va a `resumen.json` y a la salida pasa por `_sin_datos` (cada texto, claves y valores, por `sin_datos_protegidos`) |
| H-05 | Hipótesis de copia truncada: cada serie se prueba redondeada (centro p̃, media anchura q/2p̃) y truncada hacia abajo (centro p̃ + q/2, media anchura (q/2)/(p̃ + q/2)); un par es copia si cabe en alguna de las cuatro combinaciones (`_pares_por_hipotesis`). Solo se desplazan los precios con q/p ≤ `tolerancia_clon`. Las tablas por tramo (MiFID II) y el redondeo hacia arriba quedan declarados |
| H-06, O-05 | `TIME_PERIOD` vacío (NaT) → `RespuestaBCE`; `http.client.HTTPException` capturada; `EscrituraIncompleta` con los CSV ya movidos y su mensaje; un destino o una carpeta de su ruta que es un enlace simbólico roto → `DestinoNoValido` antes de descargar |
| O-04, O-06 | `cadena_a_b.py`: el `--config-a` se lee y se mira antes de nada (diccionario; `cadena_b` y su correspondencia, diccionarios); un `paquete_json` que no existe, no es JSON o no es un objeto → `sin_envio` `PAQUETE_ILEGIBLE`. Mensaje sin el contenido (de `yaml`, solo el tipo y la posición) y código 1 |

- Contratos y esquemas: no cambian (goldens coinciden). Estado persistido: no cambia. Códigos nuevos: `PAQUETE_ILEGIBLE` (motivo de `sin_envio` en el resumen del script, no de la librería).
- Números: ninguno nuevo. El umbral de desplazamiento es `tolerancia_clon` (el tope de la cota que ya existía) y la tolerancia numérica, `tolerancia_numerica_copias`.
- Falla cerrado: la hipótesis truncada solo agrupa más (la amplitud no se sirve); lo que no se lee no ejecuta ni envía nada; un traslado a medias no se presenta como «nada escrito».
- `[PROPUESTO]`: la hipótesis truncada y su umbral (INC-T127-01, ronda T-150).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La hipótesis truncada agrupa series distintas | Amplitud no servida en índices de verdad | Medido con 300 semillas (`medir_truncado.py`, `T-149/medir_copias.py`): índices y rentabilidad total, 0; solo suben tres casillas del límite declarado de los fondos frente a su índice con pasos del ~1 % del precio. Sin el umbral por precio, un monetario a 1,00 se agrupaba (prueba) |
| Coste del doble de filas | IDX-CONC-001 más lento | n = 2000, T = 2520: de ~3,2 s a ~5,7 s, de 551 a 698 MB (cota de la prueba, 60 s) |
| Los textos que mutan los scripts de mutantes cambian | Sus scripts no corren | Las líneas que mutan se conservan tal cual (M17, M18, Q08–Q10, N06–N12, N21, N25–N27, N30–N35) |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): `r01_03_r8_y_g3_qa.py` R1 en OK; dos datos que el detector ve, pegados, sin rastro (`test_t150.py`).
2. CA-2 (H-02): R4 en OK; con el corte de 2000 o de 1000 dentro del dato, ningún trozo en el mensaje.
3. CA-3 (H-03): `r01_02_mutantes_qa.py` con N21 y N27 muertos y 0 vivos.
4. CA-4 (H-04): R3 en OK; ningún dato de R8 en `resumen.json` ni en la salida.
5. CA-5 (H-05, O-01): `r01_01_rejillas_qa.py` con 0 hallazgos; las tablas por tramo nombradas en INC-T127-01; falsos positivos en 0 con series truncadas.
6. CA-6 (H-06, O-05): `r01_04_bce_qa.py` con 0 hallazgos; fila sin fecha y lectura cortada → 1, mensaje, nada escrito; el traslado a medias nombra lo escrito.
7. CA-7 (O-04, O-06): paquete o `--config-a` que no se leen → mensaje sin el dato, código 1, sin traza ni envío.
8. CA-8: mutantes de `T-149/revisores/r01_02_mutantes_qa.py`, `T-147/mutantes.py` y `T-150/mutantes.py` muertos; suite completa de A en verde; ruff ≤ 2838, mypy A ≤ 109; `refs_vivas`, `secrets_scan`, `nfc_check`, `corpus_integridad` (695) en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t150.py::test_h01_*` | nominal, límite, regresión | CA-1 |
| `test_t150.py::test_h02_*` | límite, regresión | CA-2 |
| `test_t149.py::test_t150_*` | regresión de mutantes | CA-3 |
| `test_t150.py::test_h04_*` | fallo cerrado, regresión | CA-4 |
| `test_t150.py::test_h05_*`, `test_t144.py::test_t149_la_cota_de_niveles_…` | nominal, límite, falsos positivos, límites declarados | CA-5 |
| `test_t150.py::test_h06_*`, `test_o05_*` | fallo cerrado, regresión | CA-6 |
| `test_t150.py::test_o04_*`, `test_o06_*` | fallo cerrado | CA-7 |
| revisores, mutantes, suite completa, gates | regresión | CA-8 |

## Scripts

`.docs/tickets/T-150/medir_truncado.py` (copias truncadas y falsos positivos; `--modulo` mide otra versión de `frontera_b.py`); `.docs/tickets/T-150/mutantes.py` (22 mutantes del código nuevo); los del revisor de T-149 y de T-147, `T-149/medir_copias.py` y `T-147/mutantes.py`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · claude · plan, implementación y pruebas en la copia `t150` (commit local)
- 2026-11-15 · EN QA · claude · pendiente de QA por un agente que no implementó
