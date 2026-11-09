"""r2_02 · H-02: el Analista declara naturaleza y horizonte principal incoherentes. El ejecutor no debe «arreglarlo» en silencio:
C17 (HT-09) tiene que bloquear, y el run no puede salir COMPLETO y ENTREGADO con la opción incoherente publicada.
(a) TACTICA + H5 (ofrecido en RV);  (b) VALORACION + H2;  (c) ESTRUCTURAL + H3;
(d) naturaleza inválida «FOO» + H5: ¿se sustituye en silencio por ESTRUCTURAL?;
(e) ESTRUCTURAL sin horizonte principal;  (f) control coherente CICLICA + H3."""
import json, pathlib, tempfile
from bloque_a import mock_respuestas as mr
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR, naturaleza_coherente
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

orig = mr._ficha


def run(etq, cambios: dict, quitar=()):
    def _f(u, msg, ctx, rng, iny):
        out = orig(u, msg, ctx, rng, iny)
        out.update(cambios)
        for k in quitar:
            out.pop(k, None)
        return out
    mr._ficha = _f
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
    r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
    mr._ficha = orig
    ops = r["paquete"]["clases"].get("RV", {}).get("opciones", [])
    inco = [(o["opp_id"], o["naturaleza_inversion"], o["horizonte_principal"]) for o in ops
            if not naturaleza_coherente(o["naturaleza_inversion"], o["horizonte_principal"])]
    c17 = [x for x in json.dumps(r["g3"].get("bloqueos"), ensure_ascii=False).split("},") if "C17" in x]
    g3v = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V"]
    c17_ha = sum(json.dumps(e, ensure_ascii=False).count("C17") for e in g3v)
    lim = [x[:170] for x in r["paquete"]["limitaciones"] if not x.startswith("Ninguna")]
    motivo = r["paquete"]["clases"].get("RV", {}).get("menos_de_tres_motivo")
    print(f"[{etq}] estado={r['estado']} entrega={r.get('entrega')} g3={r['g3']['dictamen']} n_opciones={len(ops)} "
          f"publicadas_incoherentes={inco}\n      C17 en bloqueos finales={len(c17)} C17 en G3V(HA)={c17_ha} "
          f"nat/hp={[(o['naturaleza_inversion'], o['horizonte_principal']) for o in ops]}\n      limitaciones={lim}")
    return r


run("a_TACTICA_H5", {"naturaleza_inversion": "TACTICA", "horizonte_principal": "H5"})
run("b_VALORACION_H2", {"naturaleza_inversion": "VALORACION", "horizonte_principal": "H2"})
run("c_ESTRUCTURAL_H3", {"naturaleza_inversion": "ESTRUCTURAL", "horizonte_principal": "H3"})
run("d_FOO_H5", {"naturaleza_inversion": "FOO", "horizonte_principal": "H5"})
run("e_ESTRUCTURAL_sin_hp", {"naturaleza_inversion": "ESTRUCTURAL"}, quitar=("horizonte_principal",))
run("f_control_CICLICA_H3", {"naturaleza_inversion": "CICLICA", "horizonte_principal": "H3"})
