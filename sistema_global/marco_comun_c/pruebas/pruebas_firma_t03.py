"""Pruebas de T-03 (tercera parte, V0.45): la firma con clave del estado guardado y del diario (HMAC-SHA256). Sin la clave no se
puede rehacer lo que la huella sin clave dejaba abierto: el reloj, el kill-switch o las líneas del diario. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_firma_t03.py
"""
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_diario_t03 import escribir, lineas, recadenar  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402
from pruebas_persistencia_t03 import rehacer  # noqa: E402

T = "2026-11-06T09:30:00+00:00"
K1 = bytes(range(32))
K2 = bytes(range(1, 33))


def _lanza(f):
    try:
        f()
        return False
    except TypeError:
        return True


def main():
    h = Arnes()
    with tempfile.TemporaryDirectory() as tmp:
        # -------------------------------------------------------------- la clave (en la Fase 1, un fichero 0600 hace de bóveda)
        rk = os.path.join(tmp, "clave")
        k = pe.nueva_clave()
        g = pe.escribir_clave(rk, k)
        h.chk("escribir_clave_0600", g["ok"] and stat.S_IMODE(os.stat(rk).st_mode) == 0o600 and g["clave_id"] == pe.clave_id(k), g)
        h.chk("escribir_clave_no_pisa", pe.escribir_clave(rk, k)["codigo"] == "PE-07")
        r = pe.leer_clave(rk)
        h.chk("leer_clave", r["ok"] and r["clave"] == k and len(k) == 32)
        os.chmod(rk, 0o644)
        h.chk("clave_legible_por_otros_PE07", pe.leer_clave(rk)["codigo"] == "PE-07")
        os.chmod(rk, 0o600)
        for nombre, contenido in (("corta", "00" * 16), ("no_hex", "zz" * 32), ("vacia", "")):
            ruta = os.path.join(tmp, "k_" + nombre)
            fd = os.open(ruta, os.O_WRONLY | os.O_CREAT, 0o600)
            os.write(fd, contenido.encode()); os.close(fd)
            h.chk(f"clave_{nombre}_PE07", pe.leer_clave(ruta)["codigo"] == "PE-07")
        h.chk("clave_inexistente_PE07", pe.leer_clave(os.path.join(tmp, "nada"))["codigo"] == "PE-07")
        h.chk("clave_corta_en_escribir_PE07", pe.escribir_clave(os.path.join(tmp, "k3"), b"corta")["codigo"] == "PE-07")
        h.chk("el_id_no_es_la_clave", pe.clave_id(K1) != K1.hex()[:16] and pe.clave_id(K1) != pe.clave_id(K2))

        # -------------------------------------------------------------- estado firmado
        o = nuevo(); hasta(o, "PROPUESTA")
        t = pe.volcar(o, T, K1)
        d = json.loads(t)
        h.chk("volcado_firmado", set(d) == pe.CLAVES_FIRMADO and d["clave_id"] == pe.clave_id(K1) and len(d["firma"]) == 64)
        r = pe.cargar(t, K1)
        h.chk("se_carga_con_su_clave", r["ok"] and pe.volcar(r["orquestador"], T, K1) == t, (r["codigo"], r["motivo"]))
        h.chk("firmado_sin_clave_PE06", pe.cargar(t)["codigo"] == "PE-06")
        h.chk("con_otra_clave_PE06", (lambda r: r["codigo"] == "PE-06" and "otra clave" in r["motivo"])(pe.cargar(t, K2)))
        h.chk("sin_firmar_con_clave_PE06", pe.cargar(pe.volcar(o, T), K1)["codigo"] == "PE-06")
        h.chk("clave_corta_al_cargar_PE07", pe.cargar(t, b"x")["codigo"] == "PE-07")
        h.chk("clave_corta_al_guardar_PE07", pe.guardar(o, os.path.join(tmp, "e.json"), T, b"x")["codigo"] == "PE-07")
        try:
            pe.volcar(o, T, "no son bytes")
            h.chk("clave_que_no_son_bytes_no_se_vuelca", False)
        except ValueError:
            h.chk("clave_que_no_son_bytes_no_se_vuelca", True)
        # lo que en V0.42 era un límite: rehacer la huella de algo no encadenado. Con la firma ya no pasa.
        def atrasa(x):
            x["estado"]["ultimo_ahora"] = "2026-11-05T00:00:00+00:00"
        h.chk("reloj_atrasado_con_la_huella_rehecha_PE06", pe.cargar(rehacer(t, atrasa), K1)["codigo"] == "PE-06")
        def quita_kill(x):
            x["estado"]["kill"] = None
        ok_ = nuevo(); ok_.activar_kill_switch("prueba", "OPERADOR", AHORA)
        h.chk("kill_switch_quitado_con_la_huella_rehecha_PE06", pe.cargar(rehacer(pe.volcar(ok_, T, K1), quita_kill), K1)["codigo"] == "PE-06")
        for campo, valor in (("guardado_en", "2026-11-07T00:00:00+00:00"), ("firma", "0" * 64), ("clave_id", pe.clave_id(K2))):
            h.chk(f"cabecera_tocada_{campo}_PE06", pe.cargar(pe._texto({**d, campo: valor}), K1)["codigo"] == "PE-06")
        with tempfile.TemporaryDirectory() as t2:
            ruta = os.path.join(t2, "e.json")
            h.chk("guardar_y_cargar_de_firmados", pe.guardar(o, ruta, T, K1)["ok"] and pe.cargar_de(ruta, K1)["ok"] and pe.cargar_de(ruta)["codigo"] == "PE-06")

        # -------------------------------------------------------------- diario firmado
        re_, rd = os.path.join(tmp, "f.estado"), os.path.join(tmp, "f.diario")
        c = di.crear(nuevo(), re_, rd, T, K1)
        dd = c["diario"]
        hasta(dd, "PROPUESTA")
        assert autorizar_op(dd, "EXP-0001", informe_f(dd), AHORA)["ok"]
        ls = lineas(rd)
        h.chk("cada_linea_lleva_su_firma", c["ok"] and all(len(x.get("firma", "")) == 64 for x in ls) and len(ls) > 5)
        a = di.abrir(re_, rd, K1)
        h.chk("se_reabre_con_la_clave_al_mismo_estado", a["ok"] and pe.volcar(a["diario"].orquestador, T) == pe.volcar(dd.orquestador, T), (a["codigo"], a["motivo"]))
        h.chk("sin_la_clave_no_se_reabre_PE06", di.abrir(re_, rd)["codigo"] == "PE-06")
        h.chk("con_otra_clave_no_se_reabre_PE06", di.abrir(re_, rd, K2)["codigo"] == "PE-06")
        p = a["diario"].punto(T)
        h.chk("el_punto_de_control_guarda_firmado", p["ok"] and pe.cargar_de(re_, K1)["ok"] and pe.cargar_de(re_)["codigo"] == "PE-06" and "firma" in lineas(rd)[0])
        a["diario"].barrer(AHORA)
        ls = lineas(rd)
        escribir(rd, recadenar([{k: v for k, v in x.items() if k != "firma"} for x in ls]))   # cadena rehecha sin la clave
        h.chk("diario_recadenado_sin_la_clave_DI02", di.abrir(re_, rd, K1)["codigo"] == "DI-02")
        x = [dict(e) for e in ls]
        x[-1].pop("firma")
        escribir(rd, x)
        h.chk("una_linea_sin_firma_DI02", di.abrir(re_, rd, K1)["codigo"] == "DI-02")
        x = [dict(e) for e in ls]
        x[-1]["firma"] = pe.firmar(K2, "robot-investor/diario/" + x[-1]["hash"])
        escribir(rd, x)
        h.chk("una_linea_firmada_con_otra_clave_DI02", di.abrir(re_, rd, K1)["codigo"] == "DI-02")
        escribir(rd, ls)
        h.chk("el_diario_bueno_sigue_abriendose", di.abrir(re_, rd, K1)["ok"])
        h.chk("crear_con_clave_corta_PE07", di.crear(nuevo(), os.path.join(tmp, "g.e"), os.path.join(tmp, "g.d"), T, b"x")["codigo"] == "PE-07")
        h.chk("abrir_con_clave_corta_PE07", di.abrir(re_, rd, b"x")["codigo"] == "PE-07")
        # un diario sin firmar no se abre con clave, ni uno firmado sin ella
        re2, rd2 = os.path.join(tmp, "s.estado"), os.path.join(tmp, "s.diario")
        di.crear(nuevo(), re2, rd2, T)
        h.chk("diario_sin_firmar_abierto_con_clave_PE06", di.abrir(re2, rd2, K1)["codigo"] == "PE-06")
        escribir(rd2, [dict(lineas(rd2)[0], firma="0" * 64)])
        h.chk("linea_con_firma_en_diario_sin_clave_DI02", di.abrir(re2, rd2)["codigo"] == "DI-02")

    # ------------------------------------------------------------------ regresiones de la revisión independiente de V0.45
    with tempfile.TemporaryDirectory() as tmp:
        o = nuevo(); hasta(o, "EN_ANALISIS", n=2); hasta(o, "EN_ANALISIS", n=1)
        d = json.loads(pe.volcar(o, T, K1))
        d["estado"]["encargos"] = dict(reversed(list(d["estado"]["encargos"].items())))   # solo cambia el orden, sin la clave
        h.chk("r01_reordenar_el_estado_firmado_PE06", pe.cargar(pe._texto(d), K1)["codigo"] == "PE-06")
        re_, rd = os.path.join(tmp, "o.e"), os.path.join(tmp, "o.d")
        dd = di.crear(nuevo(), re_, rd, T, K1)["diario"]
        dd.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": AHORA}, "G", AHORA)
        ls = lineas(rd)
        x = [dict(e) for e in ls]
        op = next(i for i, e in enumerate(x) if e["tipo"] == "OP")
        x[op]["args"] = [dict(reversed(list(x[op]["args"][0].items())))] + x[op]["args"][1:]   # mismo contenido, otro orden
        escribir(rd, x)
        h.chk("r02_reordenar_los_argumentos_de_una_linea_firmada_DI02", di.abrir(re_, rd, K1)["codigo"] == "DI-02")
        h.chk("r05_una_clave_trivial_no_vale", not pe.clave_valida(bytes(32)) and pe.escribir_clave(os.path.join(tmp, "z"), bytes(32))["codigo"] == "PE-07"
              and pe.clave_valida(pe.nueva_clave()))
        rk = os.path.join(tmp, "k"); pe.escribir_clave(rk, K1)
        os.symlink(rk, os.path.join(tmp, "enlace"))
        h.chk("r05_un_enlace_a_la_clave_no_se_sigue_PE07", pe.leer_clave(os.path.join(tmp, "enlace"))["codigo"] == "PE-07")
        ajena = os.path.join(tmp, "ajena"); pe.escribir_clave(ajena, K2)
        try:
            os.chown(ajena, os.getuid() + 4242, -1)
            h.chk("r04_una_clave_de_otro_usuario_no_vale_PE07", pe.leer_clave(ajena)["codigo"] == "PE-07")
        except PermissionError:   # sin permiso para cambiar el dueño: el caso no se puede montar aquí
            h.chk("r04_una_clave_de_otro_usuario_no_vale_PE07 (no montable sin permisos)", True)
        os.mkfifo(os.path.join(tmp, "fifo"), 0o600)
        h.chk("r06_una_fifo_no_cuelga_PE07", pe.leer_clave(os.path.join(tmp, "fifo"))["codigo"] == "PE-07")
        h.chk("r07_un_diario_no_se_serializa", (lambda: __import__("pickle").dumps(dd))() if False else _lanza(lambda: __import__("pickle").dumps(dd)))
        kb = bytearray(K1)
        re2, rd2 = os.path.join(tmp, "b.e"), os.path.join(tmp, "b.d")
        d2 = di.crear(nuevo(), re2, rd2, T, kb)["diario"]
        kb[:] = b""
        d2.barrer(AHORA)
        h.chk("r09_borrar_la_clave_del_llamador_no_cambia_la_del_diario", di.abrir(re2, rd2, K1)["ok"])
        linea = lineas(rd2)[0]
        h.chk("dominios_distintos_la_firma_de_una_linea_no_es_la_de_un_estado", linea["firma"] != pe.firmar(K1, linea["hash"]))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO FIRMA T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
