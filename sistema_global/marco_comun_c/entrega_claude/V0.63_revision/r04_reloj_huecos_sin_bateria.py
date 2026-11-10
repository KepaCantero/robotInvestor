"""T-84, QA r01 de la V0.63: dos propiedades del Reloj que la semana usa y que ninguna batería del marco fija (las mutaciones
R04 y R06 de r01_mutaciones_semana.py quedan vivas en todas). El código actual las cumple; esta sonda las deja escritas para
que se conviertan en pruebas.

  1. contrastar da el MAYOR de reloj y referencia (docstring de reloj.py): con el reloj 3 s por delante del intermediario, el
     instante es el del reloj, no el de la referencia.
  2. Un salto del reloj de pared tras un día de marcha: la deriva tolerada desde el ancla ya es de 2 + 0,0005 × 86400 = 45 s,
     así que un salto de 10 s solo lo para la comprobación entre dos lecturas seguidas (max_salto_s = 2 s). Sin ella pasaría.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.63_revision/r04_reloj_huecos_sin_bateria.py
"""
import sys
from datetime import datetime
from pathlib import Path

MARCO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MARCO / "validador"))
import reloj as rl  # noqa: E402

T0 = datetime.fromisoformat("2026-11-09T08:00:00+00:00").timestamp()


class F:
    def __init__(self):
        self.p, self.m = T0, 1000.0

    def pared(self):
        return self.p

    def mono(self):
        return self.m


def iso(s):
    return datetime.fromtimestamp(s, rl.timezone.utc).isoformat()


def main():
    fallos = 0
    f = F()
    r = rl.Reloj(f.pared, f.mono)
    c = r.contrastar(iso(T0 - 3), "INTERMEDIARIO")   # el intermediario va 3 s por detrás del reloj
    ok1 = c["ok"] and c["ahora"] == iso(T0)
    print("OK   " if ok1 else "FALLA", "1 contrastar da el mayor de reloj y referencia (el reloj, 3 s por delante)", "" if ok1 else c)
    fallos += not ok1

    f = F()
    r = rl.Reloj(f.pared, f.mono)
    r.contrastar(iso(T0), "INTERMEDIARIO")
    for _ in range(24):                               # un día de marcha, una lectura por hora, con contraste
        f.p += 3600
        f.m += 3600
        assert r.contrastar(iso(f.p), "INTERMEDIARIO")["ok"]
    f.p += 10                                         # alguien adelanta la hora 10 s (el monótono no)
    a = r.ahora()
    ok2 = a["codigo"] == "RL-01" and a["ahora"] is None
    print("OK   " if ok2 else "FALLA", "2 tras un día de marcha, un salto de 10 s del reloj de pared se para (RL-01)", "" if ok2 else a)
    fallos += not ok2
    print("RESULTADO r04:", "LAS DOS PROPIEDADES SE CUMPLEN (faltan como pruebas)" if not fallos else "HAY FALLOS")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
