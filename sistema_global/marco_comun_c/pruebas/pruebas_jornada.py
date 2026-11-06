"""Escenario de una jornada con reinicios (V0.44). Dos sistemas gemelos recorren la misma jornada simulada: uno con el
Orquestador en memoria y otro con el diario de operaciones (T-03). Tras cada paso, el del diario se «reinicia» (se reabre desde
disco) y debe ser idéntico al gemelo. La jornada toca casi todo: K, encargo, sobre, D, E, F con su contexto, autorización con
pantalla, G (ejecución, cotización, foto, conciliación), H (vigilancia y cierre por objetivo), reducción parcial, operación LIBRE
declarada a mano, degradación y restablecimiento, kill-switch y rearme, y un punto de control a mitad. Tras algunos pasos el
sistema se «corta» antes de reiniciar (sin el RES de la última operación o con una línea a medias). Datos SIMULADOS.

Sirve también de red al integrar piezas: si una pieza nueva rompe algo entre módulos o algo que el diario no reproduce, aquí se ve.

Uso: python3 pruebas/pruebas_jornada.py
"""
import os
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
from ejecucion_g import BrokerSimulado, cerrar, conciliar, declarar_manual, ejecutar, foto_cartera, kill_switch, reducir  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_extremo import HORA_DATOS, candidatos  # noqa: E402
from pruebas_manual import a_mano, libre  # noqa: E402
from pruebas_orquestador import AHORA, ENTRADA, SALIDA, Arnes, autorizar_op, dim, nuevo  # noqa: E402
from vigilancia import vigilar  # noqa: E402

T = "2026-11-06T09:00:00+00:00"
CFG = {"nivel_autonomia": {"TACTICA": "L2"}}


def instante(m):
    return f"2026-11-06T{9 + m // 60:02d}:{m % 60:02d}:00+00:00"


def lista_rearme():
    return {k: True for k in ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")}


def pasos():
    """Cada paso es (nombre, función(o, b) -> resultado comparable). Se aplica igual a los dos gemelos."""
    def p_candidatos(o, b):
        candidatos(o)
        return sorted(o.expedientes)

    def p_comparar(o, b):
        return o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)

    def p_proponer(o, b):
        foto = foto_cartera(o, b, AHORA)
        return o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, cartera=foto))

    def p_autorizar(o, b):
        return autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", 1, cartera=foto_cartera(o, b, AHORA)), AHORA)

    def p_ejecutar(o, b):
        return ejecutar(o, "EXP-0001", b, AHORA)

    def p_conciliar(o, b):
        return conciliar(o, b, instante(5))

    def p_reducir(o, b):
        return reducir(o, "POS-EXP-0001", b, instante(10), cantidad=o.posiciones["POS-EXP-0001"]["cantidad"] / 2, actor="OPERADOR",
                       motivo="Reduzco a la mitad en la jornada simulada")

    def p_libre(o, b):
        a_mano(b, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")
        return declarar_manual(o, libre(emitido_en=instante(15), ejecutado_en=instante(14)), b, instante(15))

    def p_degradar(o, b):   # G baja la cartera a L1 (por ejemplo, un dato viejo)
        return o.degradar("TACTICA", "dato viejo en la jornada simulada", "G", instante(16))

    def p_restablecer(o, b):   # el operador acusa los avisos y la devuelve a L2
        for a in o.avisos:
            if a["acuse"] is None:
                o.acusar_aviso(a["id"], "OPERADOR", instante(17))
        return o.restablecer_nivel("TACTICA", "OPERADOR", instante(18))

    def p_kill(o, b):
        return kill_switch(o, b, instante(20), "prueba de la jornada")

    def p_rearmar(o, b):
        for a in o.avisos:
            if a["acuse"] is None and a.get("prioridad") == "ALTA":
                o.acusar_aviso(a["id"], "OPERADOR", instante(25))
        conciliar(o, b, instante(25))
        return o.rearmar_kill_switch(lista_rearme(), "OPERADOR", instante(26))

    def p_vigilar_objetivo(o, b):
        b.mover_precio("EURUSD", 1.16, instante(40))
        return vigilar(o, b, {"EURUSD": {"precio": 1.16, "hora": instante(40)}}, instante(40))

    def p_cerrar_operador(o, b):   # tras el kill-switch la cartera queda en L1: H solo prepara el cierre y lo hace el operador
        return cerrar(o, "POS-EXP-0001", b, instante(42), actor="OPERADOR", motivo="Cierro yo lo que H preparó por objetivo")

    def p_conciliar_final(o, b):
        return conciliar(o, b, instante(45))

    return [("candidatos", p_candidatos), ("comparar", p_comparar), ("proponer", p_proponer), ("autorizar", p_autorizar),
            ("ejecutar", p_ejecutar), ("conciliar", p_conciliar), ("reducir", p_reducir), ("libre", p_libre),
            ("degradar", p_degradar), ("restablecer", p_restablecer), ("kill", p_kill),
            ("rearmar", p_rearmar), ("vigilar_objetivo", p_vigilar_objetivo), ("cerrar_operador", p_cerrar_operador),
            ("conciliar_final", p_conciliar_final)]


# lo que cada paso debe dar (revisión de V0.44, hallazgo 2): sin esto, dos fallos iguales pasarían por «mismo resultado»
ESPERADO = {"comparar": lambda r: r["ok"] and r["ganador"] == "EXP-0001", "proponer": lambda r: r["ok"], "autorizar": lambda r: r["ok"],
            "ejecutar": lambda r: r["ok"], "conciliar": lambda r: r["ok"], "reducir": lambda r: r["ok"] and r["restante"] > 0,
            "libre": lambda r: r["ok"], "degradar": lambda r: r["ok"], "restablecer": lambda r: r["ok"], "kill": lambda r: r["ok"],
            "rearmar": lambda r: r["ok"],
            # tras el kill-switch la cartera se queda en L1 (periodo mínimo): H prepara el cierre por objetivo (H-10) y no lo hace
            "vigilar_objetivo": lambda r: [(a["regla"], a.get("condicion"), a["codigo"]) for a in r["acciones"]] == [("H-10", "OBJ-1", "H-10")],
            "cerrar_operador": lambda r: r["ok"], "conciliar_final": lambda r: r["ok"]}
# cómo se corta el sistema antes de reiniciar tras algunos pasos (hallazgo 5): sin el RES de la última operación, o con una línea a medias
CORTES = {"ejecutar": "sin_res", "libre": "linea_a_medias", "rearmar": "sin_res"}


def cortar(rd, como):
    with open(rd, encoding="ascii") as f:
        lineas = f.read().splitlines(keepends=True)
    if como == "sin_res" and len(lineas) > 1 and '"tipo":"RES"' in lineas[-1]:
        lineas = lineas[:-1]
    elif como == "linea_a_medias":
        lineas = lineas + [lineas[-1][:25]]
    with open(rd, "w", encoding="ascii") as f:
        f.write("".join(lineas))


def broker():
    return BrokerSimulado(100000.0, {"EURUSD": 1.10, "GBPUSD": 1.30}, HORA_DATOS)


def main():
    h = Arnes()
    with tempfile.TemporaryDirectory() as tmp:
        re_, rd = os.path.join(tmp, "estado.json"), os.path.join(tmp, "diario")
        g = nuevo(CFG)                                   # gemelo en memoria
        c = di.crear(nuevo(CFG), re_, rd, T)
        assert c["ok"], c
        d = c["diario"]                                  # gemelo con diario
        bg, bd = broker(), broker()
        for i, (nombre, paso) in enumerate(pasos()):
            rg, rdia = paso(g, bg), paso(d, bd)
            h.chk(f"{nombre}: mismo resultado con y sin diario y el esperado", rg == rdia and ESPERADO.get(nombre, lambda r: True)(rg), (rg, rdia))
            if nombre in CORTES:
                cortar(rd, CORTES[nombre])
            a = di.abrir(re_, rd)                         # reinicio
            h.chk(f"{nombre}: tras reiniciar{' (' + CORTES[nombre] + ')' if nombre in CORTES else ''}, el estado es el del gemelo",
                  a["ok"] and pe.volcar(a["diario"].orquestador, T) == pe.volcar(g, T), (a["codigo"], a["motivo"]))
            d = a["diario"]
            if nombre == "conciliar":
                antes = pe.volcar(d.orquestador, T)
                pc = d.punto(instante(6))
                ls = di._leer(rd)[0]
                guardado = pe.cargar_de(re_)
                h.chk("punto_de_control_a_mitad_de_jornada_reduce_el_diario_y_guarda_el_estado", pc["ok"] and len(ls) == 1 and ls[0]["estado"] == pc["huella"]
                      and guardado["ok"] and pe.volcar(guardado["orquestador"], T) == antes, (pc, len(ls)))
        h.chk("tras_el_kill_switch_la_cartera_queda_en_L1", g.nivel("TACTICA") == "L1")
        # lo que la jornada debe haber dejado
        o = d.orquestador
        h.chk("H_preparo_el_cierre_en_L1_y_lo_cerro_el_operador", o.posiciones["POS-EXP-0001"]["estado"] == "CERRADA"
              and all(x["instrumento"] == "GBPUSD" for x in bd.posiciones()), (o.posiciones["POS-EXP-0001"]["estado"], bd.posiciones()))
        h.chk("hubo_una_reduccion_parcial", len(o.posiciones["POS-EXP-0001"]["reducciones"]) == 1)
        h.chk("la_operacion_libre_quedo_declarada", any(m["vinculo"]["tipo"] == "LIBRE" for m in o.manuales))
        h.chk("el_kill_switch_se_activo_y_se_rearmo", o.kill is None and len(o.rearmes) == 1)
        h.chk("integridad_al_final_de_la_jornada", o.integridad() == [], o.integridad())
        ls = di._leer(rd)[0]
        h.chk("el_diario_empieza_en_el_punto_y_solo_tiene_lo_posterior", ls[0]["tipo"] == "PUNTO" and ls[0]["n"] == 1
              and not any(x["tipo"] == "OP" and x["metodo"] in ("detectar", "emitir_encargo", "entregar_sobre", "comparar", "proponer", "autorizar")
                          for x in ls) and sum(x["tipo"] == "OP" for x in ls) > 10, [x.get("metodo") for x in ls][:6])
        h.chk("y_el_gemelo_en_memoria_es_identico", pe.volcar(o, T) == pe.volcar(g, T))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO JORNADA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
