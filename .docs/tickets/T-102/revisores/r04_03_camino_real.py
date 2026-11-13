"""QA r04 de T-102 · Ataques por el camino real del ciclo (C1 simulado, DIV) con lo que pasa la unidad en `r04_01` y `r04_02`.

- `fugas`: cada frase que pasa la unidad, en TODOS los textos del Sintetizador; ¿llega su firma al paquete o a los tres
  entregables? ¿se declara? ¿qué dictamen da G3?
- `legitimas`: las legítimas que la r04 quita (vehículo + verbo, «medio plazo», «Cada ETF»): ¿qué queda en el informe, se
  declara, bloquea G3?
- `nombre_llano`: un Analista pone en `nombre_llano` una probabilidad en letra o un ticker en minúscula (H-27 de la r03).
- `glosario`: término y definición que no son texto, o con un ticker (H-24).
- `reescritura`: primera respuesta ilegible y segunda con fugas.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_03_camino_real.py <raiz_repo> [-k <parte>]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith("-")]
FILTRO = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
ARGS = [a for a in ARGS if a != FILTRO]
M = C.preparar(ARGS[0] if ARGS else ".")
v6 = M["v6"]
BASE = C.ciclo()
MARCAS = BASE["marcas"]
OPP = next(k for k in MARCAS if k.startswith("opp:"))

FUGAS = {
    "contra_uno": "Las apuestas pagan tres contra uno a favor de la subida.",
    "porciento": "Vemos un setenta porciento de opciones de subida.",
    "tercio": "Hay un tercio de opciones de recorte.",
    "veces_de": "Sale bien dos veces de tres.",
    "ingles": "There is a seventy percent chance of a rally.",
    "quinto": "Estimamos el riesgo de caída en un quinto.",
    "confiamos": "Confiamos al noventa en que el dólar suba.",
    "mk_veces_de": "Sale bien {n:DIV} veces de {candidatas:DIV}.",
    "mk_contra": "Con {n_ideas} contra {n_tipos}, la subida gana.",
    "espaciado": "Comprar N V D A ya.",
    "accion_min": "La apuesta es la acción nvda.",
    "tracker_min": "Recomendamos el tracker iwda.",
    "fondo_min5": "Recomendamos el fondo vwrl.",
    "token_min": "Comprar el token pepe.",
}
LEGITIMAS_QUITADAS = {
    "fondo_es": "El fondo es sencillo y barato.", "etf_sube": "El ETF sube con el oro.",
    "medio_plazo": "Es probable que el euro se aprecie a medio plazo.", "cada_etf": "Cada ETF tiene su propio coste.",
}
RES: list[tuple[str, str]] = []


def informe(nombre, estado, detalle):
    RES.append((nombre, estado))
    print(f"[{estado:5}] {nombre}: {detalle}", flush=True)


def _todos(f):
    def iny(out, msg):
        out["regimen_macro"] = "Marca régimen. " + f
        for x in out.get("factores_dominantes") or []:
            x["factor"] = "Marca factor. " + f
        out["preguntas_sugeridas"] = ["¿Marca pregunta? " + f]
        out["lectura_conjunto"] = "Marca lectura. " + f
        out["limitaciones"] = ["Marca limitación. " + f]
        out["frases_30s"][0] = "Marca treinta. " + f
        for t in out["tarjetas"]:
            t["por_que_llano"] = ("Marca. " + f)[:160]
            t["que_puede_salir_mal_llano"] = ("Marca. " + f)[:200]
            t["ambito_llano"] = ("Marca. " + f)[:160]
        out["glosario"] = [{"termino": "Carry", "definicion": "Marca glosario. " + f}]
        out["frase_historial"] = "Marca historial. " + f
    return iny


def t_fugas():
    llegan = {}
    for k, f in FUGAS.items():
        firma = v6.rellenar(f, MARCAS).rstrip(".").strip()
        r = C.ciclo(_todos(f))
        if "error" in r:
            llegan[k] = ("ERROR", r["error"])
            continue
        en = [n for n in ("paquete", "json", "html", "md") if firma in " ".join(r[n].split())]
        decl = [x for x in r["limitaciones"] if "quitad" in x.lower()]
        llegan[k] = {"firma": firma, "llega_a": en, "declarado": bool(decl), "G3": r["dictamen"]}
        print(f"    {k}: {llegan[k]}")
    n = sum(1 for v in llegan.values() if isinstance(v, dict) and v["llega_a"])
    sin_decl = sum(1 for v in llegan.values() if isinstance(v, dict) and v["llega_a"] and not v["declarado"])
    informe("fugas", "FALLO" if n else "OK", f"llegan {n}/{len(FUGAS)} (sin declarar {sin_decl})")


def t_legitimas():
    for k, f in LEGITIMAS_QUITADAS.items():
        r = C.ciclo(_todos(f))
        if "error" in r:
            informe(f"legitima_{k}", "ERROR", r["error"])
            continue
        llega = f.rstrip(".") in r["html"]
        decl = [x for x in r["limitaciones"] if "quitad" in x.lower()]
        tarjeta = r["red"]["tarjetas"][0]["por_que_llano"]
        informe(f"legitima_{k}", "FALLO" if not llega else "OK",
                f"llega al HTML {llega}; declarado {decl[:1]}; tarjeta 0 = {tarjeta!r}; G3 {r['dictamen']}")


def t_nombre_llano():
    mr = M["mr"]
    casos = {"prob_letra": "Divisas con tres contra uno a favor", "ticker_min": "Divisas vía el tracker fxe",
             "tercio": "Un tercio de opciones de subida del euro", "control_ticker": "Divisas vía FXE y UUP"}
    orig = mr._analista if hasattr(mr, "_analista") else None
    for k, nombre in casos.items():
        def iny(out, msg, nombre=nombre):
            out["frases_30s"][0] = "Destacamos {%s}." % OPP
        # el nombre llano lo pone el Analista; se cambia en el paquete que ve el Sintetizador y en el de la redacción
        orig_gen = None
        b_ciclo = C.ciclo

        def ciclo_con_nombre(inyectar):
            orig_marcadores = v6.marcadores

            def marc(paquete, perm=None):
                for d in (paquete.get("clases") or {}).values():
                    for o in d.get("opciones") or []:
                        o["nombre_llano"] = nombre
                return orig_marcadores(paquete, perm)
            v6.marcadores = marc
            try:
                return b_ciclo(inyectar)
            finally:
                v6.marcadores = orig_marcadores
        r = ciclo_con_nombre(iny)
        if "error" in r:
            informe(f"nombre_llano_{k}", "ERROR", r["error"])
            continue
        treinta = r["red"]["frases_30s"][0]
        informe(f"nombre_llano_{k}", "FALLO" if nombre in treinta else "OK", f"frase de 30 s: {treinta!r}")
    del orig, orig_gen


def t_glosario():
    casos = {"termino_lista": [{"termino": ["NVDA"], "definicion": "Un valor."}],
             "termino_ticker": [{"termino": "NVDA", "definicion": "La acción que más nos gusta."}],
             "termino_prob": [{"termino": "Tres contra uno", "definicion": "Lo que pagan las apuestas."}],
             "definicion_num": [{"termino": "Carry", "definicion": 7}],
             "entrada_texto": ["Comprar NVDA"]}
    for k, g in casos.items():
        def iny(o, msg, g=g):
            o["glosario"] = g
        r = C.ciclo(iny)
        if "error" in r:
            informe(f"glosario_{k}", "FALLO", r["error"])
            continue
        fuga = any(x in r["html"] for x in ("NVDA", "Tres contra uno"))
        informe(f"glosario_{k}", "FALLO" if fuga else "OK", f"glosario entregado {r['red']['glosario']}; G3 {r['dictamen']}")


def t_reescritura():
    larga = ("Las consideraciones macroeconómicas internacionalizadas multidimensionalmente condicionan extraordinariamente "
             "la interpretación probabilísticamente fundamentada de correlaciones intertemporales heterogéneas")
    n = {"k": 0}

    def iny(o, msg):
        n["k"] += 1
        if n["k"] == 1:
            o["frases_30s"] = [larga + ".", larga + ".", larga + "."]
            for t in o["tarjetas"]:
                t["por_que_llano"] = larga[:150] + "."
            o["frase_historial"] = larga + "."
        else:
            o["frases_30s"][0] = "Las apuestas pagan tres contra uno a favor de la subida. El dólar manda."
            o["frases_30s"][1] = "Recomendamos el tracker iwda."
    r = C.ciclo(iny)
    if "error" in r:
        return informe("reescritura", "FALLO", r["error"])
    llegan = [x for x in ("tres contra uno", "iwda") if x in r["html"]]
    informe("reescritura", "FALLO" if llegan else "OK", f"llamadas {n['k']}; llegan al HTML {llegan}; G3 {r['dictamen']}")


PRUEBAS = [t_fugas, t_legitimas, t_nombre_llano, t_glosario, t_reescritura]

if __name__ == "__main__":
    for p in PRUEBAS:
        if FILTRO and FILTRO not in p.__name__:
            continue
        try:
            p()
        except Exception as e:   # noqa: BLE001
            informe(p.__name__[2:], "ERROR", f"{type(e).__name__}: {e}")
    print(f"\nResumen: {sum(1 for r in RES if r[1] == 'OK')} OK, {sum(1 for r in RES if r[1] == 'FALLO')} FALLO, "
          f"{sum(1 for r in RES if r[1] == 'ERROR')} ERROR")
