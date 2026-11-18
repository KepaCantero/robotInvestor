"""Arma la página de la prueba PB-40: la plantilla con el informe visual incrustado (T-186)."""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def armar(informe: Path, plantilla: Path, salida: Path) -> None:
    t = informe.read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", t, flags=re.S))
    cuerpo = re.search(r"<body[^>]*>(.*)</body>", t, flags=re.S)
    html = cuerpo.group(1) if cuerpo else t
    if re.search(r"<script", html, flags=re.I):
        raise SystemExit("el informe trae scripts: no se incrusta")
    datos = json.dumps({"css": css, "html": html}, ensure_ascii=False).replace("</", "<\\/")
    salida.write_text(plantilla.read_text(encoding="utf-8").replace("__INFORME_JSON__", datos), encoding="utf-8")


if __name__ == "__main__":
    armar(AQUI / "informe_visual_RUN-2024-0001.html", AQUI / "plantilla_prueba.html", Path(sys.argv[1]))
