"""QA r01 de T-143 · La batería, el corpus, el movimiento de la V5.1 y lo que no se borró, contra el commit base.

Desde la raíz del repositorio, con el Python del .venv y git:

    .venv/bin/python .docs/tickets/T-143/revisores/r01_02_bateria_y_corpus.py [BASE]

BASE es el commit anterior a la tarea (por defecto 1ccffd5). Termina con 1 si algo no cuadra.

- Batería: cada caso que en BASE partía de un ejemplo (`base`) que cambia en la V5.2 lleva ahora dentro, como `cuerpo`, el
  ejemplo de BASE, con su contrato y tipo de mensaje; el resto del caso no cambia (salvo `que` en los tres casos
  «ejemplo_del_anexo_b_suelto»); los casos que siguen con `base` apuntan a un ejemplo que no cambió. Y el orden y el número
  de casos son los mismos, y `aceptaciones_rechazos.json` es idéntico byte a byte.
- Corpus: el diff del manifiesto toca exactamente las seis rutas declaradas; las dos movidas conservan el hash; el hash del
  manifiesto de cada fichero coincide con el disco.
- Documento 0: fuera del Anexo B solo cambian la cabecera (4 líneas) y una fila del Anexo F.
- .docs: ningún fichero borrado.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BASE = sys.argv[1] if len(sys.argv) > 1 else "1ccffd5"
GOLD = "bloque_a/11_Ejecutor/tests/goldens"
V51 = "Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1"
V52 = "bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md"
MAL: list[str] = []


def git(*args: str) -> str:
    return subprocess.run(["git", "-c", "core.quotepath=false", "-C", str(RAIZ), *args], check=True, capture_output=True, text=True).stdout


def en_base(ruta: str) -> str:
    return git("show", f"{BASE}:{ruta}")


def anota(ok: bool, texto: str) -> None:
    print(("OK    " if ok else "MAL   ") + texto)
    if not ok:
        MAL.append(texto)


def bateria() -> None:
    ej_base = json.loads(en_base(f"{GOLD}/anexo_b_ejemplos.json"))
    ej_hoy = json.loads((RAIZ / GOLD / "anexo_b_ejemplos.json").read_text(encoding="utf-8"))
    bat_base = json.loads(en_base(f"{GOLD}/bateria_mensajes.json"))
    bat_hoy = json.loads((RAIZ / GOLD / "bateria_mensajes.json").read_text(encoding="utf-8"))
    casos_b = bat_base["casos"] if isinstance(bat_base, dict) and "casos" in bat_base else bat_base
    casos_h = bat_hoy["casos"] if isinstance(bat_hoy, dict) and "casos" in bat_hoy else bat_hoy
    if isinstance(casos_b, dict):
        claves_b, claves_h = list(casos_b), list(casos_h)
        anota(claves_b == claves_h, f"batería: mismos {len(claves_b)} casos y en el mismo orden")
        pares = [(k, casos_b[k], casos_h[k]) for k in claves_b if k in casos_h]
    else:
        anota(len(casos_b) == len(casos_h), f"batería: mismo número de casos ({len(casos_b)} → {len(casos_h)})")
        pares = [(i, a, b) for i, (a, b) in enumerate(zip(casos_b, casos_h))]
    if isinstance(bat_base, dict):
        otros_b = {k: v for k, v in bat_base.items() if k != "casos"}
        otros_h = {k: v for k, v in bat_hoy.items() if k != "casos"}
        anota(otros_b.keys() == otros_h.keys(), "batería: mismas claves de cabecera")
    movidos = mal = 0
    for k, a, b in pares:
        base = a.get("base")
        if base is not None and ej_base.get(base) != ej_hoy.get(base):
            movidos += 1
            ct, sentido = base.split(".")
            esperado = {kk: vv for kk, vv in a.items() if kk != "base"}
            esperado.update({"cuerpo": ej_base[base], "contrato": ct, "tipo_mensaje": sentido})
            resto_b = {kk: vv for kk, vv in esperado.items() if kk != "que"}
            resto_h = {kk: vv for kk, vv in b.items() if kk != "que"}
            if resto_b != resto_h or (b.get("que") != a.get("que") and "suelto" not in str(k) + str(a.get("que"))):
                mal += 1
                print(f"      caso {k}: esperado {json.dumps(esperado, ensure_ascii=False)[:300]}\n      obtenido {json.dumps(b, ensure_ascii=False)[:300]}")
        else:
            if a != b:
                mal += 1
                print(f"      caso {k} cambió sin que su ejemplo cambiara: {json.dumps(a, ensure_ascii=False)[:200]} → {json.dumps(b, ensure_ascii=False)[:200]}")
            if b.get("base") is not None and ej_base.get(b["base"]) != ej_hoy.get(b["base"]):
                mal += 1
    anota(mal == 0, f"batería: {movidos} casos pasan a llevar el ejemplo V5.1 dentro, sin otro cambio; {len(pares) - movidos} intactos")
    anota(movidos == 86, f"batería: son 86 los casos cuyo ejemplo cambió ({movidos})")
    acept = (RAIZ / GOLD / "aceptaciones_rechazos.json").read_bytes()
    anota(acept == en_base(f"{GOLD}/aceptaciones_rechazos.json").encode("utf-8"), "aceptaciones_rechazos.json idéntico byte a byte a BASE")
    cambiados = sorted(k for k in set(ej_base) | set(ej_hoy) if ej_base.get(k) != ej_hoy.get(k))
    print(f"      ejemplos que cambian ({len(cambiados)}): {', '.join(cambiados)}")


def corpus() -> None:
    viejo = dict(reversed(l.split("  ", 1)) for l in en_base("tools/corpus_manifest.txt").splitlines() if l.strip())
    nuevo = dict(reversed(l.split("  ", 1)) for l in (RAIZ / "tools/corpus_manifest.txt").read_text(encoding="utf-8").splitlines() if l.strip())
    quitadas, puestas = sorted(set(viejo) - set(nuevo)), sorted(set(nuevo) - set(viejo))
    cambiadas = sorted(r for r in set(viejo) & set(nuevo) if viejo[r] != nuevo[r])
    esperado_q = [f"bloque_a/01_Gobernanza/{V51}.docx", f"bloque_a/01_Gobernanza/{V51}.md"]
    esperado_p = [V52, f"bloque_a/99_Historico_V5.1/01_Gobernanza/{V51}.docx", f"bloque_a/99_Historico_V5.1/01_Gobernanza/{V51}.md"]
    anota(quitadas == esperado_q, f"manifiesto: quitadas {quitadas}")
    anota(sorted(puestas) == sorted(esperado_p), f"manifiesto: puestas {puestas}")
    anota(cambiadas == ["bloque_a/README - Índice de la entrega y registro de la actualización V5.1.md"], f"manifiesto: cambiadas {cambiadas}")
    anota(len(viejo) == 695 and len(nuevo) == 696, f"manifiesto: {len(viejo)} → {len(nuevo)} archivos")
    for ext in ("docx", "md"):
        anota(viejo[f"bloque_a/01_Gobernanza/{V51}.{ext}"] == nuevo[f"bloque_a/99_Historico_V5.1/01_Gobernanza/{V51}.{ext}"],
              f"la V5.1 .{ext} conserva su hash al moverse")
    distintos = [r for r, h in nuevo.items() if not (RAIZ / r).exists() or hashlib.sha256((RAIZ / r).read_bytes()).hexdigest() != h]
    anota(not distintos, f"manifiesto: los {len(nuevo)} hashes coinciden con el disco" + (f" (difieren {distintos[:5]})" if distintos else ""))
    tocados = [l for l in git("diff", "--name-status", BASE, "HEAD").splitlines()]
    corpus_tocado = [l for l in tocados if l.split("\t")[-1] in set(viejo) | set(nuevo)]
    print("      ficheros del corpus en el diff de git:\n        " + "\n        ".join(corpus_tocado))


def documento_0() -> None:
    v51 = en_base(f"bloque_a/01_Gobernanza/{V51}.md")
    v52 = (RAIZ / V52).read_text(encoding="utf-8")

    def sin_b(t: str) -> list[str]:
        return (t[:t.index("## ANEXO B.")] + t[t.index("## ANEXO C."):]).splitlines()

    dif = [x for x in difflib.unified_diff(sin_b(v51), sin_b(v52), lineterm="", n=0) if x[:1] in "+-" and not x.startswith(("+++", "---"))]
    quit_ = [x for x in dif if x[0] == "-"]
    pue = [x for x in dif if x[0] == "+"]
    anota(len(quit_) == 4 and len(pue) == 5, f"Documento 0 fuera del Anexo B: {len(quit_)} líneas quitadas y {len(pue)} puestas")
    for x in dif:
        print("      " + x[:160])
    # el Anexo B: ningún título, ancla ni separador nuevo fuera de su sitio
    b51, b52 = (t[t.index("## ANEXO B."):t.index("## ANEXO C.")] for t in (v51, v52))
    anota([l for l in b51.splitlines() if l.startswith("#")] == [l for l in b52.splitlines() if l.startswith("#")],
          "Anexo B: los mismos títulos")
    anota(b52.count("```") % 2 == 0 and b52.rstrip().endswith("---"), "Anexo B: bloques de código cerrados y separador final")
    anota(b51[b51.index("**Esquema `informe_seguimiento_opcion`"):] == b52[b52.index("**Esquema `informe_seguimiento_opcion`"):],
          "Anexo B: los esquemas de seguimiento y del paquete, sin cambios")


def docs_sin_borrar() -> None:
    borrados = git("diff", "--diff-filter=D", "--name-only", BASE, "HEAD", "--", ".docs").split()
    anota(not borrados, f".docs: ficheros borrados {borrados}")


def main() -> int:
    bateria()
    corpus()
    documento_0()
    docs_sin_borrar()
    print(f"\n{len(MAL)} fallos")
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
