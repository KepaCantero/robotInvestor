"""QA r02 de T-126 (revisor sin contexto): medida propia del desempate por fecha en F7, F8 y F9, sin pasar por las funciones de
`test_t126_r02.py`.

Para cada sección `## TX-nn` y cada Q con empate, toma la secuencia de años de publicación (campo «Año») en el orden del
archivo y cuenta: (a) pares contiguos al revés (lo que mira la prueba), (b) pares al revés en toda la secuencia ignorando las
fichas sin año (lo que pide «a igualdad, la más reciente primero»), (c) fichas sin año en empates.

Uso, desde `bloque_a/11_Ejecutor`:  python ../../.docs/tickets/T-126/revisores/r02_01_desempate_medida.py
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.herramientas import ht02  # noqa: E402
from bloque_a.referencias import Referencias  # noqa: E402

RE_ANIO = re.compile(r"^\s*((?:19|20)\d{2})\b")
refs = Referencias(cargar_config())
for archivo in ("F7", "F8", "F9"):
    lineas = Path(refs.rutas[archivo]).read_text(encoding="utf-8").splitlines()
    inicio = {f.linea_inicio: f for f in ht02.leer_fichas(lineas)}
    grupos: dict = defaultdict(list)
    seccion, anios_raros = None, defaultdict(int)
    for i, ln in enumerate(lineas):
        m = re.match(r"^## (T[AMF]-\d{2})\b", ln)
        if m:
            seccion = m.group(1)
        if i in inicio:
            f = inicio[i]
            campo = f.campo("Año") or ""
            a = RE_ANIO.match(campo)
            if not a:
                anios_raros[campo.strip()[:30]] += 1
            grupos[(seccion, f.q)].append((f.id, int(a.group(1)) if a else None))
    contiguos = todos = sin_anio = 0
    ejemplos = []
    for (sec, q), fs in grupos.items():
        if len(fs) < 2:
            continue
        sin_anio += sum(1 for _, a in fs if a is None)
        for x, y in zip(fs, fs[1:]):
            if x[1] is not None and y[1] is not None and y[1] > x[1]:
                contiguos += 1
        con = [(i, a) for i, a in fs if a is not None]
        for k in range(len(con)):
            for j in range(k + 1, len(con)):
                if con[j][1] > con[k][1]:
                    todos += 1
                    if len(ejemplos) < 3:
                        ejemplos.append((sec, q, con[k], con[j]))
    print(f"{archivo} · fichas {sum(len(v) for v in grupos.values())} · al revés contiguos {contiguos} · al revés en toda la secuencia "
          f"{todos} · sin año en empates {sin_anio} · ejemplos {ejemplos} · campos «Año» que no empiezan por un año: {dict(anios_raros)}")

# La función de la prueba solo compara pares contiguos: una ficha sin año entre dos con año esconde un desempate al revés.
sys.path.insert(0, str(Path.cwd() / "tests"))
from test_t126_r02 import desempates_al_reves  # noqa: E402

trio = [{"ref_id": "X1", "seccion": "TA-01", "q": 90, "anio": 2010}, {"ref_id": "X2", "seccion": "TA-01", "q": 90, "anio": None},
        {"ref_id": "X3", "seccion": "TA-01", "q": 90, "anio": 2020}]
print(f"trío 2010 · sin año · 2020 con la misma Q: desempates_al_reves = {desempates_al_reves(trio)} (2010 va antes que 2020)")
