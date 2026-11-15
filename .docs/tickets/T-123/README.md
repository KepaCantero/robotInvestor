# T-123 · Bloque A: R8, IBAN de otros países y números de tarjeta

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `contratos.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que pases a completar el apartado 3 de huecos menores apuntados en la deuda técnica» |
| Deuda técnica | T-123 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (antes, límite declarado de T-120 y T-122) |

## Objetivo

Que R8 (datos sensibles fuera de los mensajes) detecte también un IBAN de otro país y un número de tarjeta, sin falsos positivos con las series de cifras corrientes.

## Diseño

- Un patrón solo marcaría cualquier serie de cifras, así que el candidato se valida con su dígito de control:
  - **IBAN:** dos letras de país, dos cifras de control y el resto alfanumérico, con hasta dos separadores seguidos (cualquier espacio, punto o guion); la longitud de su país (registro ISO 13616 de SWIFT, `LONGITUD_IBAN`, 42 países: SEPA y algunos más) y el módulo 97 igual a 1.
  - **Tarjeta:** 13 a 19 cifras con un espacio o guion opcional entre ellas; prefijo y longitud de una red corriente (Visa, Mastercard, American Express, Discover, JCB, UnionPay) y el control de Luhn. No vale una serie pegada a un punto o una coma con cifras (la parte de un número decimal). Se devuelve enmascarada.
- Se añade a `secretos_en_texto`, así que vale para todos los caminos de R8 (mensajería, `contenido_sensible`, HT-09).
- Contratos y estado persistido: no cambian; goldens de contratos sin cambios.

## Criterios de aceptación (binarios)

1. CA-1: los IBAN de ejemplo de ocho países se detectan juntos, con espacios, con espacio duro y con guiones; con el control mal, no.
2. CA-2: las tarjetas de prueba de cinco redes se detectan juntas, con espacios y con guiones, y se devuelven enmascaradas.
3. CA-3: once textos con series de cifras corrientes (años, teléfonos, ISIN, CUSIP, decimales del ciclo) no se marcan; 20 000 series al azar sin prefijo de red, ninguna.
4. CA-4: un CT-04 con una tarjeta o un IBAN alemán se rechaza y el dato no queda en ningún archivo.
5. CA-5: goldens de contratos sin cambios; el ciclo simulado, sin rechazos nuevos; gate 12/12.

## Plan de pruebas

`tests/test_t123_r8_iban_y_tarjetas.py` y, desde la r02, `tests/test_t123_r02.py`.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección |
| --- | --- |
| H-02 (alta): tramos de cifras de huellas SHA-256 y UUID pasaban como tarjeta | La tarjeta no admite letra ni cifra pegadas; 100 000 huellas y 3 000 UUID, ninguna marcada |
| H-01 (media): tarjeta con caducidad o CVV, IBAN seguido de una cifra o tras «AB12», IBAN con tres espacios: sin detectar | Ventanas de grupos consecutivos dentro de cada serie; hasta tres separadores |
| H-03 (baja): `pruebas.md` era la plantilla | Rellenado |
| H-04 (baja): importes con espacio de miles y listas de enteros marcados | Grupos de al menos cuatro cifras salvo el último; lo que queda, declarado en INC-T123-01 |


## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN QA · claude · implementado. Al probarlo con el ciclo simulado, tres decimales de las señales del Motor (p. ej. 0.4228715933084759) pasaban como tarjeta y bloqueaban un CT-12: se excluyen las series pegadas a un punto o una coma con cifras
- 2026-11-14 · EN QA · claude · un IBAN seguido de otra cifra ya no se marca (era otra serie); pruebas vecinas (684) en verde
- 2026-11-14 · QA r01 · revisor nuevo · NO APTO (H-02 alta: huellas y UUID como tarjeta; H-01 media; H-03 y H-04 bajas)
- 2026-11-14 · EN QA · claude · ronda r02: los cuatro corregidos (tabla de arriba); la prueba de T-122 de «tres separadores» pasa a «cuatro» (INC-T123-01)
- 2026-11-15 · CERRADO · QA r02 APTO (revisor nuevo sin contexto); hallazgos abiertos (H-05 a H-10) corregidos en T-130
