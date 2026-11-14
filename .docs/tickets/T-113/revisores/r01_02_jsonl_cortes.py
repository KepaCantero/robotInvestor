"""QA r01 de T-113 · H-54 de T-104: caché y cinta cortadas en cualquier byte, líneas ilegibles en medio, vacías, enormes,
y qué pasa al seguir escribiendo después de una línea cortada.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_02_jsonl_cortes.py"""
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, ".")
from bloque_a.herramientas.ht06_indice import CacheResultados, leer_jsonl  # noqa: E402
from bloque_a.llm import LLMClient, ReplayClient, RespuestaLLM, Uso  # noqa: E402


class _Base(LLMClient):
    nombre = "base_qa"

    def generar(self, **k):
        return RespuestaLLM('{"ok": true}', Uso(entrada=1, salida=1), k["modelo"], "end_turn")

fallos = 0


def ok(cond, texto):
    global fallos
    fallos += not cond
    print(("ok   " if cond else "FALLO"), texto)


tmp = Path(tempfile.mkdtemp(prefix="qa_t113_jsonl_"))
filas = [{"clave": f"k{i}", "valor": {"n": i, "t": "añó   línea\u0085 «é»"}} for i in range(4)]
entero = "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in filas).encode()

print("== caché: corte en cada byte")
mal = []
for corte in range(len(entero) + 1):
    r = tmp / "c.jsonl"
    r.write_bytes(entero[:corte])
    try:
        c = CacheResultados(r)
    except Exception as e:  # noqa: BLE001
        mal.append((corte, type(e).__name__)); continue
    completas = entero[:corte].count(b"\n")
    # las líneas completas se leen todas; lo que queda es, como mucho, una cortada
    if any(c.obtener(f"k{i}") != filas[i]["valor"] for i in range(completas)) or c.descartadas > 1:
        mal.append((corte, "contenido"))
ok(not mal, f"caché abre en los {len(entero) + 1} cortes y conserva las líneas completas ({mal[:5]})")

print("== cinta: corte en cada byte (reproducir)")
cinta = [{"clave": f"k{i}", "texto": "{}", "uso": {}, "modelo": "m"} for i in range(4)]
entero_c = "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in cinta).encode()
mal = []
for corte in range(1, len(entero_c) + 1):
    r = tmp / "cinta.jsonl"
    r.write_bytes(entero_c[:corte])
    try:
        rc = ReplayClient(r, "reproducir")
    except Exception as e:  # noqa: BLE001
        mal.append((corte, type(e).__name__, str(e)[:60])); continue
    if len(rc._tabla) < entero_c[:corte].count(b"\n"):
        mal.append((corte, "faltan"))
ok(not mal, f"la cinta abre en todos los cortes ({mal[:5]})")

print("== un corte que deja JSON válido pero otro valor (número o texto truncado)")
r = tmp / "c2.jsonl"
r.write_bytes(b'{"clave": "a", "valor": 1}\n12')
c = CacheResultados(r)
ok(c.obtener("a") == 1 and c.descartadas == 1, f"caché: última línea «12» (JSON válido, no registro) descartada y contada ({c.descartadas})")
r.write_bytes(b'{"clave": "a", "texto": "x"}\n12')
try:
    ReplayClient(r, "reproducir"); ok(False, "cinta con última línea «12» sin salto: se esperaba descarte o error claro")
except ValueError as e:
    print("     cinta con última línea «12» cortada ->", str(e)[-60:], "(ERROR al arrancar: es una escritura cortada que sigue impidiendo arrancar)")
    cinta_12 = True

print("== seguir escribiendo tras una línea cortada")
r = tmp / "c3.jsonl"
r.write_bytes(b'{"clave": "a", "valor": 1}\n{"clave": "b", "val')
c = CacheResultados(r); c.guardar("nuevo", 7)
c2 = CacheResultados(r)
ok(c2.obtener("a") == 1, "caché: tras cortar y guardar, sigue abriendo")
print("     caché: lo guardado después del corte se recupera al reabrir:", c2.obtener("nuevo") == 7, "· descartadas:", c2.descartadas)
perdida_cache = c2.obtener("nuevo") != 7
c2.guardar("otro", 8)
print("     y lo siguiente:", CacheResultados(r).obtener("otro") == 8)

r = tmp / "cinta3.jsonl"
r.write_bytes(b'{"clave": "a", "texto": "{}", "uso": {}, "modelo": "m"}\n{"clave": "b", "tex')
rc = ReplayClient(r, "grabar", _Base())
resp = rc.generar(agente="AG-01", modelo="m", system=[{"type": "text", "text": "s"}], mensajes=[{"role": "user", "content": "hola"}], max_tokens=100)
n1 = len(rc._tabla)
rc.generar(agente="AG-01", modelo="m", system=[{"type": "text", "text": "s"}], mensajes=[{"role": "user", "content": "adiós"}], max_tokens=100)
try:
    rc2 = ReplayClient(r, "reproducir")
    ok(len(rc2._tabla) == 3, f"cinta: tras cortar y grabar dos, reabre con las 3 claves (tiene {len(rc2._tabla)})")
except Exception as e:  # noqa: BLE001
    ok(False, f"cinta: tras una línea cortada, grabar dos respuestas y reabrir -> {type(e).__name__}: {str(e)[-90:]}")

print("== líneas raras")
for nombre, datos, tolera in (("vacío", b"", True), ("solo saltos", b"\n\n\n", True), ("BOM", b'\xef\xbb\xbf{"clave": "a", "valor": 1}\n', None),
                              ("CRLF", b'{"clave": "a", "valor": 1}\r\n{"clave": "b", "valor": 2}\r\n', True),
                              ("NUL en medio", b'{"clave": "a", "valor": 1}\n\x00\x00\x00\n{"clave": "b", "valor": 2}\n', None),
                              ("lista", b'[1,2]\n', None), ("null", b"null\n", None), ("NaN", b'{"clave": "a", "valor": NaN}\n', None),
                              ("clave no texto", b'{"clave": ["x"], "valor": 1}\n', None), ("clave nula", b'{"clave": null, "valor": 1}\n', None),
                              ("clave repetida", b'{"clave": "a", "valor": 1}\n{"clave": "a", "valor": 2}\n', True),
                              ("anidado 100 000", b'{"clave": "a", "valor": ' + b"[" * 100000 + b"]" * 100000 + b"}\n", None)):
    r = tmp / "c4.jsonl"; r.write_bytes(datos)
    try:
        c = CacheResultados(r); res = f"abre, {len(c._mem)} claves, {c.descartadas} descartadas"
    except Exception as e:  # noqa: BLE001
        res = f"EXC {type(e).__name__}: {str(e)[:70]}"; fallos += 1
    try:
        rc = ReplayClient(r, "reproducir"); res2 = f"abre, {len(rc._tabla)} claves, {rc.descartadas} descartadas"
    except Exception as e:  # noqa: BLE001
        res2 = f"{type(e).__name__}: {str(e)[-70:]}"
    print(f"  {nombre:16s} caché: {res} | cinta: {res2}")

print("== enorme")
r = tmp / "grande.jsonl"
with open(r, "wb") as fh:
    for i in range(200000):
        fh.write(json.dumps({"clave": f"k{i}", "valor": {"t": "x" * 200}}).encode() + b"\n")
    fh.write(b'{"clave": "cort')
t0 = time.perf_counter(); c = CacheResultados(r); dt = time.perf_counter() - t0
ok(len(c._mem) == 200000 and c.descartadas == 1, f"caché de {r.stat().st_size >> 20} MB y 200 000 líneas: {dt:.1f} s, {c.descartadas} descartada")

print("== leer_jsonl sin tolerar: el error nombra fichero y línea")
r = tmp / "x.jsonl"; r.write_bytes(b'{"a": 1}\n\xff\xfe\n{"b": 2}\n')
try:
    leer_jsonl(r); ok(False, "se esperaba ValueError")
except ValueError as e:
    ok("x.jsonl: línea 2" in str(e), f"mensaje: {str(e)[-70:]}")
print("FALLOS:", fallos)
