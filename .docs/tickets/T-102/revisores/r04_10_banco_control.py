"""QA r04 de T-102 (revisor nuevo, ronda relanzada sobre `b36176a`) · Banco de control propio.

Escrito por este revisor sin mirar los bancos de las rondas anteriores ni las pruebas del implementador, para medir la
generalización de la regla estricta del Sintetizador (CIFRA, R21, MARCADOR). Todas las frases están escritas como pide §4 del
prompt (sin dígitos y sin códigos fuera de la lista), salvo las prohibidas, que buscan las formas que un modelo al que se le
prohíben los dígitos y los códigos escribiría de todas formas.

Grupos:
- Legítimas (deben conservarse): «llana» (sin números ni siglas), «sigla» (siglas de la lista, de los doce tipos), «marcador»
  (con marcadores bien usados), «tiempo» (expresiones de tiempo o lugar con «medio», «mitad», «segundo»…, que no son cifras),
  «region» (regiones y países tras un vehículo genérico: «las acciones de Europa»).
- «ambigua»: números en letra que no son una probabilidad («los dos bancos centrales»). El prompt dice «ninguna cifra»; se
  informan, no cuentan.
- Prohibidas (deben quitarse): «r13_letra» (probabilidad o frecuencia numérica en letra, sin «%» ni «por ciento»),
  «r13_marcador» (probabilidad compuesta con marcadores), «r21_sufijo» (sufijo societario que la regla promete cazar),
  «r21_invisible» (código partido por caracteres invisibles o marcas combinantes: en pantalla se lee el código entero),
  «r21_vehiculo» (ticker en minúscula tras un vehículo en español: acción, valor, título).
- «limite»: lo declarado como límite en `analisis-tecnico.md` (nombre propio, minúscula sin vehículo, colisión, una letra).
- «control»: formas prohibidas que ya se quitan (prefijo de bolsa, N.V., A/S, ancho completo…). Se informan aparte.
- «exotica»: escrituras de mala fe que NFKC no pliega (cheroqui, versalitas, indicadores regionales). Se informan aparte.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_10_banco_control.py <raiz_repo> [--detalle | --lista]
Sale con 1 si alguna legítima de los grupos que cuentan se quita o alguna prohibida pasa. No escribe en el repositorio.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

TIPOS = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
LEGITIMAS = ("llana", "sigla", "marcador", "tiempo", "region")
PROHIBIDAS = ("r13_letra", "r13_marcador", "r21_sufijo", "r21_invisible", "r21_vehiculo")
APARTE = ("ambigua", "limite", "exotica", "control")
ZWSP, SHY, WJ, UND = "\u200b", "\u00ad", "\u2060", "\u0332"

BANCO: list[tuple[str, str]] = [
    # --- llana: sin números ni siglas
    ("llana", "La renta variable europea gana peso frente a la estadounidense."),
    ("llana", "El crédito de peor calidad sufre cuando suben los diferenciales."),
    ("llana", "El dólar se aprecia frente a casi todas las monedas."),
    ("llana", "El oro aguanta bien en los episodios de tensión."),
    ("llana", "Los fondos mixtos reciben entradas por segundo trimestre consecutivo."),
    ("llana", "Las opciones sobre índices encarecen la cobertura."),
    ("llana", "Los alquileres de oficinas siguen bajo presión."),
    ("llana", "Las criptomonedas se mueven con el apetito por el riesgo."),
    ("llana", "El capital privado tarda en reflejar las caídas de la bolsa."),
    ("llana", "Los depósitos remuneran menos tras los recortes de tipos."),
    ("llana", "La curva de tipos se empina y premia los plazos largos."),
    ("llana", "Es probable que el banco central mantenga los tipos."),
    ("llana", "Las probabilidades de un recorte han subido esta semana."),
    ("llana", "El mercado descuenta con bastante confianza una pausa."),
    ("llana", "Hay poca certeza sobre la inflación de servicios."),
    ("llana", "Los escenarios alcista y bajista quedan lejos del central."),
    ("llana", "La confianza del consumidor cae por segundo mes."),
    ("llana", "Los ETF de oro reciben entradas."),
    ("llana", "Varios ETF de renta fija ganan peso."),
    ("llana", "Los REIT de oficinas sufren con el teletrabajo."),
    ("llana", "Un fondo de renta fija a corto plazo reduce la duración."),
    ("llana", "Los futuros de crudo anticipan déficit."),
    # --- sigla: siglas de la lista
    ("sigla", "El BCE y la Fed divergen en el ritmo de recortes."),
    ("sigla", "La RV de EEUU se apoya en la IA."),
    ("sigla", "El USD gana frente al EUR y al JPY."),
    ("sigla", "Los bonos HY y los IG divergen."),
    ("sigla", "El VIX sube con las dudas."),
    ("sigla", "El DXY cae frente a las monedas EM."),
    ("sigla", "El PMI manufacturero mejora."),
    ("sigla", "El S&P marca máximos mientras el DAX se queda atrás."),
    ("sigla", "La OPEP recorta la producción."),
    ("sigla", "El IPC sube más de lo previsto."),
    ("sigla", "El PIB de la eurozona se frena."),
    ("sigla", "Los TIPS protegen de la inflación."),
    ("sigla", "Las SOCIMI cotizadas descuentan valor."),
    ("sigla", "El MSCI World pesa más en tecnología."),
    ("sigla", "Los CDS de la periferia se estrechan."),
    ("sigla", "Las letras ganan atractivo con el BCE en pausa."),
    # --- marcador
    ("marcador", "Esta semana vemos {n_ideas} ideas en {n_tipos} tipos de inversión."),
    ("marcador", "{opp:OPP-2026-0001} depende del dólar."),
    ("marcador", "En {tipo:DIV} hay {n:DIV} opciones de {candidatas:DIV} ideas analizadas."),
    ("marcador", "Las {n_ideas} ideas se reducen a {n_apuestas} apuestas independientes."),
    ("marcador", "Es probable que {opp:OPP-2026-0002} sufra si sube el dólar."),
    ("marcador", "{opp:OPP-2026-0003} y {opp:OPP-2026-0001} comparten riesgo."),
    # --- tiempo: «medio», «mitad», «segundo», «Oriente Medio»: no son cifras
    ("tiempo", "Es probable que el BCE recorte en la segunda mitad del año."),
    ("tiempo", "Es probable que la renta fija gane a medio plazo."),
    ("tiempo", "En el escenario central, el dólar se debilita a medio plazo."),
    ("tiempo", "El riesgo en Oriente Medio pesa en los escenarios del crudo."),
    ("tiempo", "La confianza empresarial se recupera en la segunda mitad del trimestre."),
    ("tiempo", "Hay poca certeza sobre el medio plazo."),
    # --- region: país o región tras un vehículo genérico
    ("region", "Las acciones de Europa ganan peso frente a las de EEUU."),
    ("region", "Las opciones sobre Europa encarecen la cobertura."),
    ("region", "El fondo Europa del Este sufre con la guerra."),
    ("region", "Cada ETF replica un índice distinto."),
    ("region", "Las acciones de Japón suben con el yen débil."),
    # --- ambigua (se informa)
    ("ambigua", "La seguridad jurídica mejora en dos de los mercados."),
    ("ambigua", "La confianza empresarial cae en la mitad de los países."),
    ("ambigua", "Los dos escenarios favorecen al dólar."),
    ("ambigua", "La confianza del consumidor es uno de los riesgos."),
    ("ambigua", "Es el doble de probable que suba."),
    ("ambigua", "La curva de los UST se empina."),
    ("ambigua", "Las empresas BB sufren más."),
    # --- r13_letra: probabilidad o frecuencia numérica en letra
    ("r13_letra", "Sube una de cada tres veces."),
    ("r13_letra", "Una de cada dos semanas el dólar sube tras el dato de empleo."),
    ("r13_letra", "Sube siete veces de cada diez."),
    ("r13_letra", "De cada diez veces, siete acaban en subida."),
    ("r13_letra", "Vemos un sesenta-cuarenta a favor de la subida."),
    ("r13_letra", "Es un cincuenta-cincuenta que el BCE recorte."),
    ("r13_letra", "Las cuotas están tres a uno a favor del alza."),
    ("r13_letra", "Apostamos tres contra uno a que el oro sube."),
    ("r13_letra", "Hay una cuarta parte de probabilidad de caída."),
    ("r13_letra", "Hay una tercera parte de probabilidad de que el BCE suba."),
    ("r13_letra", "Le damos una cuarta parte de opciones a la caída."),
    ("r13_letra", "Dos terceras partes de las simulaciones acaban en subida."),
    ("r13_letra", "En siete de diez simulaciones la bolsa sube."),
    ("r13_letra", "El riesgo de impago es de tres por mil."),
    ("r13_letra", "Una vez de cada cuatro, el crudo cae tras la reunión."),
    ("r13_letra", "Las criptomonedas caen la mitad de las veces tras un máximo."),
    ("r13_letra", "Nueve de diez veces el oro sube tras un recorte."),
    # controles r13 (formas que el implementador cubrió: deben quitarse)
    ("r13_letra", "Siete de cada diez veces sube."),
    ("r13_letra", "La probabilidad de subida es de setenta sobre cien."),
    ("r13_letra", "Hay dos tercios de probabilidad de recorte."),
    # --- r13_marcador
    ("r13_marcador", "La renta variable sube {n:DIV} veces de cada {candidatas:DIV}."),
    ("r13_marcador", "Las apuestas van {n:DIV} contra {n_tipos} a favor del dólar."),
    ("r13_marcador", "Sube {n:DIV} de cada {candidatas:DIV} semanas."),
    ("r13_marcador", "La probabilidad es de {n:DIV} sobre {candidatas:DIV}."),
    # --- r21_sufijo
    ("r21_sufijo", "Recomendamos Enel SpA."),
    ("r21_sufijo", "Recomendamos Enel S.p.A. para la cartera."),
    ("r21_sufijo", "Comprar Toyota Motor Co. ya."),
    ("r21_sufijo", "Comprar Rio Tinto Limited."),
    ("r21_sufijo", "Recomendamos apple inc."),
    ("r21_sufijo", "Vender Deutsche Bank Aktiengesellschaft."),
    ("r21_sufijo", "Comprar Infineon Technologies AG."),
    ("r21_sufijo", "Comprar Unilever plc."),
    ("r21_sufijo", "Recomendamos el Vanguard Global Stock Index Fund."),
    ("r21_sufijo", "Comprar Grifols, S.A."),
    # --- r21_invisible
    ("r21_invisible", f"Comprar N{ZWSP}V{ZWSP}D{ZWSP}A ya."),
    ("r21_invisible", f"Comprar N{SHY}V{SHY}D{SHY}A ya."),
    ("r21_invisible", f"Comprar N{WJ}V{WJ}D{WJ}A ya."),
    ("r21_invisible", f"Comprar N{UND}V{UND}D{UND}A{UND} ya."),
    ("r21_invisible", f"La opción preferida es T{ZWSP}S{ZWSP}L{ZWSP}A."),
    ("r21_invisible", f"Comprar NV{ZWSP}DA ya."),   # control (dos trozos de dos letras)
    # --- r21_vehiculo
    ("r21_vehiculo", "Comprar la acción nvda."),
    ("r21_vehiculo", "Comprar el valor nvda."),
    ("r21_vehiculo", "Comprar el título tsla."),
    ("r21_vehiculo", "Comprar el ETF qqq."),   # control
    # --- limite (declarado)
    ("limite", "Recomendamos comprar Tesla."),
    ("limite", "La opción preferida es nvda."),
    ("limite", "Comprar COP antes del dividendo."),
    ("limite", "Comprar F ya."),
    # --- control: formas que deben quitarse y ya se quitan (se informan aparte, no cuentan en las tasas)
    ("control", "Comprar NASDAQ:NVDA ya."),
    ("control", "Vender Ferrari N.V. cuanto antes."),
    ("control", "Comprar Novo Nordisk A/S."),
    ("control", "Comprar Siemens AG."),
    ("control", "Comprar \uff2e\uff36\uff24\uff21 ya."),
    ("control", "Comprar Toyota Motor Co., Ltd."),
    ("control", "Comprar Sony Group Corporation."),
    ("control", "Comprar \u24c3\u24cb\u24b9\u24b6 ya."),
    ("control", "Comprar $EUR ya."),
    # --- exotica
    ("exotica", "Comprar ᏚᏢᎩ cuanto antes."),
    ("exotica", "Comprar ɴᴠᴅᴀ ya."),
    ("exotica", "Comprar \U0001F1F3\U0001F1FB\U0001F1E9\U0001F1E6 ya."),
    ("exotica", "La subida es del {n:DIV} ٪."),
    ("exotica", "Vemos 〔n_ideas〕 ideas."),
]


def main() -> int:
    raiz = sys.argv[1]
    detalle = "--detalle" in sys.argv
    M = C.preparar(raiz)
    v6 = M["v6"]
    b = C.bloque()
    perm = v6.permitidos_r21(b)
    base = C.ciclo()
    marcas = dict(base["marcas"] or {})
    for t in TIPOS:
        marcas.setdefault(f"tipo:{t}", t.lower())
        marcas.setdefault(f"n:{t}", "2")
        marcas.setdefault(f"candidatas:{t}", "5")
    res: dict[str, list] = defaultdict(list)
    for g, f in BANCO:
        res[g].append((f, v6.frase_prohibida(f, perm, marcas)))
    if "--lista" in sys.argv:   # para r04_14: una línea por frase (grupo, regla, frase)
        for g, f in BANCO:
            print(f"{g}\t{dict(res[g])[f]}\t{f!r}")
        return 0
    malos = 0
    print("Legítimas (deben conservarse):")
    for g in LEGITIMAS:
        q = [(f, r) for f, r in res[g] if r]
        malos += len(q)
        print(f"  {g:13}: quitadas {len(q)}/{len(res[g])}")
    print("Prohibidas (deben quitarse):")
    for g in PROHIBIDAS:
        p = [(f, r) for f, r in res[g] if not r]
        malos += len(p)
        print(f"  {g:13}: pasan {len(p)}/{len(res[g])}")
    print("Aparte (se informan):")
    for g in APARTE:
        q = [(f, r) for f, r in res[g] if r]
        print(f"  {g:13}: quitadas {len(q)}/{len(res[g])}")
    tl = sum(len(res[g]) for g in LEGITIMAS)
    ql = sum(1 for g in LEGITIMAS for _, r in res[g] if r)
    tp = sum(len(res[g]) for g in PROHIBIDAS)
    pp = sum(1 for g in PROHIBIDAS for _, r in res[g] if not r)
    print(f"TOTAL legítimas quitadas {ql}/{tl} ({100 * ql / tl:.1f} %); prohibidas que pasan {pp}/{tp} ({100 * pp / tp:.1f} %)")
    print("Fallos:")
    for g in LEGITIMAS:
        for f, r in res[g]:
            if r:
                print(f"  [FP {g}] ({r}) «{f!r}»")
    for g in PROHIBIDAS:
        for f, r in res[g]:
            if not r:
                print(f"  [FN {g}] «{f!r}»")
    if detalle:
        for g in APARTE:
            for f, r in res[g]:
                print(f"  [{g}] {r} «{f!r}»")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
