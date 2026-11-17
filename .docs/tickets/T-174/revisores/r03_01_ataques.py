"""QA r03 de T-174 (revisor independiente): el conjunto en memoria de revisiones en marcha (H-07) con varios Bloque en el
mismo proceso, y tras un fork.

Uso (desde la copia):  cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-174/revisores/r03_01_ataques.py"""
import os
import sys
import threading
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor" / "tests"
sys.path.insert(0, str(TESTS))
from conftest import AS_OF, nuevo_bloque, universo  # noqa: E402,F401

P = {"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen"}


def _entregado(tmp, universo):
    b = nuevo_bloque(tmp, universo)
    cns = b.consultas.enviar({"tipo": "OTRA", "modo": "NO_BLOQUEANTE", "preguntas": [dict(P)]}, AS_OF)["cns_id"]
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    return b, cns


def _avisos(b, cns):
    return [i for i in b.almacen.leer("HA") if "sin proceso que la ejecute" in str(i) and cns in str(i)]


def _huerfana(b, cns):
    """Revisión EN_CURSO de este proceso que ya no se ejecuta (el ciclo murió con una BaseException)."""
    orig = b.ciclo

    def muere(*a, **k):
        raise KeyboardInterrupt
    b.ciclo = muere
    with pytest.raises(KeyboardInterrupt):
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    b.ciclo = orig


# C1 · Mismo proceso, misma carpeta: otra instancia mira huérfanas justo entre la reserva EN_CURSO (bajo el cerrojo) y el alta
# en el conjunto en marcha (al entrar en _ejecutar_revision). La revisión está viva: no debe marcarse huérfana
def test_c1_ventana_entre_reserva_y_en_marcha(tmp_path, universo):
    b, cns = _entregado(tmp_path, universo)
    b2 = nuevo_bloque(tmp_path, universo)
    reservada, seguir = threading.Event(), threading.Event()
    orig = b.consultas._ejecutar_revision

    def tarde(*a, **k):   # ensancha la ventana que ya existe entre soltar el cerrojo y el alta en _EN_MARCHA
        reservada.set()
        seguir.wait(60)
        return orig(*a, **k)
    b.consultas._ejecutar_revision = tarde
    h = threading.Thread(target=lambda: b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF))
    h.start()
    reservada.wait(60)
    vistas = b2.consultas.huerfanas()
    seguir.set()
    h.join(900)
    print("huérfanas vistas con la revisión viva:", [(x["cns_id"], x["estado"]) for x in vistas], "| avisos:", len(_avisos(b, cns)))
    assert vistas == [] and _avisos(b, cns) == [], "falso huérfano: aviso escalado de una revisión viva (y el operador la relanzaría)"


# C2 · Mismo proceso, dos carpetas de estado distintas con los mismos ids (CNS-2026-0001, MSG-…): una huérfana en X no debe
# quedar oculta porque Y esté ejecutando la revisión con la misma clave
def test_c2_dos_carpetas_con_los_mismos_ids(tmp_path, universo):
    bx, cx = _entregado(tmp_path / "x", universo)
    by, cy = _entregado(tmp_path / "y", universo)
    _huerfana(bx, cx)
    mx = bx.consultas._todas()[cx]["revisiones_c2"][-1]["msg_id"]
    empezado, seguir = threading.Event(), threading.Event()
    orig = by.ciclo

    def lento(*a, **k):
        empezado.set()
        seguir.wait(120)
        return orig(*a, **k)
    by.ciclo = lento
    h = threading.Thread(target=lambda: by.consultas.responder(cy, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF))
    h.start()
    empezado.wait(120)
    my = by.consultas._todas()[cy]["revisiones_c2"][-1]["msg_id"]
    vistas = bx.consultas.huerfanas()
    seguir.set()
    h.join(900)
    print("claves X/Y:", (cx, mx), (cy, my), "| huérfanas de X vistas mientras Y corre:", len(vistas))
    assert vistas, "falso vivo: la huérfana de X se da por viva porque Y ejecuta una revisión con la misma (cns_id, msg_id)"


# C3 · Fork: el hijo hereda el conjunto en marcha del padre, pero su pid es otro; una huérfana del padre (pid vivo) no la
# marca el hijo (no puede saberlo); la marca el padre. Y una revisión que el padre tiene viva no la ve huérfana el hijo
@pytest.mark.skipif(not hasattr(os, "fork"), reason="sin fork")
def test_c3_fork(tmp_path, universo):
    b, cns = _entregado(tmp_path, universo)
    _huerfana(b, cns)
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:   # hijo
        try:
            n = len(nuevo_bloque(tmp_path, universo).consultas.huerfanas())
        except BaseException:  # noqa: BLE001
            n = -1
        os.write(w, str(n).encode())
        os._exit(0)
    os.waitpid(pid, 0)
    n_hijo = int(os.read(r, 16).decode())
    n_padre = len(b.consultas.huerfanas())
    print("huérfanas vistas por el hijo:", n_hijo, "| por el padre:", n_padre, "| avisos:", len(_avisos(b, cns)))
    assert n_hijo == 0 and n_padre == 1 and len(_avisos(b, cns)) == 1
