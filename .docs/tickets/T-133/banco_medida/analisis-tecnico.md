# T-133 · Análisis técnico (banco de medida)

## Motivo

La QA r03 de T-94 dejó medios y bajos abiertos (H-21 a H-29). Los dos que había que corregir antes de usar el banco con el cliente real eran:
- H-21: adoptar un resultado por repetición;
- H-23: verificar contra un registro fabricado.

La parte del registro de los dos la resolvió T-99, con la regla de adopción por variante, el ancla y el sello. Aquí se cierra lo que es del banco.

## Implementación (banco 0.4.0)

- **Fuente por contenido (H-21, H-22).**
  - `huella_datos` resume nombres y bytes de los CSV de la carpeta de datos y del universo.
  - El prerregistro guarda `huella_datos` y `huella_universo`, y la fuente del experimento es `cliente + huellas`. Así:
    - los mismos datos copiados en otra carpeta son el mismo experimento;
    - unos datos cambiados son otra variante;
    - en el registro no queda ninguna ruta de la máquina.
- **Verificar (H-23).**
  - Sin `--registro`, se comprueba contra el registro del agente (`REGISTRO_DEFECTO` de `RI_AGENTE`), nunca contra el que dice la carpeta.
  - Si `experimento.json` cita otro, se avisa.
  - `dentro_del_maximo` de `experimento.json` se compara con el del registro.
- **Muestra primero (H-24).**
  - `ejecutar_a` evalúa una vez la plantilla del titular para elegir las fechas sin solape.
  - Después evalúa titular y referencias solo con la plantilla de esas fechas.
  - El informe da `plantilla` con las selecciones totales y las que entran en la muestra.
- **H-25.** Las NEUTRAL no gastan ventana en `fechas_sin_solape`.
- **H-26.** `leer_consumo` rechaza decimales en los recuentos, columnas obligatorias que faltan y columnas repetidas, y declara las opcionales ausentes (`columnas_ausentes`).
- **H-27.** `MIN_EFECTIVAS_MIN = MIN_EFECTIVAS` (10, el de A). Es la cota de un experimento, en `ejecutar_a`, en `diferencia` y en la línea de órdenes.

## Evidencia

- `pruebas_banco_medida.py`: 98 en verde, entre ellas `test_t133_*`, una por hallazgo.
- Simulación nula de T-94 (`nula_r03.py`, 100 mundos): un 10 % de veredictos firmes sin habilidad, con tema y sin tema.
- `mutantes.py` (esta carpeta): 0 vivos de 68. Son los 57 de la r03 de T-94, con M40 y M43 puestos al día porque el código cambió en T-99, y 11 nuevos de T-133.

## Límites

- La muestra de fechas se calcula con el titular, que es lo diseñado. Una referencia con fechas propias quedaría fuera de la muestra.
- La huella de los datos lee todos los CSV de la carpeta, lo que puede tardar con carpetas muy grandes.

## Ronda r02 (15-11-2026, QA r01 NO APTO, sin altos)

Banco 0.5.0.

| Hallazgo | Corrección |
| --- | --- |
| H-01 (media) | **Los datos van en la variante, no en el experimento** (`[PROPUESTO]`): la fuente es el cliente, y las huellas de los datos y del universo están en el prerregistro. Así, unos datos cambiados son otra variante del mismo experimento, fuera del máximo, y no un experimento nuevo con su máximo sin estrenar. La huella es solo de lo que A lee: el CSV de cada símbolo del universo y, del universo, los pares (símbolo, clase), sin el nombre del fichero. Un CSV que A no lee, o renombrar el universo, ya no cambian nada. Si los datos cambian durante la ejecución (o el titular usa otros), el banco se detiene. Unos datos nuevos de verdad (los de K) se prerregistran aparte. |
| H-02 (media) | Que `experimento.json` cite otro registro es un **aviso**, no un problema: una carpeta auténtica copiada a otra profundidad se verifica con código 0. |
| H-03 (media) | Pruebas de `verificar` sin `--registro`, con el registro del agente (`REGISTRO_DEFECTO`): un registro fabricado que cite la carpeta no se usa, y sin un `RI_AGENTE` válido se dice. |
| H-04 (baja) | Pruebas de N19 (en `construir_informe`), F03 (subcarpetas), F04 (orden), F05 (carpeta sin CSV), P03 (fechas sin normalizar) y la huella en NFC. |
| H-05 (baja) | `informe.md` dice cuántas selecciones tenía la plantilla, cuántas entran en la muestra y que una ventana que acaba después del último dato también ocupa su fecha. |
| H-06 (baja) | Una celda vacía, o una fila corta, en una columna obligatoria de `consumo.csv` es un error. Una columna ausente sale «sin dato» en `informe.md`. |
| H-07 (baja) | El docstring, el índice de scripts y la fila T-94 de la deuda están al día. En la r01, este análisis decía «otra variante» de los datos cambiados, y era falso: ahora sí lo es. |
| H-08 (baja) | Nivel mínimo de un veredicto: 0,90 (`[PROPUESTO]`; al 0,80 con 10 fechas salía un 24,5 % de firmes). El mínimo de fechas se lee de `evaluacion.min_conglomerados_bootstrap` de la configuración de A. |
| H-09 (baja) | La huella lee en trozos y normaliza los nombres a NFC. |

**Evidencia:** 106 pruebas del banco y 79 mutantes muertos (`mutantes.py`). Los mutantes del revisor que siguen casando mueren; los que ya no casan («sin patrón») están rehechos en `mutantes.py` como B01 a B22.
