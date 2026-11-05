"""Pruebas del informe del Contradictor CT-G-03 (reglas C-01 a C-10). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_contradictor.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from validar_contradictor import hash_contenido, validar_informe  # noqa: E402
from generar_casos import validos as sobres_validos  # noqa: E402

AHORA = "2026-11-06T09:00:00+00:00"


def sobre_base():
    s = copy.deepcopy(sobres_validos()["valido_div_n3.json"])
    s["data_refs"] = ["K-20261105-001", "SRC-EURUSD", "EVID-0001"]
    return s


AUTORIA = {"modelo": "modelo-contradictor-1", "proveedor": "proveedor-b", "diversidad": "OTRO_PROVEEDOR"}
ESC = {"id": "EF-1", "descripcion": "El par cierra por debajo del soporte y la tesis queda invalidada",
       "disparador": {"metrica": "precio_cierre", "operador": "<", "umbral": 1.05, "unidad": "USD"}, "consecuencia": "INVALIDA_TESIS",
       "evid_refs": ["SRC-EURUSD"]}


def informe(sobre, n=1, veredicto="SIN_OBJECIONES_RELEVANTES", objeciones=None, no_rev=(), escenarios=None, autoria=None):
    sec = sorted(sobre["payload"])
    no = [{"seccion": x, "motivo": "no se pudo revisar"} for x in no_rev]
    return {
        "event_id": f"EV-CTR-{n:04d}", "correlation_id": sobre["correlation_id"], "expediente_id": sobre["expediente_id"],
        "producer": "CONTRADICTOR", "consumer": "ORQUESTADOR", "tipo_mensaje": "CT-G-03", "version_esquema": "0.2.0",
        "emitido_en": "2026-11-05T20:00:00+00:00", "valid_until": "2026-11-08T12:00:00+00:00",
        "data_refs": [sobre["event_id"]],
        "payload": {
            "sobre_ref": {"event_id": sobre["event_id"], "hash": hash_contenido(sobre)},
            "nivel_analisis": sobre["payload"]["identificacion"]["nivel_analisis"],
            "independencia": {"vio_conclusion": False, "vio_confianza": False, "contexto_compartido_con_c": False},
            "objeciones": objeciones or [], "veredicto": veredicto,
            "autoria": dict(autoria or AUTORIA), "escenarios_fallo": copy.deepcopy(escenarios if escenarios is not None else [ESC]),
            "cobertura": {"revisadas": [x for x in sec if x not in no_rev], "no_revisadas": no},
        },
    }


def obj(i, gravedad="MENOR", refs=(), tipo="DATO", esc=None):
    """Una objeción; las MAYOR y CRITICA apuntan por defecto al escenario de fallo EF-1 (C-13)."""
    esc = list(esc) if esc is not None else ([] if gravedad == "MENOR" else ["EF-1"])
    return {"id": f"OB-{i}", "tipo": tipo, "gravedad": gravedad, "texto": "La cifra no sostiene la tesis", "evid_refs": list(refs), "escenarios": esc}


def main():
    S = sobre_base()
    ctx = {"ahora": AHORA, "sobre": S}
    ok = True
    n = 0

    def caso(nombre, inf, esperada, c=None):
        nonlocal ok, n
        n += 1
        reglas = sorted({x["regla"] for x in validar_informe(inf, c or ctx)})
        bien = reglas == esperada
        ok &= bien
        print(("OK   " if bien else "FALLA"), nombre, "" if bien else f"esperado={esperada} obtenido={reglas}")

    def mut(fn, **kw):
        i = informe(S, **kw)
        fn(i)
        return i

    P = lambda i: i["payload"]  # noqa: E731
    caso("valido_sin_objeciones", informe(S), [])
    caso("valido_objecion_menor", informe(S, objeciones=[obj(1)]), [])
    caso("valido_mayor_con_evidencia", informe(S, "1", objeciones=[obj(1, "MAYOR", ["EVID-0001"])]) if False else informe(S, veredicto="OBJECION_MAYOR", objeciones=[obj(1, "MAYOR", ["EVID-0001"])]), [])
    caso("valido_critica_con_evidencia", informe(S, veredicto="OBJECION_CRITICA", objeciones=[obj(1, "CRITICA", ["SRC-EURUSD"], "LOGICA")]), [])
    caso("valido_con_parte_no_revisada_y_mayor", informe(S, veredicto="OBJECION_MAYOR", objeciones=[obj(1, "MAYOR", ["EVID-0001"])], no_rev=["capa3"]), [])
    caso("inv_C01_no_objeto", [], ["C-01"])
    caso("inv_C01_producer", mut(lambda i: i.update(producer="C-DIV")), ["C-01"])
    caso("inv_C01_version", mut(lambda i: i.update(version_esquema="9.9.9")), ["C-01"])
    caso("inv_C01_campo_extra", mut(lambda i: i.update(extra=1)), ["C-01"])
    caso("inv_C01_gravedad_invalida", informe(S, objeciones=[{**obj(1), "gravedad": "ALTA"}]), ["C-01"])
    caso("inv_C01_texto_vacio", informe(S, objeciones=[{**obj(1), "texto": "  "}]), ["C-01"])
    caso("inv_C01_nan", mut(lambda i: i["payload"].update(x=float("nan"))), ["C-01"])
    caso("inv_C01_contexto_sin_sobre", informe(S), ["C-01"], c={"ahora": AHORA})
    caso("inv_C02_hash", mut(lambda i: P(i)["sobre_ref"].update(hash="0" * 64)), ["C-02"])
    caso("inv_C02_sobre_distinto", mut(lambda i: P(i)["sobre_ref"].update(event_id="EV-OTRO")), ["C-02"])
    caso("inv_C02_expediente", mut(lambda i: i.update(expediente_id="EXP-9999")), ["C-02"])
    for k in ("vio_conclusion", "vio_confianza", "contexto_compartido_con_c"):
        caso(f"inv_C03_{k}", mut(lambda i, k=k: P(i)["independencia"].update({k: True})), ["C-03"])
    caso("inv_C04_ids_repetidos", informe(S, objeciones=[obj(1), obj(1)]), ["C-04"])
    caso("inv_C04_event_id_del_sobre", mut(lambda i: i.update(event_id=S["event_id"])), ["C-04"])
    caso("valido_texto_multilinea", informe(S, objeciones=[{**obj(1), "texto": "linea1\nlinea2"}]), [])
    caso("inv_C05_mayor_sin_evidencia", informe(S, veredicto="OBJECION_MAYOR", objeciones=[obj(1, "MAYOR")]), ["C-05"])
    caso("inv_C05_evidencia_ajena", informe(S, veredicto="OBJECION_CRITICA", objeciones=[obj(1, "CRITICA", ["EVID-9999"])]), ["C-05"])
    caso("inv_C06_veredicto_blando", informe(S, veredicto="SIN_OBJECIONES_RELEVANTES", objeciones=[obj(1, "CRITICA", ["EVID-0001"])]), ["C-06"])
    caso("inv_C06_veredicto_duro", informe(S, veredicto="OBJECION_CRITICA", objeciones=[obj(1)]), ["C-06"])
    caso("inv_C07_sin_objeciones_con_parte_sin_revisar", informe(S, veredicto="OBJECION_MAYOR", no_rev=["capa3"]), ["C-06", "C-07"])
    caso("inv_C08_nivel", mut(lambda i: P(i).update(nivel_analisis="N2")), ["C-08"])
    caso("inv_C09_antes_del_sobre", mut(lambda i: i.update(emitido_en="2026-11-05T10:00:00+00:00")), ["C-09"])
    caso("inv_C09_futuro", mut(lambda i: i.update(emitido_en="2026-11-07T10:00:00+00:00", valid_until="2026-11-08T12:00:00+00:00")), ["C-09"])
    caso("inv_C09_vence_despues_del_sobre", mut(lambda i: i.update(valid_until="2026-11-20T00:00:00+00:00")), ["C-09"])
    caso("inv_C09_ya_vencido", mut(lambda i: i.update(valid_until="2026-11-05T21:00:00+00:00")), ["C-09"])
    caso("inv_C10_no_cubre_todo", mut(lambda i: P(i)["cobertura"].update(revisadas=["identificacion"])), ["C-10"])
    caso("inv_C10_parte_inexistente", mut(lambda i: P(i)["cobertura"]["revisadas"].append("inventada")), ["C-10"])
    caso("inv_C10_parte_en_ambas", mut(lambda i: P(i)["cobertura"]["no_revisadas"].append({"seccion": "tesis", "motivo": "x"})), ["C-07", "C-10"])
    caso("inv_C10_no_revisada_y_sin_objeciones_ok", informe(S, no_rev=["capa3"]), ["C-07", "C-10"])
    prof = []
    for _ in range(100000):
        prof = [prof]
    caso("anidamiento_extremo_no_lanza", mut(lambda i: P(i).update(x=prof)), ["C-01"])
    print(f"\n{n} comprobaciones")
    print("RESULTADO CT-G-03:", "TODAS LAS PRUEBAS PASAN" if ok else "HAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
