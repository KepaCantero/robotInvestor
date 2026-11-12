"""QA r01 de T-100 (V0.76): mutantes nuevos de las correcciones de la V0.76 contra las baterías de la sombra y del embudo.

Copia validador/, pruebas/ y esquemas/ a una carpeta temporal (no toca el repositorio), aplica cada mutante, ejecuta la batería que
le toca y dice MUERTO (la batería falla, bien), VIVO (la batería pasa con el código cambiado) o NO APLICA (el texto no aparece una
sola vez). Termina con 0.
Uso (desde la raíz del repositorio): .venv/bin/python -I .docs/tickets/T-100/revisores/r01_03_mutantes.py [ruta del marco]
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
O = "validador/orquestador.py"
SOMBRA, EMBUDO = "pruebas/pruebas_sombra_t76.py", "pruebas/pruebas_embudo_sequia_t75.py"

MUTANTES = [
    # T-76 H-17: la referencia
    ("N01_sin_rama_O03_todo_es_duplicado", O, SOMBRA,
     'if previo["tipo"] == tipo and previo["importe_eur"] == float(importe_eur):', "if True:"),
    ("N02_contenido_igual_solo_por_tipo", O, SOMBRA,
     'if previo["tipo"] == tipo and previo["importe_eur"] == float(importe_eur):', 'if previo["tipo"] == tipo:'),
    ("N03_contenido_igual_solo_por_importe", O, SOMBRA,
     'if previo["tipo"] == tipo and previo["importe_eur"] == float(importe_eur):', 'if previo["importe_eur"] == float(importe_eur):'),
    ("N04_conflicto_sin_kill_switch", O, SOMBRA,
     '            self._activar_kill(f"referencia {ref} de la sombra repetida con otro contenido", "ORQUESTADOR", ahora)\n', ""),
    ("N05_conflicto_sin_aviso_O03", O, SOMBRA,
     '            self._aviso("O-03", f"la referencia {ref} de un movimiento de la sombra se repite con otro tipo o importe", ahora)\n', ""),
    ("N06_referencia_en_blanco_admitida", O, SOMBRA, "if not (isinstance(ref, str) and ref.strip()):", "if not isinstance(ref, str):"),
    ("N07_referencia_no_se_guarda", O, SOMBRA, '"ahora": ahora, "ref": ref}', '"ahora": ahora}'),
    ("N08_duplicado_rechazado_ok_false", O, SOMBRA,
     'return _r(True, "O-02", f"el movimiento {ref} ya está replicado', 'return _r(False, "O-02", f"el movimiento {ref} ya está replicado'),
    ("N09_busca_solo_el_mismo_tipo", O, SOMBRA,
     'x["tipo"] in sb.TIPOS_MOVIMIENTO and x.get("ref") == ref', 'x["tipo"] == tipo and x.get("ref") == ref'),
    ("N10_sin_busqueda_de_previo", O, SOMBRA,
     'previo = next((x for x in self.sombra["entradas"] if x["tipo"] in sb.TIPOS_MOVIMIENTO and x.get("ref") == ref), None)', "previo = None"),
    ("N11_referencia_opcional", O, SOMBRA, 'return _no("O-01", "falta la referencia del movimiento en el intermediario (ref)")', "pass"),
    ("N12_sin_control_de_retirada_mayor_previo_a_T100", O, SOMBRA,
     "        if sb.estado_sombra(self.sombra[\"entradas\"] + [e], float(precio_indice), _dt(ahora)) is None:\n"
     "            return _no(\"O-06\", \"la retirada es mayor que lo que tiene la sombra\")\n",
     ""),
    ("N13_conflicto_fija_el_reloj", O, SOMBRA,
     'return _no("O-03", "la misma referencia de movimiento con otro tipo o importe")',
     'return _no("O-03", "la misma referencia de movimiento con otro tipo o importe", reloj_firme=True)'),
    ("N14_referencia_normalizada_strip_correccion_sugerida_debe_vivir", O, SOMBRA, "    previo = next((x for x in", "    ref = ref.strip()\n        previo = next((x for x in"),
    # T-76 H-19: el barrido con el registro roto
    ("N15_barrer_sin_kill", O, SOMBRA,
     '            self._activar_kill("integridad rota en SOMBRA", "ORQUESTADOR", ahora)\n', ""),
    ("N16_barrer_calcula_lo_pendiente_igual", O, SOMBRA,
     "falta = None if sombra_rota else self.comparaciones_sombra_pendientes(ahora)", "falta = self.comparaciones_sombra_pendientes(ahora)"),
    ("N17_barrer_kill_solo_si_el_aviso_es_nuevo", O, SOMBRA,
     '            self._activar_kill("integridad rota en SOMBRA", "ORQUESTADOR", ahora)\n            if len(self.avisos) > n0:\n',
     '            if len(self.avisos) > n0:\n                self._activar_kill("integridad rota en SOMBRA", "ORQUESTADOR", ahora)\n'),
    # T-75 H-15: el reinicio del veto en el embudo (los dos sitios por separado)
    ("N18_embudo_sin_reinicio_fuera_del_periodo", O, EMBUDO,
     "                        if nuevo_analisis:\n                            veto = None\n                        continue",
     "                        continue"),
    ("N19_embudo_sin_reinicio_dentro_del_periodo", O, EMBUDO,
     "                    if nuevo_analisis:\n                        veto = None\n                if d0",
     "                if d0"),
    ("N20_embudo_reinicio_antes_de_contar_la_salida", O, EMBUDO,
     '                    if x["hasta"] == "VALIDADA":   # la clave es el análisis',
     '                    if nuevo_analisis:\n                        veto = None\n                    if x["hasta"] == "VALIDADA":   # la clave es el análisis'),
    ("N21_embudo_nuevo_analisis_incluye_anotaciones_iguales", O, EMBUDO,
     'nuevo_analisis = x["desde"] != x["hasta"] and x["hasta"] in ("VALIDADA", "EN_ANALISIS")',
     'nuevo_analisis = x["hasta"] in ("VALIDADA", "EN_ANALISIS")'),
    ("N22_embudo_solo_VALIDADA_es_analisis_nuevo", O, EMBUDO,
     'nuevo_analisis = x["desde"] != x["hasta"] and x["hasta"] in ("VALIDADA", "EN_ANALISIS")',
     'nuevo_analisis = x["desde"] != x["hasta"] and x["hasta"] == "VALIDADA"'),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="r01_t100_mut_"))
    try:
        for d in ("validador", "pruebas", "esquemas"):
            shutil.copytree(MARCO / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__"))
        orig = (tmp / O).read_text(encoding="utf-8")
        for bat in (SOMBRA, EMBUDO):
            b = subprocess.run([sys.executable, "-I", bat], cwd=tmp, capture_output=True, text=True, timeout=900)
            print(f"sin mutar {bat}: {'PASA' if b.returncode == 0 else 'FALLA'}")
        vivos = []
        for nombre, f, bat, viejo, nuevo in MUTANTES:
            n = orig.count(viejo)
            if n != 1:
                print(f"NO APLICA {nombre}: el texto aparece {n} veces")
                continue
            (tmp / f).write_text(orig.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", bat], cwd=tmp, capture_output=True, text=True, timeout=900)
            (tmp / f).write_text(orig, encoding="utf-8")
            vivo = r.returncode == 0
            fallan = [ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith(("FALLA", "FAIL")) and len(ln.split()) > 1]
            vivos += [nombre] if vivo else []
            print(f"{'VIVO  ' if vivo else 'MUERTO'} {nombre}  {'' if vivo else fallan[:3] or r.stderr.strip().splitlines()[-1:]}")
        print(f"\n{len(vivos)} vivos de {len(MUTANTES)}: {vivos}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
