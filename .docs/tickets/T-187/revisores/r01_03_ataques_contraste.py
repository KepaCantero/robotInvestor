"""QA r01 de T-187: ataques al paso 3 (lectura y validación de los veredictos) de `revision_prompts_pb51.py`.

QA r02: el script se movió a `.docs/scripts/` (H-06); se carga de ahí, por encargo del coordinador. Los casos no cambian.

Uso, desde la raíz del repositorio con el Python del .venv:
    python .docs/tickets/T-187/revisores/r01_03_ataques_contraste.py
Cada caso copia los veredictos reales a una carpeta temporal, los estropea y llama a `principal --comprobar` con
`--veredictos` ahí. Se espera la salida 2 (fallo cerrado, sin traza). Imprime OK o FALLO por caso; sale con 1 si alguno falla.
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
SCRIPT = TICKET.parents[1] / "scripts" / "revision_prompts_pb51.py"   # QA r02: antes, TICKET / "revision_prompts_pb51.py"
RAIZ = TICKET.parents[2]
spec = importlib.util.spec_from_file_location("revision_prompts_pb51", SCRIPT)
assert spec and spec.loader
rp = importlib.util.module_from_spec(spec)
sys.modules["revision_prompts_pb51"] = rp
spec.loader.exec_module(rp)


def _lote(d: Path, n: int) -> dict:
    return json.loads((d / f"lote_{n}.json").read_text(encoding="utf-8"))


def _guardar(d: Path, nombre: str, obj) -> None:
    (d / nombre).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def caso_discutible_no_hashable(d):
    c = json.loads((d / "comentario.json").read_text(encoding="utf-8")); c["discutibles"] = [["AF-AG-22-03"]]
    _guardar(d, "comentario.json", c)


def caso_lote_utf8_invalido(d):
    (d / "lote_4.json").write_bytes((d / "lote_4.json").read_bytes()[:-3] + b"\xff\xfe}")


def caso_comentario_utf8_invalido(d):
    (d / "comentario.json").write_bytes(b"\xff" + (d / "comentario.json").read_bytes())


def caso_lote_es_carpeta(d):
    (d / "lote_9.json").mkdir()


def caso_revisor_vacio(d):
    lt = _lote(d, 1); lt["revisor"] = "  "; _guardar(d, "lote_1.json", lt)


def caso_dudosa_sin_matiz(d):
    c = json.loads((d / "comentario.json").read_text(encoding="utf-8")); c["dudosas"]["AF-AG-13-09"] = ""
    _guardar(d, "comentario.json", c)


def caso_nota_solo_signos(d):
    lt = _lote(d, 2); lt["veredictos"][0]["nota"] = "—"; _guardar(d, "lote_2.json", lt)


def caso_veredicto_lista(d):
    lt = _lote(d, 3); lt["veredictos"][0]["veredicto"] = ["CORRECTA"]; _guardar(d, "lote_3.json", lt)


def caso_lote_duplicado_con_otro_nombre(d):
    shutil.copy(d / "lote_4.json", d / "lote_4 (copia).json")


def caso_nfd_en_id(d):
    lt = _lote(d, 1); lt["veredictos"][0]["id"] = lt["veredictos"][0]["id"] + "́"; _guardar(d, "lote_1.json", lt)


CASOS = [caso_discutible_no_hashable, caso_lote_utf8_invalido, caso_comentario_utf8_invalido, caso_lote_es_carpeta,
         caso_revisor_vacio, caso_dudosa_sin_matiz, caso_nota_solo_signos, caso_veredicto_lista,
         caso_lote_duplicado_con_otro_nombre, caso_nfd_en_id]


def main() -> int:
    malos = 0
    for caso in CASOS:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "veredictos"
            shutil.copytree(TICKET / "veredictos", d)
            caso(d)
            err = io.StringIO()
            try:
                with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                    rc = rp.principal(["--raiz", str(RAIZ), "--salida", str(TICKET), "--veredictos", str(d), "--comprobar"])
                res = f"salida {rc}"
            except BaseException as e:   # noqa: BLE001 - se informa la traza como fallo
                rc, res = None, f"traza {type(e).__name__}: {str(e)[:80]}"
            ok = rc == 2
            malos += not ok
            print(f"{'OK   ' if ok else 'FALLO'} {caso.__name__}: {res}")
    print(f"{len(CASOS) - malos} de {len(CASOS)} casos fallan cerrado")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
