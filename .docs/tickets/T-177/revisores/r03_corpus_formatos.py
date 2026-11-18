"""QA r03 de T-177 · H-12 contra los formatos canónicos del corpus.

Extrae todos los objetos JSON de ejemplo de los system prompts de `bloque_a/02_System_prompts` (los formatos de retorno de
cada agente, con sus «…») y los pasa por `llm.respuesta_segura`:
  (a) tal cual, con `solicitudes_credenciales: []` en la raíz (como lo emiten los Analistas): nada debe bloquearse;
  (b) con una solicitud de credencial válida y sin valor: lo que se bloquea es el coste de la extensión de la r03
      (ficha opaca en todo el retorno).
Uso: python r03_corpus_formatos.py ARBOL   (imprime un JSON con el recuento y los bloqueados)."""
import json
import sys
from pathlib import Path

arbol = Path(sys.argv[1])
sys.path.insert(0, str(arbol / "bloque_a" / "11_Ejecutor"))
from bloque_a.llm import RespuestaLLM, Uso, respuesta_segura  # noqa: E402

SOL = {"servicio": "API de fondos cerrados", "motivo": "Cribado semanal de FON", "impacto_si_falta": "Datos públicos"}


def objetos(texto):
    dec = json.JSONDecoder()
    i = 0
    while (i := texto.find("{", i)) >= 0:
        try:
            o, fin = dec.raw_decode(texto, i)
        except ValueError:
            i += 1
            continue
        if isinstance(o, dict) and len(o) >= 3:
            yield o
        i = fin


def bloqueado(o):
    return respuesta_segura(RespuestaLLM(json.dumps(o, ensure_ascii=False), Uso(), "m")).stop_reason == "contenido_sensible"


res = {"objetos": 0, "a_bloqueados": [], "b_bloqueados": []}
for p in sorted((arbol / "bloque_a" / "02_System_prompts").glob("*.md")):
    for n, o in enumerate(objetos(p.read_text(encoding="utf-8"))):
        res["objetos"] += 1
        nombre = f"{p.name[:60]}#{n}"
        a = {**o, "solicitudes_credenciales": o.get("solicitudes_credenciales") or []}
        if bloqueado(a):
            res["a_bloqueados"].append(nombre)
        if bloqueado({**o, "solicitudes_credenciales": [SOL]}):
            res["b_bloqueados"].append(nombre)
print(json.dumps(res, ensure_ascii=False, indent=1))
