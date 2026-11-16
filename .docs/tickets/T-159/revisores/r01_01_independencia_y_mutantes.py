"""QA r01 de T-159 · (1) las pruebas nuevas no dependen de ningún cambio del ejecutor y (2) mutantes propios del revisor.

(1) `git diff` de HEAD~1 a HEAD en el código del ejecutor y de las herramientas: solo puede tocar lo de T-160 (evaluador.py,
    motor/servicio.py y motor/operaciones.py). Después se extrae `bloque_a/` de HEAD~1 (sin T-160) en `<copia>/antes`, se le
    pone el `tests/test_t159_extremo_a_extremo.py` de HEAD y se ejecuta: tiene que pasar entero con el código anterior.
(2) Mutantes P02–P67 sobre el código que cada prueba (A) debería vigilar, en la copia desechable `<copia>` (con «qa31_» y
    «_mut» en la ruta y `bloque_a/` entero); cada uno contra la prueba de su PB. Vivo = la prueba no lo detecta.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-159/revisores/r01_01_independencia_y_mutantes.py <copia «qa31_…_mut»>
Termina con 1 si (1) falla, si un mutante no aplica o si vive uno.
"""
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
COPIA = Path(sys.argv[1]).resolve()
assert "qa31_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
PY = str(RAIZ / ".venv" / "bin" / "python")
PRUEBA = "tests/test_t159_extremo_a_extremo.py"
OR, SI, EVA, SE, SV = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("orquestacion", "sintesis", "evaluador", "seguimiento",
                                                                         "motor/servicio"))
H9 = "bloque_a/11_Ejecutor/bloque_a/herramientas/referencia/ht09_validador_g3.py"
MUTANTES = [
    ("P02", "pb02", "HT-03 no recibe la segunda pasada", OR,
     '"segunda_pasada": f.get("segunda_pasada") or {},\n                                  "anterior"', '"segunda_pasada": {},\n                                  "anterior"'),
    ("P03", "pb03", "PS3 da por buena una invertibilidad falsa", OR,
     '.get("universo_suficiente") is True and bool(f.get("indicador_seguimiento"))',
     '.get("universo_suficiente") is not None and bool(f.get("indicador_seguimiento"))'),
    ("P30", "pb30", "C08 solo advierte de un CALC- sin artefacto", H9,
     'R.bloqueo("C08", f"{ro}.calculos", f"{x} sin artefacto', 'R.advertencia("C08", f"{ro}.calculos", f"{x} sin artefacto'),
    ("P39", "pb39", "C12 solo advierte de un visual por debajo de 70", H9,
     'R.bloqueo("C12", informe_visual, f"Fernández-Huerta', 'R.advertencia("C12", informe_visual, f"Fernández-Huerta'),
    ("P41", "pb41", "apuestas independientes que no son los clústeres", SI, '"apuestas_independientes": len(clust),',
     '"apuestas_independientes": len(clust) + 1,'),
    ("P44", "pb44", "la nota no declara los NO_RESOLUBLE", EVA,
     '+ (f"; {len(no_res)} no resolubles excluidos y declarados" if no_res else "")', '+ ""'),
    ("P44b", "pb44", "el historial cuenta los contaminados", EVA,
     "        lst = [p for p in self.resueltos(as_of, solo_informe=True) if",
     "        lst = [p for p in self.resueltos(as_of, solo_informe=True, admisibles=False) if"),
    ("P47", "pb47", "el Motor sirve una ficha DOCUMENTADO", SV, 'return estado.startswith(("IMPLEMENTADO", "VALIDADO"))', "return True"),
    ("P52", "pb52", "con HT-09 caído, APTO por defecto", OR,
     '            res = sint.ht09_validar(self, paquete, extras, None)\n',
     '            try:\n                res = sint.ht09_validar(self, paquete, extras, None)\n            except Exception:\n'
     '                res = {"dictamen": "APTO", "comprobaciones": []}\n'),
    ("P67", "pb67", "el C6 no propone el envío", SE, 'return "PROPONER_ENVIO_A_B", "La opción vuelve', 'return "MANTENER", "La opción vuelve'),
]
# Equivalentes en el escenario de la prueba: su supervivencia no es un hallazgo
EQUIVALENTES = {
    "P44b": "con el cliente simulado ningún PRG lleva `contaminacion_posible` (PA-09 lo marca un backtest con modelo real); la "
            "exclusión la cubren las pruebas de T-66 (test_pa09_*), no PB-44",
}


def pytest(args, cwd):
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *args], cwd=cwd, capture_output=True, text=True,
                       timeout=3600)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1]


mal = 0
# ---------------------------------------------------------------- (1) independencia
cambiados = subprocess.run(["git", "-C", str(RAIZ), "diff", "--name-only", "HEAD~1", "HEAD", "--",
                            "bloque_a/11_Ejecutor/bloque_a", "bloque_a/10_Herramientas"], capture_output=True, text=True,
                           check=True).stdout.split()
de_t160 = {"bloque_a/11_Ejecutor/bloque_a/evaluador.py", "bloque_a/11_Ejecutor/bloque_a/motor/servicio.py",
           "bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py"}
print("código del ejecutor y de las herramientas cambiado en HEAD~1..HEAD:", cambiados)
if set(cambiados) - de_t160:
    print("  ¡cambia algo que no es de T-160!", sorted(set(cambiados) - de_t160))
    mal += 1
antes = COPIA / "antes"
if antes.exists():
    shutil.rmtree(antes)
antes.mkdir()
arch = subprocess.run(["git", "-C", str(RAIZ), "archive", "HEAD~1", "bloque_a"], check=True, capture_output=True).stdout
subprocess.run(["tar", "-x", "-C", str(antes)], input=arch, check=True)
shutil.copy(RAIZ / "bloque_a" / "11_Ejecutor" / PRUEBA, antes / "bloque_a" / "11_Ejecutor" / PRUEBA)
ok, ultima = pytest([PRUEBA], antes / "bloque_a" / "11_Ejecutor")
print(f"pruebas de T-159 con el ejecutor de HEAD~1 (sin T-160): {'PASAN' if ok else 'FALLAN'} · {ultima}")
mal += not ok
shutil.rmtree(antes)
# ---------------------------------------------------------------- (2) mutantes
ejec = COPIA / "bloque_a" / "11_Ejecutor"
ok, ultima = pytest([PRUEBA], ejec)
assert ok, f"las pruebas no pasan sin mutar: {ultima}"
vivos, no_aplica = [], []
for mid, k, desc, ruta, viejo, nuevo in MUTANTES:
    f = COPIA / ruta
    texto = f.read_text(encoding="utf-8")
    if texto.count(viejo) != 1:
        no_aplica.append(mid)
        print(f"{mid} NO APLICA ({texto.count(viejo)} apariciones): {desc}")
        continue
    f.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
    try:
        pasa, ultima = pytest([PRUEBA, "-k", k], ejec)
    finally:
        f.write_text(texto, encoding="utf-8")
    if pasa:
        vivos.append(mid)
    eq = f" [equivalente: {EQUIVALENTES[mid]}]" if mid in EQUIVALENTES else ""
    print(f"{mid} {'vivo' if pasa else 'muerto'}{eq} ({k}): {desc} · {ultima}")
reales = [m for m in vivos if m not in EQUIVALENTES]
print(f"\n{len(MUTANTES)} mutantes · muertos {len(MUTANTES) - len(vivos) - len(no_aplica)} · vivos {vivos} · no aplican {no_aplica}")
sys.exit(1 if mal or reales or no_aplica else 0)
