"""Mide llamadas y tokens de entrada por agente en un análisis simulado del Bloque B (cliente mock, sin coste).

Uso (desde bloque_b/11_Ejecutor): ../../.venv/bin/python ../../.docs/scripts/medir_consumo_b.py ejemplos/peticiones/<petición>.json <carpeta>
Deja <carpeta>/llamadas.json con una fila por llamada (agente, modelo, tokens de prompt de sistema, de encargo y de salida,
lectura y escritura de caché). La salida del simulador no es representativa; la entrada sí. Evaluación del Bloque B, 11-11-2026."""
import json, sys, collections, shutil
from pathlib import Path
from bloque_b import llm, cli
reg = []
orig = llm.MockClient.generar
def espia(self, **kw):
    r = orig(self, **kw)
    sys_txt = "".join(b.get("text", "") for b in kw["system"]) if isinstance(kw["system"], list) else str(kw["system"])
    user_txt = json.dumps(kw["mensajes"], ensure_ascii=False)
    reg.append({"agente": kw["agente"], "modelo": kw["modelo"], "sys_tok": llm._tokens_aprox(sys_txt),
                "user_tok": llm._tokens_aprox(user_txt), "out_tok": r.uso.salida, "max_tokens": kw["max_tokens"],
                "cache_lect": r.uso.cache_lectura, "cache_escr": r.uso.cache_escritura, "entrada": r.uso.entrada})
    return r
llm.MockClient.generar = espia
peticion, S = sys.argv[1], Path(sys.argv[2])
shutil.rmtree(S, ignore_errors=True)
base = ["--cliente", "mock", "--estado", str(S / "estado"), "--salida", str(S / "ENT")]
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    cli.main(base + ["analizar", "--json", peticion])
out = json.loads(buf.getvalue())
if out.get("aut_id"):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cli.main(base + ["autorizar", "--aut", out["aut_id"], "--opcion", "CONTINUAR"])
    out = json.loads(buf.getvalue())
json.dump(reg, open(S / "llamadas.json", "w"), ensure_ascii=False)
print(json.dumps({k: out.get(k) for k in ("estado_peticion", "consumo_uc", "estado_g3")}, ensure_ascii=False), len(reg), "llamadas")
