# T-72 · Estado público del diario y tolerancias del reloj a prueba de NaN (T-72 y T-85, marco V0.69)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO, 10-11-2026) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | No necesaria: es deuda técnica del marco que no depende de él. El operador pidió el 2026-11-10: «reducir la deuda técnica: todo aquello que no dependa de mis decisiones personales» |
| Deuda técnica | T-72 y T-85 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los hallazgos H-05 y H-06 de la QA de T-79. La consola debe ver un diario desincronizado y no depender de sus privados. Las tolerancias del reloj no deben poder dejarlo dando instantes sin contrastar.

## Alcance

- **Entra:**
  - `Diario.estado_diario()`, la foto pública de solo lectura;
  - la consola, que la usa;
  - las tolerancias del `Reloj`, de solo lectura y con comparaciones que fallan cerrado;
  - una batería nueva.
- **No entra:** el Orquestador. Tampoco cambian el esquema del código, el estado guardado ni el formato del diario.

## Diseño

Detalle en `sistema_global/documentos_0/V0.69_Estado_del_diario_y_tolerancias_del_reloj.md`.
- **Contratos y estado persistido:** no cambian.
- **Números:** ninguno nuevo.
- **Cómo falla cerrado:**
  - un diario que no se puede comprobar no está sincronizado, y la consola lo pinta ROJO;
  - una tolerancia NaN o que no se compara bloquea el reloj o no da instantes, sin lanzar.
- **`[PROPUESTO]`:** ninguno.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| `estado_diario()` calcula la huella del estado entero | El panel tarda más con estados grandes | Es el mismo cálculo que hace cada operación del diario; el panel no está en el camino de las operaciones |
| Una prueba con un diario falso leía los privados | Fallaría al cambiar la consola | El diario falso gana `estado_diario()` con el mismo caso (líneas booleanas → ROJO) |

## Criterios de aceptación (binarios)

1. CA-1: un cambio por fuera del diario, o su fichero reescrito, sale como desincronizado, y el panel es ROJO antes de la operación que daría DI-06, sin bloquear el diario.
2. CA-2: la consola no lee `_roto` ni `_n`.
3. CA-3: las tolerancias del reloj no se pueden cambiar tras construirlo. Aunque se toque lo privado, un NaN nunca da instantes sin contrastar, y el reloj no lanza.
4. CA-4: las 58 baterías pasan y el gate da 12/12.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_reloj_diario_t72.py` · `un_cambio_por_fuera_*`, `fichero_reescrito_*`, `mirar_no_bloquea_*` | regresión de H-05 | CA-1 |
| `la_consola_usa_la_foto_publica`, `una_foto_ilegible_*`, `si_estado_diario_lanza_*` | fallo cerrado | CA-2 |
| `*_es_de_solo_lectura`, `contraste_NaN_*`, `salto_NaN_*`, `desfase_NaN_*`, `tolerancia_que_no_se_compara_*` | regresión de H-06 y fallo cerrado | CA-3 |
| `.docs/scripts/pruebas_marco.sh` | regresión | CA-4 |

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · V0.69 implementada; batería nueva con 24 comprobaciones, que falla con la V0.68; 58 baterías en verde
- 2026-11-10 · CERRADO · QA r01 APTO (seis hallazgos bajos); H-01, H-02, H-04, H-05 y H-06 corregidos al cerrar (32 comprobaciones); H-03 a la deuda (T-89)
