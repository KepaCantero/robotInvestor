"""r05_03 · El «fallido» tardío por `_seq` (H-36) y la regla nueva de la 0.5.0: no se repite una variante con un intento abierto.
1. Registros anteriores a la regla (intentos de la misma variante abiertos a la vez, construidos con la cadena bien hecha y la
   versión 0.4.0): el «fallido» tardío se decide por el orden de la cadena, con instantes iguales, atrasados o adelantados.
2. Resultado anterior al inicio de su intento: se rechaza.
3. La regla nueva: la misma variante (también en NFD) no se repite con uno abierto; otra variante sí; cerrar el abierto como
   «fallido» desbloquea y no deja la variante tardía.
4. ¿Se puede quedar alguien bloqueado sin salida? Intento con un inicio adelantado (reloj adelantado); registro antiguo con dos
   intentos abiertos de la misma variante; la línea de órdenes de verdad.
5. El banco con el cliente simulado: un `kill -9` deja el intento abierto, la repetición se niega con un motivo que dice la salida,
   el «fallido» a mano la desbloquea y la variante sigue pudiendo adoptarse.
Uso: .venv/bin/python -B r05_03_tardio_y_abiertos.py <raíz> [--sin-banco]"""
import json
import os
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r05_comun import (AHORA, PY, RAIZ, SCRIPTS, borrar, caso, cli, fin, lanza, lineas, pre, recadenar, rehacer_sello, rx,  # noqa: E402
                       tmpdir, escribir_lineas)

tmps = []
T = lambda hh, mm=0, ss=0: f"2026-11-12T{hh:02d}:{mm:02d}:{ss:02d}+00:00"   # noqa: E731


def nuevo(maximo=1):
    d = tmpdir("r05_t99_"); tmps.append(d)
    reg = rx.Registro(d / "registro.jsonl")
    return reg, reg.prerregistrar(pre(max_variantes=maximo), "qa", ahora=AHORA)["exp_id"]


def antiguo(eventos, maximo=1):
    """Registro «de la 0.4.0» con los eventos dados en ese orden: ('I', variante, instante) o ('R', n, veredicto, instante)."""
    d = tmpdir("r05_t99_old_"); tmps.append(d)
    contenido = {k: v for k, v in sorted(pre(max_variantes=maximo).items())}
    h = rx.huella(contenido)
    objs = [{"tipo": "PRERREGISTRO", "exp_id": "EXP-2026-0001", "autor": "qa", "creado_en": AHORA, "version_registro": "0.4.0",
             "contenido": contenido, "huella_prerregistro": h}]
    previos = []
    for ev in eventos:
        if ev[0] == "I":
            objs.append({"tipo": "INTENTO", "exp_id": "EXP-2026-0001", "n": len(previos) + 1, "variante": ev[1], "inicio": ev[2],
                         "huella_prerregistro": h, "dentro_del_maximo": rx._dentro(previos, ev[1], maximo)})
            previos.append(objs[-1])
        else:
            objs.append({"tipo": "RESULTADO", "exp_id": "EXP-2026-0001", "n": ev[1], "veredicto": ev[2], "detalle": {},
                         "registrado_en": ev[3]})
    reg = rx.Registro(d / "registro.jsonl")
    escribir_lineas(reg.ruta, recadenar(objs))
    rehacer_sello(reg)
    return reg, "EXP-2026-0001"


def corto(reg, exp):
    r = reg.resumen(exp)
    return r["adoptable"], {k: (v["veredicto"], v["pendiente"], v["fallido_tardio"]) for k, v in r["por_variante"].items()}


# 1. «Fallido» tardío por el orden de la cadena (registros anteriores a la regla)
for titulo, evs, esperado in (
    ("mismo instante en todo: fallido del 1 después del mejor del 2", [("I", "v1", T(12)), ("I", "v1", T(12)), ("R", 2, "mejor", T(12)),
                                                                       ("R", 1, "fallido", T(12))], False),
    ("fallido del 1 con el instante atrasado a antes del inicio del 2", [("I", "v1", T(11)), ("I", "v1", T(12)),
                                                                         ("R", 2, "mejor", T(12, 30)), ("R", 1, "fallido", T(11, 30))], False),
    ("fallido del 1 escrito después de EMPEZAR el 2, antes de su resultado", [("I", "v1", T(11)), ("I", "v1", T(12)),
                                                                              ("R", 1, "fallido", T(12)), ("R", 2, "mejor", T(13))], False),
    ("(control) fallido del 1 antes del intento 2 en la cadena, con instante adelantado", [("I", "v1", T(11)), ("R", 1, "fallido", T(14)),
                                                                                         ("I", "v1", T(12)), ("R", 2, "mejor", T(13))], True),
    ("otra variante en medio no cambia nada (v2 abierto, v1 fallido tardío)", [("I", "v1", T(11)), ("I", "v2", T(11)), ("I", "v1", T(12)),
                                                                              ("R", 3, "mejor", T(12)), ("R", 1, "fallido", T(13)),
                                                                              ("R", 2, "peor", T(13))], False),
):
    reg, exp = antiguo(evs, maximo=2)
    a, d = corto(reg, exp)
    caso(f"tardío por _seq: {titulo}: adoptable={esperado}", a is esperado, f"{d}")

# 2. Resultado anterior al inicio de su intento
reg, exp = nuevo()
reg.intento(exp, "v1", ahora=T(12))
e = lanza(lambda: reg.resultado(exp, 1, "mejor", ahora=T(11)), rx.RegistroError)
caso("resultado anterior al inicio de su intento: se rechaza sin escribir", e is not None and len(lineas(reg.ruta)) == 2, str(e)[:80] if e else "")
caso("(control) resultado en el mismo segundo que el inicio: se admite", lanza(lambda: reg.resultado(exp, 1, "mejor", ahora=T(12)), rx.RegistroError) is None)

# 3. La regla nueva
reg, exp = nuevo(maximo=2)
reg.intento(exp, "única", ahora=T(11))
nfd = unicodedata.normalize("NFD", "única")
e = lanza(lambda: reg.intento(exp, nfd, ahora=T(12)), rx.RegistroError)
caso("con el 1 abierto, la misma variante en NFD se niega sin escribir", e is not None and len(lineas(reg.ruta)) == 2, str(e)[:80] if e else "")
e = lanza(lambda: reg.intento(exp, "otra", ahora=T(12)), rx.RegistroError)
caso("con el 1 abierto, otra variante sí se puede", e is None)
reg.resultado(exp, 1, "fallido", ahora=T(12, 30))
e = lanza(lambda: reg.intento(exp, "única", ahora=T(13)), rx.RegistroError)
caso("cerrado el 1 como «fallido», la variante se repite", e is None)
reg.resultado(exp, 3, "mejor", ahora=T(14)); reg.resultado(exp, 2, "peor", ahora=T(14))
a, d = corto(reg, exp)
caso("y la repetición «mejor» se adopta (el fallido no es tardío)", a is True, f"{d}")
reg2, exp2 = nuevo()
reg2.intento(exp2, "v1", ahora=T(11)); reg2.resultado(exp2, 1, "peor", ahora=T(11, 30))
reg2.intento(exp2, "v1", ahora=T(12)); reg2.resultado(exp2, 2, "mejor", ahora=T(12, 30))
a, d = corto(reg2, exp2)
caso("(control) peor y después mejor de la misma variante: contradictoria, no se adopta", a is False, f"{d}")

# 4. ¿Bloqueos sin salida?
reg, exp = nuevo()
futuro = "2099-01-01T00:00:00+00:00"
reg.intento(exp, "v1", ahora=futuro)
rc, out = cli("--registro", str(reg.ruta), "resultado", exp, "1", "fallido")
caso("(observación) intento con el inicio adelantado (reloj de la máquina adelantado): la línea de órdenes no puede cerrarlo",
     rc != 0, out[:110])
rc2, out2 = cli("--registro", str(reg.ruta), "intento", exp, "--variante", "v1")
caso("(observación) y la variante no se puede repetir hasta esa fecha (otra variante sí, pero fuera del máximo 1)", rc2 != 0, out2[:80])
e = lanza(lambda: reg.intento(exp, "2099", ahora=AHORA), rx.RegistroError)
caso("(observación) intento con un inicio anterior al de otro intento del mismo experimento: se admite", e is None,
     "no se valida que los inicios no retrocedan ni que no vayan por delante del reloj")

reg, exp = antiguo([("I", "v1", T(11)), ("I", "v1", T(12))])
e1 = lanza(lambda: reg.resultado(exp, 1, "fallido", ahora=T(13)), rx.RegistroError)
e2 = lanza(lambda: reg.resultado(exp, 2, "fallido", ahora=T(13)), rx.RegistroError)
e3 = lanza(lambda: reg.intento(exp, "v1", ahora=T(14)), rx.RegistroError)
caso("registro antiguo con dos abiertos de v1: se cierran los dos y v1 se repite", (e1, e2, e3) == (None, None, None),
     str(e1 or e2 or e3)[:80])

d = tmpdir("r05_t99_cli_"); tmps.append(d)
(d / "pre.json").write_text(json.dumps(pre(max_variantes=1)), encoding="utf-8")
R = ["--registro", str(d / "r.jsonl")]
pasos = [cli(*R, "prerregistrar", str(d / "pre.json")), cli(*R, "intento", "EXP-2026-0001", "--variante", "v1"),
         cli(*R, "intento", "EXP-2026-0001", "--variante", "v1"), cli(*R, "resultado", "EXP-2026-0001", "1", "fallido"),
         cli(*R, "intento", "EXP-2026-0001", "--variante", "v1"), cli(*R, "resultado", "EXP-2026-0001", "2", "mejor")]
caso("línea de órdenes: repetir con uno abierto sale con código 2 y dice «fallido si se cortó»",
     pasos[2][0] == 2 and "fallido" in pasos[2][1], pasos[2][1][-90:])
caso("línea de órdenes: el camino honrado tras un corte (fallido y repetir) acaba adoptable",
     [p[0] for p in pasos] == [0, 0, 2, 0, 0, 0] and rx.Registro(d / "r.jsonl").adoptable("EXP-2026-0001"))

# 5. El banco con el cliente simulado: kill -9, repetición, «fallido» a mano
if "--sin-banco" not in sys.argv:
    d = tmpdir("r05_t99_banco_"); tmps.append(d)
    reg_banco = d / "registro.jsonl"
    entorno = {k: v for k, v in os.environ.items() if k != "RI_AGENTE"}
    base = [PY, "-B", str(SCRIPTS / "banco_medida.py"), "a", "--desde", "2024-01-05", "--hasta", "2024-03-29", "--cliente", "mock",
            "--registro", str(reg_banco)]
    p = subprocess.Popen(base + ["--salida", str(d / "s1")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=entorno, cwd=RAIZ)
    t0 = time.monotonic()
    while time.monotonic() - t0 < 60 and not (reg_banco.exists() and len(lineas(reg_banco)) >= 2):
        time.sleep(0.2)
    time.sleep(1.0)
    p.kill(); p.wait()
    r = rx.Registro(reg_banco)
    caso("banco: tras un kill -9 queda el intento 1 abierto", r.resumen("EXP-2026-0001")["sin_resultado"] == [1])
    q = subprocess.run(base + ["--salida", str(d / "s2")], capture_output=True, text=True, env=entorno, cwd=RAIZ)
    caso("banco: la repetición se niega con código 2 y dice cómo salir", q.returncode == 2 and "fallido" in q.stderr,
         q.stderr.strip()[-110:])
    rc, out = cli("--registro", str(reg_banco), "resultado", "EXP-2026-0001", "1", "fallido", "--detalle", '{"motivo": "kill -9"}')
    q = subprocess.run(base + ["--salida", str(d / "s3")], capture_output=True, text=True, env=entorno, cwd=RAIZ)
    res = r.resumen("EXP-2026-0001")
    v = next(iter(res["por_variante"].values()))
    caso("banco: con el 1 cerrado a mano como «fallido», la repetición se anota y no queda tardía",
         rc == 0 and q.returncode == 0 and res["intentos"] == 2 and not v["fallido_tardio"] and not v["pendiente"],
         f"{res['veredictos']}; {v}")
    q = subprocess.run([PY, "-B", str(SCRIPTS / "banco_medida.py"), "verificar", str(d / "s3")], capture_output=True, text=True,
                       env=entorno, cwd=RAIZ)
    caso("banco: verificar la salida de la repetición", q.returncode == 0, q.stdout.strip()[:60])

for t in tmps:
    borrar(t)
fin()
