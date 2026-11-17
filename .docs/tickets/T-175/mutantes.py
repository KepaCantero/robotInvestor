"""Mutantes propios de T-175: cada uno cambia una línea del código nuevo y las pruebas de `tests/test_t175_alternativas.py` (y la
de PB-38 de `tests/test_autocritica.py`) tienen que fallar. Restaura el fichero siempre. Uso, desde la raíz del repo:

    .venv/bin/python .docs/tickets/T-175/mutantes.py
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
PRUEBAS = ["tests/test_t175_alternativas.py"]
R, S = "bloque_a/redaccion.py", "bloque_a/sintesis.py"
MUTANTES = [
    ("sin la subsección 4.N.4", R, "            if alternativas.get(c):\n", "            if False:\n"),
    ("sin las filas de la sección 6", R, "            for a in alternativas.get(c, []):\n", "            for a in []:\n"),
    ("filtro de elegibilidad invertido", S, 'ev.get("elegible") is not False', 'ev.get("elegible") is not True'),
    ("lista también las vigentes", S, 'or f.get("_arrastre") or f.get("_vigente")):', 'or f.get("_arrastre")):'),
    ("lista también las de arrastre", S, 'or f.get("_arrastre") or f.get("_vigente")):', 'or f.get("_vigente")):'),
    ("estado siempre RESPONDIDA en la alternativa", S, '"estado": "RESPONDIDA" if _objecion_respondida(o) else "SIN_RESOLVER"}\n',
     '"estado": "RESPONDIDA"}\n'),
    ("regla del estado sin exigir la resolución de la fuerte", S, '(o.get("fuerza") != "fuerte" or bool(o.get("resuelta")))', "True"),
    ("sin «qué la resolvería»", S, 'for o in abiertas:\n                q = o.get("que_la_resolveria")', 'for o in []:\n                q = o.get("que_la_resolveria")'),
    ("sin los OBJ- en el motivo", S, 'if m["codigo"] == "OBJECION_FUERTE" and ids else ""', 'if False else ""'),
    ("orden ascendente", S, 'key=lambda x: (-(x["rk"] if x["rk"] is not None else -1), x["opp_id"])',
     'key=lambda x: ((x["rk"] if x["rk"] is not None else -1), x["opp_id"])'),
    ("sin escapar la barra", R, '.replace("|", "\\\\|")', ""),
    ("sin las moderadas", S, 'o.get("fuerza") in ("fuerte", "moderada")]\n            abiertas', 'o.get("fuerza") in ("fuerte",)]\n            abiertas'),
    # r02 (QA r01, H-01 y H-02)
    ("sin la sustitución del texto que G3-MET-13 rechaza", S, "return bloque is not None and _texto_rechazado(bloque, t)", "return False"),
    ("la sustitución solo mira las reglas A a C, no la raíz", S, "return ht09.tiene_raiz_valid(texto) or bool(", "return bool("),
    ("la sustitución solo mira la raíz, no las reglas A a C", S,
     ' or bool(_comprobar_met13(bloque, [("informe_tecnico", texto, "BLOQUEO")])["incidencias"])', ""),
    ("generar no pasa el bloque", R, "sint.alternativas_descartadas(paquete, extras, bloque)", "sint.alternativas_descartadas(paquete, extras)"),
    ("sin la ADVERTENCIA en HA", R, '        sint.advertir_alternativas_retiradas(res, extras["alternativas_descartadas"])\n', ""),
    ("la ADVERTENCIA al final (fuera de los cinco detalles de HA)", S, 'destino["incidencias"][:0] = [', 'destino["incidencias"][len(destino["incidencias"]):] = ['),
    ("motivos sin comprobar que son lista", S, "(mot if isinstance(mot, list) else [])", "(mot or [])"),
    ("objeciones sin comprobar que son lista", S, "(crudas if isinstance(crudas, list) else [])", "(crudas or [])"),
    ("RK booleano admitido", S, "and not isinstance(rk, bool) and math.isfinite(rk)", "and math.isfinite(rk)"),
    ("RK no finito admitido", S, "and not isinstance(rk, bool) and math.isfinite(rk)", "and not isinstance(rk, bool)"),
    # ronda de cierre de la QA r02 (H-04)
    ("el G3V sin ordenar los BLOQUEOS delante", R, 'sorted(comprobacion["incidencias"], key=lambda i: i.get("severidad") != "BLOQUEO")',
     'comprobacion["incidencias"]'),
    ("las alternativas sin dejar los BLOQUEOS delante", S, '    bloqueos_delante(destino)\n    if destino["resultado"]', '    if destino["resultado"]'),
    ("el técnico sin dejar sus BLOQUEOS delante", S, "        bloqueos_delante(destino)   # T-175", "        pass   # T-175"),
]


def main() -> int:
    vivos = []
    for nombre, rel, viejo, nuevo in MUTANTES:
        p = EJ / rel
        original = p.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"ERROR  {nombre}: el texto a mutar aparece {original.count(viejo)} veces")
            return 2
        try:
            p.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=EJ,
                               capture_output=True, text=True, check=False)
        finally:
            p.write_text(original, encoding="utf-8")
        muerto = r.returncode != 0
        print(f"{'MUERTO' if muerto else 'VIVO  '} {nombre}")
        if not muerto:
            vivos.append(nombre)
    print(f"{len(MUTANTES) - len(vivos)}/{len(MUTANTES)} muertos")
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
