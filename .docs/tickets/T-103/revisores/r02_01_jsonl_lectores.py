"""QA r02 de T-103 (revisor independiente): lectores de JSONL tras partir solo por «\\n» (H-48).

Uso: python -I r02_01_jsonl_lectores.py <ruta a bloque_a/11_Ejecutor en 7feb697> [<ruta a bloque_a/11_Ejecutor anterior>]
     [--repo <raíz del repositorio, para los casos INFO de A-Forex, B y .docs/scripts>]

Casos (FALLO solo en el Bloque A, que es el alcance de T-103; lo demás es INFO):
 1. Almacén con U+2028, U+2029 y U+0085 en un valor, en una clave del registro, en un dict anidado y en una lista, sellado y
    anterior a los sellos (se migra al abrir); `verificar_integridad` si existe.
 2. Escritura cortada (último registro a medias) justo en mitad de los 3 bytes de U+2028: abre y aparta lo no sellado.
 3. Ficheros con «\\r\\n»: el almacén convertido entero a CRLF abre, escribe y vuelve a abrir; la cinta y la caché también.
    Se compara con el código anterior (mismo comportamiento esperado).
 4. Ficheros con «\\r» solo (fin de línea de Mac clásico): INFO, comparado con el anterior.
 5. Cinta (`ReplayClient`) en modo grabar con un cliente base que devuelve U+2028/U+2029/U+0085, y reproducir después;
    caché de resultados `guardar` y reabrir; las dos con CRLF.
 6. (INFO, fuera del alcance) el mismo patrón en A-Forex, B y `.docs/scripts/registro_experimentos.py`.
Sin red, sin claves.
"""
import json
import subprocess
import sys
from pathlib import Path

args = [a for a in sys.argv[1:]]
REPO = None
if "--repo" in args:
    i = args.index("--repo")
    REPO = Path(args[i + 1]).resolve()
    del args[i:i + 2]
EJ = Path(args[0]).resolve()
ANTES = Path(args[1]).resolve() if len(args) > 1 else None
fallos = 0


def ver(ok, nombre, detalle="", info=False):
    global fallos
    if info:
        print(f"INFO  {nombre} — {detalle}")
        return
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}{' — ' + str(detalle) if detalle else ''}")
    fallos += 0 if ok else 1


# Cada caso corre en un proceso aparte con -I y la ruta del ejecutor, para poder comparar dos versiones del código.
PROG = r'''
import json, sys, shutil, tempfile, os
from pathlib import Path
sys.path.insert(0, sys.argv[1])
caso = sys.argv[2]
from bloque_a.almacen import Almacen
SEPS = {"U+2028": " ", "U+2029": " ", "U+0085": "\u0085"}
out = {}
def reabrir(d):
    try:
        a = Almacen(d)
        return "ok", a
    except Exception as e:
        return f"{type(e).__name__}: {str(e)[:80]}", None

if caso == "valores":
    for nombre, s in SEPS.items():
        for legado in (False, True):
            d = Path(tempfile.mkdtemp())
            a = Almacen(d)
            a.escribir("F5", "AG-01", {"id": "uno", "nota": f"a{s}b"})
            a.escribir("F5", "AG-01", {"id": "dos", f"clave{s}rara": 1, "anidado": {"x": [f"{s}", {"y": f"z{s}"}]}})
            a.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": "INC-1", "detalle": f"{s}" * 50})
            a.escribir("F5", "AG-01", {"id": "tres"})
            if legado:
                (d / "sellos_integridad.json").unlink(); (d / "formato_almacen.json").unlink()
            r, b = reabrir(d)
            if b is not None:
                ids = list(b.estado("F5"))
                ok = ids == ["uno", "dos", "tres"] and b.estado("F5")["uno"]["nota"] == f"a{s}b" and len(b.leer("HA")) == 1
                b.escribir("F5", "AG-01", {"id": "cuatro", "nota": s})
                r2, c = reabrir(d)
                ok = ok and c is not None and list(c.estado("F5")) == ["uno", "dos", "tres", "cuatro"]
                if c is not None and hasattr(c, "verificar_integridad"):
                    try:
                        v = c.verificar_integridad(); ok = ok and (v is None or bool(v) or v == [])
                    except Exception as e:
                        ok = False; r2 = f"verificar_integridad: {type(e).__name__}"
                r = "ok" if ok else f"mal: {ids} / {r2}"
            out[f"{nombre} {'legado' if legado else 'sellado'}"] = r
            shutil.rmtree(d)

elif caso == "corte_en_u2028":
    for corte in (1, 2):
        d = Path(tempfile.mkdtemp())
        a = Almacen(d)
        a.escribir("F5", "AG-01", {"id": "uno"})
        ruta = d / "F5_historial_analisis.jsonl"
        antes = ruta.read_bytes()
        a.escribir("F5", "AG-01", {"id": "dos", "nota": "x y"})
        datos = ruta.read_bytes()
        nuevo = datos[len(antes):]
        k = nuevo.index(" ".encode()) + corte
        ruta.write_bytes(antes + nuevo[:k])   # el proceso murió a mitad del carácter, antes del sello
        import json as _j
        sellos = _j.loads((d / "sellos_integridad.json").read_text()); sellos["F5"] = [1, a._entradas["F5"][0]["_hash"]]
        (d / "sellos_integridad.json").write_text(_j.dumps(sellos, sort_keys=True))
        r, b = reabrir(d)
        apartado = (d / "F5_historial_analisis.jsonl.no_confirmado.jsonl").exists()
        out[f"corte a {corte} byte(s) de U+2028"] = r if b is None else ("ok" if list(b.estado("F5")) == ["uno"] and apartado else f"mal {list(b.estado('F5'))} {apartado}")
        shutil.rmtree(d)

elif caso in ("crlf", "cr"):
    fin = b"\r\n" if caso == "crlf" else b"\r"
    for legado in (False, True):
        d = Path(tempfile.mkdtemp())
        a = Almacen(d)
        for i in range(3):
            a.escribir("F5", "AG-01", {"id": f"r{i}", "nota": "a b"})
        a.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": "INC-1", "detalle": "x"})
        for p in d.glob("*.jsonl"):
            p.write_bytes(p.read_bytes().replace(b"\n", fin))
        if legado:
            (d / "sellos_integridad.json").unlink(); (d / "formato_almacen.json").unlink()
        r, b = reabrir(d)
        if b is not None:
            try:
                b.escribir("F5", "AG-01", {"id": "r3"})
                r2, c = reabrir(d)
                r = "ok" if c is not None and list(c.estado("F5")) == ["r0", "r1", "r2", "r3"] else f"mal tras escribir: {r2}"
            except Exception as e:
                r = f"escribir: {type(e).__name__}: {str(e)[:60]}"
        out[f"almacén {caso} {'legado' if legado else 'sellado'}"] = r
        shutil.rmtree(d)
    from bloque_a.llm import ReplayClient
    from bloque_a.herramientas.ht06_indice import CacheResultados
    d = Path(tempfile.mkdtemp())
    cinta = d / "c.jsonl"
    cinta.write_bytes(b"".join(json.dumps({"clave": f"k{i}", "nota": "a b"}, ensure_ascii=False).encode() + fin for i in range(3)))
    try:
        t = ReplayClient(cinta, "reproducir")._tabla
        out[f"cinta {caso}"] = "ok" if sorted(t) == ["k0", "k1", "k2"] and t["k1"]["nota"] == "a b" else f"mal {sorted(t)}"
    except Exception as e:
        out[f"cinta {caso}"] = f"{type(e).__name__}: {str(e)[:60]}"
    cache = d / "r.jsonl"
    cache.write_bytes(b"".join(json.dumps({"clave": f"k{i}", "valor": "a\u0085b"}, ensure_ascii=False).encode() + fin for i in range(3)))
    try:
        c = CacheResultados(cache)
        out[f"caché {caso}"] = "ok" if c.obtener("k2") == "a\u0085b" and c.obtener("k0") == "a\u0085b" else "mal"
    except Exception as e:
        out[f"caché {caso}"] = f"{type(e).__name__}: {str(e)[:60]}"
    shutil.rmtree(d)

elif caso == "cinta_cache_vivas":
    from bloque_a.llm import ReplayClient, LLMClient, RespuestaLLM, Uso
    from bloque_a.herramientas.ht06_indice import CacheResultados
    import dataclasses
    campos = {f.name for f in dataclasses.fields(Uso)}
    class Base(LLMClient):
        nombre = "base_qa"
        def generar(self, *, agente, modelo, system, mensajes, max_tokens, herramientas=None, esquema=None):
            return RespuestaLLM("respuesta con separadores\u0085fin", Uso(**{k: 1 for k in campos}), modelo, "end_turn")
    d = Path(tempfile.mkdtemp())
    cinta = d / "cinta.jsonl"
    g = ReplayClient(cinta, "grabar", base=Base())
    pedidas = []
    for i in range(3):
        kw = dict(agente=f"AG-0{i}", modelo="m", system=[{"text": "s "}], mensajes=[{"role": "user", "content": f"p{i}\u0085"}], max_tokens=10)
        g.generar(**kw); pedidas.append(kw)
    try:
        rep = ReplayClient(cinta, "reproducir")
        textos = [rep.generar(**kw).texto for kw in pedidas]
        out["cinta grabar → reproducir"] = "ok" if textos == ["respuesta con separadores\u0085fin"] * 3 else f"mal {textos}"
    except Exception as e:
        out["cinta grabar → reproducir"] = f"{type(e).__name__}: {str(e)[:60]}"
    c = CacheResultados(d / "cache.jsonl")
    for i in range(3):
        c.guardar(f"k{i}", {"t": f"v {i}", "l": [" ", "\u0085"]})
    try:
        c2 = CacheResultados(d / "cache.jsonl")
        out["caché guardar → reabrir"] = "ok" if c2.obtener("k1") == {"t": "v 1", "l": [" ", "\u0085"]} else "mal"
    except Exception as e:
        out["caché guardar → reabrir"] = f"{type(e).__name__}: {str(e)[:60]}"
    shutil.rmtree(d)
print(json.dumps(out, ensure_ascii=True))
'''


def correr(ruta, caso):
    r = subprocess.run([sys.executable, "-I", "-c", PROG, str(ruta), caso], capture_output=True, text=True, timeout=600)
    if r.returncode:
        return {"_error": (r.stderr.strip().splitlines() or ["?"])[-1][:160]}
    return json.loads(r.stdout.strip().splitlines()[-1])


for caso, titulo, solo_info in [
    ("valores", "1. Separadores de Unicode en valores, claves, anidados y listas (sellado y legado)", False),
    ("corte_en_u2028", "2. Escritura cortada a mitad de U+2028 (sin sello)", False),
    ("crlf", "3. Ficheros con «\\r\\n» (almacén, cinta y caché)", False),
    ("cr", "4. Ficheros con «\\r» solo (INFO)", True),
    ("cinta_cache_vivas", "5. Cinta y caché de extremo a extremo con los tres separadores", False),
]:
    print(f"--- {titulo}")
    nuevo = correr(EJ, caso)
    viejo = correr(ANTES, caso) if ANTES else {}
    for k, v in nuevo.items():
        antes = f" (antes: {viejo.get(k, viejo.get('_error', '?'))})" if ANTES else ""
        ver(v == "ok", f"{caso} {k}", f"{v}{antes}", info=solo_info)

# 6. Fuera del alcance de T-103 (regla 8: no mezclar bloques): el mismo patrón en los otros bloques y en .docs/scripts
if REPO:
    print("--- 6. El mismo patrón fuera del Bloque A (INFO: fuera del alcance de T-103)")
    PROG_OTRO = r'''
import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, sys.argv[1])
mod = sys.argv[2]
d = Path(tempfile.mkdtemp())
try:
    if mod == "registro":
        import registro_experimentos as m
        clase = [getattr(m, n) for n in dir(m) if isinstance(getattr(m, n), type) and hasattr(getattr(m, n), "anotaciones")][0]
        r = clase(d / "registro.jsonl")
        e = {"_seq": 1, "_hash_prev": "0" * 64, "nota": "a b"}
        e["_hash"] = m.huella(e)
        (d / "registro.jsonl").write_text(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        print("ok" if len(r.anotaciones()) == 1 else "mal")
    else:
        alm = __import__(mod + ".almacen", fromlist=["Almacen"])
        a = alm.Almacen(d)
        archivo, autor = next(iter(alm.PROPIETARIOS.items())) if hasattr(alm, "PROPIETARIOS") else (None, None)
        autor = sorted(autor)[0] if isinstance(autor, (set, frozenset, list, tuple)) else autor
        clave = alm.CLAVES[archivo] if hasattr(alm, "CLAVES") else "id"
        a.escribir(archivo, autor, {clave: "uno", "nota": "a b"})
        alm.Almacen(d)
        print("ok")
except Exception as e:
    print(f"{type(e).__name__}: {str(e)[:90]}")
'''
    for nombre, ruta, mod in [("A-Forex almacén", REPO / "bloque_a_forex" / "11_Ejecutor", "bloque_a_forex"),
                              ("B almacén", REPO / "bloque_b" / "11_Ejecutor", "bloque_b"),
                              (".docs/scripts/registro_experimentos.py", REPO / ".docs" / "scripts", "registro")]:
        r = subprocess.run([sys.executable, "-I", "-c", PROG_OTRO, str(ruta), mod], capture_output=True, text=True, timeout=300)
        ver(False, f"6 {nombre} con U+2028 en un valor", (r.stdout.strip() or r.stderr.strip().splitlines()[-1])[:160], info=True)

print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
