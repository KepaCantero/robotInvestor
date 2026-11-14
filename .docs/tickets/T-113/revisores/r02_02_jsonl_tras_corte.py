"""QA r02 de T-113 · H-02 y H-06: la caché y la cinta cortadas en cada byte; se abre, se graba algo más y se reabre.
Se comprueba: (a) ninguna línea completa se pierde al truncar; (b) lo grabado después del corte se recupera; (c) sin corte el
fichero no cambia ni un byte; (d) al reproducir no se toca; (e) la incidencia se registra (y solo cuando hay algo descartado).
Uso (desde bloque_a/11_Ejecutor de la copia): QA_TMP=<carpeta> python .../r02_02_jsonl_tras_corte.py"""
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.herramientas.ht06_indice import CacheResultados, acabar_en_salto, leer_jsonl  # noqa: E402
from bloque_a.llm import LLMClient, MockClient, ReplayClient, RespuestaLLM, Uso  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402


class _Base(LLMClient):
    nombre = "base_qa"

    def generar(self, **k):
        return RespuestaLLM('{"ok": "ñandú €"}', Uso(entrada=1, salida=1), k["modelo"], "end_turn")


tmp = Path(tempfile.mkdtemp(prefix="qa_t113_r02_jsonl_", dir=os.environ.get("QA_TMP")))
fallos = 0


def ok(cond, texto):
    global fallos
    fallos += not cond
    if not cond:
        print("FALLO", texto)


def gen(cli, i):
    return cli.generar(agente="AG-01", modelo="m", system=[{"type": "text", "text": "s"}], mensajes=[{"role": "user", "content": f"p{i} ñ"}],
                       max_tokens=10)


# ---------- caché ----------
print("== caché: corte en cada byte, guardar y reabrir")
ref = tmp / "ref_cache.jsonl"
c = CacheResultados(ref)
for i in range(4):
    c.guardar(f"k{i}", {"v": i, "t": "ñandú € " * 3, "l": [1, {"a": None}]})
entero = ref.read_bytes()
saltos = [i for i, b in enumerate(entero) if b == 10]
n_cortes = perdidas = pegadas = 0
for corte in range(len(entero) + 1):
    p = tmp / "c.jsonl"
    p.write_bytes(entero[:corte])
    completas = sum(1 for s in saltos if s <= corte)   # cortar justo antes del salto deja la línea entera (sin salto): vale
    acaba_bien = corte == 0 or entero[corte - 1] == 10 or corte in saltos
    try:
        c1 = CacheResultados(p)
    except BaseException as e:  # noqa: BLE001
        ok(False, f"caché corte {corte}: no abre ({type(e).__name__})")
        continue
    ok(len(c1._mem) == completas, f"caché corte {corte}: {len(c1._mem)} claves, se esperaban {completas}")
    ok(c1.descartadas == (0 if acaba_bien else 1), f"caché corte {corte}: descartadas {c1.descartadas}")
    tras = p.read_bytes()
    ok(tras == entero[:saltos[completas - 1] + 1] if completas else tras == b"", f"caché corte {corte}: el fichero no queda en el último salto")
    if corte == 0 or entero[corte - 1] == 10:
        ok(tras == entero[:corte], f"caché corte {corte}: sin corte y el fichero cambió")
    c1.guardar("nuevo", {"n": corte})
    c2 = CacheResultados(p)
    perdidas += len(c2._mem) != completas + 1
    pegadas += c2.obtener("nuevo") != {"n": corte}
    ok(c2.descartadas == 0, f"caché corte {corte}: al reabrir, descartadas {c2.descartadas}")
    ok(all(c2.obtener(f"k{i}") is not None for i in range(completas)), f"caché corte {corte}: falta una línea completa")
    n_cortes += 1
ok(perdidas == 0 and pegadas == 0, f"caché: {perdidas} cortes con claves perdidas, {pegadas} sin recuperar lo nuevo")
print(f"   {n_cortes} puntos de corte; con claves perdidas: {perdidas}; lo grabado después no se recupera: {pegadas}")

# ---------- cinta ----------
print("== cinta: corte en cada byte, abrir para grabar, grabar y reproducir")
refc = tmp / "ref_cinta.jsonl"
g = ReplayClient(refc, "grabar", _Base())
for i in range(4):
    gen(g, i)
entero = refc.read_bytes()
saltos = [i for i, b in enumerate(entero) if b == 10]
n_cortes = malos = 0
for corte in range(len(entero) + 1):
    p = tmp / "cinta.jsonl"
    p.write_bytes(entero[:corte])
    completas = sum(1 for s in saltos if s <= corte)   # cortar justo antes del salto deja la línea entera (sin salto): vale
    acaba_bien = corte == 0 or entero[corte - 1] == 10 or corte in saltos
    # (d) al reproducir no se toca
    try:
        r0 = ReplayClient(p, "reproducir")
        ok(p.read_bytes() == entero[:corte], f"cinta corte {corte}: reproducir cambió el fichero")
        ok(r0.descartadas == (0 if acaba_bien else 1), f"cinta corte {corte}: descartadas al reproducir {r0.descartadas}")
    except BaseException as e:  # noqa: BLE001
        ok(False, f"cinta corte {corte}: reproducir no abre ({type(e).__name__}: {str(e)[:60]})")
    try:
        g1 = ReplayClient(p, "grabar", _Base())
        if corte == 0 or entero[corte - 1] == 10:
            ok(p.read_bytes() == entero[:corte], f"cinta corte {corte}: sin corte y el fichero cambió")
        gen(g1, 99)
        r1 = ReplayClient(p, "reproducir")
        ok(r1.descartadas == 0 and len(r1._tabla) == completas + 1, f"cinta corte {corte}: {len(r1._tabla)} registros, se esperaban {completas + 1}")
        ok(gen(r1, 99).texto == '{"ok": "ñandú €"}', f"cinta corte {corte}: lo grabado después no se reproduce")
        for i in range(completas):
            gen(r1, i)
    except BaseException as e:  # noqa: BLE001
        malos += 1
        ok(False, f"cinta corte {corte}: {type(e).__name__}: {str(e)[:80]}")
    n_cortes += 1
print(f"   {n_cortes} puntos de corte; con error: {malos}")

# ---------- colas raras ----------
print("== colas raras (última línea sin salto)")
linea = json.dumps({"clave": "a", "valor": 1}).encode()
COLAS = {
    "línea entera sin salto": (linea, 1, linea + b"\n"),
    "línea entera + espacios": (linea + b"\n   ", 1, linea + b"\n"),
    "línea entera + \\r": (linea + b"\r", 1, linea + b"\r\n"),
    "CRLF cortado tras \\r\\n": (linea + b"\r\n" + linea[:5], 1, linea + b"\r\n"),
    "cola que es JSON pero no un registro (12)": (linea + b"\n12", 1, linea + b"\n12\n"),
    "cola «null»": (linea + b"\nnull", 1, linea + b"\nnull\n"),
    "cola UTF-8 partida": (linea + b"\n" + '{"clave": "ñ'.encode()[:-1], 1, linea + b"\n"),
    "ilegible en medio y cola entera": (b"{mal\n" + linea, 1, b"{mal\n" + linea + b"\n"),
    "ilegible en medio y cola cortada": (b"{mal\n" + linea + b"\n" + linea[:7], 1, b"{mal\n" + linea + b"\n"),
    "solo una línea cortada": (linea[:9], 0, b""),
    "vacío": (b"", 0, b""),
    "cola de 100 000 corchetes": (linea + b"\n" + b"[" * 100000, 1, linea + b"\n"),
}
for nombre, (datos, claves, esperado) in COLAS.items():
    p = tmp / "cola.jsonl"
    p.write_bytes(datos)
    try:
        cc = CacheResultados(p)
        res = f"caché: {len(cc._mem)} claves, {cc.descartadas} descartadas, fichero {'como se esperaba' if p.read_bytes() == esperado else 'DISTINTO: ' + repr(p.read_bytes()[-30:])}"
        ok(len(cc._mem) == claves and p.read_bytes() == esperado, f"cola «{nombre}»: {res}")
        cc.guardar("z", 2)
        ok(CacheResultados(p).obtener("z") == 2 and CacheResultados(p).obtener("a") == (1 if claves else None), f"cola «{nombre}»: tras guardar no se recupera")
    except BaseException as e:  # noqa: BLE001
        res = f"caché: {type(e).__name__}: {str(e)[:60]}"
        ok(False, f"cola «{nombre}»: {res}")
    print(f"   {nombre:44s} {res}")

# acabar_en_salto es idempotente y no toca un fichero acabado en salto
p = tmp / "idem.jsonl"
p.write_bytes(linea + b"\n" + linea[:4])
acabar_en_salto(p)
a1 = p.read_bytes()
acabar_en_salto(p)
ok(a1 == p.read_bytes() == linea + b"\n", "acabar_en_salto no es idempotente")

# ---------- incidencia ----------
print("== incidencia al arrancar")


def bloque(carp, cli=None):
    return Bloque(config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli or MockClient(), carp / "e", carp / "n")


def incs(b):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "descartada" in e.get("detalle", "")]


t1 = tmp / "inc_limpio"
b = bloque(t1)
ok(not incs(b), "estado nuevo: hay incidencia de descartadas")
(t1 / "e" / "cache_resultados.jsonl").write_bytes(linea + b"\n")
b = bloque(t1)
ok(not incs(b), "caché sana: hay incidencia de descartadas")
with open(t1 / "e" / "cache_resultados.jsonl", "ab") as fh:
    fh.write(linea[:8])
b = bloque(t1)
i1 = incs(b)
ok(len(i1) == 1 and i1[0]["tipo"] == "HERRAMIENTA" and "1 línea" in i1[0]["detalle"], f"caché cortada: incidencias {[(x['tipo'], x['detalle'][:60]) for x in i1]}")
print("   caché cortada:", [(x["tipo"], x["severidad"], x["objeto"], x["detalle"]) for x in i1])
b = bloque(t1)
ok(len(incs(b)) == 1, f"segundo arranque (ya truncada): incidencias {len(incs(b))}, se esperaba que siguiera habiendo 1")
with open(t1 / "e" / "cache_resultados.jsonl", "ab") as fh:
    fh.write(b"{ilegible en medio\n" + linea + b"\n")
n0 = len(incs(bloque(t1)))
n1 = len(incs(bloque(t1)))
print(f"   caché con una línea ilegible EN MEDIO (no se quita del fichero): incidencias tras dos arranques más: {n0} y {n1} (una por arranque)")
# cinta cortada, en modo grabar y en modo reproducir
t2 = tmp / "inc_cinta"
t2.mkdir()
cin = t2 / "cinta.jsonl"
g = ReplayClient(cin, "grabar", _Base())
gen(g, 0)
with open(cin, "ab") as fh:
    fh.write(b'{"clave": "x", "tex')
b = bloque(t2, ReplayClient(cin, "reproducir"))
ok(len(incs(b)) == 1, f"cinta cortada (reproducir): incidencias {len(incs(b))}")
b = bloque(t2, ReplayClient(cin, "grabar", _Base()))
ok(len(incs(b)) == 2, f"cinta cortada (grabar): incidencias {len(incs(b))}")
b = bloque(t2, ReplayClient(cin, "grabar", _Base()))
ok(len(incs(b)) == 2, f"cinta ya truncada: incidencias {len(incs(b))}")
print("   cinta:", [x["detalle"][:70] for x in incs(b)])
# un cliente por agente (el Contradictor) con líneas descartadas: ¿se declara?
t3 = tmp / "inc_contradictor"
t3.mkdir()
cin2 = t3 / "cinta11.jsonl"
g = ReplayClient(cin2, "grabar", _Base())
gen(g, 0)
with open(cin2, "ab") as fh:
    fh.write(b'{"clave": "x", "tex')
try:
    b = Bloque(config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t3 / "e", t3 / "n",
               cliente_contradictor=ReplayClient(cin2, "reproducir"))
    print(f"   cinta cortada del cliente del Contradictor: incidencias {len(incs(b))} (observación si es 0)")
except TypeError as e:
    print("   (no se pudo montar el cliente del Contradictor:", str(e)[:80], ")")
# la cadena del almacén sigue íntegra
print("FALLOS:", fallos)
