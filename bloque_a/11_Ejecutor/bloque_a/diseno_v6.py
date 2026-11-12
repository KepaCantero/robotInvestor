"""Diseño V6 del Bloque A (T-101): el rediseño aspirante con menos papeles de IA.

Se activa con `diseno: v6` (por defecto `v5`). Recoge la propuesta de Claude (`.docs/diseno/bloque_a/propuesta_claude.md`),
los cambios de la revisión C-01 de Astra que acepta la decisión de Claude (`decision_claude_c01.md`) y sus ideas nuevas:

- GC1 por código antes del Analista, con catálogo mínimo de señales por perfil, paso marcado de lo que no tiene señal
  medible y exploración sembrada para medir falsos negativos;
- Prospectiva una vez por ciclo, en lotes por tamaño y con control de cobertura por identificador (A-02);
- Contradictor solo de la selección provisional y de sus sustitutas; lo que no se ha podido criticar no se entrega (A-01);
- integración determinista antes de G3 y Sintetizador (AG-26) después, sobre el paquete validado;
- registro de cobertura del embudo y muestra de descartes con seguimiento contrafactual (A-05).

Las funciones reciben el `Bloque` y reutilizan sus piezas: los contratos, los archivos y las herramientas no cambian.
"""
from __future__ import annotations

import hashlib
import math
import re
from typing import Any

import pandas as pd

from . import sintesis as sint
from .configuracion import NOMBRE_CLASE, parametro
from .contratos import AGENTE_CLASE
from .herramientas.ht01_datos import DatosNoDisponibles, FugaDeInformacion

DISENOS = ("v5", "v6")
# Señales numéricas que calcula el Motor para cada ámbito (`Bloque.senales_clase`): las que puede usar GC1 por perfil (H-19)
SENALES_GC1 = ("senal_compuesta", "momentum_12_1", "pct_momentum_clase", "z_momentum_clase", "senal_tsmom", "vol_20d", "vol_ewma",
               "p_tendencia", "pendiente_sen_semanal", "riesgo_1a5", "mdd", "drawdown_actual", "z_precio_3a", "pct_precio_3a",
               "rent_1s", "rent_1m", "rent_3m", "rent_12m", "familias_concordantes")
BOLSA_GLOBAL = "V6_GLOBAL"   # bolsa de las llamadas de todo el ciclo (Prospectiva, Contradictor y Sintetizador)


def _entero(cfg, clave, minimo):
    v = parametro(cfg, f"v6.{clave}")
    if isinstance(v, bool) or not isinstance(v, int) or v < minimo:
        raise ValueError(f"v6.{clave} debe ser un entero ≥ {minimo} (es {v!r})")


def validar(cfg: dict) -> bool:
    """`diseno` debe ser «v5» o «v6» y, con la V6, su sección `v6` debe ser legible (falla cerrado al crear el Bloque; QA r01
    de T-101, H-07). Devuelve si el diseño es V6."""
    d = cfg.get("diseno", "v5")
    if d not in DISENOS:
        raise ValueError(f"`diseno` desconocido: {d!r} (v5 | v6)")
    if d != "v6":
        return False
    for clave, minimo in (("gc1.exploracion_celdas", 0), ("prospectiva.max_encargos_por_lote", 1),
                          ("contradictor.max_rondas_sustitucion", 0), ("cobertura.muestra_descartes", 0),
                          ("contradictor.max_evidencias", 1), ("contradictor.contrarreplica_max", 1),
                          ("cobertura.dias_max_espera_precio", 0)):
        _entero(cfg, clave, minimo)
    fr = parametro(cfg, "v6.auditoria_fraccion")
    if isinstance(fr, bool) or not isinstance(fr, (int, float)) or not 0 <= float(fr) <= 1:
        raise ValueError(f"v6.auditoria_fraccion debe estar entre 0 y 1 (es {fr!r})")
    if parametro(cfg, "v6.analista.base_conocimientos") not in ("ninguna", "completa"):
        raise ValueError("v6.analista.base_conocimientos debe ser «ninguna» o «completa»")
    if parametro(cfg, "v6.contradictor.proveedor") not in ("mismo", "otro"):
        raise ValueError("v6.contradictor.proveedor debe ser «mismo» u «otro»")
    if parametro(cfg, "v6.cobertura.horizonte_contrafactual") not in parametro(cfg, "horizontes"):
        raise ValueError("v6.cobertura.horizonte_contrafactual debe ser un horizonte de `horizontes`")
    from .configuracion import CLASES
    spp = ((cfg.get("v6") or {}).get("gc1") or {}).get("senal_por_perfil") or {}
    if not isinstance(spp, dict) or any(k not in CLASES or v not in SENALES_GC1 for k, v in spp.items()):
        raise ValueError(f"v6.gc1.senal_por_perfil debe ser {{tipo de activo: señal del Motor}}, con señales de {SENALES_GC1}")
    lim = parametro(cfg, "v6.sintetizador_limites")
    for k in ("regimen", "factor", "lectura", "texto_minimo", "preguntas", "limitaciones", "limitacion"):
        if isinstance(lim.get(k), bool) or not isinstance(lim.get(k), int) or lim[k] < 1:
            raise ValueError(f"v6.sintetizador_limites.{k} debe ser un entero ≥ 1")
    return True


def op(bloque, clave: str) -> Any:
    return parametro(bloque.cfg, f"v6.{clave}")


def activo(bloque, clave: str) -> bool:
    return bool(getattr(bloque, "v6", False)) and bool(op(bloque, clave))


def _sembrado(*partes) -> str:
    return hashlib.sha256("|".join(str(p) for p in partes).encode()).hexdigest()


def _ref(clase: str, f: dict) -> str:
    return f"{clase}:{f['proxy']}"


def _lotes(items: list, por_lote: int) -> list[list]:
    n = max(1, int(por_lote))
    return [items[i:i + n] for i in range(0, len(items), n)]


# ======================================================================================================
# Presupuesto: las llamadas de todo el ciclo salen de lo que cada tipo reservaba para ellas
# ======================================================================================================
def repartir_presupuesto(bloque, asign: dict[str, float], clases: list[str], fija: float | None = None) -> dict[str, float]:
    """Con Prospectiva y Contradictor por ciclo, la parte de `reparto_fases` de prospectiva y refutación de cada tipo pasa
    a una bolsa común del ciclo (`V6_GLOBAL`): el total no cambia (R5)."""
    if not activo(bloque, "prospectiva.global"):
        return asign
    rep = parametro(bloque.cfg, "presupuesto_uc.reparto_fases")
    fr = float(rep["prospectiva"]) + float(rep["refutacion"])
    out = dict(asign)
    if fija is not None:   # QA r02, H-18: un `presupuesto_override` de la bolsa del ciclo se respeta tal cual
        out[BOLSA_GLOBAL] = float(fija)
        return out
    out[BOLSA_GLOBAL] = 0.0
    for c in clases:
        parte = round(out[c] * fr, 6)
        out[c] = round(out[c] - parte, 6)
        out[BOLSA_GLOBAL] = round(out[BOLSA_GLOBAL] + parte, 6)
    return out


# ======================================================================================================
# GC1 por código (PA-04)
# ======================================================================================================
def gc1(bloque, clase: str, universo: list[dict], vigentes: list[dict], as_of) -> tuple[list[dict], dict]:
    """Filtra el universo que recibe el Analista. Pasan como mucho `seleccion.max_candidatas` ámbitos cuya señal llega a
    `seleccion.umbral_senal_gc1`; un ámbito sin señal medible no se descarta (pasa marcado: la falta de señal no prueba la
    falta de oportunidad); `v6.gc1.exploracion_celdas` de los que no pasan llegan igualmente, elegidos por una semilla del
    corte, para medir los falsos negativos; las vigentes siempre llegan. Devuelve el universo y el registro de GC1."""
    clave = (op(bloque, "gc1.senal_por_perfil") or {}).get(clase) or "senal_compuesta"
    umbral = float(parametro(bloque.cfg, "seleccion.umbral_senal_gc1"))
    maxc = int(parametro(bloque.cfg, "seleccion.max_candidatas"))
    n_expl = int(op(bloque, "gc1.exploracion_celdas"))
    from .orquestacion import simbolo_seguimiento
    simb_vig = {simbolo_seguimiento(v) for v in vigentes}
    con: list[dict] = []
    sin: list[dict] = []
    for u in universo:
        v = (u.get("senales") or {}).get(clave)
        # H-06 (QA r01): una señal NaN o infinita no es una señal medible: pasa marcada, no ordena ni descarta
        medible = isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))
        (con if medible else sin).append(u)
    orden = sorted(con, key=lambda u: (-float(u["senales"][clave]), u["simbolo"]))
    pasan = [u for u in orden if float(u["senales"][clave]) >= umbral][:maxc]
    ids_pasan = {u["simbolo"] for u in pasan}
    resto = [u for u in orden if u["simbolo"] not in ids_pasan]
    expl = sorted(resto, key=lambda u: _sembrado(pd.Timestamp(as_of).date(), clase, u["simbolo"]))[:n_expl]
    ids_expl = {u["simbolo"] for u in expl}
    marca = {}
    for u in pasan:
        marca[u["simbolo"]] = "PASA"
    for u in expl:
        marca[u["simbolo"]] = "EXPLORACION"
    for u in sin:
        marca[u["simbolo"]] = "SIN_SENAL_MEDIBLE"
    for u in universo:
        if u["simbolo"] in simb_vig and u["simbolo"] not in marca:
            marca[u["simbolo"]] = "VIGENTE"
    filtrado = []
    for u in universo:
        if u["simbolo"] in marca:
            filtrado.append({**u, "gc1": marca[u["simbolo"]]})
    descartes = [{"simbolo": u["simbolo"], "senal": round(float(u["senales"][clave]), 4),
                  "motivo": f"{clave} {float(u['senales'][clave]):.2f} < {umbral}" if float(u["senales"][clave]) < umbral
                  else f"fuera de las {maxc} candidatas con más señal"}
                 for u in resto if u["simbolo"] not in ids_expl and marca.get(u["simbolo"]) != "VIGENTE"]
    reg = {"clave_senal": clave, "umbral": umbral, "universo": len(universo), "pasan": sorted(ids_pasan),
           "exploracion": sorted(ids_expl), "sin_senal_medible": sorted(u["simbolo"] for u in sin),
           "vigentes": sorted(s for s, m in marca.items() if m == "VIGENTE"), "descartes": descartes, "falsos_negativos": []}
    return filtrado, reg


NOTA_GC1 = (" El ejecutor ya ha aplicado GC1 por código (diseño V6). Cada ámbito del universo lleva la marca `gc1`: PASA (su señal "
            "llega al umbral), EXPLORACION (no llega, pero se te ofrece para medir lo que el filtro deja escapar), "
            "SIN_SENAL_MEDIBLE (el Motor no tiene señal para él) o VIGENTE. Evalúa todos con la estrategia de tu tipo de activo: "
            "no descartes un ámbito EXPLORACION o SIN_SENAL_MEDIBLE solo por su señal; propónlo como finalista si tu análisis lo "
            "sostiene. En `cribado`, `paso_gc1` es tu juicio sobre el ámbito, no la marca del ejecutor.")


def gc1_decisiones(an: dict) -> list[dict] | None:
    """QA r02, H-16: con GC1 por código, las decisiones de GC1 (embudo del paquete y F5) son las del código, no el `paso_gc1`
    del Analista. None si el tipo no pasó por GC1 por código."""
    g = an.get("gc1")
    if not g:
        return None
    out = [{"objeto": x, "resultado": True, "motivo": f"{g['clave_senal']} ≥ {g['umbral']}"} for x in g["pasan"]]
    out += [{"objeto": x, "resultado": False, "motivo": "no llega al umbral: se ofrece al Analista como exploración"} for x in g["exploracion"]]
    out += [{"objeto": x, "resultado": False, "motivo": "sin señal medible: se ofrece al Analista sin descartar"} for x in g["sin_senal_medible"]]
    out += [{"objeto": d["simbolo"], "resultado": False, "motivo": d["motivo"]} for d in g["descartes"]]
    return out


def gc1_falsos_negativos(out: dict) -> None:
    """Un ámbito de exploración que el Analista convierte en finalista es un falso negativo de GC1 (idea 5)."""
    reg = out.get("gc1")
    if not reg:
        return
    expl = set(reg["exploracion"])
    reg["falsos_negativos"] = sorted({f["proxy"] for f in out["finalistas"] if f["proxy"] in expl})


# ======================================================================================================
# Prospectiva una vez por ciclo (A-02)
# ======================================================================================================
INSTR_PROSPECTIVA = ("Para cada encargo, construye escenarios por horizonte y propone un pronóstico verificable por horizonte pedido: "
                     "vista (alcista/bajista para DIRECCIONAL; relativa_favorable/relativa_desfavorable para RELATIVO frente a la "
                     "referencia), probabilidad interna (0,05–0,95), afirmación inequívoca y escenario. Devuelve un resultado por "
                     "cada «ref» recibida: los encargos son de tipos de activo distintos y no comparten razonamiento.")


def prospectiva_global(bloque, grupos: dict[str, list[dict]], as_of, run_id, presupuesto, hz_interes) -> dict:
    """Prospectiva de las finalistas de todos los tipos, en lotes de `v6.prospectiva.max_encargos_por_lote` (o uno por tipo
    si `lotes_por_perfil`). Un encargo sin resultado se pide una vez más en un lote aparte; si sigue faltando, la finalista
    queda sin pronóstico, marcada y declarada (nunca como pronóstico negativo)."""
    certs = [c["celda"] for c in bloque.evaluador.certificados_vigentes(as_of) if c["celda"].get("metodo")]
    encargos, por_ref = [], {}
    for clase, finales in grupos.items():
        for f in finales:
            ref_i = bloque._referencia(clase, f["proxy"])
            tipo_p = "DIRECCIONAL" if ref_i is None or ref_i == f["proxy"] else "RELATIVO"
            hs = [h for h in f.get("horizontes_aplicables", []) if h in hz_interes]
            f["_tipo_pronostico"], f["_referencia"] = tipo_p, (None if tipo_p == "DIRECCIONAL" else ref_i)
            r = _ref(clase, f)
            por_ref[r] = f
            encargos.append({"ref": r, "clase": clase, "opp_id": f.get("opp_id"), "tesis": f["tesis"], "proxy": f["proxy"],
                             "referencia_indice": f["_referencia"], "tipo_pronostico": tipo_p, "horizontes": hs,
                             "datos": {k: v for k, v in f["senales"].items() if k != "calc_ids"},
                             "catalizadores_conocidos": f.get("catalizadores", []), "invalidacion_propuesta": f.get("invalidacion", []),
                             "certificado_r13": {h: False for h in hs},
                             "metodos_certificados_por_horizonte": {h: sorted(c["metodo"] for c in certs if c["clase"] == clase
                                                                             and c["horizonte"] == h) for h in hs}})
    if not encargos:
        return {"lotes": 0, "encargos": 0, "omitidos": []}
    if op(bloque, "prospectiva.lotes_por_perfil"):
        lotes = [[e for e in encargos if e["clase"] == c] for c in grupos if any(e["clase"] == c for e in encargos)]
    else:
        lotes = _lotes(encargos, op(bloque, "prospectiva.max_encargos_por_lote"))
    res: dict[str, dict] = {}
    n_lotes = 0

    def _llamar(lote, reintento=False):
        nonlocal n_lotes
        n_lotes += 1
        msg = {"encargos": lote, "fecha_limite_informacion": str(pd.Timestamp(as_of).date())}
        if reintento:   # QA r01 de T-101, H-04: otro encargo, que no sale de la caché HT-06 con la misma respuesta incompleta
            msg["reintento_de_cobertura"] = {"motivo": "estos encargos no volvieron en la primera llamada", "refs": [e["ref"] for e in lote]}
        bloque.mensajeria.crear("CT-12", "AG-02", "AG-10", msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(BOLSA_GLOBAL)})
        r = bloque._invocar("AG-10", "CT-12", msg, "PROSPECTIVA", INSTR_PROSPECTIVA, as_of, run_id, None, "prospectiva",
                            presupuesto, bolsa=BOLSA_GLOBAL)
        pedidos = {e["ref"] for e in lote}
        for x in (r.datos or {}).get("resultados", []) if r and r.datos else []:
            if isinstance(x, dict) and x.get("ref") in pedidos and x["ref"] not in res:
                res[x["ref"]] = x

    for lote in lotes:
        _llamar(lote)
    faltan = [e for e in encargos if e["ref"] not in res]
    if faltan:   # control de cobertura: una vez más, solo con lo que falta
        for lote in _lotes(faltan, op(bloque, "prospectiva.max_encargos_por_lote")):
            _llamar(lote, reintento=True)
    omitidos = []
    for r, f in por_ref.items():
        f["_prospectiva"] = res.get(r)
        if f["_prospectiva"] is None:
            f["_prospectiva_omitida"] = True
            omitidos.append(r)
    return {"lotes": n_lotes, "encargos": len(encargos), "omitidos": sorted(omitidos)}


# ======================================================================================================
# Contradictor de la selección provisional y de sus sustitutas (A-01)
# ======================================================================================================
INSTR_REFUTACION = ("Refuta de forma independiente cada tesis: objeciones graduadas (fuerte, moderada, débil) con id OBJ-<ref>-nn, "
                    "tipo, argumento, evidencia y qué la resolvería; veredicto global por tesis. Devuelve un resultado por cada «ref».")


def refutacion_global(bloque, grupos: dict[str, list[dict]], nivel: dict[str, str], as_of, run_id, presupuesto) -> dict:
    """La misma refutación de PA-05 que la V5 (objeciones con id del código, respuesta del Analista acusado y contrarréplica
    con evidencia verificable de la propia opción), pero con una llamada al Contradictor por lote para todos los tipos.
    Una opción que el Contradictor no devuelve ni en un segundo intento queda sin crítica y no se puede entregar."""
    from .orquestacion import INSTR
    todas = []
    for clase, fs in grupos.items():
        bloque._filtrar_evidencia(fs, as_of)
        todas += [(clase, f) for f in fs]
    if not todas:
        return {"criticadas": [], "sin_respuesta": []}
    peticiones = {}
    for clase, f in todas:
        peticiones[_ref(clase, f)] = {
            "ref": _ref(clase, f), "opp_id": f.get("opp_id"), "clase": clase, "nivel": nivel.get(clase),
            "afirmaciones_verificables": [{"horizonte": p.get("horizonte"), "vista": p.get("vista"), "afirmacion": p.get("afirmacion")}
                                          for p in (f.get("_prospectiva") or {}).get("pronosticos", [])],
            "evidencias": [{"fuente": p.get("fuente"), "afirmacion": p["afirmacion"], "direccion": p.get("direccion")}
                           for p in f["_piezas"]][:op(bloque, "contradictor.max_evidencias")],
            "calculos": f["senales"].get("calc_ids", [])}
    nivel_msg = "N3" if "N3" in nivel.values() else "N2"
    res: dict[str, dict] = {}

    def _llamar(lote, reintento=False):
        msg = {"peticiones": lote, "nivel": nivel_msg}
        if reintento:   # H-04
            msg["reintento_de_cobertura"] = {"motivo": "estas peticiones no volvieron en la primera llamada", "refs": [p["ref"] for p in lote]}
        bloque.mensajeria.crear("CT-13", "AG-02", "AG-11", msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(BOLSA_GLOBAL)})
        r = bloque._invocar("AG-11", "CT-13", msg, "REFUTACION", INSTR_REFUTACION, as_of, run_id, None, "refutacion", presupuesto,
                            bolsa=BOLSA_GLOBAL)
        pedidos = {p["ref"] for p in lote}
        for x in (r.datos or {}).get("resultados", []) if r and r.datos else []:
            if isinstance(x, dict) and x.get("ref") in pedidos and x["ref"] not in res:
                res[x["ref"]] = x

    por_lote = op(bloque, "prospectiva.max_encargos_por_lote")
    for lote in _lotes(list(peticiones.values()), por_lote):
        _llamar(lote)
    faltan = [p for r, p in peticiones.items() if r not in res]
    if faltan:
        for lote in _lotes(faltan, por_lote):
            _llamar(lote, reintento=True)
    pendientes: dict[str, list] = {}
    sin_respuesta = []
    for clase, f in todas:
        x = res.get(_ref(clase, f))
        f["_critica_pendiente"] = False
        if x is None:
            f["_refutacion"], f["_objeciones"], f["_sin_critica"] = None, [], True
            sin_respuesta.append(_ref(clase, f))
            continue
        f["_refutacion"], f["_objeciones"], f["_criticada"] = x, [], True
        for nn, o in enumerate(x.get("objeciones", []), start=1):
            oid = f"OBJ-{f['proxy']}-{nn:02d}"
            f["_objeciones"].append({"objecion_id": oid, "id_modelo": o.get("id"), "tipo": o.get("tipo"), "fuerza": o["fuerza"],
                                     "resumen": o["argumento"], "que_la_resolveria": o.get("que_la_resolveria"),
                                     "respuesta": None, "resuelta": False})
            if o["fuerza"] in ("fuerte", "moderada"):
                pendientes.setdefault(clase, []).append({"ref": f["proxy"], "objecion_id": oid, "fuerza": o["fuerza"], "argumento": o["argumento"],
                                                         "que_la_resolveria": o.get("que_la_resolveria"), "dimensiones_E": f["dimensiones"].get("E"),
                                                         "evidencia_disponible": bloque._evidencia_verificable(f)})
    replicas = []
    for clase, pend in pendientes.items():   # el Analista acusado responde: una llamada por tipo, con su kit
        agente = AGENTE_CLASE[clase]
        msg2 = {"clase": clase, "fase": "RESPUESTA_OBJECIONES", "nivel": nivel.get(clase), "opciones_vigentes": [], "lecciones": [],
                "objeciones": pend}
        bloque.mensajeria.crear("CT-06", "AG-02", agente, msg2, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(clase)})
        r2 = bloque._invocar(agente, "CT-06", msg2, "RESPUESTA_OBJECIONES", INSTR["RESPUESTA_OBJECIONES"], as_of, run_id, clase,
                             "respuesta_objeciones", presupuesto)
        resp = {x["objecion_id"]: x for x in (r2.datos or {}).get("respuestas", [])} if r2 and r2.datos else {}
        for f in grupos[clase]:
            verificables = set(bloque._evidencia_verificable(f))
            for o in f.get("_objeciones", []):
                x = resp.get(o["objecion_id"])
                if x and (x.get("respuesta") or "").strip():
                    o["respuesta"] = x["respuesta"]
                    if o["fuerza"] != "fuerte":
                        o["resuelta"] = True
                        continue
                    citada = [str(e) for e in (x.get("evidencia_citada") or []) if str(e) in verificables]
                    o["evidencia_citada"] = citada
                    if x.get("resuelta") and citada:
                        replicas.append({"ref": f["proxy"], "objecion_id": o["objecion_id"], "argumento": o["resumen"],
                                         "que_la_resolveria": o.get("que_la_resolveria"), "respuesta": x["respuesta"],
                                         "evidencia_citada": [bloque._contenido_evidencia(f, e, run_id) for e in citada]})
    if replicas:
        msg3 = {"peticiones": [], "contrarreplicas": replicas, "nivel": nivel_msg}
        bloque.mensajeria.crear("CT-13", "AG-02", "AG-11", msg3, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(BOLSA_GLOBAL)})
        r3 = bloque._invocar("AG-11", "CT-13", msg3, "CONTRARREPLICA", INSTR["CONTRARREPLICA"], as_of, run_id, None, "refutacion",
                             presupuesto, bolsa=BOLSA_GLOBAL)
        enviadas = {x["objecion_id"] for x in replicas}
        conf = {x["objecion_id"]: x for x in (r3.datos or {}).get("resultados", [])
                if isinstance(x, dict) and x.get("objecion_id") in enviadas} if r3 and r3.datos else {}
        for _, f in todas:
            for o in f.get("_objeciones", []):
                if o["fuerza"] == "fuerte" and o["objecion_id"] in conf:
                    o["resuelta"] = conf[o["objecion_id"]].get("resuelta") is True
                    o["contrarreplica"] = str(conf[o["objecion_id"]].get("motivo") or "")[:op(bloque, "contradictor.contrarreplica_max")]
    for _, f in todas:
        if f.get("_refutacion") is not None:
            f["_veredicto"] = bloque._veredicto_refutacion(f)
            f["_veredicto_contradictor"] = (f.get("_refutacion") or {}).get("veredicto_global")
    return {"criticadas": sorted(_ref(c, f) for c, f in todas if f.get("_criticada")), "sin_respuesta": sorted(sin_respuesta)}


def _top3(sel: dict) -> set[str]:
    return {t["opp_id"] for t in sel["seleccion"]["top3"]}


def seleccion_con_critica(bloque, clases, analisis, clusteres, nivel, as_of, run_id, hz_interes, presupuesto) -> tuple[dict, dict]:
    """A-01: selección provisional → crítica → selección final. Las finalistas nuevas de un tipo N2/N3 llegan a la selección
    provisional con la crítica pendiente; el Contradictor critica las que quedan en algún top-3; si alguna cae, la que entra
    pasa la misma crítica, hasta `v6.contradictor.max_rondas_sustitucion` rondas de sustitución. Al final, lo que no se ha
    podido criticar deja de ser elegible y no se entrega."""
    if not activo(bloque, "contradictor.solo_seleccion"):
        raise ValueError("v6.contradictor.solo_seleccion: false no está soportado con la Prospectiva global")
    for c in clases:
        if nivel[c] in ("N2", "N3"):
            for f in analisis[c]["finalistas"]:
                if f.get("_gc3") and f.get("_refutacion") is None:
                    f["_critica_pendiente"] = True

    def _seleccionar_todo():
        sel = {c: bloque._seleccionar(c, analisis[c], clusteres, as_of, run_id, hz_interes) for c in clases}
        bloque._deduplicar_entre_tipos(sel)
        return sel

    rondas = []
    max_rondas = int(op(bloque, "contradictor.max_rondas_sustitucion"))
    sel = _seleccionar_todo()
    for ronda in range(max_rondas + 1):
        grupos = {c: [f for f in sel[c]["candidatos"] if f["opp_id"] in _top3(sel[c]) and f.get("_critica_pendiente")] for c in clases}
        grupos = {c: fs for c, fs in grupos.items() if fs}
        if not grupos:
            break
        r = refutacion_global(bloque, grupos, nivel, as_of, run_id, presupuesto)
        rondas.append({"ronda": ronda, "tipo": "PROVISIONAL" if ronda == 0 else "SUSTITUCION", **r})
        sel = _seleccionar_todo()
    # Lo que sigue con la crítica pendiente deja de ser elegible; se declara lo que, por eso, no se entrega (estaba en un top-3)
    sin_critica: list[dict] = []
    no_criticadas: list[dict] = []
    for c in clases:
        top = _top3(sel[c])
        for f in analisis[c]["finalistas"]:
            if f.get("_critica_pendiente"):
                f["_critica_pendiente"], f["_sin_critica"] = False, True
                (sin_critica if f.get("opp_id") in top else no_criticadas).append({"clase": c, "proxy": f["proxy"], "opp_id": f.get("opp_id")})
    # QA r01 de T-101, H-03: lo que se envió al Contradictor (estaba en un top-3) y no volvió en dos intentos no se entrega
    # y se declara, aunque ya no sea elegible
    sin_respuesta = sorted({r for ronda in rondas for r in ronda.get("sin_respuesta", [])})
    if sin_critica:
        sel = _seleccionar_todo()
    return sel, {"rondas": rondas, "sin_critica": sin_critica, "sin_respuesta": sin_respuesta,
                 "no_criticadas_fuera_del_top3": no_criticadas}


# ======================================================================================================
# Integración determinista (antes de G3) y Sintetizador (después)
# ======================================================================================================
def integracion_determinista(bloque, seleccion, analisis, as_of) -> dict:
    """La integración que hacía el Analizador (AG-02), sin modelo: el régimen de cada tipo y los cambios frente al run
    anterior. La lectura del conjunto y los factores los escribe el Sintetizador sobre el paquete ya validado."""
    reg = [f"{NOMBRE_CLASE[c]}: {analisis[c].get('regimen')}" for c in seleccion if (analisis[c].get("regimen") or "").strip()]
    anterior = [r for r in bloque.almacen.leer("F5", as_of) if r.get("tipo_entrada") == "RUN"]
    previo = (anterior[-1].get("top3_por_clase") if anterior else None) or {}
    cambios = []
    for c, s in seleccion.items():
        ahora_ids = [t["opp_id"] for t in s["seleccion"]["top3"]]
        antes = [x if isinstance(x, str) else x.get("opp_id") for x in (previo.get(c) or [])]
        entran, salen = [x for x in ahora_ids if x not in antes], [x for x in antes if x and x not in ahora_ids]
        if entran or salen:
            cambios.append(f"{NOMBRE_CLASE[c]}: entran {', '.join(entran) or 'ninguna'}; salen {', '.join(salen) or 'ninguna'}")
    return {"regimen_macro": ("; ".join(reg) if reg else "Régimen por tipo no disponible en este ciclo")[:op(bloque, "sintetizador_limites")["regimen"]],
            "factores_dominantes": [], "lectura_conjunto": "Integración determinista (diseño V6): la lectura del conjunto la "
            "escribe el Sintetizador sobre el paquete validado.", "preguntas_sugeridas": [], "limitaciones": [],
            "cambios_vs_anterior": "; ".join(cambios) if cambios else "Sin cambios en los top-3 frente al run anterior."}


INSTR_SINTESIS = ("Sobre el paquete ya validado: escribe la integración (régimen macro común, el factor que domina cada clúster, "
                  "la lectura del conjunto, preguntas sugeridas para el Broker y limitaciones) y los textos llanos del informe "
                  "visual (tres frases de «la semana en 30 segundos», por cada opción «por qué» y «qué podría salir mal» "
                  "(≤ 20 palabras, sin jerga o explicada entre paréntesis), motivos llanos de los tipos sin tres opciones, un "
                  "glosario de hasta 5 términos y una frase honesta sobre el historial). Índice Fernández-Huerta ≥ 70. No cambies "
                  "la selección ni las cifras: vienen calculadas y validadas.")
_CAMPOS_REDACCION = ("frases_30s", "tarjetas", "motivos_llanos", "glosario", "frase_historial")


# QA r01 de T-101, H-09, y r02, H-12: un texto del Sintetizador con una probabilidad numérica (R13) o con la compra o venta de un
# instrumento concreto (R21) no se toma. Son reglas por patrón; un nombre propio sin patrón (p. ej. «entrar en Tesla») no se
# detecta: lo revisa el Auditor por muestreo y queda declarado como límite.
_NUM = r"\d{1,3}(?:[.,]\d+)?"
_PROB = r"(?:probabilidad(?:es)?|posibilidad(?:es)?|opciones|chances?)"
_R13 = (re.compile(rf"{_NUM}\s*(?:%|por\s+ciento)\s+de\s+{_PROB}", re.IGNORECASE),
        re.compile(rf"\b{_PROB}\b[^.;:!?]{{0,40}}?\b(?:0[.,]\d+|{_NUM}\s*(?:%|por\s+ciento))(?!\s*(?:%\s*)?de\s+las\s+veces)",
                   re.IGNORECASE))
_VERBO = r"(?:compr(?:a|ar|e|en|amos)|vend(?:e|er|a|an|emos)|adquiri(?:r|d)|sobrepond(?:erar|era|ere)|infrapond(?:erar|era|ere)|la\s+compra\s+de|la\s+venta\s+de)"
_R21 = (re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}\d\b"),                                                    # un ISIN
        re.compile(r"\b[A-Z][\w&.-]+(?:\s+[A-Z][\w&.-]+)*\s+(?:Corp|Corporation|Inc|Incorporated|plc|PLC|AG|NV|SE|S\.A\.)\b"),
        re.compile(r"\bbonos?\b[^.;]{0,60}?\bvencimiento\s+(?:en\s+)?(?:19|20)\d{2}\b", re.IGNORECASE))  # una emisión concreta
_CODIGO_VERBO = re.compile(rf"\b{_VERBO}\b(?:\s+(?:acciones|bonos|participaciones|t[íi]tulos)\s+de)?(?:\s+[\wÁÉÍÓÚáéíóúñ]+){{0,2}}?\s*\(?\$?([A-Z]{{1,5}}(?:\.[A-Z]{{1,3}})?)\)?", re.IGNORECASE)
_CODIGO_PARENTESIS = re.compile(r"\(\$?([A-Z]{1,5}(?:\.[A-Z]{1,3})?)\)")


def texto_prohibido(t, permitidos=frozenset()) -> str | None:
    """«R13», «R21» o None para un texto del Sintetizador. `permitidos`: códigos que no son instrumentos (divisas, tipos de
    activo, siglas de segmentos y los símbolos del universo)."""
    if not isinstance(t, str):
        return None
    if any(r.search(t) for r in _R13):
        return "R13"
    if any(r.search(t) for r in _R21) or sint._UNITARIA.search(t):
        return "R21"
    for m in _CODIGO_VERBO.finditer(t):   # «comprar AAPL», «compra acciones de Apple (AAPL)», «la compra de MSFT»
        cod = m.group(1)
        if cod.isupper() and cod not in permitidos:
            return "R21"
    # con un verbo de compra o venta, un código entre paréntesis ajeno
    if re.search(rf"\b{_VERBO}\b", t, re.IGNORECASE) and any(c not in permitidos for c in _CODIGO_PARENTESIS.findall(t)):
        return "R21"
    return None


def permitidos_r21(bloque) -> frozenset:
    simbolos = set(bloque.universo["simbolo"].astype(str))
    if "subyacente" in bloque.universo:
        simbolos |= {str(x) for x in bloque.universo["subyacente"].dropna()}
    return frozenset(op(bloque, "filtro_r21_codigos")) | simbolos


def _textos(x) -> list:
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [t for v in x.values() for t in _textos(v)]
    if isinstance(x, list):
        return [t for v in x for t in _textos(v)]
    return []


def _aplicar_integracion(paquete: dict, d: dict, lim: dict, permitidos=frozenset()) -> list[str]:
    """Solo se toman textos (el Sintetizador no puede cambiar la selección, las puntuaciones, las fechas ni las cifras), con las
    longitudes de `v6.sintetizador_limites`, y nunca uno que incumpla R13 o R21. Devuelve los campos descartados."""
    descartados = []

    def _ok(campo, t):
        if not isinstance(t, str) or len(t.strip()) < lim["texto_minimo"]:
            return False
        regla = texto_prohibido(t, permitidos)
        if regla:
            descartados.append(f"{campo} ({regla})")
            return False
        return True
    if _ok("regimen_macro", d.get("regimen_macro")):
        paquete["regimen_macro"] = d["regimen_macro"].strip()[:lim["regimen"]]
    fact = {str(x.get("cluster_id")): str(x["factor"]).strip() for x in d.get("factores_dominantes") or []
            if isinstance(x, dict) and _ok("factores_dominantes", x.get("factor"))}
    for c in paquete.get("clusteres_exposicion", []):
        if c["cluster_id"] in fact:
            c["factor_dominante"] = fact[c["cluster_id"]][:lim["factor"]]
    preg = [x.strip() for x in d.get("preguntas_sugeridas") or [] if _ok("preguntas_sugeridas", x)][:lim["preguntas"]]
    if preg:
        paquete["preguntas_sugeridas"] = preg
    if _ok("lectura_conjunto", d.get("lectura_conjunto")):
        paquete["x_lectura_conjunto"] = d["lectura_conjunto"].strip()[:lim["lectura"]]
    nuevas = [f"Sintetizador: {x.strip()}"[:lim["limitacion"]] for x in d.get("limitaciones") or [] if _ok("limitaciones", x)][:lim["limitaciones"]]
    if descartados:
        nuevas.append("Textos del Sintetizador descartados por R13 o R21: " + ", ".join(dict.fromkeys(descartados)))
    if nuevas:
        paquete["limitaciones"] = [x for x in paquete["limitaciones"] if not x.startswith("Ninguna limitación")] + nuevas
    return descartados


def _redaccion_segura(bloque, paquete, d, permitidos=frozenset()) -> dict:
    """Los textos llanos del Sintetizador; si alguno incumple R13 o R21, se usan los textos por defecto y se declara (H-09)."""
    if not d:
        return bloque.redaccion.textos_por_defecto(paquete)
    red = {k: d[k] for k in _CAMPOS_REDACCION}
    malas = sorted({r for r in (texto_prohibido(t, permitidos) for t in _textos(red)) if r is not None})
    if malas:
        paquete["limitaciones"] = [x for x in paquete["limitaciones"] if not x.startswith("Ninguna limitación")] + [
            f"Textos llanos del Sintetizador descartados por {', '.join(malas)}: se usan los textos por defecto"]
        return bloque.redaccion.textos_por_defecto(paquete)
    return red


def sintetizar(bloque, paquete, extras, as_of, run_id, presupuesto, estado_run) -> tuple[dict, dict, dict]:
    """El Sintetizador (AG-26) en una llamada sobre el paquete validado por G3; después, la generación determinista de los
    entregables con su segunda pasada de HT-09 (esquema JSON, coherencia y legibilidad). Si el índice de legibilidad no
    llega, una reescritura, como con el Redactor."""
    msg = {"paquete_sintesis": sint.mensaje_redactor(paquete), "clusteres": [c["cluster_id"] for c in paquete.get("clusteres_exposicion", [])],
           "regimenes": paquete.get("regimen_macro"), "cambios_vs_anterior": paquete.get("x_cambios_vs_anterior")}
    bloque.mensajeria.crear("CT-15", "AG-02", "AG-26", {"paquete_sintesis": msg["paquete_sintesis"]}, run_id=run_id,
                            presupuesto={"uc": presupuesto.asignado.get("COMUN")})
    r = bloque._invocar("AG-26", "CT-15", msg, "SINTESIS", INSTR_SINTESIS, as_of, run_id, None, "redaccion", presupuesto, bolsa="COMUN")
    d = r.datos if r and r.datos else None
    lim = op(bloque, "sintetizador_limites")
    perm = permitidos_r21(bloque)
    if d:
        _aplicar_integracion(paquete, d, lim, perm)
    red = _redaccion_segura(bloque, paquete, d, perm)
    entreg, g3b = bloque.redaccion.generar(bloque, paquete, extras, red, as_of, run_id, estado_run)
    if g3b["dictamen"] == "BLOQUEADO" and any(c == "C12" for c in g3b.get("bloqueos", [])):
        msg2 = {**msg, "reescritura": {"fernandez_huerta": g3b.get("legibilidad"), "frases_largas": g3b.get("frases_largas", [])}}
        r2 = bloque._invocar("AG-26", "CT-15", msg2, "SINTESIS", INSTR_SINTESIS + " Reescribe: el índice no alcanza 70.", as_of, run_id,
                             None, "redaccion", presupuesto, bolsa="COMUN")
        if r2 and r2.datos:
            red = _redaccion_segura(bloque, paquete, r2.datos, perm)
            entreg, g3b = bloque.redaccion.generar(bloque, paquete, extras, red, as_of, run_id, estado_run)
    return entreg, g3b, red


# ======================================================================================================
# Registro de cobertura del embudo y muestra de descartes (A-05, ideas 3 y 4)
# ======================================================================================================
def _precio(bloque, simbolo, fecha) -> float | None:
    try:
        return float(bloque.proveedor.valor_en(simbolo, fecha)[1])
    except (DatosNoDisponibles, FugaDeInformacion, KeyError, TypeError, ValueError, IndexError):
        return None


def registrar_cobertura(bloque, run_id, as_of, clases, analisis, seleccion, info_prosp, info_critica) -> dict:
    """Una entrada COB- en HA por run: para cada tipo, hasta dónde llegó cada candidata y por qué se quedó; y la muestra de
    descartes con su precio en la fecha de corte, para el seguimiento contrafactual."""
    if not activo(bloque, "cobertura.registrar"):
        return {}
    n_muestra = int(op(bloque, "cobertura.muestra_descartes"))
    omitidas = set((info_prosp or {}).get("omitidos", []))
    sin_critica = {(x["clase"], x["proxy"]) for x in (info_critica or {}).get("sin_critica", [])}
    sin_respuesta = set((info_critica or {}).get("sin_respuesta", []))
    por_clase = {}
    for c in clases:
        an, s = analisis[c], seleccion[c]
        top = _top3(s)
        ev = {e["opp_id"]: e for e in s["evaluadas"]}
        filas = []
        for d in (an.get("gc1") or {}).get("descartes", []):
            filas.append({"simbolo": d["simbolo"], "fase": "GC1", "motivo": d["motivo"]})
        for f in an["finalistas"]:
            if not f.get("_gc2"):
                fase, motivo = "GC2", "E provisional, mecanismo o datos insuficientes"
            elif not f.get("_gc3"):
                fase, motivo = "GC3", "fuera de las finalistas con más RK"
            elif _ref(c, f) in omitidas:
                fase, motivo = "PROSPECTIVA", "sin pronóstico: omitido por Prospectiva dos veces (declarado, no negativo)"
            elif _ref(c, f) in sin_respuesta:   # QA r01 de T-101, H-03
                fase, motivo = "CRITICA", "el Contradictor no la devolvió en dos intentos: no se entrega (A-01)"
            elif (c, f["proxy"]) in sin_critica:
                fase, motivo = "CRITICA", "sin crítica del Contradictor: no se entrega (A-01)"
            elif f.get("opp_id") in top:
                fase, motivo = "SELECCION_FINAL", "en el top-3"
            elif f.get("_sin_critica"):
                fase, motivo = "SELECCION", "no llegó a un top-3 mientras había crítica disponible: no criticada y no elegible"
            else:
                e = ev.get(f.get("opp_id")) or {}
                mot = "; ".join(m.get("codigo", "") for m in e.get("motivos_no_elegible", [])) if not e.get("elegible", True) else "RK menor que las elegidas"
                fase, motivo = "SELECCION", mot or "no elegida"
            filas.append({"simbolo": f["proxy"], "opp_id": f.get("opp_id"), "fase": fase, "motivo": motivo,
                          "criticada": bool(f.get("_criticada")), "exploracion": f["proxy"] in set((an.get("gc1") or {}).get("exploracion", []))})
        # QA r01 de T-101, H-01: también lo que el Analista recibió y no propuso, y las vigentes (mantenidas o cerradas)
        g = an.get("gc1") or {}
        finalistas = {f["proxy"] for f in an["finalistas"]}
        motivos_an = {str(d.get("nombre")): d.get("motivo") for d in an.get("descartadas", []) if isinstance(d, dict)}
        en_top = {x.get("proxy") for x in s["candidatos"] if x.get("opp_id") in top}
        vigentes_sim = set(g.get("vigentes", [])) | {x.get("proxy") for x in s["candidatos"] if x.get("_vigente") or x.get("_arrastre")}
        for sim in sorted(set(g.get("pasan", [])) | set(g.get("exploracion", [])) | set(g.get("sin_senal_medible", []))):
            # QA r02, H-14: una vigente que sigue en el top-3 tiene su fila de selección, no la de «no propuesta»
            if sim not in finalistas and sim not in en_top and sim not in vigentes_sim:
                filas.append({"simbolo": sim, "fase": "ANALISTA", "exploracion": sim in set(g.get("exploracion", [])),
                              "motivo": f"el Analista no la propuso como finalista ({motivos_an.get(sim) or 'sin motivo declarado'})"})
        por_opp = {f.get("opp_id") for f in an["finalistas"]}
        for x in s["candidatos"]:
            if x.get("opp_id") in top and x.get("opp_id") not in por_opp:
                filas.append({"simbolo": x.get("proxy"), "opp_id": x["opp_id"], "fase": "SELECCION_FINAL", "vigente": True,
                              "criticada": bool(x.get("_criticada")), "motivo": "vigente mantenida en el top-3 (arrastre verificado)"})
        for x in s.get("cerradas", []):
            filas.append({"opp_id": x["opp_id"], "simbolo": None, "fase": "CIERRE", "vigente": True,
                          "motivo": f"vigente cerrada: {x.get('motivo_cierre')} ({x.get('comentario')})"})
        # QA r02, H-13: la rotación exploratoria de un ciclo ligero (N1) y lo que el Analista propone de ella (alta en F3)
        expl_f3 = {(f.get("indicador_seguimiento") or {}).get("simbolo") for f in an.get("exploratorias", [])}
        for sim in an.get("rotacion", []):
            if sim in expl_f3:
                filas.append({"simbolo": sim, "fase": "EXPLORATORIA_F3", "exploracion": True,
                              "motivo": "rotación exploratoria del ciclo ligero: el Analista la propone y queda en F3 como CANDIDATA"})
            elif sim not in en_top:
                filas.append({"simbolo": sim, "fase": "ROTACION", "exploracion": True,
                              "motivo": "rotación exploratoria del ciclo ligero: el Analista no la propone"})
        descartes = [x for x in filas if x["fase"] not in ("SELECCION_FINAL", "CIERRE", "EXPLORATORIA_F3") and x.get("simbolo")
                     and x["simbolo"] not in en_top]
        muestra = sorted(descartes, key=lambda x: _sembrado(run_id, c, x["simbolo"]))[:n_muestra]
        fecha = str(pd.Timestamp(as_of).date())
        # QA r02, H-15: también las vigentes arrastradas, con su símbolo y su precio
        elegidas = [{"opp_id": x["opp_id"], "simbolo": x.get("proxy"), "precio": _precio(bloque, x.get("proxy"), as_of) if x.get("proxy") else None}
                    for x in s["candidatos"] if x.get("opp_id") in top]
        por_clase[c] = {"filas": filas, "gc1": {k: v for k, v in (an.get("gc1") or {}).items() if k != "descartes"},
                        "muestra_descartes": [{"simbolo": x["simbolo"], "fase": x["fase"], "precio": _precio(bloque, x["simbolo"], as_of)}
                                              for x in muestra],
                        "elegidas": elegidas, "fecha": fecha}
    entrada = {"tipo_entrada": "COBERTURA", "id": bloque.almacen.nuevo_id("COB"), "run_id": run_id, "fecha": str(pd.Timestamp(as_of).date()),
               "horizonte_contrafactual": op(bloque, "cobertura.horizonte_contrafactual"),
               "prospectiva": info_prosp or {}, "critica": info_critica or {}, "clases": por_clase}
    bloque.almacen.escribir("HA", "AG-18", entrada)
    return entrada


def _fecha_vencimiento(bloque, fecha, horizonte) -> pd.Timestamp:
    from .herramientas.ht05_planificador import fecha_resolucion
    return pd.Timestamp(fecha_resolucion(pd.Timestamp(fecha), horizonte, parametro(bloque.cfg, "horizontes")))


def resolver_contrafactual(bloque, as_of, run_id) -> list[dict]:
    """Idea 4: cuando vence el horizonte de una muestra de descartes, compara, sin IA y con los datos de HT-01 hasta la fecha
    de hoy, la rentabilidad de los descartes muestreados con la de las opciones elegidas del mismo tipo y fecha. Escribe una
    entrada CTF- por cobertura resuelta (una sola vez)."""
    hechas = {e.get("cobertura_id") for e in bloque.almacen.leer("HA") if e.get("tipo_entrada") == "CONTRAFACTUAL"}
    out = []
    hoy = pd.Timestamp(as_of)
    for e in bloque.almacen.leer("HA", as_of):
        if e.get("tipo_entrada") != "COBERTURA" or e["id"] in hechas:
            continue
        try:
            vence = _fecha_vencimiento(bloque, e["fecha"], e["horizonte_contrafactual"])
        except (KeyError, TypeError, ValueError):   # horizonte o fecha ilegibles: no se resuelve (falla cerrado)
            continue
        if vence > hoy:
            continue
        clases: dict[str, dict[str, Any]] = {}
        for c, d in e["clases"].items():
            def _rent(x, vence=vence):
                if not x.get("simbolo") or not x.get("precio"):
                    return None
                p1 = _precio(bloque, x["simbolo"], vence)
                return None if p1 is None else round(p1 / x["precio"] - 1, 6)
            items = list(d.get("muestra_descartes", [])) + list(d.get("elegidas", []))
            rd = [r for r in (_rent(x) for x in d.get("muestra_descartes", [])) if r is not None]
            re_ = [r for r in (_rent(x) for x in d.get("elegidas", [])) if r is not None]
            media_e = sum(re_) / len(re_) if re_ else None
            medibles = sum(1 for x in items if x.get("simbolo") and x.get("precio"))
            clases[c] = {"descartes": len(rd), "elegidas": len(re_), "sin_precio": medibles - len(rd) - len(re_),
                         "rent_media_descartes": round(sum(rd) / len(rd), 6) if rd else None,
                         "rent_media_elegidas": round(media_e, 6) if media_e is not None else None,
                         "descartes_que_superan": sum(1 for r in rd if media_e is not None and r > media_e),
                         # QA r02, H-20: cada tipo dice si se pudo medir
                         "estado": "RESUELTO" if rd or re_ else ("SIN_DATOS" if medibles else "SIN_MUESTRA")}
        # QA r01 de T-101, H-10: si al vencer no hay ningún precio de lo que se podía medir, se espera al ciclo siguiente
        # (sin datos no hay conclusión); con datos parciales se resuelve y se cuenta lo que faltó (`sin_precio`)
        estado = "RESUELTO"
        if any(v["sin_precio"] for v in clases.values()) and not any(v["descartes"] + v["elegidas"] for v in clases.values()):
            # QA r02, H-20: se espera como mucho `dias_max_espera_precio` días; después se cierra como NO_RESOLUBLE
            if hoy <= vence + pd.Timedelta(days=int(op(bloque, "cobertura.dias_max_espera_precio"))):
                continue
            estado = "NO_RESOLUBLE"
        ctf = {"tipo_entrada": "CONTRAFACTUAL", "id": bloque.almacen.nuevo_id("CTF"), "run_id": run_id, "cobertura_id": e["id"],
               "fecha_muestra": e["fecha"], "fecha_resolucion": str(vence.date()), "estado": estado, "clases": clases}
        bloque.almacen.escribir("HA", "AG-18", ctf)
        out.append(ctf)
    return out


def auditar_este_run(bloque, run_id: str) -> bool:
    """Auditor por muestreo sembrado (V6): audita la fracción `v6.auditoria_fraccion` de los runs."""
    h = int(hashlib.sha256(run_id.encode()).hexdigest(), 16) % 10000
    return h < int(10000 * float(op(bloque, "auditoria_fraccion")))


def limitaciones_diseno(bloque) -> list[str]:
    """Lo que la V6 declara de sí misma en cada informe."""
    out = []
    if bloque.v6 and op(bloque, "contradictor.proveedor") == "otro" and "AG-11" not in bloque.agentes.clientes:
        out.append("Contradictor del mismo proveedor de IA: el segundo proveedor no está configurado (decisión 2 de la tanda 1); "
                   "la independencia del contraste es menor de la prevista")
    elif bloque.v6 and "AG-11" not in bloque.agentes.clientes:
        out.append("Contradictor del mismo proveedor de IA que el resto del bloque (segundo proveedor aún sin contratar)")
    if bloque.v6 and not op(bloque, "curacion_llm"):
        out.append("Curación determinista: independencia de las raíces por fuente declarada, sin evaluación semántica (la revisa "
                   "el Auditor por muestreo)")
    return out

