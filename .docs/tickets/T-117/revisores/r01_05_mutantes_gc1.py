"""QA r01 de T-117 · Mutantes de `diseno_v6.gc1()`, de la validación de `v6.gc1` y de los valores de `por_defecto.yaml`.

Uso:  python r01_05_mutantes_gc1.py <copia_desechable> [--solo G01,G02] [--suite "rutas de pytest"]
Por defecto ejecuta tests/test_t117_gc1.py; con --suite, esas rutas. Solo toca la copia desechable.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
D, Y = "bloque_a/diseno_v6.py", "config/por_defecto.yaml"
MUTANTES = [
    ("G01", D, "borde: >= umbral pasa a > umbral", 'if float(u["senales"][clave]) >= umbral and not pocas_familias(u)][:maxc]', 'if float(u["senales"][clave]) > umbral and not pocas_familias(u)][:maxc]'),
    ("G02", D, "el umbral del tipo se ignora (siempre el general)", 'umbral = float(propio if propio is not None else parametro(bloque.cfg, "seleccion.umbral_senal_gc1"))', 'umbral = float(parametro(bloque.cfg, "seleccion.umbral_senal_gc1"))'),
    ("G03", D, "familias: n < fam_min pasa a n <= fam_min", 'not isinstance(n, bool) and n < fam_min', 'not isinstance(n, bool) and n <= fam_min'),
    ("G04", D, "familias: se exige con cualquier señal", 'if clave == "senal_compuesta" else 0', 'if True else 0'),
    ("G05", D, "familias: nunca se exige", 'return fam_min > 0 and isinstance(n, int)', 'return False and isinstance(n, int)'),
    ("G06", D, "familias: sin recuento SÍ se descarta", 'return fam_min > 0 and isinstance(n, int) and not isinstance(n, bool) and n < fam_min', 'return fam_min > 0 and (n is None or (isinstance(n, int) and n < fam_min))'),
    ("G07", D, "familias: un booleano cuenta como entero", 'isinstance(n, int) and not isinstance(n, bool) and n < fam_min', 'isinstance(n, int) and n < fam_min'),
    ("G08", D, "el tope de candidatas se aplica ANTES del filtro de familias",
     'pasan = [u for u in orden if float(u["senales"][clave]) >= umbral and not pocas_familias(u)][:maxc]',
     'pasan = [u for u in [x for x in orden if float(x["senales"][clave]) >= umbral][:maxc] if not pocas_familias(u)]'),
    ("G09", D, "registro sin familias_min", '"umbral": umbral, "familias_min": fam_min, "universo"', '"umbral": umbral, "universo"'),
    ("G10", D, "registro con el umbral general en vez del usado", 'reg = {"clave_senal": clave, "umbral": umbral,', 'reg = {"clave_senal": clave, "umbral": float(parametro(bloque.cfg, "seleccion.umbral_senal_gc1")),'),
    ("G11", D, "motivo del descarte por familias sustituido por el de tope", 'else (f"{u[\'senales\'][\'familias_concordantes\']} familias concordantes < {fam_min}" if pocas_familias(u)', 'else (f"fuera de las {maxc} candidatas con más señal" if pocas_familias(u)'),
    ("G12", D, "validar: umbral 0 admitido", 'or not 0 < float(v) <= 1 for k, v in upp.items()', 'or not 0 <= float(v) <= 1 for k, v in upp.items()'),
    ("G13", D, "validar: umbral 1 rechazado", 'or not 0 < float(v) <= 1 for k, v in upp.items()', 'or not 0 < float(v) < 1 for k, v in upp.items()'),
    ("G14", D, "validar: umbral por encima de 1 admitido", 'or not 0 < float(v) <= 1 for k, v in upp.items()', 'or not 0 < float(v) for k, v in upp.items()'),
    ("G15", D, "validar: umbral no finito admitido", 'or not math.isfinite(float(v)) or not 0 < float(v) <= 1', 'or not 0 < float(v) <= 1'),
    ("G16", D, "validar: umbral booleano admitido", 'any(k not in CLASES or isinstance(v, bool) or not isinstance(v, (int, float))', 'any(k not in CLASES or not isinstance(v, (int, float))'),
    ("G17", D, "validar: tipo de activo desconocido admitido", 'any(k not in CLASES or isinstance(v, bool) or not isinstance(v, (int, float))', 'any(isinstance(v, bool) or not isinstance(v, (int, float))'),
    ("G18", D, "validar: umbral_por_perfil que no es diccionario admitido", 'if not isinstance(upp, dict) or any(k not in CLASES or isinstance(v, bool)', 'if isinstance(upp, dict) and any(k not in CLASES or isinstance(v, bool)'),
    ("G19", D, "validar: familias_min hasta 4", 'or not 0 <= fmin <= FAMILIAS_SENAL_COMPUESTA:', 'or not 0 <= fmin <= FAMILIAS_SENAL_COMPUESTA + 1:'),
    ("G20", D, "validar: familias_min negativo admitido", 'or not 0 <= fmin <= FAMILIAS_SENAL_COMPUESTA:', 'or not fmin <= FAMILIAS_SENAL_COMPUESTA:'),
    ("G21", D, "validar: familias_min booleano admitido", 'if isinstance(fmin, bool) or not isinstance(fmin, int) or not 0 <= fmin', 'if not isinstance(fmin, int) or not 0 <= fmin'),
    ("G22", D, "validar: familias_min no entero admitido", 'if isinstance(fmin, bool) or not isinstance(fmin, int) or not 0 <= fmin', 'if isinstance(fmin, bool) or not isinstance(fmin, (int, float)) or not 0 <= fmin'),
    ("G23", D, "validar: familias_min 0 rechazado y 3 rechazado", 'or not 0 <= fmin <= FAMILIAS_SENAL_COMPUESTA:', 'or not 0 < fmin < FAMILIAS_SENAL_COMPUESTA:'),
    ("G24", D, "un descartado por familias no puede llegar como exploración", 'resto = [u for u in orden if u["simbolo"] not in ids_pasan]', 'resto = [u for u in orden if u["simbolo"] not in ids_pasan and not pocas_familias(u)]'),
    ("G25", Y, "yaml: familias_min 2 → 1", 'familias_min: 2 ', 'familias_min: 1 '),
    ("G26", Y, "yaml: RF 0.65 → 0.66", 'umbral_por_perfil: {RF: 0.65, MON: 0.65, TCV: 0.65}', 'umbral_por_perfil: {RF: 0.66, MON: 0.65, TCV: 0.65}'),
    ("G27", Y, "yaml: se añade DER 0.65", 'umbral_por_perfil: {RF: 0.65, MON: 0.65, TCV: 0.65}', 'umbral_por_perfil: {RF: 0.65, MON: 0.65, TCV: 0.65, DER: 0.65}'),
    ("G28", Y, "yaml: umbral general 0.75 → 0.74", None, None),
    ("G29", Y, "yaml: IDX usa momentum_12_1", 'MP: senal_compuesta, IDX: senal_compuesta,', 'MP: senal_compuesta, IDX: momentum_12_1,'),
    ("G30", D, "familias: se compara con FAMILIAS_SENAL_COMPUESTA en vez de familias_min", 'not isinstance(n, bool) and n < fam_min', 'not isinstance(n, bool) and n < FAMILIAS_SENAL_COMPUESTA - 1'),
]


def main() -> int:
    copia = Path(sys.argv[1]).resolve()
    assert "qa_f3_mut" in str(copia), "solo en la copia desechable"
    solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
    suite = sys.argv[sys.argv.index("--suite") + 1].split() if "--suite" in sys.argv else ["tests/test_t117_gc1.py"]
    ej = copia / "bloque_a" / "11_Ejecutor"
    vivos = []
    for mid, fich, desc, viejo, nuevo in MUTANTES:
        if solo and mid not in solo:
            continue
        ruta = ej / fich
        original = ruta.read_text(encoding="utf-8")
        if mid == "G28":
            import re
            m = re.search(r"^( *umbral_senal_gc1: *)0\.75", original, flags=re.MULTILINE)
            viejo, nuevo = (m.group(0), m.group(1) + "0.74") if m else ("<no hallado>", "")
        if original.count(viejo) != 1:
            print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}"); continue
        try:
            ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([PY, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *suite], cwd=ej, capture_output=True, text=True, timeout=1800)
            ult = (r.stdout + r.stderr).strip().splitlines()[-1][:110]
            falla = next((x for x in r.stdout.splitlines() if x.startswith("FAILED") or x.startswith("ERROR")), "")[:150]
            print(f"{mid} · {'MUERTO' if r.returncode else 'VIVO  '} · {desc} · {ult} {falla}", flush=True)
            if r.returncode == 0:
                vivos.append(mid)
        finally:
            ruta.write_text(original, encoding="utf-8")
    print("vivos: " + (", ".join(vivos) or "ninguno"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
