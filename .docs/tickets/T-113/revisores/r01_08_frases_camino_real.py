"""QA r01 de T-113 · H-49 y H-50 de T-110 por el camino real: un ciclo V6 con el Sintetizador simulado devolviendo 0, 1, 2, 3 o 4
frases de 30 s, frases vacías o no texto, motivos de claves ajenas y un texto con ticker en minúscula. Se mira qué se entrega,
qué se declara y que el estado quede bien.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_08_frases_camino_real.py"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a import mock_respuestas as mr  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

orig = mr._sintetizador
CASOS = {
    "dos (normal)": lambda o: o,
    "una": lambda o: {**o, "frases_30s": o["frases_30s"][:1]},
    "tres": lambda o: {**o, "frases_30s": o["frases_30s"] + ["Tercera frase del modelo."]},
    "cero": lambda o: {**o, "frases_30s": []},
    "cuatro": lambda o: {**o, "frases_30s": o["frases_30s"] + ["Tercera.", "Cuarta."]},
    "dos, la segunda vacía": lambda o: {**o, "frases_30s": [o["frases_30s"][0], "   "]},
    "dos, la primera vacía": lambda o: {**o, "frases_30s": ["", o["frases_30s"][1]]},
    "una y prohibida": lambda o: {**o, "frases_30s": ["Sube un 70 % seguro."]},
    "tres, la tercera es la buena": lambda o: {**o, "frases_30s": ["Sube un 70 %.", "Cae un 30 %.", "El mercado espera con calma."]},
    "dos iguales": lambda o: {**o, "frases_30s": [o["frases_30s"][0]] * 2},
    "número en la lista": lambda o: {**o, "frases_30s": [o["frases_30s"][0], 7]},
    "sin el campo": lambda o: {k: v for k, v in o.items() if k != "frases_30s"},
    "frases_30s texto": lambda o: {**o, "frases_30s": "Una sola frase."},
    "motivos ajenos": lambda o: {**o, "motivos_llanos": {**o["motivos_llanos"], "ZETA": "No es un tipo.", "RV 2027": "Tampoco."}},
    "motivos lista": lambda o: {**o, "motivos_llanos": ["x"]},
}
fallos = 0
for nombre, cambio in CASOS.items():
    mr._sintetizador = lambda msg, ctx, rng, _c=cambio: _c(orig(msg, ctx, rng))
    tmp = Path(tempfile.mkdtemp(prefix="qa_t113_frases_", dir=os.environ.get("QA_TMP")))
    b = Bloque(config_pruebas(diseno="v6", perfiles={"activos": ["RV", "DIV", "MP"]}), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
               MockClient(), tmp / "estado", tmp / "ent")
    try:
        res = b.ciclo(AS_OF)
    except BaseException as e:  # noqa: BLE001
        fallos += 1; print(f"FALLO {nombre}: EXCEPCIÓN {type(e).__name__}: {str(e)[:120]}"); continue
    paq = res["paquete"]
    red = res.get("redaccion") or {}
    frases = red.get("frases_30s") if isinstance(red, dict) else None
    decl = [x for x in paq["limitaciones"] if "Sintetizador" in x or "FORMATO" in x or "redacción" in x.lower()]
    print(f"--- {nombre}: estado={res.get('estado')} G3={(res.get('g3') or {}).get('dictamen')}")
    print("    claves del resultado:", sorted(res)[:14]) if nombre == "dos (normal)" else None
    print("    frases_30s entregadas:", frases)
    print("    declarado:", decl)
    if isinstance(red, dict) and red.get("motivos_llanos") is not None and "motivos" in nombre:
        print("    motivos_llanos:", sorted(red["motivos_llanos"]))
mr._sintetizador = orig
print("FALLOS (excepciones):", fallos)
