# Documento 0 — pasada de coherencia contra la Constitución (V0.65) — GLM, revisada el 10 de noviembre de 2026

## 1. Problema y alcance

La última pasada de coherencia del código contra la Constitución se hizo en V0.13 y desde entonces las
versiones van de la V0.14 a la V0.64 (las piezas del fin de semana V0.37–V0.41 y las cinco primeras del
kit 2).
Hacía falta saber, requisito a requisito, qué está hecho, qué está a medias, qué falta y dónde el código
dice otra cosa que la Constitución: es la base para planificar lo que queda de la Fase 1 (pieza 6 del kit
2, `Directrices_GLM_kit2.md` §7).

**Entra en esta versión:** el documento `entrega_glm/V0.65/pasada_coherencia.md`, con la tabla de
requisitos (§0 a §16, 185 filas), ocho hallazgos PC2-01 a PC2-08 con su script cada uno, y el resumen con
los estados y el orden de importancia; las filas de deuda nuevas propuestas en `notas_deuda.md`; el
generador de la tabla (`generar_pasada.py`) y los ocho scripts de los hallazgos (`scripts/pc2_*.py`).

**Queda fuera:** cualquier cambio de código, esquema o prueba (la pieza es «solo documento»: el único
fichero del marco tocado es `LEEME.md`, con su cabecera, el párrafo de fecha y un punto «Comprobado en»);
la revisión independiente (otra conversación, con la Constitución, el código y `pasada_coherencia.md`, 20
filas al azar con `random.Random(20261113)` y todos los scripts de los hallazgos); y aplicar ninguna de
las propuestas: lo que sea defecto lo arregla el operador o irá a una pieza posterior.

## 2. Diseño

**Método.** Partida del ZIP de V0.64 con sus 54 baterías en verde (0 con fallos; `salida_pruebas.txt`).
Recorrido de la Constitución V0.4 §0 a §16 requisito a requisito, con tres reglas: lo que la Constitución
deja para las Fases 2–5 va como FUERA DE FASE 1 y no cuenta como hallazgo; lo que depende del operador se
anota como decisión pendiente (D-xx, P-xx), no como defecto; y lo que ya está en la deuda no se repite:
se cita la fila (T-01, T-02, T-04, T-13, T-14, T-37, T-38, T-40, T-41, T-53, T-54, T-56, T-57, T-58,
D-02, D-03, D-05..D-11, D-18, D-20, D-29..D-34, P-02..P-24).

**La tabla.** Una fila por requisito verificable que afecta a la Fase 1, con seis columnas: § (sección y
párrafo), requisito (parafraseado con fidelidad), dónde (módulo · función), prueba (batería ·
comprobación), estado (CUMPLE, PARCIAL, FALTA, CONTRADICE, FUERA DE FASE 1) y nota. Donde una sección no
tiene requisitos verificables en el código (§0 en lo meta, §16 glosario, y varias reglas de gobernanza)
hay una fila de cortesía que lo dice. Resultado: **185 filas** — 91 CUMPLE, 48 PARCIAL, 20 FALTA,
1 CONTRADICE y 25 FUERA DE FASE 1. La única CONTRADICE (un mismo activo en dos carteras son dos
posiciones, contra G-06 de una posición por instrumento) ya está en la deuda como T-13 y no abre
hallazgo.

**Citas sin memoria.** Cada «dónde» y cada «prueba» se comprobaron abriendo el fichero, y no a mano: el
generador que viaja en la entrega (`entrega_glm/V0.65/generar_pasada.py`) contiene las 185 filas como
datos y, antes de escribir el Markdown, verifica con `ast` que cada función, clase o constante citada
existe en su módulo de `validador/` y que cada comprobación citada aparece en su batería de `pruebas/`;
si una sola cita no cuadra, no escribe nada y lista el fallo. Durante la pieza el verificador cazó cinco
citas mal (nombres de comprobación que venían de memoria), que se corrigieron antes de generar.

**Hallazgos.** Ocho, PC2-01 a PC2-08, cada uno con gravedad, la cita de la Constitución, la cita del
código, un script mínimo (`entrega_glm/V0.65/scripts/`, se ejecutan desde la carpeta `marcoC`) y una
propuesta (deuda T-6x, decisión del operador o enmienda de la Constitución):

1. **PC2-01 (media)** — El perfil inversor y la política de inversión personal no existen en SC-1
   (`mandatos.py` solo lleva mandatos por cartera). Propuesta: T-64.
2. **PC2-02 (media)** — F no controla la liquidez (el 5 % del volumen medio diario de D-27), el coste,
   el margen ni la exposición compartida por divisa/emisor/factor, y la política de F es una sola para
   las tres carteras (T-22 cerró con «Fuera: liquidez, costes, margen y límites por cartera» y nadie lo
   retomó). Propuesta: T-65.
3. **PC2-03 (media)** — Los contrapesos de la abstención de D-22 no existen: ni embudo visible en N ni
   alarma de sequía a 60 días (el seguimiento de lo descartado es de I, Fase 5). Propuesta: T-66.
4. **PC2-04 (media)** — La cartera sombra pasiva (D-22/D-27, «desde el primer día», contenido de la
   Fase 1) no existe; la comparación mensual es de I. Propuesta: T-67.
5. **PC2-05 (media)** — El posicionamiento de grandes inversores (COT de la CFTC, 13F, CNMV, directivos)
   falta en K y los cuatro registros comunes de D-23 no existen como almacenes consultables. Propuesta:
   T-68.
6. **PC2-06 (baja)** — SC-11 mínimo (Fase 1) y los lectores aislados no existen; lo bloquea la decisión
   del operador (P-24, que espera a P-05, según T-56). Sin deuda nueva.
7. **PC2-07 (baja)** — `methodology_version` (§13) no existe; el versionado real va por version_esquema,
   version_politica, VERSION_REGLAS, version_config y VERSION_PARAMETROS. Propuesta: enmienda de la §13
   (o añadir el campo a la envoltura).
8. **PC2-08 (baja)** — La envoltura de la §5 pide confianza e incertidumbre en todo mensaje y los
   contratos vigentes no las llevan como campos (CT-G-02 lleva incertidumbre y la confianza en su capa
   3; CT-G-01/03/08/14 no llevan ninguna; CT-G-03 y CT-G-14 sin resultado_politica; el registro marca
   todo «COMPLETA»). Propuesta: T-69.

Los ocho scripts dan **FALLA** con el código de V0.64 (salidas en `salida_pruebas.txt`), que es lo
esperado: demuestran que la divergencia sigue ahí.

## 3. Reglas y comprobaciones

No hay reglas ni códigos nuevos (no se cambia código). La tabla de la pasada es la comprobación: cada
fila de estado CUMPLE cita la batería y la comprobación que lo demuestra, y las de PARCIAL/FALTA citan
lo que sí hay. Los códigos que citan los hallazgos (O-xx, F-xx, CT-xx, PE-xx…) son los del catálogo de
V0.61 (`validador/catalogo_codigos.py`), sin ninguno nuevo.

## 4. Códigos, API, pruebas y revisión independiente

- **Funciones nuevas o cambiadas:** ninguna en `validador/` ni en `pruebas/`. Ficheros nuevos todos en
  `entrega_glm/V0.65/`: `pasada_coherencia.md` (el entregable), `generar_pasada.py` (el generador con
  el verificador de citas), `scripts/pc2_01..pc2_08` (ocho scripts de hallazgo) y las plantillas de
  siempre. Único fichero del marco modificado: `LEEME.md` (cabecera con la versión nueva, párrafo
  «Fecha: …» de esta pieza y punto «Comprobado en la pasada de coherencia»); no cambia nada del
  esquema del código ni de `MODULOS_ESQUEMA`.
- **Baterías:** no hay batería nueva; el lote completo (54 baterías) pasa sin tocar ninguna
  (`salida_pruebas.txt`, 0 con fallos). Los ocho scripts de hallazgo se ejecutan a mano y dan FALLA.
- **Defectos encontrados por la propia pieza:** cinco citas erróneas de la tabla detectadas por el
  verificador del generador (nombres de comprobación citados de memoria: `inv_V02_perfil_no_activo`,
  `reduccion_parcial_vuelve_a_abierta` con batería equivocada, `estado_sello_del_corte_vigente`,
  `colision_de_ids_ya_no_se_puede_crear` con batería equivocada y `registro_version_REG030` con batería
  equivocada); corregidas contra el fichero antes de generar. Además, el primer script de PC2-06 dio un
  falso OK: barría también las pruebas con la palabra «noticia» a secas, y la cazaba en el motivo que una
  prueba le pasa a H (`pruebas_orquestador.py:529`, «la tesis parece debilitada por una noticia», dentro
  de la batería de las propuestas de H) y los «lectores» de los comentarios de `pruebas_robustez_t03.py`;
  el docstring de H-16 no dice «noticia» (habla de «una invalidez por una métrica que no es el precio»).
  Se restringió el barrido a `validador/` con los patrones del servicio (SC-11, sc11,
  riesgos_geopoliticos, lectores de contenido) y volvió a dar FALLA. La atribución la corrigió la
  revisión independiente (hallazgo 1, ver `revision.md`); el fondo y la corrección técnica ya eran
  correctos.
- **Revisión independiente:** hecha el 10 de noviembre de 2026 (otra conversación): 20 filas al azar de
  la tabla con `random.Random(20261113)`, todos los scripts de los hallazgos, el lote completo de 54
  baterías repetido por el revisor, el documento regenerado y comparado byte a byte, y la búsqueda de
  requisitos de la Constitución que la tabla no recoja. Resultado: dos hallazgos documentales bajos, sin
  ninguno de producto, corregidos aquí: la atribución del falso OK de PC2-06 (párrafo anterior) y las
  filas §9.5 y §9.10, que la tabla saltaba (los puntos 5 y 10 de la §9 de la Constitución, ambos de
  aprendizaje fuera de la Fase 1; con ellos la tabla pasa de 183 a 185 filas). El detalle, en
  `revision.md`.

## 5. Límites y deuda técnica

- **Datos simulados.** Toda la pasada se apoya en el código y sus baterías: ningún sobre real de C-DIV
  (D-02) ha pasado por el sistema, así que las filas de CUMPLE demuestran lo que las baterías comprueban,
  no más.
- **La tabla no sustituye a la Constitución.** El parafraseo es fiel pero resumido; la revisión
  independiente debe leer la fila con la Constitución al lado.
- **Filas de deuda que propone** (`notas_deuda.md`): T-64 (perfil inversor en SC-1), T-65 (controles de
  F que T-22 dejó fuera), T-66 (embudo y sequía), T-67 (cartera sombra), T-68 (registros comunes y
  posicionamiento en K), T-69 (envoltura común al día con la §5). Ninguna fila de D nueva: lo que
  depende del operador ya tiene fila (P-02..P-24, T-56, T-57) o va a la enmienda (PC2-07, PC2-08).
- **Enmiendas propuestas a la Constitución** (para el §15, las ratifica el operador): §13
  (`methodology_version` frente al versionado real, PC2-07) y §5 (confianza/incertidumbre de la
  envoltura, PC2-08).
- Lo que esta pasada no puede decidir: el orden de la deuda nueva dentro de lo que queda de Fase 1; la
  propuesta de la pasada está en el resumen (cinco frentes: perfil inversor, controles de F, piezas que
  esperan al operador o a A/B/C, servicios sin empezar y detalles documentales).
