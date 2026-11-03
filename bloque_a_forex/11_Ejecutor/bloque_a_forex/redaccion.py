"""Redacción de entregables (F7): informe técnico (Markdown), informe visual (HTML autocontenido a partir de la
plantilla vigente del informe visual del Bloque A Forex: mapa de monedas que suben y bajan, lista accesible, termómetro
de la divisa base, semáforo de los seis segmentos y tarjetas con banderas) y paquete JSON conforme al esquema del
Bloque A Forex V1.0 (Anexo B; sin instrumentos). Las plantillas se localizan por su nombre con cualquier sufijo de
versión, con preferencia por las del Bloque A Forex. Después, HT-07 sobre el informe visual y segunda pasada de HT-09
con coherencia entre los tres entregables."""
from __future__ import annotations

import copy
import json
import re
from html import escape
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import jsonschema
import pandas as pd

from . import fx
from .configuracion import NOMBRE_SEGMENTO, buscar_versionado, ruta
from .herramientas import ht04_graficos as ht04
from .herramientas import ht07

# Nombre llano y aclaración de los seis segmentos (plantilla visual Forex V1.0)
LLANO = {"G10N": ("Grandes monedas", "dólar, euro, yen, libra, franco"),
         "G10M": ("Monedas de materias primas", "Australia, Canadá, Noruega…"),
         "EMAS": ("Asia emergente", "China, India, Corea…"),
         "EMLA": ("Latinoamérica", "México, Brasil, Chile…"),
         "EMEA": ("Europa del este, Oriente Medio y África", ""),
         "ESTR": ("Estrategias", "grupos de monedas con una regla fija")}
# Frase fija de la frontera con el Bloque B (plantilla visual Forex V1.0)
FRASE_BLOQUE_B = "Después, otro equipo del sistema estudiará cada idea y elegirá la mejor forma de llevarla a la práctica."
# Casillas fijas del mapa de monedas (columna, fila); las divisas que no figuran van a una fila adicional
MAPA = {"CAD": (1, 0), "USD": (1, 1), "MXN": (1, 2), "CLP": (1, 3), "COP": (2, 2), "BRL": (2, 3), "GBP": (3, 0), "EUR": (3, 1),
        "CHF": (3, 2), "NOK": (4, 0), "PLN": (4, 1), "ZAR": (4, 3), "SEK": (5, 0), "TRY": (5, 1), "INR": (5, 2), "CNH": (6, 1),
        "IDR": (6, 2), "KRW": (7, 1), "AUD": (7, 3), "JPY": (8, 1), "NZD": (8, 3)}
CAMPOS_OPCION_SOLO_SINTESIS = ("puertas", "cluster", "vigente")
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
SIN_VENTAJA = "aún sin ventaja demostrada frente a no hacer nada"


def fecha_larga(f) -> str:
    f = pd.Timestamp(f)
    return f"{DIAS[f.weekday()]}, {f.day} de {MESES[f.month - 1]} de {f.year}"


def entregable_json(paquete: Dict) -> Dict:
    p = copy.deepcopy(paquete)
    for d in p["segmentos"].values():
        for o in d["opciones"]:
            for k in CAMPOS_OPCION_SOLO_SINTESIS:
                o.pop(k, None)
            for h in o["horizontes"].values():
                h.pop("advertencia", None)
                h.pop("metodo", None)
            for ob in o["objeciones"]:
                ob.pop("resuelta", None)
            for k in ("por_que_llano", "que_puede_salir_mal_llano", "sube_baja_llano"):
                if k in o and not o[k]:
                    o.pop(k)
    return p


class Redaccion:
    def __init__(self, cfg: Dict) -> None:
        self.cfg = cfg
        base = ruta(cfg, "plantillas")
        # Se localizan por nombre con cualquier sufijo («… - Bloque A Forex - V1.0», …): gana la del Bloque A Forex
        self.plantilla_html = (buscar_versionado(base, "Plantilla - Informe visual para el usuario", ".html")
                               or base / "Plantilla - Informe visual para el usuario - Bloque A Forex - V1.0.html")
        self.esquema_json = (buscar_versionado(base, "Esquema JSON - Paquete de oportunidades", ".json")
                             or base / "Esquema JSON - Paquete de oportunidades - Bloque A Forex - V1.0.json")

    # ------------------------------------------------------------------------------------
    def textos_por_defecto(self, paquete: Dict) -> Dict:
        n = sum(len(d["opciones"]) for d in paquete["segmentos"].values())
        nc = sum(1 for d in paquete["segmentos"].values() if d["opciones"])
        return {"frases_30s": [f"Esta semana vemos {n} ideas en {nc} grupos de monedas.",
                               "Cada idea tiene su riesgo y su plazo.", "Nada de esto es un consejo para ti."],
                "tarjetas": [{"opp_id": o["opp_id"], "por_que_llano": "El sistema ve señales a favor de esta idea.",
                              "que_puede_salir_mal_llano": "La moneda puede moverse al revés de lo previsto.",
                              "sube_baja_llano": o.get("sube_baja_llano") or ""}
                             for d in paquete["segmentos"].values() for o in d["opciones"]],
                "motivos_llanos": {}, "glosario": [], "frase_historial": "Aún hay pocos casos para saber si acertamos más que el azar."}

    # ------------------------------------------------------------------------------------
    def _cabecera_plantilla(self) -> str:
        t = self.plantilla_html.read_text(encoding="utf-8")
        i = t.find('<div class="ejemplo"', max(t.find("<body"), 0))   # la de la franja, no la citada en el comentario
        cab = t[:i] if i > 0 else t[:t.find("<body>") + 6]
        return cab.replace('lang="es-ES"', f'lang="{self.cfg.get("idioma", "es-ES")}"')

    def visual(self, bloque, paquete: Dict, red: Dict, as_of) -> str:
        tarj = {t["opp_id"]: t for t in red.get("tarjetas", [])}
        segmentos = paquete["segmentos"]
        n_tot = sum(len(d["opciones"]) for d in segmentos.values())
        n_cl = sum(1 for d in segmentos.values() if d["opciones"])
        frases = (red.get("frases_30s") or [])[:3]
        todas = [o for d in segmentos.values() for o in d["opciones"]]
        neta = fx.exposicion_neta(todas)
        h = [self._cabecera_plantilla(), '<div class="wrap">']
        h.append(f'<header class="top"><div><div class="marca">Robot Investor · tus monedas esta semana</div>'
                 f'<h1>{escape(_semana_o_peticion(paquete))}</h1><p class="sub">Lo que el sistema ha visto en las monedas del mundo, explicado sin jerga.</p></div>'
                 f'<div class="meta"><div>{escape(fecha_larga(as_of).capitalize())}</div>'
                 f'<div>Datos del {escape(fecha_larga(paquete["fecha_datos_mercado"]))}</div></div></header>')
        if paquete.get("x_estado_run") == "PARCIAL":
            h.append('<div class="vacia" role="note"><b>Informe parcial.</b> Algunas partes no se pudieron completar. Lo decimos para que lo tengas en cuenta.</div>')
        h.append('<section aria-labelledby="h-30"><div class="panel"><h2 id="h-30">La semana en 30 segundos</h2><ol class="treinta">')
        for i, f in enumerate(frases):
            h.append(f'<li><span class="num" aria-hidden="true">{i + 1}</span><span>{escape(f)}</span></li>')
        h.append(f'</ol><div class="cifras"><div class="cifra"><b>{n_tot}</b><span>ideas</span></div>'
                 f'<div class="cifra"><b>{n_cl} de {len(segmentos)}</b><span>grupos con ideas</span></div>'
                 f'<div class="cifra"><b>{paquete["apuestas_independientes"]}</b><span>apuestas distintas</span></div></div></div></section>')
        # Mapa de monedas que suben y bajan + lista accesible + termómetro de la divisa base
        estado = {d: ("sube" if v > 0 else "baja") for d, v in neta.items()}
        extras = sorted(d for d in neta if d not in MAPA)
        casillas = dict(MAPA)
        for k, d in enumerate(extras):
            casillas[d] = (k % 9, 4 + k // 9)
        filas = max(r for _, r in casillas.values()) + 1
        g = []
        for d, (cx, fy) in casillas.items():
            x, y = 3 + 72 * cx, 3 + 64 * fy
            est = estado.get(d, "igual")
            fl = {"sube": "▲", "baja": "▼", "igual": "–"}[est]
            g.append(f'<g class="t {est}"><rect x="{x}" y="{y}" width="66" height="58"/><text x="{x + 13}" y="{y + 25}">{d}</text>'
                     f'<text class="fl" x="{x + 13}" y="{y + 47}">{fl}</text></g>')
        suben = [d for d, v in sorted(neta.items(), key=lambda x: -x[1]) if v > 0]
        bajan = [d for d, v in sorted(neta.items(), key=lambda x: x[1]) if v < 0]
        alt = (f"Podrían subir: {', '.join(fx.llano(d, False) for d in suben) or 'ninguna'}. "
               f"Podrían bajar: {', '.join(fx.llano(d, False) for d in bajan) or 'ninguna'}. Sin cambio esperado: el resto.")
        def lista(xs):
            """Grupos de hasta cinco monedas por línea (bloques <br>), para que ninguna «frase» supere 20 palabras."""
            if not xs:
                return "ninguna esta semana"
            trozos = [" · ".join(f"{fx.bandera(d)} {escape(fx.llano(d, False))}" for d in xs[i:i + 5]) for i in range(0, len(xs), 5)]
            return "<br>".join(trozos)
        h.append('<section class="duo"><div class="panel mapa" aria-labelledby="h-mapa"><h2 id="h-mapa">Qué monedas suben y cuáles bajan</h2>'
                 '<p class="peq">Cada casilla es una moneda, colocada más o menos donde está en el mapa. Flecha arriba: podría ganar valor. '
                 'Flecha abajo: podría perderlo.</p>'
                 f'<svg viewBox="0 0 648 {64 * filas}" role="img" aria-labelledby="mapa-t mapa-d"><title id="mapa-t">Mapa de monedas que podrían subir o bajar</title>'
                 f'<desc id="mapa-d">{escape(alt)}</desc>{"".join(g)}</svg>'
                 '<div class="leyenda" aria-hidden="true"><span><i style="background:var(--sube)"></i>▲ Podría subir</span>'
                 '<span><i style="background:var(--baja)"></i>▼ Podría bajar</span>'
                 '<span><i style="background:var(--igual-f);border:1px solid var(--igual)"></i>– Sin idea esta semana</span></div></div>')
        lb = paquete.get("lectura_divisa_base") or {"divisa": paquete.get("divisa_base_usuario") or "EUR", "sentido": "estable", "texto_llano": ""}
        nb = neta.get(lb["divisa"], 0.0)
        pos = round(50 + 25 * max(min(nb, 2.0), -2.0))
        tx_termo = {"se_aprecia": "gana algo de valor", "se_deprecia": "pierde algo de valor", "estable": "estable"}[lb["sentido"]]
        nom_base = fx.llano(lb["divisa"], False)
        h.append('<div class="panel" aria-labelledby="h-lista"><h2 id="h-lista">En una lista</h2><ul class="lista-divisas">'
                 f'<li class="sube"><b>▲ Podrían subir</b><span>{lista(suben)}</span></li>'
                 f'<li class="baja"><b>▼ Podrían bajar</b><span>{lista(bajan)}</span></li></ul>'
                 f'<div class="termo" aria-labelledby="h-termo"><h3 id="h-termo">Termómetro del {escape(nom_base)}</h3>'
                 f'<p class="peq">Qué significan estas ideas para quien ahorra en esa moneda.</p>'
                 f'<div class="barra" role="img" aria-label="{escape(fx.llano(lb["divisa"]).capitalize())}: {tx_termo}">'
                 f'<span class="marca-t" style="left:{pos}%"></span></div>'
                 '<div class="escala" aria-hidden="true"><span>Pierde valor</span><span>Estable</span><span>Gana valor</span></div>'
                 f'<p style="margin-top:8px">{escape(lb.get("texto_llano") or "")}</p></div></div></section>')
        # Semáforo de los seis segmentos (orden de la tabla 2.6)
        txt_sem = {"VERDE": ("verde", "Claras", "Claras"), "AMBAR": ("ambar", "Pocas", "Pocas o dudosas"),
                   "GRIS": ("gris", "Nada", "Nada destacable")}
        h.append(f'<section aria-labelledby="h-sem"><div class="panel"><h2 id="h-sem">Semáforo de los {_numero(len(segmentos))} grupos de monedas</h2>'
                 '<p class="peq">Verde: hay ideas claras. Ámbar: pocas o dudosas. Gris: nada destacable esta semana.</p><ul class="sem">')
        for c, d in segmentos.items():
            nom, peq = LLANO[c]
            cl, tx, _ = txt_sem[d["estado_semaforo"]]
            peq_html = f' <span class="peq">({escape(peq)})</span>' if peq else ""
            h.append(f'<li><span class="luz {cl}" aria-hidden="true"></span><span class="nom">{escape(nom)}{peq_html}</span>'
                     f'<span class="est">{tx} · {len(d["opciones"])}</span></li>')
        h.append('</ul></div></section>')
        h.append('<section aria-labelledby="h-despues"><div class="panel"><h2 id="h-despues">Qué pasa después</h2><ol class="pasos">'
                 '<li class="aqui"><span class="num" aria-hidden="true">1</span><span><b>Buscamos qué monedas pueden moverse.</b> '
                 'Una moneda frente a otra, un grupo de monedas o una forma de invertir en ellas.</span></li>'
                 f'<li><span class="num" aria-hidden="true">2</span><span><b>Otro equipo decide cómo.</b> {escape(FRASE_BLOQUE_B)}</span></li>'
                 '<li><span class="num" aria-hidden="true">3</span><span><b>Tu Broker decide contigo.</b> '
                 'Tu Broker Personal mira si alguna idea encaja con tus metas y tu riesgo.</span></li></ol></div></section>')
        # Tarjetas
        h.append('<section aria-labelledby="h-ideas"><h2 id="h-ideas">Las ideas, una a una</h2>'
                 '<p class="sub">Riesgo de 1 (muy bajo) a 5 (muy alto). La barra azul dice cuánto confiamos.</p>')
        nivel_r = {1: "muy bajo", 2: "bajo", 3: "medio", 4: "alto", 5: "muy alto"}
        conf = {"establecido": (3, "Alta"), "probable": (2, "Media"), "especulativo": (1, "Baja"), "en disputa": (1, "Baja")}
        hz_txt = [("H1", "días"), ("H2", "semanas"), ("H3", "meses"), ("H4", "años"), ("H5", "décadas")]
        k_card = 0
        orden = [c for c in segmentos if segmentos[c]["opciones"]] + [c for c in segmentos if not segmentos[c]["opciones"]]
        for c in orden:
            d = segmentos[c]
            nom, _ = LLANO[c]
            cl, _, tx_largo = txt_sem[d["estado_semaforo"]]
            h.append(f'<div class="seg-h"><span class="luz {cl}" aria-hidden="true"></span><h3>{escape(nom)}</h3><span class="peq">{tx_largo}</span></div>')
            if d["opciones"]:
                h.append('<div class="tarjetas">')
            for o in d["opciones"]:
                k_card += 1
                t = tarj.get(o["opp_id"], {})
                pq = o.get("por_que_llano") or t.get("por_que_llano") or "El sistema ve señales a favor de esta idea."
                mal = o.get("que_puede_salir_mal_llano") or t.get("que_puede_salir_mal_llano") or "La moneda puede moverse al revés."
                r = o["riesgo_1a5"]
                pips = "".join('<i class="on"></i>' if i < r else "<i></i>" for i in range(5))
                # V1.1: el horizonte principal se destaca en negrita; «décadas» solo aparece si la opción ofrece H5
                hzs = "".join((f'<span class="on"><b>{tx_}</b></span>' if hh == o.get("horizonte_principal") else
                               f'<span{" class=\"on\"" if hh in o["horizontes"] else ""}>{tx_}</span>')
                              for hh, tx_ in hz_txt if hh != "H5" or "H5" in o["horizontes"])
                nconf, tconf = conf[o["confianza"]]
                segs = "".join('<i class="on"></i>' if i < nconf else "<i></i>" for i in range(3))
                hp = o["horizontes"][o["horizonte_principal"]]
                cert = (SIN_VENTAJA if not hp["certificado_r13"] or hp.get("prob") is None
                        else f"en {round(hp['prob'] * 10)} de cada 10 casos parecidos acertamos")
                graf = _spark(bloque, o, as_of, f"g{k_card}t")
                h.append(f'<article class="card" aria-labelledby="c{k_card}">{_banderas(o)}'
                         f'<h4 id="c{k_card}">{escape(fx.sin_jerga(o["nombre_llano"]))}</h4>{_subebaja(o)}'
                         f'<p class="porque">{escape(pq)}</p>'
                         f'<div class="fila"><span>Riesgo</span><span><span class="pips" aria-hidden="true">{pips}</span> <b>{r} de 5</b> · {nivel_r[r]}</span></div>'
                         f'<div class="fila"><span>Plazo</span><span class="hz">{hzs}</span></div>'
                         f'<div class="fila"><span>Confianza</span><span><span class="conf" aria-hidden="true">{segs}</span> <b>{tconf}</b>'
                         f'<span class="banda" style="display:block">{escape(hp["banda"].capitalize())} · {escape(cert)}</span></span></div>{graf}'
                         f'<div class="mal"><b>Qué podría salir mal:</b> <span>{escape(mal)}</span></div>'
                         f'<div class="pie-card"><span>{o["opp_id"]}</span></div></article>')
            if d["opciones"]:
                h.append('</div>')
            if len(d["opciones"]) < 3:
                motivo = (red.get("motivos_llanos") or {}).get(c) or (
                    f"Miramos {d['candidatas_analizadas']} ideas. " + ("Ninguna pasó todos los filtros." if not d["opciones"] else "Las demás no pasaron todos los filtros.")
                    + " Preferimos no rellenar el hueco.")
                pre = "<b>¿Por qué no hay más?</b> " if d["opciones"] else ""
                h.append(f'<div class="vacia">{pre}{escape(motivo)}</div>')
        h.append('</section>')
        # Cómo nos fue (frente a no hacer nada: el paseo aleatorio)
        hg = paquete["historial_aciertos"].get("global") or {}
        n, ac = hg.get("n", 0), hg.get("aciertos", 0)
        h.append('<section aria-labelledby="h-hist"><div class="panel"><h2 id="h-hist">Cómo nos fue</h2>'
                 f'<p class="sub">Ideas de las últimas {escape(paquete["historial_aciertos"]["ventana"])} con el plazo ya terminado, frente a no hacer nada.</p>')
        if n:
            pct = round(100 * ac / n)
            ref = round(100 * (hg.get("tasa_esperada_azar") or 0.5))
            nv = min(n, 28)
            okv = round(ac * nv / n)
            mos = "".join('<i class="ok"></i>' if i < okv else "<i></i>" for i in range(nv))
            h.append(f'<div class="historial"><figure style="margin:0"><div class="mosaico" role="img" aria-label="{ac} ideas acertadas y {n - ac} falladas de {n}">{mos}</div>'
                     '<figcaption class="leyenda"><span><i style="background:var(--ok)"></i>Acertada</span><span><i style="background:var(--ko)"></i>Fallada</span></figcaption></figure>'
                     f'<div><p style="font-size:1.15rem;margin-top:0"><b>{ac} de cada {n}</b> ideas acertaron.</p>'
                     f'<div class="barra-h"><div class="rot"><span>Nuestras ideas</span><b>{pct}&nbsp;%</b></div><div class="pista"><div class="relleno" style="width:{pct}%"></div></div></div>'
                     f'<div class="barra-h"><div class="rot"><span>No hacer nada (decir «la moneda no se moverá»)</span><b>{ref}&nbsp;%</b></div><div class="pista"><div class="relleno ref" style="width:{ref}%"></div></div></div>'
                     f'<p class="peq" style="margin-top:10px">{escape(red.get("frase_historial") or "")}</p></div></div>')
        else:
            h.append('<p>Aún no hay ideas con el plazo terminado. Lo veremos en las próximas semanas.</p>')
        h.append('</div></section>')
        glos = (red.get("glosario") or [])[:5]
        if glos:
            h.append('<section aria-labelledby="h-glos"><h2 id="h-glos">Palabras de hoy</h2><dl class="glosario">')
            for gl in glos:
                h.append(f'<div><dt>{escape(gl["termino"])}</dt><dd>{escape(gl["definicion"])}</dd></div>')
            h.append('</dl></section>')
        h.append('<section><div class="aviso" role="note"><span aria-hidden="true" style="font-size:1.4rem">ℹ️</span>'
                 '<div><b>Esto no es una recomendación personal; tu Broker Personal valora si encaja contigo.</b>'
                 '<p class="peq" style="margin-top:6px">Este resumen no conoce tu situación ni tus ahorros. Las monedas pueden moverse mucho '
                 'y puedes perder dinero. Lo que pasó antes no asegura lo que pasará.</p></div></div></section>')
        h.append(f'<footer><span>Informe {paquete["run_id"]}</span><span>Método {paquete["methodology_version"]}</span>'
                 '<span>Bloque A Forex · Robot Investor</span></footer></div></body></html>')
        cab, cuerpo = h[0], "\n".join(h[1:])
        # separa los elementos en línea para que el texto visible no concatene palabras (HT-07 y lectores de pantalla)
        cuerpo = re.sub(r"(</(?:span|b|small|h4|h1|h2|h3|div|dt|dd|li)>)(<)", r"\1 \2", cuerpo)
        return cab + "\n" + cuerpo

    # ------------------------------------------------------------------------------------
    def tecnico(self, paquete: Dict, extras: Dict, g3: Dict, rutas: Dict, estado_run: str, consumo: Dict) -> str:
        p = paquete
        L = [f"# Informe técnico del Bloque A Forex — {_semana_o_peticion(p)}", "",
             "**Bloque A Forex · Robot Investor · Versión V1.0** · Documento 0 del Bloque A Forex V1.0 · Generado por el ejecutor "
             "`bloque_a_forex` V1.0.", "",
             "> El Bloque A Forex delimita ámbitos cambiarios (qué divisa, frente a cuál, por qué y en qué plazo); el instrumento, "
             "el coste, la cobertura y la ejecución corresponden al Bloque B, que recibe el encargo del `paquete_para_bloque_B`.", "",
             "| Campo | Valor |", "|---|---|", f"| Identificador | `{p['run_id']}` |", f"| Tipo | {p['tipo']} |",
             f"| Fecha de referencia | {p['fecha']} |", f"| Datos de mercado al cierre de | {p['fecha_datos_mercado']} |",
             f"| Divisa base del usuario | {p.get('divisa_base_usuario')} |",
             f"| Versión de metodología | {p['methodology_version']} |",
             f"| Informes transversales (CT-06T) | BCM `{(p.get('informes_transversales') or {}).get('BCM')}` · "
             f"PFV `{(p.get('informes_transversales') or {}).get('PFV')}` |",
             f"| Dictamen G3 | {g3.get('dictamen')} {', '.join(g3.get('advertencias', []))} |", f"| Estado del retorno | {estado_run} |",
             f"| Entregables hermanos | `{rutas.get('informe_visual')}` · `{rutas.get('paquete_json')}` |", "",
             "## 1. Resumen ejecutivo", "", f"**Lectura del conjunto.** {p.get('x_lectura_conjunto') or '—'}", "",
             f"**Qué ha cambiado.** {p.get('x_cambios_vs_anterior') or 'Sin ciclo anterior comparable.'}", "",
             f"**Apuestas independientes: {p['apuestas_independientes']}** (N efectivo ML-CLUS-001: {p.get('x_n_efectivo')}).", ""]
        for e in p.get("clusteres_exposicion", []):
            L.append(f"- {e['cluster_id']}: {e['factor_dominante']} — {', '.join(e['opp_ids'])}")
        L += ["", "| Segmento | Semáforo | Opción | RK | Riesgo | Carry | Relevancia | Siguiente paso |", "|---|---|---|---|---|---|---|---|"]
        for c, d in p["segmentos"].items():
            if not d["opciones"]:
                L.append(f"| {c} | {d['estado_semaforo']} | — | — | — | — | — | — |")
            for o in d["opciones"]:
                ca = o.get("carry") or {}
                L.append(f"| {c} | {d['estado_semaforo']} | {o['rango']} · {o['nombre']} · `{o['opp_id']}` | {o['puntuaciones']['RK']} | "
                         f"{o['riesgo_1a5']} | {_fmt_carry(ca)} | {o['relevancia_decisional']} | {o['siguiente_paso_sugerido']} |")
        L += ["", "## 2. Alcance, nivel, presupuesto y consumo", "", "| Segmento | Nivel | GC0 cambio material | Motivos |", "|---|---|---|---|"]
        for c, nv in p["nivel_por_segmento"].items():
            g = extras["gc0"].get(c, {})
            L.append(f"| {c} | {nv} | {'sí' if g.get('cambio_material') else 'no'} | {'; '.join(g.get('motivos', [])) or 'arrastre verificado'} |")
        rc = p.get("regimen_cambiario") or {}
        L += ["", f"Consumo del RUN (hasta la redacción): {consumo.get('llamadas')} llamadas, {consumo.get('uc')} UC "
                  f"(LLM {consumo.get('uc_llm')}, Motor {consumo.get('uc_motor')}); tokens de entrada {consumo.get('entrada')}, "
                  f"salida {consumo.get('salida')}, caché escritura {consumo.get('cache_escritura')}, lectura {consumo.get('cache_lectura')}.", "",
              "## 3. Régimen macro y cambiario y exposición agregada", "", p["regimen_macro"], "",
              f"**Régimen cambiario.** Dólar {rc.get('dolar')} · riesgo {rc.get('riesgo')} · volatilidad {rc.get('volatilidad')}"
              + (f" ({rc['nota']})" if rc.get("nota") else "") + ".", "",
              "| Divisa | Exposición agregada | Neta (opciones equivalentes) |", "|---|---|---|"]
        neta = extras.get("exposicion_neta") or {}
        for dv, v in (p.get("exposicion_agregada") or {}).items():
            L.append(f"| {dv} | {v} | {neta.get(dv, 0):+.2f} |")
        lb = p.get("lectura_divisa_base") or {}
        L += ["", f"**Lectura para la divisa base ({lb.get('divisa')}).** {lb.get('sentido')}: {lb.get('texto_llano')}", ""]
        if p.get("contradicciones_entre_segmentos"):
            L += ["**Contradicciones entre segmentos (9.6.6).**", ""]
            L += [f"- {x['divisa']}: {', '.join(x['opp_ids'])} — {x['justificacion_contradiccion']}" for x in p["contradicciones_entre_segmentos"]]
            L.append("")
        L += ["## 4. Análisis por segmento de divisas", ""]
        for i, (c, d) in enumerate(p["segmentos"].items(), 1):
            emb = d.get("embudo", {})
            L += [f"### 4.{i} {NOMBRE_SEGMENTO[c]} ({c}) — semáforo {d['estado_semaforo']}", "", f"**Régimen.** {d['regimen_segmento']}", "",
                  "| Etapa | Número |", "|---|---|", f"| Candidatas cribadas | {emb.get('cribadas')} |", f"| Pasan GC1 | {emb.get('pasan_gc1')} |",
                  f"| Pasan GC2 | {emb.get('pasan_gc2')} |", f"| Finalistas GC3 | {emb.get('finalistas_gc3')} |",
                  f"| Elegibles | {emb.get('elegibles')} |", f"| En el top-3 | {len(d['opciones'])} |", ""]
            if d.get("menos_de_tres_motivo"):
                L += [f"**Menos de tres (R14).** {d['menos_de_tres_motivo']}", ""]
            for o in d["opciones"]:
                pu = o["puntuaciones"]
                cv = o["convertibilidad"]
                comp = ", ".join(f"{x['divisa']} {x['lado']} {x['peso']:.2f}" for x in o.get("composicion") or []) or "—"
                vista = o.get("vista_volatilidad")
                L += [f"##### {o['rango']}. {o['nombre']} · `{o['opp_id']}`", "",
                      f"- Tipo de opción: {o['tipo_opcion']} · par: {o.get('par') or '—'} · dirección: {o.get('direccion') or '—'}"
                      + (f" · vista de volatilidad: {vista['sentido']} a {vista['plazo']}" if vista else "")
                      + f" · divisa de financiación: {o.get('divisa_financiacion') or '—'}",
                      f"- **Composición.** {comp}" + (f" · {o['sube_baja_llano']}" if o.get("sube_baja_llano") else ""),
                      f"- **Ámbito.** Incluye: {o['ambito']['incluye']} · Excluye: {o['ambito']['excluye']}",
                      f"- **Indicador de seguimiento.** {o['indicador_seguimiento']['nombre']} (`{o['indicador_seguimiento'].get('simbolo')}`, "
                      f"{o['indicador_seguimiento']['fuente']})",
                      f"- **Convertibilidad (PS3).** convertible {'sí' if cv['convertible'] else 'no'} · NDF {'sí' if cv['ndf'] else 'no'} · "
                      f"controles {'sí' if cv['controles_capitales'] else 'no'} · profundidad {cv['profundidad']} · {cv['nota']}",
                      f"- **Carry (FX-CARRY-001).** {_fmt_carry(o.get('carry') or {})}"
                      + (f" · diferencial base − cotizada {o['carry']['diferencial_tipos_pct']:+.2f} %" if (o.get('carry') or {}).get('diferencial_tipos_pct') is not None else "")
                      + (f" · `{o['carry']['calc_id']}`" if (o.get('carry') or {}).get('calc_id') else ""),
                      f"- Clúster: {o.get('cluster_id')} · confianza: {o['confianza']} · relevancia: {o['relevancia_decisional']} · reversibilidad: {o['reversibilidad']} · liquidez: {o['liquidez']}"
                      + (f" · régimen de la divisa: {o['regimen_cambiario_divisa']}" if o.get("regimen_cambiario_divisa") else ""),
                      f"- **Naturaleza de la inversión y horizonte principal (8.3).** {o.get('naturaleza_inversion') or '—'} · "
                      f"**{o.get('horizonte_principal')}**" + (f" · justificación: {o['justificacion_horizonte']}" if o.get("justificacion_horizonte") else "")
                      + (f" · ámbito H5: {o['ambito_h5']}" if o.get("ambito_h5") else ""),
                      f"- **Siguiente paso sugerido: {o['siguiente_paso_sugerido']}**", "",
                      f"**Tesis.** {o['tesis']}", "", f"**Mecanismo.** {o['mecanismo']}", "", f"**Valoración.** {o['valoracion']}", "",
                      f"**Puntuaciones (HT-03, `{pu['desglose_ref']}`).** T {pu['T']} · E {pu['E']} · M {pu.get('M')} · A {pu['A']} · RK {pu['RK']}", "",
                      "| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |",
                      "|---|---|---|---|---|---|---|---|"]
                for hh, v in o["horizontes"].items():
                    L.append(f"| {hh} | {v['vista']} | {v['banda'] if v['prob'] is None else v['prob']} | {'sí' if v['certificado_r13'] else v.get('etiqueta')} | "
                             f"{v.get('referencia')} | {v.get('tipo_rentabilidad')} en {v.get('divisa_medicion')} | "
                             f"`{v['prg_id']}` | {v.get('fecha_resolucion')} — {v.get('criterio_resolucion')} |")
                if (o["horizontes"].get("H5") or {}).get("hitos"):
                    L += ["", "**Hitos H5 (HIT-FX-, se evalúan en su fecha frente al paseo aleatorio).** "
                          + "; ".join(f"`{x.get('hit_id')}` {x['fecha']}: {x['criterio']}" for x in o["horizontes"]["H5"]["hitos"])]
                L += ["", f"**Catalizadores.** {'; '.join(x['evento'] + ' (' + x['fecha'] + ')' for x in o['catalizadores']) or '—'}", "",
                      f"**Riesgos.** {'; '.join(o['riesgos'])} — riesgo sintético **{o['riesgo_1a5']}/5** (RISK-DD-001 v2.0).", "",
                      f"**Invalidación.** {'; '.join(o['invalidacion'])}", "", f"**Qué cambiaría la conclusión.** {'; '.join(o['que_cambiaria_la_conclusion'])}", "",
                      f"**Lo que no sabemos.** {'; '.join(o['lo_que_no_sabemos'])}", ""]
                b = next((x for x in p.get("paquete_para_bloque_B", []) if x.get("opp_id") == o["opp_id"]), None)
                if b:
                    niv = "; ".join(f"{k}: {v['valor']:.6g} ({v['fecha_dato']}, {v['hora_fijacion']})" for k, v in (b.get("niveles_referencia") or {}).items())
                    L += [f"**Encargo para el Bloque B.** Consideraciones de implementación: {'; '.join(b['consideraciones_implementacion'])}. "
                          f"Carry esperado: {_fmt_carry(b['carry_esperado'])}. Niveles de referencia: {niv or '—'}. "
                          f"Métricas clave: {'; '.join(b['metricas_clave'])}. Preguntas: {' '.join(b['preguntas_para_B'])}", ""]
                L += [f"**Evidencia y cálculos.** {', '.join(o['evidencias'])} · {', '.join(o['calculos'])}", ""]
        L += ["## 5. Seguimiento de opciones vigentes", "", "| OPP | Estado | Decisión del Broker | Comentario |", "|---|---|---|---|"]
        for s_ in p["seguimiento_vigentes"]:
            L.append(f"| `{s_['opp_id']}` | {s_['estado']} {s_.get('motivo_cierre') or ''} | {s_.get('decision_broker') or '—'} | {s_['comentario']} |")
        L += ["", "## 6. Objeciones y respuestas", "", "| OPP | Fuerza | Objeción | Respuesta | Estado |", "|---|---|---|---|---|"]
        for d in p["segmentos"].values():
            for o in d["opciones"]:
                for ob in o["objeciones"]:
                    L.append(f"| `{o['opp_id']}` | {ob['fuerza']} | {ob['resumen']} | {ob.get('respuesta') or '—'} | {ob['estado']} |")
        L += ["", "## 7. Limitaciones, lagunas y qué no sabemos", ""] + [f"- {x}" for x in p["limitaciones"]]
        if p.get("supuestos_declarados"):
            L += ["", "**Supuestos declarados (consultas al Broker sin respuesta, CT-23).**", ""] + [
                f"- {s_['supuesto']} (`{s_.get('cns_id') or '—'}`); si fuera falso: {s_['efecto_si_falso']}" for s_ in p["supuestos_declarados"]]
        hg = p["historial_aciertos"]
        L += ["", "## 8. Historial de aciertos (Evaluador)", "",
              f"Ventana: **{hg['ventana']}**. Referencia: {hg.get('referencia', 'paseo aleatorio y forward')}. {hg.get('nota', '')}", "",
              "| Ámbito | n | Aciertos | Tasa | Paseo aleatorio | Forward | Significativo |", "|---|---|---|---|---|---|---|"]
        for k, v in [("Global", hg.get("global") or {})] + list(hg.get("por_segmento", {}).items()):
            L.append(f"| {k} | {v.get('n')} | {v.get('aciertos')} | {v.get('tasa_acierto')} | {v.get('tasa_esperada_azar')} | "
                     f"{v.get('tasa_forward')} | {v.get('significativo')} |")
        L += ["", "## 9. Preguntas sugeridas", ""] + [f"- {x}" for x in p["preguntas_sugeridas"]]
        L += ["", f"*{p['aviso_legal']}*", ""]
        return "\n".join(L)

    # ------------------------------------------------------------------------------------
    def generar(self, bloque, paquete: Dict, extras: Dict, red: Dict, as_of, run_id: str, estado_run: str) -> Tuple[Dict, Dict]:
        from . import sintesis as sint
        as_of = pd.Timestamp(as_of)
        tarj = {t.get("opp_id"): t for t in red.get("tarjetas", []) if isinstance(t, dict)}
        for d in paquete["segmentos"].values():
            for o in d["opciones"]:
                t = tarj.get(o["opp_id"], {})
                o["por_que_llano"] = (t.get("por_que_llano") or "El sistema ve señales a favor de esta idea.")[:160]
                o["que_puede_salir_mal_llano"] = (t.get("que_puede_salir_mal_llano") or "El precio puede bajar más de lo previsto.")[:200]
        paquete["x_estado_run"] = estado_run
        fecha = str(as_of.date())
        if bloque.modo == "backtest":
            base = bloque.carpeta_entregables / fecha
            dirs = {"informe_tecnico": base, "informe_visual": base, "paquete_json": base}
        else:
            base = bloque.carpeta_entregables
            dirs = {"informe_tecnico": base / "Informes técnicos Broker", "informe_visual": base / "Informes visuales Usuario",
                    "paquete_json": base / "Paquetes JSON"}
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        rutas = {"informe_tecnico": str(dirs["informe_tecnico"] / f"{fecha}_informe-tecnico_{run_id}.md"),
                 "informe_visual": str(dirs["informe_visual"] / f"{fecha}_informe-visual_{run_id}.html"),
                 "paquete_json": str(dirs["paquete_json"] / f"{fecha}_paquete-json_{run_id}.json")}
        Path(rutas["informe_visual"]).write_text(self.visual(bloque, paquete, red, as_of), encoding="utf-8")
        leg = ht07.analizar(Path(rutas["informe_visual"]).read_text(encoding="utf-8"), es_html=True)
        res = sint.ht09_validar(bloque, paquete, extras, rutas["informe_visual"])
        bloq = [c["id"] for c in res["comprobaciones"] if c["resultado"] == "BLOQUEO"]
        adv = [c["id"] for c in res["comprobaciones"] if c["resultado"] == "ADVERTENCIA"]
        dictamen = "BLOQUEADO" if bloq else ("APTO_CON_ADVERTENCIAS" if adv else "APTO")
        paquete["estado_g3"] = dictamen if dictamen != "BLOQUEADO" else "APTO_CON_ADVERTENCIAS"
        js = entregable_json(paquete)
        if dictamen == "BLOQUEADO":
            js.pop("estado_g3", None)
        esquema = json.loads(self.esquema_json.read_text(encoding="utf-8"))
        errores = [f"{'/'.join(map(str, e.absolute_path))}: {e.message}"[:200]
                   for e in jsonschema.Draft202012Validator(esquema).iter_errors(js)][:10]
        Path(rutas["paquete_json"]).write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding="utf-8")
        g3 = {"dictamen": dictamen, "advertencias": adv}
        cons = bloque.contabilidad.resumen(run_id)
        Path(rutas["informe_tecnico"]).write_text(self.tecnico(paquete, extras, g3, rutas, estado_run, cons), encoding="utf-8")
        coh = coherencia(rutas, js)
        if errores:
            bloq.append("ESQUEMA_JSON")
        if coh:
            bloq.append("COHERENCIA_ENTREGABLES")
        dictamen = "BLOQUEADO" if bloq else dictamen
        bloque.almacen.escribir("HA", "AG-18", {"tipo_entrada": "G3V", "id": f"G3V-{run_id[4:]}-F7", "run_id": run_id, "fase": "F7",
                                                "tipo_control": "SINCRONO_DETERMINISTA", "dictamen_ht09": res["dictamen"], "dictamen_efectivo": dictamen,
                                                "legibilidad": {"fernandez_huerta": leg["fernandez_huerta"], "pct_frases_mas_de_20": leg["pct_frases_mas_de_20"],
                                                                "jerga_sin_explicar": leg["jerga_sin_explicar"]},
                                                "errores_esquema": errores, "incoherencias": coh,
                                                "comprobaciones": [{"id": c["id"], "resultado": c["resultado"], "detalle": [i["detalle"] for i in c["incidencias"]][:5]}
                                                                   for c in res["comprobaciones"]]})
        return rutas, {"dictamen": dictamen, "bloqueos": bloq, "advertencias": adv, "legibilidad": leg["fernandez_huerta"],
                       "frases_largas": leg["frases_largas"][:10], "errores_esquema": errores, "incoherencias": coh}


def _numero(n: int) -> str:
    return {1: "un", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis"}.get(n, str(n))


def _fmt_carry(ca: Dict) -> str:
    if not ca or ca.get("anual_pct") is None:
        return ca.get("signo", "no aplicable") if ca else "—"
    return f"{ca['anual_pct']:+.2f} % anual ({ca['signo']})"


def _banderas(o: Dict) -> str:
    comp = o.get("composicion") or []
    if o.get("tipo_opcion") == "VOLATILIDAD":
        par = str(o.get("par") or "")
        divs = [d for d in par.split("/") if d]
        fl = "".join(f'<span role="img" aria-label="{escape(fx.llano(d, False))}">{fx.bandera(d)}</span>' for d in divs)
        return f'<div class="flags">{fl}<span role="img" aria-label="Movimientos del cambio">📈</span></div>'
    largos = [c["divisa"] for c in comp if c["lado"] == "LARGO"]
    cortos = [c["divisa"] for c in comp if c["lado"] == "CORTO"]

    def grupo(ds):
        if len(ds) == 1:
            return f'<span role="img" aria-label="{escape(fx.llano(ds[0], False))}">{fx.bandera(ds[0])}</span>'
        return (f'<span role="img" aria-label="{escape(", ".join(fx.llano(d, False) for d in ds))}">'
                f'{"".join(fx.bandera(d) for d in ds)}</span>')
    cesta = '<span role="img" aria-label="Grupo de monedas">🧺</span>' if len(comp) > 2 else ""
    return f'<div class="flags">{cesta}{grupo(largos)}<span class="vs" aria-hidden="true">frente a</span>{grupo(cortos)}</div>'


def _subebaja(o: Dict) -> str:
    if o.get("tipo_opcion") == "VOLATILIDAD":
        v = (o.get("vista_volatilidad") or {}).get("sentido", "ALZA")
        return (f'<div class="subebaja"><span class="{"s" if v == "ALZA" else "b"}">{"▲ Suben" if v == "ALZA" else "▼ Bajan"} '
                f'los movimientos de {escape(str(o.get("par") or ""))}</span></div>')
    comp = o.get("composicion") or []
    sube = [fx.llano(c["divisa"]) for c in comp if c["lado"] == "LARGO"][:3]
    baja = [fx.llano(c["divisa"]) for c in comp if c["lado"] == "CORTO"][:3]

    def lista(xs):
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]
    if not sube or not baja:
        return ""
    return (f'<div class="subebaja"><span class="s">▲ {"Sube" if len(sube) == 1 else "Suben"} {escape(lista(sube))}</span>'
            f'<span class="b">▼ {"Baja" if len(baja) == 1 else "Bajan"} {escape(lista(baja))}</span></div>')


def _spark(bloque, o: Dict, as_of, id_svg: str) -> str:
    """Minigráfico de un año del indicador con la flecha punteada de la dirección esperada (HT-04)."""
    try:
        s = bloque.proveedor.cierres(o["indicador_seguimiento"]["simbolo"], pd.Timestamp(as_of) - pd.Timedelta(days=370), as_of)
    except Exception:
        return ""
    vals = [float(x) for x in s.values]
    if len(vals) < 5:
        return ""
    sube = bool(o.get("x_indicador_sube", True))
    lo, hi = min(vals), max(vals)
    rango = (hi - lo) or 1.0
    lo, hi = lo - 0.15 * rango, hi + 0.15 * rango
    pts, (xh, yh) = ht04.puntos_polyline(vals, ancho=254, vmin=lo, vmax=hi)
    y2 = max(min(yh + (-22 if sube else 22), 64), 6)
    cl = "s" if sube else "b"
    nombre = fx.sin_jerga(o["indicador_seguimiento"]["nombre"])
    alt = f"{nombre} en un año y dirección esperada: {'sube' if sube else 'baja'}"
    return (f'<figure class="spark"><svg viewBox="0 0 280 72" role="img" aria-labelledby="{id_svg}"><title id="{id_svg}">{escape(alt)}</title>'
            f'<polyline class="linea" points="{pts}"/><line class="flecha {cl}" x1="{xh}" y1="{yh}" x2="272" y2="{y2}"/>'
            f'<circle class="punta {cl}" cx="272" cy="{y2}" r="4"/></svg>'
            f'<figcaption>Un año del indicador. La línea punteada: lo que esperamos.</figcaption></figure>')


def _semana_o_peticion(p: Dict) -> str:
    if p["tipo"] == "PERIODICO":
        f = pd.Timestamp(p["fecha"])
        return f"Semana {f.isocalendar()[1]} de {f.isocalendar()[0]}"
    return f"Informe a petición del {p['fecha']}"


def coherencia(rutas: Dict, js: Dict) -> List[str]:
    """Mismas OPP-, orden y RK en el JSON, el informe técnico y el informe visual (G3-ENT-07)."""
    orden_js = [o["opp_id"] for d in js["segmentos"].values() for o in d["opciones"]]
    rk_js = {o["opp_id"]: o["puntuaciones"]["RK"] for d in js["segmentos"].values() for o in d["opciones"]}
    md = Path(rutas["informe_tecnico"]).read_text(encoding="utf-8")
    html = Path(rutas["informe_visual"]).read_text(encoding="utf-8")
    orden_md = re.findall(r"^##### \d+\. .*· `(OPP-FX-\d{4}-\d+)`", md, re.M)
    orden_html = re.findall(r'<div class="pie-card"><span>(OPP-FX-\d{4}-\d+)</span>', html)
    out = []
    if orden_md != orden_js:
        out.append(f"orden del informe técnico {orden_md} ≠ JSON {orden_js}")
    if orden_html != orden_js:
        out.append(f"orden del informe visual {orden_html} ≠ JSON {orden_js}")
    for oid, rk in rk_js.items():
        if f"· `{oid}` | {rk} |" not in md:
            out.append(f"RK de {oid} distinto en el informe técnico")
    return out
