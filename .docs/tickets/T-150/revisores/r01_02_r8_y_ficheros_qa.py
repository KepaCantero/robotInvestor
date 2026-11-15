"""QA r01 de T-150 (revisor) · R8 en `sin_datos_protegidos` (H-01), en `cadena_a_b.py` (H-02, H-04) y los ficheros que no
se leen (O-04, O-06).

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-150/revisores/r01_02_r8_y_ficheros_qa.py <carpeta temporal>
Sin red ni coste: los ejecutores se simulan (`_cli` y `subprocess.run` del script). Partes:
  T. `sin_datos_protegidos` con dos y tres datos pegados por 14 uniones distintas, con y sin copia suelta: ningún dato
     que el detector ve (en el texto con el dato o suelto) deja su núcleo; lo que el detector solo ve en parte (pegado a
     una letra, O-03 / INC-T123-01) es OBS;
  S. `_cli`: el dato en cada posición alrededor del corte de 2000 (stderr) y de 1000 (stdout que no es JSON), medido
     sobre el texto ya limpio;
  R. `resumen.json` y la salida con datos en los campos que devuelve el ciclo (`run_id`, `estado`, `entrega`, `g3`,
     `top3_por_clase`) y en el `opp_id`, por las tres salidas (sin entrega, entrega normal, fallo de un ejecutor);
  C. `--config-a` que no se lee (no existe, carpeta, YAML roto de cuatro formas, UTF-8 inválido, no es un diccionario,
     `cadena_b` o su correspondencia que no lo son, valores de la correspondencia que no son textos);
  P. `paquete_json` que no se lee (no existe, carpeta, vacío, no es JSON, UTF-8 inválido, lista, texto con un correo) y
     uno que se lee pero no tiene la forma (fuera de O-04: OBS).
Los datos de prueba van partidos en dos cadenas. Termina con 1 si hay algún hallazgo."""
import contextlib
import copy
import importlib.util
import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
from bloque_a import cadena_b  # noqa: E402
from bloque_a.contratos import contiene_credenciales, secretos_en_texto  # noqa: E402

TMP = Path(sys.argv[1]).resolve()
TMP.mkdir(parents=True, exist_ok=True)
EJEMPLO = json.loads((EJ.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json").read_text(encoding="utf-8"))
OPP = "OPP-2026-9112"
CORREO = "cuenta.falsa" + "@example.org"
DATOS = {   # nombre: (dato, núcleo que no puede quedar)
    "correo": (CORREO, "cuenta.falsa"),
    "api_key": ("api" + "_key=ZXCV98765432QWER", "ZXCV98765432QWER"),
    "token": ("tok" + "en: Abc123Def456Ghi789", "Abc123Def456Ghi789"),
    "password=": ("pass" + "word=Lavanda-77x", "Lavanda-77x"),
    "password JSON": ('"pass' + 'word": "Gato-Negro-55"', "Gato-Negro-55"),
    "iban": ("ES76 2077 0024 " + "0031 0257 5766", "0024 0031 0257 5766"),
    "sk": ("sk-" + "ant-api03-" + "W" * 30 + "k3J", "W" * 20),
    "akia": ("AKIA" + "QWERTYUIOPASDFGH", "QWERTYUIOPASDFGH"),
    "bearer": ("Bear" + "er abcdefghijKLMNOP0123456789", "abcdefghijKLMNOP0123456789"),
    "dni": ("1234" + "5678Z", "12345678Z"),
}
UNIONES = ["", " ", "x", "_", "=", ":", "\\n", "\n", '"', "'", ",", "@", ".", "-"]
hallazgos = 0


def caso(nombre, ok, detalle="", obs=False):
    global hallazgos
    hallazgos += (not ok) and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def visto(dato, texto):
    """El detector da el dato tal cual (una de sus coincidencias es el dato entero). Si solo lo da dentro de una
    coincidencia más larga (pegado a otro: «…valor» + «token: …») o no lo da, lo que queda es el límite O-03."""
    return DATOS[dato][0] in secretos_en_texto(texto)


# ---------------------------------------------------------------- T. tramos
fallos, parciales, total = [], set(), 0
nombres = list(DATOS)
for i, n1 in enumerate(nombres):
    for n2 in nombres:
        if n1 == n2:
            continue
        for u in UNIONES:
            for suelto in (False, True):
                (d1, k1), (d2, k2) = DATOS[n1], DATOS[n2]
                texto = f"error: {d1}{u}{d2} fin" + (f" · {d1} · {d2}" if suelto else "")
                for n3 in ([None] if (i + len(u)) % 3 else [nombres[(i + 3) % len(nombres)]]):
                    if n3 and n3 not in (n1, n2):
                        texto += f"{u}{DATOS[n3][0]}"
                total += 1
                r = cadena_b.sin_datos_protegidos(texto)
                if r == cadena_b.DETALLE_OMITIDO:
                    continue
                if secretos_en_texto(r) or contiene_credenciales(r):
                    fallos.append(f"el detector ve algo en lo limpio: {r[:60]!r}")
                for n, (d, k) in DATOS.items():
                    if k in r and d in texto:
                        # ¿lo veía el detector? en el texto (entero) o, si no, es el límite de lo pegado (O-03)
                        if visto(n, texto):
                            fallos.append(f"{n} en {texto[:50]!r} → {r[:70]!r}")
                        else:
                            parciales.add(f"{n} tras {n1}+{u!r}" if n == n2 else n)
caso(f"T sin_datos_protegidos: ningún dato que el detector ve deja su núcleo ({total} textos)", not fallos, "; ".join(fallos[:3]))
caso("T lo que el detector no ve entero (pegado a una letra o una cifra) queda (O-03, INC-T123-01, fuera de T-150)",
     not parciales, f"{len(parciales)} combinaciones, p. ej. " + "; ".join(sorted(parciales)[:6]), obs=True)
# un dato dentro de otro que acaba antes (un correo dentro del valor de una contraseña): la unión no se acorta (el mutante
# Y01 de `r01_04_mutantes_qa.py`, que ninguna prueba de T-150 mata, deja «/ZZZZ1234567»)
dentro = "error: pass" + "word=x/" + CORREO + "/ZZZZ1234567 fin"
r = cadena_b.sin_datos_protegidos(dentro)
caso("T un dato contenido en otro que acaba después: la unión llega al final del más largo", "ZZZZ1234567" not in r
     and "cuenta.falsa" not in r, repr(r))
# el caso de la QA de T-149 sin la copia suelta: el correo se come «api» y la clave no se ve entera (O-03)
r = cadena_b.sin_datos_protegidos(CORREO + DATOS["api_key"][0])
caso("T el correo pegado a «api_key=…» sin copia suelta: el valor de la clave queda (O-03: el detector no ve la clave)",
     DATOS["api_key"][1] not in r, repr(r), obs=True)


# ---------------------------------------------------------------- utilidades del script
def modulo_script():
    spec = importlib.util.spec_from_file_location("cadena_a_b_qa150", RAIZ / ".docs" / "scripts" / "cadena_a_b.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ejecutar(mod, args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            codigo = mod.main(args)
        except BaseException as e:   # noqa: BLE001  (una traza también es una salida)
            codigo = f"excepción {type(e).__name__}"
            print(f"Traceback {type(e).__name__}: {e}", file=err)
    return codigo, out.getvalue(), err.getvalue()


def sin_nucleos(*textos):
    return [n for n, (_, k) in DATOS.items() for t in textos if k in t or k[-10:] in t]


EXTRA = TMP / "extra.yaml"
EXTRA.write_text(json.dumps({"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}}), encoding="utf-8")

# ---------------------------------------------------------------- S. limpiar y recortar en `_cli`
mod = modulo_script()
fallos = []
for canal, corte in (("stderr", 2000), ("stdout", 1000)):
    for n, (d, k) in DATOS.items():
        for detras in range(corte - 60, corte + 60):
            # `detras` caracteres después del dato (separado por un espacio): el corte cae antes, dentro o después del dato
            # en el texto crudo; en el limpio, el dato es «dato protegido por R8» y el corte cae en él o en el relleno
            texto = "inicio " + d + " " + "y" * (detras - 1)
            antes = detras
            sal = SimpleNamespace(returncode=3 if canal == "stderr" else 0, stdout=texto if canal == "stdout" else "",
                                  stderr=texto if canal == "stderr" else "")
            mod.subprocess = SimpleNamespace(run=lambda *a, _s=sal, **kw: _s)
            try:
                mod._cli("a", ["ciclo"])
                fallos.append(f"{canal} {n}: no falló")
            except mod.FalloEjecutor as e:
                if sin_nucleos(str(e)) or secretos_en_texto(str(e)):
                    fallos.append(f"{canal} {n} a {antes}: {str(e)[-40:]!r}")
caso("S el error de un ejecutor (stderr a 2000, stdout a 1000) no deja trozos de ningún dato en ninguna posición del corte",
     not fallos, "; ".join(fallos[:3]))
# texto grande: lo limpia entero (antes, solo 2000): el coste es lineal en el tamaño, salvo muchos datos distintos
import time  # noqa: E402

grande = ("linea de registro sin datos\n" * 40000)
t0 = time.time()
cadena_b.sin_datos_protegidos(grande)
t1 = time.time() - t0
muchos = " ".join(f"u{i}" + "@exam" + "ple.org" for i in range(20000))
t0 = time.time()
cadena_b.sin_datos_protegidos(muchos)
t2 = time.time() - t0
caso("S coste de limpiar el stderr entero", t1 < 10, f"1,1 MB de registro: {t1:.1f} s; 20 000 correos distintos (0,4 MB): {t2:.1f} s "
     "(cada dato distinto recorre el texto: crece con datos × tamaño)", obs=True)


# ---------------------------------------------------------------- R. resumen.json y la salida
def cli_falso(paquete_json, ciclo, llamadas, falla_b=False):
    def cli(bloque, args):
        llamadas.append(bloque)
        if bloque == "a" and args[-1] == "ciclo":
            return {"entregables": {"paquete_json": str(paquete_json)}, **ciclo}
        if bloque == "b":
            if falla_b:
                raise mod.FalloEjecutor(f"bloque B analizar: código 4\nValueError: {CORREO} {DATOS['token'][0]}")
            return {"pet_id": "PET-2026-0001", "estado_peticion": "ENTREGADA", "acuse_inmediato": {"pet_id": "PET-2026-0001",
                    "admision": "ADMITIDA"}, "entregables": {}, "resumen": {"veredicto": CORREO}}
        if bloque == "a" and "decision" in args:
            return {"ret_id": "RET-2026-0001", "estado": DATOS["iban"][0]}
        raise AssertionError(f"llamada inesperada {bloque} {args[-3:]}")
    return cli


paq = copy.deepcopy(EJEMPLO)
paq["estado_g3"] = "APTO"
ruta_paq = TMP / "r_paquete.json"
ruta_paq.write_text(json.dumps(paq, ensure_ascii=False), encoding="utf-8")
DATO_CICLO = {"run_id": CORREO, "estado": DATOS["password="][0], "top3_por_clase": {CORREO: [DATOS["sk"][0]], "RV": [{"x": DATOS["akia"][0]}]}}
ESCENARIOS = [
    ("sin entrega, con datos en entrega y g3", {**DATO_CICLO, "entrega": CORREO, "g3": DATOS["bearer"][0]}, False),
    ("entrega normal, datos en lo que devuelven A y B", {**DATO_CICLO, "entrega": "ENTREGADA", "g3": "APTO"}, False),
    ("fallo del Bloque B con datos", {**DATO_CICLO, "entrega": "ENTREGADA", "g3": "APTO"}, True),
]
for nombre, ciclo, falla in ESCENARIOS:
    mod = modulo_script()
    mod._cli = cli_falso(ruta_paq, ciclo, [], falla)
    w = TMP / f"r_{len(nombre)}"
    codigo, out, err = ejecutar(mod, ["--trabajo", str(w), "--config-a", str(EXTRA)])
    resumen = (w / "resumen.json").read_text(encoding="utf-8") if (w / "resumen.json").exists() else ""
    quedan = sorted(set(sin_nucleos(resumen, out, err)))
    caso(f"R {nombre}: ningún dato en resumen.json ni en la salida", not quedan and "Traceback" not in err and resumen != "",
         f"código {codigo}; quedan {quedan}; resumen.json {'sí' if resumen else 'no'}")

# ---------------------------------------------------------------- C. --config-a que no se lee
CONFIGS = {
    "no existe": None,
    "una carpeta": "DIR",
    "YAML roto (corchete sin cerrar) con un correo": f"cadena_b:\n  peticion: [{CORREO}\n",
    "YAML roto (sangría) con una clave": f"cadena_b:\n peticion: 1\n  otra: {DATOS['api_key'][0]}\n",
    "YAML con una etiqueta de Python y un correo": f"cadena_b: !!python/object:os.system {CORREO}\n",
    "YAML con un carácter de control y un correo": f"x: {CORREO}\x07\n",
    "UTF-8 inválido": b"cadena_b: \xff\xfe " + CORREO.encode(),
    "una lista con un correo": f"- {CORREO}\n",
    "un texto con un correo": f"{CORREO}\n",
    "cadena_b es un texto con un correo": f"cadena_b: {CORREO}\n",
    "la correspondencia es una lista con un correo": f"cadena_b:\n  correspondencia_ambitos: [{CORREO}]\n",
    "un valor de la correspondencia es una lista": "cadena_b:\n  correspondencia_ambitos:\n    LETRAS-EUR-12M: [liquidez_eur]\n",
    "un valor de la correspondencia es un diccionario": "cadena_b:\n  correspondencia_ambitos:\n    LETRAS-EUR-12M: {a: 1}\n",
    "valores de la correspondencia de tipos que no se ordenan": "cadena_b:\n  correspondencia_ambitos:\n    A: 1\n    B: x\n",
}
fuera_de_o06 = ("un valor de la correspondencia es una lista", "un valor de la correspondencia es un diccionario",
                "valores de la correspondencia de tipos que no se ordenan")
for nombre, contenido in CONFIGS.items():
    ruta = TMP / f"cfg_{abs(hash(nombre))}.yaml"
    if contenido == "DIR":
        ruta.mkdir(exist_ok=True)
    elif isinstance(contenido, bytes):
        ruta.write_bytes(contenido)
    elif contenido is not None:
        ruta.write_text(contenido, encoding="utf-8")
    mod = modulo_script()
    llamadas: list = []
    mod._cli = cli_falso(ruta_paq, {"entrega": "ENTREGADA", "g3": "APTO"}, llamadas)
    codigo, out, err = ejecutar(mod, ["--trabajo", str(TMP / "c"), "--config-a", str(ruta)])
    ok = codigo in (1, 2) and not llamadas and "Traceback" not in err and not sin_nucleos(out, err) and err.strip()
    caso(f"C --config-a {nombre}: mensaje sin el contenido, código 1 (2 si cita ámbitos ajenos) y nada ejecutado", ok,
         f"código {codigo}, llamadas {len(llamadas)}: {err.strip()[:110]!r}", obs=nombre in fuera_de_o06)

# ---------------------------------------------------------------- P. paquete_json que no se lee
PAQUETES = {
    "no existe": None,
    "una carpeta": "DIR",
    "vacío": "",
    "no es JSON (con un correo)": f"{{'opp_id': '{CORREO}'",
    "UTF-8 inválido": b'{"x": "\xff' + CORREO.encode() + b'"}',
    "una lista": "[1, 2]",
    "un texto con un correo": json.dumps(CORREO),
    "NaN suelto": "NaN",
}
for nombre, contenido in PAQUETES.items():
    ruta = TMP / f"paq_{abs(hash(nombre))}.json"
    if contenido == "DIR":
        ruta.mkdir(exist_ok=True)
    elif isinstance(contenido, bytes):
        ruta.write_bytes(contenido)
    elif contenido is not None:
        ruta.write_text(contenido, encoding="utf-8")
    mod = modulo_script()
    llamadas = []
    mod._cli = cli_falso(ruta, {"entrega": "ENTREGADA", "g3": "APTO"}, llamadas)
    w = TMP / f"p_{abs(hash(nombre))}"
    codigo, out, err = ejecutar(mod, ["--trabajo", str(w), "--config-a", str(EXTRA)])
    resumen = json.loads((w / "resumen.json").read_text(encoding="utf-8")) if (w / "resumen.json").exists() else {}
    ok = (codigo == 1 and llamadas == ["a"] and "Traceback" not in err and not sin_nucleos(out, err, json.dumps(resumen))
          and (resumen.get("sin_envio") or {}).get("motivo") == "PAQUETE_ILEGIBLE")
    caso(f"P paquete {nombre}: PAQUETE_ILEGIBLE, código 1, sin envío ni traza ni contenido", ok,
         f"código {codigo}, llamadas {llamadas}: {err.strip()[:100]!r}")
# se lee pero no tiene la forma de un paquete (fuera de O-04, que habla de los que no se leen)
FORMAS = {"paquete_para_bloque_B es un texto": {"estado_g3": "APTO", "paquete_para_bloque_B": "x", "clases": {}},
          "una opción sin opp_id": {"estado_g3": "APTO", "clases": {"RV": {"opciones": [{"siguiente_paso_sugerido": "ENVIAR_A_BLOQUE_B"}]}}},
          "clases es una lista": {"estado_g3": "APTO", "clases": [1]}}
for nombre, contenido in FORMAS.items():
    ruta = TMP / f"forma_{abs(hash(nombre))}.json"
    ruta.write_text(json.dumps(contenido), encoding="utf-8")
    mod = modulo_script()
    llamadas = []
    mod._cli = cli_falso(ruta, {"entrega": "ENTREGADA", "g3": "APTO"}, llamadas)
    codigo, out, err = ejecutar(mod, ["--trabajo", str(TMP / "f"), "--config-a", str(EXTRA)])
    caso(f"P paquete legible sin la forma ({nombre}): sin traza", "Traceback" not in err and "b" not in llamadas,
         f"código {codigo}, llamadas {llamadas}: {err.strip()[:90]!r} (fuera de O-04; G3 de A no entrega un paquete así)", obs=True)

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
