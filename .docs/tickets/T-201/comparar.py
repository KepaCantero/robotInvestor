"""T-201: compara dos árboles de resultados del ejecutor byte a byte, salvo rutas temporales y latencias.

Uso: comparar.py <resultados_base> <resultados_nuevo> <raiz_base> <raiz_nuevo>
Normaliza solo (r02, QA r01 de T-201, H-01): (1) las rutas de cada lado (resultados y raíz del paquete) a un marcador común;
(2) las dos latencias por su nombre exacto, `latencia_s` y `tiempo_respuesta_s` (su valor, no su presencia), y la columna
`latencia_s` de `consumo.csv`; (3) los resúmenes encadenados. Ningún instante ni ningún otro campo se enmascara: las dos
ejecuciones de `equivalencia.sh` corren a la vez, así que lo que lleva la fecha del reloj (F10) coincide. Todo lo demás tiene que
coincidir byte a byte.
"""
import re
import sys
from pathlib import Path

R_BASE, R_NUEVO, RAIZ_BASE, RAIZ_NUEVO = (Path(a) for a in sys.argv[1:5])
# las dos latencias (segundos de pared), por su nombre exacto; se cambia su valor por «T», no la clave
LATENCIAS = re.compile(rb'("(?:latencia_s|tiempo_respuesta_s)"\s*:\s*)("[^"]*"|-?[0-9.eE+-]+)')
# consumo.csv: la última columna es `latencia_s` (segundos de pared)
LATENCIA_CSV = re.compile(rb"^(RUN-[^\r\n]*,)[0-9.]+(\r?)$", re.MULTILINE)


# resúmenes encadenados (`_hash`, `_hash_prev` y los sellos de integridad): se calculan sobre entradas que llevan rutas e
# instantes de reloj, así que difieren aunque lo demás coincida; se enmascara el resumen y se compara el resto (incluido el
# número de entradas de cada sello). El contenido que resumen se compara normalizado, entrada a entrada
RESUMEN = re.compile(rb'("_hash(?:_prev)?"\s*:\s*)"[0-9a-f]{64}"|(\[\d+, )"[0-9a-f]{64}"')


def volcar_sqlite(p: Path) -> bytes:
    import sqlite3
    con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    try:
        return "\n".join(con.iterdump()).encode()
    finally:
        con.close()


def normalizar(datos: bytes, lado_r: Path, lado_raiz: Path) -> bytes:
    datos = RESUMEN.sub(lambda m: (m.group(1) or m.group(2)) + b'"H"', datos)
    for p, marca in ((lado_r, b"<RES>"), (lado_raiz, b"<RAIZ>"), (lado_raiz.resolve(), b"<RAIZ>")):
        datos = datos.replace(str(p).encode(), marca)
    datos = LATENCIAS.sub(rb'\1"T"', datos)
    datos = LATENCIA_CSV.sub(rb"\1T\2", datos)
    return datos


def ficheros(raiz: Path) -> dict[str, Path]:
    return {str(p.relative_to(raiz)): p for p in sorted(raiz.rglob("*")) if p.is_file()}


fb, fn = ficheros(R_BASE), ficheros(R_NUEVO)
solo = sorted(set(fb) ^ set(fn))
distintos = []
for nombre in sorted(set(fb) & set(fn)):
    leer = volcar_sqlite if nombre.endswith(".sqlite3") else (lambda p: p.read_bytes())
    a = normalizar(leer(fb[nombre]), R_BASE, RAIZ_BASE)
    b = normalizar(leer(fn[nombre]), R_NUEVO, RAIZ_NUEVO)
    if a != b:
        distintos.append(nombre)
        la, lb = a.splitlines(), b.splitlines()
        for i, (x, y) in enumerate(zip(la, lb)):
            if x != y:
                print(f"  {nombre}:{i + 1}\n    base : {x[:300]!r}\n    nuevo: {y[:300]!r}")
                break
        else:
            print(f"  {nombre}: {len(la)} frente a {len(lb)} líneas")
crudos = sum(fb[n].read_bytes() == fn[n].read_bytes() for n in set(fb) & set(fn))
print(f"ficheros: {len(fb)} base, {len(fn)} nuevo; idénticos sin normalizar: {crudos}; solo en un lado: {solo}")
print(f"distintos tras normalizar: {distintos}")
for n in ("01_backtest.out", "02_ciclo.out", "03_peticion.out", "04_consulta.out", "05_seg_alta.out", "06_seg_ejecutar.out"):
    print(f"  {n}: {fb[n].read_text(encoding='utf-8', errors='replace')[-160:]!r}" if n in fb else f"  {n}: FALTA")
print("VEREDICTO:", "EQUIVALENTE" if not distintos and not solo else "DISTINTO")
sys.exit(0 if not distintos and not solo else 1)
