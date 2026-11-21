"""PB-24 y PB-25: decisiones del custodio y propagación en los almacenes reales."""
import pytest
from bloque_a.mantenimiento_fuentes import (
    bajas_registradas,
    publicar,
    revisar_bajas,
    tratar,
)
from conftest import nuevo_bloque

RID = "ANA-DOC-0001"
FICHA = f"#### {RID} · Q 90 (A) — Título\n- **Calidad Q:** 90 (A)\n- **URL:** https://example.org/doc\n"
DIA = "2026-06-05"


def barrido(**extra):
    fila = {"id": RID, "estado": "ROTO", "accion": "BORRAR", "confirmado": True, "codigo_http": 404,
            "fecha_verificacion": DIA, **extra}
    return {"fecha": DIA, "resumen": {"incidencia_red": False}, "resultados": [fila]}


def test_baja_con_registro_y_propagacion(tmp_path, universo, monkeypatch):
    monkeypatch.setattr("bloque_a.mantenimiento_fuentes._sin_copia", lambda r: True)
    bloque = nuevo_bloque(tmp_path, universo)
    ruta = tmp_path / "F7.md"
    ruta.write_text(FICHA)
    bloque.referencias.rutas = {"F7": ruta}
    bloque.referencias.bajas.clear()
    nuevo = tratar("F7", FICHA, barrido(), {})
    publicar(ruta, FICHA, nuevo)
    assert list(bajas_registradas(ruta.read_text().splitlines())) == [(RID, DIA)]
    assert "####" not in nuevo
    alm = bloque.almacen
    bloque.fijar_fecha("2026-06-04")
    alm.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": "EVD-1", "ref_id": "REF-" + RID})
    alm.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": "CLM-1", "evidencias": ["EVD-1"]})
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-1", "estado": "VIGENTE", "evidencias": ["CLM-1"], "ps1": True})
    alm.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": "EVD-2", "ref_id": "REF-ANA-DOC-0002",
                 "direccion": "FAVORABLE", "grado_independencia": "RAIZ", "nivel_fuente": "A", "tipo_fuente": "PRIMARIA"})
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-2", "estado": "VIGENTE", "evidencias": ["CLM-1", "EVD-2"],
                 "evidencias_ps1": ["EVD-1", "EVD-2"], "ps1": True})
    revisar_bajas(bloque, "2026-06-04", "RUN-1")
    assert not alm.estado("F2", clave="baja_id")
    for dia in (DIA, "2026-07-01", "2026-07-01"):
        bloque.fijar_fecha(dia)
        revisar_bajas(bloque, dia, "RUN-2")
    assert alm.estado("F2", clave="evd_id")["EVD-1"]["estado_verificacion"] == "FUENTE_RETIRADA"
    assert alm.estado("F3")["OPP-1"]["ps1"] is False
    assert alm.estado("F3")["OPP-2"]["revision_bajas"]["conclusion"] == "MANTIENE_RESPALDO"
    alertas = [x["mensaje"] for x in alm.leer("F2") if "mensaje" in x]
    assert [x["contrato"] for x in alertas] == ["CT-11"]
    paquetes = [x["mensaje"] for x in alm.leer("HA") if x.get("mes_bajas")]
    assert [(x["contrato"], x["mes"], x["bajas"]) for x in paquetes] == [("CT-21", "2026-06", ["REF-" + RID])]


def test_revision_cambio_y_retractacion():
    informe = barrido(estado="CONTENIDO_CAMBIADO", accion="DEGRADAR", hash="nueva", huella="simhash", codigo_http=200)
    rev = {"accion": "DEGRADAR", "hash": "nueva", "puntos": [20, 10, 15, 5, 8, 7, 10], "motivo": "Método modificado"}
    texto = tratar("F8", FICHA, informe, {RID: rev})
    assert "Q 75 (B)" in texto and "Calidad Q:** 75 (B)" in texto and rev["motivo"] in texto
    with pytest.raises(ValueError):
        tratar("F8", FICHA, informe, {RID: {**rev, "hash": "anterior"}})
    informe = barrido(retractacion=["retracted"], hash="editor", codigo_http=200)
    assert "####" in tratar("F8", FICHA, informe, {})
    texto = tratar("F8", FICHA, informe, {RID: {"accion": "RETRACTADA", "hash": "editor", "motivo": "Aviso del editor"}})
    assert "Aviso del editor" in texto and list(bajas_registradas(texto.splitlines())) == [(RID, DIA)]


@pytest.mark.parametrize("fila", [{"confirmado": False}, {"codigo_http": None}, {"accion": "REPARAR"},
                                  {"copia_archivada": {"url": "https://example.org/archivo"}}])
def test_conserva_ficha(fila):
    assert "####" in tratar("F7", FICHA, barrido(**fila), {})


def test_concurrente_no_pisa(tmp_path):
    ruta = tmp_path / "F7.md"
    ruta.write_text("edición de otro custodio")
    with pytest.raises(ValueError):
        publicar(ruta, FICHA, "otra versión")
    assert ruta.read_text() == "edición de otro custodio"


def test_reparar_exige_copia_original(monkeypatch):
    from bloque_a.herramientas import ht02
    url = "https://web.archive.org/web/20260601/https://example.org/doc"
    informe = barrido(estado="CONTENIDO_CAMBIADO", accion="DEGRADAR", hash="modificado", copia_archivada={"url": url})
    rev = {RID: {"accion": "REPARAR", "hash": "modificado", "motivo": "Versión original archivada", "url": url}}
    ficha = FICHA + "- **Hash de contenido:** original\n"
    monkeypatch.setattr(ht02, "comprobar_url", lambda *a: {"hash": "incorrecto"})
    with pytest.raises(ValueError):
        tratar("F8", ficha, informe, rev)
    monkeypatch.setattr(ht02, "comprobar_url", lambda *a: {"hash": "original", "huella": "original"})
    reparada = tratar("F8", ficha, informe, rev)
    assert f"URL:** {url}" in reparada and "Estado del enlace:** OK" in reparada


def test_caida_archivo_y_ausencia_no_equivalen(monkeypatch):
    from bloque_a.herramientas import ht02
    from bloque_a.mantenimiento_fuentes import _sin_copia
    fila = {"url": "https://example.org/doc"}
    for codigo, cuerpo, esperado in [(503, b"", False), (200, b"{}", False), (200, b'{"archived_snapshots":{}}', True)]:
        monkeypatch.setattr(ht02.modulo, "_con_reintentos", lambda *a, codigo=codigo, cuerpo=cuerpo: ({"codigo": codigo, "cuerpo": cuerpo}, 1))
        assert _sin_copia(fila) is esperado


def test_cli_solo_informe_y_aplicar(tmp_path, monkeypatch):
    import json

    from bloque_a.herramientas import ht02
    from bloque_a.referencias import ARCHIVOS_REF

    from bloque_a import cli
    prefijo = ARCHIVOS_REF["F7"]
    ruta = tmp_path / f"{prefijo} - V1.0.md"
    ruta.write_text(FICHA)
    for nombre in list(ARCHIVOS_REF.values())[1:]:
        (tmp_path / f"{nombre} - V1.0.md").write_text("")
    monkeypatch.setattr(cli, "ruta", lambda *a: tmp_path)
    monkeypatch.setattr("bloque_a.mantenimiento_fuentes._sin_copia", lambda r: True)
    monkeypatch.setattr(ht02.modulo, "verificar_archivo", lambda lineas, *a: barrido(url="https://example.org/doc")["resultados"] if lineas else [])
    args = ["--salida", str(tmp_path), "--estado", str(tmp_path / "estado"), "--as-of", DIA, "verificar-enlaces"]
    assert cli.main(args) == 0 and ruta.read_text() == FICHA
    assert cli.main([*args, "--aplicar"]) == 0
    assert list(bajas_registradas(ruta.read_text().splitlines())) == [(RID, DIA)]
    assert json.loads((tmp_path / "ht02_F7.json").read_text())["fecha"] == DIA


def test_retractacion_editor_f8_hasta_f2(tmp_path, monkeypatch):
    import json

    from bloque_a.almacen import Almacen
    from bloque_a.herramientas import ht02
    from bloque_a.referencias import ARCHIVOS_REF

    from bloque_a import cli

    ref = "MOT-DOC-0002"
    for archivo, nombre in ARCHIVOS_REF.items():
        ruta = tmp_path / f"{nombre} - V1.0.md"
        ruta.write_text(FICHA.replace(RID, ref) if archivo == "F8" else "")
    cuerpo = b"<html>This article has been retracted by its publisher.</html>"
    def emisor(url, metodo, cfg):
        return {"codigo": 200, "url_final": url, "redirecciones": [], "content_type": "text/html",
                "error": None, "cuerpo": cuerpo}, 1
    monkeypatch.setattr(ht02.modulo, "_con_reintentos", emisor)
    monkeypatch.setattr(cli, "ruta", lambda *a: tmp_path)
    estado = tmp_path / "estado"
    almacen = Almacen(estado)
    almacen.reloj.fijar(DIA)
    almacen.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": "EVD-2", "ref_id": "REF-" + ref})
    args = ["--estado", str(estado), "--salida", str(tmp_path), "--as-of", DIA, "verificar-enlaces"]
    assert cli.main(args) == 0
    fila = json.loads((tmp_path / "ht02_F8.json").read_text())["resultados"][0]
    decision = tmp_path / "revision.json"
    decision.write_text(json.dumps({"F8": {ref: {"hash": fila["hash"], "accion": "RETRACTADA",
                                               "motivo": "Confirmada la nota del editor"}}}))
    assert cli.main([*args, "--aplicar", "--revisiones", str(decision)]) == 0
    assert almacen.estado("F2", clave="evd_id")["EVD-2"]["estado_verificacion"] == "FUENTE_RETIRADA"
    assert almacen.estado("F2", clave="baja_id")[f"F8/{DIA}/REF-{ref}"]["mensaje"]["emisor"] == "AG-15"
