# QA · T-193 · PB-18 (cola saturada y apertura de instancia)

## Ronda r01 · 24-11-2026 · Claude (revisor independiente; no implementó)

**Veredicto: NO APTO** (3 hallazgos medios y 3 bajos).

Código revisado: rama `astra/encargos-bloque-a-c38-c47`, tip `2d99af6`, sobre `develop` `9ce57b2`. Commits del ticket:
`a7651a9` (HT-08 mide la ingesta, cierre con histéresis, lote de F2 en una transacción) y `fb4dd3d` (la lectura de
HT-08 se hace tras la ingesta del ciclo). `5ef929b` solo reordena los `import` de la prueba.

Vara de medir: el criterio del plan V3.0, PB-18: «Apertura ≤ 1 ciclo de lectura tras superar el umbral; cero
duplicados en F2; tiempo medio de ingesta vuelve al objetivo», con el resultado esperado «al superar cola > 3 o tiempo
> 2× objetivo, ORD- ABRIR con c = ⌈λ/(μ·0,75)⌉; escritura de F2 serializada por hash; ORD- CERRAR tras 2 lecturas con
cola 0 y ρ < 0,30».

### Reproducción desde limpio

Worktree propio en `2d99af6`, Python 3.12, venv del repo.

| Comprobación | Resultado |
|---|---|
| `tests/test_t193_ingesta.py` (3 pruebas) | 3 superadas |
| Las 3 pruebas nuevas con el código de `9ce57b2` (revertidos `a7651a9` y `fb4dd3d` en un worktree aparte) | las 3 fallan: la primera por el constructor, la de concurrencia con 3 EVD en vez de 1 y la del ciclo sin ORD- |
| `mutantes.py` de Astra (2 mutantes) | los 2 muertos |
| Vecinas: `test_t178.py`, `test_t53_evaluacion_y_almacen.py`, `test_unitarias.py` (HT-08) e `test_integracion.py` | 189 superadas en una sola tanda (con `test_t178.py`, `test_t53_evaluacion_y_almacen.py` y las del ticket) |
| `revisores/r01_mutantes_revisor.py` (11 mutantes propios) | **8 vivos**, 2 muertos, 1 equivalente para estas pruebas (H-02) |
| `revisores/r01_ataques_monitor.py` (ataques directos al monitor) | 3 fallos de 22 casos (H-03, H-04, H-05) |
| ruff y mypy de los ficheros tocados frente a `9ce57b2` | sin cambios (ruff: `ht08_monitor.py` 0, `agentes.py` 0, `orquestacion.py` 8 igual que antes, prueba nueva 0; mypy A 102 = 102) |

Lo que sí cumple, con evidencia: el disparo por tiempo abre en la misma lectura y en el borde no abre (W = 2× no
abre; 2,0001× sí); el dimensionado da c = 4 con λ = 1/s y W = 3 s; el cierre exige cola 0 y ρ < 0,30 en dos lecturas
consecutivas, una lectura ocupada reinicia la cuenta, cierra de una en una, nunca por debajo de 1 y nunca con un
encargo en curso; dos lecturas en el mismo instante no dividen por cero; respeta `instancias_max`; un objetivo
inválido (0, negativo, NaN, infinito, booleano, texto, lista) se rechaza al construir. Cuarenta ingestas concurrentes
de la misma pieza dejan un EVD y un CLM (sin la transacción del lote quedan 3). La ORD- de apertura queda en HA en el
mismo ciclo (`fb4dd3d`). El cambio de `agentes.py` (no contar dos veces la llamada CT-11 de AG-12, que ya está dentro
del lote medido) es correcto. Ningún esquema congelado ni golden cambia; el campo nuevo de `config/por_defecto.yaml`
es `paralelismo.objetivo_ingesta_s: null`, sin número: el Anexo A dice «2× el objetivo» pero no fija el objetivo,
y está declarado como INC-T193-01 [PROPUESTO].

### Hallazgos

#### H-01 · media · Números del disparo y del cierre escritos a mano

- **Dónde:** `herramientas/ht08_monitor.py`, `evaluar_instancias`: `media > 2 * self.objetivo_ingesta_s`,
  `math.ceil(tasa * media / 0.75)`, `rho < 0.30` y `self._lecturas_vacias[ag] >= 2`.
- **Por qué:** el factor 2 es el parámetro P-20 de F10, CALIBRABLE («Cola > 3 encargos o tiempo de respuesta > 2× el
  objetivo», propuesta «factor de tiempo ±0,5 por trimestre», esquema de F10 V3.0) y la fila «Umbral de escalado por
  instancias (R25)» del Anexo A; 0,75, 0,30 y las 2 lecturas son del prompt del Orquestador V5.0, 6.10. La cola de esa
  misma fila sí sale de la configuración (`paralelismo.umbral_cola`); el factor de tiempo, no. Regla 2 del proyecto:
  ningún número a mano. Ni `docs/incidencias.md` ni el comentario del YAML los declaran.
- **Corrección:** en `config/por_defecto.yaml`, bajo `paralelismo`, `factor_tiempo: 2` (Anexo A, R25; P-20 de F10),
  `rho_objetivo: 0.75`, `rho_cierre: 0.30` y `lecturas_cierre: 2` (prompt del Orquestador V5.0, 6.10), con su
  comentario de origen. `Monitor.__init__` los recibe (con validación de positivos y finitos, como el objetivo) y
  `Bloque` se los pasa con `parametro(cfg, "paralelismo.…")`. Mantener los valores por defecto del constructor solo
  como lectura de esa configuración, no como literal nuevo.
- **Prueba de regresión:** con `factor_tiempo: 3`, una ingesta de 2,5× el objetivo no abre y una de 3,1× sí; con
  `lecturas_cierre: 3`, el cierre llega a la tercera lectura libre y no a la segunda; con `rho_cierre: 0.05`, una
  lectura con ρ = 0,1 no cuenta como libre; con `rho_objetivo: 0.5`, el caso λ = 1/s, W = 3 s da c = 6.

#### H-02 · media · Las pruebas no matan ocho mutantes que cambian el comportamiento

`revisores/r01_mutantes_revisor.py` aplica cada mutante en una copia y pasa `test_t193_ingesta.py`, la prueba del
monitor de T-53 y `test_ht04_y_ht06_y_ht08`. Quedan vivos:

| Mutante | Cláusula del plan sin prueba que la mate |
|---|---|
| M01 cierre sin `rho < 0.30` | «ρ < 0,30» del cierre |
| M02 cierre sin `q == 0` | «cola 0» del cierre (y «nunca con encargos en curso») |
| M03 disparo a 1× el objetivo | «tiempo > 2× objetivo» |
| M04 dimensionado sin el 0,75 | «c = ⌈λ/(μ·0,75)⌉» (el ejemplo de la prueba da 2 con o sin 0,75) |
| M05 λ acumulada entre lecturas | λ de la ventana de lectura |
| M07 la ventana no avanza | ρ y λ por lectura |
| M08 cierra todas las adicionales de golpe | cierre de una instancia por orden |
| M09 la histéresis no se reinicia | «2 lecturas consecutivas» |

M11 (no encolar la ingesta) solo cambia λ y queda cubierto por la corrección de M05. M06 y M10 mueren.

- **Corrección:** añadir a `tests/test_t193_ingesta.py` las pruebas de los casos 2 a 9 de
  `revisores/r01_ataques_monitor.py` con el reloj controlado: borde 2× / 2,0001×; c = 4 con diez llegadas en 10 s y
  W = 3 s; ρ ≥ 0,30 en dos lecturas no cierra; cola 1 en curso no cierra; libre-ocupado-libre no cierra y la
  siguiente libre sí, a una instancia; nunca baja de 1; dos lecturas seguidas con ventana 0; tope `instancias_max`.
  Añadir los mutantes M01 a M05, M07 a M09 a `mutantes.py` del ticket.
- **Prueba de regresión:** `revisores/r01_mutantes_revisor.py` con los 11 mutantes muertos (o M11 explicado como
  equivalente en `pruebas.md`).

#### H-03 · media · «El tiempo medio de ingesta vuelve al objetivo» no tiene mecanismo de medida

- **Reproducción:** `r01_ataques_monitor.py`, caso 11: tras una ORD- ABRIR por tiempo, una ingesta de 0,5 s (por
  debajo del objetivo de 1 s) y una lectura: `evaluar_instancias()` devuelve `[]`. Para un agente sin estado, HT-08
  solo emite algo cuando abre o cierra; ningún registro de HA deja W frente al objetivo después de abrir.
- **Esperado:** el criterio del plan es «tiempo medio de ingesta vuelve al objetivo». Con carga real o sin ella,
  hace falta que cada lectura posterior a una apertura deje constancia de W frente al objetivo. Si no, la cláusula no
  se puede comprobar nunca, tampoco con carga real. La motivación «carga real» del mapa cubre la cifra de recuperación,
  no la falta de medida.
- **Corrección:** en `evaluar_instancias`, para un agente sin estado con objetivo de tiempo y con ingestas en la
  ventana, mientras tenga instancias adicionales abiertas (y en la lectura en que se cierra la última), emitir un
  `CAR-` (esquema HA V2.0, 4.5) con `saturado: False`, `W`, `objetivo`, `rho`, `instancias` y `en_objetivo`
  (`W ≤ objetivo`). `carga.registrar_carga` ya escribe los CAR- en HA; uno con `saturado: False` no abre P3-.
- **Prueba de regresión:** apertura por tiempo, después una ingesta por debajo del objetivo: la lectura devuelve un
  CAR- con `en_objetivo: True`; con una ingesta por encima, `en_objetivo: False`. En un ciclo completo con la ingesta
  lenta en el primero y rápida en el segundo, HA tiene la ORD- ABRIR del primero y el CAR- en objetivo del segundo.
  Actualizar el «no comprueba» de PB-18: lo que falta es la cifra con carga real, no la medida.

#### H-04 · baja · `metricas_disparo` de la ORD- no sigue el esquema de HA

- **Reproducción:** `r01_ataques_monitor.py`, caso 3: `metricas_disparo` es `{cola, W_medio_s, rho}`. El esquema de HA
  V2.0, 4.5, fija `metricas_disparo {cola, W, rho, lambda, mu}` y `calculo`. La ORD- CERRAR no lleva `calculo`.
- **Corrección:** `metricas_disparo = {"cola": q, "W": media, "rho": rho, "lambda": tasa, "mu": 1 / media si media}`
  (None donde no haya dato) en ABRIR y en CERRAR; `calculo` también en CERRAR (la regla de histéresis, p. ej.
  «2 lecturas con cola 0 y ρ < 0,30»). Ajustar las dos aserciones `W_medio_s` de `test_t193_ingesta.py`.
- **Prueba de regresión:** las claves de `metricas_disparo` son exactamente las del esquema en ABRIR y en CERRAR, y en
  el caso c = 4, `lambda == 1.0` y `mu == 1/3`.

#### H-05 · baja · El disparo por tiempo solo existe para el Curador, sin declararlo

- **Reproducción:** `r01_ataques_monitor.py`, caso 12: AG-03 con W = 30× el objetivo no abre (`ag == "AG-12"` en
  `evaluar_instancias`). R25, el Documento 0 4.5 y el prompt del Orquestador 6.10 aplican la regla de tiempo a cualquier
  agente sin estado.
- **Corrección:** declarar el alcance en INC-T193-01 (solo la ingesta tiene objetivo de tiempo; el resto de agentes
  sin estado escala por cola hasta que el operador fije sus objetivos) y en el «no comprueba» de PB-18. Si se prefiere
  generalizar, `paralelismo.objetivo_s` por agente en lugar de un único `objetivo_ingesta_s`.
- **Prueba de regresión:** una prueba que fije el comportamiento declarado (AG-03 lento sin objetivo no abre por
  tiempo; con objetivo por agente, si se generaliza, sí abre).

#### H-06 · baja · INC-T193-01 incompleta y objetivo inválido de la configuración sin prueba

- **Qué falta:** INC-T193-01 no dice la decisión tomada mientras el operador no fije el objetivo: con `null`, el
  disparo por tiempo está desactivado en la configuración por defecto y HT-08 solo escala por cola. Tampoco recoge
  la regla de dimensionado sin tasa observada (`c = antes + 1`), que no está en el spec. Ninguna prueba cubre el
  rechazo de un objetivo inválido, ni que un `objetivo_ingesta_s` inválido en el YAML impida construir el `Bloque`
  (falla cerrado).
- **Corrección:** completar INC-T193-01 con esas dos decisiones y con los números de H-01; añadir a la deuda la
  decisión pendiente del operador (el valor del objetivo), como pendiente del operador y no como hallazgo.
- **Prueba de regresión:** prueba parametrizada con los valores del caso 1 de `r01_ataques_monitor.py` (0, −1, NaN,
  inf, True, "5", [1]) que espera `ValueError` del `Monitor`, y otra que construye el `Bloque` con
  `paralelismo.objetivo_ingesta_s: "5"` y espera el error.

### Invariantes

- Números: H-01. Esquemas y corpus: ningún fichero congelado cambia; el golden `formas_flujos_mock.json` lo cambió
  T-185, no este ticket. HA: H-04.
- Fallar cerrado: el objetivo inválido se rechaza; el lote de F2 va en una transacción del almacén, que también
  excluye entre procesos. Un fallo a mitad del lote deja escritas las piezas anteriores del lote (el almacén no
  deshace), como en `9ce57b2`: no empeora.
- R8 y G3-MET-13: el ticket no escribe textos ni datos protegidos nuevos.
- Pruebas antiguas: este ticket no debilita ninguna. Los cambios en `test_fase4_huecos.py` (T-189) y en
  `test_t159_extremo_a_extremo.py` (T-191; `5ef929b` solo quita un `import` sin uso) son de otros tickets y los juzga
  su QA.
- Mapa y evidencias: PB-18 sigue «Superada en parte» y PARCIAL, honesto. Tras H-03, el «no comprueba» debe decir que
  falta la cifra con carga real y un objetivo acordado, no la medida.

### Regresión

Una sola tanda con `test_t173.py`, `test_t176_pb36_pb33.py`, `test_t178.py`, `test_t66_evaluacion.py`, `test_t65_qa_r01.py`,
`test_t53_evaluacion_y_almacen.py`, `test_unitarias.py`, `test_integracion.py` y las de T-192 y T-193: 189 superadas, 0 fallos. El gate completo (12/12) lo pasa
el coordinador sobre la copia del PR.

### Scripts del revisor

- `revisores/r01_mutantes_revisor.py`: mutantes propios (`python -I .docs/tickets/T-193/revisores/r01_mutantes_revisor.py`).
- `revisores/r01_ataques_monitor.py`: ataques al monitor (desde `bloque_a/11_Ejecutor`).

Para la ronda r02: pasar los dos scripts sin fallos (salvo M11, si se explica) y las pruebas de regresión de cada
hallazgo.
