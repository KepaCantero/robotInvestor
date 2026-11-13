"""QA r01 de T-102 · Banco nuevo de frases de informes de los doce tipos de activo contra el filtro R13/R21 frase a frase.

Frases como las que escribe el Sintetizador (régimen, factores, lectura del conjunto, preguntas y textos llanos), en español,
de los doce tipos (RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON y TCV). Cada una lleva la etiqueta que le da el revisor:
- None: legítima. No da una probabilidad numérica de un pronóstico (R13) ni compra, vende o recomienda un instrumento concreto
  (R21). Citar un fondo o un índice como ejemplo del ámbito es legítimo (R21: «solo puede citar nombres concretos como ejemplos
  ilustrativos del ámbito»); comprar o vender un segmento, una divisa, un par, una región, una calificación o un índice también.
- "R13" o "R21": prohibida. R21 solo con un patrón que el README promete (un código tras un verbo de compra, venta o inversión,
  un ISIN, un sufijo societario o una emisión con vencimiento). El nombre propio sin código ni sufijo (límite declarado) no está.
Las frases dudosas (BTC como código permitido, «suscribir … FI») van aparte, en DUDOSAS, y no cuentan en las tasas.

Cada frase lleva además una marca de grupo para separar las tasas:
- "sigla": la frase legítima lleva un verbo de compra, venta o inversión seguido de una sigla en mayúsculas;
- "llana": el resto.

Uso (desde la raíz del repositorio; la raíz del código a atacar es opcional, por defecto el repositorio):
  .venv/bin/python -I .docs/tickets/T-102/revisores/r01_banco_frases.py [<raiz_repo>] [--detalle]
Imprime las tasas de falsos positivos y negativos por tipo y en total, y la lista de fallos. No escribe nada.
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

L, S = "llana", "sigla"
# (tipo, etiqueta esperada, grupo, frase)
BANCO: list[tuple[str, str | None, str, str]] = [
    # ------------------------------------------------------------------ RV
    ("RV", None, L, "La renta variable de EE. UU. sube un 2,1 % en el mes, con la tecnología a la cabeza."),
    ("RV", None, L, "El sector financiero europeo gana impulso tras la subida de tipos del BCE."),
    ("RV", None, L, "Sobreponderar tecnología frente a utilities es la lectura del régimen actual."),
    ("RV", None, L, "Las tres opciones de RV comparten el factor crecimiento."),
    ("RV", None, L, "El ETF del sector (XLK) es solo un ejemplo del ámbito."),
    ("RV", None, L, "Puede tener sentido reducir exposición a RV cíclica si el PMI cae por debajo de 50."),
    ("RV", None, L, "Conviene vender parte de la exposición a energía tras la subida del 15 %."),
    ("RV", None, L, "El sector salud (XLV) defiende bien en las caídas."),
    ("RV", None, S, "Invertir en IA sigue siendo el tema dominante del mercado."),
    ("RV", None, S, "Sobreponderar LATAM frente a Asia gana peso con el dólar débil."),
    ("RV", None, S, "Comprar compañías con PER bajo ha batido al índice este trimestre."),
    ("RV", "R21", L, "Conviene comprar AAPL y MSFT esta semana."),
    ("RV", "R21", L, "Comprar: NVDA, AMD y AVGO."),
    ("RV", "R21", L, "Recomendamos vender las acciones de Inditex (ITX.MC)."),
    ("RV", "R21", L, "Apostar por NVDA antes de resultados."),
    ("RV", "R21", L, "Sobreponderar Apple Inc frente al índice."),
    ("RV", "R21", L, "Conviene comprar, por valoración, META."),
    ("RV", "R13", L, "La probabilidad de que el S&P 500 suba este mes es del 70 %."),
    # ------------------------------------------------------------------ RF
    ("RF", None, L, "La curva de EE. UU. se empina: el diferencial entre 2 y 10 años sube 15 pb."),
    ("RF", None, L, "Conviene comprar duración si la inflación sigue bajando."),
    ("RF", None, L, "La TIR del bono a 10 años alemán ronda el 2,6 %."),
    ("RF", None, L, "El crédito HY (HYG como ejemplo) sufre con la subida de diferenciales."),
    ("RF", None, L, "Vender duración larga protege si el BCE retrasa los recortes."),
    ("RF", None, L, "La compra de bonos ligados a la inflación (TIPS) gana sentido con el IPC al alza."),
    ("RF", None, L, "El mercado descuenta dos recortes del BCE antes de junio."),
    ("RF", None, L, "Conviene vender bonos de EE. UU. a largo si sube la prima por plazo."),
    ("RF", None, S, "Comprar crédito BBB a dos años ofrece un diferencial atractivo frente al Tesoro."),
    ("RF", None, S, "La venta de bonos del Tesoro de EE.UU. por bancos centrales extranjeros continúa."),
    ("RF", "R21", L, "Comprar el bono del Tesoro con vencimiento en 2034."),
    ("RF", "R21", L, "Comprar US912810TM08 para fijar el tipo."),
    ("RF", "R21", L, "Conviene comprar el ETF TLT antes de la Fed."),
    ("RF", "R21", L, "Invertir en LQD es la forma más simple de exponerse al crédito."),
    ("RF", "R13", L, "Hay un 65 % de probabilidad de que el BCE recorte en junio."),
    ("RF", "R13", L, "Las probabilidades de un recorte en marzo son del 60 %."),
    # ------------------------------------------------------------------ DIV
    ("DIV", None, L, "El dólar se fortalece frente a las divisas emergentes."),
    ("DIV", None, L, "El carry en MXN sigue siendo atractivo con baja volatilidad."),
    ("DIV", None, L, "Vender JPY frente a USD es la operación de carry clásica."),
    ("DIV", None, L, "El par EURUSD cae un 1,2 % en la semana."),
    ("DIV", None, L, "Comprar CHF como refugio tiene sentido si sube la aversión al riesgo."),
    ("DIV", None, L, "La libra (GBP) depende del dato de inflación del Reino Unido."),
    ("DIV", None, L, "Comprar divisas de materias primas (AUD, CAD, NOK) encaja con el ciclo."),
    ("DIV", None, L, "El yen se aprecia tras la intervención del BOJ."),
    ("DIV", None, S, "Conviene vender EUR/USD si el BCE recorta antes que la Fed."),
    ("DIV", None, S, "El mercado compra USD/JPY por el diferencial de tipos."),
    ("DIV", "R13", L, "Probabilidad de que el euro caiga: 70 %."),
    ("DIV", "R13", L, "El euro tiene un 60 % de probabilidades de caer frente al dólar."),
    ("DIV", "R21", L, "Comprar el ETF FXE para exponerse al euro."),
    ("DIV", "R21", L, "Conviene vender UUP y comprar FXY."),
    ("DIV", "R21", L, "Para la cobertura, comprar: FXF."),
    # ------------------------------------------------------------------ MP
    ("MP", None, L, "El oro sube un 3 % en el mes por las compras de los bancos centrales."),
    ("MP", None, L, "La compra de WTI se recupera tras el recorte de la OPEP."),
    ("MP", None, L, "El cobre del LME marca máximos del año."),
    ("MP", None, L, "Vender crudo BRENT frente a WTI aprovecha el diferencial."),
    ("MP", None, L, "El ETF de oro (GLD) es solo un ejemplo del ámbito."),
    ("MP", None, L, "Las materias primas agrícolas sufren por la cosecha récord."),
    ("MP", None, L, "Conviene vender parte de la exposición a metales industriales si China frena."),
    ("MP", None, L, "Comprar plata (XAG) tiene sentido si el dólar se debilita."),
    ("MP", None, S, "Conviene comprar gas TTF para el invierno si los inventarios bajan."),
    ("MP", None, S, "Vender el índice BCOM frente al oro ha funcionado en el ciclo."),
    ("MP", "R21", L, "Comprar USO antes de la reunión de la OPEP."),
    ("MP", "R21", L, "Conviene vender las acciones de BHP y comprar RIO."),
    ("MP", "R21", L, "Invertir en Glencore plc para el ciclo del cobre."),
    ("MP", "R13", L, "El oro tiene una probabilidad del 75 % de superar los 2.500 dólares."),
    ("MP", "R13", L, "Probabilidad de subida del crudo: 80 %."),
    # ------------------------------------------------------------------ IDX
    ("IDX", None, L, "El S&P 500 sube un 1,5 % en la semana."),
    ("IDX", None, L, "Conviene vender MSCI World frente a emergentes según el régimen."),
    ("IDX", None, L, "Comprar el índice Nikkei 225 cubierto en divisa encaja con el yen débil."),
    ("IDX", None, L, "El IBEX 35 se apoya en la banca."),
    ("IDX", None, L, "La venta de índices de EE. UU. se acelera tras el dato de empleo."),
    ("IDX", None, L, "El índice indio (^NSEI) sube un 4 % en el trimestre."),
    ("IDX", None, L, "Sobreponderar Japón frente a Europa es la lectura del régimen."),
    ("IDX", None, L, "Las bolsas emergentes (EM) recuperan terreno."),
    ("IDX", None, S, "Invertir en el EURO STOXX 50 tiene sentido si mejora el PMI europeo."),
    ("IDX", None, S, "Invertir en el MSCI ACWI es la forma más sencilla de diversificar."),
    ("IDX", None, S, "Comprar el CSI 300 tiene sentido si China estimula."),
    ("IDX", "R21", L, "Comprar el ETF VOO es la mejor forma de exponerse al S&P 500."),
    ("IDX", "R21", L, "Recomendamos comprar SPY esta semana."),
    ("IDX", "R21", L, "Invertir en el fondo LU0274208692 para replicar el índice."),
    ("IDX", "R13", L, "Hay un 70 % de probabilidad de que el S&P 500 cierre el año en positivo."),
    ("IDX", "R13", L, "La probabilidad de una corrección del 10 % es del 30 %."),
    # ------------------------------------------------------------------ FON
    ("FON", None, L, "Los fondos de gestión alternativa (QAI como ejemplo) amortiguan las caídas."),
    ("FON", None, L, "Los fondos de futuros gestionados ganan con las tendencias fuertes."),
    ("FON", None, L, "Conviene vender fondos de retorno absoluto si la dispersión cae."),
    ("FON", None, L, "Invertir en fondos de fusiones y adquisiciones rinde un 4 % anual de media."),
    ("FON", None, L, "Las opciones de FON comparten poca correlación con la RV."),
    ("FON", None, L, "El descuento de los fondos cerrados se estrecha 2 puntos."),
    ("FON", None, S, "Invertir en fondos con TER bajo mejora la rentabilidad neta."),
    ("FON", None, S, "La compra de fondos cerrados con descuento sobre el NAV es una idea recurrente."),
    ("FON", "R21", L, "Comprar el fondo LU0996182563 cuanto antes."),
    ("FON", "R21", L, "Invertir en DBMF para cubrir la cartera."),
    ("FON", "R21", L, "Vender MNA y comprar QAI."),
    ("FON", "R13", L, "Los fondos de tendencia tienen un 60 % de posibilidades de batir al índice."),
    # ------------------------------------------------------------------ DER
    ("DER", None, L, "La venta de opciones de compra sobre el S&P 500 rinde un 1,5 % mensual."),
    ("DER", None, L, "Comprar protección con opciones de venta encarece la cartera en un 2 % anual."),
    ("DER", None, L, "El índice BXM (^BXM) bate a la RV en mercados laterales."),
    ("DER", None, L, "La estructura temporal del VIX está en contango."),
    ("DER", None, L, "Conviene vender volatilidad solo si el VIX está por encima de su media."),
    ("DER", None, L, "Comprar futuros del Euro Stoxx encaja con la cobertura del riesgo de cola."),
    ("DER", None, L, "Las opciones sobre tipos descuentan movimientos amplios."),
    ("DER", None, S, "Vender straddles sobre el SPX rinde un 1 % al mes con volatilidad baja."),
    ("DER", None, S, "El VaR al 95 % de confianza de la estrategia es del 2,1 %."),
    ("DER", "R21", L, "Comprar la opción call de AAPL a 200 con vencimiento en marzo."),
    ("DER", "R21", L, "Vender puts de TSLA para cobrar la prima."),
    ("DER", "R21", L, "Comprar TAIL como cobertura de cola."),
    ("DER", "R13", L, "El mercado de opciones da un 25 % de probabilidad a una caída del 10 %."),
    ("DER", "R13", L, "La probabilidad implícita de un movimiento del 5 % es del 18 %."),
    # ------------------------------------------------------------------ INM
    ("INM", None, L, "El sector inmobiliario cotizado (REIT) sufre con los tipos altos."),
    ("INM", None, L, "Comprar inmobiliario logístico tiene sentido si cae la vacancia."),
    ("INM", None, L, "Las opciones de INM pierden un 3 % en el mes."),
    ("INM", None, L, "Conviene vender exposición a oficinas mientras suba la vacancia."),
    ("INM", None, L, "El inmobiliario global (VNQ como ejemplo) depende del tipo a 10 años."),
    ("INM", None, L, "La compra de inmuebles comerciales en Europa cae un 20 %."),
    ("INM", None, S, "Invertir en SOCIMI cotizadas da exposición al alquiler residencial."),
    ("INM", "R21", L, "Comprar VNQ antes del recorte de la Fed."),
    ("INM", "R21", L, "Conviene vender las acciones de PLD esta semana."),
    ("INM", "R13", L, "La probabilidad de que bajen los alquileres es del 40 %."),
    # ------------------------------------------------------------------ CRI
    ("CRI", None, L, "Las criptomonedas de gran capitalización suben un 8 % en la semana."),
    ("CRI", None, L, "La volatilidad de las criptomonedas triplica la de la RV."),
    ("CRI", None, L, "Conviene vender parte de la exposición a cripto tras la subida del 30 %."),
    ("CRI", None, L, "La entrada de flujos en los ETF de bitcoin al contado se modera."),
    ("CRI", None, L, "Las tres opciones de CRI comparten el factor liquidez."),
    ("CRI", "R21", L, "Comprar SOL y AVAX antes de la actualización."),
    ("CRI", "R21", L, "Invertir en COIN para exponerse a cripto."),
    ("CRI", "R21", L, "Conviene comprar el ETF IBIT esta semana."),
    ("CRI", "R13", L, "Bitcoin tiene un 70 % de probabilidades de superar su máximo."),
    # ------------------------------------------------------------------ ALT
    ("ALT", None, L, "El capital privado (PSP como ejemplo) depende de las salidas a bolsa."),
    ("ALT", None, L, "Invertir en deuda privada ofrece un diferencial de 300 pb sobre el crédito HY."),
    ("ALT", None, L, "Comprar bonos catástrofe aporta descorrelación con la RV."),
    ("ALT", None, L, "Invertir en infraestructuras encaja con la inflación persistente."),
    ("ALT", None, L, "Conviene vender exposición a capital riesgo si se cierran las salidas a bolsa."),
    ("ALT", None, S, "Invertir en ILS tiene sentido tras una temporada de huracanes tranquila."),
    ("ALT", "R21", L, "Comprar BIZD para el dividendo."),
    ("ALT", "R21", L, "Invertir en Blackstone Inc para el capital privado."),
    ("ALT", "R21", L, "Conviene comprar ARCC y MAIN esta semana."),
    ("ALT", "R13", L, "El escenario de recuperación del capital privado tiene una probabilidad del 55 %."),
    # ------------------------------------------------------------------ MON
    ("MON", None, L, "Las letras del Tesoro a tres meses rinden un 3,8 %."),
    ("MON", None, L, "Invertir en fondos monetarios protege si la RV corrige."),
    ("MON", None, L, "Conviene comprar liquidez en EUR mientras el BCE mantenga el depósito en el 2 %."),
    ("MON", None, L, "La compra de letras en la subasta sube un 10 %."),
    ("MON", None, L, "Las opciones de MON apenas varían en el mes."),
    ("MON", None, L, "La liquidez en USD (BIL como ejemplo) rinde más que en EUR."),
    ("MON", None, S, "Invertir en FMM a corto plazo da un 3 % sin riesgo de duración."),
    ("MON", "R21", L, "Comprar SHV para aparcar la liquidez."),
    ("MON", "R21", L, "Invertir en XEON.DE para la liquidez en euros."),
    ("MON", "R21", L, "Conviene comprar la letra ES0L02501103 en la próxima subasta."),
    ("MON", "R13", L, "Hay un 90 % de probabilidad de que el BCE mantenga el tipo."),
    # ------------------------------------------------------------------ TCV
    ("TCV", None, L, "El diferencial BAMLH0A0HYM2 se estrecha 20 pb en el mes."),
    ("TCV", None, L, "La pendiente CURVA-USD-2S10S-TR vuelve a positivo."),
    ("TCV", None, L, "Comprar volatilidad del MOVE encaja con la incertidumbre de tipos."),
    ("TCV", None, L, "El breakeven a 10 años (T10YIE) sube al 2,4 %."),
    ("TCV", None, L, "Vender el diferencial de crédito HY tiene sentido si el ciclo se deteriora."),
    ("TCV", None, L, "Conviene comprar pendiente en la curva de EE. UU. si la Fed recorta."),
    ("TCV", None, L, "El tipo a 10 años (^TNX) baja 15 pb tras el IPC."),
    ("TCV", None, S, "Conviene no vender volatilidad antes de la reunión del FOMC."),
    ("TCV", "R21", L, "Comprar el futuro VXX para cubrir la cartera."),
    ("TCV", "R21", L, "Comprar el bono a 10 años con vencimiento 2035 para jugar la curva."),
    ("TCV", "R13", L, "La probabilidad de inversión de la curva este año es del 35 %."),
    ("TCV", "R13", L, "El modelo asigna una probabilidad del 65 % a que el diferencial se amplíe."),
    # ------------------------------------------------------------------ textos generales del informe
    ("GEN", None, L, "Aún hay pocos casos para saber si acertamos más que el azar."),
    ("GEN", None, L, "Los pronósticos acertaron el 58 % de las veces en el historial."),
    ("GEN", None, L, "La probabilidad de acierto aún no está certificada."),
    ("GEN", None, L, "Nada de esto es un consejo para comprar o vender."),
    ("GEN", None, L, "¿Qué haría cambiar el semáforo de RV?"),
    ("GEN", "R13", L, "Con un 80 % de seguridad, la renta variable sube este mes."),
    ("GEN", "R13", L, "El escenario alcista tiene una probabilidad estimada del 65 %."),
]

# Dudosas: se enseñan, pero no cuentan en las tasas.
DUDOSAS = [
    "Comprar BTC ahora.",                                  # BTC es un código permitido de la configuración
    "Comprar ETH antes de la actualización.",              # ídem, ETH
    "Conviene suscribir el fondo Magallanes Iberian Equity FI.",   # nombre propio con forma jurídica de fondo
    "Banco Santander S.A. publica resultados el martes.",  # mención de una sociedad con sufijo, sin verbo
    "La posibilidad de subidas del 0,25 % gana peso.",     # 0,25 % es el tamaño de la subida, no una probabilidad
]


def permitidos():
    tmp = Path(tempfile.mkdtemp(prefix="r01_t102_"))
    b = Bloque(config_pruebas(diseno="v6", perfiles={"activos": list(CLASES)}), ProveedorCSV(DATOS),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    return v6.permitidos_r21(b)


def main() -> int:
    perm = permitidos()
    por_tipo: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])   # legítimas, FP, prohibidas, FN
    por_grupo: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    regla_mal: list[tuple[str, str, str, str]] = []
    fallos: list[tuple[str, str, str, str | None]] = []
    for tipo, esperado, grupo, frase in BANCO:
        obtenido = v6.texto_prohibido(frase, perm)
        c = por_tipo[tipo]
        if esperado is None:
            c[0] += 1
            por_grupo[grupo][0] += 1
            if obtenido:
                c[1] += 1
                por_grupo[grupo][1] += 1
                fallos.append(("FP", tipo, frase, obtenido))
        else:
            c[2] += 1
            if obtenido is None:
                c[3] += 1
                fallos.append(("FN", tipo, frase, esperado))
            elif obtenido != esperado:
                regla_mal.append((tipo, frase, esperado, obtenido))
    print(f"{'tipo':5} {'legít.':>6} {'FP':>4} {'prohib.':>7} {'FN':>4}")
    tot = [0, 0, 0, 0]
    for tipo, c in por_tipo.items():
        print(f"{tipo:5} {c[0]:6} {c[1]:4} {c[2]:7} {c[3]:4}")
        tot = [a + b for a, b in zip(tot, c)]
    print(f"{'TOTAL':5} {tot[0]:6} {tot[1]:4} {tot[2]:7} {tot[3]:4}")
    print(f"Falsos positivos: {tot[1]}/{tot[0]} = {100 * tot[1] / tot[0]:.1f} % de las legítimas")
    for g, (n, fp) in por_grupo.items():
        print(f"  grupo {g}: {fp}/{n} = {100 * fp / n:.1f} %")
    fn_r = {r: [0, 0] for r in ("R13", "R21")}
    for tipo, esperado, _g, frase in BANCO:
        if esperado:
            fn_r[esperado][0] += 1
            fn_r[esperado][1] += v6.texto_prohibido(frase, perm) is None
    print(f"Falsos negativos: {tot[3]}/{tot[2]} = {100 * tot[3] / tot[2]:.1f} % de las prohibidas")
    for r, (n, fn) in fn_r.items():
        print(f"  {r}: {fn}/{n} = {100 * fn / n:.1f} %")
    print(f"Cazadas con otra regla: {len(regla_mal)}")
    for x in regla_mal:
        print("  ", x)
    print("Fallos:")
    for f in fallos:
        print(f"  [{f[0]}] {f[1]:4} ({f[3]}) «{f[2]}»")
    print("Dudosas (no cuentan):")
    for d in DUDOSAS:
        print(f"  {v6.texto_prohibido(d, perm)}: «{d}»")
    if DETALLE:
        for tipo, esperado, _g, frase in BANCO:
            print(f"  {tipo:4} esperado={esperado} obtenido={v6.texto_prohibido(frase, perm)} «{frase}»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
