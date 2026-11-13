# T-106 · Motor Fase 1: las 21 fichas V5.0 (IDX, FON, DER, MON, TCV) y su promoción en el Catálogo

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r03) |
| Pieza | `bloque_a/11_Ejecutor` (`bloque_a/motor/`) y el Catálogo del Motor (`bloque_a/04_Motor_conocimiento_y_catalogo/`, corpus congelado) |
| Planifica · implementa · QA | claude · claude con tres agentes por familia (MON+IDX, FON+DER, TCV) · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-12: «2) sí, te autorizo» (promover en el Catálogo las fichas que superen sus casos de control, re-congelando el corpus); datos reales «por decidir aún», así que solo sintéticos |
| Deuda técnica | T-106 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (Fase 1 del plan de fases de CLAUDE.md) |

## Objetivo

Dar cálculos citables del Motor a los analistas de IDX, FON, DER, MON y TCV, que hoy solo tienen fichas DOCUMENTADO. Se implementan sus 21 fichas V5.0 con sus casos de control (§20.2 del Catálogo) y se pasan a IMPLEMENTADO las que los superan.

## Alcance

- Entra:
  - las 21 fichas, una por manejador, en `motor/fichas_mon_idx.py`, `motor/fichas_fon_der.py` y `motor/fichas_tcv.py`, con `PARAMETROS_POR_DEFECTO` sacados de cada ficha y `CASOS_CONTROL` sacados de su «Verificación»;
  - la integración en `servicio.py`: `IMPLEMENTADAS` y `CASOS_CONTROL`;
  - `madurez_catalogo()`: el Motor lee la madurez en la tabla del Catálogo y solo sirve lo que tiene código y está IMPLEMENTADO;
  - `Motor.verificar_casos_control()`: ejecuta los casos y los registra en RC (CASOS_CONTROL);
  - `.docs/scripts/promover_fichas_catalogo.py`, la promoción en el Catálogo (fila, línea de madurez y recuento del §1.3), con el corpus re-congelado en el mismo commit.
- No entra:
  - las 35 fichas DOCUMENTADO de la línea V4.0 (Fase 2);
  - los datos reales (sin fuente decidida);
  - la copia `.docx` del Catálogo, que no se edita;
  - VALIDADO (las baterías de `09_Pruebas`, Fase 4).

## Criterios de aceptación (binarios)

1. CA-1: cada una de las 21 fichas tiene manejador y casos de control de su «Verificación», y los supera (`verificar_casos_control`, registrado en RC).
2. CA-2: el Motor sirve exactamente las fichas con código e IMPLEMENTADO en el Catálogo; sin Catálogo legible, ninguna.
3. CA-3: cada ficha rechaza (`ErrorFicha` → RECHAZADO) según su «Aclaración y rechazo» y sus «Entradas mínimas», y es determinista.
4. CA-4: en el Catálogo, las 21 pasan a IMPLEMENTADO en su fila y en su ficha, el §1.3 cuadra (35 IMPLEMENTADO, 11 heredadas, 35 DOCUMENTADO) y el corpus se re-congela en el mismo commit, con el motivo.
5. CA-5: el gate da 12/12, sin subir cuotas.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_fase1_mon_idx.py` (118), `tests/test_fase1_fon_der.py` (122), `tests/test_fase1_tcv.py` (101) | Casos de control, rechazos, determinismo, valores a mano | CA-1, CA-3 |
| `tests/test_t106_motor.py` (27) | Integración: coherencia código ↔ Catálogo, RC, CT-09 por ficha | CA-1, CA-2 |
| `.docs/scripts/promover_fichas_catalogo.py` | Promoción | CA-4 |
| `./tools/check_all.sh` | Gate | CA-5 |

## Registro

- 2026-11-12 · ABIERTO · creado con nuevo_ticket.sh, tras la autorización del operador
- 2026-11-12 · EN QA · 21 fichas implementadas (tres agentes por familia) e integradas; casos de control de las 21 fichas superados (50 casos); promovidas en el Catálogo y corpus re-congelado; ruff 2938 → 2908
- 2026-11-12 · NO APTO · QA r01 (revisor nuevo, commit `7064f60`): H-01 alto (MON-EXP-001 servía sendas que no reproducían la curva), H-02 alto (excepciones no previstas y cifras no finitas tumbaban el CT-09), H-03 a H-05, H-07 y H-08 medios, H-06 y H-09 a H-13 bajos
- 2026-11-12 · EN QA · Ronda r02: el Motor convierte cualquier excepción de una ficha y cualquier cifra no finita en RECHAZADO; Catálogo leído de la raíz configurada, solo en la tabla del §4 y releído si cambia; MON-EXP rehecho (todos los nodos, falla cerrado); validación de entradas y casos de control reforzados en las tres familias (66 casos); 562 pruebas del Motor Fase 1
- 2026-11-13 · NO APTO · QA r02 (revisor nuevo, commit `4be8ea6`): H-14 alto (una petición bajaba los umbrales de MON e IDX), H-15, H-16 y H-18 medios, H-17 y H-19 a H-21 bajos
- 2026-11-13 · EN QA · Ronda r03: umbrales fijos en MON e IDX; peticiones mal formadas rechazadas y en RC; incertidumbre de las probabilidades de MON-EXP con limitación; `nivel_es` de DER-VRP en 0,90–0,99; decisiones de MON-EXP y política de no finitos en INC-T106-01; 45 pruebas nuevas, 0 mutantes vivos de la r02
