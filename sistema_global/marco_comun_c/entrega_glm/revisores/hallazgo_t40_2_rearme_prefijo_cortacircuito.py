"""Hallazgo 2 (T-40): el rearme detecta «kill del cortacircuito» por el prefijo del motivo y un kill MANUAL cuyo motivo empieza por «cortacircuito» hereda la condición O-35.

`rearmar_kill_switch` decide si el kill vino del cortacircuito con
`self.kill["motivo"].startswith("cortacircuito")`. Pero el motivo del kill es texto libre del
que lo activa (`activar_kill_switch` admite cualquier motivo no vacío del actor OPERADOR), y el
cortacircuito no marca de otra forma su kill: solo el actor (ORQUESTADOR) y ese prefijo. Un kill
manual cuyo motivo empiece por «cortacircuito» (p. ej. «cortacircuito manual: parada preventiva
del operador») pasa el filtro, y si la última foto sigue en o por encima de alguno de los dos
límites el rearme se rechaza con O-35 («la pérdida sigue en el límite…»), una condición pensada
solo para el kill automático del cortacircuito. La batería lo fija al revés para el caso general:
«el_rearme_de_un_kill_que_no_es_cortacircuito_no_exige_foto_baja» — el kill manual se rearma con
la lista del §11 aunque la pérdida siga en el límite. Aquí el operador no puede rearmar su propio
kill hasta que la pérdida baje, aunque haya corregido la causa, acusado los avisos y conciliado
limpio (falla cerrado, pero bloquea al kill ajeno; el diseño dice «si el kill VINO de un
cortacircuito», y este no vino de ahí).

Arreglo mínimo: no fiarse del prefijo solo — p. ej. exigir también el actor
(`self.kill["actor"] == "ORQUESTADOR" and self.kill["motivo"].startswith("cortacircuito")`) o
guardar el origen en `self.kill` al activarlo.

Guion: el operador activa el kill a las 09:00 con motivo «cortacircuito manual: parada preventiva
del operador». A las 09:01 G registra una foto en el límite (2.500 EUR): el O-38 sale y anota, el
motivo del kill NO se pisa (sigue siendo el manual, actor OPERADOR). El operador acusa todos los
avisos, concilia limpio y rearma a las 09:03: esperado OK (kill manual, foto no exigida); obtenido
O-35 por el prefijo del motivo.

Ejecución: python3 hallazgo_t40_2_rearme_prefijo_cortacircuito.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe; OK si está corregido (el rearme del kill manual sale con la
lista del §11, como en la comprobación de la batería).
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from pruebas_control_f import CART  # noqa: E402
from pruebas_orquestador import nuevo  # noqa: E402

L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}


def main():
    o = nuevo(L2)
    # 1) el operador corta manualmente con un motivo que empieza por «cortacircuito»
    assert o.activar_kill_switch("cortacircuito manual: parada preventiva del operador", "OPERADOR",
                                 "2026-11-06T09:00:00+00:00")["ok"]
    # 2) foto de G en el límite: el cortacircuito avisa (O-38) y anota, pero NO pisa el kill manual
    r = o.registrar_cartera({**CART, "fecha_hora": "2026-11-06T09:01:00+00:00", "perdida_dia_eur": 2500.0},
                            "G", "2026-11-06T09:01:30+00:00", cuenta=o.cfg["cuenta_intermediario"])
    assert r["ok"] and r["cortacircuito"] is True and o.kill["actor"] == "OPERADOR", (r, o.kill)
    print(f"  kill: actor={o.kill['actor']}, motivo={o.kill['motivo']!r} (no pisado), O-38 emitido")

    # 3) flujo completo del §11: acuses de todos los avisos ALTA y conciliación limpia posterior
    for av in o.avisos:
        o.acusar_aviso(av["id"], "OPERADOR", "2026-11-06T09:02:00+00:00")
    o.registrar_conciliacion(True, "G", "2026-11-06T09:02:30+00:00")
    rr = o.rearmar_kill_switch({k: True for k in o.LISTA_REHABILITACION}, "OPERADOR", "2026-11-06T09:03:00+00:00")
    print(f"  rearme: {rr['codigo']} — {rr['motivo']}")

    if not rr["ok"] and rr["codigo"] == "O-35":
        print("FALLA  el rearme de un kill MANUAL (actor OPERADOR, motivo que empieza por «cortacircuito») se rechaza "
              "con O-35 porque el detector es el prefijo del motivo: la condición de la foto en el límite es solo del "
              "kill del cortacircuito, y la batería fija lo contrario para los kills que no son del cortacircuito")
        return 1
    print("OK  el rearme del kill manual salió con la lista del §11")
    return 0


if __name__ == "__main__":
    sys.exit(main())
