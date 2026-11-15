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
