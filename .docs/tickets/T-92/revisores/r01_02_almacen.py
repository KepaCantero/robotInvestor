"""QA r01 de T-92: ataques al almacén con cerrojo y sellos (O5, O7, H-02).

Uso: python -I r01_02_almacen.py <ruta a bloque_a/11_Ejecutor>
"""
import json, multiprocessing as mp, sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import Almacen

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

def abre(t):
    try:
        a = Almacen(t); return a, None
    except Exception as x:
        return None, f"{type(x).__name__}: {x}"

def f5(t):
    return next(t.glob("F5*"))

# 4. Dos procesos escribiendo a la vez en la misma carpeta (cerrojo entre procesos)
def _escritor(carpeta, n, tag):
    a = Almacen(Path(carpeta))
    for i in range(n):
        a.escribir("F5", "AG-01", {"id": f"{tag}-{i}"})

def pruebas():
    # 1. Fallo a mitad (OSError al guardar el sello): el registro se deshace y el almacén sigue abriendo
    for exc in (OSError("disco lleno"), KeyboardInterrupt()):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d); a = Almacen(t)
            a.escribir("F5", "AG-01", {"id": "uno"})
            orig = Almacen._guardar_json
            def roto(ruta, datos, _o=orig, _e=exc):
                if ruta.name == "sellos_integridad.json":
                    raise _e
                return _o(ruta, datos)
            Almacen._guardar_json = staticmethod(roto)
            try:
                a.escribir("F5", "AG-01", {"id": "dos"})
            except BaseException:
                pass
            finally:
                Almacen._guardar_json = staticmethod(orig)
            lineas = [l for l in f5(t).read_text().splitlines() if l.strip()]
            b, err = abre(t)
            informe(f"1  {type(exc).__name__} al guardar el sello deja el almacén intacto y abrible",
                    b is not None and len(lineas) == 1, f"líneas={len(lineas)}; abrir: {err or 'ok'}")

    # 2. Truncado del final + borrado de sellos Y de la marca de formato: ¿se vuelve a sellar en silencio?
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); a = Almacen(t)
        for k in ("uno", "dos", "tres"):
            a.escribir("F5", "AG-01", {"id": k})
        ls = f5(t).read_text().splitlines()
        f5(t).write_text("\n".join(ls[:-1]) + "\n")
        (t / "sellos_integridad.json").unlink(); (t / "formato_almacen.json").unlink()
        b, err = abre(t)
        informe("2  truncado + borrar sellos y marca de formato no se acepta en silencio", b is None,
                f"abre={'sí' if b else 'no'}; F5 = {list(b.estado('F5')) if b else err}")

    # 3. Manipulaciones que deben detectarse
    for nombre, accion in {
        "cambiar un campo de un registro intermedio": lambda t: f5(t).write_text(f5(t).read_text().replace('"dos"', '"DOS"')),
        "sello alterado": lambda t: (t / "sellos_integridad.json").write_text(json.dumps({**json.loads((t / "sellos_integridad.json").read_text()), "F5": [2, "0" * 64]})),
        "sello no JSON": lambda t: (t / "sellos_integridad.json").write_text("{"),
        "línea JSON no objeto": lambda t: f5(t).write_text(f5(t).read_text() + "[1,2]\n"),
        "añadir una línea al final": lambda t: f5(t).write_text(f5(t).read_text() + f5(t).read_text().splitlines()[-1] + "\n"),
    }.items():
        with tempfile.TemporaryDirectory() as d:
            t = Path(d); a = Almacen(t)
            for k in ("uno", "dos", "tres"):
                a.escribir("F5", "AG-01", {"id": k})
            accion(t)
            b, err = abre(t)
            detect_vivo = None
            try:
                a.leer("F5"); a.escribir("F5", "AG-01", {"id": "cuatro"}); detect_vivo = "no"
            except Exception as x:
                detect_vivo = type(x).__name__
            informe(f"3  {nombre}: no abre y la instancia viva no escribe", b is None and detect_vivo != "no",
                    f"abrir: {err or 'abre'}; instancia viva: {detect_vivo}")


if __name__ == "__main__":
    pruebas()
    with tempfile.TemporaryDirectory() as d:
        Almacen(Path(d))
        ps = [mp.get_context("spawn").Process(target=_escritor, args=(d, 40, k)) for k in "ABC"]
        [p.start() for p in ps]; [p.join() for p in ps]
        b, err = abre(Path(d))
        n = len(b.leer("F5")) if b else None
        informe("4  tres procesos × 40 escrituras: cadena íntegra y 120 registros", b is not None and n == 120
                and b.verificar_integridad("F5")["F5"], f"registros={n}; {err or ''}")
    print("fallos:", fallos)
