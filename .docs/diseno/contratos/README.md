# Borradores de contratos (sin ratificar)

Esquemas JSON de contratos que salen de decisiones ya aceptadas como rumbo (tanda 1, 11-11-2026) y que el código todavía no usa. **No están en el marco común**: se aplicarán allí, con su versión y su batería de conformidad, cuando el operador ratifique la enmienda 5 y se cierre el diseño del bloque correspondiente. Mientras tanto sirven para discutirlos con datos y para que el código nuevo (como el registro de experimentos) ya escriba con su forma.

| Fichero | Contrato | Sale de | Qué añade |
| --- | --- | --- | --- |
| `ct-g-08_0.4.0-borrador.schema.json` | CT-G-08 · Resultado de control de F | Decisión 4 de la tanda 1; cambios 47 y 78 de la enmienda 5 | El tipo de acción que deduce F (`ABRIR_O_AUMENTAR`, `REDUCIR_O_CERRAR`, `PROTEGER`, `REEQUILIBRAR`) y cómo lo dedujo (posición conciliada de G, cantidad y sentido pedidos, criterio). Si reduce, cierra o protege: nunca `REDUCIDO`, y solo puede vetar una regla de forma |
| `ct-g-24_0.1.0-borrador.schema.json` | CT-G-24 · Anotación del registro de experimentos | Decisión 5 de la tanda 1 (D-53 propuesta); T-99 | Las tres anotaciones del registro: prerregistro sellado, intento y resultado. Es exactamente lo que escribe `.docs/scripts/registro_experimentos.py` |

Los dos se generan con `python3 .docs/diseno/contratos/generar_borradores.py`. CT-G-08 parte del 0.3.0 vigente del marco (`sistema_global/marco_comun_c/esquemas/ct-g-08_0.3.0.schema.json`), así que no se separan. Las pruebas, con ejemplos sacados de un informe real de F y del propio registro, están en `.docs/scripts/pruebas_borradores_contratos.py`.

## Lo que estos borradores concretan por su cuenta (`[PROPUESTO]`, para Astra y el operador)

1. **Reglas de forma** que pueden vetar una reducción o una protección: F-01 (forma), F-10 (cartera sin conciliar o vieja), F-12 (sin tipo de cambio), F-23 (precio alejado de la referencia del intermediario) y dos nuevas: **F-24**, cantidad mayor que la de la posición conciliada, y **F-25**, orden duplicada. Las dos nuevas salen de la lista de errores de forma del cambio 47.
2. **Una reducción no sale `REDUCIDO`**: o pasa o se veta por forma. Reducirla a medias por un límite sería, precisamente, lo que la asimetría prohíbe.
3. **`REEQUILIBRAR` va aparte**: el esquema no le aplica la regla de las reducciones, porque es una compra; su exención de los límites de pérdida, frecuencia y ventanas (cambio 78) la aplicará F, no el esquema.
4. **CT-G-24 sin envoltura común** (`event_id`, `producer`…): es un registro, no un mensaje entre bloques. Si J lo publica como mensaje, la envoltura se añade al cerrar su diseño.
