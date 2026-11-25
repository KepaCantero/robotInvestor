"""Respaldo de una afirmación. F2 conserva tanto la referencia citada como su origen documental."""
import math
import re
from collections import defaultdict

from .configuracion import parametro
from .herramientas.ht06_indice import normalizar


def cumple_ps1(raices, cfg=None):
    minimo = parametro(cfg, "ps1.raices_min")
    return (sum(n in ("A", "B") for n, _ in raices.values()) >= minimo
            or any(n == "A" and t == "PRIMARIA" for n, t in raices.values()))


def _origen_catalogo(ref_id, referencias):
    actual = ref_id
    vistos = set()
    while actual not in vistos:
        vistos.add(actual)
        ficha = referencias.por_id(actual)
        siguiente = (ficha or {}).get("fuente_original")
        if not siguiente:
            return actual
        actual = "REF-" + siguiente.strip().removeprefix("REF-")
    return None


def _trios(extracto):
    palabras = re.findall(r"\w+", normalizar(extracto or ""))
    return set(zip(palabras, palabras[1:], palabras[2:]))


def umbral_similitud(cfg):
    u = parametro(cfg, "evidencia.umbral_similitud_derivada")
    if type(u) not in (float, int) or not math.isfinite(u) or not 0 < u <= 1:
        raise ValueError("evidencia.umbral_similitud_derivada debe estar en (0, 1]")
    return u


def enlazar_documentos(clms, evds, referencias, almacen, umbral):
    """Reconstruye los enlaces de las piezas documentales en orden de disponibilidad.

    Solo una raíz localizable puede actuar como soporte. La comparación textual se limita a
    evidencias de la misma afirmación y con tres o más palabras. Una raíz explícita de catálogo
    se busca en todo F2, aunque figure en otra afirmación o llegase después que su derivada.
    """
    documentos = sorted((e for e in evds.values() if e.get("ref_id", "").startswith("REF-")),
                        key=lambda e: (e.get("conocible_desde") or "9999", e["evd_id"]))
    por_fuente = {}
    raices_por_clm = defaultdict(list)
    derivados = []
    origenes = {}
    for e in documentos:
        fuente = e["ref_id"]
        if fuente not in origenes:
            origenes[fuente] = _origen_catalogo(fuente, referencias)
        origen = origenes[fuente]
        if origen != fuente:
            derivados.append((e, origen, None))
            continue
        trios = _trios(e.get("extracto"))
        soporte = None
        for cid in e.get("clm_ids", []):
            if trios and cid in clms:
                soporte = next((r for r, t in raices_por_clm[cid] if len(trios & t) / len(trios | t) >= umbral), None)
                if soporte is not None:
                    break
        if soporte is not None:
            derivados.append((e, soporte["ref_id"], soporte))
            continue
        # Una cita en cuarentena conserva el historial pero no ofrece un soporte documental.
        if e.get("estado_verificacion") in ("VERIFICADA", "PENDIENTE"):
            por_fuente.setdefault(fuente, e)
            if trios:
                for cid in e.get("clm_ids", []):
                    raices_por_clm[cid].append((e, trios))
        _actualizar_evd(e, almacen, grado_independencia="RAIZ", origen_documental=fuente,
                       raiz_evd_id=None, motivo_raiz=None)
    for e, origen, soporte in derivados:
        raiz = soporte or por_fuente.get(origen)
        motivo = None if raiz else (f"Derivada de {origen or e['ref_id']}; original no ingerido, retirado o cadena circular")
        campos = {"grado_independencia": "DERIVADA", "origen_documental": origen, "motivo_raiz": motivo,
                  "raiz_evd_id": raiz["evd_id"] if raiz else "no identificada"}
        if motivo:
            campos["limitaciones"] = motivo
        elif e.get("limitaciones") and e["limitaciones"] == e.get("motivo_raiz"):
            campos["limitaciones"] = "Origen documental identificado en F2"
        _actualizar_evd(e, almacen, **campos)


def _actualizar_evd(e, almacen, **campos):
    cambios = {k: v for k, v in campos.items() if e.get(k) != v}
    if cambios:
        almacen.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": e["evd_id"], **cambios})
        e.update(cambios)
