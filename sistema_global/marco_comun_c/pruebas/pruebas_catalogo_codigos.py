"""Pruebas de coherencia del catálogo de códigos (V0.61, Pieza 2 del kit 2). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_catalogo_codigos.py

Comprueba que `validador/catalogo_codigos.py` y el código real no se separan: todo código que aparece en el
código está en el catálogo con su módulo, todo código del catálogo aparece en el código (salvo los
retirados con su motivo), las colisiones entre módulos son solo las admitidas con su explicación, todo
prefijo usado está en el registro del LEEME, cada aviso de PRIORIDAD_AVISO está en el catálogo con esa
prioridad, ningún texto está vacío y los "(sin documentar)" son menos de 10. No depende del orden de
lectura de ficheros (la función del catálogo los ordena) y es determinista.

A las 18 comprobaciones de la pieza, la revisión independiente añadió cinco regresiones (r01 a r05): los
dos choques reales llevan textos distintos por módulo y su par está admitido (r01); toda regla Q/K con
efecto BLOQUEA tiene un BLOQUEO real en `k_calidad` y toda AVISO advierte sin bloquear (r02); las reglas
que REDUCEN no son RECHAZA (r03); los códigos con muchas emisiones distintas no citan una ruta literal y
las filas declaradas "familia" no copian un solo mensaje (r04); y el recuento de pares admitidos es el
que declaran los documentos (r05).
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from catalogo_codigos import (CATALOGO, CHOQUES_REALES, COLISIONES_ADMITIDAS, EFECTOS,   # noqa: E402
                              REGLAS_QUE_REDUCEN, codigos_en_el_codigo, como_markdown,
                              prefijos_del_leeme, sitios_de_emision)
from orquestador import PRIORIDAD_AVISO   # noqa: E402
from pruebas_orquestador import Arnes   # noqa: E402

EXPRESION = re.compile(r"[A-Z]{1,2}-\d{2}")
LEEME = AQUI.parent / "LEEME.md"
VALIDADOR = AQUI.parent / "validador"
PRIORIDADES = {"ALTA", "MEDIA", "BAJA"}
RUTA = re.compile(r"[a-z_]+(?:\.[a-z_]+)+")   # una ruta de mensaje tipo condiciones_entrada.resto_parcial


def main():
    h = Arnes()
    codigos = codigos_en_el_codigo(VALIDADOR)
    emision = sitios_de_emision(VALIDADOR)
    claves = set(CATALOGO)
    retirados = {k for k, v in CATALOGO.items() if v.get("retirado")}

    # ---------------------------------------------------------------- estructura del catálogo
    forma_ok = (len(claves) > 0
                and all(isinstance(m, str) and isinstance(c, str) and EXPRESION.fullmatch(c)
                        for m, c in claves)
                and all(isinstance(v, dict) and {"que", "efecto", "desde"} <= set(v)
                        for v in CATALOGO.values()))
    h.chk("catalogo_no_vacio_y_con_la_forma_pedida", forma_ok, len(CATALOGO))

    faltan = sorted(codigos - claves)
    h.chk("todo_codigo_en_el_codigo_esta_en_el_catalogo", not faltan, faltan[:8] or "ninguno falta")

    muertos = sorted(claves - codigos - retirados)
    h.chk("todo_codigo_del_catalogo_aparece_en_el_codigo_salvo_los_retirados", not muertos,
          muertos[:8] or "ninguno muerto")

    mal_retirados = [k for k in retirados
                     if not CATALOGO[k].get("motivo") or k in codigos]
    h.chk("los_retirados_llevan_motivo_y_no_aparecen_en_el_codigo", not mal_retirados, mal_retirados[:5])

    # ---------------------------------------------------------------- colisiones entre módulos
    por_codigo = {}
    for m, c in codigos:
        por_codigo.setdefault(c, set()).add(m)
    for k, v in CATALOGO.items():
        por_codigo.setdefault(k[1], set()).add(k[0])
    compartidos = {c: mods for c, mods in por_codigo.items() if len(mods) > 1}
    pares_sin_admitir = []
    for c, mods in compartidos.items():
        mods = sorted(mods)
        for i in range(len(mods)):
            for j in range(i + 1, len(mods)):
                par = (mods[i], mods[j])
                if par not in COLISIONES_ADMITIDAS and (par[1], par[0]) not in COLISIONES_ADMITIDAS:
                    pares_sin_admitir.append((c, par))
    h.chk("las_colisiones_son_solo_las_admitidas_con_su_explicacion", not pares_sin_admitir,
          pares_sin_admitir[:6] or f"{len(COLISIONES_ADMITIDAS)} pares admitidos, todos con explicación")

    sin_explicacion = [p for p, txt in COLISIONES_ADMITIDAS.items()
                       if not isinstance(txt, str) or len(txt) < 20]
    h.chk("cada_colision_admitida_lleva_explicacion", not sin_explicacion, sin_explicacion[:5])

    # ---------------------------------------------------------------- prefijos y LEEME
    prefijos_leeme = prefijos_del_leeme(LEEME)
    usados = {c.split("-")[0] for _, c in claves}
    h.chk("todo_prefijo_usado_esta_en_el_registro_del_leeme", usados <= prefijos_leeme,
          sorted(usados - prefijos_leeme) or f"{len(prefijos_leeme)} prefijos registrados")
    faltan_en_leeme = {"PE", "DI", "MG", "RL", "K", "CL"} - prefijos_leeme
    h.chk("el_leeme_registra_los_prefijos_de_t03_y_de_la_clave_tras_esta_pieza", not faltan_en_leeme,
          sorted(faltan_en_leeme) or f"PE, DI, MG, RL, K y CL registrados ({sorted(prefijos_leeme)})")
    sin_uso = sorted(prefijos_leeme - usados)
    h.chk("el_registro_del_leeme_no_registra_prefijos_sin_uso", not sin_uso, sin_uso[:6])

    # ---------------------------------------------------------------- prioridades de los avisos
    mal_prioridad = [(c, PRIORIDAD_AVISO[c], CATALOGO.get(("orquestador", c), {}).get("prioridad"))
                     for c in PRIORIDAD_AVISO
                     if CATALOGO.get(("orquestador", c), {}).get("prioridad") != PRIORIDAD_AVISO[c]]
    h.chk("cada_aviso_de_prioridad_aviso_esta_en_el_catalogo_con_esa_prioridad", not mal_prioridad,
          f"{len(PRIORIDAD_AVISO)} avisos comprobados" if not mal_prioridad else mal_prioridad[:5])
    avisos = [(k, v.get("prioridad")) for k, v in CATALOGO.items()
              if k[0] == "orquestador" and k[1].startswith("O-")]
    mal_avisos = [k for k, p in avisos if p not in PRIORIDADES]
    h.chk("los_avisos_del_orquestador_llevan_prioridad_valida", len(avisos) == 45 and not mal_avisos,   # V0.75 (T-76 r03): O-44, falta comparar el mes de juicio. V0.74 (T-97): O-43, tope anual de gasto. V0.70 (T-75): O-40, sequía; V0.71 (T-76): O-41, cartera sombra; V0.73: O-42, sombra sin comparar
          f"{len(avisos)} avisos" if not mal_avisos else mal_avisos[:5])

    # ---------------------------------------------------------------- textos y efectos
    vacios = [k for k, v in CATALOGO.items() if not isinstance(v["que"], str) or not v["que"].strip()]
    h.chk("ningun_que_esta_vacio", not vacios, vacios[:5])
    sin_doc = [k for k, v in CATALOGO.items() if v["que"] == "(sin documentar)"]
    h.chk("los_sin_documentar_son_menos_de_diez", len(sin_doc) < 10,
          f"{len(sin_doc)} sin documentar" if sin_doc else "todos documentados")
    mal_efecto = [k for k, v in CATALOGO.items() if v["efecto"] not in EFECTOS]
    h.chk("el_efecto_es_siempre_uno_de_los_declarados", not mal_efecto, mal_efecto[:5])

    # ---------------------------------------------------------------- como_markdown y determinismo
    md = como_markdown()
    filas = [ln for ln in md.splitlines() if ln.startswith("| `")]
    claves_md = []
    for ln in filas:
        celdas = [x.strip() for x in ln.split("|")]
        m, c = celdas[1].strip("`"), celdas[2].strip("`")
        claves_md.append((m, c))
    h.chk("como_markdown_devuelve_toda_la_tabla_ordenada_por_modulo_y_codigo",
          len(filas) == len(CATALOGO) and claves_md == sorted(CATALOGO),
          f"{len(filas)} filas" if claves_md == sorted(CATALOGO) else "orden o filas distintas")

    de_nuevo = codigos_en_el_codigo(VALIDADOR)
    h.chk("codigos_en_el_codigo_determinista_y_sin_el_propio_catalogo",
          de_nuevo == codigos and not any(m == "catalogo_codigos" for m, _ in codigos),
          f"{len(codigos)} pares, dos llamadas iguales")

    # sonda: ast, no grep (un comentario no cuenta; una cadena sí; un .py roto no lanza)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / "sonda.py").write_text(
            "# O-99 esto va en un comentario y no cuenta\n"
            "X = \"O-98\"   # tampoco cuenta este comentario\n"
            "Y = f\"mencion suelta O-97 dentro de un mensaje más largo\"\n",
            encoding="utf-8")
        (raiz / "roto.py").write_text("def f(:\n", encoding="utf-8")   # sintaxis rota: no lanza
        hallados = codigos_en_el_codigo(raiz)
    h.chk("codigos_en_el_codigo_usa_ast_y_no_grep_comentarios_o_ficheros_rotos",
          hallados == {("sonda", "O-98")} and ("sonda", "O-97") not in hallados
          and ("sonda", "O-99") not in hallados and not any(m == "roto" for m, _ in hallados),
          sorted(hallados) or "vacío")

    h.chk("e06_esta_en_el_catalogo_como_retirada_con_su_motivo",
          CATALOGO.get(("validar_encargo", "E-06"), {}).get("retirado") is True
          and "CT-G-01 0.2.0" in CATALOGO[("validar_encargo", "E-06")]["motivo"],
          CATALOGO[("validar_encargo", "E-06")]["motivo"])

    # ---------------------------------------------------------------- regresiones de la revisión (r01-r05)
    # r01: los choques reales declarados (T-70, T-71) llevan textos distintos por módulo y su par está
    # admitido; ninguna explicación «CHOQUE REAL» cita una deuda sin choque declarado.
    mal_choques = []
    for (m1, m2, c), deuda in CHOQUES_REALES.items():
        fa, fb = CATALOGO.get((m1, c)), CATALOGO.get((m2, c))
        admite = COLISIONES_ADMITIDAS.get((m1, m2)) or COLISIONES_ADMITIDAS.get((m2, m1))
        if not fa or not fb or fa["que"] == fb["que"] or not admite \
                or not any(deuda in txt for txt in COLISIONES_ADMITIDAS.values()):
            mal_choques.append((m1, m2, c, deuda))
    sin_deuda = [p for p, txt in COLISIONES_ADMITIDAS.items()
                 if "CHOQUE REAL" in txt and not any(d in txt for d in CHOQUES_REALES.values())]
    h.chk("r01_los_pares_con_choque_real_tienen_textos_distintos_por_modulo",
          not mal_choques and not sin_deuda,
          mal_choques[:4] or sin_deuda[:4] or "T-70 y T-71: textos distintos por módulo y pares admitidos")

    # r02: el efecto de las reglas Q/K es el real de k_calidad: BLOQUEA exige un BLOQUEO real (llamada con
    # "BLOQUEO" o el envoltorio _bloqueo, que devuelve BLOQUEO) y AVISO exige advertir sin bloquear nunca.
    qk = sorted(k for k in CATALOGO
                if k[0] == "k_calidad" and (k[1].startswith("Q-") or k[1].startswith("K-")))
    sin_bloqueo, aviso_falso = [], []
    for m, c in qk:
        d = emision.get((m, c), {"resultados": set(), "envoltorios": set()})
        bloquea = "BLOQUEO" in d["resultados"] or any("bloqueo" in e.lower() for e in d["envoltorios"])
        if CATALOGO[(m, c)]["efecto"] == "BLOQUEA" and not bloquea:
            sin_bloqueo.append((m, c))
        if CATALOGO[(m, c)]["efecto"] == "AVISO" and (bloquea or "ADVERTENCIA" not in d["resultados"]):
            aviso_falso.append((m, c))
    h.chk("r02_el_efecto_BLOQUEA_de_las_reglas_Q_exige_un_BLOQUEO_real",
          not sin_bloqueo and not aviso_falso,
          sin_bloqueo[:5] or aviso_falso[:5]
          or f"{len(qk)} reglas Q/K: BLOQUEA con BLOQUEO real y AVISO advirtiendo sin bloquear")

    # r03: las reglas de F que aprueban con menos cantidad (REDUCIDO con cantidad_aprobada > 0) no son
    # RECHAZA: efecto REDUCE en control_f y sus copias del Orquestador, y ninguna otra fila lo lleva.
    txt_control_f = (VALIDADOR / "control_f.py").read_text(encoding="utf-8")
    pares_reduce = {(m, c) for c in REGLAS_QUE_REDUCEN for m in ("control_f", "orquestador")}
    mal_reduce = [(m, c) for m, c in sorted(pares_reduce)
                  if CATALOGO.get((m, c), {}).get("efecto") != "REDUCE"
                  or "recorta" not in CATALOGO.get((m, c), {}).get("que", "")]
    reduce_sobra = sorted(k for k, v in CATALOGO.items()
                          if v["efecto"] == "REDUCE" and k not in pares_reduce)
    sin_mapa = sorted(c for c in REGLAS_QUE_REDUCEN if f'("{c}"' not in txt_control_f)
    if "REDUCE" not in txt_control_f:
        sin_mapa.append("control_f.py sin el resultado REDUCE")
    h.chk("r03_las_reglas_que_REDUCEN_no_son_RECHAZA",
          not mal_reduce and not reduce_sobra and not sin_mapa,
          mal_reduce[:5] or reduce_sobra[:5] or sin_mapa[:5]
          or f"{len(REGLAS_QUE_REDUCEN)} reglas con REDUCE en control_f y orquestador")

    # r04: un código con cinco o más mensajes de emisión distintos no documenta un solo caso: su texto no
    # cita una ruta literal de un mensaje, y las filas declaradas "familia" no copian ni caben en uno.
    con_ruta, mal_familia, genericos = [], [], 0
    for k, d in sorted(emision.items()):
        fila = CATALOGO.get(k)
        if fila is None or len(d["mensajes"]) < 5:
            continue
        genericos += 1
        rutas = {t for msj in d["mensajes"] for t in RUTA.findall(msj)}
        if any(t in fila["que"] for t in rutas):
            con_ruta.append(k)
    for k, fila in sorted(CATALOGO.items()):
        if not fila.get("familia"):
            continue
        d = emision.get(k)
        if not d or len(d["mensajes"]) < 2:
            mal_familia.append((k[0], k[1], "sin mensajes distintos que justifiquen el texto de familia"))
            continue
        que = fila["que"].strip()
        if que in d["mensajes"] or any(que in msj for msj in d["mensajes"]):
            mal_familia.append((k[0], k[1], "el texto es (o cabe en) un solo mensaje de emisión"))
    h.chk("r04_codigos_con_muchas_emisiones_llevan_texto_de_familia",
          not con_ruta and not mal_familia,
          con_ruta[:5] or mal_familia[:5]
          or f"{genericos} códigos con >= 5 mensajes sin citar rutas; familia: O-00, O-01 y O-02 del orquestador")

    # r05: el recuento de pares admitidos es el que declaran Documento 0, LEEME y notas_briefing: si
    # cambia la lista, cambian los documentos (busca «dieciséis»).
    h.chk("r05_el_recuento_de_pares_admitidos_es_el_declarado", len(COLISIONES_ADMITIDAS) == 16,
          f"{len(COLISIONES_ADMITIDAS)} pares admitidos (los documentos declaran dieciséis)")

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CATALOGO CODIGOS:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
