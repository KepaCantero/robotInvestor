"""QA r01 de T-199 (revisor): prueba candidata para ST-INF-001 que cuenta evaluaciones de la potencia en vez de medir tiempo.

Mata M12 y M13 de `mutantes.py` sin depender de la carga: con la aproximación, el caso d = 0.05 (aprox > cota) no evalúa
ninguna potencia de búsqueda y el caso d = 0.06 (aprox ≤ cota) evalúa unas pocas alrededor de la aproximación.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-199/revisores/r01_02_test_st_inf_cuenta.py --rootdir=.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))
from bloque_a.motor import fichas_series as S  # noqa: E402
from test_fase2_series import _correr  # noqa: E402

TOPE = 50
V = {"contrastes": [{"nombre": "a", "muestra": [0.3, 1.2, -0.4, 0.8, 1.9, 0.1]}]}


def _evaluaciones(monkeypatch, d):
    original, n = S._potencia_t, [0]

    def contada(*a, **k):
        n[0] += 1
        assert n[0] <= TOPE, f"más de {TOPE} evaluaciones de la potencia"   # corta en seguida un mutante cuadrático
        return original(*a, **k)
    monkeypatch.setattr(S, "_potencia_t", contada)
    r, _ = _correr("ST-INF-001", V, {"tipo_contraste": "t_una_muestra", "efecto_potencia": d, "potencia_objetivo": 0.8})
    monkeypatch.setattr(S, "_potencia_t", original)
    return n[0], r["contrastes"]["a"]["potencia"]["n_minimo"]


def test_st_inf_la_busqueda_del_n_minimo_empieza_en_la_aproximacion(monkeypatch):
    for d in (0.05, 1e-300):
        evals, n_min = _evaluaciones(monkeypatch, d)
        assert n_min is None and evals <= 1, (d, evals)     # solo la potencia de la muestra; ninguna de búsqueda
    evals, n_min = _evaluaciones(monkeypatch, 0.06)
    assert n_min is not None and evals <= 20, evals          # unas pocas alrededor de la aproximación (cota: 2 520)
