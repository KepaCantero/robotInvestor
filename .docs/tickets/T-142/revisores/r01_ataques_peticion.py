"""QA r01 de T-142 (revisor independiente): ataques a `bloque_a/cadena_b.py` y envío de peticiones raras al ejecutor
del Bloque B por su línea de comandos (cliente simulado, coste cero). No importa código del Bloque B.

Uso (desde la raíz de la copia):  <python> .docs/tickets/T-142/revisores/r01_ataques_peticion.py [--sin-b] [--trabajo DIR]
Imprime una línea por caso: OK (lo esperado) u OBS (observación: comportamiento discutible) y termina con 0."""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ_A = RAIZ / "bloque_a" / "11_Ejecutor"
EJ_B = RAIZ / "bloque_b" / "11_Ejecutor"
sys.path.insert(0, str(EJ_A))
from bloque_a import cadena_b  # noqa: E402
from bloque_a.configuracion import cargar_config, fusionar  # noqa: E402

CON_B = "--sin-b" not in sys.argv
TRABAJO = sys.argv[sys.argv.index("--trabajo") + 1] if "--trabajo" in sys.argv else None
cfg = cargar_config()
ejemplo = json.loads((EJ_A.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json").read_text("utf-8"))
OPP = "OPP-2026-9112"     # opción MON del ejemplo publicado (ENVIAR_A_BLOQUE_B)
CFG = fusionar(cfg, {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}})
res: list[tuple[str, str, str]] = []


def caso(nombre: str, ok: bool, detalle: str = "") -> None:
    res.append(("OK" if ok else "OBS", nombre, detalle))


def entrada_de(p: dict) -> dict:
    return next(e for e in p["paquete_para_bloque_B"] if e["opp_id"] == OPP)


def opcion_de(p: dict) -> dict:
    return next(o for c in p["clases"].values() for o in c["opciones"] if o["opp_id"] == OPP)


def intenta(p: dict, c: dict = CFG, **kw):
    try:
        return cadena_b.construir_peticion(p, OPP, c, **kw), None
    except cadena_b.ErrorCadenaB as e:
        return None, e.codigo
    except Exception as e:   # noqa: BLE001
        return None, f"EXCEPCION_NO_CONTROLADA:{type(e).__name__}:{e}"


# --- Anexo B.1 frente a la petición (lectura propia del Documento 0 del Bloque B)
doc0 = next(p for p in (RAIZ / "bloque_b" / "01_Gobernanza").iterdir()
            if unicodedata.normalize("NFC", p.name).startswith("Documento 0") and p.suffix == ".md").read_text("utf-8")
b1 = json.loads(re.search(r"```json\n(.*?)```", doc0[doc0.index("### B.1 CT-B-01"):], re.S).group(1))
pet, err = intenta(copy.deepcopy(ejemplo))
caso("B.1: mismas claves de primer nivel", pet is not None and set(pet) == set(b1), str(set(pet or {}) ^ set(b1)))
caso("B.1: objeto ⊆ B.1 + clave_universo", set(pet["objeto"]) <= set(b1["objeto"]) | {"clave_universo"})
caso("B.1: marco ⊆ B.1", set(pet["marco_invertibilidad"]) <= set(b1["marco_invertibilidad"]))
for campo in ("origen", "nivel", "prioridad"):
    caso(f"B.1: {campo} dentro de su enumeración", pet[campo] in b1[campo].split("|"), str(pet[campo]))
ent = entrada_de(ejemplo)
caso("Encargo tal cual + x_clave_universo", pet["paquete_para_bloque_B"] == {**ent, "x_clave_universo": "liquidez_eur"})
caso("Determinista (dos veces, igual)", cadena_b.construir_peticion(copy.deepcopy(ejemplo), OPP, CFG) == pet)

# --- Campos de más en el encargo de A
p = copy.deepcopy(ejemplo); entrada_de(p)["puntuaciones_A"] = {"A": 70}
caso("Campo no x_ en el encargo → ENTRADA_B_INVALIDA", intenta(p)[1] == "ENTRADA_B_INVALIDA", str(intenta(p)[1]))
p = copy.deepcopy(ejemplo); entrada_de(p)["x_nota_libre"] = "extensión de A"
r, e = intenta(p)
caso("Extensión x_ de A viaja tal cual (esquema A la admite)", r is not None and r["paquete_para_bloque_B"].get("x_nota_libre") == "extensión de A", str(e))
p = copy.deepcopy(ejemplo); entrada_de(p)["x_clave_universo"] = "cobre"
r, e = intenta(p)
caso("x_clave_universo previa de A se sustituye por la de la tabla", r is not None and r["paquete_para_bloque_B"]["x_clave_universo"] == "liquidez_eur")
r, e = intenta(p, exigir_correspondencia=True)
p2 = copy.deepcopy(p); entrada_de(p2)["indicador_seguimiento"]["simbolo"] = "SIN-FILA"
r, e = intenta(p2, exigir_correspondencia=False)
caso("Sonda sin correspondencia: no arrastra una x_clave_universo previa del paquete",
     r is not None and "x_clave_universo" not in r["paquete_para_bloque_B"], json.dumps((r or {}).get("paquete_para_bloque_B", {}).get("x_clave_universo")))

# --- Tipos de activo
p = copy.deepcopy(ejemplo); opcion_de(p)["tipos_secundarios"] = "RF"
r, e = intenta(p)
caso("tipos_secundarios como texto no se trocea en letras", r is None or r["tipos_activo_admitidos"] in (["MON", "RF"], ["MON"]),
     str((r or {}).get("tipos_activo_admitidos") or e))
p = copy.deepcopy(ejemplo); opcion_de(p)["tipos_secundarios"] = ["XYZ", "RF", "RF", None]
r, e = intenta(p)
caso("tipos_secundarios ajenos a los 12 tipos / duplicados / None no pasan", r is None or r["tipos_activo_admitidos"] == ["MON", "RF"],
     str((r or {}).get("tipos_activo_admitidos") or e))
p = copy.deepcopy(ejemplo); entrada_de(p)["tipo_activo"] = "ACCIONES"
caso("tipo_activo fuera del esquema → ENTRADA_B_INVALIDA", intenta(p)[1] == "ENTRADA_B_INVALIDA")

# --- Horizontes
p = copy.deepcopy(ejemplo); entrada_de(p)["horizontes"] = ["H5"]; entrada_de(p)["horizonte_principal"] = "H5"
r, e = intenta(p); caso("H5 viaja", r is not None and r["horizontes"] == ["H5"], str(e))
p = copy.deepcopy(ejemplo); entrada_de(p)["horizontes"] = ["H6"]
caso("H6 → ENTRADA_B_INVALIDA", intenta(p)[1] == "ENTRADA_B_INVALIDA")
p = copy.deepcopy(ejemplo); entrada_de(p)["horizontes"] = ["H2"]; entrada_de(p)["horizonte_principal"] = "H4"
r, e = intenta(p)
caso("horizonte_principal fuera de horizontes (incoherente) no se envía", r is None, f"construida: {r is not None}")

# --- Datos protegidos R8 en textos del encargo
for etiqueta, texto in (("correo", "Contacto: inversor.real@example.com"), ("clave", "api_key=ABCDEF1234567890"),
                        ("IBAN", "ES91 2100 0418 4502 0005 1332")):
    p = copy.deepcopy(ejemplo); entrada_de(p)["tesis"] = f"La tesis del ámbito monetario. {texto}"
    r, e = intenta(p)
    caso(f"R8 ({etiqueta}) en la tesis: el Broker no lo envía", r is None, f"construida: {r is not None} ({e})")
    if r is not None and etiqueta == "correo":
        PET_R8 = r

# --- Paquetes rotos
for etiqueta, mod in (("clases lista", lambda q: q.update(clases=[])), ("clases None", lambda q: q.update(clases=None)),
                      ("opciones dict", lambda q: q["clases"]["MON"].update(opciones={"a": 1})),
                      ("paquete_para_bloque_B dict", lambda q: q.update(paquete_para_bloque_B={"x": 1})),
                      ("run_id entero", lambda q: q.update(run_id=7)),
                      ("entrada no dict", lambda q: q.update(paquete_para_bloque_B=[1, "a", None] + q["paquete_para_bloque_B"])),
                      ("ambito con NaN", lambda q: entrada_de(q)["ambito"].update(region=float("nan"))),
                      ("opción duplicada en otra clase", lambda q: q["clases"].setdefault("RF", {"opciones": []})["opciones"].append(copy.deepcopy(opcion_de(q))))):
    p = copy.deepcopy(ejemplo)
    mod(p)
    r, e = intenta(p)
    caso(f"Paquete raro ({etiqueta}) falla cerrado con ErrorCadenaB", r is None and e and not e.startswith("EXCEPCION"), str(e))

# --- Configuración rota
for etiqueta, sec in (("clave con espacios", {"correspondencia_ambitos": {"LETRAS-EUR-12M": " liquidez_eur "}}),
                      ("nivel fuera de B.1", {"peticion": {"nivel": "N9"}}),
                      ("prioridad fuera de B.1", {"peticion": {"prioridad": "URGENTISIMA"}}),
                      ("idioma no texto", None)):
    c = fusionar(CFG, {"cadena_b": sec}) if sec else fusionar(CFG, {"idioma": 123})
    r, e = intenta(copy.deepcopy(ejemplo), c)
    caso(f"Configuración rota ({etiqueta}) falla cerrado", r is None, f"construida: {r is not None}: "
         + json.dumps({k: (r or {}).get(k) for k in ("nivel", "prioridad", "idioma_usuario")} | {"clave": (r or {}).get("objeto", {}).get("clave_universo")}))

# --- No muta
p = copy.deepcopy(ejemplo); antes = copy.deepcopy(p); intenta(p); caso("No muta el paquete", p == antes)

# --- CT-04 de vuelta
for etiqueta, resp in (("sin pet_id", {}), ("lista", []), ("pet_id vacío", {"pet_id": ""})):
    try:
        cadena_b.ct04_desde_respuesta_b(OPP, resp); caso(f"CT-04 ({etiqueta}) falla cerrado", False)
    except cadena_b.ErrorCadenaB:
        caso(f"CT-04 ({etiqueta}) falla cerrado", True)
ct = cadena_b.ct04_desde_respuesta_b(OPP, {"pet_id": "PET-B-1", "admision": "RECHAZADA", "motivo": "DATOS_SENSIBLES"})
caso("CT-04 de una petición RECHAZADA por B sigue siendo ENVIADA_A_BLOQUE_B (decisión del Broker: la envió)",
     ct["decisiones"][0]["decision"] == "ENVIADA_A_BLOQUE_B", ct["resultado_comunicado"]["texto"])

# --- Al ejecutor del Bloque B (CLI, mock)
if CON_B:
    w = Path(tempfile.mkdtemp(prefix="t142_r01_", dir=TRABAJO))

    def b(pet: dict, nombre: str) -> dict:
        f = w / f"{nombre}.json"; f.write_text(json.dumps(pet, ensure_ascii=False), "utf-8")
        r = subprocess.run([sys.executable, "-m", "bloque_b.cli", "--cliente", "mock", "--estado", str(w / nombre / "e"),
                            "--salida", str(w / nombre / "s"), "--as-of", "2024-03-29", "analizar", "--json", str(f)],
                           cwd=EJ_B, capture_output=True, text=True)
        try:
            return json.loads(r.stdout)
        except json.JSONDecodeError:
            return {"_codigo": r.returncode, "_stderr": r.stderr[-300:]}

    if "PET_R8" in globals():
        r = b(PET_R8, "r8")
        a = r.get("acuse_inmediato") or r
        caso("B rechaza íntegro el encargo con correo (DATOS_SENSIBLES)", a.get("motivo") == "DATOS_SENSIBLES", json.dumps(a, ensure_ascii=False)[:160])
    p = copy.deepcopy(pet); p["nivel"] = "N9"
    r = b(p, "nivel_n9"); a = r.get("acuse_inmediato") or r
    caso("B con nivel N9 (fuera de B.1) lo rechaza", a.get("admision") == "RECHAZADA", f"{a.get('admision')} {r.get('estado_peticion') or r.get('estado')} {str(r.get('_stderr',''))[-120:]}")
    p = copy.deepcopy(pet); p["tipos_activo_admitidos"] = ["M", "O", "N"]
    r = b(p, "tipos_letras"); a = r.get("acuse_inmediato") or r
    caso("B con tipos troceados en letras lo rechaza", a.get("admision") == "RECHAZADA", f"{a.get('admision')} {r.get('estado_peticion') or r.get('estado')}")
    print(f"(trabajo del Bloque B en {w})")

for est, n, d in res:
    print(f"{est:3} · {n}" + (f" · {d}" if d else ""))
print(f"\n{sum(1 for r in res if r[0] == 'OK')} OK · {sum(1 for r in res if r[0] == 'OBS')} OBS")
