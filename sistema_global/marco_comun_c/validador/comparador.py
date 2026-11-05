"""D — comparador de candidatos (código de referencia V0.1).

Ordena sobres CT-G-02 ya aceptados por el Orquestador. Determinista, sin LLM. D no re-valida el sobre entero (lo hizo
el Orquestador): lee solo los campos que usa y falla cerrado si falta alguno. Solo compara dentro de una misma clase de
comparabilidad (Q, S, K); no mezcla clases. Si dos candidatos quedan demasiado cerca, lo dice (AJUSTADA) y no elige.
Puntuación = retorno esperado por unidad de riesgo × confianza × factor de evidencia [PROPUESTO].
Códigos: OK; D-01 entrada inválida; D-03 no hay un grupo con al menos dos candidatos elegibles.
Motivos de exclusión por candidato: FORMA, DUPLICADO, EXCLUSION_DURA, CADUCADO, SIN_ESCENARIOS, SIN_RETORNO_POSITIVO, SIN_PAR_EN_SU_CLASE.
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


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


RENT_MIN, RENT_MAX = -100.0, 500.0   # [PROPUESTO] rentabilidad neta plausible en %; fuera de ahí el dato es sospechoso
EXCL = {"sanciones", "invertibilidad", "acceso"}


def _leer(c, ahora):
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
        if c2["estado"] not in ("ESTIMADO", "SUPUESTO") or not isinstance(esc, list) or len(esc) < 2:
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
        if not (_num(conf) and _num(tope) and 0 <= conf <= tope <= 1 and isinstance(pr, dict) and set(pr) == set(PESO_EVIDENCIA)
                and all(_num(pr[k]) and 0 <= pr[k] <= 1 for k in PESO_EVIDENCIA) and abs(math.fsum(pr.values()) - 1.0) <= 1e-3):
            return None, "FORMA"
        esperado = math.fsum(e["probabilidad"] * e["rentabilidad_neta_pct"] for e in esc)
        if esperado <= 0:   # con retorno esperado no positivo no hay nada que ordenar: dividir una pérdida por más riesgo la haría parecer menor
            return None, "SIN_RETORNO_POSITIVO"
        peor = min(e["rentabilidad_neta_pct"] for e in con_peso)   # un escenario de probabilidad cero no cuenta
        evidencia = math.fsum(PESO_EVIDENCIA[k] * pr[k] for k in PESO_EVIDENCIA)
        punt = esperado / max(RIESGO_MIN_PCT, -peor) * conf * evidencia
        if not math.isfinite(punt):
            return None, "FORMA"
        return {"expediente_id": c["expediente_id"], "instrumento": inst.strip().upper(), "direccion": ident["direccion"],
                "clase": ident["clase_comparabilidad"], "retorno_esperado_pct": esperado, "peor_escenario_pct": peor,
                "confianza": conf, "factor_evidencia": evidencia, "puntuacion": punt}, None
    except Exception:   # noqa: BLE001 - falta un campo o tiene un tipo raro: se excluye, nunca se adivina
        return None, "FORMA"


def comparar_candidatos(candidatos, ahora):
    """candidatos: lista de {"expediente_id", "sobre"}. Devuelve los grupos ordenados por clase y los excluidos."""
    try:
        return _comparar(candidatos, ahora)
    except Exception as ex:   # noqa: BLE001
        return {"ok": False, "codigo": "D-01", "motivo": f"error de cálculo: {type(ex).__name__}", "grupos": {}, "excluidos": []}


def _eid(c):
    try:
        e = c["expediente_id"]
        return e if type(e) is str else None
    except Exception:   # noqa: BLE001
        return None


def _comparar(candidatos, ahora):
    if not (isinstance(candidatos, list) and len(candidatos) >= 2):
        return {"ok": False, "codigo": "D-01", "motivo": "se necesitan al menos dos candidatos con expediente_id y sobre", "grupos": {}, "excluidos": []}
    for c in candidatos:
        try:
            ok = isinstance(c, dict) and set(c) == {"expediente_id", "sobre"}
        except Exception:   # noqa: BLE001
            ok = False
        if not ok:
            return {"ok": False, "codigo": "D-01", "motivo": "cada candidato debe llevar exactamente expediente_id y sobre", "grupos": {}, "excluidos": []}
    if not isinstance(ahora, str) or not FH.match(ahora):
        return {"ok": False, "codigo": "D-01", "motivo": "instante inválido", "grupos": {}, "excluidos": []}
    try:
        _dt(ahora)
    except Exception:   # noqa: BLE001
        return {"ok": False, "codigo": "D-01", "motivo": "instante ilegible", "grupos": {}, "excluidos": []}
    ids = [_eid(c) for c in candidatos]
    cuenta = Counter(i for i in ids if i is not None)
    elegibles, excluidos = [], []
    for c, eid in zip(candidatos, ids):
        if eid is None:
            excluidos.append({"expediente_id": None, "motivo": "FORMA"})
        elif cuenta[eid] > 1:
            excluidos.append({"expediente_id": eid, "motivo": "DUPLICADO"})
        else:
            d, mot = _leer(c, ahora)
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
    grupos = {}
    for clase in CLASES:
        g = sorted((d for d in elegibles if d["clase"] == clase), key=lambda d: (-d["puntuacion"], d["expediente_id"]))
        if len(g) >= 2:
            a, b = g[0]["puntuacion"], g[1]["puntuacion"]
            ajustada = abs(a - b) <= MARGEN_AJUSTADO * max(abs(a), abs(b), 1e-12)
            grupos[clase] = {"ranking": g, "decision": "AJUSTADA" if ajustada else "CLARA", "primero": None if ajustada else g[0]["expediente_id"]}
        elif g:
            excluidos.append({"expediente_id": g[0]["expediente_id"], "motivo": "SIN_PAR_EN_SU_CLASE"})
    excluidos.sort(key=lambda x: (str(x["expediente_id"]), x["motivo"]))
    if not grupos:
        return {"ok": False, "codigo": "D-03", "motivo": "ningún grupo de clase tiene dos candidatos elegibles", "grupos": {}, "excluidos": excluidos}
    return {"ok": True, "codigo": "OK", "motivo": "", "grupos": grupos, "excluidos": excluidos}
