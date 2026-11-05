"""D — comparador de candidatos (código de referencia V0.1).

Ordena sobres CT-G-02 ya aceptados por el Orquestador. Determinista, sin LLM. D no re-valida el sobre entero (lo hizo
el Orquestador): lee solo los campos que usa y falla cerrado si falta alguno. Solo compara dentro de una misma clase de
comparabilidad (Q, S, K); no mezcla clases.

La referencia de toda comparación es no hacer nada: el benchmark de la cartera (Constitución, P5). Cada candidato se mide por
su exceso sobre la rentabilidad de la referencia en su propio horizonte; si ninguno la supera con margen, D se abstiene
(decision_global ABSTENERSE). Un candidato solo también se compara: con la referencia.
Puntuación = exceso esperado por unidad de riesgo × confianza normalizada por el tope de su clase × factor de evidencia [PROPUESTO].
Escenarios SUPUESTO son opinión, no dato: no se ordenan (ESCENARIOS_SUPUESTO). Si dos candidatos quedan demasiado cerca, o el
primero cambia al variar las ponderaciones (sensibilidad), la decisión es AJUSTADA y D no elige. Cada candidato lista quién lo domina.
Códigos: OK; D-01 entrada inválida.
Motivos de exclusión por candidato: FORMA, DUPLICADO, EXCLUSION_DURA, CADUCADO, SIN_ESCENARIOS, SIN_RETORNO_POSITIVO,
NO_SUPERA_REFERENCIA, ESCENARIOS_SUPUESTO, SIN_CONFIANZA.
La referencia se compone al horizonte del candidato. Los «aspirantes» de un grupo son el primero, los empatados con él y los que
serían primeros con otra ponderación: entre ellos elige el operador cuando la decisión es AJUSTADA.
"""
from __future__ import annotations

import math
import re
from collections import Counter

from validar_sobre import _dt

PESO_EVIDENCIA = {"VERIFICADO": 1.0, "ESTIMADO": 0.5, "SUPUESTO": 0.25}   # [PROPUESTO]
MARGEN_AJUSTADO = 0.05   # [PROPUESTO] diferencia relativa por debajo de la cual no se declara un claro ganador
RIESGO_MIN_PCT = 1.0     # [PROPUESTO] suelo del denominador, para no premiar escenarios casi sin pérdida
TOL = 1e-6
ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
CLASES = ("Q", "S", "K")
TOPE_CLASE = {"Q": 0.80, "S": 0.60, "K": 0.40}   # [PROPUESTO] topes de confianza por clase (D-03 del operador)
EXCESO_MIN_PCT = 0.10    # [PROPUESTO] exceso mínimo sobre la referencia, en puntos porcentuales, para no abstenerse
REFERENCIA_EFECTIVO = {"benchmark_ref": "BENCH-EFECTIVO", "rentabilidad_anual_pct": 0.0}   # [PROPUESTO] valor de partida


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


RENT_MIN, RENT_MAX = -100.0, 500.0   # [PROPUESTO] rentabilidad neta plausible en %; fuera de ahí el dato es sospechoso
EXCL = {"sanciones", "invertibilidad", "acceso"}


def _referencia_ok(r):
    return (isinstance(r, dict) and set(r) == {"benchmark_ref", "rentabilidad_anual_pct"} and isinstance(r["benchmark_ref"], str)
            and ID.match(r["benchmark_ref"]) is not None and _num(r["rentabilidad_anual_pct"]) and -5 <= r["rentabilidad_anual_pct"] <= 50)


def _leer(c, ahora, ref=REFERENCIA_EFECTIVO):
    """Devuelve (datos, motivo_de_exclusion). Nunca lanza."""
    try:
        s = c["sobre"]
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
        esperado = math.fsum(e["probabilidad"] * e["rentabilidad_neta_pct"] for e in esc)
        if esperado <= 0:   # con retorno esperado no positivo no hay nada que ordenar: dividir una pérdida por más riesgo la haría parecer menor
            return None, "SIN_RETORNO_POSITIVO"
        peor = min(e["rentabilidad_neta_pct"] for e in con_peso)   # un escenario de probabilidad cero no cuenta
        horizonte = math.fsum(e["probabilidad"] * e["horizonte_dias"] for e in esc)
        liston = ((1 + ref["rentabilidad_anual_pct"] / 100.0) ** (horizonte / 365.0) - 1) * 100.0   # no hacer nada durante el mismo plazo, compuesto
        exceso = esperado - liston
        if not exceso > EXCESO_MIN_PCT:
            return None, "NO_SUPERA_REFERENCIA"
        if c2["estado"] == "SUPUESTO":   # opinión, no dato: no se ordena (V-13 ya lo impide en un sobre válido; D se defiende igual)
            return None, "ESCENARIOS_SUPUESTO"
        if conf <= 0:
            return None, "SIN_CONFIANZA"
        evidencia = math.fsum(PESO_EVIDENCIA[k] * pr[k] for k in PESO_EVIDENCIA)
        conf_n = conf / TOPE_CLASE[ident["clase_comparabilidad"]]
        punt = exceso / max(RIESGO_MIN_PCT, -peor) * conf_n * evidencia
        if not math.isfinite(punt):
            return None, "FORMA"
        return {"expediente_id": c["expediente_id"], "instrumento": inst.strip().upper(), "direccion": ident["direccion"],
                "clase": ident["clase_comparabilidad"], "retorno_esperado_pct": esperado, "exceso_sobre_referencia_pct": exceso,
                "horizonte_dias": horizonte, "peor_escenario_pct": peor, "confianza": conf, "confianza_normalizada": conf_n,
                "factor_evidencia": evidencia, "puntuacion": punt}, None
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


def _orden(g, punt):
    return sorted(g, key=lambda d: (-punt(d), d["expediente_id"]))


def _domina(a, b):
    ka = (a["exceso_sobre_referencia_pct"], a["peor_escenario_pct"], a["confianza_normalizada"], a["factor_evidencia"])
    kb = (b["exceso_sobre_referencia_pct"], b["peor_escenario_pct"], b["confianza_normalizada"], b["factor_evidencia"])
    return all(x >= y for x, y in zip(ka, kb)) and any(x > y for x, y in zip(ka, kb))


def _comparar(candidatos, ahora, ref):
    if not (isinstance(candidatos, list) and len(candidatos) >= 1):
        return _no("se necesita al menos un candidato con expediente_id y sobre")
    if not _referencia_ok(ref):
        return _no("referencia inválida: benchmark_ref y rentabilidad_anual_pct entre -50 y 50")
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
    alternativas = (lambda d: d["exceso_sobre_referencia_pct"] / max(RIESGO_MIN_PCT, -d["peor_escenario_pct"]) * d["confianza_normalizada"],
                    lambda d: d["exceso_sobre_referencia_pct"] / max(RIESGO_MIN_PCT, -d["peor_escenario_pct"]) * d["factor_evidencia"],
                    lambda d: d["exceso_sobre_referencia_pct"] / max(2 * RIESGO_MIN_PCT, -d["peor_escenario_pct"]) * d["confianza_normalizada"] * d["factor_evidencia"])
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
        alternos = {_orden(g, f)[0]["expediente_id"] for f in alternativas}
        aspirantes = sorted(empatados | alternos)
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
