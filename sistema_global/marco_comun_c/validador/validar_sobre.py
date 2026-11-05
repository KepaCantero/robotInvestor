"""Validador determinista del sobre CT-G-02 0.1.0 (reglas V-01 a V-23).

Primero comprueba la forma con el esquema JSON; luego aplica las reglas que cruzan
campos. Devuelve una lista de incumplimientos {regla, ruta, mensaje}. Lista vacía = válido.
Sin LLM, sin red, sin reloj propio: la fecha actual y el contexto del encargo se pasan.
Nunca lanza excepciones por un sobre mal formado: lo rechaza con V-01.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from jsonschema import Draft202012Validator

AQUI = Path(__file__).resolve().parent
VERSIONES_CONOCIDAS = {"0.1.0"}
EPISODIOS_ESTANDAR = ["EP-2008-LEHMAN", "EP-2011-EUROZONA", "EP-2015-SNB",
                      "EP-2018-Q4", "EP-2020-COVID", "EP-2022-TIPOS"]
FACTORES_ESTANDAR = ["TIPOS", "RV", "USD", "CREDITO", "INFLACION",
                     "MATERIAS_PRIMAS", "VOLATILIDAD", "LIQUIDEZ"]
TOPE_POR_CLASE = {"Q": 0.80, "S": 0.60, "K": 0.40}   # valores de partida [PROPUESTO]
FACTOR_DISCREPANCIA = 0.75                            # [PROPUESTO]
VIGENCIA_MAX = timedelta(days=30)                     # [PROPUESTO]
MAX_NO_ESTIMABLE_N2 = 0.50                            # [PROPUESTO]
TOLERANCIA = 1e-6
CAPA1 = ["identificacion", "tesis", "entrada_salida", "liquidez", "costes", "capital",
         "estres_historico", "factores", "evidencia", "exclusiones_duras", "referencias"]
EXIGIDOS = {
    "N0": ["identificacion", "exclusiones_duras", "evidencia"],
    "N1": ["identificacion", "exclusiones_duras", "evidencia", "tesis",
           "entrada_salida", "liquidez", "costes", "capital", "referencias"],
    "N2": CAPA1,
    "N3": CAPA1 + ["capa2", "capa3"],
}
# Unidad exigida y rango permitido por ruta de cifra (V-17, V-21). None = sin límite.
UNIDADES = {
    "liquidez.tiempo_salida": ("días", 0, None),
    "liquidez.coste_salida": ("pb", 0, None),
    "liquidez.tamano_max_sin_impacto": ("EUR", 0, None),
    "costes.entrada": ("pb", 0, None),
    "costes.mantenimiento_anual": ("pb", None, None),   # puede ser negativo (carry a favor)
    "costes.salida": ("pb", 0, None),
    "costes.impacto_fiscal": ("EUR", None, None),
    "capital.capital_necesario": ("EUR", 0, None),
    "capital.margen": ("EUR", 0, None),
    "capital.apalancamiento": ("x", 0, None),
    "factores.calidad_ajuste": ("R2", 0, 1),
}
UNIDAD_ESTRES = ("%", -100, 0)
UNIDAD_BETA = ("beta", -10, 10)


def cargar_json(texto: str):
    """Carga JSON rechazando NaN e infinitos (que json.loads acepta por defecto)."""
    def _no(c):
        raise ValueError(f"constante no permitida en JSON: {c}")
    return json.loads(texto, parse_constant=_no)


def _esquema():
    ruta = AQUI.parent / "esquemas" / "ct-g-02_0.1.0.schema.json"
    return json.loads(ruta.read_text(encoding="utf-8"))


def _dt(s):
    """Fecha-hora con zona obligatoria; ValueError si no."""
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError("falta zona horaria")
    return d


def _numeros_no_finitos(nodo, ruta="(raíz)"):
    if isinstance(nodo, float) and not math.isfinite(nodo):
        yield ruta
    elif isinstance(nodo, dict):
        for k, v in nodo.items():
            yield from _numeros_no_finitos(v, f"{ruta}.{k}")
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from _numeros_no_finitos(v, f"{ruta}[{i}]")


def _es_cifra(n):
    return isinstance(n, dict) and {"valor", "unidad", "estado"} <= set(n)


def _cifras(nodo, ruta="payload"):
    if _es_cifra(nodo):
        yield ruta, nodo
    elif isinstance(nodo, dict):
        for k, v in nodo.items():
            yield from _cifras(v, f"{ruta}.{k}")
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from _cifras(v, f"{ruta}[{i}]")


def _numeros_sueltos(nodo, ruta):
    """Números fuera de una Cifra válida dentro del cuerpo especializado (V-19)."""
    if _es_cifra(nodo):
        if nodo.get("estado") not in ("VERIFICADO", "ESTIMADO", "SUPUESTO", "NO_ESTIMABLE"):
            yield ruta, "estado de cifra no válido"
        return
    if isinstance(nodo, bool):
        return
    if isinstance(nodo, (int, float)):
        yield ruta, "número suelto: toda cifra debe ser una Cifra con estado"
    elif isinstance(nodo, dict):
        for k, v in nodo.items():
            yield from _numeros_sueltos(v, f"{ruta}.{k}")
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from _numeros_sueltos(v, f"{ruta}[{i}]")


def proporcion_real(payload):
    """Proporción de cifras VERIFICADO/ESTIMADO/SUPUESTO entre las no NO_ESTIMABLE."""
    cuenta = {"VERIFICADO": 0, "ESTIMADO": 0, "SUPUESTO": 0}
    for _, c in _cifras(payload):
        if c.get("estado") in cuenta:
            cuenta[c["estado"]] += 1
    total = sum(cuenta.values())
    return {k: (v / total if total else 0.0) for k, v in cuenta.items()}


def validar(sobre, ctx: dict) -> list[dict]:
    """ctx: ahora (ISO con zona), fecha_corte_encargo (YYYY-MM-DD), perfiles_activos,
    clases_ratificadas {perfil: Q|S|K}, apalancamiento_permitido (bool)."""
    fallos: list[dict] = []

    def f(regla, ruta, msg):
        fallos.append({"regla": regla, "ruta": ruta, "mensaje": msg})

    # Contexto: sin él no se puede validar con garantías
    try:
        ahora = _dt(ctx["ahora"])
        fc_encargo = date.fromisoformat(ctx["fecha_corte_encargo"])
        activos, rat = list(ctx["perfiles_activos"]), dict(ctx["clases_ratificadas"])
    except (KeyError, ValueError, TypeError) as e:
        f("V-01", "contexto", f"contexto de validación inválido: {e}")
        return fallos

    # V-01 forma, versión conocida, números finitos
    ver = sobre.get("version_esquema") if isinstance(sobre, dict) else None
    if not isinstance(ver, str) or ver not in VERSIONES_CONOCIDAS:
        f("V-01", "version_esquema", f"versión desconocida: {ver!r}")
        return fallos
    for ruta in _numeros_no_finitos(sobre):
        f("V-01", ruta, "número no finito (NaN o infinito)")
    if fallos:
        return fallos
    for e in sorted(Draft202012Validator(_esquema()).iter_errors(sobre),
                    key=lambda e: [str(x) for x in e.absolute_path]):
        f("V-01", ".".join(str(x) for x in e.absolute_path) or "(raíz)", e.message[:200])
    if fallos:
        return fallos

    p = sobre["payload"]
    ident = p["identificacion"]
    perfil = ident["perfil"]
    nivel = ident["nivel_analisis"]

    # V-02 perfil construido y coherente con el emisor
    if perfil not in activos:
        f("V-02", "payload.identificacion.perfil", f"{perfil} está NO_CONSTRUIDO")
    if sobre["producer"] != perfil:
        f("V-02", "producer", "el emisor no coincide con el perfil del sobre")

    # V-03 vigencia (zona horaria obligatoria, vigencia máxima)
    emitido = None
    try:
        emitido, vence = _dt(sobre["emitido_en"]), _dt(sobre["valid_until"])
        if vence <= emitido:
            f("V-03", "valid_until", "valid_until no es posterior a emitido_en")
        if vence - emitido > VIGENCIA_MAX:
            f("V-03", "valid_until", f"vigencia superior a {VIGENCIA_MAX.days} días")
        if vence <= ahora:
            f("V-03", "valid_until", "el sobre está caducado")
        if emitido > ahora:
            f("V-03", "emitido_en", "emitido en el futuro")
    except ValueError as e:
        f("V-03", "emitido_en", f"fecha-hora inválida: {e}")

    # V-04 fecha de corte común con el encargo y no posterior a la emisión
    try:
        fc = date.fromisoformat(ident["fecha_corte"])
        if fc != fc_encargo:
            f("V-04", "payload.identificacion.fecha_corte", "no coincide con la fecha de corte del encargo")
        if emitido is not None and fc > emitido.astimezone(ahora.tzinfo).date():
            f("V-04", "payload.identificacion.fecha_corte", "posterior a la emisión")
        if "entrada_salida" in p:
            fr = date.fromisoformat(p["entrada_salida"]["fecha_revision"])
            if fr < fc:
                f("V-04", "payload.entrada_salida.fecha_revision", "anterior a la fecha de corte")
    except ValueError:
        f("V-04", "payload", "fecha no interpretable")

    # V-05 capas exigidas según el nivel
    for bloque in EXIGIDOS[nivel]:
        if bloque not in p:
            f("V-05", f"payload.{bloque}", f"falta; exigido en {nivel}")

    # V-06 clase de comparabilidad ratificada para el perfil
    if rat.get(perfil) != ident["clase_comparabilidad"]:
        f("V-06", "payload.identificacion.clase_comparabilidad",
          f"la clase ratificada para {perfil} es {rat.get(perfil)!r}")

    # V-07 / V-08 / V-20 coherencia de cada Cifra (P3, P16)
    motores = set(p.get("referencias", {}).get("artefactos_motor", []))
    cifras = list(_cifras(p))
    for ruta, c in cifras:
        est = c["estado"]
        if est == "NO_ESTIMABLE":
            if c["valor"] is not None:
                f("V-07", ruta, "NO_ESTIMABLE exige valor null")
        else:
            if not isinstance(c["valor"], (int, float)) or isinstance(c["valor"], bool):
                f("V-07", ruta, f"estado {est} exige un valor numérico")
        if est in ("VERIFICADO", "ESTIMADO"):
            if not (c.get("modelo_ref") and c.get("motor_id")):
                f("V-08", ruta, f"{est} exige modelo_ref y motor_id (sin ellos es SUPUESTO)")
            elif "referencias" in p and c["motor_id"] not in motores:
                f("V-20", ruta, f"motor_id {c['motor_id']} no figura en referencias.artefactos_motor")
        elif c.get("modelo_ref") or c.get("motor_id"):
            f("V-20", ruta, f"{est} no puede declarar modelo_ref ni motor_id")

    # V-09 invalidez medible
    ci = p.get("tesis", {}).get("condiciones_invalidez")
    if "tesis" in p:
        if not ci:
            f("V-09", "payload.tesis.condiciones_invalidez", "al menos una condición medible")
        elif len({c["id"] for c in ci}) != len(ci):
            f("V-09", "payload.tesis.condiciones_invalidez", "identificadores repetidos")

    # V-10 evidencia: la proporción declarada es la real y suma 1
    pr = p["evidencia"]["proporcion"]
    if abs(sum(pr.values()) - 1) > 1e-3:
        f("V-10", "payload.evidencia.proporcion", f"suman {sum(pr.values()):.3f}, no 1")
    real = proporcion_real(p)
    if cifras and any(abs(pr[k] - real[k]) > 0.02 for k in real):
        f("V-10", "payload.evidencia.proporcion",
          "no coincide con el recuento real de estados de las cifras")

    # V-11 estrés / V-12 factores: conjunto estándar exacto
    if "estres_historico" in p:
        ids = [e["episodio_id"] for e in p["estres_historico"]["episodios"]]
        if sorted(ids) != sorted(EPISODIOS_ESTANDAR):
            f("V-11", "payload.estres_historico.episodios",
              "debe tener exactamente los episodios estándar, uno cada uno")
    if "factores" in p:
        ids = [e["factor"] for e in p["factores"]["exposiciones"]]
        if sorted(ids) != sorted(FACTORES_ESTANDAR):
            f("V-12", "payload.factores.exposiciones",
              "debe tener exactamente los factores comunes, uno cada uno")

    # V-13 capa 2
    if "capa2" in p:
        c2 = p["capa2"]
        if c2["estado"] == "ESTIMADO":
            esc = c2.get("escenarios") or []
            if not (c2.get("metodo") and c2.get("base_datos")) or len(esc) < 2:
                f("V-13", "payload.capa2", "ESTIMADO exige metodo, base_datos y al menos 2 escenarios")
            elif abs(sum(e["probabilidad"] for e in esc) - 1) > 1e-3:
                f("V-13", "payload.capa2.escenarios", "las probabilidades no suman 1")
            elif len({e["nombre"] for e in esc}) != len(esc):
                f("V-13", "payload.capa2.escenarios", "nombres de escenario repetidos")
        elif c2.get("escenarios") or c2.get("metodo") or c2.get("base_datos"):
            f("V-13", "payload.capa2", f"{c2['estado']} no puede llevar método, datos ni escenarios")

    # V-14 confianza
    if "capa3" in p:
        c3 = p["capa3"]
        tope = TOPE_POR_CLASE[ident["clase_comparabilidad"]]
        if abs(c3["tope_confianza"] - tope) > TOLERANCIA:
            f("V-14", "payload.capa3.tope_confianza", f"el tope de la clase es {tope}")
        if c3["doble_analisis"]["discrepa"]:
            tope *= FACTOR_DISCREPANCIA
        tope *= (1 - pr["SUPUESTO"])
        if c3["confianza"] > tope + TOLERANCIA:
            f("V-14", "payload.capa3.confianza", f"{c3['confianza']} supera el tope efectivo {tope:.3f}")
        if nivel == "N3" and not c3["doble_analisis"]["realizado"]:
            f("V-14", "payload.capa3.doble_analisis", "N3 exige doble análisis")

    # V-15 apalancamiento
    if "capital" in p and not ctx.get("apalancamiento_permitido", False):
        a = p["capital"]["apalancamiento"]
        if a["estado"] == "NO_ESTIMABLE" or a["valor"] != 0:
            f("V-15", "payload.capital.apalancamiento", "apalancamiento no habilitado: debe declararse 0")

    # V-16 exclusiones duras (en cualquier nivel)
    ex = p["exclusiones_duras"]
    if any(v == "BLOQUEADO" for v in ex.values()):
        f("V-16", "payload.exclusiones_duras", "candidato bloqueado: no pasa a D")
    elif any(v == "DESCONOCIDO" for v in ex.values()):
        f("V-16", "payload.exclusiones_duras", "desconocido: resolver antes de entregar a D")

    # V-17 / V-21 unidades y rangos por ruta
    def revisar(ruta, c, unidad, lo, hi, regla_u="V-17"):
        if c["unidad"] != unidad:
            f(regla_u, ruta, f"la unidad debe ser {unidad!r}")
        v = c["valor"]
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if (lo is not None and v < lo) or (hi is not None and v > hi):
                f("V-21", ruta, f"valor {v} fuera del rango permitido [{lo}, {hi}]")
    for suf, (u, lo, hi) in UNIDADES.items():
        bloque, campo = suf.split(".")
        if bloque in p:
            revisar(f"payload.{suf}", p[bloque][campo], u, lo, hi)
    for e in p.get("estres_historico", {}).get("episodios", []):
        revisar(f"payload.estres_historico[{e['episodio_id']}]", e["perdida"], *UNIDAD_ESTRES)
    for e in p.get("factores", {}).get("exposiciones", []):
        revisar(f"payload.factores[{e['factor']}]", e["beta"], *UNIDAD_BETA)

    # V-18 cuerpo especializado con esquema propio
    cuerpo = p.get("cuerpo_especializado")
    if cuerpo is None:
        f("V-18", "payload.cuerpo_especializado", "falta el cuerpo especializado del perfil")
    else:
        if not cuerpo["esquema_ref"].startswith(perfil + "-"):
            f("V-18", "payload.cuerpo_especializado.esquema_ref",
              f"el esquema propio debe nombrarse con el prefijo {perfil}-")
        # V-19 ningún número suelto en el cuerpo especializado
        for ruta, msg in _numeros_sueltos(cuerpo["contenido"], "payload.cuerpo_especializado.contenido"):
            f("V-19", ruta, msg)

    # V-22 coherencia interna
    if "entrada_salida" in p:
        st, ob = p["entrada_salida"]["stop"], p["entrada_salida"]["objetivo"]
        if all(isinstance(c["valor"], (int, float)) and not isinstance(c["valor"], bool) for c in (st, ob)):
            if (ident["direccion"] == "LARGO" and st["valor"] >= ob["valor"]) or \
               (ident["direccion"] == "CORTO" and st["valor"] <= ob["valor"]):
                f("V-22", "payload.entrada_salida", "stop y objetivo incoherentes con la dirección")

    # V-23 comparabilidad mínima: en N2 y N3 no más de la mitad de las cifras en NO_ESTIMABLE
    if nivel in ("N2", "N3") and cifras:
        ne = sum(1 for _, c in cifras if c["estado"] == "NO_ESTIMABLE") / len(cifras)
        if ne > MAX_NO_ESTIMABLE_N2:
            f("V-23", "payload", f"{ne:.0%} de las cifras son NO_ESTIMABLE; máximo {MAX_NO_ESTIMABLE_N2:.0%}")
    return fallos


def main(argv):
    if len(argv) < 3:
        print("uso: validar_sobre.py sobre.json contexto.json")
        return 2
    try:
        sobre = cargar_json(Path(argv[1]).read_text(encoding="utf-8"))
        ctx = cargar_json(Path(argv[2]).read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"V-01  (archivo): {e}\nRECHAZADO (1 incumplimiento)")
        return 1
    fallos = validar(sobre, ctx)
    for x in fallos:
        print(f"{x['regla']}  {x['ruta']}: {x['mensaje']}")
    print("VÁLIDO" if not fallos else f"RECHAZADO ({len(fallos)} incumplimientos)")
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
