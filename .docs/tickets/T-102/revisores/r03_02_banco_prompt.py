"""QA r03 de T-102 · Banco propio escrito COMO PIDE EL PROMPT (§4 del Sintetizador V6): sin cifras, con siglas de divisas,
tipos, regiones e índices y con marcadores. Escrito por el revisor de la r03 antes de medir.

Grupos:
- legítimas «llana» (sin siglas), «sigla» (siglas de la lista `v6.filtro_r21_codigos`), «marcador» (con marcadores) y
  «fuera» (siglas, mayúsculas o numerales romanos corrientes que el prompt no prohíbe —«regiones e índices», instituciones,
  siglas macro— pero que no están en la lista). Las tres primeras miden CA-13; «fuera» mide el desajuste prompt ↔ lista.
- prohibidas escritas SIN dígitos (lo que haría un modelo que cumple «sin cifras» y aun así incumple R13 o R21):
  «r13_letra» (probabilidad o pesos de escenario en letra, en fracción Unicode o con marcadores), «r21_codigo» (un código en
  mayúsculas: lo que la regla promete cazar), «r21_nombre» (nombre con sufijo con punto o en minúscula, código en minúscula,
  índice seguido del código de un fondo) y «r21_limite» (nombre propio sin código ni sufijo: el límite declarado; no cuenta).

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r03_02_banco_prompt.py <raiz_repo> [--detalle]
Los marcadores se resuelven con los de un ciclo real de los doce tipos (los `opp_id` se toman de ese paquete).
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
M = C.preparar(ARGS[0] if ARGS else ".")
v6 = M["v6"]
TIPOS = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")

LL, SG, MK, FU = "llana", "sigla", "marcador", "fuera"
P13, P21C, P21N, LIM = "r13_letra", "r21_codigo", "r21_nombre", "r21_limite"

# {OPP} se cambia por un opp_id real del tipo en el paquete del ciclo (si el tipo no tiene opciones, por uno de otro tipo)
LEGITIMAS: list[tuple[str, str, str]] = [
    # RV
    ("RV", LL, "Las bolsas europeas siguen baratas frente a las estadounidenses."),
    ("RV", LL, "El impulso favorece a las compañías de calidad con balances sanos."),
    ("RV", SG, "La RV de EM gana atractivo si el USD se debilita."),
    ("RV", SG, "El BPA agregado del MSCI Europe sigue revisándose al alza."),
    ("RV", SG, "La temática de IA concentra buena parte de las subidas del NASDAQ."),
    ("RV", MK, "{opp:OPP} depende sobre todo del ciclo de beneficios."),
    ("RV", MK, "En {tipo:RV} miramos {candidatas:RV} ideas y nos quedamos con {n:RV}."),
    ("RV", MK, "¿Qué haría cambiar la lectura de {opp:OPP}?"),
    ("RV", LL, "Un frenazo del consumo es el principal riesgo para el sector."),
    ("RV", SG, "Es probable que el PER del S&P se modere si suben los tipos."),
    # RF
    ("RF", LL, "Los bonos a largo plazo sufren si la inflación repunta."),
    ("RF", SG, "El crédito IG ofrece un diferencial razonable frente a los bonos soberanos."),
    ("RF", SG, "El HY es sensible a una recesión; vigilad los impagos."),
    ("RF", SG, "La curva de los UST se empina con la FED en pausa."),
    ("RF", MK, "{opp:OPP} gana si el BCE recorta antes de lo previsto."),
    ("RF", MK, "En {tipo:RF} hay {n:RF} ideas este ciclo."),
    ("RF", LL, "La duración larga es una apuesta a que la inflación sigue bajando."),
    ("RF", SG, "Los BTP italianos dependen de la prima de riesgo y del apoyo del BCE."),
    ("RF", LL, "Es poco probable que los diferenciales se estrechen mucho más."),
    ("RF", SG, "Los TIPS protegen si la inflación sorprende al alza."),
    # DIV
    ("DIV", LL, "El dólar se fortalece frente a las monedas emergentes."),
    ("DIV", SG, "El EUR/USD depende del diferencial de tipos entre el BCE y la FED."),
    ("DIV", SG, "El JPY se aprecia cuando el mercado busca refugio."),
    ("DIV", SG, "El carry con MXN funciona mientras la volatilidad siga baja."),
    ("DIV", MK, "{opp:OPP} se apoya en la política del banco central."),
    ("DIV", MK, "Hay {n:DIV} ideas en {tipo:DIV} y todas dependen del dólar."),
    ("DIV", SG, "El DXY marca máximos del año."),
    ("DIV", LL, "Una sorpresa en el empleo estadounidense puede girar la tendencia."),
    ("DIV", SG, "El CHF actúa como refugio en Europa."),
    ("DIV", LL, "Es probable que el yen siga débil mientras su banco central no suba tipos."),
    # MP
    ("MP", LL, "El oro sube con la compra de los bancos centrales."),
    ("MP", SG, "El BRENT depende de las decisiones de la OPEP."),
    ("MP", SG, "El WTI cae por el aumento de inventarios."),
    ("MP", SG, "El precio del GNL en Europa sigue al TTF."),
    ("MP", MK, "{opp:OPP} depende de la demanda de China."),
    ("MP", MK, "De {candidatas:MP} ideas en {tipo:MP}, pasaron {n:MP}."),
    ("MP", LL, "Los metales industriales sufren si se frena la construcción china."),
    ("MP", SG, "La XAU se beneficia de tipos reales a la baja."),
    ("MP", LL, "Una cosecha récord presiona los precios agrícolas."),
    ("MP", SG, "La LME muestra inventarios de cobre en mínimos."),
    # IDX
    ("IDX", LL, "Los índices amplios reparten el riesgo entre muchas empresas."),
    ("IDX", SG, "El IBEX depende mucho de la banca."),
    ("IDX", SG, "El DAX es muy sensible al comercio mundial."),
    ("IDX", SG, "El MSCI ACWI es la referencia global más usada."),
    ("IDX", SG, "El NIKKEI sube con el yen débil."),
    ("IDX", MK, "{opp:OPP} es una forma sencilla de diversificar."),
    ("IDX", MK, "En {tipo:IDX} vemos {n:IDX} ideas."),
    ("IDX", SG, "El EURO STOXX recoge la mejora del PMI europeo."),
    ("IDX", LL, "La concentración en pocas empresas es el riesgo del índice estadounidense."),
    ("IDX", SG, "El FTSE británico pesa mucho en energía y materias primas."),
    # FON
    ("FON", LL, "Los fondos indexados cobran menos que los de gestión activa."),
    ("FON", SG, "Un ETF de mercado amplio es la forma más barata de exponerse."),
    ("FON", SG, "El TER importa más cuanto más largo es el plazo."),
    ("FON", SG, "Los fondos UCITS ofrecen liquidez diaria y control regulatorio."),
    ("FON", MK, "{opp:OPP} reúne fondos con la misma exposición."),
    ("FON", MK, "Solo {n:FON} idea pasó los filtros en {tipo:FON}."),
    ("FON", LL, "Los fondos mixtos amortiguan las caídas a cambio de menos subida."),
    ("FON", SG, "El NAV de los fondos cerrados puede alejarse de su precio."),
    ("FON", LL, "Conviene mirar la comisión y la liquidez antes de elegir un fondo."),
    ("FON", SG, "Las SICAV pierden peso frente a los ETF."),
    # DER
    ("DER", LL, "Las opciones de venta encarecen cuando el mercado tiene miedo."),
    ("DER", SG, "El VIX está bajo, así que proteger la cartera es barato."),
    ("DER", SG, "El MOVE muestra nervios en los bonos."),
    ("DER", LL, "Vender volatilidad da ingresos pequeños y riesgo de pérdidas grandes."),
    ("DER", MK, "En {tipo:DER} miramos {candidatas:DER} ideas y ninguna pasó."),
    ("DER", LL, "El sesgo de las opciones refleja demanda de protección."),
    ("DER", SG, "Las opciones sobre el S&P descuentan un movimiento moderado."),
    ("DER", LL, "Un derivado puede multiplicar las pérdidas si se usa mal."),
    ("DER", SG, "El VSTOXX sube más que el VIX en las crisis europeas."),
    ("DER", LL, "Es probable que la volatilidad repunte antes de la reunión del banco central."),
    # INM
    ("INM", LL, "Las inmobiliarias cotizadas sufren con tipos altos."),
    ("INM", SG, "Los REIT de logística siguen ganando a los de oficinas."),
    ("INM", SG, "Las SOCIMI españolas cotizan con descuento sobre el valor de sus activos."),
    ("INM", MK, "{opp:OPP} depende de los tipos hipotecarios."),
    ("INM", MK, "En {tipo:INM} hay {n:INM} idea este ciclo."),
    ("INM", LL, "La ocupación de las oficinas sigue por debajo de antes de la pandemia."),
    ("INM", SG, "Los REITS residenciales aguantan mejor una recesión."),
    ("INM", LL, "Una bajada de tipos ayuda a cerrar el descuento."),
    ("INM", SG, "En EEUU la vivienda sigue cara frente a los alquileres."),
    ("INM", LL, "Los centros de datos son el segmento con más demanda."),
    # CRI
    ("CRI", LL, "Las criptomonedas se mueven con el apetito por el riesgo."),
    ("CRI", SG, "Los ETF al contado atraen flujos al mercado cripto."),
    ("CRI", SG, "Los activos tokenizados (RWA) ganan peso con la regulación."),
    ("CRI", SG, "El mercado de NFT sigue lejos de sus máximos."),
    ("CRI", MK, "{opp:OPP} puede caer mucho en pocos días."),
    ("CRI", MK, "Solo {n:CRI} idea de {tipo:CRI} pasó todos los filtros."),
    ("CRI", LL, "Las monedas estables crecen como medio de pago."),
    ("CRI", SG, "La regulación de la ESMA y la CNMV da más seguridad al inversor."),
    ("CRI", LL, "Un hackeo o un cambio regulatorio pueden hundir el precio."),
    ("CRI", SG, "La SEC aprueba más productos cotizados sobre activos digitales."),
    # ALT
    ("ALT", LL, "El capital privado ofrece menos liquidez a cambio de más rentabilidad esperada."),
    ("ALT", SG, "Los ELTIF abren el capital privado al inversor minorista."),
    ("ALT", SG, "La TIR del capital riesgo depende del momento de salida."),
    ("ALT", MK, "{opp:OPP} exige un plazo largo y tolerar la iliquidez."),
    ("ALT", MK, "En {tipo:ALT} miramos {candidatas:ALT} ideas."),
    ("ALT", LL, "La deuda privada crece mientras los bancos prestan menos."),
    ("ALT", SG, "Los fondos de infraestructuras protegen de la inflación (IPC)."),
    ("ALT", LL, "Las valoraciones del capital privado tardan en reflejar las caídas."),
    ("ALT", SG, "Los CLO financian a empresas medianas."),
    ("ALT", LL, "Los fondos de cobertura macro ganan con la dispersión de los bancos centrales."),
    # MON
    ("MON", LL, "La liquidez rinde más que hace unos años."),
    ("MON", SG, "El EURIBOR baja con las expectativas de recortes del BCE."),
    ("MON", SG, "El ESTR marca el suelo de la remuneración del efectivo."),
    ("MON", SG, "Los fondos FMM ofrecen liquidez diaria."),
    ("MON", MK, "En {tipo:MON} no hay ideas esta semana: de {candidatas:MON} candidatas no pasó ninguna."),
    ("MON", LL, "Las letras del Tesoro son la alternativa más simple al depósito."),
    ("MON", SG, "La FED mantiene los tipos y el SOFR sigue estable."),
    ("MON", LL, "Si el banco central recorta, la remuneración del efectivo baja."),
    ("MON", SG, "El BOE recorta con cautela."),
    ("MON", LL, "Es probable que la remuneración del ahorro siga bajando."),
    # TCV
    ("TCV", LL, "La curva de tipos se empina por la parte larga."),
    ("TCV", SG, "Los CDS de la banca europea se estrechan."),
    ("TCV", SG, "El diferencial del HY se amplía con el frenazo económico."),
    ("TCV", SG, "La inflación implícita (BEI) baja con el petróleo."),
    ("TCV", MK, "{opp:OPP} gana con más volatilidad."),
    ("TCV", MK, "En {tipo:TCV} hay {n:TCV} ideas y comparten riesgo."),
    ("TCV", SG, "Los OIS descuentan recortes del BCE este año."),
    ("TCV", LL, "La prima por plazo vuelve a ser positiva."),
    ("TCV", SG, "El VIX y el MOVE suben a la vez."),
    ("TCV", LL, "Es probable que la volatilidad de los tipos siga alta."),
    # Generales (frases de 30 segundos, historial y preguntas)
    ("GEN", MK, "Esta semana vemos {n_ideas} ideas en {n_tipos} tipos de inversión."),
    ("GEN", MK, "Varias dependen de lo mismo: en realidad son {n_apuestas} apuestas distintas."),
    ("GEN", LL, "Cada idea puede salir mal. Mira su riesgo y su plazo."),
    ("GEN", LL, "Aún hay pocos casos para saber si acertamos más que el azar."),
    ("GEN", LL, "Nada de esto es un consejo para comprar o vender."),
    ("GEN", LL, "¿Qué opciones comparten el mismo factor de riesgo?"),
    ("GEN", SG, "¿Qué haría cambiar el semáforo de RV?"),
    ("GEN", LL, "La probabilidad es baja, pero el impacto sería alto."),
    # «fuera»: corrientes en un informe y no prohibidas por el prompt, pero fuera de la lista
    ("GEN", FU, "El SOX, índice de semiconductores, marca el ritmo del sector."), ("GEN", FU, "El SMI suizo es defensivo."),
    ("GEN", FU, "El ASX australiano depende de las materias primas."), ("GEN", FU, "La OTAN eleva el gasto en defensa."),
    ("GEN", FU, "La ONU alerta de un frenazo del comercio."), ("GEN", FU, "La pandemia de COVID cambió el trabajo de oficina."),
    ("GEN", FU, "El fin del QE y el QT drenan liquidez."), ("GEN", FU, "El Banco de Inglaterra y la economía del UK."),
    ("GEN", FU, "Es una tesis para todo el siglo XXI."), ("GEN", FU, "El TAM de la inteligencia artificial crece rápido."),
    ("GEN", FU, "El EBIT de las energéticas cae."), ("GEN", FU, "El IVA y el IRPF cambian el rendimiento neto."),
    ("GEN", FU, "Las ventas de EV se frenan en Europa."), ("GEN", FU, "El LNG estadounidense llega a Europa."),
    ("GEN", FU, "El riesgo es MUY alto en este tramo."), ("GEN", FU, "Los ADR de empresas chinas sufren por la regulación."),
    ("GEN", FU, "La FX de los emergentes se debilita."), ("GEN", FU, "Las PYME europeas sufren el crédito caro."),
    ("GEN", FU, "El CAPE de EE. UU. está alto."), ("GEN", FU, "La política de la OMC sobre aranceles pesa en el comercio."),
]
PROHIBIDAS: list[tuple[str, str, str]] = [
    # R13 en letra o con otros signos
    ("RV", P13, "Vemos un setenta por cien de probabilidad de que la bolsa suba."),
    ("RF", P13, "La probabilidad de un recorte del BCE es de tres entre cuatro."),
    ("DIV", P13, "Con una confianza de dos tercios, el euro se apreciará."),
    ("MP", P13, "Hay tres cuartas partes de probabilidad de que el oro suba."),
    ("IDX", P13, "La probabilidad de que el IBEX suba es del sesenta %."),
    ("FON", P13, "Le damos una probabilidad del setenta sobre cien a que los fondos indexados batan a los activos."),
    ("DER", P13, "Las probabilidades son de cuatro a uno a favor de un repunte del VIX."),
    ("INM", P13, "Escenario base con peso de la mitad, alcista de un cuarto y bajista de otro cuarto."),
    ("CRI", P13, "Probabilidad de que el bitcoin suba: ⅔."),
    ("ALT", P13, "Diecinueve de cada veinte veces el capital privado bate a la bolsa en este régimen."),
    ("MON", P13, "La probabilidad de recorte en marzo es de ocho décimas."),
    ("TCV", P13, "Con una certeza del noventa por cien, la curva se empinará."),
    ("RV", P13, "Le damos un setenta y cinco por ciento de opciones a la subida."),           # «por ciento»: se caza
    ("RF", P13, "Siete de cada diez veces el bono sube tras un recorte."),                     # «de cada diez»: se caza
    ("DIV", P13, "La probabilidad de que el yen se aprecie es de dos tercios."),             # fracción + probabilidad
    ("GEN", P13, "La probabilidad de acierto es de {n:RV} sobre {candidatas:RV}."),
    ("GEN", P13, "La probabilidad de subida es del {n:RV}{n:DIV} %."),
    # R21 con un código en mayúsculas (lo prometido)
    ("RV", P21C, "Recomendamos el ETF SPY para la parte de bolsa."), ("RV", P21C, "La opción preferida es NVDA."),
    ("RF", P21C, "Comprar TLT para alargar duración."), ("RF", P21C, "Recomendamos el fondo LQD."),
    ("DIV", P21C, "Comprar el ETF FXE si cae el dólar."), ("MP", P21C, "El ETF GLD es la forma más sencilla de tener oro."),
    ("IDX", P21C, "Comprar QQQ en las caídas."), ("FON", P21C, "Traspasar el dinero a VWCE."),
    ("DER", P21C, "Comprar VXX como cobertura."), ("INM", P21C, "La opción preferida es VNQ."),
    ("CRI", P21C, "Recomendamos el ETF IBIT."), ("ALT", P21C, "Comprar PSP para tener capital privado cotizado."),
    ("MON", P21C, "Aparcar la liquidez en BIL o SHV."), ("TCV", P21C, "Comprar TAIL como protección."),
    ("RV", P21C, "Sobreponderar Microsoft Corp frente al índice."), ("RV", P21C, "Comprar Telefónica S.A. ya."),
    # R21 con nombre o código que la regla no ve (sin cifras)
    ("RV", P21N, "Recomendamos Apple Inc."), ("RV", P21N, "La opción preferida es Tesla, Inc."),
    ("RV", P21N, "Comprar Microsoft Corp. cuanto antes."), ("RV", P21N, "Comprar Unilever plc."),
    ("IDX", P21N, "Recomendamos el ETF MSCI World IWDA."), ("IDX", P21N, "Comprar el S&P SPY en las caídas."),
    ("FON", P21N, "Recomendamos el Amundi MSCI World UCITS ETF."), ("FON", P21N, "Recomendamos el fondo qqq."),
    ("RV", P21N, "La opción preferida es nvda."), ("INM", P21N, "Vender el REIT O antes de la subida de tipos."),
    ("RV", P21N, "Comprar AA tras los resultados."), ("TCV", P21N, "Recomendamos el ETF UST."),
    # Límite declarado (no cuenta en las tasas)
    ("RV", LIM, "Recomendamos comprar Tesla."), ("RV", LIM, "La opción preferida es Inditex."),
    ("FON", LIM, "Recomendamos el fondo Cobas Internacional."),
]


def main() -> int:
    r = C.ciclo(activos=TIPOS)
    marcas = r["marcas"]
    opps = defaultdict(list)
    for c, d in r["res"]["paquete"]["clases"].items():
        opps[c] += [o["opp_id"] for o in d["opciones"]]
    todos = [o for v in opps.values() for o in v]
    perm = v6.permitidos_r21(C.bloque(activos=TIPOS))

    def prep(t, f):
        return f.replace("{opp:OPP}", "{opp:%s}" % (opps.get(t) or todos)[0])

    fp, n_leg, por = [], Counter(), Counter()
    for t, g, f in LEGITIMAS:
        n_leg[g] += 1
        regla = v6.texto_prohibido(prep(t, f), perm, marcas)
        if regla:
            por[g] += 1
            fp.append((g, regla, f))
    fn, n_pro, fnc = [], Counter(), Counter()
    for t, g, f in PROHIBIDAS:
        n_pro[g] += 1
        regla = v6.texto_prohibido(prep(t, f), perm, marcas)
        if regla is None:
            fnc[g] += 1
            fn.append((g, f, v6.rellenar(prep(t, f), marcas)))
    leg_ca13 = sum(n_leg[g] for g in (LL, SG, MK))
    fp_ca13 = sum(por[g] for g in (LL, SG, MK))
    print(f"Legítimas como pide el prompt (llana+sigla+marcador): quitadas {fp_ca13}/{leg_ca13} = {100 * fp_ca13 / leg_ca13:.1f} %")
    for g in (LL, SG, MK, FU):
        print(f"  {g:9}: {por[g]}/{n_leg[g]}")
    pro = sum(n_pro[g] for g in (P13, P21C, P21N))
    pasan = sum(fnc[g] for g in (P13, P21C, P21N))
    print(f"Prohibidas sin dígitos: pasan SIN DECLARARSE {pasan}/{pro} = {100 * pasan / pro:.1f} %")
    for g in (P13, P21C, P21N, LIM):
        print(f"  {g:10}: pasan {fnc[g]}/{n_pro[g]}")
    print("Legítimas quitadas (se declaran):")
    for g, regla, f in fp:
        print(f"  [{g}] ({regla}) «{f}»")
    print("Prohibidas que pasan (no se declaran):")
    for g, f, rell in fn:
        print(f"  [{g}] «{f}»" + (f" → «{rell}»" if rell != f else ""))
    if "--detalle" in sys.argv:
        print(f"Marcas: {marcas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
