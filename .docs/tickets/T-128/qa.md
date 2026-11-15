# T-128 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01 · 2026-11-15
- **Copia revisada:** clon desconectado en `f7faa1b` («wip local: T-127 r02 y T-128»): `motor/fichas_reales.py` (REI-NAV-001, REI-FFO-001, CHR-FUND-001 y sus casos de control), `motor/fichas_mon_idx.py` (IDX-REB-001), `motor/fichas_fon_der.py` (FON-DISC-001, FON-TD-001), `motor/frontera_b.py`; `tests/test_t128_frontera.py` y las pruebas cambiadas de `test_fase1_fon_der.py`, `test_fase1_mon_idx.py` y `test_fase2_reales.py`; INC-T128-01.
- **Orden de lectura:** `README.md` → diff del código → mis scripts → al final `analisis-tecnico.md` (la tabla de CA-1), `pruebas.md` e INC-T128-01.

## Reproducción desde limpio

Desde la raíz de la copia, con `.venv` enlazado al del repositorio (enlace borrado al acabar).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Mi barrido (independiente del del implementador) | `.venv/bin/python -I .docs/tickets/T-128/revisores/r01_01_barrido_un_componente.py bloque_a/11_Ejecutor` | 235 casos de control de 66 fichas por `Motor.servir`. **ID:** solo aparecen nombres de ámbitos o de quien pide (categorías de FON-FLOW, pares de FX-MOM, escenarios de IDX-ERP, regímenes de SCN-H, variables de TCV-SLOPE, muestras de ST-INF, referencias de BIB-MET) y los nombres de las plataformas de CHR-FUND como fuentes sin cifra (declarado). Ninguna de las seis fichas corregidas. **UNO** (cada colección de componentes dejada en uno): REI-NAV, REI-FFO, FON-DISC, FON-TD y CHR-FUND rechazan o no se sirven con uno; se sirven ámbitos (categorías, pares, escenarios, variables, eventos comparables, contrastes) y **CHR-FLOW-001 con una sola moneda estable** (H-02) |
| Mi script de troceo | `.venv/bin/python -I .docs/tickets/T-128/revisores/r01_02_troceo_y_una_moneda.py bloque_a/11_Ejecutor` | **1/3**. Ver H-01 (IDX-REB) y H-02 (CHR-FLOW) |
| Script de T-127 r02 (vías de REI-NAV y REI-FFO) | `.venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py bloque_a/11_Ejecutor` | REI-NAV-001 y REI-FFO-001 dan la cifra de una sociedad (H-01) |
| Mutantes del implementador | `python .docs/tickets/T-128/revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/qa9_mut_t128_mut` | **21 de 21 muertos**. Copia borrada |
| Goldens, gates, cuotas, suite | «Comunes» de `.docs/tickets/T-127/qa.md` (ronda r02) | en verde |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (tabla de las 80 con su motivo) | sí, con una excepción | La tabla está y sus cuentas cuadran (6 cambian, 3 de T-127, 71 no). Muestra contrastada con la ficha del Catálogo leída por su identificador: IDX-CONC-001 (peso de los n mayores con `top_n` en 5–50, HHI, N_ef: agregados del índice, sin identificar; ✔), DER-OPT-001 («contratos genéricos del subyacente … no compara contratos», propósito juzgado por quien pide, declarado; ✔), PRV-CF-001 («flujos agregados; los fondos individuales solo como componentes»: la entrada ya viene agregada; ✔ con H-03), ALT-AUC-001 (dispersión de rentabilidades individuales que pide su «Método», con ≥ 200 pares; ✔), FON-FLOW-001 (filas por categoría, que son ámbitos; ✔) y **CHR-FLOW-001**: la tabla dice «entrega la oferta agregada, sin cifra por moneda», pero con una sola moneda estable la agregada es la suya (H-02) |
| CA-2 (ninguna salida con el `id` ni una cifra individual reconstruible) | **no** | El `id` ya no sale en ninguna (mi barrido y `test_ninguna_salida_ni_limitacion_lleva_el_identificador_de_un_componente`). Pero una sola petición da la cifra de una sociedad en REI-NAV-001 y REI-FFO-001 y la de un valor incluido en IDX-REB-001 (H-01) |
| CA-3 (casos de control y gate) | casos sí; gate no comprobado | `verificar_casos_control` 67/67 (en `.docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py`); el gate entero no se lanza por instrucción |

## Casos de control y pruebas cambiadas (¿se debilitó alguna?)

Leídos en el diff `fb3ccd4..f7faa1b`:

- REI-NAV-001 «método»: con 2 sociedades, la dispersión y el rango pasan a `null` y el NAV ajustado se comprueba en su total en vez de en A; la dispersión con 3 y el rango con 7 se comprueban contra el mismo oráculo en `test_rei_nav_dispersion_desde_tres_y_rango_desde_siete` (rel 1e-12). «NAV = activos − pasivos»: el total ajustado igual al NAV total sustituye a «cada sociedad igual»; con la misma cap rate es la misma identidad sumada (algo más débil: dos errores de signo contrario se compensarían; aceptable). ✔
- REI-FFO-001: cuatro sociedades más con la misma capitalización, FFO y AFFO de 2025 que las tres de antes, para que la mediana y el IQR de la cobertura se sigan comprobando (ahora hacen falta 7 distintos); los múltiplos y el empate del percentil no cambian. ✔
- IDX-REB-001: dos valores por cesta con la misma demanda total (±1e9); `test_idx_reb_demanda_a_mano` comprueba los días de volumen de la cesta con los nuevos volúmenes. ✔
- CHR-FUND-001: la agregada se comprueba contra las de cada plataforma calculadas a mano y ponderadas por su interés abierto (antes, también la de cada una y el peso de P1). ✔
- FON-DISC-001: «P = NAV ⇒ d = 0» con la desviación nula en lugar del máximo (agregado 0 y desviación 0 implican todos 0: igual de fuerte); «agregado entre el mínimo y el máximo», con el indicador `ponderada_entre_min_y_max` que calcula la ficha (antes lo comparaba el caso con las salidas; ambos dependen del mínimo y el máximo que calcula la ficha). `test_disc_valores_a_mano`: rango `null` con 5; el rango con 7 contra `np.ptp` en `test_fon_disc_minimo_maximo_y_rango_desde_siete_miembros`. ✔
- FON-TD-001: el segmento de menos de 5 sin TD lo prueba `test_fon_td_segmento_con_menos_miembros_que_el_minimo`. ✔

Ninguna se rebaja sin que otra compruebe lo mismo con más componentes.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `.venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py bloque_a/11_Ejecutor` (REI-NAV-001 y REI-FFO-001) y `.venv/bin/python -I .docs/tickets/T-128/revisores/r01_02_troceo_y_una_moneda.py bloque_a/11_Ejecutor` (IDX-REB-001) | **Esperado** (CA-2): ninguna cifra individual reconstruible. **Obtenido**, con una sola petición y solo los datos de la sociedad o del valor: **REI-NAV-001**, la sociedad A en 2 partes con el mismo peso y NAV por acción 20/1,04 y 20/0,96 → prima agregada −10 %, la de A, exacta, y su percentil y z frente a la historia; **REI-FFO-001**, X en 2 partes (acciones 40/60 y repartos distintos de cada importe) → P/FFO 13,33, P/AFFO 16,13 y cobertura 1,24, los de X; **IDX-REB-001**, la inclusión única IN (cuya demanda INC-T128-01 dice que no se entrega) troceada en IN-a (0,0007, volumen 3e8) e IN-b (0,0003, 2e8) → demanda 1e9 y 2 días de volumen, los de IN (y lo mismo en las exclusiones). Las partes no son copias a escala (sus cifras difieren más del 1 %) ni dominan. Es la misma raíz que T-127 H-04 | La de T-127 H-04: declararlo con su alcance en INC-T128-01 (y en su pregunta para T-57), quitando «ni una cifra individual reconstruible» de CA-2 o matizándolo («sin construir los componentes a propósito»), o verificar los componentes contra el universo. En IDX-REB, decir que «la cesta de un valor no da su demanda» se esquiva troceándolo | abierto |
| H-02 | media | `r01_02_troceo_y_una_moneda.py`, vía «U»: el caso de control 0 de CHR-FLOW-001 con `oferta_stablecoins` = {EURX: …} | **Esperado:** la tabla de CA-1 y INC-T128-01 dicen que CHR-FLOW-001 entrega «la oferta agregada, sin cifra por moneda»; el principio prohíbe la cifra de un token concreto. **Obtenido:** con una sola moneda estable se sirve, y `crecimiento_stablecoins_pct` (3,360245003 %) y `oferta_stablecoins` son los de EURX. No hay mínimo ni dominancia (con dos, una del 99 % también daría la suya) | Como en CHR-TOKEN-001: al menos 2 monedas distintas y la dominancia del 95 % de la oferta de `FRONTERA_B` (rechazo o `null` del crecimiento y la razón), con su prueba; o declarar en INC-T128-01 que la oferta de una moneda estable se acepta como indicador del ámbito y llevarlo a la pregunta para T-57 | abierto |
| H-03 | baja | Lectura: CHR-FLOW-001 (`flujos_etf` «del agregado de ETF spot»), PRV-CF-001 y PRV-PME-001 («flujos agregados») | Reciben la entrada ya agregada: el Motor no puede saber si los flujos son de un ETF o de un fondo concreto, y daría su cifra. INC-T128-01 declara este límite para ST-INF-001 y DER-OPT-001 (el propósito lo juzga quien pide), no para estas | Añadirlas a esa línea de «Límites declarados» de INC-T128-01 | abierto |
| H-04 | baja | `grep -n "T-128" sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | Sin fila de T-128 (el README dice que la añade quien hace el commit; el commit revisado es un «wip local»). Lo anoto para que no se pierda al cerrar | Añadir la fila en el commit | abierto |

## Invariantes

- Ningún camino a una orden: el Motor no emite órdenes. ✔
- Sin LLM en la ruta: las seis fichas son deterministas. ✔
- Controles: `FRONTERA_B` y los dos números nuevos (`componentes_minimos_dispersion: 3` de REI-NAV-001, `componentes_minimos: 2` de REI-FFO-001) en `UMBRALES` con su motivo; la petición no los cambia (`test_las_reglas_son_las_de_frontera_b_y_la_peticion_no_las_cambia`). ✔
- Falla cerrado: copias, dominancia y aportación de la cifra principal rechazan sin citar componentes; lo demás, `null` con limitación (recuentos, sin nombres). ✔ (salvo H-01 y H-02)
- Números: ninguno a mano fuera de `UMBRALES`/`FRONTERA_B`. ✔
- Decisiones del operador: `[PROPUESTO]` en INC-T128-01 con pregunta para T-57 y fila en §5 de `Decisiones_del_operador_Bloque_A.md`. ✔
- Secretos y datos personales: ninguno (`secrets_scan`). ✔
- Documentación: INC-T128-01 y la tabla de CA-1 al día salvo H-01 a H-03; deuda técnica sin la fila (H-04). ✔ con nota

## Veredicto

**NO APTO.**

Lo pedido en forma está bien hecho: ninguna de las 80 fichas devuelve ya el identificador de un componente ni filas por componente (mi barrido independiente lo confirma), los subconjuntos tienen el mínimo de la ficha, el mínimo y el máximo esperan a 7, los casos de control comprueban lo mismo con otros datos, ninguna prueba se debilita, 21 de 21 mutantes mueren y las cuotas no suben.

Pero **H-01 (alta)**: CA-2 pide que no haya «una cifra individual reconstruible», y una sola petición con la sociedad o el valor troceados da la prima de una sociedad en REI-NAV-001, sus múltiplos en REI-FFO-001 y la demanda de una inclusión única en IDX-REB-001 (la misma raíz que T-127 H-04). Además **H-02 (media)**, CHR-FLOW-001 sirve el crecimiento de una sola moneda estable, contra lo que dice la tabla; H-03 y H-04 (bajas), un límite sin declarar y la fila de la deuda técnica.

Vuelve a `ri-implementar` junto con T-127 H-04 (es una sola decisión para T-57): H-01 declarado o resuelto, H-02 corregido o declarado, con sus pruebas. En la r02 se vuelven a ejecutar `r01_01_barrido_un_componente.py` y `r01_02_troceo_y_una_moneda.py`.

**Sin comprobar:** el gate entero; A-Forex y B; las 14 fichas del ejecutor V1.0 solo se han visto en la tabla y en el barrido (no tienen casos de control); ciclos con el modelo real.
