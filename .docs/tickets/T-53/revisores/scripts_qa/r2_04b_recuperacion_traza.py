"""r2_04b · Traza de r2_04 (3a): tras restituir «SI» en F10, ¿qué tabla recibe el Analista y por qué las opciones siguen sin H5?
Se registra el valor de H5 en `horizontes_aplicables_clase` de cada mensaje al Analista (mock) y la fase de cada ciclo."""
import pathlib, sys
from bloque_a import mock_respuestas as mr
sys.path.insert(0, str(pathlib.Path(__file__).parent))
traza = []
orig = mr._horizontes
def _h(msg):
    traza.append((msg.get("fase"), (msg.get("horizontes_aplicables_clase") or {}).get("H5")))
    return orig(msg)
mr._horizontes = _h
import builtins
_print = builtins.print
def p(*a, **k):
    _print(*a, **k); _print("      mensajes al Analista (fase, H5):", sorted(set(traza))); traza.clear()
builtins.print = p
exec(compile(pathlib.Path(__file__).with_name("r2_04_degradacion_y_recuperacion.py").read_text(encoding="utf-8"), "r2_04", "exec"))
