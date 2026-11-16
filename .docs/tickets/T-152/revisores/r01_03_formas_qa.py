"""T-152 · QA r01 · formas de fichero inesperadas en `.docs/scripts/cadena_a_b.py` después de `_forma_paquete` y de la
comprobación de textos de `_leer_yaml_extra` (O-02 de la QA r01 de T-150).

Uso:  .venv/bin/python -I .docs/tickets/T-152/revisores/r01_03_formas_qa.py <carpeta temporal> [--raiz <copia>]

Ejecuta `main()` en el proceso con los ejecutores sustituidos por dobles (sin red, sin coste, sin los ejecutores reales) y,
por caso, dice si termina con un código y un mensaje (OK) o con una excepción sin capturar (TRAZA), y si el mensaje o
`resumen.json` copian un dato protegido o una marca del contenido (FUGA). Los casos de la QA de T-150 (O-02) van como
control; los demás son nuevos. Termina con 0 (solo informa: la lectura, en `qa.md`)."""
import argparse
import contextlib
import copy
import importlib.util
import io
import json
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("tmp")
ap.add_argument("--raiz", default=str(Path(__file__).resolve().parents[4]))
ARGS = ap.parse_args()
RAIZ = Path(ARGS.raiz).resolve()
TMP = Path(ARGS.tmp).resolve()
TMP.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
spec = importlib.util.spec_from_file_location("cadena_a_b_qa", RAIZ / ".docs" / "scripts" / "cadena_a_b.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
EJEMPLO = json.loads((RAIZ / "bloque_a" / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json")
                     .read_text(encoding="utf-8"))
CORREO = "inversor.prueba" + "@example.com"
MARCA = "marca-del-contenido-qa"
EXTRA = json.dumps({"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}})
OPP = "OPP-2026-9112"


def cli_doble(ruta_paquete):
    def cli(bloque, args):
        if bloque == "a" and args[-1] == "ciclo":
            return {"run_id": "RUN-X", "entrega": "ENTREGADA", "g3": "APTO", "entregables": {"paquete_json": str(ruta_paquete)}}
        if bloque == "b":
            return {"pet_id": "PET-QA-1", "estado_peticion": "ENTREGADA", "acuse_inmediato": {"admision": "ADMITIDA"}}
        return {"ret_id": "RET-QA-1", "estado": "REGISTRADA"}
    return cli


def correr(nombre, paquete_texto=None, extra=EXTRA, n=[0]):
    n[0] += 1
    d = TMP / f"caso_{n[0]:02d}"
    d.mkdir(parents=True, exist_ok=True)
    ruta = d / "paquete.json"
    if paquete_texto is not None:
        ruta.write_text(paquete_texto, encoding="utf-8", errors="surrogatepass")
    else:
        ruta.write_text(json.dumps(EJEMPLO, ensure_ascii=False), encoding="utf-8")
    cfg = d / "extra.yaml"
    cfg.write_text(extra, encoding="utf-8", errors="surrogatepass")
    mod._cli = cli_doble(ruta)
    err, out = io.StringIO(), io.StringIO()
    w = d / "w"
    try:
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            codigo = mod.main(["--trabajo", str(w), "--config-a", str(cfg)])
        estado = f"OK, código {codigo}"
    except BaseException as e:   # noqa: BLE001
        estado = f"TRAZA {type(e).__name__}"
    resumen = (w / "resumen.json").read_text(encoding="utf-8", errors="replace") if (w / "resumen.json").exists() else ""
    texto = err.getvalue() + out.getvalue() + resumen
    fuga = [m for m in ("inversor",) if m in texto]
    copia = MARCA in texto
    fuera = sorted(str(p.relative_to(TMP)) for p in TMP.rglob("*escape*"))
    mensaje = err.getvalue().strip().splitlines()[-1][:150] if err.getvalue().strip() else ""
    print(f"| {nombre} | {estado}{' · FUGA R8 ' + str(fuga) if fuga else ''}{' · copia contenido' if copia else ''}{' · FUERA ' + str(fuera) if fuera else ''} | "
          f"{mensaje} |", flush=True)


def con(f, ascii_=False):
    p = copy.deepcopy(EJEMPLO)
    f(p)
    return json.dumps(p, ensure_ascii=ascii_)


def entrada(p, opp=OPP):
    return next(e for e in p["paquete_para_bloque_B"] if e["opp_id"] == opp)


def opcion(p, opp=OPP):
    return next(o for c in p["clases"].values() for o in c["opciones"] if o["opp_id"] == opp)


def renombrar(p, nuevo):
    entrada(p)["opp_id"] = nuevo
    opcion(p)["opp_id"] = nuevo


def main():
    print("| Caso | Resultado | Última línea del mensaje |\n|---|---|---|")
    correr("control: el paquete de ejemplo")
    # controles de O-02 (T-150)
    correr("O-02: «clases» es una lista", con(lambda p: p.__setitem__("clases", [MARCA])))
    correr("O-02: una opción sin opp_id", con(lambda p: opcion(p).pop("opp_id")))
    correr("O-02: correspondencia con una lista", extra="cadena_b:\n  correspondencia_ambitos:\n    A: [" + CORREO + "]\n")
    # paquetes nuevos
    correr("JSON anidado 100 000 niveles en un campo que no se mira",
           con(lambda p: p.__setitem__("x", None)).replace('"x": null', '"x": ' + "[" * 100000 + "]" * 100000))
    correr("opp_id de 300 cifras (el patrón ^OPP-[0-9]{4}-[0-9]{4,}$ lo admite)",
           con(lambda p: renombrar(p, "OPP-2026-" + "9" * 300)))
    correr("opp_id con un salto de línea final (el $ de Python lo admite)", con(lambda p: renombrar(p, OPP + "\n")))
    correr("opp_id con «/../escape» (el patrón lo rechaza)", con(lambda p: renombrar(p, OPP + "/../../escape")))
    correr("símbolo con un sustituto suelto (\\ud800) y sin correspondencia",
           con(lambda p: entrada(p)["indicador_seguimiento"].__setitem__("simbolo", "SIMB-\ud800"), True))
    correr("nombre con un sustituto suelto (\\ud800), con correspondencia",
           con(lambda p: entrada(p).__setitem__("nombre", "Letras \ud800 " + MARCA), True))
    correr("una opción que es un texto con un correo (se salta)",
           con(lambda p: next(iter(p["clases"].values()))["opciones"].append(CORREO + " " + MARCA)))
    correr("una entrada de paquete_para_bloque_B que es un número", con(lambda p: p["paquete_para_bloque_B"].append(7)))
    correr("indicador_seguimiento es una lista", con(lambda p: entrada(p).__setitem__("indicador_seguimiento", [MARCA])))
    correr("«clases» repetida: la segunda es una lista", con(lambda p: None)[:-1] + ', "clases": [' + json.dumps(MARCA) + ']}')
    correr("un número 1e400 (infinito) en un campo", con(lambda p: p.__setitem__("x", None)).replace('"x": null', '"x": 1e400'))
    correr("run_id que no es texto", con(lambda p: p.__setitem__("run_id", [CORREO])))
    # --config-a nuevos
    correr("--config-a anidado 100 000 niveles", extra="a: " + "[" * 100000 + "]" * 100000 + "\n")
    correr("--config-a con fechas como símbolo (YAML)", extra="cadena_b:\n  correspondencia_ambitos:\n    2024-01-01: liquidez_eur\n")
    correr("--config-a con !!set como correspondencia", extra="cadena_b:\n  correspondencia_ambitos: !!set {a, b}\n")
    correr("--config-a con un símbolo con sustituto suelto", extra='cadena_b:\n  correspondencia_ambitos:\n    "X\\ud800": liquidez_eur\n')
    correr("--config-a con «cadena_b.peticion» lista", extra="cadena_b:\n  correspondencia_ambitos: {LETRAS-EUR-12M: liquidez_eur}\n"
                                                         "  peticion: [" + CORREO + "]\n")
    correr("--config-a con un ancla y referencias (alias)", extra="x: &a [" + ", ".join(["1"] * 50) + "]\ny: [*a, *a, *a, *a]\n"
                                                              "cadena_b:\n  correspondencia_ambitos: {LETRAS-EUR-12M: liquidez_eur}\n")
    return 0


if __name__ == "__main__":
    sys.setrecursionlimit(1000)
    sys.exit(main())
