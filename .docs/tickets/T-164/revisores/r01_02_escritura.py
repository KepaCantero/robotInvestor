"""QA r01 de T-164 · ataques a la escritura en grupo (H-11) con `main` en el mismo proceso y fallos simulados.

Los destinos ya existen con un contenido «VIEJO» (el caso real: se regenera el informe), y se comprueba que un fallo deja ese
contenido intacto, salida 2 y ningún temporal. Casos: disco lleno en el último temporal (la auditoría), permiso denegado en el
primero, destino cuya «carpeta» es un fichero, temporal abandonado que es una carpeta, el mismo destino dos veces, y el límite
declarado (un renombrado que falla a mitad). Sale 1 si algo no se cumple; el último caso solo informa.

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-164/revisores/r01_02_escritura.py
"""
import contextlib
import errno
import io
import os
import sys
import tempfile
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
RAIZ = EJ.parent
from bloque_a.herramientas import verificador_ids as vi

resultados: list[tuple[str, bool]] = []
ESCRIBIR, REEMPLAZAR = Path.write_text, os.replace


def comprobar(que: str, ok: bool, detalle: str = "") -> None:
    resultados.append((que, ok))
    print(f"[{'OK ' if ok else 'MAL'}] {que}" + (f" · {detalle}" if detalle else ""))


def preparar(d: Path) -> tuple[Path, Path, Path, dict[Path, str]]:
    d.mkdir()
    js, md, aud = d / "i.json", d / "i.md", d / "aud.md"
    viejo = {js: "VIEJO json", md: "VIEJO md", aud: f"# A\n\n{vi.MARCA_INICIO}\nVIEJO\n{vi.MARCA_FIN}\n"}
    for p, t in viejo.items():
        ESCRIBIR(p, t, encoding="utf-8")
    return js, md, aud, viejo


def lanzar(*args: str) -> tuple[int, str]:
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        rc = vi.main(["--raiz", str(RAIZ), *args])
    return rc, err.getvalue()


def intacto(d: Path, viejo: dict[Path, str]) -> tuple[bool, str]:
    cambiados = [p.name for p, t in viejo.items() if p.read_text(encoding="utf-8") != t]
    tmps = [p.name for p in d.iterdir() if p.name.endswith(".tmp")]
    return not cambiados and not tmps, f"cambiados={cambiados}, temporales={tmps}"


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    # 1. disco lleno en el último temporal (la auditoría)
    js, md, aud, viejo = preparar(tmp / "lleno")
    def lleno(self, *a, **k):
        if self.name == ".aud.md.tmp":
            ESCRIBIR(self, "a medi", encoding="utf-8")
            raise OSError(errno.ENOSPC, "No queda espacio en el dispositivo")
        return ESCRIBIR(self, *a, **k)
    Path.write_text = lleno
    rc, err = lanzar("--json", str(js), "--md", str(md), "--auditoria", str(aud))
    Path.write_text = ESCRIBIR
    ok, det = intacto(tmp / "lleno", viejo)
    comprobar("disco lleno en el temporal de la auditoría → salida 2, JSON/MD/auditoría viejos, sin temporales",
              rc == 2 and ok and "no se puede escribir" in err, f"rc={rc}, {det}")

    # 2. permiso denegado en el primer temporal
    js, md, aud, viejo = preparar(tmp / "permiso")
    def sin_permiso(self, *a, **k):
        if self.name == ".i.json.tmp":
            raise PermissionError(errno.EACCES, "Permiso denegado")
        return ESCRIBIR(self, *a, **k)
    Path.write_text = sin_permiso
    rc, err = lanzar("--json", str(js), "--md", str(md), "--auditoria", str(aud))
    Path.write_text = ESCRIBIR
    ok, det = intacto(tmp / "permiso", viejo)
    comprobar("permiso denegado en el primer temporal → salida 2 y todo intacto", rc == 2 and ok, f"rc={rc}, {det}")

    # 3. la «carpeta» del destino es un fichero
    js, md, aud, viejo = preparar(tmp / "fichero")
    rc, err = lanzar("--json", str(js), "--md", str(tmp / "fichero" / "i.json" / "x.md"), "--auditoria", str(aud))
    ok, det = intacto(tmp / "fichero", viejo)
    comprobar("destino dentro de un fichero (i.json/x.md) → salida 2 (FALLO CERRADO) y todo intacto",
              rc == 2 and ok and "FALLO CERRADO" in err, f"rc={rc}, {det}")

    # 4. un temporal abandonado que es una carpeta
    js, md, aud, viejo = preparar(tmp / "tmpdir")
    (tmp / "tmpdir" / ".i.md.tmp").mkdir()
    rc, err = lanzar("--json", str(js), "--md", str(md), "--auditoria", str(aud))
    cambiados = [p.name for p, t in viejo.items() if p.read_text(encoding="utf-8") != t]
    comprobar("temporal abandonado que es una carpeta → salida 2, nada cambiado, sin .i.json.tmp/.aud.md.tmp",
              rc == 2 and not cambiados and not (tmp / "tmpdir" / ".i.json.tmp").exists()
              and not (tmp / "tmpdir" / ".aud.md.tmp").exists(), f"rc={rc}, cambiados={cambiados}")
    os.rmdir(tmp / "tmpdir" / ".i.md.tmp")

    # 5. el mismo destino dos veces (--json X --md X)
    js, md, aud, viejo = preparar(tmp / "doble")
    rc, err = lanzar("--json", str(js), "--md", str(js))
    contenido = js.read_text(encoding="utf-8")
    tmps = [p.name for p in (tmp / "doble").iterdir() if p.name.endswith(".tmp")]
    comprobar("el mismo destino dos veces → o salida 2 con el destino intacto, o salida 1 con un informe completo",
              (rc == 2 and contenido == "VIEJO json") or (rc in (0, 1) and contenido.startswith(("{", "#"))) and not tmps,
              f"rc={rc}, destino={'VIEJO' if contenido == 'VIEJO json' else contenido[:12]!r}, temporales={tmps}, "
              f"stderr={err.strip()[:90]!r}")

    # 6. límite declarado: el segundo renombrado falla
    js, md, aud, viejo = preparar(tmp / "limite")
    n = {"i": 0}
    def segundo_falla(a, b):
        n["i"] += 1
        if n["i"] == 2:
            raise OSError(errno.EXDEV, "otro dispositivo")
        return REEMPLAZAR(a, b)
    vi.os.replace = segundo_falla
    rc, err = lanzar("--json", str(js), "--md", str(md), "--auditoria", str(aud))
    vi.os.replace = REEMPLAZAR
    cambiados = sorted(p.name for p, t in viejo.items() if p.read_text(encoding="utf-8") != t)
    tmps = [p.name for p in (tmp / "limite").iterdir() if p.name.endswith(".tmp")]
    print(f"[INF] límite declarado (2.º renombrado falla): rc={rc}, cambiados={cambiados}, temporales={tmps}")
    comprobar("límite declarado: salida 2, solo el primero renombrado, sin temporales",
              rc == 2 and cambiados == ["i.json"] and not tmps)

    # 7. permisos: el destino conserva su modo
    js, md, aud, viejo = preparar(tmp / "modo")
    os.chmod(js, 0o640)
    rc, _ = lanzar("--json", str(js))
    print(f"[INF] modo del JSON antes 0o640, después {oct(js.stat().st_mode & 0o777)} (rc={rc})")

malos = [q for q, ok in resultados if not ok]
print(f"\n{len(resultados) - len(malos)}/{len(resultados)} bien. Fallan: {malos if malos else 'ninguna'}")
sys.exit(1 if malos else 0)
