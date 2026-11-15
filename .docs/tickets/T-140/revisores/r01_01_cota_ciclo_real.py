"""QA r01 de T-137 · ¿la cota de `estimar_coste_ciclo_a.py` acota lo que el cliente real puede pedir en un ciclo C1?

La cota se calcula sobre el `llamadas.json` de `medir_consumo_a.py`: un ciclo con el cliente simulado, desde un estado vacío.
Este script mide, con el mismo cliente simulado (sin coste, sin red), tres cosas que la cota no ve:
 1. llamadas que dependen de la respuesta del modelo y que el simulado no dispara: las peticiones de conocimiento CT-07/CT-08
    (hasta `seleccion.peticiones_conocimiento_por_clase` por tipo de activo, a AG-14/AG-16, con búsqueda web), las
    contrarréplicas CT-13 del Contradictor (una por tipo de activo como mucho) y la reescritura de AG-17 cuando G3 bloquea por
    legibilidad (C12). Se añaden copias de la llamada medida más cara de ese agente hasta el máximo que permite el código;
 2. la entrada de los agentes que leen lo que escriben otros (Contradictor, Curador, Integrador, Redactor, Auditor): el
    simulado escribe respuestas cortas; aquí cada respuesta del simulado se alarga (repitiendo sus textos) hasta cerca de su
    `max_tokens`, sin salirse de su esquema, y se mide otra vez la entrada de todas las llamadas;
 3. un segundo ciclo sobre el mismo estado (con opciones vigentes, lecciones, F2…), una semana después.
Uso (desde bloque_a/11_Ejecutor): python -I <este script> <carpeta temporal> [--config yaml]
"""
import contextlib
import importlib.util
import io
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
import jsonschema  # noqa: E402
import yaml  # noqa: E402
from bloque_a import cli, llm  # noqa: E402

spec = importlib.util.spec_from_file_location("est", RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py")
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)

S = Path(sys.argv[1])
extra = ["--config", sys.argv[sys.argv.index("--config") + 1]] if "--config" in sys.argv else []
cfg = est._config(extra[1] if extra else None)
tarifa = yaml.safe_load((RAIZ / "bloque_a" / "11_Ejecutor" / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))
bw = cfg["busqueda_web"]
AGB = set(bw["agentes"]) if bw.get("habilitada_en_vivo") else set()
ARGS = (tarifa["precios_por_millon"], float(tarifa["precio_busqueda_web_por_mil"]), AGB, int(bw["max_usos_por_llamada"]),
        float(tarifa["factor_tokens_cota"]), int(cfg["llm"]["max_continuaciones_pause_turn"]), int(cfg["llm"]["reintento_reparacion"]))

reg: list[dict] = []
INFLAR = {"activo": False}
orig = llm.MockClient.generar


def _alargar(obj, k):
    if isinstance(obj, str):
        return obj if len(obj) < 25 else " ".join([obj] * k)
    if isinstance(obj, list):
        return [_alargar(x, k) for x in obj]
    if isinstance(obj, dict):
        return {c: _alargar(v, k) for c, v in obj.items()}
    return obj


def espia(self, **kw):
    r = orig(self, **kw)
    if INFLAR["activo"] and kw.get("esquema") is not None:
        try:
            datos = json.loads(r.texto)
        except ValueError:
            datos = None
        if datos is not None:
            k = max(1, int(0.8 * kw["max_tokens"] / max(r.uso.salida, 1)))
            while k > 1:
                nuevo = _alargar(datos, k)
                txt = json.dumps(nuevo, ensure_ascii=False)
                if (llm._tokens_aprox(txt) <= kw["max_tokens"]
                        and not list(jsonschema.Draft202012Validator(kw["esquema"]).iter_errors(nuevo))):
                    r = llm.RespuestaLLM(txt, llm.Uso(salida=llm._tokens_aprox(txt)), r.modelo, stop_reason="end_turn")
                    break
                k = k // 2 if k > 4 else k - 1
    sys_txt = "".join(b.get("text", "") for b in kw["system"])
    reg.append({"agente": kw["agente"], "modelo": kw["modelo"], "sys_tok": llm._tokens_aprox(sys_txt),
                "user_tok": llm._tokens_aprox(json.dumps(kw["mensajes"], ensure_ascii=False, default=str)),
                "out_tok": r.uso.salida, "max_tokens": kw["max_tokens"], "cache_lect": 0, "cache_escr": 0})
    return r


llm.MockClient.generar = espia


def ciclo(estado: Path, as_of: str) -> list[dict]:
    reg.clear()
    base = ["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--estado", str(estado), "--salida",
            str(estado.parent / ("salida_" + as_of)), "--as-of", as_of] + extra + ["ciclo"]
    with contextlib.redirect_stdout(io.StringIO()):
        cli.main(base)
    return list(reg)


def cota(ll):
    return est.estimar(ll, *ARGS[:4], factor_tokens=ARGS[4], continuaciones=ARGS[5], reparaciones=ARGS[6])["cota_superior"]


def resumen(nombre, ll, ref=None):
    c = cota(ll)
    ent = sum(x["user_tok"] for x in ll)
    rel = f" ({100 * (c / ref - 1):+.1f} % sobre la cota del README)" if ref else ""
    print(f"{nombre:52} llamadas {len(ll):3} · encargo {ent:8} tok · cota {c:7.2f} USD{rel}")
    return c


shutil.rmtree(S, ignore_errors=True)
S.mkdir(parents=True)
base_ll = ciclo(S / "e0", "2024-03-29")
c0 = resumen("0. ciclo medido (como medir_consumo_a)", base_ll)

# 1. llamadas condicionales hasta el máximo que permite el código
n_clases = len(cfg["perfiles"]["activos"])
maxp = int(cfg["seleccion"]["peticiones_conocimiento_por_clase"]) * n_clases
cuenta = {a: sum(1 for x in base_ll if x["agente"] == a) for a in ("AG-14", "AG-16", "AG-11", "AG-17")}
analistas = sum(1 for x in base_ll if x["agente"] in {"AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08", "AG-09", "AG-21", "AG-22",
                                                       "AG-23", "AG-24", "AG-25"}) // 2 or n_clases


def mas_cara(agentes, defecto):
    cands = [x for x in base_ll if x["agente"] in agentes]
    return max(cands, key=lambda x: cota([x])) if cands else defecto


busq = mas_cara({"AG-14", "AG-16"}, {"agente": "AG-14", "modelo": cfg["modelos"]["AG-14"], "sys_tok": 20353, "user_tok": 1000,
                                       "out_tok": 0, "max_tokens": int(cfg["max_tokens"]["por_defecto"]), "cache_lect": 0, "cache_escr": 0})
contra = mas_cara({"AG-11"}, None)
red = mas_cara({"AG-17"}, None)
faltan_busq = max(0, maxp - cuenta["AG-14"] - cuenta["AG-16"])
faltan_contra = max(0, 2 * n_clases - cuenta["AG-11"])          # refutación + contrarréplica por tipo de activo (V5)
faltan_red = 1 if cuenta["AG-17"] == 1 else 0
extra_ll = [busq] * faltan_busq + [contra] * faltan_contra + [red] * faltan_red
print(f"   llamadas que faltan: {faltan_busq} de búsqueda (máximo {maxp}), {faltan_contra} contrarréplicas, {faltan_red} reescritura de AG-17")
c1 = resumen("1. + llamadas condicionales al máximo", base_ll + extra_ll, c0)

# 2. respuestas largas: la entrada de los agentes que leen a otros
INFLAR["activo"] = True
largo_ll = ciclo(S / "e1", "2024-03-29")
INFLAR["activo"] = False
c2 = resumen("2. respuestas del simulado alargadas hasta ~max_tokens", largo_ll, c0)
for a in ("AG-11", "AG-12", "AG-02", "AG-17", "AG-19"):
    b = sum(x["user_tok"] for x in base_ll if x["agente"] == a)
    lg = sum(x["user_tok"] for x in largo_ll if x["agente"] == a)
    print(f"   {a}: encargo {b:7} → {lg:7} tokens")
resumen("1 + 2", largo_ll + extra_ll, c0)

# 3. segundo ciclo sobre el mismo estado
ciclo(S / "e2", "2024-03-22")
seg = ciclo(S / "e2", "2024-03-29")
resumen("3. segundo ciclo sobre el mismo estado", seg, c0)
print(f"{'FALLA' if max(c1, c2) > c0 else 'ok   '} la cota del README ({c0:.2f}) cubre los escenarios 1 y 2")
