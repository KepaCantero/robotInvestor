"""QA r01 de T-113 · T-109 y T-110: el filtro del Sintetizador por `frase_prohibida` y por el camino real (`limpiar`).
Tickers del universo en minúscula, romanos, letras sueltas con separadores, siglas nuevas, y que no se quiten textos legítimos.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_06_filtro_sintetizador.py"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a import diseno_v6 as v6  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

t = Path(tempfile.mkdtemp(prefix="qa_t113_filtro_", dir=os.environ.get("QA_TMP")))
b = Bloque(config_pruebas(diseno="v6"), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t / "e", t / "n")
perm = v6.permitidos_r21(b)
print("tickers del universo:", len(perm["tickers"]), sorted(perm["tickers"])[:40])
comunes = sorted(x for x in perm["tickers"] if x.lower() in v6._PALABRA_COMUN)
print("tickers que en minúscula son palabra común (no se cazan):", comunes)
fallos = 0


def espera(regla, frase, nota=""):
    global fallos
    r = v6.frase_prohibida(frase, perm)
    limpio, reglas = v6.limpiar(frase, perm, {})
    mal = r != regla
    real = (reglas[:1] or [None])[0]
    fallos += mal
    print(f"{'FALLO' if mal else 'ok   '} esperado={regla} frase_prohibida={r} limpiar={reglas} · {frase!r} {nota}")
    if not mal and real != regla and not (regla is None and not reglas):
        print(f"      aviso: por el camino real (`limpiar`) sale {reglas} -> {limpio!r}")


tk = [x for x in sorted(perm["tickers"]) if x.isalpha() and len(x) >= 3 and x.lower() not in v6._PALABRA_COMUN][:3]
print("== H-34: ticker del universo en minúscula tras el vehículo")
for x in tk:
    for veh in ("la acción", "el valor", "el título", "La acción", "EL VALOR", "la accion", "el titulo", "las acciones", "los valores",
                "los títulos", "la acción de", "el valor ", "el valor  ", "el valor «", "el bono", "la cripto", "el token"):
        sep = "" if veh.endswith((" ", " ", "«")) else " "
        frase = f"Comprar {veh}{sep}{x.lower()} ya."
        r = v6.frase_prohibida(frase, perm)
        print(f"  {'caza' if r else 'PASA'} ({r}) {frase!r}")
    espera("R21", f"Comprar la acción {x.lower()} ya.")
    espera("R21", f"Comprar el valor {x.capitalize()} ya.", "(capitalizado)") if False else print("  capitalizado:", v6.frase_prohibida(f"Comprar el valor {x.capitalize()} ya.", perm))

print("== H-34: frases legítimas con «acción», «valor» y «título»")
for frase in ("El valor real del activo baja.", "La acción del banco central pesa.", "El valor es alto.", "El título lo dice todo.",
              "La acción sube.", "El valor cae.", "El valor añadido del sector crece.", "El valor razonable es menor.",
              "El título de la deuda vence pronto.", "La acción colectiva ayuda.", "El valor en libros es bajo.",
              "El valor total sube.", "El valor medio baja.", "La acción ha subido mucho.", "El valor nominal no cambia.",
              "El valor intrínseco es mayor.", "La acción ordinaria paga más.", "El valor de mercado es alto.", "El valor mas alto del año.",
              "La acción se frena.", "El valor futuro depende del tipo.", "El título cotiza bajo par.", "La acción cotiza barata.",
              "El valor actual es bajo.", "La acción ya recoge la noticia.", "El valor oro sirve de refugio.", "El valor sol no existe.",
              "El valor t es bajo.", "El valor c baja.", "El valor all in es alto.", "El valor ma crece."):
    espera(None, frase)
print("  palabras de 1 a 6 letras que son ticker del universo en minúscula y palabra española corriente:")
ESP = ("ha he va ve da di en es si no ya yo tu mi te me se le lo la el un al del con por sin tras oro sol mar red luz paz ley fin año mes dia uno dos tres"
       " real total medio alto bajo mayor menor nuevo viejo libre neto bruto puro fijo cat cost all low now key car air gas ore man sea sun arm ser estar"
       " ir ver dar son fue era hay más mas muy bien mal casi solo cada todo otra otro ante bajo cabe hasta para segun so entre desde").split()
print("   ", sorted(w for w in set(ESP) if w.upper() in perm["tickers"] and w not in v6._PALABRA_COMUN))

print("== romanos")
for regla, frase in (("CIFRA", "Vemos las VII ideas de la semana."), ("CIFRA", "Los III motivos pesan."), ("CIFRA", "Sus IV pilares aguantan."),
                     ("CIFRA", "Estas XII semanas pesan."), ("CIFRA", "Unas XX ideas."), ("CIFRA", "Las XXXIX ideas."),
                     (None, "Basilea III endurece el capital de los bancos."), (None, "Solvencia II pesa en las aseguradoras."),
                     (None, "Es el gran tema del siglo XXI."), (None, "La Fase II del plan avanza."), (None, "El MiFID II cambia las reglas."),
                     (None, "Las IIC españolas ganan peso."), (None, "Los CLI de la OCDE mejoran."), (None, "Sus CV son sólidos."),
                     (None, "Las CCC pagan más cupón."), (None, "Los XL del sector ganan."), (None, "Las LIC no cambian."),
                     (None, "Los VIX altos asustan."), (None, "Las reglas de Basilea III y IV pesan."), (None, "Carlos III reina."),
                     (None, "El capítulo II lo explica."), (None, "Los I y los V no cuentan.")):
    espera(regla, frase)
print("  romanos como cantidad sin determinante o con otro (límite declarado en INC-T113-01: «detrás de un determinante»):")
for frase in ("Vemos VII ideas esta semana.", "Hay XII ideas.", "Son III motivos.", "LAS VII IDEAS.", "Las primeras VII ideas.", "Dichas VII ideas.",
              "Otras VII ideas.", "Entre las VII ideas.", "Las vii ideas.", "Las Ⅶ ideas.", "Las V ideas.", "Las X ideas.", "Las L ideas.",
              "Las XL ideas.", "Las LX ideas.", "Las C ideas.", "Ambas II ideas.", "Tres de las VII.", "Mis VII ideas.", "Varias VII ideas."):
    print(f"   {str(v6.frase_prohibida(frase, perm)):6s} {frase!r}")

print("== H-53: letras sueltas con separadores")
for regla, frase in (("R21", "Comprar N·V·D·A ya."), ("R21", "Comprar N.V.D.A ya."), ("R21", "Comprar N-V-D-A ya."), ("R21", "Comprar N/V/D/A ya."),
                     ("R21", "Comprar N‧V‧D‧A ya."), ("R21", "Comprar N∙V∙D∙A ya."), ("R21", "Comprar N•V•D•A ya."), ("R21", "Comprar N V D A ya."),
                     (None, "La sociedad es una S.A. española."), (None, "El plan A/B funciona."), (None, "El I+D pesa."), (None, "Suben EE. UU. y Europa."),
                     (None, "La renta fija a corto-medio plazo rinde."), (None, "El escenario A o B."), (None, "Es una relación E/S normal.")):
    espera(regla, frase)
print("  otros separadores (H-53 de origen pedía «cualquier signo no alfanumérico»; lo que sigue es informativo):")
for frase in ("Comprar N. V. D. A. ya.", "Comprar N - V - D - A ya.", "Comprar N,V,D,A ya.", "Comprar N|V|D|A ya.", "Comprar N*V*D*A ya.",
              "Comprar N+V+D+A ya.", "Comprar N:V:D:A ya.", "Comprar N'V'D'A ya.", "Comprar N–V–D–A ya.", "Comprar N—V—D—A ya.", "Comprar N\\V\\D\\A ya.",
              "Comprar N​V​D​A ya.", "Comprar N­V­D­A ya.", "Comprar n·v·d·a ya.", "Comprar N·v·D·a ya.", "Comprar N..V..D..A ya.",
              "Comprar (N)(V)(D)(A) ya.", "La U.S.A. crece.", "La O.N.U. avisa.", "Es una S.A.U. española.", "Plan A-B-C.", "Opciones A/B/C."):
    limpio, reglas = v6.limpiar(frase, perm, {})
    print(f"   frase_prohibida={str(v6.frase_prohibida(frase, perm)):5s} limpiar={reglas} -> {limpio!r} · {frase!r}")

print("== H-52: siglas")
for regla, frase in ((None, "Según la AIE, la demanda de petróleo cae."), (None, "El INE publica la EPA el jueves."), (None, "La TAE de los depósitos sube."),
                     (None, "El BID financia infraestructuras."), (None, "Las AIEs no existen.") if False else (None, "La EPA dirá si el empleo aguanta."),
                     ("CIFRA", "El G7 discute aranceles."), ("CIFRA", "El G20 se reúne."), (None, "La OCDE y el FMI avisan.")):
    espera(regla, frase)
cods = b.cfg["v6"]["filtro_r21_codigos"] if "v6" in b.cfg else []
print("  en la lista de códigos: G7/G10/G20 ->", [c for c in ("G7", "G10", "G20") if c in perm["codigos"]], "· AIE, INE, EPA, TAE, BID ->",
      [c for c in ("AIE", "INE", "EPA", "TAE", "BID") if c in perm["codigos"]], "· repetidos en la lista:", sorted({c for c in cods if list(cods).count(c) > 1}))
print("  siglas nuevas que también son ticker del universo:", [c for c in ("AIE", "INE", "EPA", "TAE", "BID") if c in perm["tickers"]])

print("== H-49: mayúscula tras quitar")
for texto in ("Hay un 70 % de subida; el dólar pesa.", "Sube un 3 %. el resto aguanta.", "Hay un 70 % de subida; ¿el dólar pesa?", "Hay un 70 %; «el dólar» pesa.",
              "Hay un 70 %; ñandú corre.", "Hay un 70 %; élite compra.", "El dólar pesa; hay un 70 %.", "Hay un 70 %; iPhone vende.", "Hay un 70 %. "):
    limpio, reglas = v6.limpiar(texto, perm, {})
    print(f"   {reglas} {limpio!r} · {texto!r}")
print("idempotencia de limpiar:", all(v6.limpiar(v6.limpiar(x, perm, {})[0], perm, {})[0] == v6.limpiar(x, perm, {})[0]
                                      for x in ("Hay un 70 % de subida; el dólar pesa.", "El dólar pesa.", "Comprar N·V·D·A ya. El resto sigue.")))
print("FALLOS:", fallos)
