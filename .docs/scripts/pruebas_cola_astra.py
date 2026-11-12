"""Pruebas de `cola_astra.py` en una copia temporal del repositorio (git worktree), sin tocar el árbol de trabajo ni subir nada.

Uso: python3 .docs/scripts/pruebas_cola_astra.py. Devuelve 1 si alguna falla.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
COLA = ".docs/tickets/_relevo/cola_astra.md"
ok = True


def sh(cwd, *args):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, check=False)


def chk(nombre, cond, detalle=""):
    global ok
    print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)
    ok &= bool(cond)


def poner_estado(w, fila, estado):
    p = w / COLA
    s = p.read_text(encoding="utf-8")
    lineas = []
    for l in s.splitlines():
        if l.startswith(f"| {fila} |"):
            c = l.split("|")
            c[6] = f" {estado} "
            l = "|".join(c)
        lineas.append(l)
    p.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def commit(w, msg):
    sh(w, "git", "add", "-A")
    sh(w, "git", "-c", "user.name=prueba", "-c", "user.email=prueba@example.invalid", "commit", "-q", "-m", msg)


def correr(w):
    shutil.copy(RAIZ / ".docs/scripts/cola_astra.py", w / ".docs/scripts/cola_astra.py")
    r = sh(w, sys.executable, "-I", ".docs/scripts/cola_astra.py")
    return r.returncode, r.stdout


def main():
    base = Path(tempfile.mkdtemp(prefix="cola_astra_"))
    w = base / "copia"
    if sh(RAIZ, "git", "worktree", "add", "--detach", "-q", str(w), "HEAD").returncode:
        print("no se pudo crear la copia")
        return 1
    try:
        shutil.copy(RAIZ / COLA, w / COLA)   # la cola del árbol de trabajo, aunque aún no tenga commit
        commit(w, "cola")
        rc, out = correr(w)
        chk("cola_limpia_sin_errores_y_C01_siguiente", rc == 0 and "Siguiente: C-01" in out and "ERROR" not in out, out)

        poner_estado(w, "C-01", "HECHA"); commit(w, "marca sin entregable")
        rc, out = correr(w)
        chk("HECHA_sin_entregable_es_ERROR", rc == 1 and re.search(r"ERROR\s+C-01.*no existe", out), out)

        (w / ".docs/diseno/bloque_a/revision_astra.md").write_text("BORRADOR, sigue en la próxima sesión\n", encoding="utf-8")
        commit(w, "borrador")
        rc, out = correr(w)
        chk("HECHA_con_borrador_es_ERROR", rc == 1 and "borrador" in out, out)

        (w / ".docs/diseno/bloque_a/revision_astra.md").write_text("# Revisión de A\n\nResumen.\n", encoding="utf-8")
        commit(w, "revisión")
        rc, out = correr(w)
        chk("HECHA_con_entregable_sin_errores", rc == 0 and "1 hechas" in out and "Siguiente: C-02" in out, out)

        (w / ".docs/diseno/bloque_c/revision_astra.md").write_text("# Revisión de C\n", encoding="utf-8")
        commit(w, "revisión sin marcar")
        rc, out = correr(w)
        chk("entregable_sin_marcar_HECHA_es_AVISO", rc == 0 and re.search(r"AVISO\s+C-03.*no está marcada HECHA", out), out)

        (w / ".docs/tickets/T-68/revision_astra.md").write_text("# Revisión de T-68\n", encoding="utf-8")
        poner_estado(w, "C-02", "HECHA"); commit(w, "B sin rediseño")
        rc, out = correr(w)
        chk("B_sin_la_seccion_del_rediseno_es_ERROR", rc == 1 and "Rediseño" in out, out)
        poner_estado(w, "C-02", "PENDIENTE"); commit(w, "deshacer")

        poner_estado(w, "C-04", "EN CURSO 2026-01-01"); poner_estado(w, "C-05", "EN CURSO 2099-01-01"); commit(w, "en curso")
        rc, out = correr(w)
        chk("EN_CURSO_viejo_es_AVISO_y_es_la_siguiente", "AVISO  C-04" in out and "abandonado" in out and "Siguiente: C-04" in out, out)
        chk("dos_EN_CURSO_a_la_vez_es_AVISO", "2 tareas EN CURSO" in out, out)

        (w / ".docs/diseno/bloque_d/revision_astra.md").write_text("# a medias\n", encoding="utf-8")
        sh(w, "git", "add", ".docs/diseno/bloque_d/revision_astra.md")
        commit(w, "d")
        (w / ".docs/diseno/bloque_d/revision_astra.md").write_text("# a medias, más\n", encoding="utf-8")
        rc, out = correr(w)
        chk("cambios_sin_commit_en_un_entregable_es_AVISO", "C-04: el entregable tiene cambios sin commit" in out, out)

        poner_estado(w, "C-28", "HECHA"); commit(w, "QA vieja")
        rc, out = correr(w)
        chk("QA_marcada_con_un_qa_md_anterior_a_la_cola_es_ERROR", rc == 1 and re.search(r"ERROR\s+C-28.*no ha cambiado", out), out)

        poner_estado(w, "C-03", "RETIRADA"); commit(w, "retirada")
        rc, out = correr(w)
        chk("RETIRADA_con_entregable_no_avisa", "C-03" not in out.split("Siguiente:")[1], out)
        poner_estado(w, "C-01", "RETIRADA"); poner_estado(w, "C-02", "RETIRADA"); poner_estado(w, "C-04", "PENDIENTE")
        poner_estado(w, "C-05", "PENDIENTE"); commit(w, "retiradas")
        rc, out = correr(w)
        chk("RETIRADA_no_es_la_siguiente_y_se_cuenta", "Siguiente: C-04" in out and "retiradas" in out, out)

        poner_estado(w, "C-06", "LISTA"); commit(w, "estado raro")
        rc, out = correr(w)
        chk("estado_desconocido_es_AVISO", "C-06: estado desconocido" in out, out)
    finally:
        sh(RAIZ, "git", "worktree", "remove", "--force", str(w))
        shutil.rmtree(base, ignore_errors=True)
    print("RESULTADO PRUEBAS COLA ASTRA:", "TODAS PASAN" if ok else "HAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
