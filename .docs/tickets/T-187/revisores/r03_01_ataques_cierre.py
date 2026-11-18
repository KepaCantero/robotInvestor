"""QA de la ronda de cierre de T-187: ataques a las correcciones de H-08 (allowlist) y H-09 (cita de al menos
`MIN_PALABRAS_CITA` palabras y cita a la vista en el informe).

Uso, desde la raíz del repositorio con el Python del .venv:
    python .docs/tickets/T-187/revisores/r03_01_ataques_cierre.py
Sale con 1 si algún caso no da lo esperado.
"""
import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TICKET = Path(__file__).resolve().parents[1]
RAIZ = TICKET.parents[2]
spec = importlib.util.spec_from_file_location("revision_prompts_pb51", RAIZ / ".docs" / "scripts" / "revision_prompts_pb51.py")
assert spec and spec.loader
rp = importlib.util.module_from_spec(spec)
sys.modules["revision_prompts_pb51"] = rp
spec.loader.exec_module(rp)


def _cita(d: Path, i: str, cita, dudosa: bool = False) -> None:
    c = json.loads((d / "comentario.json").read_text(encoding="utf-8"))
    (c["dudosas_cita_nota"] if dudosa else c["erratas"][i]).__setitem__(i if dudosa else "cita_nota", cita)
    (d / "comentario.json").write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")


NOTA_1907 = "se publicó en Journal of Computational Finance 20(4), 2017"
CASOS = {
    # nombre: (esperado, id, cita, dudosa). 1 = pasa la validación pero --comprobar ve el cambio (la cita está en el informe).
    "dos_palabras_errata": (2, "AF-AG-19-07", "Journal of", False),
    "tres_signos_y_una_palabra": (2, "AF-AG-19-07", "— , Journal", False),
    "tres_palabras_literales_otra_cita": (1, "AF-AG-19-07", "Journal of Computational", False),
    "dos_palabras_dudosa": (2, "AF-AG-13-09", "mejor citar", True),
    "tres_palabras_dudosa_otra_cita": (1, "AF-AG-13-09", "mejor citar 2004", True),
    "cita_original_errata": (0, "AF-AG-19-07", NOTA_1907, False),
    "cita_no_literal_de_tres_palabras": (2, "AF-AG-19-07", "publicado en 2018", False),
}


def main() -> int:
    malos = 0
    for nombre, (esperado, i, cita, dudosa) in CASOS.items():
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "veredictos"
            shutil.copytree(TICKET / "veredictos", d)
            _cita(d, i, cita, dudosa)
            try:
                with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                    rc = rp.principal(["--raiz", str(RAIZ), "--salida", str(TICKET), "--veredictos", str(d), "--comprobar"])
                res = f"salida {rc}"
            except BaseException as e:   # noqa: BLE001 - una traza cuenta como fallo
                rc, res = None, f"traza {type(e).__name__}"
            ok = rc == esperado
            malos += not ok
            print(f"{'OK   ' if ok else 'FALLO'} {nombre} (espera {esperado}): {res}")
    # H-08: ninguna ruta de T-187 en la allowlist y refs-vivas en verde
    allow = (RAIZ / "tools" / "refs_allowlist.txt").read_text(encoding="utf-8")
    ok = "T-187" not in allow
    malos += not ok
    print(f"{'OK   ' if ok else 'FALLO'} allowlist_sin_T-187")
    r = subprocess.run([sys.executable, str(RAIZ / "tools" / "refs_vivas.py")], capture_output=True, text=True, check=False)
    malos += r.returncode != 0
    print(f"{'OK   ' if r.returncode == 0 else 'FALLO'} refs_vivas (salida {r.returncode})")
    print(f"{len(CASOS) + 2 - malos} de {len(CASOS) + 2} casos como se espera")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
