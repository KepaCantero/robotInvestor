import json

import pytest
from bloque_a.herramientas import ht02
from bloque_a.referencias import ARCHIVOS_REF

from bloque_a import cli


def test_treinta_altas_y_lote_invalido(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "ruta", lambda *a: tmp_path)
    for archivo, pref, tema in [("F7", "ANA-DOC", "TA-06"), ("F8", "DOC-MOT", "TM-11"), ("F9", "RF", "TF-04")]:
        r = tmp_path / f"{ARCHIVOS_REF[archivo]} - V1.0.md"
        r.write_text(f"## {tema} Prueba\n\n## Registro de bajas\n")
        altas = [{"id": f"{pref}-{i:04d}", "titulo": f"Estudio {i}", "tematica": tema, "q": 41+i//2,
                  "fecha_publicacion": f"2020-01-{i+1:02d}", "url": f"https://example.org/{i}"} for i in range(10)]
        archivo_json = tmp_path / "lote.json"
        cmd = ["alta-referencias", "--archivo", archivo, "--json", str(archivo_json)]
        archivo_json.write_text(json.dumps([*altas, {**altas[0], "tematica": "XX-99"}]))
        original = r.read_bytes()
        with pytest.raises(ValueError):
            cli.main(cmd)
        assert r.read_bytes() == original
        archivo_json.write_text(json.dumps(altas))
        assert cli.main(cmd) == 0
        fichas = ht02.leer_fichas(r.read_text().splitlines())
        assert [f.id for f in fichas] == [a["id"] for a in reversed(altas)]
        assert all(f.nivel == "D" and "baja" in f.campo("Seguimiento") for f in fichas)
        assert r.read_text().rstrip().endswith("## Registro de bajas")
