"""Pruebas de T-72 y T-85 (V0.69): estado público de solo lectura del diario (`Diario.estado_diario()`, que la consola usa en lugar
de los privados `_roto` y `_n` y que ve un diario desincronizado del Orquestador) y tolerancias del reloj de solo lectura y
comparadas de forma que un NaN no pase (QA de T-79, H-05 y H-06). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_reloj_diario_t72.py
"""
import copy
import os
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
from consola import panel  # noqa: E402
from pruebas_consola_sistema import comp, nuevo_diario  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo  # noqa: E402
from pruebas_reloj_t03 import iso, nuevo_reloj  # noqa: E402

NAN = float("nan")


def main():
    h = Arnes()

    # ------------------------------------------------------------------ T-85: tolerancias del reloj
    f, r = nuevo_reloj()
    for nombre in ("max_salto_s", "max_desfase_s", "max_sin_contraste_s"):
        antes = getattr(r, nombre)
        try:
            setattr(r, nombre, NAN)
            cambiada = True
        except AttributeError:
            cambiada = False
        h.chk(f"{nombre}_es_de_solo_lectura", not cambiada and getattr(r, nombre) == antes)
    h.chk("con_tolerancias_sanas_el_reloj_da_instantes", r.ahora()["ok"] and comp(nuevo(), "reloj", reloj=r)["nivel"] == "VERDE")

    # aunque alguien llegue a lo privado, un NaN falla cerrado en cada comparación
    f, r = nuevo_reloj()
    r._tol = (r._tol[0], r._tol[1], NAN)
    x = r.ahora()
    h.chk("contraste_NaN_no_da_instantes_H06", not x["ok"] and x["codigo"] == "RL-04", x)
    h.chk("contraste_NaN_no_es_verde_en_el_panel_H06", comp(nuevo(), "reloj", reloj=r)["nivel"] == "AMBAR")

    f, r = nuevo_reloj()
    r._tol = (NAN, r._tol[1], r._tol[2])
    f.pasa(1.0)
    x = r.ahora()
    h.chk("salto_NaN_bloquea_el_reloj", not x["ok"] and x["codigo"] == "RL-01" and r.bloqueo is not None, x)

    f, r = nuevo_reloj(contrastar=False)
    r._tol = (r._tol[0], NAN, r._tol[2])
    x = r.contrastar(iso(f.p), "REFERENCIA DE PRUEBA")
    h.chk("desfase_NaN_no_contrasta", not x["ok"] and x["codigo"] == "RL-03", x)

    f, r = nuevo_reloj()
    r._tol = ("x", r._tol[1], r._tol[2])
    f.pasa(1.0)
    x = r.ahora()
    h.chk("tolerancia_que_no_se_compara_no_da_instantes", not x["ok"], x)

    # QA de T-72, H-01 y H-02: infinitos, enormes y _tol mal formado tampoco desactivan el control ni hacen lanzar
    for nombre, tol in (("contraste_infinito", lambda t: (t[0], t[1], float("inf"))), ("salto_infinito", lambda t: (float("inf"), t[1], t[2])),
                        ("desfase_enorme", lambda t: (t[0], 1e308, t[2])), ("salto_entero_enorme", lambda t: (10 ** 400, t[1], t[2])),
                        ("tol_None", lambda t: None), ("tol_vacio", lambda t: ()), ("tol_corto", lambda t: (t[0],))):
        f, r = nuevo_reloj()
        r._tol = tol(r._tol)
        f.pasa(1.0)
        try:
            x = r.ahora()
            ok = not x["ok"]
        except Exception as ex:   # noqa: BLE001
            ok, x = False, repr(ex)
        h.chk(f"{nombre}_no_da_instantes_ni_lanza_H01_H02", ok, x)

    class FotoContradictoria:
        def estado_diario(self):
            return {"operativo": False, "bloqueo": None, "lineas": 2, "sincronizado": True, "motivo_desincronizado": None}
    h.chk("una_foto_no_operativa_es_ROJO_H04", comp(nuevo(), "diario", diario=FotoContradictoria())["nivel"] == "ROJO")

    # ------------------------------------------------------------------ T-72: estado del diario
    with tempfile.TemporaryDirectory() as tmp:
        o = nuevo()
        d = nuevo_diario(os.path.join(tmp, "a"), o)
        e = d.estado_diario()
        h.chk("diario_nuevo_operativo_y_sincronizado", e == {"operativo": True, "bloqueo": None, "lineas": 1, "sincronizado": True,
                                                           "motivo_desincronizado": None}, e)
        assert d.barrer(AHORA)["ok"]
        h.chk("tras_una_operacion_cuenta_sus_lineas", d.estado_diario()["lineas"] == 3)
        tam = os.path.getsize(d._ruta_diario)
        antes = (d._n, d._roto, d._huella, copy.deepcopy(vars(d.orquestador)))
        d.estado_diario()
        h.chk("estado_diario_no_cambia_nada", (d._n, d._roto, d._huella, vars(d.orquestador)) == antes
              and os.path.getsize(d._ruta_diario) == tam)

        # H-05 de la QA de T-79: un cambio por fuera del diario. Antes el panel daba VERDE y la operación siguiente, DI-06
        d.cotizaciones["EURUSD"] = {"ultima": 1.0}
        e = d.estado_diario()
        h.chk("un_cambio_por_fuera_se_ve_desincronizado_H05", e["sincronizado"] is False and e["operativo"] is False
              and e["motivo_desincronizado"] == "el estado cambió sin pasar por el diario" and e["bloqueo"] is None, e)
        k = comp(o, "diario", diario=d)
        h.chk("y_el_panel_lo_pinta_ROJO_antes_de_operar_H05", k["nivel"] == "ROJO" and "DI-06" in k["motivo"], k)
        h.chk("mirar_no_bloquea_el_diario", d._roto is None)
        r1 = d.barrer(AHORA)
        h.chk("la_operacion_siguiente_da_DI06_como_avisaba", r1["codigo"] == "DI-06", r1)
        e = d.estado_diario()
        h.chk("bloqueado_lleva_su_codigo", e["bloqueo"] == {"codigo": "DI-06", "motivo": "el estado cambió sin pasar por el diario"}
              and e["operativo"] is False, e)
        k = comp(o, "diario", diario=d)
        h.chk("bloqueado_es_ROJO_con_el_codigo", k["nivel"] == "ROJO" and "DI-06" in k["motivo"] and "bloqueado" in k["motivo"], k)

        # el fichero del diario reescrito por otro proceso
        o = nuevo()
        d = nuevo_diario(os.path.join(tmp, "b"), o)
        with open(d._ruta_diario, "a", encoding="ascii") as fh:
            fh.write("\n")
        e = d.estado_diario()
        h.chk("fichero_reescrito_por_fuera_desincronizado", e["sincronizado"] is False and e["motivo_desincronizado"] == di.FUERA, e)
        h.chk("y_el_panel_ROJO", comp(o, "diario", diario=d)["nivel"] == "ROJO")

        # la consola ya no lee los privados: lo que manda es la foto pública
        class Publico:
            _roto = "un privado que la consola ya no mira"
            _n = 10 ** 9

            def estado_diario(self):
                return {"operativo": True, "bloqueo": None, "lineas": 2, "sincronizado": True, "motivo_desincronizado": None}
        h.chk("la_consola_usa_la_foto_publica", comp(nuevo(), "diario", diario=Publico())["nivel"] == "VERDE")

        class Raro:
            def __init__(self, foto):
                self.foto = foto

            def estado_diario(self):
                return self.foto
        ilegibles = (None, "x", [], {"bloqueo": "texto"}, {"bloqueo": None, "sincronizado": "sí", "lineas": 2},
                     {"bloqueo": None, "sincronizado": True, "lineas": 0}, {"bloqueo": None, "sincronizado": True})
        h.chk("una_foto_ilegible_es_ROJO_sin_lanzar", all(comp(nuevo(), "diario", diario=Raro(x))["nivel"] == "ROJO" for x in ilegibles))

        class Lanza:
            def estado_diario(self):
                raise RuntimeError("roto")
        h.chk("si_estado_diario_lanza_es_ROJO", comp(nuevo(), "diario", diario=Lanza())["nivel"] == "ROJO"
              and panel(nuevo(), AHORA, diario=Lanza())["nivel"] == "ROJO")
        h.chk("estado_diario_es_del_Diario_no_del_Orquestador", "estado_diario" in vars(di.Diario)
              and not hasattr(nuevo(), "estado_diario"))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO RELOJ Y DIARIO T-72:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
