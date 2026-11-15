"""QA r01 de T-131 · ¿el borrador de la corrección del Anexo B refleja todo `divergencias_anexo_b.json`?

Recorre el golden y busca cada dato en el borrador generado:
 1. cada clave de `por_contrato` (contrato.parte) tiene al menos una fila; cada subclave y cada campo que nombra aparece en
    la fila de su contrato (incluida `el_ejecutor_rechaza_el_ejemplo_del_anexo_b`, con su motivo);
 2. cada mensaje de `mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b`: los que no son «required property» o son
    de la raíz, ¿dónde quedan?;
 3. cada valor de `valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro` y los contratos sin campos;
 4. `--comprobar` coincide y el script no escribe nada con él.
Uso (desde la raíz): python -I r01_02_fidelidad_borrador.py
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("ba", RAIZ / ".docs" / "scripts" / "borrador_anexo_b.py")
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)
d = json.loads(ba.DIVERGENCIAS.read_text(encoding="utf-8"))
texto = ba.generar()
filas = [x for x in texto.splitlines() if x.startswith("| CT-")]
OK, FALLOS = 0, []


def comprobar(cond, msg):
    global OK
    OK += cond
    if not cond:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg}")


def filas_de(clave):
    return [f for f in filas if f.startswith(f"| {clave} |")]


print("1. por_contrato")
sin_fila, sin_dato = [], []
for clave, v in d["por_contrato"].items():
    fs = filas_de(clave)
    if not fs:
        sin_fila.append(clave)
    for sub, valor in v.items():
        for x in (valor if isinstance(valor, list) else [valor]):
            # un campo se busca por su nombre; un motivo (texto) por sus primeras palabras
            aguja = x if isinstance(x, str) and len(x) < 60 else str(x)[:40]
            if not any(aguja in f for f in fs):
                sin_dato.append(f"{clave} · {sub} · {str(x)[:90]}")
comprobar(not sin_fila, f"{len(d['por_contrato'])} contratos con diferencias, todos con fila (sin fila: {sin_fila})")
comprobar(not sin_dato, f"cada dato de por_contrato en su fila ({len(sin_dato)} sin reflejar)")
for x in sin_dato[:15]:
    print("        ·", x)

print("2. mensajes de los flujos")
no_req = [(k, m) for k, ms in d["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"].items() for m in ms
          if "required property" not in m or "(raíz)" in m]
total = sum(len(ms) for ms in d["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"].values())
print(f"     {total} mensajes; {len(no_req)} no son «required property» o son de la raíz y el generador los descarta:")
for k, m in no_req[:12]:
    print(f"        · {k}: {m[:110]}")
cubiertos = []
for k, m in no_req:
    campo = m.split("'")[1] if "'" in m else m
    cubiertos.append(any(campo in f for f in filas_de(k)) or campo in texto)
comprobar(all(cubiertos), f"los descartados están dichos de otra forma en el borrador ({sum(cubiertos)}/{len(no_req)})")
malas = []
for k, ms in d["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"].items():
    for m in ms:
        if "required property" in m and "(raíz)" not in m:
            r = ba._ruta(m)
            if r.startswith(".") or ".." in r or "/" in r:
                malas.append((m, r))
comprobar(not malas, f"rutas traducidas de jsonschema bien formadas ({malas[:3]})")

print("3. otro campo y contratos sin campos")
oc = d["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"]
falt = [(k, x["valor"]) for k, xs in oc.items() for x in xs if not any(x["valor"] in f for f in filas_de(k))]
comprobar(not falt, f"valores en otro campo, todos en su fila ({falt})")
comprobar(all(c in texto for c in d["contratos_sin_campos_en_el_anexo_b"]), "contratos sin campos en el §3")

print("4. --comprobar")
antes = ba.SALIDA.stat().st_mtime_ns
p = subprocess.run([sys.executable, str(RAIZ / ".docs" / "scripts" / "borrador_anexo_b.py"), "--comprobar"], capture_output=True)
comprobar(p.returncode == 0 and ba.SALIDA.stat().st_mtime_ns == antes, f"--comprobar coincide (código {p.returncode}) sin escribir")
comprobar("is a required property" not in texto, "sin mensajes de jsonschema sin traducir")
print(f"\nr01_02 T-131: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
