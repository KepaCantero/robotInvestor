"""QA r01 de T-72 (V0.69): `Diario.estado_diario()` frente a lo que hace de verdad la operación siguiente.

Para cada escenario se toma la foto (tres veces) y después se hace una operación del diario (`barrer`) o un `punto`. Se exige:
  - la foto no cambia nada: ni el Diario (su __dict__ entero), ni el Orquestador, ni el fichero del diario (bytes, inodo, tamaño
    y mtime) ni el del estado; y las tres fotos son iguales;
  - nunca lanza;
  - bloqueo {codigo} ⇒ la operación siguiente da ese código;
  - sin bloqueo y no sincronizado ⇒ la operación siguiente da DI-06 con el mismo motivo;
  - operativo ⇒ la operación siguiente no da DI-05 ni DI-06;
  - el panel es ROJO si y solo si la foto no es operativa (con un tope de líneas holgado).
Escenarios: limpio, cambios por fuera (valor, revertido, NaN, tupla, orden de claves, atributo nuevo o quitado), fichero
reescrito (añadido, otro inodo con los mismos bytes, borrado, mismos bytes en el sitio), punto, reabrir (también con línea a medias
y con una OP sin RES), con clave, dos Diarios sobre los mismos ficheros, DI-01 y bloqueos DI-05/DI-06.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.69/qa/r01_03_estado_diario_oraculo.py
"""
import copy
import hashlib
import os
import sys
import tempfile

M = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(M, "validador"))
sys.path.insert(0, os.path.join(M, "pruebas"))
import diario as di  # noqa: E402
from pruebas_consola_sistema import comp  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

CLAVE = bytes(range(32))   # simulada, sin valor
res = []


def chk(nombre, cond, detalle=""):
    res.append(bool(cond))
    print(("OK      " if cond else "HALLAZGO"), nombre, "" if cond else detalle)


def huella_ficheros(d):
    out = []
    for ruta in (d._ruta_diario, d._ruta_estado):
        try:
            st = os.stat(ruta)
            with open(ruta, "rb") as f:
                out.append((hashlib.sha256(f.read()).hexdigest(), st.st_ino, st.st_size, st.st_mtime_ns))
        except OSError:
            out.append(None)
    return out


def interno(d):
    return copy.deepcopy({k: v for k, v in object.__getattribute__(d, "__dict__").items() if k != "_o"}), copy.deepcopy(vars(d.orquestador))


def crear(tmp, nombre, clave=None):
    os.makedirs(os.path.join(tmp, nombre))
    base = os.path.join(tmp, nombre)
    r = di.crear(nuevo(), os.path.join(base, "estado.json"), os.path.join(base, "diario"), AHORA, clave)
    assert r["ok"], r
    return r["diario"]


def comprobar(nombre, d, op="barrer", esperado=None):
    """Foto, que no cambie nada, y oráculo con la operación siguiente. `esperado`: ('sinc', bool) para fijar el caso."""
    antes_f, antes_i = huella_ficheros(d), interno(d)
    try:
        fotos = [d.estado_diario() for _ in range(3)]
    except Exception as ex:   # noqa: BLE001
        chk(f"{nombre}: la foto no lanza", False, repr(ex))
        return None
    e = fotos[0]
    chk(f"{nombre}: la foto no cambia nada y es estable", huella_ficheros(d) == antes_f and interno(d) == antes_i
        and all(x == e for x in fotos), e)
    nivel = comp(d.orquestador, "diario", diario=d, lineas_diario_ambar=10 ** 6)["nivel"]
    chk(f"{nombre}: panel ROJO si y solo si no operativo", (nivel == "ROJO") == (not e["operativo"]), (nivel, e))
    if esperado is not None:
        chk(f"{nombre}: sincronizado = {esperado}", e["sincronizado"] is esperado, e)
    r = d.barrer(AHORA) if op == "barrer" else d.punto(AHORA)
    if e["bloqueo"] is not None:
        chk(f"{nombre}: bloqueado {e['bloqueo']['codigo']} y la operación da lo mismo", r["codigo"] == e["bloqueo"]["codigo"], (e, r))
    elif not e["sincronizado"]:
        chk(f"{nombre}: desincronizado y la operación da DI-06 con el mismo motivo",
            r["codigo"] == "DI-06" and r["motivo"].startswith(e["motivo_desincronizado"]), (e, r))
    else:
        chk(f"{nombre}: operativo y la operación no da DI-05/DI-06", r.get("codigo") not in ("DI-05", "DI-06"), (e, r))
    return e


with tempfile.TemporaryDirectory() as tmp:
    for clave in (None, CLAVE):
        sfx = " (con clave)" if clave else ""
        d = crear(tmp, "limpio" + sfx, clave)
        comprobar("limpio" + sfx, d, esperado=True)
        comprobar("tras una operación" + sfx, d, esperado=True)
        comprobar("punto" + sfx, d, op="punto", esperado=True)
        comprobar("tras el punto" + sfx, d, esperado=True)

        d = crear(tmp, "valor" + sfx, clave)
        d.orquestador.cotizaciones["EURUSD"] = {"ultima": 1.0}
        comprobar("cambio por fuera" + sfx, d, esperado=False)
        comprobar("ya bloqueado DI-06" + sfx, d)

        d = crear(tmp, "revertido" + sfx, clave)
        d.orquestador.cotizaciones["EURUSD"] = {"ultima": 1.0}
        del d.orquestador.cotizaciones["EURUSD"]
        comprobar("cambio por fuera y revertido" + sfx, d, esperado=True)

    d = crear(tmp, "nan")
    d.orquestador.cotizaciones["EURUSD"] = {"ultima": float("nan")}
    e = comprobar("NaN en el estado", d, esperado=False)

    d = crear(tmp, "tupla")
    k = next(iter(vars(d.orquestador)))
    for nombre_attr, v in vars(d.orquestador).items():
        if isinstance(v, list):
            object.__setattr__(d.orquestador, nombre_attr, tuple(v))
            break
    comprobar(f"una lista convertida en tupla ({nombre_attr})", d, esperado=False)

    d = crear(tmp, "orden")
    o = d.orquestador
    for nombre_attr, v in vars(o).items():
        if isinstance(v, dict) and len(v) >= 2:
            setattr(o, nombre_attr, dict(reversed(list(v.items()))))
            break
    comprobar(f"mismo contenido con otro orden de claves ({nombre_attr})", d, esperado=False)

    d = crear(tmp, "nuevo_attr")
    d.orquestador.algo_nuevo = 1
    comprobar("atributo nuevo en el Orquestador", d, esperado=False)

    d = crear(tmp, "quitar_attr")
    delattr(d.orquestador, "cotizaciones")
    comprobar("atributo quitado del Orquestador", d, esperado=False)

    d = crear(tmp, "append")
    with open(d._ruta_diario, "a") as f:
        f.write("\n")
    comprobar("fichero con una línea añadida por fuera", d, esperado=False)

    d = crear(tmp, "inodo")
    with open(d._ruta_diario, "rb") as f:
        b = f.read()
    with open(d._ruta_diario + ".n", "wb") as f:
        f.write(b)
    os.replace(d._ruta_diario + ".n", d._ruta_diario)
    comprobar("fichero con los mismos bytes en otro inodo", d, esperado=False)

    d = crear(tmp, "borrado")
    os.rename(d._ruta_diario, d._ruta_diario + ".aparte")
    comprobar("fichero del diario quitado", d, esperado=False)

    d = crear(tmp, "insitu")
    with open(d._ruta_diario, "r+b") as f:
        b = f.read()
        f.seek(0)
        f.write(b)
    comprobar("mismos bytes reescritos en el sitio (no se distingue, tampoco la operación)", d, esperado=True)

    # reabrir tras un DI-06: vuelve al estado anotado y sincronizado
    d = crear(tmp, "reabrir")
    assert d.barrer(AHORA)["ok"]
    d.orquestador.cotizaciones["EURUSD"] = {"ultima": 1.0}
    d.barrer(AHORA)
    r = di.abrir(d._ruta_estado, d._ruta_diario)
    chk("reabrir tras DI-06", r["ok"], r)
    comprobar("reabierto", r["diario"], esperado=True)

    # reabrir con una línea a medias al final (se reescribe el fichero: el Diario nuevo debe quedar sincronizado)
    d = crear(tmp, "medias")
    assert d.barrer(AHORA)["ok"]
    with open(d._ruta_diario, "a") as f:
        f.write('{"n": 4, "tipo": "OP"')
    r = di.abrir(d._ruta_estado, d._ruta_diario)
    chk("reabrir con línea a medias", r["ok"] and r["linea_incompleta"], r)
    comprobar("reabierto tras quitar la línea a medias", r["diario"], esperado=True)

    # reabrir con una OP sin su RES al final
    d = crear(tmp, "sinres")
    assert d.barrer(AHORA)["ok"]
    with open(d._ruta_diario, "rb") as f:
        lineas = f.read().split(b"\n")
    with open(d._ruta_diario, "wb") as f:
        f.write(b"\n".join(lineas[:-2]) + b"\n")   # quita el último RES
    r = di.abrir(d._ruta_estado, d._ruta_diario)
    chk("reabrir con una OP sin RES", r["ok"], r)
    comprobar("reabierto tras completar la OP sin RES", r["diario"], esperado=True)

    # dos Diarios sobre los mismos ficheros
    d1 = crear(tmp, "dos")
    d2 = di.abrir(d1._ruta_estado, d1._ruta_diario)["diario"]
    assert d2.barrer(AHORA)["ok"]
    comprobar("el otro Diario escribió en el fichero", d1, esperado=False)
    comprobar("el Diario que escribió", d2, esperado=True)

    # DI-01 no desincroniza
    d = crear(tmp, "di01")
    x = d.barrer((1, 2))
    chk("argumentos que no se guardan dan DI-01", x["codigo"] == "DI-01", x)
    comprobar("tras un DI-01", d, esperado=True)

    # bloqueos simulados de cada clase
    for motivo, cod in (("OSError", "DI-05"), ("operación interrumpida (KeyboardInterrupt)", "DI-05"), (di.FUERA, "DI-06"),
                        (di.ROTOS_DI06[1], "DI-06")):
        d = crear(tmp, "bloq" + cod + str(abs(hash(motivo)) % 1000))
        object.__setattr__(d, "_roto", motivo)
        e = comprobar(f"bloqueado con «{motivo}»", d)
        chk(f"bloqueado con «{motivo}» lleva {cod}", e is not None and e["bloqueo"]["codigo"] == cod and e["operativo"] is False, e)

    # copias y Diario a medio construir
    d = crear(tmp, "copias")
    for etq, c in (("copy.copy", copy.copy(d)), ("copy.deepcopy", copy.deepcopy(d))):
        k = comp(nuevo(), "diario", diario=c)
        chk(f"{etq} del Diario es un Orquestador sin foto: panel ROJO", k["nivel"] == "ROJO", k)
    medio = di.Diario.__new__(di.Diario)
    try:
        medio.estado_diario()
        lanzo = None
    except Exception as ex:   # noqa: BLE001
        lanzo = type(ex).__name__
    print(f"INFO     Diario a medio construir (Diario.__new__): estado_diario() {'lanza ' + lanzo if lanzo else 'no lanza'};",
          "panel:", comp(nuevo(), "diario", diario=medio)["nivel"])

print(f"\n{len(res)} comprobaciones, {res.count(False)} hallazgos")
print("RESULTADO r01_03:", "SIN HALLAZGOS" if all(res) else "HAY HALLAZGOS")
sys.exit(0 if all(res) else 1)
