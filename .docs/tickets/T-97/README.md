# T-97 · Marco común V0.74: valores por defecto alineados con la tanda 2

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `sistema_global/marco_comun_c/` (una sola pieza: el código de referencia de la Fase 1) |
| Planifica · implementa · QA | claude · claude · sin asignar (el operador decide quién, 12-11-2026) |
| Aprobación del operador | Apertura autorizada el 2026-11-12 («Sí, abre el ticket»). Toca los controles de F: plan **aprobado por escrito el 2026-11-12**: «Apruebo; empieza ya» (implementar sobre la V0.73 y avisar a Astra de que la QA de T-83 se hace sobre la V0.74) |
| Deuda técnica | T-97 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que los valores por defecto del marco común coincidan con lo que proponen los diseños y quedó decidido en la tanda 2 (`.docs/diseno/coherencia/cuestionario_tanda_2.md`, §8). Hoy el marco deja gastar 50 € al día en análisis, sus límites de F en euros no frenan con carteras pequeñas, la alerta de H es un −5 % fijo y el contraste de tipos de cambio es un 3 % para todas las divisas.

Son **valores por defecto para cualquier copia** (D-45), no el perfil de nadie: coinciden con las opciones recomendadas del cuestionario. Cada copia los personaliza en su SC-1.

## Cambios de alcance al implementar (12-11-2026)

- **H1 sale del ticket.** El Motor del marco no calcula la oscilación de ningún activo, y el Orquestador repite la cuenta de H con su propio umbral (no se fía del dato que le pase H). Hace falta una función nueva del Motor con datos de K y fijar el umbral en la posición al nacer: es T-98. Mientras, la alerta sigue en el −5 % fijo.
- **F se queda en lo que faltaba.** El marco ya limitaba en % del capital el tamaño por orden (F-04, 10 %), la concentración en un activo (F-07, 20 %) y la pérdida del día (F-08, 2 %). Faltaban el importe del día (25 %) y la pérdida de la semana por cartera (4 %, 5 % y 5 %). El largo plazo conserva el 2 % diario de F-08: quitarlo relajaría, y el ticket solo endurece. El capital es el de la foto de G (la cuenta tiene una sola cartera en la Fase 1).
- **Capital declarado.** Sin foto de G (L0 sin simulador conectado, L1 manual) el tope anual no tendría base: se añade `capital_referencia_eur`, None por defecto. Sin foto y sin capital declarado, no se admite ningún encargo con coste.

## Alcance

- Entra (cuatro de las seis discrepancias):
  1. **Tope anual de gasto en IA y datos** (E2, cambio 76 de la parte 2):
     - clave nueva `tope_anual_gasto_pct_capital`, por defecto 0,5;
     - el Orquestador suma el gasto del año natural (UTC) y no admite un encargo que lo pase, con el capital gestionado de la última foto de cartera conciliada;
     - al llegar al tope: no entra ningún encargo que consuma IA, las rutinas deterministas siguen y sale un aviso nuevo, con acuse;
     - sin foto de cartera válida, no se admiten encargos con coste: falla cerrado;
     - el tope diario de hoy (`dia_coste_max_eur`) se queda como segundo límite.
  2. **Límites de F también en porcentaje de cada cartera** (F1 y F2):
     - claves nuevas en `politica_f`: importe máximo por orden (10 % de la cartera), por día (25 %) y por activo (20 %);
     - pérdida que frena aperturas y aumentos, por cartera:
       - trading: 2 % al día y 4 % a la semana;
       - táctica: 2 % al día y 5 % a la semana;
       - largo plazo: 5 % a la semana, sin límite diario;
     - los topes en euros de hoy siguen como techo absoluto: manda el más estricto;
     - **solo endurece**: con carteras grandes, los límites siguen como hoy; con carteras pequeñas, frenan antes.
  3. **Alerta de pérdida de H en veces la oscilación normal** (H1):
     - clave nueva `alerta_perdida_veces_oscilacion`, por defecto 2;
     - H pide revisar al perder dos veces la oscilación normal del activo en el plazo de la tesis, si el dato le llega en las métricas de la posición;
     - si no le llega, usa `alerta_perdida_pct` (−5 %), como hoy, y lo marca;
     - el resultado se acota al rango que ya valida `ALERTA_PERDIDA_RANGO`.
  4. **Contraste de tipos de cambio por divisa** (A3):
     - claves nuevas `tolerancia_tipo_k_rel_principales` (0,005) y `divisas_principales` (USD, GBP, JPY y CHF `[PROPUESTO]`);
     - `tolerancia_tipo_k_rel` (0,03) se queda para el resto.
- No entra:
  - **la discrepancia 5, el benchmark de cada cartera:** depende del mandato (P-03), que el cuestionario no preguntaba y que cada copia fija en su SC-1. Sigue en efectivo, marcado `[PROPUESTO]`;
  - **la discrepancia 6, los papeles del Broker:** resuelta en el diseño (E6), sin código en el marco;
  - el resto de respuestas de la tanda 2 que no son discrepancias (F3, F4, F5, H2 a H5, M1 a M4, A1, A2): son funciones nuevas y van con la construcción de cada bloque;
  - la asimetría de F por tipo de acción y el reequilibrio (cambios 47 y 78): esperan a la ratificación de la enmienda 5;
  - los bloques A, A-Forex y B, y la Constitución.

## Diseño

- **Versión:** marco V0.74. Antes del código, su Documento 0 en `sistema_global/documentos_0/V0.74_Valores_por_defecto_de_la_tanda_2.md`, como en cada versión.
- **Contratos:** ninguno cambia de forma. El informe de F (CT-G-08) añade los controles nuevos con su código de regla F-xx (forma ya existente).
- **Estado persistido:** cambia la configuración guardada. `CFG-0.11.0` pasa a `CFG-0.12.0` y la migración **MIG-010** añade las claves nuevas con su valor por defecto, con su lista `cambia`. Una copia guardada con V0.73 se abre en V0.74 sin perder nada, y sus valores personalizados no se tocan.
- **Números:**
  - todos son `[PROPUESTO]` en la configuración y en la tabla de `validador/parametros_doc.py` (T-83), cada uno con su justificación y su pregunta del cuestionario (D-45);
  - ninguno se escribe fuera de la configuración;
  - salen de las preguntas F1, F2, H1, A3 y E2 del cuestionario de la tanda 2.
- **Cómo falla cerrado:**
  - sin capital conocido, no hay encargos con coste;
  - con un límite en porcentaje y otro en euros, manda el más estricto;
  - una divisa sin clasificar usa la tolerancia del resto;
  - sin dato de oscilación, alerta con el porcentaje fijo y lo dice.
- **Decisiones del operador usadas:** E2, F1, F2, H1 y A3 de la tanda 2. La lista de divisas principales es `[PROPUESTO]` y va a la deuda técnica.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| T-83 (valores documentados) y V0.73 (T-75 y T-76) siguen esperando la QA de Astra | V0.74 cambia piezas que Astra tiene que revisar | Se construye sobre V0.73 tal cual, sin tocar lo de T-75 y T-76. El ticket avisa a Astra de que la QA de T-83 debe hacerse sobre V0.74, o la de V0.74 después |
| Muchas baterías (18) usan estos valores | Pruebas que cambian por motivos de configuración | Las claves nuevas no cambian el resultado de una cartera de las pruebas salvo donde el porcentaje es más estricto; cada prueba que cambie se justifica en `pruebas.md` |
| El tope anual bloquea las pruebas que no traen foto de cartera | Falsos fallos | Las pruebas existentes traen foto; se comprueba en la primera pasada de las 61 baterías |
| Endurecer F sin querer | Vetos donde antes no los había | Una batería nueva compara carteras grandes (sin cambios frente a V0.73) y pequeñas (frenan antes) |

## Criterios de aceptación (binarios)

1. CA-1: el Documento 0 de V0.74 existe y lo cita el `LEEME.md` del marco.
2. CA-2: con 20.000 € de capital, un encargo que pase el 0,5 % del año (100 €) no se admite, sale el aviso nuevo y una rutina determinista sigue funcionando; sin foto de cartera, ningún encargo con coste se admite.
3. CA-3: en una cartera de 20.000 € con 4.500 € ya invertidos hoy, F-14 deja como mucho 500 € más (25 %), aunque los 50.000 € del tope en euros dejarían pasar 45.500 €. En una cartera de 1.000.000 €, el resultado de F es el mismo que sin los porcentajes.
4. CA-4: con una pérdida del 4 % en la semana, la cartera de trading no abre; con la misma pérdida, la táctica sí (su límite es el 5 %).
5. CA-5: ~~alerta de H en veces la oscilación~~ fuera del ticket (T-98); la alerta sigue en el −5 % y sus pruebas no cambian.
6. CA-6: un tipo EUR/USD con un 0,6 % de desviación se rechaza y un EUR/SEK con el mismo 0,6 % pasa; con un 3,1 %, los dos se rechazan.
7. CA-7: un estado guardado con V0.73 se abre con MIG-010, recibe las claves nuevas con su valor por defecto y conserva los valores que tenía.
8. CA-8: `parametros_doc.py` documenta todas las claves nuevas (`faltan()` y `desfasados()` vacíos).
9. CA-9: las 61 baterías del marco y las nuevas pasan (`.docs/scripts/pruebas_marco.sh`), el `LEEME.md` coincide con el disco (`.docs/scripts/leeme_marco.py`) y el gate del repositorio da 12/12.
10. CA-10: no cambia ningún fichero de los bloques A, A-Forex ni B, ni de la Constitución.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Batería nueva `pruebas/pruebas_tanda2_t97.py` | Nominal y límites | CA-2 a CA-6 |
| Fallo cerrado: sin foto, sin oscilación, divisa sin clasificar | Fallo cerrado | CA-2, CA-5, CA-6 |
| Migración V0.73 → V0.74 con un estado guardado de V0.73 | Migración | CA-7 |
| `pruebas_parametros_doc_t83.py` | Regresión | CA-8 |
| Las 61 baterías, el LEEME y el gate | Regresión e integración | CA-9 y CA-10 |
