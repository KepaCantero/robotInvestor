"""QA r03 de T-102 · Prototipo del revisor (NO es código del producto): CIFRA ampliada con NFKC, categorías N* de Unicode,
«%», «‰», «por cien» y números en letra junto a una palabra de probabilidad, confianza o escenario, y marcadores seguidos de
«sobre», «entre», «de cada», «%» u otro marcador. Envuelve `v6.frase_prohibida` en memoria y vuelve a medir los bancos.

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r03_04_prototipo_cifra.py <raiz_repo>
"""
import sys, re, unicodedata, importlib.util, io, contextlib
sys.path.insert(0, "/home/user/robotinvestor/.docs/tickets/T-102/revisores")
raiz = sys.argv[1]
import r03_comun as C
M = C.preparar(raiz); v6 = M["v6"]
NUM = r"(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieci\w+|veint\w*|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|\w+cientos|\w+cientas|mil)"
LETRA = re.compile(rf"\b{NUM}\b|%|‰|\bpor\s+cien(?:to)?\b|\b(?:tercios?|cuart[oa]s?\s+partes|d[eé]cim[oa]s|mitad)\b", re.I)
PROB = re.compile(r"\b(?:(?:im)?probab\w*|posibilidad\w*|chances?|opciones\s+de\s+que|confianza|certeza|seguridad|escenarios?|pesa\w*|peso)\b", re.I)
orig = v6.frase_prohibida
def nueva(t, perm, marcas=None):
    r = orig(t, perm, marcas)
    if r: return r
    libre = unicodedata.normalize("NFKC", v6._MARCADOR.sub(" ", t))
    if any(unicodedata.category(ch).startswith("N") for ch in libre): return "CIFRA"
    if "%" in libre or "‰" in libre: return "CIFRA"
    if LETRA.search(libre) and PROB.search(libre): return "CIFRA"
    if PROB.search(t) and len(list(v6._MARCADOR.finditer(t))) >= 1 and re.search(r"\}\s*(?:sobre|entre|de\s+cada|%|\{)", t): return "CIFRA"
    return None
v6.frase_prohibida = nueva
# banco propio
spec = importlib.util.spec_from_file_location("b3", "/home/user/robotinvestor/.docs/tickets/T-102/revisores/r03_02_banco_prompt.py")
sys.argv = [sys.argv[0], raiz]
b3 = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(b3)
buf = io.StringIO()
with contextlib.redirect_stdout(buf): b3.main()
print("\n".join(l for l in buf.getvalue().splitlines() if not l.startswith("  [fuera]") and "«" not in l or "r13" in l))
spec2 = importlib.util.spec_from_file_location("b2", "/home/user/robotinvestor/.docs/tickets/T-102/revisores/r02_banco_nuevo.py")
b2 = importlib.util.module_from_spec(spec2)
with contextlib.redirect_stdout(io.StringIO()): spec2.loader.exec_module(b2)
perm = b2.permitidos()
leg = [f for t, e, g, f in b2.BANCO if e is None and not re.search(r"\d", f)]
q = [f for f in leg if v6.texto_prohibido(f, perm)]
print("r02 legítimas sin dígitos quitadas:", len(q), "/", len(leg), q)
