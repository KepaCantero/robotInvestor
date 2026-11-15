"""Comprueba una carpeta de datos históricos contra el universo del Bloque A antes de usarla (punto 7 de las tareas del
15-11-2026). Sirve para la fuente de datos reales que elija el operador: el ejecutor ya lee CSV genéricos (HT-01,
`ProveedorCSV`: columnas `fecha` y `cierre` como mínimo, con alias como `Date`/`Close`), y este script dice, símbolo a
símbolo, si la carpeta sirve sin tener que lanzar un ciclo.

Para cada símbolo del universo: OK, FALTA (no hay archivo), INVALIDO (HT-01 lo rechaza, con su motivo) o ANTIGUO (su
último cierre a la fecha as_of tiene más días, o sesiones en H1, que `ps2_antiguedad_maxima_dias` del horizonte pedido,
Anexo A); se valida como en el ciclo (`cierres()` de HT-01: cierres positivos y finitos, sin fechas repetidas); su primera
y última fecha, el número de filas y el mayor hueco entre dos fechas. Al final, cuántos símbolos sirven por tipo de activo.

Uso (desde la raíz):
  .venv/bin/python .docs/scripts/comprobar_datos_a.py <carpeta> [--universo csv] [--as-of AAAA-MM-DD] [--horizonte H3]
Termina con 0 si todos los símbolos están OK, con 1 si no y con 2 si la carpeta no existe.
"""
import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR))

from bloque_a.calendario import _sesiones_entre, validar_festivos_ps2  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, parametro  # noqa: E402
from bloque_a.herramientas.ht01_datos import (  # noqa: E402
    DatosInvalidos,
    DatosNoDisponibles,
    ProveedorCSV,
    cargar_universo,
)


def comprobar(carpeta: str | Path, universo: pd.DataFrame, as_of: str, horizonte: str = "H3",
              cfg: dict | None = None) -> list[dict]:
    cfg = cfg or cargar_config()
    max_dias = int(parametro(cfg, f"ps2_antiguedad_maxima_dias.{horizonte}"))
    festivos = validar_festivos_ps2(parametro(cfg, "ps2_festivos"))
    prov = ProveedorCSV(carpeta)
    prov.fijar_as_of(as_of)
    corte = pd.Timestamp(as_of).normalize()
    filas = []
    for _, u in universo.iterrows():
        f = {"simbolo": u["simbolo"], "clase": u["clase"], "estado": "OK", "motivo": "", "desde": None, "hasta": None,
             "filas": 0, "mayor_hueco_dias": None}
        try:
            # T-131 r02 (QA r01, H-01): con `cierres()`, como el ciclo, que rechaza cierres no numéricos, a cero o negativos y
            # fechas repetidas en el rango; `serie()` no valida las filas
            s = prov.cierres(u["simbolo"])
        except DatosInvalidos as e:            # antes que DatosNoDisponibles, que es su clase madre
            f.update(estado="INVALIDO", motivo=str(e))
        except DatosNoDisponibles as e:
            f.update(estado="FALTA", motivo=str(e))
        else:
            if s.empty:
                f.update(estado="FALTA", motivo="sin observaciones hasta as_of")
            else:
                idx = pd.DatetimeIndex(s.index)
                f.update(desde=idx.min().date().isoformat(), hasta=idx.max().date().isoformat(), filas=len(idx),
                         mayor_hueco_dias=int(idx.to_series().diff().dt.days.max()) if len(idx) > 1 else 0)
                # H-03: en H1 la antigüedad se cuenta en sesiones, sin los cierres habituales de mercado, como el ejecutor
                ultimo = idx.max().normalize()
                antiguedad = _sesiones_entre(ultimo, corte, festivos) if horizonte == "H1" else (corte - ultimo).days
                unidad = "sesiones" if horizonte == "H1" else "días"
                if antiguedad > max_dias:
                    f.update(estado="ANTIGUO", motivo=f"último cierre hace {antiguedad} {unidad} (máximo {max_dias} en {horizonte})")
        filas.append(f)
    return filas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--universo", default=str(RUTA_UNIVERSO_EJEMPLO))
    ap.add_argument("--as-of", default=pd.Timestamp.today().date().isoformat())
    ap.add_argument("--horizonte", default="H3", choices=["H1", "H2", "H3", "H4", "H5"])
    a = ap.parse_args(argv)
    if not Path(a.carpeta).is_dir():   # H-04: un mensaje, no una traza
        print(f"no existe la carpeta de datos {a.carpeta}", file=sys.stderr)
        return 2
    filas = comprobar(a.carpeta, cargar_universo(a.universo), a.as_of, a.horizonte)
    for f in filas:
        if f["estado"] != "OK":
            print(f"{f['estado']:9} {f['clase']:4} {f['simbolo']:14} {f['motivo'][:110]}")
    por_clase: dict[str, Counter] = defaultdict(Counter)
    for f in filas:
        por_clase[f["clase"]][f["estado"]] += 1
    print(f"\nas_of {a.as_of}, horizonte {a.horizonte}: {sum(f['estado'] == 'OK' for f in filas)} de {len(filas)} símbolos OK")
    for clase, c in sorted(por_clase.items()):
        print(f"  {clase:4} OK {c['OK']:3} · falta {c['FALTA']:3} · inválido {c['INVALIDO']:3} · antiguo {c['ANTIGUO']:3}")
    return 0 if all(f["estado"] == "OK" for f in filas) else 1


if __name__ == "__main__":
    sys.exit(main())
