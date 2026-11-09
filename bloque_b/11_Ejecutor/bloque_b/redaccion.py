"""F9 (redacción de los seis entregables) y F10 (entrega y registro) del Bloque B (V2.1), con el informe de parada
(7.11, 14.7) y el informe de seguimiento (7.13, 14.8).

Los seis entregables (V2.1: más el mapa de oportunidades por eslabón, entregable 6, en Markdown, .docx y JSON) salen del paquete de síntesis autorizado y declaran la misma fecha de corte (14): informe técnico
(Markdown, 16 secciones de 14.1), informe visual (HTML autocontenido con los estilos y los iconos de la plantilla
vigente de 06_Plantillas_entregables), paquete JSON (validado con el esquema), memorando ejecutivo (Markdown) y anexo de
datos y cálculos (XLSX y CSV con HT-10). HT-07 mide la legibilidad del informe visual y HT-09 hace la segunda pasada."""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .configuracion import NOMBRE_LLANO_TIPO, NOMBRE_TIPO, TIPOS_ACTIVO, buscar_versionado, ruta
from .herramientas import ht03, ht07, ht09, ht10
from . import sintesis
from .sintesis import NOMBRE_DIM, esquema_paquete, extracto_f2

CARPETAS = {"informe_tecnico": ("Informes técnicos Broker", "informe-tecnico", ".md"),
            "informe_visual": ("Informes visuales Usuario", "informe-visual", ".html"),
            "paquete_json": ("Paquetes JSON", "paquete-json", ".json"),
            "memorando": ("Memorandos ejecutivos", "memorando", ".md"),
            "anexo_datos": ("Anexos de datos", "anexo-datos", ".xlsx"),
            "mapa_eslabones": ("Mapas por eslabón", "mapa-eslabones", ".md")}
CARPETA_PARADA = "Informes de parada"
CARPETA_SEGUIMIENTO = "Informes de seguimiento"
VIA_LLANA = {"COTIZADA_DIRECTA": "Ya cotiza en bolsa.", "MATRIZ_COTIZADA": "Se accede a través de su empresa madre.",
             "ETF_O_FONDO": "Está dentro de un fondo.", "FUTURA_SALIDA_A_BOLSA": "Podría salir a bolsa.",
             "NO_INVERTIBLE_HOY": "Hoy no se puede comprar."}
HZ_LLANO = ["Días", "Semanas", "Meses", "Años", "Décadas"]
JERGA_TABLAS = {"ETF": "Un ETF (fondo que cotiza en bolsa) junta muchas empresas en una sola compra.",
                "bono": "Un bono (un préstamo que se compra y se vende) paga intereses."}
SEMAFORO = {"INVERTIR": ("verde", "Buena idea ahora", "i-ok"), "INVERTIR_ESCALONADO": ("verde-claro", "Buena idea, poco a poco", "i-escalon"),
            "VIGILAR": ("ambar", "Mirar y esperar", "i-ojo"), "DESCARTAR": ("gris", "No la vemos", "i-no")}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
TEXTOS_SEGUROS = {
    "frases_30s": ["Hemos estudiado este mercado a fondo.", "Miramos quién gana, quién pierde y cuánto cuesta.", "Te contamos lo que vemos."],
    "por_que": "Hay más demanda que oferta y la oferta tarda en crecer.",
    "riesgos_llanos": ["La demanda podría frenar.", "Podrían llegar nuevos rivales.", "Si sube el precio del dinero, todo vale menos."],
}


def _h(t) -> str:
    return html.escape(str(t if t is not None else ""), quote=True)


def fecha_larga(f: str, con_anio: bool = True) -> str:
    d = dt.date.fromisoformat(f)
    return f"{DIAS[d.weekday()]}, {d.day} de {MESES[d.month - 1]}" + (f" de {d.year}" if con_anio else "")


def nombre_entregable(fecha: str, clave: str, pet_id: str, fase: Optional[int] = None) -> str:
    carpeta, tipo, ext = CARPETAS[clave]
    return f"{fecha}_{tipo}_{pet_id}" + (f"_fase{fase}" if fase else "") + ext


# =============================================================================================================
# Informe visual (HTML)
# =============================================================================================================
def _plantilla_visual(cfg: Dict) -> str:
    p = buscar_versionado(ruta(cfg, "plantillas"), "Plantilla - Informe visual para el usuario", ".html")
    return p.read_text(encoding="utf-8") if p else ""


def _estilos_e_iconos(plantilla: str) -> (str, str):
    estilos = "\n".join(re.findall(r"<style>.*?</style>", plantilla, flags=re.S)) or "<style>body{font-family:system-ui,sans-serif}</style>"
    m = re.search(r'<svg width="0" height="0".*?</svg>', plantilla, flags=re.S)
    return estilos, (m.group(0) if m else "")


def informe_visual(cfg: Dict, p: Dict, t: Dict, fase: Optional[int] = None) -> str:
    est, iconos = _estilos_e_iconos(_plantilla_visual(cfg))
    v = p["veredicto"]["valor"]
    clase, texto_sem, icono = SEMAFORO[v]
    pu = p["puntuaciones"]
    riesgo = p["riesgo_1a5"]
    hz = p["estrategia"]["horizonte_dominante"]
    h_idx = ["H1", "H2", "H3", "H4", "H5"].index(hz)
    frases = (t.get("frases_30s") or TEXTOS_SEGUROS["frases_30s"])[:3]
    cadena = []
    for i, e in enumerate(p["despliegue_estructural"]["mapa_cadena"][:4]):
        papel = {"es": ("gana", "▲ Gana"), "consume": ("neutro", "Ni gana ni pierde"), "alimenta": ("neutro", "Ni gana ni pierde")}[e["papel_del_ambito"]]
        if i:
            cadena.append('<li class="flecha" aria-hidden="true">→</li>')
        cadena.append(f'<li><span class="papel {papel[0]}">{papel[1]}</span><span class="nombre">{_h(e.get("x_nombre_llano") or _llano_eslabon(e["eslabon"]))}</span></li>')
    perd = p["mapa_cobertura"].get("perdedores_sistematicos") or []
    if perd:
        nombre = perd[0]["objeto"] if isinstance(perd[0], dict) else perd[0]
        cadena.append('<li class="flecha" aria-hidden="true">→</li>')
        cadena.append(f'<li><span class="papel pierde">▼ Pierde</span><span class="nombre">{_h(_corta(nombre))}</span></li>')
    tipos_html = []
    for tipo in TIPOS_ACTIVO:
        est_t = "estudiado" if p["candidatos_por_tipo"][tipo].get("aplicable") else "no-aplica"
        tipos_html.append(f'<li class="{est_t}"><svg aria-hidden="true"><use href="#i-{tipo}"/></svg>{_h(NOMBRE_LLANO_TIPO[tipo])}'
                          f'<small>{"en estudio" if est_t == "estudiado" else "no aplica"}</small></li>')
    n_est = sum(1 for x in TIPOS_ACTIVO if p["candidatos_por_tipo"][x].get("aplicable"))
    riesgos = (t.get("riesgos_llanos") or TEXTOS_SEGUROS["riesgos_llanos"])[:3]
    hist = p["historial_aciertos"]
    n_res = (hist.get("ambitos") or {}).get("resueltos") or 0
    n_ok = (hist.get("ambitos") or {}).get("aciertos") or 0
    hist_frase = (f"De {n_res} análisis ya cerrados, {n_ok} salieron bien." if n_res else "Aún no hay análisis cerrados con los que medirnos.")
    gl = t.get("glosario") or []
    glos = "".join(f"<dt>{_h(g.get('termino'))}</dt><dd>{_h(g.get('definicion'))}</dd>" for g in gl if isinstance(g, dict))
    glos += "<dt>Fondos</dt><dd>Cestas con muchas empresas que compras de una vez.</dd>" if "Fondo" not in glos else ""
    puntos = "".join('<i class="lleno"></i>' if i < riesgo else "<i></i>" for i in range(5))
    hzs = "".join(f'<span class="{"activo" if i == h_idx else ""}">' + ('<span aria-hidden="true">🌳</span> ' if i == 4 else "") + f'{n}</span>'
                  for i, n in enumerate(HZ_LLANO))
    tablas = _tablas_eslabon(p)
    lect = {"alta": "Alta", "media": "Media", "baja": "Baja"}[pu["lectura_C"]]
    leyenda = "".join(f'<li class="{"actual" if k == v else ""}"><i class="punto {SEMAFORO[k][0]}" aria-hidden="true"></i>{txt}</li>'
                      for k, txt in (("INVERTIR", "Verde: buena idea ahora"), ("INVERTIR_ESCALONADO", "Verde claro: buena idea, poco a poco"),
                                     ("VIGILAR", "Ámbar: mirar y esperar"), ("DESCARTAR", "Gris: no la vemos")))
    pct = 100 * n_ok / n_res if n_res else 0
    return f"""<!doctype html>
<html lang="es-ES">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="Bloque B · AG-B17 Redactor y Diseñador de Informes · ejecutor bloque_b">
<meta name="pet_id" content="{_h(p['pet_id'])}">
<meta name="run_id" content="{_h(p['run_ids'][-1])}">
<meta name="data_cutoff" content="{_h(p['data_cutoff'])}">
<meta name="semaforo" content="{clase}">
<meta name="color-scheme" content="light dark">
<title>Tu informe: {_h(_corta(p['ambito']['nombre_llano'], 60))}</title>
{est}
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
{iconos}
<div class="envoltorio">
  <header class="cabecera">
    <div class="marca">Robot Investor · Tu análisis a petición{f" · fase {fase}" if fase else ""}</div>
    <div class="fechas">Informe del {fecha_larga(p['fecha'])}. Datos hasta el {fecha_larga(p['data_cutoff'], False)}.</div>
  </header>
  <main id="contenido">
    <h1>{_h(p['ambito']['nombre_llano'])}</h1>
    <section class="tarjeta" aria-labelledby="t-30s">
      <div class="resumen">
        <div>
          <h2 id="t-30s">En 30 segundos</h2>
          {''.join(f'<p>{_h(f)}</p>' for f in frases)}
        </div>
        <div class="semaforo" role="img" aria-label="Semáforo: {_h(texto_sem)}">
          <div class="luz {clase}"><svg aria-hidden="true"><use href="#{icono}"/></svg></div>
          <div><strong>{_h(texto_sem)}</strong><br><span>{_h(t.get('semaforo_explicacion') or '')}</span></div>
        </div>
      </div>
      <ul class="leyenda-semaforo" aria-label="Qué significa cada luz">{leyenda}</ul>
    </section>
    <section class="tarjeta" aria-labelledby="t-porque">
      <h2 id="t-porque">Por qué</h2>
      <p>{_h(t.get('por_que') or TEXTOS_SEGUROS['por_que'])}</p>
      <ol class="cadena" aria-label="Esquema de la cadena: quién gana y quién pierde">{''.join(cadena)}</ol>
    </section>
{tablas}    <section class="tarjeta" aria-labelledby="t-medidas">
      <h2 id="t-medidas" class="visually-hidden">Riesgo, plazo y confianza</h2>
      <div class="tres">
        <div class="medida"><h3>Riesgo</h3><div class="escala" role="img" aria-label="Riesgo {riesgo} de 5">{puntos}</div>
          <span class="valor">{riesgo} de 5</span><p>{_h(t.get('riesgo_texto') or 'Su precio puede bajar en un mal año.')}</p></div>
        <div class="medida"><h3>Plazo</h3><div class="horizontes" role="img" aria-label="Plazo: {['días', 'semanas', 'meses', 'años', 'décadas'][h_idx]}">{hzs}</div>
          <p>{_h(t.get('horizonte_texto') or 'Es una idea para varios meses.')}</p></div>
        <div class="medida"><h3>Confianza</h3><div class="barra" role="img" aria-label="Confianza {pu['C']} de 100, {lect.lower()}"><b style="width:{pu['C']}%"></b></div>
          <span class="valor">{pu['C']} de 100</span><p>{lect}: {_h(t.get('conviccion_texto') or 'hay datos, pero también dudas.')}</p></div>
      </div>
    </section>
    <section class="tarjeta" aria-labelledby="t-tipos">
      <h2 id="t-tipos">Qué tipo de activos se están estudiando</h2>
      <p>Hemos mirado {n_est} {"tipo" if n_est == 1 else "tipos"}. Otro equipo del sistema estudiará cada opción a fondo. Esto no es una lista de compra.</p>
      <ul class="tipos">{''.join(tipos_html)}</ul>
    </section>
    <section class="tarjeta" aria-labelledby="t-mal">
      <h2 id="t-mal">Qué podría salir mal</h2>
      <ul class="lista">{''.join(f'<li>{_h(r)}</li>' for r in riesgos)}</ul>
    </section>
    <section class="tarjeta" aria-labelledby="t-historial">
      <h2 id="t-historial">Cómo nos fue</h2>
      <div class="historial">
        <svg class="anillo" viewBox="0 0 36 36" role="img" aria-label="{n_ok} aciertos de {n_res} análisis cerrados">
          <circle cx="18" cy="18" r="15.9" fill="none" stroke="var(--barra-fondo)" stroke-width="4"/>
          <circle cx="18" cy="18" r="15.9" fill="none" stroke="var(--barra)" stroke-width="4" stroke-dasharray="{pct:.1f} {100 - pct:.1f}" stroke-dashoffset="25" stroke-linecap="round"/>
          <text x="18" y="21" text-anchor="middle" font-size="9" font-weight="700" fill="currentColor">{n_ok}/{n_res}</text>
        </svg>
        <div><p>{_h(hist_frase)}</p><p>Aún son pocos casos para saber si tenemos ventaja.</p></div>
      </div>
    </section>
    <section class="tarjeta paso" aria-labelledby="t-paso">
      <h2 id="t-paso">Qué pasa ahora</h2>
      <p>{_h(t.get('siguiente_paso_llano') or 'Tu Broker decide el siguiente paso. Nosotros vigilamos las señales y te avisamos si cambian.')}</p>
    </section>
    <section class="tarjeta" aria-labelledby="t-glosario">
      <h2 id="t-glosario">Palabras útiles</h2>
      <dl class="glosario">{glos}</dl>
    </section>
  </main>
  <p class="aviso"><strong>Esto no es una recomendación personal. Tu Broker Personal valora si encaja contigo.</strong><br>
  Análisis {_h(p['pet_id'])} · datos hasta el {_h(p['data_cutoff'])}.</p>
</div>
<style>.visually-hidden{{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}</style>
</body>
</html>
"""


def _tablas_eslabon(p: Dict) -> str:
    """Tablas simplificadas por eslabón (14.2, 3 bis): top-3 por eslabón atractivo, lenguaje llano, sin S ni precios."""
    esl = [e for e in (p.get("mapa_cadena_valor") or {}).get("eslabones") or [] if e.get("opciones") and ht09.ht03.eslabon_cualifica(e)["cualifica"]]
    if not esl:
        return ""
    llano = {x["eslabon"]: x.get("x_nombre_llano") for x in p["despliegue_estructural"]["mapa_cadena"] if x.get("x_nombre_llano")}
    bloques = []
    for e in esl[:4]:
        atasco = bool(e["cuello_botella"].get("material"))
        filas = []
        for o in e["opciones"][:3]:
            frase = "Una de las mejor situadas de su tipo." if o.get("en_top_n_tipo") else "La añadimos para cubrir este paso."
            filas.append(f'<tr class="opcion"><td>{_h(o["nombre"])}</td><td><svg aria-hidden="true"><use href="#i-{o["tipo_activo"]}"/></svg>'
                         f'{_h(NOMBRE_LLANO_TIPO[o["tipo_activo"]])}</td><td>{frase}</td></tr>')
        for g in sorted(e.get("emergentes") or [], key=lambda g: -(g.get("PEM") or 0))[:1]:
            filas.append(f'<tr class="emergente"><td colspan="3">Empresa nueva a vigilar: {_h(_corta(g["nombre"], 60))}. '
                         f'{VIA_LLANA[g["via_exposicion"]]}</td></tr>')
        nombre = llano.get(e["nombre"]) or _llano_eslabon(e["nombre"])
        clase = " si" if atasco else ""
        etiqueta = "Hay atasco" if atasco else "Sin atasco"
        nota = "Piden más de lo que se puede hacer ahora." if atasco else "Este paso de la cadena gana valor."
        bloques.append(f'        <table class="eslabon" data-eslabon="{_h(e["eslabon_id"])}">\n'
                       f'          <caption><span>{_h(nombre)}</span> <span class="atasco{clase}">{etiqueta}</span>\n'
                       f'            <small>{nota}</small></caption>\n'
                       '          <thead><tr><th scope="col">Opción estudiada</th><th scope="col">Tipo</th><th scope="col">En una frase</th></tr></thead>\n'
                       f'          <tbody>{"".join(filas)}</tbody>\n        </table>')
    return ('    <section class="tarjeta" aria-labelledby="t-eslabones">\n'
            '      <h2 id="t-eslabones">Dónde está el valor, paso a paso</h2>\n'
            '      <p class="rotulo"><strong>Activos que el análisis ha estudiado; no son recomendaciones; tu Broker decide.</strong></p>\n'
            + "".join(f'      <p>{frase}</p>\n' for termino, frase in JERGA_TABLAS.items()
                      if re.search(rf"\b{termino}", " ".join(o["nombre"] + " " + NOMBRE_LLANO_TIPO[o["tipo_activo"]]
                                                           for e in esl[:4] for o in e["opciones"][:3]), re.I))
            + '      <div class="eslabones">\n' + "\n".join(bloques) + '\n      </div>\n    </section>\n')


def _corta(t: str, n: int = 48) -> str:
    t = str(t or "")
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"


def _llano_eslabon(e: str) -> str:
    return _corta(re.sub(r"\s*\(.*?\)", "", e), 40)


# =============================================================================================================
# Informe técnico y memorando (Markdown)
# =============================================================================================================
def _tabla(cab: List[str], filas: List[List]) -> str:
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for f in filas:
        out.append("| " + " | ".join(str(x if x is not None else "—").replace("|", "/").replace("\n", " ") for x in f) + " |")
    return "\n".join(out)


def informe_tecnico(p: Dict, st: Dict, fase: Optional[int] = None) -> str:
    v = p["veredicto"]
    pu = p["puntuaciones"]
    tc = p["tiempo_consumo"]
    L: List[str] = []
    L.append(f"# Informe técnico · {p['ambito']['nombre']}" + (f" · fase {fase}" if fase else ""))
    L.append("")
    L.append("## 1. Portada\n")
    L.append(_tabla(["Campo", "Valor"], [
        ["Petición", p["pet_id"]], ["Ejecuciones", ", ".join(p["run_ids"])], ["Análisis registrado", f"{p['rec_id']} · {p['ambito']['mkt_id']}"],
        ["Nivel", f"{p['estrategia']['nivel']} · plan de cálculo {p['estrategia'].get('plan_calculo')}"],
        ["Tipo de objeto", p["ambito"]["tipo_objeto"]],
        ["Horizonte principal · secundarios", f"{p['estrategia']['horizonte_dominante']} · {', '.join(p['estrategia'].get('horizontes_secundarios') or []) or 'ninguno'}"],
        ["Capas y puertas de viabilidad", " · ".join(f"{g} {x}" for g, x in ((p.get("capas") or {}).get("puertas_viabilidad") or {}).items())],
        ["Continuación forzada", (lambda cf: f"tras {cf['puerta']} ({cf.get('motivo')})" if cf else "No")((p.get("capas") or {}).get("continuacion_forzada"))],
        ["Supuestos aplicados (consultas sin respuesta)", "; ".join(f"{x['cns_id']}: {x['supuesto']}" for x in p.get("supuestos_aplicados") or []) or "Ninguno"],
        ["Fecha · fecha de corte", f"{p['fecha']} · data_cutoff {p['data_cutoff']}"],
        ["Resultado del análisis", v["resultado_del_analisis"]],
        ["Validación G3 · auditoría", f"{(p.get('auditoria') or {}).get('dictamen_g3')} · auditoría {'realizada' if (p.get('auditoria') or {}).get('realizada') else 'no realizada (muestreo o backtest)'}"],
        ["Reservas de auditoría", "; ".join(p["reservas_auditoria"]) or "Ninguna"],
        ["Estados degradados", "; ".join(p.get("estados_degradados") or []) or "Ninguno"],
        ["Alcance reducido", "; ".join(p["estrategia"].get("recortes_declarados") or []) or "Ninguno"],
        ["Metodología", p["methodology_version"]]]))
    L.append("\n## 2. Resumen ejecutivo\n")
    L.append(f"**Veredicto del ámbito: {v['valor']}** · horizonte {v['horizonte']} · relevancia decisional **{v['relevancia_decisional']}** · "
             f"siguiente paso **{v['siguiente_paso_sugerido']}** · reversibilidad {v['reversibilidad']}.\n")
    L.append(f"{v.get('motivo') or ''}\n")
    L.append(_tabla(["Puntuación", "Valor", "Lectura"], [["A · Atractivo del ámbito", f"A = {pu['A']}", "umbrales 65 / 60 / 50"],
                                                         ["E · Calidad de la evidencia", f"E = {pu['E']}", "umbral 60"],
                                                         ["C · Convicción", f"C = {pu['C']}", f"{pu['lectura_C']} (C ≤ E + 10)"],
                                                         ["RF · RE", f"RF = {pu['RF']} · RE = {pu['RE']}", f"refutación {p['refutacion']['veredicto_tesis']}"]]))
    L.append(f"\n**Tesis.** {p['tesis']['enunciado']}\n")
    L.append(_tabla(["Evaluación", "Conclusión"], [[k.replace("_", " "), x] for k, x in p["evaluaciones_separadas"].items()]))
    L.append("\n**Candidatos prioritarios por Bloque C.x**\n")
    filas = []
    for t in TIPOS_ACTIVO:
        d = p["candidatos_por_tipo"][t]
        for c in d.get("top_n") or [] if d.get("aplicable") else []:
            if c["veredicto"] == "PRIORITARIO_PARA_C":
                filas.append([ht03.BLOQUE_C[t], f"{c['cand_id']} {c['nombre']}", c.get("isin") or c.get("ticker") or "—",
                              f"S = {c['S']} ({c['ic90_S'][0]}–{c['ic90_S'][1]})", c["rol_en_tesis"]])
    L.append(_tabla(["Bloque", "Candidato", "Identificador", "S (IC 90 %)", "Por qué"], filas) if filas else
             "Ningún candidato prioritario: ver la sección 10 (R21).")
    cond = v.get("condiciones_entrada") or [f"Tramo {x['tramo']}: {x['condicion']}" for x in v.get("tramos") or []] or \
        [f"{x['disparador']} ({x.get('fecha_esperada')})" for x in v.get("disparadores") or []] or [v.get("motivo_descarte") or "—"]
    L.append("\n**Condiciones, tramos o disparadores:** " + "; ".join(cond))
    L.append("\n**Qué cambiaría la conclusión:** " + "; ".join(v["que_cambiaria_la_conclusion"]))
    L.append(f"\n**Apuestas independientes:** {p['apuestas_independientes']}\n")
    L.append("## 3. Petición, origen, estrategia, tiempo y autorizaciones\n")
    L.append(f"- Ámbito: **incluye** {p['ambito']['incluye']} · **excluye** {p['ambito']['excluye']} · región {p['ambito']['region']}.")
    L.append(f"- Origen: {p['origen']['tipo']}" + (f" ({p['origen']['opp_id_A']})" if p['origen'].get('opp_id_A') else "") +
             f" · confirmado: {'; '.join(p['origen']['confirmado']) or '—'} · refutado: {'; '.join(p['origen']['refutado']) or '—'} · sin verificar: {'; '.join(p['origen'].get('sin_verificar') or []) or '—'}.")
    L.append("\n" + _tabla(["Pregunta", "Origen", "Respuesta"], [[r["pregunta"], r["origen"], r["respuesta"]] for r in p.get("respuestas_preguntas") or []])
             if p.get("respuestas_preguntas") else "\nSin preguntas expresas.")
    e = p["estrategia"]
    L.append(f"\nPerfil del Motor {', '.join(e['perfil_motor'])} · playbooks {', '.join(e['playbooks']) or '—'} · especialistas {', '.join(e.get('especialistas_activados') or [])}.\n")
    dims = {d["dim"]: d for d in p["dimensiones"]}
    L.append(_tabla(["Dimensión", "Peso", "Profundidad", "Especialista", "Tratada en"],
                    [[f"{k} {NOMBRE_DIM[k]}", e["pesos_efectivos"][k], e["profundidad"][k], (dims.get(k) or {}).get("especialista", "—"),
                      (dims.get(k) or {}).get("profundidad_tratada", "excluida")] for k in ht03.DIMENSIONES]))
    cap = p.get("capas") or {}
    L.append("\n**Capas y puertas de viabilidad (7.10).**\n")
    L.append(_tabla(["Capa", "Minutos", "Puerta", "Resultado"], [[k, v, {"1": "PV1", "2": "PV2", "3": "PV3"}.get(k, "—"),
                                                                 (cap.get("puertas_viabilidad") or {}).get({"1": "PV1", "2": "PV2", "3": "PV3"}.get(k), "—")]
                                                                for k, v in sorted((cap.get("minutos_por_capa") or {}).items())]))
    if p.get("consultas_broker"):
        L.append("\n**Consultas al Broker (CT-B-28).**\n")
        L.append(_tabla(["Consulta", "Tipo", "Modo", "Pregunta", "Supuesto", "Resolución", "Efecto"],
                        [[q["cns_id"], q["tipo"], q["modo"], q.get("pregunta"), q["supuesto"], q["resolucion"], q.get("efecto")] for q in p["consultas_broker"]]))
    L.append(f"\nTiempo: estimación p50 {tc.get('estimado_p50_min')} min · p80 {tc.get('estimado_p80_min')} min · real {tc['minutos']} min "
             f"(reloj {tc.get('reloj')}) · consumo {tc['uc']} UC · autorizaciones {', '.join(tc['autorizaciones']) or 'ninguna'} · "
             f"puntos de control {', '.join(tc.get('puntos_control') or [])}.\n")
    r = p["regimen"]
    L.append(f"## 4. Régimen de referencia\n\n{r['rgm_id']} · estado de confianza **{r['estado_confianza']}** · variables dominantes: "
             f"{', '.join(r['variables_dominantes'])}. {r.get('resumen') or ''}\n")
    L.append("## 5. Las doce dimensiones\n")
    for k in ht03.DIMENSIONES:
        d = dims.get(k)
        if not d:
            ex = next((x for x in e["exclusiones"] if x["dim"] == k), {})
            L.append(f"### {k} · {NOMBRE_DIM[k]} — excluida\nMotivo: {ex.get('motivo', '—')}\n")
            continue
        L.append(f"### {k} · {d['nombre']} — {d['profundidad_tratada']} · {d['especialista']}\n**Pregunta central:** {d['pregunta_central']}\n")
        for n in d["notas"]:
            refs = ", ".join((n.get("evidencias") or []) + (n.get("datos") or []) + (n.get("calculos") or []))
            L.append(f"- {n['etiqueta']} {n['afirmacion']}" + (f" — {n.get('clase_cifra')}" if n.get("clase_cifra") else "") + (f" · {refs}" if refs else ""))
        L.append(f"\n**Conclusión parcial:** {d['conclusion']} · **Confianza:** {d['confianza']['nivel']} · **Lagunas:** {'; '.join(d['lagunas']) or 'ninguna'}\n")
    de = p["despliegue_estructural"]
    L.append(f"## 6. Despliegue estructural de la cadena de valor\n\nAlcance: {de['alcance']}.\n")
    L.append(_tabla(["Eslabón", "Papel del ámbito", "Evidencias"], [[x["eslabon"], x["papel_del_ambito"], ", ".join(x.get("evidencias") or [])] for x in de["mapa_cadena"]]))
    L.append("\n" + (_tabla(["Actor", "Tipo", "Invertibilidad"], [[x["actor"], x["tipo"], x["invertibilidad"]] for x in de["actores"]]) if de["actores"] else "Sin actores identificados."))
    L.append("\n" + (_tabla(["Horizonte", "Avance", "Etiqueta"], [[x["horizonte_anos"], x["avance"], x["etiqueta"]] for x in de["vigilancia_tecnologica"]]) if de["vigilancia_tecnologica"] else "Sin vigilancia tecnológica material."))
    L.append("\n" + (_tabla(["Cuello", "Causa", "Señal de resolución", "Perdedores sistemáticos"],
                            [[x["eslabon"], x["causa"], x["senal_resolucion"], ", ".join(x.get("perdedores_sistematicos") or [])] for x in de["cuellos_botella"]])
                     if de["cuellos_botella"] else "Sin cuellos de botella identificados."))
    L.append("\n" + "\n".join(f"- {x['etiqueta']} {x['respuesta']}" for x in de["efectos_segundo_orden"]) + "\n")
    mcv = p.get("mapa_cadena_valor") or {}
    L.append("**Desglose jerárquico, cuellos (PCB) y atractivo por eslabón (AE)** — detalle completo en el entregable 6.\n")
    L.append(_tabla(["Eslabón", "Nivel", "PCB", "Cuello material", "AE", "Opciones", "Emergentes"],
                    [[f"{e['eslabon_id']} {e['nombre']}", e["nivel"], e["cuello_botella"]["PCB"], "sí" if e["cuello_botella"].get("material") else "no",
                      e["atractivo"]["AE"], len(e.get("opciones") or []), len(e.get("emergentes") or [])] for e in mcv.get("eslabones") or []]))
    L.append(f"\nSíntesis: {mcv.get('sintesis') or '—'}\n")
    pr = p["proyecciones"]
    L.append(f"## 7. Máquina de proyecciones\n\nActivada: {'sí' if pr['activada'] else 'no'}" + (f" · motivo de exclusión: {pr.get('motivo_exclusion')}" if not pr["activada"] else "") + "\n")
    if pr["activada"]:
        L.append(_tabla(["Etapa", "Contenido"], [[x["etapa"], x["contenido"]] for x in pr["etapas"]]))
        L.append("\n" + _tabla(["Premisa", "Valor", "Fuente", "Invalidación"], [[x["premisa"], x["valor"], x["fuente"], x.get("invalidacion")] for x in pr["premisas"]]))
        L.append(f"\nBrecha de expectativas: {pr.get('brecha_expectativas') or '—'}\n")
    L.append("## 8. Escenarios, sensibilidades, robustez y pronósticos\n")
    L.append(_tabla(["Escenario", "Premisas", "Régimen", "Banda", "Resultado frente a la referencia"],
                    [[x["nombre"], x["premisas"], x["regimen"], x["banda"] or x["probabilidad"], x["resultado_vs_referencia"]] for x in p["escenarios"]]))
    L.append(f"\nRobustez entre escenarios: RE = {pu['RE']}. Sin certificado, solo bandas verbales (R13).\n")
    if p.get("sensibilidades"):
        L.append(_tabla(["Variable", "Base", "Rango", "Efecto"], [[x["variable"], x.get("valor_base"), f"{x.get('valor_bajo')} – {x.get('valor_alto')}",
                                                                    f"{x['efecto_bajo']} / {x['efecto_alto']}"] for x in p["sensibilidades"]]))
    L.append("\n" + _tabla(["PRG-B", "Tipo", "Afirmación", "Resolución", "Banda"],
                           [[x["prg_id"], x["tipo"], x["afirmacion"], x["fecha_resolucion"], x["banda"]] for x in p["pronosticos_detalle"]]) + "\n")
    L.append(f"## 9. Tesis, hipótesis competidoras y su cierre\n\n**Tesis:** {p['tesis']['enunciado']}\n\n**Mecanismo:** {p['tesis'].get('mecanismo') or '—'}\n")
    L.append(_tabla(["Premisa", "Evidencia", "Comprobación", "Invalidación"], [[x["premisa"], ", ".join(x["evidencia"]), x["comprobacion"], x["invalidacion"]] for x in p["tesis"]["premisas"]]))
    L.append("\n" + _tabla(["Hipótesis", "Discriminante", "Estado"], [[f"{h['hip_id']} {h['enunciado']}", h["discriminante"], h["estado"]] for h in p["tesis"]["hipotesis"]]))
    L.append(f"\n**Steelman de la tesis contraria:** {p['tesis']['steelman_contrario']}\n")
    L.append("## 10. Selección de activos\n")
    for t in TIPOS_ACTIVO:
        d = p["candidatos_por_tipo"][t]
        if not d.get("aplicable"):
            continue
        u = d["universo"]
        L.append(f"### {t} · {NOMBRE_TIPO[t]} ({d['playbook']} → Bloque {ht03.BLOQUE_C[t]})\n")
        L.append(f"Universo: {u['tamano']} activos ({u.get('tamano_invertible')} invertibles) a {u['fecha']} · fuentes: {', '.join(u['fuentes'])} · {u.get('metodo')}. "
                 f"Exclusiones: {', '.join(f'{k} {n}' for k, n in d['excluidos_por_motivo'].items()) or 'ninguna'}.\n")
        L.append("Traducción de rasgos: " + "; ".join(f"{x['rasgo']} → {', '.join(x['metricas'])}" for x in d.get("traduccion_rasgos_metricas") or []) + "\n")
        if d["top_n"]:
            L.append(_tabla(["Rango", "Candidato", "S", "IC 90 % S", "IC rango", "PE", "QL", "VA", "MO", "RI", "LA", "CO", "Pureza", "Veredicto"],
                            [[c["rango"], f"{c['cand_id']} {c['nombre']}", f"S = {c['S']}", f"{c['ic90_S'][0]}–{c['ic90_S'][1]}",
                              f"{c['ic90_rango'][0]}–{c['ic90_rango'][1]}" + (" FRONTERA" if c["frontera"] else "")] +
                             [("—" if c["desglose"].get(k) is None else round(c["desglose"][k])) for k in ht03.COMPONENTES_S] +
                             [c["pureza"]["valor"], c["veredicto"]] for c in d["top_n"]]))
            for c in d["top_n"]:
                L.append(f"\n**{c['cand_id']} · {c['nombre']}** — {c['veredicto']}, S = {c['S']}. {c['rol_en_tesis']} Pureza: {c['pureza']['metrica']} = "
                         f"{c['pureza']['valor']} ({c['pureza']['fuente']}). Alertas: {', '.join(a['senal'] for a in c['alertas']) or 'ninguna'}."
                         + (f" Motivo de SECUNDARIO: {', '.join(c.get('motivo_secundario') or [])}." if c["veredicto"] == "SECUNDARIO" else "")
                         + (f" Exposición compartida: {c['exposicion_compartida']}." if c.get("exposicion_compartida") else ""))
        L.append(f"\nAlternativas: {', '.join(d['alternativas']) or 'ninguna'} · sustituciones por diversidad: "
                 f"{'; '.join(f'{s['desplazado']} (S {s['S']}): {s['motivo']}' for s in d['sustituciones_diversidad']) or 'ninguna'} · "
                 f"menos de N: {d.get('menos_de_N_motivo') or '—'}\n")
    noap = [[t, p["candidatos_por_tipo"][t]["motivo"]] for t in TIPOS_ACTIVO if not p["candidatos_por_tipo"][t].get("aplicable")]
    L.append(_tabla(["Tipo no aplicable", "Motivo"], noap) + "\n")
    rf = p["refutacion"]
    L.append(f"## 11. Refutación y registro de contraste adversarial\n\nRealizada por {rf['realizada_por']} · tesis **{rf['veredicto_tesis']}**.\n")
    L.append(_tabla(["Objeción", "Objeto", "Fuerza", "Argumento", "Respuesta", "Referencias de la respuesta", "Estado"],
                    [[o["obj_id"], o.get("x_nombre_eslabon") or o["objeto"], o["fuerza"], o["argumento"], o.get("respuesta"),
                      ", ".join(o.get("x_evidencia_respuesta", [])) or "—",
                      o.get("x_motivo_abierta") or o["estado_contraste"]] for o in rf["objeciones"]])
             if rf["objeciones"] else "Autorrefutación del Director (no independiente).")
    L.append(f"\n**Pre-mortem:** {rf.get('pre_mortem') or '—'}\n")
    m = p["mapa_cobertura"]
    fmt = lambda xs: "; ".join((x if isinstance(x, str) else f"{x['objeto']}" + (f" ({x.get('motivo') or x.get('mecanismo')})" if x.get("motivo") or x.get("mecanismo") else "")) for x in xs) or "—"  # noqa: E731
    L.append("## 12. Mapa de cobertura de oportunidades\n")
    for k, nom in (("directas", "Oportunidades directas"), ("indirectas", "Oportunidades indirectas"), ("perdedores_sistematicos", "Perdedores sistemáticos"),
                   ("investigado", "Investigado"), ("excluido_con_motivo", "Excluido con motivo"), ("vigilancia_informativa", "Vigilancia informativa"),
                   ("vigilancia_pre_salida", "Vigilancia pre-salida a bolsa")):
        L.append(f"- **{nom}:** {fmt(m.get(k) or [])}")
    ps = p["plan_de_seguimiento"]
    L.append(f"\n## 13. Plan de seguimiento\n\nVigente hasta {ps['vigente_hasta']} · frecuencia {ps['frecuencia']}.\n")
    L.append(_tabla(["Señal", "Serie", "Fluctuación", "Revisión", "Invalidación", "Dirección"],
                    [[f"{s['sig_id']} {s['nombre']}", s["serie"], f"{s['umbral_fluctuacion']['min']} – {s['umbral_fluctuacion']['max']}",
                      s["umbral_revision"], s["umbral_invalidacion"], s["direccion"]] for s in ps["senales"]]))
    L.append("\nEl Vigía avisa al Broker por el Coordinador; nunca abre un análisis nuevo (R32).\n")
    L.append("## 14. Limitaciones, lagunas, discrepancias abiertas y qué no sabemos\n")
    L.append("- **Limitaciones:** " + "; ".join(p["limitaciones"]))
    L.append("- **Qué podría salir mal:** " + "; ".join(f"{r['riesgo']} ({r['mecanismo']}; señal: {r['senal_temprana']})" for r in p["riesgos"]))
    L.append("- **Lo que no sabemos:** " + ("; ".join(p["tesis"].get("lo_que_no_sabemos") or []) or "—"))
    lag = [f"{d['dim']}: {l}" for d in p["dimensiones"] for l in d["lagunas"]]
    L.append("- **Lagunas:** " + ("; ".join(lag) or "ninguna") + "\n")
    h = p["historial_aciertos"]
    L.append("### 14 bis. Lista de comprobación profesional (8.10)\n")
    L.append(_tabla(["Ítem", "Estado", "Referencia"], [[f"{x['item']}. {sintesis.LISTA_PROFESIONAL[x['item']][0]}", x["estado"], x["referencia"]]
                                                     for x in p.get("lista_profesional") or []]) + "\n")
    L.append(f"## 15. Historial de aciertos\n\nVentana {h['ventana']} · ámbitos {json.dumps(h['ambitos'], ensure_ascii=False)} · rankings "
             f"{json.dumps(h['rankings'], ensure_ascii=False)} · **certificación: {h['certificacion']}**.\n")
    L.append("## 16. Anexos de evidencia, cálculos y metodología\n")
    L.append("- Afirmaciones y evidencias: " + ", ".join(sorted({e for d in p["dimensiones"] for n in d["notas"] for e in n.get("evidencias") or []}))[:2000])
    L.append("- Datos (DAT-B) y cálculos (CALC-B): ver el anexo de datos (hojas Cifras y Artefactos).")
    L.append("- Metodología: Documento 0 del Bloque B V2.0; HT-03, HT-08, HT-09, HT-10, HT-11.")
    L.append("- Preguntas sugeridas para consultas N0: " + "; ".join(p["preguntas_sugeridas"]))
    L.append(f"\n---\n*Análisis del Bloque B (Robot Investor). No constituye asesoramiento personalizado ni una recomendación de inversión. "
             f"El Broker Personal decide; los candidatos son encargos para los Bloques C.x, no valoraciones individuales. data_cutoff {p['data_cutoff']}.*\n")
    return "\n".join(L)


def memorando(p: Dict, t: Dict, fase: Optional[int] = None) -> str:
    v = p["veredicto"]
    pu = p["puntuaciones"]
    tc = p["tiempo_consumo"]
    tesis3 = t.get("tesis_3_frases") or [p["tesis"]["enunciado"]]
    L = [f"# Memorando · {p['ambito']['nombre']}" + (f" · fase {fase}" if fase else ""), "",
         f"**{p['pet_id']}** · {p['rec_id']} · nivel {p['estrategia']['nivel']} · {p['ambito']['tipo_objeto']} · horizonte {v['horizonte']} · "
         f"fecha {p['fecha']} · **data_cutoff {p['data_cutoff']}**", ""]
    if p["reservas_auditoria"]:
        L.append("**Reservas de auditoría:** " + "; ".join(p["reservas_auditoria"]) + "\n")
    cf = (p.get("capas") or {}).get("continuacion_forzada")
    if cf:
        L.append(f"**Continuación forzada por el Broker tras {cf['puerta']} no superada** ({cf.get('motivo')}).\n")
    if p.get("supuestos_aplicados"):
        L.append("**Supuestos aplicados por falta de respuesta:** " + "; ".join(f"{x['cns_id']}: {x['supuesto']}" for x in p["supuestos_aplicados"]) + "\n")
    L += ["## 1. Veredicto", f"**{v['valor']}** · relevancia decisional **{v['relevancia_decisional']}** · resultado {v['resultado_del_analisis']} · "
          f"siguiente paso **{v['siguiente_paso_sugerido']}**", "", _tabla(["A · atractivo", "E · evidencia", "C · convicción"],
                                                                            [[f"A = {pu['A']}", f"E = {pu['E']}", f"C = {pu['C']} ({pu['lectura_C']})"]]), "",
          "## 2. Tesis en tres frases", " ".join(tesis3[:3]), "", "## 3. Cifras decisivas"]
    esc = {e["nombre"]: e for e in p["escenarios"]}
    L.append(f"- Escenario base: {esc.get('base', {}).get('resultado_vs_referencia', '—')} — {p['data_cutoff']} · {', '.join(esc.get('base', {}).get('calculos') or [])} · estimación estadística")
    L.append(f"- Robustez entre escenarios RE = {pu['RE']} — {p['data_cutoff']} · estimación estadística")
    L.append("\n## 4. Candidatos prioritarios por Bloque C.x")
    filas = []
    for tp in TIPOS_ACTIVO:
        d = p["candidatos_por_tipo"][tp]
        for c in d.get("top_n") or [] if d.get("aplicable") else []:
            if c["veredicto"] == "PRIORITARIO_PARA_C":
                filas.append([ht03.BLOQUE_C[tp], f"{c['cand_id']} {c['nombre']}", c.get("isin") or c.get("ticker") or "—", f"S = {c['S']}", _corta(c["rol_en_tesis"], 90)])
    L.append(_tabla(["Bloque", "Candidato", "Identificador", "S", "Por qué"], filas) if filas else "Ninguno (R21): ver el informe técnico, sección 10.")
    esl = [e for e in (p.get("mapa_cadena_valor") or {}).get("eslabones") or [] if e["eslabon_id"] != "ESL-00"][:3]
    if esl:
        L.append("\n**Eslabones más atractivos y cuellos materiales** (entregable 6):")
        L += [f"- {e['eslabon_id']} {e['nombre']}: AE {e['atractivo']['AE']}, PCB {e['cuello_botella']['PCB']}"
              + (" (cuello material)" if e["cuello_botella"].get("material") else "") for e in esl]
    L.append(f"\nApuestas independientes: {p['apuestas_independientes']}.\n\n## 5. Riesgos principales")
    L += [f"- {r['riesgo']} — señal temprana: {r['senal_temprana']}" for r in p["riesgos"][:4]]
    L.append("\n## 6. Disparadores, tramos e invalidación")
    L += [f"- Tramo {x['tramo']}: {x['condicion']}" for x in v.get("tramos") or []]
    L += [f"- Condición de entrada: {x}" for x in v.get("condiciones_entrada") or []]
    L += [f"- Disparador: {x['disparador']} ({x.get('fecha_esperada')})" for x in v.get("disparadores") or []]
    L.append("- Invalidación: " + "; ".join(p["invalidacion"][:3]))
    L.append("- Qué cambiaría la conclusión: " + "; ".join(v["que_cambiaria_la_conclusion"][:3]))
    L.append(f"\n## 7. Tiempo y consumo\n{tc['minutos']} min (estimación p80 {tc.get('estimado_p80_min')} min) · {tc['uc']} UC · autorizaciones "
             f"{', '.join(tc['autorizaciones']) or 'ninguna'}.\n")
    L.append(f"---\n*No es asesoramiento personalizado. El Broker Personal decide; los candidatos son encargos para los Bloques C.x. "
             f"Historial: {p['historial_aciertos']['certificacion']}.*\n")
    return "\n".join(L)


# =============================================================================================================
# Entregable 6 · Mapa de oportunidades por eslabón de la cadena de valor (8.7.4, 14.6)
# =============================================================================================================
def mapa_eslabones_md(p: Dict) -> str:
    m = p["mapa_cadena_valor"]
    pv = (p.get("capas") or {}).get("puertas_viabilidad") or {}
    L = [f"# Mapa de oportunidades por eslabón · {p['ambito']['nombre']}", "",
         f"**{p['pet_id']}** · {p['rec_id']} · nivel {p['estrategia']['nivel']} · {p['ambito']['tipo_objeto']} · horizonte principal "
         f"{p['estrategia']['horizonte_dominante']} · fecha {p['fecha']} · **data_cutoff {m['data_cutoff']}**", "",
         f"Entregable 6 del Bloque B para el Broker (8.7.4, 14.6). Veredicto del ámbito: **{p['veredicto']['valor']}**. "
         f"Puertas de viabilidad: PV1 {pv.get('PV1')} · PV2 {pv.get('PV2')} · PV3 {pv.get('PV3')}.", ""]
    if pv.get("PV3") == "NO_SUPERADA":
        L += ["> **PV3 no superada.** Ningún eslabón atractivo o con cuello material tiene opciones invertibles que superen los filtros: "
              "las opciones de las tablas son **indicativas (PV3 no superada)**, sin PRIORITARIO_PARA_C ni encargos C.x.", ""]
    L += ["## 1. Alcance del desglose", "",
          f"Nivel de detalle {m['nivel_detalle']} · eslabón crítico {m.get('eslabon_critico') or '—'} · {len(m['eslabones'])} eslabones.", ""]
    L.append(_tabla(["Omitido", "Motivo"], [[o.get("eslabon"), o.get("motivo")] for o in m.get("omisiones") or []]) if m.get("omisiones") else "Sin omisiones.")
    L += ["", "## 2. Árbol de la cadena", "", "```"]
    hijos: Dict[Optional[str], List[Dict]] = {}
    for e in m["eslabones"]:
        hijos.setdefault(e.get("padre"), []).append(e)

    def rama(padre, nivel):
        for e in sorted(hijos.get(padre, []), key=lambda x: x["eslabon_id"]):
            cb = e["cuello_botella"]
            L.append("  " * nivel + f"{e['eslabon_id']} {e['nombre']} [{e['nivel']}] · AE {e['atractivo']['AE']} · PCB {cb['PCB']}"
                     + (" · CUELLO MATERIAL" if cb.get("material") else ""))
            rama(e["eslabon_id"], nivel + 1)
    rama(None, 0)
    L += ["```", "", "## 3. Eslabones (orden descendente por AE)", ""]
    for e in m["eslabones"]:
        mt = e["metricas"]
        cb = e["cuello_botella"]
        at = e["atractivo"]
        tam = mt.get("tamano") or {}
        L += [f"### {e['eslabon_id']} · {e['nombre']}" + (" · cuello material" if cb.get("material") else ""), "",
              f"{e['descripcion']} Papel del ámbito: {e.get('papel_ambito')}. Nivel: {e['nivel']}" + (f" (padre {e['padre']})" if e.get("padre") else "") + ".", ""]
        L.append(_tabla(["Métrica", "Valor"], [
            ["Tamaño", f"{tam.get('valor')} {tam.get('unidad') or ''} ({tam.get('fecha') or 's. f.'}; {tam.get('fuente') or 'sin fuente'})" if tam.get("valor") is not None else "—"],
            ["Crecimiento anual", _pct(mt.get("crecimiento_anual"))],
            ["Margen típico (bruto / operativo)", f"{_pct((mt.get('margen_tipico') or {}).get('bruto'))} / {_pct((mt.get('margen_tipico') or {}).get('operativo'))}"],
            ["Poder de negociación", mt.get("poder_negociacion") or "—"], ["HHI de proveedores", mt.get("hhi") if mt.get("hhi") is not None else "—"],
            ["Cuello de botella", f"{'sí' if cb.get('es_cuello') else 'no'} · severidad {cb['severidad']} · persistencia {cb['persistencia']} · relevancia {cb['relevancia_valor']} · PCB = {cb['PCB']}"
                                  + (" (material)" if cb.get("material") else "")],
            ["Indicadores", "; ".join(f"{x['indicador']} = {x.get('valor')} ({x['estado']})" for x in cb.get("indicadores") or []) or "—"],
            ["Señal de resolución", cb.get("senal_resolucion")],
            ["Atractivo del eslabón", f"AE = {at['AE']} · " + ", ".join(f"{k} {v}" for k, v in (at.get("desglose") or {}).items())]]))
        L += ["", "**Mejores opciones del eslabón** (hasta cinco; adicionales al top-N por tipo, sin duplicarlo; 9.13)", ""]
        if e.get("opciones"):
            L.append(_tabla(["Rango", "Candidato", "Ticker / ISIN", "Tipo", "Rol en el eslabón", "Pureza al eslabón", "S (IC 90 %)", "Veredicto", "Motivo", "Riesgos clave"],
                            [[o["rango"], f"{o['cand_id']} {o['nombre']}", o.get("ticker") or o.get("isin") or "—", o["tipo_activo"], o.get("rol_en_eslabon"),
                              o.get("pureza_eslabon"), f"{o['S']} ({(o.get('ic90_S') or ['—', '—'])[0]}–{(o.get('ic90_S') or ['—', '—'])[1]})",
                              o["veredicto"], o.get("motivo"), "; ".join(o.get("riesgos_clave") or [])] for o in e["opciones"]]))
        else:
            L.append(f"Sin opciones: {e.get('sin_opciones_motivo') or 'el eslabón no es atractivo ni tiene un cuello material (9.13)'}.")
        L += ["", "**Emergentes, startups y spin-offs del eslabón** (radar de AG-B24; PEM ordena, no recomienda)", ""]
        if e.get("emergentes"):
            L.append(_tabla(["Nombre", "Tipo", "Financiación conocida", "Tecnología o ventaja", "Señales de tracción", "Vía de exposición", "PEM", "Riesgos"],
                            [[f"{g['emg_id']} {g['nombre']}", g["tipo"], _financiacion(g.get("financiacion_conocida")), g.get("tecnologia_o_ventaja"),
                              "; ".join(g.get("senales_traccion") or []), g["via_exposicion"] + (f" ({(g.get('instrumento_exposicion') or {}).get('nombre')})"
                                                                                                if (g.get("instrumento_exposicion") or {}).get("nombre") else ""),
                              g.get("PEM"), "; ".join(g.get("riesgos") or [])] for g in e["emergentes"]]))
        else:
            L.append("Sin emergentes identificados en este eslabón.")
        L.append("")
    L += ["## 4. Síntesis: dónde se captura el valor y qué eslabones evitar", "", m.get("sintesis") or "—", "",
          "---", f"*Mapa del Bloque B (Robot Investor). No es asesoramiento personalizado ni una recomendación de inversión; las opciones son "
                 f"encargos para los Bloques C.x, no valoraciones individuales. Toda cifra tiene su DAT-B o CALC-B en el anexo de datos "
                 f"(hojas Eslabones, Opciones_eslabon y Emergentes). data_cutoff {m['data_cutoff']}.*", ""]
    return "\n".join(L)


def _financiacion(f: Optional[Dict]) -> str:
    if not f or f.get("importe") is None:
        return "no publicada"
    partes = [f"{f.get('importe')} M{f.get('divisa') or ''}", f.get("ultima_ronda"), f.get("fecha")]
    return " · ".join(str(x) for x in partes if x)


def _pct(x) -> str:
    """Fracción como porcentaje legible («—» si no hay dato; nunca «None»)."""
    if x is None or x == "":
        return "—"
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    return f"{v * 100:.1f} %".replace(".", ",") if abs(v) <= 1.5 else f"{v:.1f} %".replace(".", ",")


def md_a_docx(md_ruta: Path, docx_ruta: Path) -> Optional[str]:
    """Copia .docx por conversión fiel del .md (pandoc si está disponible; si no, python-docx con encabezados, párrafos y
    tablas). Devuelve la ruta o None si no hay conversor (se declara)."""
    import subprocess
    if shutil.which("pandoc"):
        try:
            subprocess.run(["pandoc", str(md_ruta), "-f", "gfm", "-o", str(docx_ruta)], check=True, capture_output=True, timeout=120)
            return str(docx_ruta)
        except (subprocess.SubprocessError, OSError):
            pass
    try:
        from docx import Document
    except ImportError:
        return None
    doc = Document()
    filas: List[List[str]] = []

    def volcar():
        if filas:
            t = doc.add_table(rows=len(filas), cols=len(filas[0]))
            t.style = "Table Grid"
            for i, f in enumerate(filas):
                for j, c in enumerate(f[:len(filas[0])]):
                    t.cell(i, j).text = c
            filas.clear()
    for linea in md_ruta.read_text(encoding="utf-8").splitlines():
        if linea.startswith("|"):
            celdas = [c.strip() for c in linea.strip("|").split("|")]
            if not all(set(c) <= {"-", ":"} for c in celdas):
                filas.append(celdas)
            continue
        volcar()
        if linea.startswith("#"):
            n = len(linea) - len(linea.lstrip("#"))
            doc.add_heading(linea.lstrip("# ").strip(), level=min(n, 4))
        elif linea.strip() and linea.strip() != "```":
            doc.add_paragraph(linea.replace("**", ""))
    volcar()
    doc.save(str(docx_ruta))
    return str(docx_ruta)


# =============================================================================================================
# Informe de parada (7.11, 14.7, B.15) e informe de seguimiento (7.13, 14.8, B.14)
# =============================================================================================================
def informe_parada_md(inf: Dict, resumen: Optional[str] = None) -> str:
    L = [f"# Informe de parada · {inf['ambito']['nombre']}", "",
         f"**{inf['pet_id']}** · {inf['rec_id']} · {inf['run_id']} · fecha {inf['fecha']} · **data_cutoff {inf['data_cutoff']}** · "
         f"tipo de objeto {inf['ambito']['tipo_objeto']} · horizonte principal {inf['ambito']['horizonte_principal']}", "",
         f"**Resultado: DETENIDO_EN_PUERTA en {inf['puerta']} (capa {inf['capa']}).** Sugerencia del bloque: **{inf['sugerencia']}** · "
         f"veredicto registrado {inf['veredicto_registrado']}.", ""]
    if resumen:
        L += [resumen, ""]
    L += ["## 1. Por qué no merece seguir", ""] + [f"- {x}" for x in inf.get("por_que_no_merece_seguir") or []] + [""]
    L.append(_tabla(["Criterio", "Clase", "Detalle", "Evidencia", "Etiqueta"],
                    [[m["criterio"], m["clase"], m["detalle"], ", ".join((m.get("evidencia") or []) + (m.get("calculos") or [])), m["etiqueta"]]
                     for m in inf["motivos"]]))
    L += ["", "## 2. Qué lo cambiaría", ""] + [f"- {x}" for x in inf["que_lo_cambiaria"]]
    L += ["", "## 3. Sugerencia", "", f"**{inf['sugerencia']}**."]
    sp = inf.get("seguimiento_propuesto")
    if sp:
        L.append(f"Seguimiento propuesto (CT-B-29): frecuencia {sp['frecuencia']}; señales: {'; '.join(sp['senales_de_interes'])}"
                 + (f"; disparadores: {'; '.join(sp['disparadores'])}" if sp.get("disparadores") else "") + ".")
    pp = inf.get("puntuaciones_provisionales") or {}
    tc = inf["tiempo_consumo"]
    L += ["", "## 4. Lo que ya se sabe", ""] + [f"- {x}" for x in inf["lo_que_ya_se_sabe"]]
    L += ["", (f"Puntuaciones provisionales: A {pp.get('A')} · E {pp.get('E')}." if pp.get("A") is not None or pp.get("E") is not None
                  else "Puntuaciones provisionales: no calculadas (la parada es anterior a la capa 2).") + f" Tiempo {tc['minutos']} min · {tc['uc']} UC · por capa "
              + ", ".join(f"capa {k}: {v} min" for k, v in sorted((tc.get("por_capa_min") or {}).items())) + "."]
    fc = inf["forzar_continuacion"]
    L += ["", f"**Forzar la continuación:** posible hasta el {fc['posible_hasta']} (CT-B-04 o CT-B-28) desde el punto de control "
              f"{fc['checkpoint_id']}; estimación del resto p80 {fc['estimacion_resto_p80_min']} min. No se rebaja ningún umbral (R33)."]
    if inf.get("supuestos_aplicados"):
        L += ["", "Supuestos aplicados por falta de respuesta: " + "; ".join(f"{x['cns_id']}: {x['supuesto']}" for x in inf["supuestos_aplicados"])]
    L += ["", "---", f"*{inf['aviso']} No genera candidatos, encargos C.x ni pronósticos congelados (7.11).*", ""]
    return "\n".join(L)


def escribir_informe_parada(salida: Path, inf: Dict, md: str) -> Dict:
    d = Path(salida) / CARPETA_PARADA
    d.mkdir(parents=True, exist_ok=True)
    base = f"{inf['fecha']}_informe-parada_{inf['pet_id']}"
    (d / f"{base}.md").write_text(md, encoding="utf-8")
    (d / f"{base}.json").write_text(json.dumps(inf, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"markdown": str(d / f"{base}.md"), "json": str(d / f"{base}.json")}


def informe_seguimiento_md(inf: Dict, resumen: Optional[str] = None) -> str:
    L = [f"# Informe de seguimiento · {inf['objeto'].get('ambito') or inf['seg_id']}", "",
         f"**{inf['seg_id']}** · ciclo {inf['ciclo_id']} · {inf['run_id']} · fecha {inf['fecha']} · **data_cutoff {inf['data_cutoff']}**", "",
         f"**Semáforo: {inf['semaforo']}** · recomendación **{inf['recomendacion']}** · próximo ciclo {inf.get('proximo_ciclo') or '—'}.", ""]
    if resumen:
        L += [resumen, ""]
    L += [inf["resumen"], "", "## Qué ha cambiado", ""]
    L.append(_tabla(["Dimensión", "Antes", "Ahora", "Importancia"], [[x["dimension"], x["antes"], x["ahora"], x["importancia"]] for x in inf["que_ha_cambiado"]])
             if inf["que_ha_cambiado"] else "Sin cambios materiales en las dimensiones clave.")
    L += ["", "## Señales y disparadores", ""]
    L.append(_tabla(["Señal o disparador", "Valor", "Umbral", "Estado"],
                    [[f"{x['sig_id']} {x.get('nombre') or ''}", x.get("valor"), x.get("umbral"), x["estado"]] for x in inf["senales"]] +
                    [[f"{x['descripcion']} ({x['origen']})", "—", "—", x["estado"]] for x in inf["disparadores"]]))
    if inf["candidatos"]:
        L += ["", "## Candidatos entregados", "", _tabla(["Candidato", "Eslabón", "Cambio", "Estado"],
                                                          [[x["cand_id"], x.get("eslabon_id"), x.get("cambio"), x["estado"]] for x in inf["candidatos"]])]
    af = inf.get("actualizacion_F6") or {}
    L += ["", f"Biblioteca F6: {af.get('mkt_id')} {af.get('version') or ''} · dimensiones {', '.join(af.get('dimensiones') or []) or '—'}. "
              f"Alertas del Vigía incluidas: {', '.join(inf.get('alertas_vigia_incluidas') or []) or 'ninguna'}.",
          "", f"**Recomendación: {inf['recomendacion']}.** {inf['motivo']}"]
    if inf.get("peticion_sugerida"):
        ps = inf["peticion_sugerida"]
        L.append(f"Petición sugerida (no iniciada): nivel {ps.get('nivel')}, alcance «{ps.get('alcance')}», estimación p80 {ps.get('estimacion_min_p80')} min.")
    tc = inf["tiempo_consumo"]
    L += ["", f"Tiempo {tc['minutos']} min · {tc['uc']} UC.", "", "---", f"*{inf['nota']} No es una recomendación personal.*", ""]
    return "\n".join(L)


def escribir_informe_seguimiento(salida: Path, inf: Dict, md: str) -> Dict:
    d = Path(salida) / CARPETA_SEGUIMIENTO
    d.mkdir(parents=True, exist_ok=True)
    cc = inf["ciclo_id"].rsplit("-", 1)[-1]
    base = f"{inf['fecha']}_informe-seguimiento_{inf['seg_id']}_c{cc}"
    (d / f"{base}.md").write_text(md, encoding="utf-8")
    (d / f"{base}.json").write_text(json.dumps(inf, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"markdown": str(d / f"{base}.md"), "json": str(d / f"{base}.json")}


# =============================================================================================================
# Anexo (HT-10)
# =============================================================================================================
def datos_anexo(c, st: Dict, p: Dict) -> Dict:
    universo = {}
    for t in st["tipos_aplicables"]:
        s = st["seleccion"].get(t) or {}
        top = {x["cand_id"]: x for x in (p["candidatos_por_tipo"][t].get("top_n") or [])}
        alt = set(p["candidatos_por_tipo"][t].get("alternativas") or [])
        filas = []
        for cid, cd in (s.get("candidatos") or {}).items():
            f = cd["_fila"]
            fila = {"tipo_activo": t, "cand_id": cid, "id": f.get("id"), "nombre": f.get("nombre"), "isin": f.get("isin"), "mercado": f.get("mercado"),
                    "divisa": f.get("divisa"), "subcluster": f.get("subcluster"), "emisor": f.get("emisor"), "invertible": True,
                    "pureza": cd.get("pureza"), "pureza_metodo": f.get("pureza_metodo"), "fecha_dato": (cd.get("_precio") or {}).get("ultima_fecha_precio"),
                    "S": cd.get("S"), "ic90_S_inf": (cd.get("ic90_S") or [None])[0], "ic90_S_sup": (cd.get("ic90_S") or [None, None])[1],
                    "en_top_n": cid in top, "alternativa": cid in alt, "veredicto": (top.get(cid) or {}).get("veredicto") or
                    ("SECUNDARIO" if cid in alt else None), "alertas": [a["senal"] for a in cd.get("alertas") or []]}
            if cid in top:
                fila.update({"rango": top[cid]["rango"], "ic90_rango_inf": top[cid]["ic90_rango"][0], "ic90_rango_sup": top[cid]["ic90_rango"][1],
                             "frontera": top[cid]["frontera"]})
            for k in ht03.COMPONENTES_S:
                v = (cd.get("componentes") or {}).get(k)
                fila[f"comp_{k}"] = None if v in ("NA", "NE") else v
            for k, v in (cd.get("_metricas") or {}).items():
                fila[k] = v
            filas.append(fila)
        u = st["universos"][t]
        for e in u["excluidos"]:
            filas.append({"tipo_activo": t, "id": e["id"], "nombre": e["nombre"], "isin": e.get("isin"), "invertible": False,
                          "motivo_exclusion": e["motivo"], "detalle_exclusion": e.get("detalle"), "veredicto": "EXCLUIDO"})
        universo[t] = filas
    cifras, artefactos = [], []
    pet = st["pet_id"]
    for e in c.alm.leer("RC"):
        if e.get("tipo_entrada") != "CALC" or e["_fecha"] > c.ent.as_of:
            continue
        artefactos.append({"calc_id": e["id"], "metodo": e["metodo"], "modulo": e["modulo"], "perfil": e.get("perfil"), "plan_calculo": e.get("plan_calculo"),
                           "semilla": e.get("semilla"), "fecha_corte": e.get("fecha_corte"), "huella_datos": e.get("huella_datos"),
                           "insumos": json.dumps(e.get("insumos"), ensure_ascii=False)[:300], "como_reproducir": e.get("como_reproducir")})
    esc = st["escenarios_motor"]
    if esc.get("disponible"):
        for k in ("p10", "p50", "p90", "RE"):
            cifras.append({"id": f"{esc['calc_id']}:{k}", "descripcion": f"Escenarios: {k}", "valor": esc[k], "unidad": "fracción" if k != "RE" else "0–100",
                           "fecha": p["data_cutoff"], "fuente": "Motor MC-B08", "dat_calc": esc["calc_id"], "etiqueta": "[INTERPRETACIÓN]",
                           "clase_cifra": "estimacion_estadistica", "dimension": "D12"})
    for k, v in (st["indicador_metricas"] or {}).items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            cifras.append({"id": f"{st['dat']['indicador']}:{k}", "descripcion": f"Indicador {st['indicador']['simbolo']}: {k}", "valor": round(v, 6),
                           "unidad": "", "fecha": p["data_cutoff"], "fuente": "HT-01", "dat_calc": st["dat"]["indicador"], "etiqueta": "[HECHO]",
                           "clase_cifra": "determinista", "dimension": "D9"})
    fuentes = []
    usados = set(st.get("referencias_metodo") or [])
    for rid in sorted(usados):
        f = c.ent.refs.por_id(rid)
        if f:
            fuentes.append({"ref_id": rid, "nombre": f["titulo"], "archivo": f["archivo"], "tematica": f["area"], "nivel": f["nivel"], "q": f["q"],
                            "url": f.get("url"), "fecha_consulta": c.ent.as_of, "uso": "método"})
    fuentes.append({"ref_id": "HT-01", "nombre": f"Proveedor de datos {c.ent.prov.nombre}", "archivo": "HT-01", "nivel": "A", "uso": "precios y series"})
    return {"universo": universo, "cifras": cifras, "fuentes": fuentes, "sensibilidades": p.get("sensibilidades"), "artefactos": artefactos}


# =============================================================================================================
# F9 · Redacción
# =============================================================================================================
def redactar(c, st: Dict) -> None:
    if st.get("bloqueado"):
        return
    p = st["paquete"]
    v = p["veredicto"]["valor"]
    fase = st.get("fase_division")
    r = c.inv.llamar("AG-B17", "CT-B-20", "redaccion",
                     {"pet_id": p["pet_id"], "veredicto": v, "nombre_llano": p["ambito"]["nombre_llano"], "puntuaciones": p["puntuaciones"],
                      "riesgo_1a5": p["riesgo_1a5"], "horizonte": p["estrategia"]["horizonte_dominante"], "tesis": p["tesis"]["enunciado"],
                      "riesgos": p["riesgos"], "cadena": p["despliegue_estructural"]["mapa_cadena"]},
                     "Redacta los textos llanos del informe visual (frases ≤ 20 palabras; Fernández-Huerta ≥ 70; sin nombres de "
                     "valores) y la tesis en tres frases del memorando. No añadas afirmaciones.",
                     {"frases_30s": "array", "por_que": "string", "riesgos_llanos": "array"}, c._ctx("AG-B17"), st["run_id"])
    textos = {k: v_ for k, v_ in r.items() if not k.startswith("_")}
    html_v = informe_visual(c.cfg, p, textos, fase)
    leg = ht07.analizar(html_v, es_html=True)
    if leg["fernandez_huerta"] is None or leg["fernandez_huerta"] < 70 or leg["pct_frases_mas_de_20"] > 5:
        r2 = c.inv.llamar("AG-B17", "CT-B-20", "redaccion", {"pet_id": p["pet_id"], "veredicto": v, "nombre_llano": p["ambito"]["nombre_llano"],
                                                              "reescribir": True, "legibilidad": leg["fernandez_huerta"]},
                          "Reescribe los textos con palabras más cortas y frases de menos de 15 palabras.", {"frases_30s": "array"},
                          c._ctx("AG-B17"), st["run_id"])
        textos.update({k: v_ for k, v_ in r2.items() if not k.startswith("_")})
        html_v = informe_visual(c.cfg, p, textos, fase)
        leg = ht07.analizar(html_v, es_html=True)
        if leg["fernandez_huerta"] is None or leg["fernandez_huerta"] < 70 or leg["pct_frases_mas_de_20"] > 5:
            textos.update(TEXTOS_SEGUROS)
            textos["glosario"] = []
            html_v = informe_visual(c.cfg, p, textos, fase)
            leg = ht07.analizar(html_v, es_html=True)
    # Tiempo hasta el cierre (incluye F9 y F10 estimadas) y autorización de salida
    tec = informe_tecnico(p, st, fase)
    memo = memorando(p, textos, fase)
    borr = c.ent.salida / ".borradores" / p["pet_id"]
    rutas = {}
    for k in CARPETAS:
        carpeta = borr / CARPETAS[k][0]
        carpeta.mkdir(parents=True, exist_ok=True)
        rutas[k] = str(carpeta / nombre_entregable(p["fecha"], k, p["pet_id"], fase))
    Path(rutas["informe_tecnico"]).write_text(tec, encoding="utf-8")
    Path(rutas["informe_visual"]).write_text(html_v, encoding="utf-8")
    Path(rutas["memorando"]).write_text(memo, encoding="utf-8")
    mapa_md = mapa_eslabones_md(p)
    Path(rutas["mapa_eslabones"]).write_text(mapa_md, encoding="utf-8")
    Path(rutas["mapa_eslabones"]).with_suffix(".json").write_text(json.dumps(p["mapa_cadena_valor"], ensure_ascii=False, indent=1), encoding="utf-8")
    if not md_a_docx(Path(rutas["mapa_eslabones"]), Path(rutas["mapa_eslabones"]).with_suffix(".docx")):
        p["limitaciones"].append("Copia .docx del mapa por eslabón no generada: sin conversor disponible (se entrega el Markdown)")
    anexo = ht10.generar_anexo(p, Path(rutas["anexo_datos"]).parent, Path(rutas["anexo_datos"]).stem, datos_anexo(c, st, p))
    auts = c.alm.nuevo_id("AUTS-B")
    p["auditoria"]["autorizacion_salida"] = auts
    Path(rutas["paquete_json"]).write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    g3 = ht09.validar(p, informe_visual=html_v, informe_tecnico=tec, memorando=memo, anexo=anexo["xlsx"], rutas=rutas,
                      esquema=esquema_paquete(c.cfg), f2=extracto_f2(c, p["pet_id"]),
                      parametros_f10={"methodology_version": c.ent.f10().get("methodology_version")}, preguntas=st["plan"]["preguntas"],
                      mapa_eslabones=mapa_md, f1=c.alm.estado("F1", tipo="CONSULTA_BROKER"))
    c.alm.escribir("HA", "AG-B21", {"tipo_entrada": "G3V", "id": c.alm.nuevo_id("G3V-B"), "pet_id": p["pet_id"], "run_id": st["run_id"],
                                    "pasada": "FIDELIDAD_ENTREGABLES", "dictamen": g3["dictamen"], "resumen": g3["resumen"], "motivo": g3["motivo"],
                                    "fallos": [{"id": x["id"], "clase": x.get("clase_fallo"), "detalles": x.get("detalles")}
                                               for x in g3["comprobaciones"] if x["resultado"] == "FALLA"],
                                    "legibilidad": {"fernandez_huerta": leg["fernandez_huerta"], "pct_frases_mas_de_20": leg["pct_frases_mas_de_20"]}})
    st["g3_fidelidad"] = {"dictamen": g3["dictamen"], "resumen": g3["resumen"], "motivo": g3["motivo"],
                          "fallos": [x for x in g3["comprobaciones"] if x["resultado"] == "FALLA"]}
    if g3["dictamen"] == "BLOQUEADO":
        st["bloqueado"] = "G3_FIDELIDAD"
        return
    c.alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUTORIZACION_SALIDA", "id": auts, "pet_id": p["pet_id"], "dictamen_g3": g3["dictamen"]})
    st["borradores"] = rutas
    st["legibilidad"] = {"fernandez_huerta": leg["fernandez_huerta"], "pct_frases_mas_de_20": leg["pct_frases_mas_de_20"]}


# =============================================================================================================
# F10 · Entrega y registro
# =============================================================================================================
def entregar(c, st: Dict) -> None:
    alm, ent = c.alm, c.ent
    p = st["paquete"]
    fase = st.get("fase_division")
    if st.get("bloqueado"):
        estado = "BLOQUEADO_AUDITORIA"
        c._estado_pet(st, estado, motivo=st["bloqueado"])
        entrega = {"pet_id": p["pet_id"], "run_ids": p["run_ids"], "rec_id": None, "estado_peticion": estado, "motivo": st["bloqueado"],
                   "estado_g3": (st.get("g3_fidelidad") or st.get("g3") or {}).get("dictamen"),
                   "opciones": ["ampliar el tiempo para subsanar", "aceptar un alcance reducido", "cancelar"]}
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "ENTREGA", "id": alm.nuevo_id("ENT-B"), "pet_id": p["pet_id"], "ct_b_02": entrega})
        st["resultado"] = entrega
        return
    rutas = {}
    for k, src in st["borradores"].items():
        carpeta = ent.salida / CARPETAS[k][0]
        carpeta.mkdir(parents=True, exist_ok=True)
        dst = carpeta / Path(src).name
        shutil.copy2(src, dst)
        if k == "anexo_datos":
            csv_src = Path(src).parent / (Path(src).stem + "_csv")
            if csv_src.exists():
                shutil.copytree(csv_src, carpeta / csv_src.name, dirs_exist_ok=True)
        rutas[k] = str(dst)
        if k == "mapa_eslabones":
            for ext in (".json", ".docx"):
                if Path(src).with_suffix(ext).exists():
                    shutil.copy2(Path(src).with_suffix(ext), dst.with_suffix(ext))
                    rutas[f"mapa_eslabones{ext.replace('.', '_')}"] = str(dst.with_suffix(ext))
    shutil.rmtree(ent.salida / ".borradores" / p["pet_id"], ignore_errors=True)
    v = p["veredicto"]
    prior = v.get("prioritarios_por_bloque_C") or {}
    entrega = {"pet_id": p["pet_id"], "run_ids": p["run_ids"], "rec_id": p["rec_id"], "entregables": rutas,
               "resumen": {"veredicto": v["valor"], "A": p["puntuaciones"]["A"], "E": p["puntuaciones"]["E"], "C": p["puntuaciones"]["C"],
                           "resultado_del_analisis": v["resultado_del_analisis"], "prioritarios_por_bloque_C": prior,
                           "siguiente_paso_sugerido": v["siguiente_paso_sugerido"], "relevancia_decisional": v["relevancia_decisional"],
                           "eslabones_destacados": [e["eslabon_id"] for e in p["mapa_cadena_valor"]["eslabones"]
                                                    if e.get("opciones") and ht03.eslabon_cualifica(e)["cualifica"]][:3]},
               "puertas_viabilidad": {**p["capas"]["puertas_viabilidad"], "continuacion_forzada": p["capas"]["continuacion_forzada"]},
               "supuestos_aplicados": p.get("supuestos_aplicados") or [],
               "estado_g3": st["g3_fidelidad"]["dictamen"], "auditoria": {"realizada": p["auditoria"]["realizada"], "reservas": p["reservas_auditoria"]},
               "tiempo": {"estimado_p80_min": st["estimacion"]["minutos_p80"], "real_min": round(st["consumido_min"], 1),
                          "por_capa_min": dict(st.get("minutos_capa") or {}), "autorizaciones": st["autorizaciones"]},
               "consumo_uc": round(c.inv.consumo()["uc"] + c.motor.uc, 1), "estado_peticion": "DIVIDIDA" if fase == 1 else "ENTREGADA", "fase": fase,
               "autorizacion_salida": p["auditoria"]["autorizacion_salida"]}
    (ent.salida / f"{p['fecha']}_entrega_{p['pet_id']}{'_fase' + str(fase) if fase else ''}.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=1), encoding="utf-8")
    alm.escribir("F1", "AG-B01", {"tipo_entrada": "ENTREGA", "id": alm.nuevo_id("ENT-B"), "pet_id": p["pet_id"], "ct_b_02": entrega,
                                  "tiempos_por_tramo": st["tiempos"], "estimacion_fases": st.get("estimacion_fases"), "uc_por_tramo": st.get("uc_tramos")})
    # F3: REC-B y CAND-B (Director); F4: PRG-B (Prospectiva); F6: MKT-B (Director); agenda HT-05 (Coordinador)
    alm.escribir("F3", "AG-B02", {"tipo_entrada": "REC", "id": p["rec_id"], "pet_id": p["pet_id"], "ambito": p["ambito"], "tipo_objeto": p["ambito"]["tipo_objeto"],
                                  "veredicto": v["valor"], "A": p["puntuaciones"]["A"], "E": p["puntuaciones"]["E"], "C": p["puntuaciones"]["C"],
                                  "resultado_del_analisis": v["resultado_del_analisis"], "puertas_viabilidad": p["capas"]["puertas_viabilidad"],
                                  "continuacion_forzada": p["capas"]["continuacion_forzada"], "mapa_cadena_valor": p["mapa_cadena_valor"],
                                  "horizonte": v["horizonte"], "tesis": p["tesis"]["enunciado"], "plan_de_seguimiento": p["plan_de_seguimiento"],
                                  "estado_vigilancia": "VIGENTE" if v["valor"] != "DESCARTAR" else "CERRADA", "fase": fase,
                                  "indicador": p["ambito"]["indicador_seguimiento"], "referencia": p["ambito"]["referencia_comparacion"]})
    for t in TIPOS_ACTIVO:
        d = p["candidatos_por_tipo"][t]
        if not d.get("aplicable"):
            continue
        s = st["seleccion"].get(t) or {}
        top = {x["cand_id"]: x for x in d.get("top_n") or []}
        for cid, cd in (s.get("candidatos") or {}).items():
            x = top.get(cid)
            alm.escribir("F3", "AG-B02", {"tipo_entrada": "CAND", "id": cid, "rec_id": p["rec_id"], "pet_id": p["pet_id"], "tipo_activo": t,
                                          "instrumento_id": f"{p['pet_id']}::{cd['_fila']['id']}", "nombre": cd["_fila"].get("nombre"),
                                          "simbolo": cd["_fila"].get("simbolo"), "S": cd.get("S"), "en_top_n": cid in top,
                                          "eslabon_id": cd.get("eslabon_id"), "pureza_eslabon": cd.get("pureza_eslabon"),
                                          "en_tabla_eslabon": cid in {o["cand_id"] for e in p["mapa_cadena_valor"]["eslabones"] for o in e["opciones"]},
                                          "rango": x["rango"] if x else None, "veredicto": x["veredicto"] if x else ("SECUNDARIO" if cid in d["alternativas"] else "EXCLUIDO"),
                                          "estado_vigilancia": "VIGENTE" if x else "CERRADO"})
    for pr in st["pronosticos"]:
        alm.escribir("F4", "AG-B13", {"tipo_entrada": "ALTA", "id": pr["prg_id"], "pet_id": p["pet_id"], "rec_id": p["rec_id"],
                                      **{k: v_ for k, v_ in pr.items() if k != "prg_id" and not k.startswith("_")},
                                      "probabilidad_interna": pr.get("_prob_interna"), "estado": "ABIERTO",
                                      "top_n_simbolos": _simbolos_top(st, p, pr.get("tipo_activo")),
                                      "universo_simbolos": _simbolos_universo(st, pr.get("tipo_activo")),
                                      "universo_S": _universo_S(st, pr.get("tipo_activo"))})
    alm.escribir("F6", "AG-B02", {"tipo_entrada": "MKT", "id": p["ambito"]["mkt_id"], "mkt_clave": st["clave"], "pet_id": p["pet_id"],
                                  "ambito": p["ambito"], "mapa_cadena": p["despliegue_estructural"]["mapa_cadena"],
                                  "mapa_cadena_valor": {**{k: v_ for k, v_ in p["mapa_cadena_valor"].items() if k != "eslabones"}, "eslabones": [
                                      {k: v_ for k, v_ in e.items() if k != "opciones"} for e in p["mapa_cadena_valor"]["eslabones"]]},
                                  "radar_emergentes": [g for e in p["mapa_cadena_valor"]["eslabones"] for g in e.get("emergentes") or []],
                                  "universos": {t: st["universos"][t]["tamano_invertible"] for t in st["tipos_aplicables"]},
                                  "caducidad_dias": {"D1": 365, "D4": 365, "D11": 365, "D2": 182, "D3": 182, "D5": 182, "D6": 91, "D8": 91,
                                                     "D7": 30, "D12": 30, "D9": 91 if v["horizonte"] == "H5" else 30, "D10": 7, "universos": 30,
                                                     "radar_emergentes": 91}, "rgm_id": p["regimen"]["rgm_id"],
                                  "veredicto": v["valor"]})
    alm.escribir("F1", "AG-B01", {"tipo_entrada": "AGENDA", "id": alm.nuevo_id("AGE-B"), "pet_id": p["pet_id"], "rec_id": p["rec_id"],
                                  "vigia_frecuencia": p["plan_de_seguimiento"]["frecuencia"], "vencimientos": [x["fecha_resolucion"] for x in st["pronosticos"]],
                                  "nota": "HT-05: rondas del Vigía y vencimientos (no programa análisis)"})
    if fase == 1:
        # Fase 2 del análisis dividido: nueva solicitud de autorización con su estimación
        st2 = json.loads(json.dumps(st, default=str))
        st2["fase_division"] = 2
        st2["siguiente"] = "FASE2"
        st2["recortes"] = [r for r in st2.get("recortes", []) if not r.startswith("Análisis dividido")]
        st2.pop("borradores", None)
        st2.pop("paquete", None)
        aut = alm.nuevo_id("AUT-B")
        ckp = alm.nuevo_id("CKP")
        from .herramientas import ht08
        ht08.guardar_punto_control(alm.dir_puntos_control, ckp, st2)
        est2 = ht08.estimar(c._plan_ht08(st), c.pt.get("modelo"), ["F4", "F5", "F6", "F7", "F8", "F9", "F10"])
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "AUTORIZACION", "id": aut, "pet_id": p["pet_id"], "tipo": "SOLICITUD", "puerta": "PTA",
                                      "momento": "EN_EJECUCION", "estado": "PENDIENTE", "fase_division": 2, "estimacion": est2,
                                      "justificacion": {"que_aporta": "Selección de candidatos, refutación de finalistas y encargos C.x (fase 2)"},
                                      "opciones": [{"opcion": "CONTINUAR", "minutos_p80": est2["minutos_p80"]}, {"opcion": "CANCELAR"}],
                                      "checkpoint_reanudacion": ckp, "solicitada": alm.reloj.ahora()})
        entrega["fase_2"] = {"aut_id": aut, "estimacion": est2}
        c._estado_pet(st, "DIVIDIDA", aut_id=aut)
    else:
        c._estado_pet(st, "ENTREGADA", rec_id=p["rec_id"])
    st["resultado"] = entrega


def _simbolos_top(st, p, tipo) -> List[str]:
    if not tipo:
        return []
    s = st["seleccion"].get(tipo) or {}
    return [s["candidatos"][x["cand_id"]]["_fila"].get("simbolo") for x in (p["candidatos_por_tipo"][tipo].get("top_n") or [])
            if x["cand_id"] in (s.get("candidatos") or {})]


def _simbolos_universo(st, tipo) -> List[str]:
    if not tipo:
        return []
    return [cd["_fila"].get("simbolo") for cd in ((st["seleccion"].get(tipo) or {}).get("candidatos") or {}).values()]


def _universo_S(st, tipo) -> Dict:
    if not tipo:
        return {}
    return {cd["_fila"].get("simbolo"): cd.get("S") for cd in ((st["seleccion"].get(tipo) or {}).get("candidatos") or {}).values()
            if cd.get("S") is not None}
