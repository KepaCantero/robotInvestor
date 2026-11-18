"""QA r02 de T-187: ataques a lo nuevo de la r02 en `.docs/scripts/revision_prompts_pb51.py` (cita_nota, criterio de
los dudosos, discutibles, sensibilidad y fuentes).

Uso, desde la raíz del repositorio con el Python del .venv:
    python .docs/tickets/T-187/revisores/r02_01_ataques_r02.py
Cada caso copia los veredictos reales a una carpeta temporal, los estropea y llama a `principal --comprobar` con
`--veredictos` ahí. Se espera la salida 2 (fallo cerrado, sin traza); el caso de control, 0. Sale con 1 si alguno falla.
"""
import contextlib
import importlib.util
import io
import json
import shutil
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


def _com(d: Path) -> dict:
    return json.loads((d / "comentario.json").read_text(encoding="utf-8"))


def _poner(d: Path, c: dict) -> None:
    (d / "comentario.json").write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")


def _lote(d: Path, n: int) -> dict:
    return json.loads((d / f"lote_{n}.json").read_text(encoding="utf-8"))


def _cambiar(d, f):
    c = _com(d); f(c); _poner(d, c)


CASOS = {
    # (esperado, función)
    "control_sin_cambios": (0, lambda d: None),
    "cita_inventada": (2, lambda d: _cambiar(d, lambda c: c["erratas"]["AF-AG-19-07"].update(cita_nota="no se publicó nunca"))),
    "cita_vacia": (2, lambda d: _cambiar(d, lambda c: c["erratas"]["AF-AG-19-07"].update(cita_nota=""))),
    "cita_de_otra_nota": (2, lambda d: _cambiar(d, lambda c: c["erratas"]["AF-AG-19-07"].update(
        cita_nota=c["erratas"]["AF-MC-01-05"]["cita_nota"]))),
    "cita_no_texto": (2, lambda d: _cambiar(d, lambda c: c["erratas"]["AF-AG-19-07"].update(cita_nota=["2017"]))),
    "cita_de_una_letra": (2, lambda d: _cambiar(d, lambda c: c["erratas"]["AF-AG-19-07"].update(cita_nota="a"))),
    "cita_de_una_palabra_vacia": (2, lambda d: _cambiar(d, lambda c: c["erratas"]["AF-AG-19-07"].update(cita_nota=" de "))),
    "dudosa_sin_cita": (2, lambda d: _cambiar(d, lambda c: c["dudosas_cita_nota"].pop("AF-MC-02-04"))),
    "dudosa_que_falta": (2, lambda d: _cambiar(d, lambda c: (c["dudosas"].pop("AF-MC-02-04"), c["dudosas_cita_nota"].pop("AF-MC-02-04")))),
    "dudosa_sin_matiz_en_la_nota": (2, lambda d: _cambiar(d, lambda c: (c["dudosas"].update({"AF-AG-21-07": "x y"}),
                                                                       c["dudosas_cita_nota"].update({"AF-AG-21-07": "Búsqueda web"})))),
    "discutible_sin_apoyo": (2, lambda d: _cambiar(d, lambda c: c["discutibles"].append("AF-AG-22-03"))),
    "sensibilidad_con_una_correcta": (2, lambda d: _cambiar(d, lambda c: c["sensibilidad"]["ids"].append("AF-AG-07-01"))),
    "sensibilidad_sin_motivo": (2, lambda d: _cambiar(d, lambda c: c["sensibilidad"].update(motivo=" — "))),
    "sensibilidad_no_lista": (2, lambda d: _cambiar(d, lambda c: c["sensibilidad"].update(ids="AF-AG-22-03"))),
    "sin_sensibilidad": (2, lambda d: _cambiar(d, lambda c: c.pop("sensibilidad"))),
    "dudosas_cita_no_dict": (2, lambda d: _cambiar(d, lambda c: c.update(dudosas_cita_nota=[]))),
}


def main() -> int:
    malos = 0
    for nombre, (esperado, f) in CASOS.items():
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "veredictos"
            shutil.copytree(TICKET / "veredictos", d)
            f(d)
            try:
                with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                    rc = rp.principal(["--raiz", str(RAIZ), "--salida", str(TICKET), "--veredictos", str(d), "--comprobar"])
                res = f"salida {rc}"
            except BaseException as e:   # noqa: BLE001 - una traza cuenta como fallo
                rc, res = None, f"traza {type(e).__name__}: {str(e)[:80]}"
            ok = rc == esperado
            malos += not ok
            print(f"{'OK   ' if ok else 'FALLO'} {nombre} (espera {esperado}): {res}")
    print(f"{len(CASOS) - malos} de {len(CASOS)} casos como se espera")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
