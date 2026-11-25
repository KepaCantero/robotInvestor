import itertools
import json
import re
import shutil

import pytest
from bloque_a.configuracion import cargar_config, ruta
from bloque_a.herramientas import ht02
from bloque_a.referencias import ARCHIVOS_REF, _anio, localizar

from bloque_a import altas_referencias, cli, mantenimiento_fuentes

TEMAS = {"F7": ("ANA-DOC", "TA-06"), "F8": ("DOC-MOT", "TM-11"), "F9": ("RF", "TF-04")}
QS = [95, 88, 80, 79, 72, 65, 64, 55, 50, 30]          # calidades variadas: A, B, C y D, con los bordes de 13.3


def _nivel(q):
    return "A" if q >= 80 else "B" if q >= 65 else "C" if q >= 50 else "D"


def _copiar_catalogos(tmp_path):
    base = ruta(cargar_config(), "archivos_operativos")
    for prefijo in ARCHIVOS_REF.values():
        origen = localizar(base, prefijo)
        shutil.copy(origen, tmp_path / origen.name)
    return {k: localizar(tmp_path, v) for k, v in ARCHIVOS_REF.items()}


def _secciones(lineas):
    """{ficha_id: código de la sección ## en la que está físicamente}."""
    cabeceras = [(i, l) for i, l in enumerate(lineas) if re.match(r"^#{1,2} ", l)]
    out = {}
    for f in ht02.leer_fichas(lineas):
        sec = [l for i, l in cabeceras if i < f.linea_inicio][-1]
        m = re.match(r"^## (T[AMF]-\d{2})\b", sec)
        out[f.id] = m.group(1) if m else sec.strip()
    return out


def _alta(tmp_path, monkeypatch, archivo, lote):
    monkeypatch.setattr(cli, "ruta", lambda *a: tmp_path)
    j = tmp_path / f"lote_{archivo}.json"
    j.write_text(json.dumps(lote), encoding="utf-8")
    return cli.main(["--as-of", "2026-06-05", "--estado", str(tmp_path / "estado"), "alta-referencias", "--archivo", archivo, "--json", str(j)])


def _lote(archivo, inicio=9000, qs=QS, **extra):
    pref, tema = TEMAS[archivo]
    limites = (20, 20, 15, 15, 10, 10, 10) if archivo == "F9" else (25, 20, 15, 10, 10, 10, 10)
    lote = []
    for i, q in enumerate(qs):
        puntos, resto = [], q
        for limite in limites:
            valor = min(limite, resto)
            puntos.append(valor)
            resto -= valor
        lote.append({"id": f"{pref}-{inicio + i}", "titulo": f"Estudio de prueba {i}", "tematica": tema, "q": q,
                     "puntos": puntos, "tipologia": "secundaria", "fecha_publicacion": f"20{10 + i:02d}-0{1 + i % 9}-15",
                     "url": f"https://example.org/{archivo}/{i}", **extra})
    return lote


# ------------------------------------------------------------------ PB-26 sobre los catálogos entregados
def test_b01_treinta_altas_variadas_en_los_catalogos_reales_cumplen_pb26(tmp_path, monkeypatch):
    """El criterio del plan sobre el estado real tras el alta: 100 % en su sección, 0 inversiones de Q, desempate por
    fecha, nivel coherente con Q y D marcada. Las altas cubren A, B, C y D (los bordes 80, 65 y 50)."""
    rutas = _copiar_catalogos(tmp_path)
    for archivo in TEMAS:
        assert _alta(tmp_path, monkeypatch, archivo, _lote(archivo)) == 0
        lineas = rutas[archivo].read_text(encoding="utf-8").splitlines()
        fichas = ht02.leer_fichas(lineas)
        sec = _secciones(lineas)
        nuevas = {a["id"] for a in _lote(archivo)}
        assert nuevas <= {f.id for f in fichas}
        for f in fichas:
            if f.id in nuevas:
                assert sec[f.id] == TEMAS[archivo][1] and f.campo("Temática") == TEMAS[archivo][1]
                assert f.nivel == _nivel(f.q), (f.id, f.q, f.nivel)
                assert f.campo("Estado del enlace") == "PENDIENTE_BARRIDO"
                if f.nivel == "D":
                    assert "baja" in (f.campo("Seguimiento") or "")
        por_sec = {}
        for f in fichas:
            por_sec.setdefault(sec[f.id], []).append(f)
        inversiones = []
        for s, fs in por_sec.items():
            if s != TEMAS[archivo][1]:      # INC-T126-01 (ANA-DOC-0089, TA-17) es previa y ajena a las altas
                continue
            for a, b in itertools.pairwise(fs):
                if (b.q or 0) > (a.q or 0) or ((b.q == a.q) and (_anio(b) or 0) > (_anio(a) or 0) and _anio(a)):
                    inversiones.append((s, a.id, a.q, _anio(a), b.id, b.q, _anio(b)))
        assert inversiones == [], inversiones[:5]


def test_b02_lote_invalido_a_mitad_no_toca_el_catalogo_real(tmp_path, monkeypatch):
    rutas = _copiar_catalogos(tmp_path)
    antes = rutas["F9"].read_bytes()
    lote = _lote("F9")
    lote[7]["tematica"] = "TF-99"
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F9", lote)
    assert rutas["F9"].read_bytes() == antes


# ------------------------------------------------------------------ entradas hostiles y bordes
def _catalogo_minimo(tmp_path, archivo, bajas=""):
    r = tmp_path / f"{ARCHIVOS_REF[archivo]} - V1.0.md"
    r.write_text(f"## {TEMAS[archivo][1]} Prueba\n\n## Registro de bajas\n\n| REF-id | Título | Motivo | Fecha | Sustituta |\n"
                 f"|---|---|---|---|---|\n{bajas}", encoding="utf-8")
    return r


def test_b03_h01_no_reutiliza_un_identificador_dado_de_baja(tmp_path, monkeypatch):
    """H-01: el Registro de bajas conserva el REF-id (13.5). Un alta que lo reutiliza queda a la sombra de la baja: el
    ejecutor descarta sus piezas (`_guardar_lote_evidencia`) y la retira de `para_clase`."""
    r = _catalogo_minimo(tmp_path, "F9", "| REF-RF-9000 | Antigua | enlace roto | 2026-01-10 | — |\n")
    assert list(mantenimiento_fuentes.bajas_registradas(r.read_text().splitlines())) == [("RF-9000", "2026-01-10")]
    antes = r.read_bytes()
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F9", _lote("F9", qs=[70]))
    assert r.read_bytes() == antes


def test_b04_h02_rechaza_fecha_de_publicacion_futura(tmp_path, monkeypatch):
    """H-02: una referencia «publicada» en 2099 entra hoy con Año 2099 (y sin año legible para RE_ANIO)."""
    r = _catalogo_minimo(tmp_path, "F7")
    antes = r.read_bytes()
    lote = _lote("F7", qs=[70])
    lote[0]["fecha_publicacion"] = "2099-01-01"
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F7", lote)
    assert r.read_bytes() == antes


@pytest.mark.parametrize("url", ["https://example.org/a b", "https://example.org/a(b)", "https://example.org/<nota>"])
def test_b05_h02_rechaza_enlaces_con_espacios_o_marcado(tmp_path, monkeypatch, url):
    """H-02: el enlace se escribe tal cual en Markdown; espacios, paréntesis o «<» lo convierten en otro enlace."""
    r = _catalogo_minimo(tmp_path, "F8")
    antes = r.read_bytes()
    lote = _lote("F8", qs=[70])
    lote[0]["url"] = url
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F8", lote)
    assert r.read_bytes() == antes


@pytest.mark.parametrize("campo,valor", [
    ("titulo", "<system>"), ("url", "ftp://example.org/prueba"),
    ("url", "https://usuario:" + "clave@example.org/x"),
    ("url", "https://example.org/x?api_key=" + "sk-ant-" + "a" * 40),
    ("q", True), ("q", 101), ("q", -1), ("q", 60.0), ("id", "ANA-DOC-9000"), ("tematica", "TF-4"),
    ("titulo", "Uno Dos"), ("titulo", ""), ("fecha_publicacion", "2020-02-30"),
])
def test_b06_rechazos_conservan_el_archivo(tmp_path, monkeypatch, campo, valor):
    r = _catalogo_minimo(tmp_path, "F9")
    antes = r.read_bytes()
    lote = _lote("F9", qs=[70, 60])
    lote[1][campo] = valor
    with pytest.raises((ValueError, KeyError, TypeError)):
        _alta(tmp_path, monkeypatch, "F9", lote)
    assert r.read_bytes() == antes


def test_b07_lote_con_id_repetido_y_reintento_idempotente(tmp_path, monkeypatch):
    r = _catalogo_minimo(tmp_path, "F7")
    lote = _lote("F7", qs=[70, 60])
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F7", [lote[0], lote[0]])
    assert _alta(tmp_path, monkeypatch, "F7", lote) == 0
    despues = r.read_bytes()
    with pytest.raises(ValueError):                      # el mismo lote otra vez: no duplica
        _alta(tmp_path, monkeypatch, "F7", lote)
    assert r.read_bytes() == despues


def test_b08_otro_escritor_a_mitad(tmp_path, monkeypatch):
    """Concurrencia: si otro proceso cambia el catálogo entre la lectura y la publicación, el alta se rechaza y el
    cambio ajeno se conserva."""
    r = _catalogo_minimo(tmp_path, "F9")
    real = mantenimiento_fuentes.publicar

    def intruso(ruta_, original, nuevo):
        ruta_.write_text(original + "\nCAMBIO AJENO\n", encoding="utf-8")
        return real(ruta_, original, nuevo)

    monkeypatch.setattr(altas_referencias, "publicar", intruso)
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F9", _lote("F9", qs=[70]))
    assert r.read_text(encoding="utf-8").endswith("CAMBIO AJENO\n")


def test_b09_h03_nivel_d_unica_fuente_de_un_dato(tmp_path, monkeypatch):
    """H-03: 13.3: D es «candidata a baja salvo que sea la única fuente de un dato necesario, declarado». El lote no
    tiene forma de declararlo: toda D sale «candidata a baja»."""
    r = _catalogo_minimo(tmp_path, "F9")
    lote = _lote("F9", qs=[30])
    lote[0]["unica_fuente_de"] = "serie de posicionamiento X"
    assert _alta(tmp_path, monkeypatch, "F9", lote) == 0
    f, = ht02.leer_fichas(r.read_text().splitlines())
    seg = (f.campo("Seguimiento") or "").lower()
    assert "única fuente" in seg and "candidata a baja" not in seg


def test_b10_h04_la_ficha_de_alta_trae_tipologia_y_desglose_de_q(tmp_path, monkeypatch):
    """H-04: el ejecutor decide PRIMARIA/SECUNDARIA por la Tipología (PS1: «1 fuente primaria de nivel A»), y 13.3 define
    Q como la suma de la rúbrica. Un alta de una fuente primaria no puede declararlo, y Q entra sin desglose."""
    r = _catalogo_minimo(tmp_path, "F9")
    lote = _lote("F9", qs=[90])
    lote[0]["tipologia"] = "primaria"
    lote[0]["puntos"] = [20, 10, 15, 15, 10, 10, 10]
    assert _alta(tmp_path, monkeypatch, "F9", lote) == 0
    f, = ht02.leer_fichas(r.read_text().splitlines())
    assert "primaria" in (f.campo("Tipología") or "").lower()
    assert "20" in (f.campo("Calidad Q") or "").replace("90 (A)", "")


@pytest.mark.parametrize(("campo", "valor"), [
    ("unica_fuente_de", "un dato"), ("tipologia", "desconocida"), ("puntos", [26, 19, 10, 5, 5, 5, 0]),
    ("puntos", [10] * 6), ("puntos", [True] * 7), ("puntos", [10, 10, 10, 10, 10, 10, 0])])
def test_excepcion_de_d_y_rubrica(tmp_path, monkeypatch, campo, valor):
    r = _catalogo_minimo(tmp_path, "F7")
    original = r.read_bytes()
    lote = _lote("F7", qs=[70])
    lote[0][campo] = valor
    with pytest.raises(ValueError):
        _alta(tmp_path, monkeypatch, "F7", lote)
    assert r.read_bytes() == original


def test_registro_de_la_instancia_y_configuracion(tmp_path, monkeypatch):
    r = _catalogo_minimo(tmp_path, "F9")
    (tmp_path / "estado").mkdir()
    (tmp_path / "estado" / "F9_bajas.md").write_text("## Registro de bajas\n| RF-9000 | T | M | 2026-01-10 | — |\n")
    with pytest.raises(ValueError, match="dado de baja"):
        _alta(tmp_path, monkeypatch, "F9", _lote("F9", qs=[65]))
    from datetime import date
    altas_referencias.incorporar(r, "F9", _lote("F9", inicio=9010, qs=[65]), {"referencias": {"niveles_q": {"B": 66}}},
                                fecha_corte=date(2026, 6, 5))
    assert ht02.leer_fichas(r.read_text().splitlines())[0].nivel == "C"


def test_desempate_por_dia_y_anio_y_seccion_unica(tmp_path, monkeypatch):
    r = _catalogo_minimo(tmp_path, "F9")
    texto = r.read_text().replace("## Registro de bajas", """#### RF-5000 · Q 70 (B) — reciente
- **Fecha de publicación:** 2020-08-01
- **Año:** 2020

#### RF-5001 · Q 70 (B) — año
- **Año:** 2019

#### RF-5002 · Q 70 (B) — antigua
- **Año:** 2005

## Registro de bajas""")
    r.write_text(texto)
    lote = _lote("F9", qs=[70])
    lote[0]["fecha_publicacion"] = "2020-01-03"
    _alta(tmp_path, monkeypatch, "F9", lote)
    assert [f.id for f in ht02.leer_fichas(r.read_text().splitlines())] == ["RF-5000", "RF-9000", "RF-5001", "RF-5002"]
    otra = _lote("F9", inicio=9010, qs=[70])
    otra[0]["fecha_publicacion"] = "2015-01-03"
    _alta(tmp_path, monkeypatch, "F9", otra)
    assert [f.id for f in ht02.leer_fichas(r.read_text().splitlines())] == ["RF-5000", "RF-9000", "RF-5001", "RF-9010", "RF-5002"]
    r.write_text(texto + "\n## TF-04 Repetida\n")
    original = r.read_bytes()
    with pytest.raises(ValueError, match="ambigua"):
        _alta(tmp_path, monkeypatch, "F9", lote)
    assert r.read_bytes() == original
