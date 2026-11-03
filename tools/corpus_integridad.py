#!/usr/bin/env python3
"""Congela y verifica la integridad del corpus canónico (adaptación de los
conformance goldens de robotTrading: el corpus .md/.docx/esquemas es la fuente
de verdad y no puede cambiar sin un re-congelado deliberado).

Alcance del manifiesto: todo lo entregado en bloque_a/, bloque_a_forex/ y
bloque_b/ EXCEPTO sus 11_Ejecutor (el código evoluciona en las fases) y los
directorios de ejecución; más los README de la raíz del repo.

Uso:
  python tools/corpus_integridad.py            # verificar (exit 1 si diverge)
  python tools/corpus_integridad.py --update   # re-congelar (SOLO deliberado:
                                               # mismo commit que el cambio + motivo)
"""
import hashlib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANIFIESTO = Path(__file__).resolve().parent / "corpus_manifest.txt"
EXCLUIR_PARTES = {".git", ".venv", "__pycache__", ".pytest_cache", "estado_bloque_a", "entregables"}
README_RAIZ = ["README - Índice de la entrega y registro de la actualización V5.1.md",
               "README - Índice de la entrega y registro de la actualización V5.1.docx"]


def es_corpus(ruta: Path) -> bool:
    rel = ruta.relative_to(RAIZ)
    if any(p in EXCLUIR_PARTES for p in rel.parts):
        return False
    if rel.parts[0] in ("bloque_a", "bloque_a_forex", "bloque_b"):
        # El ejecutor es código vivo: fuera del congelado
        return "11_Ejecutor" not in rel.parts
    return str(rel) in README_RAIZ


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def inventario() -> dict:
    return {str(p.relative_to(RAIZ)): sha256(p)
            for p in sorted(RAIZ.rglob("*"))
            if p.is_file() and not p.name.startswith(".")
            and es_corpus(p) and p.suffix not in (".pyc",)}


def main() -> int:
    actualizar = "--update" in sys.argv
    actual = inventario()
    if actualizar:
        with open(MANIFIESTO, "w", encoding="utf-8") as f:
            for ruta, h in sorted(actual.items()):
                f.write(f"{h}  {ruta}\n")
        print(f"Manifiesto re-congelado: {len(actual)} archivos.")
        print("RECUERDA: el re-congelado va en el MISMO commit que el cambio, con el motivo.")
        return 0
    if not MANIFIESTO.exists():
        print("FALLO: no existe tools/corpus_manifest.txt; congela primero con --update.")
        return 1
    congelado = {}
    for linea in MANIFIESTO.read_text(encoding="utf-8").splitlines():
        if linea.strip():
            h, _, ruta = linea.partition("  ")
            congelado[ruta] = h
    cambios = sorted(set(congelado) ^ set(actual))
    divergido = [r for r in set(congelado) & set(actual) if congelado[r] != actual[r]]
    if cambios or divergido:
        for r in cambios:
            tipo = "AÑADIDO al corpus sin re-congelar" if r in actual else "ELIMINADO del corpus sin re-congelar"
            print(f"  {tipo}: {r}")
        for r in divergido:
            print(f"  MODIFICADO sin re-congelar: {r}")
        print("FALLO: el corpus canónico diverge del manifiesto congelado.")
        print("Si el cambio es deliberado: --update + motivo en el commit (protocolo de CLAUDE.md).")
        return 1
    print(f"Corpus íntegro: {len(actual)} archivos coinciden con el manifiesto congelado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
