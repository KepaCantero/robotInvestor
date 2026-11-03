#!/usr/bin/env python3
"""Escáner de secretos (repo público): patrones reales de credenciales con
allowlist explícita. Equivalente ligero del detect-secrets de robotTrading
para CI; detect-secrets queda además en pre-commit.

Allowlist: tools/secrets_allowlist.txt — una cadena exacta por línea.
La conocida: el fixture sk-ant-abc… de test_unitarias.py es un SECRETO FALSO
del test anti-inyección de instrucciones, verificado a mano.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXCLUIR = {".git", ".venv", "__pycache__", ".pytest_cache"}
ALLOWLIST = [l.strip() for l in (Path(__file__).parent / "secrets_allowlist.txt").read_text().splitlines() if l.strip() and not l.startswith("#")]

PATRONES = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"glpat-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{30,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
]


def main() -> int:
    hallazgos = []
    for p in RAIZ.rglob("*"):
        if not p.is_file() or p.suffix in (".pyc", ".png", ".svg", ".docx", ".zip", ".epub"):
            continue
        if any(part in EXCLUIR for part in p.relative_to(RAIZ).parts):
            continue
        try:
            texto = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in PATRONES:
            for m in pat.finditer(texto):
                if m.group(0) in ALLOWLIST:
                    continue
                linea = texto.count("\n", 0, m.start()) + 1
                hallazgos.append(f"{p.relative_to(RAIZ)}:{linea}: {m.group(0)[:18]}…")
    if hallazgos:
        for h in hallazgos:
            print(f"  POSIBLE SECRETO: {h}")
        print(f"FALLO: {len(hallazgos)} posibles secretos. Verificar y, si son falsos, allowlist EXPLÍCITA.")
        return 1
    print("Secretos: sin hallazgos (allowlist aplicada).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
