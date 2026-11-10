"""QA r01 de T-76 (V0.71): sondas de diario (reproducción determinista), persistencia y MIG-008 desde un estado genuino de V0.70.

Uso (desde sistema_global/marco_comun_c, dentro del repositorio git): python3 -I entrega_claude/V0.71/qa/r01_sondas_diario_migracion.py
El estado de V0.70 se genera con el código del commit c4d0c5a (extraído con git archive a una carpeta temporal).
Cada sonda imprime CONFIRMADO (el fallo existe) o NO (el código se comporta bien).
"""
import json
import os
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
COMMIT_V070 = "c4d0c5a"


def sonda(nombre, confirmado, detalle=""):
    RES.append((nombre, confirmado))
    print(f"{'CONFIRMADO' if confirmado else 'NO':10s} {nombre}  {detalle}")


def mes_k(k):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a:04d}-{m:02d}-28T12:00:00+00:00"


tmp = Path(tempfile.mkdtemp(prefix="r01_t76_"))

# ---------------------------------------------------------------- D1: el diario reproduce la sombra exactamente
o = nuevo()
hasta(o, "EN_ANALISIS", 1)
assert o.registrar_gasto("EV-ENC-0001", 3.0, 1.0, AHORA)["ok"]
r = di.crear(o, str(tmp / "e.json"), str(tmp / "d.jsonl"), AHORA)
assert r["ok"], r
d = r["diario"]
assert d.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)["ok"]
assert d.movimiento_sombra("APORTE", 1100.0, 110.0, "G", AHORA)["ok"]
for k in range(1, 25):
    mes, t = mes_k(k)
    if k == 5:
        assert d.movimiento_sombra("RETIRADA", 500.0, 95.0, "OPERADOR", t)["ok"]
    rr = d.comparar_sombra(mes, 9000.0, 100.0 + k, 100.0, 100.0 + k / 2, 10.0, "I", t)
    assert rr["ok"], rr
vivo = json.dumps(d.orquestador.sombra, sort_keys=True)
avisos_vivos = [a["codigo"] for a in d.orquestador.avisos]
r2 = di.abrir(str(tmp / "e.json"), str(tmp / "d.jsonl"))
re_ = r2["diario"].orquestador if r2["ok"] else None
sonda("D1_el_diario_no_reproduce_la_sombra", not (r2["ok"] and json.dumps(re_.sombra, sort_keys=True) == vivo
                                                  and [a["codigo"] for a in re_.avisos] == avisos_vivos and re_.integridad() == []),
      f"abrir: {r2['codigo']} aplicadas={r2.get('aplicadas')} O-41 vivos={avisos_vivos.count('O-41')}")

# ---------------------------------------------------------------- D2: una comparación aceptada con NaN bloquea el diario y el guardado
o = nuevo()
r = di.crear(o, str(tmp / "e2.json"), str(tmp / "d2.jsonl"), AHORA)
d = r["diario"]
assert d.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
rc = d.comparar_sombra("2026-12", 1000.0, 1e308, 100.0, 100.0, 0.0, "I", "2026-12-28T12:00:00+00:00")
sig = d.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", "2026-12-28T13:00:00+00:00")
pt = d.punto("2026-12-28T14:00:00+00:00")
sonda("D2_comparacion_aceptada_con_NaN_deja_el_diario_sin_poder_seguir", rc["ok"] and not (sig["ok"] and pt["ok"]),
      f"comparar: {rc['codigo']}; operación siguiente: {sig['codigo']} {sig.get('motivo', '')[:70]}; punto: {pt['codigo']} {pt.get('motivo', '')[:70]}")

# ---------------------------------------------------------------- D3: MIG-008 desde un estado genuino de V0.70
viejo = tmp / "v070"
viejo.mkdir()
arch = subprocess.run(["git", "-C", str(MARCO), "archive", COMMIT_V070, "--", "."], capture_output=True, check=True).stdout
subprocess.run(["tar", "-x", "-C", str(viejo)], input=arch, check=True)
gen = (
    "import sys; sys.path.insert(0, 'validador'); sys.path.insert(0, 'pruebas')\n"
    "import persistencia as pe\n"
    "from pruebas_orquestador import AHORA, hasta, nuevo\n"
    "o = nuevo(); hasta(o, 'EN_ANALISIS', 1); assert o.registrar_gasto('EV-ENC-0001', 2.0, 1.0, AHORA)['ok']\n"
    "assert not hasattr(o, 'sombra')\n"
    "print(pe.volcar(o, AHORA))\n")
salida = subprocess.run([sys.executable, "-I", "-c", gen], cwd=str(viejo), capture_output=True, text=True)
assert salida.returncode == 0, salida.stderr[-500:]
texto = salida.stdout.strip()
esq = json.loads(texto)["esquema"]
directo = pe.cargar(texto)
m = mg.migrar(texto, "2026-11-10T10:00:00+00:00", "QA r01 de T-76: estado genuino de V0.70")
om = None
if m["ok"]:
    rr = pe.cargar(m["texto"]) if "texto" in m else {"ok": True, "orquestador": m.get("orquestador")}
    om = rr.get("orquestador")
ok_mig = bool(m["ok"] and om is not None and om.sombra == {"historial": [], "estado": "VIGENTE", "entradas": []}
              and om.integridad() == [] and m.get("migraciones") == ["MIG-008"])
r_ini = om.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-10T10:00:00+00:00") if om else {"codigo": None}
sonda("D3_MIG008_no_migra_bien_un_estado_de_V070", not (esq == mg.ESQUEMA_V0_70 and not directo["ok"] and ok_mig and r_ini.get("ok")),
      f"esquema V0.70={esq == mg.ESQUEMA_V0_70}; cargar sin migrar: {directo['codigo']}; migrar: {m['codigo']} {m.get('migraciones')} "
      f"claves={sorted(k for k in m if k not in ('texto',))}; luego iniciar: {r_ini.get('codigo')}")

# ---------------------------------------------------------------- D4: guardar y cargar un estado con la sombra tocada
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
assert o.comparar_sombra("2026-12", 900.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-28T12:00:00+00:00")["ok"]
o.sombra["entradas"][-1]["veredicto"] = "SUPERA"
t = pe.volcar(o, "2026-12-28T12:00:01+00:00")
c = pe.cargar(t)
sonda("D4_cargar_un_estado_con_la_sombra_tocada_no_avisa", not (c["ok"] is False or (c.get("orquestador") and c["orquestador"].kill is not None)),
      f"cargar: {c['codigo']} kill={(c.get('orquestador').kill is not None) if c.get('orquestador') else None}")

# ---------------------------------------------------------------- D5: el esquema V0.71 del catálogo lleva O-41 y los parámetros
esquemas = json.loads((MARCO / "validador" / "esquemas_codigo.json").read_text())
txt71 = json.dumps(esquemas.get(mg.ESQUEMA_V0_71) if isinstance(esquemas, dict) else esquemas, ensure_ascii=False)
sonda("D5_el_esquema_V071_registrado_no_cita_la_sombra", not ("sombra" in txt71 and pe.esquema_actual() == mg.ESQUEMA_V0_71),
      f"esquema_actual==V0.71: {pe.esquema_actual() == mg.ESQUEMA_V0_71}")

print(f"\n{sum(1 for _, c in RES if c)} confirmadas de {len(RES)} sondas")
