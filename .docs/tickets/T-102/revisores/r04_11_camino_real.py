"""QA r04 de T-102 (revisor nuevo, ronda relanzada sobre `b36176a`) · El camino real del ciclo V6 con el cliente simulado.

- `fugas`: las prohibidas de `r04_10_banco_control.py` que pasan la unidad, una a una, en TODOS los textos del Sintetizador
  (integración y redacción) de un ciclo C1 real (DIV). ¿Llega la frase al paquete JSON, al HTML o al informe técnico? ¿Se
  declara? ¿Qué dictamen da la segunda pasada de HT-09? Para los caracteres invisibles se compara también sin ellos (en
  pantalla no se ven).
- `listas`: R13 en lista o partido en líneas (palabra de probabilidad y número en letra en frases distintas).
- `legitimas`: las legítimas de `r04_10` que la regla quita («medio plazo», «Oriente Medio», «las acciones de Europa»…). ¿Qué
  queda en el informe (el texto por defecto) y se declara?
- `cli`: el ejecutor entero por la línea de órdenes (`bloque-a --cliente mock … ciclo`) con `diseno: v6` y los doce tipos, con
  el Sintetizador simulado sin tocar: termina, deja los tres entregables y no quita frases del simulado.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_11_camino_real.py <raiz_repo> [-k <parte>]
Sale con 1 si alguna prohibida llega a un entregable sin declararse. No escribe en el repositorio (usa una carpeta temporal).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402
import r04_10_banco_control as B  # noqa: E402

FALLOS: list[str] = []


def _visible(s: str) -> str:
    return "".join(ch for ch in s if unicodedata.category(ch) not in ("Cf", "Mn"))


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
            t["por_que_llano"] = ("Lo mueve el dólar. " + f)[:160]
            t["que_puede_salir_mal_llano"] = ("El dólar puede girar. " + f)[:200]
            t["ambito_llano"] = ("Monedas. " + f)[:160]
        out["glosario"] = [{"termino": "Carry", "definicion": "Cobrar el diferencial de tipos. " + f}]
        out["frase_historial"] = "El historial es corto. " + f
    return iny


def t_fugas(v6, perm, marcas) -> None:
    casos = [(g, f) for g, f in B.BANCO if g in B.PROHIBIDAS and v6.frase_prohibida(f, perm, marcas) is None]
    llegan = 0
    for g, f in casos:
        r = C.ciclo(_inyectar(f))
        if "error" in r:
            print(f"  [ERROR] {g} «{f!r}»: {r['error']}")
            FALLOS.append(f)
            continue
        firma = v6.rellenar(f, r["marcas"] or {}).rstrip(".").strip()
        en = [n for n in ("json", "html", "md") if firma in " ".join(r[n].split())
              or _visible(firma) in _visible(" ".join(r[n].split()))]
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        if en:
            llegan += 1
            FALLOS.append(f)
        print(f"  [{'LLEGA' if en else 'no llega'}] {g:13} entregables={en} declarado={bool(decl)} G3={r['dictamen']} «{firma!r}»")
    print(f"fugas: llegan {llegan}/{len(casos)} a algún entregable")


LISTAS = {
    "lista_escenarios": "Probabilidades por escenario:\n- base: la mitad\n- alcista: un cuarto\n- bajista: un cuarto",
    "lista_puntos": "Pesos de los escenarios. Base: la mitad. Alcista: un cuarto. Bajista: otro cuarto.",
    "lista_puntoycoma": "Escenarios: base, la mitad; alcista, un cuarto; bajista, otro cuarto.",
    "lineas_cortadas": "Probabilidad de subida del oro:\nsetenta\nde cien",
    "lista_cada": "Opciones de que el BCE recorte:\n- en marzo, una de cada tres\n- en junio, dos de cada tres",
    "frase_suelta": "La probabilidad de subida es alta. Siete de diez.",
}
FIRMAS = {"lista_escenarios": "alcista: un cuarto", "lista_puntos": "Alcista: un cuarto", "lista_puntoycoma": "alcista, un cuarto",
          "lineas_cortadas": "setenta", "lista_cada": "una de cada tres", "frase_suelta": "Siete de diez"}


def t_listas(v6) -> None:
    """R13 en lista o partido en líneas (la forma de H-11 de la r02, ahora con números en letra): la palabra de probabilidad va
    en una frase y el número en otra. Se pone el texto entero en la lectura del conjunto, el régimen y la frase de 30 s."""
    llegan = 0
    for k, t in LISTAS.items():
        def iny(out, msg, t=t):
            out["lectura_conjunto"] = t
            out["regimen_macro"] = t
            out["frases_30s"][0] = t
        r = C.ciclo(iny)
        if "error" in r:
            print(f"  [ERROR] {k}: {r['error']}")
            FALLOS.append(k)
            continue
        en = [n for n in ("json", "html", "md") if FIRMAS[k] in r[n]]
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        if en:
            llegan += 1
            FALLOS.append(k)
        print(f"  [{'LLEGA' if en else 'no llega'}] {k:17} entregables={en} declarado={bool(decl)} G3={r['dictamen']} «{FIRMAS[k]}»")
    print(f"listas: llegan {llegan}/{len(LISTAS)}")


def t_legitimas(v6, perm, marcas) -> None:
    casos = [(g, f) for g, f in B.BANCO if g in B.LEGITIMAS and v6.frase_prohibida(f, perm, marcas)]
    for g, f in casos:
        r = C.ciclo(_inyectar(f))
        if "error" in r:
            print(f"  [ERROR] {g} «{f}»: {r['error']}")
            continue
        firma = f.rstrip(".")
        en = [n for n in ("json", "html", "md") if firma in " ".join(r[n].split())]
        decl = [x for x in r["limitaciones"] if "quitadas" in x]
        hist = (r["red"] or {}).get("frase_historial")
        print(f"  [{g:7}] en entregables={en} declarado={len(decl)} G3={r['dictamen']} historial→«{hist}» «{f}»")


def t_cli(raiz: Path) -> None:
    ejec = raiz / "bloque_a" / "11_Ejecutor"
    py = Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python"
    with tempfile.TemporaryDirectory(prefix="r04_t102_cli_") as tmp:
        cfg = Path(tmp) / "v6.yaml"
        cfg.write_text("diseno: v6\nperfiles:\n  activos: [" + ", ".join(B.TIPOS) + "]\n", encoding="utf-8")
        # con -I no cuenta PYTHONPATH: la ruta se pone a mano y se comprueba que el código es el de la raíz dada
        arranque = (f"import sys; sys.path.insert(0, {str(ejec)!r}); import bloque_a; "
                    f"assert bloque_a.__file__.startswith({str(ejec)!r}), bloque_a.__file__; "
                    "from bloque_a.cli import main; sys.exit(main())")
        orden = [str(py), "-I", "-c", arranque,
                 "--cliente", "mock", "--config", str(cfg), "--datos", "ejemplos/datos_sinteticos",
                 "--universo", "config/universo_ejemplo.csv", "--estado", f"{tmp}/estado", "--salida", f"{tmp}/salida",
                 "--as-of", "2024-03-29", "ciclo"]
        p = subprocess.run(orden, cwd=ejec, capture_output=True, text=True, timeout=1800,
                           env={"PYTHONPATH": str(ejec), "PATH": "/usr/bin:/bin"})
        ent = sorted(str(x.relative_to(tmp)) for x in Path(tmp, "salida").rglob("*") if x.is_file())
        paquetes = [x for x in Path(tmp, "salida").rglob("*paquete*json*") if x.is_file()]
        lim = []
        disenos = set()
        for x in paquetes:
            try:
                d = json.loads(x.read_text(encoding="utf-8"))
                lim += [s for s in d.get("limitaciones", []) if "quitadas" in s]
            except (ValueError, OSError):
                pass
        estado_txt = " ".join(x.read_text(encoding="utf-8", errors="replace") for x in Path(tmp, "estado").rglob("*.jsonl"))
        disenos = {d for d in ("AG-26",) if d in estado_txt}
        ok = p.returncode == 0 and len(paquetes) >= 1 and "AG-26" in disenos
        if not ok:
            FALLOS.append("cli")
        print(f"  cli: exit={p.returncode} entregables={len(ent)} paquetes={len(paquetes)} AG-26 en el estado={bool(disenos)}"
              f" frases quitadas del simulado={lim or 'ninguna'}")
        if p.returncode:
            print("  stderr:", p.stderr[-800:])


def main() -> int:
    raiz = Path(sys.argv[1]).resolve()
    solo = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    M = C.preparar(raiz)
    v6 = M["v6"]
    perm = v6.permitidos_r21(C.bloque())
    marcas = dict(C.ciclo()["marcas"] or {})
    for t in B.TIPOS:
        marcas.setdefault(f"tipo:{t}", t.lower())
        marcas.setdefault(f"n:{t}", "2")
        marcas.setdefault(f"candidatas:{t}", "5")
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
