"""QA r04 de T-102 · Banco nuevo de control, escrito ANTES de leer las expresiones de la r04 y sin mirar los bancos de las
rondas anteriores salvo para no repetir sus formas. El implementador no lo ha visto.

Grupos:
- Legítimas (no deben quitarse): «llana» (sin siglas), «sigla» (siglas de `v6.filtro_r21_codigos`), «marcador» (con
  marcadores), «prob_cualitativa» (palabras de probabilidad sin cifra), de los doce tipos. «ambigua»: números en letra que
  no son una probabilidad («los tres grandes bancos centrales»); el prompt dice «ninguna cifra», así que no cuentan como
  falso positivo, solo se informan.
- Prohibidas (deben quitarse y declararse): «r13» (probabilidad numérica por formas nuevas, en letra, con signos o con
  marcadores), «r21» (instrumento concreto por formas nuevas: código o sufijo que la regla promete cazar).
- Límites declarados de R21 (se cuentan aparte): «lim_nombre» (nombre propio sin código), «lim_minus» (ticker en minúscula sin
  vehículo), «lim_sigla» (ticker que coincide con una sigla de la lista), «lim_letra» (ticker de una letra sin vehículo).
- «exotica»: escrituras de mala fe (alfabetos que NFKC no pliega, numerales CJK, indicadores regionales). Se informan aparte.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_01_banco_nuevo.py <raiz_repo> [--detalle]
Los marcadores y los permitidos salen de un ciclo real (simulado) de los doce tipos. No escribe nada en el repositorio.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

TIPOS = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
LL, SG, MK, PC, AM = "llana", "sigla", "marcador", "prob_cualitativa", "ambigua"
R13, R21 = "r13", "r21"
LIM = ("lim_nombre", "lim_minus", "lim_sigla", "lim_letra")
EX = "exotica"

# {opp:OPP} se cambia por un opp_id real del tipo (o de otro tipo si ese no tiene opciones)
LEGITIMAS: list[tuple[str, str, str]] = [
    # RV
    ("RV", LL, "Las compañías pequeñas recuperan terreno cuando bajan los tipos."),
    ("RV", LL, "Los resultados del trimestre decepcionan en el consumo discrecional."),
    ("RV", SG, "La RV japonesa se beneficia de un JPY débil."),
    ("RV", SG, "Las recompras sostienen el BPA en EEUU más que las ventas."),
    ("RV", SG, "El sector de semiconductores sigue al SOX, que marca el tono de la IA."),
    ("RV", MK, "Dentro de {tipo:RV}, {opp:OPP} es la que más depende del crecimiento."),
    ("RV", MK, "Solo {n:RV} de las {candidatas:RV} ideas de {tipo:RV} superan los filtros."),
    ("RV", PC, "Es improbable que las tecnológicas sigan liderando sin mejores beneficios."),
    ("RV", SG, "Las small caps de la UE cotizan con descuento frente a las de EE. UU."),
    # RF
    ("RF", LL, "Alargar plazos tiene sentido si el banco central empieza a recortar."),
    ("RF", LL, "Los bonos de empresas aguantan mientras no suban los impagos."),
    ("RF", SG, "El BUND sigue siendo el refugio de la eurozona."),
    ("RF", SG, "La prima de los BTP frente a los OAT se estrecha."),
    ("RF", SG, "El crédito HY de EM sufre si el USD se aprecia."),
    ("RF", MK, "{opp:OPP} gana si la inflación de EE. UU. sigue bajando."),
    ("RF", MK, "Esta semana hay {n:RF} ideas de {tipo:RF}."),
    ("RF", PC, "Hay bastantes posibilidades de que el BCE espere a la primavera."),
    ("RF", SG, "La inflación implícita de los TIPS vuelve a subir."),
    # DIV
    ("DIV", LL, "La libra se debilita por la incertidumbre fiscal británica."),
    ("DIV", SG, "El AUD sigue al cobre y a la demanda china."),
    ("DIV", SG, "Vender CHF contra EUR funciona cuando baja la aversión al riesgo."),
    ("DIV", SG, "El diferencial entre la FED y el BOJ explica casi todo el movimiento del JPY."),
    ("DIV", MK, "{opp:OPP} depende del diferencial de tipos con el dólar."),
    ("DIV", MK, "En {tipo:DIV} hay {n:DIV} ideas de {candidatas:DIV} analizadas."),
    ("DIV", PC, "La probabilidad de una intervención en el yen ha aumentado."),
    ("DIV", SG, "El MXN y el BRL ofrecen carry, pero con más riesgo político."),
    ("DIV", LL, "Una moneda fuerte abarata las importaciones y frena la inflación."),
    # MP
    ("MP", LL, "El oro brilla cuando los tipos reales bajan."),
    ("MP", LL, "Las cosechas abundantes presionan los precios agrícolas."),
    ("MP", SG, "El BRENT reacciona a cada reunión de la OPEP."),
    ("MP", SG, "El WTI y el GNL dependen del invierno en el hemisferio norte."),
    ("MP", SG, "Los inventarios del LME de cobre siguen en mínimos."),
    ("MP", MK, "{opp:OPP} se apoya en la demanda industrial de China."),
    ("MP", MK, "En {tipo:MP} quedan {n:MP} ideas tras los filtros."),
    ("MP", PC, "Es probable que la OPEP mantenga los recortes de producción."),
    ("MP", SG, "La plata (XAG) acompaña al oro (XAU) con más volatilidad."),
    # IDX
    ("IDX", LL, "La bolsa mundial depende cada vez más de unas pocas tecnológicas."),
    ("IDX", SG, "El MSCI EM gana si China estimula su economía."),
    ("IDX", SG, "El IBEX tiene mucho peso de bancos y eléctricas."),
    ("IDX", SG, "El STOXX europeo cotiza con descuento frente al S&P."),
    ("IDX", SG, "El NIKKEI acusa la fortaleza del JPY."),
    ("IDX", MK, "{opp:OPP} representa la bolsa entera de su región."),
    ("IDX", MK, "De {candidatas:IDX} índices analizados, elegimos {n:IDX}."),
    ("IDX", PC, "Hay pocas opciones de que el DAX recupere máximos sin la industria."),
    ("IDX", SG, "El MSCI ACWI y el MSCI EAFE se separan cuando el dólar sube."),
    # FON
    ("FON", LL, "Los fondos de gestión alternativa reducen la dependencia de la bolsa."),
    ("FON", SG, "Los ETF de bajo coste ganan cuota frente a los fondos activos."),
    ("FON", SG, "El TER importa más cuanto más largo es el plazo."),
    ("FON", SG, "Las SICAV y los fondos UCITS tienen reglas de liquidez distintas."),
    ("FON", SG, "El descuento sobre el NAV de los fondos cerrados se ha ampliado."),
    ("FON", MK, "{opp:OPP} recoge el descuento de los fondos cerrados."),
    ("FON", MK, "En {tipo:FON} solo hay {n:FON} idea esta semana."),
    ("FON", PC, "Es poco probable que el descuento se cierre de golpe."),
    # DER
    ("DER", LL, "Vender opciones de compra cubiertas rinde más con el mercado lateral."),
    ("DER", LL, "La protección con opciones de venta cuesta más tras una caída."),
    ("DER", SG, "El VIX alto encarece las coberturas sobre el S&P."),
    ("DER", SG, "Los derivados OTC exigen más garantías desde la regulación de ESMA."),
    ("DER", MK, "Ninguna idea de {tipo:DER} pasa el filtro de {candidatas:DER} analizadas."),
    ("DER", PC, "Las probabilidades implícitas en las opciones apuntan a calma."),
    ("DER", SG, "El VSTOXX y el VIX suben a la vez cuando hay miedo."),
    # INM
    ("INM", LL, "Las oficinas sufren y la logística aguanta."),
    ("INM", SG, "Las SOCIMI dependen del coste de la financiación."),
    ("INM", SG, "Los REIT de EEUU recuperan cuando bajan los tipos largos."),
    ("INM", MK, "{opp:OPP} gana si los tipos largos bajan."),
    ("INM", MK, "En {tipo:INM} hay {n:INM} idea entre {candidatas:INM} candidatas."),
    ("INM", PC, "Es probable que las rentas de la logística sigan subiendo."),
    ("INM", SG, "Los REITS europeos cotizan por debajo de su NAV."),
    # CRI
    ("CRI", LL, "Los criptoactivos siguen muy ligados al apetito por el riesgo."),
    ("CRI", SG, "La regulación de la SEC pesa sobre los activos digitales."),
    ("CRI", SG, "Los RWA tokenizados atraen a gestoras tradicionales."),
    ("CRI", SG, "Los ETP de criptoactivos facilitan el acceso al inversor minorista."),
    ("CRI", MK, "{opp:OPP} se mueve con la liquidez global."),
    ("CRI", MK, "De {candidatas:CRI} ideas de {tipo:CRI}, se queda {n:CRI}."),
    ("CRI", PC, "Hay poca confianza en que la volatilidad se modere pronto."),
    # ALT
    ("ALT", LL, "El capital privado tarda años en devolver el dinero."),
    ("ALT", SG, "Los ELTIF abren el capital privado al inversor minorista en la UE."),
    ("ALT", SG, "La deuda privada compite con el HY cotizado."),
    ("ALT", MK, "{opp:OPP} depende de que las empresas puedan refinanciarse."),
    ("ALT", MK, "En {tipo:ALT} queda {n:ALT} idea."),
    ("ALT", PC, "Es probable que las valoraciones del capital privado tarden en ajustarse."),
    # MON
    ("MON", LL, "La liquidez remunera bien mientras los tipos sigan altos."),
    ("MON", SG, "El ESTR marca lo que paga la liquidez en euros."),
    ("MON", SG, "Los FMM de EEUU reciben entradas récord."),
    ("MON", SG, "Las letras del Tesoro siguen de cerca al SOFR."),
    ("MON", MK, "En {tipo:MON} no queda ninguna idea de las {candidatas:MON} analizadas."),
    ("MON", PC, "Es probable que la remuneración de la liquidez baje con los recortes."),
    ("MON", SG, "El EURIBOR a corto anticipa los movimientos del BCE."),
    # TCV
    ("TCV", LL, "La curva de tipos se empina cuando el mercado espera recortes."),
    ("TCV", LL, "Los diferenciales de crédito siguen estrechos pese a la desaceleración."),
    ("TCV", SG, "El MOVE refleja el nerviosismo del mercado de bonos."),
    ("TCV", SG, "Los CDS de los bancos europeos se mantienen tranquilos."),
    ("TCV", SG, "El VRP de la RV sigue siendo positivo."),
    ("TCV", MK, "{opp:OPP} depende de que la volatilidad siga baja."),
    ("TCV", MK, "En {tipo:TCV} hay {n:TCV} ideas, pero son {n_apuestas} apuestas en total."),
    ("TCV", PC, "La probabilidad de una recesión ha bajado, según los diferenciales."),
    ("TCV", SG, "La inflación implícita (BEI) y el OIS se separan."),
    # Comunes
    ("*", MK, "Esta semana hay {n_ideas} ideas en {n_tipos} tipos de inversión."),
    ("*", MK, "Aunque son {n_ideas} ideas, en el fondo son {n_apuestas} apuestas."),
    ("*", PC, "Con bastante confianza, el dólar seguirá mandando."),
    ("*", PC, "Las opciones de que la Fed recorte antes que el BCE son escasas."),
    ("*", LL, "Nada de esto es una recomendación de compra."),
    ("*", LL, "¿Cambiaría la lectura un dato de empleo más flojo?"),
    ("*", SG, "El riesgo común es un repunte del IPC en EEUU."),
    ("*", SG, "Las ideas de RV y de RF comparten el mismo factor: los tipos de la FED."),
    ("*", PC, "Aún no sabemos si acertamos más que el azar."),
    ("*", PC, "El historial es corto: los aciertos pueden ser suerte."),
    # Ambiguas (números en letra que no son probabilidad): solo se informan
    ("*", AM, "Los tres grandes bancos centrales se reúnen esta semana."),
    ("*", AM, "El oro encadena cuatro semanas al alza."),
    ("*", AM, "Dos de las ideas comparten el mismo factor."),
    ("*", AM, "La mitad de las ideas depende del dólar."),
    ("*", AM, "Es la primera vez en años que el BCE recorta antes que la Fed."),
]

# (grupo, frase). Formas que NO están en los bancos ni en los ataques de las r01 a r03 ni en las pruebas de la r04.
PROHIBIDAS: list[tuple[str, str]] = [
    # --- R13: probabilidad numérica sin dígitos
    (R13, "Las apuestas pagan tres contra uno a favor de la subida."),
    (R13, "Le damos nueve contra uno a que el BCE recorte."),
    (R13, "La probabilidad de recorte ronda el ochenta."),
    (R13, "La subida tiene una probabilidad del noventa."),
    (R13, "Le damos un ochenta por ciento a la pausa."),
    (R13, "Vemos un setenta porciento de opciones de subida."),
    (R13, "Le asignamos un setenta pct de probabilidad."),
    (R13, "Hay un tercio de opciones de recorte."),
    (R13, "La probabilidad de subida es de nueve décimos."),
    (R13, "La probabilidad de recorte es de tres quintos."),
    (R13, "La subida es probable en cuatro escenarios de cinco."),
    (R13, "Sale bien dos veces de tres."),
    (R13, "La probabilidad es de cero coma siete."),
    (R13, "Probabilidad estimada: setenta y cinco centésimas."),
    (R13, "Lo vemos casi al cien por cien."),
    (R13, "La probabilidad de impago es de una entre mil."),
    (R13, "Las posibilidades de subida son del ochenta."),
    (R13, "Damos un noventa y tantos de certeza al recorte."),
    (R13, "Hay una probabilidad de setenta y cinco sobre cien."),
    (R13, "Las probabilidades están al cincuenta-cincuenta."),
    (R13, "La probabilidad de subida es de setenta ٪."),
    (R13, "La probabilidad de subida es de setenta ﹪."),
    (R13, "Probabilidad de subida: setenta per cent."),
    (R13, "There is a seventy percent chance of a rally."),
    (R13, "The odds of a cut are three to one."),
    (R13, "La probabilidad de una recesión es del veinte y pico."),
    (R13, "Las opciones de que suba son de nueve sobre diez."),
    (R13, "Estimamos el riesgo de caída en un quinto."),
    (R13, "El escenario alcista tiene un peso de dos quintos."),
    (R13, "Confiamos al noventa en que el dólar suba."),
    # R13 con marcadores (composiciones que no estaban en la r03)
    (R13, "La probabilidad es de {n:RV} contra {n:RF}."),
    (R13, "Sale bien {n:RV} veces de {candidatas:RV}."),
    (R13, "La probabilidad de subida es de {n_tipos} décimas."),
    (R13, "Confianza de {n_ideas} por ciento en la subida."),
    (R13, "La probabilidad de recorte es {n:TCV} de {candidatas:TCV}."),
    (R13, "Le damos {n_apuestas} puntos de probabilidad sobre cien."),
    (R13, "Las opciones de subida son de {n:MP} entre {candidatas:MP}."),
    # --- R21: instrumento concreto que la regla promete cazar, por formas nuevas
    (R21, "Comprar NASDAQ:NVDA en la próxima caída."),
    (R21, "Comprar BME:ITX antes de resultados."),
    (R21, "Recomendamos «NVDA» como idea estrella."),
    (R21, "Recomendamos `NVDA` como idea estrella."),
    (R21, "La apuesta es **NVDA**."),
    (R21, "La apuesta es [NVDA]."),
    (R21, "Sobreponderar #NVDA ya."),
    (R21, "Comprar ＄NVDA ya."),
    (R21, "El valor que más nos gusta es NVDA's."),
    (R21, "Comprar N.V.D.A. ya."),
    (R21, "Comprar N V D A ya."),
    (R21, "Comprar N-V-D-A ya."),
    (R21, "Recomendamos Inditex SA para el consumo."),
    (R21, "Comprar Siemens AG en la debilidad."),
    (R21, "Recomendamos Allianz SE."),
    (R21, "Comprar ASML Holding N.V. ya."),
    (R21, "La opción preferida es Iberdrola, S. A."),
    (R21, "Comprar Shell plc."),
    (R21, "Comprar Samsung Co., Ltd."),
    (R21, "Recomendamos Cobas Internacional FI."),
    (R21, "Recomendamos Bestinver Bolsa, F.I."),
    (R21, "Recomendamos Azvalor Internacional FIL."),
    (R21, "Recomendamos el Vanguard FTSE All-World UCITS ETF."),
    (R21, "Recomendamos el tracker iwda para la RV global."),
    (R21, "Comprar el cotizado vwrl."),
    (R21, "La apuesta es la acción nvda."),
    (R21, "La apuesta es el título nvda."),
    (R21, "El ticker nvda es nuestra idea."),
    (R21, "La idea es el valor con símbolo nvda."),
    (R21, "Comprar la stablecoin usdt para la liquidez."),
    (R21, "Comprar el token pepe."),
    (R21, "Comprar la memecoin DOGE."),
    (R21, "La única idea de la semana es comprar BBVA."),
    (R21, "Vender en corto TSLA."),
    (R21, "Ponerse largo de META y corto de SNAP."),
    (R21, "Acumular MSFT en las caídas."),
    (R21, "Mantener GOOGL en cartera."),
    (R21, "Rotar de AAPL a NVDA."),
    (R21, "El fondo de oro físico SGLN es la forma de entrar."),
    (R21, "Para la liquidez, el monetario XEON es suficiente."),
    (R21, "En RF, el fondo IEAC es el que preferimos."),
    (R21, "El contrato CLZ es la forma de jugar el petróleo."),
    (R21, "La SICAV Cartesio X es la idea."),
    (R21, "La acción de Repsol es la idea de la semana."),
    (R21, "Los bonos de Telefónica son la idea de RF."),
    # --- Límites declarados de R21 (se cuentan aparte)
    ("lim_nombre", "Comprar Nvidia en la caída."),
    ("lim_nombre", "Recomendamos el fondo Cobas Selección."),
    ("lim_nombre", "Comprar bitcoin antes del halving."),
    ("lim_nombre", "La idea es Banco Santander."),
    ("lim_minus", "Comprar nvda ya."),
    ("lim_minus", "La idea de la semana es iwda."),
    ("lim_minus", "Vender tsla en corto."),
    ("lim_sigla", "Comprar COP ya."),
    ("lim_sigla", "Recomendamos DAX como idea."),
    ("lim_sigla", "Comprar NAV en la caída."),
    ("lim_sigla", "Comprar ASX antes de resultados."),
    ("lim_letra", "Comprar F ya."),
    ("lim_letra", "Vender T antes de resultados."),
    ("lim_letra", "La idea de la semana es V."),
    # --- Exóticas (mala fe)
    (EX, "Comprar ɴᴠᴅᴀ ya."),
    (EX, "Comprar 🇳🇻🇩🇦 ya."),
    (EX, "Comprar 🅽🆅🅳🅰 ya."),
    (EX, "Probabilidad de subida: 七成."),
    (EX, "Probabilidad de subida: 七十 %."),
    (EX, "Comprar Ｎｖｉｄｉａ ya."),
    (EX, "Probabilidad de subida: 𝟽𝟶 %."),
    (EX, "Comprar NVDΑ ya."),
]


def opp_por_tipo(res) -> dict[str, list[str]]:
    d: dict[str, list[str]] = defaultdict(list)
    for o in res["paquete"].get("paquete_para_bloque_B") or []:
        d[o["tipo_activo"]].append(o["opp_id"])
    return d


def preparar(raiz):
    M = C.preparar(raiz)
    base = C.ciclo(activos=TIPOS)
    perm = M["v6"].permitidos_r21(C.bloque(activos=TIPOS))
    return M, base, perm


def resolver(frase: str, tipo: str, opps: dict) -> str:
    if "{opp:OPP}" not in frase:
        return frase
    ids = opps.get(tipo) or [x for v in opps.values() for x in v]
    return frase.replace("{opp:OPP}", "{opp:" + ids[0] + "}")


def medir(v6, perm, marcas, frase: str):
    """(salida, reglas) de limpiar con una frase de control delante: así se ve que solo cae la que toca."""
    salida, reglas = v6.limpiar("El dólar sube. " + frase, perm, marcas)
    return salida, reglas


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    detalle = "--detalle" in sys.argv
    M, base, perm = preparar(args[0] if args else ".")
    v6, marcas, opps = M["v6"], base["marcas"], opp_por_tipo(base["res"])
    print(f"Ciclo de los doce tipos: {len(marcas)} marcas; tipos con opciones: {sorted(opps)}")

    fp = defaultdict(list)
    tot = Counter()
    for tipo, grupo, f in LEGITIMAS:
        f = resolver(f, tipo, opps)
        salida, reglas = medir(v6, perm, marcas, f)
        tot[grupo] += 1
        if reglas:
            fp[grupo].append((tipo, f, reglas))
    n_leg = sum(v for k, v in tot.items() if k != AM)
    n_fp = sum(len(v) for k, v in fp.items() if k != AM)
    print(f"\nLEGÍTIMAS: {n_fp}/{n_leg} quitadas (sin contar «ambigua»)")
    for g in (LL, SG, MK, PC, AM):
        print(f"  {g:17} {len(fp[g])}/{tot[g]}")
        for t, f, r in fp[g]:
            print(f"      [{t}] {r} {f}")
    por_tipo = Counter(t for t, g, _ in LEGITIMAS if g != AM)
    fp_tipo = Counter(t for g, v in fp.items() if g != AM for t, _, _ in v)
    print("  por tipo: " + ", ".join(f"{t} {fp_tipo[t]}/{por_tipo[t]}" for t in (*TIPOS, "*")))

    pasan = defaultdict(list)
    quitan = defaultdict(list)
    totp = Counter()
    for grupo, f in PROHIBIDAS:
        salida, reglas = medir(v6, perm, marcas, f)
        totp[grupo] += 1
        (quitan if reglas else pasan)[grupo].append((f, reglas, salida))
    print("\nPROHIBIDAS: pasan SIN DECLARARSE / se quitan y declaran")
    for g in (R13, R21, *LIM, EX):
        print(f"  {g:11} pasan {len(pasan[g])}/{totp[g]} · quitadas {len(quitan[g])}/{totp[g]} "
              f"{dict(Counter(r[0] for _, r, _ in quitan[g]))}")
        for f, _, s in pasan[g]:
            print(f"      PASA: {f!r} -> {s!r}")
        if detalle:
            for f, r, _ in quitan[g]:
                print(f"      quitada {r}: {f!r}")
    n_pro = totp[R13] + totp[R21]
    n_pasan = len(pasan[R13]) + len(pasan[R21])
    print(f"\nRESUMEN · FP {n_fp}/{n_leg} · FN (r13+r21, sin límites ni exóticas) {n_pasan}/{n_pro} · "
          f"límites que pasan {sum(len(pasan[g]) for g in LIM)}/{sum(totp[g] for g in LIM)} · "
          f"exóticas que pasan {len(pasan[EX])}/{totp[EX]}")
    return pasan, marcas


if __name__ == "__main__":
    main()
