"""Estado de la cola de Astra (`.docs/tickets/_relevo/cola_astra.md`) contrastado con el repositorio.

Dice cuál es la siguiente tarea y detecta lo que se podría perder:
- ERROR: una tarea marcada HECHA cuyo entregable no está (o es un borrador, o sin el veredicto rellenado);
- AVISO: un entregable que ya está pero cuya tarea no se marcó HECHA; una tarea EN CURSO de hace más de 3 días;
  más de una EN CURSO; entregables con cambios sin commit (trabajo sin subir); una fila con estado desconocido.

Cuándo cuenta un entregable como hecho:
- REVISION: el fichero existe, está en git, no empieza por «BORRADOR» y, si la fila lo pide, contiene su sección;
- QA: `qa.md` cambió en un commit desde la fecha de la cola y su último veredicto está rellenado (APTO o NO APTO);
- IMPLEMENTAR: el README del ticket cambió desde la fecha de la cola y su estado es EN QA o CERRADO.

Uso: python3 .docs/scripts/cola_astra.py [--json]. Devuelve 1 si hay algún ERROR. Solo biblioteca estándar.
"""
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
COLA = RAIZ / ".docs/tickets/_relevo/cola_astra.md"
FECHA_COLA = "2026-11-12"   # lo que cambió antes no cuenta como hecho para QA e IMPLEMENTAR
DIAS_EN_CURSO = 3
REQUISITOS = {"C-02": "Rediseño"}   # la revisión de B lleva una sección para el rediseño (encargo de bloque_b)
ESTADOS = re.compile(r"^(PENDIENTE|HECHA|BLOQUEADA|EN CURSO( \d{4}-\d{2}-\d{2})?)$")


def git(*args):
    r = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, text=True, check=False)
    return r.stdout.strip() if r.returncode == 0 else ""


def filas():
    out = []
    for linea in COLA.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| C-\d{2} \|", linea):
            continue
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if len(c) != 8:
            out.append({"id": c[0], "error_forma": f"la fila tiene {len(c)} columnas y no 8"})
            continue
        ruta = re.findall(r"`([^`]+)`|«([^»]+)»", c[4])   # «…» para lo que aún no existe (el gate refs-vivas no lo exige)
        ruta = [x or y for x, y in ruta]
        out.append({"id": c[0], "tarea": c[1], "tipo": c[2], "entregable": ruta[0] if ruta else "", "estado": c[5],
                    "commit": c[6], "nota": c[7]})
    return out


def _ultimo_veredicto(texto):
    trozos = re.split(r"^#+ .*Veredicto.*$", texto, flags=re.MULTILINE)
    if len(trozos) < 2:
        return None
    m = re.search(r"\*\*(NO APTO|APTO)\*\*", trozos[-1])
    return m.group(1) if m and "APTO / NO APTO" not in trozos[-1][:200] else None


def evidencia(f):
    """(hecha, motivo, commit): si el entregable de la fila cuenta como hecho, por qué no, y el último commit que lo tocó."""
    p = RAIZ / f["entregable"]
    if not f["entregable"] or not p.exists():
        return False, "el entregable no existe", ""
    if not git("ls-files", "--error-unmatch", f["entregable"]):
        return False, "el entregable no está en git", ""
    commit = git("log", "-1", "--format=%h", "--", f["entregable"])
    fecha = git("log", "-1", "--format=%cs", "--", f["entregable"])
    texto = p.read_text(encoding="utf-8", errors="replace")
    if f["tipo"] == "REVISION":
        if texto.lstrip().upper().startswith("BORRADOR"):
            return False, "el entregable es un borrador", commit
        req = REQUISITOS.get(f["id"])
        if req and req not in texto:
            return False, f"falta la sección «{req}»", commit
        return True, "", commit
    if fecha and fecha < FECHA_COLA:
        return False, f"el entregable no ha cambiado desde la cola ({fecha})", commit
    if f["tipo"] == "QA":
        v = _ultimo_veredicto(texto)
        return (True, "", commit) if v else (False, "sin veredicto rellenado", commit)
    if f["tipo"] == "IMPLEMENTAR":
        m = re.search(r"^\| Estado \| ([^|]+)\|", texto, re.MULTILINE)
        est = m.group(1).strip() if m else ""
        return (True, "", commit) if est.startswith(("EN QA", "CERRADO")) else (False, f"estado del ticket «{est or '?'}»", commit)
    return False, f"tipo desconocido «{f['tipo']}»", commit


def main():
    hoy = date.today()
    errores, avisos, resumen = [], [], []
    rows = filas()
    st = subprocess.run(["git", "-C", str(RAIZ), "status", "--porcelain"], capture_output=True, text=True, check=False).stdout
    sin_subir = {l[3:] for l in st.splitlines() if len(l) > 3}   # sin recortar: la primera columna puede ser un espacio
    en_curso = []
    for f in rows:
        if "error_forma" in f:
            errores.append(f"{f['id']}: {f['error_forma']}")
            continue
        if not ESTADOS.match(f["estado"]):
            avisos.append(f"{f['id']}: estado desconocido «{f['estado']}»")
        hecha, motivo, commit = evidencia(f)
        f["evidencia"], f["motivo"], f["commit_encontrado"] = hecha, motivo, commit
        if f["estado"] == "HECHA" and not hecha:
            errores.append(f"{f['id']} ({f['tarea']}): marcada HECHA pero {motivo}")
        if hecha and f["estado"] != "HECHA":
            avisos.append(f"{f['id']} ({f['tarea']}): el entregable ya está ({commit}) pero la tarea no está marcada HECHA")
        if f["estado"].startswith("EN CURSO"):
            en_curso.append(f["id"])
            m = re.search(r"\d{4}-\d{2}-\d{2}", f["estado"])
            if not m:
                avisos.append(f"{f['id']}: EN CURSO sin fecha")
            elif date.fromisoformat(m.group(0)) < hoy - timedelta(days=DIAS_EN_CURSO):
                avisos.append(f"{f['id']} ({f['tarea']}): EN CURSO desde {m.group(0)}; ¿trabajo abandonado? Nota: {f['nota'] or '—'}")
        if f["entregable"] in sin_subir:
            avisos.append(f"{f['id']}: el entregable tiene cambios sin commit (trabajo sin subir)")
        resumen.append(f)
    if len(en_curso) > 1:
        avisos.append(f"hay {len(en_curso)} tareas EN CURSO a la vez: {', '.join(en_curso)}")
    siguiente = next((f for f in resumen if f["estado"].startswith("EN CURSO")), None) or \
        next((f for f in resumen if f["estado"] == "PENDIENTE"), None)
    cuenta = {e: sum(1 for f in resumen if f["estado"].startswith(e)) for e in ("HECHA", "EN CURSO", "PENDIENTE", "BLOQUEADA")}
    if "--json" in sys.argv:
        print(json.dumps({"cuenta": cuenta, "siguiente": siguiente and {k: siguiente[k] for k in ("id", "tarea", "entregable")},
                          "errores": errores, "avisos": avisos}, ensure_ascii=False, indent=1))
    else:
        print(f"Cola de Astra: {cuenta['HECHA']} hechas, {cuenta['EN CURSO']} en curso, {cuenta['PENDIENTE']} pendientes, "
              f"{cuenta['BLOQUEADA']} bloqueadas (de {len(resumen)})")
        print(f"Siguiente: {siguiente['id']} · {siguiente['tarea']} · entregable {siguiente['entregable']}" if siguiente else "Siguiente: nada pendiente")
        for e in errores:
            print("ERROR ", e)
        for a in avisos:
            print("AVISO ", a)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
