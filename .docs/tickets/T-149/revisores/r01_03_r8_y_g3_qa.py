"""QA r01 de T-149 (revisor) · errores de la cadena B sin datos de R8 y sin encargos con G3 BLOQUEADO.

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-149/revisores/r01_03_r8_y_g3_qa.py <carpeta temporal>
Sin red ni coste: los ejecutores se simulan (`_cli` y `subprocess.run` del script) con el paquete de ejemplo del Bloque A.
Partes:
  R. `sin_datos_protegidos` con cada dato en varias posiciones y mezclado con otros; los mensajes de `jsonschema` con el
     dato junto al corte de 200 caracteres; un `opp_id` con un correo en un paquete manipulado; el mensaje de un ejecutor
     que falla, recortado antes de limpiarlo; una configuración YAML rota con un correo;
  G. el script y la librería con cada combinación de entrega, G3 del ciclo y `estado_g3` del paquete.
Los datos de prueba van partidos en dos cadenas y son de dominios de ejemplo. Termina con 1 si hay algún hallazgo; lo que
es un límite declarado (INC-T123-01) o queda fuera del ticket se imprime como OBS."""
import contextlib
import copy
import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
from bloque_a.configuracion import cargar_config, fusionar  # noqa: E402

from bloque_a import cadena_b  # noqa: E402
from bloque_a.contratos import contiene_credenciales, secretos_en_texto  # noqa: E402

TMP = Path(sys.argv[1]).resolve()
TMP.mkdir(parents=True, exist_ok=True)
EJEMPLO = json.loads((EJ.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json").read_text(encoding="utf-8"))
OPP = "OPP-2026-9112"
CORREO = "inversor.prueba" + "@example.com"
CLAVE = "api" + "_key=ABCDEF1234567890"
IBAN = "ES91 2100 0418 " + "4502 0005 1332"
SK = "sk-" + "ant-api03-" + "Q" * 30 + "x9Z"
PWD = '"pass' + 'word": "Hunter2-Secreto"'
DATOS = {"correo": (CORREO, "inversor.prueba"), "clave": (CLAVE, "ABCDEF1234567890"), "iban": (IBAN, "0418 4502 0005 1332"),
         "sk": (SK, "Q" * 20), "password JSON": (PWD, "Hunter2-Secreto")}
CFG = fusionar(cargar_config(), {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}})
hallazgos = 0


def caso(nombre, ok, detalle="", obs=False):
    global hallazgos
    hallazgos += (not ok) and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def limpio(texto, nucleo):
    """Ni el detector ve nada ni queda el núcleo del dato (la parte local del correo, el valor de la clave…)."""
    return not secretos_en_texto(texto) and not contiene_credenciales(texto) and nucleo not in texto


# ---------------------------------------------------------------- R1. sin_datos_protegidos, posiciones y mezclas
fallos, no_vistos = [], []
for nombre, (dato, nucleo) in DATOS.items():
    for plantilla in ("{d}", "x{d}", "'{d}' is not one of ['RV']", "a/b: {{'k': '{d}'}} is not of type 'string'",
                      "linea\\n{d}", "{d}; {d}", "«{d}»", "(" + "z" * 180 + " {d})", "{d}\n" * 3):
        t = plantilla.format(d=dato)
        r = cadena_b.sin_datos_protegidos(t)
        if not secretos_en_texto(t):   # el detector no lo ve ni en el original: límite del detector (INC-T123-01)
            no_vistos.append(f"{nombre} en {plantilla[:12]!r}")
        elif not limpio(r, nucleo):
            fallos.append(f"{nombre} en {plantilla[:20]!r}: {r[:60]!r}")
for (n1, (d1, k1)), (n2, (d2, k2)) in ((a, b) for a in DATOS.items() for b in DATOS.items() if a[0] < b[0]):
    r = cadena_b.sin_datos_protegidos(f"{d1} {d2} y {d2}{d1}")
    if not (limpio(r, k1) and limpio(r, k2)):
        fallos.append(f"{n1}+{n2}: {r[:60]!r}")
caso("R1 sin_datos_protegidos: cada dato en 9 posiciones y por pares, sin rastro (dos datos pegados: el primero reemplazado se come el principio del segundo, y su cola ya no se reconoce)", not fallos, "; ".join(fallos[:3]))
caso("R1 lo que el detector no ve tampoco se quita (pegado a una letra: «x» + dato)", not no_vistos, "; ".join(no_vistos), obs=True)

# ---------------------------------------------------------------- R2. jsonschema: el dato junto al corte de 200
fallos = []
for relleno in range(120, 210, 3):
    p = copy.deepcopy(EJEMPLO)
    e = next(x for x in p["paquete_para_bloque_B"] if x["opp_id"] == OPP)
    e["tipo_activo"] = "Z" * relleno + " " + CORREO
    try:
        cadena_b.construir_peticion(p, OPP, CFG)
        fallos.append(f"{relleno}: se construyó")
    except cadena_b.ErrorCadenaB as err:
        if not limpio(str(err), "inversor.prueba") or "prueba@" in str(err) or "@example" in str(err):
            fallos.append(f"{relleno}: {str(err)[-60:]!r}")
caso("R2 el correo junto al corte de 200 de un mensaje de jsonschema no deja su parte local", not fallos, "; ".join(fallos[:2]))


def modulo_script():
    spec = importlib.util.spec_from_file_location("cadena_a_b_qa", RAIZ / ".docs" / "scripts" / "cadena_a_b.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ejecutar(mod, args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            codigo = mod.main(args)
        except Exception as e:   # noqa: BLE001  (una traza también es una salida)
            codigo = f"excepción {type(e).__name__}"
            print(f"{type(e).__name__}: {e}", file=err)
    return codigo, out.getvalue(), err.getvalue()


def cli_falso(paquete_json, ciclo, llamadas):
    def cli(bloque, args):
        llamadas.append((bloque, args[-1] if bloque == "a" else args[args.index("analizar") if "analizar" in args else -1]))
        if bloque == "a" and args[-1] == "ciclo":
            return {"run_id": EJEMPLO["run_id"], **ciclo, "entregables": ciclo.get("entregables", {"paquete_json": str(paquete_json)})}
        if bloque == "b":
            return {"pet_id": "PET-2026-0001", "estado_peticion": "ENTREGADA", "acuse_inmediato": {"pet_id": "PET-2026-0001",
                    "admision": "ADMITIDA"}, "entregables": {}, "resumen": {"veredicto": "X"}}
        if bloque == "a" and "decision" in args:
            return {"ret_id": "RET-2026-0001", "estado": "REGISTRADA"}
        raise AssertionError(f"llamada inesperada {bloque} {args[-3:]}")
    return cli


EXTRA = TMP / "extra.yaml"
EXTRA.write_text(json.dumps({"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}}), encoding="utf-8")

# ---------------------------------------------------------------- R3. un opp_id con un correo (paquete manipulado)
mod = modulo_script()
p = copy.deepcopy(EJEMPLO)
for o in (o for c in p["clases"].values() for o in c["opciones"]):
    if o["opp_id"] == OPP:
        o["opp_id"] = CORREO
for e in p["paquete_para_bloque_B"]:
    if e["opp_id"] == OPP:
        e["opp_id"] = CORREO
ruta = TMP / "r3_paquete.json"
ruta.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
mod._cli = cli_falso(ruta, {"entrega": "ENTREGADA", "g3": "APTO"}, [])
w = TMP / "r3"
codigo, out, err = ejecutar(mod, ["--trabajo", str(w), "--config-a", str(EXTRA)])
resumen = (w / "resumen.json").read_text(encoding="utf-8") if (w / "resumen.json").exists() else ""
caso("R3 un opp_id con un correo no llega a resumen.json ni a la salida", all("inversor.prueba" not in t for t in (resumen, out, err)),
     f"código {codigo}; en resumen.json: {'inversor.prueba' in resumen}, en la salida: {'inversor.prueba' in out + err} "
     "(solo con un paquete que no cumple el esquema de A, `^OPP-…`: G3 lo bloquearía)", obs=False)

# ---------------------------------------------------------------- R4. el fallo de un ejecutor, recortado antes de limpiar
mod = modulo_script()
fallos = []
for nombre, (dato, nucleo) in DATOS.items():
    for corte in range(2, len(dato) - 3, 3):          # el recorte de 2000 cae dentro del dato
        cola = dato[corte:]
        # el dato entero en el stderr; `_cli` se queda con los 2000 últimos caracteres, que empiezan en `cola`
        stderr = "inicio " + dato + " " + "y" * (2000 - len(cola) - 1)
        mod.subprocess = SimpleNamespace(run=lambda *a, _s=stderr, **k: SimpleNamespace(returncode=3, stdout="", stderr=_s))
        codigo, out, err = ejecutar(mod, ["--trabajo", str(TMP / "r4"), "--config-a", str(EXTRA)])
        nuc = nucleo[-8:]
        if nuc in err and nuc in cola and nucleo not in err:   # un trozo del dato, sin el dato entero
            fallos.append(f"{nombre} cortado en {corte}: queda {cola[:24]!r}")
            break
caso("R4 el stderr de un ejecutor que falla, recortado a 2000 antes de limpiarlo, no deja un trozo del dato",
     not fallos, "; ".join(fallos[:5]), obs=False)

# ---------------------------------------------------------------- R5. configuración YAML rota con un correo
mod = modulo_script()
roto = TMP / "roto.yaml"
roto.write_text("cadena_b:\n  peticion: {nivel: " + CORREO + "\n  otra: [\n", encoding="utf-8")
r = subprocess.run([sys.executable, "-I", str(RAIZ / ".docs" / "scripts" / "cadena_a_b.py"), "--trabajo", str(TMP / "r5"),
                    "--config-a", str(roto)], capture_output=True, text=True, check=False, cwd=RAIZ)
caso("R5 una configuración YAML rota no imprime el correo que lleva", "inversor.prueba" not in r.stdout + r.stderr,
     f"código {r.returncode}; traza: {'Traceback' in r.stderr} (fuera de T-149: lo imprime `yaml` antes de `cadena_b`)", obs=True)

# ---------------------------------------------------------------- G. G3: script y librería
for estado in (None, "BLOQUEADO", "SIN_RESULTADO", "APTO ", "apto", ["APTO"], {"APTO": 1}, 1, True):
    p = copy.deepcopy(EJEMPLO)
    if estado is None:
        p.pop("estado_g3", None)
    else:
        p["estado_g3"] = estado
    try:
        cadena_b.construir_peticion(p, OPP, CFG)
        caso(f"G1 librería con estado_g3={estado!r}: no sale la petición", False, "salió")
    except cadena_b.ErrorCadenaB as e:
        caso(f"G1 librería con estado_g3={estado!r}: no sale la petición", e.codigo == "ENTREGA_BLOQUEADA_G3", e.codigo)
    except Exception as e:   # noqa: BLE001
        caso(f"G1 librería con estado_g3={estado!r}: no sale la petición", False, f"traza {type(e).__name__}")
# el G3 se mira antes que el resto: un paquete bloqueado con otros errores da ENTREGA_BLOQUEADA_G3, no otro código
p = copy.deepcopy(EJEMPLO)
p.pop("estado_g3", None)
next(x for x in p["paquete_para_bloque_B"] if x["opp_id"] == OPP)["tipo_activo"] = "XX"
try:
    cadena_b.construir_peticion(p, "OPP-0000-0000", CFG)
except cadena_b.ErrorCadenaB as e:
    caso("G1 un paquete bloqueado con otros errores: el código es el de G3", e.codigo == "ENTREGA_BLOQUEADA_G3", e.codigo)

ESCENARIOS = [   # (nombre, ciclo, estado_g3 del paquete en disco, se espera envío)
    ("ENTREGADA · APTO · APTO", {"entrega": "ENTREGADA", "g3": "APTO"}, "APTO", True),
    ("ENTREGADA · APTO_CON_ADVERTENCIAS · ídem", {"entrega": "ENTREGADA", "g3": "APTO_CON_ADVERTENCIAS"}, "APTO_CON_ADVERTENCIAS", True),
    ("ENTREGADA · BLOQUEADO · APTO", {"entrega": "ENTREGADA", "g3": "BLOQUEADO"}, "APTO", False),
    ("BLOQUEADA · APTO (el G3 de F6) · sin estado", {"entrega": "BLOQUEADA", "g3": "APTO"}, None, False),
    ("BLOQUEADA · APTO · APTO (paquete manipulado)", {"entrega": "BLOQUEADA", "g3": "APTO"}, "APTO", False),
    ("ENTREGADA · APTO · sin estado en el paquete", {"entrega": "ENTREGADA", "g3": "APTO"}, None, False),
    ("ENTREGADA · APTO · BLOQUEADO en el paquete", {"entrega": "ENTREGADA", "g3": "APTO"}, "BLOQUEADO", False),
    ("sin «entrega» · APTO · APTO", {"g3": "APTO"}, "APTO", False),
    ("ENTREGADA · sin «g3» · APTO", {"entrega": "ENTREGADA"}, "APTO", False),
    ("ENTREGADA · APTO · sin entregables", {"entrega": "ENTREGADA", "g3": "APTO", "entregables": None}, "APTO", False),
    ("ENTREGADA · APTO · paquete_json inexistente", {"entrega": "ENTREGADA", "g3": "APTO",
                                                     "entregables": {"paquete_json": str(TMP / "no_existe.json")}}, "APTO", False),
]
for i, (nombre, ciclo, estado, envia) in enumerate(ESCENARIOS):
    mod = modulo_script()
    p = copy.deepcopy(EJEMPLO)
    p.pop("estado_g3", None)
    if estado is not None:
        p["estado_g3"] = estado
    ruta = TMP / f"g2_{i}.json"
    ruta.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
    llamadas: list = []
    mod._cli = cli_falso(ruta, ciclo, llamadas)
    w = TMP / f"g2_{i}"
    codigo, out, err = ejecutar(mod, ["--trabajo", str(w), "--config-a", str(EXTRA), "--sonda-sin-correspondencia"])
    al_b = [x for x in llamadas if x[0] == "b"]
    pets = list((w / "peticiones").glob("*.json")) if (w / "peticiones").exists() else []
    if envia:   # el B simulado no da paquete: el código es 1 (no hay entregas válidas), pero la petición sale
        ok = bool(al_b and pets)
    else:
        ok = not al_b and not pets and (codigo in (1, 2) or isinstance(codigo, str)) and not (w / "sonda").exists()
    traza = isinstance(codigo, str)
    caso(f"G2 script {nombre}: {'envía' if envia else 'no envía nada'}" + (" (y sin traza)" if not envia else ""), ok and not traza,
         f"código {codigo}, llamadas al B {len(al_b)}, peticiones {len(pets)}"
         + (f", traza {err.strip().splitlines()[-1][:60]}" if traza else ""), obs=ok and traza)   # falla cerrado, con traza

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
