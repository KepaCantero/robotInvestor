"""QA r06 de T-102 · Banco ciego del revisor (CA-12 y CA-13 con los umbrales [PROPUESTO] de INC-T102-01).

Escrito por el revisor de la r06 antes de leer los bancos de las pruebas y de las rondas anteriores; frases nuevas.

Grupos:
- PROHIBIDAS_DATO: llevan un dato (dígitos, un marcador de cuenta o desconocido, o un código de un instrumento). Tolerancia cero.
- PROHIBIDAS_LETRA: cifras en letra, fracciones y probabilidades en palabras, sin ningún dato.
- LEGITIMAS: escritas como pide el prompt (§4): sin cifras, tampoco en letra, sin marcadores de cuenta; con siglas de la lista
  y con marcadores {opp:…} y {tipo:…} del paquete.
- LEGITIMAS_LETRA: legítimas con un número en letra o un giro numérico (coste declarado de la regla estricta; se miden aparte).
- SIGLAS_FUERA: legítimas con siglas institucionales que no están en `filtro_r21_codigos` (informativo).
- LIMITES: prohibidas que caen en los límites declarados de INC-T102-01 (informativo: se espera que pasen).

Umbrales (INC-T102-01, [PROPUESTO]): pasan ≤ 5 % de las prohibidas y ninguna con dato; se quitan ≤ 10 % de las legítimas.

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r06_01_banco_ciego.py [RAIZ]   (por defecto, la raíz del repo)
Devuelve 0 si se cumplen los tres umbrales y 1 si no.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

# «OPP1», «OPP2» y «OPP3» se cambian por {opp:<id>} de opciones reales del paquete; «TIPO1» y «TIPO2» por {tipo:<clase>}.

PROHIBIDAS_DATO = [
    "La renta variable estadounidense pesa un 35 % de la selección.",
    "El euro podría caer hasta 1,05 frente al dólar.",
    "Vemos una probabilidad del 60% de recorte de tipos.",
    "Desde 2022 la inflación no ha dejado de bajar.",
    "El oro cotiza cerca de los 2.400 dólares.",
    "Hay {n_ideas} ideas esta semana y casi todas dependen del dólar.",
    "De las {candidatas:RV} candidatas solo pasaron unas pocas.",
    "Sumando {n:DIV} apuestas, el riesgo se concentra.",
    "{n_tipos} tipos de activo comparten el mismo factor.",
    "Nos gusta especialmente NVDA por su exposición a la IA.",
    "La idea se expresa mejor con el fondo IE00B5BMR087.",
    "Conviene vigilar AAPL y MSFT, que dominan el índice.",
    "Una vía sencilla para esta idea es VWCE.",
    "Si el petróleo sube, XOM sería la más beneficiada.",
    "Preferimos SAN.MC frente al resto de bancos.",
    "Recomendamos sobreponderar TLT ante la bajada de tipos.",
    "Esta semana entraríamos en QQQ.",
    "La subida de la bolsa fue del 12 por ciento.",
    "Los bonos a 10 años ofrecen más rentabilidad.",
    "El índice podría ganar un ５ % más.",
    "La cartera reparte el riesgo en ٣ bloques.",
    "El escenario base da 3/4 de opciones al alza.",
    "Comprar BTC ahora tiene sentido por el ciclo.",
    "ETH lidera el rebote de los activos digitales.",
    "La mejor opción para el sector es AMZN.",
    "Proponemos tomar posiciones en GLD como cobertura.",
    "El ISIN ES0113900J37 encaja con la tesis.",
    "Una cesta con META, GOOGL y NFLX resume la idea.",
    "La caída del S&P 500 abriría una oportunidad.",
    "Con un objetivo de 150 puntos básicos, la idea es atractiva.",
    "El tipo oficial subiría hasta el 4,25 %.",
    "Prob.: 70 %.",
    "El valor TSLA concentra demasiado riesgo.",
    "{opp:OPP-2026-9999} es la idea más sólida.",
    "La idea {opp:OPP1X depende del dólar.",
    "Invertir en BRK.B da exposición diversificada.",
    "Se aconseja vender INTC antes de resultados.",
    "Un 20% de caída ya está descontado.",
    "El 1T del año fue flojo para el crédito.",
    "Recomendamos ASML, líder en litografía.",
    "La pata más clara del clúster es SMH.",
    "El dólar se apoya en el diferencial de tipos: compraríamos UUP.",
    "La pieza clave del clúster de crédito es HYG.",
    "{opp:OPP1} junto con {n_apuestas} apuestas más depende del petróleo.",
    "El bono del Tesoro a 2a rinde más que el largo.",
]

PROHIBIDAS_LETRA = [
    "Hay tres ideas que dependen del mismo factor.",
    "Dos de las apuestas son en realidad la misma.",
    "La probabilidad de que el BCE baje tipos es alta, cercana a tres cuartos.",
    "Calculamos un setenta por ciento de opciones de subida.",
    "Una de cada tres ideas está ligada al petróleo.",
    "La mitad de la selección depende del dólar.",
    "El riesgo es el doble que la semana pasada.",
    "Un cuarto de la cartera está en TIPO1.",
    "Esperamos un recorte de medio punto.",
    "La bolsa europea ha subido un diez por ciento.",
    "Cinco tipos de activo quedan sin opciones.",
    "Dos mil veintisiete es el horizonte de la tesis.",
    "Las cuatro ideas de renta fija se mueven juntas.",
    "Esperamos cien puntos básicos de recortes.",
    "La inflación ronda el dos y medio.",
    "Nueve de cada diez analistas esperan subidas.",
    "Mil millones de dólares han salido de los fondos emergentes.",
    "Una docena de bancos centrales ya han bajado tipos.",
    "El peso de la renta fija es el triple que el de la variable.",
    "Veinte años de datos respaldan la idea.",
    "Las opciones de éxito son de cuatro sobre cinco.",
    "Hay un ochenta por cien de posibilidades de recesión.",
    "Vemos el euro en uno con diez.",
    "Cuarenta puntos básicos separan los bonos de ambos países.",
    "El primero de los clústeres concentra seis ideas.",
    "Once ideas pasaron el filtro.",
    "Las ideas de crédito suman un tercio del riesgo.",
    "La posibilidad de impago es de una entre veinte.",
    "Siete ideas apuntan en la misma dirección.",
    "La tasa de paro bajó una décima.",
]

LEGITIMAS = [
    "El dólar fuerte es el factor común de la semana.",
    "OPP1 depende sobre todo de los tipos de la FED.",
    "Si el BCE baja tipos antes de lo previsto, la idea pierde fuerza.",
    "La renta fija emergente sufre cuando sube el USD.",
    "El petróleo y el gas se mueven por la misma razón: la oferta de la OPEP.",
    "La inflación (subida general de precios) sigue bajando poco a poco.",
    "El historial todavía no demuestra ventaja frente al azar.",
    "Aún no hay suficientes ideas cerradas para saber si el sistema acierta.",
    "¿Conviene limitar la exposición conjunta al dólar?",
    "¿Qué parte del riesgo viene de Oriente Medio?",
    "La demanda de acero en Asia se enfría.",
    "El estrés en el crédito de alto rendimiento (HY) es bajo.",
    "Todos los bancos centrales miran el empleo.",
    "La eficiencia del mercado hace difícil batir al índice.",
    "Una subida del petróleo perjudicaría a OPP2.",
    "Un euro más débil ayuda a los exportadores europeos.",
    "A medio plazo, la tesis depende del crecimiento en EEUU.",
    "En el cuarto trimestre suele haber más volatilidad.",
    "El índice MSCI de emergentes recoge esta apuesta.",
    "La duración (sensibilidad del precio de un bono a los tipos) es alta en esta idea.",
    "El riesgo principal es un frenazo de la economía china.",
    "Si el VIX se dispara, el Broker debería revisar el riesgo.",
    "TIPO1 y TIPO2 comparten la apuesta por tipos más bajos.",
    "Ambas ideas son, en el fondo, la misma apuesta.",
    "La lectura del conjunto: demasiada dependencia de la FED.",
    "Una sorpresa de inflación en EEUU tumbaría la tesis.",
    "El PIB de la zona euro crece poco.",
    "El IPC subyacente (sin energía ni alimentos) se resiste a bajar.",
    "Los emergentes (EM) dependen del apetito por el riesgo.",
    "La familia de ideas de materias primas es pequeña.",
    "Las expectativas de recortes son similares a las del mes pasado.",
    "La conciencia del riesgo político está creciendo.",
    "El crédito con grado de inversión (IG) aguanta bien.",
    "El oro sirve de refugio cuando hay miedo.",
    "Una guerra comercial golpearía a las exportadoras.",
    "El yen se fortalece cuando los inversores huyen del riesgo.",
    "La curva de tipos (diferencia entre tipos largos y cortos) se ha empinado.",
    "No hay base para prometer ganancias.",
    "La idea OPP1 es sensible al precio del petróleo.",
    "Si el dólar se debilita, OPP3 gana atractivo.",
    "El mercado ya descuenta varios recortes.",
    "¿Debería el Broker cubrir el riesgo de divisa?",
    "Una parte importante del riesgo viene del mismo sitio.",
    "El Nasdaq depende mucho de las grandes tecnológicas.",
    "El sector inmobiliario cotizado (REIT) sufre con tipos altos.",
    "La primera señal de alarma sería un repunte del paro.",
    "En segundo plano queda la política fiscal.",
    "La volatilidad (cuánto se mueve el precio) está en mínimos.",
    "Los datos de empleo en EEUU marcan el tono de la semana.",
    "El índice IBEX depende mucho de la banca.",
    "La tesis se rompe si el BCE sube tipos.",
    "Esta semana domina un único factor: el dólar.",
    "El S&P y el Nasdaq se mueven juntos.",
    "Los bonos ligados a la inflación (TIPS) protegen si los precios suben.",
    "La economía japonesa sale poco a poco de la deflación.",
    "Varias ideas de TIPO1 dependen de la inteligencia artificial.",
    "Los precios del gas en Europa siguen altos.",
    "El riesgo de crédito de las empresas medianas sube.",
    "Los mercados emergentes de LATAM dependen de las materias primas.",
    "La política monetaria sigue siendo restrictiva.",
    "La sincronía entre bolsa y bonos complica la diversificación.",
    "El margen de error del modelo es amplio.",
    "Hay pocas ideas cerradas; es pronto para sacar conclusiones.",
    "El sistema todavía no ha demostrado que acierte más que el azar.",
    "La tesis de OPP1 pierde fuerza si el yen se aprecia.",
    "Un escenario de recesión golpearía a todas las ideas a la vez.",
    "En cambio, el oro gana en ese escenario.",
    "El precio del cobre anticipa el ciclo industrial.",
    "¿Hay que reducir la dependencia del petróleo en la selección?",
    "El euro vuelve a acercarse a la paridad con el dólar.",
    "Diversificar (repartir el dinero entre activos distintos) reduce el riesgo, pero no lo elimina.",
    "El Tesoro de EE. UU. emite más deuda y eso presiona los tipos largos.",
]

LEGITIMAS_LETRA = [
    "Los dos bancos centrales se mueven en direcciones opuestas.",
    "Las tres grandes economías frenan a la vez.",
    "Medio mundo mira a la Reserva Federal.",
    "Es un arma de doble filo para los exportadores.",
    "Son las dos caras de la misma moneda.",
    "Uno de los riesgos es la política comercial.",
    "Cien días de gobierno marcan el tono.",
    "Las cuatro grandes tecnológicas pesan mucho en el índice.",
    "Hay una sola idea de renta fija esta semana.",
    "La economía crece a dos velocidades.",
    "El G7 discute aranceles esta semana.",
]

SIGLAS_FUERA = [
    "Según la AIE, la demanda de petróleo se frena.",
    "El INE publica el dato de paro esta semana.",
    "La EPA dirá si el empleo aguanta.",
    "La TAE de los depósitos sigue bajando.",
    "El BID financia proyectos en Latinoamérica.",
]

LIMITES = [
    "Comprar acciones de Tesla tiene sentido.",          # nombre propio sin código ni sufijo
    "Conviene comprar el valor nvda.",                   # minúscula tras «el valor» (T-109)
    "Las VII ideas comparten factor.",                   # romanos como cantidad (T-109)
    "Conviene comprar COP antes del verano.",            # código que coincide con una sigla de la lista
]


def _sust(s: str, ids: list[str], tipos: list[str]) -> str:
    s = s.replace("OPP1X", ids[0])   # marcador mal formado: sin llave de cierre
    for k, i in enumerate(ids[:3], 1):
        s = s.replace(f"OPP{k}", "{opp:" + i + "}")
    for k, t in enumerate(tipos[:2], 1):
        s = s.replace(f"TIPO{k}", "{tipo:" + t + "}")
    return s


def medir(raiz: str | Path) -> dict:
    C.preparar(raiz)
    v6 = C.M["v6"]
    r = C.ciclo(activos=("DIV", "RV", "RF"))
    assert not r.get("error"), r.get("error")
    marcas = r["marcas"]
    ids = [k.split(":", 1)[1] for k in marcas if k.startswith("opp:")]
    tipos = [k.split(":", 1)[1] for k in marcas if k.startswith("tipo:")]
    assert len(ids) >= 3 and len(tipos) >= 2, marcas
    perm = v6.permitidos_r21(C.bloque(activos=("DIV", "RV", "RF")))

    def evalua(grupo):
        out = []
        for s in grupo:
            f = _sust(s, ids, tipos)
            salida, reglas = v6.limpiar(f, perm, marcas)
            out.append((f, reglas, salida))
        return out
    return {g: evalua(globals()[g]) for g in ("PROHIBIDAS_DATO", "PROHIBIDAS_LETRA", "LEGITIMAS", "LEGITIMAS_LETRA",
                                              "SIGLAS_FUERA", "LIMITES")}


def main() -> int:
    raiz = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
    res = medir(raiz)
    pd_, pl, lg = res["PROHIBIDAS_DATO"], res["PROHIBIDAS_LETRA"], res["LEGITIMAS"]
    pasan_dato = [f for f, r, _ in pd_ if not r]
    pasan_letra = [f for f, r, _ in pl if not r]
    n_proh = len(pd_) + len(pl)
    tasa_paso = (len(pasan_dato) + len(pasan_letra)) / n_proh
    quitadas = [(f, r) for f, r, _ in lg if r]
    tasa_fp = len(quitadas) / len(lg)
    print(f"Prohibidas: {n_proh} ({len(pd_)} con dato, {len(pl)} en letra)")
    print(f"  pasan con dato: {len(pasan_dato)}/{len(pd_)}")
    for f in pasan_dato:
        print(f"    PASA (dato): {f}")
    print(f"  pasan en letra: {len(pasan_letra)}/{len(pl)}")
    for f in pasan_letra:
        print(f"    PASA (letra): {f}")
    print(f"  tasa de paso: {tasa_paso:.1%} (umbral ≤ 5 %)")
    print(f"Legítimas: {len(lg)}; quitadas {len(quitadas)} ({tasa_fp:.1%}; umbral ≤ 10 %)")
    for f, r in quitadas:
        print(f"    QUITADA {r}: {f}")
    for g in ("LEGITIMAS_LETRA", "SIGLAS_FUERA", "LIMITES"):
        q = [(f, r) for f, r, _ in res[g] if r]
        print(f"{g}: quitadas {len(q)}/{len(res[g])}")
        for f, r, _ in res[g]:
            print(f"    {'QUITADA ' + str(r) if r else 'pasa'}: {f}")
    # comprobación de relleno: las legítimas con marcador salen con el nombre llano, sin llaves
    llaves = [s for f, r, s in lg if not r and "{" in s]
    print(f"Legítimas conservadas con llaves sin rellenar: {len(llaves)}")
    ok = not pasan_dato and tasa_paso <= 0.05 and tasa_fp <= 0.10 and not llaves
    print("UMBRALES:", "CUMPLEN" if ok else "NO CUMPLEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
