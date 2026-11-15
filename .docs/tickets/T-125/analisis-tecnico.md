# T-125 · Análisis técnico

## Motivo

PB-46 era uno de los tres casos del plan «sin prueba» y la funcionalidad no existía (FUE- no se escribía nunca). Es un hueco menor de la deuda que el operador pidió completar.

## Implementación

- `evaluador.py`: `_campos_pronostico_fuente`, `Evaluador.pronosticos_de_fuentes`, `_cierre_en` y `fiabilidad_fuentes`; `ciclo` devuelve `fiabilidad_fuentes`.
- `orquestacion.py`: `_comunicar_fiabilidad` (CT-19 a AG-16) tras el informe de aprendizaje; `_registrar_evidencia_clase` guarda `pronostico_fuente` en la CLM cuando la pieza es PRONOSTICO_FUENTE.
- `config/por_defecto.yaml`: sección `fiabilidad_fuentes`.
- Decisiones `[PROPUESTO]` (INC-T125-01): mínimo de 5 pronósticos; ventana de 24 meses; probabilidad 0,7 para un pronóstico explícito sin ella; referencia ingenua 0,5; antigüedad máxima del cierre la de H2 (3 días); una FUE- por fuente y mes.
- Límites: la recalificación de Q y el orden en F9 los hace el Buscador con el modelo real (fuera del ejecutor); con el cliente simulado no se generan piezas PRONOSTICO_FUENTE, así que en un ciclo normal no sale ninguna FUE-.
- Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t125_fiabilidad_fuentes.py`.

## Ronda r02 (QA r01 NO APTO)

La QA r01 abrió H-01 (alta: en un ciclo ningún pronóstico de fuente llegaba a F2), H-02 a H-04 (medias: zona horaria, registro tardío, `ref_id` sin validar) y H-05 a H-08 (bajas). La frase del apartado «Límites» de arriba («con el cliente simulado no se generan piezas PRONOSTICO_FUENTE») era inexacta: el que perdía el bloque era el ejecutor, también con el modelo real.

### Cambios

| Hallazgo | Archivo | Cambio |
| --- | --- | --- |
| H-01 | `orquestacion.py` | `_bloque_pronostico_fuente`: las piezas de las afirmaciones del Analista (`_analizar_clase_en_ambito`) y de las referencias del Buscador (`_peticion_conocimiento`) llevan el bloque `pronostico_fuente` si lo traen. `_tipo_con_pronostico_fuente`, en el alta de la CLM: un bloque registrable hace la afirmación PRONOSTICO_FUENTE (aunque el Curador diga otra cosa); uno no registrable no se guarda, la afirmación PRONOSTICO_FUENTE pasa a PREVISION y el rechazo queda en HA (DATOS, Menor) con su motivo |
| H-01, H-03, H-04 | `evaluador.py` | `motivo_pronostico_fuente_no_registrable` (bloque completo y bien formado, `ref_id` de F9 y fuente de la pieza, emisión ≤ registro < fecha objetivo) y `fuente_de_opinion_registrada`. El Evaluador recibe `referencias` (el `Bloque` le pasa su `Referencias`); sin ellas no cuenta ningún pronóstico |
| H-02 | `evaluador.py` | `_fecha_de_calendario`: con zona horaria, la fecha de esa zona sin convertir; un valor no textual no se lee. En `Evaluador.ciclo`, un fallo de `fiabilidad_fuentes` deja `[]`, una incidencia HERRAMIENTA y el resto del C5 intacto |
| H-03 | `evaluador.py` | `pronosticos_de_fuentes` lee el bloque de la primera entrada de F2 que lo trajo y exige `emision <= registro < objetivo` |
| H-05 | `evaluador.py` | Deduplicación por (fuente, serie, fecha objetivo, emisión, dirección, umbral): cuenta la CLM de menor identificador |
| H-06 | `evaluador.py` | `fiabilidad_fuentes`: «ya hay FUE- del mes» se mira por fuente |
| H-08 | `evaluador.py`, `por_defecto.yaml` | Brier de la fuente y de la referencia por el Motor (`_brier_del_motor`, FC-EVAL-001) y `calc_id` en la FUE-; sin el Motor, no hay FUE-. `prob_sin_declarar: 0.65` (la de la banda «más probable que no») |
| H-07 | pruebas | `tests/test_t125_r02.py` (ventana con su borde, antigüedad del cierre con su borde, no vencido con dato disponible, emisión = objetivo, bordes de «dentro» y «fuera», p = 0 y 1, puntos acotados a 0) |

Las líneas que fijan los mutantes del revisor (`r01_02_mutantes.py`) se conservan tal cual (siguen apareciendo una vez), para que el script se pueda volver a ejecutar sin cambiarlo.

### Esquema de la respuesta del agente

`INFORME_CLASE.finalistas[].afirmaciones[]` y `BUSQUEDA.referencias[]` (`contratos.py`) no nombran `pronostico_fuente`, pero tampoco cierran las propiedades: el bloque pasa la validación de la respuesta y el ejecutor lo valida por código. No se toca `contratos.py` (lo lleva otra sesión) ni ningún esquema del corpus; el corpus no dice por qué camino llega el bloque a F2 (el esquema de F2 lo define; el prompt del Buscador, 5.3, los registra «en su ficha» de F9; el formato de los Analistas no lo nombra). Todo en INC-T125-01, `[PROPUESTO]`.

### Pruebas existentes que cambian

`tests/test_t125_fiabilidad_fuentes.py`: las pruebas sembraban F2 con el reloj en `AS_OF` (después de la fecha objetivo) y con `REF-0001`/`REF-0002`, que no son fuentes de F9. Con H-03 y H-04 ya no contarían. Ahora cada pieza se registra el día de su emisión (`_escribir_clm`) y las fuentes son `REF-RF-0001` y `REF-RF-0003`. Las afirmaciones no cambian (las mismas cifras, los mismos casos); se vuelven más estrictas, no más débiles: cada caso de «no cuenta» se rechaza ahora por su regla y no por el registro tardío.

### Límites

- En backtest no entra ningún pronóstico de una fuente de F9: no tienen fecha y el filtro de evidencia no las da por conocibles. Se prueba en modo vivo.
- K08 del revisor (emisión = objetivo) queda **equivalente**: la regla nueva de H-03 (`emision <= registro < objetivo`) implica `emision < objetivo`, así que ninguna entrada distingue el mutante. Se deja la comprobación por claridad.
- La recalificación en F9 sigue siendo del Buscador (modelo real).

### Comandos

Desde `bloque_a/11_Ejecutor`: `python -m pytest -q tests/test_t125_fiabilidad_fuentes.py tests/test_t125_r02.py`. Camino entero: `python ../../.docs/tickets/T-125/r02_camino_de_entrada_a_f2.py`. Mutantes del revisor con las pruebas nuevas, desde la raíz: `python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia con «_mut»>/bloque_a tests/test_t125_r02.py`.
