"""QA r03 de T-101 · Mutantes de las correcciones de la ronda r03 (H-12 a H-22) contra la batería `tests/test_t101_v6.py`.

Mismo método que `r01_mutantes.py` (que se reutiliza): copia `bloque_a/` de la raíz indicada a una carpeta temporal por
mutante, aplica UNA mutación textual y ejecuta la batería de T-101. Un mutante «sobrevive» si la batería sigue en verde.

Uso: .venv/bin/python -I .docs/tickets/T-101/revisores/r03_mutantes.py <raiz_repo> [n_paralelo] [ids separados por comas]
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_mutantes as base  # noqa: E402  (lee RAIZ, PAR y SOLO de sys.argv igual que aquí)

D6, ORQ, SIN = "bloque_a/diseno_v6.py", "bloque_a/orquestacion.py", "bloque_a/sintesis.py"

MUTANTES = [
    # H-12: filtro R13/R21
    ("P01", D6, "        if cod.isupper() and cod not in permitidos:", "        if cod.isupper():",
     "el filtro ignora los códigos permitidos tras el verbo"),
    ("P02", D6, "    if re.search(rf\"\\b{_VERBO}\\b\", t, re.IGNORECASE) and any(c not in permitidos for c in _CODIGO_PARENTESIS.findall(t)):",
     "    if False:", "sin la regla del código entre paréntesis"),
    ("P03", D6, "    return frozenset(op(bloque, \"filtro_r21_codigos\")) | simbolos", "    return frozenset(op(bloque, \"filtro_r21_codigos\"))",
     "los símbolos del universo dejan de estar permitidos"),
    ("P04", D6, "        regla = texto_prohibido(t, permitidos)", "        regla = texto_prohibido(t)",
     "la integración no pasa los códigos permitidos"),
    ("P05", D6, "    malas = sorted({r for r in (texto_prohibido(t, permitidos) for t in _textos(red)) if r is not None})",
     "    malas = sorted({r for r in (texto_prohibido(t) for t in _textos(red)) if r is not None})",
     "los textos llanos no pasan los códigos permitidos"),
    ("P06", D6, "_R21 = (re.compile(r\"\\b[A-Z]{2}[A-Z0-9]{9}\\d\\b\"),", "_R21 = (re.compile(r\"(?!x)x\"),", "sin la regla del ISIN"),
    ("P07", D6, "|la\\s+compra\\s+de|la\\s+venta\\s+de)\"", ")\"", "sin «la compra de» y «la venta de»"),
    # H-13, H-14 y H-15: cobertura
    ("P08", ORQ, "                out[\"rotacion\"] = list(rot)", "                out[\"rotacion\"] = []", "la rotación N1 no se guarda"),
    ("P09", D6, "            if sim in expl_f3:", "            if False:", "la exploratoria dada de alta en F3 sale como ROTACION"),
    ("P10", D6, "            if sim not in finalistas and sim not in en_top and sim not in vigentes_sim:",
     "            if sim not in finalistas:", "vuelve la fila ANALISTA de la vigente mantenida (H-14)"),
    ("P11", D6, "\n                     and x[\"simbolo\"] not in en_top]", "]", "la muestra de descartes puede tomar del top-3"),
    ("P12", D6, "                    for x in s[\"candidatos\"] if x.get(\"opp_id\") in top]",
     "                    for x in s[\"candidatos\"] if x.get(\"opp_id\") in top and not x.get(\"_arrastre\")]",
     "las vigentes arrastradas salen de las elegidas (H-15)"),
    # H-16: embudo y F5
    ("P13", SIN, "\"pasan_gc1\": len(an[\"gc1\"][\"pasan\"]) if an.get(\"gc1\") else", "\"pasan_gc1\":",
     "el embudo vuelve a contar el juicio del Analista"),
    ("P14", ORQ, "            dec_gc1 = v6.gc1_decisiones(an) if self.v6 else None", "            dec_gc1 = None",
     "F5 vuelve a registrar el juicio del Analista como GC1"),
    # H-17
    ("P15", ORQ, "            simbolos_clase = {u[\"simbolo\"] for u in universo}", "            pass",
     "vale una finalista que GC1 no envió"),
    # H-18
    ("P16", D6, "    if fija is not None:   # QA r02, H-18", "    if False:   # QA r02, H-18", "el override de la bolsa se suma otra vez"),
    # H-19
    ("P17", D6, "any(k not in CLASES or v not in SENALES_GC1 for k, v in spp.items())", "False",
     "senal_por_perfil sin validar"),
    # H-20
    ("P18", D6, "            if hoy <= vence + pd.Timedelta(days=int(op(bloque, \"cobertura.dias_max_espera_precio\"))):",
     "            if True:", "el contrafactual espera para siempre (sin NO_RESOLUBLE)"),
    ("P19", D6, "            if hoy <= vence + pd.Timedelta(days=int(op(bloque, \"cobertura.dias_max_espera_precio\"))):",
     "            if hoy < vence + pd.Timedelta(days=int(op(bloque, \"cobertura.dias_max_espera_precio\"))):",
     "cierra NO_RESOLUBLE un día antes (borde)"),
    ("P20", D6, "(\"SIN_DATOS\" if medibles else \"SIN_MUESTRA\")", "\"RESUELTO\"", "el estado por tipo no distingue lo que no se midió"),
    ("P21", D6, "\"fecha_resolucion\": str(vence.date()), \"estado\": estado,", "\"fecha_resolucion\": str(vence.date()), \"estado\": \"RESUELTO\",",
     "NO_RESOLUBLE se registra como RESUELTO"),
    ("P22", D6, "(\"cobertura.dias_max_espera_precio\", 0)):", "):", "dias_max_espera_precio sin validar"),
]

if __name__ == "__main__":
    lista = [m for m in MUTANTES if not base.SOLO or m[0] in base.SOLO]
    with ThreadPoolExecutor(base.PAR) as ex:
        res = list(ex.map(base.correr, lista))
    for mid, desc, est, det in res:
        print(f"{mid} {est:10} {desc} · {det}")
    vivos = [r for r in res if r[2] == "SOBREVIVE"]
    print(f"\n{len(res) - len(vivos)}/{len(res)} matados; sobreviven: {[r[0] for r in vivos]}")
