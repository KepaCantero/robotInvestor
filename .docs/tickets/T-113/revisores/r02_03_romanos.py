"""QA r02 de T-113 · H-03: la regla de los números romanos como cantidad, con un banco propio.
L = frase legítima (se espera que pase: None) · P = romano usado como cantidad (se espera CIFRA) · O = observación (se
imprime lo que da, sin contar). Sirve sobre cualquier árbol para comparar:
  cd <árbol>/bloque_a/11_Ejecutor && python <este script> [--tsv]
Con --tsv imprime solo «regla<TAB>frase» (para `diff` entre árboles)."""
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

t = Path(tempfile.mkdtemp(prefix="qa_t113_r02_rom_", dir=os.environ.get("QA_TMP")))
b = Bloque(config_pruebas(diseno="v6"), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t / "e", t / "n")
perm = v6.permitidos_r21(b)
ROM = sorted(c for c in perm["codigos"] | perm["series"] | perm.get("tickers", frozenset()) if c and set(c) <= set("IVXLCDM"))

BANCO = """
L|Las IIC españolas ganan peso.
L|Las IIC y los fondos pesan.
L|Sus IIC ganan.
L|Estas IIC son baratas.
L|Los VIX altos asustan.
L|Los IG y los HY se estrechan.
L|Las EM ganan.
L|Los ETF de renta fija ganan peso.
L|Las SICAV y las SOCIMI pesan poco.
L|Los TIPS protegen de la inflación.
L|Los REIT sufren con los tipos.
L|Las OPA animan el mercado.
L|Sus CAPEX suben.
L|Los PMI mejoran.
L|Unas IPO frenadas.
L|Esos BTP se encarecen.
L|Estos CDS se abren.
L|Felipe VI visitó la bolsa.
L|El rey Felipe VI y la reina.
L|El siglo XXI es digital.
L|La Fase II del ensayo va bien.
L|Basilea III y Basilea IV endurecen el capital.
L|Solvencia II pesa en las aseguradoras.
L|MiFID II cambió los costes.
L|Juan Pablo II fue papa.
L|Carlos III reina.
L|El plan del Capítulo XI de la quiebra.
L|La Segunda Guerra Mundial y el siglo XX.
L|El acuerdo de Basilea III; los bancos cumplen.
L|Los años del siglo XX fueron inflacionistas.
L|El grupo tiene las ideas claras.
L|Los valores cíclicos mejoran.
L|Las vías de transmisión son lentas.
L|Los mixtos ganan.
L|Las ex colonias crecen.
L|Los xilófonos no cotizan.
L|Sus vivencias pesan.
L|Las Islas Canarias reciben turismo.
L|Los Índices suben.
L|Las Ideas pasan los filtros.
L|Los Vicios del mercado.
L|Unos Inversores prudentes.
P|Las VII ideas pasan los filtros.
P|Los III tipos de activo mejoran.
P|Sus IV apuestas son defensivas.
P|Estas XII ideas son las mejores.
P|Unas XX candidatas quedaron fuera.
P|Esos II tipos concentran el riesgo.
P|Hay ideas; las IX primeras son de bolsa.
P|De las XV ideas, quedan pocas.
P|Los XXXIX valores caen.
P|Estos XIX candidatos no pasan.
P|Esas XXIV ideas pesan.
P|Unos VIII analistas coinciden.
P|Las VII ideas pasan.
P|Las  VII ideas pasan.
P|Suben las VI ideas de bolsa.
P|Todas las XI ideas son de renta fija.
O|Hay VII ideas en la lista.
O|Con XII candidatas, quedan dos.
O|VII ideas pasan los filtros.
O|Otras VII ideas pasan.
O|Quedan XII ideas.
O|Entre XX y XXX candidatas.
O|Las otras VII ideas.
O|Las últimas XII ideas.
O|Mis VII ideas.
O|Nuestras VII ideas.
O|Dichas VII ideas.
O|Ambas II ideas.
O|Cada VII días.
O|Un total de XV ideas.
O|Son XV las ideas.
O|LAS VII IDEAS PASAN.
O|Las V ideas pasan.
O|Los X valores mejores.
O|Las XL ideas pasan.
O|Los L valores pasan.
O|Las C ideas pasan.
O|Las XLII ideas pasan.
O|Los CD valores pasan.
O|Las vii ideas pasan.
O|Las IIII ideas pasan.
O|Las VV ideas pasan.
O|Las IIX ideas pasan.
O|Las XXXX ideas pasan.
O|Las VII-VIII ideas.
O|Las VII, VIII y IX.
O|Las (VII) ideas.
O|Las «VII» ideas.
O|Las Ⅶ ideas.
O|Las ⅶ ideas.
O|Las II Jornadas de inversión ayudan.
O|Los XXV Juegos Olímpicos animan el consumo.
O|Las XV legislaturas fueron estables.
O|Los III Premios del sector.
O|Sus IV trimestres seguidos de caídas.
O|Los IV de las opciones suben.
O|Los XXI retos del siglo.
O|Los VI Presupuestos.
""".strip().splitlines()

tsv = "--tsv" in sys.argv
fp = fn = 0
if not tsv:
    print("códigos, series o tickers permitidos hechos solo de letras de romano:", ROM)
for linea in BANCO:
    clase, frase = linea.split("|", 1)
    frase = frase.encode().decode("unicode_escape").encode("latin-1").decode() if "\\u" in frase else frase
    r = v6.frase_prohibida(frase, perm)
    if tsv:
        print(f"{r}\t{frase}")
        continue
    mal = (clase == "L" and r is not None) or (clase == "P" and r != "CIFRA")
    fp += clase == "L" and r is not None
    fn += clase == "P" and r != "CIFRA"
    if mal or clase == "O":
        print(f"{'FALLO' if mal else '     '} {clase} {r!s:8s} {frase}")
if not tsv:
    # un romano que además es una sigla permitida: no es cifra (lo que añade la r02)
    perm2 = dict(perm)
    perm2["codigos"] = frozenset(perm["codigos"] | {"IV", "XX"})
    print("con IV y XX en la lista permitida:", [(f, v6.frase_prohibida(f, perm2)) for f in ("Los IV de las opciones suben.", "Las XX mejores.", "Las IV y las VII ideas.")])
    print(f"\nlegítimas quitadas (falsos positivos): {fp} · cantidades que pasan (falsos negativos): {fn}")
