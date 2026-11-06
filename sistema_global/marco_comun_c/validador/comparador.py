"""D — comparador de candidatos (código de referencia V0.1).

Ordena sobres CT-G-02 ya aceptados por el Orquestador. Determinista, sin LLM. D no re-valida el sobre entero (lo hizo
el Orquestador): lee solo los campos que usa y falla cerrado si falta alguno. Solo compara dentro de una misma clase de
comparabilidad (Q, S, K); no mezcla clases.

La referencia de toda comparación es no hacer nada: el benchmark de la cartera (Constitución, P5). Cada candidato se mide por
su exceso sobre la rentabilidad de la referencia en su propio horizonte; si ninguno la supera con margen, D se abstiene
(decision_global ABSTENERSE). Un candidato solo también se compara: con la referencia.
Puntuación = exceso esperado por unidad de riesgo × confianza normalizada por el tope de su clase × factor de evidencia [PROPUESTO].
T-17 (V0.35): D no se fía de lo que declara el productor. (1) Costes: si el sobre declara menos coste de entrar y salir (o de
mantener) que el suelo de su clase, o no lo puede estimar, D descuenta la diferencia de todos los escenarios (la mitad del suelo de
ida y vuelta por pierna). (2) Riesgo: el riesgo es la mayor de la pérdida del peor escenario, el p05 declarado (ambos tras costes)
y la pérdida hasta el stop (más el coste de ida y vuelta): un escenario adverso más suave que el propio stop no abarata el riesgo.
Sin stop legible, un LARGO cuenta con perderlo todo (d_riesgo_sin_stop_largo_pct) y un CORTO o NEUTRAL no se ordena (SIN_STOP).
(3) Horizontes: el exceso se anualiza (×365/h) y el riesgo se escala con la raíz del tiempo (×√(365/h)), con su suelo aplicado
antes de anualizar; el mínimo para no abstenerse también es anual. Si el primero cambia sin esa normalización, la decisión es
AJUSTADA; la dominancia exige ser mejor o igual en las dos unidades. (4) Confianza: sin un doble análisis hecho que no discrepe,
la confianza no pasa de d_factor_tope_sin_doble_analisis × el tope de la clase. Cada candidato lista en `ajustes` lo que D cambió
respecto a lo declarado (COSTE_SUELO, RIESGO_P05, RIESGO_STOP, RIESGO_SIN_STOP, CONFIANZA_DISCREPA, CONFIANZA_SIN_DOBLE).
Escenarios SUPUESTO son opinión, no dato: no se ordenan (ESCENARIOS_SUPUESTO). Si dos candidatos quedan demasiado cerca, o el
primero cambia al variar las ponderaciones (sensibilidad), la decisión es AJUSTADA y D no elige. Cada candidato lista quién lo domina.
Códigos: OK; D-01 entrada inválida.
Motivos de exclusión por candidato: FORMA, DUPLICADO, EXCLUSION_DURA, CADUCADO, SIN_ESCENARIOS, SIN_RETORNO_POSITIVO,
NO_SUPERA_REFERENCIA, ESCENARIOS_SUPUESTO, SIN_CONFIANZA, SIN_STOP.
La referencia se compone al horizonte del candidato. Los «aspirantes» de un grupo son el primero, los empatados con él y los que
serían primeros con otra ponderación: entre ellos elige el operador cuando la decisión es AJUSTADA.
"""
from __future__ import annotations

import math
import re
from collections import Counter

from validar_sobre import VERSIONES_CONOCIDAS, _dt

from parametros import PARAMETROS as _P   # noqa: E402  (valores [PROPUESTO] versionados, T-25)

PESO_EVIDENCIA = dict(_P["d_peso_evidencia"])   # [PROPUESTO]
MARGEN_AJUSTADO = _P["d_margen_ajustado"]   # [PROPUESTO] diferencia relativa por debajo de la cual no se declara un claro ganador
RIESGO_MIN_PCT = _P["d_riesgo_min_pct"]     # [PROPUESTO] suelo del denominador, para no premiar escenarios casi sin pérdida
TOL = 1e-6
ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
CLASES = ("Q", "S", "K")
TOPE_CLASE = dict(_P["d_tope_confianza_clase"])   # [PROPUESTO] topes de confianza por clase (D-03 del operador)
EXCESO_MIN_PCT = _P["d_exceso_min_pct"]    # [PROPUESTO] exceso mínimo sobre la referencia, en puntos porcentuales, para no abstenerse
REFERENCIA_EFECTIVO = {"benchmark_ref": "BENCH-EFECTIVO", "rentabilidad_anual_pct": 0.0}   # [PROPUESTO] valor de partida
COSTE_SUELO_IV = dict(_P["d_coste_suelo_ida_vuelta_pb"])   # T-17 [PROPUESTO]
COSTE_SUELO_MANT = dict(_P["d_coste_suelo_mant_anual_pb"])   # T-17 [PROPUESTO]
FACTOR_SIN_DOBLE = _P["d_factor_tope_sin_doble_analisis"]   # T-17 [PROPUESTO]
RIESGO_SIN_STOP_LARGO = _P["d_riesgo_sin_stop_largo_pct"]   # T-17 [PROPUESTO]


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


RENT_MIN, RENT_MAX = _P["d_rentabilidad_plausible_pct"]   # [PROPUESTO] rentabilidad neta plausible en %; fuera de ahí el dato es sospechoso
REF_MIN, REF_MAX = _P["d_referencia_rango_pct"]   # [PROPUESTO] rentabilidad anual admisible de una referencia
EXCL = {"sanciones", "invertibilidad", "acceso"}


def _pb(p, campo):
    """Coste declarado en el sobre, en puntos básicos; lo que no se puede leer o no se estimó cuenta como 0 (y D aplica el suelo)."""
    c = (p.get("costes") or {}).get(campo)
    if isinstance(c, dict) and c.get("unidad") == "pb" and _num(c.get("valor")) and c["valor"] >= 0 and c.get("estado") != "NO_ESTIMABLE":
        return float(c["valor"])
    return 0.0


def _perdida_al_stop(p, direccion):
    """Pérdida en % desde el límite de entrada hasta el stop declarados, o None si no se puede calcular."""
    es = p.get("entrada_salida") or {}
    lim = ((es.get("entrada") or {}).get("limite") or {}).get("valor")
    st = (es.get("stop") or {}).get("valor")
    if not (_num(lim) and _num(st) and lim > 0 and st > 0) or direccion not in ("LARGO", "CORTO", "NEUTRAL"):
        return None
    if direccion == "NEUTRAL":   # el validador lo trata como CORTO; D no adivina el sentido y toma la distancia
        r = abs(st - lim) / lim * 100.0
    else:
        r = (lim - st) / lim * 100.0 if direccion == "LARGO" else (st - lim) / lim * 100.0
    return r if r > 0 else None


def _referencia_ok(r):
    return (isinstance(r, dict) and set(r) == {"benchmark_ref", "rentabilidad_anual_pct"} and isinstance(r["benchmark_ref"], str)
            and ID.match(r["benchmark_ref"]) is not None and _num(r["rentabilidad_anual_pct"]) and REF_MIN <= r["rentabilidad_anual_pct"] <= REF_MAX)


def _leer(c, ahora, ref=REFERENCIA_EFECTIVO):
    """Devuelve (datos, motivo_de_exclusion). Nunca lanza."""
    try:
        s = c["sobre"]
        if s.get("version_esquema") not in VERSIONES_CONOCIDAS:   # T-27: una versión retirada no se interpreta
            return None, "FORMA"
        p = s["payload"]
        ident = p["identificacion"]
        inst = ident["instrumento"]
        if not (isinstance(c["expediente_id"], str) and ID.match(c["expediente_id"]) and ident["clase_comparabilidad"] in CLASES
                and isinstance(inst, str) and inst.strip() and ident["direccion"] in ("LARGO", "CORTO", "NEUTRAL")
                and s["expediente_id"] == c["expediente_id"]):
            return None, "FORMA"
        ex = p["exclusiones_duras"]
        if not (isinstance(ex, dict) and set(ex) == EXCL):
            return None, "FORMA"
        rechazado = s.get("resultado_politica", {}).get("resultado") == "RECHAZADO"
        if rechazado or any(v != "OK" for v in ex.values()):
            return None, "EXCLUSION_DURA"
        if not (isinstance(ahora, str) and _dt(s["emitido_en"]) <= _dt(ahora) < _dt(s["valid_until"])):
            return None, "CADUCADO"
        ent = (p.get("entrada_salida") or {}).get("entrada")
        if isinstance(ent, dict) and not _dt(ahora) < _dt(ent["ventana_hasta"]):   # T-27: sin ventana de entrada no hay candidato
            return None, "CADUCADO"
        c2 = p["capa2"]
        esc = c2["escenarios"]
        if c2["estado"] not in ("ESTIMADO", "VERIFICADO", "SUPUESTO") or not isinstance(esc, list) or len(esc) < 2:
            return None, "SIN_ESCENARIOS"
        if not all(isinstance(e, dict) and _num(e["probabilidad"]) and 0 <= e["probabilidad"] <= 1 and _num(e["rentabilidad_neta_pct"])
                   and RENT_MIN <= e["rentabilidad_neta_pct"] <= RENT_MAX and isinstance(e["horizonte_dias"], int) and not isinstance(e["horizonte_dias"], bool)
                   and e["horizonte_dias"] >= 1 for e in esc) or abs(math.fsum(e["probabilidad"] for e in esc) - 1.0) > TOL:
            return None, "SIN_ESCENARIOS"
        con_peso = [e for e in esc if e["probabilidad"] > 0]
        if len(con_peso) < 2:
            return None, "SIN_ESCENARIOS"
        conf, tope = p["capa3"]["confianza"], p["capa3"]["tope_confianza"]
        pr = p["evidencia"]["proporcion"]
        if not (_num(conf) and _num(tope) and 0 <= conf <= tope <= TOPE_CLASE[ident["clase_comparabilidad"]] + 1e-6 and isinstance(pr, dict) and set(pr) == set(PESO_EVIDENCIA)
                and all(_num(pr[k]) and 0 <= pr[k] <= 1 for k in PESO_EVIDENCIA) and abs(math.fsum(pr.values()) - 1.0) <= 1e-3):
            return None, "FORMA"
        clase = ident["clase_comparabilidad"]
        horizonte = math.fsum(e["probabilidad"] * e["horizonte_dias"] for e in esc)
        ajustes = []
        # T-17 (1) costes: lo que falte hasta el suelo de la clase se descuenta de todos los escenarios. El suelo de ida y vuelta se
        # reparte a partes iguales entre la entrada y la salida, para que una entrada cara no tape una salida sin estimar
        medio = COSTE_SUELO_IV[clase] / 2.0
        ent_pb, sal_pb, mant_decl = _pb(p, "entrada"), _pb(p, "salida"), _pb(p, "mantenimiento_anual")
        coste_extra = (max(0.0, medio - ent_pb) + max(0.0, medio - sal_pb) + max(0.0, COSTE_SUELO_MANT[clase] - mant_decl) * horizonte / 365.0) / 100.0
        if coste_extra > 0:
            ajustes.append("COSTE_SUELO")
        coste_iv_pct = (max(ent_pb, medio) + max(sal_pb, medio)) / 100.0
        esperado = math.fsum(e["probabilidad"] * e["rentabilidad_neta_pct"] for e in esc) - coste_extra
        if esperado <= 0:   # con retorno esperado no positivo no hay nada que ordenar: dividir una pérdida por más riesgo la haría parecer menor
            return None, "SIN_RETORNO_POSITIVO"
        peor = min(e["rentabilidad_neta_pct"] for e in con_peso) - coste_extra   # un escenario de probabilidad cero no cuenta
        liston = ((1 + ref["rentabilidad_anual_pct"] / 100.0) ** (horizonte / 365.0) - 1) * 100.0   # no hacer nada durante el mismo plazo, compuesto
        exceso = esperado - liston
        k_h = 365.0 / horizonte
        if not exceso * k_h > EXCESO_MIN_PCT:   # T-17: el mínimo es anual, como la comparación
            return None, "NO_SUPERA_REFERENCIA"
        if c2["estado"] == "SUPUESTO":   # opinión, no dato: no se ordena (desde T-27 un sobre válido puede traer escenarios SUPUESTO)
            return None, "ESCENARIOS_SUPUESTO"
        if conf <= 0:
            return None, "SIN_CONFIANZA"
        # T-17 (2) riesgo verificado: ni más suave que el p05 declarado ni que la pérdida hasta el stop (con el coste de ida y vuelta)
        riesgo = max(0.0, -peor)
        dist = c2.get("distribucion")
        if isinstance(dist, dict) and _num(dist.get("p05")) and coste_extra - dist["p05"] > riesgo + TOL:   # el p05 también paga el coste
            riesgo = coste_extra - dist["p05"]
            ajustes.append("RIESGO_P05")
        al_stop = _perdida_al_stop(p, ident["direccion"])
        if al_stop is None:   # sin stop legible no hay pérdida máxima: un LARGO puede perderlo todo; un CORTO o NEUTRAL, sin límite
            if ident["direccion"] != "LARGO":
                return None, "SIN_STOP"
            if RIESGO_SIN_STOP_LARGO > riesgo + TOL:
                riesgo = RIESGO_SIN_STOP_LARGO
                ajustes.append("RIESGO_SIN_STOP")
        elif al_stop + coste_iv_pct > riesgo + TOL:
            riesgo = al_stop + coste_iv_pct
            ajustes.append("RIESGO_STOP")
        # T-17 (4) confianza verificada: sin un doble análisis que la confirme (no hecho o discrepante) no pasa de una fracción del tope
        da = p["capa3"].get("doble_analisis")
        conf_v = conf
        confirmada = isinstance(da, dict) and da.get("realizado") is True and da.get("discrepa") is False
        if not confirmada and conf > FACTOR_SIN_DOBLE * TOPE_CLASE[clase] + TOL:
            conf_v = FACTOR_SIN_DOBLE * TOPE_CLASE[clase]
            ajustes.append("CONFIANZA_DISCREPA" if isinstance(da, dict) and da.get("discrepa") is True else "CONFIANZA_SIN_DOBLE")
        evidencia = math.fsum(PESO_EVIDENCIA[k] * pr[k] for k in PESO_EVIDENCIA)
        conf_n = conf_v / TOPE_CLASE[clase]
        # T-17 (3) horizontes en la misma unidad: exceso anualizado y riesgo escalado con la raíz del tiempo; el suelo del riesgo se
        # aplica en el plazo del candidato, antes de anualizar, para que un horizonte corto no lo diluya
        exceso_anual, riesgo_anual = exceso * k_h, riesgo * math.sqrt(k_h)
        punt = exceso_anual / (max(RIESGO_MIN_PCT, riesgo) * math.sqrt(k_h)) * conf_n * evidencia
        if not (math.isfinite(punt) and math.isfinite(riesgo_anual)):
            return None, "FORMA"
        return {"expediente_id": c["expediente_id"], "instrumento": inst.strip().upper(), "direccion": ident["direccion"],
                "clase": ident["clase_comparabilidad"], "retorno_esperado_pct": esperado, "exceso_sobre_referencia_pct": exceso,
                "horizonte_dias": horizonte, "peor_escenario_pct": peor, "confianza": conf, "confianza_normalizada": conf_n,
                "factor_evidencia": evidencia, "puntuacion": punt,
                # T-17: lo verificado por D
                "coste_descontado_pct": coste_extra, "riesgo_pct": riesgo, "exceso_anual_pct": exceso_anual, "riesgo_anual_pct": riesgo_anual,
                "confianza_verificada": conf_v, "ajustes": ajustes}, None
    except Exception:   # noqa: BLE001 - falta un campo o tiene un tipo raro: se excluye, nunca se adivina
        return None, "FORMA"


def comparar_candidatos(candidatos, ahora, referencia=None):
    """candidatos: lista de {"expediente_id", "sobre"}; referencia: el benchmark de la cartera (por defecto, efectivo al 0 %).
    Devuelve la decisión global (INVERTIR o ABSTENERSE), los grupos ordenados por clase y los excluidos."""
    try:
        return _comparar(candidatos, ahora, REFERENCIA_EFECTIVO if referencia is None else referencia)
    except Exception as ex:   # noqa: BLE001
        return {"ok": False, "codigo": "D-01", "motivo": f"error de cálculo: {type(ex).__name__}", "grupos": {}, "excluidos": []}


def _eid(c):
    try:
        e = c["expediente_id"]
        return e if type(e) is str else None
    except Exception:   # noqa: BLE001
        return None


def _no(motivo):
    return {"ok": False, "codigo": "D-01", "motivo": motivo, "decision_global": None, "grupos": {}, "excluidos": []}


def _domina(a, b):
    # T-17: domina si es mejor o igual en todo tanto en la unidad anual como en el plazo de cada uno; así la dominancia no
    # depende de la normalización de horizontes y un dominado no puede ser primero en ninguna ponderación de la sensibilidad
    ka = (a["exceso_anual_pct"], -a["riesgo_anual_pct"], a["exceso_sobre_referencia_pct"], -a["riesgo_pct"], a["confianza_normalizada"], a["factor_evidencia"])
    kb = (b["exceso_anual_pct"], -b["riesgo_anual_pct"], b["exceso_sobre_referencia_pct"], -b["riesgo_pct"], b["confianza_normalizada"], b["factor_evidencia"])
    return all(x >= y for x, y in zip(ka, kb)) and any(x > y for x, y in zip(ka, kb))


def _comparar(candidatos, ahora, ref):
    if not (isinstance(candidatos, list) and len(candidatos) >= 1):
        return _no("se necesita al menos un candidato con expediente_id y sobre")
    if not _referencia_ok(ref):
        return _no(f"referencia inválida: benchmark_ref y rentabilidad_anual_pct entre {REF_MIN} y {REF_MAX}")
    for c in candidatos:
        try:
            ok = isinstance(c, dict) and set(c) == {"expediente_id", "sobre"}
        except Exception:   # noqa: BLE001
            ok = False
        if not ok:
            return _no("cada candidato debe llevar exactamente expediente_id y sobre")
    if not isinstance(ahora, str) or not FH.match(ahora):
        return _no("instante inválido")
    try:
        _dt(ahora)
    except Exception:   # noqa: BLE001
        return _no("instante ilegible")
    ids = [_eid(c) for c in candidatos]
    cuenta = Counter(i for i in ids if i is not None)
    elegibles, excluidos = [], []
    for c, eid in zip(candidatos, ids):
        if eid is None:
            excluidos.append({"expediente_id": None, "motivo": "FORMA"})
        elif cuenta[eid] > 1:
            excluidos.append({"expediente_id": eid, "motivo": "DUPLICADO"})
        else:
            d, mot = _leer(c, ahora, ref)
            if mot:
                excluidos.append({"expediente_id": eid, "motivo": mot})
            else:
                elegibles.append(d)
    # dos análisis del mismo instrumento, sentido y clase no son alternativas: se queda el mejor (ante empate, el de menor id)
    mejores = {}
    for d in sorted(elegibles, key=lambda d: (-d["puntuacion"], d["expediente_id"])):
        k = (d["clase"], d["instrumento"], d["direccion"])
        if k in mejores:
            excluidos.append({"expediente_id": d["expediente_id"], "motivo": "DUPLICADO"})
        else:
            mejores[k] = d
    elegibles = list(mejores.values())
    # sensibilidad: el primero debe seguir siéndolo sin el factor de evidencia, sin la confianza y con otro suelo de riesgo
    # T-17: y sin normalizar los horizontes (si eso cambia el primero, los horizontes deciden y elige el operador)
    def anual(d, suelo):   # riesgo anual con el suelo aplicado en el plazo del candidato
        return d["exceso_anual_pct"] / (max(suelo, d["riesgo_pct"]) * math.sqrt(365.0 / d["horizonte_dias"]))
    alternativas = (lambda d: anual(d, RIESGO_MIN_PCT) * d["confianza_normalizada"],
                    lambda d: anual(d, RIESGO_MIN_PCT) * d["factor_evidencia"],
                    lambda d: anual(d, 2 * RIESGO_MIN_PCT) * d["confianza_normalizada"] * d["factor_evidencia"],
                    lambda d: d["exceso_sobre_referencia_pct"] / max(RIESGO_MIN_PCT, d["riesgo_pct"]) * d["confianza_normalizada"] * d["factor_evidencia"])
    grupos = {}
    for clase in CLASES:
        g = [d for d in elegibles if d["clase"] == clase]
        if not g:
            continue
        for d in g:
            d["dominado_por"] = sorted(x["expediente_id"] for x in g if x is not d and _domina(x, d))
        g = sorted(g, key=lambda d: (-d["puntuacion"], len(d["dominado_por"]), d["expediente_id"]))   # ante empate, el no dominado
        top = g[0]["puntuacion"]
        empatados = {d["expediente_id"] for d in g if abs(top - d["puntuacion"]) <= MARGEN_AJUSTADO * max(abs(top), abs(d["puntuacion"]), 1e-12)}
        # en cada ponderación cuentan todos los que quedan a la par del primero (no se desempata por id), y nunca un dominado
        dominados = {d["expediente_id"] for d in g if d["dominado_por"]}
        alternos = set()
        for f in alternativas:
            v = {d["expediente_id"]: f(d) for d in g}
            tf = max(v.values())
            alternos |= {e for e, x in v.items() if abs(tf - x) <= MARGEN_AJUSTADO * max(abs(tf), abs(x), 1e-12)}
        alternos -= dominados
        aspirantes = sorted((empatados - dominados) | alternos | {g[0]["expediente_id"]})
        sensible = alternos != {g[0]["expediente_id"]}
        clara = aspirantes == [g[0]["expediente_id"]]
        grupos[clase] = {"ranking": g, "decision": "CLARA" if clara else "AJUSTADA", "primero": g[0]["expediente_id"] if clara else None,
                         "sensible": sensible, "aspirantes": aspirantes}
    # con varias clases no hay un ganador único: decide el operador entre los aspirantes de todas (Fase 1 compara una sola clase)
    claras = [v["primero"] for v in grupos.values() if v["decision"] == "CLARA"]
    ganador_global = claras[0] if len(grupos) == 1 and claras else None
    aspirantes_global = sorted({a for v in grupos.values() for a in v["aspirantes"]}) if ganador_global is None else [ganador_global]
    excluidos.sort(key=lambda x: (str(x["expediente_id"]), x["motivo"]))
    return {"ok": True, "codigo": "OK", "motivo": "" if grupos else "ningún candidato supera la referencia con datos ordenables: no hacer nada",
            "decision_global": "INVERTIR" if grupos else "ABSTENERSE", "referencia": dict(ref), "grupos": grupos, "excluidos": excluidos,
            "ganador_global": ganador_global, "aspirantes": aspirantes_global if grupos else []}
