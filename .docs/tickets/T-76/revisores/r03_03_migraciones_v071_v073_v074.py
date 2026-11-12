"""QA r03 de T-76 (V0.75): estados genuinos de la V0.71, la V0.73 y la V0.74, con la sombra en marcha, migrados a la V0.75; diario y
volcado. Datos SIMULADOS.

Uso: python3 -I .docs/tickets/T-76/revisores/r03_03_migraciones_v071_v073_v074.py [ruta del marco]
El código antiguo se extrae con `git archive` de los commits c306132 (V0.71), 7b775cc (V0.73) y 5d03192 (V0.74). Si la copia del
repositorio es superficial y no los tiene, se indica otro directorio git con R03_GIT_DIR (por ejemplo, un clon «bare» con
`git fetch --depth=80` de develop en una carpeta temporal). Cada sonda imprime FALLA o BIEN. Termina con 0 siempre: es una sonda.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

RES = []
COMMITS = {"V0.71": ("c3061327ca69d1763ca550ca2040c674d9e3e1f5", mg.ESQUEMA_V0_71, ["MIG-009", "MIG-010", "MIG-011"]),
           "V0.73": ("7b775cc4502c55a0a79e06a0a4deb88b651c91a7", mg.ESQUEMA_V0_73, ["MIG-010", "MIG-011"]),
           "V0.74": ("5d03192ccf889689d66b0b3560e4f3ccd9b9658f", mg.ESQUEMA_V0_74, ["MIG-011"])}
GIT_DIR = os.environ.get("R03_GIT_DIR")


def sonda(nombre, falla, detalle=""):
    RES.append((nombre, falla))
    print(f"{'FALLA' if falla else 'BIEN':6s} {nombre}  {str(detalle)[:500]}")


def git(*args, **kw):
    base = ["git", f"--git-dir={GIT_DIR}"] if GIT_DIR else ["git", "-C", str(MARCO)]
    return subprocess.run(base + list(args), capture_output=True, **kw)


# Generador: lo ejecuta el código antiguo. Meses 1 a 24 en el día 2 de cada mes siguiente (válido en V0.73 y V0.74; la V0.71 aceptaba
# el día 28 del propio mes). Un aporte tras el cierre del mes 24 y antes de compararlo (H-10 de la r02) y un O-42 sin acusar.
GEN = r'''
import sys; sys.path.insert(0, 'validador'); sys.path.insert(0, 'pruebas')
import persistencia as pe
from pruebas_orquestador import AHORA, hasta, nuevo
V071 = sys.argv[1] == "V0.71"
o = nuevo(); hasta(o, 'EN_ANALISIS', 1); assert o.registrar_gasto('EV-ENC-0001', 2.0, 1.0, AHORA)['ok']
assert o.iniciar_sombra(100000.0, 100.0, 'OPERADOR', AHORA)['ok']
def mk(k):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    return f'{a:04d}-{m:02d}', (f'{a:04d}-{m:02d}-28T12:00:00+00:00' if V071 else f'{a2:04d}-{m2:02d}-02T06:00:00+00:00')
for k in range(1, 24):
    mes, t = mk(k)
    r = o.comparar_sombra(mes, 100000.0, 100.0, 100.0, 100.0, 0.0, 'I', t); assert r['ok'], (k, r)
mes, t = mk(24)
if not V071:
    assert o.movimiento_sombra('RETIRADA', 50000.0, 100.0, 'OPERADOR', '2028-12-01T12:00:00+00:00')['ok']
r = o.comparar_sombra(mes, 99000.0, 100.0, 100.0, 100.0, 0.0, 'I', t); assert r['ok'], r
print(r['veredicto'], file=sys.stderr)
if not V071 and hasattr(o, 'comparacion_sombra_pendiente'):
    o.barrer('2029-02-01T06:00:00+00:00')   # 2029-01 sin comparar: O-42 (V0.73/V0.74: sin plazo de gracia)
print(pe.volcar(o, '2029-02-01T06:00:01+00:00'))
'''

tmp = Path(tempfile.mkdtemp(prefix="r03_t76_"))
estados = {}
for v, (sha, esq, _) in COMMITS.items():
    if git("cat-file", "-e", sha).returncode != 0:
        sonda(f"M0_{v}_codigo_disponible", True, f"no está el commit {sha[:7]}: define R03_GIT_DIR (ver docstring)")
        continue
    d = tmp / v
    d.mkdir()
    arch = git("archive", sha, "sistema_global/marco_comun_c", check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(d)], input=arch, check=True)
    cwd = d / "sistema_global" / "marco_comun_c"
    s = subprocess.run([sys.executable, "-I", "-c", GEN, v], cwd=str(cwd), capture_output=True, text=True)
    if s.returncode != 0:
        sonda(f"M0_{v}_genera_el_estado", True, s.stderr[-600:])
        continue
    estados[v] = (s.stdout.strip(), s.stderr.strip())

for v, (texto, ver_viejo) in estados.items():
    sha, esq, cadena = COMMITS[v]
    doc = json.loads(texto)
    directo = pe.cargar(texto)
    m = mg.migrar(texto, "2029-02-02T06:00:00+00:00", f"QA r03 de T-76: estado genuino de la {v} con la sombra en marcha")
    om = m.get("orquestador") if m["ok"] else None
    inf = om.informe_sombra() if om else None
    sonda(f"M1_{v}_migra_con_su_cadena_y_queda_integro",
          not (doc["esquema"] == esq and not directo["ok"] and m["ok"] and m["migraciones"] == cadena and om.integridad() == []
               and inf["comparaciones"] == 24 and inf["ultima"]["mes"] == "2028-11"),
          f"esquema {v} {doc['esquema'] == esq}; cargar sin migrar {directo['codigo']}; migrar {m['codigo']} {m.get('migraciones')} "
          f"{'' if m['ok'] else m.get('motivo')}; integridad {om.integridad() if om else None}; juicio antiguo del mes 24: {ver_viejo}")
    if not om:
        continue
    # el veredicto antiguo se conserva tal cual (histórico)
    ult = inf["ultima"]
    sonda(f"M2_{v}_la_comparacion_antigua_se_conserva_como_historica", ult["veredicto"] != ver_viejo, f"{ult['veredicto']} (antes {ver_viejo})")
    # después: barrer con plazo de gracia; la comparación siguiente funciona y se valora al cierre
    n42_antes = sum(a["codigo"] in ("O-42", "O-44") for a in om.avisos)
    om.barrer("2029-02-06T00:00:00+00:00")   # gracia de 2029-01 vencida (5 días)
    nuevos = [(a["codigo"], a["prioridad"], a["motivo"][:60]) for a in om.avisos if a["codigo"] in ("O-42", "O-44")][n42_antes:]
    r1 = om.comparar_sombra("2028-12", 50000.0, 100.0, 100.0, 100.0, 0.0, "I", "2029-02-06T01:00:00+00:00")
    r2 = om.comparar_sombra("2029-01", 50000.0, 100.0, 100.0, 100.0, 0.0, "I", "2029-02-06T02:00:00+00:00")
    om.barrer("2029-02-06T03:00:00+00:00")
    pend = om.comparaciones_sombra_pendientes("2029-02-06T03:00:00+00:00")
    sonda(f"M3_{v}_tras_migrar_sigue_O44_y_se_pone_al_dia", not (nuevos and nuevos[0][0] == "O-44" and r1["ok"] and r2["ok"] and pend is None and om.integridad() == []),
          f"avisos nuevos {nuevos}; dic {r1['codigo']} {r1.get('veredicto')}; ene {r2['codigo']} {r2.get('veredicto')}; pendientes {pend}")
    viejos42 = [a for a in om.avisos if a["codigo"] == "O-42" and a["acuse"] is None]
    if v != "V0.71":
        sonda(f"M4_{v}_O42_antiguo_sin_acusar_queda_junto_al_nuevo", len(viejos42) > 0 and nuevos,
              f"O-42 antiguos sin acusar: {[a['motivo'][:70] for a in viejos42]} (sigue vivo aunque ya se comparó; lo acusa el operador)")
    # volcar y cargar de nuevo
    t2 = pe.volcar(om, "2029-02-06T04:00:00+00:00")
    c2 = pe.cargar(t2)
    sonda(f"M5_{v}_volcar_y_cargar_tras_migrar", not (c2["ok"] and c2["orquestador"].sombra == om.sombra and json.loads(t2)["esquema"] == mg.ESQUEMA_V0_75),
          c2["codigo"])

# M6: la descripción de MIG-011 y la de MIG-009 frente a lo que cambia el código
d11 = next(m.descripcion for m in mg.MIGRACIONES if m.id == "MIG-011")
sonda("M6_MIG011_declara_que_las_comparaciones_de_V073_V074_se_valoraron_en_el_instante_y_no_al_cierre",
      not any(p in d11 for p in ("histórica", "historicas", "históricas", "con sus reglas")), d11[:300])

# M7: el diario reproduce la sombra con la V0.75 (aporte tras el cierre, comparación tardía, O-41, O-44)
dd = tmp / "diario"
dd.mkdir()
o = nuevo()
r = di.crear(o, str(dd / "estado.json"), str(dd / "diario.jsonl"), AHORA)
D = r.get("diario")
ok = r["ok"] and D is not None
if ok:
    pasos = [("iniciar_sombra", (100000.0, 100.0, "OPERADOR", "2026-11-06T10:00:00+00:00"))]
    for k in range(1, 24):
        a, mm = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
        a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
        pasos.append(("comparar_sombra", (f"{a:04d}-{mm:02d}", 100000.0, 100.0, 100.0, 100.0, 0.0, "I", f"{a2:04d}-{m2:02d}-02T06:00:00+00:00")))
    pasos += [("movimiento_sombra", ("RETIRADA", 50000.0, 100.0, "OPERADOR", "2028-12-02T09:00:00+00:00")),
              ("barrer", ("2028-12-06T00:00:00+00:00",)),
              ("comparar_sombra", ("2028-11", 99000.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-07T09:00:00+00:00"))]
    for met, args in pasos:
        rr = getattr(D, met)(*args)
        assert rr["ok"], (met, rr)
    vivo = D.orquestador
    ab = di.abrir(str(dd / "estado.json"), str(dd / "diario.jsonl"))
    re_ = ab["diario"].orquestador if ab.get("diario") is not None else None
    av = lambda x: [(a["codigo"], a["motivo"]) for a in x.avisos if a["codigo"] in ("O-41", "O-42", "O-44")]  # noqa: E731
    sonda("M7_el_diario_reproduce_la_sombra_valorada_al_cierre", not (ab["ok"] and re_ is not None and re_.sombra == vivo.sombra and av(re_) == av(vivo)
                                                                       and [c for c, _ in av(vivo)] == ["O-44", "O-41"]),
          f"abrir {ab['codigo']}; avisos {[c for c, _ in av(vivo)]}")
else:
    sonda("M7_el_diario_reproduce_la_sombra_valorada_al_cierre", True, f"crear: {r}")

print(f"\n{sum(1 for _, c in RES if c)} FALLA de {len(RES)} sondas")
shutil.rmtree(tmp, ignore_errors=True)
