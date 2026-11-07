"""Pruebas de T-03 (sexta parte, V0.49): rotación de la clave de firma del estado guardado y del diario. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_rotacion_t03.py
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
import persistencia as pe  # noqa: E402
import rotacion as rt  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402
from pruebas_persistencia_t03 import rehacer  # noqa: E402

T = "2026-11-06T09:30:00+00:00"
TR = "2026-11-07T10:00:00+00:00"   # instante de la rotación
M = "La clave anterior estaba en una copia de seguridad perdida"
K1, K2, K3 = bytes(range(32)), bytes(range(1, 33)), bytes(range(2, 34))


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def estado():
    o = nuevo()
    hasta(o, "AUTORIZADA", n=1)
    return o


def main():
    h = Arnes()
    o = estado()
    t1 = pe.volcar(o, T, K1)
    # ------------------------------------------------------------------------------------------- rotar el texto
    r = rt.rotar(t1, TR, M, K1, K2)
    h.chk("rotar_de_K1_a_K2", r["ok"], r.get("motivo"))
    t2 = r["texto"]
    h.chk("con_la_clave_nueva_se_carga", pe.cargar(t2, K2)["ok"] and json.loads(t2)["clave_id"] == pe.clave_id(K2))
    h.chk("con_la_vieja_ya_no_PE06", pe.cargar(t2, K1)["codigo"] == "PE-06" and pe.cargar(t2)["codigo"] == "PE-06")
    o2 = r["orquestador"]
    ult = o2.limites["entradas"][-1]
    h.chk("la_rotacion_queda_en_el_registro", ult["tipo"] == "ROTACION" and ult["clave_antes"] == pe.clave_id(K1)
          and ult["clave_despues"] == pe.clave_id(K2) and ult["fichero_antes"] == hashlib.sha256(t1.encode()).hexdigest()
          and ult["motivo"] == M and o2.limites["historial"][-1]["actor"] == "OPERADOR" and o2.ultimo_ahora == TR, ult)
    h.chk("ni_las_claves_ni_la_firma_quedan_en_el_estado", K1.hex() not in t2 and K2.hex() not in t2)
    h.chk("integro_y_lo_demas_igual", o2.integridad() == [] and all(getattr(o2, k) == getattr(o, k)
                                                                     for k in vars(o) if k not in ("limites", "ultimo_ahora")))
    h.chk("la_rotacion_no_anula_autorizaciones", o2.autorizacion_vigente(o2.expedientes["EXP-0001"]))
    h.chk("rotar_otra_vez_de_K2_a_K3", rt.rotar(t2, TR, M, K2, K3)["ok"])
    o2.limites["entradas"][-1]["clave_antes"] = "x"
    h.chk("la_entrada_ROTACION_va_encadenada", "CONFIG" in o2.integridad())
    o2 = pe.cargar(t2, K2)["orquestador"]
    # primera firma
    t0 = pe.volcar(o, T)
    r = rt.rotar(t0, TR, M, None, K1)
    h.chk("firmar_por_primera_vez", r["ok"] and pe.cargar(r["texto"], K1)["ok"] and r["orquestador"].limites["entradas"][-1]["clave_antes"] is None)
    # ------------------------------------------------------------------------------------------- lo que no se rota
    h.chk("CL01_sin_clave_nueva_nunca_se_quita_la_firma", rt.rotar(t1, TR, M, K1, None)["codigo"] == "CL-01")
    h.chk("CL01_la_misma_clave", rt.rotar(t1, TR, M, K1, K1)["codigo"] == "CL-01")
    h.chk("CL01_clave_nueva_trivial", rt.rotar(t1, TR, M, K1, bytes(32))["codigo"] == "CL-01")
    h.chk("CL01_clave_vieja_no_valida", rt.rotar(t1, TR, M, b"corta", K2)["codigo"] == "CL-01")
    h.chk("PE06_con_otra_clave_vieja", rt.rotar(t1, TR, M, K3, K2)["codigo"] == "PE-06")
    h.chk("PE06_firmado_y_sin_clave_vieja", rt.rotar(t1, TR, M, None, K2)["codigo"] == "PE-06")
    h.chk("PE06_sin_firmar_y_con_clave_vieja", rt.rotar(t0, TR, M, K1, K2)["codigo"] == "PE-06")
    d = json.loads(t1)
    d["guardado_en"] = AHORA
    h.chk("PE06_estado_tocado", rt.rotar(pe._texto(d), TR, M, K1, K2)["codigo"] == "PE-06")

    def toca(d):
        d["estado"]["expedientes"]["EXP-0001"]["historial"][0]["motivo"] = "otro"
    h.chk("CL02_estado_sin_integridad_no_se_rota", rt.rotar(rehacer(t0, toca), TR, M, None, K1)["codigo"] == "CL-02")
    h.chk("CL03_instante_anterior_al_reloj", rt.rotar(t1, "2026-11-01T00:00:00+00:00", M, K1, K2)["codigo"] == "CL-03")
    h.chk("CL03_instante_ilegible", rt.rotar(t1, "mañana", M, K1, K2)["codigo"] == "CL-03")
    h.chk("CL03_motivo", rt.rotar(t1, TR, "corto", K1, K2)["codigo"] == "CL-03" and rt.rotar(t1, TR, "x" * 600, K1, K2)["codigo"] == "CL-03")
    h.chk("CL03_actor", all(rt.rotar(t1, TR, M, K1, K2, actor=a)["codigo"] == "CL-03" for a in ("G", None, "", 1)))
    h.chk("PE01_texto_que_no_es_str", rt.rotar(t1.encode(), TR, M, K1, K2)["codigo"] == "PE-01")
    h.chk("PE01_texto_roto", rt.rotar(t1[:-5], TR, M, K1, K2)["codigo"] == "PE-01")
    antes = pe.MAX_BYTES
    try:
        pe.MAX_BYTES = len(t1) + 10
        h.chk("CL02_resultado_demasiado_grande", rt.rotar(t1, TR, M, K1, K2)["codigo"] == "CL-02")
    finally:
        pe.MAX_BYTES = antes

    # ------------------------------------------------------------------------------------------- ficheros y diario
    with tempfile.TemporaryDirectory() as tmp:
        re_, rd = os.path.join(tmp, "e"), os.path.join(tmp, "d")
        dd = di.crear(estado(), re_, rd, T, K1)["diario"]
        dd.barrer(T)
        h.chk("RF_diario_abierto_CL04", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["codigo"] == "CL-04")
        dd.punto(T)
        viejo = leer(re_)
        r = rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
        a = di.abrir(re_, rd, K2)
        h.chk("RF_rotar_ficheros", r["ok"] and not r["completada"] and a["ok"], (r, a["codigo"]))
        h.chk("RF_copia_del_estado_anterior", r["copia"] and leer(r["copia"]) == viejo and pe.cargar(leer(r["copia"]), K1)["ok"])
        h.chk("RF_con_la_vieja_ya_no_se_abre", di.abrir(re_, rd, K1)["codigo"] in ("PE-06", "DI-02"))
        h.chk("RF_el_diario_sigue_funcionando_con_la_nueva", a["diario"].barrer(TR)["ok"] and di.abrir(re_, rd, K2)["ok"])
        a["diario"].punto(TR)
        antes_f = (leer(re_), leer(rd))
        r = rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
        h.chk("RF_repetir_no_hace_nada", r["ok"] and not r["completada"] and (leer(re_), leer(rd)) == antes_f, r)
        # un corte entre el estado y el diario
        re_, rd = os.path.join(tmp, "c.e"), os.path.join(tmp, "c.d")
        di.crear(estado(), re_, rd, T, K1)
        rr = rt.rotar(leer(re_), TR, M, K1, K2)
        with open(re_, "w", encoding="utf-8") as f:
            f.write(rr["texto"])
        h.chk("RF_cortado_no_se_abre_con_ninguna", di.abrir(re_, rd, K2)["ok"] is False and di.abrir(re_, rd, K1)["ok"] is False)
        r = rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
        h.chk("RF_completa_la_rotacion_cortada", r["ok"] and r["completada"] and di.abrir(re_, rd, K2)["ok"], r)
        # completar con claves que no son las de la rotación
        re_, rd = os.path.join(tmp, "x.e"), os.path.join(tmp, "x.d")
        di.crear(estado(), re_, rd, T, K1)
        rr = rt.rotar(leer(re_), TR, M, K1, K2)
        with open(re_, "w", encoding="utf-8") as f:
            f.write(rr["texto"])
        h.chk("RF_completar_con_otra_clave_vieja_CL04", rt.rotar_ficheros(re_, rd, TR, M, K3, K2)["codigo"] in ("CL-04", "DI-02"))
        # primera firma de unos ficheros sin firmar
        re_, rd = os.path.join(tmp, "s.e"), os.path.join(tmp, "s.d")
        di.crear(estado(), re_, rd, T)
        r = rt.rotar_ficheros(re_, rd, TR, M, None, K1)
        h.chk("RF_firmar_por_primera_vez", r["ok"] and di.abrir(re_, rd, K1)["ok"] and di.abrir(re_, rd)["codigo"] == "PE-06")
        # diario de otro fichero
        re_, rd = os.path.join(tmp, "o.e"), os.path.join(tmp, "o.d")
        di.crear(estado(), re_, rd, T, K1)
        otro_rd = os.path.join(tmp, "otro.d")
        di.crear(nuevo(), os.path.join(tmp, "otro.e"), otro_rd, AHORA, K1)
        os.replace(otro_rd, rd)
        viejo = leer(re_)
        h.chk("RF_diario_de_otro_fichero_CL04", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["codigo"] == "CL-04" and leer(re_) == viejo)
        h.chk("RF_fichero_inexistente_PE05", rt.rotar_ficheros(os.path.join(tmp, "no"), rd, TR, M, K1, K2)["codigo"] == "PE-05")
        h.chk("RF_diario_con_otra_clave_DI02", rt.rotar_ficheros(re_, rd, TR, M, K3, K2)["codigo"] in ("DI-02", "PE-06"))
        with open(rd, "w", encoding="ascii") as f:
            f.write('{"n":1,"tipo":"PUN')
        h.chk("RF_diario_sin_lineas_DI02", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["codigo"] == "DI-02")
        h.chk("RF_argumentos_raros_no_lanzan", not rt.rotar_ficheros(None, None, TR, M, K1, K2)["ok"]
              and not rt.rotar_ficheros(re_, rd, None, None, object(), object())["ok"])

    # ------------------------------------------------------------------------------------------- revisión de V0.49
    import shutil
    import migraciones as mg
    import orquestador as orq
    from pruebas_migraciones_t03 import mig
    K1b = K1 + b"\0"                      # para HMAC, la misma clave que K1
    K1l = bytes(range(70))                 # más de 64 bytes: HMAC la sustituye por su SHA-256
    with tempfile.TemporaryDirectory() as tmp:
        def par(nombre, o=None, clave=K1):
            re_, rd = os.path.join(tmp, nombre + ".e"), os.path.join(tmp, nombre + ".d")
            di.crear(o or estado(), re_, rd, T, clave)
            return re_, rd
        # r01 y r02: tras rotar, lo firmado con la clave retirada (fabricado o la copia) no se vuelve a firmar
        re_, rd = par("r01")
        viejo_e, viejo_d = leer(re_), leer(rd)
        r = rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
        h.chk("r01_la_clave_vieja_queda_retirada", r["ok"] and leer(re_ + ".claves-retiradas").split() == [pe.clave_id(K1)])
        shutil.copy(r["copia"], re_)
        with open(rd, "w", encoding="ascii") as f:
            f.write(viejo_d)
        r = rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
        h.chk("r01_r02_lo_firmado_con_la_retirada_no_se_vuelve_a_firmar_CL01", r["codigo"] == "CL-01" and leer(re_) == viejo_e, r)
        re_, rd = par("r02")
        sha = hashlib.sha256(leer(re_).encode()).hexdigest()
        with open(f"{re_}.antes-{sha[:16]}", "w", encoding="utf-8") as f:
            f.write("otra cosa")
        h.chk("r02_una_copia_distinta_no_se_pisa_CL04", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["codigo"] == "CL-04")
        re_, rd = par("r02b")
        with open(re_ + ".claves-retiradas", "w", encoding="ascii") as f:
            f.write("esto no es un id\n")
        h.chk("r02_registro_de_retiradas_ilegible_CL04", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["codigo"] == "CL-04")
        # r03: un Diario abierto con la clave vieja que se sigue usando tras rotar se bloquea y no deshace nada
        re_, rd = par("r03")
        dv = di.abrir(re_, rd, K1)["diario"]
        h.chk("r03_rotar", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["ok"])
        rb, rp = dv.barrer(TR), dv.punto(TR)
        h.chk("r03_el_diario_viejo_se_bloquea_DI06", rb["codigo"] == "DI-06" and rp["codigo"] == "DI-06", (rb, rp))
        h.chk("r03_y_la_rotacion_sigue_en_pie", di.abrir(re_, rd, K2)["ok"])
        # r04: claves equivalentes para HMAC
        h.chk("r04_clave_con_ceros_al_final_CL01", rt.rotar(t1, TR, M, K1, K1b)["codigo"] == "CL-01")
        t_l = pe.volcar(o, T, K1l)
        h.chk("r04_clave_larga_y_su_sha256_CL01", rt.rotar(t_l, TR, M, K1l, hashlib.sha256(K1l).digest())["codigo"] == "CL-01")
        re_, rd = par("r04")
        h.chk("r04_tambien_en_ficheros", rt.rotar_ficheros(re_, rd, TR, M, K1, K1b)["codigo"] == "CL-01")
        # r05: la misma clave dos veces, o una vieja cualquiera con la actual, no responde «nada que hacer»
        h.chk("r05_misma_clave_en_ficheros_CL01", rt.rotar_ficheros(re_, rd, TR, M, K1, K1)["codigo"] == "CL-01")
        h.chk("r05_vieja_cualquiera_y_la_actual_como_nueva_CL04", rt.rotar_ficheros(re_, rd, TR, M, K3, K1)["codigo"] == "CL-04")
        # r06: no se vuelve a una clave retirada (ni con el registro de fuera ni con el del estado)
        re_, rd = par("r06")
        rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
        h.chk("r06_volver_a_la_retirada_en_ficheros_CL01", rt.rotar_ficheros(re_, rd, TR, M, K2, K1)["codigo"] == "CL-01")
        h.chk("r06_volver_a_la_retirada_en_el_texto_CL01", rt.rotar(leer(re_), TR, M, K2, K1)["codigo"] == "CL-01")
        # r07: un corte y luego otro código: se completa la rotación y después se migra
        re_, rd = par("r07")
        rr = rt.rotar(leer(re_), TR, M, K1, K2)
        with open(re_, "w", encoding="utf-8") as f:
            f.write(rr["texto"])
        e0, antes_min = pe.esquema_actual(), orq.MOTIVO_MIN
        try:
            orq.MOTIVO_MIN = antes_min + 1
            e1 = pe.esquema_actual()
            r = rt.rotar_ficheros(re_, rd, TR, M, K1, K2)
            rm = mg.migrar_ficheros(re_, rd, "2026-11-08T10:00:00+00:00", M, K2, registro=mg.MIGRACIONES + (mig("MIG-T", e0, e1),))
            h.chk("r07_corte_y_codigo_nuevo_se_completa_y_se_migra", r["ok"] and r["completada"] and rm["ok"] and di.abrir(re_, rd, K2)["ok"], (r, rm))
        finally:
            orq.MOTIVO_MIN = antes_min
        # r08: completar también comprueba actor, instante y motivo
        re_, rd = par("r08")
        rr = rt.rotar(leer(re_), TR, M, K1, K2)
        with open(re_, "w", encoding="utf-8") as f:
            f.write(rr["texto"])
        h.chk("r08_completar_con_actor_instante_o_motivo_malos_CL03", all(rt.rotar_ficheros(re_, rd, a, m, K1, K2, actor=ac)["codigo"] == "CL-03"
                                                                           for a, m, ac in ((TR, M, "G"), ("mañana", M, "OPERADOR"), (TR, "", "OPERADOR"))))
        # r09: nada desde 2100 (bloquearía el reloj para siempre)
        h.chk("r09_rotar_en_2100_CL03", rt.rotar(t1, "2100-01-01T00:00:00+00:00", M, K1, K2)["codigo"] == "CL-03")
        from pruebas_migraciones_t03 import a_010
        h.chk("r09_migrar_un_010_en_2100_MG05", mg.migrar(a_010(pe.volcar(o, T)), "2100-01-01T00:00:00+00:00", M)["codigo"] == "MG-05")
        # r10: un diario firmado con otra clave da DI-02 (documentado)
        re_, rd = par("r10")
        os.replace(par("r10b", clave=K3)[1], rd)
        h.chk("r10_diario_de_otra_clave_DI02", rt.rotar_ficheros(re_, rd, TR, M, K1, K2)["codigo"] == "DI-02")

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ROTACION T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
