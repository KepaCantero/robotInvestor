"""QA r01 de T-120 · El patrón del IBAN español con separadores, con un banco propio, y el camino real (CT-04, CT-03, CT-23).
S = se espera que se marque (es un IBAN español en grupos de cuatro) · N = no es un IBAN, se espera que no se marque ·
O = observación (formas del IBAN fuera de lo declarado o dudosas: se imprime lo que da). Compara además con el patrón anterior
(6b9f916^): nada que antes se marcara deja de marcarse.
Uso (desde bloque_a/11_Ejecutor de la copia): QA_TMP=<carpeta> python .../r01_01_iban_banco.py
El IBAN de prueba es el de ejemplo de la documentación bancaria y va partido."""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a import contratos  # noqa: E402
from bloque_a.contratos import DatosSensibles, contiene_credenciales, secretos_en_texto  # noqa: E402
from bloque_a.llm import contenido_sensible  # noqa: E402

I = "ES91" + "2100" + "0418" + "4502" + "0005" + "1332"
G = [I[i:i + 4] for i in range(0, 24, 4)]
ESP = " ".join(G)
fuente = subprocess.run(["git", "show", "6b9f916^:bloque_a/11_Ejecutor/bloque_a/contratos.py"], capture_output=True, text=True, check=True).stdout
viejo_src = re.search(r"^RE_SECRETO = re\.compile\(.*?\n\n", fuente, re.S | re.M).group(0)
ns = {"re": re}
exec(viejo_src, ns)  # noqa: S102 — el patrón anterior, del propio repositorio
RE_VIEJO = ns["RE_SECRETO"]

BANCO = [
    ("S", "junto", I), ("S", "espacios", ESP), ("S", "puntos", ".".join(G)), ("S", "guiones", "-".join(G)),
    ("S", "mezcla de separadores", f"{G[0]} {G[1]}-{G[2]}.{G[3]} {G[4]}{G[5]}"), ("S", "solo el primero separado", G[0] + " " + "".join(G[1:])),
    ("S", "solo el último separado", "".join(G[:5]) + " " + G[5]), ("S", "tras «IBAN:» pegado", "IBAN:" + ESP), ("S", "tras «IBAN=»", "iban=" + I),
    ("S", "entre paréntesis", f"({ESP})"), ("S", "con punto final", f"Cobren en {ESP}."), ("S", "con coma detrás", f"{ESP}, gracias"),
    ("S", "entre comillas", f"«{ESP}»"), ("S", "dentro de JSON", json.dumps({"c": ESP})), ("S", "dentro de JSON dos veces", json.dumps(json.dumps({"c": ESP}))),
    ("S", "con \\n escapado delante", "cuenta\\n" + ESP), ("S", "con \\u0020 escapado entre grupos", "\\u0020".join(G)),
    ("S", "con %20 entre grupos", "%20".join(G)), ("S", "en bytes", ESP.encode()), ("S", "seguido de salto de línea", ESP + "\nfin"),
    ("S", "dos IBAN seguidos", ESP + " " + "-".join(G)), ("S", "tras un guion", "cuenta-" + ESP),
    ("N", "ISIN español", "ES0113900J37"), ("N", "ISIN de deuda", "ES0000012B88"), ("N", "dos ISIN", "ISIN ES0113900J37 y ES0000012B88"),
    ("N", "NIF de sociedad", "A28015865"), ("N", "CIF con guion", "B-12345678"), ("N", "índice y nivel", "El ES50 cerró en 4 900 puntos."),
    ("N", "incompleto (4 grupos)", " ".join(G[:5])), ("N", "último grupo de 3", ESP[:-1]), ("O", "seguido de otro grupo de cuatro cifras (se marca: es un IBAN y un número)", ESP + " 0000"),
    ("N", "una cifra de más pegada", ESP + "0"), ("N", "importes", "Ingresos de 2100 0418 4502 y 0005 1332 millones."),
    ("N", "años", "Entre 2021 2022 2023 2024 2025 hubo subidas."), ("N", "fechas", "Del 2024-01-05 al 2024-03-29 y del 2025-01-03 al 2025-03-28."),
    ("N", "número de serie", "Serie SN91 2100 0418 4502 0005 1332."), ("N", "IBAN alemán", "DE89 3704 0044 0532 0130 00"),
    ("N", "palabra que acaba en ES", "REDES91 2100 0418 4502 0005 1332"), ("N", "ES y fechas ISO", "ES 2024-01-05 2024-03-29 2025-01-03"),
    ("N", "teléfono", "+34 912 345 678"), ("N", "código de mercado y años", "XMAD 2021 2022 2023 2024 2025"),
    ("O", "ES + dos cifras + cinco años (falso positivo posible)", "ES24 2021 2022 2023 2024 2025"),
    ("O", "ES35 y cinco niveles de cuatro cifras", "ES35 9100 9200 9300 9400 9500"),
    ("O", "dos espacios (límite declarado)", "  ".join(G)), ("O", "tabulador", "\t".join(G)), ("O", "espacio duro (U+00A0)", " ".join(G)),
    ("O", "espacio fino (U+202F)", " ".join(G)), ("O", "salto de línea entre grupos", "\n".join(G)), ("O", "guion largo", "–".join(G)),
    ("O", "guion bajo", "_".join(G)), ("O", "barra", "/".join(G)), ("O", "dos puntos", ":".join(G)), ("O", "espacio y guion", " - ".join(G)),
    ("O", "separador tras ES", "ES " + I[2:4] + " " + " ".join(G[1:])), ("O", "ES-91", "ES-" + I[2:]),
    ("O", "formato CCC (4-4-2-10)", f"{G[0]} {G[1]} {G[2]} {G[3][:2]} {G[3][2:]}{G[4]}{G[5]}"),
    ("O", "en grupos de dos", " ".join(I[i:i + 2] for i in range(0, 24, 2))), ("O", "en grupos de 4-4-4-4-8", " ".join(G[:4]) + " " + G[4] + G[5]),
    ("O", "minúsculas (declarado)", ESP.lower()), ("O", "pegado a una palabra delante", "cuenta" + ESP), ("O", "guion bajo delante", "iban_" + I),
    ("O", "letra pegada detrás", ESP + "EUR"), ("O", "partido en dos campos", {"a": " ".join(G[:3]), "b": " ".join(G[3:])}),
    ("O", "lista de grupos", G), ("O", "cifras de ancho completo", "ES91" + "".join(chr(ord(c) + 0xFEE0) for c in I[4:])),
    ("O", "con ceros de ancho cero", "​".join(G)), ("O", "IBAN en letra «IBAN ES91» + CCC con guiones", f"{G[0]} {G[1]}-{G[2]}-{G[3][:2]}-{G[3][2:]}{G[4]}{G[5]}"),
    ("O", "en URL (%2D)", "%2D".join(G)), ("O", "con «\\t» escapado", "\\t".join(G)),
]
fallos = 0
for clase, nombre, v in BANCO:
    if isinstance(v, (dict, list)):
        ahora, antes = bool(contiene_credenciales(v)), None
    else:
        ahora = bool(secretos_en_texto(v))
        tv = v.decode() if isinstance(v, bytes) else v
        antes = any(RE_VIEJO.search(x) for x in {tv, contratos.RE_ESCAPES.sub(" ", tv)})
    cs = contenido_sensible([{"a": (v,)}]) if not isinstance(v, (dict, list)) else contenido_sensible([v])
    mal = (clase == "S" and not (ahora and cs)) or (clase == "N" and (ahora or cs)) or (antes and not ahora)
    fallos += bool(mal)
    if mal or clase == "O":
        print(f"{'FALLO' if mal else '     '} {clase} marcado={ahora!s:5s} contenido_sensible={cs!s:5s} antes={antes!s:5s} {nombre}")
print(f"banco: {len(BANCO)} casos ({sum(c == 'S' for c, *_ in BANCO)} S, {sum(c == 'N' for c, *_ in BANCO)} N, {sum(c == 'O' for c, *_ in BANCO)} O) · fallos: {fallos}")

# falsos positivos al azar: textos con cifras en grupos de cuatro y códigos «ES..»
import random  # noqa: E402

rng = random.Random(120)
fp = 0
for _ in range(200000):
    partes = [rng.choice(["ES", "ES" + str(rng.randint(0, 99)), "ISIN", "ES0", "el", "en", str(rng.randint(0, 99999)), f"{rng.randint(1990, 2030)}",
                          f"{rng.randint(0, 9999):04d}", "ES" + "".join(rng.choice("0123456789ABCDEFGHJ") for _ in range(10))])
              for _ in range(rng.randint(3, 9))]
    txt = rng.choice([" ", " ", ". ", "-"]).join(partes)
    if secretos_en_texto(txt) and not re.search(r"\bES\d{2}(?:[ .\-]?\d{4}){5}\b", txt):
        fp += 1
    elif secretos_en_texto(txt) and fp < 0:
        pass
n_iban = sum(bool(re.search(r"\bES\d{2}(?:[ .\-]?\d{4}){5}\b", " ".join(["ES" + f"{rng.randint(0, 99):02d}"] + [f"{rng.randint(1990, 2030)}" for _ in range(5)]))) for _ in range(10))
print(f"al azar: marcados por otra regla distinta de la del IBAN: {fp}; «ESnn» seguido de cinco años se marca siempre: {n_iban}/10 (falso positivo de forma, improbable)")

# ---------- camino real ----------
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="qa_t120_", dir=os.environ.get("QA_TMP")))
uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def restos(carp, formas):
    out = []
    for p in Path(carp).rglob("*"):
        if p.is_file():
            cuerpo = p.read_bytes().decode("utf-8", errors="ignore")
            if any(f in cuerpo for f in formas) or re.search(r"2100\D{0,12}0418", cuerpo):
                out.append(p.name)
    return out


print("== camino real: cada forma S por CT-04, CT-03 y CT-23 (envío, respuesta y entrante)")
FORMAS = {"espacios": ESP, "puntos": ".".join(G), "guiones": "-".join(G), "junto": I, "mezcla": f"{G[0]} {G[1]}-{G[2]}.{G[3]} {G[4]}{G[5]}"}
for nombre, iban in FORMAS.items():
    carp = tmp / nombre
    b = nuevo_bloque(carp, uni)
    b.fijar_fecha(AS_OF)
    cns = b.consultas.enviar({"tipo": "OTRA", "preguntas": [{"texto": "¿Confirma el alcance?", "supuesto_declarado": "se mantiene"}]}, AS_OF)
    cns_id = cns.get("cns_id") or cns.get("id")
    ENVIOS = {
        "CT-04 comentario": lambda: b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"cobren en {iban}"}}, AS_OF),
        "CT-04 anidado": lambda: b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": "ok", "extra": [{"x": (iban,)}]}}, AS_OF),
        "CT-03 pregunta": lambda: b.consulta(f"¿Pueden pagar en {iban}?", as_of=AS_OF),
        "CT-03 contexto": lambda: b.consulta("¿Qué opinan del oro?", contexto={"nota": [iban]}, as_of=AS_OF),
        "CT-23 envío": lambda: b.consultas.enviar({"tipo": "OTRA", "preguntas": [{"texto": f"¿Es {iban} su cuenta?", "supuesto_declarado": "sí"}]}, AS_OF),
        "CT-23 respuesta": lambda: b.consultas.responder(cns_id, [{"texto": f"mi cuenta es {iban}"}], as_of=AS_OF),
        "CT-23 entrante": lambda: b.consultas.entrante(f"apunten {iban}", as_of=AS_OF),
    }
    for canal, f in ENVIOS.items():
        n_inc = len([e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"])
        try:
            f()
            res = "ADMITIDO"
        except DatosSensibles:
            res = "rechazado"
        except Exception as e:  # noqa: BLE001
            res = f"{type(e).__name__}: {str(e)[:60]}"
        inc = len([e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]) - n_inc
        r = restos(carp, [iban, I, ESP])
        mal = res != "rechazado" or inc != 1 or r
        fallos += bool(mal)
        if mal or nombre == "espacios":
            print(f"{'FALLO' if mal else 'ok   '} {nombre:9s} {canal:18s} {res} · incidencias SEGURIDAD +{inc} · archivos con el dato: {r}")
print("FALLOS:", fallos)
