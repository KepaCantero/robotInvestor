"""QA r02 de T-164 · regresiones de las correcciones r02 (H-01 a H-05) en una copia del corpus real.

1. Frases que ahora se juntan (RE_FIN_FRASE sin «;» y con abreviaturas) y claves JSON (la frase empieza en la clave), con
   IDX-FICT-001, el único símbolo real con forma de ficha. «ERROR»/«INFO» se comprueban; «[INF]» solo informa de un caso
   discutible (el criterio del ticket lo decide así a sabiendas).
2. Que el corpus real no gane errores ni pierda notas: el informe es el de la QA r01 (2 errores, 2 avisos).
3. H-04 y H-05: un enlace simbólico al mismo destino se rechaza; un enlace duro no se pisa; un destino de solo lectura (0444)
   se regenera y conserva el modo.
Sale 1 si alguna comprobación falla. El corpus del repositorio no se toca (huellas antes y después).

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-164/revisores/r02_01_regresiones.py
"""
import contextlib
import hashlib
import io
import os
import shutil
import sys
import tempfile
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
RAIZ = EJ.parent
from bloque_a.herramientas import verificador_ids as vi

P_RV = "02_System_prompts/System prompt - Analista de Renta Variable - Versión óptima V5.0.md"
X = "IDX-FICT-001"
CASOS = [
    # (clave, esperado: "ERROR", "INFO", "ERROR+INFO" o "[INF]", línea)
    ("A01 «etc.» sigue cerrando la frase", "INFO", f"Fichas ST-DESC-001, VOL-GARCH-001, etc. La serie {X} sube."),
    ("A02 «?» y «!» siguen cerrando", "INFO", f"¿Qué ficha se usa? ¡La serie {X} sube!"),
    ("A03 «p. ej.» con coma", "ERROR", f"Una ficha de índices, p. ej., {X}."),
    ("A04 «vs.» entre dos fichas", "ERROR", f"La ficha ST-DESC-001 vs. {X}."),
    ("A05 «e.g.»", "ERROR", f"Use an index card (ficha), e.g. {X}."),
    ("A06 «Ej.» con mayúscula", "[INF]", f"Una ficha de índices (Ej. {X})."),
    ("A07 «i.e.», fuera de la lista", "[INF]", f"La ficha de índices (i.e. {X})."),
    ("A08 «;» junta una ficha con la serie de después", "[INF]", f"Se usa la ficha ST-DESC-001; la serie {X} sube."),
    ("A09 clave «ficha» con estado y la serie en otra clave", "INFO", f'{{"ficha":"VIGENTE","serie_ht01":"{X}"}}'),
    ("A10 clave «ficha» y la serie en la prosa de otro valor", "INFO", f'{{"ficha":"VIGENTE","nota":"La serie {X} sube"}}'),
    ("A11 «ficha» en prosa y la serie en un JSON detrás", "INFO", f'La ficha ST-DESC-001 lee {{"serie_ht01":"{X}"}}'),
    ("A12 array de objetos: dos objetos, serie y ficha", "ERROR+INFO",
     f'{{"datos":[{{"serie_ht01":"{X}"}},{{"ficha_id":"{X}"}}]}}'),
    ("A13 array de objetos anidado dos niveles", "ERROR", f'{{"a":[{{"b":[{{"method_id":"{X}"}}]}}]}}'),
    ("A14 array de escalares con corchetes dentro de la cadena, clave «fichas»", "ERROR", f'{{"fichas":["{X} [v1]"]}}'),
    ("A15 array de escalares con llaves dentro de la cadena, method_id", "[INF]", f'{{"method_id":["{X} {{v1}}"]}}'),
    ("A16 array dentro de array en estado_madurez_metodos", "[INF]", f'{{"estado_madurez_metodos":[["{X}"]]}}'),
    ("A17 «fichaje» con «;» (no es «ficha»)", "INFO", f"Tras el fichaje; la serie {X} sube."),
]
resultados: list[tuple[str, bool]] = []


def comprobar(que: str, ok: bool, detalle: str = "") -> None:
    resultados.append((que, ok))
    print(f"[{'OK ' if ok else 'MAL'}] {que}" + (f" · {detalle}" if detalle else ""))


def huellas() -> dict[str, str]:
    return {p.relative_to(RAIZ).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(RAIZ.rglob("*")) if p.is_file() and p.suffix in (".md", ".docx") and "11_Ejecutor" not in p.parts}


def lanzar(*args: str) -> int:
    with contextlib.redirect_stderr(io.StringIO()):
        return vi.main(["--raiz", str(RAIZ), *args])


antes = huellas()
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    r = tmp / "bloque_a"
    shutil.copytree(RAIZ, r, ignore=lambda d, n: [x for x in n if x == "11_Ejecutor" or x.startswith("99_Historico")])
    p = r / P_RV
    lineas = p.read_text(encoding="utf-8").split("\n")
    donde = {}
    for clave, _, linea in CASOS:
        lineas += ["", linea]
        donde[clave] = len(lineas)
    p.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    inf = vi.verificar(r)
    nivel_de: dict[int, set[str]] = {}
    for h in inf["hallazgos"]:
        if h["id"] == X:
            for u in h["ubicaciones"]:
                if u["archivo"] == P_RV:
                    nivel_de.setdefault(u["linea"], set()).add(h["nivel"])
    for clave, esperado, _ in CASOS:
        obtenido = nivel_de.get(donde[clave], set())
        if esperado == "[INF]":
            print(f"[INF] {clave}: obtenido {sorted(obtenido) or 'nada'}")
            continue
        comprobar(f"{clave}: esperado {esperado}", obtenido == set(esperado.split("+")), f"obtenido {sorted(obtenido) or 'nada'}")

    # 2. corpus real: el mismo informe que en la QA r01
    real = vi.verificar(RAIZ)
    errores = sorted({h["id"] for h in real["hallazgos"] if h["nivel"] == "ERROR"})
    infos = sorted((h["id"], h["codigo"], len(h["ubicaciones"])) for h in real["hallazgos"] if h["nivel"] == "INFO")
    comprobar("corpus real: 2 errores (FX-MC10-003, RF-0123)", errores == ["FX-MC10-003", "RF-0123"], str(errores))
    simb = [i for i in infos if i[0] == X]
    comprobar(f"corpus real: {X} solo en INFO (CITA_EN_CONTEXTO_AJENO)", bool(simb) and X not in errores, str(simb))

    # 3. H-04 y H-05
    d = tmp / "salidas"
    d.mkdir()
    a, b, enl = d / "a.json", d / "b.md", d / "enlace.md"
    a.write_text("VIEJO", encoding="utf-8")
    enl.symlink_to(a)
    rc = lanzar("--json", str(a), "--md", str(enl))
    comprobar("H-04: --md es un enlace simbólico al --json → salida 2 y nada escrito",
              rc == 2 and a.read_text(encoding="utf-8") == "VIEJO" and not list(d.glob(".*.tmp")), f"rc={rc}")
    enl.unlink()
    os.link(a, b)
    rc = lanzar("--json", str(a), "--md", str(b))
    comprobar("H-04: --md es un enlace duro del --json → cada uno con su informe",
              rc == 1 and a.read_text(encoding="utf-8").startswith("{") and b.read_text(encoding="utf-8").startswith("#"),
              f"rc={rc}")
    os.chmod(a, 0o444)
    rc = lanzar("--json", str(a))
    comprobar("H-05: un destino de solo lectura (0444) se regenera y sigue en 0444",
              rc == 1 and (a.stat().st_mode & 0o777) == 0o444, f"rc={rc}, modo={oct(a.stat().st_mode & 0o777)}")
    rc = lanzar("--json", str(d / "nuevo.json"))
    m = (d / "nuevo.json").stat().st_mode & 0o777
    um = os.umask(0)
    os.umask(um)
    comprobar("H-05: un destino nuevo nace con la umask", rc == 1 and m == 0o666 & ~um, f"modo={oct(m)}")

comprobar("el corpus del repositorio no cambia", huellas() == antes)
malos = [q for q, ok in resultados if not ok]
print(f"\n{len(resultados) - len(malos)}/{len(resultados)} bien. Fallan: {malos if malos else 'ninguna'}")
sys.exit(1 if malos else 0)
