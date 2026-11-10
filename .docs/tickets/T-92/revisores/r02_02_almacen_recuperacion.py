"""QA r02 de T-92 (revisor nuevo): ataques a la recuperación de una escritura no confirmada (H-10) en `almacen.py`.

Uso: python -I r02_02_almacen_recuperacion.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso. Un proceso que muere entre el registro y su sello deja como mucho UN registro sin sellar por
fichero (cada `escribir` es registro + sello bajo el cerrojo); cualquier otra diferencia es manipulación o un sello viejo.
"""
import json, multiprocessing as mp, os, sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import Almacen, _hash

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

def abre(t):
    try:
        return Almacen(t), None
    except Exception as x:
        return None, f"{type(x).__name__}: {x}"

def f5(t):
    return t / "F5_historial_analisis.jsonl"

def con(t, ids):
    a = Almacen(t)
    for k in ids:
        a.escribir("F5", "AG-01", {"id": k})
    return a

def anexar_valido(t, id_):
    """Añade al final de F5 un registro con la cadena bien calculada (cualquiera con acceso a la carpeta puede hacerlo)."""
    lineas = f5(t).read_text(encoding="utf-8").splitlines()
    ult = json.loads(lineas[-1])
    e = {"id": id_, "_seq": ult["_seq"] + 1, "_fecha": ult["_fecha"], "_ts": ult["_ts"], "_autor": "AG-01", "_hash_prev": ult["_hash"]}
    e["_hash"] = _hash(e["_hash_prev"], {k: v for k, v in e.items() if k != "_hash"})
    with open(f5(t), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")

def incidencias(t):
    a, err = abre(t)
    return [] if a is None else [e.get("detalle", "") for e in a.leer("HA")]

def _muere_entre_registro_y_sello(carpeta):
    a = Almacen(Path(carpeta))
    a.escribir("F5", "AG-01", {"id": "uno"})
    Almacen._guardar_json = staticmethod(lambda ruta, datos: os._exit(9))   # muere al ir a guardar el sello
    a.escribir("F5", "AG-01", {"id": "dos"})

def pruebas():
    # 1. Caso legítimo: el proceso muere de verdad entre el registro y el sello
    with tempfile.TemporaryDirectory() as d:
        t = Path(d)
        p = mp.get_context("spawn").Process(target=_muere_entre_registro_y_sello, args=(d,)); p.start(); p.join()
        a, err = abre(t)
        aparte = f5(t).with_name(f5(t).name + ".no_confirmado.jsonl")
        ok = a is not None and list(a.estado("F5")) == ["uno"] and aparte.exists() and any("sin confirmar" in x for x in incidencias(t))
        informe("1  muerte real entre registro y sello: abre en lo sellado, aparta el registro y deja incidencia", ok,
                f"exit={p.exitcode}; {err or list(a.estado('F5'))}")

    # 2. Sello viejo (restaurado de una copia anterior): dos registros CONFIRMADOS por encima del sello
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); con(t, ["uno", "dos", "tres"])
        sellos = json.loads((t / "sellos_integridad.json").read_text())
        primera = json.loads(f5(t).read_text(encoding="utf-8").splitlines()[0])
        sellos["F5"] = [1, primera["_hash"]]
        (t / "sellos_integridad.json").write_text(json.dumps(sellos))
        a, err = abre(t)
        informe("2  con 2 registros por encima del sello (no puede ser una sola escritura cortada) falla cerrado", a is None,
                err or f"abre; F5 = {list(a.estado('F5'))}; apartados: "
                        f"{[json.loads(x)['id'] for x in f5(t).with_name(f5(t).name + '.no_confirmado.jsonl').read_text().splitlines()]}")

    # 3. Instancia viva: alguien añade al final un registro con la cadena bien calculada
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); a = con(t, ["uno", "dos"])
        anexar_valido(t, "forjado")
        try:
            vista = list(a.estado("F5"))
            integ = a.verificar_integridad()["F5"]
            n_inc = sum("sin confirmar" in str(e.get("detalle")) for e in a.leer("HA"))
            informe("3  instancia viva: un registro añadido por fuera se detecta (error o incidencia), no se borra en silencio",
                    not integ or n_inc > 0, f"estado F5 = {vista}; verificar_integridad = {integ}; incidencias = {n_inc}; "
                                            f"apartado = {f5(t).with_name(f5(t).name + '.no_confirmado.jsonl').exists()}")
        except ValueError as x:
            informe("3  instancia viva: un registro añadido por fuera se detecta (error o incidencia), no se borra en silencio", True, str(x))

    # 4. Validar antes de mutar: si la apertura falla por otro fichero, no se reescribe F5
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); a = con(t, ["uno", "dos"])
        a.escribir("F6", "AG-20", {"id": "m1"})
        anexar_valido(t, "sin-sello")
        f6 = t / "F6_memoria_aprendizaje.jsonl"
        f6.write_text(f6.read_text(encoding="utf-8").replace('"m1"', '"m2"'), encoding="utf-8")
        antes = f5(t).read_bytes()
        a2, err = abre(t)
        informe("4  si la apertura falla (F6 manipulado), F5 queda como estaba", a2 is None and f5(t).read_bytes() == antes,
                f"abre={a2 is not None}; F5 reescrito={f5(t).read_bytes() != antes}; {err}")

    # 5. Una escritura cortada en HA (la propia incidencia va a HA)
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); a = Almacen(t)
        a.incidencia("OTRO", "previa")
        ha = t / "HA_historial_auditorias.jsonl"
        sellos = json.loads((t / "sellos_integridad.json").read_text())
        a.incidencia("OTRO", "cortada")
        (t / "sellos_integridad.json").write_text(json.dumps(sellos))
        a2, err = abre(t)
        det = [] if a2 is None else [e["detalle"] for e in a2.leer("HA")]
        informe("5  escritura cortada en HA: abre, aparta la cortada y anota la incidencia en HA",
                a2 is not None and "cortada" not in det and any("sin confirmar" in x for x in det), err or str(det))
    # 6. Ctrl-C justo después de sustituir el sello (en la limpieza del temporal de `_guardar_json`): el sello ya dice n+1
    #    y `escribir` trunca el registro, así que el almacén queda con menos registros que el sello
    from unittest.mock import patch
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); a = con(t, ["uno"])
        real = Path.unlink
        def unlink(self, missing_ok=False):
            if self.parent == t and not self.exists():
                raise KeyboardInterrupt
            return real(self, missing_ok=missing_ok)
        with patch.object(Path, "unlink", unlink):
            try:
                a.escribir("F5", "AG-01", {"id": "dos"})
            except KeyboardInterrupt:
                pass
        a2, err = abre(t)
        informe("6  Ctrl-C tras sustituir el sello no deja el almacén sin abrir", a2 is not None,
                err or str(list(a2.estado("F5"))))
    print("fallos:", fallos)

if __name__ == "__main__":
    pruebas()
