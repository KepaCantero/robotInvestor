"""Documentación de los valores por defecto como datos (T-83, V0.72; Constitución V0.6, §2 punto 4 y §9 punto 4, D-44 y D-45).

D-45: «todo parámetro tiene un valor por defecto prudente, válido para cualquier usuario y con su justificación escrita […];
cada parámetro nuevo de cualquier bloque llega con su valor por defecto y su pregunta del cuestionario». Este módulo da, para
cada clave de `parametros.PARAMETROS`, de `orquestador.CONFIG_DEFECTO` y de `control_f.POLITICA_DEFECTO` (la política de F,
que viaja dentro de `CONFIG_DEFECTO["politica_f"]`), un registro con:

- `estado`: `RATIFICADO` (una decisión ratificada de la Constitución fija ese valor), `PROPUESTO` (valor de partida que
  decidirá el operador en la sesión T-57) o `TECNICO` (no lo decide el operador y no lleva ningún número dentro);
- `fuente`: de dónde sale, con el documento delante para no confundir las decisiones de la Constitución con las de la tabla
  de pendientes de la deuda técnica (los comentarios del código mezclan las dos): «Constitución D-45», «Constitución P-17»,
  «Deuda D-29» (tabla de pendientes del operador), «Deuda T-75» (deuda técnica) o «V0.67» (Documento 0 de esa versión);
- `justificacion`: una o dos frases, por qué ese valor;
- `pregunta`: la pregunta en lenguaje sencillo que hará el cuestionario guiado del asesor de configuración (§2); obligatoria
  en `PROPUESTO` y en `RATIFICADO` (los cambios posteriores usan el mismo cuestionario, D-46) y None en `TECNICO`.

Solo datos y consultas: no cambia ningún valor, no decide nada y no forma parte de la huella del esquema del código
(`persistencia.MODULOS_ESQUEMA`): corregir una redacción no debe exigir versión de esquema ni migración. La correspondencia con
los valores la vigilan `faltan()` y la batería `pruebas/pruebas_parametros_doc_t83.py`. Falla cerrado: `doc()` lanza KeyError
ante una clave sin documentar y ValueError ante una tabla desconocida o una clave ambigua; los registros son de solo lectura y
las funciones devuelven copias.
"""
from __future__ import annotations

import copy
import re
from types import MappingProxyType

VERSION_DOC = "PDOC-0.1.0"
ESTADOS = ("RATIFICADO", "PROPUESTO", "TECNICO")
TABLAS = ("PARAMETROS", "CONFIG_DEFECTO", "POLITICA_DEFECTO")
CAMPOS = ("estado", "fuente", "justificacion", "pregunta")
RE_FUENTE = re.compile(r"(Constitución [DP]-\d{2}|Deuda [DT]-\d{2}|V0\.\d{2})\Z")

R, P, TEC = "RATIFICADO", "PROPUESTO", "TECNICO"


def _r(estado, fuente, justificacion, pregunta=None):
    return {"estado": estado, "fuente": tuple(fuente), "justificacion": justificacion, "pregunta": pregunta}


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
            "¿Cada cuánto tiempo como mínimo hay que volver a revisar una inversión abierta?"),
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
            "¿En qué niveles de análisis quieres que un revisor independiente busque fallos antes de invertir?"),
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
        "politica_f": _r(TEC, ["Deuda T-22"],
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
        "promocion_nivel": _r(P, ["Deuda D-34", "Constitución P-02", "Deuda T-18"],
            "Para subir de nivel hacen falta 30 días en el nivel actual sin incidentes: un mes es el mínimo para ver cómo se "
            "comporta una cartera.",
            "¿Cuánto tiempo sin incidentes debe pasar antes de dar más autonomía a una cartera?"),
        "libres_tope_dia_eur": _r(P, ["Deuda D-32", "Deuda T-33"],
            "Las operaciones libres declaradas fuera del sistema no pasan de 2.000 € por cartera y día, para que no esquiven los "
            "controles.",
            "¿Cuánto puedes invertir al día por tu cuenta en cada cartera fuera de las propuestas del sistema?"),
        "mandatos": _r(P, ["Deuda D-28", "Constitución P-03", "Deuda T-51"],
            "Mandato prudente por cartera: efectivo como referencia, el horizonte de su clase, como mucho un 10 % por posición, sin "
            "apalancar, cualquier instrumento y sin exclusiones.",
            "Para cada cartera, ¿qué horizonte, qué tamaño máximo por inversión y qué exclusiones quieres?"),
        "referencias": _r(P, ["Deuda D-17", "Constitución P-03", "Deuda T-37"],
            "La referencia de cada cartera es el efectivo al 0 %; es provisional, porque casi todo la supera.",
            "¿Con qué referencia quieres comparar cada cartera para saber si invertir vale la pena?"),
        "aprobacion": _r(P, ["Deuda D-18", "Deuda D-19", "Constitución P-08", "Constitución P-12"],
            "Una aprobación caduca a los 15 minutos, solo desde la consola, de 07:00 a 21:00 UTC y con 30 minutos de espera tras "
            "cualquier pérdida del día: la prisa y el cansancio llevan a malas decisiones.",
            "¿Cuánto tiempo tienes para aprobar una operación, en qué horario y cuánto debes esperar tras un día con pérdidas?"),
        "avisos": _r(P, ["Deuda D-07", "Deuda D-19", "Constitución P-08", "Deuda T-41"],
            "Los avisos van a la consola, se repiten cada 15 minutos y se escalan tras tres repeticiones sin acuse: un aviso "
            "importante no se pierde.",
            "¿Por dónde quieres recibir los avisos y cuándo deben insistir o escalar a otro canal?"),
        "kill_switch": _r(P, ["Deuda D-19"],
            "Tras una parada de emergencia la cartera pasa al menos 24 horas en L1 antes de volver a subir: un día para entender qué "
            "pasó.",
            "Después de una parada de emergencia, ¿cuánto tiempo debe pasar antes de devolver autonomía al sistema?"),
        "divisas_cotizacion": _r(TEC, ["Deuda T-10"],
            "Tabla de los instrumentos que no son un par de divisas ISO y de la divisa en que cotizan; vacía, porque en la Fase 1 "
            "todo son pares y la divisa sale del nombre."),
        "rangos_tipo_cambio_eur": _r(P, ["Deuda D-21", "Deuda T-10"],
            "Un tipo de cambio fuera de su rango plausible se rechaza: protege de un dato erróneo que cambiaría el tamaño de las "
            "posiciones.",
            "¿Qué rango de tipos de cambio se considera plausible para cada divisa?"),
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
        "exposicion_max_pct": _r(P, ["Deuda D-01", "Constitución D-45"],
            "La exposición total no supera el capital, porque por defecto no se invierte con dinero prestado.",
            "¿Qué parte de tu capital puede estar invertida a la vez?"),
        "concentracion_max_pct": _r(P, ["Deuda D-01"],
            "Lo invertido en un mismo activo, sumando todas sus posiciones, no pasa del 20 % del capital.",
            "¿Cuánto de tu capital puede acumularse en un mismo activo?"),
        "perdida_dia_max_pct": _r(P, ["Deuda D-01", "Deuda T-50"],
            "Si en el día se pierde el 2 % del capital, no se abren más posiciones ese día: frena la tentación de recuperar.",
            "¿Qué pérdida en un día, como parte de tu capital, debe parar las operaciones nuevas hasta el día siguiente?"),
        "max_posiciones": _r(P, ["Deuda D-01"],
            "Como mucho diez posiciones abiertas a la vez: más no se pueden vigilar bien cuando el operador decide cada una.",
            "¿Cuántas inversiones abiertas a la vez quieres como máximo?"),
        "apalancamiento_max": _r(P, ["Deuda D-01", "Deuda D-12", "Constitución D-45"],
            "Un 1 significa sin apalancamiento, el valor prudente que la Constitución pide por defecto para cualquier copia.",
            "¿Quieres permitir invertir con dinero prestado y, si es así, cuánto como máximo?"),
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
}


def _congela(t):
    return MappingProxyType({tab: MappingProxyType({k: MappingProxyType(dict(v)) for k, v in regs.items()}) for tab, regs in t.items()})


# De solo lectura: una corrección de redacción cambia este fichero, no la huella del esquema
DOC = _congela(_DOC)


def tablas_del_codigo():
    """Las tres tablas de valores por defecto del código, por nombre. Se importan al llamar (el Orquestador arrastra todo el
    marco) y se devuelven tal cual, sin copiar: quien las use no debe cambiarlas."""
    from control_f import POLITICA_DEFECTO
    from orquestador import CONFIG_DEFECTO
    from parametros import PARAMETROS
    return {"PARAMETROS": PARAMETROS, "CONFIG_DEFECTO": CONFIG_DEFECTO, "POLITICA_DEFECTO": POLITICA_DEFECTO}


def _registro(tabla, clave):
    return {"tabla": tabla, "clave": clave, **{c: DOC[tabla][clave][c] for c in CAMPOS}}


def doc(clave, tabla=None):
    """El registro de una clave (copia, con `tabla` y `clave`). Sin `tabla`, se busca en las tres: si está en más de una es
    ValueError (ambigua); si no está documentada, KeyError. Una tabla desconocida es ValueError."""
    if tabla is not None and tabla not in TABLAS:
        raise ValueError(f"tabla desconocida: {tabla!r}")
    donde = [t for t in (TABLAS if tabla is None else (tabla,)) if isinstance(clave, str) and clave in DOC[t]]
    if not donde:
        raise KeyError(f"sin documentar: {clave!r}")
    if len(donde) > 1:
        raise ValueError(f"clave ambigua {clave!r}: está en {donde}; indique la tabla")
    return _registro(donde[0], clave)


def faltan(tablas=None):
    """Lo que no cuadra entre la documentación y las tablas del código, como lista ordenada de (tabla, clave, motivo):
    `SIN_DOCUMENTAR` (clave del código sin registro) o `NO_EXISTE` (registro de una clave que el código ya no tiene). Vacía si
    todo cuadra. `tablas` (por defecto, las del código) permite comprobar otra versión; una tabla que falte o sobre es
    ValueError."""
    tablas = tablas_del_codigo() if tablas is None else tablas
    if not isinstance(tablas, dict) or set(tablas) != set(TABLAS):
        raise ValueError(f"se esperan exactamente las tablas {list(TABLAS)}")
    out = []
    for t in TABLAS:
        codigo, documentadas = set(tablas[t]), set(DOC[t])
        out += [(t, k, "SIN_DOCUMENTAR") for k in sorted(codigo - documentadas, key=str)]
        out += [(t, k, "NO_EXISTE") for k in sorted(documentadas - codigo)]
    return out


def por_estado(estado):
    """(tabla, clave) de los registros con ese estado, en el orden de las tablas y del código. Estado desconocido: ValueError."""
    if estado not in ESTADOS:
        raise ValueError(f"estado desconocido: {estado!r}; válidos {list(ESTADOS)}")
    return [(t, k) for t in TABLAS for k, v in DOC[t].items() if v["estado"] == estado]


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
    partida actual del código (copia serializable), en el orden de por_estado("PROPUESTO")."""
    tablas = tablas_del_codigo() if tablas is None else tablas
    out = []
    for t, k in por_estado("PROPUESTO"):
        r = _registro(t, k)
        r["valor"] = _copia(tablas[t][k]) if k in tablas[t] else None
        out.append(r)
    return out


def defectos():
    """Defectos de forma de la propia tabla (lista de textos; vacía si no hay): estado, fuente, justificación y pregunta. La
    existencia de cada fuente en sus documentos la comprueba la batería."""
    out = []
    for t in TABLAS:
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
            q = v["pregunta"]
            if v["estado"] == TEC:
                if q is not None:
                    out.append(f"{sitio}: TECNICO con pregunta")
            elif not (isinstance(q, str) and 10 <= len(q) <= 250 and "¿" in q and q.endswith("?") and "_" not in q):   # sin nombres de código
                out.append(f"{sitio}: pregunta ausente o que no es lenguaje sencillo")
    return out
