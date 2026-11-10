# T-84 · Pruebas (ronda de correcciones c1)

Todas las ejecuciones con `/home/claude/repo/.venv/bin/python -I`. Dónde:

- en el árbol de trabajo;
- y en dos copias limpias del scratchpad de la sesión, fuera del repositorio, hechas con `git archive`:
  - la primera, de `1a91d28` con los cambios de esta ronda, para las mutaciones;
  - la segunda, de `7b775cc`, el HEAD de `develop` al terminar (otro agente lo subió durante la ronda), con el parche de esta ronda aplicado con `git apply`, para el lote y el esquema.

## Recuentos

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas/pruebas_semana.py` | 123 | **176** |
| `pruebas/pruebas_reloj_t03.py` | 77 | **80** |
| Resto del lote del marco | sin cambios | sin cambios (`leeme_marco.py`: SIN DIFERENCIAS en el árbol de trabajo) |
| Lote del marco (`pruebas_marco.sh`) | 61 baterías | **61 pasan, 0 fallan** (árbol de trabajo y copia limpia de `7b775cc` con el parche) |

## Criterio → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CC-1 (H-01) | r01 `--doradas --resto` sobre la copia limpia. En la semana: la `Maquina` con `Reloj.ahora()` y `DESFASES`, «arranque del … (pared ±x s …)», «el Reloj da el instante del paso», «cada instante del Reloj es el del modelo…» y «al vencer el plazo del contraste, ahora() pide otro (RL-04)…» | Se cazan R01, R02, R03, R05, R07, R08 y R09, que antes quedaban vivas. También R04, que es FUERA. La semana caza 14 de las 14 que dice cubrir de r01 (sin S02, véase abajo) |
| CC-2 (H-01, H-08) | Cuatro ejecuciones de la semana en el árbol de trabajo; `pruebas_doradas.py` sin regenerar `pruebas/doradas/semana.json` | sha-256 `8b5d447ba7ec2431…` en las cuatro; la dorada pasa |
| CC-3 (H-02) | Sin `assert` en la `Maquina`; `chk_arranque`; «arranque del martes con la hora mal puesta (+30 s): contrastar da RL-03…»; los ocho «mañana atrasada…» (1 h: RL-02, degradación por el diario, rearme sin poner en hora; 5,5 s; 5 s; 4 s) | S02, aplicada al texto nuevo, queda cazada (falla «mañana atrasada, el reloj 1 h detrás…»), y también R01, R02 y R03 |
| CC-4 (H-03) | «miercoles_libre: el corte se ve al reabrir (linea_incompleta) y el diario queda limpio…»; «jueves_stop: tras reiniciar (primer corte en el diario firmado: la última OP sin su RES)…»; «jueves_conciliar: segundo corte en el diario firmado, en 9 posiciones…» y el corte en vivo; «jueves_degradar: tras reiniciar (corte dentro de la reescritura…)» | S01 y S03 quedan cazadas. D10 (FUERA) también cae ahora en la semana |
| CC-5 (H-07) | `t84_contrastar_da_el_mayor_con_el_reloj_por_delante`, `t84_contrastar_da_el_mayor_con_el_intermediario_por_delante`, `t84_tras_un_dia_de_marcha_un_salto_de_10_s_se_para_RL01` en `pruebas_reloj_t03.py` | r01 `--resto`: R04 y R06, que antes no cazaba ninguna batería, las caza ahora `reloj_t03` |
| CC-6 (H-06) | «jueves_degradar: al reabrir se borran los dos temporales huérfanos (.diario-*.tmp y .estado-*.tmp) y no los ficheros parecidos» | D11 cazada. La nota final de r02 da «quedan 0 fichero(s) temporal(es)» (antes, 1) |
| CC-7 | `persistencia.esquema_actual()` en copias de HEAD sin los cambios y con ellos | `aa778db7…0459` en `1a91d28` y `2bcc76b8…6bde` en `7b775cc`, el mismo con y sin los cambios en los dos. `reloj.py` y `persistencia.py` quedan sin cambios |
| CC-8 | `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c` | Árbol de trabajo: **SIN DIFERENCIAS (0)**. En la copia limpia de `7b775cc` queda una diferencia que no es de esta ronda: `pruebas_parametros_doc_t83.py` ejecuta 62 y el LEEME de HEAD ya cita 109, porque los cambios de T-83 que la llevan a 109 están en el árbol de trabajo, sin commit |
| CC-9 | `.docs/scripts/pruebas_marco.sh` | 61 de 61 en el árbol de trabajo y en la copia limpia con el parche. La línea base del árbol de trabajo al empezar daba 54 de 61 por los cambios a medias de otro agente en `orquestador.py` (esquema sin migración); al terminar, ese agente ya había subido `7b775cc` |
| CC-10 | `README.md` (resultado de la ronda) y `analisis-tecnico.md`; la nota final de `entrega_glm/V0.63/revision.md` | Hecho |

## Mutaciones (r01, regresiones)

r01 se ejecutó con `--doradas --resto` sobre la copia limpia de `1a91d28` con los cambios.

| ID | Se espera | Antes (r01 de la QA) | Ahora en la semana | Dorada ahora | Otras que la cazan ahora |
| --- | --- | --- | --- | --- | --- |
| D02, D04, D05, D07 | CAZAR | cazadas | cazadas | viva | como antes |
| D10 | FUERA | viva | **cazada** | viva | diario_t03, jornada |
| R01 | CAZAR | **viva** | **cazada** | viva | reloj_t03 |
| R02 | CAZAR | **viva** | **cazada** | viva | reloj_t03 |
| R03 | CAZAR | **viva** | **cazada** | viva | reloj_t03 |
| R04 | FUERA | viva (ninguna) | **cazada** | viva | **reloj_t03** (H-07) |
| R05 | CAZAR | **viva** | **cazada** | viva | reloj_t03, robustez_t03, reloj_diario_t72 |
| R06 | FUERA | viva (ninguna) | viva | viva | **reloj_t03** (H-07) |
| R07 | CAZAR | **viva** | **cazada** | **cazada** | reloj_t03, reloj_diario_t72 |
| R08 | CAZAR | **viva** | **cazada** | **cazada** | reloj_t03, reloj_diario_t72 |
| R09 | CAZAR | **viva** | **cazada** | **cazada** | reloj_t03, robustez_t03 |
| P05, P06 | CAZAR | cazadas | cazadas | viva | como antes |
| S01 | CAZAR | **viva** | **cazada** | viva | ninguna |
| S02 | CAZAR | **viva** | no aplicable a r01 tal cual; **cazada** con el texto nuevo | viva | ninguna |
| S03 (nueva) | CAZAR | — | **cazada** | viva | ninguna |
| D11 (nueva, H-06) | CAZAR | — | **cazada** | viva | ninguna |
| D01, D03, D06, D08, D09, P01 a P04 | FUERA | vivas | vivas | vivas | como antes (baterías de T-03) |

**Recuento.**

- r01 tal cual (26 mutaciones aplicables): la semana caza **16**. Son las 14 CAZAR (D02, D04, D05, D07, R01 a R03, R05, R07 a R09, P05, P06 y S01) y 2 FUERA (D10 y R04). Antes cazaba 6 (D02, D04, D05, D07, P05 y P06).
- Con S02 adaptada y las nuevas S03 y D11, la semana caza **19 de 29**, entre ellas las 17 CAZAR.
- **R06**, que es FUERA, sigue viva en la semana, porque las fuentes de la semana no saltan. La caza `reloj_t03`.
- Con S02 adaptada al texto nuevo y las nuevas S03 y D11, ninguna de las CAZAR queda viva: «LA SEMANA CAZA TODO LO QUE DICE PROBAR».
- Cada regresión falla sin su corrección; eso es lo que mide cada mutación. Revirtiendo:
  - el uso de `ahora()` (R07 y R08), la semana cae;
  - el modelo del instante (R04 y R09), cae;
  - la mañana atrasada (R01 a R03 y S02), cae;
  - los cortes (S01 y S03), cae;
  - la limpieza de temporales (D11), cae en «jueves_degradar: al reabrir se borran…»;
  - las pruebas de H-07 (R04 y R06), cae `reloj_t03`.

**Defecto de la sonda r01.** Al llegar a una mutación que no se puede aplicar (S02, cuyo texto con `assert` se quitó por H-02), r01 se cae con `ValueError: not enough values to unpack (expected 5, got 4)`. La rama «no aplicable» de `una()` devuelve 4 valores y `main()` desempaqueta 5. Las 26 anteriores quedaron medidas e impresas. S02 se midió con un envoltorio de r01 en el scratchpad, fuera del repositorio, que sustituye la cadena de S02 por la nueva («`ce = self.reloj.comprobar_estado(self.o)`» → «`ce = {"ok": True, "codigo": "OK"}`») y añade S03 y D11. r01 no se ha tocado: lo corrige quien mantenga la sonda (QA r02).

## Sondas de la QA tras la ronda (copia limpia de `7b775cc` con el parche)

- **r02:** «TODO FALLA CERRADO» (27 de 27). La nota final pasa de 1 temporal huérfano a 0 (H-06).
- **r03:** «HAY FALLOS», solo por B9, que es la corrección de H-02. B9 exigía que la `Maquina` parase la batería con un AssertionError; ahora arranca y deja el RL-02 en `arranque` para contarlo. B8 y B10 siguen como hallazgos: son H-04 y H-05, que pasan a la deuda.
- **r04:** «LAS DOS PROPIEDADES SE CUMPLEN». Ahora además son pruebas de `pruebas_reloj_t03.py`.

## Determinismo y límites de la batería

- Salida idéntica byte a byte en cuatro ejecuciones (sha-256 `8b5d447ba7ec2431…`), unos 10 s de reloj y 4,3 s de CPU.
- Con `python -O` la semana no pasa, ni antes ni ahora. Lo que H-02 pedía sí está: los arranques del reloj ya no dependen de `assert`. Pero los auxiliares compartidos de `pruebas/pruebas_orquestador.py` (`nuevo()`, `registrar_sello`, `detectar` en el lote) y `p_encargos` llaman al Orquestador dentro de `assert`, que desaparece con `-O`. Arreglarlo toca `pruebas_orquestador.py`, fuera de esta ronda (deuda, con H-08).

## Gate

- `tools/refs_vivas.py`: «todas las rutas citadas … existen».
- `tools/secrets_scan.py`: «sin hallazgos».
- `./tools/check_all.sh`: resultado abajo.

## Comandos usados

```bash
cd sistema_global/marco_comun_c
/home/claude/repo/.venv/bin/python -I pruebas/pruebas_semana.py            # dos veces, comparando sha-256
/home/claude/repo/.venv/bin/python -I pruebas/pruebas_reloj_t03.py
/home/claude/repo/.venv/bin/python -I pruebas/pruebas_doradas.py
/home/claude/repo/.venv/bin/python -I entrega_claude/V0.63_revision/r01_mutaciones_semana.py --doradas --resto   # en la copia limpia
/home/claude/repo/.venv/bin/python -I entrega_claude/V0.63_revision/r02_segundo_corte_firmado.py
/home/claude/repo/.venv/bin/python -I entrega_claude/V0.63_revision/r03_reloj_detras_del_estado.py
/home/claude/repo/.venv/bin/python -I entrega_claude/V0.63_revision/r04_reloj_huecos_sin_bateria.py
cd validador && /home/claude/repo/.venv/bin/python -I -c "import sys; sys.path.insert(0,'.'); import persistencia as p; print(p.esquema_actual())"
cd /home/claude/repo
.docs/scripts/pruebas_marco.sh
/home/claude/repo/.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c
.venv/bin/python tools/refs_vivas.py && .venv/bin/python tools/secrets_scan.py
./tools/check_all.sh
```

## Gate final de c1

El agente de c1 se paró mientras pasaba el gate. Al subirlo, `.docs/scripts/commit_limpio.sh` pasó sobre una copia limpia de HEAD, con solo los ficheros de T-84, las baterías del marco, su LEEME y el gate completo; si no hubieran pasado, no habría commit.
