"""QA r02 de T-103 (revisor independiente): los otros dos lectores de JSONL (caché de resultados y cinta) ante una escritura
cortada, que el almacén sí recupera (H-29/H-35) y ellos no.

Uso: python -I r02_06_cache_cortada.py <ruta a bloque_a/11_Ejecutor>

1. `cache_resultados.jsonl` con el último registro a medias (el proceso murió durante `guardar`): ¿arranca un `Bloque` nuevo
   sobre el mismo estado? Se espera que falle cerrado con un mensaje que diga qué fichero y qué hacer, o que aparte la línea.
2. Lo mismo con un corte a mitad de un carácter UTF-8 (byte suelto al final).
3. La cinta (`ReplayClient`, reproducir) con el último registro a medias.
INFO: todo esto es anterior a T-103 (el lector es el mismo que corrige H-48); se mide para la deuda. Sin red, sin claves.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
from bloque_a.herramientas.ht06_indice import CacheResultados
from bloque_a.llm import ReplayClient
from conftest import nuevo_bloque, universo

uni = universo.__wrapped__() if hasattr(universo, "__wrapped__") else None
if uni is None:
    from conftest import RUTA_UNIVERSO_EJEMPLO, cargar_universo
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def intento(nombre, f):
    try:
        r = f()
        print(f"INFO  {nombre} — abre ({r})")
    except Exception as e:
        print(f"INFO  {nombre} — {type(e).__name__}: {str(e)[:110]}")


for corte, titulo in ((b'{"clave": "k9", "valor": {"t": "a', "1. registro a medias"), (b'{"clave": "k9", "valor": "\xe2\x80', "2. corte a mitad de UTF-8")):
    d = Path(tempfile.mkdtemp())
    b = nuevo_bloque(d, uni)
    ruta = Path(d) / "estado" / "cache_resultados.jsonl"
    b.cache.guardar("k1", {"t": "uno"})
    ruta.write_bytes(ruta.read_bytes() + corte)
    intento(f"{titulo}: CacheResultados", lambda: len(CacheResultados(ruta)._mem))
    intento(f"{titulo}: Bloque nuevo sobre el mismo estado", lambda: type(nuevo_bloque(d, uni)).__name__)
    shutil.rmtree(d)

d = Path(tempfile.mkdtemp())
cinta = d / "cinta.jsonl"
cinta.write_text(json.dumps({"clave": "k1", "texto": "x"}) + "\n" + '{"clave": "k2", "tex', encoding="utf-8")
intento("3. cinta con el último registro a medias: ReplayClient(reproducir)", lambda: len(ReplayClient(cinta, "reproducir")._tabla))
shutil.rmtree(d)
print("fallos: 0 (solo INFO)")
