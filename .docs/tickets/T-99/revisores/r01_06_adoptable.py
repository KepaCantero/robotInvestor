"""r01_06 · Regla de «adoptable»: intento anterior al prerregistro por reloj, variantes fuera del máximo, repetición de la
misma variante (T-133, H-21 de la QA r03 de T-94), resultados mezclados y la comparación de fechas como texto.
Uso: python3 -B r01_06_adoptable.py <raíz>"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ANTES, DESPUES, caso, fin, pre, registro_temporal  # noqa: E402


def exp(max_variantes=1, creado=AHORA):
    reg = registro_temporal()
    return reg, reg.prerregistrar(pre(max_variantes=max_variantes), "qa", creado)["exp_id"]


def anotar(reg, e, variante, veredicto, inicio=DESPUES):
    n = reg.intento(e, variante, inicio)["n"]
    if veredicto:
        reg.resultado(e, n, veredicto, ahora=DESPUES)
    return n


# 1. Intento anterior al prerregistro por reloj (inyectado): no adoptable
reg, e = exp(); anotar(reg, e, "v1", "mejor", ANTES)
caso("intento con inicio anterior al prerregistro: no adoptable", not reg.adoptable(e))
# 1b. mismo segundo: adoptable (>=)
reg, e = exp(); anotar(reg, e, "v1", "mejor", AHORA)
caso("intento en el mismo segundo que el prerregistro: adoptable (borde >=)", reg.adoptable(e))

# 2. Fechas en otra zona: la comparación es de texto
reg, e = exp(creado="2026-11-12T10:00:00-02:00")          # 12:00 UTC
anotar(reg, e, "v1", "mejor", "2026-11-12T11:00:00+00:00")  # 11:00 UTC: UNA HORA ANTES del prerregistro
caso("intento una hora ANTES del prerregistro escrito en otra zona: no adoptable", not reg.adoptable(e),
     "adoptable: compara «2026-11-12T11…» con «2026-11-12T10…» como texto" if reg.adoptable(e) else "")
reg, e = exp(creado="2026-11-12T10:00:00+00:00")
anotar(reg, e, "v1", "mejor", "2026-11-12T09:30:00-02:00")  # 11:30 UTC: después
caso("intento después del prerregistro escrito en otra zona: adoptable", reg.adoptable(e),
     "no adoptable por la comparación de texto (falla hacia el lado seguro)" if not reg.adoptable(e) else "")
reg, e = exp(creado="2026-11-12T10:00:00Z")
anotar(reg, e, "v1", "mejor", "2026-11-12T10:00:00+00:00")
caso("«Z» y «+00:00» en el mismo instante: adoptable", reg.adoptable(e),
     "«+00:00» < «Z» como texto" if not reg.adoptable(e) else "")
reg, e = exp(creado="ayer")
anotar(reg, e, "v1", "mejor", DESPUES)
caso("un «ahora» inyectado que no es una fecha se rechaza", False, f"se aceptó creado_en='ayer' y adoptable={reg.adoptable(e)}")

# 3. Variantes fuera del máximo
reg, e = exp(2)
for v, ver in (("v1", "peor"), ("v2", "peor"), ("v3", "mejor")):
    anotar(reg, e, v, ver)
caso("la tercera variante con max 2 gana: no adoptable (CA-4)", not reg.adoptable(e))
reg, e = exp(2)
anotar(reg, e, "v1", "peor"); anotar(reg, e, "v3", "peor"); anotar(reg, e, "v2", "peor"); anotar(reg, e, "v1", "mejor")
caso("repetir v1 tras salir del máximo: sigue dentro (es de las 2 primeras)", reg.adoptable(e))

# 4. Repetición de la MISMA variante con un titular no determinista (T-133, H-21)
reg, e = exp(1)
for ver in ("peor", "peor", "fallido", "todavía no se sabe", "peor", "mejor"):
    anotar(reg, e, "única", ver)
r = reg.resumen(e)
caso("repetir la misma variante hasta que sale «mejor» (5 en contra, 1 a favor) no la deja adoptable", not r["adoptable"],
     f"adoptable={r['adoptable']}, adoptables={r['adoptables']}, veredictos={r['veredictos']}, fuera_del_maximo={r['fuera_del_maximo']}")
caso("…y el resumen avisa de que esa variante tiene veredictos contradictorios", "contradictorios" in str(r) or "repeticiones" in r,
     f"claves del resumen: {sorted(r)}")

# 5. Etiqueta de variante libre: diez cambios distintos con la misma etiqueta caben en max_variantes=1
reg, e = exp(1)
for i in range(10):
    anotar(reg, e, "única", "peor" if i < 9 else "mejor")
caso("diez cambios distintos etiquetados igual: el registro no puede distinguirlos (la etiqueta es texto libre)",
     not reg.adoptable(e), f"adoptable={reg.adoptable(e)}: nada ata la etiqueta a una huella de lo ejecutado")

# 6. Resultados mezclados entre variantes dentro del máximo
reg, e = exp(3)
anotar(reg, e, "v1", "peor"); anotar(reg, e, "v2", "mejor"); anotar(reg, e, "v3", "peor")
r = reg.resumen(e)
caso("max 3: v2 gana y las otras pierden → adoptable solo el intento de v2", r["adoptables"] == [2])
reg, e = exp(1000)
for i in range(1000):
    anotar(reg, e, f"v{i}", "mejor" if i == 999 else "peor")
r = reg.resumen(e)
caso("(regla declarada) con max 1000, una de mil variantes gana y es adoptable sin corrección por intentos",
     True, f"adoptable={r['adoptable']}: la corrección por número de intentos (§9.17) no está en esta regla; queda para J")

# 7. Intento sin resultado y luego «mejor»: adoptable; resultado «mejor» de un intento fuera del máximo: no
reg, e = exp(1); anotar(reg, e, "única", None); anotar(reg, e, "única", "mejor")
caso("un intento sin resultado antes no impide adoptar (cuenta en sin_resultado)", reg.adoptable(e)
     and reg.resumen(e)["sin_resultado"] == [1])
fin()
