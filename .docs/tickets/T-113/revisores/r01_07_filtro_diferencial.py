"""QA r01 de T-113 · filtro del Sintetizador, antes (3a5fbfe^) frente a ahora, sobre un banco de frases legítimas: ¿qué frases
que antes pasaban se quitan ahora? Se ejecuta dos veces, una por árbol, y se comparan las salidas:
  cd <árbol>/bloque_a/11_Ejecutor && python <este script> > salida.txt
Uso: python r01_07_filtro_diferencial.py   (imprime «regla<TAB>frase» por cada frase del banco)"""
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

t = Path(tempfile.mkdtemp(prefix="qa_t113_dif_", dir=os.environ.get("QA_TMP")))
b = Bloque(config_pruebas(diseno="v6"), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t / "e", t / "n")
perm = v6.permitidos_r21(b)
BANCO = """Las IIC españolas ganan peso.
Los VIX altos asustan.
Las IIC y los fondos pesan.
Sus IIC ganan.
Los CLI de la OCDE mejoran.
Sus CV son sólidos.
Las CCC pagan más cupón.
Los XL del sector ganan.
La sociedad es una S.A. española.
El plan A/B funciona.
El escenario A o B.
Es una relación E/S normal.
La U.S.A. crece.
La O.N.U. avisa.
Es una S.A.U. española.
Plan A-B-C.
Opciones A/B/C.
El G7 discute aranceles.
El G20 se reúne.
Suben EE.UU. y Europa.
El valor real del activo baja.
La acción del banco central pesa.
El valor es alto.
La acción sube con fuerza.
El título cotiza bajo par.
El valor añadido crece.
Basilea III endurece el capital.
Es el gran tema del siglo XXI.
La I+D pesa.
El tipo sube poco a poco.
Las pymes sufren.
Los bancos ganan con los tipos altos.
El sector de la energía pesa más.
La inflación baja despacio.
Las bolsas de Europa suben.
El oro sirve de refugio.
El dólar se frena.
Un riesgo es la deuda.
La renta fija rinde más.
Hay menos miedo en el mercado.
El BCE y la Fed esperan.
El PIB crece.
El IPC baja.
Sube la bolsa. baja el bono.
Los resultados salen el jueves; el mercado espera.
La guerra pesa - y mucho - en el gas.
Compra o venta: A. Sube. B. Baja. C. Igual.
Las empresas de EE. UU. ganan más.
El punto A.B.C del plan.
Los bonos a corto/medio/largo plazo rinden.
El ratio P/E/G es alto.
Las letras A-B-C del plan.
Las emisiones de CO-V-I-D pesan.
""".strip().split("\n")
for frase in BANCO:
    limpio, reglas = v6.limpiar(frase, perm, {})
    print(f"{v6.frase_prohibida(frase, perm)}\t{reglas}\t{frase}")
