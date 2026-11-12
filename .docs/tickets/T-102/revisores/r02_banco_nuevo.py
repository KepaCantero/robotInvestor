"""QA r02 de T-102 · Banco NUEVO de frases (no visto por el implementador) contra el filtro R13/R21 frase a frase.

Escrito por el revisor de la r02 antes de leer las expresiones del código. Frases como las que escribiría un sintetizador de
informes de inversión en español, de los doce tipos de activo del Documento 0 (tabla 2.4): RV, RF, DIV, MP, IDX, FON, DER, INM,
CRI, ALT, MON y TCV. Cada frase lleva:
- etiqueta: None (legítima), "R13" (probabilidad numérica de un pronóstico) o "R21" (comprar, vender, recomendar o proponer
  un valor, emisión, fondo, contrato o token concreto, Documento 0 R21). Comprar un segmento, una divisa, un par, una región,
  una calificación o un índice, o citar un fondo o un índice como ejemplo del ámbito, es legítimo.
- grupo:
  - legítimas: "llana" (sin trampa), "t13" (palabra de probabilidad u «opciones» junto a una cifra que no es una
    probabilidad), "t21" (verbo de compra, venta o inversión seguido de una sigla o un nombre que NO es un instrumento);
  - prohibidas: "evidente" (lo que el ticket promete cazar: un porcentaje de probabilidad, un código o ISIN tras el verbo,
    un sufijo societario o una emisión con vencimiento) y "dificil" (semántica prohibida fuera de lo prometido: escenarios
    con porcentaje sin la palabra probabilidad, verbos o sustantivos no previstos, ticker de una letra...).
Las frases DUDOSAS (la regla no las decide con claridad) van aparte y no cuentan en las tasas.

Uso (desde la raíz del repositorio; la raíz del código a atacar es opcional):
  .venv/bin/python -I .docs/tickets/T-102/revisores/r02_banco_nuevo.py [<raiz_repo>] [--detalle]
Imprime las tasas por regla, por grupo y por tipo, y la lista de fallos. No escribe nada en el repositorio.
"""
from __future__ import annotations

import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
DETALLE = "--detalle" in sys.argv
RAIZ = Path(ARGS[0] if ARGS else ".").resolve()
EJEC = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJEC / "tests"))
sys.path.insert(0, str(EJEC))

from conftest import DATOS, config_pruebas  # noqa: E402

from bloque_a import diseno_v6 as v6  # noqa: E402
from bloque_a.configuracion import CLASES, RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

assert Path(v6.__file__).resolve().is_relative_to(EJEC.resolve()), v6.__file__

L, T13, T21, EV, DF = "llana", "t13", "t21", "evidente", "dificil"
# (tipo, etiqueta esperada, grupo, frase)
BANCO: list[tuple[str, str | None, str, str]] = [
    # ------------------------------------------------------------------ RV
    ("RV", None, L, "El mercado estadounidense cotiza a 21 veces beneficios, por encima de su media de diez años."),
    ("RV", None, T13, "Es probable que las pequeñas compañías europeas sigan rezagadas mientras el BCE no recorte."),
    ("RV", None, L, "Preferimos comprar calidad y dividendo frente a crecimiento caro en este tramo del ciclo."),
    ("RV", None, L, "La banca española, con el Ibex como referencia, acumula un 18 % en el año."),
    ("RV", None, L, "Sobreponderar Japón frente a Europa tiene sentido con un yen débil."),
    ("RV", None, L, "El sector de semiconductores, por ejemplo el índice SOX, depende del ciclo de inventarios."),
    ("RV", None, T13, "La probabilidad de una corrección ha aumentado tras una subida del 22 % en el año."),
    ("RV", None, L, "Vender exposición a consumo discrecional reduce la sensibilidad a un frenazo del empleo."),
    ("RV", None, L, "Las compañías de defensa europeas suben un 35 % desde enero por el gasto militar."),
    ("RV", None, L, "El BPA agregado del Stoxx 600 crece un 6 % interanual."),
    ("RV", None, L, "Comprar mercados emergentes asiáticos ex China es la opción con mejor relación entre valoración y momento."),
    ("RV", None, L, "La prima de riesgo del mercado se sitúa en el 4,2 %, la más baja desde 2007."),
    ("RV", None, L, "Un ejemplo de vehículo del ámbito sería un fondo indexado al MSCI Europe Value."),
    ("RV", None, T21, "Invertir en small caps de EE. UU. exige tolerar caídas del 25 %."),
    ("RV", None, T13, "Es probable que los beneficios del sector crezcan un 8 % en 2027."),
    ("RV", None, T21, "Comprar RV de EE. UU. frente a RV de la UE es la lectura del régimen."),
    ("RV", "R21", EV, "Compramos acciones de Inditex (ITX.MC) para el horizonte H3."),
    ("RV", "R21", EV, "Recomendamos vender META antes de resultados."),
    ("RV", "R21", EV, "Nuestra opción preferida es entrar en ASML.AS en la próxima caída."),
    ("RV", "R21", EV, "Abrir una posición larga en TSLA con stop por debajo de 200 dólares."),
    ("RV", "R21", EV, "Conviene comprar el valor US0378331005 antes del dividendo."),
    ("RV", "R21", EV, "Aumentar posiciones en Banco Santander S.A. es la idea principal del mes."),
    ("RV", "R21", DF, "Acumular GOOGL en las caídas es la idea del trimestre."),
    ("RV", "R21", DF, "Nuestra recomendación para el trimestre es NVDA."),
    ("RV", "R13", EV, "Asignamos una probabilidad del 70 % a que el S&P 500 cierre el año en positivo."),
    ("RV", "R13", EV, "Hay un 65 % de posibilidades de que la banca europea bata al índice en H3."),
    ("RV", "R13", EV, "Le damos un 55 % de probabilidades a un rebote de las pequeñas compañías."),
    ("RV", "R13", DF, "Escenarios para la RV europea: base (55 %), alcista (25 %) y bajista (20 %)."),
    # ------------------------------------------------------------------ RF
    ("RF", None, L, "La curva alemana se empina: el diferencial 2-10 años alcanza 45 puntos básicos."),
    ("RF", None, L, "Comprar duración en el tramo de 5 a 7 años protege si la economía se enfría."),
    ("RF", None, L, "El crédito IG europeo ofrece una TIR del 3,4 % con duración de 4,5 años."),
    ("RF", None, L, "El mercado descuenta dos recortes del BCE antes de junio."),
    ("RF", None, T13, "Es probable que la TIR del Treasury a 10 años oscile entre el 4 % y el 4,6 % en H2."),
    ("RF", None, T21, "Vender HY frente a IG reduce el riesgo de impago de la cartera."),
    ("RF", None, L, "La prima de riesgo de Italia baja a 110 puntos básicos, mínimo desde 2015."),
    ("RF", None, T21, "Comprar TIPS a cinco años gana atractivo si el IPC repunta."),
    ("RF", None, L, "Comprar deuda periférica a corto plazo es la opción de menor riesgo del ámbito."),
    ("RF", None, L, "La tasa de impago del high yield estadounidense se sitúa en el 3,8 %."),
    ("RF", None, L, "Un ejemplo de referencia del ámbito es el índice Bloomberg Euro Aggregate."),
    ("RF", None, T21, "Preferimos comprar bonos con calificación BBB frente a BB en este tramo del ciclo."),
    ("RF", None, T13, "La probabilidad de recesión que descuenta la curva ha bajado con el diferencial en 40 puntos básicos."),
    ("RF", None, T21, "Comprar Bund frente a BTP es una apuesta de diferencial soberano."),
    ("RF", None, T21, "Vender JGB a largo plazo es la expresión de un BOJ más duro."),
    ("RF", None, T21, "Comprar el tramo AAA de los CLO europeos ofrece un diferencial atractivo."),
    ("RF", None, T21, "Comprar OAT francesas a diez años exige vigilar el déficit público."),
    ("RF", "R21", EV, "Comprar el bono ES0000012M85 para alargar duración."),
    ("RF", "R21", EV, "Recomendamos el bono de Telefónica con vencimiento en 2031."),
    ("RF", "R21", EV, "Vender el TLT antes de la reunión de la Fed."),
    ("RF", "R21", EV, "Invertir en el ETF IEAC para capturar el crédito europeo."),
    ("RF", "R21", EV, "Tomar posiciones en deuda de Volkswagen AG a cinco años."),
    ("RF", "R13", EV, "La probabilidad de que el BCE recorte en diciembre es del 75 %."),
    ("RF", "R13", EV, "Estimamos en un 60 % la probabilidad de que la TIR alemana baje del 2 %."),
    ("RF", "R13", EV, "Con una confianza del 70 %, el diferencial italiano se estrechará en H3."),
    ("RF", "R13", EV, "Las opciones de un empinamiento de la curva son de 3 de cada 4."),
    # ------------------------------------------------------------------ DIV
    ("DIV", None, T21, "Comprar EUR/USD tiene sentido si el diferencial de tipos sigue estrechándose."),
    ("DIV", None, T21, "Vender USDJPY es la forma más directa de jugar un giro del BOJ."),
    ("DIV", None, L, "El dólar índice (DXY) cae un 4 % desde máximos."),
    ("DIV", None, T13, "Es probable que el franco suizo siga actuando como refugio en episodios de tensión."),
    ("DIV", None, T21, "Comprar divisas de materias primas, como el AUD y el NOK, depende del ciclo chino."),
    ("DIV", None, L, "El carry del peso mexicano frente al dólar supera el 6 % anual."),
    ("DIV", None, L, "La libra cotiza un 3 % por debajo de su valor de paridad de poder adquisitivo."),
    ("DIV", None, T21, "Vender yuanes offshore (CNH) es una cobertura frente a una devaluación gradual."),
    ("DIV", None, T13, "Las opciones a un mes sobre el euro descuentan una volatilidad del 7 %."),
    ("DIV", None, L, "Comprar coronas suecas frente al euro gana atractivo si el Riksbank endurece."),
    ("DIV", None, L, "El par GBP/USD lleva tres semanas en un rango estrecho."),
    ("DIV", None, L, "La posición especulativa en yenes es la más corta desde 2007."),
    ("DIV", None, T21, "Vender GBP frente a CHF protege ante una sorpresa fiscal en el Reino Unido."),
    ("DIV", None, L, "El tipo de cambio efectivo real del euro está cerca de su media histórica."),
    ("DIV", None, T21, "Comprar USD/MXN funciona como cobertura barata frente a la aversión al riesgo."),
    ("DIV", "R13", EV, "La probabilidad de que EUR/USD supere 1,15 en H3 es del 60 %."),
    ("DIV", "R13", EV, "Asignamos un 70 % de probabilidad a una depreciación del yen."),
    ("DIV", "R13", EV, "Hay un 40 % de posibilidades de que el BOJ suba tipos en enero."),
    ("DIV", "R21", EV, "Comprar el ETF FXE para jugar la subida del euro."),
    ("DIV", "R21", EV, "Comprar el futuro 6EZ6 del euro en el CME."),
    ("DIV", "R21", EV, "Recomendamos el fondo Invesco CurrencyShares Japanese Yen Trust (FXY)."),
    ("DIV", "R21", EV, "Abrir un largo en el contrato M6EZ6 de diciembre."),
    # ------------------------------------------------------------------ MP
    ("MP", None, L, "El oro sube un 12 % en el trimestre por las compras de bancos centrales."),
    ("MP", None, L, "Comprar oro como cobertura tiene sentido con tipos reales a la baja."),
    ("MP", None, L, "El Brent se mueve entre 70 y 85 dólares por barril desde el verano."),
    ("MP", None, T13, "Es probable que la OPEP+ mantenga los recortes de producción hasta marzo."),
    ("MP", None, L, "La curva del WTI está en backwardation, señal de mercado físico tenso."),
    ("MP", None, L, "Vender exposición a metales industriales reduce el riesgo si China frena."),
    ("MP", None, L, "El cobre del LME cotiza a 9.200 dólares por tonelada."),
    ("MP", None, L, "Las existencias de gas en Europa están al 92 % de su capacidad."),
    ("MP", None, L, "Comprar materias primas agrícolas es una apuesta sobre el clima y no sobre el ciclo."),
    ("MP", None, L, "El índice Bloomberg Commodity es un ejemplo de referencia amplia del ámbito."),
    ("MP", None, L, "La plata se comporta con una beta de 1,5 frente al oro."),
    ("MP", None, L, "Invertir en metales de transición, como el litio y el níquel, exige horizonte H4."),
    ("MP", None, T13, "La probabilidad de un déficit de cobre crece con una demanda que sube un 4 % al año."),
    ("MP", None, T21, "Comprar GNL asiático frente al TTF europeo captura una prima del 15 %."),
    ("MP", None, T21, "Vender WTI frente a Brent es una apuesta sobre el diferencial transatlántico."),
    ("MP", None, T13, "Lo más probable es que el oro consolide tras subir un 25 % en el año."),
    ("MP", "R13", EV, "Damos un 65 % de probabilidad a que el oro supere los 3.000 dólares."),
    ("MP", "R13", EV, "La probabilidad estimada de que el Brent baje de 70 dólares asciende al 45 %."),
    ("MP", "R13", EV, "Con un 80 % de confianza, el cobre seguirá en déficit en 2027."),
    ("MP", "R13", DF, "Escenario alcista (30 %): el oro sube a 3.200 dólares."),
    ("MP", "R21", EV, "Comprar el ETC SGLD para cubrir la cartera."),
    ("MP", "R21", EV, "Vender el contrato CLZ6 del WTI antes del vencimiento."),
    ("MP", "R21", EV, "Tomar posiciones en Barrick Gold Corp como apuesta apalancada al oro."),
    ("MP", "R21", EV, "Invertir en GLD es la forma más sencilla de exponerse al oro."),
    # ------------------------------------------------------------------ IDX
    ("IDX", None, T21, "Comprar el S&P 500 equiponderado reduce la concentración en las siete grandes."),
    ("IDX", None, L, "El Euro Stoxx 50 cotiza a 13 veces beneficios, con descuento frente a EE. UU."),
    ("IDX", None, T21, "Vender el Nasdaq 100 frente al Russell 2000 es una apuesta a la amplitud del mercado."),
    ("IDX", None, L, "El MSCI Emerging Markets acumula un 9 % en el año."),
    ("IDX", None, T13, "Es probable que el Nikkei siga ligado al tipo de cambio del yen."),
    ("IDX", None, L, "La concentración del índice estadounidense en diez valores roza el 35 %."),
    ("IDX", None, T21, "Invertir en el MSCI World es la referencia neutral del ámbito."),
    ("IDX", None, L, "El DAX alcanza máximos históricos con un 60 % de sus ventas fuera de Alemania."),
    ("IDX", None, L, "La volatilidad implícita del S&P 500 (VIX) está en 14 puntos."),
    ("IDX", None, T21, "Comprar el Ibex 35 es una apuesta sobre la banca y las utilities."),
    ("IDX", None, T21, "Sobreponderar el FTSE 100 da exposición a energía y materias primas."),
    ("IDX", None, T13, "La probabilidad de que el índice vuelva a su media aumenta con una TIR real del 2 %."),
    ("IDX", None, T21, "Comprar el KOSPI es una apuesta sobre el ciclo de los semiconductores."),
    ("IDX", None, T21, "Comprar el CAC 40 y vender el DAX es una apuesta sobre el consumo de lujo."),
    ("IDX", None, L, "El CSI 300 rebota un 20 % tras los estímulos de Pekín."),
    ("IDX", None, T21, "Comprar el Hang Seng frente al MSCI ACWI es una apuesta contraria."),
    ("IDX", "R13", EV, "Asignamos un 70 % de probabilidad a que el Euro Stoxx 50 cierre por encima de 5.000."),
    ("IDX", "R13", EV, "Las posibilidades de que el Nikkei supere su máximo en H3 son del 55 %."),
    ("IDX", "R13", EV, "Probabilidad de que el Nasdaq corrija más de un 10 %: 35 %."),
    ("IDX", "R21", EV, "Comprar el ETF CSPX para replicar el S&P 500."),
    ("IDX", "R21", EV, "Recomendamos el fondo Vanguard S&P 500 UCITS ETF (VUSA)."),
    ("IDX", "R21", EV, "Comprar el futuro ESZ6 sobre el S&P 500."),
    ("IDX", "R21", EV, "Vender el ETF EXS1 del DAX antes de las elecciones."),
    # ------------------------------------------------------------------ FON
    ("FON", None, L, "Los fondos monetarios en euros reciben entradas por octavo mes consecutivo."),
    ("FON", None, L, "Comprar fondos de renta fija flexible tiene sentido con la curva empinada."),
    ("FON", None, L, "Un ejemplo del ámbito sería un fondo indexado de bajo coste al MSCI World."),
    ("FON", None, L, "Las comisiones medias de los fondos de gestión activa bajan al 1,3 %."),
    ("FON", None, T13, "Es probable que la gestión activa en pequeñas compañías bata a la pasiva en este entorno."),
    ("FON", None, L, "Invertir en fondos de retorno absoluto exige revisar su correlación con la bolsa."),
    ("FON", None, L, "Los fondos mixtos moderados ganan un 5 % en el año."),
    ("FON", None, L, "Vender fondos de crecimiento con sesgo tecnológico reduce la concentración."),
    ("FON", None, L, "El patrimonio en ETF europeos supera los dos billones de euros."),
    ("FON", None, L, "Los fondos de deuda emergente en moneda local sufren salidas por la fortaleza del dólar."),
    ("FON", None, T13, "La probabilidad de que un fondo activo bata a su índice es baja: solo el 15 % lo logra a diez años."),
    ("FON", None, L, "Comprar fondos de fondos alternativos añade una capa de comisiones."),
    ("FON", None, L, "La categoría de fondos de dividendo europeo tiene una volatilidad del 14 %."),
    ("FON", None, T21, "Sobreponderar ETF de RF a corto plazo reduce la duración de la cartera."),
    ("FON", None, T21, "Comprar fondos cerrados con descuento sobre el NAV del 12 % es la oportunidad del ámbito."),
    ("FON", None, T21, "Invertir en ETF UCITS de acumulación simplifica la fiscalidad."),
    ("FON", "R21", EV, "Comprar el fondo LU0996182563 para la parte de RV global."),
    ("FON", "R21", EV, "Invertir en el fondo Amundi MSCI World UCITS ETF (MWRD) es nuestra opción."),
    ("FON", "R21", EV, "Vender participaciones del fondo IE00B4L5Y983 antes del cierre del ejercicio."),
    ("FON", "R21", DF, "Traspasar el dinero al ETF VWCE es la opción preferida."),
    ("FON", "R21", EV, "Recomendamos comprar el ETF SPYD por su dividendo."),
    ("FON", "R13", EV, "La probabilidad de que el fondo bata a su índice este año es del 60 %."),
    ("FON", "R13", EV, "Damos un 70 % de probabilidad a que los fondos monetarios sigan recibiendo entradas."),
    # ------------------------------------------------------------------ DER
    ("DER", None, L, "La volatilidad implícita a un mes del S&P 500 está por debajo de la realizada."),
    ("DER", None, T21, "Comprar volatilidad es barato cuando el VIX está por debajo de 13."),
    ("DER", None, L, "La curva de futuros del VIX está en contango."),
    ("DER", None, L, "El skew de las opciones sobre el Euro Stoxx 50 refleja demanda de protección."),
    ("DER", None, L, "Vender volatilidad en el tramo corto tiene un perfil de pérdidas asimétrico."),
    ("DER", None, L, "El delta de una put a tres meses un 10 % fuera de dinero ronda 0,2."),
    ("DER", None, T13, "Las opciones sobre el Brent descuentan una volatilidad del 32 %."),
    ("DER", None, T13, "Es probable que la volatilidad repunte en torno a las elecciones."),
    ("DER", None, L, "El coste de cubrir una cartera con puts a tres meses equivale al 2,1 % del nominal."),
    ("DER", None, T13, "Las opciones de vencimiento diario suponen el 45 % del volumen."),
    ("DER", None, L, "Comprar protección con collares reduce el coste de la cobertura."),
    ("DER", None, L, "La volatilidad de la volatilidad está en mínimos de dos años."),
    ("DER", None, T13, "La probabilidad de un movimiento del 5 % en el día es baja según las opciones."),
    ("DER", None, T13, "Las opciones de compra sobre el oro un 5 % fuera de dinero se encarecen."),
    ("DER", None, L, "Sobreponderar estrategias de dispersión tiene sentido con correlaciones implícitas altas."),
    ("DER", None, T21, "Vender CDS del iTraxx Main es una forma de cobrar la prima de crédito."),
    ("DER", "R21", EV, "Comprar la opción SPXW 5000P de marzo como cobertura."),
    ("DER", "R21", EV, "Vender el futuro VXZ6 del VIX para capturar el contango."),
    ("DER", "R21", EV, "Comprar calls sobre NVDA a tres meses."),
    ("DER", "R21", EV, "Recomendamos el ETN VXX como cobertura táctica."),
    ("DER", "R13", EV, "La probabilidad de que el VIX supere 30 en H2 es del 20 %."),
    ("DER", "R13", EV, "Asignamos un 35 % de probabilidad a un repunte de la volatilidad antes de fin de año."),
    ("DER", "R13", EV, "Hay un 25 % de posibilidades de que el skew se normalice."),
    # ------------------------------------------------------------------ INM
    ("INM", None, L, "Las SOCIMI españolas cotizan con un descuento del 30 % sobre su valor neto de activos."),
    ("INM", None, L, "Comprar inmobiliario logístico tiene sentido con la demanda del comercio electrónico."),
    ("INM", None, L, "Los REIT de oficinas estadounidenses sufren por una tasa de desocupación del 19 %."),
    ("INM", None, T13, "Es probable que el precio de la vivienda en España siga subiendo, aunque a menor ritmo."),
    ("INM", None, L, "La rentabilidad por dividendo de los REIT europeos se sitúa en el 4,8 %."),
    ("INM", None, L, "Vender exposición a oficinas y comprar residencial en alquiler es la rotación del ámbito."),
    ("INM", None, L, "El índice FTSE EPRA Nareit Developed Europe es un ejemplo de referencia del ámbito."),
    ("INM", None, L, "Los tipos hipotecarios bajan al 3,1 %, mínimos de dos años."),
    ("INM", None, L, "Invertir en centros de datos exige separar el componente inmobiliario del tecnológico."),
    ("INM", None, T13, "La probabilidad de una caída fuerte de la vivienda es baja con un déficit de oferta del 20 %."),
    ("INM", None, L, "El endeudamiento medio de los REIT, un 38 % del valor de los activos, es manejable."),
    ("INM", None, T21, "Sobreponderar REIT sanitarios aporta flujos ligados a la demografía."),
    ("INM", None, L, "Las transacciones de oficinas en Madrid caen un 25 % interanual."),
    ("INM", None, T21, "Comprar SOCIMI de residencial en alquiler tiene sentido con la escasez de oferta."),
    ("INM", None, L, "La prima de los REIT frente al bono a 10 años está en 150 puntos básicos."),
    ("INM", "R21", EV, "Comprar acciones de Merlin Properties (MRL.MC) por su descuento."),
    ("INM", "R21", EV, "Recomendamos invertir en Prologis Inc por su exposición logística."),
    ("INM", "R21", DF, "Vender el REIT O antes de la subida de tipos."),
    ("INM", "R21", EV, "Comprar el ETF IPRP para exponerse a los REIT europeos."),
    ("INM", "R13", EV, "La probabilidad de que el precio de la vivienda caiga en 2027 es del 15 %."),
    ("INM", "R13", EV, "Hay un 60 % de posibilidades de que las SOCIMI cierren su descuento en H4."),
    # ------------------------------------------------------------------ CRI
    ("CRI", None, L, "Bitcoin acumula un 40 % desde el halving, con entradas en los ETF al contado."),
    ("CRI", None, L, "La volatilidad realizada de las criptomonedas cae al 45 % anualizado."),
    ("CRI", None, T13, "Es probable que la regulación MiCA reduzca el número de emisores de stablecoins."),
    ("CRI", None, L, "La dominancia de bitcoin sobre la capitalización total sube al 58 %."),
    ("CRI", None, L, "Comprar criptoactivos de gran capitalización exige tolerar caídas del 50 %."),
    ("CRI", None, L, "Vender altcoins pequeñas reduce el riesgo de liquidez del ámbito."),
    ("CRI", None, L, "Las stablecoins superan los 200.000 millones de dólares en circulación."),
    ("CRI", None, L, "La correlación de las criptomonedas con el Nasdaq ronda 0,5."),
    ("CRI", None, T13, "La probabilidad de un nuevo invierno cripto aumenta tras una caída del 30 % desde máximos."),
    ("CRI", None, T21, "Invertir en DeFi exige revisar el riesgo de contrato inteligente."),
    ("CRI", None, L, "El índice CoinDesk 20 es un ejemplo de referencia amplia del ámbito."),
    ("CRI", None, L, "Los ETF de bitcoin al contado reciben 1.200 millones en la semana."),
    ("CRI", None, L, "La tasa de financiación de los perpetuos está en terreno positivo."),
    ("CRI", None, T21, "Vender exposición a NFT reduce el riesgo de liquidez del ámbito."),
    ("CRI", None, T21, "Comprar RWA tokenizados de deuda pública es la parte prudente del ámbito."),
    ("CRI", "R21", EV, "Comprar SOL y AVAX antes de la actualización de la red."),
    ("CRI", "R21", EV, "Vender el token PEPE por su falta de liquidez."),
    ("CRI", "R21", EV, "Recomendamos el ETF IBIT para la exposición a bitcoin."),
    ("CRI", "R21", EV, "Invertir en MicroStrategy Inc como vehículo apalancado."),
    ("CRI", "R13", EV, "La probabilidad de que bitcoin supere los 150.000 dólares en H3 es del 30 %."),
    ("CRI", "R13", EV, "Damos un 55 % de probabilidad a la aprobación de un ETF de solana."),
    # ------------------------------------------------------------------ ALT
    ("ALT", None, T21, "El capital riesgo afronta un entorno de salidas lento, con las IPO todavía escasas."),
    ("ALT", None, L, "Comprar deuda privada directa ofrece primas de iliquidez de 200 a 300 puntos básicos."),
    ("ALT", None, L, "Los hedge funds macro ganan un 6 % en el año con la dispersión de los bancos centrales."),
    ("ALT", None, T13, "Es probable que las valoraciones del capital privado se ajusten con retraso a las cotizadas."),
    ("ALT", None, L, "Invertir en infraestructuras aporta flujos ligados a la inflación."),
    ("ALT", None, L, "Vender capital riesgo en el secundario implica descuentos del 10 % al 15 %."),
    ("ALT", None, T13, "La probabilidad de impagos en deuda privada crece con tipos del 5 %."),
    ("ALT", None, L, "Los bonos catástrofe ofrecen diferenciales del 7 % por encima del monetario."),
    ("ALT", None, L, "Sobreponderar estrategias de seguimiento de tendencia tiene sentido con alta volatilidad."),
    ("ALT", None, L, "El arte y el vino no son invertibles en el ámbito sin vehículo con liquidez suficiente."),
    ("ALT", None, L, "Las estrategias long/short de renta variable reducen su exposición neta al 35 %."),
    ("ALT", None, L, "Comprar infraestructuras cotizadas da liquidez diaria a un ámbito ilíquido."),
    ("ALT", None, L, "La correlación de los hedge funds con la bolsa se sitúa en 0,6."),
    ("ALT", None, T21, "Invertir en ELTIF de infraestructuras abre el capital privado al minorista."),
    ("ALT", None, L, "La captación de capital riesgo cae un 20 % interanual."),
    ("ALT", "R21", EV, "Invertir en Blackstone Inc es la forma más directa de exponerse al capital privado."),
    ("ALT", "R21", EV, "Comprar el ELTIF LU2524194378 para la parte ilíquida."),
    ("ALT", "R21", EV, "Recomendamos comprar KKR antes de sus resultados."),
    ("ALT", "R21", EV, "Vender el fondo DBMF de seguimiento de tendencia."),
    ("ALT", "R13", EV, "La probabilidad de que el capital riesgo recupere las salidas en 2027 es del 40 %."),
    ("ALT", "R13", EV, "Asignamos un 65 % de probabilidad a que los hedge funds macro batan a la bolsa."),
    # ------------------------------------------------------------------ MON
    ("MON", None, L, "El BCE mantiene el tipo de depósito en el 2 %."),
    ("MON", None, T13, "Es probable que la Fed recorte dos veces más antes del verano."),
    ("MON", None, L, "Los activos monetarios en euros rinden un 2,1 %, por encima de la inflación subyacente."),
    ("MON", None, L, "Comprar letras del Tesoro a seis meses fija la rentabilidad antes de los recortes."),
    ("MON", None, T13, "La probabilidad de un recorte en marzo ha bajado tras un paro del 3,9 %."),
    ("MON", None, T13, "El mercado descuenta con alta probabilidad un recorte hasta el 1,75 % en 2027."),
    ("MON", None, L, "Vender monetario en dólares y comprar en euros reduce el riesgo de cambio."),
    ("MON", None, L, "El euríbor a doce meses cae al 2,2 %."),
    ("MON", None, L, "La curva monetaria descuenta un tipo terminal del 3,25 % en EE. UU."),
    ("MON", None, L, "Invertir en depósitos a plazo es la alternativa sin riesgo de mercado del ámbito."),
    ("MON", None, L, "El BOE recorta 25 puntos básicos, hasta el 4 %."),
    ("MON", None, L, "Los fondos monetarios estadounidenses superan los 7 billones de dólares."),
    ("MON", None, T13, "Es poco probable que el tipo de depósito baje del 1,5 % en este ciclo."),
    ("MON", None, L, "Sobreponderar liquidez es prudente mientras el régimen siga sin señal clara."),
    ("MON", None, T13, "La posibilidad de una subida del BOJ al 0,75 % gana peso en la semana."),
    ("MON", "R13", EV, "La probabilidad de un recorte de la Fed en diciembre es del 80 %."),
    ("MON", "R13", EV, "Asignamos un 70 % de probabilidad a que el BCE baje el tipo de depósito al 1,75 %."),
    ("MON", "R13", EV, "Hay un 30 % de posibilidades de que el BOE suba tipos."),
    ("MON", "R13", EV, "Probabilidad estimada de recorte en marzo: 65 %."),
    ("MON", "R21", EV, "Comprar el ETF XEON para aparcar la liquidez."),
    ("MON", "R21", EV, "Comprar la letra ES0L02606125 en la subasta del martes."),
    ("MON", "R21", EV, "Invertir en el fondo monetario LU0128494944 es nuestra opción."),
    # ------------------------------------------------------------------ TCV
    ("TCV", None, L, "La pendiente 2s10s estadounidense pasa a terreno positivo por primera vez en dos años."),
    ("TCV", None, L, "Comprar pendiente en la curva euro es la expresión más limpia de un BCE que recorta."),
    ("TCV", None, L, "La inflación implícita a cinco años en cinco años se sitúa en el 2,3 %."),
    ("TCV", None, L, "El índice iTraxx Crossover cotiza en 290 puntos básicos."),
    ("TCV", None, T13, "Es probable que el MOVE siga elevado mientras la Fed dependa de los datos."),
    ("TCV", None, T21, "Vender MOVE tiene sentido cuando está en el percentil 90 de su historia."),
    ("TCV", None, L, "La prima por plazo del Treasury a 10 años vuelve a terreno positivo."),
    ("TCV", None, L, "Comprar breakevens es barato con la inflación implícita por debajo de la esperada."),
    ("TCV", None, T21, "Comprar VSTOXX como factor protege frente a un repunte de la tensión europea."),
    ("TCV", None, L, "Los diferenciales de CDS soberanos de la periferia están en mínimos de cinco años."),
    ("TCV", None, T13, "La probabilidad de que la curva se aplane ha aumentado tras subir la TIR a 2 años al 4,1 %."),
    ("TCV", None, T21, "Sobreponderar el diferencial IG frente a HY reduce la convexidad negativa."),
    ("TCV", None, L, "La correlación implícita del S&P 500 cae a 10 puntos, mínimo histórico."),
    ("TCV", None, L, "El swap de inflación a diez años en euros cotiza al 2,1 %."),
    ("TCV", None, T21, "Comprar futuros de SOFR a un año es la forma de jugar más recortes de la Fed."),
    ("TCV", "R21", EV, "Comprar el futuro FGBLZ6 del Bund para jugar la caída de tipos."),
    ("TCV", "R21", EV, "Vender el ETF VIXY antes de que se normalice la curva del VIX."),
    ("TCV", "R21", EV, "Recomendamos el ETF TBT para apostar por la subida de la TIR."),
    ("TCV", "R13", EV, "La probabilidad de que la 2s10s supere 50 puntos básicos en H3 es del 45 %."),
    ("TCV", "R13", EV, "Asignamos un 60 % de probabilidad a que el iTraxx Crossover se amplíe."),
    ("TCV", "R13", EV, "La inflación implícita bajará del 2 % con una probabilidad del 70 %."),
]

DUDOSAS = [
    "Comprar BTC y ETH en las caídas.",                              # bitcoin como segmento o como token concreto
    "Probabilidad de impago a un año del high yield: 4 %.",          # métrica de crédito o pronóstico
    "Las opciones sobre el oro reflejan una probabilidad del 25 % de superar los 3.000 dólares.",   # implícita de mercado
    "Con una probabilidad de dos tercios, el BCE recortará en enero.",   # cifra en palabras
    "Compramos Telefónica para el horizonte H3.",                    # nombre propio sin código (límite declarado)
]


def permitidos():
    tmp = Path(tempfile.mkdtemp(prefix="r02_t102_"))
    b = Bloque(config_pruebas(diseno="v6", perfiles={"activos": list(CLASES)}), ProveedorCSV(DATOS),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    return v6.permitidos_r21(b)


def _pct(a: int, b: int) -> str:
    return f"{a}/{b} = {100 * a / b:.1f} %" if b else "0/0"


def main() -> int:
    perm = permitidos()
    vistos = set()
    for _t, _e, _g, f in BANCO:
        assert f not in vistos, f"frase repetida: {f}"
        vistos.add(f)
    tipos = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
    assert {t for t, *_ in BANCO} == set(tipos)
    por_tipo: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])   # legítimas, FP, prohibidas, FN
    por_grupo: dict[str, list[int]] = defaultdict(lambda: [0, 0])          # casos, fallos
    fp_regla: dict[str, int] = defaultdict(int)
    fn_regla: dict[str, list[int]] = {"R13": [0, 0], "R21": [0, 0]}
    regla_mal, fallos = [], []
    for tipo, esperado, grupo, frase in BANCO:
        obt = v6.texto_prohibido(frase, perm)
        c = por_tipo[tipo]
        por_grupo[grupo][0] += 1
        if esperado is None:
            c[0] += 1
            if obt:
                c[1] += 1
                por_grupo[grupo][1] += 1
                fp_regla[obt] += 1
                fallos.append(("FP", tipo, grupo, frase, obt))
        else:
            c[2] += 1
            fn_regla[esperado][0] += 1
            if obt is None:
                c[3] += 1
                por_grupo[grupo][1] += 1
                fn_regla[esperado][1] += 1
                fallos.append(("FN", tipo, grupo, frase, esperado))
            elif obt != esperado:
                regla_mal.append((tipo, frase, esperado, obt))
    print(f"{'tipo':5} {'legít.':>6} {'FP':>4} {'prohib.':>7} {'FN':>4}")
    tot = [0, 0, 0, 0]
    for tipo in tipos:
        c = por_tipo[tipo]
        print(f"{tipo:5} {c[0]:6} {c[1]:4} {c[2]:7} {c[3]:4}")
        tot = [a + b for a, b in zip(tot, c)]
    print(f"{'TOTAL':5} {tot[0]:6} {tot[1]:4} {tot[2]:7} {tot[3]:4}")
    print(f"Falsos positivos: {_pct(tot[1], tot[0])} de las legítimas; por regla que las quita: {dict(fp_regla)}")
    for g in (L, T13, T21):
        print(f"  legítimas {g}: {_pct(por_grupo[g][1], por_grupo[g][0])}")
    print(f"Falsos negativos: {_pct(tot[3], tot[2])} de las prohibidas")
    for r, (n, fn) in fn_regla.items():
        print(f"  {r}: {_pct(fn, n)}")
    for g in (EV, DF):
        print(f"  prohibidas {g}: {_pct(por_grupo[g][1], por_grupo[g][0])}")
    print(f"Cazadas con otra regla: {len(regla_mal)}")
    for x in regla_mal:
        print("  ", x)
    print("Fallos:")
    for f in fallos:
        print(f"  [{f[0]}] {f[1]:4} {f[2]:8} ({f[4]}) «{f[3]}»")
    print("Dudosas (no cuentan):")
    for d in DUDOSAS:
        print(f"  {v6.texto_prohibido(d, perm)}: «{d}»")
    if DETALLE:
        for tipo, esperado, g, frase in BANCO:
            print(f"  {tipo:4} {g:8} esperado={esperado} obtenido={v6.texto_prohibido(frase, perm)} «{frase}»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
