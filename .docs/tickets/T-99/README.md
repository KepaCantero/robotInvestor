# T-99 · Registro de experimentos con prerregistro sellado

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `.docs/scripts/registro_experimentos.py` y su uso en `.docs/scripts/banco_medida.py` (fuera de los bloques y del marco común) |
| Planifica · implementa · QA | claude · claude · astra |
| Aprobación del operador | 2026-11-12: «haz todo» (punto 2 de lo que se podía adelantar). La decisión de fondo es la 5 de la tanda 1, aceptada el 11-11-2026 |
| Deuda técnica | T-99 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que desde ya cada prueba que pueda cambiar cómo decide o cuánto cuesta el robot quede registrada **antes** de ejecutarse, con su hipótesis y su criterio de éxito sellados, y que cuenten todos los intentos, también los fallidos. Sin eso, un resultado se puede elegir a posteriori y la corrección por número de intentos (§9, punto 17) usa una cifra inventada.

## Alcance

- Entra:
  - el registro: fichero de solo anexar encadenado por huellas, con prerregistro, intento y resultado; validaciones y fallo cerrado; resumen por experimento y regla de «adoptable»; línea de órdenes;
  - el banco de medida lo usa: cada ejecución desde la línea de órdenes prerregistra (o añade un intento a `--experimento`) y anota su resultado, también si falla;
  - su forma, como borrador del contrato CT-G-24 (`.docs/diseno/contratos/`).
- No entra: J ni SC-4 (sin construir); el formato definitivo, que se fija con el diseño de J; los entrenamientos.

## Diseño

- **Dónde:** «.docs/experimentos/registro.jsonl» por defecto (nace con el primer experimento), en el repositorio, porque los experimentos sobre el código son del proyecto y no de un usuario. Una copia con datos propios elige otro fichero con `--registro`.
- **Sellado:** el prerregistro guarda la huella SHA-256 de su contenido; cada línea lleva `_seq`, `_hash_prev` y `_hash`, así que reescribir, quitar o reordenar una anotación rompe la cadena. Con la cadena rota no se anota nada más.
- **Reglas:**
  - sin prerregistro no hay intento, y sin intento no hay resultado;
  - un resultado no se reescribe;
  - veredictos cerrados: «mejor», «peor», «todavía no se sabe» y «fallido»;
  - una variante está dentro del máximo si es una de las primeras `max_variantes` distintas;
  - **adoptable** solo si el veredicto es «mejor», el intento está dentro del máximo y empezó después del prerregistro.
- **En el banco:** el veredicto del intento es «mejor» solo si gana al azar y al momento a la vez, «peor» si pierde con alguno y, si no, «todavía no se sabe».
- **Números:** el máximo de variantes lo declara cada prerregistro (en el banco, `--max-variantes`, 1 por defecto); ningún umbral nuevo.

## Criterios de aceptación (binarios)

1. CA-1: un prerregistro incompleto o mal formado no escribe nada.
2. CA-2: no hay intento sin prerregistro, ni resultado sin intento, ni dos resultados del mismo intento.
3. CA-3: reescribir un resultado, quitar un intento o cambiar el criterio después se detecta, y con la cadena rota no se anota nada más.
4. CA-4: cuentan todos los intentos, también los fallidos y los que no dan resultado; una variante de más no es adoptable aunque gane.
5. CA-5: el banco, ejecutado dos veces, deja un experimento con dos intentos y sus dos resultados; un intento que falla queda como «fallido».
6. CA-6: todo lo que escribe el registro valida contra el borrador de CT-G-24.
7. CA-7: no cambia ningún bloque ni el marco común, y las pruebas del banco no escriben en el registro del repositorio.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `.docs/scripts/pruebas_registro_experimentos.py` | Nominal, límites, fallo cerrado y manipulación | CA-1 a CA-4 |
| `.docs/scripts/pruebas_banco_medida.py` | Integración con A y el cliente simulado | CA-5 y CA-7 |
| `.docs/scripts/pruebas_borradores_contratos.py` | Contrato | CA-6 |
