"""QA r06 de T-102 · El camino real del ciclo V6 hasta los entregables (CA-12, CA-13 y CA-15).

Partes (-k <parte>):
- `cli`: la orden `bloque-a --cliente mock … ciclo` con `diseno: v6` y los doce tipos, con el Sintetizador simulado tal cual.
  Se comprueba que las frases de cuenta que escribe el código (la primera de «la semana en 30 segundos» y el principio de
  cada motivo llano) salen en el HTML con los números del paquete JSON entregado, y que no queda ningún marcador.
- `banco`: las prohibidas y las legítimas del banco ciego (`r06_01_banco_ciego.py`), repartidas por todos los textos del
  Sintetizador de un ciclo real (RV, RF y DIV, cliente simulado). ¿Llega alguna prohibida al paquete JSON, al HTML o al informe
  técnico? ¿Llegan las legítimas, rellenadas?
- `motivos`: claves raras en `motivos_llanos` (un tipo que no está en el paquete, un tipo con tres opciones, una clave con
  cifras) y un motivo que se queda vacío: ¿qué cuenta escribe el código y dónde sale?
- `esquema`: el Sintetizador devuelve tres frases de 30 s (el formato de la r05) o una: ¿qué se entrega?

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r06_02_camino_real.py <raiz_repo> [-k <parte>]
Sale con 1 si una prohibida o una cifra que no está en el paquete llega a un entregable, o si una cuenta del código no
coincide con el paquete. No escribe en el repositorio (carpetas temporales).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402
import r06_01_banco_ciego as B  # noqa: E402

FALLOS: list[str] = []
TIPOS = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")


def _norm(s: str) -> str:
    return " ".join(s.split())


def _entregables(r: dict) -> dict[str, str]:
    """Textos de los entregables; el JSON, vuelto a escribir sin escapes para buscar con tildes."""
    js = r["json"]
    try:
        js = json.dumps(json.loads(js), ensure_ascii=False)
    except Exception:   # noqa: BLE001
        pass
    return {"json": _norm(js), "html": _norm(r["html"]), "md": _norm(r["md"])}


def comprobar_cuentas(paquete: dict, html: str, nombre_clase: dict, etiqueta: str) -> None:
    """La primera frase de 30 s y el principio de cada motivo, frente a los números del paquete entregado."""
    clases = paquete["clases"]
    n = sum(len(d["opciones"]) for d in clases.values())
    nc = sum(1 for d in clases.values() if d["opciones"])
    esperada = f"Esta semana vemos {n} ideas en {nc} tipos de inversión."
    ok30 = esperada in html
    print(f"  [{etiqueta}] 30 s: {'OK' if ok30 else 'NO'} «{esperada}»")
    if not ok30:
        FALLOS.append(f"{etiqueta}: frase de 30 s")
    for c, d in clases.items():
        if len(d["opciones"]) >= 3:
            continue
        no, cand = len(d["opciones"]), int(d.get("candidatas_analizadas") or 0)
        tipo = nombre_clase.get(c, c).lower()
        esp = f"De {cand} ideas de {tipo} analizadas, {no} {'pasó' if no == 1 else 'pasaron'} todos los filtros."
        # sin motivo del Sintetizador (o quitado entero), la redacción pone su defecto, también con datos del paquete
        defecto = f"Miramos {cand} ideas. " + ("Ninguna pasó todos los filtros." if not no else "Las demás no pasaron todos los filtros.")
        estado = "OK (código)" if esp in html else "OK (defecto de la redacción)" if defecto in html else "NO"
        print(f"  [{etiqueta}] motivo {c}: {estado} «{esp if esp in html else defecto}»")
        if estado == "NO":
            FALLOS.append(f"{etiqueta}: motivo {c}")
    # ninguna cifra de cuenta del código que no esté en el paquete: cada «De N ideas de X analizadas, M …» del HTML
    for m in re.finditer(r"De (\d+) ideas de ([\w ]+?) analizadas, (\d+) (?:pasó|pasaron)", html):
        cand, tipo, no = int(m.group(1)), m.group(2), int(m.group(3))
        c = next((k for k in clases if nombre_clase.get(k, k).lower() == tipo), None)
        if c is None or int(clases[c].get("candidatas_analizadas") or 0) != cand or len(clases[c]["opciones"]) != no:
            print(f"  [{etiqueta}] CUENTA AJENA AL PAQUETE: «{m.group(0)}»")
            FALLOS.append(f"{etiqueta}: cuenta ajena {m.group(0)}")
    for pat in (r"\{[a-z_]+(?::[A-Za-z0-9-]+)?\}", r"\bn_(?:ideas|tipos|apuestas)\b"):
        if re.search(pat, html):
            print(f"  [{etiqueta}] MARCADOR en el HTML: {re.search(pat, html).group(0)}")
            FALLOS.append(f"{etiqueta}: marcador en el HTML")


ENVOLTORIO = r'''
import sys
sys.path.insert(0, {ejec!r})
import bloque_a
assert bloque_a.__file__.startswith({ejec!r}), bloque_a.__file__
from bloque_a.cli import main
sys.exit(main())
'''


def t_cli(raiz: Path) -> None:
    ejec = raiz / "bloque_a" / "11_Ejecutor"
    py = Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python"
    sys.path.insert(0, str(ejec))
    from bloque_a.configuracion import NOMBRE_CLASE   # noqa: E402
    with tempfile.TemporaryDirectory(prefix="r06_t102_cli_") as tmp:
        cfg = Path(tmp) / "v6.yaml"
        cfg.write_text("diseno: v6\nperfiles:\n  activos: [" + ", ".join(TIPOS) + "]\n", encoding="utf-8")
        orden = [str(py), "-I", "-c", ENVOLTORIO.format(ejec=str(ejec)),
                 "--cliente", "mock", "--config", str(cfg), "--datos", "ejemplos/datos_sinteticos",
                 "--universo", "config/universo_ejemplo.csv", "--estado", f"{tmp}/estado", "--salida", f"{tmp}/salida",
                 "--as-of", "2024-03-29", "ciclo"]
        p = subprocess.run(orden, cwd=ejec, capture_output=True, text=True, timeout=1800, env={"PATH": "/usr/bin:/bin"})
        ficheros = [x for x in Path(tmp, "salida").rglob("*") if x.is_file() and "_borradores" not in x.parts]
        print(f"  cli: exit={p.returncode} ficheros={len(ficheros)} {[x.name for x in ficheros]}")
        if p.returncode or len(ficheros) < 3:
            print("  stderr:", p.stderr[-1500:])
            FALLOS.append("cli")
            return
        js = json.loads(next(x for x in ficheros if x.suffix == ".json").read_text(encoding="utf-8"))
        html = _norm(C._html_a_texto(next(x for x in ficheros if x.suffix == ".html").read_text(encoding="utf-8")))
        print("  clases:", {c: (len(d["opciones"]), d.get("candidatas_analizadas")) for c, d in js["clases"].items()})
        comprobar_cuentas(js, html, NOMBRE_CLASE, "cli")
        i = html.find("La semana en 30 segundos")
        print("  30 s en el HTML:", html[i:i + 330])
        lim = [x for x in js.get("limitaciones", []) if "quitadas" in x]
        print("  declaraciones:", lim or "ninguna (el simulado escribe como pide el prompt)")
        if lim:
            FALLOS.append("cli: el simulado tal cual pierde frases")


def _sustituir_banco(marcas):
    ids = [k.split(":", 1)[1] for k in marcas if k.startswith("opp:")]
    tipos = [k.split(":", 1)[1] for k in marcas if k.startswith("tipo:")]
    return lambda s: B._sust(s, ids, tipos)


CAMPOS = ("regimen_macro", "factor", "pregunta", "lectura_conjunto", "limitacion", "frase30_a", "frase30_b", "por_que",
          "que_mal", "ambito", "glosario", "historial", "motivo")


def _inyectar(frases: dict):
    """frases: campo -> frase (una por campo); en las tarjetas, la misma en todas."""
    def iny(out, msg):
        g = frases.get
        if g("regimen_macro"):
            out["regimen_macro"] = "El dólar manda. " + g("regimen_macro")
        if g("factor"):
            for x in out.get("factores_dominantes") or []:
                x["factor"] = "El dólar manda. " + g("factor")
        if g("pregunta"):
            out["preguntas_sugeridas"] = [g("pregunta")]
        if g("lectura_conjunto"):
            out["lectura_conjunto"] = "El dólar manda. " + g("lectura_conjunto")
        if g("limitacion"):
            out["limitaciones"] = [g("limitacion")]
        if g("frase30_a"):
            out["frases_30s"][0] = "El dólar manda. " + g("frase30_a")
        if g("frase30_b"):
            out["frases_30s"][1] = g("frase30_b")
        for t in out["tarjetas"]:
            if g("por_que"):
                t["por_que_llano"] = "Lo mueve el dólar. " + g("por_que")
            if g("que_mal"):
                t["que_puede_salir_mal_llano"] = "El dólar puede girar. " + g("que_mal")
            if g("ambito"):
                t["ambito_llano"] = "Monedas. " + g("ambito")
        if g("glosario"):
            out["glosario"] = [{"termino": "Carry", "definicion": g("glosario")}]
        if g("historial"):
            out["frase_historial"] = "El historial es corto. " + g("historial")
        if g("motivo"):
            out["motivos_llanos"] = {k: g("motivo") for k in out.get("motivos_llanos") or {}}
    return iny


def _firma(v6, f: str, marcas: dict) -> str:
    return _norm(v6.rellenar(f, marcas)).rstrip(".")


def t_banco(raiz: Path) -> None:
    activos = ("RV", "RF", "DIV")
    base = C.ciclo(activos=activos)
    assert not base.get("error"), base.get("error")
    v6, marcas = C.M["v6"], base["marcas"]
    sust = _sustituir_banco(marcas)
    proh = [sust(s) for s in B.PROHIBIDAS_DATO + B.PROHIBIDAS_LETRA]
    leg = [sust(s) for s in B.LEGITIMAS]
    llegan, legit_no, runs = [], [], 0
    for grupo, lista in (("prohibida", proh), ("legitima", leg)):
        for k in range(0, len(lista), len(CAMPOS)):
            trozo = lista[k:k + len(CAMPOS)]
            asign = dict(zip(CAMPOS, trozo))
            r = C.ciclo(_inyectar(asign), activos=activos)
            runs += 1
            if r.get("error"):
                print("  ERROR del ciclo:", r["error"])
                FALLOS.append("banco: error")
                continue
            ent = _entregables(r)
            for campo, f in asign.items():
                firma = _firma(v6, f, marcas)
                donde = [n for n, s in ent.items() if firma in s]
                if grupo == "prohibida" and donde:
                    llegan.append((campo, f, donde))
                # las legítimas: en un entregable o, si el informe no muestra ese texto (el historial sin casos cerrados no se
                # muestra), en la redacción que recibe `redaccion.generar`, ya rellenada
                if grupo == "legitima" and not donde and firma not in _norm(r["red_txt"]):
                    legit_no.append((campo, f))
            decl = [x for x in r["limitaciones"] if "quitadas" in x]
            if grupo == "prohibida" and not decl:
                FALLOS.append("banco: sin declarar")
                print("  SIN DECLARAR en el ciclo", runs)
    print(f"  ciclos: {runs}; prohibidas que llegan a un entregable: {len(llegan)}/{len(proh)}")
    for c, f, d in llegan:
        print(f"    LLEGA [{c}] {d}: {f}")
    print(f"  legítimas que no aparecen en ningún entregable: {len(legit_no)}/{len(leg)}")
    for c, f in legit_no:
        print(f"    no aparece [{c}]: {f}")
    if llegan:
        FALLOS.append("banco: prohibidas que llegan")


def t_motivos(raiz: Path) -> None:
    v6 = C.M["v6"]
    from bloque_a.configuracion import NOMBRE_CLASE   # noqa: E402

    def iny(out, msg):
        clases = msg["paquete_sintesis"]["clases"]
        tres = next((k for k, c in clases.items() if c["n"] >= 3), None)
        pocas = [k for k, c in clases.items() if c["n"] < 3]
        out["motivos_llanos"] = {"CRI": "No hubo ideas con señal clara.", "RV 2027": "Clave con cifras.",
                                 "Zeta": "Un tipo inventado.", **({tres: "Este tipo tiene tres opciones."} if tres else {}),
                                 **{k: "Hay {n_ideas} ideas pero {n:" + k + "} pasan." for k in pocas[:1]},
                                 **{k: "Preferimos no rellenar el hueco." for k in pocas[1:]}}
    r = C.ciclo(iny, activos=("RV", "RF", "DIV"))
    if r.get("error"):
        print("  ERROR:", r["error"]); FALLOS.append("motivos: error"); return
    ent = _entregables(r)
    paquete = r["res"]["paquete"]
    print("  clases:", {c: (len(d["opciones"]), d.get("candidatas_analizadas")) for c, d in paquete["clases"].items()})
    print("  motivos que recibe la redacción:", r["red"]["motivos_llanos"])
    for clave in ("criptoactivos", "rv 2027", "zeta", "Clave con cifras", "Un tipo inventado", "Este tipo tiene tres opciones",
                  "No hubo ideas con señal clara"):
        donde = [n for n, s in ent.items() if clave in s]
        print(f"  «{clave}» en los entregables: {donde}")
        if donde:
            FALLOS.append(f"motivos: {clave}")
    comprobar_cuentas(paquete, ent["html"], NOMBRE_CLASE, "motivos")
    print("  declaraciones:", [x for x in r["limitaciones"] if "quitadas" in x])
    _ = v6


def t_esquema(raiz: Path) -> None:
    from bloque_a.configuracion import NOMBRE_CLASE   # noqa: E402
    for nombre, frases in (("tres frases (formato r05)", ["Esta semana vemos {n_ideas} ideas.", "Varias dependen de lo mismo.",
                                                          "Cada idea puede salir mal."]),
                           ("una frase", ["Varias dependen de lo mismo."]),
                           ("dos frases vacías", ["", ""])):
        def iny(out, msg, frases=frases):
            out["frases_30s"] = list(frases)
            out["frase_historial"] = "Marca de esta prueba: historial propio."
        r = C.ciclo(iny, activos=("RV", "RF", "DIV"))
        if r.get("error"):
            print(f"  [{nombre}] ERROR del ciclo: {r['error']}")
            FALLOS.append(f"esquema: {nombre}")
            continue
        ent = _entregables(r)
        propio = "Marca de esta prueba" in ent["html"]
        i = ent["html"].find("La semana en 30 segundos")
        print(f"  [{nombre}] se usa la respuesta del Sintetizador: {propio}; dictamen {r['dictamen']}; 30 s: "
              f"{ent['html'][i + 25:i + 260]}")
        comprobar_cuentas(r["res"]["paquete"], ent["html"], NOMBRE_CLASE, nombre)


def main() -> int:
    raiz = Path(sys.argv[1]).resolve()
    solo = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    C.preparar(raiz)
    for parte, f in (("cli", t_cli), ("banco", t_banco), ("motivos", t_motivos), ("esquema", t_esquema)):
        if solo in (None, parte):
            print(f"== {parte}")
            f(raiz)
    print("FALLOS:", FALLOS or "ninguno")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
