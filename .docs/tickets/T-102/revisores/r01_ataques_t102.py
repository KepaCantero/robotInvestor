"""QA r01 de T-102 · Ataques al filtro R13/R21 frase a frase de los textos del Sintetizador (diseño V6, cliente simulado).

Comprueba la división en frases (abreviaturas, cifras, signos de interrogación, saltos de línea), los textos vacíos o que no
son texto, que un texto que se queda vacío tome el suyo por defecto (y solo el suyo), la declaración de lo quitado, la segunda
pasada de HT-09 con la reescritura por legibilidad, y el rendimiento con textos largos.

Uso (desde la raíz del repositorio; la raíz del código a atacar es opcional, por defecto el repositorio):
  .venv/bin/python -I .docs/tickets/T-102/revisores/r01_ataques_t102.py [<raiz_repo>] [-k <filtro>]

Cada ataque imprime OK, FALLO (contradice el ticket, el README o una regla) u OBS (observación sin veredicto). Sale con 1 si
hay algún FALLO o ERROR. No escribe nada fuera de carpetas temporales.
"""
from __future__ import annotations

import json
import sys
import tempfile
import time
import traceback
from pathlib import Path

ARGS = list(sys.argv[1:])
FILTRO = None
if "-k" in ARGS:
    i = ARGS.index("-k")
    FILTRO = ARGS[i + 1]
    del ARGS[i:i + 2]
RAIZ = Path(ARGS[0] if ARGS else ".").resolve()
EJEC = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJEC / "tests"))
sys.path.insert(0, str(EJEC))

from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

from bloque_a import diseno_v6 as v6  # noqa: E402
from bloque_a import mock_respuestas as mr  # noqa: E402
from bloque_a.configuracion import CLASES, RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from bloque_a.redaccion import AMBITO_LLANO_DEFECTO  # noqa: E402

assert Path(v6.__file__).resolve().is_relative_to(EJEC.resolve()), v6.__file__
RES: list[tuple[str, str, str]] = []
UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def informe(nombre, estado, detalle=""):
    RES.append((nombre, estado, detalle))
    print(f"[{estado:5}] {nombre}: {detalle}", flush=True)


def bloque(perfiles=("DIV",)):
    tmp = Path(tempfile.mkdtemp(prefix="r01_t102_"))
    c = config_pruebas(diseno="v6", perfiles={"activos": list(perfiles)}, seleccion={"umbral_senal_gc1": 0.55})
    return Bloque(c, ProveedorCSV(DATOS), UNIVERSO, MockClient(), tmp / "estado", tmp / "ent")


_PERM = None


def perm():
    global _PERM
    if _PERM is None:
        _PERM = v6.permitidos_r21(bloque(tuple(CLASES)))
    return _PERM


def ciclo_con_sintetizador(cambiar, perfiles=("DIV",)):
    """Un ciclo V6 en el que el Sintetizador simulado escribe lo que da `cambiar(out, n)` (n = número de llamada, desde 1).
    Devuelve el bloque, el resultado del ciclo, la lista de `red` que recibió `generar` y el número de llamadas."""
    orig = mr._sintetizador
    n = {"llamadas": 0}

    def g(msg, ctx, rng):
        n["llamadas"] += 1
        out = orig(msg, ctx, rng)
        cambiar(out, n["llamadas"])
        return out
    mr._sintetizador = g
    try:
        b = bloque(perfiles)
        reds = []
        gen = b.redaccion.generar

        def generar(bl, paquete, extras, red, *a, **k):
            reds.append(json.loads(json.dumps(red, ensure_ascii=False)))
            return gen(bl, paquete, extras, red, *a, **k)
        b.redaccion.generar = generar
        r = b.ciclo(AS_OF)
    finally:
        mr._sintetizador = orig
    return b, r, reds, n["llamadas"]


def entregables_texto(r) -> str:
    e = r.get("entregables") or {}
    return " ".join(Path(p).read_text(encoding="utf-8") for p in e.values() if isinstance(p, str) and Path(p).exists())


# ============================================================================================== bancos de la QA de T-101
def _lista_literal(ruta: Path, nombre: str):
    import ast
    arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    for n in arbol.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nombre for t in n.targets):
            return ast.literal_eval(n.value)
    raise KeyError(nombre)


def at_bancos_anteriores():
    """CA-1 y CA-2: los bancos de `r02_ataques_v6.py` y `r03_ataques_v6.py` de T-101, con los códigos permitidos reales."""
    rev = Path(__file__).resolve().parents[2] / "T-101" / "revisores"
    leg = list(_lista_literal(rev / "r02_ataques_v6.py", "LEGITIMOS"))
    leg += [t for ts in _lista_literal(rev / "r03_ataques_v6.py", "LEGITIMOS").values() for t in ts]
    pro = list(_lista_literal(rev / "r02_ataques_v6.py", "PROHIBIDOS")) + list(_lista_literal(rev / "r03_ataques_v6.py", "PROHIBIDOS"))
    fp = [t for t in leg if v6.texto_prohibido(t, perm())]
    fn = [(r, t) for r, t in pro if v6.texto_prohibido(t, perm()) != r]
    limite = [x for x in fn if "Tesla" in x[1]]
    informe("bancos_anteriores", "OK" if not fp and fn == limite else "FALLO",
            f"legítimas quitadas {len(fp)}/{len(leg)} {fp}; prohibidas no cazadas con su regla {len(fn)}/{len(pro)} {fn} "
            f"(límite declarado: {len(limite)})")


def at_regresion_frente_a_t101():
    """Frases que el filtro de T-101 (commit 9b4741a) cazaba y el de T-102 deja pasar (comprobado con `r01_banco_frases.py`
    sobre las dos raíces): «probabilidad» separada de la cifra por una subordinada, y el código entre paréntesis tras una coma."""
    casos = [("R13", "La probabilidad de que el S&P 500 suba este mes es del 70 %."),
             ("R13", "Las probabilidades de un recorte en marzo son del 60 %."),
             ("R13", "La probabilidad de que bajen los alquileres es del 40 %."),
             ("R13", "El escenario alcista tiene una probabilidad estimada del 65 %."),
             ("R13", "La probabilidad implícita de un movimiento del 5 % es del 18 %."),
             ("R21", "Compra, esta semana, acciones de Apple (AAPL).")]
    pasan = [(r, t) for r, t in casos if v6.texto_prohibido(t, perm()) != r]
    informe("regresion_frente_a_t101", "FALLO" if pasan else "OK", f"{len(pasan)}/{len(casos)} pasan: {pasan}")


# ============================================================================================== división en frases
def at_division_abreviatura_legitima():
    """«EE. UU.» parte la frase en dos, pero al juntar lo que queda el texto legítimo debe salir entero."""
    t = "La renta variable de EE. UU. sube un 2 %. Conviene comprar AAPL. El dólar cae frente al EUR."
    limpio, reglas = v6.limpiar(t, perm())
    esperado = "La renta variable de EE. UU. sube un 2 %. El dólar cae frente al EUR."
    informe("division_abreviatura_legitima", "OK" if (limpio, reglas) == (esperado, ["R21"]) else "FALLO", f"{reglas} «{limpio}»")


def at_division_abreviatura_esconde_compra():
    """Si la compra va después de «EE. UU.», la abreviatura separa el verbo del código y la compra no se ve."""
    casos = ["Conviene comprar acciones de EE. UU. como AAPL esta semana.",
             "Vender bancos de EE. UU. y en concreto JPM.",
             "Comprar tecnológicas de EE. UU. (AAPL, MSFT)."]
    res = {t: v6.texto_prohibido(t, perm()) for t in casos}
    pasan = [t for t, r in res.items() if r is None]
    informe("division_abreviatura_esconde_compra", "FALLO" if pasan else "OK", f"{len(pasan)}/{len(casos)} pasan: {pasan}")


def at_division_deja_fragmentos():
    """Al quitar una frase cortada por una abreviatura (S.A., EE.UU.), queda un trozo suelto en el texto."""
    casos = ["Comprar acciones de Banco Santander S.A. ya. El dólar cae.", "Comprar bonos de EE.UU. a dos años. El dólar cae."]
    res = [(t, *v6.limpiar(t, perm())) for t in casos]
    malos = [(t, lim) for t, lim, _r in res if not lim.startswith("El dólar")]
    informe("division_deja_fragmentos", "FALLO" if malos else "OK", "; ".join(f"«{t}» → «{lim}»" for t, lim in malos))


def at_division_sufijo_sa():
    """El README promete detectar un sufijo societario; el patrón incluye «S.A.», pero `S\\.A\\.\\b` no puede casar nunca
    (no hay límite de palabra entre «.» y un espacio o el final). «Apple Inc» y «Microsoft Corp» sí se cazan sin verbo."""
    casos = {"Telefónica S.A. mejora márgenes.": v6.frase_prohibida("Telefónica S.A. mejora márgenes.", perm()),
             "Banco Santander S.A.": v6.frase_prohibida("Banco Santander S.A.", perm()),
             "Apple Inc mejora márgenes.": v6.frase_prohibida("Apple Inc mejora márgenes.", perm()),
             "Microsoft Corp mejora márgenes.": v6.frase_prohibida("Microsoft Corp mejora márgenes.", perm())}
    sa_muerto = casos["Telefónica S.A. mejora márgenes."] is None and casos["Banco Santander S.A."] is None
    informe("division_sufijo_sa", "FALLO" if sa_muerto else "OK", str(casos))


def at_division_cifras():
    """Los puntos y comas de las cifras no parten frases."""
    t = "El IBEX sube un 1.5 % y el bono rinde un 4,25 %; la emisión supera los 1.000 millones. Comprar AAPL."
    limpio, reglas = v6.limpiar(t, perm())
    ok = limpio == "El IBEX sube un 1.5 % y el bono rinde un 4,25 %; la emisión supera los 1.000 millones." and reglas == ["R21"]
    informe("division_cifras", "OK" if ok else "FALLO", f"{reglas} «{limpio}»")


def at_division_interrogacion_exclamacion():
    casos = {"¿Conviene comprar AAPL? El dólar sube.": "El dólar sube.",
             "¡Comprar AAPL ya! El dólar sube.": "El dólar sube.",
             "El dólar sube. ¿Qué haría cambiar el semáforo de RV?": "El dólar sube. ¿Qué haría cambiar el semáforo de RV?"}
    malos = {t: v6.limpiar(t, perm())[0] for t, esp in casos.items() if v6.limpiar(t, perm())[0] != esp}
    informe("division_interrogacion", "FALLO" if malos else "OK", str(malos))


def at_division_saltos_de_linea_y_puntos_suspensivos():
    """Un salto de línea sin punto o unos puntos suspensivos («…») no separan frases: se quita también lo legítimo. Y en un
    texto sin nada prohibido, los saltos de línea se convierten en espacios."""
    a = v6.limpiar("El dólar sube frente al euro\nConviene comprar AAPL", perm())
    b = v6.limpiar("El dólar sube frente al euro… Conviene comprar AAPL.", perm())
    c = v6.limpiar("El dólar sube.\n\nEl euro baja.", perm())
    pierde = a[0] == "" or b[0] == ""
    informe("division_saltos_y_suspensivos", "OBS", f"salto sin punto → «{a[0]}» {a[1]}; «…» → «{b[0]}» {b[1]}; "
            f"párrafos sin nada prohibido → {c[0]!r}" + (" (se pierde la parte legítima)" if pierde else ""))


# ============================================================================================== vacíos y no texto
def at_vacios_y_no_texto():
    raros = [None, 0, 1.5, float("nan"), True, [], {}, ["Comprar AAPL."], {"t": "Comprar AAPL."}, b"Comprar AAPL.", "", "   ", "\n\n"]
    errores, res = [], {}
    for x in raros:
        try:
            res[repr(x)] = (v6.texto_prohibido(x, perm()), v6.limpiar(x, perm()))
        except Exception as e:   # noqa: BLE001
            errores.append(f"{x!r}: {type(e).__name__}: {e}")
    try:
        sin_perm = (v6.texto_prohibido("Conviene vender EURUSD."), v6.texto_prohibido("Conviene vender EURUSD.", ["EUR", "USD"]),
                    v6.texto_prohibido("Conviene vender EURUSD.", "EURUSD"))
    except Exception as e:   # noqa: BLE001
        errores.append(f"permitidos raros: {type(e).__name__}: {e}")
        sin_perm = None
    informe("vacios_y_no_texto", "FALLO" if errores else "OK",
            f"errores={errores}; sin permitidos / lista / cadena = {sin_perm}; "
            f"vacíos: {[res.get(repr(x)) for x in ('', '   ')]}; una lista o un dict con una compra: "
            f"{res.get(repr(['Comprar AAPL.']))} {res.get(repr({'t': 'Comprar AAPL.'}))} (no son textos: los llamadores filtran el tipo)")


# ============================================================================================== por defecto, elemento a elemento
def at_vacio_toma_su_defecto():
    """Cada elemento que se queda vacío toma su texto por defecto; los demás no cambian; todo se declara; nada llega."""
    capt = {}

    def cambiar(out, n):
        capt["orig"] = json.loads(json.dumps(out, ensure_ascii=False))
        out["frases_30s"][1] = "Conviene comprar AAPL cuanto antes."
        t0 = out["tarjetas"][0]
        t0["que_puede_salir_mal_llano"] = "Hay un 70 % de probabilidad de caída."
        if len(out["tarjetas"]) > 1:
            out["tarjetas"][1]["ambito_llano"] = "Comprar el ETF QQQ."
        out["motivos_llanos"] = {**(out.get("motivos_llanos") or {}), "RV": "Comprar NVDA es mejor."}
        out["frase_historial"] = "Hay un 70 % de probabilidad de acertar."
        out["tarjetas"].append({"opp_id": "OPP-9999-9999", "por_que_llano": "Comprar MSFT.", "que_puede_salir_mal_llano": "Nada."})
        capt["mod"] = json.loads(json.dumps(out, ensure_ascii=False))
    b, r, reds, n = ciclo_con_sintetizador(cambiar)
    red = reds[-1]
    defecto = b.redaccion.textos_por_defecto(r["paquete"])
    mod, problemas = capt["mod"], []
    if red["frases_30s"][1] != defecto["frases_30s"][1]:
        problemas.append(f"frases_30s[1]={red['frases_30s'][1]!r}")
    if [red["frases_30s"][0], red["frases_30s"][2]] != [mod["frases_30s"][0], mod["frases_30s"][2]]:
        problemas.append("cambian las otras frases de 30 s")
    t0 = red["tarjetas"][0]
    if t0["que_puede_salir_mal_llano"] != "El precio puede bajar más de lo previsto.":
        problemas.append(f"tarjeta 0 riesgo={t0['que_puede_salir_mal_llano']!r}")
    if t0["por_que_llano"] != mod["tarjetas"][0]["por_que_llano"]:
        problemas.append("cambia el «por qué» de la tarjeta 0")
    if len(mod["tarjetas"]) > 2 and red["tarjetas"][1].get("ambito_llano") != AMBITO_LLANO_DEFECTO:
        problemas.append(f"ámbito tarjeta 1={red['tarjetas'][1].get('ambito_llano')!r}")
    if "RV" in red["motivos_llanos"]:
        problemas.append("el motivo prohibido sigue")
    if red["frase_historial"] != defecto["frase_historial"]:
        problemas.append(f"historial={red['frase_historial']!r}")
    texto = json.dumps(r["paquete"], ensure_ascii=False) + entregables_texto(r)
    for x in ("AAPL", "QQQ", "NVDA", "70 % de probabilidad"):
        if x in texto:
            problemas.append(f"«{x}» llega a los entregables")
    lim = [x for x in r["paquete"]["limitaciones"] if "Frases llanas del Sintetizador quitadas" in x]
    informe("vacio_toma_su_defecto", "FALLO" if problemas or not lim else "OK",
            f"problemas={problemas}; limitación={lim}; tarjeta inventada → {red['tarjetas'][-1]}; dictamen={r['g3_entregables']['dictamen']}")


def at_glosario_quitado_se_declara():
    """CA-4: lo quitado se declara. Una entrada de glosario con una compra se quita entera: ¿se cuenta y se declara?"""
    def cambiar(out, n):
        out["glosario"] = [{"termino": "ETF", "definicion": "Fondo cotizado. Comprar QQQ es un ejemplo."},
                           {"termino": "Carry", "definicion": "Ganar el diferencial de tipos entre dos divisas."}]
    b, r, reds, n = ciclo_con_sintetizador(cambiar)
    glos = reds[-1]["glosario"]
    lim = [x for x in r["paquete"]["limitaciones"] if "Sintetizador quitadas" in x]
    quitada = all(g["termino"] != "ETF" for g in glos)
    declarada = bool(lim)
    informe("glosario_quitado_se_declara", "FALLO" if quitada and not declarada else "OK",
            f"glosario={[g['termino'] for g in glos]}; limitaciones del filtro={lim}")


def at_cuenta_de_lo_quitado():
    """La limitación cuenta las frases quitadas: tres en una tarjeta, una en las frases de 30 s y una en la integración."""
    def cambiar(out, n):
        out["tarjetas"][0]["por_que_llano"] = "Comprar AAPL. Comprar MSFT. Hay un 70 % de probabilidad de subida."
        out["frases_30s"][0] = out["frases_30s"][0] + " Comprar NVDA."
        out["lectura_conjunto"] = "Las opciones dependen del dólar. Comprar TSLA."
    b, r, reds, n = ciclo_con_sintetizador(cambiar)
    lim = [x for x in r["paquete"]["limitaciones"] if "quitadas" in x]
    ok = any("R13, R21: 4" in x for x in lim) and any(": 1 (lectura_conjunto (R21))" in x for x in lim)
    informe("cuenta_de_lo_quitado", "OK" if ok else "FALLO", str(lim))


# ============================================================================================== segunda pasada de HT-09
LARGA = ("Las consideraciones macroeconómicas internacionalizadas multidimensionalmente condicionan extraordinariamente "
         "la interpretación probabilísticamente fundamentada de correlaciones intertemporales heterogéneas")


def at_segunda_pasada_y_reescritura():
    """Primera respuesta ilegible y con una compra; la reescritura, legible y con otra compra. La segunda pasada de HT-09 no
    bloquea, nada prohibido llega y la limitación describe lo que se entrega (no se duplica la de la primera respuesta)."""
    def cambiar(out, n):
        if n == 1:
            out["frases_30s"] = [LARGA + ". Comprar AAPL.", LARGA + ".", LARGA + "."]
            for t in out["tarjetas"]:
                t["por_que_llano"] = LARGA[:150] + "."
            out["frase_historial"] = LARGA + "."
        else:
            out["frases_30s"][0] = out["frases_30s"][0] + " Comprar MSFT."
    b, r, reds, n = ciclo_con_sintetizador(cambiar)
    g3 = r["g3_entregables"]
    lim = [x for x in r["paquete"]["limitaciones"] if "Frases llanas del Sintetizador quitadas" in x]
    texto = json.dumps(r["paquete"], ensure_ascii=False) + entregables_texto(r)
    fugas = [x for x in ("AAPL", "MSFT") if x in texto]
    estado = "OK" if n == 2 and g3["dictamen"] != "BLOQUEADO" and not fugas and len(lim) == 1 else ("FALLO" if fugas or g3["dictamen"] == "BLOQUEADO" else "OBS")
    informe("segunda_pasada_y_reescritura", estado, f"llamadas AG-26={n}; dictamen={g3['dictamen']}; legibilidad={g3.get('legibilidad')}; "
            f"fugas={fugas}; limitaciones del filtro={lim}")


def at_segunda_pasada_con_muchas_quitadas():
    """Todas las frases y tarjetas con una frase prohibida: el paquete sale con los textos por defecto y legible."""
    def cambiar(out, n):
        out["frases_30s"] = ["Comprar AAPL.", "Hay un 70 % de probabilidad de subida.", "Vender TSLA."]
        for t in out["tarjetas"]:
            t["por_que_llano"] = "Comprar NVDA."
            t["que_puede_salir_mal_llano"] = "Probabilidad de caída: 30 %."
        out["frase_historial"] = "Acertamos con un 80 % de probabilidad."
        out["regimen_macro"] = "Comprar AAPL. Hay un 70 % de probabilidad de subida."
        out["lectura_conjunto"] = "Comprar AAPL."
    b, r, reds, n = ciclo_con_sintetizador(cambiar)
    g3 = r["g3_entregables"]
    texto = json.dumps(r["paquete"], ensure_ascii=False) + entregables_texto(r)
    fugas = [x for x in ("AAPL", "NVDA", "TSLA", "70 %", "30 %.", "80 %") if x in texto]
    informe("segunda_pasada_muchas_quitadas", "OK" if g3["dictamen"] != "BLOQUEADO" and not fugas else "FALLO",
            f"dictamen={g3['dictamen']}; legibilidad={g3.get('legibilidad')}; fugas={fugas}; estado={r['estado']}; "
            f"limitaciones={[x[:90] for x in r['paquete']['limitaciones'] if 'quitadas' in x]}")


# ============================================================================================== rendimiento
def at_rendimiento_textos_largos():
    """Expresiones regulares lentas: textos largos sin puntuación con muchos nombres en mayúscula, «acciones de»,
    verbos y porcentajes. Umbral: 2 s por texto de unos 50.000 caracteres (más que la salida máxima del modelo)."""
    casos = {
        "mayusculas": "Ab " * 17000,
        "mayusculas_sufijo_al_final": "Ab " * 17000 + "Inc",
        "acciones_de": "acciones de la empresa " * 2200,
        "verbos_y_codigos": "comprar AAPL vender TSLA " * 2000,
        "porcentajes_y_probabilidad": "probabilidad de 70 % de " * 2100,
        "bonos": "bonos con plazo largo " * 2300,
        "codigos": "ABCDEFGHIJKLMNOP " * 3000,
        "puntos": "A. " * 17000,
        "real_repetido": ("Las opciones de renta fija ganan un 3 % en el mes; el dólar sube frente al EUR y el IBEX 35 cae. " * 500),
    }
    tiempos = {}
    for k, t in casos.items():
        t0 = time.perf_counter()
        v6.limpiar(t, perm())
        tiempos[k] = round(time.perf_counter() - t0, 3)
    lentos = {k: s for k, s in tiempos.items() if s > 2}
    informe("rendimiento_textos_largos", "FALLO" if lentos else "OK", f"segundos={tiempos}")


ATAQUES = [at_bancos_anteriores, at_regresion_frente_a_t101, at_division_abreviatura_legitima, at_division_abreviatura_esconde_compra, at_division_deja_fragmentos,
           at_division_sufijo_sa, at_division_cifras, at_division_interrogacion_exclamacion,
           at_division_saltos_de_linea_y_puntos_suspensivos, at_vacios_y_no_texto, at_vacio_toma_su_defecto,
           at_glosario_quitado_se_declara, at_cuenta_de_lo_quitado, at_segunda_pasada_y_reescritura,
           at_segunda_pasada_con_muchas_quitadas, at_rendimiento_textos_largos]

if __name__ == "__main__":
    for f in ATAQUES:
        if FILTRO and FILTRO not in f.__name__:
            continue
        try:
            f()
        except Exception as e:   # noqa: BLE001
            informe(f.__name__, "ERROR", f"{type(e).__name__}: {e} · {traceback.format_exc()[-600:]}")
    cuenta = {k: sum(1 for x in RES if x[1] == k) for k in ("OK", "FALLO", "OBS", "ERROR")}
    print(f"\nResumen: {cuenta}")
    sys.exit(1 if cuenta["FALLO"] or cuenta["ERROR"] else 0)
