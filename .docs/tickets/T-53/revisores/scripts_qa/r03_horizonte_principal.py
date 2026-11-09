"""r03 · CS-01 (horizonte principal) y CS-17 (siguiente paso): ciclo mock con el Analista declarando el horizonte principal.
(a) sin parche: valores de siguiente_paso, campos del horizonte principal;
(b) el Analista declara horizonte_principal=H5 (ofrecido) sin naturaleza: ¿qué naturaleza pone el ejecutor y qué dice HT-09?
(c) el Analista declara horizonte_principal H1, no ofrecido: ¿se sustituye en silencio?"""
import tempfile, pathlib, collections, sys, json
from bloque_a import mock_respuestas as mr
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

orig = mr._ficha
def run(etq, parche=None):
    if parche:
        def _f(u, msg, ctx, rng, iny):
            out = orig(u, msg, ctx, rng, iny); parche(out); return out
        mr._ficha = _f
    else:
        mr._ficha = orig
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
    r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
    ops = r["paquete"]["clases"].get("RV", {}).get("opciones", [])
    print(f"[{etq}] estado={r['estado']} entrega={r.get('entrega')} g3={r['g3']['dictamen']} bloqueos_g3={r['g3'].get('bloqueos')} n_opciones={len(ops)}")
    for o in ops:
        hp = o["horizonte_principal"]
        print("   ", o["opp_id"], "hz=", sorted(o["horizontes"]), "hp=", hp, "nat=", o["naturaleza_inversion"], "just=", o["justificacion_horizonte"],
              "| paso=", o["siguiente_paso_sugerido"], "E/A=", o["puntuaciones"]["E"], o["puntuaciones"]["A"],
              "| campos hz[hp]=", sorted((o["horizontes"].get(hp) or {}).keys())[:12])
    g3v = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V"]
    c17 = [c for e in g3v for c in (e.get("comprobaciones") or e.get("hallazgos") or []) if "C17" in json.dumps(c, ensure_ascii=False)]
    print("    C17 en G3V:", json.dumps(c17, ensure_ascii=False)[:600])
    print("    limitaciones con 'horizonte':", [x for x in r["paquete"]["limitaciones"] if "orizonte" in x][:3])
    return r

run("a_sin_parche")
run("b_hp_H5_sin_naturaleza", lambda o: o.update(horizonte_principal="H5"))
run("c_hp_H1_no_ofrecido", lambda o: o.update(horizonte_principal="H1", naturaleza_inversion="TACTICA"))
