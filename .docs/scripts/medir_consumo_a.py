"""Mide llamadas y tokens de entrada por agente en un ciclo simulado del Bloque A (cliente mock, sin coste).

Uso (desde bloque_a/11_Ejecutor):
  ../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py <carpeta> [as_of] [--config yaml] [subcomando...]
Por defecto ejecuta el ciclo periódico C1 con los datos sintéticos de ejemplo y as_of 2024-03-29.
Deja <carpeta>/llamadas.json con una fila por llamada (agente, modelo, tokens de prompt de sistema, de encargo y de
salida, máximo de salida, lectura y escritura de caché) e imprime un resumen por agente. La salida del simulador no es
representativa; la entrada sí. Evaluación del Bloque A, 11-11-2026."""
import collections
import contextlib
import io
import json
import shutil
import sys
from pathlib import Path

from bloque_a import cli, llm

reg = []
orig = llm.MockClient.generar


def espia(self, **kw):
    r = orig(self, **kw)
    sys_txt = "".join(b.get("text", "") for b in kw["system"])
    user_txt = json.dumps(kw["mensajes"], ensure_ascii=False, default=str)
    reg.append({"agente": kw["agente"], "modelo": kw["modelo"], "sys_tok": llm._tokens_aprox(sys_txt),
                "user_tok": llm._tokens_aprox(user_txt), "out_tok": r.uso.salida, "max_tokens": kw["max_tokens"],
                "cache_lect": r.uso.cache_lectura, "cache_escr": r.uso.cache_escritura})
    return r


llm.MockClient.generar = espia
S = Path(sys.argv[1])
as_of = sys.argv[2] if len(sys.argv) > 2 else "2024-03-29"
resto = sys.argv[3:]
extra = []
if resto[:1] == ["--config"]:
    extra, resto = resto[:2], resto[2:]
sub = resto or ["ciclo"]
shutil.rmtree(S, ignore_errors=True)
base = ["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--estado", str(S / "estado"),
        "--salida", str(S / "salida"), "--as-of", as_of] + extra
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    cli.main(base + sub)
S.mkdir(parents=True, exist_ok=True)
(S / "llamadas.json").write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
por = collections.defaultdict(lambda: [0, 0, 0, 0, ""])
for x in reg:
    a = por[x["agente"]]
    a[0] += 1
    a[1] += x["sys_tok"]
    a[2] += x["user_tok"]
    a[3] += x["out_tok"]
    a[4] = x["modelo"]
tot_sys = sum(v[1] for v in por.values())
tot_user = sum(v[2] for v in por.values())
print(f"{len(reg)} llamadas, {len(por)} agentes; entrada: sistema {tot_sys}, encargo {tot_user}")
for ag, (n, s, u, o, m) in sorted(por.items(), key=lambda kv: -(kv[1][1] + kv[1][2])):
    print(f"{ag:8} {m:20} llamadas {n:3}  sistema {s:8}  encargo {u:7}  salida {o:6}")
