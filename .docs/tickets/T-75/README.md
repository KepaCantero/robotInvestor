# T-75 · Embudo visible y alarma de sequía (D-22) y tope del contraste del reloj (T-89), marco V0.70

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r02) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | No necesaria: aplica una decisión ratificada (D-22, D-27) y deuda técnica. El operador pidió el 2026-11-10 «reducir la deuda técnica: todo aquello que no dependa de mis decisiones personales» |
| Deuda técnica | T-75 y T-89 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el control no deje de invertir sin que nadie lo vea (P5):
- N muestra cada semana el embudo de las oportunidades;
- si en 60 días no se invierte nada habiendo candidatos validados, se avisa al operador.

Además, el reloj gana un tope para el tiempo sin contrastar.

## Alcance

- **Entra:**
  - `embudo()` y `sequia()` del Orquestador;
  - el aviso O-40 en `barrer()`;
  - `consola.informe_embudo()`;
  - `TOPE_SIN_CONTRASTE_S`.
- **No entra:**
  - el seguimiento de lo descartado (I y SC-4, T-81);
  - el envío por canal externo (T-41).

## Diseño

Detalle en `sistema_global/documentos_0/V0.70_Embudo_y_alarma_de_sequia.md`.
- **Contratos:** no cambian.
- **Estado persistido:** no cambia. El esquema del código pasa a V0.70, con MIG-007 sin cambios en el estado.
- **Números:**
  - `o_dias_sequia` = 60 y `n_dias_embudo` = 7, ratificados;
  - `TOPE_SIN_CONTRASTE_S` = 7 días, `[PROPUESTO]`, que va a T-57.
- **Cómo falla cerrado:**
  - lo ilegible no dispara la alarma ni lanza;
  - `embudo()` y `sequia()` solo leen;
  - un sistema más joven que el plazo no juzga sequía.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La alarma cambia los avisos de las simulaciones largas (doradas, semana) | Pruebas doradas en rojo | Ninguna simulación dura 60 días: las 59 baterías siguen en verde |
| Alarma repetida en cada barrido | Ruido para el operador | Una por plazo, aunque se acuse |

## Criterios de aceptación (binarios)

1. CA-1: con candidatos validados y sin inversiones en 60 días, `barrer()` avisa una vez con O-40 y el embudo; con una inversión, sin candidatos o con un sistema más joven, no avisa.
2. CA-2: el embudo da las que entran, la capa de cada una con su motivo, las salidas con quién y por qué, y las validadas e invertidas del periodo; N lo muestra semanal.
3. CA-3: `embudo()`, `sequia()` e `informe_embudo()` solo leen y no lanzan.
4. CA-4: el reloj rechaza un tiempo sin contrastar por encima de su tope.
5. CA-5: las 59 baterías pasan, MIG-007 encadena desde las versiones anteriores y el gate da 12/12.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_embudo_sequia_t75.py` · `*_sequia*`, `barrer_avisa_*`, `una_sola_alarma_*` | nominal y límite | CA-1 |
| `el_embudo_dice_*`, `y_por_que_salen`, `N_muestra_*` | nominal | CA-2 |
| `sequia_y_embudo_solo_leen`, `*_ilegible_*` | fallo cerrado | CA-3 |
| `contraste_de_*_se_rechaza_H03`, `el_tope_exacto_*` | límite | CA-4 |
| `pruebas_integracion_v053.py` · `v070_*`, cadenas hasta MIG-007 | migración | CA-5 |

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · V0.70 implementada; batería nueva con 24 comprobaciones; 59 baterías en verde
- 2026-11-10 · DETENIDO · QA r01 NO APTO: H-08, H-01 y H-02 medios; H-03 a H-07 bajos. Por indicación del operador («si no supera esta ronda no continúes»), no se abre otra ronda; los hallazgos quedan en la fila T-75 de la deuda. El código de la V0.70 está en develop (commit `d6fbdb6`)
- 2026-11-10 · reabierto por el operador («Abre las rondas detenidas»)
- 2026-11-10 · EN QA · Ronda r02 (V0.73): corregidos H-01 (veto de F anotado y visible en el embudo), H-03 (un análisis cuenta una vez), H-04 (salidas por oportunidad y periodo abierto por la izquierda), H-05 (solo se informa el aviso si se añade), H-07 (días validados) y H-08 (sequía desde la última inversión: con barridos diarios salta); H-02 y H-06 (documentación) también. 34 comprobaciones; pendiente la QA r02
