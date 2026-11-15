"""r04_04 · La regla del «fallido» tardío de la 0.4.0 (H-27, decisión [PROPUESTO] (1)): instantes iguales, en otras zonas,
instantes atrasados con `ahora`, intentos intercalados de otras variantes, el camino honrado tras un corte y la línea de
órdenes de verdad (el reloj del sistema, al segundo). Uso: .venv/bin/python -B r04_04_fallido_tardio.py <raíz>"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import AHORA, borrar, caso, cli, fin, lanza, pre, rx, tmpdir  # noqa: E402

tmps = []


def montar(maximo=1):
    d = tmpdir("r04_t99_"); tmps.append(d)
    reg = rx.Registro(d / "registro.jsonl")
    return reg, reg.prerregistrar(pre(max_variantes=maximo), "qa", ahora=AHORA)["exp_id"]


def resumen_corto(reg, exp):
    r = reg.resumen(exp)
    return r["adoptable"], {k: (v["veredicto"], v["pendiente"], v["fallido_tardio"]) for k, v in r["por_variante"].items()}


T = lambda hh, mm=0, ss=0, zona="+00:00": f"2026-11-12T{hh:02d}:{mm:02d}:{ss:02d}{zona}"   # noqa: E731

# 1. Control (H-27 con instantes distintos): 1 abierto a las 11, 2 a las 12 «mejor», el 1 cerrado «fallido» a las 13
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(11)); reg.intento(exp, "v1", ahora=T(12)); reg.resultado(exp, 2, "mejor", ahora=T(12, 30))
reg.resultado(exp, 1, "fallido", ahora=T(13))
a, d = resumen_corto(reg, exp)
caso("control: «fallido» del 1 anotado después de empezar el 2 (13:00 > 12:00): no se adopta", a is False, f"adoptable={a}; {d}")

# 2. El mismo orden en el fichero, con instantes iguales (todo en el mismo segundo): la regla compara instantes con «<»
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(12)); reg.intento(exp, "v1", ahora=T(12)); reg.resultado(exp, 2, "mejor", ahora=T(12))
reg.resultado(exp, 1, "fallido", ahora=T(12))
a, d = resumen_corto(reg, exp)
caso("instantes iguales: el «fallido» del 1 escrito DESPUÉS del «mejor» del 2 (orden del fichero) no deja adoptar",
     a is False, f"adoptable={a}; {d}")

# 3. El mismo orden, con el «fallido» atrasado con `ahora` (biblioteca): el fichero dice que se escribió después
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(11)); reg.intento(exp, "v1", ahora=T(12)); reg.resultado(exp, 2, "mejor", ahora=T(12, 30))
e = lanza(lambda: reg.resultado(exp, 1, "fallido", ahora=T(11, 30)), rx.RegistroError)
a, d = resumen_corto(reg, exp) if e is None else (None, str(e)[:100])
caso("«fallido» escrito después del «mejor» con un instante atrasado (11:30): o se rechaza, o no deja adoptar",
     e is not None or a is False, f"adoptable={a}; {d}")

# 4. Instantes que retroceden: un resultado anterior a su propio intento, o al prerregistro, se acepta?
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(12))
e = lanza(lambda: reg.resultado(exp, 1, "mejor", ahora=T(9)), rx.RegistroError)
caso("un resultado registrado ANTES de que empezara su intento (09:00 < 12:00) se rechaza", e is not None,
     "se aceptó" if e is None else str(e)[:100])

# 5. Otras zonas: el 2 empieza a las 12:00+02:00 (= 10:00Z) y el «fallido» del 1 se anota a las 10:30Z
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(9)); reg.intento(exp, "v1", ahora=T(12, zona="+02:00")); reg.resultado(exp, 2, "mejor", ahora=T(10, 20))
reg.resultado(exp, 1, "fallido", ahora=T(10, 30, zona="Z"))
a, d = resumen_corto(reg, exp)
caso("otras zonas: 2 empieza 12:00+02:00 (10:00Z), «fallido» del 1 a las 10:30Z: tardío, no se adopta", a is False, f"{a}; {d}")
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(10)); reg.resultado(exp, 1, "fallido", ahora=T(10, 30, zona="Z"))
reg.intento(exp, "v1", ahora=T(12, 40, zona="+02:00")); reg.resultado(exp, 2, "mejor", ahora=T(11))
a, d = resumen_corto(reg, exp)
caso("otras zonas: «fallido» del 1 a las 10:30Z y el 2 a las 12:40+02:00 (10:40Z): a tiempo, se adopta", a is True, f"{a}; {d}")

# 6. Intentos intercalados de otra variante (máximo 2): v1 abierto, v2 «mejor», v1 repetido «mejor», el 1 cerrado tarde
reg, exp = montar(2)
reg.intento(exp, "v1", ahora=T(9)); reg.intento(exp, "v2", ahora=T(10)); reg.resultado(exp, 2, "mejor", ahora=T(10, 30))
reg.intento(exp, "v1", ahora=T(11)); reg.resultado(exp, 3, "mejor", ahora=T(11, 30)); reg.resultado(exp, 1, "fallido", ahora=T(12))
r = reg.resumen(exp)
caso("intercalados: v1 «fallido» tardío no se adopta y v2 sí (no depende de v1)", r["adoptables"] == [2],
     f"adoptables={r['adoptables']}; {r['por_variante']['v1']['fallido_tardio']}")

# 7. El camino honrado tras un corte: el 1 se cierra «fallido» ANTES de repetir: la repetición «mejor» se adopta
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(9)); reg.resultado(exp, 1, "fallido", ahora=T(10)); reg.intento(exp, "v1", ahora=T(10))
reg.resultado(exp, 2, "mejor", ahora=T(11))
a, d = resumen_corto(reg, exp)
caso("honrado: «fallido» a las 10:00 y la repetición empieza a las 10:00 (mismo segundo, después en el fichero): se adopta",
     a is True, f"{a}; {d}")

# 8. El honrado que repite primero y cierra después: la variante no se podrá adoptar nunca (falla cerrado). ¿Se avisa?
reg, exp = montar()
reg.intento(exp, "v1", ahora=T(9)); reg.intento(exp, "v1", ahora=T(10))
r = reg.resumen(exp)
caso("(referencia) repetir sin cerrar el abierto: la variante queda «pendiente» y el resumen lo dice",
     r["por_variante"]["v1"]["pendiente"] is True and r["sin_resultado"] == [1, 2], f"{r['sin_resultado']}")
e = lanza(lambda: reg.intento(exp, "v1", ahora=T(10, 5)), rx.RegistroError)
caso("(observación) un tercer intento de una variante con intentos abiertos se admite sin aviso",
     e is None, "se rechaza" if e else "se admite")

# 9. La línea de órdenes de verdad (reloj del sistema, al segundo): intento, intento, «mejor» del 2 y «fallido» del 1 seguidos.
#    Se repite hasta 5 veces buscando que caigan en el mismo segundo.
d = tmpdir("r04_t99_cli_"); tmps.append(d)
(d / "pre.json").write_text(__import__("json").dumps(pre(max_variantes=1)), encoding="utf-8")
adoptado, intentos_cli = None, 0
for k in range(5):
    reg_p = d / f"r{k}.jsonl"
    cli("--registro", str(reg_p), "prerregistrar", str(d / "pre.json"))
    while time.time() % 1 > 0.2:   # empezar al principio de un segundo
        time.sleep(0.01)
    t0 = int(time.time())
    for args in (("intento", "EXP-2026-0001", "--variante", "v1"), ("intento", "EXP-2026-0001", "--variante", "v1"),
                 ("resultado", "EXP-2026-0001", "2", "mejor"), ("resultado", "EXP-2026-0001", "1", "fallido")):
        cli("--registro", str(reg_p), *args)
    intentos_cli += 1
    if int(time.time()) == t0:
        adoptado = rx.Registro(reg_p).adoptable("EXP-2026-0001")
        break
caso("línea de órdenes, las cuatro órdenes en el mismo segundo: el «fallido» tardío no deja adoptar",
     adoptado is not True, f"adoptable={adoptado} (en {intentos_cli} tanda(s); None: no cayeron en el mismo segundo)")

for t in tmps:
    borrar(t)
fin()
