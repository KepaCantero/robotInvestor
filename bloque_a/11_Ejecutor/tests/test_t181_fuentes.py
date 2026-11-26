"""PB-24 y PB-25: decisiones del custodio y propagación en los almacenes reales."""
import json
from pathlib import Path

import jsonschema
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
    for oid, estado, ps1 in [("OPP-3", "DESCARTADA", True), ("OPP-4", "VIGENTE", False)]:
        alm.escribir("F3", "AG-02", {"opp_id": oid, "estado": estado, "evidencias": ["CLM-1", "EVD-2"],
                     "evidencias_ps1": ["EVD-1", "EVD-2"], "ps1": ps1})
    alm.escribir("F2", "AG-12", {"evd_id": "EVD-1", "ref_id": "REF-" + RID, "direccion": "FAVORABLE",
                 "grado_independencia": "RAIZ", "nivel_fuente": "A", "tipo_fuente": "PRIMARIA"})
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-1", "evidencias_ps1": ["EVD-1"]})
    alm.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": "EVD-3", "ref_id": "REF-ANA-DOC-0003",
                 "direccion": "FAVORABLE", "grado_independencia": "RAIZ", "nivel_fuente": "B", "tipo_fuente": "SECUNDARIA"})
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-5", "estado": "VIGENTE", "ps1": True,
                 "evidencias": ["CLM-1", "EVD-3"], "evidencias_ps1": ["EVD-1", "EVD-3"]})
    revisar_bajas(bloque, "2026-06-04", "RUN-1")
    assert not alm.estado("F2", clave="baja_id")
    for dia in (DIA, "2026-07-01", "2026-07-01"):
        bloque.fijar_fecha(dia)
        revisar_bajas(bloque, dia, "RUN-2")
        if dia == DIA:
            assert not any("mes_bajas" in e for e in alm.leer("HA"))
    assert len([e for e in alm.leer("F2") if e.get("estado_verificacion") == "FUENTE_RETIRADA"]) == 1
    assert len([e for e in alm.leer("F3") if "revision_bajas" in e]) == 4
    assert "revision_bajas" not in alm.estado("F3")["OPP-3"]
    assert alm.estado("F3")["OPP-4"]["ps1"] is False
    assert alm.estado("F3")["OPP-5"]["revision_bajas"]["conclusion"] == "REQUIERE_REEVALUACION"
    assert alm.estado("F3")["OPP-5"]["ps1"] is False
    assert alm.estado("F2", clave="evd_id")["EVD-1"]["estado_verificacion"] == "FUENTE_RETIRADA"
    assert alm.estado("F3")["OPP-1"]["ps1"] is False
    assert alm.estado("F3")["OPP-2"]["revision_bajas"]["conclusion"] == "MANTIENE_RESPALDO"
    alertas = [x["mensaje"] for x in alm.leer("F2") if "mensaje" in x]
    assert [x["contrato"] for x in alertas] == ["CT-11"]
    paquetes = [x["mensaje"] for x in alm.leer("HA") if x.get("mes_bajas")]
    esquemas = json.loads((Path(__file__).parent / "goldens/anexo_b_esquemas.json").read_text())
    jsonschema.validate(alertas[0], esquemas["CT-11.ENCARGO"])
    motivo = "Enlace roto confirmado y sin alternativa tras dos barridos"
    assert motivo in alertas[0]["piezas"][0]["afirmacion"]
    assert [(x["contrato"], x["periodo"], x["bajas"]) for x in paquetes] == [
        ("CT-21", "2026-06", [{"ref_id": "REF-" + RID, "motivo": motivo}])]


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
    ruta.write_text(FICHA + "\n## Registro de bajas\n| ANA-DOC-0999 | T | M | 2027-01-01 | — |\n")
    original = ruta.read_text()
    for nombre in list(ARCHIVOS_REF.values())[1:]:
        (tmp_path / f"{nombre} - V1.0.md").write_text("")
    monkeypatch.setattr(cli, "ruta", lambda *a: tmp_path)
    monkeypatch.setattr("bloque_a.mantenimiento_fuentes._sin_copia", lambda r: True)
    monkeypatch.setattr(ht02.modulo, "verificar_archivo", lambda lineas, *a: barrido(url="https://example.org/doc")["resultados"] if lineas else [])
    args = ["--salida", str(tmp_path), "--estado", str(tmp_path / "estado"), "--as-of", DIA, "verificar-enlaces"]
    assert cli.main(args) == 0 and ruta.read_text() == original
    assert cli.main([*args, "--aplicar"]) == 0
    assert (RID, DIA) in list(bajas_registradas(ruta.read_text().splitlines()))
    from bloque_a.almacen import Almacen
    alertas = Almacen(tmp_path / "estado").estado("F2", clave="baja_id")
    assert len(alertas) == 1 and all("0999" not in clave for clave in alertas)
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


@pytest.mark.parametrize("motivo", ["primera\nsegunda", "texto <externo>", "clave AKIA" + "ABCDEFGHIJKLMNOP"])
def test_motivo_no_apto(motivo):
    with pytest.raises(ValueError):
        tratar("F7", FICHA, barrido(retractacion=True, hash="abc"),
               {RID: {"accion": "RETRACTADA", "hash": "abc", "motivo": motivo}})


def test_informe_sin_respuesta_y_revision_sin_observacion():
    datos = barrido(codigo_http=None, primer_fallo=DIA)
    assert f"Última verificación:** {DIA}" in tratar("F7", FICHA, datos, {})
    with pytest.raises(ValueError, match="observación HTTP"):
        tratar("F7", FICHA, datos, {RID: {"accion": "REPARAR"}})
    with pytest.raises(ValueError):
        tratar("F7", FICHA, barrido(estado="OK", hash="abc", retractacion=False),
               {RID: {"accion": "RETRACTADA", "hash": "abc", "motivo": "ejemplo"}})


def test_baja_con_alternativa_o_doi_sin_verificar(monkeypatch):
    from bloque_a import mantenimiento_fuentes as mf
    monkeypatch.setattr(mf.ht02.modulo, "_con_reintentos", lambda *a: ({"codigo": 200, "cuerpo": b'{"archived_snapshots":{}}'}, 1))
    assert not mf._sin_copia({"url": "https://example.org", "doi": "identificador", "doi_codigo_http": None})
    monkeypatch.setattr(mf, "_sin_copia", lambda r: True)
    assert "####" in tratar("F7", FICHA + "- **Copia archivada:** copia\n", barrido(), {})
    datos = barrido()
    datos["resumen"]["incidencia_red"] = True
    assert tratar("F7", FICHA, datos, {}) == FICHA


def test_lectura_registro_con_sufijo_y_error_contextual():
    lineas = ["## Registro de bajas (R24)", "| ANA-DOC-0001 | T | M | 2026-02-03 | — |"]
    assert list(bajas_registradas(lineas, "F7.md")) == [(RID, "2026-02-03")]
    with pytest.raises(ValueError, match=r"F7.md, fila 2"):
        list(bajas_registradas([lineas[0], lineas[1].replace("02-03", "13-45")], "F7.md"))


@pytest.mark.parametrize(("q", "nivel"), [(80, "A"), (79, "B"), (65, "B"), (64, "C"), (50, "C"), (49, "D")])
def test_bordes_de_calidad(q, nivel):
    from bloque_a.referencias import nivel_de_q
    assert nivel_de_q(q) == nivel
    assert nivel_de_q(65, {"referencias": {"niveles_q": {"B": 66}}}) == "C"


def test_igual_calidad_no_es_degradacion():
    datos = barrido(estado="CONTENIDO_CAMBIADO", hash="h1", codigo_http=200)
    with pytest.raises(ValueError, match="reducción"):
        tratar("F8", FICHA, datos, {RID: {"accion": "DEGRADAR", "hash": "h1", "motivo": "revisión",
                                         "puntos": [25, 20, 15, 10, 10, 5, 5]}})


def test_la_copia_debe_ser_la_aprobada_y_no_retractada(monkeypatch):
    from bloque_a.herramientas import ht02
    url = "https://web.archive.org/web/20260601/https://example.org/doc"
    datos = barrido(estado="CONTENIDO_CAMBIADO", hash="modificado", copia_archivada={"url": url})
    ficha = FICHA + "- **Hash de contenido:** anterior\n"
    revision = {"accion": "REPARAR", "hash": "modificado", "motivo": "copia", "url": url}
    monkeypatch.setattr(ht02, "comprobar_url", lambda *a: {"hash": "anterior", "huella": "ok"})
    with pytest.raises(ValueError):
        tratar("F8", ficha, datos, {RID: {**revision, "url": "https://example.org"}})
    monkeypatch.setattr(ht02, "comprobar_url", lambda *a: {"hash": "anterior", "huella": "ok", "retractacion": True})
    with pytest.raises(ValueError):
        tratar("F8", ficha, datos, {RID: revision})


def test_dos_ciclos_y_baja_con_fuentes_supervivientes(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(DIA)
    primeras = {k: v for k, v in b.almacen.estado("F3").items() if v.get("estado") == "PROPUESTA"}
    assert any(v.get("evidencias_ps1") for v in primeras.values())
    b.ciclo("2026-06-12")
    evds = b.almacen.estado("F2", clave="evd_id")
    arrastradas = {oid: op for oid, op in b.almacen.estado("F3").items() if op.get("estado") == "VIGENTE"
                   and oid in primeras and primeras[oid].get("evidencias_ps1")}
    assert arrastradas and all(op["evidencias_ps1"] for op in arrastradas.values())
    for oid, op in arrastradas.items():
        fuentes = [evds[e] for e in op["evidencias_ps1"]]
        for fuente in fuentes:
            ref = fuente["ref_id"]
            otras = {e.get("origen_documental") for e in fuentes if e["ref_id"] != ref and e.get("nivel_fuente") in ("A", "B")}
            if ref.startswith("REF-") and len(otras) >= 2 and op["ps1"]:
                b.fijar_fecha("2026-06-13")
                b.referencias.bajas["F7"].append((ref.removeprefix("REF-"), "2026-06-13"))
                revisar_bajas(b, "2026-06-13", "RUN-3")
                final = b.almacen.estado("F3")[oid]
                assert final["revision_bajas"]["conclusion"] == "MANTIENE_RESPALDO" and final["ps1"]
                return
    pytest.fail("El ciclo debe contener una opción con fuentes independientes supervivientes")


def test_una_fuente_retirada_no_vuelve_a_ingresar(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.modo = "vivo"
    dia = b.fijar_fecha(DIA)
    b.referencias.bajas["F7"] = [(RID, DIA)]
    f = {"proxy": "X", "senales": {}, "_piezas": [{"fuente": "REF-" + RID, "afirmacion": "dato anterior",
         "direccion": "favorable", "origen": "AG-14"}]}
    b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, dia, "RUN-1")
    assert not any(e.get("ref_id") == "REF-" + RID for e in b.almacen.leer("F2"))


def test_nivel_configurado_se_aplica_en_la_revision():
    revision = {"accion": "DEGRADAR", "hash": "h", "motivo": "revisión de la rúbrica",
                "puntos": [25, 20, 15, 5, 0, 0, 0]}
    datos = barrido(estado="CONTENIDO_CAMBIADO", codigo_http=200, hash="h", huella="h")
    assert "Q 65 (B)" in tratar("F8", FICHA, datos, {RID: revision})
    cfg = {"referencias": {"niveles_q": {"B": 66}}}
    assert "Q 65 (C)" in tratar("F8", FICHA, datos, {RID: revision}, cfg)


def test_reintento_tras_baja_persistida_antes_de_actualizar_clm(tmp_path, universo, monkeypatch):
    bloque = nuevo_bloque(tmp_path, universo)
    bloque.fijar_fecha(DIA)
    bloque.referencias.bajas["F7"].append((RID, DIA))
    almacen = bloque.almacen
    almacen.escribir("F2", "AG-12", {
        "tipo_entrada": "EVD", "evd_id": "EVD-1", "ref_id": "REF-" + RID, "clm_ids": ["CLM-1"],
        "estado_verificacion": "VERIFICADA", "direccion": "FAVORABLE", "grado_independencia": "RAIZ",
        "nivel_fuente": "A", "tipo_fuente": "PRIMARIA",
    })
    almacen.escribir("F2", "AG-12", {
        "tipo_entrada": "CLM", "clm_id": "CLM-1", "evidencias": ["EVD-1"], "evidencias_ps1": ["EVD-1"],
        "raices_independientes": 1, "ps1_cumple": True,
    })
    escribir = almacen.escribir

    def interrumpir(archivo, agente, entrada):
        if entrada.get("clm_id") == "CLM-1":
            raise OSError("fallo al guardar CLM")
        return escribir(archivo, agente, entrada)

    with monkeypatch.context() as parche:
        parche.setattr(almacen, "escribir", interrumpir)
        with pytest.raises(OSError, match="guardar CLM"):
            revisar_bajas(bloque, DIA, "RUN-1")
    assert almacen.estado("F2", clave="evd_id")["EVD-1"]["estado_verificacion"] == "FUENTE_RETIRADA"
    assert almacen.estado("F2", clave="clm_id")["CLM-1"]["ps1_cumple"] is True

    revisar_bajas(bloque, DIA, "RUN-2")
    clm = almacen.estado("F2", clave="clm_id")["CLM-1"]
    assert clm["raices_independientes"] == 0 and clm["ps1_cumple"] is False
    registros = almacen.leer("F2")
    revisar_bajas(bloque, DIA, "RUN-3")
    assert almacen.leer("F2") == registros


@pytest.mark.parametrize("interrumpir", [False, True], ids=["consulta-historica", "reintento"])
def test_retractacion_cli_al_corte_y_tras_interrupcion(tmp_path, monkeypatch, interrumpir, universo):
    from bloque_a.almacen import Almacen
    from bloque_a.herramientas import ht02
    from bloque_a.referencias import ARCHIVOS_REF, Referencias
    from conftest import config_pruebas

    from bloque_a import cli, mantenimiento_fuentes

    rutas = {k: tmp_path / f"{nombre} - V1.0.md" for k, nombre in ARCHIVOS_REF.items()}
    ficha = FICHA + "- **Temática:** TA-05\n- **Año:** 2020\n- **Tipo de fuente:** primaria\n"
    for k, ruta in rutas.items():
        ruta.write_text(ficha if k == "F7" else "")
    def respuesta_editor(url, metodo, cfg):
        return {"codigo": 200, "url_final": url, "redirecciones": [], "content_type": "text/html",
                "error": None, "cuerpo": b"This article has been retracted by its publisher."}, 1

    monkeypatch.setattr(ht02.modulo, "_con_reintentos", respuesta_editor)
    monkeypatch.setattr(cli, "ruta", lambda *a: tmp_path)
    estado = tmp_path / "estado"
    almacen = Almacen(estado)
    almacen.reloj.fijar(DIA)
    almacen.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": "EVD-2", "ref_id": "REF-" + RID,
                                      "estado_verificacion": "VERIFICADA"})
    args = ["--estado", str(estado), "--salida", str(tmp_path), "--as-of", DIA, "verificar-enlaces"]
    lector = Referencias(config_pruebas(), rutas)
    def consulta(lector, corte):
        return lector.para_clase("RV", corte, "backtest", archivos=("F7",))["referencias"]
    anterior = "2026-06-04"
    esperado = consulta(lector, anterior)
    metadatos = lector.por_id(RID, anterior)
    assert [f["ref_id"] for f in esperado] == ["REF-" + RID]
    assert cli.main(args) == 0
    fila = json.loads((tmp_path / "ht02_F7.json").read_text())["resultados"][0]
    decision = {"accion": "RETRACTADA", "hash": fila["hash"], "motivo": "Confirmada por el editor"}
    ruta_revision = tmp_path / "revision.json"
    ruta_revision.write_text(json.dumps({"F7": {RID: decision}}))
    aplicar = [*args, "--aplicar", "--revisiones", str(ruta_revision)]
    if interrumpir:
        def fallo(*args, **kwargs):
            raise OSError("interrupción después de publicar")
        with monkeypatch.context() as parche:
            parche.setattr(mantenimiento_fuentes, "avisar_curador", fallo)
            with pytest.raises(OSError, match="después de publicar"):
                cli.main(aplicar)
        assert almacen.estado("F2", clave="evd_id")["EVD-2"]["estado_verificacion"] == "VERIFICADA"
    assert cli.main(aplicar) == 0
    if interrumpir:
        registros = almacen.leer("F2")
        assert cli.main(aplicar) == 0
        assert almacen.leer("F2") == registros
        assert len(almacen.estado("F2", clave="baja_id")) == 1
        assert almacen.estado("F2", clave="evd_id")["EVD-2"]["estado_verificacion"] == "FUENTE_RETIRADA"
        assert list(bajas_registradas(rutas["F7"].read_text().splitlines())) == [(RID, DIA)]
        persistido = rutas["F7"].read_text()
        sin_red = {"fecha": DIA, "resumen": {"incidencia_red": True}, "resultados": []}
        assert tratar("F7", persistido, sin_red, {RID: decision}) == persistido
        ruta_revision.write_text(json.dumps({"F7": {RID: {**decision, "hash": "distinta"}}}))
        with pytest.raises(ValueError, match="Revisión sin referencia"):
            cli.main(aplicar)
    else:
        lector.actualizar()
        for leido in (lector, Referencias(config_pruebas(), rutas)):
            assert consulta(leido, anterior) == esperado
            assert leido.por_id(RID, anterior) == metadatos
            assert consulta(leido, DIA) == []
            assert leido.por_id(RID, DIA) is None
            assert consulta(leido, "2019-12-31") == []

        bloque = nuevo_bloque(tmp_path / "backtest", universo)
        bloque.referencias.rutas = rutas
        bloque.referencias.actualizar()
        dia = bloque.fijar_fecha(anterior)
        pieza = {"fuente": "REF-" + RID, "afirmacion": "Informe del editor", "direccion": "favorable", "origen": "AG-14"}
        opcion = {"proxy": "X", "senales": {}, "_piezas": [pieza], "_refs_ofrecidas": ["REF-" + RID]}
        bloque._filtrar_evidencia([opcion], dia)
        assert opcion["_piezas"] == [pieza]
        bloque._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [opcion]}, dia, "RUN-1")
        evidencia, = bloque.almacen.estado("F2", clave="evd_id").values()
        assert (evidencia["nivel_fuente"], evidencia["tipo_fuente"], evidencia["anio_publicacion"]) == ("A", "PRIMARIA", 2020)


def test_reintento_lote_con_degradacion_y_retractacion():
    segunda = "ANA-DOC-0002"
    catalogo = FICHA + FICHA.replace(RID, segunda)
    datos = barrido(estado="CONTENIDO_CAMBIADO", codigo_http=200, hash="nuevo", huella="abc")
    datos["resultados"].append({**datos["resultados"][0], "id": segunda, "retractacion": ["editor"]})
    decisiones = {RID: {"accion": "DEGRADAR", "hash": "nuevo", "puntos": [20, 10, 15, 5, 8, 7, 10], "motivo": "Revisión"},
                  segunda: {"accion": "RETRACTADA", "hash": "nuevo", "motivo": "Confirmación del editor"}}
    actualizado = tratar("F7", catalogo, datos, decisiones)
    siguiente = barrido(estado="OK", codigo_http=200, hash="nuevo", huella="abc")
    recuperado = tratar("F7", actualizado, siguiente, decisiones)
    assert "Q 75 (B)" in recuperado
    assert list(bajas_registradas(recuperado.splitlines())) == [(segunda, DIA)]
    assert tratar("F7", recuperado, siguiente, decisiones) == recuperado
    with pytest.raises(ValueError):
        tratar("F7", actualizado, siguiente, {**decisiones, RID: {**decisiones[RID], "motivo": "otra decisión"}})



def test_baja_antigua_sin_instantanea(tmp_path):
    from bloque_a.referencias import Referencias
    from conftest import config_pruebas

    catalogo = "## Registro de bajas (R24)\n| ANA-DOC-0001 | Título | Enlace roto | 2026-06-05 | — |\n"
    ruta = tmp_path / "F7.md"
    ruta.write_text(catalogo)
    lector = Referencias(config_pruebas(), {"F7": ruta})
    assert lector.bajas["F7"] == [(RID, DIA)]
    assert lector.motivos_bajas["F7", "REF-" + RID, DIA] == "Enlace roto"
    assert lector.por_id(RID, "2026-06-04") is None
    with pytest.raises(ValueError, match="Revisión sin referencia"):
        tratar("F7", catalogo, {**barrido(), "resultados": []}, {RID: {"accion": "RETRACTADA", "hash": "ajena"}})
