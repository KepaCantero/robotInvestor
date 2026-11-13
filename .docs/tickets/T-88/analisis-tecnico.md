# T-88 · Análisis técnico

## Causa raíz

Con el simulador, la primera llamada a un prefijo lo escribe en la caché y las siguientes lo leen, igual que la API real. Cuando varios tipos llaman al mismo agente en paralelo, cuál escribe depende del orden de los hilos. En un ciclo V5 de doce perfiles, las escrituras de AG-10 y AG-11 caen en RV en una ejecución y en RF en otra (unos 20.000 tokens cada una). Lo mismo pasa con AG-14 en MP o IDX. En la V6 ocurre con el núcleo de los analistas (IDX o FON) y con AG-28. El total del run es el mismo; cambia el reparto entre tipos (hasta ±3,5 UC en FON).

## Evidencia

Script de diagnóstico (tres ciclos con los doce perfiles y seis hilos, comparación de `presupuesto` en F5): antes, en la V5, cambian DIV, FON, RF y RV; después, iguales en V5 y V6. Con seis perfiles, `tests/test_t88_consumo.py`.

## Implementación

- `orquestacion.py`, `Bloque._cargar` (llamado desde `_invocar`): si la llamada tiene tokens cacheados y no es un acierto de la caché de respuestas, se carga la lectura de todo lo cacheado más la prima «solo». Esa prima es el prefijo (cacheados ÷ intentos) si es la primera llamada de ese agente en esa bolsa, y 0 si no. Los tokens escritos de verdad quedan pendientes.
- `consumo.py`, `Presupuesto`: `primera_llamada`, `cargar_con_prima` y `liquidar_primas`, con las primas en tokens enteros. La prima en UC es la parte de entrada de `Contabilidad.uc_de` (0,5 × tokens × (1 − factor de lectura) / tokens por UC). `resumen()` liquida antes de resumir, y el ciclo liquida al acabar la fase en paralelo.
- **Primer intento descartado:** cargar todas las primas a la bolsa común. Subía su consumo de 4,9 a 22,8 de 24 UC, porque también se llevaba las escrituras propias de cada analista, que sí son deterministas.
- **Segundo intento descartado:** cada bolsa paga su coste «solo» sin liquidar. Es determinista, pero en la V5 carga 83 UC frente a 55 reales.
- **Tercer intento, con un fallo:** liquidar con la prima real calculada como la resta de dos importes redondeados. El redondeo dependía de qué llamada escribía (110.821 frente a 110.818 diezmilésimas). Por eso la prima se guarda en tokens.

## Límites

- Con la API real, la caché caduca (TTL). Si un tipo vuelve a escribir un prefijo caducado, su prima «solo» no lo recoge; la liquidación sí reparte lo escrito de verdad.
- Las llamadas posteriores al registro de F5 (AG-18, AG-19 y AG-20 en la V5) no se cargan a ninguna bolsa: unos 3 UC en un ciclo de doce perfiles. Ya pasaba; en la V6 son código.

## Comandos

```bash
.venv/bin/pytest -q bloque_a/11_Ejecutor/tests/test_t88_consumo.py
```

## Ronda r02 (QA r01)

- **H-01 (media):** cargar durante la fase la prima «solo» de todos los agentes sumaba unos 2,8 UC a cada tipo en la V5 y cerraba fases que antes no se cerraban. Ahora, durante la fase, cada tipo carga la lectura de lo cacheado y solo la escritura del prompt de su propio analista (`AGENTE_CLASE`), que siempre escribe él. Es lo mismo que antes de T-88 para esos prompts. Las escrituras de los agentes compartidos (AG-10, AG-11, AG-12, AG-14, AG-28) y del núcleo V6 se reparten al liquidar, al acabar la fase en paralelo. Con `r01_03_prima_solo_ampliaciones.py`, 57 de 59 comprobaciones; las dos que no pasan van en la otra dirección: la versión anterior cerraba fases en el tipo cuyo hilo escribía primero la caché compartida (el que pagaba la escritura), así que en ese escenario de presupuesto justo su selección tampoco era fija.
- **H-02 (baja):** la liquidación reparte por grupo de prefijos: todos los analistas (comparten el núcleo V6; en la V5 cada uno escribe el suyo, que vuelve entero a su tipo) y cada agente compartido aparte.
- **H-03 (baja):** ya no se promete prudencia: durante la fase, lo que el control ve de los agentes compartidos es su lectura, como en la estimación previa (`_estimar_uc`). Si la caché se pierde a mitad del ciclo, la liquidación carga lo escrito de verdad.

## Ronda r03 (QA r02 NO APTO)

- **H-05:** en la V5, cada analista es su propio grupo de prefijos (escribe solo su prompt), así que ningún tipo paga el de otro. En la V6, los analistas comparten el núcleo común y siguen en un grupo, en el que el kit de cada uno se reparte junto con el núcleo: hasta unos 0,03 UC por tipo y 0,16 por ciclo, según la QA r02. Separar núcleo y kit exigiría saber cuántos tokens escribió cada bloque, y la API solo da el total; queda declarado en INC-T88-01.
- **H-06 (declarado):** en la V6, cada analista carga durante la fase su prima «solo», núcleo y kit enteros. Es prudente, pero con un presupuesto muy justo puede cerrar una fase que antes no se cerraba (INM en el barrido de la QA). Se acepta porque es la dirección que falla cerrado.
- **H-07:** el README ya no promete prudencia en la V5. Durante la fase, el control no ve las escrituras de los agentes compartidos (unos 3,5 UC por ciclo de doce perfiles); se cargan al liquidar.
- **H-08:** pruebas unitarias de `Bloque._cargar` (analista propio frente a agente compartido, caché caliente, intentos, segunda llamada, grupos de la V5 y de la V6) y de las dos liquidaciones por ciclo.
- **H-09:** `cierres_parciales` se guarda en F5 ordenado por tipo, fase y motivo. El orden de las ampliaciones en HA sigue dependiendo de los hilos, pero no cambia su contenido.
