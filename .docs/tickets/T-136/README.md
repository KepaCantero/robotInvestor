# T-136 · Bloque A: hallazgos de las QA r01 de T-129 y T-130

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/contratos.py`, `config/precios_anthropic.yaml`); `.docs/scripts/estimar_coste_ciclo_a.py` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; 2026-11-15: los tickets nuevos, con QA APTO |
| Deuda técnica | T-136 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| T-130 H-01 (media, regresión): el tope de 4 letras del BBAN dejaba sin detectar IBAN reales de Rumanía, Letonia… | `ESTRUCTURA_BBAN`: la estructura de cada país del registro ISO 13616 («n» cifras, «a» letras, «c» alfanumérico); las 42 cuadran con su longitud |
| T-130 H-02 (media): filas de 8 números de 4 cifras con un espacio marcadas como tarjeta (33 %) | Cinco o más grupos de exactamente 4 cifras seguidos son una fila de tabla: no se miran |
| T-130 H-03 (baja): faltaba VA entre los BBAN solo de cifras | `BBAN_NUMERICO` se deriva de la estructura: 21 países |
| T-130 H-04 (baja): tarjeta tras un campo numérico y una coma («17,<tarjeta>») | Declarado: en español es también un decimal con coma, y excluir decimales es lo que evita marcar las cifras del Motor |
| T-130 H-05 (baja): ISIN seguido de decimales con punto marcado como IBAN | Una cifra suelta en un grupo intermedio corta el IBAN (una letra suelta no: el CIN italiano) |
| (nuevo, al medir) ISIN o índice seguido de palabras en minúsculas en países con BBAN alfanumérico | Las letras del IBAN van en la misma caja que su código de país |
| T-129 H-01 (media): la cota superior no era una cota | La cota paga toda la entrada como escritura de caché, con `factor_tokens_cota` (1,35) y las continuaciones de `pause_turn` en los agentes con búsqueda |
| T-129 H-02 (baja): la estimación no contaba el razonamiento | Pasa a llamarse «suelo» y lo dice; la cota lo cubre (cabe en `max_tokens`) |
| T-129 H-03 (baja): dos mutantes vivos del cliente real | Pruebas de que `output_config` solo lleva el formato y de que la búsqueda es la versión más reciente |

## Coste de un ciclo semanal C1 (tarifa del 15-11-2026, USD)

| Tipos activos | Llamadas | Suelo | Cota superior |
| --- | --- | --- | --- |
| Solo divisas (configuración actual) | 8 | 0,86 | 2,11 |
| Los 12 tipos (`perfiles.activos` con los doce, en un YAML aparte pasado con `--config`) | 77 | 2,98 | 22,60 (con hasta 120 búsquedas) |

## Criterios de aceptación (binarios)

1. CA-1: `tests/test_t136_r8.py` y `tests/test_t136_coste.py` en verde; las pruebas vecinas de R8 y `test_t129_modo_sombra.py` en verde.
2. CA-2: scripts de la QA de T-130 (`r01_01_registro_y_formatos.py` sin más fallo que H-04, declarado; `r01_02_comparacion_r02.py`) y de T-123 (`r02_01` 12/12; `r01_02` 30/30).
3. CA-3: la cota supera cada escenario de `r01_02_sensibilidad_cota.py` de la QA de T-129; goldens coinciden; gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado
- 2026-11-15 · EN QA · claude · renumerado de T-133 a T-136: otra sesión usó T-133 para los hallazgos del banco de medida (T-94) y lo subió antes
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto, revisado como T-133); hallazgos (H-01 y H-02 medios, H-03 y H-04 bajos) en T-137
