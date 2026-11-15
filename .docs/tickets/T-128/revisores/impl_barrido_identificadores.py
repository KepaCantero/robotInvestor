"""T-128 · barrido de las fichas con casos de control: ¿qué salidas llevan el identificador de un componente o una fila por
componente? Para cada caso de control, se ejecuta la ficha como lo hace `verificar_casos_control` y se buscan en el
resultado:
  ID   un texto de los datos que identifica un componente (claves «id», «ticker», «isin», «emisor», «sociedad», «token»,
       «nombre» dentro de una lista de componentes, o la clave de un objeto de objetos, como «miembros») o el nombre de una
       serie de la petición, como valor o como clave, también dentro de una limitación;
  FILA una lista de objetos (una fila por algo) o un objeto cuyas claves son esos identificadores.
No juzga: da los candidatos para leer la ficha del Catálogo (por su identificador) y decidir. Las 14 fichas del ejecutor
V1.0 (sin casos de control) se revisan leyendo su código.
Uso: python -I .docs/tickets/T-128/revisores/impl_barrido_identificadores.py [carpeta del ejecutor]
"""
import re
import sys
import tempfile
from pathlib import Path

EJE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJE))
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio

CLAVES_ID = {"id", "ticker", "isin", "emisor", "sociedad", "token", "activo", "fondo", "contrato", "componente"}


class _Proveedor:
    as_of = None
    nombre = "barrido-t128"


def _ids(x, en_lista=False, out=None):
    out = set() if out is None else out
    if isinstance(x, dict):
        if len(x) >= 2 and all(isinstance(v, dict) for v in x.values()):   # {nombre: {datos}}: los nombres son ids
            out.update(str(k) for k in x)
        for k, v in x.items():
            if isinstance(v, str) and (k in CLAVES_ID or (en_lista and k == "nombre")) and v.strip():
                out.add(v)
            _ids(v, False, out)
    elif isinstance(x, list):
        for v in x:
            _ids(v, isinstance(v, dict), out)
    return out


def _recorrer(x, ruta=""):
    yield ruta, x
    if isinstance(x, dict):
        for k, v in x.items():
            yield from _recorrer(v, f"{ruta}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _recorrer(v, f"{ruta}[{i}]")


def _rutas_genericas(r):
    return re.sub(r"\[\d+\]", "[]", r)


m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="barrido_t128_"))), _Proveedor(), cargar_config())
filas = {}
for ficha in sorted(servicio.CASOS_CONTROL):
    marcas: dict[str, set[str]] = {}
    for caso in servicio.CASOS_CONTROL[ficha]:
        try:
            ent, _ = m._resolver_datos(caso.get("datos") or [], None)
            m._contexto(ent, caso.get("fecha_corte"))
            r, lim = servicio.IMPLEMENTADAS[ficha]["fn"](ent, dict(caso.get("parametros") or {}))
        except Exception as exc:  # noqa: BLE001
            marcas.setdefault("ERROR", set()).add(f"{type(exc).__name__}: {str(exc)[:80]}")
            continue
        ids = _ids(ent.get("valores") or {}) | {str(k) for k in (ent.get("series") or {})}
        ids -= {"advertencias"}
        for ruta, v in _recorrer(r):
            g = _rutas_genericas(ruta)
            if g.startswith(".advertencias"):
                continue
            if isinstance(v, str) and v in ids:
                marcas.setdefault("ID", set()).add(g)
            if isinstance(v, dict) and ids & set(map(str, v)):
                marcas.setdefault("FILA", set()).add(g + "{id: …}")
            if isinstance(v, list) and v and all(isinstance(e, dict) for e in v):
                marcas.setdefault("FILA", set()).add(g + "[]")
        for x in lim:   # las limitaciones también llegan al solicitante
            if any(re.search(rf"(?<![\w-]){re.escape(i)}(?![\w-])", x) for i in ids):
                marcas.setdefault("ID", set()).add(f"limitaciones: «{x[:60]}…»")
    filas[ficha] = marcas
for ficha, marcas in filas.items():
    if marcas:
        print(f"{ficha}:")
        for k, rutas in sorted(marcas.items()):
            print(f"    {k}: {', '.join(sorted(rutas))[:400]}")
print(f"\n{len(filas)} fichas con casos de control; con candidatos: {sum(1 for x in filas.values() if x)}")
