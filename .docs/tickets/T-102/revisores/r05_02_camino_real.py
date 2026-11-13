"""QA r05 de T-102 (revisor nuevo, commit `bf7235b`) · El camino real del ciclo V6, hasta los entregables.

- `fugas`: cada prohibida de `r05_01_banco.py` que pasa la unidad, puesta en TODOS los textos del Sintetizador de un ciclo C1
  real (DIV, cliente simulado). ¿Llega rellenada al paquete JSON, al HTML o al informe técnico? ¿Se declara? ¿Qué dice G3?
- `listas`: probabilidades por escenario escritas con marcadores en líneas separadas (la forma de H-11 y H-31, ahora con
  marcadores): ¿llega «base: 3 de 12» a los entregables?
- `legitimas`: las legítimas de `r05_01` que la regla quita («a corto y medio plazo», «la acción de los bancos centrales»):
  qué queda en el informe y si se declara.
- `cli`: la orden `bloque-a --cliente mock … ciclo` con `diseno: v6` y los doce tipos, con el Sintetizador simulado
  modificado por un envoltorio (una lista de probabilidades con marcadores, un decimal compuesto, «Pfizer Inc.» al empezar
  y una legítima con «a corto y medio plazo»). Se buscan en los ficheros que deja en la carpeta de salida.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r05_02_camino_real.py <raiz_repo> [-k <parte>]
Sale con 1 si alguna prohibida llega a un entregable. No escribe en el repositorio (usa una carpeta temporal).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402
import r05_01_banco as B  # noqa: E402

FALLOS: list[str] = []


def _inyectar(f: str):
    def iny(out, msg):
        out["regimen_macro"] = "El dólar manda. " + f
        for x in out.get("factores_dominantes") or []:
            x["factor"] = "El dólar manda. " + f
        out["preguntas_sugeridas"] = ["¿Sigue el dólar? " + f]
        out["lectura_conjunto"] = "El dólar manda. " + f
        out["limitaciones"] = ["El historial es corto. " + f]
        out["frases_30s"][0] = "El dólar manda. " + f
        for t in out["tarjetas"]:
            t["por_que_llano"] = "Lo mueve el dólar. " + f
            t["que_puede_salir_mal_llano"] = "El dólar puede girar. " + f
            t["ambito_llano"] = "Monedas. " + f
        out["glosario"] = [{"termino": "Carry", "definicion": "Cobrar el diferencial de tipos. " + f}]
        out["frase_historial"] = "El historial es corto. " + f
    return iny


def _firma(v6, f: str, marcas: dict) -> str:
    """El trozo más reconocible de la frase ya rellenada: su última línea, sin el punto final ni la viñeta."""
    lineas = [x.strip(" -.") for x in v6.rellenar(f, marcas).split("\n") if x.strip(" -.")]
    return lineas[-1]


def _donde(r: dict, firma: str) -> list[str]:
    return [n for n in ("json", "html", "md") if firma in " ".join(r[n].split())]


def t_fugas(v6, perm, marcas) -> None:
    casos = [(g, f) for g, f in B.BANCO if g in B.PROHIBIDAS and v6.texto_prohibido(f, perm, marcas) is None]
    llegan = 0
    for g, f in casos:
        r = C.ciclo(_inyectar(f))
        if "error" in r:
            print(f"  [ERROR] {g} {f!r}: {r['error']}")
            FALLOS.append(f)
            continue
        firma = _firma(v6, f, r["marcas"] or {})
        en = _donde(r, firma)
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        if en:
            llegan += 1
            FALLOS.append(f)
        print(f"  [{'LLEGA' if en else 'no llega'}] {g:13} {en} declarado={bool(decl)} G3={r['dictamen']} «{firma}»")
    print(f"fugas: llegan {llegan}/{len(casos)}")


LISTAS = {
    "escenarios_n_de": ("Probabilidades por escenario:\n- base: {n:DIV} de {candidatas:DIV}\n- bajista: {n_tipos} de {n_ideas}",
                        "bajista: {n_tipos} de {n_ideas}"),
    "confianza_lineas": ("Grado de confianza de la tesis.\n{n_tipos} de {n_ideas}.", "{n_tipos} de {n_ideas}"),
    "decimal": ("El crecimiento esperado del PIB es de un {n_tipos},{n_ideas} este año.", "un {n_tipos},{n_ideas} este año"),
    "cuota_a_uno": ("Las apuestas están {n_ideas} a uno a favor del dólar.", "{n_ideas} a uno a favor del dólar"),
}


def t_listas(v6) -> None:
    llegan = 0
    for k, (t, firma) in LISTAS.items():
        def iny(out, msg, t=t):
            out["lectura_conjunto"] = t
            out["regimen_macro"] = t
            out["frases_30s"][0] = t
        r = C.ciclo(iny)
        if "error" in r:
            print(f"  [ERROR] {k}: {r['error']}")
            FALLOS.append(k)
            continue
        fr = v6.rellenar(firma, r["marcas"] or {})
        en = _donde(r, fr)
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        if en:
            llegan += 1
            FALLOS.append(k)
        print(f"  [{'LLEGA' if en else 'no llega'}] {k:17} {en} declarado={bool(decl)} G3={r['dictamen']} «{fr}»")
    print(f"listas: llegan {llegan}/{len(LISTAS)}")


def t_legitimas(v6, perm, marcas) -> None:
    casos = [(g, f) for g, f in B.BANCO if g in B.LEGITIMAS and v6.texto_prohibido(f, perm, marcas)]
    for g, f in casos:
        r = C.ciclo(_inyectar(f))
        if "error" in r:
            print(f"  [ERROR] {g} {f!r}: {r['error']}")
            continue
        en = _donde(r, f.rstrip("."))
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        hist = (r["red"] or {}).get("frase_historial")
        print(f"  [{g:8}] en entregables={en} declaraciones={len(decl)} G3={r['dictamen']} historial→«{hist}» «{f}»")


ENVOLTORIO = r'''
import sys
sys.path.insert(0, {ejec!r})
import bloque_a
assert bloque_a.__file__.startswith({ejec!r}), bloque_a.__file__
from bloque_a import mock_respuestas as mr
orig = mr._sintetizador
def sint(msg, ctx, rng):
    out = orig(msg, ctx, rng)
    out["lectura_conjunto"] = "Probabilidades por escenario:\n- base: {{n_tipos}} de {{n_ideas}}\n- bajista: {{n_apuestas}} de {{n_ideas}}"
    out["regimen_macro"] = "Vemos valor a corto y medio plazo en la renta fija. El PIB crece un {{n_tipos}},{{n_ideas}} este año."
    out["frases_30s"][0] = "Pfizer Inc. sube con fuerza. Es un fifty-fifty entre subida y bajada."
    return out
mr._sintetizador = sint
from bloque_a.cli import main
sys.exit(main())
'''


def t_cli(raiz: Path) -> None:
    ejec = raiz / "bloque_a" / "11_Ejecutor"
    py = Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python"
    with tempfile.TemporaryDirectory(prefix="r05_t102_cli_") as tmp:
        cfg = Path(tmp) / "v6.yaml"
        cfg.write_text("diseno: v6\nperfiles:\n  activos: [" + ", ".join(B.TIPOS) + "]\n", encoding="utf-8")
        orden = [str(py), "-I", "-c", ENVOLTORIO.format(ejec=str(ejec)),
                 "--cliente", "mock", "--config", str(cfg), "--datos", "ejemplos/datos_sinteticos",
                 "--universo", "config/universo_ejemplo.csv", "--estado", f"{tmp}/estado", "--salida", f"{tmp}/salida",
                 "--as-of", "2024-03-29", "ciclo"]
        p = subprocess.run(orden, cwd=ejec, capture_output=True, text=True, timeout=1800,
                           env={"PATH": "/usr/bin:/bin"})
        ficheros = [x for x in Path(tmp, "salida").rglob("*") if x.is_file()]
        texto = {str(x.relative_to(tmp)): C._html_a_texto(x.read_text(encoding="utf-8", errors="replace"))
                 if x.suffix == ".html" else x.read_text(encoding="utf-8", errors="replace") for x in ficheros}
        print(f"  cli: exit={p.returncode} ficheros={len(ficheros)}")
        if p.returncode:
            print("  stderr:", p.stderr[-1500:])
            FALLOS.append("cli")
            return
        import re
        for nombre, patron in (("lista con marcadores (base: N de M)", r"base:\s*\d+\s+de\s+\d+"),
                               ("decimal compuesto (un N,M este año)", r"un\s+\d+,\d+\s+este año"),
                               ("Pfizer Inc.", r"Pfizer Inc"), ("fifty-fifty", r"fifty-fifty"),
                               ("legítima «a corto y medio plazo»", r"corto y medio plazo")):
            en = sorted({k.split("/")[-1] for k, s in texto.items() if re.search(patron, " ".join(s.split()))})
            prohibida = not nombre.startswith("legítima")
            if prohibida and en:
                FALLOS.append(nombre)
            print(f"  [{'LLEGA' if en else 'no llega'}] {nombre}: {en}")
        decl = sorted({m for s in texto.values() for m in re.findall(r"Frases (?:llanas )?del Sintetizador quitadas[^\"\n]{0,90}", s)})
        print(f"  declaraciones en los entregables: {decl or 'ninguna'}")


def main() -> int:
    raiz = Path(sys.argv[1]).resolve()
    solo = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    res, v6, perm, marcas = B.evaluar(raiz)
    if solo in (None, "fugas"):
        print("== fugas"); t_fugas(v6, perm, marcas)
    if solo in (None, "listas"):
        print("== listas"); t_listas(v6)
    if solo in (None, "legitimas"):
        print("== legitimas"); t_legitimas(v6, perm, marcas)
    if solo in (None, "cli"):
        print("== cli"); t_cli(raiz)
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
