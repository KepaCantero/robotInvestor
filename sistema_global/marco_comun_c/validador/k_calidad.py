"""K · Datos de corte y calendario — reglas de calidad Q-01 a Q-15, emisión del sello y
validación del sello (S-01 a S-14). Sello 0.2.0 (T-26, parte 2): cada fuente lleva su procedencia (proveedor, licencia,
cuándo se obtuvo y referencia) y su último cierre; el sello lleva el calendario de eventos; Q-14 exige procedencia
completa y licencia admitida y que ningún dato sea posterior a su obtención; Q-15 exige eventos bien formados y anunciados
antes de emitir. `punto_en_el_tiempo` responde con lo que se sabía en un instante (sin look-ahead).

Determinista: sin LLM, sin red, sin reloj propio (la hora se pasa en ctx["ahora"]).
Falla cerrado: ante cualquier entrada defectuosa devuelve BLOQUEO (K-00) y no emite sello.
Todos los umbrales son valores de partida [PROPUESTO].
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from validar_sobre import _dt, cargar_json  # noqa: E402

VERSION_REGLAS = "Q-0.2.0"
VERSION_SELLO = "0.2.0"
REGLAS = [f"Q-{i:02d}" for i in range(1, 16)]
from parametros import PARAMETROS as _P   # noqa: E402  (valores [PROPUESTO] versionados, T-25)

TOPE_ANTIGUEDAD = dict(_P["k_tope_antiguedad_dias_habiles"])   # días hábiles [PROPUESTO]
SALTO_ADV, SALTO_BLOQ = _P["k_salto_adv_bloq"]                       # Q-04
HUECO_ADV, HUECO_BLOQ = _P["k_hueco_adv_bloq"]                       # Q-05
CRUCE_ADV, CRUCE_BLOQ = _P["k_cruce_adv_bloq"]                       # Q-09
TIPOS_AJUSTE = {"SPLIT", "DIVIDENDO", "SIMBOLO"}
ORDEN = {"OK": 0, "ADVERTENCIA": 1, "BLOQUEO": 2}
_FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")
_FECHAHORA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
ID_RE = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
SELLO_RE = re.compile(r"^K-\d{8}-\d{3}\Z")
MIN_OBS = _P["k_min_observaciones"]            # observaciones mínimas por fuente [PROPUESTO]
RANGO_MAX = _P["k_rango_max_intradia"]         # máximo/mínimo intradía admisible (Q-07) [PROPUESTO]
VENTANA_ACUM = _P["k_ventana_acumulado_obs"]   # observaciones de la ventana de movimiento acumulado (Q-04)
AJUSTE_TOL = _P["k_ajuste_tol_rel"]            # tolerancia relativa entre factor del ajuste y salto observado
LICENCIAS = tuple(_P["k_licencias_admitidas"])   # Q-14 [PROPUESTO]
TIPOS_EVENTO = ("BANCO_CENTRAL", "DATO_MACRO", "RESULTADOS", "DIVIDENDO", "SPLIT", "VENCIMIENTO", "FESTIVO_EXTRA", "OTRO")
CLAVES_PROCEDENCIA = {"proveedor", "licencia", "obtenido_en", "referencia"}
CLAVES_EVENTO = {"fecha", "tipo", "instrumentos", "descripcion", "anunciado_en"}
MAX_SERIE, MAX_FUENTES = 20000, 100
CLAVES_OBS = {"fecha", "apertura", "maximo", "minimo", "cierre", "volumen"}
CLAVES_FUENTE = {"fuente_id", "instrumento", "version_conjunto", "serie", "critico", "contraste",
                 "hash_declarado", "disponible", "procedencia"}
ERRORES = (KeyError, TypeError, AttributeError, ValueError, IndexError, OverflowError,
           RecursionError, MemoryError)


class EntradaInvalida(ValueError):
    pass


def _fecha(s, nombre="fecha"):
    if not isinstance(s, str) or not _FECHA_RE.match(s):
        raise EntradaInvalida(f"{nombre} no es una fecha AAAA-MM-DD: {s!r}")
    try:
        return date.fromisoformat(s)
    except ValueError as e:
        raise EntradaInvalida(f"{nombre} inválida: {e}")


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


# ---------------------------------------------------------------- calendario
class SinCobertura(Exception):
    pass


class Calendario:
    """Calendario de mercados: lunes a viernes salvo festivos. Falla si el año no está cubierto."""

    def __init__(self, cal):
        if not isinstance(cal, dict) or not isinstance(cal.get("version"), str) or not cal["version"].strip():
            raise EntradaInvalida("calendario sin versión")
        self.version = cal["version"]
        self.mercados = {}
        self.cierres = {}
        mercs = cal.get("mercados")
        if not isinstance(mercs, dict):
            raise EntradaInvalida("calendario sin mercados")
        for nombre, m in mercs.items():
            anios = m.get("anios")
            fest = m.get("festivos", [])
            if not isinstance(anios, list) or not all(isinstance(a, int) and not isinstance(a, bool) for a in anios):
                raise EntradaInvalida(f"mercado {nombre}: anios inválidos")
            self.mercados[nombre] = (set(anios), {_fecha(x, "festivo") for x in fest})
            hc = m.get("hora_cierre_utc")   # T-26 (R-G3): hora UTC desde la que existe el cierre de un día; sin ella, el día siguiente
            if hc is not None and not (isinstance(hc, str) and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", hc)):
                raise EntradaInvalida(f"mercado {nombre}: hora_cierre_utc mal formada")
            self.cierres[nombre] = hc

    def cierre_de(self, mercado, d):
        """Instante UTC desde el que existe la barra del día d en ese mercado (prudente: sin hora declarada, el día siguiente)."""
        hc = self.cierres.get(mercado)
        if hc is None:
            return datetime(d.year, d.month, d.day, tzinfo=timezone.utc) + timedelta(days=1)
        hh, mm = map(int, hc.split(":"))
        return datetime(d.year, d.month, d.day, hh, mm, tzinfo=timezone.utc)

    def es_habil(self, mercado, d):
        if mercado not in self.mercados:
            raise SinCobertura(f"mercado sin calendario: {mercado}")
        anios, fest = self.mercados[mercado]
        if d.year not in anios:
            raise SinCobertura(f"el calendario de {mercado} no cubre {d.year}")
        return d.weekday() < 5 and d not in fest

    def dias_habiles(self, mercado, desde, hasta):
        """Días hábiles en el intervalo (desde, hasta]."""
        if hasta < desde:
            raise EntradaInvalida("intervalo invertido")
        n, d = 0, desde
        while d < hasta:
            d += timedelta(days=1)
            if self.es_habil(mercado, d):
                n += 1
        return n

    def anterior_habil(self, mercado, d):
        for _ in range(15):
            if self.es_habil(mercado, d):
                return d
            d -= timedelta(days=1)
        raise SinCobertura("no hay día hábil en los últimos 15 días")


# ---------------------------------------------------------------- hash
def hash_serie(serie) -> str:
    texto = json.dumps(serie, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def hash_del_sello(s) -> str:
    """Hash canónico del sello, sin `hash_sello` ni `estado` (que cambia en la vida del sello)."""
    return hash_serie({k: v for k, v in s.items() if k not in ("hash_sello", "estado")})


# ---------------------------------------------------------------- emisión
class _Acum:
    def __init__(self):
        self.res = {r: ["OK", []] for r in REGLAS}

    def poner(self, regla, nivel, detalle):
        if ORDEN[nivel] > ORDEN[self.res[regla][0]]:
            self.res[regla][0] = nivel
        if nivel != "OK":
            self.res[regla][1].append(detalle)

    def lista(self):
        out = []
        for r in REGLAS:
            nivel, det = self.res[r]
            x = {"regla": r, "resultado": nivel}
            if det:
                x["detalle"] = "; ".join(det[:5]) + (f" (+{len(det) - 5} más)" if len(det) > 5 else "")
            out.append(x)
        return out

    def global_(self):
        return max((v[0] for v in self.res.values()), key=lambda n: ORDEN[n])


def _bloqueo(regla, detalle):
    return {"sello": None, "resultado_global": "BLOQUEO",
            "resultados": [{"regla": regla, "resultado": "BLOQUEO", "detalle": detalle}]}


def _procedencia_fallo(p, ahora):
    """Motivo por el que la procedencia de una fuente no vale (Q-14), o None."""
    if not (isinstance(p, dict) and set(p) == CLAVES_PROCEDENCIA):
        return f"procedencia incompleta: declara exactamente {sorted(CLAVES_PROCEDENCIA)}"
    if not all(isinstance(p[k], str) and ID_RE.match(p[k]) for k in ("proveedor", "licencia")):
        return "proveedor o licencia mal formados"
    if p["licencia"] not in LICENCIAS:
        return f"licencia {p['licencia']!r} no admitida ({', '.join(LICENCIAS)})"
    if not (isinstance(p["referencia"], str) and p["referencia"].strip() and len(p["referencia"]) <= 200):
        return "referencia vacía o demasiado larga"
    if not (isinstance(p["obtenido_en"], str) and _FECHAHORA_RE.match(p["obtenido_en"])):
        return "obtenido_en no es una fecha-hora con zona"
    if _dt(p["obtenido_en"]) > ahora:
        return "obtenido_en posterior a la emisión del sello"
    return None


def _evento_fallo(ev, ahora):
    """Motivo por el que un evento del calendario no vale (Q-15), o None."""
    if set(ev) != CLAVES_EVENTO:
        return f"un evento declara exactamente {sorted(CLAVES_EVENTO)}"
    if ev["tipo"] not in TIPOS_EVENTO:
        return f"tipo desconocido {ev['tipo']!r}"
    if not (ev["instrumentos"] and all(ID_RE.match(i) for i in ev["instrumentos"]) and len(set(ev["instrumentos"])) == len(ev["instrumentos"])):
        return "instrumentos vacíos, mal formados o repetidos"
    if not (isinstance(ev["descripcion"], str) and ev["descripcion"].strip() and len(ev["descripcion"]) <= 200):
        return "descripción vacía o demasiado larga"
    if not (isinstance(ev["anunciado_en"], str) and _FECHAHORA_RE.match(ev["anunciado_en"])):
        return "anunciado_en no es una fecha-hora con zona"
    if _dt(ev["anunciado_en"]) > ahora:
        return "anunciado después de emitir el sello (anticipación)"
    return None


def construir_sello(entrada, calendario, ctx) -> dict:
    """Aplica Q-01..Q-13 y, si no hay BLOQUEO, emite el sello. Nunca lanza excepciones.
    Devuelve {sello|None, resultado_global, resultados}."""
    try:
        return _construir(entrada, calendario, ctx)
    except SinCobertura as e:
        return _bloqueo("Q-11", str(e))
    except ERRORES as e:
        return _bloqueo("K-00", f"entrada o contexto mal formado: {type(e).__name__}: {e}")


def _construir(entrada, calendario, ctx):
    if not isinstance(entrada, dict) or not isinstance(ctx, dict):
        raise EntradaInvalida("entrada y contexto deben ser objetos")
    cal = Calendario(calendario)
    if not isinstance(ctx["ahora"], str) or not _FECHAHORA_RE.match(ctx["ahora"]):
        raise EntradaInvalida("ahora no tiene el formato AAAA-MM-DDThh:mm:ss±zona")
    ahora = _dt(ctx["ahora"])
    sec = ctx["secuencia"]
    if not isinstance(sec, int) or isinstance(sec, bool) or not 1 <= sec <= 999:
        raise EntradaInvalida("secuencia fuera de 1..999")
    cartera = entrada["cartera"]
    if cartera not in TOPE_ANTIGUEDAD:
        raise EntradaInvalida(f"cartera desconocida: {cartera!r}")
    tope = TOPE_ANTIGUEDAD[cartera]
    mercado = entrada["mercado"]
    if not isinstance(mercado, str) or not ID_RE.match(mercado):
        raise EntradaInvalida("mercado con formato inválido")
    solicitada = _fecha(entrada["fecha_corte_solicitada"], "fecha_corte_solicitada")
    reemplaza = ctx.get("reemplaza_a")
    if reemplaza is not None and not (isinstance(reemplaza, str) and SELLO_RE.match(reemplaza)):
        raise EntradaInvalida("reemplaza_a no es un sello_id")

    # ---- estructura de fuentes
    fuentes_in = entrada["fuentes"]
    if not isinstance(fuentes_in, list) or not fuentes_in or len(fuentes_in) > MAX_FUENTES:
        raise EntradaInvalida("fuentes ausentes o demasiadas")
    ids = []
    for fu in fuentes_in:
        if not isinstance(fu, dict) or not isinstance(fu.get("fuente_id"), str) or not ID_RE.match(fu["fuente_id"]):
            raise EntradaInvalida("fuente sin fuente_id válido")
        if set(fu) - CLAVES_FUENTE:
            raise EntradaInvalida(f"{fu['fuente_id']}: claves no admitidas {sorted(set(fu) - CLAVES_FUENTE)}")
        ids.append(fu["fuente_id"])
        if not isinstance(fu.get("disponible", True), bool):
            raise EntradaInvalida("disponible debe ser booleano")
        if "critico" in fu and not isinstance(fu["critico"], bool):
            raise EntradaInvalida("critico debe ser booleano")
        for k in ("instrumento", "version_conjunto"):
            if k in fu and not (isinstance(fu[k], str) and ID_RE.match(fu[k])):
                raise EntradaInvalida(f"{fu['fuente_id']}: {k} con formato inválido")
        if "contraste" in fu and not (isinstance(fu["contraste"], list) and all(isinstance(c, str) for c in fu["contraste"])):
            raise EntradaInvalida("contraste debe ser una lista de textos")
    if len(set(ids)) != len(ids):
        raise EntradaInvalida("fuente_id repetido")

    # ---- fechas de las series y cobertura del calendario (Q-11)
    series = {}
    for fu in fuentes_in:
        if fu.get("disponible", True):
            s = fu.get("serie")
            if not isinstance(s, list) or not s or len(s) > MAX_SERIE:
                raise EntradaInvalida(f"{fu['fuente_id']}: serie vacía, ausente o demasiado larga")
            for o in s:
                if not isinstance(o, dict):
                    raise EntradaInvalida(f"{fu['fuente_id']}: observación no es un objeto")
                if set(o) - CLAVES_OBS:
                    raise EntradaInvalida(f"{fu['fuente_id']}: claves de observación no admitidas {sorted(set(o) - CLAVES_OBS)}")
            series[fu["fuente_id"]] = [(_fecha(o.get("fecha"), "fecha de observación"), o) for o in s]
    a = _Acum()
    primera = min([d for v in series.values() for d, _ in v] + [solicitada])
    for anio in range(primera.year, solicitada.year + 1):
        if anio not in cal.mercados.get(mercado, (set(),))[0]:
            raise SinCobertura(f"el calendario de {mercado} no cubre {anio}")

    # ---- Q-01
    cal.es_habil(mercado, solicitada)   # comprueba mercado y año
    corte = cal.anterior_habil(mercado, solicitada)
    if corte != solicitada:
        a.poner("Q-01", "ADVERTENCIA", f"{solicitada} no es día hábil en {mercado}; corte en {corte}")
    if corte > ahora.date():
        a.poner("Q-13", "BLOQUEO", f"el corte {corte} es posterior a la fecha de emisión {ahora.date()}")
    if reemplaza is not None and (reemplaza == f"K-{corte:%Y%m%d}-{sec:03d}" or reemplaza[2:10] > f"{corte:%Y%m%d}"):
        raise EntradaInvalida("reemplaza_a no puede ser el propio sello ni uno de un corte posterior")

    # ---- Q-08 ajustes
    aj = entrada.get("ajustes")
    ajustados = []   # (fuente_id, fecha_efectiva, factor)
    if not isinstance(aj, dict) or not isinstance(aj.get("version"), str) or not ID_RE.match(aj["version"]):
        a.poner("Q-08", "BLOQUEO", "ajustes sin versión")
        version_ajustes = None
    else:
        version_ajustes = aj["version"]
        items = aj.get("items", [])
        if not isinstance(items, list):
            a.poner("Q-08", "BLOQUEO", "items de ajustes no es una lista")
            items = []
        for i, it in enumerate(items):
            try:
                ok = (isinstance(it, dict) and isinstance(it.get("fuente_id"), str)
                      and it.get("tipo") in TIPOS_AJUSTE and _num(it.get("factor")) and it["factor"] > 0)
                fe = _fecha(it.get("fecha_efectiva"), "fecha_efectiva") if ok else None
            except EntradaInvalida:
                ok = False
            if not ok:
                a.poner("Q-08", "BLOQUEO", f"ajuste {i} incompleto o inválido")
            else:
                ajustados.append((it["fuente_id"], fe, it["factor"]))
    eventos = entrada.get("eventos", [])
    if not isinstance(eventos, list):
        raise EntradaInvalida("eventos no es una lista")
    explicados = set()   # (instrumento, fecha)
    calendario_eventos = []
    for ev in eventos:
        if not isinstance(ev, dict) or not isinstance(ev.get("instrumentos"), list) or not all(isinstance(i, str) for i in ev["instrumentos"]):
            raise EntradaInvalida("evento mal formado")
        fe = _fecha(ev.get("fecha"), "fecha de evento")
        # Q-15 calendario de eventos (T-26): forma completa y anunciado antes de emitir el sello
        mal = _evento_fallo(ev, ahora)
        if mal:
            a.poner("Q-15", "BLOQUEO", f"evento del {fe}: {mal}")
            continue
        calendario_eventos.append({k: (sorted(ev[k]) if k == "instrumentos" else ev[k]) for k in sorted(CLAVES_EVENTO)})
        for ins in ev["instrumentos"]:
            explicados.add((ins, fe))
    calendario_eventos.sort(key=lambda x: (x["fecha"], x["tipo"], x["descripcion"]))

    # ---- reglas por fuente
    fuentes_sello = []
    cierres = {}   # fuente_id -> {fecha: cierre válido}
    disponibles = 0
    for fu in fuentes_in:
        fid = fu["fuente_id"]
        if not fu.get("disponible", True):
            fuentes_sello.append({"fuente_id": fid, "estado": "NO_DISPONIBLE"})
            continue
        disponibles += 1
        obs = series[fid]
        instr = fu.get("instrumento", fid)
        # Q-14 procedencia completa, licencia admitida y ningún dato posterior a su obtención (T-26, hallazgo 11)
        mal = _procedencia_fallo(fu.get("procedencia"), ahora)
        if mal:
            a.poner("Q-14", "BLOQUEO", f"{fid}: {mal}")
        else:
            obtenido = _dt(fu["procedencia"]["obtenido_en"])
            despues = [d for d, _ in obs if cal.cierre_de(mercado, d) > obtenido]   # R-G3: la barra existe solo tras el cierre
            if despues:
                a.poner("Q-14", "BLOQUEO", f"{fid}: {len(despues)} observación(es) cuyo cierre es posterior a cuando se obtuvo el dato "
                                           f"({fu['procedencia']['obtenido_en']}; primera {min(despues)})")
        # Q-13 anticipación
        post = [d for d, _ in obs if d > corte]
        if post:
            a.poner("Q-13", "BLOQUEO", f"{fid}: {len(post)} observación(es) posteriores al corte ({min(post)})")
        # Q-06 orden y duplicados
        fechas = [d for d, _ in obs]
        if any(b <= x for x, b in zip(fechas, fechas[1:])):
            a.poner("Q-06", "BLOQUEO", f"{fid}: fechas repetidas o fuera de orden")
        nohab = [d for d in fechas if d <= corte and not cal.es_habil(mercado, d)]
        if nohab:
            a.poner("Q-06", "BLOQUEO", f"{fid}: {len(nohab)} observación(es) en día no hábil ({nohab[0]})")
        # Q-03 y Q-07
        validas = {}
        for d, o in obs:
            vals = [o.get(k) for k in ("apertura", "maximo", "minimo", "cierre")]
            if not all(_num(v) and v > 0 for v in vals) or ("volumen" in o and not (_num(o["volumen"]) and o["volumen"] >= 0)):
                a.poner("Q-03", "BLOQUEO", f"{fid} {d}: valor ausente, no numérico, no finito o no positivo")
                continue
            ap, mx, mn, ci = vals
            if mx < max(ap, ci) or mn > min(ap, ci) or mx < mn:
                a.poner("Q-07", "BLOQUEO", f"{fid} {d}: barra incoherente")
            elif mx / mn > RANGO_MAX:
                a.poner("Q-07", "BLOQUEO", f"{fid} {d}: rango intradía superior a {RANGO_MAX}×")
            if d <= corte:
                validas[d] = ci
        cierres[fid] = validas
        # observaciones hasta el corte
        hasta = sorted({d for d in fechas if d <= corte})
        if not hasta:
            a.poner("Q-02", "BLOQUEO", f"{fid}: sin datos hasta el corte")
            continue   # bloquea: no se emite sello, no hace falta describir la fuente
        ultima = hasta[-1]
        ant = cal.dias_habiles(mercado, ultima, corte)
        if ant > tope:
            a.poner("Q-02", "BLOQUEO", f"{fid}: antigüedad {ant} d.h. supera el tope {tope} de {cartera}")
        # Q-04 saltos: factor del ajuste = precio nuevo / precio anterior
        mis_aj = [(dd, fac) for (ff, dd, fac) in ajustados if ff == fid]

        def ajuste_en(d0, d1, ratio):
            return any(d0 < dd <= d1 and abs(ratio / fac - 1) <= AJUSTE_TOL for dd, fac in mis_aj)

        fv = sorted(validas)
        for p_, d_ in zip(fv, fv[1:]):
            ratio = validas[d_] / validas[p_]
            salto = abs(ratio - 1)
            if salto <= SALTO_ADV or ajuste_en(p_, d_, ratio):
                continue
            ev = any(x for x in explicados if x[0] == instr and p_ < x[1] <= d_)
            nota = " (coincide con un evento, que no lo explica del todo)" if ev else " sin explicación"
            if salto > SALTO_BLOQ:
                a.poner("Q-04", "BLOQUEO", f"{fid} {d_}: salto {salto:.0%}{nota}")
            else:
                a.poner("Q-04", "ADVERTENCIA", f"{fid} {d_}: salto {salto:.0%}{nota}")
        for i in range(VENTANA_ACUM, len(fv)):
            ratio = validas[fv[i]] / validas[fv[i - VENTANA_ACUM]]
            if abs(ratio - 1) > SALTO_BLOQ and not ajuste_en(fv[i - VENTANA_ACUM], fv[i], ratio):
                a.poner("Q-04", "BLOQUEO", f"{fid} {fv[i]}: movimiento acumulado {abs(ratio - 1):.0%} en {VENTANA_ACUM} observaciones")
                break
        # Q-05 huecos (ventana: primera observación a última observación hasta el corte)
        presentes = set(hasta)
        dias, d = [], hasta[0]
        while d <= ultima:
            if cal.es_habil(mercado, d):
                dias.append(d)
            d += timedelta(days=1)
        if len(presentes) < MIN_OBS:
            a.poner("Q-05", "BLOQUEO", f"{fid}: solo {len(presentes)} observaciones (mínimo {MIN_OBS})")
        faltan = [x for x in dias if x not in presentes]
        if dias and faltan:
            r = len(faltan) / len(dias)
            if r > HUECO_BLOQ:
                a.poner("Q-05", "BLOQUEO", f"{fid}: faltan {len(faltan)} de {len(dias)} días hábiles ({r:.1%})")
            elif r > HUECO_ADV:
                a.poner("Q-05", "ADVERTENCIA", f"{fid}: faltan {len(faltan)} de {len(dias)} días hábiles ({r:.1%})")
        # Q-12 integridad
        h = hash_serie(fu["serie"])
        if fu.get("hash_declarado") != h:
            a.poner("Q-12", "BLOQUEO", f"{fid}: el hash declarado no coincide con el contenido")
        if not mal:   # con Q-14 en BLOQUEO no se emite sello
            fuentes_sello.append({"fuente_id": fid, "estado": "DISPONIBLE", "instrumento": instr,
                                  "version_conjunto": str(fu.get("version_conjunto", "")).strip() or "SIN-VERSION",
                                  "ultima_observacion": str(ultima), "antiguedad_dias_habiles": ant, "hash": h,
                                  "ultimo_cierre": validas.get(ultima),
                                  "procedencia": {k: fu["procedencia"][k] for k in sorted(CLAVES_PROCEDENCIA)}})
    if disponibles == 0:
        a.poner("Q-02", "BLOQUEO", "no hay ninguna fuente disponible")

    # ---- Q-09 cruces de divisas (c = a × b), en la última fecha común hasta el corte
    cruces = entrada.get("cruces", [])
    if not isinstance(cruces, list):
        raise EntradaInvalida("cruces no es una lista")
    if disponibles and mercado == "FX" and not cruces:
        a.poner("Q-09", "ADVERTENCIA", "mercado FX sin cruces definidos: coherencia no comprobada")
    for cr in (cruces if disponibles else []):
        if not (isinstance(cr, dict) and all(isinstance(cr.get(k), str) for k in "abc")):
            raise EntradaInvalida("cruce mal formado")
        trio = [cierres.get(cr[k]) for k in "abc"]
        comunes = set.intersection(*[set(t) for t in trio]) if all(trio) else set()
        if not comunes:
            a.poner("Q-09", "ADVERTENCIA", f"cruce {cr['a']}×{cr['b']}≈{cr['c']}: sin fecha común, no evaluable")
            continue
        d = max(comunes)
        dev = abs(trio[0][d] * trio[1][d] / trio[2][d] - 1)
        if dev > CRUCE_BLOQ:
            a.poner("Q-09", "BLOQUEO", f"cruce {cr['c']}: desviación {dev:.2%} el {d}")
        elif dev > CRUCE_ADV:
            a.poner("Q-09", "ADVERTENCIA", f"cruce {cr['c']}: desviación {dev:.2%} el {d}")

    # ---- Q-10 dato crítico con una sola fuente
    vivos = {fu["fuente_id"] for fu in fuentes_in if fu.get("disponible", True)}
    for fu in fuentes_in:
        if fu.get("critico") is True and fu.get("disponible", True):
            con = fu.get("contraste", [])
            if not isinstance(con, list) or not [c for c in con if c in vivos and c != fu["fuente_id"]]:
                a.poner("Q-10", "ADVERTENCIA", f"{fu['fuente_id']}: dato crítico sin fuente de contraste disponible")

    # ---- Q-11 se cumplió si hemos llegado aquí
    glob = a.global_()
    resultados = a.lista()
    if glob == "BLOQUEO":
        return {"sello": None, "resultado_global": glob, "resultados": resultados}
    sello = {
        "hash_sello": "",
        "sello_id": f"K-{corte:%Y%m%d}-{sec:03d}",
        "version_esquema": VERSION_SELLO,
        "fecha_corte": str(corte),
        "fecha_solicitada": str(solicitada),
        "emitido_en": ctx["ahora"],
        "cartera": cartera,
        "mercados": [{"mercado": mercado, "version_calendario": cal.version}],
        "fuentes": fuentes_sello,
        "version_ajustes": version_ajustes,
        "version_reglas": VERSION_REGLAS,
        "resultado_reglas": resultados,
        "resultado_global": glob,
        "eventos": calendario_eventos,   # T-26 (hallazgo 12): el calendario de eventos vive en K
        "estado": "VIGENTE",
    }
    if reemplaza:
        sello["reemplaza_a"] = reemplaza
    sello["hash_sello"] = hash_del_sello(sello)
    return {"sello": sello, "resultado_global": glob, "resultados": resultados}


# ---------------------------------------------------------------- validación del sello
def _esquema():
    return json.loads((AQUI.parent / "esquemas" / f"k-sello_{VERSION_SELLO}.schema.json").read_text(encoding="utf-8"))


def validar_sello(sello, ctx=None) -> list[dict]:
    """Reglas S-01 a S-14 sobre un sello ya emitido. Nunca lanza excepciones.
    ctx opcional: {"calendario": {...}} para recomprobar días hábiles y antigüedad (S-10)."""
    try:
        return _validar_sello(sello, ctx or {})
    except (*ERRORES, SinCobertura) as e:
        return [{"regla": "S-01", "ruta": "(interno)", "mensaje": f"sello o contexto mal formado: {type(e).__name__}: {e}"}]


def _validar_sello(s, ctx):
    fallos = []

    def f(regla, ruta, m):
        fallos.append({"regla": regla, "ruta": ruta, "mensaje": m})

    if not isinstance(s, dict):
        f("S-01", "(raíz)", "el sello no es un objeto")
        return fallos
    for e in sorted(Draft202012Validator(_esquema()).iter_errors(s), key=lambda e: list(e.absolute_path)):
        f("S-01", ".".join(str(x) for x in e.absolute_path) or "(raíz)", e.message[:200])
    if fallos:
        return fallos
    corte = _fecha(s["fecha_corte"])
    # S-02 el identificador corresponde a la fecha de corte
    if s["sello_id"][2:10] != f"{corte:%Y%m%d}":
        f("S-02", "sello_id", "la fecha del identificador no coincide con fecha_corte")
    # S-03 el resultado global es el peor y no hay BLOQUEO en un sello emitido
    reglas = [x["regla"] for x in s["resultado_reglas"]]
    peor = max((x["resultado"] for x in s["resultado_reglas"]), key=lambda n: ORDEN[n])
    if s["resultado_global"] != peor:
        f("S-03", "resultado_global", f"debe ser el peor resultado ({peor})")
    if peor == "BLOQUEO":
        f("S-03", "resultado_reglas", "un sello emitido no puede contener BLOQUEO")
    # S-04 las 13 reglas, una vez cada una
    if sorted(reglas) != REGLAS:
        f("S-04", "resultado_reglas", f"deben figurar Q-01 a Q-{len(REGLAS):02d} exactamente una vez")
    # S-05 fuentes coherentes
    ids = [x["fuente_id"] for x in s["fuentes"]]
    if len(set(ids)) != len(ids):
        f("S-05", "fuentes", "fuente_id repetido")
    nm = [m["mercado"] for m in s["mercados"]]
    if len(set(nm)) != len(nm):
        f("S-05", "mercados", "mercado repetido")
    if not any(x["estado"] == "DISPONIBLE" for x in s["fuentes"]):
        f("S-05", "fuentes", "debe haber al menos una fuente DISPONIBLE")
    for x in s["fuentes"]:
        if x["estado"] == "DISPONIBLE" and _fecha(x["ultima_observacion"]) > corte:
            f("S-05", f"fuentes.{x['fuente_id']}", "ultima_observacion posterior a fecha_corte")
        if x["estado"] == "DISPONIBLE" and x["antiguedad_dias_habiles"] > TOPE_ANTIGUEDAD[s["cartera"]]:
            f("S-05", f"fuentes.{x['fuente_id']}", "antigüedad por encima del tope de la cartera")
    # S-06 no se emite antes del corte; el corte no es posterior a lo solicitado
    if _dt(s["emitido_en"]).astimezone(timezone.utc).date() < corte:
        f("S-06", "emitido_en", "emitido antes de la fecha de corte")
    if _fecha(s["fecha_solicitada"]) < corte:
        f("S-06", "fecha_solicitada", "el corte no puede ser posterior a la fecha solicitada")
    # S-07 una corrección no se reemplaza a sí misma ni a un sello posterior
    if "reemplaza_a" in s:
        if s["reemplaza_a"] == s["sello_id"]:
            f("S-07", "reemplaza_a", "un sello no puede reemplazarse a sí mismo")
        elif s["reemplaza_a"][2:10] > s["sello_id"][2:10]:
            f("S-07", "reemplaza_a", "no puede reemplazar a un sello de un corte posterior")
    # S-08 un sello recién emitido no puede estar ya ANULADO sin sustituto conocido (informativo en ctx)
    if s["estado"] == "ANULADO" and ctx.get("exigir_vigente"):
        f("S-08", "estado", "el sello está ANULADO")
    # S-09 una ADVERTENCIA lleva detalle para poder citarla
    for x in s["resultado_reglas"]:
        if x["resultado"] == "ADVERTENCIA" and "detalle" not in x:
            f("S-09", f"resultado_reglas.{x['regla']}", "una ADVERTENCIA debe llevar detalle")
        if x["resultado"] == "OK" and "detalle" in x:
            f("S-09", f"resultado_reglas.{x['regla']}", "un OK no lleva detalle")
    # S-10 con calendario: la última observación es día hábil y la antigüedad cuadra
    if ctx.get("calendario") is not None:
        cal = Calendario(ctx["calendario"])
        for m in s["mercados"]:
            mercado = m["mercado"]
            if m["version_calendario"] != cal.version:
                f("S-10", "mercados", f"versión de calendario de {mercado} distinta de la proporcionada")
            if not cal.es_habil(mercado, corte):
                f("S-10", "fecha_corte", f"el corte no es día hábil de {mercado}")
            for x in s["fuentes"]:
                if x["estado"] == "DISPONIBLE":
                    u = _fecha(x["ultima_observacion"])
                    if not cal.es_habil(mercado, u):
                        f("S-10", f"fuentes.{x['fuente_id']}", "ultima_observacion no es día hábil")
                    elif u <= corte and cal.dias_habiles(mercado, u, corte) != x["antiguedad_dias_habiles"]:
                        f("S-10", f"fuentes.{x['fuente_id']}", "antiguedad_dias_habiles no cuadra con el calendario")
    # S-11 versiones no vacías y de formato conocido
    if s["version_esquema"] != VERSION_SELLO:
        f("S-11", "version_esquema", "versión de esquema desconocida")
    if s["version_reglas"] != VERSION_REGLAS:
        f("S-11", "version_reglas", f"versión de reglas desconocida (esperada {VERSION_REGLAS})")
    # S-12 integridad del propio sello
    if s["hash_sello"] != hash_del_sello(s):
        f("S-12", "hash_sello", "el hash no corresponde al contenido del sello")
    # S-14 procedencia y calendario coherentes con la emisión (T-26): licencia admitida, nada obtenido ni anunciado después de
    # emitir y ninguna observación posterior a cuando se obtuvo el dato
    em = _dt(s["emitido_en"])
    for x in s["fuentes"]:
        if x["estado"] != "DISPONIBLE":
            continue
        pr = x["procedencia"]
        if pr["licencia"] not in LICENCIAS:
            f("S-14", f"fuentes.{x['fuente_id']}.procedencia.licencia", f"licencia {pr['licencia']!r} no admitida")
        if _dt(pr["obtenido_en"]) > em:
            f("S-14", f"fuentes.{x['fuente_id']}.procedencia.obtenido_en", "obtenido después de emitir el sello")
        cal_ = Calendario(ctx["calendario"]) if ctx.get("calendario") is not None else None
        u = _fecha(x["ultima_observacion"])
        # con calendario, a la hora de cierre del mercado; sin él solo se puede comprobar el día (S-10 tampoco lo recomprueba)
        cierre_u = (cal_.cierre_de(s["mercados"][0]["mercado"], u) if cal_ else
                    datetime(u.year, u.month, u.day, tzinfo=timezone.utc))
        if cierre_u > _dt(pr["obtenido_en"]):
            f("S-14", f"fuentes.{x['fuente_id']}.ultima_observacion", "su cierre es posterior a cuando se obtuvo el dato")
    for i, ev in enumerate(s["eventos"]):   # R-M2: cada evento entero, fecha real incluida
        try:
            _fecha(ev["fecha"], "fecha de evento")
            mal = _evento_fallo(ev, em)
        except EntradaInvalida as e_:
            mal = str(e_)
        if mal:
            f("S-14", f"eventos[{i}]", mal)
    # S-13 coherencia entre fecha solicitada y Q-01
    q01 = next((x["resultado"] for x in s["resultado_reglas"] if x["regla"] == "Q-01"), None)
    if (s["fecha_solicitada"] != s["fecha_corte"]) != (q01 == "ADVERTENCIA"):
        f("S-13", "resultado_reglas.Q-01", "Q-01 debe ser ADVERTENCIA si y solo si el corte difiere de la fecha solicitada")
    return fallos


def estado_sello(sello, fecha_uso, cartera_uso, calendario) -> str:
    """VIGENTE, CADUCADO o ANULADO. Cualquier problema devuelve CADUCADO (falla cerrado)."""
    try:
        if sello["estado"] == "ANULADO":
            return "ANULADO"
        if cartera_uso not in TOPE_ANTIGUEDAD:
            return "CADUCADO"
        cal = Calendario(calendario)
        uso, corte = _fecha(fecha_uso, "fecha_uso"), _fecha(sello["fecha_corte"])
        if uso < corte:
            return "CADUCADO"
        edad = max(cal.dias_habiles(m["mercado"], corte, uso) for m in sello["mercados"])
        if sello["cartera"] not in TOPE_ANTIGUEDAD or TOPE_ANTIGUEDAD[sello["cartera"]] > TOPE_ANTIGUEDAD[cartera_uso]:
            return "CADUCADO"   # emitido con una frescura menos exigente que la de la cartera de uso
        if any(x.get("antiguedad_dias_habiles", 10**9) > TOPE_ANTIGUEDAD[cartera_uso]
               for x in sello["fuentes"] if x.get("estado") == "DISPONIBLE"):
            return "CADUCADO"
        return "VIGENTE" if edad <= TOPE_ANTIGUEDAD[cartera_uso] and sello["estado"] == "VIGENTE" else "CADUCADO"
    except (*ERRORES, SinCobertura):
        return "CADUCADO"


# ---------------------------------------------------------------- T-26: consulta «punto en el tiempo» y calendario
def _respuesta_pit(fu, d, obt, cal):
    mercado = fu.get("mercado", "FX")
    obs = [o for o in fu["serie"] if isinstance(o, dict) and _FECHA_RE.match(str(o.get("fecha", ""))) and _fecha(o["fecha"]) <= d
           and (cal.cierre_de(mercado, _fecha(o["fecha"])) if cal else
                datetime.combine(_fecha(o["fecha"]), datetime.min.time(), timezone.utc) + timedelta(days=1)) <= obt
           and _num(o.get("cierre")) and o["cierre"] > 0]
    if not obs:
        return None
    o = max(obs, key=lambda x: x["fecha"])
    return {"fuente_id": fu["fuente_id"], "version_conjunto": fu.get("version_conjunto"), "obtenido_en": fu["procedencia"]["obtenido_en"],
            "fecha": o["fecha"], "cierre": o["cierre"]}


def punto_en_el_tiempo(fuentes, instrumento, fecha, conocido_en, calendario=None):
    """Lo que K sabía de `instrumento` el día `fecha` en el instante `conocido_en` (P7: sin información posterior).
    `fuentes`: entradas de K (con serie y procedencia); los datos originales no se sobrescriben, así que puede haber varias
    versiones de un conjunto: vale la última obtenida no después de `conocido_en`, y de ella la última observación no posterior
    a `fecha` cuyo cierre ya existía cuando se obtuvo (con el calendario, a su hora de cierre; sin él, al día siguiente). Si dos
    versiones se obtuvieron en el mismo instante y no coinciden, no responde. Devuelve {fuente_id, version_conjunto,
    obtenido_en, fecha, cierre} o None. Nunca lanza."""
    try:
        t = _dt(conocido_en)
        d = _fecha(fecha)
        cal = Calendario(calendario) if calendario is not None else None
        cands = []
        for fu in fuentes:
            pr = fu.get("procedencia")
            if fu.get("disponible", True) is False or fu.get("instrumento") != instrumento or _procedencia_fallo(pr, t):
                continue
            obt = _dt(pr["obtenido_en"])
            cands.append((obt, fu))
        if not cands:
            return None
        tmax = max(c[0] for c in cands)
        resp = [_respuesta_pit(fu, d, tmax, cal) for t_, fu in cands if t_ == tmax]
        if any(x is None for x in resp) or len({(x["fecha"], x["cierre"]) for x in resp}) != 1:
            return None   # R-M1: versiones obtenidas en el mismo instante que no coinciden: no se elige (falla cerrado)
        return min(resp, key=lambda x: x["fuente_id"])
    except (*ERRORES, SinCobertura):
        return None


def eventos_entre(sello, desde, hasta, instrumento=None):
    """Eventos del calendario del sello con fecha en [desde, hasta] (y, si se da, que afectan al instrumento). Nunca lanza:
    un calendario ilegible devuelve None (no es lo mismo que «sin eventos», R-M2)."""
    try:
        d0, d1 = _fecha(desde), _fecha(hasta)
        out = []
        for ev in sello.get("eventos", []):
            if d0 <= _fecha(ev["fecha"]) <= d1 and (instrumento is None or _norm_ins(instrumento) in {_norm_ins(i) for i in ev["instrumentos"]}):
                out.append(dict(ev))
        return out
    except (*ERRORES, SinCobertura):
        return None


def _norm_ins(t):
    return re.sub(r"[^A-Z0-9]", "", str(t).upper())
