"""r03_02 · El sello tolerante a un corte (H-16, H-18) y la orden `sellar` del registro 0.3.0. ¿La tolerancia (sello una
anotación por detrás) o las dos excepciones nuevas sin sello (una sola anotación; idéntico a HEAD) permiten algo que la r02 no
permitía SIN tocar el sello? ¿Queda basura que se suba? Fuera de git (sin ancla), para que solo hable el sello.
Uso: .venv/bin/python -B r03_02_sello_tolerante.py <raíz>"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import (AHORA, DESPUES, RAIZ, borrar, caso, escribir_lineas, experimento_completo, fin, git, lanza,  # noqa: E402
                       lineas, pre, recadenar, repo_temporal, rx, subir, tmpdir)

tmps = []


def base():
    """Registro fuera de git: prerregistro y tres intentos con resultado (7 anotaciones)."""
    d = tmpdir(); tmps.append(d)
    reg = rx.Registro(d / "registro.jsonl")
    exp = experimento_completo(reg, "peor")
    experimento_completo(reg, "peor", "v1", exp=exp)
    experimento_completo(reg, "fallido", "v1", exp=exp)
    return reg, exp


def detecta(reg):
    e = lanza(reg.verificar, rx.RegistroError)
    return e is not None, (str(e)[:100] if e else f"verificar = {reg.verificar()}")


# 1. Manipulaciones SOLO del registro (el sello no se toca): todas menos anexar se detectan
reg, exp = base()
ls = lineas(reg.ruta)
objs = [json.loads(x) for x in ls]
cambiado = [*objs[:-1], {**objs[-1], "veredicto": "mejor"}]
cambiado2 = [*objs[:-2], {**objs[-2], "variante": "v9"}, objs[-1]]
manip = {
    "quitar la última": ls[:-1],
    "quitar las dos últimas": ls[:-2],
    "cambiar el veredicto de la última y recalcular su huella": recadenar(cambiado),
    "cambiar la penúltima y recalcular las dos": recadenar(cambiado2),
    "quitar la última y poner otra con el mismo número": recadenar([*objs[:-1], {**objs[-1], "detalle": {"x": 1}}]),
}
for nombre, nuevas in manip.items():
    escribir_lineas(reg.ruta, nuevas)
    ok, d = detecta(reg)
    caso(f"sello sin tocar · {nombre}: se detecta", ok, d)
escribir_lineas(reg.ruta, ls)
caso("(control) el registro original vuelve a leerse", lanza(reg.verificar) is None)

# anexar a mano una línea válida sin poner al día el sello: es lo que hace una escritura cortada, se admite
i = reg.intento(exp, "v1", ahora=DESPUES)
ls2 = lineas(reg.ruta)
sello_antes = reg.sello.read_text(encoding="utf-8")
extra = recadenar([*[json.loads(x) for x in ls2], {"tipo": "RESULTADO", "exp_id": exp, "n": i["n"], "veredicto": "mejor",
                                                     "detalle": {}, "registrado_en": DESPUES}])[-1]
escribir_lineas(reg.ruta, [*ls2, extra])
caso("(referencia) anexar a mano una anotación válida sin el sello: se admite como un corte",
     lanza(reg.verificar) is None, f"sello {sello_antes.strip()[:40]}…; anotaciones {len(ls2) + 1}")
escribir_lineas(reg.ruta, [*ls2, extra, recadenar([*[json.loads(x) for x in ls2], json.loads(extra),
                                                    {**json.loads(ls2[1]), "n": i["n"] + 1, "variante": "v1"}])[-1]])
ok, d = detecta(reg)
caso("(referencia) anexar dos a mano sin el sello: se rechaza (dos por detrás)", ok, d)

# 2. Un sello viejo restaurado (manipular el sello, límite declarado) + quitar la última: se admite
reg, exp = base()
ls = lineas(reg.ruta)
viejo = json.dumps({"seq": json.loads(ls[-3])["_seq"], "hash": json.loads(ls[-3])["_hash"]}) + "\n"
escribir_lineas(reg.ruta, ls[:-1]); reg.sello.write_text(viejo, encoding="utf-8")
ok, d = detecta(reg)
caso("(límite declarado: tocar el sello) sello de dos escrituras antes + quitar la última: se detecta", ok, d)

# 3. Corte de verdad entre la línea y el sello (el proceso muere en os.replace): se admite y la siguiente lo pone al día
repo = repo_temporal(); tmps.append(repo)
(repo / ".gitignore").write_bytes((RAIZ / ".gitignore").read_bytes())   # el .gitignore del proyecto
ruta = repo / ".docs" / "experimentos" / "registro_claude.jsonl"
reg = rx.Registro(ruta)
exp = experimento_completo(reg, "peor")
subir(repo, ruta, Path(str(ruta) + ".sello"))
codigo = f"""
import os, sys
sys.path.insert(0, {str(RAIZ / '.docs' / 'scripts')!r})
import registro_experimentos as rx
os.replace = lambda *a, **k: os._exit(9)
rx.Registro({str(ruta)!r}).intento({exp!r}, "v1", ahora={DESPUES!r})
"""
p = subprocess.run([sys.executable, "-I", "-c", codigo], capture_output=True, text=True)
e = lanza(reg.verificar)
caso("corte entre la línea y el sello (proceso muerto): el registro se sigue leyendo", p.returncode == 9 and e is None,
     f"código {p.returncode}; {e or reg.verificar()}")
tmp = Path(str(reg.sello) + ".tmp")
ignorado = subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", str(tmp)]).returncode == 0
estado = git(repo, "status", "--porcelain", "--untracked-files=all")
caso("tras el corte, el «.sello.tmp» que queda no se sube (ignorado por git) ni lo recoge un «git add -A»",
     not tmp.exists() or ignorado, f"existe {tmp.exists()}; ignorado {ignorado}; git status: {estado.replace(chr(10), ' | ')[:160]}")
n = reg.resultado(exp, 2, "peor", ahora=DESPUES)
caso("…y la escritura siguiente pone el sello al día", json.loads(reg.sello.read_text(encoding="utf-8"))["seq"] == n["_seq"])

# 4. os.replace del sello falla (sin morir): RegistroError, el registro sigue vivo (H-16)
reg, exp = base()
orig = os.replace
os.replace = lambda *a, **k: (_ for _ in ()).throw(OSError(28, "No queda espacio"))
try:
    e = lanza(lambda: reg.intento(exp, "v1", ahora=DESPUES))
finally:
    os.replace = orig
caso("si el sello no se puede poner al día, sale RegistroError y no otra excepción", isinstance(e, rx.RegistroError), repr(e)[:120])
caso("…y el registro sigue vivo (una por detrás)", lanza(reg.verificar) is None)
Path(str(reg.sello) + ".tmp").unlink(missing_ok=True); Path(str(reg.sello) + ".tmp").mkdir()   # el temporal no se puede escribir: no se escribe nada
antes = reg.ruta.read_bytes()
e = lanza(lambda: reg.resultado(exp, 4, "peor", ahora=DESPUES))
caso("«.sello.tmp» que no se puede escribir: RegistroError y el registro intacto",
     isinstance(e, rx.RegistroError) and reg.ruta.read_bytes() == antes, repr(e)[:100])

# 5. Las excepciones nuevas sin sello (no hacen falta para el atacante, que puede rehacer el sello; ¿y por accidente?)
reg, exp = base()
ls = lineas(reg.ruta)
reg.sello.unlink(); escribir_lineas(reg.ruta, ls[:1])
ok, d = detecta(reg)
caso("(límite declarado: tocar el sello) sin sello y truncado a la primera anotación: se detecta", ok, d)

# 6. La orden «sellar»: ¿solo para registros 0.1.0? ¿deja rastro?
reg, exp = base()
ls = lineas(reg.ruta)
reg.sello.unlink(); escribir_lineas(reg.ruta, ls[:3])   # se quitan los dos intentos de después, el «fallido» incluido
r = subprocess.run([sys.executable, "-I", str(RAIZ / ".docs" / "scripts" / "registro_experimentos.py"), "--registro",
                    str(reg.ruta), "sellar"], capture_output=True, text=True)
version = {json.loads(x).get("version_registro") for x in ls[:3]} - {None}
caso("«sellar» se niega con un registro que no es de la 0.1.0 (sus prerregistros dicen version_registro "
     f"{sorted(version)})", r.returncode != 0, (r.stdout + r.stderr).strip()[:120])
caso("…o al menos deja rastro en la cadena (una anotación o un aviso que «verificar» repita)",
     len(lineas(reg.ruta)) > 3 or "sell" in subprocess.run([sys.executable, "-I", str(RAIZ / ".docs/scripts/registro_experimentos.py"),
                                                           "--registro", str(reg.ruta), "verificar"],
                                                          capture_output=True, text=True).stdout,
     f"anotaciones {len(lineas(reg.ruta))}; verificar: "
     + subprocess.run([sys.executable, "-I", str(RAIZ / ".docs/scripts/registro_experimentos.py"), "--registro", str(reg.ruta),
                       "verificar"], capture_output=True, text=True).stdout.strip())
r = subprocess.run([sys.executable, "-I", str(RAIZ / ".docs" / "scripts" / "registro_experimentos.py"), "--registro",
                    str(reg.ruta), "sellar"], capture_output=True, text=True)
caso("«sellar» con el sello ya puesto: se niega", r.returncode == 2, r.stderr.strip()[:100])

# 7. Sello con tipos raros que en Python se comparan iguales
reg, exp = base()
s = json.loads(reg.sello.read_text(encoding="utf-8"))
reg.sello.write_text(json.dumps({"seq": float(s["seq"]), "hash": s["hash"]}), encoding="utf-8")
caso("(cosmético) sello con «seq» 7.0 en vez de 7: se acepta (inofensivo: casa la huella)", lanza(reg.verificar) is None)

for t in tmps:
    borrar(t)
fin()
