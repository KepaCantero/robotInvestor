"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). Mutantes de lo que hizo T-97 en el marco común, aplicados de uno en uno a
una COPIA DESECHABLE del marco (su ruta debe contener «_mut»; nunca el árbol principal). Un mutante muere si alguna prueba falla.
Las pruebas de PRUEBAS son rutas relativas a la copia del marco; las de REVISOR son los scripts de este revisor (reciben la
copia como primer argumento).

Uso: python3 -I r01_mutantes.py <copia del marco con «_mut»> [<marco de la V0.73> [<estado_v073.json> <estado_v074.json>]] [--solo=M06,M25]
(el marco de la V0.73 es para r01_f_bordes_y_solo_endurece.py; los estados, de r01_genera_estado_v073.py, para r01_migracion_v073.py)
"""
import subprocess
import sys
from pathlib import Path

PRUEBAS = ["pruebas/pruebas_tanda2_t97.py", "pruebas/pruebas_parametros_doc_t83.py", "pruebas/pruebas_control_f_t22.py",
           "pruebas/pruebas_migraciones_t03.py"]
AQUI = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith("--solo=")]
SOLO = next((a[7:].split(",") for a in sys.argv[1:] if a.startswith("--solo=")), None)
COPIA = Path(ARGS[0]).resolve()
assert "_mut" in str(COPIA), "la copia debe llevar «_mut» en la ruta"
V073 = ARGS[1] if len(ARGS) > 1 else None
REVISOR = [[str(AQUI / "r01_tope_anual.py")], [str(AQUI / "r01_tipo_cambio_divisas.py")], [str(AQUI / "r01_envio_semana.py")]]
if V073:
    REVISOR.append([str(AQUI / "r01_f_bordes_y_solo_endurece.py"), "{copia}", V073])
if len(ARGS) > 3:
    REVISOR.append([str(AQUI / "r01_migracion_v073.py"), "{copia}", str(Path(ARGS[2]).resolve()), str(Path(ARGS[3]).resolve())])

CF, OR, MG = "validador/control_f.py", "validador/orquestador.py", "validador/migraciones.py"
MUTANTES = [
    ("M01_F14_max_en_vez_de_min", CF, 'tope_dia = min(pol["importe_max_dia_eur"], pol["importe_max_dia_pct"] / 100 * cap_total)',
     'tope_dia = max(pol["importe_max_dia_eur"], pol["importe_max_dia_pct"] / 100 * cap_total)'),
    ("M02_F14_sin_porcentaje", CF, 'tope_dia = min(pol["importe_max_dia_eur"], pol["importe_max_dia_pct"] / 100 * cap_total)',
     'tope_dia = pol["importe_max_dia_eur"]'),
    ("M03_F16_max_en_vez_de_min", CF, 'lim_sem = min(lim_sem, pol[SEMANA_PCT[sol["cartera"]]] / 100 * cap)',
     'lim_sem = max(lim_sem, pol[SEMANA_PCT[sol["cartera"]]] / 100 * cap)'),
    ("M04_F16_trading_con_la_clave_de_tactica", CF, '{"TRADING": "perdida_semana_max_pct_trading", "TACTICA": "perdida_semana_max_pct_tactica",',
     '{"TRADING": "perdida_semana_max_pct_tactica", "TACTICA": "perdida_semana_max_pct_tactica",'),
    ("M05_F16_menor_o_igual", CF, 'chk("F-16", ac["perdida_semana_eur"] < lim_sem,', 'chk("F-16", ac["perdida_semana_eur"] <= lim_sem,'),
    ("M06_al_enviar_sin_capital", OR, 'ctx, cf["entradas"]["cartera"]["capital_eur"])', 'ctx, None)'),
    ("M07_al_enviar_capital_invalido_admitido", CF, 'if cap is not None and not _num(cap, 0, True):', 'if False:'),
    ("M08_politica_sin_tope_100_de_los_pct", CF, '"importe_max_dia_pct", *SEMANA_PCT.values()))', '))'),
    ("M09_sin_capital_se_admite_el_encargo", OR, 'if p["coste_max_eur"] > 0 and (tope_a is None or ga + ra + p["coste_max_eur"] > tope_a):',
     'if p["coste_max_eur"] > 0 and (tope_a is not None and ga + ra + p["coste_max_eur"] > tope_a):'),
    ("M10_tope_anual_sin_reservas", OR, 'reservas = sum(max(0.0, en["coste_max"] - en["coste"]) for en in self.encargos.values() if en["estado"] == "EN_CURSO")\n        f = self.ultima_foto',
     'reservas = 0.0\n        f = self.ultima_foto'),
    ("M11_tope_anual_suma_todos_los_anios_salvo_el_actual", OR, 'if date.fromisoformat(f).year == anio)\n        reservas',
     'if date.fromisoformat(f).year != anio)\n        reservas'),
    ("M12_capital_declarado_manda_sobre_la_foto", OR, 'cap = f.get("capital_eur") if isinstance(f, dict) else self.cfg["capital_referencia_eur"]',
     'cap = self.cfg["capital_referencia_eur"] or (f.get("capital_eur") if isinstance(f, dict) else None)'),
    ("M13_tope_anual_mayor_o_igual_al_admitir", OR, 'ga + ra + p["coste_max_eur"] > tope_a)', 'ga + ra + p["coste_max_eur"] >= tope_a)'),
    ("M14_aviso_O43_solo_al_pasar", OR, 'if tope_a is not None and ga >= tope_a:', 'if tope_a is not None and ga > tope_a:'),
    ("M15_sin_aviso_O43", OR, 'alertas.append("O-43")', 'pass'),
    ("M16_tolerancia_siempre_la_general", OR,
     'return self.cfg["tolerancia_tipo_k_rel_principales"] if divisa in self.cfg["divisas_principales"] else self.cfg["tolerancia_tipo_k_rel"]',
     'return self.cfg["tolerancia_tipo_k_rel"]'),
    ("M17_tolerancia_invertida", OR, 'if divisa in self.cfg["divisas_principales"] else', 'if divisa not in self.cfg["divisas_principales"] else'),
    ("M18_contraste_con_la_tolerancia_general", OR, 'tol = self.tolerancia_tipo_k(div)', 'tol = self.cfg["tolerancia_tipo_k_rel"]'),
    ("M19_config_principales_mas_laxa_admitida", OR, '0 < c["tolerancia_tipo_k_rel_principales"] <= c["tolerancia_tipo_k_rel"]',
     '0 < c["tolerancia_tipo_k_rel_principales"] <= 0.5'),
    ("M20_config_EUR_admitido_como_principal", OR, 're.fullmatch(r"[A-Z]{3}", x) and x != "EUR"', 're.fullmatch(r"[A-Z]{3}", x)'),
    ("M21_config_capital_negativo_admitido", OR, '_num(c["capital_referencia_eur"]) and c["capital_referencia_eur"] > 0', '_num(c["capital_referencia_eur"])'),
    ("M22_MIG010_principales_sin_min", MG, 'cfg.setdefault("tolerancia_tipo_k_rel_principales", min(0.005, cfg.get("tolerancia_tipo_k_rel", 0.005)))',
     'cfg.setdefault("tolerancia_tipo_k_rel_principales", 0.005)'),
    ("M23_MIG010_pisa_la_version_propia", MG, 'if cfg.get("version_config") == "CFG-0.11.0":\n        cfg["version_config"] = "CFG-0.12.0"',
     'cfg["version_config"] = "CFG-0.12.0"'),
    ("M24_MIG010_tope_anual_distinto", MG, 'cfg.setdefault("tope_anual_gasto_pct_capital", 0.5)', 'cfg.setdefault("tope_anual_gasto_pct_capital", 5.0)'),
    ("M25_MIG010_semana_trading_mas_laxa", MG, '("perdida_semana_max_pct_trading", 4.0)', '("perdida_semana_max_pct_trading", 100.0)'),
    ("M26_MIG010_pisa_la_politica", MG, '            pol.setdefault(k, v)', '            pol[k] = v\n        pol["importe_max_dia_eur"] = 50000.0'),
    ("M27_defecto_tope_anual_1pct", OR, '"tope_anual_gasto_pct_capital": 0.5,', '"tope_anual_gasto_pct_capital": 1.0,'),
    ("M28_defecto_dia_pct_30", CF, '"importe_max_dia_pct": 25.0, "perdida_semana_max_pct_trading": 4.0,', '"importe_max_dia_pct": 30.0, "perdida_semana_max_pct_trading": 4.0,'),
]


def correr(cmd):
    try:
        return subprocess.run(cmd, cwd=COPIA, capture_output=True, text=True, timeout=900).returncode
    except subprocess.TimeoutExpired:
        return 99


vivos = []
for nombre, rel, viejo, nuevo in MUTANTES:
    if SOLO and nombre[:3] not in SOLO:
        continue
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    if original.count(viejo) != 1:
        print(f"{nombre}: NO APLICA (el texto aparece {original.count(viejo)} veces)")
        vivos.append(nombre)
        continue
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        quien = []
        for p in PRUEBAS:
            if correr([sys.executable, p]) != 0:
                quien.append(Path(p).name)
                break
        rev = []
        for r in REVISOR:
            cmd = [sys.executable, "-I", r[0], *([x.format(copia=COPIA) for x in r[1:]] if len(r) > 1 else [str(COPIA)])]
            if correr(cmd) != 0:
                rev.append(Path(r[0]).name)
        print(f"{nombre}: {'MUERE' if quien or rev else 'SOBREVIVE'} · baterías del marco: {quien or 'ninguna'} · revisor: {rev or 'ninguno'}", flush=True)
        if not quien and not rev:
            vivos.append(nombre)
    finally:
        ruta.write_text(original, encoding="utf-8")
print("SOBREVIVEN:", vivos)
