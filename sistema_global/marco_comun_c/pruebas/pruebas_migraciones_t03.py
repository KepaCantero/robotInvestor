"""Pruebas de T-03 (cuarta parte, V0.46): migraciones del estado guardado entre versiones del código. Un estado de otro esquema o
del formato 0.1.0 no se carga (PE-08); se migra de forma explícita (migraciones.migrar y migrar_ficheros), con una entrada
MIGRACION en el registro de límites. Datos SIMULADOS.

Si esta batería falla en «esquema_del_codigo_registrado», el código cambió de esquema (configuración por defecto, atributos del
Orquestador, parámetros, constantes de los módulos o versiones de reglas): hay que registrar el esquema nuevo
(python3 validador/migraciones.py --registrar-esquema V0.xx) y añadir a migraciones.MIGRACIONES una migración que llegue a él.

Uso: python3 pruebas/pruebas_migraciones_t03.py
"""
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import orquestador as orq  # noqa: E402
import persistencia as pe  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402

T = "2026-11-06T09:30:00+00:00"
TM = "2026-11-07T10:00:00+00:00"   # instante de la migración
M = "Actualizo el código del robot a la versión nueva"
K1 = bytes(range(32))
K2 = bytes(range(1, 33))
E_FALSO = "e" * 64
# un esquema «anterior» de prueba: la misma parte de código con una marca (así su huella de configuración es la de este código)
PARTE = pe.parte_de_codigo()
PARTE_F = {**PARTE, "marca": "código anterior de prueba"}
E_F = pe.esquema_de_parte(PARTE_F)
ESQ = {**mg.ESQUEMAS, E_F: {"version": "prueba", "parte": PARTE_F}}


def como_v045(e):
    """V0.51: rehace la huella de configuración del estado e con la parte de código de V0.45 (la que V0.45 habría calculado) y la
    cadena del registro de límites que la lleva. Desde V0.51 las constantes de la configuración completa cambiaron (PRIORIDAD_AVISO
    con O-39), así que un estado de este código ya no pasa por uno de V0.45 sin esto."""
    viejo = e["huella_config"]
    nuevo_h = orq._hash(orq._canon({"version_config": e["cfg"]["version_config"], "orquestador": e["cfg"], "calendario": e["cal_def"],
                                    **mg.ESQUEMAS[mg.ESQUEMA_V0_45]["parte"]["codigo"]}))
    e["huella_config"] = nuevo_h
    L = e["limites"]
    for x in L["entradas"]:
        if x.get("huella_config") == viejo:
            x["huella_config"] = nuevo_h
    prev = "0" * 64
    for h, x in zip(L["historial"], L["entradas"]):
        h["datos"], h["hash_prev"] = orq._hash(x), prev
        h["hash"] = orq._hash({k: v for k, v in h.items() if k != "hash"})
        prev = h["hash"]
    return e


def a_010(texto, clave=None):
    """El mismo estado como lo habría guardado V0.45 (formato 0.1.0, sin esquema, huella de configuración de V0.45), firmado si hay clave."""
    d = json.loads(texto)
    del d["esquema"]
    if d["estado"]["huella_config"] == orq._hash(orq._canon({"version_config": d["estado"]["cfg"]["version_config"], "orquestador": d["estado"]["cfg"],
                                                             "calendario": d["estado"]["cal_def"], **pe.parte_de_codigo()["codigo"]})):
        como_v045(d["estado"])   # solo si la huella es la de este código (no se arregla lo que una prueba tocó a propósito)
        d["huella"] = pe._huella(d["estado"])
    d.pop("firma", None)
    d["formato"] = pe.FORMATO_010
    if clave is not None:
        d["firma"] = pe._firma_doc(clave, d)
    return pe._texto(d)


def otro(texto, esquema=None, cambio=None, clave=None):
    """El estado como lo habría guardado otro código: otro esquema y, si se da, otro estado (huella y firma rehechas)."""
    d = json.loads(texto)
    d.pop("firma", None)
    if esquema is not None:
        d["esquema"] = esquema
    if cambio:
        cambio(d["estado"])
    d["atributos"] = sorted(d["estado"])
    d["huella"] = pe._huella(d["estado"])
    if clave is not None:
        d["firma"] = pe._firma_doc(clave, d)
    return pe._texto(d)


def mig(id_, desde, hasta_, f=mg._sin_cambios, cambia=frozenset(), formato=pe.FORMATO):
    return mg.Migracion(id_, formato, desde, hasta_, f, frozenset(cambia), "prueba")


def punto_de(texto, clave=None):
    return di._linea({"n": 1, "tipo": "PUNTO", "estado": json.loads(texto)["huella"],
                      "fichero": hashlib.sha256(texto.encode("ascii")).hexdigest()}, di.CERO, clave)


def escribir_lineas(ruta, ls):
    with open(ruta, "w", encoding="ascii") as f:
        f.write("".join(json.dumps(e, ensure_ascii=True, separators=(",", ":")) + "\n" for e in ls))


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def ficheros_010(tmp, nombre, o, clave=None, extra=()):
    """Un estado 0.1.0 y su diario cerrado (un PUNTO de ese fichero, más las líneas extra que se pidan)."""
    re_, rd = os.path.join(tmp, nombre + ".e"), os.path.join(tmp, nombre + ".d")
    t = a_010(pe.volcar(o, T, clave), clave)
    with open(re_, "w", encoding="utf-8") as f:
        f.write(t)
    p = punto_de(t, clave)
    ls = [p]
    for x in extra:
        ls.append(di._linea({**x, "n": ls[-1]["n"] + 1}, ls[-1]["hash"], clave))
    escribir_lineas(rd, ls)
    return re_, rd, t


def con_autorizacion():
    o = nuevo()
    hasta(o, "AUTORIZADA", n=1)
    # una solicitud de subir el límite pendiente: la migración la anula
    o._anota_limite({"tipo": "SOLICITUD", "antes": 2.0, orq.LIMITE_PERDIDA: 2.5, "motivo": "subida pendiente de confirmar",
                     "canal": "CONSOLA", "hasta": AHORA}, "OPERADOR", AHORA, "solicitud de prueba")
    assert o.integridad() == [], o.integridad()
    return o


def main():
    h = Arnes()
    o = con_autorizacion()
    texto = pe.volcar(o, T)
    d = json.loads(texto)
    # ---------------------------------------------------------------------------------------------- el esquema y el formato
    E0 = pe.esquema_actual()
    h.chk("esquema_del_codigo_registrado (si falla: registra el esquema nuevo y su migración)", E0 in mg.ESQUEMAS
          and pe.esquema_de_parte(mg.ESQUEMAS[E0]["parte"]) == E0, E0)
    h.chk("el_registro_de_esquemas_cuadra", all(pe.esquema_de_parte(v["parte"]) == k for k, v in mg.ESQUEMAS.items()) and mg.ESQUEMA_V0_45 in mg.ESQUEMAS)
    h.chk("hay_camino_desde_V0_45_hasta_este_codigo", mg.camino(pe.FORMATO_010, mg.ESQUEMA_V0_45, E0) is not None)
    pares = [(m.formato_desde, m.esquema_desde) for m in mg.MIGRACIONES]
    h.chk("registro_sin_ambiguedad_ni_ids_repetidos", len(set(pares)) == len(pares) and len({m.id for m in mg.MIGRACIONES}) == len(mg.MIGRACIONES))
    h.chk("volcado_en_formato_020_con_esquema", d["formato"] == pe.FORMATO and d["esquema"] == E0 and set(d) == pe.CLAVES)
    h.chk("el_estado_actual_se_carga", pe.cargar(texto)["ok"])
    t010 = a_010(texto)
    r = pe.cargar(t010)
    h.chk("un_estado_010_no_se_carga_PE08", r["codigo"] == "PE-08" and r["orquestador"] is None, r)
    r = pe.cargar(otro(texto, E_FALSO))
    h.chk("un_estado_de_otro_esquema_no_se_carga_PE08", r["codigo"] == "PE-08" and r["esquema"] == E_FALSO, r)
    h.chk("un_formato_desconocido_sigue_siendo_PE03", pe.cargar(otro(texto, cambio=None).replace(pe.FORMATO, "ESTADO-ORQUESTADOR-9.9.9"))["codigo"] == "PE-03")

    # ---------------------------------------------------------------------------------------------- migrar un 0.1.0 (MIG-001)
    # la cadena desde un documento 0.1.0: MIG-001 y las que vengan después (V0.50: MIG-002); antes de V0.50 era solo MIG-001
    CADENA_010 = [m.id for m in mg.camino(pe.FORMATO_010, mg.ESQUEMA_V0_45, E0)]
    h.chk("la_cadena_desde_010_empieza_por_MIG001", CADENA_010[:1] == ["MIG-001"], CADENA_010)
    sha010 = hashlib.sha256(t010.encode("ascii")).hexdigest()
    r = mg.migrar(t010, TM, M)
    h.chk("migrar_010_con_MIG001", r["ok"] and r["migraciones"] == CADENA_010, r.get("motivo"))
    o2 = r["orquestador"]
    ult = o2.limites["entradas"][-1]
    h.chk("la_migracion_queda_en_el_registro_de_limites", ult["tipo"] == "MIGRACION" and ult["migraciones"] == CADENA_010
          and ult["fichero_antes"] == sha010 and ult["esquema_antes"] == mg.ESQUEMA_V0_45 and ult["esquema_despues"] == E0
          and o2.limites["historial"][-1]["actor"] == "OPERADOR" and o2.limites["historial"][-1]["ahora"] == TM, ult)
    h.chk("el_estado_migrado_esta_integro_y_se_carga", o2.integridad() == [] and pe.cargar(r["texto"])["ok"]
          and json.loads(r["texto"])["formato"] == pe.FORMATO)
    # V0.51: la cadena desde 0.1.0 pasa por el código de V0.45 (otra huella de configuración); la configuración en sí no cambia
    h.chk("la_cadena_no_cambia_la_configuracion_y_anota_la_huella_de_V0_45", o2.huella_config == o.huella_config and o2.cfg == o.cfg
          and ult["huella_antes"] == json.loads(t010)["estado"]["huella_config"] != o.huella_config)
    h.chk("la_migracion_adelanta_el_reloj", o2.ultimo_ahora == TM)
    # r12: con el mismo código (misma huella), una migración no toca las autorizaciones ni la subida pendiente; V0.51: desde 0.1.0
    # (código de V0.45, otra huella) la cadena sí las anula
    h.chk("la_cadena_desde_V0_45_anula_las_autorizaciones_y_la_subida_pendiente", o.autorizacion_vigente(o.expedientes["EXP-0001"])
          and not o2.autorizacion_vigente(o2.expedientes["EXP-0001"]) and o2._subida_pendiente() is None)
    rf = mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-F", E_F, E0),))
    of = rf.get("orquestador")
    h.chk("r12_con_la_misma_huella_se_mantienen_las_autorizaciones_y_la_subida_pendiente", rf["ok"] and of.huella_config == o.huella_config
          and of.autorizacion_vigente(of.expedientes["EXP-0001"]) and of._subida_pendiente() is not None, rf.get("motivo"))
    h.chk("lo_demas_del_estado_no_cambia", all(getattr(o2, k) == getattr(o, k) for k in vars(o) if k not in ("limites", "ultimo_ahora")))
    r2 = mg.migrar(r["texto"], TM, M)
    h.chk("migrar_lo_ya_migrado_no_hace_nada", r2["ok"] and r2["migraciones"] == [] and r2["texto"] == r["texto"])
    h.chk("la_entrada_MIGRACION_va_encadenada", pe.cargar(otro(r["texto"], cambio=lambda e: e["limites"]["entradas"][-1].__setitem__(
        "migraciones", ["MIG-999"])))["codigo"] == "O-13")

    # ---------------------------------------------------------------------------------------------- con clave
    t010k = a_010(pe.volcar(o, T, K1), K1)
    r = mg.migrar(t010k, TM, M, K1)
    h.chk("migrar_un_010_firmado_lo_deja_firmado", r["ok"] and json.loads(r["texto"])["clave_id"] == pe.clave_id(K1)
          and pe.cargar(r["texto"], K1)["ok"] and pe.cargar(r["texto"])["codigo"] == "PE-06")
    h.chk("sin_la_clave_o_con_otra_no_se_migra_PE06", mg.migrar(t010k, TM, M)["codigo"] == "PE-06" and mg.migrar(t010k, TM, M, K2)["codigo"] == "PE-06")
    dk = json.loads(t010k)
    dk["guardado_en"] = AHORA
    h.chk("un_010_firmado_y_tocado_no_se_migra_PE06", mg.migrar(pe._texto(dk), TM, M, K1)["codigo"] == "PE-06")
    dk = json.loads(pe.volcar(o, T, K1))
    dk["esquema"] = E_FALSO
    h.chk("la_firma_cubre_el_esquema", pe.cargar(pe._texto(dk), K1)["codigo"] == "PE-06")

    # ---------------------------------------------------------------------------------------------- lo que no se migra
    h.chk("MG05_instante_anterior_al_reloj", mg.migrar(t010, "2026-11-01T00:00:00+00:00", M)["codigo"] == "MG-05")
    h.chk("MG05_instante_ilegible", mg.migrar(t010, "mañana", M)["codigo"] == "MG-05")
    h.chk("MG05_motivo_corto", mg.migrar(t010, TM, "porque sí")["codigo"] == "MG-05")
    h.chk("MG01_esquema_sin_camino", mg.migrar(otro(texto, E_FALSO), TM, M)["codigo"] == "MG-01")
    amb = (mig("MIG-A", E_F, E0), mig("MIG-B", E_F, E0))
    h.chk("MG01_registro_ambiguo", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=amb)["codigo"] == "MG-01")
    ciclo = (mig("MIG-A", E_F, "f" * 64), mig("MIG-B", "f" * 64, E_F))
    h.chk("MG01_ciclo", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=ciclo)["codigo"] == "MG-01")

    def lanza(e):
        raise KeyError("x")
    h.chk("MG03_la_migracion_lanza", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, lanza),))["codigo"] == "MG-03")
    h.chk("MG03_la_migracion_devuelve_algo_que_JSON_no_guarda",
          mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, lambda e: {**e, "cfg": {**e["cfg"], "x": (1, 2)}}),))["codigo"] == "MG-03")

    def cambia_alerta(e):
        e["cfg"]["alerta_perdida_pct"] = -7.0
        return e
    h.chk("MG04_cambiar_un_valor_del_operador_sin_declararlo",
          mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, cambia_alerta),))["codigo"] == "MG-04")
    r = mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, cambia_alerta, {"cfg.alerta_perdida_pct"}),))
    h.chk("declarado_si_se_puede_y_la_huella_de_configuracion_cambia", r["ok"] and r["orquestador"].cfg["alerta_perdida_pct"] == -7.0
          and r["orquestador"].huella_config != o.huella_config and r["orquestador"].integridad() == [], r.get("motivo"))

    def quita(e):
        del e["cfg"]["autoria_c"]
        return e
    h.chk("MG04_quitar_una_clave", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, quita),))["codigo"] == "MG-04")

    def limite(e):
        e["cfg"]["politica_f"][orq.LIMITE_PERDIDA] = 9.0
        return e
    h.chk("MG04_el_limite_de_perdida_ni_declarado", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ,
                                                             registro=(mig("MIG-X", E_F, E0, limite, {"cfg.politica_f"}),))["codigo"] == "MG-04")

    def anida(e):
        e["cfg"]["politica_f"]["deriva_precio_max_pct"] = 3
        return e
    h.chk("MG04_un_valor_anidado", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, anida),))["codigo"] == "MG-04")
    h.chk("MG04_un_valor_que_solo_cambia_de_tipo", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0,
          lambda e: {**e, "cfg": {**e["cfg"], "alerta_perdida_pct": int(e["cfg"]["alerta_perdida_pct"])}}),))["codigo"] == "MG-04")
    h.chk("un_atributo_nuevo_sin_declarar_MG04",
          mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, lambda e: {**e, "sobra": 1}),))["codigo"] == "MG-04")
    h.chk("un_atributo_que_este_codigo_no_tiene_PE03",
          mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, lambda e: {**e, "sobra": 1}, {"sobra"}),))["codigo"] == "PE-03")

    def toca_exp(e):
        e["expedientes"]["EXP-0001"]["historial"][0]["motivo"] = "otro"
    h.chk("MG02_un_estado_alterado_no_se_migra", mg.migrar(a_010(otro(texto, cambio=toca_exp)), TM, M)["codigo"] == "MG-02")

    def toca_lim(e):
        e["huella_config"] = "0" * 64
    h.chk("MG02_registro_de_limites_que_no_cuadra", mg.migrar(a_010(otro(texto, cambio=toca_lim)), TM, M)["codigo"] == "MG-02")

    # ---------------------------------------------------------------------------------------------- un código «nuevo» simulado
    # (1) el código nuevo añade una clave a la configuración: un estado del código actual no la tiene
    try:
        orq.CONFIG_DEFECTO["clave_nueva_de_prueba"] = 7
        e1 = pe.esquema_actual()
        h.chk("una_clave_nueva_es_otro_esquema", e1 != E0)
        h.chk("sin_migrar_falta_la_clave_PE08", pe.cargar(texto)["codigo"] == "PE-08")
        r = mg.migrar(texto, TM, M, registro=(mig("MIG-T1", E0, e1, lambda e: {**e, "cfg": {**e["cfg"], "clave_nueva_de_prueba": 7}}),))
        h.chk("una_migracion_anade_la_clave_nueva_con_su_valor_sin_declararla", r["ok"] and r["orquestador"].cfg["clave_nueva_de_prueba"] == 7
              and r["orquestador"].integridad() == [], r.get("motivo"))
        r = mg.migrar(texto, TM, M, registro=(mig("MIG-T1", E0, e1, lambda e: {**e, "cfg": {**e["cfg"], "clave_nueva_de_prueba": 8}}),))
        h.chk("con_otro_valor_que_el_del_codigo_hay_que_declararla_MG04", r["codigo"] == "MG-04", r)
    finally:
        del orq.CONFIG_DEFECTO["clave_nueva_de_prueba"]
    # (2) el código nuevo cambia una constante: cambia el esquema y la huella de la configuración
    antes_min = orq.MOTIVO_MIN
    try:
        orq.MOTIVO_MIN = antes_min + 1
        e1 = pe.esquema_actual()
        h.chk("otra_constante_es_otro_esquema", e1 != E0)
        r0 = pe.cargar(texto)
        h.chk("con_el_codigo_nuevo_el_estado_viejo_no_se_carga_PE08", r0["codigo"] == "PE-08")
        r = mg.migrar(texto, TM, M, registro=(mig("MIG-T2", E0, e1),))
        o3 = r["orquestador"]
        h.chk("migrado_al_codigo_nuevo_con_la_huella_nueva", r["ok"] and o3.huella_config != o.huella_config
              and o3.limites["entradas"][-1]["huella_antes"] == o.huella_config and o3.integridad() == [] and pe.cargar(r["texto"])["ok"], r.get("motivo"))
        h.chk("con_otro_codigo_las_autorizaciones_dejan_de_valer_y_la_subida_se_anula",
              not o3.autorizacion_vigente(o3.expedientes["EXP-0001"]) and o3._subida_pendiente() is None)
        nuevo_texto = r["texto"]
    finally:
        orq.MOTIVO_MIN = antes_min
    h.chk("y_no_se_vuelve_atras_con_el_codigo_anterior_PE08", pe.cargar(nuevo_texto)["codigo"] == "PE-08"
          and mg.migrar(nuevo_texto, TM, M)["codigo"] == "MG-01")

    # ---------------------------------------------------------------------------------------------- revisión independiente de V0.46
    # r01: una configuración tocada no se blanquea migrando (sin clave, con la huella rehecha; con clave, guardada ya rota)
    def a_l2(e):
        e["cfg"]["nivel_autonomia"]["TRADING"] = "L1" if e["cfg"]["nivel_autonomia"].get("TRADING") == "L2" else "L2"
        e["cfg"]["anulaciones_veto_mes"] = 10
    h.chk("r01_config_tocada_sin_clave_MG02", mg.migrar(a_010(otro(texto, cambio=a_l2)), TM, M)["codigo"] == "MG-02")
    o_roto = con_autorizacion()
    o_roto.cfg["anulaciones_veto_mes"] = 10
    h.chk("r01_config_rota_guardada_con_clave_MG02", "CONFIG" in o_roto.integridad()
          and mg.migrar(a_010(pe.volcar(o_roto, T, K1), K1), TM, M, K1)["codigo"] == "MG-02")
    # r02: anidamiento extremo: no lanza

    def hondo(e):
        x = 0
        for _ in range(5000):
            x = [x]
        e["fotos"] = {"x": x}
    try:
        profundo = a_010(otro(texto, cambio=hondo))
    except RecursionError:
        profundo = None
    with tempfile.TemporaryDirectory() as tmp:
        if profundo is not None:
            rp = os.path.join(tmp, "p.e")
            with open(rp, "w", encoding="utf-8") as f:
                f.write(profundo)
            escribir_lineas(os.path.join(tmp, "p.d"), [punto_de(profundo)])
            r1, r2 = mg.migrar(profundo, TM, M), mg.migrar_ficheros(rp, os.path.join(tmp, "p.d"), TM, M)
            h.chk("r02_anidamiento_extremo_no_lanza", not r1["ok"] and not r2["ok"], (r1["codigo"], r2["codigo"]))
        else:
            h.chk("r02_anidamiento_extremo_no_lanza (no montable aquí)", True)
    # r03: el esquema no necesita la configuración guardada: un código que retira una clave puede migrar
    try:
        orq.CONFIG_DEFECTO["clave_retirada_de_prueba"] = 1
        o_ret = con_autorizacion()
        t_ret = pe.volcar(o_ret, T)
        e_ret = pe.esquema_actual()
        esq_ret = {**mg.ESQUEMAS, e_ret: {"version": "prueba", "parte": pe.parte_de_codigo()}}
    finally:
        del orq.CONFIG_DEFECTO["clave_retirada_de_prueba"]
    quitar = mig("MIG-T3", e_ret, E0, lambda e: {**e, "cfg": {k: v for k, v in e["cfg"].items() if k != "clave_retirada_de_prueba"}},
                 {"cfg.clave_retirada_de_prueba"})
    r = mg.migrar(t_ret, TM, M, registro=(quitar,), esquemas=esq_ret)
    h.chk("r03_un_codigo_que_retira_una_clave_migra_el_estado", r["ok"] and "clave_retirada_de_prueba" not in r["orquestador"].cfg, r.get("motivo"))
    r = mg.migrar(t_ret, TM, M, registro=(mig("MIG-T3", e_ret, E0, quitar.aplicar),), esquemas=esq_ret)
    h.chk("r03_sin_declararla_no_MG04", r["codigo"] == "MG-04", r)
    # r04: añadir dentro de un diccionario que ya existía también es cambiar

    def nivel_nuevo(e):
        e["cfg"]["nivel_autonomia"]["CARTERA_NUEVA"] = "L2"
        return e
    h.chk("r04_anadir_dentro_de_un_diccionario_sin_declararlo_MG04",
          mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, nivel_nuevo),))["codigo"] == "MG-04")
    # r05: lo que no está encadenado tampoco cambia sin declararlo; el kill-switch, los rearmes y el reloj, nunca
    for nombre, f, decl in (("calendario", lambda e: {**e, "cal_def": {**e["cal_def"], "version": "OTRO"}}, ()),
                            ("avisos", lambda e: {**e, "avisos": [{"id": "AV-X"}]}, ()),
                            ("degradadas", lambda e: {**e, "degradadas": {"TACTICA": {"motivo": "x"}}}, ()),
                            ("kill_aunque_se_declare", lambda e: {**e, "kill": {"motivo": "x", "actor": "OPERADOR", "ahora": AHORA}}, {"kill"}),
                            ("reloj_aunque_se_declare", lambda e: {**e, "ultimo_ahora": TM}, {"ultimo_ahora"})):
        h.chk(f"r05_{nombre}_MG04", mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, f, decl),))["codigo"] == "MG-04")
    # r10: el registro de límites no se reescribe nunca

    def reinicia(e):
        e["limites"]["entradas"][0][orq.LIMITE_PERDIDA] = 10.0
        return e
    h.chk("r10_reescribir_el_registro_de_limites_ni_declarado_MG04",
          mg.migrar(otro(texto, E_F), TM, M, esquemas=ESQ, registro=(mig("MIG-X", E_F, E0, reinicia, {"limites"}),))["codigo"] == "MG-04")
    # r06: un registro de migraciones mal formado falla cerrado
    for nombre, reg in (("None", None), ("generador", (m for m in mg.MIGRACIONES)), ("no_Migracion", ("MIG-001",)),
                        ("cambia_None", (mg.Migracion("MIG-X", pe.FORMATO_010, mg.ESQUEMA_V0_45, E0, mg._sin_cambios, None),)),
                        ("cambia_lista", (mg.Migracion("MIG-X", pe.FORMATO_010, mg.ESQUEMA_V0_45, E0, mg._sin_cambios, [["x"]]),))):
        r = mg.migrar(t010, TM, M, registro=reg)
        h.chk(f"r06_registro_{nombre}_MG01", r["codigo"] == "MG-01", r)
    h.chk("r06_registro_de_esquemas_mal_formado_MG01", mg.migrar(t010, TM, M, esquemas={mg.ESQUEMA_V0_45: {"parte": {"otra": 1}}})["codigo"] == "MG-01"
          and mg.migrar(t010, TM, M, esquemas=[])["codigo"] == "MG-01")
    # r07: el esquema recoge las versiones y constantes de los módulos
    import k_calidad
    import mandatos
    import motor
    for modulo, nombre in ((k_calidad, "VERSION_SELLO"), (motor, "VERSION_SC3"), (mandatos, "VERSION_SC1"), (orq, "NIVELES"), (orq, "VIVOS")):
        antes = getattr(modulo, nombre)
        try:
            setattr(modulo, nombre, ("X",) if not isinstance(antes, str) else antes + "-X")
            otro_e = pe.esquema_actual()
        finally:
            setattr(modulo, nombre, antes)
        h.chk(f"r07_{nombre}_esta_en_el_esquema", otro_e != E0)
    # r09 / r11: motivo con tope, actor del operador, tamaño
    h.chk("r09_motivo_largo_MG05", mg.migrar(t010, TM, "x" * 20000)["codigo"] == "MG-05")
    h.chk("r11_actor_que_no_es_el_operador_MG05", all(mg.migrar(t010, TM, M, actor=a)["codigo"] == "MG-05" for a in (None, "G", "MOTOR", "", 1.5)))
    h.chk("menor_texto_que_no_es_str_PE01", mg.migrar(t010.encode(), TM, M)["codigo"] == "PE-01")
    antes_max = pe.MAX_BYTES
    try:
        pe.MAX_BYTES = len(t010) - 10
        h.chk("r09_un_estado_migrado_demasiado_grande_MG02", mg.migrar(t010, TM, M)["codigo"] == "MG-02")
        h.chk("r09_guardar_no_escribe_lo_que_no_podria_leer_PE05", pe.guardar(o, os.path.join(tempfile.gettempdir(), "nunca-v046.json"), T)["codigo"] == "PE-05")
    finally:
        pe.MAX_BYTES = antes_max

    # ---------------------------------------------------------------------------------------------- ficheros y diario
    with tempfile.TemporaryDirectory() as tmp:
        re_, rd, t = ficheros_010(tmp, "a", o)
        h.chk("un_diario_sobre_un_010_no_se_abre_PE08", di.abrir(re_, rd)["codigo"] == "PE-08")
        r = mg.migrar_ficheros(re_, rd, TM, M)
        a = di.abrir(re_, rd)
        ls = di._leer(rd)[0]
        h.chk("migrar_ficheros_y_abrir", r["ok"] and r["migraciones"] == CADENA_010 and not r["completada"] and a["ok"]
              and len(ls) == 1 and ls[0]["tipo"] == "PUNTO" and a["diario"].limites["entradas"][-1]["tipo"] == "MIGRACION", (r, a["codigo"]))
        h.chk("tras_migrar_el_diario_sigue_funcionando", a["diario"].barrer(TM)["ok"] and di.abrir(re_, rd)["ok"])
        antes = (leer(re_), leer(rd))
        r = mg.migrar_ficheros(re_, rd, TM, M)
        h.chk("migrar_ficheros_ya_migrados_no_toca_nada", r["ok"] and r["migraciones"] == [] and (leer(re_), leer(rd)) == antes, r)
        # con clave
        re_, rd, t = ficheros_010(tmp, "k", o, K1)
        h.chk("ficheros_firmados_sin_la_clave_PE06", mg.migrar_ficheros(re_, rd, TM, M)["codigo"] in ("PE-06", "DI-02"))
        r = mg.migrar_ficheros(re_, rd, TM, M, K1)
        h.chk("ficheros_firmados_se_migran_con_su_clave", r["ok"] and di.abrir(re_, rd, K1)["ok"] and di._leer(rd, K1)[0][0].get("firma"), r)
        # un diario con operaciones después del punto
        re_, rd, t = ficheros_010(tmp, "op", o, extra=({"tipo": "OP", "metodo": "barrer", "args": [TM], "kwargs": {}},))
        r = mg.migrar_ficheros(re_, rd, TM, M)
        h.chk("MG06_diario_con_operaciones_pendientes", r["codigo"] == "MG-06" and leer(re_) == t, r)
        # un diario de otro fichero
        re_, rd, t = ficheros_010(tmp, "otro", o)
        escribir_lineas(rd, [punto_de(pe.volcar(o, AHORA))])
        h.chk("MG06_diario_de_otro_fichero", mg.migrar_ficheros(re_, rd, TM, M)["codigo"] == "MG-06" and leer(re_) == t)
        # un corte entre el estado y el diario
        re_, rd, t = ficheros_010(tmp, "corte", o)
        r = mg.migrar(t, TM, M)
        with open(re_, "w", encoding="utf-8") as f:
            f.write(r["texto"])
        h.chk("cortado_entre_estado_y_diario_no_se_abre_DI03", di.abrir(re_, rd)["codigo"] == "DI-03")
        r = mg.migrar_ficheros(re_, rd, TM, M)
        h.chk("migrar_ficheros_completa_la_migracion_cortada", r["ok"] and r["completada"] and r["migraciones"] == CADENA_010
              and di.abrir(re_, rd)["ok"], r)
        # un PUNTO cuyo estado no es el del fichero que cita
        re_, rd, t = ficheros_010(tmp, "huella", o)
        p = punto_de(t)
        p2 = di._linea({"n": 1, "tipo": "PUNTO", "estado": "0" * 64, "fichero": p["fichero"]}, di.CERO)
        escribir_lineas(rd, [p2])
        h.chk("MG06_punto_con_otra_huella", mg.migrar_ficheros(re_, rd, TM, M)["codigo"] == "MG-06" and leer(re_) == t)
        h.chk("fichero_inexistente_PE05", mg.migrar_ficheros(os.path.join(tmp, "no"), rd, TM, M)["codigo"] == "PE-05")
        # r09: queda una copia del estado anterior
        re_, rd, t = ficheros_010(tmp, "copia", o)
        r = mg.migrar_ficheros(re_, rd, TM, M)
        h.chk("r09_queda_una_copia_del_estado_anterior", r["ok"] and r["copia"] and leer(r["copia"]) == t, r)
        # r08: una migración cortada y, antes de reintentar, un código más nuevo
        re_, rd, t = ficheros_010(tmp, "corte2", o)
        with open(re_, "w", encoding="utf-8") as f:
            f.write(mg.migrar(t, TM, M)["texto"])
        antes_min = orq.MOTIVO_MIN
        try:
            orq.MOTIVO_MIN = antes_min + 1
            e1 = pe.esquema_actual()
            reg = mg.MIGRACIONES + (mig("MIG-T2", E0, e1),)
            r = mg.migrar_ficheros(re_, rd, "2026-11-08T10:00:00+00:00", M, registro=reg)
            h.chk("r08_corte_y_codigo_nuevo_se_migra", r["ok"] and r["migraciones"] == ["MIG-T2"] and di.abrir(re_, rd)["ok"], r)
        finally:
            orq.MOTIVO_MIN = antes_min
        # menores: diario de una sola línea cortada; estado migrado a mano con el diario abierto
        re_, rd, t = ficheros_010(tmp, "cortada", o)
        with open(rd, "w", encoding="ascii") as f:
            f.write('{"n":1,"tipo":"PUN')
        h.chk("menor_diario_sin_ninguna_linea_completa_DI02", mg.migrar_ficheros(re_, rd, TM, M)["codigo"] == "DI-02" and leer(re_) == t)
        re_, rd, t = ficheros_010(tmp, "amano", o, extra=({"tipo": "OP", "metodo": "barrer", "args": [TM], "kwargs": {}},))
        with open(re_, "w", encoding="utf-8") as f:
            f.write(mg.migrar(t, TM, M)["texto"])
        h.chk("menor_estado_migrado_con_el_diario_abierto_MG06", mg.migrar_ficheros(re_, rd, TM, M)["codigo"] == "MG-06")
        # r09: el punto de control no guarda lo que luego no podría leer
        c = di.crear(nuevo(), os.path.join(tmp, "g.e"), os.path.join(tmp, "g.d"), T)
        antes_max = pe.MAX_BYTES
        try:
            pe.MAX_BYTES = 100
            h.chk("r09_punto_demasiado_grande_PE05", c["diario"].punto(TM)["codigo"] == "PE-05")
        finally:
            pe.MAX_BYTES = antes_max

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO MIGRACIONES T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
