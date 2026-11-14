# T-118 · Bloque A: hallazgos abiertos de la QA r02 de T-112 (H-09 a H-15)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO, 14-11-2026) |
| Pieza | bloque_a (11_Ejecutor, motor) |
| Planifica · implementa · QA | claude (encargo del operador) · claude (un agente, en una copia de trabajo aparte) · un revisor que no haya implementado |
| Aprobación del operador | no necesaria: son correcciones de hallazgos de una QA. Las decisiones que la especificación deja abiertas van como `[PROPUESTO]` en INC-T118-01 (el operador pidió que el agente decida por defecto y lo deje apuntado) |
| Deuda técnica | T-118 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la añade quien encarga el ticket) |

## Objetivo

Corregir los siete hallazgos que la QA r02 de T-112 (veredicto APTO) dejó abiertos en el Motor Fase 2 del Bloque A: tres medios (H-09, H-10 y H-11) y cuatro bajos (H-12 a H-15). Su reproducción está en `.docs/tickets/T-112/qa.md`, sección «Ronda r02», tabla «Hallazgos nuevos».

## Alcance

- **Entra:**
  - `motor/fichas_riesgo.py` (H-09 y H-10), `motor/fichas_series.py` y `motor/fichas_reales.py` (H-12) y `motor/servicio.py` (H-11, H-13 y H-14);
  - las pruebas nuevas (`tests/test_t118_hallazgos.py`);
  - las cifras de los documentos de T-112 (H-15);
  - INC-T118-01 en `docs/incidencias.md`.
- **No entra:**
  - fichas nuevas ni cambios de método;
  - el grupo V, que no usa números de la configuración;
  - las observaciones sin hallazgo de la QA r02 (la caché entrega el mismo objeto a todos los clientes, TEM-DIFF-001 y el año en curso, ALT-DESMOOTH-001 sin dominio superior);
  - la deuda técnica, el diario y la memoria, que los lleva quien encarga.

## Diseño

- **Contratos.** CT-09 y CT-10 no cambian de forma. En el Registro de cálculos (esquema V2.0):
  - el `artefacto` de un SERVICIO gana `configuracion_usada`;
  - la `reejecucion` gana `configuracion`;
  - se usa por primera vez la categoría `ERROR_REEJECUCION`, que el esquema ya tenía.
- **Estado persistido.** No hay migración. Las entradas anteriores del RC, sin `configuracion_usada`, se siguen pudiendo re-ejecutar.
- **Números y su origen.** Tabla de cotas en `analisis-tecnico.md`. Salen de la configuración (`horizontes.H5`, `calendario`, `senales.ventana_anios`), de una ficha (SIM-MC-001, REG-HMM-001) o del Documento 0 (número de horizontes). Tres son `[PROPUESTO]` en INC-T118-01: 1 000 configuraciones en BT-PBO-001, 20 variables en ML-PRED-001 y 32 niveles de anidamiento de una petición.
- **Cómo falla cerrado.**
  - Un dato posterior al corte, o mayor que su cota, se rechaza: no se recorta.
  - Una petición mal formada es RECHAZADO con su entrada en RC, nunca una excepción.
  - Una re-ejecución que la ficha rechaza queda registrada con `coincide` NO.
  - Si no consta la configuración con que se calculó, o ya no es la vigente, no se culpa al cálculo original.
- **Decisiones `[PROPUESTO]`.** INC-T118-01.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Las cotas nuevas rechazan algo que antes se servía | Un cliente con una historia de más de 2 520 observaciones recibe RECHAZADO | La cota es la que el grupo S ya aplica a sus series y sigue a la configuración. Los ciclos simulados no cambian (`tests/test_integracion.py`) |
| El artefacto del RC crece | Más bytes por servicio | Solo se guardan las secciones que la ficha lee. La mayor es `parametros_ht03`, que solo lee DEC-VOI-001 |
| Otro agente añade fichas a los mismos módulos | Conflictos al fusionar | Cambios localizados: las cotas de R van en un bloque aparte tras `UMBRALES`, y no se reordena ni se reformatea nada |

## Criterios de aceptación (binarios)

1. CA-1 (H-09): ML-PRED-001, y cualquier otra ficha del grupo R con datos fechados, rechaza («no conocible») un dato fechado después de la fecha de corte. El dato del día del corte se sirve.
2. CA-2 (H-10): cada dato de las nueve fichas del grupo R tiene cota. Justo en la cota se sirve y con un elemento más se rechaza. El servicio más caro que admiten las cotas termina en torno a un minuto.
3. CA-3 (H-11):
   - el artefacto guarda la configuración que la ficha usó, y CT-10 re-ejecuta con ella;
   - tras un cambio de configuración, un cálculo correcto no recibe ERROR_ORIGINAL;
   - un artefacto sin ese registro se sigue re-ejecutando y, si no coincide, es CONVENCION_DISTINTA.
4. CA-4 (H-12): las cotas de S y P que salen de la configuración siguen a la configuración del Motor. La discrepancia de H2 queda aclarada en una incidencia.
5. CA-5 (H-13): ninguna excepción escapa de `Motor.servir` con los casos del hallazgo. Cada llamada deja una entrada en RC.
6. CA-6 (H-14): `reejecutar` registra con `coincide` NO y `ERROR_REEJECUCION` la re-ejecución que la ficha rechaza.
7. CA-7 (H-15): los documentos de T-112 dicen 136 casos de control en la Fase 2 (S 36, R 36, V 38, P 26) y 6 de AUD-REX-001, comprobado al ejecutar.
8. CA-8:
   - los 136 casos de control y los 6 de AUD-REX-001 siguen superados;
   - `tests/test_integracion.py` y `tests/test_t112_motor.py` siguen en verde;
   - ruff no pasa de 2902 ni mypy de A de 109, y los cuatro gates de árbol pasan;
   - cada corrección tiene un mutante que alguna prueba mata.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t118_hallazgos.py::test_h09_*` | Regresión, límite (el día del corte) y fallo cerrado | CA-1 |
| `test_t118_hallazgos.py::test_h10_*` (17 cotas, cada una en su borde) | Límite y fallo cerrado | CA-2 |
| `costes_motor` (medida por `Motor.servir`, en `pruebas.md`) | Medida | CA-2 |
| `test_t118_hallazgos.py::test_h11_*` | Regresión, migración (artefacto anterior) e integración | CA-3 |
| `test_t118_hallazgos.py::test_h12_*` | Regresión y límite | CA-4 |
| `test_t118_hallazgos.py::test_h13_*` | Fallo cerrado y límite (profundidad) | CA-5 |
| `test_t118_hallazgos.py::test_h14_*` | Regresión | CA-6 |
| `verificar_casos_control` (por `r02_07` y `r02_09`) | Nominal | CA-7, CA-8 |
| Scripts `r02_*` del revisor, sin tocar | Regresión independiente | CA-1 a CA-6 |
| 50 mutantes en una copia desechable | Mutación | CA-8 |
| `tests/test_fase2_*.py`, `test_t112_motor.py`, `test_t113_deuda.py`, `test_t106_*.py`, `test_integracion.py` y la suite completa de A | Regresión | CA-8 |

## Scripts

Ninguno nuevo en `.docs/scripts/`. Usa `nuevo_ticket.sh`. Los scripts de medida y de mutantes de este ticket están en `.docs/tickets/T-118/revisores/` (`impl_costes_motor.py` e `impl_mutantes.py`).

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · EN QA · claude · H-09 a H-15 corregidos en la rama local `t118-trabajo`, cada uno con su prueba de regresión y su mutante. Decisiones en INC-T118-01. Falta la QA de un revisor que no haya implementado
- 2026-11-14 · CERRADO · QA r01 APTO (revisor nuevo sin contexto): los siete hallazgos corregidos; `r02_01` completo (15 986 llamadas, 0 escapes); CT-10 da SI en las 56 fichas con caso de control; ciclo V5 idéntico salvo el campo nuevo del RC; 72 mutantes, 56 muertos y 11 equivalentes. Quedan abiertos un medio (H-01) y cuatro bajos (H-02, H-03, H-05, H-06), y uno medio fuera de alcance (H-04, de T-106): a la deuda en T-121
