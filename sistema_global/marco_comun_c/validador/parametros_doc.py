"""Documentación de los valores por defecto como datos (T-83, V0.72; Constitución V0.6, §2 punto 4 y §9 punto 4, D-44 y D-45).

D-45: «todo parámetro tiene un valor por defecto prudente, válido para cualquier usuario y con su justificación escrita […];
cada parámetro nuevo de cualquier bloque llega con su valor por defecto y su pregunta del cuestionario». Este módulo da, para
cada clave de `parametros.PARAMETROS`, de `orquestador.CONFIG_DEFECTO` y de `control_f.POLITICA_DEFECTO` (la política de F,
que viaja dentro de `CONFIG_DEFECTO["politica_f"]`), y para cada campo de las claves compuestas de la configuración (las
subtablas de SUBTABLAS: `aprobacion`, `avisos`, `kill_switch`, `promocion_nivel`, y los campos del mandato y de la referencia
de cada cartera), un registro con:

- `estado`: `RATIFICADO` (una decisión ratificada de la Constitución fija ese valor), `PROPUESTO` (valor de partida que
  decidirá el operador en la sesión T-57) o `TECNICO` (no lo decide el operador y no lleva ningún número dentro);
- `fuente`: de dónde sale, con el documento delante para no confundir las decisiones de la Constitución con las de la tabla
  de pendientes de la deuda técnica (los comentarios del código mezclan las dos): «Constitución D-45», «Constitución P-17»,
  «Deuda D-29» (tabla de pendientes del operador), «Deuda T-75» (deuda técnica) o «V0.67» (Documento 0 de esa versión);
- `justificacion`: una o dos frases, por qué ese valor;
- `pregunta`: la pregunta en lenguaje sencillo que hará el cuestionario guiado del asesor de configuración (§2); obligatoria
  en `PROPUESTO` y en `RATIFICADO` (los cambios posteriores usan el mismo cuestionario, D-46), None en `TECNICO`, en una clave
  compuesta (sus campos llevan la suya) y en un `RATIFICADO` que la Constitución no deja cambiar todavía (`cerrada_por`);
- `valor_documentado`: el valor que justifican el texto y la pregunta (forma JSON: listas en lugar de tuplas). Si el código
  cambia el valor, `desfasados()` lo señala y hay que revisar el texto y actualizar `_VALOR_DOCUMENTADO` (QA r01, H-05);
- `detalle`: en una clave compuesta, la tabla o subtabla donde se documenta campo a campo (None en las demás);
- `cerrada_por`: en un `RATIFICADO` sin pregunta, la decisión de la Constitución que impide preguntarla (None en los demás).

Solo datos y consultas: no cambia ningún valor, no decide nada y no forma parte de la huella del esquema del código
(`persistencia.MODULOS_ESQUEMA`): corregir una redacción no debe exigir versión de esquema ni migración. La correspondencia con
los valores la vigilan `faltan()`, `desfasados()` y la batería `pruebas/pruebas_parametros_doc_t83.py`. Falla cerrado: `doc()`
lanza KeyError ante una clave sin documentar y ValueError ante una tabla desconocida o una clave ambigua; `faltan()` y
`preguntas_pendientes()` lanzan ValueError si las tablas no son las tres esperadas, y `preguntas_pendientes()` también si la
documentación y el código no cuadran; los registros son de solo lectura y las funciones devuelven copias.
"""
from __future__ import annotations

import copy
import json
import re
from types import MappingProxyType

VERSION_DOC = "PDOC-0.2.0"   # 0.2.0 (QA r01 de T-83): subtablas de las claves compuestas, valor documentado, cerrada_por
ESTADOS = ("RATIFICADO", "PROPUESTO", "TECNICO")
TABLAS = ("PARAMETROS", "CONFIG_DEFECTO", "POLITICA_DEFECTO")
# Subtabla -> (tabla, clave compuesta, forma). CAMPOS: un diccionario de campos fijos. POR_CARTERA: un diccionario por cartera,
# todos con los mismos campos; cada campo se documenta una vez y su valor es {cartera: valor}.
SUBTABLAS = {
    "CONFIG_DEFECTO.aprobacion": ("CONFIG_DEFECTO", "aprobacion", "CAMPOS"),
    "CONFIG_DEFECTO.avisos": ("CONFIG_DEFECTO", "avisos", "CAMPOS"),
    "CONFIG_DEFECTO.kill_switch": ("CONFIG_DEFECTO", "kill_switch", "CAMPOS"),
    "CONFIG_DEFECTO.promocion_nivel": ("CONFIG_DEFECTO", "promocion_nivel", "CAMPOS"),
    "CONFIG_DEFECTO.mandatos": ("CONFIG_DEFECTO", "mandatos", "POR_CARTERA"),
    "CONFIG_DEFECTO.referencias": ("CONFIG_DEFECTO", "referencias", "POR_CARTERA"),
}
TODAS = TABLAS + tuple(SUBTABLAS)
CAMPOS = ("estado", "fuente", "justificacion", "pregunta", "valor_documentado", "detalle", "cerrada_por")
RE_FUENTE = re.compile(r"(Constitución [DP]-\d{2}|Deuda [DT]-\d{2}|V0\.\d{2})\Z")

R, P, TEC = "RATIFICADO", "PROPUESTO", "TECNICO"


def _r(estado, fuente, justificacion, pregunta=None, cerrada_por=None):
    return {"estado": estado, "fuente": tuple(fuente), "justificacion": justificacion, "pregunta": pregunta,
            "detalle": None, "cerrada_por": cerrada_por}


def _compuesta(estado, fuente, detalle, justificacion):
    """Una clave compuesta: sin pregunta propia; sus valores se documentan en `detalle` y su estado es el de ellos (agregado)."""
    return {"estado": estado, "fuente": tuple(fuente), "justificacion": justificacion, "pregunta": None, "detalle": detalle,
            "cerrada_por": None}


_DOC = {
    # ------------------------------------------------------------------ parametros.PARAMETROS
    "PARAMETROS": {
        # K: calidad y antigüedad de los datos de corte
        "k_tope_antiguedad_dias_habiles": _r(P, ["Deuda T-25"],
            "Un dato de corte más viejo que esto ya no describe el mercado en el que se decide: un día hábil en trading y táctica y "
            "cinco en largo plazo, donde el precio de ayer pesa menos.",
            "¿Con qué antigüedad máxima aceptas los precios con los que se analiza cada cartera?"),
        "k_min_observaciones": _r(P, ["Deuda T-25"],
            "Con menos de 20 observaciones por fuente no hay serie suficiente para comprobar saltos y huecos; es un mínimo prudente, "
            "no un óptimo.",
            "¿Cuántos datos de precio como mínimo debe tener una serie para fiarse de ella?"),
        "k_rango_max_intradia": _r(P, ["Deuda T-25"],
            "Un máximo del día más de 1,5 veces el mínimo es casi siempre un error de datos en divisas, así que se bloquea antes de "
            "usarlo.",
            "¿A partir de qué diferencia entre el precio más alto y el más bajo de un día se considera que el dato está mal?"),
        "k_salto_adv_bloq": _r(P, ["Deuda T-25"],
            "Un salto de precio entre dos observaciones del 20 % avisa y del 50 % bloquea, salvo que un ajuste declarado lo explique: "
            "en divisas esos saltos casi siempre son errores.",
            "¿Qué salto de precio de un día a otro debe hacer dudar del dato, y cuál debe impedir usarlo?"),
        "k_hueco_adv_bloq": _r(P, ["Deuda T-25"],
            "Si faltan más del 2 % de los días hábiles se avisa y si faltan más del 10 % se bloquea: con muchos huecos los cálculos de "
            "riesgo salen optimistas.",
            "¿Cuántos días sin dato admites en una serie de precios antes de avisar y antes de rechazarla?"),
        "k_cruce_adv_bloq": _r(P, ["Deuda T-25"],
            "Los cruces de divisas deben cuadrar con sus dos pares: una desviación del 0,1 % avisa y del 1 % bloquea, porque delata "
            "un dato incoherente.",
            "¿Qué descuadre entre tipos de cambio relacionados admites antes de avisar y antes de rechazar los datos?"),
        "k_ventana_acumulado_obs": _r(P, ["Deuda T-25"],
            "El movimiento acumulado se mide en cinco observaciones, una semana hábil, para ver un error repartido en varios días "
            "que ningún salto diario delata.",
            "¿En cuántos días seguidos se vigila un movimiento de precio acumulado anómalo?"),
        "k_ajuste_tol_rel": _r(P, ["Deuda T-25"],
            "Un salto se da por explicado por un ajuste si coincide con su factor con un 10 % de margen; un margen menor rechazaría "
            "ajustes reales redondeados.",
            "¿Cuánto puede diferir un salto de precio del ajuste declarado, como un desdoblamiento o un dividendo, para darlo por "
            "explicado?"),
        "k_licencias_admitidas": _r(P, ["Deuda D-29", "Deuda T-26"],
            "Solo se usan datos propios, del intermediario para uso interno o con licencia abierta, para no depender de datos que no "
            "se pueden usar legalmente.",
            "¿Qué tipos de licencia de datos aceptas para los precios que usa el sistema?"),
        # D: comparación de candidatos
        "d_peso_evidencia": _r(P, ["Deuda T-25", "Deuda T-17"],
            "Al comparar candidatos, una cifra verificada cuenta entera, una estimada la mitad y una supuesta un cuarto: una tesis "
            "hecha de suposiciones no gana a una comprobada.",
            "Al comparar inversiones, ¿cuánto deben contar las cifras estimadas o supuestas frente a las comprobadas?"),
        "d_margen_ajustado": _r(P, ["Deuda T-21", "Deuda T-25"],
            "Si dos candidatos quedan a menos de un 5 % relativo, D no declara un claro ganador y lo dice: diferencias menores están "
            "dentro del error de las estimaciones.",
            "¿Qué ventaja mínima debe tener una inversión sobre otra para decir que es claramente mejor?"),
        "d_riesgo_min_pct": _r(P, ["Deuda T-21", "Deuda T-25"],
            "El riesgo por el que se divide la rentabilidad nunca baja del 1 %, para no premiar escenarios que dicen casi no poder "
            "perder.",
            "¿Qué riesgo mínimo se supone siempre en una inversión, aunque su análisis diga que casi no puede perder?"),
        "d_tope_confianza_clase": _r(P, ["Deuda D-03", "Constitución P-15"],
            "La confianza máxima depende de lo comparable que sea el activo: 0,80 en la clase Q, 0,60 en la S y 0,40 en la K, porque "
            "cuanto menos comparable, menos se puede verificar.",
            "¿Cuánta confianza máxima se puede dar al análisis de cada tipo de activo según lo fácil que sea compararlo con otros?"),
        "d_exceso_min_pct": _r(P, ["Deuda T-21"],
            "Un candidato debe superar a la referencia de no hacer nada en al menos 0,10 puntos; si no, D se abstiene, porque no "
            "compensa el riesgo de equivocarse.",
            "¿Cuánto debe superar una inversión a no hacer nada para que valga la pena?"),
        "d_rentabilidad_plausible_pct": _r(P, ["Deuda T-21"],
            "Una rentabilidad neta fuera del intervalo de −100 % a 500 % es casi seguro un error de quien la declara; se excluye en "
            "lugar de dejar que gane la comparación.",
            "¿Qué rentabilidad esperada es tan extrema que hay que tratarla como un error?"),
        "d_referencia_rango_pct": _r(P, ["Deuda D-17", "Deuda T-37"],
            "La rentabilidad anual de la referencia de una cartera debe estar entre −5 % y 50 %; fuera de ese rango la referencia "
            "está mal configurada.",
            "¿Qué rentabilidad anual es razonable para la referencia con la que se compara cada cartera?"),
        "d_coste_suelo_ida_vuelta_pb": _r(P, ["Deuda D-30", "Deuda T-17"],
            "Si un análisis declara costes de entrar y salir por debajo de 2, 10 o 30 puntos básicos según la clase, D descuenta "
            "este mínimo: nadie gana la comparación declarando costes irreales.",
            "¿Qué coste mínimo de comprar y vender se supone siempre, aunque el análisis diga que será menor?"),
        "d_coste_suelo_mant_anual_pb": _r(P, ["Deuda D-30", "Deuda T-17"],
            "En divisas al contado mantener una posición no tiene un coste anual mínimo seguro, así que el suelo es cero hasta tener "
            "los costes del intermediario.",
            "¿Qué coste anual mínimo de mantener una inversión se supone siempre?"),
        "d_factor_tope_sin_doble_analisis": _r(P, ["Deuda D-30", "Deuda D-03", "Deuda T-17"],
            "Sin un segundo análisis que confirme el primero, la confianza no pasa del 75 % del tope de su clase, igual que cuando "
            "los dos análisis discrepan.",
            "¿Cuánta confianza se quita a un análisis que nadie ha confirmado con un segundo análisis independiente?"),
        "d_riesgo_sin_stop_largo_pct": _r(P, ["Deuda D-30", "Deuda T-17"],
            "Una compra sin una orden de protección legible puede perderlo todo, así que D le cuenta un riesgo del 100 %.",
            "Si una compra no tiene una orden de protección clara, ¿qué pérdida máxima se le supone?"),
        # H: vigilancia
        "h_max_edad_dato_min": _r(P, ["Deuda T-25", "Deuda T-49"],
            "El vigilante solo actúa sobre una posición con datos de menos de 15 minutos; con datos más viejos podría cerrar o "
            "mantener por un precio que ya no existe.",
            "¿Con qué antigüedad máxima del precio puede el vigilante actuar sobre una inversión abierta?"),
        "h_salto_max_horas": _r(P, ["Deuda T-25", "Deuda T-03"],
            "Si entre dos revisiones pasan más de 72 horas, más que un fin de semana largo, el instante recibido se trata como "
            "sospechoso en lugar de darlo por bueno.",
            "¿Cuánto tiempo sin revisar las posiciones se considera tan anómalo que hay que desconfiar de la hora recibida?"),
        # E y el Orquestador
        "e_max_edad_dimensionado_min": _r(P, ["Deuda T-16", "Deuda T-25"],
            "El cálculo del tamaño de la posición no puede tener más de 60 minutos al proponer: el precio y la cartera cambian y el "
            "tamaño dejaría de ser el correcto.",
            "¿Cuánto tiempo puede pasar entre calcular el tamaño de una inversión y proponértela?"),
        # CT-G-14: declaración manual
        "manual_ventana_declaracion_horas": _r(P, ["Deuda D-20", "Constitución P-13"],
            "Lo que hagas a mano en el intermediario debe declararse en 72 horas; pasado el plazo cuenta como discrepancia, porque el "
            "sistema ya no puede explicar la diferencia.",
            "¿Cuánto tiempo tienes para declarar una operación que hiciste a mano fuera del sistema?"),
        # N: consola
        "n_lineas_diario_ambar": _r(P, ["V0.67", "Deuda T-83"],
            "Con más de 1.000 líneas del diario sin punto de control el panel avisa en ámbar: recuperar el estado tras un fallo se "
            "vuelve lento.",
            "¿Cuántas anotaciones sin copia intermedia del estado admite el diario antes de avisarte?"),
        "o_max_analisis_consulta": _r(P, ["Deuda T-80"],
            "Una consulta puede citar hasta 50 análisis, para que su rastro no crezca sin límite; es holgado para comparar los "
            "candidatos de una cartera.",
            "¿Cuántos análisis como máximo puede reunir una consulta que no acaba en una decisión?"),
        "o_dias_sequia": _r(R, ["Constitución D-22", "Constitución D-27", "Constitución P-17", "Deuda T-75"],
            "La Constitución fija la alarma de sequía a los 60 días: si nada se invierte habiendo candidatos que pasaron el análisis, "
            "se avisa para que el control no impida invertir sin que lo sepas.",
            "¿Tras cuántos días sin invertir nada, habiendo candidatos aprobados, quieres que te avise?"),
        "n_dias_embudo": _r(R, ["Constitución D-22", "Deuda T-75"],
            "La Constitución pide que la consola muestre el embudo de oportunidades cada semana.",
            "¿Cada cuántos días quieres ver el resumen de oportunidades y dónde se quedó cada una?"),
        # I: cartera sombra pasiva
        "i_meses_juicio_sombra": _r(R, ["Constitución D-27", "Constitución P-18", "Deuda T-76"],
            "La Constitución juzga al robot frente a la cartera sombra a los 24 meses: antes, la suerte pesa más que la habilidad.",
            "¿Tras cuántos meses se juzga si el robot ha superado a una inversión pasiva en un índice?"),
        "i_indice_sombra": _r(P, ["Constitución D-27", "Deuda T-76"],
            "La Constitución fija un índice mundial como plan pasivo; cuál exactamente lo decide el operador, y aquí solo está su "
            "nombre provisional.",
            "¿Qué índice mundial quieres usar como inversión pasiva con la que comparar al robot?"),
        "i_coste_anual_sombra_pct": _r(P, ["Deuda T-76"],
            "Un fondo indexado mundial barato cuesta en torno al 0,20 % al año; restarlo a la sombra hace justa la comparación con "
            "el robot.",
            "¿Qué coste anual tiene el fondo indexado con el que se compara al robot?"),
    },
    # ------------------------------------------------------------------ orquestador.CONFIG_DEFECTO
    "CONFIG_DEFECTO": {
        "max_reintentos": _r(P, ["Deuda D-05"],
            "Tras tres encargos a C sin avance el Orquestador deja de reintentar y avisa al operador: más intentos gastan presupuesto "
            "en algo que no sale.",
            "¿Cuántas veces se reintenta un análisis que no avanza antes de avisarte?"),
        "umbral_corte_comun_dias_habiles": _r(P, ["Deuda D-05", "Constitución P-13"],
            "Los análisis que se comparan deben tener la misma fecha de corte: comparar datos de días distintos favorece al que se "
            "hizo con más información.",
            "¿Cuántos días de diferencia admites entre las fechas de los datos de dos análisis que se comparan?"),
        "version_config": _r(TEC, ["Deuda T-25"],
            "Identifica la versión de esta configuración en la huella de cada decisión; la cambia el código, no el operador."),
        "dia_coste_max_eur": _r(P, ["Deuda D-05", "Constitución P-07"],
            "Tope de 50 € al día en análisis: un límite bajo mientras todo es simulado, que impide que un error dispare el gasto.",
            "¿Cuánto dinero al día como máximo puede gastar el sistema en análisis?"),
        "revision_max_dias": _r(P, ["Deuda D-22"],
            "Al confirmar una tesis, la nueva fecha de revisión no puede estar a más de 90 días: ninguna posición pasa más de un "
            "trimestre sin que alguien la vuelva a mirar.",
            "¿Cuánto tiempo como máximo puede pasar sin revisar una inversión abierta?"),
        "observacion_max_dias": _r(P, ["Deuda D-23"],
            "Una oportunidad en observación caduca a los 30 días: un mes basta para que se cumpla la condición que se esperaba.",
            "¿Cuánto tiempo como máximo se vigila una oportunidad aparcada antes de olvidarla?"),
        "max_reaperturas": _r(P, ["Deuda D-23"],
            "Un expediente se puede reabrir dos veces sin el operador; después decide él, para que una oportunidad que no cuaja no se "
            "repita sin fin.",
            "¿Cuántas veces puede el sistema reabrir por su cuenta una oportunidad aparcada?"),
        "dia_tiempo_max_min": _r(P, ["Deuda D-05", "Constitución P-07"],
            "Tope de 600 minutos de análisis al día: acota el trabajo de los agentes y obliga a priorizar.",
            "¿Cuánto tiempo de análisis al día como máximo puede usar el sistema?"),
        "tolerancia_precio_entrada": _r(P, ["Deuda D-05"],
            "Una ejecución a más de un 5 % del precio límite propuesto no se da por buena: el precio ya no es el que se autorizó.",
            "¿Cuánto puede alejarse el precio real de compra del precio que autorizaste?"),
        "alerta_perdida_pct": _r(P, ["Deuda D-26", "Deuda T-49"],
            "Con una pérdida no realizada del 5 %, y otra vez en cada múltiplo, el vigilante pide revisar la posición: es pronto para "
            "un susto y tarde para no mirar.",
            "¿Con qué pérdida de una inversión quieres que el sistema pida revisarla?"),
        "anulaciones_veto_mes": _r(P, ["Deuda D-27", "Deuda T-50"],
            "El operador puede anular como mucho dos vetos de F al mes, con motivo: más anulaciones indicarían que los límites están "
            "mal o que se están saltando.",
            "¿Cuántas veces al mes puedes saltarte un veto del control de riesgo?"),
        "tolerancia_tipo_k_rel": _r(P, ["Deuda D-29", "Deuda T-42"],
            "El tipo de cambio del intermediario no puede desviarse más de un 3 % del último cierre de la fuente de datos: más allá, "
            "uno de los dos está mal.",
            "¿Qué diferencia admites entre el tipo de cambio de tu intermediario y el de la fuente de datos?"),
        "exige_contradictor_en": _r(P, ["Deuda D-25", "Deuda D-06", "Constitución D-35", "Deuda T-48"],
            "La Constitución exige varios análisis independientes siempre en N3; se propone exigir también el Contradictor en N2, "
            "donde ya se compara y se propone.",
            "Además de en N3, donde la Constitución pide siempre varios análisis, ¿quieres que un revisor independiente busque "
            "fallos en N2?"),
        "contradictor_desactivado_motivo": _r(TEC, ["Deuda T-48"],
            "Solo se rellena, con su motivo, si se deja de exigir el Contradictor en algún nivel; por defecto se exige y queda vacío."),
        "autoria_c": _r(P, ["Deuda D-25", "Deuda T-48"],
            "Sin declarar qué modelo y qué proveedor hacen cada análisis no se puede comprobar que el revisor sea distinto; queda "
            "vacío y cada informe lo avisa.",
            "¿Qué modelo y qué proveedor de inteligencia artificial hacen los análisis de cada tipo de activo?"),
        "autoria_contradictor": _r(P, ["Deuda D-25", "Deuda D-06", "Deuda T-48"],
            "Vacío hasta que se elija el modelo del Contradictor; sin él la diversidad no se comprueba y se avisa.",
            "¿Qué modelo y qué proveedor de inteligencia artificial hacen de revisor independiente?"),
        "matriz_autonomia": _r(P, ["Deuda D-05", "Constitución P-01"],
            "Vacía: la matriz no autoriza nada sola en ninguna cartera y todo lo autoriza el operador, que es lo prudente en simulado.",
            "¿En qué carteras puede el sistema autorizar inversiones sin preguntarte?"),
        "politica_f": _compuesta(P, ["Deuda T-22"], "POLITICA_DEFECTO",
            "Contenedor de los límites de F: cada uno se documenta por separado en la tabla de la política de F."),
        "nivel_autonomia": _r(R, ["Constitución D-45", "Deuda D-16"],
            "Sin dato, cada cartera está en L1, donde el sistema propone y el operador decide: es el valor por defecto ratificado "
            "para cualquier copia nueva.",
            "¿Qué nivel de autonomía quieres para cada cartera?"),
        "tolerancia_conciliacion_rel": _r(P, ["Deuda D-20", "Constitución P-13"],
            "Lo que dice el intermediario y lo que registra el sistema deben cuadrar exactamente: cualquier diferencia se investiga.",
            "¿Qué diferencia admites entre lo que dice tu intermediario y lo que registra el sistema?"),
        "umbral_l2_eur": _r(P, ["Deuda D-33", "Constitución P-01", "Deuda T-18"],
            "En L2 la matriz solo abre sola órdenes de hasta 5.000 € por cartera; por encima decide el operador.",
            "¿Hasta qué importe por orden puede el sistema invertir solo en las carteras a las que des autonomía?"),
        "promocion_nivel": _compuesta(P, ["Deuda D-34", "Deuda T-18"], "CONFIG_DEFECTO.promocion_nivel",
            "Condiciones para subir de nivel de autonomía; cada una se documenta en su subtabla."),
        "libres_tope_dia_eur": _r(P, ["Deuda D-32", "Deuda T-33"],
            "Las operaciones libres declaradas fuera del sistema no pasan de 2.000 € por cartera y día, para que no esquiven los "
            "controles.",
            "¿Cuánto puedes invertir al día por tu cuenta en cada cartera fuera de las propuestas del sistema?"),
        "mandatos": _compuesta(P, ["Deuda D-28", "Constitución P-03", "Deuda T-51"], "CONFIG_DEFECTO.mandatos",
            "Mandato de cada cartera en SC-1; cada campo (referencia, horizonte, apalancamiento, tamaño, instrumentos y exclusiones) "
            "se documenta en su subtabla."),
        "referencias": _compuesta(P, ["Deuda D-17", "Constitución P-03", "Deuda T-37"], "CONFIG_DEFECTO.referencias",
            "Referencia de cada cartera con la que D compara no hacer nada; sus dos campos se documentan en su subtabla."),
        "aprobacion": _compuesta(P, ["Deuda D-18", "Deuda D-19", "Constitución P-08", "Constitución P-12"], "CONFIG_DEFECTO.aprobacion",
            "Condiciones con las que el operador aprueba una operación; cada una se documenta en su subtabla."),
        "avisos": _compuesta(P, ["Deuda D-07", "Deuda D-19", "Constitución P-08", "Deuda T-41"], "CONFIG_DEFECTO.avisos",
            "Canales y repeticiones de los avisos; cada valor se documenta en su subtabla."),
        "kill_switch": _compuesta(P, ["Deuda D-19"], "CONFIG_DEFECTO.kill_switch",
            "Rehabilitación tras una parada de emergencia; su valor se documenta en su subtabla."),
        "divisas_cotizacion": _r(TEC, ["Deuda T-10"],
            "Tabla de los instrumentos que no son un par de divisas ISO y de la divisa en que cotizan; vacía, porque en la Fase 1 "
            "todo son pares y la divisa sale del nombre."),
        "rangos_tipo_cambio_eur": _r(P, ["Deuda D-21", "Deuda T-10"],
            "Un tipo de cambio fuera de su rango plausible se rechaza: protege de un dato erróneo que cambiaría el tamaño de las "
            "posiciones, y los rangos son anchos para no rechazar datos buenos.",
            "¿Te vale el rango recomendado de tipos de cambio de cada divisa, que solo sirve para descartar datos erróneos?"),
        "tolerancia_tipo_par_pct": _r(P, ["Deuda D-21"],
            "El tipo de cambio de la cartera y el que implica el precio de un par con el euro no pueden diferir más de un 15 %: "
            "holgado para no rechazar datos buenos y estrecho para ver errores.",
            "¿Qué diferencia admites entre el tipo de cambio de tu cartera y el que implica el precio de la operación?"),
        "cuenta_intermediario": _r(P, ["Deuda D-21", "Constitución P-05"],
            "Cuenta simulada mientras no haya un intermediario real elegido.",
            "¿Qué cuenta de tu intermediario debe usar el sistema?"),
    },
    # ------------------------------------------------------------------ control_f.POLITICA_DEFECTO (CONFIG_DEFECTO["politica_f"])
    "POLITICA_DEFECTO": {
        "riesgo_max_pct": _r(P, ["Deuda D-01"],
            "Una orden no puede arriesgar más del 1 % del capital hasta su stop: una racha de pérdidas no hunde la cartera.",
            "¿Qué parte de tu capital estás dispuesto a perder como mucho en una sola operación?"),
        "tamano_max_pct": _r(P, ["Deuda D-01"],
            "Ninguna posición pasa del 10 % del capital: es la diversificación mínima.",
            "¿Qué parte de tu capital puede ir como mucho a una sola inversión?"),
        "exposicion_max_pct": _r(P, ["Deuda D-01", "Constitución D-16", "Constitución D-45"],
            "La exposición total no supera el capital, porque la Constitución no deja invertir con dinero prestado hasta la Fase 3; "
            "el operador puede bajarla, no subirla.",
            "¿Qué parte de tu capital, como mucho el total, puede estar invertida a la vez?"),
        "concentracion_max_pct": _r(P, ["Deuda D-01"],
            "Lo invertido en un mismo activo, sumando todas sus posiciones, no pasa del 20 % del capital.",
            "¿Cuánto de tu capital puede acumularse en un mismo activo?"),
        "perdida_dia_max_pct": _r(P, ["Deuda D-01", "Deuda T-50"],
            "Si en el día se pierde el 2 % del capital, no se abren más posiciones ese día: frena la tentación de recuperar.",
            "¿Qué pérdida en un día, como parte de tu capital, debe parar las operaciones nuevas hasta el día siguiente?"),
        "max_posiciones": _r(P, ["Deuda D-01"],
            "Como mucho diez posiciones abiertas a la vez: más no se pueden vigilar bien cuando el operador decide cada una.",
            "¿Cuántas inversiones abiertas a la vez quieres como máximo?"),
        "apalancamiento_max": _r(R, ["Constitución D-16", "Constitución D-45", "Deuda D-12"],
            "Un 1 significa sin apalancamiento: la Constitución no habilita el apalancamiento hasta que el operador lo decida, no "
            "antes de la Fase 3 (D-16), y lo pone entre los valores por defecto de cualquier copia (D-45, y el §7: «inicialmente "
            "cero»).",
            None, cerrada_por="Constitución D-16"),
        "frescura_max_min": _r(P, ["Deuda D-01"],
            "F no decide con una foto de la cartera de más de 60 minutos: el capital y las posiciones pueden haber cambiado.",
            "¿Con qué antigüedad máxima de la información de tu cartera puede decidir el control de riesgo?"),
        "valor_min_eur": _r(P, ["Deuda D-01"],
            "No se aprueban órdenes de menos de 100 €: los costes fijos se comerían la operación.",
            "¿Cuál es el importe mínimo de una operación que vale la pena hacer?"),
        "vigencia_max_horas": _r(P, ["Deuda D-01"],
            "Un informe de F vale como mucho 24 horas: después hay que volver a controlar con datos nuevos.",
            "¿Cuánto tiempo vale el visto bueno del control de riesgo antes de repetirlo?"),
        "importe_max_orden_eur": _r(P, ["Deuda D-11", "Constitución P-11", "Deuda T-22"],
            "Ninguna orden pasa de 20.000 €: un límite nominal duro que no depende de que el capital esté bien calculado.",
            "¿Cuánto dinero como máximo quieres en una sola orden?"),
        "importe_max_dia_eur": _r(P, ["Deuda D-11", "Constitución P-11", "Deuda T-22"],
            "Las órdenes de un día no suman más de 50.000 €: un fallo que se repita no puede invertir todo de golpe.",
            "¿Cuánto dinero como máximo quieres en órdenes en un mismo día?"),
        "importe_max_activo_eur": _r(P, ["Deuda D-11", "Constitución P-11", "Deuda T-22"],
            "En un mismo activo no se acumulan más de 30.000 €, aunque el porcentaje del capital lo permitiera.",
            "¿Cuánto dinero como máximo quieres en un mismo activo?"),
        "perdida_dia_max_eur": _r(P, ["Deuda D-11", "Constitución P-11", "Deuda T-22"],
            "Con 2.500 € perdidos en el día no se abren más posiciones: el límite en euros complementa al porcentual.",
            "¿Qué pérdida en euros en un día debe frenar las operaciones nuevas?"),
        "perdida_semana_max_eur": _r(P, ["Deuda D-11", "Constitución P-11", "Deuda T-22"],
            "Con 5.000 € perdidos en la semana no se abren más posiciones: varias malas jornadas seguidas también frenan.",
            "¿Qué pérdida en euros en una semana debe frenar las operaciones nuevas?"),
        "ordenes_max_hora": _r(P, ["Deuda D-11", "Constitución P-11", "Deuda T-22"],
            "Como mucho diez órdenes por hora: frena un fallo que envíe órdenes en bucle.",
            "¿Cuántas órdenes por hora quieres permitir como máximo?"),
        "evidencia_verificada_min": _r(P, ["Deuda D-31", "Deuda T-22"],
            "Al menos el 5 % de las cifras del análisis deben estar verificadas: una tesis hecha solo de estimaciones no pasa.",
            "¿Qué parte mínima de las cifras de un análisis debe estar comprobada para invertir?"),
        "corte_max_dias": _r(P, ["Deuda D-31", "Deuda T-22"],
            "Los datos del análisis no pueden tener más de tres días al autorizar: el mercado ya sería otro.",
            "¿Cuántos días pueden tener como mucho los datos de un análisis al autorizar la inversión?"),
        "ventana_eventos_dias": _r(P, ["Deuda D-31", "Deuda T-22"],
            "No se abre el día de una reunión de un banco central o de unos resultados ni el día anterior: el movimiento del anuncio "
            "no es el que se analizó.",
            "¿Cuántos días antes de un anuncio importante se evita abrir inversiones?"),
        "viernes_corte_utc_h": _r(P, ["Deuda D-31", "Deuda T-22"],
            "No se abre desde el viernes a las 20:00 UTC ni en fin de semana: el mercado cierra y no se podría salir.",
            "¿Desde qué hora del viernes se dejan de abrir inversiones hasta el lunes?"),
        "deriva_precio_max_pct": _r(P, ["Deuda D-31", "Deuda T-22"],
            "El límite de la orden no puede alejarse más de un 2 % del precio del intermediario: el análisis se hizo con otro precio.",
            "¿Cuánto puede haberse movido el precio desde el análisis para seguir adelante con la orden?"),
        "precio_frescura_max_min": _r(P, ["Deuda D-31", "Deuda T-22"],
            "El precio del intermediario con el que se comprueba la orden no puede tener más de 15 minutos.",
            "¿Qué antigüedad máxima puede tener el precio de mercado con el que se comprueba la orden?"),
    },
    # ------------------------------------------------------------------ subtablas de las claves compuestas (QA r01, H-02)
    "CONFIG_DEFECTO.aprobacion": {
        "caduca_min": _r(P, ["Deuda D-18"],
            "Una propuesta caduca 15 minutos después de que se pueda aprobar, tras la espera si la hay: pasado ese tiempo el precio "
            "ya no es el que se propuso.",
            "¿Cuánto tiempo tienes para aprobar una operación antes de que caduque?"),
        "canales": _r(P, ["Deuda D-19", "Constitución P-08"],
            "Solo vale una aprobación desde la consola y con segundo factor; el chat nunca vale, porque cualquiera podría escribir en "
            "él.",
            "¿Desde qué canal quieres aprobar las operaciones, siempre con un segundo factor de confirmación?"),
        "enfriamiento_min": _r(P, ["Deuda D-18"],
            "Tras una pérdida en el día o fuera del horario hay que esperar 30 minutos antes de aprobar: la prisa y el cansancio "
            "llevan a malas decisiones.",
            "¿Cuánto tiempo debes esperar para aprobar después de una pérdida en el día o fuera de tu horario?"),
        "enfriamiento_tras_perdida_dia_eur": _r(P, ["Deuda D-18"],
            "Cualquier pérdida del día, por pequeña que sea, activa la espera antes de aprobar: es el umbral más prudente.",
            "¿A partir de qué pérdida en el día quieres que se active esa espera antes de aprobar?"),
        "horario_utc": _r(P, ["Deuda D-18", "Deuda D-33", "Constitución P-12"],
            "Fuera de 07:00 a 21:00 UTC no se prohíbe aprobar, pero hay que esperar 30 minutos, y una cartera en L3 actúa como en L2: "
            "fuera de las horas en que atiendes el sistema se decide peor.",
            "¿En qué horario sueles poder atender el sistema para aprobar sin espera?"),
    },
    "CONFIG_DEFECTO.avisos": {
        "canal_alta": _r(P, ["Deuda D-07", "Deuda D-19", "Constitución P-08"],
            "Los avisos de prioridad alta van a la consola mientras no haya otro canal fuera del chat.",
            "¿Por dónde quieres recibir los avisos importantes?"),
        "canal_escalado": _r(P, ["Deuda D-07", "Deuda D-19", "Constitución P-08"],
            "Un aviso que no se acusa pasa a un canal distinto del habitual, para que no se pierda si no miras la consola.",
            "¿A qué otro canal o persona debe pasar un aviso importante que no atiendes?"),
        "reiterar_min": _r(P, ["Deuda D-07", "Deuda T-41"],
            "Un aviso sin acusar se repite cada 15 minutos.",
            "¿Cada cuántos minutos debe repetirse un aviso que no has atendido?"),
        "escalar_tras": _r(P, ["Deuda D-07", "Deuda T-41"],
            "Tras tres repeticiones sin acuse el aviso se escala: casi una hora sin respuesta es demasiado para un aviso importante.",
            "¿Tras cuántas repeticiones sin respuesta debe escalarse un aviso?"),
    },
    "CONFIG_DEFECTO.kill_switch": {
        "periodo_min_l1_horas": _r(P, ["Deuda D-19"],
            "Tras una parada de emergencia la cartera pasa al menos 24 horas en L1 antes de volver a subir: un día para entender qué "
            "pasó.",
            "Después de una parada de emergencia, ¿cuánto tiempo debe pasar antes de devolver autonomía al sistema?"),
    },
    "CONFIG_DEFECTO.promocion_nivel": {
        "periodo_min_dias": _r(P, ["Deuda D-34", "Constitución P-02", "Deuda T-18"],
            "Para subir de nivel hacen falta 30 días en el nivel actual sin incidentes: un mes es el mínimo para ver cómo se "
            "comporta una cartera.",
            "¿Cuánto tiempo sin incidentes debe pasar antes de dar más autonomía a una cartera?"),
    },
    "CONFIG_DEFECTO.mandatos": {
        "version": _r(TEC, ["Deuda T-51"],
            "Versión del mandato de cada cartera, para la huella de cada decisión; la cambia quien cambia el mandato."),
        "benchmark_ref": _r(P, ["Deuda D-28", "Deuda D-17", "Constitución P-03"],
            "El efectivo es un marcador hasta que se fije la referencia de cada cartera (T-37): la Constitución (§7) pide un índice "
            "o una cesta en la que se invierte de verdad, y efectivo solo si el operador lo elige.",
            "¿Con qué índice o cesta quieres comparar cada cartera, en la que se invierta de verdad cuando no haya nada mejor?"),
        "horizonte_dias": _r(P, ["Deuda D-28", "Constitución P-04"],
            "El plazo de cada cartera es el de su clase: de 1 a 28 días en trading, de 14 a 183 en táctica y de 1.095 a 7.300 "
            "(de 3 a 20 años) en largo plazo.",
            "¿Qué plazo quieres para las inversiones de cada cartera?"),
        "apalancamiento_max": _r(R, ["Constitución D-16", "Constitución D-45", "Deuda D-28"],
            "Un 1 significa sin apalancamiento en el mandato de cada cartera: la Constitución no lo habilita antes de la Fase 3 "
            "(D-16) y en el §7 lo deja «inicialmente cero».",
            None, cerrada_por="Constitución D-16"),
        "tamano_max_pct_cartera": _r(P, ["Deuda D-28"],
            "Ninguna posición pasa del 10 % de su cartera: es la diversificación mínima dentro de cada una.",
            "¿Qué parte de cada cartera puede ir como mucho a una sola inversión?"),
        "instrumentos_permitidos": _r(P, ["Deuda D-28", "Constitución D-16"],
            "Sin lista, cada cartera admite cualquier instrumento del universo que el sistema analiza; derivados y CFD siguen "
            "cerrados por la Constitución hasta la Fase 3, así que una lista solo puede restringir.",
            "¿Quieres limitar alguna cartera a una lista de instrumentos concretos?"),
        "exclusiones": _r(P, ["Deuda D-28"],
            "Sin exclusiones de partida: son preferencias personales del operador y no hay ninguna prudente para cualquier usuario.",
            "¿Hay activos, sectores o países en los que no quieras invertir nunca?"),
    },
    "CONFIG_DEFECTO.referencias": {
        "benchmark_ref": _r(TEC, ["Deuda D-17", "Deuda T-51"],
            "Copia del benchmark del mandato de cada cartera: la configuración exige que coincidan, y se pregunta en el mandato."),
        "rentabilidad_anual_pct": _r(P, ["Deuda D-17", "Deuda T-37"],
            "No es un valor prudente sino un marcador: con efectivo al 0 % casi todo supera a la referencia y D se abstiene poco, "
            "por eso T-37 la traerá de los datos y el §7 de la Constitución pide un índice real.",
            "¿Qué rentabilidad anual quieres suponer a la referencia de cada cartera mientras no se calcule con datos reales?"),
    },
}

# El valor que justifica cada registro (forma JSON), para que un valor cambiado no deje un texto falso sin aviso (H-05). Al cambiar
# un valor del código: revisar su justificación y su pregunta, y actualizarlo aquí. Las claves compuestas no lo llevan: lo
# llevan sus campos.
_VALOR_DOCUMENTADO = {
    "PARAMETROS": {
        "k_tope_antiguedad_dias_habiles": {"TRADING": 1, "TACTICA": 1, "LARGO_PLAZO": 5},
        "k_min_observaciones": 20,
        "k_rango_max_intradia": 1.5,
        "k_salto_adv_bloq": [0.2, 0.5],
        "k_hueco_adv_bloq": [0.02, 0.1],
        "k_cruce_adv_bloq": [0.001, 0.01],
        "k_ventana_acumulado_obs": 5,
        "k_ajuste_tol_rel": 0.1,
        "k_licencias_admitidas": ["PROPIA", "INTERMEDIARIO-USO-INTERNO", "CC-BY-4.0", "DOMINIO-PUBLICO"],
        "d_peso_evidencia": {"VERIFICADO": 1.0, "ESTIMADO": 0.5, "SUPUESTO": 0.25},
        "d_margen_ajustado": 0.05,
        "d_riesgo_min_pct": 1.0,
        "d_tope_confianza_clase": {"Q": 0.8, "S": 0.6, "K": 0.4},
        "d_exceso_min_pct": 0.1,
        "d_rentabilidad_plausible_pct": [-100.0, 500.0],
        "d_referencia_rango_pct": [-5.0, 50.0],
        "d_coste_suelo_ida_vuelta_pb": {"Q": 2.0, "S": 10.0, "K": 30.0},
        "d_coste_suelo_mant_anual_pb": {"Q": 0.0, "S": 0.0, "K": 0.0},
        "d_factor_tope_sin_doble_analisis": 0.75,
        "d_riesgo_sin_stop_largo_pct": 100.0,
        "h_max_edad_dato_min": 15,
        "h_salto_max_horas": 72,
        "e_max_edad_dimensionado_min": 60,
        "manual_ventana_declaracion_horas": 72,
        "n_lineas_diario_ambar": 1000,
        "o_max_analisis_consulta": 50,
        "o_dias_sequia": 60,
        "n_dias_embudo": 7,
        "i_meses_juicio_sombra": 24,
        "i_indice_sombra": "INDICE-MUNDIAL",
        "i_coste_anual_sombra_pct": 0.2,
    },
    "CONFIG_DEFECTO": {
        "max_reintentos": 3,
        "umbral_corte_comun_dias_habiles": 0,
        "version_config": "CFG-0.11.0",
        "dia_coste_max_eur": 50.0,
        "revision_max_dias": 90,
        "observacion_max_dias": 30,
        "max_reaperturas": 2,
        "dia_tiempo_max_min": 600,
        "tolerancia_precio_entrada": 0.05,
        "alerta_perdida_pct": -5.0,
        "anulaciones_veto_mes": 2,
        "tolerancia_tipo_k_rel": 0.03,
        "exige_contradictor_en": ["N2", "N3"],
        "contradictor_desactivado_motivo": None,
        "autoria_c": {},
        "autoria_contradictor": None,
        "matriz_autonomia": {},
        "nivel_autonomia": {},
        "tolerancia_conciliacion_rel": 0.0,
        "umbral_l2_eur": {"TRADING": 5000.0, "TACTICA": 5000.0, "LARGO_PLAZO": 5000.0},
        "libres_tope_dia_eur": {"TRADING": 2000.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0},
        "divisas_cotizacion": {},
        "rangos_tipo_cambio_eur": {"USD": [0.6, 1.4], "GBP": [0.9, 1.6], "JPY": [0.003, 0.015], "CHF": [0.7, 1.4], "AUD": [0.4, 0.9],
                                   "CAD": [0.45, 0.95], "SEK": [0.06, 0.13], "NOK": [0.06, 0.13], "DKK": [0.12, 0.15]},
        "tolerancia_tipo_par_pct": 15.0,
        "cuenta_intermediario": "SIM-1",
    },
    "POLITICA_DEFECTO": {
        "riesgo_max_pct": 1.0,
        "tamano_max_pct": 10.0,
        "exposicion_max_pct": 100.0,
        "concentracion_max_pct": 20.0,
        "perdida_dia_max_pct": 2.0,
        "max_posiciones": 10,
        "apalancamiento_max": 1.0,
        "frescura_max_min": 60.0,
        "valor_min_eur": 100.0,
        "vigencia_max_horas": 24.0,
        "importe_max_orden_eur": 20000.0,
        "importe_max_dia_eur": 50000.0,
        "importe_max_activo_eur": 30000.0,
        "perdida_dia_max_eur": 2500.0,
        "perdida_semana_max_eur": 5000.0,
        "ordenes_max_hora": 10,
        "evidencia_verificada_min": 0.05,
        "corte_max_dias": 3,
        "ventana_eventos_dias": 1,
        "viernes_corte_utc_h": 20,
        "deriva_precio_max_pct": 2.0,
        "precio_frescura_max_min": 15.0,
    },
    "CONFIG_DEFECTO.aprobacion": {
        "caduca_min": 15,
        "canales": ["CONSOLA"],
        "enfriamiento_min": 30,
        "enfriamiento_tras_perdida_dia_eur": 0.0,
        "horario_utc": ["07:00", "21:00"],
    },
    "CONFIG_DEFECTO.avisos": {
        "canal_alta": "CONSOLA",
        "canal_escalado": "ESCALADO",
        "reiterar_min": 15,
        "escalar_tras": 3,
    },
    "CONFIG_DEFECTO.kill_switch": {
        "periodo_min_l1_horas": 24,
    },
    "CONFIG_DEFECTO.promocion_nivel": {
        "periodo_min_dias": 30,
    },
    "CONFIG_DEFECTO.mandatos": {
        "version": {"TRADING": "MAN-0.1.0", "TACTICA": "MAN-0.1.0", "LARGO_PLAZO": "MAN-0.1.0"},
        "benchmark_ref": {"TRADING": "BENCH-EFECTIVO", "TACTICA": "BENCH-EFECTIVO", "LARGO_PLAZO": "BENCH-EFECTIVO"},
        "horizonte_dias": {"TRADING": {"min": 1, "max": 28}, "TACTICA": {"min": 14, "max": 183}, "LARGO_PLAZO": {"min": 1095, "max": 7300}},
        "apalancamiento_max": {"TRADING": 1, "TACTICA": 1, "LARGO_PLAZO": 1},
        "tamano_max_pct_cartera": {"TRADING": 10.0, "TACTICA": 10.0, "LARGO_PLAZO": 10.0},
        "instrumentos_permitidos": {"TRADING": None, "TACTICA": None, "LARGO_PLAZO": None},
        "exclusiones": {"TRADING": [], "TACTICA": [], "LARGO_PLAZO": []},
    },
    "CONFIG_DEFECTO.referencias": {
        "benchmark_ref": {"TRADING": "BENCH-EFECTIVO", "TACTICA": "BENCH-EFECTIVO", "LARGO_PLAZO": "BENCH-EFECTIVO"},
        "rentabilidad_anual_pct": {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0},
    },
}


def _congela(t, valores=None):
    valores = _VALOR_DOCUMENTADO if valores is None else valores
    out = {}
    for tab, regs in t.items():
        out[tab] = {}
        for k, v in regs.items():
            r = dict(v)
            if r.get("detalle") is None:
                r["valor_documentado"] = valores.get(tab, {}).get(k)
            else:
                r["valor_documentado"] = None
            out[tab][k] = MappingProxyType(r)
        out[tab] = MappingProxyType(out[tab])
    return MappingProxyType(out)


# De solo lectura: una corrección de redacción cambia este fichero, no la huella del esquema
DOC = _congela(_DOC)


def tablas_del_codigo():
    """Las tres tablas de valores por defecto del código, por nombre. Se importan al llamar (el Orquestador arrastra todo el
    marco) y se devuelven tal cual, sin copiar: quien las use no debe cambiarlas."""
    from control_f import POLITICA_DEFECTO
    from orquestador import CONFIG_DEFECTO
    from parametros import PARAMETROS
    return {"PARAMETROS": PARAMETROS, "CONFIG_DEFECTO": CONFIG_DEFECTO, "POLITICA_DEFECTO": POLITICA_DEFECTO}


def _comprueba_tablas(tablas):
    tablas = tablas_del_codigo() if tablas is None else tablas
    if not isinstance(tablas, dict) or set(tablas) != set(TABLAS) or not all(hasattr(tablas[t], "items") for t in TABLAS):
        raise ValueError(f"se esperan exactamente las tablas {list(TABLAS)}, cada una un diccionario")
    return tablas


def _registro(tabla, clave):
    return {"tabla": tabla, "clave": clave, **{c: _copia(DOC[tabla][clave][c]) for c in CAMPOS}}


def doc(clave, tabla=None):
    """El registro de una clave (copia, con `tabla` y `clave`). Sin `tabla`, se busca en todas las tablas y subtablas: si está
    en más de una es ValueError (ambigua); si no está documentada, KeyError. Un campo de una clave compuesta también se pide
    como «aprobacion.canales». Una tabla desconocida es ValueError."""
    if tabla is not None and tabla not in TODAS:
        raise ValueError(f"tabla desconocida: {tabla!r}")
    if tabla is None and isinstance(clave, str) and clave.count(".") == 1:
        sub = f"CONFIG_DEFECTO.{clave.split('.')[0]}"
        if sub in SUBTABLAS:
            tabla, clave = sub, clave.split(".")[1]
    donde = [t for t in (TODAS if tabla is None else (tabla,)) if isinstance(clave, str) and clave in DOC[t]]
    if not donde:
        raise KeyError(f"sin documentar: {clave!r}")
    if len(donde) > 1:
        raise ValueError(f"clave ambigua {clave!r}: está en {donde}; indique la tabla")
    return _registro(donde[0], clave)


def valor_actual(tabla, clave, tablas=None):
    """El valor que tiene hoy en el código la clave documentada (tabla o subtabla), sin copiar. KeyError si no existe; en una
    subtabla POR_CARTERA, {cartera: valor del campo}."""
    tablas = _comprueba_tablas(tablas)
    if tabla in TABLAS:
        return tablas[tabla][clave]
    if tabla not in SUBTABLAS:
        raise ValueError(f"tabla desconocida: {tabla!r}")
    t, k, forma = SUBTABLAS[tabla]
    padre = tablas[t][k]
    if forma == "CAMPOS":
        return padre[clave]
    return {c: m[clave] for c, m in padre.items()}


def _campos_de(tablas, sub):
    """Los campos que tiene hoy en el código una clave compuesta (lista de conjuntos: uno, o uno por cartera)."""
    t, k, forma = SUBTABLAS[sub]
    padre = tablas[t].get(k)
    if not hasattr(padre, "items"):
        return None
    if forma == "CAMPOS":
        return [set(padre)]
    return [set(m) if hasattr(m, "items") else set() for m in padre.values()] or [set()]


def faltan(tablas=None):
    """Lo que no cuadra entre la documentación y las tablas del código, como lista ordenada de (tabla, clave, motivo):
    `SIN_DOCUMENTAR` (clave o campo del código sin registro), `NO_EXISTE` (registro de algo que el código ya no tiene) o
    `NO_ES_COMPUESTA` (una clave documentada campo a campo cuyo valor ya no es un diccionario). Vacía si todo cuadra. `tablas`
    (por defecto, las del código) permite comprobar otra versión; si no son exactamente las tres tablas, ValueError."""
    tablas = _comprueba_tablas(tablas)
    out = []
    for t in TABLAS:
        codigo, documentadas = set(tablas[t]), set(DOC[t])
        out += [(t, k, "SIN_DOCUMENTAR") for k in sorted(codigo - documentadas, key=str)]
        out += [(t, k, "NO_EXISTE") for k in sorted(documentadas - codigo)]
    for sub in SUBTABLAS:
        campos = _campos_de(tablas, sub)
        if campos is None:
            if SUBTABLAS[sub][1] in tablas[SUBTABLAS[sub][0]]:
                out.append((SUBTABLAS[sub][0], SUBTABLAS[sub][1], "NO_ES_COMPUESTA"))
            continue
        documentadas = set(DOC[sub])
        out += [(sub, k, "SIN_DOCUMENTAR") for k in sorted(set().union(*campos) - documentadas, key=str)]
        out += [(sub, k, "NO_EXISTE") for k in sorted({k for c in campos for k in documentadas - c})]
    return out


def _canon(v):
    return json.dumps(_copia(v), sort_keys=True, ensure_ascii=False)


def desfasados(tablas=None):
    """(tabla, clave) de los registros cuyo `valor_documentado` ya no es el valor del código: su justificación y su pregunta
    hablan de otro valor y hay que revisarlas (H-05). Lo que no existe lo da `faltan()`, no esta función."""
    tablas = _comprueba_tablas(tablas)
    out = []
    for t in TODAS:
        for k, v in DOC[t].items():
            if v["detalle"] is not None:
                continue
            try:
                actual = valor_actual(t, k, tablas)
            except (KeyError, TypeError, AttributeError):
                continue
            if _canon(actual) != _canon(v["valor_documentado"]):
                out.append((t, k))
    return out


def por_estado(estado):
    """(tabla, clave) de los registros con ese estado, en el orden de las tablas, de las subtablas y del código. Estado
    desconocido: ValueError."""
    if estado not in ESTADOS:
        raise ValueError(f"estado desconocido: {estado!r}; válidos {list(ESTADOS)}")
    return [(t, k) for t in TODAS for k, v in DOC[t].items() if v["estado"] == estado]


def _copia(v):
    if isinstance(v, MappingProxyType):
        v = dict(v)
    if isinstance(v, dict):
        return {k: _copia(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_copia(x) for x in v]
    return copy.deepcopy(v)


def preguntas_pendientes(tablas=None):
    """Las preguntas de los valores PROPUESTO, para la sesión T-57: lista de registros (copias) con además `valor`, el valor de
    partida actual del código (copia serializable), en el orden de por_estado("PROPUESTO"), sin las claves compuestas (sus
    campos llevan la pregunta). Falla cerrado como `faltan()`: ValueError si las tablas no son las tres, o si la documentación
    y el código no cuadran (algo sin documentar, documentado que no existe o con el valor cambiado), porque un cuestionario
    incompleto o que pregunta por otro valor no se presenta (H-06)."""
    tablas = _comprueba_tablas(tablas)
    mal = faltan(tablas)
    if mal:
        raise ValueError(f"la documentación no cuadra con el código: {mal[:5]}")
    viejos = desfasados(tablas)
    if viejos:
        raise ValueError(f"valores cambiados sin revisar su justificación: {viejos[:5]}")
    out = []
    for t, k in por_estado("PROPUESTO"):
        if DOC[t][k]["detalle"] is not None:
            continue
        r = _registro(t, k)
        r["valor"] = _copia(valor_actual(t, k, tablas))
        out.append(r)
    return out


def _agregado(tabla):
    estados = {v["estado"] for v in DOC[tabla].values()}
    return next(e for e in ("PROPUESTO", "RATIFICADO", "TECNICO") if e in estados) if estados else None


def defectos():
    """Defectos de forma de la propia tabla (lista de textos; vacía si no hay): estado, fuente, justificación, pregunta, valor
    documentado, detalle y cerrada_por. La existencia de cada fuente en sus documentos la comprueba la batería."""
    out = []
    for t in TODAS:
        for k, v in DOC[t].items():
            sitio = f"{t}.{k}"
            if set(v) != set(CAMPOS):
                out.append(f"{sitio}: campos {sorted(v)}")
                continue
            if v["estado"] not in ESTADOS:
                out.append(f"{sitio}: estado {v['estado']!r}")
            f = v["fuente"]
            if not (isinstance(f, tuple) and f and all(isinstance(x, str) and RE_FUENTE.match(x) for x in f) and len(set(f)) == len(f)):
                out.append(f"{sitio}: fuente {f!r}")
            j = v["justificacion"]
            if not (isinstance(j, str) and 20 <= len(j) <= 400 and j == j.strip() and j.endswith(".")
                    and len(re.findall(r"[.!?](?:\s|$)", j)) <= 2):
                out.append(f"{sitio}: justificación que no es de una o dos frases")
            q, det, cer = v["pregunta"], v["detalle"], v["cerrada_por"]
            if det is not None:
                if det not in TODAS or det == t or q is not None or cer is not None or v["estado"] != _agregado(det):
                    out.append(f"{sitio}: clave compuesta mal descrita (detalle {det!r})")
                if k in _VALOR_DOCUMENTADO.get(t, {}):
                    out.append(f"{sitio}: clave compuesta con valor documentado")
                continue
            if k not in _VALOR_DOCUMENTADO.get(t, {}):
                out.append(f"{sitio}: sin valor documentado")
            if cer is not None:
                if not (v["estado"] == R and q is None and isinstance(cer, str) and cer.startswith("Constitución D-") and cer in f):
                    out.append(f"{sitio}: cerrada_por solo en un RATIFICADO sin pregunta, con una decisión de la Constitución de su fuente")
            elif v["estado"] == TEC:
                if q is not None:
                    out.append(f"{sitio}: TECNICO con pregunta")
            elif not (isinstance(q, str) and 10 <= len(q) <= 250 and "¿" in q and q.endswith("?") and "_" not in q):   # sin nombres de código
                out.append(f"{sitio}: pregunta ausente o que no es lenguaje sencillo")
    for t, regs in _VALOR_DOCUMENTADO.items():
        for k in regs:
            if t not in DOC or k not in DOC[t]:
                out.append(f"{t}.{k}: valor documentado de un registro que no existe")
    return out
