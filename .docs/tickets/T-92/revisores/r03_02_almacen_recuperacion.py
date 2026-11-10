"""QA r03 de T-92 (revisor nuevo): ataques a la recuperación de escrituras no confirmadas de `almacen.py` (H-19 a H-21).

Uso: python -I r03_02_almacen_recuperacion.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta). Preguntas: ¿se puede perder un registro confirmado, aceptar uno manipulado o
dejar el almacén sin abrir? Las muertes del proceso son reales (`os._exit` en otro proceso).
"""
import json, multiprocessing as mp, os, sys, tempfile
from pathlib import Path
from unittest.mock import patch
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

F5 = "F5_historial_analisis.jsonl"
def f5(t): return Path(t) / F5
def aparte(t): return f5(t).with_name(F5 + ".no_confirmado.jsonl")
def ids(a): return list(a.estado("F5"))
def n_inc(a): return sum("sin confirmar" in str(e.get("detalle")) for e in a.leer("HA"))

# ---- procesos hijos (spawn) ----
def _muere_tras_el_sello(carpeta):
    a = Almacen(Path(carpeta)); a.escribir("F5", "AG-01", {"id": "uno"})
    original = Almacen._guardar_json
    def guarda_y_muere(ruta, datos):
        original(ruta, datos)
        if ruta.name == "sellos_integridad.json":
            os._exit(9)
    Almacen._guardar_json = staticmethod(guarda_y_muere)
    a.escribir("F5", "AG-01", {"id": "dos"})

def _muere_antes_del_sello(carpeta):
    a = Almacen(Path(carpeta)); a.escribir("F5", "AG-01", {"id": "uno"})
    Almacen._guardar_json = staticmethod(lambda ruta, datos: os._exit(9))
    a.escribir("F5", "AG-01", {"id": "dos"})

def _muere_al_apartar(carpeta, punto):
    """Abre un almacén con un registro sin confirmar y muere a mitad de la recuperación."""
    import bloque_a.almacen as m
    if punto == "tras_aparte":       # escrito el *.no_confirmado.jsonl, sin reescribir aún el original
        real = Path.replace
        def replace(self, destino):
            if Path(destino).name == F5:
                os._exit(9)
            return real(self, destino)
        Path.replace = replace
    else:                            # reescrito el original, antes de anotar la incidencia en HA
        m.Almacen.incidencia = lambda self, *a, **k: os._exit(9)
    Almacen(Path(carpeta))

def _escritor(carpeta, n):
    a = Almacen(Path(carpeta))
    for i in range(n):
        a.escribir("F5", "AG-01", {"id": f"w{i}"})

def _abridor(carpeta, n):
    for _ in range(n):
        Almacen(Path(carpeta)).leer("F5")

def hijo(target, *args):
    p = mp.get_context("spawn").Process(target=target, args=args); p.start(); p.join(); return p.exitcode

def pruebas():
    # 1. Muerte real tras guardar el sello (H-21 con un proceso real): el registro está confirmado y se conserva
    with tempfile.TemporaryDirectory() as d:
        ex = hijo(_muere_tras_el_sello, d)
        a, err = abre(Path(d))
        informe("1  muerte tras guardar el sello: abre y conserva el registro confirmado", a is not None and ids(a) == ["uno", "dos"]
                and not aparte(d).exists(), f"exit={ex}; {err or ids(a)}")

    # 2. Muerte antes del sello, y reabrir dos veces: una sola recuperación y una sola incidencia (idempotente)
    with tempfile.TemporaryDirectory() as d:
        hijo(_muere_antes_del_sello, d)
        a1, e1 = abre(Path(d)); a2, e2 = abre(Path(d))
        ok = a1 and a2 and ids(a2) == ["uno"] and n_inc(a2) == 1 and len(aparte(d).read_text().splitlines()) == 1
        informe("2  muerte antes del sello: recupera una vez; reabrir no repite ni duplica", bool(ok),
                e1 or e2 or f"F5={ids(a2)}; incidencias={n_inc(a2)}; apartados={len(aparte(d).read_text().splitlines())}")
        # y el almacén sigue siendo escribible
        a2.escribir("F5", "AG-01", {"id": "tres"})
        a3, e3 = abre(Path(d))
        informe("2b tras recuperar se escribe y reabre con normalidad", a3 is not None and ids(a3) == ["uno", "tres"], e3 or ids(a3))

    # 3. Muerte a mitad de la recuperación (dos puntos): ¿abre después?, ¿se pierde algo?, ¿queda rastro en HA?
    for punto in ("tras_aparte", "antes_de_la_incidencia"):
        with tempfile.TemporaryDirectory() as d:
            hijo(_muere_antes_del_sello, d)
            ex = hijo(_muere_al_apartar, d, punto)
            a, err = abre(Path(d))
            lineas = aparte(d).read_text().splitlines() if aparte(d).exists() else []
            ok = a is not None and ids(a) == ["uno"] and lineas and {json.loads(x)["id"] for x in lineas} == {"dos"}
            informe(f"3  muerte durante la recuperación ({punto}): abre en lo sellado y el registro sigue apartado",
                    bool(ok), err or f"exit={ex}; F5={ids(a)}; apartados={len(lineas)}")
            if a is not None:
                print(f"INFO  3b ({punto}): incidencias «sin confirmar» en HA = {n_inc(a)}; líneas en el apartado = {len(lineas)}")

    # 4. Línea final a medio escribir (corte de corriente o disco lleno a mitad de write): ¿abre?
    with tempfile.TemporaryDirectory() as d:
        a = Almacen(Path(d)); a.escribir("F5", "AG-01", {"id": "uno"}); del a
        with open(f5(d), "ab") as fh:
            fh.write(b'{"id": "dos", "_seq": 2, "_fec')
        a, err = abre(Path(d))
        print(f"INFO  4  línea final a medio escribir por encima del sello: abre={a is not None} ({err})")

    # 5. Un registro forjado (cadena bien calculada) por encima del sello: no entra en la cadena
    with tempfile.TemporaryDirectory() as d:
        a = Almacen(Path(d)); a.escribir("F5", "AG-01", {"id": "uno"})
        ult = json.loads(f5(d).read_text().splitlines()[-1])
        e = {"id": "forjado", "_seq": 2, "_fecha": ult["_fecha"], "_ts": ult["_ts"], "_autor": "AG-01", "_hash_prev": ult["_hash"]}
        e["_hash"] = _hash(e["_hash_prev"], {k: v for k, v in e.items() if k != "_hash"})
        with open(f5(d), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(e) + "\n")
        informe("5a instancia viva: el forjado no se lee y la escritura siguiente se rechaza",
                a.verificar_integridad("F5") == {"F5": False}, "")
        try:
            a.escribir("F5", "AG-01", {"id": "otro"}); informe("5b instancia viva rechaza escribir", False)
        except ValueError:
            informe("5b instancia viva rechaza escribir", True)
        a2, err = abre(Path(d))
        informe("5c al reabrir, el forjado se aparta (no se acepta) y queda incidencia", a2 is not None and ids(a2) == ["uno"]
                and n_inc(a2) == 1, err or ids(a2))

    # 6. Sello restaurado de una copia de UNA escritura atrás: indistinguible de una muerte → el último registro
    #    CONFIRMADO sale de la cadena (queda en el apartado con una incidencia «Operativa»)
    with tempfile.TemporaryDirectory() as d:
        a = Almacen(Path(d)); a.escribir("F5", "AG-01", {"id": "uno"})
        copia = (Path(d) / "sellos_integridad.json").read_text()
        a.escribir("F5", "AG-01", {"id": "dos-confirmado"}); del a
        (Path(d) / "sellos_integridad.json").write_text(copia)
        a2, err = abre(Path(d))
        sev = [e.get("severidad") for e in a2.leer("HA") if "sin confirmar" in str(e.get("detalle"))] if a2 else []
        print(f"INFO  6  sello viejo por una escritura: F5={ids(a2) if a2 else err}; severidad={sev} (límite: sin marca de "
              f"intención no se distingue de una muerte del proceso; no figura en «Límites» de analisis-tecnico.md)")

    # 7. Ctrl-C en cada punto de `escribir` en el mismo proceso: el almacén siempre abre y nada confirmado se pierde
    puntos = {"fsync del registro": ("os.fsync", 1), "guardar sello (antes de replace)": ("json.dump", 1),
              "replace del sello": ("replace", 1), "tras el sello (unlink)": ("unlink", 1)}
    for nombre, (que, _) in puntos.items():
        with tempfile.TemporaryDirectory() as d:
            t = Path(d); a = Almacen(t); a.escribir("F5", "AG-01", {"id": "uno"})
            import bloque_a.almacen as m
            if que == "os.fsync":
                ctx = patch.object(m.os, "fsync", side_effect=KeyboardInterrupt)
            elif que == "json.dump":
                ctx = patch.object(m.json, "dump", side_effect=KeyboardInterrupt)
            elif que == "replace":
                ctx = patch.object(Path, "replace", side_effect=KeyboardInterrupt)
            else:
                real = Path.unlink
                def unlink(self, missing_ok=False):
                    if self.parent == t and not self.exists():
                        raise KeyboardInterrupt
                    return real(self, missing_ok=missing_ok)
                ctx = patch.object(Path, "unlink", unlink)
            with ctx:
                try:
                    a.escribir("F5", "AG-01", {"id": "dos"})
                except KeyboardInterrupt:
                    pass
            sello = json.loads((t / "sellos_integridad.json").read_text())["F5"][0]
            viva = ids(a)
            a2, err = abre(t)
            ok = a2 is not None and ids(a2) == viva and len(viva) == sello
            informe(f"7  Ctrl-C en «{nombre}»: abre, la instancia viva y el disco coinciden con el sello", ok,
                    err or f"viva={viva}; disco={ids(a2)}; sello={sello}")
            if a2 is not None:
                a2.escribir("F5", "AG-01", {"id": "tres"})

    # 8. Concurrencia: un proceso escribe mientras otro abre una y otra vez → ninguna recuperación falsa
    with tempfile.TemporaryDirectory() as d:
        Almacen(Path(d))
        ctx = mp.get_context("spawn")
        ps = [ctx.Process(target=_escritor, args=(d, 150)), ctx.Process(target=_abridor, args=(d, 60))]
        [p.start() for p in ps]; [p.join() for p in ps]
        a, err = abre(Path(d))
        informe("8  escribir y abrir a la vez desde dos procesos: sin apartados y con los 150 registros",
                a is not None and len(ids(a)) == 150 and not aparte(d).exists() and n_inc(a) == 0,
                err or f"{len(ids(a))} registros; apartado={aparte(d).exists()}; exit={[p.exitcode for p in ps]}")

    # 9. Dos ficheros con un registro sin sello cada uno (no lo produce una sola escritura): ¿se aceptan dos recuperaciones?
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); a = Almacen(t); a.escribir("F5", "AG-01", {"id": "uno"}); a.escribir("F6", "AG-20", {"id": "m1"})
        copia = (t / "sellos_integridad.json").read_text()
        a.escribir("F5", "AG-01", {"id": "dos"}); a.escribir("F6", "AG-20", {"id": "m2"}); del a
        (t / "sellos_integridad.json").write_text(copia)
        a2, err = abre(t)
        print(f"INFO  9  dos ficheros con un registro sin sello cada uno (dos escrituras confirmadas): abre={a2 is not None}; "
              f"{err or f'F5={ids(a2)}, F6={list(a2.estado(chr(70) + chr(54)))}'}")
    print("fallos:", fallos)

if __name__ == "__main__":
    pruebas()
