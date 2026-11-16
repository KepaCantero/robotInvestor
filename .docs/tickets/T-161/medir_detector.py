"""T-161 · Medida del detector de conflictos de las guías CT-18 (`guias.conflicto_del_item`).

Pasa los 50 ataques de la QA r01 de T-158 (`.docs/tickets/T-158/revisores/r01_01_detector.py`, sin cambiarlo) y los ejemplos
válidos y de frontera de `tests/test_t161_guias.py` (VALIDOS_DISENO, FRONTERA) e imprime una tabla con lo que pasa y los
falsos positivos. En la r02, también los 68 ataques nuevos y los 40 válidos de la QA r01 de T-161 y los 40 de dominio
(`tests/test_t161_r02.py`: ATAQUES, VALIDOS, DOMINIO, FRONTERA_DOMINIO). Sale 1 si algún ataque pasa (salvo el repartido
que se explica en la prueba) o si algún ejemplo válido es conflicto.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python ../../.docs/tickets/T-161/medir_detector.py
"""
import importlib.util
import sys
from pathlib import Path

EJ = Path.cwd()
sys.path[:0] = [str(EJ), str(EJ / "tests")]
from bloque_a import guias as G  # noqa: E402


def cargar(ruta: Path, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    raiz = EJ.parents[1]
    r01 = cargar(raiz / ".docs" / "tickets" / "T-158" / "revisores" / "r01_01_detector.py", "r01_01")
    t161 = cargar(EJ / "tests" / "test_t161_guias.py", "t161")
    pasan = [n for n, it in r01.CONTROL + r01.ATAQUES if not G.conflicto_del_item(it)]
    fp = [n for n, it in t161.VALIDOS_DISENO if G.conflicto_del_item(it)]
    frontera = [(n, (G.conflicto_del_item(it) or {}).get("familias")) for n, it, _ in t161.FRONTERA]
    print(f"ataques de r01_01: {len(r01.ATAQUES)}; pasan el detector: {len(pasan)} {pasan or ''}")
    print(f"ejemplos válidos del diseño: {len(t161.VALIDOS_DISENO)}; falsos positivos: {len(fp)} {fp or ''}")
    print("frontera (falsos positivos aceptados por prudencia):")
    for n, f in frontera:
        print(f"  - {n}: {f}")
    r02 = cargar(EJ / "tests" / "test_t161_r02.py", "t161_r02")
    nuevos = [n for _, n, items in r02.ATAQUES
              if not all(G.conflicto_para(i, "AG-03") for i in items) and n not in r02.REPARTIDAS_CON_UN_ITEM_INOCUO]
    parciales = [n for _, n, items in r02.ATAQUES if n in r02.REPARTIDAS_CON_UN_ITEM_INOCUO]
    fp_qa = [t for _, t in r02.VALIDOS if G.conflicto_del_item(r02.it(que_cambia=t))]
    fp_dom = [t for t in r02.DOMINIO + r02.YA_NO_SON_FALSOS_POSITIVOS if G.conflicto_del_item(r02.it(que_cambia=t))]
    fr_dom = [t for t in r02.FRONTERA_DOMINIO if G.conflicto_del_item(r02.it(que_cambia=t))]
    print(f"ataques nuevos (QA r01 de T-161): {len(r02.ATAQUES)}; pasan: {len(nuevos)} {nuevos or ''}; "
          f"un ítem inocuo en una guía que se retira entera: {parciales}")
    print(f"válidos de la QA: {len(r02.VALIDOS)}; falsos positivos: {len(fp_qa)} {fp_qa or ''}")
    print(f"válidos de dominio: {len(r02.DOMINIO) + len(r02.FRONTERA_DOMINIO)} (+{len(r02.YA_NO_SON_FALSOS_POSITIVOS)} que eran "
          f"frontera); falsos positivos: {len(fp_dom) + len(fr_dom)} {fp_dom + fr_dom}")
    return 1 if pasan or fp or nuevos or fp_qa or fp_dom else 0


if __name__ == "__main__":
    sys.exit(main())
