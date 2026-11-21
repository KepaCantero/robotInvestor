import pandas as pd
from conftest import nuevo_bloque

from bloque_a import sintesis
from bloque_a.referencias import Referencias


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
    op = {"opp_id": "OPP-2026-0001", "evidencias": [clm["clm_id"]]}
    paquete = {"clases": {"RV": {"opciones": [op]}}}
    assert sintesis.control_raices(paquete, clms, evds)["resultado"] == "OK"
    clm["raices_independientes"] = 21
    assert sintesis.control_raices(paquete, clms, evds)["resultado"] == "BLOQUEO"
