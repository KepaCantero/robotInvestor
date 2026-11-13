"""QA r03 de T-102 · Ataques al rediseño con marcadores (regla estricta CIFRA / R21 / MARCADOR).

Cada ataque es una frase que, por R13 (probabilidad numérica sin certificado) o R21 (un instrumento concreto), NO debe llegar
al paquete ni a los entregables. Se mide primero con `limpiar` (con los permitidos y los marcadores REALES de un ciclo) y,
para las que pasan, por el camino real: un ciclo C1 simulado en que el Sintetizador escribe la frase en TODOS sus textos, y se
busca su firma en el paquete, la redacción y los tres entregables, y si se declaró algo.

Uso (desde la raíz del repositorio):
  .venv/bin/python -I .docs/tickets/T-102/revisores/r03_01_ataques.py <raiz_repo> [-k <parte del nombre>]
Imprime [OK] / [FALLO] / [OBS] por comprobación. No escribe nada en el repositorio.
"""
from __future__ import annotations

import sys
import time
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
PERM = v6.permitidos_r21(C.bloque())
RES: list[tuple[str, str, str]] = []


def informe(nombre, estado, detalle):
    RES.append((nombre, estado, detalle))
    print(f"[{estado:5}] {nombre}: {detalle}", flush=True)


def quitada(frase: str) -> str | None:
    """La regla con que se quita la frase con los marcadores reales, o None si pasa."""
    salida, reglas = v6.limpiar("El dólar sube. " + frase, PERM, MARCAS)
    return reglas[0] if reglas else None


# (id, regla que incumple, frase) · las de «control» deben quitarse ya; las demás son los ataques
R13 = [
    # Otras escrituras de las cifras
    ("sup", "Probabilidad de subida: ⁷⁰ %."), ("sub", "Probabilidad de subida: ₇₀ %."),
    ("frac23", "La probabilidad de subida es de ⅔."), ("frac34", "Hay ¾ de probabilidad de que el euro suba."),
    ("circ", "Probabilidad de subida: ⑦ sobre ⑩."), ("romano_u", "Probabilidad de subida: Ⅶ sobre Ⅹ."),
    ("romano_min", "Probabilidad de subida: lxx %."), ("romano_may", "Probabilidad de subida: LXX %."),
    ("ctl_ancho", "Probabilidad de subida: ７０ %."), ("ctl_arabe", "Probabilidad de subida: ٧٠ %."),
    ("ctl_matem", "Probabilidad de subida: 𝟕𝟎 %."), ("ctl_tecla", "Probabilidad de subida: 7️⃣0️⃣ %."),
    # Cifras en letra
    ("por_cien", "Vemos un setenta por cien de probabilidad de subida."),
    ("letra_pct", "La probabilidad de subida es del setenta %."),
    ("sobre_cien", "Probabilidad de subida: setenta sobre cien."),
    ("entre", "La probabilidad de recorte es de tres entre cuatro."),
    ("a_uno", "Las probabilidades son de tres a uno a favor de la subida."),
    ("confianza", "Con una confianza de dos tercios, el BCE recortará en enero."),
    ("cuartas", "Hay tres cuartas partes de probabilidad de que el euro suba."),
    ("decimas", "La probabilidad de subida es de siete décimas."),
    ("de_cada_veinte", "Diecinueve de cada veinte veces el oro sube en este régimen."),
    ("de_cada_mil", "Novecientos de cada mil escenarios acaban en subida."),
    ("cincuenta", "Lo vemos al cincuenta por cien: puede subir o bajar."),
    ("del_noventa", "Le damos una probabilidad del noventa a la subida."),
    ("escenarios", "El escenario base pesa la mitad, el alcista un cuarto y el bajista otro cuarto."),
    ("p_igual", "P(subida) = setenta por cien."),
    ("ctl_por_ciento", "Vemos un setenta por ciento de probabilidades de subida."),
    ("ctl_de_cada", "Siete de cada diez veces sube."), ("ctl_tercios", "La probabilidad de subida es de dos tercios."),
    # Cifras que componen los marcadores (las pone el código, pero las ordena el Sintetizador)
    ("mk_pct", "La probabilidad de subida es del {n_ideas}{n_tipos} %."),
    ("mk_sobre", "La probabilidad de acierto es de {n:DIV} sobre {candidatas:DIV}."),
    ("mk_de_cada", "Las opciones de que el euro suba son {n:DIV} de cada {candidatas:DIV}."),
    ("mk_conf", "Confianza del {n_apuestas}{n_tipos} %."),
]
R21 = [
    ("minus", "Recomendamos el ETF qqq."), ("minus2", "La opción preferida es nvda."), ("dolar_minus", "Comprar $tsla ya."),
    ("mixto", "La opción preferida es Nvda."), ("mixto2", "Comprar AApl ya."),
    ("ctl_latina", "Recomendamos el ETF QQQ."),
    ("homoglifo_gr", "La opción preferida es ΝVDΑ."),     # Ν y Α griegas
    ("homoglifo_cir", "Recomendamos el fondo ЅРY."),       # Ѕ y Р cirílicas
    ("ancho", "La opción preferida es ＮＶＤＡ."),
    ("guion_bajo", "Comprar _NVDA ya."), ("guion", "Comprar renta variable-NVDA."), ("igual", "Comprar =NVDA."),
    ("punto", "Comprar acciones.NVDA ya."),
    ("ctl_zw", "La opción preferida es NV​DA."), ("ctl_shy", "La opción preferida es NV­DA."),
    ("calif_AA", "Comprar AA tras los resultados."), ("calif_BB", "La opción preferida es BB."),
    ("lista_COP", "Comprar COP antes del dividendo."), ("lista_ETN", "La opción preferida es ETN."),
    ("lista_AI", "Comprar AI es la idea de la semana."), ("lista_UST", "Recomendamos el ETF UST."),
    ("una_letra", "Vender el REIT O antes de la subida de tipos."), ("una_letra_F", "Comprar F ya."),
    ("inc_punto", "Recomendamos Apple Inc."), ("corp_punto", "Comprar Microsoft Corp. cuanto antes."),
    ("coma_inc", "La opción preferida es Tesla, Inc."), ("plc_punto", "Comprar Unilever plc."),
    ("inc_minus", "Comprar Apple inc ya."), ("fund", "Recomendamos el Vanguard Global Stock Index Fund."),
    ("indice_traga", "Recomendamos el ETF MSCI World IWDA."), ("indice_traga2", "Comprar el S&P SPY ya."),
    ("indice_traga3", "La opción preferida es el FTSE All-World VWRL."),
    ("ucits", "Recomendamos el Amundi MSCI World UCITS ETF."),
    ("ctl_sa", "Comprar Banco Santander, S.A."), ("ctl_mayus", "Comprar NVDA ya."), ("ctl_sufijo", "Comprar Apple Inc ya."),
]
MARC = [
    ("anidado", "{opp:{n_ideas}} depende del dólar."), ("doble", "Vemos {{n_ideas}} ideas."), ("mayus", "Vemos {N_IDEAS} ideas."),
    ("ajeno", "{opp:OPP-2099-0001} depende del dólar."), ("llave_unicode", "Vemos ｛n_ideas｝ ideas y ❴total❵ tipos."),
]


def _bateria(nombre, casos, regla):
    pasan = {k: f for k, f in casos if not k.startswith("ctl_") and quitada(f) is None}
    ctl = {k: (f, quitada(f)) for k, f in casos if k.startswith("ctl_")}
    ctl_mal = {k: x for k, x in ctl.items() if x[1] is None}
    total = sum(1 for k, _ in casos if not k.startswith("ctl_"))
    informe(nombre, "FALLO" if pasan else "OK", f"pasan {len(pasan)}/{total} ({regla}): {list(pasan.values())}"
            + (f"; controles que pasan: {ctl_mal}" if ctl_mal else f"; {len(ctl)} controles quitados"))
    return pasan


def t_r13_unidad():
    return _bateria("r13_unidad", R13, "R13")


def t_r21_unidad():
    return _bateria("r21_unidad", R21, "R21")


def t_marcadores_unidad():
    out = {k: (quitada(f), v6.limpiar(f, PERM, MARCAS)[0]) for k, f in MARC}
    raros = {k: x for k, x in out.items() if x[0] is None}
    informe("marcadores_unidad", "OBS" if raros else "OK", f"{out}")


def _camino_real(nombre, frases: dict[str, str]):
    """Cada frase, en todos los textos del Sintetizador, por un ciclo real; ¿llega su firma? ¿se declara algo?"""
    llegan = {}
    for k, f in frases.items():
        firma = v6.rellenar(f, MARCAS).rstrip(".").strip()

        def iny(out, msg, f=f):
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
        r = C.ciclo(iny)
        if "error" in r:
            llegan[k] = ("ERROR", r["error"])
            continue
        en = [n for n in ("json", "html", "md") if firma in " ".join(r[n].split())]
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        if en or firma in r["todo"]:
            llegan[k] = {"firma": firma, "entregables": en, "declarado": bool(decl), "dictamen": r["dictamen"]}
    informe(nombre, "FALLO" if llegan else "OK", f"llegan {len(llegan)}/{len(frases)}: {llegan}")


def t_camino_real_r13():
    _camino_real("camino_real_r13", {k: f for k, f in R13 if not k.startswith("ctl_") and quitada(f) is None})


def t_camino_real_r21():
    _camino_real("camino_real_r21", {k: f for k, f in R21 if not k.startswith("ctl_") and quitada(f) is None})


def t_nombre_llano_con_ticker():
    """El valor de {opp:…} es el `nombre_llano` de un Analista (un LLM); lo que pone el código no se filtra."""
    mr = M["mr"]
    orig = mr._ficha

    def ficha(u, msg, ctx, rng, iny):
        f = orig(u, msg, ctx, rng, iny)
        f["nombre_llano"] = ("Divisas vía FXE y UUP " + f["nombre_llano"])[:70]
        return f
    mr._ficha = ficha
    try:
        def iny(out, msg):
            opp = next(o["opp_id"] for c in msg["paquete_sintesis"]["clases"].values() for o in c["opciones"])
            out["frases_30s"][0] = "{opp:%s} depende del dólar." % opp
            out["lectura_conjunto"] = "{opp:%s} es la idea más sensible al dólar." % opp
        r = C.ciclo(iny)
    finally:
        mr._ficha = orig
    if "error" in r:
        return informe("nombre_llano_con_ticker", "OBS", r["error"])
    en_sint = [k for k in ("frases_30s",) if "FXE" in str(r["red"].get(k))] + (["x_lectura_conjunto"] if "FXE" in r["paquete"] and
                                                                               "Divisas vía FXE" in str(r["res"]["paquete"].get("x_lectura_conjunto")) else [])
    informe("nombre_llano_con_ticker", "OBS" if en_sint else "OK",
            f"«FXE» en textos del Sintetizador: {en_sint}; dictamen G3 de entregables {r['dictamen']}; "
            f"en el paquete G3 {r['res'].get('g3', {}).get('dictamen') if isinstance(r['res'].get('g3'), dict) else r['res'].get('g3')}")


def t_glosario_no_texto():
    """El esquema SINTESIS no tipa `definicion`: una lista o un número no pasan por el filtro."""
    out = {}
    for k, d in {"lista": ["Comprar NVDA ya."], "numero": 70, "objeto": {"t": "Comprar NVDA"}}.items():
        def iny(o, msg, d=d):
            o["glosario"] = [{"termino": "Carry", "definicion": d}]
        r = C.ciclo(iny)
        out[k] = r["error"] if "error" in r else ("NVDA en entregables" if "NVDA" in r["html"] + r["md"] + r["json"] else
                                                  ("NVDA en red" if "NVDA" in r["red_txt"] else "no llega"))
    mal = {k: v for k, v in out.items() if v != "no llega"}
    informe("glosario_no_texto", "FALLO" if mal else "OK", f"{out}")


def t_campos_no_filtrados():
    """Claves que el código no filtra: ¿llegan a algún entregable?"""
    def iny(o, msg):
        for t in o["tarjetas"]:
            t["titulo_llano"] = "Comprar NVDA ya."
            t["nombre_llano"] = "Comprar NVDA ya."
        o["glosario"] = [{"termino": "Carry", "definicion": "Diferencial de tipos.", "ejemplo": "Comprar NVDA ya."}]
        o["motivos_llanos"] = {"NVDA": "Comprar NVDA ya.", "DIV": ["Comprar NVDA ya."]}
        o["cambios_vs_anterior"] = "Comprar NVDA ya."
        o["tarjetas"].append({"opp_id": "OPP-2099-0001", "por_que_llano": "Comprar NVDA ya.", "que_puede_salir_mal_llano": "x"})
    r = C.ciclo(iny)
    if "error" in r:
        return informe("campos_no_filtrados", "FALLO", r["error"])
    en = [n for n in ("json", "html", "md") if "NVDA" in r[n]]
    informe("campos_no_filtrados", "FALLO" if en else "OK",
            f"NVDA en entregables: {en}; en la redacción interna (no se entrega): {'NVDA' in r['red_txt']}")


def t_reescritura():
    """Primera respuesta ilegible (fuerza la reescritura) y la segunda con ataques que pasan la unidad y otros que no."""
    larga = ("Las consideraciones macroeconómicas internacionalizadas multidimensionalmente condicionan extraordinariamente "
             "la interpretación probabilísticamente fundamentada de correlaciones intertemporales heterogéneas")
    n = {"k": 0}

    def iny(o, msg):
        n["k"] += 1
        if n["k"] == 1:
            o["frases_30s"] = [larga + ". Comprar NVDA.", larga + ".", larga + "."]
            for t in o["tarjetas"]:
                t["por_que_llano"] = larga[:150] + "."
            o["frase_historial"] = larga + "."
        else:
            o["frases_30s"][0] = "Vemos un setenta por cien de probabilidad de subida. Comprar TSLA ya."
            o["frases_30s"][1] = "Recomendamos el ETF qqq."
    r = C.ciclo(iny)
    if "error" in r:
        return informe("reescritura", "FALLO", r["error"])
    llegan = [x for x in ("setenta por cien", "qqq", "TSLA", "NVDA") if x in r["todo"]]
    llanas = [x for x in r["limitaciones"] if x.startswith("Frases llanas")]
    informe("reescritura", "FALLO" if llegan else "OK",
            f"llamadas al Sintetizador {n['k']}; llegan {llegan}; declaración de la redacción entregada: {llanas}")


def t_frase_a_frase_y_declaracion():
    """CA-3/CA-4/CA-14: una frase mala no tira las demás, lo vacío toma su defecto, y lo quitado se cuenta y se declara."""
    def iny(o, msg):
        o["frases_30s"][1] = "Comprar NVDA ya."
        o["tarjetas"][0]["por_que_llano"] = "Lo mueve el dólar. Comprar NVDA ya."
        o["tarjetas"][1]["que_puede_salir_mal_llano"] = "Hay un setenta por ciento de probabilidad de caída."
    r = C.ciclo(iny)
    red, defe = r["red"], BASE["red"]
    ok = (red["frases_30s"][0] == BASE["red"]["frases_30s"][0] and red["tarjetas"][0]["por_que_llano"] == "Lo mueve el dólar."
          and red["tarjetas"][2] == defe["tarjetas"][2])
    llanas = [x for x in r["limitaciones"] if x.startswith("Frases llanas")]
    informe("frase_a_frase_y_declaracion", "OK" if ok and llanas and r["dictamen"] != "BLOQUEADO" else "FALLO",
            f"30s[1]={red['frases_30s'][1]!r}; tarjeta0={red['tarjetas'][0]['por_que_llano']!r}; "
            f"tarjeta1 mal={red['tarjetas'][1]['que_puede_salir_mal_llano']!r}; {llanas}; dictamen {r['dictamen']}")


def t_rendimiento():
    casos = {"espacios_50k": "Comprar oro" + " " * 50000 + "ya.", "tabs_50k": "x" + "\t" * 50000 + "y",
             "llaves_50k": "{" * 50000, "marcadores_20k": "{n_ideas}" * 20000, "mayusculas_50k": "ABCDE " * 10000,
             "capitalizadas_sufijo": "Aa " * 15000 + "Inc", "indice_50k": "MSCI World " * 5000,
             "probabilidad_mitad": "probabilidad mitad " * 3000, "puntos": ". " * 25000}
    t = {}
    for k, s in casos.items():
        t0 = time.perf_counter()
        v6.limpiar(s, PERM, MARCAS)
        t[k] = round(time.perf_counter() - t0, 3)
    escala = {}
    for n in (5000, 10000, 20000, 40000):
        s = "Comprar oro" + " " * n + "ya."
        t0 = time.perf_counter()
        v6.limpiar(s, PERM, MARCAS)
        escala[n] = round(time.perf_counter() - t0, 3)
    lentos = {k: v for k, v in t.items() if v > 1}
    informe("rendimiento", "FALLO" if lentos else "OK", f"total {round(sum(t.values()), 2)} s; {t}; escala de espacios {escala}")


PRUEBAS = [t_r13_unidad, t_r21_unidad, t_marcadores_unidad, t_camino_real_r13, t_camino_real_r21, t_nombre_llano_con_ticker,
           t_glosario_no_texto, t_campos_no_filtrados, t_reescritura, t_frase_a_frase_y_declaracion, t_rendimiento]

if __name__ == "__main__":
    print(f"Marcas reales del ciclo base: {MARCAS}")
    for p in PRUEBAS:
        if FILTRO and FILTRO not in p.__name__:
            continue
        try:
            p()
        except Exception as e:   # noqa: BLE001
            informe(p.__name__[2:], "ERROR", f"{type(e).__name__}: {e}")
    print(f"\nResumen: {sum(1 for r in RES if r[1] == 'OK')} OK, {sum(1 for r in RES if r[1] == 'FALLO')} FALLO, "
          f"{sum(1 for r in RES if r[1] == 'OBS')} OBS, {sum(1 for r in RES if r[1] == 'ERROR')} ERROR")
