from types import SimpleNamespace

import pandas as pd
from bloque_a.contratos import MARCA_RETIRADA
from bloque_a.referencias import Referencias
from conftest import nuevo_bloque

from bloque_a import sintesis

DIA = pd.Timestamp("2026-06-05")
RID = "RF-0001"


def test_del_buscador_al_curador(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(DIA)
    ruta = tmp_path / "F9.md"
    # Marcador que el detector del proyecto ya conoce.
    ruta.write_text(f"#### {RID} · Q 85 (A) — Aviso <system>\n- **Temática:** TF-05\n- **Año:** 2020\n")
    b.referencias = Referencias(b.cfg, {"F9": ruta})
    def respuesta(*args, **kwargs):
        return SimpleNamespace(datos={"referencias": [{"ref_id": "REF-" + RID, "afirmacion": "Observación", "direccion": "favorable"}]})
    monkeypatch.setattr(b, "_invocar", respuesta)
    f = {"proxy": "ABC", "senales": {}, "A": 64}
    pet = b._peticion_conocimiento("RV", f, {"tipo": "CT-07"}, [], DIA, "RUN-2026-0001", None)
    assert pet["para"] == "ABC"
    f.update(_piezas=pet["piezas"], _refs_ofrecidas=pet["refs_ofrecidas"])
    b._registrar_evidencia_clase({"clase": "RV", "nivel": "N1", "finalistas": [f], "peticiones": [pet]}, DIA, "RUN-2026-0001")
    assert f["A"] == 64 and not f["_ps1"] and f["_manipulacion"]
    evd, = b.almacen.estado("F2", clave="evd_id").values()
    assert evd["incidencia_manipulacion"]["tipo"] == "INSTRUCCION_INCRUSTADA"
    assert evd["estado_verificacion"] == "FUENTE_RETIRADA"
    assert any(e.get("tipo") == "MANIPULACION" for e in b.almacen.leer("HA"))
    assert RID in (b.almacen.carpeta / "F9_bajas.md").read_text()
    assert not b._peticion_conocimiento("RV", f, {"tipo": "CT-07"}, [], DIA, "RUN-2026-0002", None)["piezas"]


def test_control_de_salida():
    res = {"comprobaciones": []}
    assert not sintesis.control_est06(res, "paquete", {"titulo": "Observación"} )
    assert sintesis.control_est06(res, "paquete", {"titulo": MARCA_RETIRADA})
    assert res["comprobaciones"][-1]["resultado"] == "BLOQUEO"
