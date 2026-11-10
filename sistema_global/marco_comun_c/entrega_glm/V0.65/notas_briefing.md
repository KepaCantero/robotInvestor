# Notas de briefing — V0.65 (pasada de coherencia contra la Constitución)

V0.65: pasada de coherencia del código contra la Constitución V0.4 (solo documento, sobre V0.64 sin
cambios); el entregable es `entrega_glm/V0.65/pasada_coherencia.md`: una tabla de **185 filas** que
recorre la Constitución §0 a §16 requisito a requisito con las columnas §, requisito, dónde (módulo ·
función), prueba (batería · comprobación), estado y nota — 91 CUMPLE, 48 PARCIAL, 20 FALTA, 1 CONTRADICE
(G-06 contra «un mismo activo en dos carteras son dos posiciones», ya es T-13) y 25 FUERA DE FASE 1 —,
más ocho hallazgos **PC2-01 a PC2-08** con script cada uno y el resumen. El generador que viaja en la
entrega (`entrega_glm/V0.65/generar_pasada.py`; se ejecuta desde la carpeta `marcoC`, con `parents[2]`
como raíz) lleva las filas como datos y, antes de escribir el Markdown, verifica con `ast` que cada
función/clase/constante citada existe en su módulo de `validador/` y que cada comprobación citada
aparece en su batería de `pruebas/` (para la batería del sobre, `pruebas/ejecutar_pruebas.py`, busca
también en `generar_casos.py`); si una cita no cuadra, no escribe nada. Los hallazgos: PC2-01 (media) el
perfil inversor y la política de inversión personal no existen en SC-1 (`mandatos.py` solo tiene
mandatos: version, benchmark_ref, horizonte_dias, apalancamiento_max, tamano_max_pct_cartera,
instrumentos_permitidos, exclusiones) → T-64; PC2-02 (media) F no controla liquidez (el 5 % del ADV de
D-27), costes, margen, exposición compartida por divisa/emisor/factor ni límites por cartera
(`POLITICA_DEFECTO` de `control_f.py` sin claves de eso, `CLAVES_CONTEXTO` sin volumen, T-22 cerró con
«Fuera: liquidez, costes, margen y límites por cartera») → T-65; PC2-03 (media) sin embudo visible ni
alarma de sequía de 60 días (D-22; las comprobaciones de `consola.panel` son integridad, datos,
presupuesto, avisos, decisiones, kill_switch, autonomia, reloj, diario y migracion) → T-66; PC2-04
(media) cartera sombra pasiva inexistente (D-22/D-27, Fase 1) → T-67; PC2-05 (media) sin posicionamiento
en K (COT/CFTC, 13F, CNMV, directivos) y sin los cuatro registros comunes de D-23 → T-68; PC2-06 (baja)
sin SC-11 mínimo ni lectores aislados (bloqueado por P-24→P-05, T-56; sin deuda nueva); PC2-07 (baja)
sin `methodology_version` (§13) — el versionado real es version_esquema, version_politica (CT-G-08),
VERSION_REGLAS F-0.3.0, version_config CFG-0.11.0 y VERSION_PARAMETROS — propuesta de enmienda de la
§13; PC2-08 (baja) la envoltura de la §5 pide confianza e incertidumbre que los contratos no llevan como
campos (CT-G-02 lleva incertidumbre y la confianza en la capa 3 del payload; CT-G-01/03/08/14 ninguna;
CT-G-03 y CT-G-14 sin resultado_politica; el registro marca todo «COMPLETA») → T-69. Los ocho scripts
(`entrega_glm/V0.65/scripts/pc2_*.py`, ejecutar desde `marcoC`; el de PC2-06 usa patrones acotados: el
«noticia» que daba el falso OK estaba en el motivo que una prueba le pasa a H en `pruebas_orquestador.py`,
no en el docstring de H-16, que no dice «noticia») dan **FALLA** con V0.64 y sus salidas están en
`salida_pruebas.txt`. El lote completo sigue en 54 baterías, 0 con fallos, sin tocar ninguna: la pieza no
cambia código, esquemas ni pruebas; el único fichero del marco modificado es `LEEME.md` (cabecera V0.65,
párrafo «Fecha» y punto «Comprobado en la pasada de coherencia»). La revisión independiente que pide la
pieza: otro GLM comprueba 20 filas al azar (`random.Random(20261113)` sobre los números de fila),
ejecuta los ocho scripts y busca tres requisitos de la Constitución que la tabla no recoja. Se hizo el
10 de noviembre de 2026: dos hallazgos documentales bajos (la atribución del falso OK de PC2-06 y las
filas §9.5 y §9.10 que la tabla saltaba), corregidos en la propia entrega; el detalle queda en
`revision.md`.
