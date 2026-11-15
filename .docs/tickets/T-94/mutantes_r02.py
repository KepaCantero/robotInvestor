"""T-94 r02 · Mutantes del banco de medida: cada uno debe morir ante `pruebas_banco_medida.py`.

Trabaja en una copia de `.docs/scripts` en una carpeta temporal (nunca en el árbol principal) y sin la prueba de
integración sobre A, que necesita la raíz del repositorio. Uso: .venv/bin/python -B .docs/tickets/T-94/mutantes_r02.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PY = RAIZ / ".venv" / "bin" / "python"
MUTANTES = {
    "M01 borde del cero": ("if lo > 0:", "if lo >= 0:"),
    "M02 sin signo en el exceso": ("SIGNO[direccion] * (r - float(np.mean(cesta)))", "(r - float(np.mean(cesta)))"),
    "M03 sin precio final se estima con el último": ("if serie.empty or serie.index.max() < fin:", "if serie.empty:"),
    "M04 nivel ignorado": ("cola = (1.0 - nivel) / 2.0", "cola = 0.05"),
    "M05 azar sin semilla por fecha y clase": ('rng = random.Random(f"{semilla}|{fecha}|{clase}")', "rng = random.Random(semilla)"),
    "M06 momento CORTO elige como LARGO": ('candidatos = orden if f["direccion"] != "CORTO" else list(reversed(orden))', "candidatos = orden"),
    "M07 repeticiones contadas": ("elif clave in abiertas and abiertas[clave][0] > ini:", "elif False:"),
    "M08 ventana cerrada sigue bloqueando": ("abiertas[clave][0] > ini", "abiertas[clave][0] >= ini - pd.Timedelta(days=3650)"),
    "M09 remuestreo sin grupos": ("    if grupos is None:\n        idx = rng.integers(0, len(x), size=(n, len(x)))",
                                  "    if True:\n        idx = rng.integers(0, len(x), size=(n, len(x)))"),
    "M10 efectivas = n": ("return len(x) if grupos is None else len(set(grupos))", "return len(x)"),
    "M11 sin mínimo de efectivas": ("if min(efectivas) < min_efectivas:", "if False:"),
    "M12 cierres no positivos admitidos": ("malos = ~np.isfinite(v) | (v <= 0)", "malos = ~np.isfinite(v)"),
    "M13 no finitos admitidos": ("malos = ~np.isfinite(v) | (v <= 0)", "malos = v <= 0"),
    "M14 clase ajena admitida": ("if clase not in miembros:", "if False:"),
    "M15 símbolo de otra clase admitido": ("if clase_de.get(sim) != clase:", "if False:"),
    "M16 dirección desconocida admitida": ("if direccion not in DIRECCIONES:", "if False:"),
    "M17 zona horaria admitida": ("if serie.index.tz is not None:", "if False:"),
    "M18 azar recorta en silencio": ("if len(pool) < len(filas):", "if False:"),
    "M19 momento recorta en silencio": ("if len(puntos) < len(filas):", "if False:"),
    "M20 fuga sin efecto": ('if sin_veredicto and c["veredicto"] in ("mejor", "peor"):', "if False:"),
    "M21 caché fuera del coste": ('CAMPOS_ENTEROS = ("llamadas", "tokens_entrada", "tokens_salida", "tokens_cache_escritura", "tokens_cache_lectura")',
                                  'CAMPOS_ENTEROS = ("llamadas", "tokens_entrada", "tokens_salida")'),
    "M22 coste cero como sin dato": ("None if coste is None else round(coste / resueltas, 4)", "None if not coste else round(coste / resueltas, 4)"),
    "M23 experimento por ejecución": ("    if del_periodo:\n        return", "    if False:\n        return"),
    "M24 experimento ajeno admitido": ("        if distinto:\n            raise", "        if False:\n            raise"),
    "M25 fallo tras el titular sin anotar": ("    except BaseException as e:\n        if reg is not None:",
                                             "    except BancoError as e:\n        if reg is not None:"),
    "M26 verificar sin huella": ('if pre.get("huella") != h:', "if False:"),
    "M27 aviso de cliente siempre": ('    if cliente == "mock":\n        partes.append', '    if True:\n        partes.append'),
    "M28 huella citada de otro contenido": ("h = huella(prerregistro)", 'h = huella({**prerregistro, "tarde": True})'),
    "M29 parámetros sin validar": ("    if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)) or valor < minimo:",
                                   "    if False:"),
}


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="t94_mut_"))
    try:
        copia = tmp / ".docs" / "scripts"
        shutil.copytree(RAIZ / ".docs" / "scripts", copia, ignore=shutil.ignore_patterns("__pycache__", ".logs"))
        fichero = copia / "banco_medida.py"
        original = fichero.read_text(encoding="utf-8")
        vivos = []
        for nombre, (viejo, nuevo) in MUTANTES.items():
            if original.count(viejo) != 1:
                print(f"??    {nombre}: el patrón no aparece una sola vez")
                vivos.append(nombre)
                continue
            fichero.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([str(PY), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-k", "not integracion",
                                str(copia / "pruebas_banco_medida.py")], cwd=tmp, capture_output=True, text=True, check=False)
            muerto = r.returncode != 0
            print(("MUERE " if muerto else "VIVO  ") + nombre)
            if not muerto:
                vivos.append(nombre)
        fichero.write_text(original, encoding="utf-8")
        print(f"\n{len(vivos)} vivo(s) de {len(MUTANTES)}: {vivos}")
        return 1 if vivos else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
