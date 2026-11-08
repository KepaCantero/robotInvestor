"""Hallazgo 1 (T-40): la semana se suma con math.fsum y un sumatorio que desborda mata el registro de la foto (O-00) y deja al cortacircuito sin disparar.

`_perdida_semana_eur` (nuevo en T-40) devuelve `math.fsum(...)` de `self.perdidas_dia`.
`math.fsum` lanza `OverflowError: intermediate overflow in fsum` cuando el resultado sale del
rango float. Las pérdidas que provocan ese desbordamiento son finitas y pasan todas las
validaciones de la foto (O-01: `_num` exige solo finito y >= 0), así que llegan al bloque del
cortacircuito, que va DESPUÉS de guardar la foto, anotar su alcance y podar: la excepción sale de
`registrar_cartera`, `_seguro` la convierte en O-00 y deshace TODO el registro. Consecuencias,
contra lo que dice el diseño («la foto es buena y el registro se acepta igual», kill + O-38 +
fila cuando la semana esté en el límite):

  1) La foto válida se RECHAZA con O-00 en vez de aceptarse con `cortacircuito: True`.
  2) El cortacircuito NO dispara ese día: ni kill, ni O-38, ni fila (y tras un rearme, tampoco
     volvería a saltar): falla justo en la pérdida más extrema, que es su trabajo.
  3) Con la política por defecto el daño queda atenuado (el día anterior ya activó el kill), pero
     con una política válida de límites altos (1.7e308/1.75e308; `politica_valida` solo exige > 0)
     el cortacircuito NO LLEGA A DISPARARSE NUNCA aunque la pérdida semanal real supere su límite.

Es el mismo patrón que la revisión de T-33 ya corrigió en F-14 (defecto_02: «suma plana de
flotantes (no fsum): un importe desbordado da infinito y F-14 lo cierra, sin lanzar»); los dos
sumatorios de la semana (el del helper nuevo y el copiado en `_actividad`, línea 710) siguen con fsum.

Guion (dos escenarios):
  A) Política por defecto. Día 1: foto con pérdida 1e308 (finita, válida) -> se acepta, kill y O-38.
     Día 2: foto con pérdida 1e308 -> O-00, sin fila del día 2 ni O-38 nuevo; el registro muere.
  B) Política con límites 1.7e308/1.75e308 (válida). Día 1: foto de 9.9e307 (bajo el límite del día)
     -> aceptada. Día 2: foto de 9.9e307 -> la semana real (1.98e308) SUPERABA el límite semanal
     (1.75e308) y el cortacircuito debía saltar; en su lugar O-00, sin kill, sin O-38, sin fila,
     y ningún reintento con pérdida extrema llega nunca a dispararlo.

Ejecución: python3 hallazgo_t40_1_fsum_semana_desborda.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe; OK si está corregido (las fotos se aceptan y el cortacircuito
dispara: p. ej. con la suma plana de defecto_02 el desbordamiento da inf y `salta` sería True).
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from control_f import POLITICA_DEFECTO  # noqa: E402
from pruebas_control_f import CART  # noqa: E402
from pruebas_orquestador import nuevo  # noqa: E402

L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}


def foto(o, t, perdida, ahora):
    """Lo que hace G: registrar una foto de cartera válida (pasa la O-01: pérdida finita y >= 0)."""
    return o.registrar_cartera({**CART, "fecha_hora": t, "perdida_dia_eur": perdida}, "G", ahora,
                               cuenta=o.cfg["cuenta_intermediario"])


def main():
    # A) política por defecto (perdida_dia_max_eur 2.500, perdida_semana_max_eur 5.000)
    o = nuevo(L2, sellos=())   # sin sellos: el reloj arranca libre (las fotos son de días anteriores a las 09:00)
    r1 = foto(o, "2026-11-05T09:00:00+00:00", 1e308, "2026-11-05T09:00:30+00:00")
    assert r1["ok"] and r1["cortacircuito"] is True and o.kill is not None, (r1, o.kill)
    o38_dia1 = len([a for a in o.avisos if a["codigo"] == "O-38"])
    r2 = foto(o, "2026-11-06T09:00:00+00:00", 1e308, "2026-11-06T09:00:30+00:00")   # misma pérdida extrema, día siguiente
    print(f"A  día 1: {r1['codigo']} (cortacircuito={r1.get('cortacircuito')}, kill activo) | "
          f"día 2: {r2['codigo']} — {r2['motivo'][:80]}")
    print(f"A  estado tras el rechazo: filas={[(x['dia']) for x in o.cortacircuitos]}, "
          f"avisos O-38={len([a for a in o.avisos if a['codigo'] == 'O-38'])} (antes {o38_dia1}), "
          f"última foto={o.ultima_foto['fecha_hora']}")

    # B) política válida con límites altos: el cortacircuito debía saltar por la semana y nunca salta
    o2 = nuevo({**L2, "politica_f": {**POLITICA_DEFECTO, "perdida_dia_max_eur": 1.7e308, "perdida_semana_max_eur": 1.75e308}}, sellos=())
    f1 = foto(o2, "2026-11-05T09:00:00+00:00", 9.9e307, "2026-11-05T09:00:30+00:00")   # bajo el límite del día: OK, sin salto
    f2 = foto(o2, "2026-11-06T09:00:00+00:00", 9.9e307, "2026-11-06T09:00:30+00:00")   # semana real 1.98e308 >= 1.75e308
    print(f"B  día 1: {f1['codigo']} (cortacircuito={f1.get('cortacircuito')}) | día 2: {f2['codigo']} — {f2['motivo'][:60]} "
          f"| kill={o2.kill is not None}, filas={[(x['dia']) for x in o2.cortacircuitos]}")

    if not r2["ok"] or not f2["ok"]:
        print("FALLA  math.fsum desborda en _perdida_semana_eur y registrar_cartera rechaza con O-00 fotos válidas: "
              "la foto no se acepta (el diseño la acepta con cortacircuito=True) y el cortacircuito no dispara "
              "ni kill, ni O-38, ni fila ese día; en B la pérdida semanal real superaba el límite y el cortacircuito "
              "no llega a saltar nunca")
        return 1
    print("OK  las fotos se aceptan y el cortacircuito dispara")
    return 0


if __name__ == "__main__":
    sys.exit(main())
