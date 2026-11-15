"""QA r01 de T-128 · barrido propio de las fichas con casos de control (independiente de `impl_barrido_identificadores.py`).

Para cada caso de control, por el camino completo del Motor (`Motor.servir`, CT-09):
  ID   ¿aparece en la respuesta (resultado, limitaciones, detalle) un texto de los datos que nombra un componente? Se toman
       como nombres los valores de texto de cualquier clave dentro de una lista de objetos y las claves de un objeto cuyos
       valores son objetos o listas (p. ej. `miembros`, `plataformas`, `oferta_stablecoins`).
  UNO  cada colección de componentes de los datos (lista de objetos con «id» o «nombre», u objeto de objetos o de listas
       con 2 o más claves) se deja en UN elemento: ¿se sirve? Si se sirve, la entrega es la de ese componente; se lista para
       leer la ficha del Catálogo y decidir si es un ámbito (un par, una curva) o un instrumento.
Uso: .venv/bin/python -I .docs/tickets/T-128/revisores/r01_01_barrido_un_componente.py [ejecutor]
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.motor import servicio  # noqa: E402

m = C.motor()
GENERICOS = {"fecha", "fuente", "moneda", "EUR", "USD", "frecuencia", "metodo", "tipo", "ambito", "segmento", "nombre"}


def _es_coleccion(x, raiz):
    """Objeto de 2 o más componentes con datos propios (objetos o listas de objetos); nunca `valores` entero ni un
    objeto de series (listas de escalares), cuyas claves son nombres de variables."""
    return (not raiz and isinstance(x, dict) and len(x) >= 2
            and all(isinstance(v, dict) or (isinstance(v, list) and v and isinstance(v[0], dict)) for v in x.values()))


def nombres(x, out, raiz=True):
    if isinstance(x, dict):
        if _es_coleccion(x, raiz):
            out.update(str(k) for k in x)
        for v in x.values():
            nombres(v, out, False)
    elif isinstance(x, list):
        for v in x:
            if isinstance(v, dict):
                for k, s in v.items():
                    if isinstance(s, str) and k in ("id", "nombre", "ticker", "isin", "emisor", "miembro", "vehiculo"):
                        out.add(s)
            nombres(v, out, False)
    return out


def colecciones(x, ruta=()):
    """Rutas a colecciones de componentes dentro de `valores` (nunca `valores` entero)."""
    if isinstance(x, dict):
        if _es_coleccion(x, not ruta):
            yield ruta, "obj"
        for k, v in x.items():
            yield from colecciones(v, ruta + (k,))
    elif isinstance(x, list):
        if len(x) >= 2 and all(isinstance(e, dict) and ("id" in e or "nombre" in e) for e in x):
            yield ruta, "lista"


def en(x, ruta):
    for k in ruta:
        x = x[k]
    return x


def servir(p):
    r, exc, _ = C.servir_contando(m, p)
    if exc is not None:
        return "X", {"excepcion": repr(exc)[:200]}
    return ("S" if str(r["estado"]).startswith("SERVED") else "R"), r


ids_vistos, uno = [], []
total = 0
for ficha in sorted(servicio.CASOS_CONTROL):
    for i, caso in enumerate(servicio.CASOS_CONTROL[ficha]):
        if not caso.get("datos"):
            continue
        total += 1
        p = C.peticion(ficha, i)
        st, r = servir(p)
        val = {}
        for d in p["datos"]:
            val.update(d.get("valores") or {})
        ns = {n for n in nombres(val, set()) if n not in GENERICOS and len(n) >= 1}
        dump = json.dumps({k: r.get(k) for k in ("resultado", "limitaciones", "detalle")}, ensure_ascii=False, default=str)
        dump_claves = set()

        def claves(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    dump_claves.add(str(k))
                    claves(v)
            elif isinstance(x, list):
                for v in x:
                    claves(v)
        claves(r.get("resultado"))
        valores_txt = set()

        def textos(x):
            if isinstance(x, dict):
                for v in x.values():
                    textos(v)
            elif isinstance(x, list):
                for v in x:
                    textos(v)
            elif isinstance(x, str):
                valores_txt.add(x)
        textos(r.get("resultado"))
        hallados = sorted(n for n in ns if n in valores_txt or n in dump_claves
                          or any(f"{n}:" in s or f"«{n}»" in s or f" {n} " in f" {s} " for s in (r.get("limitaciones") or [])))
        if hallados:
            ids_vistos.append((ficha, i, st, hallados[:6]))
        for j, (ruta, tipo) in enumerate(colecciones(val)):
            if j >= 4:
                break
            q = copy.deepcopy(p)
            for d in q["datos"]:
                vv = d.get("valores") or {}
                try:
                    obj = en(vv, ruta[:-1]) if ruta else None
                    col = en(vv, ruta)
                except (KeyError, TypeError, IndexError):
                    continue
                if tipo == "lista":
                    nuevo = col[:1]
                else:
                    k0 = sorted(col)[0]
                    nuevo = {k0: col[k0]}
                if ruta:
                    obj[ruta[-1]] = nuevo
            st1, r1 = servir(q)
            if st1 == "S":
                uno.append((ficha, i, ".".join(map(str, ruta)), tipo))

print(f"{total} casos de control con datos, {len(servicio.CASOS_CONTROL)} fichas\n")
print("ID: nombres de componentes que aparecen en la respuesta")
for x in ids_vistos:
    print("   ", x)
print("\nUNO: colecciones reducidas a un solo componente que se SIRVEN (por ficha, sin repetir ruta)")
vistos = set()
for f, i, ruta, tipo in uno:
    if (f, ruta) in vistos:
        continue
    vistos.add((f, ruta))
    print(f"    {f} (caso {i}) · {ruta} [{tipo}]")
