# T-120 · Bloque A: IBAN con separadores (R8) y máximo de lecciones en la configuración

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor: `contratos.py`, `evaluador.py`, configuración) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | no necesaria (corrección; el agente decide por defecto desde el 13-11-2026) |
| Deuda técnica | T-120 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Corregir dos hallazgos que la QA r01 de T-116 encontró fuera de su ticket.

## Alcance

- Entra:
  - R8: un IBAN español escrito en grupos de cuatro con espacio, punto o guion se detecta como dato sensible, igual que escrito todo junto;
  - el máximo de lecciones por encargo sale de `aprendizaje.lecciones_por_encargo` (10, el del 12.3 del Documento 0).
- No entra:
  - números de tarjeta: no hay ningún patrón hoy y uno de 16 cifras daría falsos positivos con series y códigos; queda en la deuda;
  - IBAN de otros países; el Bloque A Forex, que tiene el mismo patrón (un bloque por tarea; además no se integra).

## Diseño

- `contratos.RE_SECRETO`: `ES`, dos cifras y cinco grupos de cuatro con un separador opcional (espacio, punto o guion) entre grupos. Sigue exigiendo mayúsculas y límite de palabra.
- `Evaluador.lecciones_vigentes`: `max_n` por defecto es el parámetro de configuración; un argumento explícito sigue mandando.
- Contratos y estado persistido: no cambian. Los goldens de contratos no cambian (el patrón no está en las tablas congeladas).
- Cómo falla cerrado: el mensaje con el dato se rechaza íntegro y deja incidencia SEGURIDAD sin el valor, como cualquier otro dato sensible.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Falsos positivos | Un mensaje legítimo rechazado | Diez textos legítimos probados (ISIN, índices, series de cuatro cifras, IBAN incompleto o con dos espacios) |

## Criterios de aceptación (binarios)

1. CA-1: el IBAN se detecta junto y con espacio, punto o guion entre grupos, también dentro de listas y diccionarios.
2. CA-2: un CT-04 cuyo comentario lleva solo un IBAN con espacios se rechaza y el IBAN no queda en ningún archivo.
3. CA-3: los diez textos legítimos no se marcan.
4. CA-4: el máximo de lecciones es el de la configuración, también con una configuración parcial, y cambia al cambiarla.
5. CA-5: las suites de contratos, de secretos y los goldens siguen en verde; gate 12/12.

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| `test_el_iban_se_detecta_con_y_sin_separador_entre_grupos` (4) | nominal | CA-1 |
| `test_un_ct04_con_solo_un_iban_con_espacios_se_rechaza_y_no_queda_en_ningun_archivo` | regresión | CA-2 |
| `test_lo_que_no_es_un_iban_espanol_no_se_marca` (10) | límite | CA-3 |
| `test_el_maximo_de_lecciones_sale_de_la_configuracion` | nominal | CA-4 |

## Scripts

Ninguno.

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN QA · claude · corregido, con 16 pruebas en `tests/test_t120_r8_y_lecciones.py`
