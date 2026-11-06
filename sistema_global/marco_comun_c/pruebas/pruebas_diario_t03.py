"""Pruebas de T-03 (segunda parte, V0.43): el diario de operaciones. Lo anotado se vuelve a aplicar al arrancar y se llega
exactamente al mismo estado; los cortes en cualquier punto se recuperan; un diario roto o ajeno no se usa (DI-01 a DI-05).
Datos SIMULADOS.

Uso: python3 pruebas/pruebas_diario_t03.py
"""
import json
import os
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
from ejecucion_g import conciliar, ejecutar  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import broker  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

T = "2026-11-06T09:30:00+00:00"


def lineas(ruta):
    with open(ruta, encoding="ascii") as f:
        return [json.loads(x) for x in f.read().splitlines()]


def escribir(ruta, ls, sin_salto_final=False):
    texto = "".join(json.dumps(e, ensure_ascii=True, separators=(",", ":")) + "\n" for e in ls)
    with open(ruta, "w", encoding="ascii") as f:
        f.write(texto[:-1] if sin_salto_final else texto)


def recadenar(ls):
    """Rehace numeración, prev y hash de una lista de líneas (lo que haría quien edita el diario sabiendo cómo)."""
    prev, out = di.CERO, []
    for i, e in enumerate(ls, 1):
        e = {k: v for k, v in e.items() if k not in ("hash", "prev")}
        e["n"] = i
        x = di._linea(e, prev)
        out.append(x)
        prev = x["hash"]
    return out


def flujo(d, b):
    """Un flujo completo a través del diario: propuesta, F, autorizar, ejecutar con G y conciliar."""
    hasta(d, "PROPUESTA")
    assert autorizar_op(d, "EXP-0001", informe_f(d), AHORA)["ok"]
    assert ejecutar(d, "EXP-0001", b, AHORA)["ok"]
    conciliar(d, b, AHORA)


def main():
    h = Arnes()
    with tempfile.TemporaryDirectory() as tmp:
        def rutas(nombre):
            return os.path.join(tmp, nombre + ".estado.json"), os.path.join(tmp, nombre + ".diario")

        # -------------------------------------------------------------- lo normal: anotar, reabrir, mismo estado
        re_, rd = rutas("a")
        c = di.crear(nuevo(), re_, rd, T)
        d = c["diario"]
        h.chk("crear_deja_estado_y_un_punto", c["ok"] and os.path.exists(re_) and [x["tipo"] for x in lineas(rd)] == ["PUNTO"], c)
        flujo(d, broker())
        ls = lineas(rd)
        h.chk("cada_operacion_deja_OP_y_RES", len(ls) > 3 and all(ls[i]["tipo"] == "OP" and ls[i + 1]["tipo"] == "RES" and ls[i + 1]["op"] == ls[i]["n"]
                                                                  for i in range(1, len(ls), 2)), [x["tipo"] for x in ls][:8])
        h.chk("las_lecturas_no_se_anotan", (d.integridad(), d.contexto_f("EXP-0001", AHORA), d.cartera_f(), len(lineas(rd)))[-1] == len(ls))
        h.chk("los_metodos_que_cambian_son_los_de_seguro", {"autorizar", "registrar_cartera", "orden_entrada", "ejecutar", "barrer"} <= di.mutantes(d.orquestador)
              and not {"integridad", "contexto_f", "nivel", "comprobar_manual"} & di.mutantes(d.orquestador))
        a = di.abrir(re_, rd)
        h.chk("reabrir_llega_al_mismo_estado", a["ok"] and a["aplicadas"] == (len(ls) - 1) // 2 and pe.volcar(a["diario"].orquestador, T) == pe.volcar(d.orquestador, T),
              (a["codigo"], a["motivo"]))
        h.chk("el_reabierto_sigue_anotando", a["diario"].barrer("2026-11-06T10:00:00+00:00")["ok"] is not None and lineas(rd)[-1]["tipo"] == "RES"
              and lineas(rd)[-2]["metodo"] == "barrer")
        b2 = di.abrir(re_, rd)
        h.chk("y_se_reabre_otra_vez_igual", b2["ok"] and pe.volcar(b2["diario"].orquestador, T) == pe.volcar(a["diario"].orquestador, T))
        h.chk("las_rechazadas_tambien_se_anotan_y_reproducen", (lambda r: r["codigo"] == "O-16" and di.abrir(re_, rd)["ok"])(
            b2["diario"].registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": "2026-11-01T00:00:00+00:00"}, "G", "2026-11-01T00:00:00+00:00")))

        # -------------------------------------------------------------- punto de control
        re_, rd = rutas("p")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "PROPUESTA")
        antes = pe.volcar(d.orquestador, T)
        p = d.punto(T)
        h.chk("punto_deja_el_diario_en_un_punto", p["ok"] and [x["tipo"] for x in lineas(rd)] == ["PUNTO"] and lineas(rd)[0]["estado"] == p["huella"], p)
        assert autorizar_op(d, "EXP-0001", informe_f(d), AHORA)["ok"]
        a = di.abrir(re_, rd)
        h.chk("tras_el_punto_se_aplica_solo_lo_posterior", a["ok"] and a["aplicadas"] == len([x for x in lineas(rd) if x["tipo"] == "OP"])
              and pe.volcar(a["diario"].orquestador, T) == pe.volcar(d.orquestador, T) != antes, (a["codigo"], a.get("aplicadas")))

        # -------------------------------------------------------------- cortes
        re_, rd = rutas("c")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "PROPUESTA")
        referencia = pe.volcar(d.orquestador, T)
        ls = lineas(rd)
        escribir(rd, ls[:-1])   # corte tras aplicar la última operación y antes de anotar su RES
        a = di.abrir(re_, rd)
        h.chk("corte_antes_del_RES_se_aplica_y_se_completa", a["ok"] and pe.volcar(a["diario"].orquestador, T) == referencia and lineas(rd)[-1]["tipo"] == "RES"
              and len(lineas(rd)) == len(ls), (a["codigo"], a["motivo"]))
        escribir(rd, ls)
        con_media = json.dumps(ls[-1], ensure_ascii=True, separators=(",", ":"))[:20]
        with open(rd, "a", encoding="ascii") as f:
            f.write(con_media)   # corte escribiendo una línea nueva
        a = di.abrir(re_, rd)
        h.chk("linea_cortada_al_final_se_ignora_y_se_limpia", a["ok"] and a["linea_incompleta"] and pe.volcar(a["diario"].orquestador, T) == referencia
              and open(rd, encoding="ascii").read().endswith("\n") and len(lineas(rd)) == len(ls))
        h.chk("y_se_sigue_anotando_bien", a["diario"].barrer(AHORA) is not None and di.abrir(re_, rd)["ok"])
        escribir(rd, ls, sin_salto_final=True)   # la última entera pero sin salto de línea
        a = di.abrir(re_, rd)
        h.chk("ultima_entera_sin_salto_se_conserva", a["ok"] and not a["linea_incompleta"] and open(rd, encoding="ascii").read().endswith("\n")
              and pe.volcar(a["diario"].orquestador, T) == referencia)
        escribir(rd, ls)
        con_op = ls + [di._linea({"n": ls[-1]["n"] + 1, "tipo": "OP", "metodo": "barrer", "args": [AHORA], "kwargs": {}}, ls[-1]["hash"])]
        escribir(rd, con_op)   # corte tras anotar la OP y antes (o después) de aplicarla
        a = di.abrir(re_, rd)
        h.chk("corte_tras_anotar_la_OP_se_aplica_una_vez", a["ok"] and lineas(rd)[-1]["tipo"] == "RES" and lineas(rd)[-1]["op"] == con_op[-1]["n"]
              and sum(1 for x in lineas(rd) if x["tipo"] == "OP") == sum(1 for x in con_op if x["tipo"] == "OP"), (a["codigo"], a["motivo"]))

        # cortes durante el punto de control
        re_, rd = rutas("q")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "PROPUESTA")
        ref = pe.volcar(d.orquestador, T)
        ls = lineas(rd)
        huella_nueva = json.loads(ref)["huella"]
        fich_nuevo = __import__("hashlib").sha256(ref.encode("ascii")).hexdigest()
        escribir(rd, ls + [di._linea({"n": ls[-1]["n"] + 1, "tipo": "PUNTO", "estado": huella_nueva, "fichero": fich_nuevo}, ls[-1]["hash"])])   # el estado no llegó a guardarse
        a = di.abrir(re_, rd)
        h.chk("corte_antes_de_guardar_el_estado_usa_el_punto_anterior", a["ok"] and pe.volcar(a["diario"].orquestador, T) == ref, (a["codigo"], a["motivo"]))
        pe.guardar(d.orquestador, re_, T)   # el estado sí se guardó, pero el diario no llegó a reducirse
        a = di.abrir(re_, rd)
        h.chk("corte_antes_de_reducir_el_diario_usa_el_punto_nuevo", a["ok"] and a["aplicadas"] == 0 and pe.volcar(a["diario"].orquestador, T) == ref, (a["codigo"], a["motivo"]))

        # -------------------------------------------------------------- lo que no se usa
        re_, rd = rutas("r")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "PROPUESTA")
        ls = lineas(rd)
        x = [dict(e) for e in ls]
        x[3]["args"] = ["EXP-9999"] + x[3]["args"][1:]   # se toca una línea sin rehacer su hash
        escribir(rd, x)
        h.chk("DI02_linea_tocada", di.abrir(re_, rd)["codigo"] == "DI-02")
        escribir(rd, recadenar(ls[:2] + ls[4:]))   # se quita una operación y se rehace la cadena
        r = di.abrir(re_, rd)
        h.chk("DI04_o_DI02_si_falta_una_operacion", r["codigo"] in ("DI-04", "DI-02") and not r["ok"], (r["codigo"], r["motivo"]))
        y = [dict(e) for e in ls]
        y[2] = {**y[2], "resultado": "0" * 64}   # el RES no es el del resultado real (cadena rehecha)
        r = di.abrir(re_, (escribir(rd, recadenar(y)), rd)[1])
        h.chk("DI04_resultado_distinto_kill_switch_y_O13", r["codigo"] == "DI-04" and r["orquestador"].kill is not None
              and any(a_["codigo"] == "O-13" for a_ in r["orquestador"].avisos), (r["codigo"], r["motivo"]))
        escribir(rd, recadenar(ls[:1] + [{"tipo": "OP", "metodo": "no_existe", "args": [], "kwargs": {}}]))
        h.chk("DI02_metodo_desconocido", di.abrir(re_, rd)["codigo"] == "DI-02")
        escribir(rd, recadenar(ls[:1] + [{"tipo": "OP", "metodo": "barrer", "args": [1, 2, 3, 4, 5], "kwargs": {}},
                                         {"tipo": "RES", "op": 2, "resultado": "0" * 64}]))
        h.chk("DI04_argumentos_que_el_metodo_no_acepta", di.abrir(re_, rd)["codigo"] == "DI-04")
        escribir(rd, recadenar(ls[:1] + ls[1:2] + ls[3:4]))   # dos OP seguidas sin RES en medio
        h.chk("DI02_operacion_sin_resultado_en_medio", di.abrir(re_, rd)["codigo"] == "DI-02")
        escribir(rd, recadenar([{"tipo": "PUNTO", "estado": "a" * 64, "fichero": "b" * 64}] + ls[1:]))
        h.chk("DI03_diario_de_otro_estado", di.abrir(re_, rd)["codigo"] == "DI-03")
        escribir(rd, [])
        h.chk("DI02_diario_vacio", di.abrir(re_, rd)["codigo"] == "DI-02")
        with open(rd, "w") as f:
            f.write("no es json\n" + json.dumps(ls[0]) + "\n")
        h.chk("DI02_primera_linea_ilegible", di.abrir(re_, rd)["codigo"] == "DI-02")
        escribir(rd, ls)
        with open(re_, "w") as f:
            f.write("{roto")
        h.chk("estado_roto_PE01", di.abrir(re_, rd)["codigo"] == "PE-01")
        h.chk("sin_diario_PE05", (os.remove(rd), di.abrir(re_, rd)["codigo"])[1] in ("PE-01", "PE-05"))

        # -------------------------------------------------------------- escritura y argumentos
        re_, rd = rutas("w")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        h.chk("crear_no_pisa", di.crear(nuevo(), re_, rd, T)["codigo"] == "DI-03")
        n = len(lineas(rd))
        r = d.registrar_cotizacion({"instrumento": "EURUSD", "valor": float("nan"), "fecha_hora": AHORA}, "G", AHORA)
        h.chk("DI01_argumentos_no_guardables_no_se_aplican", r["codigo"] == "DI-01" and len(lineas(rd)) == n and d.cotizaciones == {}, r)
        r = d.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": ("2026", "11")}, "G", AHORA)
        h.chk("DI01_tuplas_tampoco", r["codigo"] == "DI-01")
        try:
            d.cotizaciones = {}
            h.chk("no_se_asignan_atributos_por_fuera", False)
        except AttributeError:
            h.chk("no_se_asignan_atributos_por_fuera", True)
        os.remove(rd)
        os.mkdir(rd)   # el diario deja de poder escribirse (aquí, porque su ruta pasa a ser una carpeta)
        antes = pe.volcar(d.orquestador, T)
        r = d.barrer("2026-11-06T09:10:00+00:00")
        h.chk("DI05_sin_poder_escribir_no_se_aplica_y_se_bloquea", r["codigo"] == "DI-05" and pe.volcar(d.orquestador, T) == antes
              and d.barrer(AHORA)["codigo"] == "DI-05" and d.punto(T)["codigo"] == "DI-05", r)
        h.chk("crear_en_carpeta_inexistente_DI05", di.crear(nuevo(), os.path.join(tmp, "no", "e.json"), os.path.join(tmp, "no", "d"), T)["codigo"] == "DI-05")

    # ------------------------------------------------------------------ regresiones de la revisión independiente del diario
    from orquestador import Orquestador
    from pruebas_orquestador import CAL, CFG, S1
    with tempfile.TemporaryDirectory() as tmp:
        def rutas(nombre):
            return os.path.join(tmp, nombre + ".e"), os.path.join(tmp, nombre + ".d")
        re_, rd = rutas("r01")
        o0 = Orquestador(CFG, CAL)
        h.chk("r01_un_orquestador_recien_creado_es_integro", o0.integridad() == [], o0.integridad())
        d = di.crear(o0, re_, rd, T)["diario"]
        d.registrar_sello(S1, AHORA)
        a = di.abrir(re_, rd)
        h.chk("r01_y_se_reabre_con_lo_hecho_desde_el_arranque", a["ok"] and pe.volcar(a["diario"].orquestador, T) == pe.volcar(d.orquestador, T), (a["codigo"], a["motivo"]))
        re_, rd = rutas("r02")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        real = os.fsync
        llamadas = []
        def falla(fd):
            llamadas.append(fd)
            if len(llamadas) == 1:
                raise OSError(5, "EIO simulado")
            return real(fd)
        os.fsync = falla
        try:
            r = d.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": AHORA}, "G", AHORA)
        finally:
            os.fsync = real
        a = di.abrir(re_, rd)
        h.chk("r02_si_falla_el_fsync_de_la_OP_tampoco_se_aplica_al_reabrir", r["codigo"] == "DI-05" and a["ok"] and a["diario"].cotizaciones == {}, (r, a["codigo"]))
        re_, rd = rutas("r03")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        anotado = pe.volcar(d.orquestador, T)
        d.cotizaciones["EURUSD"] = [{"valor": 9.9, "fecha_hora": AHORA, "registrada_en": AHORA}]   # cambio por fuera de los métodos
        r = d.barrer(AHORA)
        h.chk("r03_un_cambio_por_fuera_lo_para_la_operacion_siguiente_DI06", r["codigo"] == "DI-06" and d.barrer(AHORA)["codigo"] == "DI-06"
              and d.punto(T)["codigo"] == "DI-06", r)
        a = di.abrir(re_, rd)
        h.chk("r03_y_al_reabrir_se_vuelve_al_estado_anotado", a["ok"] and pe.volcar(a["diario"].orquestador, T) == anotado)
        d = a["diario"]
        try:
            d._activar_kill("por fuera", "OPERADOR", AHORA)
            h.chk("r03_lo_privado_no_se_expone", False)
        except AttributeError:
            h.chk("r03_lo_privado_no_se_expone", d.kill is None)
        h.chk("r03_pero_los_privados_de_lectura_si", callable(d._testigos))
        h.chk("r04_autorizada_por_no_se_anota", "autorizada_por" not in di.mutantes(d.orquestador))
        n = len(lineas(rd))
        r = d.barrer(AHORA, self=None)
        r2 = d.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": AHORA}, "G", AHORA)
        a = di.abrir(re_, rd)
        h.chk("r05_una_excepcion_se_anota_y_el_diario_sigue_sirviendo", r["codigo"] == "O-00" and r2["ok"] and a["ok"]
              and pe.volcar(a["diario"].orquestador, T) == pe.volcar(d.orquestador, T) and len(lineas(rd)) == n + 4, (r, a["codigo"]))
        r = d.registrar_cotizacion({"instrumento": "EURUSD", "valor": 10 ** 5000, "fecha_hora": AHORA}, "G", AHORA)
        h.chk("r06_entero_enorme_DI01_sin_bloquear", r["codigo"] == "DI-01" and d.barrer(AHORA)["codigo"] != "DI-05", r)
        anidado = x = {}
        for _ in range(3000):
            x["a"] = {}
            x = x["a"]
        h.chk("r07_anidamiento_excesivo_DI01", d.registrar_cotizacion(anidado, "G", AHORA)["codigo"] == "DI-01")
        import copy as _copy
        c = _copy.deepcopy(d)
        h.chk("r08_copiar_un_diario_da_un_orquestador_sin_diario", type(c).__name__ == "Orquestador" and pe.volcar(c, T) == pe.volcar(d.orquestador, T))
        ea, da = rutas("A")
        eb, db = rutas("B")
        A = di.crear(nuevo(), ea, da, T)["diario"]
        di.crear(nuevo(), eb, db, "2026-11-06T11:00:00+00:00")
        A.barrer(AHORA)
        h.chk("r09_el_diario_de_otra_instalacion_DI03", di.abrir(eb, da)["codigo"] == "DI-03")
        re_, rd = rutas("r10")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        d.barrer(AHORA)
        ls = lineas(rd)
        escribir(rd, ls + [di._linea({"n": ls[-1]["n"] + 1, "tipo": "PUNTO", "estado": "f" * 64, "fichero": "e" * 64}, ls[-1]["hash"])])
        h.chk("r10_un_punto_intermedio_que_no_es_el_estado_reaplicado_DI04", di.abrir(re_, rd)["codigo"] == "DI-04")
        llamadas_fsync = []
        real = os.fsync
        os.fsync = lambda fd: (llamadas_fsync.append(os.path.isdir(f"/proc/self/fd/{fd}") or __import__("stat").S_ISDIR(os.fstat(fd).st_mode)), real(fd))[1]
        try:
            di.crear(nuevo(), *rutas("r11"), T)
        finally:
            os.fsync = real
        h.chk("r11_se_hace_fsync_de_la_carpeta", any(llamadas_fsync), llamadas_fsync)
        # regresiones de la revisión de V0.44 (lectura viva y DI-06)
        re_, rd = rutas("v06")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "EN_ANALISIS", n=2); hasta(d, "EN_ANALISIS", n=1)
        exps = d.expedientes
        x = exps.pop("EXP-0002"); exps["EXP-0002"] = x   # solo cambia el orden
        h.chk("v06_reordenar_por_fuera_DI06", d.barrer(AHORA)["codigo"] == "DI-06")
        re_, rd = rutas("v07")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "PROPUESTA")
        d.expedientes["EXP-0001"]["historial"] = tuple(d.expedientes["EXP-0001"]["historial"])
        h.chk("v07_una_tupla_por_fuera_DI06", d.barrer(AHORA)["codigo"] == "DI-06")
        re_, rd = rutas("v08")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        hasta(d, "EN_ANALISIS")
        enc = next(iter(d.encargos))
        r1 = d.registrar_gasto(enc, 1e308, 0, AHORA)
        r2 = d.registrar_gasto(enc, 1e308, 0, AHORA)
        a = di.abrir(re_, rd)
        h.chk("v08_un_gasto_que_desborda_se_rechaza_y_el_diario_se_abre", r1["ok"] and r2["codigo"] == "O-01" and a["ok"], (r1, r2, a["codigo"]))
        re_, rd = rutas("v09")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        real = d.orquestador.__class__.barrer
        def interrumpe(self, *a, **k):
            raise KeyboardInterrupt()
        d.orquestador.__class__.barrer = interrumpe
        try:
            try:
                d.barrer(AHORA)
            except KeyboardInterrupt:
                pass
        finally:
            d.orquestador.__class__.barrer = real
        r = d.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": AHORA}, "G", AHORA)
        a = di.abrir(re_, rd)
        h.chk("v09_una_interrupcion_bloquea_el_diario_y_se_reabre", r["codigo"] == "DI-05" and "interrumpida" in r["motivo"] and a["ok"], (r, a["codigo"]))
        re_, rd = rutas("v10")
        d = di.crear(nuevo(), re_, rd, T)["diario"]
        d.cotizaciones["X"] = []
        d.barrer(AHORA)
        h.chk("v10_tras_DI06_el_motivo_no_habla_de_un_fallo_de_escritura", "cambió sin pasar por el diario" in d.punto(T)["motivo"])
        from orquestador import Orquestador
        cal = __import__("copy").deepcopy(CAL)
        o1 = Orquestador(CFG, cal)
        h.chk("v04_el_orquestador_no_comparte_el_calendario", o1.cal_def is not cal and o1.cal_def == cal)

        viejo = pe.MAX_BYTES
        try:
            re_, rd = rutas("r12")
            d = di.crear(nuevo(), re_, rd, T)["diario"]
            pe.MAX_BYTES = max(os.path.getsize(re_) * 2, 40000)
            for _ in range(200):
                d.barrer(AHORA)
            h.chk("r12_el_diario_no_pasa_de_su_limite", os.path.getsize(rd) <= pe.MAX_BYTES // 4 + 2000 and di.abrir(re_, rd)["ok"], os.path.getsize(rd))
        finally:
            pe.MAX_BYTES = viejo

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO DIARIO T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
