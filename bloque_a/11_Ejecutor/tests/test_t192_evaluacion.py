import math
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from bloque_a.configuracion import cargar_config
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles
from conftest import AS_OF, nuevo_bloque


def contaminar(b):
    tasa_base = b.evaluador.tasa_base
    def tasa_emitida(*args, **kwargs):
        return {**tasa_base(*args, **kwargs), "valor_o_prob": 0.975}

    # La base congelada difiere numéricamente del recálculo; usar la antigua puntuación debe fallar.
    with patch.object(b.evaluador, "tasa_base", side_effect=tasa_emitida):
        b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    vencen = sorted((p for p in b.almacen.estado("F4").values() if p.get("prob_interna") is not None
                     and p["fecha_resolucion"] <= "2026-07-10"), key=lambda p: p["prg_id"])
    assert len(vencen) >= 3
    p1, p2 = vencen[:2]
    id1, id2 = [p["referencia_ingenua"]["calc_id"] for p in (p1, p2)]
    b.almacen.escribir("RC", "AG-13", {"tipo_entrada": "SERVICIO", "calc_id": id1, "as_of": "2026-06-06"})
    datos = b.almacen.estado("RC")[id2]["datos"]
    datos[0]["fecha_dato"] = "2026-06-12"
    b.almacen.escribir("RC", "AG-13", {"tipo_entrada": "SERVICIO", "calc_id": id2, "datos": datos})
    b.fijar_fecha("2026-07-10")
    return vencen


def test_recalcular_referencia_sin_futuro(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    vencen = contaminar(b)
    b.evaluador.ciclo("2026-07-10")
    alm = b.almacen
    f4 = alm.estado("F4")
    calc_dia, = [e["calc_id"] for e in alm.leer("F6") if e.get("tipo_entrada") == "RES" and e["fecha"] == "2026-07-10"]
    datos = alm.estado("RC")[calc_dia]["datos"][0]
    assert len((datos.get("valor") or datos["valores"])["p"]) == len(vencen) - 2
    for p in vencen[:2]:
        pid = p["prg_id"]
        original = f4[pid]
        r = original["resolucion"]
        assert r["comprobacion_fuga"] == "FALLIDA" and r["fuga_tasa_base"] and r["calc_id"] is None
        assert original["referencia_ingenua"] == p["referencia_ingenua"]
        c, = [e for e in alm.leer("F6") if e.get("tipo_entrada") == "CORRECCION_FUGA" and e["prg_id"] == pid]
        rc = alm.estado("RC")[c["referencia_limpia"]["calc_id"]]
        assert rc["as_of"] == c["fecha_corte"] == p["fecha_emision"]
        assert all((d.get("fecha_dato") or "") <= p["fecha_emision"] for d in rc["datos"])
        prob, o = c["referencia_limpia"]["valor_o_prob"], r["resultado_binario"]
        assert c["puntuaciones"]["brier_ref"] == pytest.approx((prob - o)**2)
        assert c["puntuaciones"]["log_ref"] == pytest.approx(-math.log(min(max(prob if o else 1 - prob, 0.01), 0.99)))
        assert c["puntuaciones"]["brier"] == r["puntuaciones"]["brier"]
        corregido, = [x for x in b.evaluador.resueltos("2026-07-10") if x["prg_id"] == pid]
        assert corregido["referencia_ingenua"] == c["referencia_limpia"]
        assert corregido["resolucion"]["puntuaciones"] == c["puntuaciones"]
    b.fijar_fecha("2026-07-17")
    b.evaluador.ciclo("2026-07-17")
    for p in vencen[:2]:
        pid = p["prg_id"]
        assert len([e for e in alm.leer("F6") if e.get("prg_corregido") == pid]) == 1
        cor, = [e for e in alm.leer("HA") if e.get("tipo_entrada") == "COR" and e["entrada_corregida"] == pid]
        assert cor["comunicado_a"] == ["AG-18"] and cor["motivo"]
        inc, = [e for e in alm.leer("HA") if e.get("tipo") == "OTRO" and e.get("objeto") == pid]
        assert inc["severidad"] == "Operativa" and "FALLIDA" in inc["tratamiento"]
    assert all(alm.verificar_integridad().values())


def test_recalculo_pendiente_y_reintento(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    vencen = contaminar(b)
    b.evaluador.resolver("2026-07-10")
    def sin_datos(*args):
        raise DatosNoDisponibles("sin histórico")
    with monkeypatch.context() as m:
        m.setattr(b.evaluador, "tasa_base", sin_datos)
        b.evaluador.corregir_fugas("2026-07-10", None)
    pid = vencen[0]["prg_id"]
    assert not any(e.get("prg_corregido") == pid for e in b.almacen.leer("F6"))
    assert not any(p["prg_id"] == pid for p in b.evaluador.resueltos("2026-07-10"))
    assert any(e.get("tipo") == "HERRAMIENTA" and e.get("objeto") == pid for e in b.almacen.leer("HA"))
    b.evaluador.corregir_fugas("2026-07-10", None)
    assert any(p["prg_id"] == pid for p in b.evaluador.resueltos("2026-07-10"))


def sembrar(b, semanas=13, mejora=0.5, sentido="POSITIVO", rota=False):
    alm = b.almacen
    b.fijar_fecha("2026-01-01")
    alm.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-1", "parametro": "P-11", "efecto_desde": "2026-01-02",
                                "sombra_hasta": "2026-04-02", "estado": "EN_SOMBRA"})
    rng = np.random.default_rng(1)
    fechas = pd.date_range("2026-01-02", periods=semanas, freq="7D").tolist()
    for i, (fecha, entrega, ajuste) in enumerate([(pd.Timestamp("2026-01-01"), "ENTREGADA", "AJU-1"),
            (pd.Timestamp("2026-01-04"), "BLOQUEADA", "AJU-1"), (pd.Timestamp("2026-01-05"), "ENTREGADA", "AJU-2"),
            *((f, "ENTREGADA", "AJU-1") for f in fechas)]):
        b.fijar_fecha(fecha)
        y, ruido = rng.normal(size=3), rng.normal(size=3)
        anterior, nueva = y * (0.5 - mejora) + ruido, y * (0.5 + mejora) + ruido
        rid = f"RUN-{i}"
        pares = {f"OPP-{i}-{k}": [anterior[k], nueva[k]] for k in range(3)}
        alm.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": rid, "entrega": entrega,
                     "sombra": {"RV": {"aju_id": ajuste, "rk_pareado": pares, "cambios": 1}}})
        for k, oid in enumerate(pares):
            pid = f"PRG-{i}-{k}"
            alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": oid, "clase": "RV", "run_id": rid,
                         "fecha_emision": str(fecha.date()), "horizonte": "H1", "sentido": sentido, "estado": "ABIERTO"})
            obs = {} if rota and i == 3 and k == 0 else {"valor_observado": float(y[k]) * (1 if sentido == "POSITIVO" else -1)}
            alm.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                         "resolucion": {**obs, "fecha_dato": str(fecha.date()), "comprobacion_fuga": "SUPERADA"}})
    b.fijar_fecha("2026-04-02")


@pytest.mark.parametrize(("mejora", "sentido", "esperado"), [(0.5, "POSITIVO", "CONFIRMADO"), (-0.5, "POSITIVO", "REVERTIDO"),
                                                            (0.5, "NEGATIVO", "CONFIRMADO")])
def test_cierre_con_comparacion_pareada(tmp_path, universo, mejora, sentido, esperado):
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config())
    sembrar(b, mejora=mejora, sentido=sentido)
    assert b.evaluador.cerrar_sombra("2026-04-01") is None
    cierre = b.evaluador.cerrar_sombra("2026-04-02")
    assert cierre["estado"] == esperado
    assert cierre["n_pares"] == 39 and cierre["n_fechas"] == cierre["dm_hln"]["n"] == 13
    p = cierre["dm_hln"]["p_unilateral"]
    assert p > .9 if mejora > 0 else p < .1
    assert cierre["resultado_sombra"] == {"decision": esperado, "metrica_anterior": cierre["ic_anterior"],
                                          "metrica_nueva": cierre["ic_nueva"], "dm_hln_p": p, "decisiones_top3_cambiadas": 13}
    assert b.evaluador.cerrar_sombra("2026-04-02") is None


@pytest.mark.parametrize(("semanas", "rota", "pares", "estado"), [(9, False, 27, "REVERTIDO"), (13, True, 38, "CONFIRMADO")])
def test_muestra_o_fila_incompleta(tmp_path, universo, semanas, rota, pares, estado):
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config())
    sembrar(b, semanas=semanas, rota=rota)
    c = b.evaluador.cerrar_sombra("2026-04-02")
    assert c["estado"] == estado and c["n_pares"] == pares
    if semanas == 9:
        assert c["dm_hln"] is None and c["resultado_sombra"]["dm_hln_p"] is None


def test_c5_sigue_si_no_se_puede_comparar(tmp_path, universo, monkeypatch):
    from bloque_a import sombra
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-1", "parametro": "P-11", "estado": "EN_SOMBRA",
                                        "efecto_desde": "2026-05-01", "sombra_hasta": AS_OF})
    def falla(*args):
        raise RuntimeError("comparación indisponible")
    monkeypatch.setattr(sombra, "comparar", falla)
    monkeypatch.setattr(b.evaluador, "recalibrar", lambda *args: pytest.fail("recalibración mientras falta la comparación"))
    novedades = []
    monkeypatch.setattr(b.evaluador, "publicar_novedades", lambda *args: novedades.append(True))
    assert b.evaluador.ciclo(AS_OF)["ajuste"] is None and novedades
    assert any(e.get("tipo") == "HERRAMIENTA" and "sombra" in e["detalle"] for e in b.almacen.leer("HA"))
    assert b.evaluador.ajuste_en_sombra(AS_OF)["id"] == "AJU-1"


@pytest.mark.parametrize(("umbral", "motivo"), [(0.10, "DM-HLN"), (0.01, "media ha disminuido")])
def test_p_reversion_independiente_de_holm(tmp_path, universo, umbral, motivo):
    cfg = cargar_config(extra={"evaluacion": {"recalibracion_rk": {"p_reversion": umbral}, "alfa_holm": .10}})
    b = nuevo_bloque(tmp_path, universo, cfg=cfg)
    sembrar(b, mejora=-.45)
    cierre = b.evaluador.cerrar_sombra("2026-04-02")
    # Con una sola métrica, un IC inferior también implica reversión. La causa registrada distingue ambas reglas.
    assert .01 < cierre["resultado_sombra"]["dm_hln_p"] < .10
    assert motivo in cierre["motivo_cierre"] and cierre["estado"] == "REVERTIDO"


def test_recupera_el_aviso_si_la_escritura_de_ha_falla(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    contaminar(b)
    b.evaluador.resolver("2026-07-10")
    escribir = b.almacen.escribir
    def fallo_ha(archivo, autor, entrada):
        if archivo == "HA" and entrada.get("tipo_entrada") == "COR":
            raise OSError("registro temporalmente indisponible")
        return escribir(archivo, autor, entrada)
    with monkeypatch.context() as m:
        m.setattr(b.almacen, "escribir", fallo_ha)
        with pytest.raises(OSError):
            b.evaluador.corregir_fugas("2026-07-10", None)
    for _ in range(2):
        b.evaluador.corregir_fugas("2026-07-10", None)
    correcciones = [e["id"] for e in b.almacen.leer("F6") if e.get("prg_corregido")]
    avisos = [e["correccion_f6"] for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "COR"]
    assert len(set(correcciones)) == 2 and sorted(correcciones) == sorted(avisos)


@pytest.mark.parametrize(("publicaciones", "estado"), [
    ("2026-06-19,90\n2026-06-15,110", "RESUELTO"),
    ("2026-06-15,110\n2026-06-15,90", "NO_RESOLUBLE"),
    ("2026-06-15,inválido\n2026-06-19,110", "NO_RESOLUBLE"),
])
def test_resolver_con_ediciones_visibles(tmp_path, universo, publicaciones, estado):
    from bloque_a.herramientas.ht01_datos import ProveedorCSV
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque

    texto = "fecha,fecha_publicacion,valor\n2026-06-05,2026-06-05,100\n"
    (tmp_path / "MACRO.csv").write_text(texto + "".join(f"2026-06-12,{p}\n" for p in publicaciones.splitlines()))
    b = Bloque(cargar_config(), ProveedorCSV(tmp_path), universo, MockClient(), tmp_path / "estado", tmp_path / "ent")
    b.fijar_fecha("2026-06-05")
    ref = b.evaluador.tasa_base("MACRO", None, "DIV", 5, True, "2026-06-05")
    pid = b.almacen.nuevo_id("PRG")
    b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "estado": "ABIERTO", "prg_id": pid,
        "fecha_emision": "2026-06-05", "fecha_resolucion": "2026-06-12", "nivel_referencia": {"fecha": "2026-06-05", "valor": 100},
        "prob_interna": .7, "clase": "DIV", "horizonte": "H1", "sentido": "POSITIVO", "tipo_pronostico": "DIRECCIONAL",
        "variable": {"serie_ht01": "MACRO"}, "referencia_ingenua": ref})
    b.fijar_fecha("2026-06-12")
    assert b.evaluador.resolver("2026-06-12") == []
    b.fijar_fecha("2026-06-29")
    p, = b.evaluador.resolver("2026-06-29")
    assert p["estado"] == estado
    if estado == "RESUELTO":
        assert p["resolucion"]["valor_observado"] == pytest.approx(.1)
        assert p["resolucion"]["resultado_binario"] == 1
        admitido, = b.evaluador.resueltos("2026-06-29")
        assert admitido["resolucion"]["puntuaciones"]["brier"] == pytest.approx(.09)


@pytest.mark.parametrize("referencia", [None, "INDICE", "CESTA"])
def test_tasa_historica_solo_con_publicaciones_conocidas(tmp_path, universo, referencia):
    from bloque_a.herramientas.ht01_datos import ProveedorCSV
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque

    fechas = pd.bdate_range(end="2026-06-05", periods=8)
    for simbolo in ("MACRO", "INDICE"):
        filas = ["fecha,valor,fecha_publicacion"]
        for i, fecha in enumerate(fechas):
            publicacion = "2026-06-18" if i == 7 else str(fecha.date())
            valor = (80 if i == 7 else 100 + i) if simbolo == "MACRO" else 100
            filas.append(f"{fecha.date()},{valor},{publicacion}")
        (tmp_path / f"{simbolo}.csv").write_text("\n".join(filas))
    # La cesta de DIV contiene solo el índice. El proxy es una serie externa.
    univ = universo.iloc[:1].copy()
    univ["simbolo"], univ["clase"] = "INDICE", "DIV"
    b = Bloque(cargar_config(), ProveedorCSV(tmp_path), univ, MockClient(), tmp_path / "estado", tmp_path / "ent")
    b.fijar_fecha("2026-06-19")
    tasa = b.evaluador.tasa_base("MACRO", referencia, "DIV", 1, True, "2026-06-05")
    assert tasa["n_ventanas"] == 6
    assert tasa["valor_o_prob"] == .95  # seis avances en seis ventanas, recorte por defecto
    assert {p["as_of"] for p in b.proveedor.registro_peticiones if p["simbolo"] in ("INDICE", "MACRO")
            and p["inicio"] is not None} == {"2026-06-05"}
