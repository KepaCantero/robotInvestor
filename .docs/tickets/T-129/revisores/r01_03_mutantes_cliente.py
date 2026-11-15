"""QA r01 de T-129 · mutantes del cliente real: ¿`test_t129_modo_sombra.py` falla si el cliente envía lo que la familia 5.5
rechaza con un 400? Cada mutante cambia `bloque_a/llm.py` (o la configuración) en una COPIA DESECHABLE y ejecuta la prueba.

Uso: python -I r01_03_mutantes_cliente.py <copia desechable de la raíz del repo, con «qa11_mut» en la ruta>
Restaura cada fichero tras su mutante.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa11_mut" in str(COPIA), "solo en una copia desechable"
EJE = COPIA / "bloque_a" / "11_Ejecutor"
LLM = EJE / "bloque_a" / "llm.py"
CFG = EJE / "config" / "por_defecto.yaml"
ANCLA = '"metadata": {"user_id": f"bloque-a-{agente}"}}'

MUTANTES = [
    ("temperature", LLM, ANCLA, ANCLA + '\n        kwargs["temperature"] = 0.0'),
    ("top_p", LLM, ANCLA, ANCLA + '\n        kwargs["top_p"] = 0.9'),
    ("top_k", LLM, ANCLA, ANCLA + '\n        kwargs["top_k"] = 5'),
    ("thinking desactivado", LLM, ANCLA, ANCLA + '\n        kwargs["thinking"] = {"type": "disabled"}'),
    ("thinking con presupuesto", LLM, ANCLA, ANCLA + '\n        kwargs["thinking"] = {"type": "enabled", "budget_tokens": 2000}'),
    ("tool_choice any", LLM, 'kwargs["tools"] = herramientas', 'kwargs["tools"] = herramientas; kwargs["tool_choice"] = {"type": "any"}'),
    ("tool_choice tool", LLM, 'kwargs["tools"] = herramientas',
     'kwargs["tools"] = herramientas; kwargs["tool_choice"] = {"type": "tool", "name": "web_search"}'),
    ("prefill de asistente", LLM, "msgs = list(mensajes)", 'msgs = list(mensajes) + [{"role": "assistant", "content": "{"}]'),
    ("thinking dentro de extra_body", LLM, ANCLA, ANCLA + '\n        kwargs["extra_body"] = {"thinking": {"type": "disabled"}}'),
    ("effort inválido en output_config", LLM, ANCLA, ANCLA + '\n        kwargs["output_config"] = {"effort": "ninguno"}'),
    ("búsqueda en todos los agentes", LLM, "if herramientas:", "herramientas = herramientas or [{'type': 'web_search_20260318', 'name': 'web_search'}]\n        if herramientas:"),
    ("metadata con el nombre del operador", LLM, 'f"bloque-a-{agente}"', 'f"bloque-a-{agente}-operador@ejemplo.org"'),
    ("max_tokens 64000 sin streaming", LLM, '"max_tokens": int(max_tokens)', '"max_tokens": 64000'),
    ("herramienta antigua web_search_20250305", CFG, "tipo_herramienta: web_search_20260318", "tipo_herramienta: web_search_20250305"),
    ("modelo retirado en la configuración", CFG, "por_defecto: claude-sonnet-5-5", "por_defecto: claude-sonnet-4-5"),
]

vivos = []
for nombre, fichero, viejo, nuevo in MUTANTES:
    original = fichero.read_text(encoding="utf-8")
    assert original.count(viejo) >= 1, (nombre, viejo)
    fichero.write_text(original.replace(viejo, nuevo, 1), encoding="utf-8")
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t129_modo_sombra.py"],
                           cwd=EJE, capture_output=True, text=True, timeout=900)
    finally:
        fichero.write_text(original, encoding="utf-8")
    muerto = p.returncode != 0
    print(f"{'muerto' if muerto else 'VIVO  '} · {nombre} · {p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:]}")
    if not muerto:
        vivos.append(nombre)
print(f"\nr01_03 T-129: {len(MUTANTES) - len(vivos)}/{len(MUTANTES)} mutantes muertos; vivos: {vivos}")
