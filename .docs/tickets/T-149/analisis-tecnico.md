# T-149 · Análisis técnico

## Causa raíz

- **T-144 H-01.** `_paso_de_precio` tomaba la mayor potencia de 10 de la que eran múltiplos **todos** los precios de la serie. Los múltiplos de 0,05 (o de 0,25, 1/8, 1/32) lo son de una potencia de 10 menor, así que el error de redondeo supuesto era una fracción del real (0,005 frente a 0,025 en 0,05; 1/32 = 3125·10⁻⁵ daba 10⁻⁵) y la copia no cabía en la cota. Con un solo precio sin redondear, «todos» fallaba en cada potencia hasta la de la coma flotante.
- **T-144 H-02.** Ninguna prueba ponía un par en el borde de bᵢ + bₖ + 2·tol: una cota el doble de laxa, sin la tolerancia numérica o con la comparación estricta pasaba la batería.
- **T-147 H-01.** Los mensajes de `jsonschema` llevan la instancia («'…' is not one of …»), y los de la configuración la copiaban con `!r`. `ErrorCadenaB` los guardaba tal cual y `cadena_a_b.py` los escribía en `resumen.json` y los imprimía. El filtro R8 de la petición está al final de `construir_peticion`, después de esas validaciones.
- **T-147 H-02.** Las repetidas se buscaban en el texto de `TIME_PERIOD` («2026-11-3» ≠ «2026-11-03») y `pivot` caía después; `escribir` hacía `mkdir` sin capturar su `OSError`.
- **T-147 H-03.** Sin pruebas de falsos positivos en el borde de 16 caracteres ni con un dominio de una letra, sin una respuesta del BCE en otro formato de fecha y sin una sonda con datos protegidos.
- **O-01.** `cadena_a_b.py` leía `entregables.paquete_json` sin mirar la entrega: si la segunda pasada de G3 bloqueaba (el borrador del paquete sí se escribe, en la carpeta de bloqueados), reenviaba sus opciones; si bloqueaba la primera, caía con un `TypeError`.

## Evidencia

- `.venv/bin/python -I .docs/tickets/T-144/revisores/r01_01_copias_otras_rejillas.py`: antes, 5 hallazgos (0,05, 0,25, 1/8, 1/32 y el precio suelto); ahora 0.
- `.venv/bin/python -I .docs/tickets/T-147/revisores/r01_01_r8_y_peticion.py`: C2 a C5 en verde (los detalles dicen «'«dato protegido por R8»' is not one of …», con el campo); `r01_02_bce_y_clases.py`: las dos trazas, código 1.
- O-01, en el diseño: Documento 0 del Bloque A, 6 (CT-02 «Entrega de resultados … paquete JSON de oportunidades (con `paquete_para_bloque_B`)») y 7.3 (G3: «BLOQUEADO impide la entrega»); R4 (el Broker decide enviar al Bloque B) y 2.2 (el Bloque A no se comunica con él); `contratos.py` rechaza un retorno CT-02 sin `estado_g3` APTO o APTO_CON_ADVERTENCIAS, y `redaccion.py` quita `estado_g3` de un paquete bloqueado (T-65). El esquema CT-B-01 (Anexo B.1 del Bloque B) no dice nada de G3; INC-T142-01 tampoco. Conclusión: el diseño lo prohíbe, no es una decisión `[PROPUESTO]`.

## Por qué la fracción en la rejilla y no el paso de cada precio

Se probó el paso de cada precio (la mayor rejilla de la que es múltiplo cada uno), que resolvería también una copia que cambia de resolución con el tiempo. Con 300 semillas toma por copias 2 pares de índices con ρ ≈ 0,995 en 1/8 a 12 y bastantes más fondos (los precios «redondos», 50,00 o 12,50, ensanchan su fecha). La regla pedida es no tener falsos positivos en series distintas, así que se queda la de la serie con el 90 % y la de su década; la mezcla de resoluciones dentro de una década queda como límite declarado. Medida completa: `.venv/bin/python -I .docs/tickets/T-149/medir_copias.py` (y `--modulo <frontera_b.py de HEAD>` para la de antes):

| 300 semillas | antes (T-144) | ahora |
| --- | --- | --- |
| índices ρ ≈ 0,995 y rentabilidad total, niveles 100/12/2 × sin redondear, 0,001, 0,01, 0,05, 0,25, 1/8, 1/32 (paso ≤ 2 % del precio) | 0 en todo | 0 en todo |
| fondo, TE 0,1 %/año, a 100: 0,05 · 0,25 · 1/8 | 0 · 0 · 0 | 9 · 278 · 148 |
| copia con un precio sin redondear: no agrupadas | 299–300 de 300 en cada rejilla | 0, salvo 1/32 a 2 (9: medio paso > 1 %, el tope) |

Los fondos con rejillas gruesas se agrupan más porque la cota es ahora el redondeo real: a esa resolución no se distinguen de su índice (falla cerrado, el límite de los datos gruesos de T-144). Con otra semilla (`tests/test_t149.py`, semillas 5000+), 1/8 a 12 agrupa 1 de 300 índices: el paso es un 1 % del precio y la cota llega al tope de los casi clones (límite declarado, como 0,01 a 0,50 en T-144).

## Implementación

- `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`: `REJILLAS_PRECIO` `[PROPUESTO]`; `_en_rejilla` (fracción de precios en múltiplos de un paso por serie, en sitio para no gastar memoria); `_paso_de_precio` reescrito (potencias desde la década del mayor precio, para pasos de 5, 10, 50…; después múltiplos 25/5/2 de la potencia y fracciones 1/2ᵏ solo en las filas donde la potencia llega a 10⁻ᵏ, porque 1/2ᵏ = 5ᵏ·10⁻ᵏ); `_paso_por_decada`; en `_etiquetas_series_copiadas`, el error de cada precio es el mayor de los dos. Las líneas que mutan los scripts de mutantes (M17–M24, Q08–Q10) no cambian de texto.
- `bloque_a/11_Ejecutor/bloque_a/cadena_b.py`: `ESTADOS_G3_ENTREGA`, `sin_datos_protegidos` (`DATO_PROTEGIDO`, `DETALLE_OMITIDO`), `ErrorCadenaB` limpia su detalle, `errores_entrada_b` limpia antes de recortar, `ENTREGA_BLOQUEADA_G3` en `construir_peticion` (después de comprobar `run_id`).
- `.docs/scripts/cadena_a_b.py`: sin entrega del Bloque A, `sin_envio` y código 1 sin llamar al Bloque B; limpia el mensaje de la correspondencia y el de un ejecutor que falla.
- `.docs/scripts/descargar_datos_bce.py`: repetidas sobre la fecha convertida (`TIME_PERIOD` como texto: «20261112» ya no llega como número), `comprobar_destino` antes de descargar y en `escribir`, `OSError` al escribir con mensaje y 1.
- Pruebas: `tests/test_t149.py` (nuevo); `tests/test_t144.py` (dos pruebas del borde de la cota; en `test_h01_paso_de_precio`, [1,2345, 1,2] tiene paso 0,0005, no 0,0001: la prueba fijaba el defecto); `tests/test_t147.py` (las de Q02, Q03, Q05 y Q07; el `_cli` simulado de `test_h02_el_script_…` devuelve ahora la entrega y el G3 que da `bloque-a ciclo`: sin ellos el script ya no encarga). Ninguna se debilita.
- `bloque_a/11_Ejecutor/README.md` (códigos de la cadena B), `docs/incidencias.md` (INC-T127-01 y INC-T142-01, «Ronda T-149»; la de T-144 está en INC-T127-01 aunque su texto cite INC-T128-01), `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (fila de las fichas con componentes).

**Desviaciones.** Ninguna de alcance. El H-01 de T-147 se corrige limpiando los mensajes y no adelantando el filtro R8: así los códigos siguen diciendo qué falla (un correo en `tipo_activo` es `ENTRADA_B_INVALIDA`, con el campo) y la sonda sigue viendo las opciones sin correspondencia.

**Límites conocidos.** Rejillas fuera de la lista (0,03, 1/3), mezcla de resoluciones en una década, más de un 10 % de precios fuera de la rejilla y pasos del orden del 1 % del precio (INC-T127-01, «Ronda T-149»); lo que el detector de R8 no reconoce tampoco se limpia de los mensajes (INC-T123-01); si `os.replace` fallara a mitad de los seis CSV, los ya movidos quedan (los destinos se comprueban antes, así que solo un fallo del disco lo provoca). Coste: el índice de 2000 valores pasa de ~2,7 s a ~6 s.

## Comandos

```bash
cd bloque_a/11_Ejecutor; PY=../../.venv/bin/python
$PY -m pytest -q -p no:cacheprovider tests/test_t149.py tests/test_t144.py tests/test_t147.py tests/test_t142_cadena_b.py \
  tests/test_t141_datos_bce.py tests/test_t135_motor.py tests/test_t127_hallazgos.py tests/test_t127_r02.py tests/test_t128_frontera.py \
  tests/test_t128_r02.py tests/test_fase3_goldens.py
$PY tests/goldens_ct.py
cd ../..
.venv/bin/python -I .docs/tickets/T-144/revisores/r01_01_copias_otras_rejillas.py
.venv/bin/python -I .docs/tickets/T-147/revisores/r01_01_r8_y_peticion.py
.venv/bin/python -I .docs/tickets/T-147/revisores/r01_02_bce_y_clases.py <tmp>
.venv/bin/python .docs/tickets/T-147/revisores/r01_03_mutantes_qa.py <copia «t147_mut»> --ticket T-144   # y --ticket T-147
.venv/bin/python .docs/tickets/T-147/mutantes.py <copia «t147_mut»>
.venv/bin/python -I .docs/tickets/T-149/medir_copias.py [--modulo <frontera_b.py de HEAD>]
```
