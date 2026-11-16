"""T-158 · Guías de mejora del Orquestador (CT-18, tipos 1 y 2) en el ejecutor del Bloque A.

Fuentes (kit de contexto): Documento 0 V5.1 (0.2, R23, 5.1, 6.1 CT-18, 18.1 y 18.3; el Anexo B remite los campos de CT-18 al
prompt del Orquestador), prompt del Orquestador V5.0 (4.5, forma del mensaje; 6.8, reclasificación obligatoria; 6.9, guías),
prompt del Analizador V5.0 («aplicas las de tipo 1 y 2 si no contradicen el Documento 0; … la registras y no la aplicas») y
esquema de HA V2.0 (4.4 GUI-, 4.8 P3- y COR-, 5 estados). Plan de pruebas V3.0: PB-48.

- `ESQUEMA_CT18_GUIA`: el cuerpo de un CT-18 de tipo GUIA. El esquema es la definición: `validar_cuerpo` lo aplica al emitir y
  otra vez antes de aplicar una guía guardada en HA. La mensajería (`contratos.py`) sigue validando solo el sobre (canal, R8),
  como hasta ahora, para no cambiar los formatos congelados.
- `conflicto_del_item`: el control doble del receptor (6.8: «El agente receptor repite la verificación»). Un ítem que toca lo
  que una guía nunca puede tocar (6.9) o lo que la reclasificación obligatoria hace de tipo 3 (6.8) está en conflicto.
- `Guias`: el Orquestador emite (`emitir`); al empezar cada run el receptor revisa las guías vigentes (`cargar`): cada ítem en
  conflicto deja un COR- y un P3- en HA y el Orquestador lo retira de la guía (versión nueva o RETIRADA). Lo que queda llega al
  contexto del agente receptor (`para`); nunca a HT-03, a las puertas ni a G3, que son código (R23 por construcción).
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
from .contratos import TODOS, MensajeInvalido

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
# Control doble del receptor: qué ítems contradicen una regla
# ---------------------------------------------------------------------------------------------------------------------
# [PROPUESTO] (T-158). Se lee solo `que_cambia` (la acción del ítem, 6.9), en minúsculas y sin tildes. Tres familias:
# 1. Tipo 3 por la reclasificación obligatoria (6.8): toca pesos, escalas, anclas, topes, umbrales, bandas, puertas,
#    esquemas, prioridades entre reglas, destinos, canales, el catálogo de comprobaciones o los estados de madurez.
# 2. Relaja un control que una guía nunca altera (6.9: corroboración, verificación, registro, seguridad, historial) o una
#    regla del Documento 0 (9.1 segunda pasada, R12 refutación): nombra el control y una acción que lo quita o rebaja.
# 3. Prohibido (6.9): pide credenciales o modificar un prompt o un contrato.
# Un falso positivo retira el ítem y lo escala (prudente); un falso negativo solo llega como contexto al modelo, porque la
# elegibilidad, las puertas y G3 son código que no lee guías.
TIPO_3 = (r"\bpesos?\b", r"\bescalas?\b", r"\banclas?\b", r"\btopes?\b", r"\bumbral(?:es)?\b", r"\bbandas?\b",
          r"\bpuertas?\b", r"\bps[1-8]\b", r"\bg[1-4]\b", r"\bgc[0-4]\b", r"\besquemas?\b", r"\bprioridad(?:es)? entre (?:las )?reglas\b",
          r"\bdestinos?\b", r"\bcanal(?:es)?\b", r"\bcatalogo de comprobaciones\b", r"\bestados? de madurez\b")
CONTROLES = (
    (r"\bsegunda pasada\b", "9.1 (banda marginal: segunda pasada)"),
    (r"\bcorrobor\w*|\braices?\b", "R10 y PS1 (corroboración)"),
    (r"\bverific\w*|\bcomprob\w*|\bcomprueb\w*|\bvalid\w*|\bcontrol(?:es)?\b", "R16 (los controles nunca se recortan)"),
    (r"\bregistr\w*|\bhistorial\w*|\btrazab\w*|\banot\w*", "R7 y R24 (registro y trazabilidad)"),
    (r"\bseguridad\b", "R8 y sección 17 (seguridad)"),
    (r"\brefut\w*|\bobjecion\w*|\bcontrari[ao]s\b|\bautocritic\w*|\binvalidacion\w*", "R12 (autocrítica obligatoria)"),
    (r"\bevidencias?\b", "R7 (trazabilidad de la evidencia)"),
)
RELAJA = re.compile(
    r"\bomit\w*|\bomision\w*|\bsalt(?:a|ar|arse|ate|e|en)\b|\bprescind\w*|\bsuprim\w*|\belimin\w*|\bquit\w*|\brelaj\w*"
    r"|\brebaj\w*|\breduc\w*|\bdesactiv\w*|\bignor\w*|\bobvi\w*|\bevit\w*|\bdej(?:a|ar|e|es|en)? de\b"
    r"|\bno (?:es |son )?(?:necesari\w*|obligatori\w*|imprescindible\w*)|\bno hace falta\b"
    r"|\bno\b(?: \w+){0,2} (?:aplic|apliqu|exig|exij|hac|hag|realiz|realic|registr|anot|comprob|comprueb|verific|verifiqu"
    r"|corrobor|ped|pid|ejecut|document|requer|requier|repet|repit|valid|refut)\w*"
    r"|\bsin (?:la |el |las |los )?(?:segunda|verific|comprob|registr|corrobor|refut|valid|control)\w*"
    r"|\bbasta(?:n|ra)? con\b|\bsuficiente con\b|\buna sola (?:fuente|raiz|pasada)\b"
    r"|\bmenos (?:fuentes|raices|comprobaciones|verificaciones|controles)\b|\bopcional\w*")
CREDENCIALES = re.compile(r"\bcredencial\w*|\bcontrasen\w*|\bpassword\w*|\bapi[ _-]?keys?\b|\bclaves? (?:de )?(?:la )?api\b"
                          r"|\btoken(?:s)? de acceso\b|\baccess[ _-]?token\w*")
PROMPT_O_CONTRATO = re.compile(r"\bprompt\w*|\bcontratos?\b|\bct-[0-9]{2}\b")
CAMBIO = re.compile(r"\b(?:modific|cambi|edit|reescrib|sustitu|actualiz|ampli|anad|quit|elimin|retir)\w*")


def _normalizar(texto: Any) -> str:
    t = unicodedata.normalize("NFKD", str(texto))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t.lower()).strip()


def conflicto_del_item(item: dict) -> dict | None:
    """El ítem contradice una regla (None si no). Devuelve las familias, los términos que lo delatan y las reglas."""
    t = _normalizar(item.get("que_cambia", ""))
    familias, terminos, reglas = [], [], []
    tipo3 = [m.group(0) for p in TIPO_3 for m in [re.search(p, t)] if m]
    if tipo3:
        familias.append("TIPO_3")
        terminos += tipo3
        reglas.append("18.1 (tipo 3) y reclasificación obligatoria (6.8 del prompt del Orquestador)")
    relaja = RELAJA.search(t)
    if relaja:
        tocados = [(m.group(0), r) for p, r in CONTROLES for m in [re.search(p, t)] if m]
        if tocados:
            familias.append("RELAJA_CONTROL")
            terminos += [relaja.group(0)] + [x for x, _ in tocados]
            reglas += [r for _, r in tocados]
    cred = CREDENCIALES.search(t)
    if cred:
        familias.append("PROHIBIDO")
        terminos.append(cred.group(0))
        reglas.append("R8 y 6.2.5 (una guía nunca pide credenciales, 6.9)")
    pc, cambio = PROMPT_O_CONTRATO.search(t), CAMBIO.search(t)
    if pc and cambio:
        familias.append("PROHIBIDO")
        terminos += [cambio.group(0), pc.group(0)]
        reglas.append("18.1 (cambiar un prompt o un contrato es tipo 3; 6.9)")
    if not familias:
        return None
    return {"familias": sorted(set(familias)), "terminos": list(dict.fromkeys(terminos)),
            "reglas": list(dict.fromkeys(reglas + ["R23 (manda la más restrictiva mientras se escala)"]))}


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
            for k in ("max_items_por_version", "max_hallazgos_por_version", "caducidad_por_defecto_meses")}


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
               motivo: str | None = None) -> dict:
        """El Orquestador emite la versión siguiente de la guía de `receptor` con `items` (cada uno con los campos de 6.9;
        `caducidad` es opcional y por defecto son dos trimestres). La guía vigente del agente pasa a SUPERSEDED. Valida antes
        de mutar: un cuerpo que no cumple el esquema o los límites se rechaza con `MensajeInvalido` y HA no cambia."""
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
            msg = self.b.mensajeria.crear("CT-18", "AG-18", receptor, cuerpo)    # sobre: canal (R2) y datos protegidos (R8)
            acuse = self.b.mensajeria.acuse(msg, receptor)
            entrada = {"tipo_entrada": "GUI", "id": gid, "agente": receptor,
                       **{k: v for k, v in cuerpo.items() if k not in ("tipo_ct18", "acuse_requerido")},
                       "msg_id": msg["msg_id"], "acuse": acuse["timestamp"], "estado": "ISSUED", "eficacia": None}
            if motivo:
                entrada["motivo"] = motivo
            self.b.almacen.escribir("HA", "AG-18", entrada)
            for k in vigentes:
                self.b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": k, "estado": "SUPERSEDED", "sustituida_por": gid})
            self._por_run.clear()
            return {"guia_id": gid, "version": version, "sustituye": sustituye, "msg_id": msg["msg_id"], "acuse": acuse,
                    "items": [i["item_id"] for i in cuerpo_items]}

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
            conflictos = [(it, c) for it in g["items"] for c in [conflicto_del_item(it)] if c]
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
        Orquestador reclasifica el ítem como tipo 3 y lo retira: versión nueva con el resto o, si no queda nada, RETIRADA."""
        agente, gid = g["agente"], g["guia_id"]
        retirados, p3s = [], []
        for it, c in conflictos:
            cor_id, p3_id = self.b.almacen.nuevo_id("COR"), self.b.almacen.nuevo_id("P3-ORQ")
            self.b.almacen.escribir("HA", "AG-18", {
                "tipo_entrada": "COR", "id": cor_id, "entrada_corregida": gid, "item_id": it["item_id"],
                "motivo": (f"El ítem {it['item_id']} (tipo {it['tipo']}) contradice {', '.join(c['reglas'])}: «{it['que_cambia']}». "
                           f"No se aplica: manda la regla más restrictiva (R23) y se escala como tipo 3 ({p3_id})."),
                "conflicto": c, "norma_aplicada": "la regla del Documento 0 que el ítem contradice (la más restrictiva, R23)",
                "detectado_por": agente, "comunicado_a": [agente, "AG-18", "OPERADOR"], "p3_id": p3_id, "run_id": run_id})
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
