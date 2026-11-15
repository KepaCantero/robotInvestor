"""QA r01 de T-133 · R8 tras T-133: IBAN reales en formas corrientes, falsos positivos nuevos y tarjetas junto a un número
de cuatro cifras. Compara la versión de T-133 con la de T-130 (el `contratos.py` del commit anterior, que se pasa como
argumento; solo usa la biblioteca estándar).

Los IBAN y las tarjetas se generan al azar con su dígito de control (módulo 97, Luhn): no hay ninguno escrito en el
fichero (gate de secretos). Semilla fija.

Uso (desde la raíz de la copia): python -I r01_01_iban_tarjetas_formas.py <contratos.py de T-130>
"""
import importlib.util
import random
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]


def cargar(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


NUEVO = cargar(RAIZ / "bloque_a" / "11_Ejecutor" / "bloque_a" / "contratos.py", "c_nuevo")
VIEJO = cargar(sys.argv[1], "c_viejo") if len(sys.argv) > 1 else None
rng = random.Random(20261115)
OK, FALLOS = 0, []


def comprobar(cond, msg):
    global OK
    OK += bool(cond)
    if not cond:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg}")


def detecta(mod, texto):
    return bool(mod.ibanes_en_texto(texto))


def tarjeta(mod, texto):
    return bool(mod.tarjetas_en_texto(texto))


def control(pais, bban):
    num = "".join(str(int(c, 36)) for c in (bban + pais + "00"))
    return f"{98 - int(num) % 97:02d}"


def bban_al_azar(estructura, letras_en_c=True):
    out, tramos = "", []
    for n, k in re.findall(r"(\d+)([nac])", estructura):
        n = int(n)
        if k == "n":
            t = "".join(rng.choice("0123456789") for _ in range(n))
        elif k == "a":
            t = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n))
        else:
            al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" if letras_en_c else "0123456789"
            t = "".join(rng.choice(al) for _ in range(n))
        tramos.append(t)
        out += t
    return out, tramos


def de4(s):
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


# ---------------------------------------------------------------------------------------------------------------------
print("1. IBAN válidos (estructura ISO 13616 de cada país, letras en los tramos «c») en formas corrientes")
FORMAS = {
    "junto": lambda p, c, b, t: p + c + b,
    "grupos de 4": lambda p, c, b, t: de4(p + c + b),
    "minúsculas": lambda p, c, b, t: de4(p + c + b).lower(),
    "tras «IBAN:» en una frase": lambda p, c, b, t: f"Pague a IBAN: {de4(p + c + b)}, gracias.",
    "espacio duro": lambda p, c, b, t: de4(p + c + b).replace(" ", " "),
    "seguido de EUR": lambda p, c, b, t: p + c + b + "EUR",
    "por tramos nacionales": lambda p, c, b, t: " ".join([p + c] + t),
    "país en mayúsculas, resto en minúsculas": lambda p, c, b, t: p + c + " " + de4(b).lower(),
    "tipo título («Gb82 West…»)": lambda p, c, b, t: " ".join(g.capitalize() for g in de4(p + c + b).split()),
}
res = {f: {"nuevo": [], "viejo": []} for f in FORMAS}
N = 30
for pais, est in sorted(NUEVO.ESTRUCTURA_BBAN.items()):
    if pais == "ES":
        continue   # el IBAN español tiene su patrón propio en RE_SECRETO
    for _ in range(N):
        b, t = bban_al_azar(est)
        c = control(pais, b)
        for f, fn in FORMAS.items():
            txt = fn(pais, c, b, t)
            if not detecta(NUEVO, txt):
                res[f]["nuevo"].append(pais)
            if VIEJO and not detecta(VIEJO, txt):
                res[f]["viejo"].append(pais)
for f, r in res.items():
    n_nuevo = sorted(set(r["nuevo"]))
    n_viejo = sorted(set(r["viejo"]))
    print(f"     {f:40} sin detectar · T-133: {len(r['nuevo']):4} {n_nuevo} · T-130: {len(r['viejo']):4}")
for f in ("junto", "grupos de 4", "minúsculas", "tras «IBAN:» en una frase", "espacio duro", "seguido de EUR"):
    comprobar(not res[f]["nuevo"], f"forma «{f}»: todos los IBAN válidos de los 41 países detectados")
# los dos casos mixtos y los tramos nacionales: ¿qué se pierde respecto de T-130?
for f in ("país en mayúsculas, resto en minúsculas", "tipo título («Gb82 West…»)", "por tramos nacionales"):
    perdidos = sorted(set(res[f]["nuevo"]) - set(res[f]["viejo"])) if VIEJO else sorted(set(res[f]["nuevo"]))
    comprobar(not perdidos, f"forma «{f}»: T-133 no pierde países que T-130 detectaba (perdidos: {perdidos})")

print("2. IBAN de solo cifras en los formatos nacionales impresos (bancos, facturas)")
casos_nac = {
    "BE 3-7-2": ("BE", "3n7n2n", lambda c, t: f"BE{c} {t[0]}-{t[1]}-{t[2]}"),
    "FR RIB 5-5-11-2": ("FR", "5n5n11c2n", lambda c, t: f"FR{c} {' '.join(t)}"),
    "IT con CIN suelto": ("IT", "1a5n5n12c", lambda c, t: f"IT{c} {' '.join(t)}"),
    "HU 3-4-1-15-1": ("HU", "3n4n1n15n1n", lambda c, t: f"HU{c} {' '.join(t)}"),
    "TR 5-1-16": ("TR", "5n1n16c", lambda c, t: f"TR{c} {' '.join(t)}"),
    "PT 4-4-11-2": ("PT", "4n4n11n2n", lambda c, t: f"PT{c} {' '.join(t)}"),
    "PT grupos de 4 (último de 1)": ("PT", "4n4n11n2n", lambda c, t: de4(f"PT{c}" + "".join(t))),
}
for nombre, (pais, est, fn) in casos_nac.items():
    malos_n, malos_v = 0, 0
    for _ in range(50):
        b, t = bban_al_azar(est, letras_en_c=False)   # un tramo «c» de 12 letras seguidas no es un número de cuenta real
        txt = fn(control(pais, b), t)
        malos_n += not detecta(NUEVO, txt)
        malos_v += bool(VIEJO) and not detecta(VIEJO, txt)
    print(f"     {nombre:30} sin detectar de 50 · T-133: {malos_n:2} · T-130: {malos_v:2}")
    if nombre in ("BE 3-7-2", "FR RIB 5-5-11-2", "IT con CIN suelto", "PT 4-4-11-2", "PT grupos de 4 (último de 1)"):
        comprobar(malos_n == 0, f"{nombre}: todos detectados")

# ---------------------------------------------------------------------------------------------------------------------
print("3. falsos positivos: identificadores en mayúsculas que empiezan como un IBAN (país + 2 cifras + alfanumérico)")
ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
fp_n, fp_v, total = 0, 0, 0
por_pais = {}
for pais, largo in sorted(NUEVO.LONGITUD_IBAN.items()):
    for _ in range(3000):
        ident = pais + "".join(rng.choice("0123456789") for _ in range(2)) + "".join(rng.choice(ALNUM) for _ in range(largo - 4))
        txt = f"pedido {ident} enviado"
        total += 1
        n = detecta(NUEVO, txt)
        fp_n += n
        fp_v += bool(VIEJO) and detecta(VIEJO, txt)
        if n:
            por_pais[pais] = por_pais.get(pais, 0) + 1
print(f"     {total} identificadores al azar · marcados como IBAN: T-133 {fp_n} · T-130 {fp_v} · por país (T-133): {por_pais}")
comprobar(fp_n <= max(fp_v, 1) * 2, f"T-133 no dispara los falsos positivos de identificadores alfanuméricos frente a T-130 "
          f"({fp_n} frente a {fp_v})")

# ---------------------------------------------------------------------------------------------------------------------
print("4. tarjetas: una tarjeta válida junto a un número de cuatro cifras (caducidad MMAA, PIN, año)")


def tarjeta_visa():
    base = "4" + "".join(rng.choice("0123456789") for _ in range(14))
    for d in "0123456789":
        if NUEVO._luhn(base + d):
            return base + d
    raise AssertionError


def g4(s, sep=" "):
    return sep.join(s[i:i + 4] for i in range(0, len(s), 4))


FORMAS_T = {
    "sola": lambda t: g4(t),
    "con caducidad «12/27»": lambda t: g4(t) + " 12/27",
    "con CVV de 3": lambda t: g4(t) + " 123",
    "con caducidad MMAA «0128»": lambda t: g4(t) + " 0128",
    "con año delante («2026 <tarjeta>»)": lambda t: "2026 " + g4(t),
    "con guiones y caducidad MMAA": lambda t: g4(t, "-") + "-0128",
    "dos tarjetas en una línea": lambda t: g4(t) + " " + g4(tarjeta_visa()),
    "con PIN de 4 y CVV": lambda t: g4(t) + " 1234 123",
}
for f, fn in FORMAS_T.items():
    n_n = n_v = 0
    for _ in range(50):
        txt = f"pago con {fn(tarjeta_visa())} hoy"
        n_n += tarjeta(NUEVO, txt)
        n_v += bool(VIEJO) and tarjeta(VIEJO, txt)
    print(f"     {f:38} detectadas de 50 · T-133: {n_n:2} · T-130: {n_v:2}")
    comprobar(n_n == 50, f"tarjeta {f}: detectada")

print("5. filas de tabla de números de cuatro cifras (lo que T-133 quería dejar de marcar)")
for n_grupos in (5, 6, 8):
    fp_n = fp_v = 0
    for _ in range(3000):
        fila = " ".join(str(rng.randint(4000, 5999)) for _ in range(n_grupos))
        fp_n += tarjeta(NUEVO, fila)
        fp_v += bool(VIEJO) and tarjeta(VIEJO, fila)
    print(f"     {n_grupos} números de 4 cifras: T-133 {fp_n}/3000 · T-130 {fp_v}/3000")
    comprobar(fp_n == 0, f"fila de {n_grupos} números de 4 cifras: ningún falso positivo")

print(f"\nr01_01 T-133: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
