"""T-158 · Guías de mejora del Orquestador (CT-18, tipos 1 y 2) en el ejecutor del Bloque A.

Fuentes (kit de contexto): Documento 0 V5.1 (0.2, R23, 5.1, 6.1 CT-18, 18.1 y 18.3; el Anexo B remite los campos de CT-18 al
prompt del Orquestador), prompt del Orquestador V5.0 (4.5, forma del mensaje; 6.8, reclasificación obligatoria; 6.9, guías),
prompt del Analizador V5.0 («aplicas las de tipo 1 y 2 si no contradicen el Documento 0; … la registras y no la aplicas») y
esquema de HA V2.0 (4.4 GUI-, 4.8 P3- y COR-, 5 estados). Plan de pruebas V3.0: PB-48.

- `ESQUEMA_CT18_GUIA`: el cuerpo de un CT-18 de tipo GUIA. El esquema es la definición: `validar_cuerpo` lo aplica al emitir y
  otra vez antes de aplicar una guía guardada en HA. La mensajería (`contratos.py`) sigue validando solo el sobre (canal, R8),
  como hasta ahora, para no cambiar los formatos congelados.
- `conflicto_del_item`: el control doble (6.8: «El agente receptor repite la verificación: el control es doble»). Un ítem que
  toca lo que una guía nunca puede tocar (6.9) o lo que la reclasificación obligatoria hace de tipo 3 (6.8) está en conflicto.
  Revisa todos los campos de texto que llegan al modelo (T-161): lo que reconoce como dudoso es conflicto; lo que no
  reconoce se aplica como contexto del modelo del receptor. `conflicto_de_leccion` hace lo mismo con las lecciones de AG-20.
- `Guias`: el Orquestador emite (`emitir`), que ya rechaza un ítem en conflicto o una guía para un agente que es un control
  (T-161, H-04 y H-05); al empezar cada run el receptor repite la revisión (`cargar`): cada ítem en conflicto deja un COR- y
  un P3- en HA (una sola vez, aunque la retirada falle a mitad) y el Orquestador lo retira de la guía (versión nueva o
  RETIRADA). Lo que queda llega al contexto del agente receptor (`para`); nunca a HT-03, a las puertas ni a G3, que son
  código. Lo que llega al contexto de un modelo depende del detector: por eso ningún agente de control recibe guías.
"""
from __future__ import annotations

import copy
import datetime as dt
import re
import threading
import unicodedata
from typing import Any

import jsonschema

from .configuracion import parametro
from .contratos import RE_INYECCION, TODOS, MensajeInvalido
from .llm import MockClient

FECHA = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
TXT = {"type": "string", "minLength": 1}

# Ítem de una guía (prompt del Orquestador 4.5 y 6.9; HA 4.4)
ITEM_GUIA = {
    "type": "object",
    "required": ["item_id", "tipo", "origen", "que_cambia", "donde_se_comprueba", "como_se_sabe", "caducidad"],
    "properties": {
        "item_id": {"type": "string", "pattern": r"^GUI-AG[0-9]{2}-[0-9]{4}-[0-9]{2}$"},
        "tipo": {"enum": [1, 2]},                                            # 6.9: «solo ítems de tipo 1 y 2»
        "origen": {"type": "array", "minItems": 1,                          # 6.9: «origen (HAL- o LEC-)»
                   "items": {"type": "string", "pattern": r"^(HAL|LEC)-[A-Z0-9-]+$"}},
        "que_cambia": TXT, "donde_se_comprueba": TXT, "como_se_sabe": TXT,
        "caducidad": {"type": "string", "pattern": FECHA},
    },
}
# Cuerpo de un CT-18 de tipo GUIA. `tipo_ct18` [PROPUESTO]: el prompt lo llama `tipo_mensaje`, pero el sobre del ejecutor ya
# usa ese campo para ENCARGO/RETORNO (contratos.py) y no se puede cambiar desde el cuerpo. Se admiten campos adicionales
# (6.2.3 del Documento 0: los campos son el mínimo común).
ESQUEMA_CT18_GUIA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "CT-18 · Guía de mejora (Orquestador → cualquier agente)",
    "type": "object",
    "required": ["tipo_ct18", "guia_id", "version", "sustituye", "fecha_aplicacion", "items", "acuse_requerido"],
    "properties": {
        "tipo_ct18": {"const": "GUIA"},
        "guia_id": {"type": "string", "pattern": r"^GUI-AG[0-9]{2}-[0-9]{4}$"},
        "version": {"type": "integer", "minimum": 1},
        "sustituye": {"anyOf": [{"type": "null"}, {"type": "string", "pattern": r"^GUI-AG[0-9]{2}-[0-9]{4}$"}]},
        "fecha_aplicacion": {"type": "string", "pattern": FECHA},
        "items": {"type": "array", "minItems": 1, "items": ITEM_GUIA},
        "acuse_requerido": {"const": True},                                 # 6.9: «se exige acuse»
    },
}
_VALIDADOR = jsonschema.Draft202012Validator(ESQUEMA_CT18_GUIA)
CAMPOS_ITEM = ("tipo", "origen", "que_cambia", "donde_se_comprueba", "como_se_sabe", "caducidad")

# Batería de regresión del Plan de pruebas V3.0 (§6), que toda propuesta de tipo 3 del Orquestador cita, más la de R23
BATERIA_REGRESION = ["PB-01", "PB-02", "PB-06", "PB-08", "PB-13", "PB-18", "PB-20", "PB-21", "PB-22", "PB-23", "PB-30",
                     "PB-31", "PB-36", "PB-37", "PB-39", "PB-49", "PB-48"]

# ---------------------------------------------------------------------------------------------------------------------
# Control doble (emisor y receptor): qué ítems contradicen una regla
# ---------------------------------------------------------------------------------------------------------------------
# [PROPUESTO] (T-158, endurecido en T-161 y en su r02 tras las QA r01 de T-158 y de T-161). Se revisan todos los campos de
# texto del ítem que llegan al modelo (`que_cambia`, `donde_se_comprueba`, `como_se_sabe`) y `origen`, normalizados
# (`_normalizar`: NFKC, sin caracteres de formato, guiones y subrayados como espacio, sin tildes, en minúsculas), y otra vez
# con las cifras de las palabras que mezclan letras y cifras leídas como letras («0mite», «n0»). Antes se enmascaran los
# sentidos financieros corrientes de algunos términos (`FINANCIERO`: «peso en el índice», «estados financieros»…).
# Lo que el detector reconoce como dudoso es conflicto; lo que no reconoce se aplica como contexto del modelo del receptor.
# En `que_cambia` (la acción, 6.9):
# 1. TIPO_3 por la reclasificación obligatoria (6.8): pesos, escalas, anclas, topes, umbrales, bandas, puertas, estados,
#    esquemas, prioridades (salvo las de la agenda de vigilancia, tipo 2 en 6.8), destinos, canales, el catálogo de
#    comprobaciones; y METRICA (6.9: nunca introduce métricas que condicionen el comportamiento).
# 2. RELAJA_CONTROL: nombra un control y una acción que lo quita o rebaja, o una rebaja implícita («un único análisis», «por
#    bueno», «como leves», «con una fuente» junto a la tesis). NOMBRA_CONTROL: nombra un control o una regla (`CONTROLES`) y
#    la acción no es claramente de reforzarlo o de no tocarlo (un verbo de `REFUERZA` sin ninguna marca de `NIEGA`, `RELAJA`
#    ni rebaja implícita).
# 3. PROHIBIDO (6.9): pide credenciales, datos protegidos (R8) o modificar un prompt o un contrato.
# En `donde_se_comprueba`, `como_se_sabe` y `origen` (nombran el campo o la comprobación, p. ej. «HT-09 G3-DAT-02 sin fallos»
# en el ejemplo del prompt) no basta con nombrar un control: lo es la acción que lo rebaja, una orden con una condición
# (`REFUERZA` y `NIEGA`) sobre un control, la rebaja implícita, el tipo 3 con un verbo de cambio y lo prohibido.
# En todos los campos: INYECCION (R9, `contratos.RE_INYECCION`), INSTRUCCION (un ítem que redefine términos o remite a otro),
# MARCADO (HTML o Markdown que tacha u oculta), IDIOMA (palabras funcionales de otra lengua, sin contar las siglas ni los
# nombres propios) y ESCRITURA (caracteres fuera de los permitidos: otra escritura, letras latinas sin base en el alfabeto del
# castellano —ø, ı, ł, versalitas—, emojis). Un falso positivo retira el ítem y lo escala (prudente); un falso negativo llega
# como contexto al modelo del receptor, nunca a la elegibilidad, las puertas ni G3, que son código que no lee guías. Las
# guías a un agente que es un control (`AGENTES_DE_CONTROL`) no se emiten ni se aplican.
TIPO_3 = (r"\bpesos?\b", r"\bescalas?\b", r"\banclas?\b", r"\btopes?\b", r"\bumbral(?:es)?\b", r"\bbandas?\b",
          r"\bpuertas?\b", r"\bps ?[1-8]\b", r"\bg[1-4]\b", r"\bgc[0-4]\b", r"\besquemas?\b", r"\bprioridad(?:es)? entre (?:las )?reglas\b",
          r"\bdestinos?\b", r"\bcanal(?:es)?\b", r"\bcatalogo de comprobaciones\b", r"\bestados?\b")
# T-161 r02 (QA r01, H-03): sentidos financieros corrientes de términos de tipo 3 y de controles; se enmascaran antes de
# detectar (lo demás del texto se revisa igual)
FINANCIERO = re.compile(
    r"\bpesos? (?:en|de|del|dentro del?) (?:el |la |los |las |un |una )?(?:indice|cartera|sector|benchmark|referencia|fondo)\w*"
    r"|\bpesos? sectorial\w*|\bestados? (?:financier|contable)\w*|\bestados? de (?:resultados|flujos|cuentas|situacion|cambios)\b"
    r"|\bdestinos? de (?:los |sus )?fondos\b|\bcanal(?:es)? de (?:distribucion|venta|ventas|comercializacion)\b"
    r"|\besquemas? de (?:comisiones|remuneracion|incentivos|pagos?|amortizacion|dividendos|cupones)\b"
    r"|\bbandas? de (?:fluctuacion|cotizacion|bollinger|precios?)\b|\b(?:fecha|dia|hora) de corte\b|\bcorte (?:del|de) cupon\b"
    r"|\bavisos? (?:de|del) (?:la |el )?(?:cnmv|sec|esma|regulador\w*|supervisor\w*|emisor\w*|bolsa)\b|\bhechos? relevantes?\b"
    r"|\bperiodos? de bloqueo\b|\block ?up\b|\bauditor(?:es|a|as)? extern\w*|\bauditorias? extern\w*|\bcuentas auditadas\b"
    r"|\bbalances? auditad\w*|\binformes? de auditoria\b|\bauditorias? de (?:los |sus )?contratos\b"
    r"|\bcontratos? (?:inteligentes|de futuros?|de opciones|de derivados|forward|de permuta|de arrendamiento|de suministro)\b"
    r"|\bvencimiento del contrato\b|\bcontrato (?:del|de) (?:subyacente|futuro)\b"
    r"|\bestados? de (?:los |las |la |el )?(?:inventarios|obras?|red|activos?|proyectos?|economia|mercados?|cosechas|balance)\b"
    r"|\bumbral de rentabilidad\b|\btopes? de concentracion\b|\bpor canal(?:es)?\b|\banclas? (?:monetari|nominal)\w*")
PRIORIDAD = re.compile(r"\bprioridad(?:es)?\b|\bprioriz\w*|\bantep[ou]n\w*|\bpor encima de\b|\bjerarquia\w*")
AGENDA = re.compile(r"\bagenda\b")   # 6.8: «prioridades de la agenda de vigilancia» es tipo 2
METRICA = re.compile(r"\bmaximiz\w*|\bminimiz\w*|\bmetricas?\b")
CONTROLES = (
    (r"\bsegunda pasada\b", "9.1 (banda marginal: segunda pasada)"),
    (r"\bpasadas?\b|\bpassada\b|\bsecond pass\b|\breevalu\w*|\bre evalu\w*|\bdimension\w*|\bpuntuacion\w*",
     "9.1 (banda marginal: segunda pasada)"),
    (r"\bcorrobor\w*|\braices?\b|\braiz\b|\borigen(?:es)? independientes?\b|\bfuentes? independientes?\b", "R10 y PS1 (corroboración)"),
    (r"\bverific\w*|\bcomprob\w*|\bcomprueb\w*|\bvalid\w*|\bcontrol(?:es)?\b|\brevis\w*|\bchecks?\b", "R16 (los controles nunca se recortan)"),
    (r"\bregistr\w*|\bhistorial\w*|\btrazab\w*|\banot\w*", "R7 y R24 (registro y trazabilidad)"),
    (r"\bseguridad\b", "R8 y sección 17 (seguridad)"),
    ((r"\brefut\w*|\bobjecion\w*|\bcontrari[ao]s?\b|\bautocritic\w*|\binvalidacion\w*|\ben contra\b|\ba favor\b|\bargument\w*"
      r"|\bdebilidad\w*|\briesgos?\b"), "R12 (autocrítica obligatoria)"),
    (r"\bevidencias?\b", "R7 (trazabilidad de la evidencia)"),
    (r"\bconfianza\b|\bcalibra\w*|\bprimari[ao]s?\b|\bsecundari[ao]s?\b", "R10 y R12 (clasificación de la evidencia y confianza)"),
    (r"\bauditor\w*|\baudit\w*|\bhallazg\w*", "R16 y auditoría (AG-19)"),
    ((r"\bvalidacion final\b|\bht ?09\b|\bdictam\w*|\baprob\w*|\bbloqueos?\b|\bblocks?\b|\bavis[aeo]s?\b|\bavisar\b|\bwarnings?\b"
      r"|\bexcepcion\w*"), "G3 (HT-09: un bloqueo nunca pasa a aviso; R16 y R17)"),
    (r"\bht ?03\b|\belegib\w*|\beligib\w*|\bbanda marginal\b|\bcorte\b|\bps ?[1-8]\b|\bpuertas?\b|\bgates?\b", "HT-03 y PS1–PS8 (elegibilidad)"),
    (r"\bht ?[0-9]{2}\b", "herramientas deterministas (HT-01 a HT-09)"),
    (r"\blimitacion\w*|\balcance reducido\b", "R7 (limitaciones declaradas)"),
    (r"\br ?[0-9]{1,2}\b|\breglas?\b|\bdocumento 0\b", "0.2 (reglas del Documento 0)"),
    (r"\bprompts?\b|\bcontratos?\b|\bct ?[0-9]{2}\b", "18.1 (prompts y contratos)"),
    ((r"\breglas? de datos\b|\bdatos? (?:\w+ ){0,4}(?:de )?(?:mas|menos) de [0-9]+ (?:dias|semanas|meses|anos|horas)\b|\bantiguedad\b"
      r"|\bfrescura\b|\bdatos? (?:antiguos|viejos|caducados|desfasados|obsoletos|sin fecha|no verificados)\b"), "6.9 (reglas de datos)"),
)
_VERBOS_NEGADOS = (r"aplic|apliqu|exig|exij|hac|hag|realiz|realic|registr|anot|comprob|comprueb|verific|verifiqu|corrobor|ped|pid"
                   r"|ejecut|document|requer|requier|repet|repit|valid|refut|busc|busqu|inform|inclu|consult|cit|revis|analiz"
                   r"|evalu|contrast|confirm|consider|ten|teng|atiend|sigu|us|mir|repas|plante|formul|argument|cuestion|escrib")
_OBJETOS_DE_CONTROL = (r"pasadas?|segunda|revision\w*|verificacion\w*|comprobacion\w*|corroboracion\w*|refutacion\w*|raiz|raices"
                       r"|objecion\w*|controles?|auditoria\w*|registros?|veces|opcion\w*|fuentes?|origen\w*|tesis")
RELAJA = re.compile(
    r"\bomit\w*|\bomision\w*|\bsalt\w*|\bprescind\w*|\bsuprim\w*|\belimin\w*|\bquit\w*|\brelaj\w*|\bborr\w*|\bvaci[oa]s?\b|\bvaciar\b"
    r"|\brebaj\w*|\breduc\w*|\bdesactiv\w*|\bignor\w*|\bobvi\w*|\bevit\w*|\bdej(?:a|ar|e|es|en)? de\b"
    r"|\baplaz\w*|\bpospon\w*|\bpospong\w*|\bdifier\w*|\bdiferir\b|\bsustitu\w*|\breemplaz\w*|\ben (?:lugar|vez) de\b|\bcopi[ae]\w*"
    r"|\blax\w*|\bflexibiliz\w*|\bmenos estrict\w*|\bpermisiv\w*|\bahorr\w*|\bdispens\w*|\bexim\w*|\bexent\w*|\binnecesari\w*"
    r"|\bsuperflu\w*|\bredundant\w*|\bprescindible\w*"
    r"|\bno (?:es |son |sera |seran )?(?:necesari\w*|obligatori\w*|imprescindible\w*|precis[oa]s?|requerid\w*)"
    r"|\bno (?:hace|hacen|haga|hagan) falta\b"
    r"|\b(?:no|nunca|jamas|tampoco|ni)\b(?: \w+){0,2} (?:" + _VERBOS_NEGADOS + r")\w*"
    r"|\bsin (?:la |el |las |los |su |sus )?(?:segunda|pasada|verific|comprob|registr|corrobor|refut|valid|control|revis|audit"
    r"|objecion|contrast)\w*"
    r"|\bbasta(?:n|ra)? con\b|\bsuficiente con\b|\bvale (?:con|para)\b|\buna sola (?:fuente|raiz|pasada)\b"
    r"|\bmenos (?:fuentes|raices|comprobaciones|verificaciones|controles|pasadas|revisiones|objeciones|hallazgos)\b|\bopcional\w*"
    # T-161 r02 (QA r01, H-02): negaciones indirectas, excepciones y números con letras
    r"|\bsobra(?:n|ra|ran|ndo)?\b|\bsobrar\b|\besta(?:n)? de mas\b|\bcarec\w*|\bpor alto\b|\bde lado\b|\bexcepto\b|\bsalvo\b"
    r"|\bmenos en\b|\bfacultativ\w*|\bvoluntari\w*|\bdescart\w*"
    r"|\b(?:cero|ningun[ao]?|nada de) (?:\w+ ){0,2}?(?:" + _OBJETOS_DE_CONTROL + r")\b|\bcero veces\b"
    r"|\bskip\w*|\bbypass\w*|\bdisabl\w*|\bwithout\b|\bno need\b|\bdon t\b|\bdo not\b|\bometr\w*|\bometi\w*|\bno cal\b|\bsense\b")
# Rebajas implícitas: conflicto por sí solas (un solo análisis u origen, dar por bueno o resuelto sin comprobar, objeciones o
# bloqueos como leves, la primera lectura como definitiva)
REBAJA_IMPLICITA = re.compile(
    r"\b(?:un (?:unico|solo)|una (?:unica|sola)|solo (?:un|una|1)|unicamente (?:un|una|1)) (?:\w+ ){0,2}?(?:analisis|lectura"
    r"|pasada|revision|fuente|raiz|origen|referencia|respaldo|apoyo|confirmacion|comprobacion|verificacion|vistazo|intento"
    r"|objecion|prueba|evidencia)\w*"
    r"|\bprimer[ao]? (?:lectura|borrador|intento|vistazo|impresion)\b"
    r"|\bpor (?:buen[oa]s?|valid[oa]s?|aprobad[oa]s?|ciert[oa]s?|correct[oa]s?|cerrad[oa]s?|resuelt[oa]s?|definitiv[oa]s?)\b"
    r"|\bcomo (?:leves?|menores?|avisos?|advertencias?|warnings?|no bloqueantes?|irrelevantes?|definitiv[oa]s?|primari[ao]s?"
    r"|resuelt[oa]s?)\b")
# Un solo apoyo para la tesis («con una fuente», «una lectura basta»): solo junto a la tesis o a una marca de suficiencia
MULTIPLICIDAD = re.compile(r"\b(?:con|en|sobre|de|a) (?:un|una) (?:respaldo|referencia|fuente|origen|raiz|apoyo|confirmacion"
                           r"|lectura)\b|\buna lectura\b")
SUFICIENCIA = re.compile(r"\btesis\b|\bbasta\w*|\bvale\b|\bsuficiente\b|\bcierr\w*|\bcerrar\b|\bapoy\w*|\bsosten\w*")
# Un verbo que refuerza el control que nombra o que no lo toca (orden, formato, búsqueda), sin ninguna marca de rebaja
REFUERZA = re.compile(
    r"\b(?:haz|hacer|haga|realiza\w*|aplica|aplicar|aplique|comprueba|comprobar|compruebe|verifica|verificar|verifique|anade|anadir"
    r"|anada|exige|exigir|exija|registra|registrar|registre|anota|anotar|anote|cita|citar|cite|repite|repetir|repita|incluye"
    r"|incluir|incluya|consulta|consultar|consulte|revisa|revisar|revise|documenta|documentar|documente|refuerza|reforzar"
    r"|refuerce|amplia|ampliar|amplie|corrobora|corroborar|corrobore|contrasta|contrastar|contraste|confirma|confirmar|confirme"
    r"|busca|buscar|busque|manten|mantener|mantenga|conserva|conservar|conserve|detalla|detallar|detalle|justifica|justificar"
    r"|justifique|explicita|explicitar|asegura|asegurar|asegurate|corrige|corregir|corrija"
    # T-161 r02 (QA r01, H-03): verbos de orden, formato y búsqueda (tipo 2 de 6.8), que no tocan el control que nombran
    r"|presenta|presentar|presente|resume|resumir|resuma|agrupa|agrupar|agrupe|ordena|ordenar|ordene|expresa|expresar|exprese"
    r"|escribe|escribir|escriba|usa|usar|use|utiliza|utilizar|utilice|lee|leer|lea|mira|mirar|mire|empieza|empezar|empiece"
    r"|indica|indicar|indique|senala|senalar|senale|muestra|mostrar|muestre|describe|describir|describa|nombra|nombrar"
    r"|explica|explicar|explique|separa|separar|separe|reutiliza|reutilizar|reutilice|rehaz|rehacer|adelanta|adelantar)\b")
NIEGA = re.compile(r"\b(?:no|nunca|jamas|ni|tampoco|sin|salvo|excepto|solo|solamente|unicamente|basta\w*|vale|suficiente"
                   r"|presupuesto|coste\w*|prisa|rapid\w*|si (?:da|hay) tiempo|si (?:lo )?permite|oportun\w*|criterio|consider\w*"
                   r"|procede|proceda|discrecion\w*|convenient\w*|si (?:quieres|puedes|prefieres)|cuando (?:puedas|quieras)"
                   # T-161 r02 (QA r01, H-02): condiciones que debilitan una orden de refuerzo
                   r"|sobra\w*|cualquier\w*|si te parece|cuando (?:lo )?veas|veas necesario|voluntari\w*|facultativ\w*|eleccion|elijas"
                   r"|despues de (?:entregar|enviar|cerrar)|siguiente|proximo|posterior\w*|mas adelante|a mano|que tengas"
                   r"|cubiert\w* por|anterior|cero|ningun\w*|nada|(?:una|uno|dos|tres|cuatro|cinco|[0-9]+) de (?:cada|las|los)"
                   r"|(?:en|a|para) (?:las |los )?(?:opciones|candidatas|casos)(?: \w+){0,2} lejos del corte)\b")
CREDENCIALES = re.compile(r"\bcredencial\w*|\bcontrasen\w*|\bpassword\w*|\bapi ?keys?\b|\bclaves? (?:de )?(?:la )?api\b"
                          r"|\btoken(?:s)? de acceso\b|\baccess ?token\w*|\bsecret\w*|\bclaves? (?:de acceso|privada\w*|secreta\w*)\b"
                          r"|\bllaves? (?:de acceso|privada\w*)\b|\btokens? (?:de )?(?:api|autenticacion|sesion)\b|\bbearer\b")
DATOS_PROTEGIDOS = re.compile(
    r"\bdatos? (?:personales|protegidos|sensibles)\b|\b(?:nombres?|apellidos?|correos?|e ?mails?|telefonos?|dni|nif|nie|pasaportes?"
    r"|domicilios?|direccion\w*|iban|cuentas?(?: bancarias?)?|patrimonio|cartera|perfil|ingresos|saldos?)(?: \w+){0,4} (?:del|de la"
    r"|de los|de las) (?:inversor\w*|operador\w*|cliente\w*|titular\w*|usuari\w*|propietari\w*)\b")
PROMPT_O_CONTRATO = re.compile(r"\bprompt\w*|\bcontratos?\b|\bct ?[0-9]{2}\b")
CAMBIO = re.compile(r"\b(?:modific|cambi|edit|reescrib|sustitu|actualiz|ampli|anad|quit|elimin|retir)\w*")
CAMBIO_T3 = re.compile(r"\b(?:modific|cambi|sustitu|actualiz|ajust|aument|disminu|establec|relaj|endurec)\w*"
                       r"|\b(?:sube|subir|suba|baja|bajar|baje|fija|fijar|fije|pon|poner|ponga|marca|marcar|marque)\b")
# Un ítem que redefine términos o remite a otro ítem no es una acción concreta y verificable (6.9)
INSTRUCCION = re.compile(r"\bsignifica\w*|\bequivale\w* a\b|\bquiere decir\b|\bse entiende por\b|\binterpret\w* (?:\w+ ){0,3}como\b"
                         r"|\blo contrario\b|\bal reves\b|\b(?:punto|item|apartado|instruccion|parrafo) anterior\b|\bcubiert[ao]s? por\b")
MARCADO = re.compile(r"<\s*/?\s*[a-z!][^>]*>|~~|\]\s*\(")   # HTML o Markdown que tacha, oculta o enlaza texto
# Palabras funcionales de otras lenguas (inglés, catalán, francés, portugués, italiano y alemán) que no son castellano
IDIOMA = re.compile(
    r"\b(?:the|and|for|with|of|when|all|skip|treat|are|does|not|without|only|any|every|if|this|that|should|must|always|never"
    r"|from|into|pass|don t|amb|per|els|dels|segona|passada|ometre|cal|nomes|sense|aquest\w*|fer|tambe|perque|mai|quan"
    r"|avec|pour|sans|ne|pas|des|du|une|est|sont|deuxieme|toujours|jamais|nao|voce|uma|sem|passagem|tambem|sempre|entao"
    r"|della|delle|degli|il|gli|seconda|passaggio|senza|nicht|und|der|die|zweite|ohne|ist|immer)\b")
# Nombres propios (dos o más palabras con mayúscula, con sus conectores) y siglas: no cuentan para IDIOMA («Bank of England»,
# «The Economist», «DER», «PER»)
_NOMBRE_PROPIO = re.compile(r"\b[A-ZÁÉÍÓÚÜÑ][\w&.'’]*(?:\s+(?:(?:of|the|and|for|de|del|la|las|los|y|&|der|die|und|du|des|le)\s+)?"
                            r"[A-ZÁÉÍÓÚÜÑ][\w&.'’]*)+")
_SIGLA = re.compile(r"\b[A-ZÁÉÍÓÚÜÑ0-9]{2,}\b")
# Caracteres permitidos fuera del ASCII: letras latinas con base ASCII (á, é, ñ, ü, ç…), guiones, espacios y estos símbolos
SIMBOLOS_PERMITIDOS = set("€£¥%‰°ºª§·•…‘’‚“”„«»¿¡±×÷≤≥≈≠→←↔↑↓⇒∞√∆⁄®©™")
_LEET = str.maketrans("013457", "oieast")
CAMPOS_TEXTO = ("que_cambia", "donde_se_comprueba", "como_se_sabe", "origen")   # T-161 (H-02): todo lo que llega al modelo
R23 = "R23 (manda la más restrictiva mientras se escala)"
# Familias que hacen sospechosa toda la guía: sus otros ítems también se retiran (una instrucción repartida entre ítems)
COMPROMETEN = {"INYECCION", "INSTRUCCION", "MARCADO"}
# T-161 (H-04) [PROPUESTO]: 6.8 y 6.9 no dicen a quién puede dirigir guías el Orquestador; por defecto, a ningún agente que
# sea un control (lo que hace un modelo y una guía podría debilitar). T-161 r02 (QA r01, H-01): AG-20 también, porque sus
# lecciones van a F6 y de ahí al contexto de todos los agentes, también los de control
AGENTES_DE_CONTROL = {"AG-11": "refutación (R12)", "AG-18": "el Orquestador: emite las guías y dictamina las excepciones (G3)",
                      "AG-20": "aprendizaje: sus lecciones llegan como contexto a todos los agentes",
                      "AG-19": "auditoría"}


def _normalizar(texto: Any) -> str:
    t = unicodedata.normalize("NFKC", str(texto))
    t = "".join(" " if c == "_" or unicodedata.category(c) == "Pd" or c in "\u2212\u2043" else c
                for c in t if unicodedata.category(c) != "Cf")
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t.lower()).strip()


def _texto(valor: Any) -> str:
    if valor is None:
        return ""
    return " ".join(str(v) for v in valor) if isinstance(valor, (list, tuple)) else str(valor)


def _otra_escritura(texto: str) -> list[str]:
    """Caracteres fuera de los permitidos (tras NFKC): letras de otra escritura (cirílico, griego…), letras latinas sin base
    ASCII (ø, ı, ł, versalitas: homoglifos), emojis y símbolos raros. Se permiten el ASCII, las letras latinas con base ASCII
    (á, é, ñ, ü, ç…), las marcas combinantes (se quitan al normalizar), los guiones, los espacios y `SIMBOLOS_PERMITIDOS`."""
    fuera = set()
    for c in unicodedata.normalize("NFKC", texto):
        if c.isascii() or c in SIMBOLOS_PERMITIDOS or unicodedata.category(c) in ("Mn", "Me", "Cf", "Pd", "Zs", "Zl", "Zp"):
            continue
        if not c.isalpha() or not unicodedata.name(c, "").startswith("LATIN"):
            fuera.add(c)                                       # otra escritura, emoji o símbolo
        elif not unicodedata.normalize("NFKD", c)[0].isascii():
            fuera.add(c)                                       # latina sin base ASCII: posible homoglifo
    return sorted(fuera)


def _sin_nombres(crudo: str) -> str:
    """El texto sin siglas ni nombres propios (para IDIOMA); si casi todo está en mayúsculas, solo sin nombres propios."""
    t = unicodedata.normalize("NFKC", crudo)
    letras = [c for c in t if c.isalpha()]
    t = _NOMBRE_PROPIO.sub(" ", t)
    if letras and sum(c.isupper() for c in letras) / len(letras) < 0.6:
        t = _SIGLA.sub(" ", t)
    return _normalizar(t)


def _variantes(t: str) -> list[str]:
    """El texto con las cifras de las palabras que mezclan letras y cifras leídas como letras («0mite», «n0»), si cambia."""
    v = re.sub(r"\b(?=\w*[a-z])(?=\w*[013457])\w+\b", lambda m: m.group(0).translate(_LEET), t)
    return [v] if v != t else []


def _controles(t: str) -> list[tuple[str, str]]:
    return [(m.group(0), r) for p, r in CONTROLES for m in [re.search(p, t)] if m]


def _refuerza(t: str) -> bool:
    """La acción es claramente de reforzar: un verbo de refuerzo y ninguna marca de negación, rebaja o excepción."""
    return bool(REFUERZA.search(t)) and not (NIEGA.search(t) or RELAJA.search(t) or REBAJA_IMPLICITA.search(t))


def _revisar_texto(t: str, estricto: bool, familias: list, terminos: list, reglas: list, crudo: str | None = None) -> None:
    """Familias de conflicto de un texto normalizado. `estricto` para `que_cambia` (la acción); los campos descriptivos
    no son conflicto solo por nombrar un control o un término de tipo 3. `crudo` (el texto sin normalizar) para IDIOMA."""
    t = FINANCIERO.sub(" termino financiero ", t)
    tipo3 = [m.group(0) for p in TIPO_3 for m in [re.search(p, t)] if m] if estricto or CAMBIO_T3.search(t) else []
    prio = PRIORIDAD.search(t) if estricto and not AGENDA.search(t) else None
    if prio:
        tipo3.append(prio.group(0))
    if tipo3:
        familias.append("TIPO_3")
        terminos += tipo3
        reglas.append("18.1 (tipo 3) y reclasificación obligatoria (6.8 del prompt del Orquestador)")
    metrica = METRICA.search(t) if estricto else None
    if metrica:
        familias.append("METRICA")
        terminos.append(metrica.group(0))
        reglas.append("6.9 (una guía nunca introduce métricas que condicionen el comportamiento)")
    relaja = RELAJA.search(t)
    if relaja:
        tocados = _controles(t)
        if tocados:
            familias.append("RELAJA_CONTROL")
            terminos += [relaja.group(0)] + [x for x, _ in tocados]
            reglas += [r for _, r in tocados]
    condicion = None if estricto else (REFUERZA.search(t) and NIEGA.search(t))
    if condicion and _controles(t):
        familias.append("RELAJA_CONTROL")    # una orden con una condición sobre un control, en un campo descriptivo
        terminos.append(condicion.group(0))
        reglas += [r for _, r in _controles(t)]
    implicita = REBAJA_IMPLICITA.search(t) or (MULTIPLICIDAD.search(t) if SUFICIENCIA.search(t) else None)
    if implicita:
        familias.append("RELAJA_CONTROL")
        terminos.append(implicita.group(0))
        reglas += [r for _, r in _controles(t)] or ["R10, R12 y R16 (rebaja implícita de un control)"]
    nombrados = _controles(t) if estricto and "RELAJA_CONTROL" not in familias and not _refuerza(t) else []
    if nombrados:
        familias.append("NOMBRA_CONTROL")
        terminos += [x for x, _ in nombrados]
        reglas += [r for _, r in nombrados]
    cred = CREDENCIALES.search(t)
    if cred:
        familias.append("PROHIBIDO")
        terminos.append(cred.group(0))
        reglas.append("R8 y 6.2.5 (una guía nunca pide credenciales, 6.9)")
    protegido = DATOS_PROTEGIDOS.search(t)
    if protegido:
        familias.append("PROHIBIDO")
        terminos.append(protegido.group(0))
        reglas.append("R8 (datos protegidos del operador)")
    pc, cambio = PROMPT_O_CONTRATO.search(t), CAMBIO.search(t)
    if pc and cambio:
        familias.append("PROHIBIDO")
        terminos += [cambio.group(0), pc.group(0)]
        reglas.append("18.1 (cambiar un prompt o un contrato es tipo 3; 6.9)")
    for patron, familia, regla in ((RE_INYECCION, "INYECCION", "R9 (instrucciones incrustadas, `contratos.RE_INYECCION`)"),
                                   (INSTRUCCION, "INSTRUCCION", ("6.9 (cada ítem es una acción concreta y verificable: no "
                                                                 "redefine términos ni remite a otro ítem)")),
                                   (MARCADO, "MARCADO", "6.9 (HTML o Markdown que tacha u oculta parte del ítem)")):
        hallado = patron.search(t)
        if hallado:
            familias.append(familia)
            terminos.append(hallado.group(0))
            reglas.append(regla)
    for t in ((_sin_nombres(crudo),) if crudo is not None else ()):   # IDIOMA, sin siglas ni nombres propios (T-161 r02)
        idioma = IDIOMA.search(t)
        if idioma:
            familias.append("IDIOMA")
            terminos.append(idioma.group(0))
            reglas.append("T-161 [PROPUESTO]: las guías se redactan en castellano; otra lengua no se revisa y se escala")


ESCRITURA = ("T-161 [PROPUESTO]: caracteres fuera de los permitidos (otra escritura, letras latinas sin base en el alfabeto "
             "del castellano, emojis); se escala")


def conflicto_del_item(item: dict) -> dict | None:
    """El ítem contradice una regla (None si no). Devuelve las familias, los términos que lo delatan, las reglas y los campos."""
    familias: list[str] = []
    terminos: list[str] = []
    reglas: list[str] = []
    campos: list[str] = []
    t = _normalizar(item.get("que_cambia", ""))
    _revisar_texto(t, True, familias, terminos, reglas, _texto(item.get("que_cambia", "")))
    for variante in _variantes(t):
        _revisar_texto(variante, True, familias, terminos, reglas)
    if familias:
        campos.append("que_cambia")
    for campo in CAMPOS_TEXTO[1:]:
        antes = len(familias)
        crudo = _texto(item.get(campo))
        normal = _normalizar(crudo)
        _revisar_texto(normal, False, familias, terminos, reglas, crudo)
        for variante in _variantes(normal):
            _revisar_texto(variante, False, familias, terminos, reglas)
        letras = _otra_escritura(crudo)
        if letras:
            familias.append("ESCRITURA")
            terminos += letras
            reglas.append(ESCRITURA)
        if len(familias) > antes:
            campos.append(campo)
    letras = _otra_escritura(_texto(item.get("que_cambia", "")))
    if letras:
        familias.append("ESCRITURA")
        terminos += letras
        reglas.append(ESCRITURA)
        if "que_cambia" not in campos:
            campos.insert(0, "que_cambia")
    if not familias:
        return None
    return {"familias": sorted(set(familias)), "terminos": list(dict.fromkeys(terminos)), "campos": campos,
            "reglas": list(dict.fromkeys(reglas + [R23]))}


def conflicto_para(item: dict, receptor: str | None) -> dict | None:
    """El conflicto del ítem para su receptor: el del texto y, si el receptor es un control (H-04), siempre conflicto."""
    c = conflicto_del_item(item)
    if receptor not in AGENTES_DE_CONTROL:
        return c
    base = c or {"familias": [], "terminos": [], "campos": [], "reglas": []}
    regla = (f"{receptor} es un control ({AGENTES_DE_CONTROL[receptor]}): una guía nunca lo dirige "
             "(T-161 [PROPUESTO]; 6.8 y 6.9 no dicen a quién se dirigen)")
    return {"familias": sorted(set(base["familias"]) | {"RECEPTOR_DE_CONTROL"}), "terminos": base["terminos"],
            "campos": base["campos"], "reglas": list(dict.fromkeys([regla] + [r for r in base["reglas"] if r != R23] + [R23]))}


def conflicto_de_leccion(leccion: dict) -> dict | None:
    """T-161 r02 (QA r01, H-01): una lección redactada por un modelo (AG-20) va a F6 y de ahí al contexto de todos los agentes;
    su `recomendacion` y su `observacion` pasan el detector con el criterio de los campos descriptivos (una lección habla de
    controles por oficio) antes de escribirse. None si no hay conflicto."""
    c = conflicto_del_item({"que_cambia": "", "donde_se_comprueba": leccion.get("recomendacion", ""),
                            "como_se_sabe": leccion.get("observacion", "")})
    if c is None:
        return None
    nombres = {"donde_se_comprueba": "recomendacion", "como_se_sabe": "observacion"}
    return {**c, "campos": [nombres.get(x, x) for x in c["campos"]]}


# ---------------------------------------------------------------------------------------------------------------------
def _fecha(valor: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(valor) if isinstance(valor, str) and re.fullmatch(FECHA, valor) else None
    except ValueError:
        return None


def _dia(valor: str) -> dt.date:
    f = _fecha(valor)
    if f is None:
        raise ValueError(f"fecha no válida {valor!r}")
    return f


def limites(cfg: dict | None) -> dict[str, int]:
    """Límites de una versión de guía (prompt del Orquestador 6.9), de `guias_orquestador` en la configuración."""
    return {k: int(parametro(cfg, f"guias_orquestador.{k}"))
            for k in ("max_items_por_version", "max_hallazgos_por_version", "caducidad_por_defecto_meses",
                      "max_caracteres_por_texto")}


def validar_cuerpo(cuerpo: Any, receptor: str | None, cfg: dict | None) -> list[str]:
    """Errores del cuerpo de un CT-18 de tipo GUIA (vacío si es válido): el esquema y, después, lo que el esquema no expresa."""
    errores = sorted(f"{'/'.join(str(p) for p in e.absolute_path) or '(raíz)'}: {e.message}" for e in _VALIDADOR.iter_errors(cuerpo))
    if errores:
        return errores
    lim = limites(cfg)
    gid, items = cuerpo["guia_id"], cuerpo["items"]
    if receptor is not None and (receptor not in TODOS or gid[4:8] != receptor.replace("-", "")):
        errores.append(f"guia_id {gid} no es del receptor {receptor} (GUI-AGnn-NNNN, versionado por agente)")
    if int(gid[-4:]) != cuerpo["version"]:
        errores.append(f"guia_id {gid} no corresponde a la versión {cuerpo['version']}")
    if cuerpo["sustituye"] is not None and (cuerpo["sustituye"][:8] != gid[:8] or int(cuerpo["sustituye"][-4:]) >= cuerpo["version"]):
        errores.append(f"sustituye {cuerpo['sustituye']} no es una versión anterior de la misma guía")
    if cuerpo["version"] == 1 and cuerpo["sustituye"] is not None:
        errores.append("la versión 1 no sustituye a ninguna")
    aplica = _fecha(cuerpo["fecha_aplicacion"])
    if aplica is None:
        errores.append(f"fecha_aplicacion no válida: {cuerpo['fecha_aplicacion']}")
    if len(items) > lim["max_items_por_version"]:
        errores.append(f"{len(items)} ítems: el máximo por versión es {lim['max_items_por_version']} (6.9)")
    hallazgos = {o for it in items for o in it["origen"] if o.startswith("HAL-")}
    if len(hallazgos) > lim["max_hallazgos_por_version"]:
        errores.append(f"{len(hallazgos)} hallazgos: el máximo por versión es {lim['max_hallazgos_por_version']} (6.9)")
    ids = [it["item_id"] for it in items]
    if len(set(ids)) != len(ids):
        errores.append("item_id repetido")
    for it in items:
        if not it["item_id"].startswith(gid + "-"):
            errores.append(f"{it['item_id']} no es un ítem de {gid}")
        for campo in ("que_cambia", "donde_se_comprueba", "como_se_sabe"):   # T-161 r02 (QA r01, H-05)
            if len(it[campo]) > lim["max_caracteres_por_texto"]:
                errores.append(f"{it['item_id']}: {campo} tiene {len(it[campo])} caracteres; el máximo es "
                               f"{lim['max_caracteres_por_texto']} (guias_orquestador.max_caracteres_por_texto)")
        cad = _fecha(it["caducidad"])
        if cad is None:
            errores.append(f"{it['item_id']}: caducidad no válida")
        elif aplica is not None and cad < aplica:
            errores.append(f"{it['item_id']}: caduca antes de su fecha de aplicación")
    return errores


def _mas_meses(f: dt.date, meses: int) -> dt.date:
    m = f.month - 1 + meses
    anio, mes = f.year + m // 12, m % 12 + 1
    for dia in range(f.day, 0, -1):   # el día 31 pasa al último día del mes de destino
        try:
            return dt.date(anio, mes, dia)
        except ValueError:
            continue
    raise ValueError(f"fecha no válida {f} + {meses} meses")   # pragma: no cover


class Guias:
    """Las guías CT-18 de un bloque: emisión (AG-18), revisión del receptor y guías aplicables por agente y run."""

    def __init__(self, bloque) -> None:
        self.b = bloque
        self._lock = threading.RLock()
        self._por_run: dict[tuple[str, str], dict[str, list[dict]]] = {}
        self._aplicadas: dict[str, dict[str, set[str]]] = {}

    # ---------------------------------------------------------------- lectura
    def todas(self, as_of=None) -> dict[str, dict]:
        """Estado de cada guía en HA (GUI-), la última entrada de cada una prevalece campo a campo."""
        return {k: v for k, v in self.b.almacen.estado("HA", as_of).items() if v.get("tipo_entrada") == "GUI"}

    def vigentes(self, agente: str | None = None, as_of=None) -> dict[str, dict]:
        """Guías emitidas (ISSUED) de un agente o de todos, sin revisarlas (la revisión se hace al cargarlas)."""
        return {k: v for k, v in sorted(self.todas(as_of).items())
                if v.get("estado") == "ISSUED" and (agente is None or v.get("agente") == agente)}

    @staticmethod
    def cuerpo(guia: dict) -> dict:
        """El cuerpo CT-18 de una guía guardada en HA (para volver a validarlo contra el esquema)."""
        return {"tipo_ct18": "GUIA", "acuse_requerido": True,
                **{k: copy.deepcopy(guia.get(k)) for k in ("guia_id", "version", "sustituye", "fecha_aplicacion", "items")}}

    # ---------------------------------------------------------------- emisión (Orquestador)
    def emitir(self, receptor: str, items: list[dict], as_of=None, fecha_aplicacion: str | None = None,
               motivo: str | None = None, *, simular_fallo_del_emisor: bool = False) -> dict:
        """El Orquestador emite la versión siguiente de la guía de `receptor` con `items` (cada uno con los campos de 6.9;
        `caducidad` es opcional y por defecto son dos trimestres). La guía vigente del agente pasa a SUPERSEDED. Valida antes
        de mutar: un cuerpo que no cumple el esquema o los límites se rechaza con `MensajeInvalido` y HA no cambia.
        T-161 (H-05): el emisor también hace el control doble y falla cerrado: un ítem en conflicto o un receptor que es un
        control se rechazan igual. `simular_fallo_del_emisor` (solo con el cliente simulado) deja pasar ese control para
        ejercer PB-48 («guía vigente que sugiere omitir la segunda pasada»); la entrada GUI- lo anota en `control_emisor`."""
        if simular_fallo_del_emisor and not isinstance(self.b.cliente, MockClient):
            raise MensajeInvalido("CT-18: la simulación del fallo del control del emisor solo se admite con el cliente simulado")
        with self._lock:
            hoy = dt.date.fromisoformat(str(as_of)[:10]) if as_of is not None else self.b.reloj.fecha
            aplica = fecha_aplicacion or hoy.isoformat()
            codigo = str(receptor).replace("-", "")
            todas = self.todas()
            previas = [v for v in todas.values() if v.get("agente") == receptor]
            version = 1 + max((int(v.get("version") or 0) for v in previas), default=0)
            gid = f"GUI-{codigo}-{version:04d}"
            if gid in todas:
                raise MensajeInvalido(f"{gid} ya existe en HA")
            vigentes = sorted(k for k, v in todas.items() if v.get("agente") == receptor and v.get("estado") == "ISSUED")
            sustituye = max(vigentes, key=lambda k: int(k[-4:])) if vigentes else None   # tras una RETIRADA no sustituye a nada
            meses = limites(self.b.cfg)["caducidad_por_defecto_meses"]
            fa = _fecha(aplica)
            if not isinstance(items, list):
                raise MensajeInvalido("CT-18: `items` debe ser una lista")
            cuerpo_items = []
            for n, it in enumerate(items, start=1):
                if not isinstance(it, dict):
                    raise MensajeInvalido("CT-18: cada ítem es un objeto")
                nuevo = {"item_id": f"{gid}-{n:02d}", **{k: copy.deepcopy(it[k]) for k in CAMPOS_ITEM if k in it}}
                if "caducidad" not in nuevo and fa is not None:
                    nuevo["caducidad"] = _mas_meses(fa, meses).isoformat()
                cuerpo_items.append(nuevo)
            cuerpo = {"tipo_ct18": "GUIA", "guia_id": gid, "version": version, "sustituye": sustituye, "fecha_aplicacion": aplica,
                      "items": cuerpo_items, "acuse_requerido": True}
            errores = validar_cuerpo(cuerpo, receptor, self.b.cfg)
            if errores:
                raise MensajeInvalido("CT-18 no cumple su esquema: " + "; ".join(errores))
            rechazos = self.control_emisor(receptor, cuerpo_items)
            if rechazos and not simular_fallo_del_emisor:
                raise MensajeInvalido("CT-18: el control doble del emisor (6.8) lo rechaza: " + "; ".join(rechazos))
            msg = self.b.mensajeria.crear("CT-18", "AG-18", receptor, cuerpo)    # sobre: canal (R2) y datos protegidos (R8)
            acuse = self.b.mensajeria.acuse(msg, receptor)
            entrada = {"tipo_entrada": "GUI", "id": gid, "agente": receptor,
                       **{k: v for k, v in cuerpo.items() if k not in ("tipo_ct18", "acuse_requerido")},
                       "msg_id": msg["msg_id"], "acuse": acuse["timestamp"], "estado": "ISSUED", "eficacia": None}
            if motivo:
                entrada["motivo"] = motivo
            if rechazos:
                entrada["control_emisor"] = {"simulado_fallo": True, "rechazos": rechazos}
            self.b.almacen.escribir("HA", "AG-18", entrada)
            for k in vigentes:
                self.b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": k, "estado": "SUPERSEDED", "sustituida_por": gid})
            self._por_run.clear()
            return {"guia_id": gid, "version": version, "sustituye": sustituye, "msg_id": msg["msg_id"], "acuse": acuse,
                    "items": [i["item_id"] for i in cuerpo_items]}

    @staticmethod
    def control_emisor(receptor: str, items: list[dict]) -> list[str]:
        """T-161 (H-04, H-05): motivos por los que el emisor no puede emitir estos ítems a `receptor` (vacío si puede)."""
        if receptor in AGENTES_DE_CONTROL:
            return [f"{receptor} es un control ({AGENTES_DE_CONTROL[receptor]}): ninguna guía lo dirige (T-161 [PROPUESTO])"]
        return [f"{it.get('item_id')}: {', '.join(c['familias'])} ({', '.join(c['terminos'][:4])})"
                for it in items for c in [conflicto_del_item(it)] if c]

    # ---------------------------------------------------------------- revisión del receptor y aplicación
    def cargar(self, as_of, run_id: str | None) -> dict[str, list[dict]]:
        """F0 de cada run: el receptor revisa las guías emitidas (control doble, 6.8) y se quedan las aplicables por agente.
        Un ítem en conflicto deja COR- y P3- en HA y se retira de la guía (R23). Si la revisión falla, no se aplica ninguna
        guía en el run (falla cerrado) y queda una incidencia."""
        hoy = dt.date.fromisoformat(str(as_of)[:10]) if as_of is not None else self.b.reloj.fecha
        clave = (run_id or "", hoy.isoformat())
        with self._lock:
            if clave in self._por_run:
                return self._por_run[clave]
            try:
                aplicables = self._revisar(hoy, run_id)
            except Exception as e:   # noqa: BLE001 - cualquier fallo deja el run sin guías, nunca con una sin revisar
                self.b.almacen.incidencia("HERRAMIENTA", f"Revisión de las guías CT-18 no disponible ({type(e).__name__}): no se "
                                          "aplica ninguna en este run", "AG-18", severidad="Operativa", run_id=run_id)
                aplicables = {}
            self._por_run[clave] = aplicables
            return aplicables

    def _revisar(self, hoy: dt.date, run_id: str | None) -> dict[str, list[dict]]:
        aplicables: dict[str, list[dict]] = {}
        for gid, g in self.vigentes(as_of=hoy).items():
            agente = str(g.get("agente"))
            errores = validar_cuerpo(self.cuerpo(g), agente, self.b.cfg)
            if errores:
                self.b.almacen.incidencia("HERRAMIENTA", f"{gid} no cumple el esquema del CT-18 y no se aplica: {'; '.join(errores)[:300]}",
                                          str(agente), severidad="Operativa", run_id=run_id)
                self.b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": gid, "estado": "RETIRADA",
                                                        "motivo": "no cumple el esquema del CT-18"})
                continue
            conflictos = [(it, c) for it in g["items"] for c in [conflicto_para(it, agente)] if c]   # T-161: receptor incluido
            if any(COMPROMETEN & set(c["familias"]) for _, c in conflictos):   # T-161 r02: instrucción repartida entre ítems
                en_conflicto = {it["item_id"] for it, _ in conflictos}
                conflictos += [(it, {"familias": ["GUIA_COMPROMETIDA"], "terminos": [], "campos": [],
                                     "reglas": [("6.9 (otro ítem de la misma guía inyecta, redefine o tacha instrucciones: la "
                                                 "guía entera es sospechosa)"), R23]})
                               for it in g["items"] if it["item_id"] not in en_conflicto]
            if conflictos:
                nueva = self._retirar(g, conflictos, hoy, run_id)
                if nueva is None:
                    continue
                g = nueva
            if _dia(g["fecha_aplicacion"]) > hoy:   # ya validadas por el esquema: `_dia` no devuelve None
                continue
            vivos = [it for it in g["items"] if _dia(it["caducidad"]) >= hoy]
            if not vivos:
                self.b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": g["guia_id"], "estado": "RETIRADA",
                                                        "motivo": "caducidad de todos sus ítems"})
                continue
            aplicables.setdefault(agente, []).extend(
                {"guia_id": g["guia_id"], **{k: copy.deepcopy(it[k]) for k in ("item_id", "tipo", "que_cambia", "donde_se_comprueba", "como_se_sabe")}}
                for it in vivos)
        return aplicables

    def _retirar(self, g: dict, conflictos: list[tuple[dict, dict]], hoy: dt.date, run_id: str | None) -> dict | None:
        """R23: el receptor no aplica el ítem, registra el conflicto (COR-) y lo escala (P3-, cola de tipo 3 de HA); el
        Orquestador reclasifica el ítem como tipo 3 y lo retira: versión nueva con el resto o, si no queda nada, RETIRADA.
        T-161 (H-03): idempotente. Si un run anterior ya registró el COR- de ese ítem de esa guía (y la retirada falló después),
        se reutiliza con su P3- (que se escribe solo si falta), sin duplicar nada en la cola de tipo 3 del operador."""
        agente, gid = g["agente"], g["guia_id"]
        retirados, p3s = [], []
        previos = {(e.get("entrada_corregida"), e.get("item_id")): e for e in self.b.almacen.leer("HA") if e.get("tipo_entrada") == "COR"}
        en_ha = self.b.almacen.estado("HA")
        for it, c in conflictos:
            previo = previos.get((gid, it["item_id"]))
            if previo is not None and previo.get("p3_id"):
                cor_id, p3_id = previo["id"], previo["p3_id"]
            else:
                cor_id, p3_id = self.b.almacen.nuevo_id("COR"), self.b.almacen.nuevo_id("P3-ORQ")
            if previo is None or not previo.get("p3_id"):
                self.b.almacen.escribir("HA", "AG-18", {
                    "tipo_entrada": "COR", "id": cor_id, "entrada_corregida": gid, "item_id": it["item_id"],
                    "motivo": (f"El ítem {it['item_id']} (tipo {it['tipo']}) contradice {', '.join(c['reglas'])}: «{it['que_cambia']}». "
                               f"No se aplica: manda la regla más restrictiva (R23) y se escala como tipo 3 ({p3_id})."),
                    "conflicto": c, "norma_aplicada": "la regla del Documento 0 que el ítem contradice (la más restrictiva, R23)",
                    "detectado_por": agente, "comunicado_a": [agente, "AG-18", "OPERADOR"], "p3_id": p3_id, "run_id": run_id})
            if p3_id not in en_ha:
                self.b.almacen.escribir("HA", "AG-18", {
                    "tipo_entrada": "P3", "id": p3_id, "origen": "ORQ", "detectado_por": agente,
                    "objeto": f"{it['item_id']} de {gid}: {it['que_cambia']}", "tipo_declarado": it["tipo"], "reclasificado_a": 3,
                    "evidencia": {"cor_id": cor_id, "guia_id": gid, "item_id": it["item_id"], "origen_item": it["origen"], **c},
                    "impacto": "El ítem no se aplica: manda la regla que contradice hasta que decida el operador (R23, 18.3)",
                    "pruebas_regresion": list(BATERIA_REGRESION),
                    "plan_reversion": "Si el operador la rechaza, el ítem sigue retirado; si la aprueba, el cambio se hace como tipo 3 "
                                      "(18.1), con sus pruebas de regresión, y no por una guía",
                    "npr": None, "estado": "PENDING_OPERATOR", "decision_operador": None, "run_id": run_id})
            retirados.append(it["item_id"])
            p3s.append(p3_id)
        quedan = [it for it in g["items"] if it["item_id"] not in retirados]
        motivo = f"retira {', '.join(retirados)} (reclasificados como tipo 3: {', '.join(p3s)})"
        if not quedan:
            self.b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": gid, "estado": "RETIRADA", "motivo": motivo})
            self._por_run.clear()
            return None
        r = self.emitir(agente, [{k: it[k] for k in CAMPOS_ITEM} for it in quedan], as_of=hoy,
                        fecha_aplicacion=g["fecha_aplicacion"], motivo=motivo)
        return self.todas()[r["guia_id"]]

    def para(self, agente: str, as_of, run_id: str | None) -> list[dict]:
        """Ítems aplicables de las guías del agente en este run (para su contexto); anota la guía como aplicada."""
        items = copy.deepcopy(self.cargar(as_of, run_id).get(agente, []))
        if items and run_id:
            with self._lock:
                self._aplicadas.setdefault(run_id, {}).setdefault(agente, set()).update(i["guia_id"] for i in items)
        return items

    def aplicadas(self, run_id: str) -> dict[str, list[str]]:
        """Guías aplicadas por agente en un run («el agente registra la guia_id aplicada en cada retorno», 6.9)."""
        with self._lock:
            return {a: sorted(g) for a, g in sorted(self._aplicadas.get(run_id, {}).items())}
