"""Semana simulada con reloj, diario, puntos de control y reinicios (V0.63, pieza 4 del kit 2). Dos sistemas gemelos
recorren la misma semana simulada — del lunes 9 al viernes 13 de noviembre de 2026, de 08:00 a 20:00 UTC —: uno con el
Orquestador en memoria y otro con el diario de operaciones (T-03), que se reinicia (se reabre desde disco) tras cada paso y
debe quedar idéntico al gemelo. A diferencia de la jornada (pruebas_jornada.py), el instante no se escribe a mano: sale del
Reloj del sistema con fuentes simuladas (clase Maquina), contrastado con la hora del intermediario en cada arranque de la
mañana, y la semana cruza cambios de día UTC, datos que llegaron el viernes anterior (el encargo y el sobre del lunes se
emitieron con el corte del viernes 6) y un corte a mitad del miércoles. Cada noche hay punto de control y se para el sistema;
cada mañana se arranca: se abre el diario, se comprueba el estado (RL-02) y se contrasta el reloj. El jueves el estado va
firmado con clave desde el arranque de ese día (diario nuevo con clave a partir del Orquestador cargado, en otra carpeta, porque
crear no pisa ficheros). La semana toca: encargo y sobre de dos candidatos y D con ganador (lunes), vigilancia cada hora con
precios que suben y una reducción parcial a mano (martes), un segundo expediente en TRADING (EUR/JPY, con sello de corte 2026-11-10
propio, que es el que sigue VIGENTE ese día) hasta ejecutado y una operación LIBRE declarada (miércoles), el stop de la primera
posición ejecutado por el intermediario y confirmado por H (H-01) con conciliación, degradación y restablecimiento (jueves), y
kill-switch manual, conciliación, rearme con la lista del §11 y cierre de lo que queda (viernes). Al final: conciliación limpia,
el diario firmado empieza en el PUNTO del viernes y una migración de prueba (a_010 → migraciones.migrar) da un estado que se
carga y sigue operando (una vigilancia más, sin incidencias). Es la red de seguridad de todas las integraciones que vienen.

Uso: python3 pruebas/pruebas_semana.py
"""
import os
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import json  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
import reloj as rl  # noqa: E402
from ejecucion_g import BrokerSimulado, cerrar, conciliar, declarar_manual, ejecutar, foto_cartera, kill_switch, reducir  # noqa: E402
from pruebas_encargo import SELLOS as SELLOS_ENC  # noqa: E402
from pruebas_k import construir as construir_k  # noqa: E402
from pruebas_manual import a_mano, libre  # noqa: E402
from pruebas_migraciones_t03 import a_010  # noqa: E402
from pruebas_orquestador import ENTRADA, Arnes, autorizar_op, dim, encargo, nuevo, registrar_motor, sobre  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from vigilancia import vigilar  # noqa: E402

S2 = SELLOS_ENC["K-20261106-001"]                 # sello de corte 2026-11-06: el VIGENTE el lunes (tope de 1 día hábil en TACTICA)
_E10, _R10 = construir_k(hasta=date(2026, 11, 10), solicitada="2026-11-10", cartera="TRADING",
                         ctx={"ahora": "2026-11-11T07:00:00+00:00", "secuencia": 1})
S10 = _R10["sello"]                               # sello de corte 2026-11-10: el VIGENTE el miércoles para TRADING
assert S10 is not None and S10["estado"] == "VIGENTE", _R10

CLAVE = bytes(range(48))                          # determinista (48 valores de byte distintos: vale para la firma)
STOP_L = {"id": "STOP-1", "tipo": "STOP", "metrica": "precio", "operador": "<=", "umbral": 1.05, "unidad": "USD"}
OBJ_L = {"id": "OBJ-1", "tipo": "OBJETIVO", "metrica": "precio", "operador": ">=", "umbral": 1.14, "unidad": "USD"}
INV_L = {"id": "INV-1", "tipo": "INVALIDEZ", "metrica": "precio_cierre", "operador": "<", "umbral": 1.05, "unidad": "USD"}
ENTRADA_L = {**ENTRADA, "limite": 1.10, "ventana_hasta": "2026-11-09T17:00:00+00:00"}   # dentro de la ventana del sobre del lunes
SALIDA_L = {"condiciones": [STOP_L, OBJ_L, INV_L], "fecha": "2026-12-05"}               # revisión dentro de la del sobre
STOP_T = {"id": "STOP-1", "tipo": "STOP", "metrica": "precio", "operador": "<=", "umbral": 155.0, "unidad": "JPY"}
OBJ_T = {"id": "OBJ-1", "tipo": "OBJETIVO", "metrica": "precio", "operador": ">=", "umbral": 172.0, "unidad": "JPY"}
INV_T = {"id": "INV-1", "tipo": "INVALIDEZ", "metrica": "precio_cierre", "operador": "<", "umbral": 155.0, "unidad": "JPY"}
ENTRADA_T = {"limite": 165.0, "ventana_hasta": "2026-11-12T17:00:00+00:00", "instrumento": "EURJPY", "activo_base": "EUR",
             "via_acceso": "Futuro de divisas, vencimiento trimestral", "apalancamiento": 1.0, "cantidad": 50.0}
SALIDA_T = {"condiciones": [STOP_T, OBJ_T, INV_T], "fecha": "2026-12-05"}
# el contrato CT-G-02 solo cubre candidatos con el euro como divisa base (divisa_base es una constante del esquema), así que el
# segundo expediente de la semana es EUR/JPY; el tipo de cambio del yen lo deduce el propio intermediario del precio del par
DIAS = {"lunes": "2026-11-09T08:10:00+00:00", "martes": "2026-11-10T08:00:00+00:00", "miercoles": "2026-11-11T08:00:00+00:00",
        "jueves": "2026-11-12T08:00:00+00:00", "viernes": "2026-11-13T08:00:00+00:00"}
NOMBRES_DIA = {"lunes": "lunes", "martes": "martes", "miercoles": "miércoles", "jueves": "jueves", "viernes": "viernes"}
CFG_SEMANA = {"nivel_autonomia": {"TACTICA": "L2", "TRADING": "L2"}}   # el escenario de la semana, a nivel de módulo para que el gemelo dorado lo importe (foto_semana) y no lo duplique a mano


def iso(s):
    return datetime.fromtimestamp(s, timezone.utc).isoformat()


def ts(txt):
    return datetime.fromisoformat(txt).timestamp()


class Fuentes:
    """Pared y monótono de la semana: dos relojes de máquina sanos que avanzan siempre lo mismo (sin saltos ni derivas; los
    saltos y las fuentes rotas tienen su batería en pruebas_reloj_t03)."""

    def __init__(self, pared):
        self.p, self.m = pared, 1000.0

    def pared(self):
        return self.p

    def mono(self):
        return self.m

    def pasa(self, s):
        self.m += s
        self.p += s


class Maquina:
    """La máquina de la semana: un Reloj con fuentes simuladas y los intermediarios, cuya hora_datos avanza a la vez. arrancar(t)
    es un arranque de máquina (Reloj nuevo: la historia del reloj vive en memoria y se pierde al parar) con comprobar_estado y
    contrastar; pasar(s) avanza pared, monótono y los intermediarios lo mismo; instante() devuelve el de
    Reloj.contrastar(broker.hora_datos, "INTERMEDIARIO") y lo apunta: es el único instante que usa la semana."""

    def __init__(self, o, brokers, t0):
        self.o, self.brokers = o, list(brokers)
        self.f, self.reloj = None, None
        self.instantes = []
        self.arrancar(t0)

    def arrancar(self, t):
        self.f = Fuentes(ts(t))
        self.reloj = rl.Reloj(self.f.pared, self.f.mono)
        ce = self.reloj.comprobar_estado(self.o)
        assert ce["ok"], ("comprobar_estado", ce)
        for b in self.brokers:
            b.avanzar_reloj(t)
        c = self.reloj.contrastar(self.brokers[0].hora_datos, "INTERMEDIARIO")
        assert c["ok"], ("contrastar", c)
        self.instantes.append(c["ahora"])
        return c["ahora"]

    def pasar(self, s):
        self.f.pasa(s)
        for b in self.brokers:
            b.avanzar_reloj(iso(self.f.p))

    def instante(self):
        c = self.reloj.contrastar(self.brokers[0].hora_datos, "INTERMEDIARIO")
        assert c["ok"], c
        self.instantes.append(c["ahora"])
        return c["ahora"]

    def para(self):
        self.f, self.reloj = None, None


def broker():
    return BrokerSimulado(100000.0, {"EURUSD": 1.10, "GBPUSD": 1.30, "EURJPY": 165.0}, DIAS["lunes"])


def lista_rearme():
    """La lista completa del §11 (como en la jornada)."""
    return {k: True for k in ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")}


def encargo_trading(o):
    """El encargo de EXP-0003 (TRADING, EUR/JPY): mandato vigente de TRADING, restricciones dentro del mandato (1–28 días)
    y fechas de la semana (emitido el miércoles antes del paso, caduca el jueves)."""
    en = encargo(3, corte="2026-11-10", sello=S10["sello_id"], producer="GESTOR_TRADING")
    en["payload"]["cartera_destino"] = "TRADING"
    en["payload"]["mandato_ref"] = o.mandato("TRADING")["referencia"]
    en["emitido_en"] = "2026-11-11T08:05:00+00:00"
    en["valid_until"] = "2026-11-12T12:00:00+00:00"
    en["payload"]["presupuesto"]["entrega_antes_de"] = "2026-11-11T20:00:00+00:00"
    en["payload"]["candidato"]["instrumento"] = "EUR/JPY"   # R-09: el mismo instrumento que analiza el sobre
    en["payload"]["restricciones"] = {"horizonte_dias": {"min": 14, "max": 28}}   # E-05: dentro del mandato de TRADING
    return en


def sobre_trading():
    """El sobre de EXP-0003: el de corte 2026-11-10 con el sello del martes, adaptado a EUR/JPY (precios en JPY, la divisa de
    cotización) y con la invalidez de su tesis en la misma divisa."""
    s = sobre(3, corte="2026-11-10", sello=S10["sello_id"])
    p = s["payload"]
    p["identificacion"]["instrumento"] = "EUR/JPY"
    p["identificacion"]["direccion"] = "LARGO"
    p["identificacion"]["cartera_compatible"] = ["TRADING", "TACTICA"]   # R-06: responde al encargo de TRADING
    for e in p["capa2"]["escenarios"]:
        e["horizonte_dias"] = 21   # V-25: horizonte común, dentro del mandato de TRADING
    p["capa2"]["horizonte_dias"] = 21
    p["entrada_salida"]["stop"]["valor"] = 155.0
    p["entrada_salida"]["stop"]["unidad"] = "JPY"   # O-21: los precios del sobre van en la divisa de cotización
    p["entrada_salida"]["objetivo"]["valor"] = 172.0
    p["entrada_salida"]["objetivo"]["unidad"] = "JPY"
    p["entrada_salida"]["entrada"]["limite"]["valor"] = round(172.0 - (172.0 - 155.0) * 0.01, 6)
    p["entrada_salida"]["entrada"]["limite"]["unidad"] = "JPY"
    p["tesis"]["condiciones_invalidez"][0].update({"umbral": 155.0, "unidad": "JPY"})
    p["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-12T18:00:00+00:00"
    s["emitido_en"] = "2026-11-11T08:20:00+00:00"
    s["valid_until"] = "2026-11-12T18:00:00+00:00"
    return s


def informe_de(o, b, eid, n, t, divisa=None):
    """El informe de F del paso de autorización: emitido con el instante del reloj y vigente una hora (CF-03), con la divisa
    de cotización del instrumento si no es un par con el euro (CF-05)."""
    sol = {"divisa_cotizacion": divisa} if divisa else None
    return informe_f(o, eid, n, cartera=foto_cartera(o, b, t), sol=sol, emitido_en=t, valid_until=iso(ts(t) + 3600))


def a_010_v045(texto):
    """a_010 (pieza 3, V0.62) con la adaptación local de la semana, documentada en el Documento 0: un documento 0.1.0 REAL de
    V0.45 no llevaba los atributos que añadieron V0.51 (ultimas_degradaciones) y V0.53 (libres, cortacircuitos); se quitan para
    que la migración los recree como en un estado de verdad (MIG-003 los deja vacíos y MIG-004 reconstruye las LIBRES desde los
    registros manuales). a_010 no los quita porque solo rehace huellas; con la semana, MIG-003 tocaría ultimas_degradaciones sin
    declararlo y MG-04 lo rechazaría."""
    d = json.loads(texto)
    for k in ("ultimas_degradaciones", "libres", "cortacircuitos"):
        d["estado"].pop(k, None)
    d["atributos"] = sorted(d["estado"])
    d["huella"] = pe._huella(d["estado"])
    return pe._texto(d)


def cortar(ruta_diario):
    """El corte a medias del miércoles: una última línea a medias, como el corte de la jornada (CORTES, linea_a_medias)."""
    with open(ruta_diario, encoding="ascii") as f:
        lineas = f.read().splitlines(keepends=True)
    with open(ruta_diario, "w", encoding="ascii") as f:
        f.write("".join(lineas + [lineas[-1][:25]]))


def con_o16(x):
    """¿Hay algún O-16 (el reloj del Orquestador habría retrocedido) en un resultado, por profundo que venga?"""
    if isinstance(x, dict):
        return x.get("codigo") == "O-16" or any(con_o16(v) for v in x.values())
    if isinstance(x, list):
        return any(con_o16(v) for v in x)
    return False


def pasos_semana():
    """Cada paso es (nombre, función(o, b, t, t_prev) -> resultado comparable, segundos desde el paso anterior). Se aplica igual
    a los dos gemelos con el MISMO instante t (el del Reloj); el tiempo avanza entre pasos, nunca dentro de un paso."""
    def p_encargos(o, b, t, tp):
        r = {}
        for n in (1, 2):
            eid = f"EXP-{n:04d}"
            assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", t)["ok"]
            r[eid] = o.emitir_encargo(eid, encargo(n, corte="2026-11-06", sello="K-20261106-001"), "GESTOR_TACTICA", t)
        return r

    def p_sobres(o, b, t, tp):
        r = {}
        for n in (1, 2):
            r[f"EXP-{n:04d}"] = o.entregar_sobre(f"EXP-{n:04d}", sobre(n, corte="2026-11-06", sello="K-20261106-001"), t)
        return r

    def p_comparar(o, b, t, tp):
        return o.comparar(["EXP-0001", "EXP-0002"], "D", t)

    def p_proponer(o, b, t, tp):
        f = foto_cartera(o, b, t)
        return o.proponer("EXP-0001", ENTRADA_L, SALIDA_L, "GESTOR_TACTICA", t, dim(o, "EXP-0001", ENTRADA_L, SALIDA_L, cartera=f, ahora=t))

    def p_autorizar(o, b, t, tp):
        return autorizar_op(o, "EXP-0001", informe_de(o, b, "EXP-0001", 1, t), t)

    def p_ejecutar(o, b, t, tp):
        return ejecutar(o, "EXP-0001", b, t)

    def p_conciliar(o, b, t, tp):
        return conciliar(o, b, t)

    def p_vigila(precios):
        def f(o, b, t, tp):
            datos = {}
            for ins, precio in precios.items():
                b.mover_precio(ins, precio, t)
                datos[ins] = {"precio": precio, "hora": b.hora_datos}
            return vigilar(o, b, datos, t)
        return f

    def p_reducir(o, b, t, tp):
        b.mover_precio("EURUSD", 1.105, t)   # T-43: G cotiza al reducir con el precio de ahora
        return reducir(o, "POS-EXP-0001", b, t, cantidad=o.posiciones["POS-EXP-0001"]["cantidad"] / 2, actor="OPERADOR",
                       motivo="Reduzco la mitad el martes en la semana simulada")

    def p_registrar_sello(o, b, t, tp):
        return {"sello": o.registrar_sello(S10, t), "motor": registrar_motor(o, S10["sello_id"], t)}

    def p_encargo_trading(o, b, t, tp):
        eid = "EXP-0003"
        r1 = o.detectar(eid, "COR-0003", "DISCRECIONAL", "TRADING", "GESTOR_TRADING", t)
        assert r1["ok"], ("detectar", r1)
        r2 = o.emitir_encargo(eid, encargo_trading(o), "GESTOR_TRADING", t)
        assert r2["ok"], ("encargo", t, r2)
        return {"detectar": r1, "encargo": r2}

    def p_sobre_trading(o, b, t, tp):
        return o.entregar_sobre("EXP-0003", sobre_trading(), t)

    def p_comparar_trading(o, b, t, tp):
        return o.comparar(["EXP-0003"], "D", t)   # T-34: único candidato vivo de TRADING

    def p_proponer_trading(o, b, t, tp):
        f = foto_cartera(o, b, t)
        return o.proponer("EXP-0003", ENTRADA_T, SALIDA_T, "GESTOR_TRADING", t, dim(o, "EXP-0003", ENTRADA_T, SALIDA_T, cartera=f, ahora=t))

    def p_autorizar_trading(o, b, t, tp):
        return autorizar_op(o, "EXP-0003", informe_de(o, b, "EXP-0003", 3, t, divisa="JPY"), t)

    def p_ejecutar_trading(o, b, t, tp):
        return ejecutar(o, "EXP-0003", b, t)

    def p_libre(o, b, t, tp):
        a_mano(b, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")
        return declarar_manual(o, libre(emitido_en=t, ejecutado_en=tp), b, t)

    def p_degradar(o, b, t, tp):
        return o.degradar("TACTICA", "ejercicio de degradación de la semana", "G", t)

    def p_restablecer(o, b, t, tp):
        for a in o.avisos:
            if a["acuse"] is None:
                o.acusar_aviso(a["id"], "OPERADOR", t)
        return o.restablecer_nivel("TACTICA", "OPERADOR", t)

    def p_kill(o, b, t, tp):
        return kill_switch(o, b, t, "fin de la semana simulada")

    def p_rearmar(o, b, t, tp):
        for a in o.avisos:
            if a["acuse"] is None and a.get("prioridad") == "ALTA":
                o.acusar_aviso(a["id"], "OPERADOR", t)
        conciliar(o, b, t)
        return o.rearmar_kill_switch(lista_rearme(), "OPERADOR", t)

    def p_cerrar_restante(o, b, t, tp):
        # tras el rearme las carteras siguen en L1 (periodo mínimo): H no cierra solo, lo hace el operador
        return cerrar(o, "POS-EXP-0003", b, t, actor="OPERADOR", motivo="Cierro lo que queda al terminar la semana")

    return [("lunes_encargos", p_encargos, 900), ("lunes_sobres", p_sobres, 600), ("lunes_comparar", p_comparar, 1200),
            ("lunes_proponer", p_proponer, 1800), ("lunes_autorizar", p_autorizar, 1800), ("lunes_ejecutar", p_ejecutar, 1200),
            ("lunes_conciliar", p_conciliar, 600),
            ("martes_vigila_09", p_vigila({"EURUSD": 1.1005}), 3600), ("martes_vigila_10", p_vigila({"EURUSD": 1.1020}), 3600),
            ("martes_reducir", p_reducir, 3600), ("martes_vigila_12", p_vigila({"EURUSD": 1.1080}), 3600),
            ("martes_vigila_13", p_vigila({"EURUSD": 1.1120}), 3600), ("martes_vigila_14", p_vigila({"EURUSD": 1.1150}), 3600),
            ("miercoles_sello", p_registrar_sello, 900), ("miercoles_encargo", p_encargo_trading, 300),
            ("miercoles_sobre", p_sobre_trading, 900), ("miercoles_comparar", p_comparar_trading, 1200),
            ("miercoles_proponer", p_proponer_trading, 1800), ("miercoles_autorizar", p_autorizar_trading, 1200),
            ("miercoles_ejecutar", p_ejecutar_trading, 1200), ("miercoles_libre", p_libre, 900),
            ("miercoles_vigila_tarde", p_vigila({"EURUSD": 1.1130, "EURJPY": 165.5}), 4 * 3600),
            ("jueves_stop", p_vigila({"EURUSD": 1.04, "EURJPY": 165.8}), 600),
            ("jueves_conciliar", p_conciliar, 300), ("jueves_degradar", p_degradar, 600),
            ("jueves_restablecer", p_restablecer, 600),
            ("viernes_kill", p_kill, 600), ("viernes_conciliar", p_conciliar, 300), ("viernes_rearmar", p_rearmar, 600),
            ("viernes_cerrar", p_cerrar_restante, 900), ("viernes_conciliar_final", p_conciliar, 600)]


def _ok(r):
    return r["ok"]


def _vigila(r):
    return r["conciliacion_ok"] and all(a.get("ok", True) for a in r["acciones"])


# lo que cada paso debe dar (como el ESPERADO de la jornada: sin esto, dos fallos iguales pasarían por «mismo resultado»)
ESPERADO = {"lunes_encargos": lambda r: all(x["ok"] for x in r.values()), "lunes_sobres": lambda r: all(x["ok"] for x in r.values()),
            "lunes_comparar": lambda r: r["ok"] and r["ganador"] == "EXP-0001", "lunes_proponer": _ok, "lunes_autorizar": _ok,
            "lunes_ejecutar": _ok, "lunes_conciliar": _ok,
            "martes_vigila_09": _vigila, "martes_vigila_10": _vigila, "martes_reducir": lambda r: r["ok"] and r["restante"] > 0,
            "martes_vigila_12": _vigila, "martes_vigila_13": _vigila, "martes_vigila_14": _vigila,
            "miercoles_sello": lambda r: r["sello"]["ok"], "miercoles_encargo": lambda r: r["detectar"]["ok"] and r["encargo"]["ok"],
            "miercoles_sobre": _ok, "miercoles_comparar": lambda r: r["ok"] and r["ganador"] == "EXP-0003",
            "miercoles_proponer": _ok, "miercoles_autorizar": _ok, "miercoles_ejecutar": _ok, "miercoles_libre": _ok,
            "miercoles_vigila_tarde": _vigila,
            "jueves_stop": lambda r: r["conciliacion_ok"] and any(a["regla"] == "H-01" and a["ok"] for a in r["acciones"]),
            "jueves_conciliar": _ok, "jueves_degradar": _ok, "jueves_restablecer": _ok,
            "viernes_kill": _ok, "viernes_conciliar": _ok, "viernes_rearmar": _ok, "viernes_cerrar": _ok,
            "viernes_conciliar_final": lambda r: r["ok"] and r["diferencias"] == []}


def main():
    h = Arnes()

    def chk(nombre, cond, detalle=""):
        h.chk(nombre, cond, detalle)
        return bool(cond)

    with tempfile.TemporaryDirectory() as tmp:
        re_, rd = os.path.join(tmp, "estado.json"), os.path.join(tmp, "diario")
        g = nuevo(CFG_SEMANA, sellos=(S2,))                                   # gemelo en memoria
        c = di.crear(nuevo(CFG_SEMANA, sellos=(S2,)), re_, rd, DIAS["lunes"])  # gemelo con diario
        assert c["ok"], c
        d = c["diario"]
        bg, bd = broker(), broker()                                    # cada gemelo, su intermediario
        m = Maquina(d, [bg, bd], DIAS["lunes"])
        semana = []                                                    # todos los instantes que da el Reloj

        def acumula():
            semana.extend(m.instantes)
            m.instantes.clear()

        acumula()
        dia_actual, rutas, con_clave = "lunes", (re_, rd), False
        t_prev = m.instante()
        hubo_o16 = False
        for nombre, paso, delta in pasos_semana():
            dia = nombre.split("_")[0]
            if dia != dia_actual:                                      # ---- noche y arranque de la mañana
                m.pasar(120)
                inst_noche = m.instante()
                acumula()
                pc = d.punto(inst_noche)
                h.chk(f"noche del {NOMBRES_DIA[dia_actual]}: punto de control y parada del sistema", pc["ok"], pc)
                h.chk(f"noche del {NOMBRES_DIA[dia_actual]}: integridad limpia al cierre del día", d.orquestador.integridad() == [],
                      d.orquestador.integridad())
                m.para()
                if dia == "jueves":   # el jueves el estado va firmado: diario nuevo con clave a partir del Orquestador cargado
                    ab = di.abrir(*rutas)
                    if not chk("arranque del jueves: el diario de la semana se reabre", ab["ok"], (ab["codigo"], ab["motivo"])):
                        break
                    re2, rd2 = os.path.join(tmp, "estado_firmado.json"), os.path.join(tmp, "diario_firmado")
                    cf = di.crear(ab["diario"].orquestador, re2, rd2, DIAS["jueves"], clave=CLAVE)   # crear no pisa ficheros
                    if not chk("arranque del jueves: diario nuevo con clave en otra carpeta, a partir del estado cargado", cf["ok"], cf):
                        break
                    rutas, con_clave = (re2, rd2), True
                ab = di.abrir(*rutas, clave=CLAVE if con_clave else None)
                if not chk(f"arranque del {NOMBRES_DIA[dia]}: el diario se abre", ab["ok"], (ab["codigo"], ab["motivo"])):
                    break
                d = ab["diario"]
                m = Maquina(d, [bg, bd], DIAS[dia])                    # reloj nuevo: comprobar_estado y contrastar dentro
                acumula()
                dia_actual = dia
                t_prev = m.instante()
            m.pasar(delta)
            t = m.instante()
            try:
                rg = paso(g, bg, t, t_prev)
                rd_ = paso(d, bd, t, t_prev)
            except Exception as ex:   # noqa: BLE001
                h.chk(f"{nombre}: el paso no lanza", False, f"{type(ex).__name__}: {ex}")
                break
            hubo_o16 = hubo_o16 or con_o16(rg) or con_o16(rd_)
            h.chk(f"{nombre}: mismo resultado en los dos gemelos y el esperado", rg == rd_ and ESPERADO[nombre](rg),
                  (rg, rd_) if rg != rd_ else rg)
            if dia == "miercoles" and nombre == "miercoles_libre":
                cortar(rutas[1])                                       # el corte a medias del miércoles, tras el paso
            ab = di.abrir(*rutas, clave=CLAVE if con_clave else None)  # reinicio: se reabre desde disco
            if not chk(f"{nombre}: tras reiniciar{' (con el corte a medias)' if dia == 'miercoles' and nombre == 'miercoles_libre' else ''}, el diario se abre",
                       ab["ok"], (ab["codigo"], ab["motivo"])):
                break
            d = ab["diario"]
            t_reinicio = m.instante()
            h.chk(f"{nombre}: tras reiniciar, el volcado es el del gemelo en memoria",
                  pe.volcar(d.orquestador, t_reinicio) == pe.volcar(g, t_reinicio))
            t_prev = t
        else:
            # ---- viernes por la noche: punto final, migración de prueba y el diario que queda
            m.pasar(120)
            inst_final = m.instante()
            o = d.orquestador
            h.chk("al terminar la semana las carteras siguen en L1 por el periodo mínimo del rearme",
                  o.nivel("TACTICA") == "L1" and o.nivel("TRADING") == "L1", (o.nivel("TACTICA"), o.nivel("TRADING")))
            h.chk("el kill-switch se activó y se rearmó una vez", o.kill is None and len(o.rearmes) == 1, (o.kill, o.rearmes))
            h.chk("las posiciones quedan como tocan: la primera cerrada por el stop del jueves y la de TRADING por el operador el viernes",
                  o.posiciones["POS-EXP-0001"]["estado"] == "CERRADA" and o.posiciones["POS-EXP-0003"]["estado"] == "CERRADA"
                  and all(p["instrumento"] in ("GBPUSD", "EURJPY") for p in bd.posiciones()),
                  {k: v["estado"] for k, v in o.posiciones.items()})
            h.chk("hubo una reducción parcial el martes", len(o.posiciones["POS-EXP-0001"]["reducciones"]) == 1,
                  o.posiciones["POS-EXP-0001"]["reducciones"])
            h.chk("la operación LIBRE del miércoles quedó declarada", any(mm["vinculo"]["tipo"] == "LIBRE" for mm in o.manuales), o.manuales)
            h.chk("el perdedor del lunes queda COMPARADA y sin propuesta ni orden de entrada",
                  o.expedientes["EXP-0002"]["estado"] == "COMPARADA" and o.expedientes["EXP-0002"].get("propuesta") is None
                  and o.expedientes["EXP-0002"].get("orden_entrada") is None, o.expedientes["EXP-0002"]["estado"])
            # migración de prueba: el estado del viernes, como lo habría guardado V0.45, migrado a este código
            r = mg.migrar(a_010_v045(a_010(pe.volcar(o, inst_final))), inst_final, "migración de prueba de la semana simulada")
            h.chk("la migración de prueba del estado del viernes pasa (MIG-001 a MIG-004)", r["ok"] and "MIG-004" in r.get("motivo", ""), r)
            if r["ok"]:
                car = pe.cargar(r["texto"])
                h.chk("el estado migrado se carga", car["ok"], (car.get("codigo"), car.get("motivo")))
                if car["ok"]:
                    datos = {"EURUSD": {"precio": 1.05, "hora": bd.hora_datos}, "EURJPY": {"precio": 165.0, "hora": bd.hora_datos}}
                    v = vigilar(car["orquestador"], bd, datos, inst_final)
                    h.chk("el estado migrado sigue operando: una vigilancia más, sin incidencias",
                          v["conciliacion_ok"] and all(a.get("ok", True) for a in v["acciones"]), v)
            pc = d.punto(m.instante())   # punto de control final del viernes: el arranque del lunes parte de aquí
            h.chk("punto de control final del viernes", pc["ok"], pc)
            ab = di.abrir(*rutas, clave=CLAVE)
            if chk("el diario firmado se reabre tras el punto final", ab["ok"], (ab["codigo"], ab["motivo"])):
                d = ab["diario"]
                t_final = m.instante()
                h.chk("y el gemelo en memoria es idéntico al final de la semana", pe.volcar(d.orquestador, t_final) == pe.volcar(g, t_final))
                ls, cortada = di._leer(rutas[1], CLAVE)[0], di._leer(rutas[1], CLAVE)[1]
                h.chk("el diario firmado empieza en el PUNTO del viernes y solo tiene esa línea",
                      len(ls) == 1 and ls[0]["tipo"] == "PUNTO" and ls[0]["n"] == 1 and not cortada, (len(ls), ls[0] if ls else None))
                h.chk("integridad limpia al final de la semana", d.orquestador.integridad() == [], d.orquestador.integridad())
            acumula()
        h.chk("los instantes del Reloj durante toda la semana nunca bajan", semana == sorted(semana), semana[:3])
        h.chk("ninguna llamada de la semana devuelve O-16 (el reloj del Orquestador nunca retrocede)", not hubo_o16)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO SEMANA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
