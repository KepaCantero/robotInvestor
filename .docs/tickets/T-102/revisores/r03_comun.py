"""QA r03 de T-102 · Piezas comunes de los scripts del revisor (no es una prueba; lo importan los r03_*.py).

- `preparar(raiz)`: pone el código de esa raíz en `sys.path` (y comprueba que se importa de ahí, no del árbol principal).
- `bloque(tmp)`: un Bloque V6 como el de `tests/test_t102_filtro.py` (DIV, cliente simulado).
- `ciclo(inyectar)`: un ciclo real con el Sintetizador simulado modificado por `inyectar(out, msg)`; devuelve lo que llega al
  paquete, a la redacción y a los tres entregables (el HTML, sin etiquetas y con las entidades deshechas).
"""
from __future__ import annotations

import copy
import html
import json
import re
import sys
import tempfile
from pathlib import Path

M: dict = {}


def preparar(raiz: str | Path) -> dict:
    raiz = Path(raiz).resolve()
    ejec = raiz / "bloque_a" / "11_Ejecutor"
    sys.path.insert(0, str(ejec / "tests"))
    sys.path.insert(0, str(ejec))
    from conftest import AS_OF, DATOS, config_pruebas

    from bloque_a import diseno_v6 as v6
    from bloque_a import mock_respuestas as mr
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, fusionar
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    assert Path(v6.__file__).resolve().is_relative_to(ejec.resolve()), v6.__file__
    M.update(dict(AS_OF=AS_OF, DATOS=DATOS, config_pruebas=config_pruebas, v6=v6, mr=mr, RUTA=RUTA_UNIVERSO_EJEMPLO,
                  fusionar=fusionar, ProveedorCSV=ProveedorCSV, cargar_universo=cargar_universo, MockClient=MockClient,
                  Bloque=Bloque, ejec=ejec))
    return M


def bloque(tmp=None, activos=("DIV",)):
    tmp = Path(tmp or tempfile.mkdtemp(prefix="r03_t102_"))
    cfg = M["config_pruebas"](**M["fusionar"]({"diseno": "v6", "perfiles": {"activos": list(activos)},
                                               "seleccion": {"umbral_senal_gc1": 0.55}}, {}))
    return M["Bloque"](cfg, M["ProveedorCSV"](M["DATOS"]), M["cargar_universo"](M["RUTA"]), M["MockClient"](),
                       tmp / "estado", tmp / "ent")


def _html_a_texto(s: str) -> str:
    s = re.sub(r"<style.*?</style>|<script.*?</script>|<svg.*?</svg>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def ciclo(inyectar=None, activos=("DIV",)) -> dict:
    """Un ciclo real (C1, mock) con el Sintetizador simulado modificado. Devuelve un dict con `res`, `red` (lo que recibe
    `redaccion.generar`), `marcas`, `paquete` (JSON del paquete), `html`, `md`, `json` (textos de los entregables) y
    `todo` (todo junto) o `error` si el ciclo revienta."""
    mr = M["mr"]
    orig = mr._sintetizador
    capt: dict = {}

    def sint(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        capt.setdefault("msg", msg)
        if inyectar:
            inyectar(out, msg)
        return out
    mr._sintetizador = sint
    try:
        b = bloque(activos=activos)
        orig_gen = b.redaccion.generar

        def generar(bl, paquete, extras, r, *a, **k):
            capt["red"] = copy.deepcopy(r)
            capt["marcas"] = M["v6"].marcadores(paquete)
            return orig_gen(bl, paquete, extras, r, *a, **k)
        b.redaccion.generar = generar
        try:
            res = b.ciclo(M["AS_OF"])
        except Exception as e:   # noqa: BLE001
            return {"error": f"{type(e).__name__}: {e}"}
    finally:
        mr._sintetizador = orig
    ent = res.get("entregables") or {}
    textos = {}
    for k, ruta in ent.items():
        p = Path(ruta)
        s = p.read_text(encoding="utf-8") if p.exists() else ""
        textos[k] = _html_a_texto(s) if k == "informe_visual" else s
    paquete_txt = json.dumps(res["paquete"], ensure_ascii=False)
    red_txt = json.dumps(capt.get("red"), ensure_ascii=False)
    return {"res": res, "red": capt.get("red"), "marcas": capt.get("marcas"), "paquete": paquete_txt, "red_txt": red_txt,
            "html": textos.get("informe_visual", ""), "md": textos.get("informe_tecnico", ""),
            "json": textos.get("paquete_json", ""), "todo": "\n".join([paquete_txt, red_txt, *textos.values()]),
            "limitaciones": res["paquete"].get("limitaciones", []), "dictamen": (res.get("g3_entregables") or {}).get("dictamen")}
