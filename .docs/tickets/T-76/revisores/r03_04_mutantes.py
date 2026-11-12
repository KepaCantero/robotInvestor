"""QA r03 de T-76 (V0.75): mutantes de una línea del código de la sombra contra `pruebas/pruebas_sombra_t76.py`.

Uso: python3 -I .docs/tickets/T-76/revisores/r03_04_mutantes.py [ruta del marco]
Copia validador/, pruebas/ y esquemas/ a una carpeta temporal (no toca el repositorio), aplica cada mutante en la copia, ejecuta la
batería y dice MUERTO (la batería falla, bien) o VIVO (la batería pasa con el código cambiado: falta una regresión). Termina con 0.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"

O, S = "validador/orquestador.py", "validador/sombra.py"
MUTANTES = [
    # H-10: valorar al cierre
    ("M01_todas_las_entradas_no_solo_hasta_el_cierre", O, '[x for x in L if _dt(x["ahora"]) <= cierre]', "L"),
    ("M02_coste_de_la_sombra_hasta_la_comparacion", O, 'float(precio_indice), cierre)\n', "float(precio_indice), a)\n"),
    ("M03_costes_de_analisis_hasta_la_comparacion", O, 'self._costes_analisis_desde(ini["ahora"], cierre)', 'self._costes_analisis_desde(ini["ahora"], a)'),
    ("M04_excluye_el_ultimo_microsegundo", O, 'if _dt(x["ahora"]) <= cierre]', 'if _dt(x["ahora"]) < cierre]'),
    ("M05_cierre_un_microsegundo_tarde", O, "tzinfo=timezone.utc) - timedelta(microseconds=1)   # H-10", "tzinfo=timezone.utc)   # H-10"),
    ("M06_costes_de_analisis_sin_el_dia_del_inicio", O, "if d0 <= date.fromisoformat(f) <=", "if d0 < date.fromisoformat(f) <="),
    # H-13: plazo de gracia, cuántos faltan y juicio
    ("M07_gracia_inclusiva", O, "if a < cierre + timedelta(days=gracia_dias):", "if a <= cierre + timedelta(days=gracia_dias):"),
    ("M08_gracia_un_dia_mas", O, "if a < cierre + timedelta(days=gracia_dias):", "if a < cierre + timedelta(days=gracia_dias + 1):"),
    ("M09_juicio_por_el_primer_mes_pendiente", O, 'sb.meses_entre(mes_ini, faltan[-1]) >=', 'sb.meses_entre(mes_ini, faltan[0]) >='),
    ("M10_juicio_estricto", O, 'faltan[-1]) >= PARAMETROS["i_meses_juicio_sombra"]', 'faltan[-1]) > PARAMETROS["i_meses_juicio_sombra"]'),
    ("M11_siempre_O42", O, 'cod = "O-44" if falta["juicio"] else "O-42"', 'cod = "O-42"'),
    ("M12_pendiente_desde_la_primera_comparacion", O, '[x["mes"] for x in L if x["tipo"] == "COMPARACION"] or [mes_ini])[-1]',
     '[x["mes"] for x in L if x["tipo"] == "COMPARACION"] or [mes_ini])[0]'),
    ("M13_pendiente_con_el_mes_de_inicio_local", O, 'mes_ini = _mes_utc(L[0]["ahora"])', 'mes_ini = L[0]["ahora"][:7]'),
    ("M14_motivo_sin_cuantos_faltan", O, "({falta['faltan']} mes(es) sin comparar)", "(1 mes(es) sin comparar)"),
    # H-12 y H-05: integridad antes de leer y O-13 en barrer
    ("M15_barrer_calla_el_registro_roto", O, "if not self.sombra_ok():   # T-76 (QA r02, H-12)", "if False:   # T-76 (QA r02, H-12)"),
    ("M16_iniciar_sin_precheck", O, 'err = self._sombra_precheck()   # T-76 (QA r02, H-12): la integridad antes de leer el registro\n        if err:\n            return err\n        if self.sombra["entradas"]:',
     'err = None\n        if err:\n            return err\n        if self.sombra["entradas"]:'),
    ("M17_mover_sin_precheck", O, 'err = self._sombra_precheck()   # T-76 (QA r02, H-12): la integridad antes de leer el registro\n        if err:\n            return err\n        if not self.sombra["entradas"]:\n            return _no("O-06", "la cartera sombra no está iniciada")\n        if tipo',
     'err = None\n        if err:\n            return err\n        if not self.sombra["entradas"]:\n            return _no("O-06", "la cartera sombra no está iniciada")\n        if tipo'),
    ("M18_comparar_sin_precheck", O, "err = self._sombra_precheck()   # QA r01, H-05", "err = None   # QA r01, H-05"),
    # H-11 y H-03: no finitos
    ("M19_iniciar_sin_unidades_finitas", O, 'if not sb.num_pos(float(importe_eur) / float(precio_indice)):   # H-11: las unidades', 'if False:   # H-11: las unidades'),
    ("M20_mover_sin_unidades_finitas", O, 'if not sb.num_pos(float(importe_eur) / float(precio_indice)):   # H-11: «no finito»', 'if False:   # H-11: «no finito»'),
    ("M21_estado_sin_isfinite", S, "return out if all(math.isfinite(v) for v in out.values()) else None", "return out"),
    ("M22_comparar_sin_isfinite", S, "return out if all(v is None or isinstance(v, bool) or math.isfinite(v) for v in out.values()) else None", "return out"),
    # H-02, H-06, H-07, H-08 y el juicio
    ("M23_compara_el_mes_en_curso", O, "if not mes < _mes_utc(ahora):", "if not mes <= _mes_utc(ahora):"),
    ("M24_mes_de_inicio_local", O, 'mes_ini = _mes_utc(ini["ahora"])', 'mes_ini = ini["ahora"][:7]'),
    ("M25_tolerancia_absoluta", S, "if u > unidades * (1 + 1e-12):", "if u > unidades + 1e-9:"),
    ("M26_indice_del_inicio_libre", O, 'if comps and float(inflacion_inicio) != comps[0]["inflacion_inicio"]:', "if False:"),
    ("M27_O41_cada_mes", O, '(not comps or comps[-1]["veredicto"] != "PROPONER_PASIVA")', "True"),
    ("M28_juicio_un_mes_tarde", S, "if meses < meses_juicio:", "if meses <= meses_juicio:"),
    ("M29_juicio_en_nominal", S, '"supera": robot_real > sombra_real}', '"supera": robot >= sombra["valor_eur"]}'),
    ("M30_anio_de_366_dias", S, "** (max(0.0, dias) / 365.0)", "** (max(0.0, dias) / 366.0)"),
    ("M31_coste_sin_tramos", S, "unidades *= _factor_coste((t - t_prev).total_seconds() / 86400.0, coste_anual_pct)", "pass"),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="r03_t76_mut_"))
    try:
        for d in ("validador", "pruebas", "esquemas"):
            shutil.copytree(MARCO / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__"))
        orig = {f: (tmp / f).read_text(encoding="utf-8") for f in (O, S)}
        base = subprocess.run([sys.executable, "-I", "pruebas/pruebas_sombra_t76.py"], cwd=tmp, capture_output=True, text=True)
        print(f"sin mutar: {'PASA' if base.returncode == 0 else 'FALLA'} ({base.stdout.strip().splitlines()[-2] if base.stdout.strip() else ''})")
        vivos = []
        for nombre, f, viejo, nuevo in MUTANTES:
            n = orig[f].count(viejo)
            if n != 1:
                print(f"NO APLICA {nombre}: el texto aparece {n} veces")
                continue
            (tmp / f).write_text(orig[f].replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", "pruebas/pruebas_sombra_t76.py"], cwd=tmp, capture_output=True, text=True, timeout=600)
            (tmp / f).write_text(orig[f], encoding="utf-8")
            vivo = r.returncode == 0
            vivos += [nombre] if vivo else []
            print(f"{'VIVO  ' if vivo else 'MUERTO'} {nombre}")
        print(f"\n{len(vivos)} vivos de {len(MUTANTES)}: {vivos}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
