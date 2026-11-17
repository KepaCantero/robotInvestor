"""T-168 QA r01 · 02: mutantes cuadráticos del filtro de diseno_v6. Cada uno se inyecta en una copia del módulo
(en el worktree del revisor; el original se restaura siempre) y se pasan las cuatro pruebas de tiempo lineal.
Se espera que cada mutante haga fallar al menos la prueba de la carga que agranda (y que el original pase).
Uso, desde bloque_a/11_Ejecutor de una copia propia:  python <este script>"""
import re
import subprocess
import sys
import time
from pathlib import Path

MOD = Path("bloque_a/diseno_v6.py")
ANCLA_FRASE = 'def frase_prohibida(t: str, perm, marcas: dict | None = None) -> str | None:\n'
ANCLA_TEXTO = 'def texto_prohibido(t, permitidos=None, marcas: dict | None = None) -> str | None:\n'
ANCLA_LIMPIAR = 'def limpiar(t, perm, marcas: dict | None = None) -> tuple[str, list[str]]:\n'
DOC_FRASE = re.compile(r'(def frase_prohibida\(.*?\n    """.*?"""\n)', re.S)

# (nombre, ancla, línea inyectada tras el docstring o la firma, pruebas que deben caer)
MUTANTES = [
    ("Q1 blancos al final (regex H-26: [ \\t]+$ backtracking)", "frase",
     '    re.search(r"[ \\t]+$", t)\n', {"r04_muchos_espacios", "r06_h45"}),
    ("Q2 sufijo con punto ((?:[A-Z]\\.)+[a-z])", "frase",
     '    re.search(r"(?:[A-Z]\\.)+[a-z]", t)\n', {"r05_h37"}),
    ("Q3 nombres propios seguidos ((?:[A-Z][a-z]+ )+[a-z])", "frase",
     '    re.search(r"(?:[A-Z][a-z]+ )+[a-z]", t)\n', {"r05_h37", "textos_largos"}),
    ("Q4 palabras seguidas en texto_prohibido ((?:\\w+[ ,]+)+;)", "texto",
     '    re.search(r"(?:\\w+[ ,]+)+;", t) if isinstance(t, str) else None\n', {"textos_largos"}),
    ("Q5 cuadrático de constante baja en C (slice+rfind, ~1e9 bytes) en limpiar: LÍMITE, se espera vivo", "limpiar",
     '    _ = [t[:i].rfind("§") for i in range(len(t))] if isinstance(t, str) else None\n', set()),
    ("Q6 cuadrático en C con más constante (slice+count de cada sufijo) en limpiar", "limpiar",
     '    _ = [t[i:].count(" ") for i in range(len(t))] if isinstance(t, str) else None\n', {"r04_muchos_espacios"}),
]


def inyectar(src: str, donde: str, linea: str) -> str:
    if donde == "frase":
        return DOC_FRASE.sub(lambda m: m.group(1) + linea, src, count=1)
    ancla = ANCLA_TEXTO if donde == "texto" else ANCLA_LIMPIAR
    i = src.index(ancla) + len(ancla)
    j = src.index('"""', src.index('"""', i) + 3) + 4   # tras el docstring
    return src[:j] + linea + src[j:]


def correr() -> tuple[set[str], float, str]:
    t0 = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_t102_filtro.py",
                            "-k", "tiempo_lineal", "-rf"], capture_output=True, text=True, timeout=600)
        out = p.stdout
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        return {"TIMEOUT"}, time.perf_counter() - t0, out
    caidas = set(re.findall(r"FAILED tests/test_t102_filtro\.py::test_(\w+?)_(?:en_tiempo_lineal|tiempo_lineal)", out))
    return caidas, time.perf_counter() - t0, out.strip().splitlines()[-1]


def main():
    orig = MOD.read_text(encoding="utf-8")
    ok = True
    try:
        caidas, dur, ult = correr()
        print(f"ORIGINAL: caídas={sorted(caidas) or '-'} · {ult} · {dur:.1f} s")
        ok &= not caidas
        for nombre, donde, linea, esperadas in MUTANTES:
            mut = inyectar(orig, donde, linea)
            assert mut != orig, nombre
            MOD.write_text(mut, encoding="utf-8")
            caidas, dur, ult = correr()
            norm = {c.replace("r04_muchos_espacios", "r04_muchos_espacios").replace("r06_h45_marcador_y_muchos_espacios", "r06_h45")
                    .replace("r05_h37_sufijo", "r05_h37").replace("textos_largos", "textos_largos") for c in caidas}
            muerto = bool(norm & esperadas) or "TIMEOUT" in caidas
            ok &= muerto or not esperadas   # sin esperadas: límite documentado (cuadrático por debajo del tope)
            print(f"{'MUERTO ' if muerto else ('LIMITE ' if not esperadas else 'VIVO   ')} {nombre}: caídas={sorted(norm)} esperadas⊇{sorted(esperadas)} · {ult} · {dur:.1f} s")
    finally:
        MOD.write_text(orig, encoding="utf-8")
    print("RESULTADO:", "todos los mutantes muertos" if ok else "HAY MUTANTES VIVOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
