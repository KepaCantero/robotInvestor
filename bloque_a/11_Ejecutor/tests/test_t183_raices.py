import pandas as pd
from bloque_a.referencias import Referencias
from conftest import nuevo_bloque

from bloque_a import sintesis


def test_un_original_y_veinte_derivadas(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    dia = pd.Timestamp("2026-06-05")
    b.fijar_fecha(dia)
    fichas, piezas = [], []
    for n in range(21):
        rid = f"RF-{n:04d}"
        ficha = f"#### {rid} · Q 75 (B) — Medio {n}\n- **Año:** 2020\n"
        if n:
            ficha += "- **Fuente original:** REF-RF-0000\n"
        fichas.append(ficha)
        piezas.append({"fuente": "REF-" + rid, "extracto": f"Versión {n}", "direccion": "favorable", "afirmacion": "Resultado"})
    ruta = tmp_path / "f9.md"
    ruta.write_text("\n".join(fichas))
    b.referencias = Referencias(b.cfg, {"F9": ruta})
    f = {"_piezas": piezas[::-1], "_refs_ofrecidas": [p["fuente"] for p in piezas], "proxy": "ABC"}
    b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, dia, "RUN-2026-0001")
    evds = b.almacen.estado("F2", clave="evd_id")
    clms = b.almacen.estado("F2", clave="clm_id")
    clm, = clms.values()
    assert not f["_ps1"] and clm["raices_independientes"] == 1
    assert len(f["_evidencias_ps1"]) == 1
    raiz, = (e for e in evds.values() if e["grado_independencia"] == "RAIZ")
    assert sum(e.get("raiz_evd_id") == raiz["evd_id"] for e in evds.values()) == 20
    op = {"puertas": {"PS1": False}, "opp_id": "OPP-2026-0001", "evidencias": [clm["clm_id"]]}
    paquete = {"clases": {"RV": {"opciones": [op]}}}
    assert sintesis.control_raices(paquete, clms, evds, b._ps1)["resultado"] == "OK"
    clm["raices_independientes"] = 21
    assert sintesis.control_raices(paquete, clms, evds, b._ps1)["resultado"] == "BLOQUEO"


def test_ps1_por_opcion_y_por_afirmacion_y_origen(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    dia = b.fijar_fecha("2026-06-05")
    ruta = tmp_path / "noticias.md"
    ruta.write_text("#### RF-0001 · Q 78 (B) — Fuente A\n- **Año:** 2020\n\n#### RF-0002 · Q 75 (B) — Fuente B\n- **Año:** 2020\n")
    b.referencias = Referencias(b.cfg, {"F9": ruta})
    f = {"proxy": "ABC", "_refs_ofrecidas": ["REF-RF-0001", "REF-RF-0002"], "_piezas": [
        {"fuente": "REF-RF-0001", "afirmacion": "Tipos de interés", "direccion": "favorable"},
        {"fuente": "REF-RF-0002", "afirmacion": "Ventas", "direccion": "favorable"}]}
    def ingresar():
        b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, dia, "RUN-1")
    ingresar()
    assert f["_ps1"] and len(f["_raices"]) == 2
    assert not any(cl["ps1_cumple"] for cl in b.almacen.estado("F2", clave="clm_id").values())
    f["_piezas"] = [{"fuente": s, "afirmacion": "Precio", "direccion": "favorable"} for s in ("HT-01:ABC", "CALC-0001")]
    # El lote que llega a este paso ya se ha contrastado en la ingesta.
    with b.almacen._transaccion():
        b._guardar_lote_evidencia([f], {}, "RV", dia, "RUN-1")
    assert list(f["_raices"]) == ["HT-01:ABC"]
    clm = next(cl for cl in b.almacen.estado("F2", clave="clm_id").values() if cl["afirmacion"] == "Precio")
    assert clm["raices_independientes"] == 1 and clm["ps1_cumple"]
    evds = b.almacen.estado("F2", clave="evd_id")
    for estado in ("FUENTE_RETIRADA", "CUARENTENA"):
        for eid in clm["evidencias_ps1"]:
            evds[eid]["estado_verificacion"] = estado
        assert not sintesis.raices_de_clm(clm, evds)
    for eid in clm["evidencias_ps1"]:
        evds[eid].update(estado_verificacion="VERIFICADA", direccion="CONTRARIA")
    assert not sintesis.raices_de_clm(clm, evds)


def test_tres_saltos_sin_ficha_ciclo_y_original_en_otra_clm(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    dia = b.fijar_fecha("2026-06-05")
    ruta = tmp_path / "f9.md"
    origenes = [None, "RF-0000", "REF-RF-0001", "RF-0004", "RF-0003", "RF-9999"]
    ruta.write_text("\n".join(f"#### RF-{n:04d} · Q 90 (A) — Pieza\n- **Año:** 2020\n- **Tipología:** primaria\n" +
                              (f"- **Fuente original:** {orig}\n" if orig else "") for n, orig in enumerate(origenes)))
    b.referencias = Referencias(b.cfg, {"F9": ruta})
    def ingesta(ids):
        f = {"proxy": "ABC", "_refs_ofrecidas": [f"REF-RF-{i:04d}" for i in ids],
             "_piezas": [{"fuente": f"REF-RF-{i:04d}", "afirmacion": f"Resultado {i}", "direccion": "favorable"} for i in ids]}
        b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, dia, "RUN-1")
        return f, {e["ref_id"]: e for e in b.almacen.estado("F2", clave="evd_id").values()}
    f, evds = ingesta([1, 2, 3, 4, 5])
    assert not f["_ps1"] and all(e["raiz_evd_id"] == "no identificada" and e["motivo_raiz"] for e in evds.values())
    f, evds = ingesta([0])
    assert f["_ps1"]
    for i in (1, 2):
        assert evds[f"REF-RF-{i:04d}"]["raiz_evd_id"] == evds["REF-RF-0000"]["evd_id"]
    assert all(evds[f"REF-RF-{i:04d}"]["raiz_evd_id"] == "no identificada" for i in (3, 4, 5))


def test_similitud_sin_metadatos_y_fuente_distinta(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    dia = b.fijar_fecha("2026-06-05")
    ruta = tmp_path / "f9.md"
    ruta.write_text("\n".join(f"#### RF-{n:04d} · Q 75 (B) — Pieza {n}\n- **Año:** {2010 if n == 0 else 2020}\n" for n in range(22)))
    b.referencias = Referencias(b.cfg, {"F9": ruta})
    base = "El organismo X prevé que el PIB crezca un 3 % en 2026 según su informe trimestral"
    piezas = [{"fuente": f"REF-RF-{n:04d}", "extracto": base + (f" medio {n}" if n else ""),
               "direccion": "favorable", "afirmacion": "Resultado"} for n in reversed(range(21))]
    def ingesta(piezas):
        f = {"_piezas": piezas, "_refs_ofrecidas": [p["fuente"] for p in piezas], "proxy": "ABC"}
        b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, dia, "RUN-1")
        return f
    replica = ingesta(piezas)
    assert not replica["_ps1"] and len(replica["_raices"]) == 1
    control = ingesta([*piezas, {**piezas[0], "fuente": "REF-RF-0021", "extracto": "Estudio independiente del crecimiento económico nacional"}])
    assert control["_ps1"] and set(control["_raices"]) == {"REF-RF-0000", "REF-RF-0021"}


def test_g3_compara_paquete_historicos_y_fecha(tmp_path, universo, monkeypatch):
    from copy import deepcopy
    b = nuevo_bloque(tmp_path, universo)
    original = sintesis.ht09_validar
    capturas = []
    def guardar(bl, paquete, extras, visual):
        capturas.append((deepcopy(paquete), extras))
        return original(bl, paquete, extras, visual)
    monkeypatch.setattr(sintesis, "ht09_validar", guardar)
    b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
    paquete, extras = capturas[0]
    def g3(paquete):
        res = original(b, paquete, extras, None)
        return next(c["resultado"] for c in res["comprobaciones"] if c["id"] == "G3-DAT-09")
    assert g3(paquete) == "OK"
    alterado = deepcopy(paquete)
    op = next(op for d in alterado["clases"].values() for op in d["opciones"])
    op["puertas"]["PS1"] = not op["puertas"]["PS1"]
    assert g3(alterado) == "BLOQUEO"
    del op["puertas"]["PS1"]
    assert g3(alterado) == "BLOQUEO"
    hist = {"opp_id": "OPP-1", "puertas": {"PS1": False}, "evidencias": ["CLM-1"]}
    parcial = {"clases": {"RV": {"opciones": [hist]}}}
    assert sintesis.control_raices(parcial, {}, {}, b._ps1)["resultado"] == "BLOQUEO"
    assert sintesis.control_raices(parcial, {"CLM-1": {}}, {}, b._ps1)["resultado"] == "ADVERTENCIA"
    b.fijar_fecha("2026-06-06")
    cid = op["evidencias"][0]
    clm = b.almacen.estado("F2", clave="clm_id")[cid]
    b.almacen.escribir("F2", "AG-12", {**clm, "raices_independientes": 123})
    assert g3(paquete) == "OK"


def test_baja_recalcula_afirmaciones_y_entrega_del_ciclo_siguiente(tmp_path, universo):
    from bloque_a.mantenimiento_fuentes import avisar_curador
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo("2026-06-05")
    clms = b.almacen.estado("F2", clave="clm_id")
    evds = b.almacen.estado("F2", clave="evd_id")
    for opciones in r["paquete"]["clases"].values():
        for op in opciones["opciones"]:
            ids = set(eid for cid in op["evidencias"] for eid in clms[cid]["evidencias_ps1"])
            for ref in sorted({evds[eid]["ref_id"] for eid in ids if evds[eid]["ref_id"].startswith("REF-")}):
                if b._ps1(sintesis.raices_de_evidencias(evds[e] for e in ids if evds[e]["ref_id"] != ref)):
                    break
            else:
                continue
            break
        else:
            continue
        break
    else:
        raise AssertionError("El paquete de prueba requiere una opción con una REF y respaldo superviviente")
    b.fijar_fecha("2026-06-06")
    baja = ("F7", ref, "2026-06-06")
    b.referencias.bajas["F7"].append((ref.removeprefix("REF-"), baja[2]))
    avisar_curador(b.almacen, b.mensajeria, baja[2], r["run_id"], {baja}, {baja: "Revisión documental"}, b.cfg)
    nuevas = b.almacen.estado("F2", clave="clm_id")
    evds = b.almacen.estado("F2", clave="evd_id")
    afectadas = [cid for cid in op["evidencias"] if any(evds[e]["ref_id"] == ref for e in clms[cid]["evidencias_ps1"])]
    assert afectadas
    for cid in afectadas:
        raices = sintesis.raices_de_clm(nuevas[cid], evds)
        assert nuevas[cid]["raices_independientes"] == len(raices)
        assert nuevas[cid]["ps1_cumple"] == b._ps1(raices)
    segundo = b.ciclo("2026-06-12")
    assert b.almacen.estado("F5")[segundo["run_id"]]["entrega"] == "ENTREGADA"
    f6 = [c for e in b.almacen.leer("HA") if e.get("run_id") == segundo["run_id"] and e.get("fase") == "F6"
          for c in e.get("comprobaciones", []) if c.get("id") == "G3-DAT-09"]
    assert f6 and all(c["resultado"] == "OK" for c in f6)
