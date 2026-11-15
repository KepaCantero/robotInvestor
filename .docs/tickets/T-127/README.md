# T-127 · Bloque A, Motor: hallazgos abiertos de la QA r02 de T-119 y de la QA r01 de T-121

| Campo | Valor |
| --- | --- |
| Estado | EN QA · ronda r03 |
| Pieza | bloque_a (11_Ejecutor, motor) |
| Planifica · implementa · QA | Claude · Claude · un revisor nuevo (otro agente o un subagente sin contexto de la implementación) |
| Aprobación del operador | no necesaria (corrección de hallazgos de QA); las decisiones van `[PROPUESTO]` (el operador pidió que el agente decida por defecto y lo deje apuntado) |
| Deuda técnica | T-127 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la añade quien hace el commit) |

## Objetivo

Cerrar los hallazgos que las QA dejaron abiertos en el Motor del Bloque A antes del modo sombra: la frontera con el Bloque B
en las fichas con componentes (T-119 H-10, media), la caché con tuplas (T-119 H-11), CT-10 cuando `por_defecto.yaml` gana
una clave (T-121 H-07), el día de la fecha de corte con zonas horarias (T-121 H-08) y la fecha de NAV con hora de
FON-DISC-001 (T-121 H-09).

## Alcance

- Entra: `motor/fichas_p2.py` (FIR-CRED-001, REI-LEV-001, CHR-TOKEN-001 y sus casos de control), `motor/servicio.py`
  (firma de la caché, CT-10), `configuracion.py` (`parametro` apunta lo que toma del fichero), `motor/operaciones.py`
  (ayudante de día), `motor/fichas_reales.py`, `motor/fichas_mon_idx.py`, `motor/fichas_tcv.py` y
  `motor/fichas_fon_der.py` (lo usan); las pruebas que fijaban el comportamiento anterior; `docs/incidencias.md`
  (INC-T119-01 corregida, INC-T121-01 anotada, INC-T127-01 nueva); la fila de §5 de
  `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`.
- No entra: `evaluador.py` y los hallazgos H-13 y H-14 de T-122 (otra sesión); otros bloques; el corpus; el marco común
  de C; la Constitución; REI-NAV-001 (T-112), que entrega una fila por sociedad con su identificador (anotado en
  INC-T127-01 para un ticket propio).

## Diseño

- Contratos CT-G afectados y versión de esquema: ninguno. La forma del resultado de CT-09 de REI-LEV-001 y CHR-TOKEN-001
  cambia solo en que `dispersion` (y las holguras de `covenants`) pueden ser `null`, como cualquier bloque opcional del
  módulo; no hay esquema que lo fije (ningún golden las cubre).
- Estado persistido: no cambia. El artefacto del RC sigue guardando `configuracion_usada` igual; lo nuevo
  (`respaldos`) se calcula al re-ejecutar.
- Números y su origen: en `FRONTERA_B` de `fichas_p2.py`, dentro de los `UMBRALES` de las tres fichas (la petición no los
  cambia), con su motivo al lado: tolerancia de clon 0,01; peso máximo de un componente 0,95; mínimo para los
  estadísticos de orden `len(ESTADISTICOS_ORDEN) + 2` = 7 (derivado: 5 estadísticos + el agregado + 1); `redes_propias`
  {bitcoin: BTC, ethereum: ETH} en los de CHR-TOKEN-001. Ninguno en `por_defecto.yaml`.
- Cómo falla cerrado: casi clones y dominancia → rechazo de la ficha (DATOS_INSUFICIENTES, sin citar identificadores);
  pocos componentes para la dispersión o para un subconjunto → `null` y una limitación; un token como «red» que no está
  en `redes_propias` → rechazo; CT-10: si la re-ejecución tomó algo del fichero cambiado, CONVENCION_DISTINTA (nunca se
  culpa al original sin poder reproducir sus condiciones).
- Decisiones del operador usadas como `[PROPUESTO]` (INC-T127-01, pregunta para T-57):
  1. H-10, regla de la frontera: casi clones a menos del 1 %, dominancia (1, k) con k = 95 %, estadísticos de orden con 7
     componentes o más, subconjuntos con el mínimo del agregado, «propia red» de una lista fija. Elegida frente a «subir
     el mínimo» (rechazaría ámbitos reales de 3 a 6 componentes y no resuelve los casi clones ni la dominancia) y frente a
     «la frontera es solo de forma» (la QA la ha cruzado tres veces).
  2. H-07: CONVENCION_DISTINTA solo si la re-ejecución tomó una ruta de `por_defecto.yaml` de una sección cuya huella cambió.
  3. H-08: el día de una fecha con zona es su día en UTC (el de la Fase 2), para el dato y para el corte.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Dos emisores reales a menos del 1 % en todos sus datos | Se rechaza un agregado legítimo | Requiere coincidir a la vez en 4 a 6 datos; el rechazo dice el motivo y el solicitante quita uno |
| Un sector real dominado por un token (más del 95 %) | Se rechaza | Es exactamente el caso en que el agregado es la cifra del token; el ámbito correcto es la red |
| Ámbitos de 3 a 6 componentes sin dispersión | Menos información | El agregado se sigue entregando; la dispersión de 3 era la lista de cifras individuales |
| Una ficha que lea la configuración sin `parametro` | CT-10 no vería que tomó algo del fichero | Todas las lecturas del Motor pasan por `parametro`, `sesiones_horizonte` o `parametros_ht03` sobre el objeto que da el Motor (comprobado con `grep`) |
| Pruebas antiguas que fijaban el comportamiento anterior | Se cambian | Cada cambio lleva su comentario T-127 y su motivo; la lista está en `analisis-tecnico.md` |

## Criterios de aceptación (binarios)

1. CA-1 (H-10, casi clones): 10, 3 y 2 copias de un emisor con diferencias de 1e-9 se rechazan en FIR-CRED-001, REI-LEV-001
   y CHR-TOKEN-001; el borde del 1 % está en |a − b| ≤ 0,01·máx; una cadena de casi clones es un componente.
2. CA-2 (H-10, dominancia): un componente con el 99,99 % de una base (GAV, deuda, EBITDA, gastos financieros, FFO,
   capitalización, FDV) se rechaza; el 95 % justo se admite.
3. CA-3 (H-10, orden): con 3 componentes de REI-LEV-001 ningún número de la entrega es el LTV o el ICR de una sociedad y
   la dispersión es `null` con su limitación; con 7, la dispersión coincide con la de numpy; en CHR-TOKEN-001, 6 tokens
   sin dispersión y 7 con ella.
4. CA-4 (H-10, subconjuntos y red): covenants de 2 de 3 no se calculan; *staking* de un token o dominado tampoco; un solo
   token solo con una red de `redes_propias` y su token.
5. CA-5 (H-10): `verificar_casos_control` sigue superado en las tres fichas (y en las 80).
6. CA-6 (H-11): una tupla de componentes da lo mismo antes y después de la lista, y la lista sigue saliendo de la caché.
7. CA-7 (H-07): los casos A2, A2b y A5 del revisor dan ERROR_ORIGINAL; un artefacto que tomó `horizontes.H5` del fichero
   y luego el fichero cambia da CONVENCION_DISTINTA.
8. CA-8 (H-08 y H-09): el mismo día en las cuatro familias de módulos; mismo veredicto en MON-YLD-001, TCV-CDS-001 y
   FON-FLOW-001 en los casos con zona del revisor; un NAV del último día con hora se sirve.
9. CA-9: scripts del revisor `r02_01` (la parte que llega a ejecutarse), `r02_02` 12/12, `r01_02` 11/11, `r01_03` sin
   diferencias por zona horaria; mutantes de `revisores/impl_mutantes.py` muertos; suites del Motor y vecinas en verde;
   ruff ≤ 2902 y mypy A ≤ 109.

### Ronda r03 (QA r02: H-04 alta, H-05 baja)

10. CA-10 (H-04): decidido y apuntado `[PROPUESTO]` en INC-T127-01 «Ronda r03» y en §5 de las decisiones del operador, con
    la pregunta para T-57: de dónde salen los componentes (los aporta quien pide; HT-01 solo da precios), el límite con su
    alcance y el aviso de `frontera_b._aviso_casi_clones`; una prueba fija el límite (S1 troceado se sirve y queda en el
    Registro con sus partes) y otra el aviso (C11 con σ_E·(1 ± δ)).
11. CA-11 (H-05): S1 con dos rellenos de deuda neta +400 y −400 se rechaza; la frase de INC-T127-01 dice la cota que se
    cumple, (1 − k)/(2 − k), y una prueba la barre con rellenos de los dos signos.
12. CA-12: `r02_01_troceo_y_simetria.py` con la vía «C» en «ok» y cada FALLA restante explicada en `pruebas.md` como límite
    declarado; casos de control 67/67; mutantes de `revisores/impl_r03_mutantes.py` muertos; suites del Motor y vecinas en
    verde; ruff ≤ 2902 y mypy A ≤ 109.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_h10_casi_clones_de_un_emisor_se_rechazan`, `test_h10_borde_de_la_tolerancia_de_clon`, `test_h10_una_cadena_de_casi_clones_es_un_solo_componente`, `test_h10_un_solo_dato_distinto_basta_para_no_ser_clon`, `test_h10_la_tolerancia_compara_por_el_mayor_y_los_ceros_son_iguales` | regresión, límite | CA-1 |
| `test_h10_un_componente_de_peso_casi_total_se_rechaza`, `test_h10_borde_de_la_dominancia_y_bases_de_rei_lev` | regresión, límite | CA-2 |
| `test_h10_con_tres_componentes_no_se_entregan_sus_cifras_individuales`, `test_h10_la_dispersion_de_rei_lev_empieza_en_siete_componentes`, `test_h10_la_dispersion_de_chr_token_empieza_en_siete_tokens`, `test_h10_fir_cred_conserva_su_dispersion_con_diez_o_mas` | regresión, límite, nominal | CA-3 |
| `test_h10_covenants_de_menos_componentes_que_el_minimo_no_se_calculan`, `test_h10_staking_y_concentracion_de_un_solo_token_o_dominados_no_se_calculan`, `test_h10_la_propia_red_es_una_red_de_la_ficha_con_su_token` | regresión, fallo cerrado | CA-4 |
| `test_h10_los_casos_de_control_siguen_superados`, `test_h10_las_reglas_de_la_frontera_son_umbrales_fijos_de_las_tres_fichas` | contrato | CA-5 |
| `test_h11_la_tupla_no_sale_de_la_cache_de_la_lista_en_ningun_orden`, `test_h11_la_firma_distingue_contenedores_y_claves` | regresión | CA-6 |
| `test_h07_una_clave_nueva_de_por_defecto_que_la_ficha_no_lee_no_ablanda_el_error` (A2, A2b, A5), `test_h07_convencion_distinta_si_la_ruta_leida_salio_del_fichero_y_este_cambio`, `test_h07_la_configuracion_leida_apunta_solo_lo_que_sale_del_fichero` | regresión | CA-7 |
| `test_h08_un_solo_criterio_de_dia_en_los_cuatro_modulos`, `test_h08_mismo_veredicto_en_mon_tcv_y_fon`, `test_h08_tcv_rechaza_un_texto_con_basura_tras_la_fecha_y_fon_admite_zonas_mezcladas`, `test_h09_fon_disc_un_nav_del_ultimo_dia_con_hora_se_sirve` | regresión, límite | CA-8 |
| Scripts del revisor, `revisores/impl_mutantes.py`, suites y cuotas | integración | CA-9 |
| `tests/test_t127_r03.py` (H-04: aviso y límite declarado; H-05: con signo y la cota) y `revisores/impl_r03_mutantes.py` | regresión, límite | CA-10 a CA-12 |

## Scripts

- `.docs/scripts/nuevo_ticket.sh` (creación del ticket).
- `.docs/tickets/T-127/revisores/impl_mutantes.py` (nuevo): mutantes de las correcciones en una copia desechable.
- Del revisor: `.docs/tickets/T-119/revisores/r02_01_frontera_b.py`, `r02_02_cache.py`;
  `.docs/tickets/T-121/revisores/r01_01_h04_campo_a_campo.py`, `r01_02_h01_ct10.py`, `r01_03_h04_bordes.py`,
  `r01_04_casos_control.py`.

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · PLANIFICADO · Claude · plan, criterios y decisiones `[PROPUESTO]` (INC-T127-01)
- 2026-11-14 · EN CURSO · Claude · implementación y pruebas (`tests/test_t127_hallazgos.py`)
- 2026-11-14 · EN QA · Claude · suites del Motor y vecinas en verde, mutantes muertos, cuotas sin subir; falta `./tools/check_all.sh` en el commit y la QA de un revisor nuevo
- 2026-11-15 · NO APTO · revisor nuevo (QA r01) · H-01 (alta, copias a escala), H-02 (media, rellenos de cifra nula), H-03 (baja, declarado)
- 2026-11-15 · EN CURSO · ronda r02 · Claude · H-01: las copias se comparan por sus cifras individuales (sin escala) y cuentan como un componente; H-02: dominancia también de la aportación a cada cifra agregada; H-03: declarado (INC-T127-01, «Ronda r02»)
- 2026-11-15 · EN QA · ronda r02 · Claude · `tests/test_t127_r02.py` (24), script del revisor 7/7, mutantes de la r02 31 de 32 (el vivo, equivalente), suites del Motor y vecinas en verde, ruff 2902 y mypy A 109; las funciones de la frontera pasan a `motor/frontera_b.py` (T-128); falta `./tools/check_all.sh` en el commit y la QA r02
- 2026-11-15 · NO APTO · revisor nuevo (QA r02) · H-04 (alta, un emisor troceado o con perturbaciones simétricas da su cifra), H-05 (baja, la frase del «error de al menos un 5 %»)
- 2026-11-15 · EN CURSO · ronda r03 · Claude · H-04: los componentes los aporta quien pide (HT-01 solo da precios): límite declarado con su alcance, aviso cuando dos componentes solo difieren en un dato y pregunta para T-57; H-05: aportación también con signo y frase corregida (INC-T127-01, «Ronda r03»); junto con la r02 de T-128
- 2026-11-15 · EN QA · ronda r03 · Claude · `tests/test_t127_r03.py` (12) y `tests/test_t128_r02.py` (17), mutantes de la r03 29 de 29, casos de control 67/67, scripts del revisor explicados uno a uno en `pruebas.md`, suites del Motor y vecinas en verde, ruff 2902 y mypy A 109; falta `./tools/check_all.sh` en el commit y la QA r03
