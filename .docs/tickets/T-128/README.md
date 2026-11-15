# T-128 · Bloque A, Motor: fichas que entregan cifras por componente con su identificador

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/motor/`) |
| Planifica · implementa · QA | Claude · Claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «me parece genial» (punto 2 de la lista de tareas de la noche) |
| Deuda técnica | T-128 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que ninguna ficha del Motor entregue la cifra de un activo, una sociedad o un emisor concreto con su identificador: eso es del Bloque B. El Catálogo lo dice en las fichas de agregados («las sociedades individuales solo como componentes del agregado», 1.6).

## Hallazgo de partida

Al revisar el informe de T-127 (15-11-2026): REI-NAV-001 (`motor/fichas_reales.py`) devuelve en `componentes` la prima, el peso, el NAV y el NAV ajustado de cada sociedad con su `id`, y en `rango_pct` el mínimo y el máximo individuales. Su ficha pide «prima/descuento agregado y su dispersión». Candidatas por la misma búsqueda: IDX-REB (`por_componente`, `fichas_mon_idx.py`) y REI-FFO (`por_comp`, `fichas_reales.py`).

## Plan

1. Revisar las 80 fichas con manejador: qué salidas llevan identificadores de componentes, y si la ficha del Catálogo lo pide (un índice o una cesta pueden necesitarlo) o lo prohíbe.
2. Donde no se pueda entregar: quitar las filas por componente y los estadísticos de orden con pocos componentes, aplicando la regla de T-127 (`FRONTERA_B` en `motor/fichas_p2.py`: casi clones, dominancia, estadísticos de orden con 7 componentes o más).
3. Casos de control (`verificar_casos_control`) en verde; pruebas en `tests/test_t128_*.py`; decisiones en INC-T128-01.

## Diseño (añadido al implementar)

- Regla (INC-T128-01, `[PROPUESTO]`): ninguna salida ni limitación con el identificador de un componente; mínimo, máximo y
  rango con 7 distintos o más; subconjuntos (subcategorías, segmentos, cestas) con el mínimo de la ficha; en los agregados
  ponderados de sociedades, las reglas de `frontera_b` de T-127 (copias a escala, dominancia de una base y de la aportación).
- Números nuevos, en `UMBRALES` de `motor/fichas_reales.py` con su origen: `componentes_minimos_dispersion: 3` (REI-NAV-001)
  y `componentes_minimos: 2` (REI-FFO-001). Los demás salen de `FRONTERA_B` y de los mínimos que ya tenían las fichas.
- Contratos y esquemas: ninguno cambia (ningún golden cubre estas salidas; `goldens_ct.py` coincide). La forma del
  resultado de CT-09 cambia en las seis fichas: claves que desaparecen (`componentes`, `cobertura_por_componente`,
  `por_componente`, `financiacion_por_plataforma_pct_anual`, `pesos`), claves que pueden ser `null` y tres nuevas
  (`n_componentes` y `antiguedad_nav_dias_max` en REI-NAV-001, `n_componentes` en REI-FFO-001, `ponderada_entre_min_y_max`
  en FON-DISC-001).
- Falla cerrado: copias, dominancia y aportación de la cifra principal rechazan (`DATOS_INSUFICIENTES`, sin citar
  componentes); lo demás va a `null` con su limitación.

## Criterios de aceptación (binarios)

1. CA-1: una tabla, en `analisis-tecnico.md`, de las 80 fichas con la decisión y su motivo.
2. CA-2: ninguna salida de las fichas corregidas contiene el `id` de un componente ni una cifra individual reconstruible (prueba por ficha). **Matizado en la ronda r02 (QA r01, H-01):** «reconstruible sin construir los componentes a propósito»; un componente troceado por quien pide da su cifra (límite declarado, INC-T128-01 e INC-T127-01 «Ronda r03», pregunta para T-57).
3. CA-3: casos de control 67/67 (o los que haya) y gate 12/12.

### Ronda r02 (QA r01: H-01 alta, H-02 media, H-03 y H-04 bajas)

4. CA-4 (H-01): declarado con su alcance en INC-T128-01 (y la decisión común en INC-T127-01 «Ronda r03»); una prueba fija
   el límite (REI-FFO-001 e IDX-REB-001 troceados se sirven) y otra el aviso de REI-NAV-001 (A con su NAV por acción ±4 %).
5. CA-5 (H-02): CHR-FLOW-001 con una moneda estable, con dos copias a escala o con una de más del 95 % de la oferta se
   rechaza; con un crecimiento que aporta casi entero una, el crecimiento es `null`; el caso de control no cambia. Revisada
   la tabla de CA-1: IDX-CONC-001 (amplitud y contribución de un componente, o dominada) corregida igual.
6. CA-6 (H-03): CHR-FLOW, PRV-CF y PRV-PME (y en general las que reciben el agregado hecho) declaradas en INC-T128-01.
7. CA-7: `r01_01_barrido_un_componente.py` sin CHR-FLOW-001 entre las que se sirven con uno; `r01_02_troceo_y_una_moneda.py`
   con la vía «U» en «ok» y la «T» explicada en `pruebas.md`; casos de control 67/67; mutantes muertos; cuotas sin subir.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · Claude · revisión de las 80 fichas (tabla de CA-1 en `analisis-tecnico.md`): cambian 6 (REI-NAV-001, REI-FFO-001, IDX-REB-001, CHR-FUND-001, FON-DISC-001, FON-TD-001); las reglas de T-127 pasan a `motor/frontera_b.py`; INC-T128-01
- 2026-11-15 · EN QA · Claude · `tests/test_t128_frontera.py` (32), mutantes 21/21, casos de control 67/67, suites del Motor y vecinas en verde, ruff 2902 y mypy A 109; falta `./tools/check_all.sh` en el commit y la QA de un revisor nuevo
- 2026-11-15 · NO APTO · revisor nuevo (QA r01) · H-01 (alta, una sociedad o un valor troceados dan su cifra; la raíz de T-127 H-04), H-02 (media, CHR-FLOW-001 con una moneda estable), H-03 (baja, flujos ya agregados sin declarar), H-04 (baja, fila de la deuda)
- 2026-11-15 · EN CURSO · ronda r02 · Claude · junto con la r03 de T-127: H-01 declarado (los componentes los aporta quien pide), aviso en REI-NAV-001; H-02: CHR-FLOW-001 con 2 monedas distintas y dominancia, e IDX-CONC-001 (la «otra igual» de la tabla); H-03 declarado; H-04: la fila ya está en el árbol principal
- 2026-11-15 · EN QA · ronda r02 · Claude · `tests/test_t128_r02.py` (17), mutantes de `T-127/revisores/impl_r03_mutantes.py` 29 de 29, casos de control 67/67, scripts del revisor explicados en `pruebas.md`, suites del Motor y vecinas en verde, ruff 2902 y mypy A 109; falta `./tools/check_all.sh` en el commit y la QA r02
- 2026-11-15 · CERRADO · QA r02 APTO (revisor nuevo sin contexto); hallazgos (H-05 media: IDX-CONC con copias a escala; H-06 baja) en T-135
