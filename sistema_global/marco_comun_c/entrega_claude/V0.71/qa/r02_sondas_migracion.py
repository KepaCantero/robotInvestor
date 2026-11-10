"""QA r02 de T-76 (V0.73): diario, persistencia, esquema V0.73 y MIG-009 desde un estado genuino de V0.71 con comparaciones.

Uso (desde sistema_global/marco_comun_c, dentro del repositorio git): python3 -I entrega_claude/V0.71/qa/r02_sondas_migracion.py
El estado de V0.71 se genera con el código del commit c306132 (extraído con git archive a una carpeta temporal).
Cada sonda imprime FALLA (el defecto existe) o BIEN. Termina con 0 siempre.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
from pruebas_orquestador import AHORA, hasta, nuevo  # noqa: E402

RES = []
COMMIT_V071 = "c306132"


def sonda(nombre, falla, detalle=""):
    RES.append((nombre, falla))
    print(f"{'FALLA' if falla else 'BIEN':6s} {nombre}  {detalle}")


def mes_k(k, dia="01T06:00:00"):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a2:04d}-{m2:02d}-{dia}+00:00"


tmp = Path(tempfile.mkdtemp(prefix="r02_t76_"))

# ---------------------------------------------------------------- M1: el diario reproduce la sombra, sus O-41 y los O-42 de barrer
o = nuevo()
hasta(o, "EN_ANALISIS", 1)
assert o.registrar_gasto("EV-ENC-0001", 3.0, 1.0, AHORA)["ok"]
r = di.crear(o, str(tmp / "e.json"), str(tmp / "d.jsonl"), AHORA)
assert r["ok"], r
d = r["diario"]
assert d.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)["ok"]
assert d.movimiento_sombra("APORTE", 1100.0, 110.0, "G", AHORA)["ok"]
for k in range(1, 28):
    mes, t = mes_k(k)
    if k == 5:
        assert d.movimiento_sombra("RETIRADA", 500.0, 95.0, "OPERADOR", t)["ok"]
    if k in (10, 20):
        assert d.barrer(t)["ok"]   # el mes k está pendiente: O-42
    rr = d.comparar_sombra(mes, 9000.0 if k != 26 else 99999.0, 100.0 + k, 100.0, 100.0 + k / 2, 10.0, "I", t)
    assert rr["ok"], (k, rr)
vivo = json.dumps(d.orquestador.sombra, sort_keys=True)
avisos_vivos = [(a["codigo"], a["motivo"]) for a in d.orquestador.avisos]
r2 = di.abrir(str(tmp / "e.json"), str(tmp / "d.jsonl"))
re_ = r2["diario"].orquestador if r2["ok"] else None
sonda("M1_el_diario_no_reproduce_la_sombra_ni_sus_avisos", not (r2["ok"] and json.dumps(re_.sombra, sort_keys=True) == vivo
                                                               and [(a["codigo"], a["motivo"]) for a in re_.avisos] == avisos_vivos
                                                               and re_.integridad() == []),
      f"abrir: {r2['codigo']}; O-41 {[c for c, _ in avisos_vivos].count('O-41')}, O-42 {[c for c, _ in avisos_vivos].count('O-42')}")

# ---------------------------------------------------------------- M2: volcar y cargar con la V0.73
t = pe.volcar(o, "2026-11-06T10:00:00+00:00") if False else pe.volcar(d.orquestador, mes_k(27)[1])
c = pe.cargar(t)
sonda("M2_volcar_y_cargar", not (c["ok"] and c["orquestador"].sombra == d.orquestador.sombra and json.loads(t)["esquema"] == mg.ESQUEMA_V0_73),
      f"{c['codigo']}; esquema del volcado V0.73: {json.loads(t)['esquema'] == mg.ESQUEMA_V0_73}")

# ---------------------------------------------------------------- M3: esquema V0.73 actual, registrado y cadena de migraciones
esquemas = json.loads((MARCO / "validador" / "esquemas_codigo.json").read_text())
claves = list(esquemas) if isinstance(esquemas, dict) else []
cadena = [m.id for m in mg.MIGRACIONES][-3:]
ult = mg.MIGRACIONES[-1]
sonda("M3_esquema_V073_mal_registrado", not (pe.esquema_actual() == mg.ESQUEMA_V0_73 and mg.ESQUEMA_V0_73 in json.dumps(esquemas)
                                              and ult.id == "MIG-009" and ult.esquema_desde == mg.ESQUEMA_V0_71 and ult.esquema_hasta == mg.ESQUEMA_V0_73),
      f"actual==V0.73 {pe.esquema_actual() == mg.ESQUEMA_V0_73}; en esquemas_codigo.json {mg.ESQUEMA_V0_73 in json.dumps(esquemas)}; "
      f"últimas {cadena}")

# ---------------------------------------------------------------- M4: MIG-009 desde un estado genuino de V0.71, con comparaciones y O-41
viejo = tmp / "v071"
viejo.mkdir()
arch = subprocess.run(["git", "-C", str(MARCO), "archive", COMMIT_V071, "--", "."], capture_output=True, check=True).stdout
subprocess.run(["tar", "-x", "-C", str(viejo)], input=arch, check=True)
gen = (
    "import sys, json; sys.path.insert(0, 'validador'); sys.path.insert(0, 'pruebas')\n"
    "import persistencia as pe\n"
    "from pruebas_orquestador import AHORA, hasta, nuevo\n"
    "o = nuevo(); hasta(o, 'EN_ANALISIS', 1); assert o.registrar_gasto('EV-ENC-0001', 2.0, 1.0, AHORA)['ok']\n"
    "assert o.iniciar_sombra(1000.0, 100.0, 'OPERADOR', AHORA)['ok']\n"
    "for k in range(1, 26):\n"
    "    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1\n"
    "    mes = f'{a:04d}-{m:02d}'\n"
    "    r = o.comparar_sombra(mes, 900.0, 100.0, 100.0 + (k == 3), 101.0, 0.0, 'I', f'{mes}-28T12:00:00+00:00')\n"
    "    assert r['ok'], r\n"
    "print(pe.volcar(o, '2028-12-28T12:00:01+00:00'))\n")
salida = subprocess.run([sys.executable, "-I", "-c", gen], cwd=str(viejo), capture_output=True, text=True)
assert salida.returncode == 0, salida.stderr[-800:]
texto = salida.stdout.strip()
esq = json.loads(texto)["esquema"]
directo = pe.cargar(texto)
m = mg.migrar(texto, "2028-12-29T10:00:00+00:00", "QA r02 de T-76: estado genuino de V0.71")
om = None
if m["ok"]:
    rr = pe.cargar(m["texto"]) if "texto" in m else {"ok": True, "orquestador": m.get("orquestador")}
    om = rr.get("orquestador")
inf = om.informe_sombra() if om else None
ok_mig = bool(m["ok"] and om is not None and om.integridad() == [] and m.get("migraciones") == ["MIG-009"]
              and inf and inf["comparaciones"] == 25 and inf["ultima"]["mes"] == "2028-12")
sonda("M4_MIG009_no_migra_un_estado_de_V071_con_su_sombra", not (esq == mg.ESQUEMA_V0_71 and not directo["ok"] and ok_mig),
      f"esquema V0.71={esq == mg.ESQUEMA_V0_71}; cargar sin migrar: {directo['codigo']}; migrar: {m['codigo']} {m.get('migraciones')}; "
      f"integridad {om.integridad() if om else None}; comparaciones {inf and inf['comparaciones']}, la última {inf and inf['ultima']['mes']} "
      f"({inf and inf['ultima']['veredicto']}); O-41 heredados {sum(a['codigo'] == 'O-41' for a in om.avisos) if om else None}")

# ---------------------------------------------------------------- M5: tras migrar, la sombra sigue: O-42, siguiente comparación y O-41
if om:
    b = om.barrer("2029-02-01T06:00:00+00:00")   # 2029-01 terminado y sin comparar
    n42 = sum(a["codigo"] == "O-42" for a in om.avisos)
    r_ind = om.comparar_sombra("2029-01", 900.0, 100.0, 101.0, 101.0, 0.0, "I", "2029-02-01T07:00:00+00:00")
    r_sig = om.comparar_sombra("2029-01", 900.0, 100.0, 100.0, 101.0, 0.0, "I", "2029-02-01T07:00:00+00:00")
    n41_antes = sum(a["codigo"] == "O-41" for a in om.avisos)
    sonda("M5_tras_migrar_no_sigue_bien", not (n42 == 1 and r_sig["ok"] and r_sig["veredicto"] == "PROPONER_PASIVA"),
          f"O-42 {n42}; índice del inicio 101 (en V0.71 cambió en el mes 3): {r_ind['codigo']}; con 100: {r_sig['codigo']} {r_sig.get('veredicto')}; "
          f"O-41 tras la comparación {n41_antes} (no se repite: el anterior ya era PROPONER_PASIVA)")
    # el índice del inicio heredado: la primera comparación de V0.71 fija 100, aunque la del mes 3 dijo 101
    sonda("M5b_el_indice_del_inicio_heredado_es_ambiguo", om.sombra["entradas"][3]["inflacion_inicio"] != om.sombra["entradas"][1]["inflacion_inicio"],
          f"en el estado de V0.71 las comparaciones llevan índices del inicio {sorted({x['inflacion_inicio'] for x in om.sombra['entradas'] if x['tipo'] == 'COMPARACION'})}; "
          "la V0.73 toma el de la primera (bajo: V0.71 no llegó a operar)")

# ---------------------------------------------------------------- M6: V0.71 con inicio en huso local: el recuento de meses cambia al migrar
gen2 = (
    "import sys; sys.path.insert(0, 'validador'); sys.path.insert(0, 'pruebas')\n"
    "import persistencia as pe\n"
    "from pruebas_orquestador import nuevo\n"
    "o = nuevo()\n"
    "assert o.iniciar_sombra(1000.0, 100.0, 'OPERADOR', '2026-12-01T00:30:00+01:00')['ok']\n"
    "assert o.comparar_sombra('2027-01', 900.0, 100.0, 100.0, 100.0, 0.0, 'I', '2027-02-01T00:00:00+00:00')['ok']\n"
    "print(pe.volcar(o, '2027-02-01T00:00:01+00:00'))\n")
s2 = subprocess.run([sys.executable, "-I", "-c", gen2], cwd=str(viejo), capture_output=True, text=True)
assert s2.returncode == 0, s2.stderr[-800:]
m2 = mg.migrar(s2.stdout.strip(), "2027-02-01T00:00:02+00:00", "QA r02 de T-76: inicio en huso local")
o2 = pe.cargar(m2["texto"])["orquestador"] if m2["ok"] and "texto" in m2 else m2.get("orquestador")
if o2 is None:
    print("M6 migrar:", m2.get("codigo"), m2.get("motivo"), pe.cargar(m2.get("texto") or "{}").get("motivo") if m2["ok"] else "")
    sys.exit(0)
r = o2.comparar_sombra("2027-02", 900.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-03-01T06:00:00+00:00")
ms = [x["meses"] for x in o2.sombra["entradas"] if x["tipo"] == "COMPARACION"]
sonda("M6_recuento_de_meses_salta_tras_migrar_un_inicio_en_huso_local", ms != [1, 2],
      f"meses anotados {ms} (V0.71 contó el mes 1 desde 2026-12 en texto local; la V0.73 cuenta desde 2026-11 en UTC)")

print(f"\n{sum(1 for _, c in RES if c)} FALLA de {len(RES)} sondas")
