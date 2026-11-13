"""Promueve en el Catálogo del Motor (Bloque A) las fichas que superan sus casos de control (§20.2: «Paso a IMPLEMENTADO»).

T-106, autorizado por el operador el 12-11-2026. El script:
1. ejecuta `Motor.verificar_casos_control` sobre un almacén temporal (los casos quedan registrados en su RC);
2. para cada ficha que los supera y que el Catálogo da por «Documentado» o, desde T-112, por «Implementado (heredado)»,
   cambia su fila de la tabla del §4 y su línea «Prioridad y madurez» a IMPLEMENTADO con la etiqueta indicada;
3. recalcula el recuento del §1.3.

Una ficha que no los supera queda como estaba, y se informa. Después hay que volver a congelar el corpus
(`./tools/check_all.sh --update-corpus`) en el mismo commit, con el motivo en el mensaje.

Uso (desde la raíz del repositorio):
  .venv/bin/python -I .docs/scripts/promover_fichas_catalogo.py [--aplicar] [--etiqueta "…"] [FICHA ...]
Sin --aplicar solo informa. Sin fichas, las que tienen casos de control.
"""
from __future__ import annotations

import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EJEC = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJEC))

from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio

CATALOGO = RAIZ / "bloque_a" / servicio.RUTA_CATALOGO[0] / servicio.RUTA_CATALOGO[1]
ETIQUETA = "ejecutor, casos de control registrados (T-106)"


def main(argv: list[str]) -> int:
    aplicar = "--aplicar" in argv
    etiqueta = argv[argv.index("--etiqueta") + 1] if "--etiqueta" in argv else ETIQUETA
    fichas = [a for a in argv if re.fullmatch(r"[A-Z]+(?:-[A-Z0-9]+)+-\d{3}", a)] or sorted(set(servicio.CASOS_CONTROL) | servicio.SERVICIOS_CT10)

    class _Proveedor:   # los casos de control llevan sus datos en línea: no se lee ninguna serie
        as_of = None
        nombre = "casos_control"

    with tempfile.TemporaryDirectory() as d:
        motor = servicio.Motor(Almacen(Path(d)), _Proveedor(), cargar_config())
        res = motor.verificar_casos_control(fichas, run_id="PROMOCION-CATALOGO")
    texto = CATALOGO.read_text(encoding="utf-8")
    promovidas, fallidas = [], []
    for f in fichas:
        r = res[f]
        casos = ", ".join(("✓ " if c["superado"] else "✗ ") + str(c["nombre"]) for c in r["casos"])
        print(f"{'SUPERA' if r['superados'] else 'NO SUPERA'} {f}: {casos}")
        if not r["superados"]:
            fallidas.append(f)
            continue
        if (servicio.madurez_catalogo(RAIZ / "bloque_a").get(f) or "").startswith(("IMPLEMENTADO", "VALIDADO")):
            continue   # ya promovida (por ejemplo, la Fase 1 al promover la Fase 2): no se cuenta ni se toca
        fila = re.compile(rf"^(\| {re.escape(f)} \|.*\| P\d \| )(?:Documentado|Implementado \(heredado\))( \|\s*)$", re.MULTILINE)
        linea = re.compile(rf"(^### {re.escape(f)} ·.*?\*\*Prioridad y madurez\.\*\* P\d · )(?:DOCUMENTADO|Implementado \(heredado\))\.",
                           re.MULTILINE | re.DOTALL)
        t2, n1 = fila.subn(rf"\g<1>IMPLEMENTADO ({etiqueta})\g<2>", texto)
        t3, n2 = linea.subn(rf"\g<1>IMPLEMENTADO ({etiqueta}).", t2, count=1)
        if n1 != 1 or n2 != 1:
            print(f"  {f}: no se encuentra «Documentado» en la fila ({n1}) o en la ficha ({n2}); no se toca")
            continue
        texto = t3
        promovidas.append(f)
    # §1.3: recuento a partir de la tabla
    mad = Counter()
    for m in re.finditer(r"^\| [A-Z]+(?:-[A-Z0-9]+)+-\d{3} \|.*\| P\d \| ([^|]+?) \|\s*$", texto, re.MULTILINE):
        v = m.group(1)
        mad["impl" if v.startswith("IMPLEMENTADO") else "her" if v.startswith("Implementado") else "doc" if v.startswith("Documentado") else "otro"] += 1
    v40 = sum(1 for m in re.finditer(r"^\| ([A-Z]+(?:-[A-Z0-9]+)+-\d{3}) \|.*\| Documentado \|\s*$", texto, re.MULTILINE)
              if not re.match(r"(IDX|FON|MON|TCV)-|DER-(VRP|SKEW|TERM|ROLL)-", m.group(1)))
    v50 = mad["doc"] - v40
    heredadas = (f"{mad['her']} heredadas de la línea V3.0 como **Implementado (heredado)**, pendientes de reverificación en el "
                 f"despliegue vigente; ") if mad["her"] else ""
    nuevo = (f"Estado actual de las {sum(mad.values())} fichas: {mad['impl']} **IMPLEMENTADO** (14 del ejecutor V1.0 con pruebas "
             f"unitarias y {mad['impl'] - 14} con casos de control registrados, T-106 y T-112); {heredadas}{mad['doc']} **DOCUMENTADO** "
             f"({v40} de la línea V4.0" + (f" y {v50} de las fichas de los tipos IDX, FON, DER, MON y TCV incorporadas en V5.0" if v50 else "")
             + "). Ninguna ficha está VALIDADA.")
    texto = re.sub(r"^Estado actual de las \d+ fichas:.*$", nuevo, texto, count=1, flags=re.MULTILINE)
    print(f"\nPromovidas: {len(promovidas)} · No superan: {fallidas}\n§1.3 → {nuevo}")
    if aplicar:
        CATALOGO.write_text(texto, encoding="utf-8")
        print(f"Escrito {CATALOGO.relative_to(RAIZ)}. Falta re-congelar el corpus en el mismo commit (--update-corpus).")
    return 0 if not fallidas else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
