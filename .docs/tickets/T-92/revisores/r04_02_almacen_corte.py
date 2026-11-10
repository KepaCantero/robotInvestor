"""QA r04 de T-92 (revisor nuevo): el almacén tras un corte real (H-27 y H-29).

Uso: python -I r04_02_almacen_corte.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta).

El corte se simula como lo deja un fallo de corriente: el último registro escrito, sin su sello, truncado en CADA byte
posible (también a mitad de un carácter UTF-8 de varios bytes, que en un almacén en español es lo normal).
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import ARCHIVOS, Almacen

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))
def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))

def ruta(d, a):
    return Path(d) / ARCHIVOS[a]
def abre(d):
    try:
        return Almacen(Path(d)), None
    except Exception as x:
        return None, f"{type(x).__name__}: {str(x)[:90]}"
def sin_confirmar(a):
    return [e for e in a.leer("HA") if "sin confirmar" in str(e.get("detalle"))]

def base_con_corte(d, texto="«España», año, ñandú — información"):
    """Tres registros sellados en F5 y un cuarto escrito sin sello (se restaura el sello previo). Devuelve (prefijo, línea)."""
    a = Almacen(Path(d))
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": texto})
    sellos = (Path(d) / "sellos_integridad.json").read_bytes()
    prefijo = ruta(d, "F5").read_bytes()
    a.escribir("F5", "AG-01", {"id": "cuatro", "nota": texto})
    linea = ruta(d, "F5").read_bytes()[len(prefijo):]
    (Path(d) / "sellos_integridad.json").write_bytes(sellos)
    return prefijo, linea

# ------------------------------------------------------------------------------------------------------------------ 1
print("--- 1. Corte en cada byte del último registro (sin sello)")
with tempfile.TemporaryDirectory() as plantilla:
    prefijo, linea = base_con_corte(plantilla)
    resultados = {"abre_bien": 0, "no_abre": 0, "mal": 0}
    no_abre, mal = [], []
    for k in range(1, len(linea) + 1):     # k = len(linea) es el registro completo con su «\n»
        with tempfile.TemporaryDirectory() as d:
            for p in Path(plantilla).iterdir():
                if p.is_file():
                    shutil.copy2(p, d)
            ruta(d, "F5").write_bytes(prefijo + linea[:k])
            a, err = abre(d)
            if a is None:
                resultados["no_abre"] += 1
                no_abre.append((k, err))
                continue
            ok = (list(a.estado("F5")) == ["uno", "dos", "tres"] and len(sin_confirmar(a)) == 1
                  and ruta(d, "F5").read_bytes() == prefijo)
            a2, err2 = abre(d)
            ok = ok and a2 is not None and len(sin_confirmar(a2)) == 1
            if ok:
                a2.escribir("F5", "AG-01", {"id": "cinco"})
                a3, err3 = abre(d)
                ok = a3 is not None and list(a3.estado("F5")) == ["uno", "dos", "tres", "cinco"]
            resultados["abre_bien" if ok else "mal"] += 1
            if not ok:
                mal.append(k)
    n = len(linea)
    multibyte = sum(1 for k, e in no_abre if "UnicodeDecodeError" in e)
    informe(f"1  corte en los {n} bytes posibles: abre en lo sellado, aparta el resto y anota UNA incidencia en "
            f"{resultados['abre_bien']}/{n}", resultados["abre_bien"] == n,
            f"no abre en {resultados['no_abre']} (UnicodeDecodeError en {multibyte}, p. ej. byte {no_abre[0][0]}: {no_abre[0][1]}); "
            f"mal en {len(mal)}" if no_abre or mal else "")
    informe("1b ningún corte abre con el registro cortado dentro de la cadena", not mal, f"{mal[:5]}")

# ------------------------------------------------------------------------------------------------------------------ 2
print("--- 2. H-27: un solo registro sin sello en todo el almacén")
with tempfile.TemporaryDirectory() as d:
    prefijo, linea = base_con_corte(d)
    a = Almacen(Path(d))
    for k in ("m1", "m2"):
        a.escribir("F6", "AG-20", {"tipo_entrada": "RES", "id": k})
    # F5: línea a medio escribir; F6: un registro completo por encima de su sello (sello de F6 una escritura atrás)
    sellos = json.loads((Path(d) / "sellos_integridad.json").read_text())
    primera = json.loads(ruta(d, "F6").read_text(encoding="utf-8").splitlines()[0])
    sellos["F6"] = [1, primera["_hash"]]
    (Path(d) / "sellos_integridad.json").write_text(json.dumps(sellos))
    ruta(d, "F5").write_bytes(prefijo + linea[:40])
    antes = {p.name: p.read_bytes() for p in Path(d).iterdir() if p.is_file()}
    a, err = abre(d)
    despues = {p.name: p.read_bytes() for p in Path(d).iterdir() if p.is_file()}
    informe("2a línea a medio escribir en F5 y un registro sin sello en F6: falla cerrado sin tocar nada",
            a is None and antes == despues, err or "abrió")
with tempfile.TemporaryDirectory() as d:
    prefijo, linea = base_con_corte(d)
    ruta(d, "F5").write_bytes(prefijo + linea + linea[:30])        # un registro completo sin sello y otro cortado
    a, err = abre(d)
    informe("2b en un mismo fichero, un registro sin sello y otro cortado encima: falla cerrado", a is None, err or "abrió")
with tempfile.TemporaryDirectory() as d:
    prefijo, linea = base_con_corte(d)
    a = Almacen(Path(d))   # aparta el cuarto
    ruta(d, "F6").write_text('{"_seq": 1, "id": "forj', encoding="utf-8")   # basura parcial en un fichero vacío y sellado
    a, err = abre(d)
    informe("2c basura sin salto de línea en un fichero vacío sellado: abre y la aparta, sin entrar en la cadena",
            a is not None and a.leer("F6") == [], err or "")
with tempfile.TemporaryDirectory() as d:
    prefijo, linea = base_con_corte(d)
    ruta(d, "F5").write_bytes(prefijo + linea[:50])
    (ruta(d, "F6")).write_text("no es json\n", encoding="utf-8")
    antes = ruta(d, "F5").read_bytes()
    a, err = abre(d)
    informe("2d validación previa: F5 cortado y F6 manipulado → no abre y F5 no se reescribe",
            a is None and ruta(d, "F5").read_bytes() == antes and not ruta(d, "F5").with_name(ARCHIVOS["F5"] + ".no_confirmado.jsonl").exists(),
            err or "abrió")

# ------------------------------------------------------------------------------------------------------------------ 3
print("--- 3. Instancia viva")
with tempfile.TemporaryDirectory() as d:
    a = Almacen(Path(d))
    for k in ("uno", "dos"):
        a.escribir("F5", "AG-01", {"id": k})
    with open(ruta(d, "F5"), "ab") as fh:
        fh.write(b'{"_seq": 3, "id": "fo')                # otro proceso murió a mitad de su escritura
    vi = a.verificar_integridad("F5")["F5"]
    try:
        a.escribir("F5", "AG-01", {"id": "tres"}); escribe = "escribió"
    except Exception as x:
        escribe = type(x).__name__
    informe("3a la instancia viva no recupera la línea cortada: verificar_integridad False y la escritura se rechaza",
            vi is False and escribe != "escribió", f"verificar={vi}; escribir={escribe}")
    b, err = abre(d)
    informe("3b al reabrir se aparta y se escribe con normalidad", b is not None and list(b.estado("F5")) == ["uno", "dos"], err or "")

# ------------------------------------------------------------------------------------------------------------------ 4
print("--- 4. Muerte real del proceso entre el registro y el sello (os._exit en _guardar_json)")
codigo = r'''
import os, sys
sys.path.insert(0, sys.argv[1])
from bloque_a.almacen import Almacen
a = Almacen(sys.argv[2])
a.escribir("F5", "AG-01", {"id": "uno"})
orig = Almacen._guardar_json
def muere(self, ruta, datos):
    if ruta.name == "sellos_integridad.json":
        os._exit(9)
    return orig(self, ruta, datos)
Almacen._guardar_json = muere
a.escribir("F5", "AG-01", {"id": "dos"})
'''
with tempfile.TemporaryDirectory() as d:
    p = subprocess.run([sys.executable, "-I", "-c", codigo, str(EJ), d], capture_output=True, text=True)
    b, err = abre(d)
    informe("4  tras os._exit antes del sello: abre, F5 = ['uno'] y el «dos» queda apartado con incidencia",
            p.returncode == 9 and b is not None and list(b.estado("F5")) == ["uno"] and len(sin_confirmar(b)) == 1,
            f"exit={p.returncode}; {err or list(b.estado('F5'))}")

# ------------------------------------------------------------------------------------------------------------------ 5
print("--- 5. Almacén anterior a los sellos con la última línea a medio escribir (migración)")
with tempfile.TemporaryDirectory() as d:
    prefijo, linea = base_con_corte(d)
    (Path(d) / "sellos_integridad.json").unlink()
    (Path(d) / "formato_almacen.json").unlink()
    ruta(d, "F5").write_bytes(prefijo + linea[:40])
    a, err = abre(d)
    if a is None:
        informe("5  almacén anterior con línea cortada: no abre (falla cerrado)", True, err)
    else:
        sellado = json.loads((Path(d) / "sellos_integridad.json").read_text())["F5"][0]
        try:
            a.escribir("F5", "AG-01", {"id": "nuevo"}); w = "escribió"
        except Exception as x:
            w = f"{type(x).__name__}: {x}"
        b, err2 = abre(d)
        conserva = b is not None and "nuevo" in b.estado("F5")
        informe("5  almacén anterior con línea cortada: abre, y el registro escrito después sigue en la cadena al reabrir",
                conserva, f"abre=sí, sello F5={sellado}, apartado={ruta(d, 'F5').with_name(ARCHIVOS['F5'] + '.no_confirmado.jsonl').exists()}; "
                f"escribir: {w}; reabrir: {err2 or list(b.estado('F5'))}")
print("fallos:", fallos)
