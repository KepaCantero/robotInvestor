"""Redacción de entregables (F7): informe técnico (Markdown), informe visual (HTML autocontenido a partir de la
plantilla vigente del informe visual, con gráficos SVG de HT-04) y paquete JSON conforme al esquema vigente
(Documento 0 óptima V5.0: doce tipos de activo; ámbitos, indicador de seguimiento y encargo para el Bloque B; sin
vehículos). Las plantillas se localizan por su nombre con cualquier sufijo de versión. Después, HT-07 sobre el
informe visual y segunda pasada de HT-09 con coherencia entre los tres entregables."""
from __future__ import annotations

import copy
import json
import re
from html import escape
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import jsonschema
import pandas as pd

from .configuracion import NOMBRE_CLASE, buscar_versionado, ruta
from .herramientas import ht04_graficos as ht04
from .herramientas import ht07

# Nombres llanos, subtítulo (explica el nombre la primera vez), icono y clase CSS de los doce tipos (plantilla V5.0)
LLANO = {"RV": ("Acciones", "empresas de un sector o tema", "#i-rv", "k-rv"),
         "RF": ("Bonos", "préstamos a Estados y empresas", "#i-rf", "k-rf"),
         "DIV": ("Monedas", "euro, dólar, yen…", "#i-div", "k-div"),
         "MP": ("Materias primas", "oro, petróleo, trigo…", "#i-mp", "k-mp"),
         "IDX": ("Bolsas enteras", "la bolsa de un país o zona", "#i-idx", "k-idx"),
         "FON": ("Fondos", "dinero de muchos, invertido junto", "#i-fon", "k-fon"),
         "DER": ("Derivados", "contratos ligados a otro precio", "#i-der", "k-der"),
         "INM": ("Inmuebles", "empresas de casas y locales en bolsa", "#i-inm", "k-inm"),
         "CRI": ("Criptomonedas", "monedas digitales", "#i-cri", "k-cri"),
         "ALT": ("Alternativas", "empresas que no cotizan, arte…", "#i-alt", "k-alt"),
         "MON": ("Ahorro a corto plazo", "letras del Tesoro y depósitos", "#i-mon", "k-mon"),
         "TCV": ("Tipos y nervios del mercado", "interés, crédito y sustos", "#i-tcv", "k-tcv")}
# Frase fija de la frontera con el Bloque B (plantilla V5.0)
FRASE_BLOQUE_B = "Después, otro equipo del sistema estudiará cada idea a fondo para encontrar las mejores inversiones concretas."
AMBITO_LLANO_DEFECTO = "Una zona del mercado, no un producto concreto."
REG_NOMBRE = {"NAM": "Norteamérica", "LAT": "Latinoamérica", "EUR": "Europa", "AFR": "África", "ORM": "Oriente Medio", "CHN": "China",
              "ASE": "Asia emergente", "JPN": "Japón", "OCE": "Oceanía", "GLB": "Global (sin región)"}
# Rectángulos del cartograma de la plantilla (versión escritorio)
REG_RECT = {"NAM": (10, 10, 208, 96), "LAT": (64, 114, 154, 200), "EUR": (226, 10, 208, 96), "AFR": (226, 114, 100, 200),
            "ORM": (334, 114, 100, 96), "CHN": (442, 10, 100, 96), "JPN": (550, 10, 100, 96), "ASE": (442, 114, 208, 96),
            "OCE": (550, 218, 100, 96), "GLB": (334, 218, 208, 96)}
CAMPOS_OPCION_SOLO_SINTESIS = ("puertas", "cluster", "vigente")
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_larga(f) -> str:
    f = pd.Timestamp(f)
    return f"{DIAS[f.weekday()]}, {f.day} de {MESES[f.month - 1]} de {f.year}"


def entregable_json(paquete: dict) -> dict:
    p = copy.deepcopy(paquete)
    for d in p["clases"].values():
        for o in d["opciones"]:
            for k in CAMPOS_OPCION_SOLO_SINTESIS:
                o.pop(k, None)
            for h in o["horizontes"].values():
                h.pop("advertencia", None)
                h.pop("metodo", None)
            for ob in o["objeciones"]:
                ob.pop("resuelta", None)
            for k in ("por_que_llano", "que_puede_salir_mal_llano"):
                if k in o and not o[k]:
                    o.pop(k)
    return p


class Redaccion:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        base = ruta(cfg, "plantillas")
        # Se localizan por nombre con cualquier sufijo de versión («… - V4.0», «… - V5.0», …): gana la más alta
        self.plantilla_html = (buscar_versionado(base, "Plantilla - Informe visual para el usuario", ".html")
                               or base / "Plantilla - Informe visual para el usuario - V5.0.html")
        self.esquema_json = (buscar_versionado(base, "Esquema JSON - Paquete de oportunidades", ".json")
                             or base / "Esquema JSON - Paquete de oportunidades - V5.0.json")

    # ------------------------------------------------------------------------------------
    def textos_por_defecto(self, paquete: dict) -> dict:
        n = sum(len(d["opciones"]) for d in paquete["clases"].values())
        nc = sum(1 for d in paquete["clases"].values() if d["opciones"])
        return {"frases_30s": [f"Esta semana vemos {n} ideas en {nc} tipos de inversión.",
                               "Cada idea tiene su riesgo y su plazo.", "Nada de esto es un consejo para ti."],
                "tarjetas": [{"opp_id": o["opp_id"], "por_que_llano": "El sistema ve señales a favor de esta idea.",
                              "que_puede_salir_mal_llano": "El precio puede bajar más de lo previsto.",
                              "ambito_llano": AMBITO_LLANO_DEFECTO}
                             for d in paquete["clases"].values() for o in d["opciones"]],
                "motivos_llanos": {}, "glosario": [], "frase_historial": "Aún hay pocos casos para saber si acertamos más que el azar."}

    # ------------------------------------------------------------------------------------
    def _cabecera_plantilla(self) -> str:
        t = self.plantilla_html.read_text(encoding="utf-8")
        i = t.find('<div class="ejemplo"')
        cab = t[:i] if i > 0 else t[:t.find("<body>") + 6]
        return cab.replace('lang="es-ES"', f'lang="{self.cfg.get("idioma", "es-ES")}"')

    def visual(self, bloque, paquete: dict, red: dict, as_of) -> str:
        tarj = {t["opp_id"]: t for t in red.get("tarjetas", [])}
        clases = paquete["clases"]
        n_tot = sum(len(d["opciones"]) for d in clases.values())
        n_cl = sum(1 for d in clases.values() if d["opciones"])
        frases = (red.get("frases_30s") or [])[:3]
        h = [self._cabecera_plantilla(), '<div class="wrap">']
        h.append(f'<header class="top"><div><div class="marca">Robot Investor · tu resumen de ideas</div>'
                 f'<h1>{escape(_semana_o_peticion(paquete))}</h1><p class="sub">Lo que el sistema ha visto, explicado sin jerga.</p></div>'
                 f'<div class="meta"><div>{escape(fecha_larga(as_of).capitalize())}</div>'
                 f'<div>Datos de mercado del {escape(fecha_larga(paquete["fecha_datos_mercado"]))}</div></div></header>')
        if paquete.get("x_estado_run") == "PARCIAL":
            h.append('<div class="vacia" role="note"><b>Informe parcial.</b> Algunas partes no se pudieron completar. Lo decimos para que lo tengas en cuenta.</div>')
        h.append('<section aria-labelledby="h-30"><div class="panel"><h2 id="h-30">La semana en 30 segundos</h2><ol class="treinta">')
        for i, f in enumerate(frases):
            h.append(f'<li><span class="num" aria-hidden="true">{i + 1}</span><span>{escape(f)}</span></li>')
        h.append(f'</ol><div class="cifras"><div class="cifra"><b>{n_tot}</b><span>ideas</span></div>'
                 f'<div class="cifra"><b>{n_cl} de {len(clases)}</b><span>tipos con ideas</span></div>'
                 f'<div class="cifra"><b>{paquete["apuestas_independientes"]}</b><span>apuestas distintas</span></div></div></div></section>')
        # Cartograma
        cuenta = {r: 0 for r in REG_RECT}
        for d in clases.values():
            for o in d["opciones"]:
                for r in o["regiones"]:
                    cuenta[r] = cuenta.get(r, 0) + 1
        alt = ", ".join(f"{REG_NOMBRE[r]} {n}" for r, n in cuenta.items() if n) or "Ninguna zona con ideas"
        g = []
        for r, (x, y, w, hh) in REG_RECT.items():
            n = cuenta[r]
            g.append(f'<g class="t n{min(n, 3)}{" glb" if r == "GLB" else ""}"><rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="12"/>'
                     f'<text class="rn" x="{x + (9 if r == "ORM" else 14)}" y="{y + 24}">{REG_NOMBRE[r].replace(" (sin región)", "")}</text>'
                     f'<text class="rc" x="{x + 14}" y="{y + 78}">{n}</text></g>')
        # Semáforo de los tipos de activo (doce por defecto, en el orden de la tabla 2.6)
        h.append(f'<section aria-labelledby="h-sem"><div class="panel"><h2 id="h-sem">Semáforo de los {len(clases)} tipos de inversión</h2>'
                 '<p class="peq">Verde: hay ideas claras. Ámbar: pocas o dudosas. Gris: nada que destacar.</p><ul class="sem">')
        txt_sem = {"VERDE": ("verde", "Claras"), "AMBAR": ("ambar", "Dudosas"), "GRIS": ("gris", "Nada")}
        for c, d in clases.items():
            nom, peq, ico, k = LLANO[c]
            cl, tx = txt_sem[d["estado_semaforo"]]
            h.append(f'<li><span class="ico {k}" aria-hidden="true"><svg><use href="{ico}"/></svg></span>'
                     f'<span class="nom">{nom} <small>({peq})</small></span>'
                     f'<span class="estado {cl}"><svg aria-hidden="true"><use href="#s-{cl}"/></svg>{tx} · {len(d["opciones"])}</span></li>')
        h.append('</ul></div></section>')
        # Mapa + qué pasa después (frontera con el Bloque B)
        h.append('<section class="duo"><div class="panel carto" aria-labelledby="h-mapa"><h2 id="h-mapa">Dónde las hemos visto</h2>'
                 '<p class="peq">Cada casilla es una zona del mundo. Más azul, más ideas.</p>'
                 f'<svg viewBox="0 0 660 340" role="img" aria-labelledby="mapa-t mapa-d"><title id="mapa-t">Mapa de zonas con ideas</title>'
                 f'<desc id="mapa-d">{escape(alt)}</desc>{"".join(g)}</svg></div>')
        h.append('<div class="panel" aria-labelledby="h-despues"><h2 id="h-despues">Qué pasa después</h2>'
                 '<p class="peq">Este informe señala zonas del mercado, no productos para comprar.</p><ol class="pasos">'
                 '<li class="aqui"><span class="num" aria-hidden="true">1</span><span><b>Buscamos dónde hay buenas ideas</b>'
                 'Un sector, un país, un grupo de bonos o una forma de invertir con buenas perspectivas.</span></li>'
                 '<li><span class="num" aria-hidden="true">2</span><span><b>Otro equipo elige qué comprar</b>'
                 f'{escape(FRASE_BLOQUE_B)}</span></li>'
                 '<li><span class="num" aria-hidden="true">3</span><span><b>Tu Broker decide contigo</b>'
                 'Tu Broker Personal mira si alguna idea encaja con tus metas y tu riesgo.</span></li></ol></div></section>')
        # Tarjetas
        h.append('<section aria-labelledby="h-ideas"><h2 id="h-ideas">Las ideas, una a una</h2>'
                 '<p class="sub">Riesgo de 1 (muy bajo) a 5 (muy alto). La barra azul dice cuánto confiamos.</p>'
                 '<div class="nota-b" role="note"><svg aria-hidden="true"><use href="#i-equipo"/></svg>'
                 f'<span>Cada idea es una zona del mercado. {escape(FRASE_BLOQUE_B)}</span></div>')
        nivel_r = {1: "muy bajo", 2: "bajo", 3: "medio", 4: "alto", 5: "muy alto"}
        conf = {"establecido": (3, "Alta"), "probable": (2, "Media"), "especulativo": (1, "Baja"), "en disputa": (1, "Baja")}
        hz_ico = [("H1", "dias", "días"), ("H2", "semanas", "semanas"), ("H3", "meses", "meses"), ("H4", "anos", "años"),
                  ("H5", "decadas", "décadas")]      # V5.1: H5 décadas; el horizonte principal se destaca
        k_card = 0
        orden = [c for c in clases if clases[c]["opciones"]] + [c for c in clases if not clases[c]["opciones"]]
        for c in orden:
            d = clases[c]
            nom, _, ico, k = LLANO[c]
            cl, tx = txt_sem[d["estado_semaforo"]]
            h.append(f'<div class="clase-h"><span class="ico {k}" aria-hidden="true"><svg><use href="{ico}"/></svg></span><h3>{nom}</h3>'
                     f'<span class="estado {cl}"><svg aria-hidden="true"><use href="#s-{cl}"/></svg>{tx}</span></div>')
            if d["opciones"]:
                h.append('<div class="tarjetas">')
            for o in d["opciones"]:
                k_card += 1
                t = tarj.get(o["opp_id"], {})
                pq = o.get("por_que_llano") or t.get("por_que_llano") or "El sistema ve señales a favor de esta idea."
                mal = o.get("que_puede_salir_mal_llano") or t.get("que_puede_salir_mal_llano") or "El precio puede bajar."
                amb = (t.get("ambito_llano") or AMBITO_LLANO_DEFECTO)[:160]
                r = o["riesgo_1a5"]
                pips = "".join('<i class="on"></i>' if i < r else "<i></i>" for i in range(5))
                hzs = " ".join(f'<span{" class=\"on\"" if hh in o["horizontes"] else ""}'
                               f'{" aria-current=\"true\"" if hh == o["horizonte_principal"] else ""}><svg aria-hidden="true">'
                               f'<use href="#i-{ic}"/></svg>{"<b>" + tx_ + "</b>" if hh == o["horizonte_principal"] else tx_}</span>'
                               for hh, ic, tx_ in hz_ico if hh != "H5" or "H5" in o["horizontes"])
                nconf, tconf = conf[o["confianza"]]
                segs = "".join('<i class="on"></i>' if i < nconf else "<i></i>" for i in range(3))
                hp = o["horizontes"][o["horizonte_principal"]]
                cert = hp["etiqueta"] if not hp["certificado_r13"] else f"en {round(hp['prob'] * 10)} de cada 10 casos parecidos acertamos"
                graf = ""
                try:
                    s = bloque.proveedor.cierres(o["indicador_seguimiento"]["simbolo"], pd.Timestamp(as_of) - pd.Timedelta(days=370), as_of)
                    z = o["minigrafico"]["zona_interes"]
                    graf = ht04.minigrafico_precio(list(s.values), (z["min"], z["max"]),
                                                   "Nivel de su indicador en el último año y franja de la zona de interés.",
                                                   "Cómo ha ido en un año. La franja azul es la zona de interés.", f"g{k_card}t")
                except Exception:
                    graf = ""
                h.append(f'<article class="card" aria-labelledby="c{k_card}"><div class="cab"><span class="ico {k}" aria-hidden="true">'
                         f'<svg><use href="{ico}"/></svg></span><div><h4 id="c{k_card}">{escape(o["nombre_llano"])}</h4></div></div>'
                         f'<p class="porque">{escape(pq)}</p>'
                         f'<p class="ambito"><b>Qué abarca:</b> <span>{escape(amb)}</span></p>'
                         f'<div class="fila"><span>Riesgo</span> <span><span class="pips" aria-hidden="true">{pips}</span> <span class="nivel"><b>{r} de 5</b> · {nivel_r[r]}</span></span></div>'
                         f'<div class="fila apilada"><span>Plazo</span> <span class="hz">{hzs}</span></div>'
                         f'<div class="fila"><span>Confianza</span> <span><span class="conf" aria-hidden="true">{segs}</span> <b>{tconf}</b>'
                         f'<div class="banda">{escape(hp["banda"].capitalize())} · {escape(cert)}</div></span></div>{graf}'
                         f'<div class="mal"><svg aria-hidden="true"><use href="#i-alerta"/></svg><span><b>Qué podría salir mal:</b> {escape(mal)}</span></div>'
                         f'<div class="pie-card"><span>{o["opp_id"]}</span></div></article>')
            if len(d["opciones"]) < 3:
                motivo = (red.get("motivos_llanos") or {}).get(c) or (
                    f"Miramos {d['candidatas_analizadas']} ideas. " + ("Ninguna pasó todos los filtros." if not d["opciones"] else "Las demás no pasaron todos los filtros.")
                    + " Preferimos no rellenar el hueco.")
                pre = "<b>¿Por qué no hay más?</b> " if d["opciones"] else ""
                h.append(f'<div class="vacia">{pre}{escape(motivo)}</div>')
            if d["opciones"]:
                h.append('</div>')
        h.append('</section>')
        # Cómo nos fue
        hg = paquete["historial_aciertos"].get("global") or {}
        n, ac = hg.get("n", 0), hg.get("aciertos", 0)
        h.append('<section aria-labelledby="h-hist"><div class="panel"><h2 id="h-hist">Cómo nos fue</h2>'
                 f'<p class="sub">Ideas de las últimas {escape(paquete["historial_aciertos"]["ventana"])} con el plazo ya terminado.</p>')
        if n:
            pct = round(100 * ac / n)
            ref = round(100 * (hg.get("tasa_esperada_azar") or 0.5))
            h.append(f'<div class="historial"><figure class="mosaico" style="margin:0">{ht04.mosaico_aciertos(ac, n)}'
                     '<figcaption class="leyenda"><span><i style="background:var(--ok)"></i>Acertada</span><span><i style="background:var(--ko)"></i>Fallada</span></figcaption></figure>'
                     f'<div><p style="font-size:1.2rem;margin-top:0"><b>{ac} de cada {n}</b> ideas acertaron.</p><div class="barras">'
                     f'<div class="barra"><div class="rotulo"><span>Nuestras ideas</span><b>{pct}&nbsp;%</b></div><div class="pista"><div class="relleno" style="width:{pct}%"></div></div></div>'
                     f'<div class="barra"><div class="rotulo"><span>Acertar por azar</span><b>{ref}&nbsp;%</b></div><div class="pista"><div class="relleno ref" style="width:{ref}%"></div></div></div>'
                     f'</div><p class="peq" style="margin-top:12px">{escape(red.get("frase_historial") or "")}</p></div></div>')
        else:
            h.append('<p>Aún no hay ideas con el plazo terminado. Lo veremos en las próximas semanas.</p>')
        h.append('</div></section>')
        glos = (red.get("glosario") or [])[:5]
        if glos:
            h.append('<section aria-labelledby="h-glos"><h2 id="h-glos">Palabras de hoy</h2><dl class="glosario">')
            for gl in glos:
                h.append(f'<div><dt>{escape(gl["termino"])}</dt><dd>{escape(gl["definicion"])}</dd></div>')
            h.append('</dl></section>')
        h.append('<section><div class="aviso" role="note"><svg aria-hidden="true"><use href="#i-info"/></svg>'
                 '<div><b>Esto no es una recomendación personal; tu Broker Personal valora si encaja contigo.</b>'
                 '<p class="peq" style="margin-top:6px">Este resumen no conoce tu situación ni tus ahorros. Invertir puede hacerte perder dinero. '
                 'Lo que pasó antes no asegura lo que pasará.</p></div></div></section>')
        h.append(f'<footer><span>Informe {paquete["run_id"]}</span><span>Método {paquete["methodology_version"]}</span>'
                 '<span>Bloque A · Robot Investor</span></footer></div></body></html>')
        cab, cuerpo = h[0], "\n".join(h[1:])
        # separa los elementos en línea para que el texto visible no concatene palabras (HT-07 y lectores de pantalla)
        cuerpo = re.sub(r"(</(?:span|b|small|h4|h1|h2|h3|div|dt|dd|li)>)(<)", r"\1 \2", cuerpo)
        return cab + "\n" + cuerpo

    # ------------------------------------------------------------------------------------
    def tecnico(self, paquete: dict, extras: dict, g3: dict, rutas: dict, estado_run: str, consumo: dict) -> str:
        p = paquete
        L = [f"# Informe técnico del Bloque A — {_semana_o_peticion(p)}", "",
             "**Bloque A · Robot Investor · Versión óptima V5.0** · Documento 0 óptima V5.0 · Generado por el Ejecutor programático V1.1.", "",
             "> El Bloque A delimita ámbitos de inversión (dónde, por qué y cuándo); la selección de activos concretos "
             "corresponde al Bloque B, que recibe el encargo de la sección 4 y del `paquete_para_bloque_B`.", "",
             "| Campo | Valor |", "|---|---|", f"| Identificador | `{p['run_id']}` |", f"| Tipo | {p['tipo']} |",
             f"| Fecha de referencia | {p['fecha']} |", f"| Datos de mercado al cierre de | {p['fecha_datos_mercado']} |",
             f"| Versión de metodología | {p['methodology_version']} |",
             f"| Dictamen G3 | {g3.get('dictamen')} {', '.join(g3.get('advertencias', []))} |", f"| Estado del retorno | {estado_run} |",
             f"| Entregables hermanos | `{rutas.get('informe_visual')}` · `{rutas.get('paquete_json')}` |", "",
             "## 1. Resumen ejecutivo", "", f"**Lectura del conjunto.** {p.get('x_lectura_conjunto') or '—'}", "",
             f"**Qué ha cambiado.** {p.get('x_cambios_vs_anterior') or 'Sin ciclo anterior comparable.'}", "",
             f"**Apuestas independientes: {p['apuestas_independientes']}** (N efectivo ML-CLUS-001: {p.get('x_n_efectivo')}).", ""]
        for e in p.get("clusteres_exposicion", []):
            L.append(f"- {e['cluster_id']}: {e['factor_dominante']} — {', '.join(e['opp_ids'])}")
        L += ["", "| Tipo de activo | Semáforo | Opción | RK | Riesgo | Relevancia | Siguiente paso |", "|---|---|---|---|---|---|---|"]
        for c, d in p["clases"].items():
            if not d["opciones"]:
                L.append(f"| {c} | {d['estado_semaforo']} | — | — | — | — | — |")
            for o in d["opciones"]:
                L.append(f"| {c} | {d['estado_semaforo']} | {o['rango']} · {o['nombre']} · `{o['opp_id']}` | {o['puntuaciones']['RK']} | "
                         f"{o['riesgo_1a5']} | {o['relevancia_decisional']} | {o['siguiente_paso_sugerido']} |")
        L += ["", "## 2. Alcance, nivel, presupuesto y consumo", "", "| Tipo de activo | Nivel | GC0 cambio material | Motivos |", "|---|---|---|---|"]
        for c, nv in p["nivel_por_clase"].items():
            g = extras["gc0"].get(c, {})
            L.append(f"| {c} | {nv} | {'sí' if g.get('cambio_material') else 'no'} | {'; '.join(g.get('motivos', [])) or 'arrastre verificado'} |")
        L += ["", f"Consumo del RUN (hasta la redacción): {consumo.get('llamadas')} llamadas, {consumo.get('uc')} UC "
                  f"(LLM {consumo.get('uc_llm')}, Motor {consumo.get('uc_motor')}); tokens de entrada {consumo.get('entrada')}, "
                  f"salida {consumo.get('salida')}, caché escritura {consumo.get('cache_escritura')}, lectura {consumo.get('cache_lectura')}.", "",
              "## 3. Régimen macro y de mercado", "", p["regimen_macro"], "", "## 4. Análisis por tipo de activo", ""]
        for i, (c, d) in enumerate(p["clases"].items(), 1):
            emb = d.get("embudo", {})
            L += [f"### 4.{i} {NOMBRE_CLASE[c]} ({c}) — semáforo {d['estado_semaforo']}", "", f"**Régimen.** {d['regimen_clase']}", "",
                  "| Etapa | Número |", "|---|---|", f"| Candidatas cribadas | {emb.get('cribadas')} |", f"| Pasan GC1 | {emb.get('pasan_gc1')} |",
                  f"| Pasan GC2 | {emb.get('pasan_gc2')} |", f"| Finalistas GC3 | {emb.get('finalistas_gc3')} |",
                  f"| Elegibles | {emb.get('elegibles')} |", f"| En el top-3 | {len(d['opciones'])} |", ""]
            if d.get("menos_de_tres_motivo"):
                L += [f"**Menos de tres (R14).** {d['menos_de_tres_motivo']}", ""]
            for o in d["opciones"]:
                pu = o["puntuaciones"]
                L += [f"##### {o['rango']}. {o['nombre']} · `{o['opp_id']}`", "",
                      f"- Tipo de opción: {o['tipo_opcion']} · subtipo: {o.get('subtipo')} · regiones: {', '.join(o['regiones'])}",
                      f"- **Ámbito.** Incluye: {o['ambito']['incluye']} · Excluye: {o['ambito']['excluye']} · Región: {o['ambito']['region']}",
                      f"- **Indicador de seguimiento.** {o['indicador_seguimiento']['nombre']} (`{o['indicador_seguimiento'].get('simbolo')}`, "
                      f"{o['indicador_seguimiento']['fuente']}) · **Invertibilidad (PS3).** {o['invertibilidad']['nota']}",
                      f"- Clúster: {o.get('cluster_id')} · confianza: {o['confianza']} · relevancia: {o['relevancia_decisional']} · reversibilidad: {o['reversibilidad']} · liquidez: {o['liquidez']}",
                      f"- **Naturaleza de la inversión:** {o.get('naturaleza_inversion')} · **horizonte principal:** {o.get('horizonte_principal')}"
                      + (f" (justificación: {o['justificacion_horizonte']})" if o.get("justificacion_horizonte") else ""),
                      f"- **Siguiente paso sugerido: {o['siguiente_paso_sugerido']}**", "",
                      f"**Tesis.** {o['tesis']}", "", f"**Mecanismo.** {o['mecanismo']}", "", f"**Valoración.** {o['valoracion']}", "",
                      f"**Puntuaciones (HT-03, `{pu['desglose_ref']}`).** T {pu['T']} · E {pu['E']} · M {pu.get('M')} · A {pu['A']} · RK {pu['RK']}", "",
                      "| Horizonte | Vista | Banda o probabilidad | Certificado | Pronóstico | Resolución |", "|---|---|---|---|---|---|"]
                for hh, v in o["horizontes"].items():
                    L.append(f"| {hh} | {v['vista']} | {v['banda'] if v['prob'] is None else v['prob']} | {'sí' if v['certificado_r13'] else v.get('etiqueta')} | "
                             f"`{v['prg_id']}` | {v.get('fecha_resolucion')} — {v.get('criterio_resolucion')} |")
                for hh, v in o["horizontes"].items():
                    if v.get("hitos"):
                        L += ["", f"**Hitos intermedios del pronóstico {hh} `{v['prg_id']}`** (probabilidad siempre cualitativa; se evalúa por sus hitos):", ""]
                        L += [f"- `{x['hit_id']}` · {x['fecha']} · {x['indicador']} · criterio: {x['criterio']}" for x in v["hitos"]]
                L += ["", f"**Catalizadores.** {'; '.join(x['evento'] + ' (' + x['fecha'] + ')' for x in o['catalizadores']) or '—'}", "",
                      f"**Riesgos.** {'; '.join(o['riesgos'])} — riesgo sintético **{o['riesgo_1a5']}/5** (RISK-DD-001).", "",
                      f"**Invalidación.** {'; '.join(o['invalidacion'])}", "", f"**Qué cambiaría la conclusión.** {'; '.join(o['que_cambiaria_la_conclusion'])}", "",
                      f"**Lo que no sabemos.** {'; '.join(o['lo_que_no_sabemos'])}", ""]
                if o.get("ejemplos_ilustrativos"):
                    L += [f"**Ejemplos ilustrativos del ámbito (no son propuestas).** {'; '.join(o['ejemplos_ilustrativos'])}", ""]
                b = next((x for x in p.get("paquete_para_bloque_B", []) if x.get("opp_id") == o["opp_id"]), None)
                if b:
                    L += [f"**Encargo para el Bloque B.** Criterios de selección sugeridos: {'; '.join(b['criterios_seleccion_sugeridos'])}. "
                          f"Métricas clave: {'; '.join(b['metricas_clave'])}. Preguntas: {' '.join(b['preguntas_para_B'])}", ""]
                L += [
                      f"**Evidencia y cálculos.** {', '.join(o['evidencias'])} · {', '.join(o['calculos'])}", ""]
        L += ["## 5. Seguimiento de opciones vigentes", "", "| OPP | Estado | Decisión del Broker | Comentario |", "|---|---|---|---|"]
        for s in p["seguimiento_vigentes"]:
            L.append(f"| `{s['opp_id']}` | {s['estado']} {s.get('motivo_cierre') or ''} | {s.get('decision_broker') or '—'} | {s['comentario']} |")
        L += ["", "## 6. Objeciones y respuestas", "", "| OPP | Fuerza | Objeción | Respuesta | Estado |", "|---|---|---|---|---|"]
        for d in p["clases"].values():
            for o in d["opciones"]:
                for ob in o["objeciones"]:
                    L.append(f"| `{o['opp_id']}` | {ob['fuerza']} | {ob['resumen']} | {ob.get('respuesta') or '—'} | {ob['estado']} |")
        L += ["", "## 7. Limitaciones, lagunas y qué no sabemos", ""] + [f"- {x}" for x in p["limitaciones"]]
        if p.get("supuestos_declarados"):
            L += ["", "**Supuestos declarados (consultas al Broker sin respuesta, CT-23).**", ""] + \
                 [f"- {s['supuesto']} (`{s['cns_id']}`) — efecto si fuera falso: {s.get('efecto_si_falso', '—')}" for s in p["supuestos_declarados"]]
        hg = p["historial_aciertos"]
        L += ["", "## 8. Historial de aciertos (Evaluador)", "", f"Ventana: **{hg['ventana']}**. {hg.get('nota', '')}", "",
              "| Ámbito | n | Aciertos | Tasa | Tasa esperada por azar | Significativo |", "|---|---|---|---|---|---|"]
        for k, v in [("Global", hg.get("global") or {})] + list(hg.get("por_clase", {}).items()):
            L.append(f"| {k} | {v.get('n')} | {v.get('aciertos')} | {v.get('tasa_acierto')} | {v.get('tasa_esperada_azar')} | {v.get('significativo')} |")
        L += ["", "## 9. Preguntas sugeridas", ""] + [f"- {x}" for x in p["preguntas_sugeridas"]]
        L += ["", f"*{p['aviso_legal']}*", ""]
        return "\n".join(L)

    # ------------------------------------------------------------------------------------
    def generar(self, bloque, paquete: dict, extras: dict, red: dict, as_of, run_id: str, estado_run: str) -> tuple[dict, dict]:
        from . import sintesis as sint
        as_of = pd.Timestamp(as_of)
        tarj = {t.get("opp_id"): t for t in red.get("tarjetas", []) if isinstance(t, dict)}
        for d in paquete["clases"].values():
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
        # Se genera y valida en una carpeta de borrador; solo lo que no queda BLOQUEADO llega a las carpetas de
        # entrega (7.3 G3: «BLOQUEADO impide la entrega»). Lo bloqueado se conserva aparte para la auditoría.
        nombres = {"informe_tecnico": f"{fecha}_informe-tecnico_{run_id}.md",
                   "informe_visual": f"{fecha}_informe-visual_{run_id}.html",
                   "paquete_json": f"{fecha}_paquete-json_{run_id}.json"}
        borrador = base / "_borradores" / run_id
        borrador.mkdir(parents=True, exist_ok=True)
        rutas = {k: str(borrador / n) for k, n in nombres.items()}
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
        rutas_entrega = {k: str(dirs[k] / n) for k, n in nombres.items()}   # las que cita el informe: las de entrega
        Path(rutas["informe_tecnico"]).write_text(self.tecnico(paquete, extras, g3, rutas_entrega, estado_run, cons), encoding="utf-8")
        coh = coherencia(rutas, js)
        if errores:
            bloq.append("ESQUEMA_JSON")
        if coh:
            bloq.append("COHERENCIA_ENTREGABLES")
        dictamen = "BLOQUEADO" if bloq else dictamen
        if dictamen == "BLOQUEADO":
            js.pop("estado_g3", None)      # nunca un estado G3 favorable en un entregable bloqueado
            Path(rutas["paquete_json"]).write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding="utf-8")
            destino = {k: base / "_bloqueados" / run_id for k in nombres}
        else:
            destino = dirs
        rutas = _publicar(rutas, destino, nombres)
        bloque.almacen.escribir("HA", "AG-18", {"tipo_entrada": "G3V", "id": f"G3V-{run_id[4:]}-F7", "run_id": run_id, "fase": "F7",
                                                "tipo_control": "SINCRONO_DETERMINISTA", "dictamen_ht09": res["dictamen"], "dictamen_efectivo": dictamen,
                                                "legibilidad": {"fernandez_huerta": leg["fernandez_huerta"], "pct_frases_mas_de_20": leg["pct_frases_mas_de_20"],
                                                                "jerga_sin_explicar": leg["jerga_sin_explicar"]},
                                                "errores_esquema": errores, "incoherencias": coh,
                                                "comprobaciones": [{"id": c["id"], "resultado": c["resultado"], "detalle": [i["detalle"] for i in c["incidencias"]][:5]}
                                                                   for c in res["comprobaciones"]]})
        return rutas, {"dictamen": dictamen, "bloqueos": bloq, "advertencias": adv, "legibilidad": leg["fernandez_huerta"],
                       "frases_largas": leg["frases_largas"][:10], "errores_esquema": errores, "incoherencias": coh}


def _publicar(rutas: dict[str, str], destino: dict[str, Path], nombres: dict[str, str]) -> dict[str, str]:
    """Mueve los entregables del borrador a su carpeta final (entrega o bloqueados) y borra el borrador vacío."""
    finales = {}
    for k, origen in rutas.items():
        destino[k].mkdir(parents=True, exist_ok=True)
        final = destino[k] / nombres[k]
        Path(origen).replace(final)
        finales[k] = str(final)
    try:
        Path(next(iter(rutas.values()))).parent.rmdir()
        Path(next(iter(rutas.values()))).parent.parent.rmdir()
    except OSError:
        pass
    return finales


def _semana_o_peticion(p: dict) -> str:
    if p["tipo"] == "PERIODICO":
        f = pd.Timestamp(p["fecha"])
        return f"Semana {f.isocalendar()[1]} de {f.isocalendar()[0]}"
    return f"Informe a petición del {p['fecha']}"


def coherencia(rutas: dict, js: dict) -> list[str]:
    """Mismas OPP-, orden y RK en el JSON, el informe técnico y el informe visual (G3-ENT-07)."""
    orden_js = [o["opp_id"] for d in js["clases"].values() for o in d["opciones"]]
    rk_js = {o["opp_id"]: o["puntuaciones"]["RK"] for d in js["clases"].values() for o in d["opciones"]}
    md = Path(rutas["informe_tecnico"]).read_text(encoding="utf-8")
    html = Path(rutas["informe_visual"]).read_text(encoding="utf-8")
    orden_md = re.findall(r"^##### \d+\. .*· `(OPP-\d{4}-\d+)`", md, re.M)
    orden_html = re.findall(r'<div class="pie-card"><span>(OPP-\d{4}-\d+)</span>', html)
    out = []
    if orden_md != orden_js:
        out.append(f"orden del informe técnico {orden_md} ≠ JSON {orden_js}")
    if orden_html != orden_js:
        out.append(f"orden del informe visual {orden_html} ≠ JSON {orden_js}")
    for oid, rk in rk_js.items():
        if f"· `{oid}` | {rk} |" not in md:
            out.append(f"RK de {oid} distinto en el informe técnico")
    return out
