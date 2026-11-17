"""T-165 QA r03 · riesgo operativo del falso positivo, medido con el CORPUS (no con frases del revisor).

1. Los ejemplos de salida de los prompts de los doce Analistas (`02_System_prompts`, el bloque JSON de la ficha de candidata):
   se leen como lo hace F6 con una candidata que es opción (`informes_clase.X[OPP-…]`, severidad BLOQUEO), después de que el
   ejecutor reescriba `estado_madurez_metodos` (`sintesis.canonizar_madurez`). Si G3-MET-13 bloquea, en un run real la opción se
   retiraría.
2. El ejemplo del paquete de oportunidades (`06_Plantillas_entregables`, «Ejemplo - Paquete de oportunidades - V5.0.json»): como
   lo lee F6 (`paquete`, BLOQUEO): qué opciones se retirarían y si se bloquearía el run.
3. Las líneas de los prompts del Analizador, del Redactor y de los Analistas que piden escribir en prosa algo con la raíz
   «valid-» (se listan para leerlas; no se cuentan como bloqueo).

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r03_01_corpus.py
"""
import copy
import glob
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path.cwd()))
from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.herramientas import ht09  # noqa: E402

B = SimpleNamespace(motor=SimpleNamespace(raiz=None))
PROMPTS = Path.cwd().parent / "02_System_prompts"
PLANT = Path.cwd().parent / "06_Plantillas_entregables"


def _bloques(md):
    out = []
    for b in re.findall(r"```(?:json)?\n(.*?)```", md, re.S):
        try:
            out.append(json.loads(b))
        except ValueError:
            pass
    return out


def analistas():
    print("== 1. Ejemplos de ficha de candidata de los Analistas (como opción en F6)")
    n = nb = 0
    for f in sorted(glob.glob(str(PROMPTS / "System prompt - Analista*.md"))):
        fichas = [o for o in _bloques(Path(f).read_text(encoding="utf-8")) if isinstance(o, dict) and "tesis" in o]
        for o in fichas:
            n += 1
            c = copy.deepcopy(o)
            c["opp_id"] = "OPP-2026-0001"
            sint.canonizar_madurez(B, {"X": {"candidatos": [c]}})
            textos = [(r, t, "BLOQUEO") for r, t in ht09.textos_de(c, "informes_clase.X[OPP-2026-0001]")]
            comp = sint._comprobar_met13(B, textos)
            bloquea = comp["resultado"] == "BLOQUEO"
            nb += bloquea
            nombre = Path(f).name.removeprefix("System prompt - ").split(" - Versión")[0]
            print(f"  {'BLOQUEA' if bloquea else 'ok     '} {nombre}")
            for i in comp["incidencias"][:2]:
                print("      ", i["detalle"][:230])
    print(f"  → {nb} de {n} ejemplos del corpus se retirarían")
    return nb, n


def paquete():
    print("== 2. Ejemplo del paquete de oportunidades V5.0 (como lo lee F6)")
    p = json.loads((PLANT / "Ejemplo - Paquete de oportunidades - V5.0.json").read_text(encoding="utf-8"))
    textos = [(r, t, "BLOQUEO") for r, t in ht09.textos_de(p, "paquete")]
    comp = sint._comprobar_met13(B, textos)
    opp = sorted({m for i in comp["incidencias"] for m in re.findall(r"OPP-\d{4}-\d{4,}", i["ruta"])})
    fuera = [i for i in comp["incidencias"] if not re.search(r"OPP-\d{4}-\d{4,}", i["ruta"])]
    n_op = sum(len(d.get("opciones", [])) for d in p.get("clases", {}).values())
    print(f"  resultado {comp['resultado']} · opciones que se retirarían {len(opp)} de {n_op} · incidencias fuera de una opción "
          f"(bloquean el run) {len(fuera)}")
    for i in comp["incidencias"][:6]:
        print("      ", i["ruta"][:70], "·", i["detalle"][:200])
    return comp


def prosa():
    print("== 3. Líneas de los prompts que piden escribir «valid-» en prosa o en un campo de texto")
    pat = re.compile(r"(?i)(decl[aá]ral|refl[eé]jal|escrib|indica|declara|marca|«pendiente de validaci|validaci[oó]n pendiente"
                     r"|no validad|validad[oa]»)")
    raiz = re.compile(r"(?i)(?<![a-záéíóúñ])(?:re|con|pre)?valid")
    for f in sorted(glob.glob(str(PROMPTS / "System prompt - Anali*.md"))) + [str(PROMPTS / "System prompt - Redactor y Diseñador de Informes - Versión óptima V5.0.md")]:
        for k, ln in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
            if raiz.search(ln) and pat.search(ln) and not ln.lstrip().startswith(("{", '"')):
                nombre = Path(f).name.removeprefix("System prompt - ").split(" - Versión")[0]
                m = raiz.search(ln)
                print(f"  {nombre}:{k}: …{ln[max(0, m.start() - 110):m.end() + 90].strip()}…")


if __name__ == "__main__":
    analistas()
    paquete()
    prosa()
