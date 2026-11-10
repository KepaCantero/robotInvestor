"""Pruebas de T-03 (quinta parte, V0.47): el reloj del sistema. Las fuentes (reloj de pared y monótono) se inyectan para simular
saltos, derivas, retrocesos, suspensiones, fuentes rotas y máquinas sin poner en hora; una prueba usa el reloj real. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_reloj_t03.py
"""
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
import reloj as rl  # noqa: E402
from ejecucion_g import BrokerSimulado, cotizar, foto_cartera  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo  # noqa: E402

BASE = datetime(2026, 11, 6, 9, 0, 0, tzinfo=timezone.utc).timestamp()
M = "Revisado: alguien cambió la hora de la máquina por error"


def iso(s):
    return datetime.fromtimestamp(s, timezone.utc).isoformat()


class Fuentes:
    """Reloj de pared y monótono controlables."""

    def __init__(self, pared=BASE, mono=1000.0):
        self.p, self.m = pared, mono
        self.falla = None

    def pared(self):
        if self.falla == "pared":
            raise OSError("sin reloj")
        return self.p

    def mono(self):
        return self.m

    def pasa(self, s, pared=None):
        self.m += s
        self.p += s if pared is None else pared


def nuevo_reloj(pared=BASE, contrastar=True, **kw):
    """Un reloj con fuentes simuladas, ya contrastado con una referencia que coincide con él (salvo contrastar=False)."""
    f = Fuentes(pared)
    r = rl.Reloj(f.pared, f.mono, **kw)
    if contrastar:
        assert r.contrastar(iso(f.p), "REFERENCIA DE PRUEBA")["ok"]
    return f, r


class SinInstante:
    ultimo_ahora = None


def main():
    h = Arnes()
    # ------------------------------------------------------------------------------------------- lecturas normales
    f, r = nuevo_reloj(contrastar=False)
    h.chk("sin_contrastar_no_da_instantes_RL04", r.ahora()["codigo"] == "RL-04")
    c = r.contrastar(iso(BASE), "INTERMEDIARIO")
    a = r.ahora()
    h.chk("contrastado_da_el_instante_en_el_formato_del_marco", c["ok"] and a["ok"] and a["ahora"] == "2026-11-06T09:00:00+00:00"
          and pe._instante_ok(a["ahora"]), (c, a))
    f.pasa(0.4)
    h.chk("con_fraccion_de_segundo", r.ahora()["ahora"] == "2026-11-06T09:00:00.400000+00:00")
    f.pasa(61)
    h.chk("avanza_con_el_tiempo", r.ahora()["ahora"] == "2026-11-06T09:01:01.400000+00:00")
    deriva = True
    for _ in range(1000):   # ajuste lento de la sincronización (0,5 ms por segundo): no es un salto
        f.pasa(1, pared=1.0005)
        deriva = deriva and r.ahora()["ok"]
    h.chk("la_deriva_lenta_no_es_un_salto", deriva and r.bloqueo is None)
    f, r = nuevo_reloj()
    f.pasa(10, pared=9.5)
    h.chk("salto_pequeno_dentro_de_la_tolerancia_pasa", r.ahora()["ok"])
    f, r = nuevo_reloj()
    f.pasa(3)
    t3 = r.ahora()["ahora"]
    f.pasa(1, pared=-0.5)   # la pared retrocede 0,5 s respecto a la última lectura
    x = r.ahora()
    h.chk("nunca_un_instante_anterior_a_otro_ya_dado", x["ok"] and x["ahora"] == t3, x)
    f, r = nuevo_reloj(max_sin_contraste_s=3600)
    f.pasa(3601)
    h.chk("pasado_el_plazo_pide_otro_contraste_RL04", r.ahora()["codigo"] == "RL-04" and r.contrastar(iso(f.p), "INTERMEDIARIO")["ok"]
          and r.ahora()["ok"])
    rr = rl.Reloj()   # el reloj real del sistema
    c = rr.contrastar(iso(time.time()), "REFERENCIA LOCAL")
    a, b = rr.ahora(), rr.ahora()
    h.chk("con_el_reloj_real", c["ok"] and a["ok"] and b["ok"] and pe._instante_ok(a["ahora"]) and a["ahora"] <= b["ahora"], (c, a, b))

    # ------------------------------------------------------------------------------------------- saltos (RL-01) y bloqueo (RL-04)
    f, r = nuevo_reloj()
    f.pasa(1, pared=3601)
    x = r.ahora()
    h.chk("RL01_salto_adelante", x["codigo"] == "RL-01" and x["ahora"] is None and r.bloqueo["codigo"] == "RL-01", x)
    h.chk("RL04_bloqueado_hasta_rearmar", r.ahora()["codigo"] == "RL-04" and r.contrastar(AHORA, "INTERMEDIARIO")["codigo"] == "RL-04")
    h.chk("RL06_rearme_que_no_es_del_operador", r.rearmar("G", M)["codigo"] == "RL-06" and r.rearmar("OPERADOR", "corto")["codigo"] == "RL-06"
          and r.bloqueo is not None)
    h.chk("rearme_del_operador", r.rearmar("OPERADOR", M)["ok"] and r.bloqueo is None and r.incidentes[-1]["codigo"] == "REARME"
          and r.incidentes[-1]["actor"] == "OPERADOR")
    h.chk("tras_rearmar_hay_que_contrastar_RL04", r.ahora()["codigo"] == "RL-04")
    h.chk("y_el_contraste_destapa_la_hora_mala_RL03", r.contrastar(iso(BASE + 1), "INTERMEDIARIO")["codigo"] == "RL-03")
    r.rearmar("OPERADOR", M)
    x = r.contrastar(iso(f.p), "INTERMEDIARIO")
    h.chk("si_la_hora_nueva_es_la_buena_sigue", x["ok"] and r.ahora()["ahora"] == "2026-11-06T10:00:01+00:00", x)
    h.chk("RL06_rearmar_sin_bloqueo", r.rearmar("OPERADOR", M)["codigo"] == "RL-06")
    f, r = nuevo_reloj()
    r.ahora()
    f.pasa(1, pared=-3600)
    h.chk("RL01_salto_atras", r.ahora()["codigo"] == "RL-01")
    r.rearmar("OPERADOR", M)
    h.chk("RL01_tras_rearmar_sigue_por_detras_de_lo_ya_dado", r.contrastar(iso(f.p), "INTERMEDIARIO")["codigo"] == "RL-01")
    f, r = nuevo_reloj()
    f.m -= 5
    h.chk("RL01_el_monotono_retrocede", r.ahora()["codigo"] == "RL-01")
    f, r = nuevo_reloj(max_salto_s=10)
    f.pasa(1, pared=9)
    h.chk("tolerancia_configurable", r.ahora()["ok"])

    # ------------------------------------------------------------------------------------------- revisión de V0.47
    # r01: congelado, acelerado o a saltos pequeños
    f, r = nuevo_reloj()
    ok = True
    for _ in range(100):
        f.pasa(1, pared=0)
        ok = ok and r.ahora()["ok"]
    h.chk("r01_reloj_congelado_RL01", not ok and r.bloqueo["codigo"] == "RL-01")
    f, r = nuevo_reloj()
    ok = True
    for _ in range(100):
        f.pasa(0.1, pared=2.05)
        ok = ok and r.ahora()["ok"]
    h.chk("r01_reloj_acelerado_RL01", not ok and r.bloqueo["codigo"] == "RL-01")
    f, r = nuevo_reloj()
    ok = True
    for _ in range(20):
        f.pasa(1, pared=2.9)
        ok = ok and r.ahora()["ok"]
    h.chk("r01_muchos_saltos_pequenos_RL01", not ok and r.bloqueo["codigo"] == "RL-01")
    # r02: una máquina que arranca con una fecha adelantada no llega a dar instantes
    f, r = nuevo_reloj(pared=datetime(2099, 1, 1, tzinfo=timezone.utc).timestamp(), contrastar=False)
    h.chk("r02_arranque_en_el_futuro_no_da_instantes", r.ahora()["codigo"] == "RL-04"
          and r.contrastar(AHORA, "INTERMEDIARIO")["codigo"] == "RL-03" and r.ahora()["codigo"] == "RL-04")
    # r03: con el intermediario un poco por delante (y con milisegundos), G registra fotos y cotizaciones
    o = nuevo()
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10, "GBPUSD": 1.30}, "2026-11-06T09:00:03.250000+00:00")
    f, r = nuevo_reloj(contrastar=False)
    c = r.contrastar(b.hora_datos, "INTERMEDIARIO")
    h.chk("r03_el_contraste_da_el_mayor_de_los_dos", c["ok"] and c["ahora"] == b.hora_datos and c["desfase_s"] == -3.25, c)
    h.chk("r03_G_registra_foto_y_cotizacion_con_ese_instante", foto_cartera(o, b, c["ahora"]) is not None
          and cotizar(o, b, "EURUSD", c["ahora"])["ok"])
    f.pasa(1)
    h.chk("r03_y_despues_no_se_vuelve_atras", r.ahora()["ahora"] == b.hora_datos)
    # r04: tras un RL-02, el rearme no deja dar instantes anteriores al estado
    o = nuevo()
    f, r = nuevo_reloj(pared=BASE - 3600, contrastar=False)
    h.chk("r04_RL02", r.comprobar_estado(o)["codigo"] == "RL-02")
    r.rearmar("OPERADOR", M)
    h.chk("r04_tras_rearmar_sigue_sin_dar_instantes_atrasados", r.contrastar(iso(f.p), "INTERMEDIARIO")["codigo"] != "OK"
          and r.ahora()["ahora"] is None)
    f, r = nuevo_reloj(pared=BASE + 1, contrastar=False)
    h.chk("r04_comprobar_estado_no_da_el_instante", r.comprobar_estado(o) == {"ok": True, "codigo": "OK",
                                                                               "motivo": "el reloj no va detrás del estado", "ahora": None})
    # r06: el desfase y la comparación con el estado usan la lectura en bruto
    f, r = nuevo_reloj(pared=BASE + 0.6, contrastar=False)
    h.chk("r06_desfase_en_bruto", r.contrastar("2026-11-06T09:00:05.510000+00:00", "INTERMEDIARIO")["ok"])

    class Estado:
        ultimo_ahora = "2026-11-06T09:00:00.500000+00:00"
    f, r = nuevo_reloj(pared=BASE + 0.7, contrastar=False)
    h.chk("r06_estado_con_fraccion_no_es_RL02_falso", r.comprobar_estado(Estado())["ok"])
    # r07: una suspensión de la máquina (el monótono por defecto sigue contando en Linux)
    if hasattr(time, "CLOCK_BOOTTIME"):
        h.chk("r07_monotono_que_cuenta_la_suspension", abs(rl.Reloj()._monotono() - time.clock_gettime(time.CLOCK_BOOTTIME)) < 1)
    else:
        h.chk("r07_monotono_que_cuenta_la_suspension (sin CLOCK_BOOTTIME aquí)", True)
    # r08: tipos raros en las fuentes: nada lanza y lo que no es un número finito es RL-05

    class Mentiroso(float):
        def __floor__(self):
            return 0
    for nombre, (pared, mono) in (("entero_enorme", (10 ** 400, 1.0)), ("float_mentiroso", (Mentiroso(0.0), 1.0)),
                                  ("monotono_enorme", (BASE, 10 ** 400))):
        try:
            x = rl.Reloj(lambda v=pared: v, lambda v=mono: v).contrastar(AHORA, "INTERMEDIARIO")
            h.chk(f"r08_{nombre}_RL05", x["codigo"] == "RL-05", x)
        except Exception as ex:   # noqa: BLE001
            h.chk(f"r08_{nombre}_RL05", False, type(ex).__name__)

    class GetQueLanza(dict):
        def get(self, *a):
            raise RuntimeError("x")
    for nombre, res in (("codigo_raro", {"codigo": object()}), ("get_que_lanza", GetQueLanza(codigo="RL-01"))):
        try:
            h.chk(f"r08_degradar_con_{nombre}_no_lanza", not rl.degradar_por_reloj(nuevo(), res)["ok"])
        except Exception as ex:   # noqa: BLE001
            h.chk(f"r08_degradar_con_{nombre}_no_lanza", False, type(ex).__name__)
    # r09: constructor
    for nombre, kw in (("salto_cero", {"max_salto_s": 0}), ("desfase_negativo", {"max_desfase_s": -1}), ("salto_texto", {"max_salto_s": "2"}),
                       ("fuente_no_invocable", {"pared": 5}), ("salto_enorme", {"max_salto_s": 10 ** 400}), ("salto_que_desactiva", {"max_salto_s": 1e9}),
                       ("desfase_que_desactiva", {"max_desfase_s": 1e6}), ("contraste_cero", {"max_sin_contraste_s": 0})):
        try:
            rl.Reloj(**kw)
            ok = False
        except ValueError:
            ok = True
        h.chk(f"r09_constructor_rechaza_{nombre}", ok)

    class Falsa:
        def __call__(self):
            return BASE

        def __bool__(self):
            return False
    h.chk("r09_una_fuente_falsa_en_booleano_se_usa", rl.Reloj(Falsa(), lambda: 1.0)._pared() == BASE)
    f, r = nuevo_reloj()
    h.chk("menor_referencia_de_1970_o_sin_zona_RL06", r.contrastar("1970-01-01T00:00:00+00:00", "X")["codigo"] == "RL-06"
          and r.contrastar("2026-11-06T09:00:00", "X")["codigo"] == "RL-06" and r.bloqueo is None)

    # ------------------------------------------------------------------------------------------- lecturas imposibles (RL-05)
    for nombre, cambio in (("lanza", lambda f: setattr(f, "falla", "pared")), ("nan", lambda f: setattr(f, "p", float("nan"))),
                           ("none", lambda f: setattr(f, "p", None)), ("texto", lambda f: setattr(f, "p", "ahora")),
                           ("bool", lambda f: setattr(f, "p", True)), ("1970", lambda f: setattr(f, "p", 0.0)),
                           ("2101", lambda f: setattr(f, "p", datetime(2101, 1, 1, tzinfo=timezone.utc).timestamp())),
                           ("enorme", lambda f: setattr(f, "p", 1e300))):
        f, r = nuevo_reloj()
        cambio(f)
        x = r.ahora()
        h.chk(f"RL05_{nombre}", x["codigo"] == "RL-05" and r.bloqueo is not None, x)
    h.chk("RL05_monotono_que_lanza", rl.Reloj(lambda: BASE, lambda: 1 / 0).ahora()["codigo"] == "RL-05")

    # ------------------------------------------------------------------------------------------- arranque con un estado (RL-02)
    o = nuevo()   # ha visto AHORA (2026-11-06T09:00:00)
    f, r = nuevo_reloj()
    h.chk("estado_del_mismo_instante_vale", r.comprobar_estado(o)["ok"])
    f, r = nuevo_reloj(pared=BASE - 60, contrastar=False)
    x = r.comprobar_estado(o)
    h.chk("RL02_reloj_detras_del_estado", x["codigo"] == "RL-02" and r.bloqueo["codigo"] == "RL-02", x)
    f, r = nuevo_reloj(pared=BASE - 3, contrastar=False)
    r.comprobar_estado(o)
    r.contrastar(iso(f.p), "INTERMEDIARIO")
    h.chk("el_estado_es_el_suelo_de_los_instantes", r.ahora()["ahora"] == AHORA)
    h.chk("estado_sin_instantes_vale", nuevo_reloj()[1].comprobar_estado(SinInstante())["ok"])

    class Roto:
        ultimo_ahora = "ayer"
    h.chk("RL02_estado_con_un_instante_ilegible", nuevo_reloj()[1].comprobar_estado(Roto())["codigo"] == "RL-02")

    # ------------------------------------------------------------------------------------------- referencias externas (RL-03, RL-06)
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, "2026-11-06T09:00:03+00:00")
    f, r = nuevo_reloj()
    x = r.contrastar(b.hora_datos, "INTERMEDIARIO")
    h.chk("contraste_dentro_de_la_tolerancia", x["ok"] and x["desfase_s"] == -3.0, x)
    b.avanzar_reloj("2026-11-06T09:00:30+00:00")
    x = r.contrastar(b.hora_datos, "INTERMEDIARIO")
    h.chk("RL03_desfase_con_el_intermediario", x["codigo"] == "RL-03" and x["desfase_s"] == -30.0 and r.bloqueo["codigo"] == "RL-03", x)
    f, r = nuevo_reloj()
    h.chk("RL03_reloj_por_delante", r.contrastar("2026-11-06T08:59:50+00:00", "PROVEEDOR")["codigo"] == "RL-03")
    f, r = nuevo_reloj()
    h.chk("RL06_referencia_ilegible_no_bloquea", r.contrastar("ayer", "PROVEEDOR")["codigo"] == "RL-06"
          and r.contrastar(None, "PROVEEDOR")["codigo"] == "RL-06" and r.contrastar(AHORA, "")["codigo"] == "RL-06" and r.bloqueo is None)

    # ------------------------------------------------------------------------------------------- uso con el Orquestador y degradación
    f, r = nuevo_reloj()
    o = nuevo({"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}})
    f.pasa(120)
    r.comprobar_estado(o)
    a = r.ahora()
    h.chk("el_Orquestador_opera_con_el_instante_del_reloj", a["ok"] and o.barrer(a["ahora"])["ok"] and o.ultimo_ahora == a["ahora"])
    f.pasa(1, pared=7200)
    inc = r.ahora()
    d = rl.degradar_por_reloj(o, inc)
    h.chk("tras_un_incidente_todas_las_carteras_a_L1", d["ok"] and d["carteras"] == list(rl.CARTERAS) and d["ya_degradadas"] == []
          and all(o.nivel(c) == "L1" for c in rl.CARTERAS) and o.ultimo_ahora == a["ahora"], d)
    d2 = rl.degradar_por_reloj(o, inc)
    h.chk("si_ya_estaban_degradadas_se_dice", d2["ok"] and d2["ya_degradadas"] == list(rl.CARTERAS))
    h.chk("degradar_solo_con_un_incidente", rl.degradar_por_reloj(o, {"ok": True, "codigo": "OK"})["codigo"] == "RL-06"
          and rl.degradar_por_reloj(o, {"codigo": "RL-04"})["codigo"] == "RL-06" and rl.degradar_por_reloj(o, None)["codigo"] == "RL-06")
    h.chk("RL07_degradar_sin_instantes", rl.degradar_por_reloj(SinInstante(), inc)["codigo"] == "RL-07")
    h.chk("RL07_degradar_con_algo_que_no_es_un_Orquestador", rl.degradar_por_reloj(object(), inc)["codigo"] == "RL-07")
    # con el diario: la degradación queda anotada y sobrevive al reinicio; con el diario bloqueado, RL-07
    with tempfile.TemporaryDirectory() as tmp:
        re_, rd = os.path.join(tmp, "e"), os.path.join(tmp, "d")
        dd = di.crear(nuevo(), re_, rd, AHORA)["diario"]
        f, r = nuevo_reloj()
        f.pasa(60)
        r.comprobar_estado(dd)
        f.pasa(1, pared=-600)
        d = rl.degradar_por_reloj(dd, r.ahora())
        ab = di.abrir(re_, rd)
        h.chk("con_el_diario_la_degradacion_sobrevive_al_reinicio", d["ok"] and ab["ok"]
              and all(ab["diario"].nivel(c) == "L1" for c in rl.CARTERAS) and pe.volcar(ab["diario"].orquestador, AHORA) == pe.volcar(dd.orquestador, AHORA))
        f2, r2 = nuevo_reloj(pared=BASE - 3600, contrastar=False)
        h.chk("RL02_al_reabrir_con_el_reloj_atrasado", r2.comprobar_estado(ab["diario"])["codigo"] == "RL-02")
        d3 = ab["diario"]
        d3.avisos.append({"tocado": True})   # un cambio por fuera bloquea el diario (DI-06)
        h.chk("RL07_con_el_diario_bloqueado", rl.degradar_por_reloj(d3, {"codigo": "RL-01", "motivo": "x"})["codigo"] == "RL-07")
    h.chk("los_incidentes_quedan_en_el_reloj", [x["codigo"] for x in r.incidentes] == ["RL-01"])

    # T-84 (QA de la V0.63, H-07; sonda r04): dos propiedades del reloj que ninguna batería fijaba
    f, r = nuevo_reloj(contrastar=False)
    c = r.contrastar(iso(BASE - 3), "INTERMEDIARIO")   # el intermediario va 3 s por detrás del reloj
    h.chk("t84_contrastar_da_el_mayor_con_el_reloj_por_delante", c["ok"] and c["ahora"] == iso(BASE) and c["desfase_s"] == 3.0, c)
    f, r = nuevo_reloj(contrastar=False)
    c = r.contrastar(iso(BASE + 3), "INTERMEDIARIO")   # y 3 s por delante: el instante es el del intermediario
    h.chk("t84_contrastar_da_el_mayor_con_el_intermediario_por_delante", c["ok"] and c["ahora"] == iso(BASE + 3) and c["desfase_s"] == -3.0, c)
    f, r = nuevo_reloj()
    marcha = True
    for _ in range(24):                               # un día de marcha, una lectura por hora, con contraste
        f.pasa(3600)
        marcha &= r.contrastar(iso(f.p), "INTERMEDIARIO")["ok"]
    tolerada = r.max_salto_s + rl.TASA_MAX * 24 * 3600   # la deriva que ya tolera el ancla tras un día (45 s)
    f.p += 10                                         # alguien adelanta la hora 10 s (el monótono no)
    a = r.ahora()
    h.chk("t84_tras_un_dia_de_marcha_un_salto_de_10_s_se_para_RL01", marcha and 10 < tolerada and a["codigo"] == "RL-01" and a["ahora"] is None
          and r.bloqueo["codigo"] == "RL-01", (marcha, tolerada, a))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO RELOJ T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
