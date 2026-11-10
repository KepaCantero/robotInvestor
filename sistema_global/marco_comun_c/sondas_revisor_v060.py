"""Sondas del revisor independiente — V0.60 (pieza 1: robustez de los seis validadores).

Ejecutar desde la raíz de marcoC:  python3 sondas_revisor_v060.py

S-1  dimensionar no muta sus cuatro entradas (la batería no lo comprueba: laguna).
S-2  Borrados de elementos de lista que dejan la lista POR DEBAJO de su minItems (rompen la forma del
     esquema JSON): _forma_real los reclasifica como «de valor» y la batería no exige la regla de
     esquema; aquí se comprueba si el validador de verdad falla cerrado con la regla correcta.
S-3  Mutación de valor del campo `estado` del sello (VIGENTE->CADUCADO), respetando la forma: el hash
     lo excluye por diseño; el Documento 0 promete «al menos S-12» para toda mutación de valor.
S-4  Mutación de las claves del contexto que el Orquestador pasa y la batería no muta: sc3 y
     sello_encargo (sobre), autoria_c/autoria_contradictor (informe).
S-5  No-vacuidad del caso fijo del calendario: recuento de casos rotos/frescos de H y cobertura por
     objetivo de la batería (informativo).
"""
import copy
import json
import math
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from validar_sobre import validar, cargar_json
from validar_encargo import validar_encargo
from validar_contradictor import validar_informe
from k_calidad import validar_sello
from dimensionado import dimensionar
from control_f import POLITICA_DEFECTO
from vigilancia import vigilar, _dato_fresco, MAX_EDAD_MIN

MAL = []


def _igual_nan(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b):
            return True
        return a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_igual_nan(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_igual_nan(x, y) for x, y in zip(a, b))
    try:
        return bool(a == b)
    except Exception:
        return a is b


def _chk(nombre, ok, detalle=""):
    print(("OK   " if ok else "FALLA") + f"  {nombre}" + (f"  [{detalle}]" if detalle else ""))
    if not ok:
        MAL.append(nombre)


# ---------------------------------------------------------------- fixtures (los mismos de la batería)
sobres = [(p.name, cargar_json(p.read_text(encoding="utf-8")))
          for p in sorted((AQUI / "pruebas" / "validos").glob("*.json"))]
CTX_SOBRE = json.loads((AQUI / "pruebas" / "contexto.json").read_text(encoding="utf-8"))
encargos = [(p.name, json.loads(p.read_text(encoding="utf-8")))
            for p in sorted((AQUI / "pruebas" / "encargos" / "validos").glob("*.json"))]
sellos = [(p.name, json.loads(p.read_text(encoding="utf-8")))
          for p in sorted((AQUI / "pruebas" / "k").glob("valido_*.sello.json"))]
from pruebas_encargo import CTX as CTX_ENC          # noqa: E402
from pruebas_contradictor import AHORA as AHORA_CTR, informe as informe_ctr, sobre_base  # noqa: E402
from pruebas_k import CAL                           # noqa: E402
from pruebas_dimensionado import AHORA as AHORA_E, CART, SOL  # noqa: E402

# ================================================================ S-1: dimensionar no muta
def s1():
    mutaciones = 0
    rng = random.Random(1)
    from pruebas_robustez import _mutar_en_sitio
    for i in range(300):
        entradas = {"sol": copy.deepcopy(SOL), "cart": copy.deepcopy(CART),
                    "pol": copy.deepcopy(POLITICA_DEFECTO), "ahora": AHORA_E}
        clave = ("sol", "cart", "pol", "ahora")[i % 4]
        entradas[clave], _ = _mutar_en_sitio(entradas[clave], rng)
        foto = copy.deepcopy(entradas)   # foto DESPUÉS de mutar y ANTES de llamar
        try:
            dimensionar(entradas["sol"], entradas["cart"], entradas["pol"], entradas["ahora"])
            dimensionar(entradas["sol"], entradas["cart"], entradas["pol"], entradas["ahora"], paso=0.5)
        except Exception as ex:
            _chk("S-1 dimensionar muta o lanza", False, f"{type(ex).__name__}: {ex}")
            return
        for k in entradas:
            if not _igual_nan(foto[k], entradas[k]):
                _chk("S-1 dimensionar no muta sus entradas", False, f"mutó {k} en el caso {i}")
                return
    _chk("S-1 dimensionar no muta sus entradas (300 casos mutados, idem con paso=0.5)", True)


# ================================================================ S-2: borrados bajo minItems
def s2():
    casos = []

    # sobre: cartera_compatible e incertidumbre con 1 elemento (minItems 1)
    for n, s in sobres:
        if len(s["payload"]["identificacion"]["cartera_compatible"]) == 1:
            x = copy.deepcopy(s)
            del x["payload"]["identificacion"]["cartera_compatible"][0]
            casos.append(("sobre", n, "cartera_compatible", x, CTX_SOBRE, "V-01"))
            break
    s0 = sobres[0][1]
    if len(s0["incertidumbre"]) == 1:
        x = copy.deepcopy(s0)
        del x["incertidumbre"][0]
        casos.append(("sobre", "incertidumbre", "incertidumbre", x, CTX_SOBRE, "V-01"))

    # informe: revisadas, escenarios_fallo y evid_refs del primer escenario
    inf = informe_ctr(sobre_base())
    ctx_inf = {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_base())}
    for ruta, lista, _m in (("revisadas", inf["payload"]["cobertura"]["revisadas"], None),):
        if len(lista) == 1:
            y = informe_ctr(sobre_base())
            del y["payload"]["cobertura"]["revisadas"][0]
            casos.append(("informe", ruta, ruta, y, ctx_inf, "C-01"))
    if len(inf["payload"]["escenarios_fallo"]) == 1:
        y = informe_ctr(sobre_base())
        del y["payload"]["escenarios_fallo"][0]
        casos.append(("informe", "escenarios_fallo", "escenarios_fallo", y, ctx_inf, "C-01"))
        y2 = informe_ctr(sobre_base())
        if len(y2["payload"]["escenarios_fallo"][0]["evid_refs"]) == 1:
            del y2["payload"]["escenarios_fallo"][0]["evid_refs"][0]
            casos.append(("informe", "evid_refs", "evid_refs", y2, ctx_inf, "C-01"))

    # sello: mercados (1, min 1) y resultado_reglas (15, min 15)
    for n, k in sellos:
        if len(k["mercados"]) == 1:
            x = copy.deepcopy(k)
            del x["mercados"][0]
            casos.append(("sello", n, "mercados", x, {"calendario": CAL}, "S-01"))
            break
    k0 = sellos[0][1]
    if len(k0["resultado_reglas"]) == 15:
        x = copy.deepcopy(k0)
        del x["resultado_reglas"][7]
        casos.append(("sello", "resultado_reglas 15->14", "resultado_reglas", x, {"calendario": CAL}, "S-01"))

    mal = []
    for modulo, nombre, campo, msg, ctx, esperada in casos:
        if modulo == "sobre":
            r = validar(msg, copy.deepcopy(ctx))
        elif modulo == "encargo":
            r = validar_encargo(msg, copy.deepcopy(ctx))
        elif modulo == "informe":
            r = validar_informe(msg, copy.deepcopy(ctx))
        else:
            r = validar_sello(msg, copy.deepcopy(ctx))
        reglas = sorted({x.get("regla") for x in r})
        ok = esperada in reglas
        if not ok:
            mal.append(f"{modulo}/{nombre}: esperaba {esperada}, dio {reglas or 'VÁLIDO'}")
    _chk("S-2 borrado bajo minItems sigue fallando cerrado con la regla de esquema",
         not mal, "; ".join(mal) or f"{len(casos)} casos, todos con la regla de esquema")


# ================================================================ S-3: estado del sello
def s3():
    n, k0 = sellos[0]
    x = copy.deepcopy(k0)
    antes = x["estado"]
    x["estado"] = "CADUCADO" if antes == "VIGENTE" else "VIGENTE"
    r = validar_sello(x, {"calendario": CAL})
    reglas = sorted({y.get("regla") for y in r})
    _chk("S-3 sello con `estado` alterado (VIGENTE<->CADUCADO) sigue VÁLIDO sin S-12 (el hash lo excluye)",
         r == [] and "S-12" not in reglas, f"reglas={reglas or '[] (el sello sigue válido)'}")
    y = copy.deepcopy(k0)
    y["estado"] = "CADUCADO"
    from pruebas_encargo import encargo_div
    enc = encargo_div()
    enc["payload"]["sello_corte_ref"] = y["sello_id"]
    CT = copy.deepcopy(CTX_ENC)
    CT["sellos"] = dict(CTX_ENC["sellos"]); CT["sellos"][y["sello_id"]] = y
    r2 = validar_encargo(enc, CT)
    reglas2 = sorted({z.get("regla") for z in r2})
    _chk("S-3b el consumidor (E-16 del encargo) sí rechaza el sello con estado alterado",
         "E-16" in reglas2, f"reglas={reglas2}")


# ================================================================ S-4: claves de contexto que el Orquestador pasa
def s4():
    s0 = sobres[0][1]
    c = copy.deepcopy(CTX_SOBRE)
    c["sc3"] = "x"                       # el Orquestador pasa self._vista_sc3()
    r = validar(copy.deepcopy(s0), c)
    reglas = sorted({y.get("regla") for y in r})
    _chk("S-4a sobre con ctx['sc3'] corrompido -> V-01 (falla cerrado; la batería no muta esta clave)",
         "V-01" in reglas, f"reglas={reglas}")
    c2 = copy.deepcopy(CTX_SOBRE)
    c2["sc3"] = {"historial": [], "estado": "VIGENTE", "entradas": []}   # como el Orquestador
    c2["sello_encargo"] = ["no", "es", "texto"]   # el Orquestador pasa en["sello_ref"] (texto)
    r2 = validar(copy.deepcopy(s0), c2)
    reglas2 = sorted({y.get("regla") for y in r2})
    _chk("S-4b sobre con ctx['sello_encargo'] corrompido (y sc3 presente) -> V-01 (idem)",
         "V-01" in reglas2, f"reglas={reglas2}")
    # informe: autoria_c y autoria_contradictor (el Orquestador las pasa cuando están configuradas)
    inf = informe_ctr(sobre_base())
    a_decl = inf["payload"]["autoria"]
    # autoria_c coherente con la diversidad declarada del informe, para que la base siga válida
    if a_decl["diversidad"] == "OTRO_MODELO":
        ac = {"modelo": "ZZZ-otro-modelo", "proveedor": a_decl["proveedor"]}
    elif a_decl["diversidad"] == "OTRO_PROVEEDOR":
        ac = {"modelo": "ZZZ-otro-modelo", "proveedor": "ZZZ-otro-proveedor"}
    else:
        ac = {"modelo": a_decl["modelo"], "proveedor": a_decl["proveedor"]}
    ci = {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_base()), "autoria_c": ac}
    r0 = validar_informe(copy.deepcopy(inf), copy.deepcopy(ci))
    if r0:
        print(f"     (nota: el informe base no valida con autoria_c configurada: {[x['regla'] for x in r0][:3]})")
    else:
        ci2 = copy.deepcopy(ci)
        ci2["autoria_c"] = {"modelo": 17, "proveedor": None}   # forma rota de autoria_c
        r2 = validar_informe(copy.deepcopy(inf), ci2)
        reglas3 = sorted({z.get("regla") for z in r2})
        _chk("S-4c informe con autoria_c corrupta (forma rota) -> la diversidad deja de comprobarse en silencio",
             r2 == [], f"reglas={reglas3 or '[] (el informe sigue válido: la comprobación C-11 desaparece sin aviso)'}")


# ================================================================ S-5: cobertura real de H (informativo)
def s5():
    from pruebas_vigilancia import T1, abierta, datos as datos_h
    from pruebas_robustez import _mutar_en_sitio
    rng = random.Random(20261110)
    o0, b0 = abierta()
    pid = next(iter(o0.posiciones))
    base = datos_h(1.10)
    rotos = frescos = 0
    acciones_rotas = set()
    for i in range(200):
        o, b = abierta()
        dm, _ = _mutar_en_sitio(copy.deepcopy(base), rng)
        r = vigilar(o, b, dm, T1)
        if not _dato_fresco(dm.get("EURUSD") if isinstance(dm, dict) else None, T1, MAX_EDAD_MIN):
            rotos += 1
            for a in r["acciones"]:
                acciones_rotas.add(a.get("regla"))
        else:
            frescos += 1
    _chk("S-5 cobertura H con la semilla de la batería (rotos/frescos)", rotos + frescos == 200,
         f"rotos={rotos} frescos={frescos} reglas_en_rotos={sorted(acciones_rotas)}")


if __name__ == "__main__":
    s1(); s2(); s3(); s4(); s5()
    print("\nSONDAS REVISOR V0.60:", "TODAS CIERRAN" if not MAL else f"{len(MAL)} FALLAN: {MAL}")
    sys.exit(0 if not MAL else 1)
