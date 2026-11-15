# T-148 · Análisis técnico

## Causa raíz

- **H-01.** S4 suponía que cada llamada lee la salida máxima de las anteriores «copiada una vez». `Bloque._refutacion` no hace eso en dos papeles: la respuesta a objeciones lleva, en cada objeción pendiente, su argumento, las dimensiones E de la opción y la lista de su evidencia citable; la contrarréplica, en cada objeción fuerte dada por resuelta, el contenido de cada evidencia citada (`_contenido_evidencia`), y una misma evidencia puede citarse varias veces. El encargo crece con objeciones × evidencias: la QA lo llevó a 196 239 tokens con S4 en 53 746. Lo único que lo para es `_invocar`: solo llama si `_estimar_uc(agente, mensaje)` cabe en lo que queda de la bolsa.
- **H-02.** S5 lo declaraba, pero la cifra se presentaba como «cota superior» sin más.
- **H-03.** `Bloque.ciclo` toma los tipos de F10 (P-02), que nace de `perfiles_activos` y después solo cambia por CT-04; la cota leía siempre la configuración.
- **H-04.** Las pruebas de T-145 no fijaban las cifras de la cota por presupuesto ni sus términos.
- **H-05.** La rama «sin datos en la ventana» de `comprobar_datos_a.py` no validaba la historia.
- **H-06.** Texto del §1 anterior a T-145. El borrador en disco de la base (`dd166b3`) no coincidía con el generador (`--comprobar` daba 1): se regenera.

## El tope de S4b

`_estimar_uc` = UC(entrada = JSON compacto del mensaje / 3,6 + 1 500, lectura = sistema, salida = 2 500) y la llamada solo va si cabe en la bolsa (con la ampliación, que la respuesta y la contrarréplica pueden pedir, hasta el máximo). Con la bolsa entera, el mensaje admitido cumple 0,5·(m + 1 500)/8 000 + 0,5·2 500/1 500 ≤ L, es decir m ≤ 2·8 000·(L − 0,5·2 500/1 500) − 1 500. En la bolsa de un tipo, L = N2 × (1 + 0,5) = 27 UC: **m ≤ 417 167 tokens**. La cota toma lo medido para el agente más ese tope (lo medido ya incluye el mensaje simulado: cuenta doble, a favor de la cota). `test_t148.py` comprueba que un mensaje de ese tamaño no cabe en `_estimar_uc` y uno del 99 % sí, y que 1 500 y 2 500 siguen en el código.

**Supuesto que queda (`[PROPUESTO]`, INC-T129-01).** La estimación mide el JSON compacto; el encargo lo lleva con sangría (`prompts.mensaje_usuario`, `indent=1`). En caracteres ocupa más; en tokens, poco (el tokenizador agrupa los espacios). La cota aplica S1 (×1,35) a los tokens del JSON compacto; se comprobará con los tokens reales del modo sombra.

## Con T-146 integrado

Aviso de la coordinación: T-146 (otra copia) hace que el presupuesto reserve el peor caso antes de cada petición (entrada × 1,35 como escritura de caché, `max_tokens` de salida, búsquedas al máximo a 0,32 UC cada una), que AG-18/19/20 paguen de la bolsa común y que la suma del ciclo no pase de 240 UC (360 con la ampliación). Esta copia no tiene ese código y no lo duplica. `cota_ciclo(…, con_t146=True)` (`--con-t146`) da la cota por presupuesto como solo los límites (46,08 USD: 360 UC al peor precio por UC); si la configuración trae `presupuesto_uc.uc_por_busqueda`, el precio por UC de una búsqueda entra en el máximo (con 0,32 UC, 0,031 USD/UC, por debajo de los 0,128 de Opus: no cambia). Sin el parámetro, la de esta copia. Al integrar T-146 hay que pasar `--con-t146` (o cambiar el valor por defecto) y quitar de la cota por presupuesto lo que ya no queda fuera.

## Implementación

- `.docs/scripts/estimar_coste_ciclo_a.py`: `MULTIPLICAN_ENCARGO`, `TOKENS_FIJOS_ESTIMACION`, `SALIDA_ESTIMACION`; S4, S4b y S5 reescritos; en `cota_ciclo`, `tipos` y `con_t146`, `limite_max` y `encargo_max` por bolsa (los términos del presupuesto se calculan antes del bucle; los textos de los mutantes del revisor siguen apareciendo una vez), `peor(…, bolsa, multiplica)`, `lee_tok` en cada papel, `usd_por_mil_tokens_leidos_por_busqueda`, `encargo_max_por_bolsa`; `tipos_del_estado`; `--estado` y `--con-t146` en `main`.
- `.docs/scripts/comprobar_datos_a.py`: aviso en la rama antigua y docstring.
- `.docs/scripts/borrador_anexo_b.py` y el borrador regenerado.
- `bloque_a/11_Ejecutor/tests/test_t145.py::test_h01_la_tabla_de_llamadas_del_ciclo`: la igualdad `encargo_tok == medido + 52 000` fijaba el supuesto S4 que la QA mostró falso; ahora fija `lee_tok == 52 000` y el encargo nuevo, igual de exacto (comentado «T-148»).
- `docs/incidencias.md` (INC-T129-01) y `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (§7): la tabla nueva.

**Límites.** Lo que lee cada búsqueda sigue fuera de la cota por llamadas (con T-146, dentro de la de presupuesto si el presupuesto lo carga); la tarifa de contexto largo no se modela (Opus 5.5 y Sonnet 5.5 no la tienen; la curación, en Haiku 5.5, queda por debajo de 100 000 tokens con S4, probado); los reintentos del SDK; el texto de ciclos anteriores.

## Comandos

```bash
cd bloque_a/11_Ejecutor; PY=/home/user/robotinvestor/.venv/bin/python
$PY ../../.docs/scripts/medir_consumo_a.py <tmp>/m_div
$PY ../../.docs/scripts/medir_consumo_a.py <tmp>/m_12 2024-03-29 --config <doce.yaml>   # perfiles.activos: los 12
$PY ../../.docs/scripts/estimar_coste_ciclo_a.py <tmp>/m_div [--con-t146]
$PY ../../.docs/scripts/estimar_coste_ciclo_a.py <tmp>/m_12 --config <doce.yaml> [--con-t146]
$PY -I ../../.docs/tickets/T-145/revisores/r01_01_amplificacion_contrarreplica.py <tmp> <tmp>/m_div --n 120,150,170 --salida real --k 1
$PY -m pytest -q -p no:cacheprovider tests/test_t148.py tests/test_t145.py
cd ../..; .venv/bin/python .docs/tickets/T-145/revisores/r01_04_mutantes.py <copia con «_mut»>   # y una copia del script con tests/test_t148.py en PRUEBAS
.venv/bin/python .docs/tickets/T-147/mutantes.py <copia con «t147_mut»> --ticket T-148
```
