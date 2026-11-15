# T-140 · Bloque A: hallazgos de las QA de T-131 r02, T-136 y T-134

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/contratos.py`, `bloque_a/evaluador.py`); `.docs/scripts/estimar_coste_ciclo_a.py`, `comprobar_datos_a.py`, `borrador_anexo_b.py` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; 2026-11-15: los tickets nuevos, con QA APTO |
| Deuda técnica | T-140 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| T-136 H-01 (media): la cota cobraba `max_tokens` una vez por llamada | Se suma petición a petición: cada intento (el original y cada reparación de JSON, `llm.reintento_reparacion`) y cada continuación de `pause_turn` reenvía lo ya generado y paga su `max_tokens` |
| T-136 H-02 (media, regresión): una tarjeta junto a otro número de 4 cifras no se detectaba | En cinco o más grupos de 4 cifras, la serie se reparte en tarjetas válidas desde el principio o el final y lo que sobra tiene que tener forma de fecha (MMAA o año): tarjeta con caducidad, año delante, con guiones y dos tarjetas seguidas se detectan |
| T-136 H-03 (baja): IBAN con el resto en minúsculas o en tipo título, y por tramos nacionales de una cifra | Declarado en INC-T123-01: admitirlos reabre el ISIN seguido de palabras |
| T-136 H-04 (baja): mutantes C03 y C12 sin prueba | Pruebas que los matan |
| T-131 H-05 (media): la comprobación validaba toda la historia | Valida la ventana del ciclo (la más larga de `senales` y `tasa_base`); un dato malo anterior deja el símbolo OK con un aviso |
| T-131 H-06 (baja): el borrador trataba CT-09 y CT-10 como retornos de `ESQUEMAS` y fijaba «null cuando no aplica» | CT-09 y CT-10 con su propia propuesta (los sirve el Motor); el cambio de tipo, sin texto fijo |
| T-134 H-19 (baja): «0000-01-01» entraba en F2 y luego hacía perder la FUE- de todas las fuentes | `_fecha_de_calendario` rechaza una fecha que no da fecha de calendario |

## Coste de un ciclo semanal C1 (tarifa del 15-11-2026, USD)

| Tipos activos | Llamadas | Suelo | Cota superior |
| --- | --- | --- | --- |
| Solo divisas | 8 | 0,86 | 4,58 |
| Los 12 tipos | 77 | 2,98 | 56,79 (con hasta 240 búsquedas) |

## Criterios de aceptación (binarios)

1. CA-1: `tests/test_t140.py` y las pruebas vecinas en verde.
2. CA-2: `.docs/tickets/T-136/revisores/r01_02_cota_por_peticion.py`: la cota cubre los escenarios A y B; `r01_01_iban_tarjetas_formas.py`: las tarjetas junto a otro número, detectadas (lo que falla está declarado); `r01_03_mutantes.py`: C03 y C12 mueren.
3. CA-3: gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado
- 2026-11-15 · claude · renumerado de T-137 a T-140: otra sesión usó T-137 y lo subió antes
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto, revisado como T-137); hallazgos (H-01 y H-02 medios, H-03 a H-06 bajos) en T-145
