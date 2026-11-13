"""QA r04 de T-102 · Sondas escritas DESPUÉS de leer las expresiones de la r04 (no son el banco ciego: `r04_01`).

Cada sonda apunta a una pieza nueva de la r04 con frases naturales de un informe llano:
- «vehiculo»: un vehículo («fondo», «ETF», «REIT»…) seguido de un verbo o una palabra corta en minúscula («El fondo es…»);
- «medio»: «medio», «mitad», «mil millones»… (de `_NUM_LETRA`) en una frase con una palabra de probabilidad o «escenario»;
- «sufijo»: una palabra con mayúscula que no es artículo antes de «ETF», «Fund», «Trust», «SE»… («Cada ETF…», «Comprar ETF…»);
- «region»: «acciones de», «opciones sobre» o «fondo» seguido de un nombre propio de región o de programa;
- «alfabeto»: letras griegas de uso técnico (α, β, Δ);
- «mixta»: plurales de siglas que no están en la lista («ONGs»);
- «fuera»: siglas corrientes de los doce tipos que no están en la lista ni en las rondas anteriores (fallan cerrado y se
  declaran; el prompt da ahora la lista, así que el modelo debería evitarlas).
Las legítimas no deben quitarse. Además, prohibidas por formas vecinas a las que la r04 cubre.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_02_sondas.py <raiz_repo>
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r04_01_banco_nuevo as B  # noqa: E402

LEGITIMAS = {
    "vehiculo": [
        "El fondo es sencillo y barato.", "En el fondo, todas dependen del dólar.", "Los ETF son la vía más barata para entrar.",
        "El ETF sube con el oro.", "Los REIT ganan cuando bajan los tipos.", "Un fondo así cae menos en las crisis.",
        "El fondo ha batido a su índice.", "Los REIT van a sufrir con tipos altos.", "Cada fondo da su NAV a diario.",
        "Las SOCIMI son sociedades que alquilan inmuebles.", "Ese ETF no reparte dividendos.", "El fondo sube poco pero seguro.",
        "Al fondo del problema está la inflación.", "El fondo tiene comisiones bajas.", "Un ETF mide lo que sube su índice.",
    ],
    "medio": [
        "Es probable que el euro se aprecie a medio plazo.", "En el escenario base, la RV sube a medio plazo.",
        "Es probable que el petróleo suba por la tensión en Oriente Medio.",
        "La confianza del consumidor cae a mínimos de medio año.",
        "Es probable que la Fed recorte una vez más.", "La seguridad jurídica pesa en la mitad de los mercados emergentes.",
        "Es probable que los flujos hacia los ETF superen los mil millones.",
        "El escenario de riesgo es que la inflación vuelva a subir dos veces seguidas.",
        "Hay pocas posibilidades de que el BCE recorte dos veces seguidas.",
    ],
    "sufijo": [
        "Cada ETF tiene su propio coste.", "Comprar ETF de oro es la forma más sencilla de tener oro.",
        "Ningún ETF elimina el riesgo de mercado.", "Cualquier ETF de RV sufre en una recesión.",
        "Todo ETF replica un índice.", "Invertir en ETF reduce costes.",
    ],
    "region": ["Las acciones de Europa están baratas.", "Las acciones de China dependen del estímulo.",
               "Las acciones de Asia suben.", "Las acciones de India siguen caras.", "Las opciones sobre Europa encarecen.",
               "El fondo Next Generation de la UE apoya la inversión."],
    "alfabeto": ["La β del sector es alta.", "La delta (Δ) de las opciones cambia con el precio."],
    "mixta": ["Las ONGs piden más regulación.", "Las OPVs vuelven al mercado."],
    "fuera": [
        "El CEO de la Fed no existe, pero sí su presidente.", "La EPA muestra un paro más bajo.", "El €STR marca la liquidez en euros.",
        "Las operaciones de M&A se reactivan.", "El TLTRO del BCE ya venció.", "El LBO depende de la financiación barata.",
        "El FFO de las SOCIMI mejora.", "El LTV de los préstamos inmobiliarios baja.", "Los CTA ganan con tendencias claras.",
        "La CBDC del BCE avanza.", "El TVL de las finanzas descentralizadas cae.", "Los informes del USDA mueven el trigo.",
        "La AIE revisa la demanda de petróleo.", "El FTSE MIB sube con los bancos.", "El TAE de los depósitos baja.",
        "El CBOE publica el VIX.", "La PPP sugiere que el yen está barato.", "Los ZEW e IFO alemanes mejoran.",
    ],
}
PROHIBIDAS = {
    "vehiculo_fuera": ["Comprar la acción nvda.", "Recomendamos el título tsla.", "Recomendamos el valor amd.",
                       "Recomendamos el fondo vwrl.", "Recomendamos el fondo iwda.", "Comprar el ETF Nvda.",
                       "Recomendamos el tracker iwda.", "Comprar la cripto sol.", "Comprar el token pepe."],
    "r13_vecinas": ["La probabilidad de subida es de setenta y cinco.", "Las opciones de subida son de tres a uno.",
                    "Hay un setenta porciento de opciones.", "Vemos tres posibilidades de cuatro.",
                    "La subida tiene setenta papeletas de cien.", "Un escenario de cada tres acaba en caída.",
                    "Lo más probable, tres veces de cada cuatro, es que suba.", "Las cuotas están en tres a uno.",
                    "Sale bien {n:RV} veces de {candidatas:RV}.", "Acierta {n:RV} de cada {candidatas:RV} veces.",
                    "Con {n_ideas} contra {n_tipos}, la subida gana."],
    "r21_vecinas": ["Comprar N V D A ya.", "Comprar N·V·D·A ya.", "Comprar NV DA ya.", "Comprar la acción NVDA.",
                    "La idea es Nvidia (NVDA).", "Comprar Apple, Inc", "Comprar Apple Incorporated.", "Comprar Inditex S.L.",
                    "Comprar Iberdrola SA.", "Comprar Banco Santander S.A.", "Comprar Toyota K.K.", "Comprar Nestlé AG."],
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    M, base, perm = B.preparar(args[0] if args else ".")
    v6, marcas = M["v6"], base["marcas"]
    tot_l = tot_fp = 0
    print("LEGÍTIMAS (no deben quitarse)")
    for g, fs in LEGITIMAS.items():
        malas = [(f, v6.limpiar(f, perm, marcas)[1]) for f in fs]
        malas = [(f, r) for f, r in malas if r]
        tot_l += len(fs)
        tot_fp += len(malas) if g != "fuera" else 0
        print(f"  {g:9} quitadas {len(malas)}/{len(fs)}")
        for f, r in malas:
            print(f"      {r} {f}")
    print("PROHIBIDAS (deben quitarse)")
    pasan = defaultdict(list)
    for g, fs in PROHIBIDAS.items():
        for f in fs:
            s, r = v6.limpiar(f, perm, marcas)
            if not r:
                pasan[g].append(s)
        print(f"  {g:15} pasan {len(pasan[g])}/{len(fs)}")
        for s in pasan[g]:
            print(f"      PASA: {s!r}")


if __name__ == "__main__":
    main()
