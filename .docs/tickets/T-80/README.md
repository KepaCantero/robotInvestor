# T-80 · Vía DIRECTA y modo CONSULTA en el Orquestador del marco (V0.68)

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | No necesaria: es una versión del marco que aplica una decisión ya ratificada (D-28, Constitución V0.6). El operador pidió el 2026-11-10: «Continúa con la T-80» |
| Deuda técnica | T-80 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el Orquestador del marco cumpla D-28 (PC3-01, que la V0.67 marcó CONTRADICE):
- el Broker entra por C, D o E con la vía `DIRECTA`, y el expediente nace en el estado de ese bloque;
- una consulta no abre expediente y deja rastro.

## Alcance

- **Entra:**
  - `abrir_directa()` por C, D y E con los mínimos del §2;
  - `consultar()` con el rastro SC-5 en el Orquestador;
  - el registro de análisis vigentes (`analisis_vigentes()`);
  - de la consulta a la decisión (`consulta_id`);
  - integridad, persistencia, diario y migración MIG-006.
- **No entra:**
  - una consulta que encarga un análisis nuevo sin expediente;
  - el SC-5 completo (lo dos, a T-87);
  - entrar por E con varios candidatos: se entra por D y se compara.

## Diseño

Detalle en el Documento 0: `sistema_global/documentos_0/V0.68_Via_directa_y_modo_consulta.md`.
- **Contratos CT-G:** no cambian.
- **Estado persistido:** el Orquestador gana el atributo `consultas`, y los expedientes `DIRECTA` llevan `bloque_entrada`, `analisis_ref` y `consulta_ref`, que van en su identidad. El esquema del código pasa a V0.68, con la migración MIG-006 (el rastro vacío; sin rutas declaradas, porque es un atributo nuevo con su valor inicial).
- **Números:** ninguno de política.
  - `o_max_analisis_consulta` = 50 en `parametros.py`, tope técnico `[PROPUESTO]` (QA r01, H-08).
  - «Nivel bajo» sale de `NIVEL_MIN_POR_DECISION["ABRIR_POSICION"]` (N2, `[PROPUESTO]`, QA r01, H-04): el más bajo con el que se puede invertir.
- **Cómo falla cerrado:**
  - todo se valida antes de crear el expediente: un rechazo no deja nada, salvo lo que el Orquestador registra a propósito en las operaciones que pasan por un encargo, como `emitir_encargo()`: encargos vencidos que pasan a `CADUCADO`, con su aviso (QA r03, H-14, y r04, H-17). `consultar()` no caduca nada;
  - un análisis en duda no se reutiliza (en juego, invertido, en reanálisis, apartado sin ratificar o excluido);
  - por E, con más candidatos vigentes, se devuelve a D;
  - un rastro SC-5 tocado da O-13 con kill-switch en el siguiente punto de decisión.
- **Decisiones del operador usadas como `[PROPUESTO]`:** qué es «nivel bajo» (N2) y el tope de análisis por consulta (50), los dos en T-57. Quién puede entrar (solo el Broker) y los bloques admitidos para una consulta (A a E y K) salen del §2.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Reutilizar un análisis mete por la puerta de atrás un candidato que alguien apartó (T-36) | Se salta la decisión de un gestor o de F | No se reutiliza si algún expediente que lo tiene fue apartado sin ratificar por el operador |
| El mismo sobre en dos expedientes en juego | Un candidato duplicado en D | No se reutiliza si algún expediente lo tiene en juego o invertido |
| D rechaza un sobre que no es del candidato (FORMA) | El expediente reutilizado no se podría comparar | El Orquestador le pasa una copia a nombre del expediente `DIRECTA` (`_candidato_d`) |
| Cambiar la identidad rompe las huellas guardadas | Expedientes de antes no íntegros | Los campos nuevos solo entran en la identidad de los `DIRECTA` |
| Cambio de esquema | Los estados guardados no se cargan | MIG-006 y las cadenas de migración probadas desde la V0.45 |

## Criterios de aceptación (binarios)

1. CA-1: por C, D y E el expediente nace en `EN_ANALISIS`, `VALIDADA` y `COMPARADA`, y llega hasta `EJECUTADA` (C) o `PROPUESTA` (D y E) por las transiciones de siempre.
2. CA-2: cada mínimo del §2 que falta rechaza sin dejar nada (C sin encargo válido; D sin análisis reutilizable ni encargo de nivel bajo; E sin motivo), y E con más candidatos se devuelve a D. F y G no son entrada.
3. CA-3: una consulta no cambia ningún expediente, ninguna comparación ni ningún encargo, y queda en un rastro encadenado cuya alteración se detecta.
4. CA-4: tocar cualquier campo nuevo se detecta en `integridad()`.
5. CA-5: guardar, cargar, el diario y la migración desde estados de versiones anteriores siguen funcionando; las 57 baterías pasan y el gate da 12/12.
6. CA-6: la pasada PC3-01 de la V0.68 da CUMPLE.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_via_directa_t80.py` · `C_*`, `D_*`, `E_*` | nominal e integración | CA-1 |
| `C_sin_encargo_*`, `D_un_analisis_en_juego_*`, `D_lo_apartado_*`, `E_sin_motivo_*`, `E_con_otros_candidatos_*`, `bloque_*` | fallo cerrado | CA-2 |
| `consulta_*`, `tocar_el_rastro_SC5_*` | nominal y fallo cerrado | CA-3 |
| `tocar_*_se_detecta` | integridad | CA-4 |
| `persistencia_*`, `diario_*`; `pruebas_integracion_v053.py` (MIG-006) | migración y regresión | CA-5 |
| `PC3_01_CUMPLE` | pasada de coherencia | CA-6 |

## Scripts

- `.docs/scripts/pruebas_marco.sh`, `.docs/scripts/leeme_marco.py` y `.docs/scripts/gate.sh`.
- `entrega_claude/V0.68/scripts/pc3_01_via_directa.py`, nuevo.

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · V0.68 implementada; batería nueva con 93 comprobaciones; 57 baterías en verde
- 2026-11-10 · QA r01 NO APTO (H-01 alta; H-02 a H-04 medias; H-05 a H-08 bajas); todos corregidos con su prueba (106 comprobaciones)
- 2026-11-10 · QA r02 NO APTO (H-09 media: propuesta caducada y descartada; H-10 a H-12 bajas); corregidos (110 comprobaciones)
- 2026-11-10 · QA r03 NO APTO (H-13 media: análisis superado por el reanálisis de un DIRECTA; H-14 y H-15 bajas); corregidos (112 comprobaciones)
- 2026-11-10 · QA r04 NO APTO (H-16 media: reencargo del origen con el análisis en juego en un DIRECTA; H-17 y H-18 bajas); corregidos (115 comprobaciones); pendiente la r05
