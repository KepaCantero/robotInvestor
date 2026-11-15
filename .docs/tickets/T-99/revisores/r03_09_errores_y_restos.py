"""r03_09 · Restos de H-20 y H-21 en el registro 0.3.0: errores del sistema de ficheros que no salen como RegistroError (el
banco los convierte en BancoError solo si lo son) y lectores que necesitan escribir el «.lock».
Uso: .venv/bin/python -B r03_09_errores_y_restos.py <raíz>"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import borrar, caso, experimento_completo, fin, lanza, rx, tmpdir  # noqa: E402

import banco_medida as bm  # noqa: E402

d = tmpdir(); tmps = [d]
# 1. El registro es un directorio
(d / "dir.jsonl").mkdir()
e = lanza(rx.Registro(d / "dir.jsonl").verificar, BaseException)
caso("registro que es un directorio: RegistroError (no IsADirectoryError)", isinstance(e, rx.RegistroError), repr(e)[:120])
ns = argparse.Namespace(desde="2025-03-07", hasta="2025-05-30", salida=str(d / "s"), cliente="mock", frecuencia=None, clases=None,
                        semilla=7, remuestreos=2000, ventana=63, registro=str(d / "dir.jsonl"), experimento=None, max_variantes=1)
e = lanza(lambda: bm.ejecutar_a(ns), BaseException)
caso("…y el banco sale con BancoError (código 2, sin traza)", isinstance(e, bm.BancoError), repr(e)[:120])

# 2. El sello es un directorio
reg = rx.Registro(d / "r.jsonl"); experimento_completo(reg)
reg.sello.unlink(); reg.sello.mkdir()
e = lanza(reg.verificar, BaseException)
caso("sello que es un directorio: RegistroError", isinstance(e, rx.RegistroError), repr(e)[:120])

# 3. Un lector necesita crear o abrir el «.lock» (lectura de un registro en una carpeta donde no se puede escribir)
reg = rx.Registro(d / "r2.jsonl"); experimento_completo(reg)
Path(str(reg.ruta) + ".lock").unlink(); Path(str(reg.ruta) + ".lock").mkdir()   # simula «no se puede abrir el .lock»
e = lanza(reg.verificar, BaseException)
caso("(referencia) un lector sin poder abrir el «.lock» falla cerrado con RegistroError", isinstance(e, rx.RegistroError), repr(e)[:120])

for t in tmps:
    borrar(t)
fin()
