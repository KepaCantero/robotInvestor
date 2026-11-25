"""T-204: genera `enmienda4_constitucion.patch` (el nombre del fichero es el de la r01; desde la r02 la enmienda se llama
«enmienda 6», QA r01 H-02) a partir de la Constitución vigente, sin tocarla.
La enmienda 6 lleva la Constitución de la V0.6 a la V0.7. Hace estos cambios:
- quita el Bloque A Forex de las cuatro menciones (cambio 17, §2, §14 y D-20), cada una anotada;
- añade el cambio 43 y D-48 con las palabras del operador;
- añade la línea del §15;
- pone la fecha nueva en la cabecera.
Las enmiendas 4 y 5 son propuestas pendientes en `.docs/diseno/` (INC-T204-01).
Uso (desde la raíz): .venv/bin/python .docs/tickets/T-204/generar_enmienda.py [--comprobar]
Con --comprobar termina con 1 si el parche guardado no es el que se genera ahora."""
import difflib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
REL = "sistema_global/constitucion/Constitucion_Global.md"
PARCHE = Path(__file__).resolve().parent / "enmienda4_constitucion.patch"
PALABRAS = "«Elimina el bloque A Forex definitivamente» y «Haz esas tres cosas. Te doy mi consentimiento»"


def enmendar(t: str) -> str:
    lineas = t.split("\n")
    d47 = [i for i, l in enumerate(lineas) if l.startswith("| D-47 |")]
    assert len(d47) == 1
    lineas.insert(d47[0] + 1, "| D-48 | Enmienda 6 (T-204): el Bloque A Forex se elimina del repositorio y de esta Constitución por orden "
                  "expresa del operador; el sistema queda con los Bloques A y B generales y los demás del mapa (§2), sin cambios; "
                  "D-20 queda con B Forex | RATIFICADO | 2026-11-25 |")
    r42 = [i for i, l in enumerate(lineas) if l.startswith("| 42 | **Una copia por usuario:**")]
    assert len(r42) == 1 and lineas[r42[0] + 1] == ""
    lineas[r42[0] + 2:r42[0] + 2] = [
        f"**Qué cambia de la V0.6 a la V0.7 (enmienda 6).** `[RATIFICADO]` el 25 de noviembre de 2026 (T-204), por orden expresa "
        f"del operador: {PALABRAS}. Las enmiendas 4 y 5 siguen propuestas; la numeración provisional de la 5 se corre en uno.",
        "", "| N.º | Cambio | Problema que resuelve | Sección |", "| --- | --- | --- | --- |",
        "| 43 | **Fuera el Bloque A Forex:** se elimina del repositorio, de sus gates y de este texto (cambio 17, §2, §14 y D-20); "
        "las divisas las sigue cubriendo el Bloque A general | Una prueba antigua que ya no forma parte del sistema seguía en el "
        "repositorio y en la Constitución | §0, §2, §14, §15 |", ""]
    t = "\n".join(lineas)
    pares = [
        ("# Constitución Global del Robot Inversor — V0.6\n\nNov 9, 2026 ·", "# Constitución Global del Robot Inversor — V0.7\n\nNov 25, 2026 ·"),
        ("Esta V0.6 (9 de noviembre de 2026) **sustituye a la V0.5**: incorpora la **enmienda 3**",
         "Esta V0.7 (25 de noviembre de 2026) **sustituye a la V0.6**: incorpora la **enmienda 6** (T-204: el Bloque A Forex se "
         "elimina del repositorio y de este texto), **ordenada por el operador** ese mismo día con su consentimiento expreso "
         "(cambio 43 y decisión D-48). La V0.6 (9 de noviembre de 2026) sustituyó a la V0.5: incorporó la **enmienda 3**"),
        ("| 17 | **A Forex y B Forex fuera** del sistema; se usan A y B generales, que analizan todo tipo de activos. La Fase 1 sigue "
         "en divisas | Eran pruebas; dos variantes de los mismos bloques | §2, §14 |",
         "| 17 | **B Forex fuera** del sistema; se usan A y B generales, que analizan todo tipo de activos. La Fase 1 sigue en divisas "
         "(texto reducido por la enmienda 6, D-48) | Era una prueba: una variante del mismo bloque | §2, §14 |"),
        ("`[RATIFICADO]` A Forex y B Forex fueron pruebas y **no forman parte del sistema** (D-20);",
         "`[RATIFICADO]` B Forex fue una prueba y **no forma parte del sistema** (D-20; texto reducido por la enmienda 6, D-48);"),
        ("faltan 6). A Forex y B Forex quedan fuera (D-20) |", "faltan 6). B Forex queda fuera (D-20; enmienda 6, D-48) |"),
        ("| D-20 | A Forex y B Forex fuera del sistema; A y B generales; la Fase 1 sigue en divisas | RATIFICADO | 2026-11-07 |",
         "| D-20 | B Forex fuera del sistema; A y B generales; la Fase 1 sigue en divisas (texto reducido por la enmienda 6, D-48) | "
         "RATIFICADO | 2026-11-07 |"),
        ("La **enmienda 3** (T-59) se aplicó y ratificó el 9-11-2026 (V0.6).",
         "La **enmienda 3** (T-59) se aplicó y ratificó el 9-11-2026 (V0.6). La **enmienda 6** (T-204) se aplicó el 25-11-2026 por "
         "orden expresa del operador, que dio su consentimiento ese día (V0.7); las enmiendas 4 y 5 siguen propuestas."),
    ]
    for a, b in pares:
        assert t.count(a) == 1, a[:70]
        t = t.replace(a, b)
    return t


def parche() -> str:
    antes = (RAIZ / REL).read_text(encoding="utf-8")
    return "".join(difflib.unified_diff(antes.splitlines(keepends=True), enmendar(antes).splitlines(keepends=True),
                                        fromfile=f"a/{REL}", tofile=f"b/{REL}"))


def main() -> int:
    nuevo = parche()
    if "--comprobar" in sys.argv:
        igual = PARCHE.read_text(encoding="utf-8") == nuevo
        print("el parche guardado es el que se genera" if igual else "el parche guardado NO es el que se genera")
        return 0 if igual else 1
    PARCHE.write_text(nuevo, encoding="utf-8")
    print(f"escrito {PARCHE.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
