"""QA r05 de T-102 (revisor nuevo, commit `bf7235b`) · Banco propio, sin frases de las rondas anteriores.

Escrito por este revisor sin reutilizar las frases de `r01_*` a `r04_*` ni las de `tests/test_t102_filtro.py`. Mide la regla
estricta del Sintetizador (CIFRA, R21, MARCADOR) frase a frase con `frase_prohibida`, los permitidos de un Bloque V6 real
(`permitidos_r21`) y las marcas de un paquete real (las de los tipos sin opciones se completan con valores de prueba).

Grupos:
- Legítimas que deben conservarse (CA-13: escritas como pide §4 del prompt, sin cifras ni códigos fuera de la lista):
  «llana», «sigla» (siglas de la lista), «marcador» (marcadores bien usados), «giro» (medio, mitad y ordinales que no son
  cantidades: «a corto y medio plazo», «un medio de cobertura», «en mitad de», «el doble mandato»), «generico» (vehículos o
  palabras de vehículo en su sentido corriente: «la acción de los bancos centrales», «el bono de referencia», «Un ETF es un fondo…», «Los ETF suben…»).
- «coste»: frases que un analista escribiría con un número en letra que no es una probabilidad ni un dato del paquete («los
  dos bancos centrales», «cupón cero»). El prompt las prohíbe; se cuentan aparte, para medir el coste de la regla estricta.
- Prohibidas que deben quitarse: «r13_letra» (cantidades y probabilidades con palabras numéricas que no están en la lista:
  billón, milésima, centésima, -avo, docena, centenar, «fifty-fifty»), «r13_marcador» (números compuestos con marcadores:
  decimales, cuotas «a uno», «por cada», listas), «r21_sufijo» (sufijos que la regla promete y no ve: nombre de una palabra
  en -er/-ar/-ir al empezar, «Plc», «Sicav», «Socimi», «KGaA», «Oyj», minúsculas sin punto), «r21_fondo» (vehículos ETC/ETP).
- Aparte (se informan): «limite» (lo declarado: nombre propio, minúscula, vehículo en español), «exotica» (mala fe: letras
  latinas con diacrítico o gancho, letras en recuadro negativo, letras separadas por espacios duros o en blanco Braille,
  romanos).

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r05_01_banco.py <raiz_repo> [--detalle | --lista]
Sale con 1 si alguna legítima de los grupos que cuentan se quita o alguna prohibida pasa. No escribe en el repositorio.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

TIPOS = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
LEGITIMAS = ("llana", "sigla", "marcador", "giro", "generico")
PROHIBIDAS = ("r13_letra", "r13_marcador", "r21_sufijo", "r21_fondo")
APARTE = ("coste", "limite", "exotica")

BANCO = [
    # ---- legítimas llanas
    ("llana", "El crédito corporativo aguanta mejor de lo que esperábamos."),
    ("llana", "Los bancos centrales siguen pendientes de los salarios."),
    ("llana", "La curva de tipos vuelve a tener pendiente positiva."),
    ("llana", "El petróleo depende ahora de la oferta más que de la demanda."),
    ("llana", "Si la inflación repunta, esta idea sufriría."),
    ("llana", "Las tensiones comerciales encarecen la cobertura de divisas."),
    ("llana", "El mercado inmobiliario cotizado respira con la bajada de tipos."),
    ("llana", "Nada de esto es una recomendación personal."),
    ("llana", "El oro funciona como refugio cuando el dólar se debilita."),
    ("llana", "La volatilidad está baja y eso suele durar poco."),
    ("llana", "Ninguna de las ideas depende solo del crecimiento chino."),
    ("llana", "Ambas ideas sufren si el dólar se dispara."),
    ("llana", "El historial todavía es corto para sacar conclusiones."),
    ("llana", "Conviene vigilar el empleo antes de la próxima reunión."),
    ("llana", "La renta fija gana atractivo frente a la liquidez."),
    ("llana", "El cobre anticipa una industria más fuerte."),
    ("llana", "Las criptomonedas siguen muy ligadas al apetito por el riesgo."),
    ("llana", "La prima de riesgo periférica se estrecha."),
    ("llana", "Este informe no tiene en cuenta los impuestos de cada inversor."),
    ("llana", "Las materias primas agrícolas dependen del clima."),
    # ---- legítimas con siglas de la lista
    ("sigla", "El BCE y la FED mantienen el tono prudente."),
    ("sigla", "El USD pierde fuerza frente al JPY."),
    ("sigla", "Los diferenciales HY se amplían más que los IG."),
    ("sigla", "El PMI manufacturero de la UE mejora."),
    ("sigla", "El VIX sigue en calma pese al ruido."),
    ("sigla", "Los ETF de RF corta captan flujos."),
    ("sigla", "La OPEP recorta la oferta y el WTI reacciona."),
    ("sigla", "El IPC subyacente frena en EEUU."),
    ("sigla", "Las SOCIMI se benefician de la caída del EURIBOR."),
    ("sigla", "Los mercados EM dependen del DXY."),
    ("sigla", "El índice MSCI de EM supera al de la OCDE."),
    ("sigla", "El ESG pierde tirón entre los grandes gestores."),
    # ---- legítimas con marcadores bien usados
    ("marcador", "Esta semana hay {n_ideas} ideas repartidas en {n_tipos} tipos de inversión."),
    ("marcador", "{opp:OPP-X} gana si el dólar se debilita."),
    ("marcador", "En {tipo:RV} elegimos {n:RV} de {candidatas:RV} candidatas."),
    ("marcador", "Las {n_ideas} ideas se resumen en {n_apuestas} apuestas independientes."),
    ("marcador", "{opp:OPP-X} y {opp:OPP-Y} dependen del mismo factor."),
    ("marcador", "En {tipo:DIV} hay {n:DIV} ideas; el resto no pasa el filtro."),
    ("marcador", "Analizamos {candidatas:MP} ideas de {tipo:MP}."),
    ("marcador", "Lo que podría salir mal con {opp:OPP-X} es un giro del BCE."),
    ("marcador", "{tipo:RF} aporta {n:RF} ideas, todas de crédito."),
    ("marcador", "La lectura de conjunto: {n_apuestas} apuestas reales detrás de {n_ideas} ideas."),
    # ---- legítimas con medio, mitad u ordinales que no son cantidades
    ("giro", "Vemos valor a corto y medio plazo en la renta fija."),
    ("giro", "En el corto y medio plazo manda la liquidez."),
    ("giro", "El oro sirve como un medio de cobertura frente a la inflación."),
    ("giro", "La renta fija es un medio para reducir el riesgo de la cartera."),
    ("giro", "El doble mandato de la Fed complica su decisión."),
    ("giro", "En mitad de la tormenta, el oro resiste."),
    ("giro", "El riesgo en Oriente Próximo y Medio sigue alto."),
    ("giro", "El IPC sube por un quinto mes consecutivo."),
    ("giro", "La industria encadena un sexto mes de contracción."),
    ("giro", "El cuarto trimestre suele ser bueno para la bolsa."),
    ("giro", "El tercer trimestre trajo más volatilidad."),
    ("giro", "La renta fija gana en la segunda mitad del año."),
    ("giro", "Las perspectivas a medio y largo plazo mejoran."),
    ("giro", "El precio medio del crudo baja."),
    ("giro", "La clase media sostiene el consumo."),
    ("giro", "Por segunda vez, el BCE sorprende al mercado."),
    # ---- legítimas con palabras de vehículo en su sentido corriente
    ("generico", "La acción de los bancos centrales sostiene a la renta fija."),
    ("generico", "El bono de referencia alemán cae."),
    ("generico", "Los ETF de oro físico captan dinero."),
    ("generico", "Las acciones europeas pesan menos en los índices globales."),
    ("generico", "Los fondos de renta fija corta reciben flujos."),
    ("generico", "El valor de la libra depende del Banco de Inglaterra."),
    ("generico", "Un ETF es un fondo que cotiza en bolsa."),
    ("generico", "Una SOCIMI es una sociedad que invierte en inmuebles."),
    ("generico", "Los ETF suben con el oro."),
    ("generico", "El fondo va bien cuando bajan los tipos."),
    # ---- coste: números en letra que un analista escribiría y que no son probabilidades ni datos del paquete
    ("coste", "Los dos grandes bancos centrales van por caminos distintos."),
    ("coste", "Los bonos cupón cero sufren más con las subidas de tipos."),
    ("coste", "La Fed ha recortado dos veces este año."),
    ("coste", "Los tres riesgos principales son la inflación, el empleo y la política."),
    ("coste", "Es la primera vez en diez años que pasa algo así."),
    ("coste", "El Euro Stoxx cincuenta sube con los bancos."),
    ("coste", "El S&P quinientos marca máximos."),
    ("coste", "El IBEX treinta y cinco depende de la banca."),
    ("coste", "Hay mil millones de razones para la prudencia."),
    ("coste", "Los beneficios crecen a doble dígito."),
    ("coste", "Una de las ideas depende del petróleo."),
    ("coste", "La política de tipos cero quedó atrás."),
    ("coste", "Los siete grandes tecnológicos pesan demasiado en el índice."),
    ("coste", "En los dos últimos meses el dólar ha bajado."),
    ("coste", "La inflación duplica el objetivo del banco central."),
    ("coste", "El tipo marginal y medio de la subasta baja."),
    ("coste", "Citamos la fecha y medio de cada noticia."),
    ("coste", "Tolerancia cero con el apalancamiento."),
    # ---- prohibidas: cantidades o probabilidades con palabras numéricas que faltan en la lista
    ("r13_letra", "La probabilidad de impago es de una entre un billón."),
    ("r13_letra", "Las opciones de recorte son de una milésima."),
    ("r13_letra", "Sube una veinteava parte de las veces."),
    ("r13_letra", "El riesgo de cola es de un onceavo."),
    ("r13_letra", "Es un fifty-fifty entre subida y bajada."),
    ("r13_letra", "Las probabilidades están fifty fifty."),
    ("r13_letra", "En medio centenar de simulaciones el oro sube."),
    ("r13_letra", "En una decena de casos de cada centenar el BCE sorprende."),
    ("r13_letra", "Sube en un centenar de simulaciones de cada millar."),
    ("r13_letra", "La centésima parte de las simulaciones acaba en impago."),
    ("r13_letra", "La probabilidad de recesión ronda la milésima."),
    ("r13_letra", "Una docena de escenarios favorecen al dólar."),
    ("r13_letra", "Gana en un par de semanas de cada docena."),
    ("r13_letra", "Las probabilidades son de uno a uno."),
    # ---- prohibidas: números compuestos con marcadores
    ("r13_marcador", "Las apuestas están {n_ideas} a uno a favor del dólar."),
    ("r13_marcador", "Sube una por cada {n_ideas} semanas."),
    ("r13_marcador", "El PIB crece un {n:RV},{n:RF} este año."),
    ("r13_marcador", "La inflación baja al {n:RV}.{n:DIV} en la zona euro."),
    ("r13_marcador", "La rentabilidad esperada es del {n:RV}'{n:RF}."),
    ("r13_marcador", "El apalancamiento llega a {n:RV}x."),
    ("r13_marcador", "Probabilidades por escenario:\n- base: {n:RV} de {candidatas:RV}\n- bajista: {n:RF} de {candidatas:RF}"),
    ("r13_marcador", "Grado de confianza.\n{n_tipos} de {n_ideas}."),
    ("r13_marcador", "Escenario alcista:\n{n:RV} veces de {candidatas:RV}."),
    # ---- prohibidas: sufijos de sociedad o de fondo que la regla promete y no ve
    ("r21_sufijo", "Pfizer Inc. sube con fuerza."),
    ("r21_sufijo", "Danaher Corp. es la idea de la semana."),
    ("r21_sufijo", "Ideas:\n- Schlumberger Ltd.\n- Heineken Holding"),
    ("r21_sufijo", "Recomendamos Unilever Plc."),
    ("r21_sufijo", "Merck KGaA es la idea."),
    ("r21_sufijo", "Recomendamos Nokia Oyj."),
    ("r21_sufijo", "Recomendamos Bestinver Sicav."),
    ("r21_sufijo", "Merlin Properties Socimi gana peso."),
    ("r21_sufijo", "recomendamos tesla inc"),
    ("r21_sufijo", "Nos gusta nvidia corporation."),
    ("r21_sufijo", "Recomendamos Alibaba Group Holding."),
    ("r21_sufijo", "Recomendamos Vale Ltda."),
    ("r21_sufijo", "Recomendamos Petronas Bhd."),
    # ---- prohibidas: nombres de fondo con vehículo de sufijo
    ("r21_fondo", "Nos gusta Invesco Physical Gold ETC."),
    ("r21_fondo", "Preferimos CoinShares Physical Bitcoin ETP."),
    ("r21_fondo", "Preferimos el WisdomTree Copper ETC."),
    ("r21_fondo", "Elegimos el iPath Bloomberg Commodity ETN."),
    # ---- límites declarados
    ("limite", "Recomendamos el fondo Naranja."),
    ("limite", "Comprar Vanguard FTSE All-World."),
    ("limite", "Preferimos el ETF de iShares sobre el MSCI World."),
    ("limite", "Recomendamos nvda esta semana."),
    ("limite", "Comprar el título msft."),
    # ---- exóticas (mala fe)
    ("exotica", "Comprar ṄVDA ya."),
    ("exotica", "Comprar ƝVDA ya."),
    ("exotica", "Comprar \U0001F17D\U0001F185\U0001F173\U0001F170 ya."),
    ("exotica", "Comprar N V D A ya."),
    ("exotica", "Comprar N⠀V⠀D⠀A ya."),
    ("exotica", "Las VII ideas tienen la misma probabilidad."),
    ("exotica", "Comprar N_V_D_A ya."),
]


def evaluar(raiz) -> tuple[dict, object, dict, dict]:
    M = C.preparar(raiz)
    v6 = M["v6"]
    perm = v6.permitidos_r21(C.bloque())
    marcas = dict(C.ciclo()["marcas"] or {})
    for t in TIPOS:
        marcas.setdefault(f"tipo:{t}", t.lower())
        marcas.setdefault(f"n:{t}", "2")
        marcas.setdefault(f"candidatas:{t}", "5")
    for o in ("OPP-X", "OPP-Y"):
        marcas.setdefault(f"opp:{o}", "esta idea")
    res: dict[str, list] = defaultdict(list)
    for g, f in BANCO:
        res[g].append((f, v6.texto_prohibido(f, perm, marcas)))
    return res, v6, perm, marcas


def main() -> int:
    res, *_ = evaluar(sys.argv[1])
    if "--lista" in sys.argv:
        for g, lst in res.items():
            for f, r in lst:
                print(f"{g}\t{r}\t{f!r}")
        return 0
    malos = 0
    print("Legítimas (CA-13, deben conservarse):")
    for g in LEGITIMAS:
        q = [x for x in res[g] if x[1]]
        malos += len(q)
        print(f"  {g:13}: quitadas {len(q)}/{len(res[g])}")
    print("Prohibidas (deben quitarse):")
    for g in PROHIBIDAS:
        p = [x for x in res[g] if not x[1]]
        malos += len(p)
        print(f"  {g:13}: pasan {len(p)}/{len(res[g])}")
    print("Aparte (se informan):")
    for g in APARTE:
        q = [x for x in res[g] if x[1]]
        print(f"  {g:13}: quitadas {len(q)}/{len(res[g])}")
    tl = sum(len(res[g]) for g in LEGITIMAS)
    ql = sum(1 for g in LEGITIMAS for _, r in res[g] if r)
    tp = sum(len(res[g]) for g in PROHIBIDAS)
    pp = sum(1 for g in PROHIBIDAS for _, r in res[g] if not r)
    print(f"TOTAL legítimas quitadas {ql}/{tl}; prohibidas que pasan {pp}/{tp}")
    print("Detalle:")
    for g in LEGITIMAS + ("coste",):
        for f, r in res[g]:
            if r:
                print(f"  [FP {g}] ({r}) {f!r}")
    for g in PROHIBIDAS:
        for f, r in res[g]:
            if not r:
                print(f"  [FN {g}] {f!r}")
    if "--detalle" in sys.argv:
        for g in ("limite", "exotica"):
            for f, r in res[g]:
                print(f"  [{g}] {r} {f!r}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
