# T-84 · Análisis técnico (ronda de correcciones c1)

## Causa raíz o motivo

La QA r01 (`qa.md`) dio **NO APTO** a la V0.63 porque `pruebas/pruebas_semana.py` no ejercitaba el Reloj que decía ejercitar (H-01, media), con tres huecos más en la batería (H-02, H-03, H-07) y tres restos de producto (H-04 a H-06). La causa raíz de H-01 estaba en la `Maquina` de la batería:

1. `instante()` era `Reloj.contrastar(broker.hora_datos)` en cada paso; `Reloj.ahora()`, lo que usaría la marcha real, no se llamaba nunca.
2. La pared de la máquina y la `hora_datos` del intermediario avanzaban exactamente a la par. Así, `max(pared, referencia)` era siempre la referencia y el instante de la semana era la hora del intermediario, con Reloj o sin él.

H-02: `arrancar` comprobaba `comprobar_estado` y `contrastar` con `assert`, así que un RL-02 tumbaba la batería sin contarse como fallo, y con `python -O` la comprobación desaparecía. Además, el reloj no arrancaba nunca por detrás del estado. H-03: tras el corte del miércoles solo se exigía `ab["ok"]`, y no había cortes en el diario firmado.

## Evidencia

- Antes, sobre `c306132`: r01 deja vivas R01, R02, R03, R05, R07, R08, R09, S01 y S02 en la semana (tabla de `qa.md`).
- Después: véase `pruebas.md`, «Mutaciones». Se repitió r01 sobre una copia limpia de `develop` (HEAD `1a91d28`) con los cambios de esta ronda.

## Implementación

### Archivos cambiados y por qué

| Archivo | Hallazgo | Cambio |
| --- | --- | --- |
| `sistema_global/marco_comun_c/pruebas/pruebas_semana.py` | H-01, H-02, H-03, H-06 (su prueba) | Detalle en las secciones de abajo |
| `sistema_global/marco_comun_c/pruebas/pruebas_reloj_t03.py` | H-07 | Tres comprobaciones nuevas (77 → 80). (1) `contrastar` da el mayor con el reloj 3 s por delante, que caza R04. (2) Lo mismo con la referencia 3 s por delante. (3) Tras 24 h de marcha, cuando la deriva tolerada desde el ancla ya es de 45 s, un salto de 10 s da RL-01, que caza R06. Son los dos casos de r04 |
| `sistema_global/marco_comun_c/validador/diario.py` | H-06 | `abrir` pasa a envolver el cuerpo de antes (ahora `_abrir`, sin cambios). Cuando la apertura va bien, `_temporales_huerfanos` borra los `.diario-*.tmp` y `.estado-*.tmp` de las carpetas del estado y del diario. Solo borra ficheros normales (`lstat`: ni enlaces ni carpetas) con esos nombres exactos, nunca lanza y devuelve la cuenta en `temporales_borrados`. Si `abrir` falla, no toca nada. No cambia el formato del estado ni el del diario |
| `sistema_global/marco_comun_c/LEEME.md` | — | Filas de la tabla (reloj_t03 80, semana 176, diario), párrafos «Comprobado en» de la semana y del reloj |
| `sistema_global/marco_comun_c/entrega_glm/V0.63/revision.md` | H-08 | Nota añadida al final: la revisión ya se hizo en T-84. No se borra nada |

#### `pruebas_semana.py`: la `Maquina` (H-01, H-02)

- Toma los instantes de `Reloj.ahora()`, con la pared desfasada del intermediario. El desfase cambia cada día (`DESFASES`: +3, +2, −2, +4 y −1,5 s, dentro de `MAX_DESFASE_S`).
- Contrasta en tres casos:
  - al arrancar;
  - cuando ahora() pide otro contraste porque venció el plazo (RL-04 sin bloqueo; el plazo de la `Maquina` es de 4 h, así que vence dentro del martes);
  - con la máquina por detrás del intermediario, después de cada ahora().
- Lleva un modelo propio del instante esperado: el mayor de la pared, la referencia de cada contraste, el último instante del estado y lo ya dado. Anota cada discrepancia, y también cada ahora() que dé instante con el plazo vencido.
- Sin `assert`: `arranque` guarda lo que dieron comprobar_estado, ahora() antes del contraste y contrastar, y la batería lo cuenta con `h.chk`. `instante()` devuelve None si el Reloj no da instante.
- `poner_en_hora` (el operador corrige la pared y rearma) sirve para el martes, que arranca con la hora mal puesta (+30 s): RL-03.
- Con el desfase 0 por defecto, que usan el gemelo dorado de la V0.66 y las sondas r02 y r03, los instantes son los de antes. `pruebas/doradas/semana.json` no cambia.

#### `pruebas_semana.py`: los pasos nuevos (H-02, H-03, H-06)

- **`manana_atrasada`**, adoptada de r03. Va la mañana del martes, en copias de los ficheros de la noche del lunes, y usa la misma `Maquina`:
  - 1 h detrás: RL-02, sin instantes, `degradar_por_reloj` a través del diario con el instante del estado (anotado al reabrir) y rearme sin poner en hora: RL-01;
  - 5,5 s detrás: RL-02;
  - 5 s y 4 s detrás: el instante es el suelo y se opera sin O-16.
- **Cortes**, adoptados de r02:
  - **Miércoles:** se exige `linea_incompleta` y un diario limpio tras reabrir (acaba en salto de línea y, tras el PUNTO, pares OP-RES).
  - **`jueves_stop`:** primer corte en el diario firmado, con la última OP sin su RES.
  - **`jueves_conciliar`:** segundo corte. Barrido de 9 posiciones en copias, cada una contra una réplica independiente, sin perder ni repetir nada y de forma idempotente. Después, el corte en vivo.
  - **`jueves_degradar`:** corte dentro de la reescritura que limpia la línea cortada, más un `.estado-*.tmp` huérfano. `abrir` borra los dos temporales y deja dos ficheros parecidos.
- **Comprobaciones nuevas:**
  - por paso: «el Reloj da el instante del paso»;
  - al final: «cada instante es el del modelo» y «al vencer el plazo, ahora() pide otro contraste».
- El orden de los instantes se compara como instantes, no como texto: con fracciones de segundo, el texto ISO no ordena bien siempre.
- Resultado: 123 → 176 comprobaciones.

### Decisiones tomadas y desviaciones de la propuesta de la QA

- **Desviación en H-01.** La QA proponía contrastar solo al arrancar y cuando ahora() pida RL-04. Con la máquina por detrás del intermediario, eso no se puede. El instante de ahora() es anterior a la `hora_datos` de lo que llega del intermediario (foto de cartera, cotizaciones), y el Orquestador lo rechaza por ser del futuro (O-10, «la foto de cartera es del futuro»). Es la razón de ser de que `contrastar` dé el mayor. Por eso, en los días con desfase negativo, la `Maquina` contrasta después de cada ahora(). Los dos se comprueban contra el modelo, así que ahora() sigue ejercitado. Para la integración real, lo que esto deja dicho es que quien use datos del intermediario debe contrastar antes, o la máquina debe ir por delante (nota para la deuda, en `README.md`).
- **S02 de r01 ya no se puede aplicar.** S02 buscaba el texto exacto «`comprobar_estado` + `assert`», que H-02 manda quitar. Para medirla, la misma mutación sobre el texto nuevo («la `Maquina` no llama a `comprobar_estado`») se ejecutó con un envoltorio de r01 en el scratchpad de la sesión, fuera del repositorio. Ese envoltorio añadía dos mutaciones más: S03 (el corte sin RES no corta) y D11 (`abrir` no borra los temporales). r01 no se ha tocado.
- **r03 B9 cambia a propósito.** B9 comprobaba que la `Maquina` paraba la batería con un AssertionError. Ahora arranca y deja el RL-02 en `arranque` para contarlo. r03 da «HAY FALLOS» solo por B9: es la corrección de H-02 y la QA r02 tiene que actualizar esa comprobación. B8 y B10 siguen como hallazgos (H-04 y H-05, a la deuda).
- **H-04, a la deuda.** Que el Reloj no dé instantes hasta un `comprobar_estado` bueno cambia el contrato de `Reloj`. Hoy piden instantes sin `comprobar_estado` `pruebas_reloj_t03.py` (su `nuevo_reloj`), `pruebas_reloj_diario_t72.py`, `pruebas_robustez_t03.py` y `pruebas_consola_sistema.py`, y adaptar las tres últimas queda fuera de los ficheros de esta ronda. El fallo ya queda cerrado más abajo: O-16 en el Orquestador, que lo deshace todo, y G-06 en G.
- **H-05, a la deuda.** Exige que `punto()`, `crear` y `volcar` rechacen instantes anteriores a `ultimo_ahora` o al `guardado_en` anterior, y que `abrir` exponga el `guardado_en` para `comprobar_estado`. Es un cambio de comportamiento del diario y de la persistencia, con efecto en las migraciones (que leen el `guardado_en`) y en las baterías de T-03. Hoy el `guardado_en` no decide nada.
- **H-06, corregido** en `abrir`, en su forma más prudente: solo tras abrir bien y solo con los nombres exactos de `mkstemp`. Como el diario, supone un solo proceso escribiendo en esas carpetas. Lo dicen el docstring de `diario.py` y el LEEME.
- **H-08, en parte.** Hecho: la nota en `revision.md` y la comprobación del determinismo byte a byte, a mano (`pruebas.md`). Lo que queda, que la batería lo exija ejecutando `main()` dos veces y comparando, va a la deuda. Doblaría el tiempo de la batería (~10 → ~20 s) y la dorada de la V0.66 ya fija el recorrido del gemelo.
- **Esquema.** `persistencia.esquema_actual()` es `aa778db7…0459` antes y después de los cambios, medido en copias limpias de HEAD. `diario.py` y `reloj.py` no están en `MODULOS_ESQUEMA`, y no se añadió ninguna constante en mayúsculas. No hace falta migración.

### Límites conocidos

- La mañana atrasada va en copias: la semana en vivo nunca arranca por detrás de su estado, porque el escenario ya no seguiría siendo el mismo para el gemelo en memoria.
- La degradación por el reloj tras el RL-03 del martes no se aplica en vivo. Ese arranque se para antes de dar ningún instante, y la degradación se ejercita en la mañana atrasada.
- El barrido del segundo corte cubre `jueves_conciliar` (9 posiciones). El de `viernes_rearmar` (41) y los diarios firmados alterados (C3) siguen solo en r02.
- Con `python -O` la semana sigue sin pasar. Los arranques del reloj ya no dependen de `assert`, pero los auxiliares compartidos de `pruebas/pruebas_orquestador.py` (`nuevo()`, que registra los sellos) y `p_encargos` llaman al Orquestador dentro de `assert`. `pruebas_orquestador.py` queda fuera de esta ronda (deuda, con H-08).
- r01 se cae cuando una mutación no se puede aplicar: la rama devuelve 4 valores y `main()` desempaqueta 5. Le pasa a S02, cuyo texto quitó H-02. Las 26 anteriores se miden; S02 se midió con un envoltorio fuera del repositorio (`pruebas.md`).
- La limpieza de temporales solo la hace `abrir`. `persistencia.cargar_de`, si se usa solo sin diario, no limpia.

### Comandos exactos para probarlo

```bash
cd sistema_global/marco_comun_c
/home/claude/repo/.venv/bin/python -I pruebas/pruebas_semana.py          # 176 comprobaciones
/home/claude/repo/.venv/bin/python -I pruebas/pruebas_reloj_t03.py       # 80
/home/claude/repo/.venv/bin/python -I pruebas/pruebas_doradas.py         # la foto de la semana no cambia
python3 -I entrega_claude/V0.63_revision/r01_mutaciones_semana.py --doradas --resto
python3 -I entrega_claude/V0.63_revision/r02_segundo_corte_firmado.py   # nota final: 0 temporales
cd /home/claude/repo
/home/claude/repo/.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c
.docs/scripts/pruebas_marco.sh
```
