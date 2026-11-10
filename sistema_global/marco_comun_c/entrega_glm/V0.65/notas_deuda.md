# Notas de deuda — V0.65 (pasada de coherencia contra la Constitución)

Cambios en «Deuda técnica y pendientes del operador» de `Deuda_tecnica.md`. La pieza no toca código: las
filas nuevas son las que propone la pasada de coherencia (`pasada_coherencia.md`, hallazgos PC2-01 a
PC2-08), para que el operador las incorpore si le parecen bien. No se numeró por encima de lo que ya
existe (la última fila era T-63, de V0.64).

## Tabla T

- **T-64 (nueva, sin resolver): el perfil inversor y la política de inversión personal no están en SC-1.**
  La Constitución (§2 con el operador, §6 «Perfil inversor y riesgo», §14 Fase 1 «Broker Personal (perfil
  inversor)») pone el perfil inversor y de riesgo del operador en SC-1, versionado, con la regla de bajar
  el riesgo de una cartera al momento y subirlo con segundo factor y espera, y una política de inversión
  personal que el Broker recuerda antes de aceptar una orden que la contradiga. `validador/mandatos.py`
  solo lleva mandatos por cartera (version, benchmark_ref, horizonte_dias, apalancamiento_max,
  tamano_max_pct_cartera, instrumentos_permitidos, exclusiones). Riesgo: los mandatos y los controles del
  §6 se fijan sin el perfil que debe orientarlos; la pieza del Broker conversacional no tiene dónde leerlo.
  Cuándo: Fase 1 (antes de fijar los mandatos con P-03/D-28). Hallazgo PC2-01 con script
  (`entrega_glm/V0.65/scripts/pc2_01_perfil_inversor.py`, FALLA).
- **T-65 (nueva, sin resolver): controles de F que T-22 dejó fuera y nadie retomó.** T-22 se cerró en
  V0.36 con «Fuera: liquidez, costes, margen y límites por cartera». Quedan fuera del código: la fracción
  del volumen medio diario (5 %, RATIFICADO en D-27/P-22), la liquidez mínima del mandato (§7), el coste
  total y el margen de la orden (§8.8), la exposición compartida por divisa, emisor o factor (§8.2, hoy
  solo F-06 total y F-07 por activo) y los límites nominales distintos por cartera (la política de F es
  un único diccionario). Riesgo: una orden enorme en un instrumento ilíquido pasa todos los controles de
  F si los demás límites la dejan. Cuándo: Fase 1 (los valores, con D-11/D-31; la estructura, en código).
  Hallazgo PC2-02 con script (FALLA).
- **T-66 (nueva, sin resolver): contrapesos de la abstención (D-22): embudo visible y alarma de sequía.**
  N debe mostrar cada semana el embudo (oportunidades por capa y por qué caen) y avisar a los 60 días
  (P-17/D-27) si nada llega a invertirse habiendo candidatos que pasaron el análisis. Hoy la consola no
  calcula ninguno de los dos y el Orquestador no lleva el temporizador. El seguimiento de lo descartado
  es del bloque I (Fase 5) y no entra en la fila. Riesgo: que los controles dejen de invertir sin que
  nadie lo vea (P5). Cuándo: Fase 1, con el flujo real de A/B. Hallazgo PC2-03 con script (FALLA).
- **T-67 (nueva, sin resolver): cartera sombra pasiva desde el primer día (D-22/D-27).** Un plan pasivo
  simple (índice mundial) corriendo en simulado con los mismos aportes y retiradas que la cartera real,
  valorado con los datos de K, con la foto mensual lista para cuando I la compare (24 meses, D-27). Hoy
  no existe nada de la sombra en el marco. Riesgo: no habrá base para decidir si el robot aporta valor
  (P17) cuando llegue I. Cuándo: Fase 1. Hallazgo PC2-04 con script (FALLA).
- **T-68 (nueva, sin resolver): posicionamiento de grandes inversores en K y registros comunes (D-23).**
  K debe llevar el posicionamiento (COT de la CFTC, 13F, participaciones de la CNMV, operaciones de
  directivos) con su fecha de publicación, y la Fase 1 pide K «mínimo, divisas, con el COT de la CFTC»
  (§14); los cuatro registros comunes (análisis vigentes, riesgos geopolíticos, tendencias tecnológicas
  y posicionamiento) deben ser almacenes consultables con punto en el tiempo. Hoy K no tiene nada de
  posicionamiento y los registros no existen como almacenes (los expedientes del Orquestador cubren de
  facto parte de «análisis vigentes» para su propia tubería). Riesgo: se investiga dos veces lo mismo y
  el contexto de posicionamiento falta en B y C. Cuándo: Fase 1 (el COT y los almacenes); los otros dos
  registros esperan a SC-11 (PC2-06) y al radar de A. Hallazgo PC2-05 con script (FALLA).
- **T-69 (nueva, sin resolver): la envoltura común al día con la §5.** La §5 pide confianza e
  incertidumbre en todo mensaje; los contratos vigentes no las llevan como campos (CT-G-02 lleva
  incertidumbre y la confianza en su capa 3 del payload; CT-G-01, CT-G-03, CT-G-08 y CT-G-14 no llevan
  ninguna), CT-G-03 y CT-G-14 tampoco llevan resultado_politica, y el registro de contratos marca todas
  las envolturas «COMPLETA» con un criterio propio. Riesgo: la Constitución y el registro dicen cosas
  distintas; un contrato nuevo puede heredar el criterio equivocado. Cuándo: con la próxima revisión de
  contratos (o enmienda de la §5 si el operador decide que confianza/incertidumbre no son obligatorias
  en todos). Hallazgo PC2-08 con script (FALLA).

## Tabla D

- Ninguna fila nueva. Todo lo que la pasada encontró pendiente del operador ya tiene fila: P-02..P-24
  (incluida P-24 para las fuentes de SC-11, hallazgo PC2-06, que espera a P-05 según T-56), T-56 (datos
  base del perfil), T-57 (sesión única de decisiones) y T-58 (enmienda 2). Las dos propuestas de enmienda
  de la Constitución (PC2-07 para la §13, methodology_version; PC2-08 para la §5, envoltura) van al §15
  cuando las ratifique el operador, no a esta tabla.
- Ninguna fila se resuelve en esta pieza: no se cambia código y las seis filas nuevas entran sin resolver.
