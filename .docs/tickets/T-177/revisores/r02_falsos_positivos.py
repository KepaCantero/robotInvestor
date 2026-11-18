"""QA r02 de T-177 · falsos positivos de `llm.solicitud_con_valor` con el formato de retorno canónico de los Analistas.

El formato de salida de los system prompts de los Analistas (Marco común V5.0, l. 33 y 44, y los 13 prompts de clase) lleva
siempre `"solicitudes_credenciales":[]` y `"regimen_clase":{"indicadores":[{"nombre":"…","valor":"…",…}]}`, con `valor` de
texto. El simulado no lo emite, así que el backtest mock no ejercita la barrera nueva con un retorno de Analista. Aquí se
hace que los Analistas simulados devuelvan esos dos campos (como haría el modelo real) y se cuenta lo que se pierde.

Uso (desde cualquier carpeta; ARBOL es la raíz de un worktree):
  python r02_falsos_positivos.py ARBOL SALIDA {v5|v6} {texto|numero|sin}
  texto: `valor` de texto («4,25 %»); numero: `valor` numérico; sin: el mock tal cual (control).
Imprime JSON con el estado del ciclo, las incidencias «Salida no conforme» por contenido_sensible y los finalistas."""
import json
import sys
from pathlib import Path

arbol, salida, diseno, modo = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
ej = arbol / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(ej))
import os  # noqa: E402

os.chdir(ej)
from bloque_a import cli, mock_respuestas  # noqa: E402

orig = mock_respuestas._analista


def _analista(msg, ctx, rng, inyectado):
    d = orig(msg, ctx, rng, inyectado)
    if modo != "sin" and isinstance(d, dict) and "regimen_clase" in d:
        d["regimen_clase"]["indicadores"] = [{"nombre": "Señal compuesta media", "valor": "0,61" if modo == "texto" else 0.61,
                                              "fecha": ctx.get("fecha_as_of"), "fuente": "HT-01"}]
        d["solicitudes_credenciales"] = []
        d["consultas_broker"] = []
    return d


mock_respuestas._analista = _analista
salida.mkdir(parents=True, exist_ok=True)
(salida / "cfg.yaml").write_text(f"diseno: {diseno}\nperfiles:\n  activos: [RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV]\n",
                                  encoding="utf-8")
args = ["--cliente", "mock", "--config", str(salida / "cfg.yaml"), "--datos", "ejemplos/datos_sinteticos",
        "--estado", str(salida / "estado"), "--salida", str(salida / "ent"), "--as-of", "2024-03-01", "ciclo"]
import contextlib  # noqa: E402
import io  # noqa: E402

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    cli.main(args)
r = json.loads(buf.getvalue()[buf.getvalue().find("{"):])
inc = []
for p in (salida / "estado").rglob("*.jsonl"):
    for linea in p.read_text(encoding="utf-8").splitlines():
        if "contenido_sensible" in linea or "bloqueada por R8" in linea:
            inc.append(json.loads(linea).get("objeto") if linea.startswith("{") else p.name)
paquete = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8")) if r.get("entregables") else {}
clases = paquete.get("clases") or []
ops = [o for c in clases if isinstance(c, dict) for o in (c.get("oportunidades") or c.get("opciones") or c.get("finalistas") or [])]
print(json.dumps({"arbol": arbol.name, "diseno": diseno, "modo": modo, "estado": r.get("estado"),
                  "bloqueos_r8": len(inc), "agentes_bloqueados": sorted(set(map(str, inc))),
                  "n_clases": len(clases), "n_oportunidades": len(ops), "limitaciones": len(paquete.get("limitaciones") or [])}, ensure_ascii=False))
