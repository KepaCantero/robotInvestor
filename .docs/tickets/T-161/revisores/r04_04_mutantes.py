"""QA r04 de T-161 · Mutantes propios del revisor (U01–U08) sobre `guias.py`: lo que la r04 promete de las lecciones
(H-11 y H-15) y que M01–M52 (`mutantes_t161.py`) pueden no tocar.

Uso, desde la raíz: python .docs/tickets/T-161/revisores/r04_04_mutantes.py <copia desechable con «qa29_» y «_mut» y `bloque_a/`
entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Con `--scripts`, a cada vivo se le
pasa además `r04_02_integracion.py`. Termina con 1 si alguno no aplica o vive.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
AQUI = Path(__file__).resolve().parent
GU = "bloque_a/11_Ejecutor/bloque_a/guias.py"
PRUEBAS = ["tests/test_t161_guias.py", "tests/test_t161_r02.py", "tests/test_t161_r03.py", "tests/test_t161_r04.py",
           "tests/test_t158_guias.py", "tests/test_t126_pb26_pb48.py"]
MUTANTES = [
    ("U01", "las PRODUCTO vuelven a ser texto del código", GU,
     'TIPOS_TEXTO_DEL_CODIGO = ("PREDICTIVA", "CALIBRACION")', 'TIPOS_TEXTO_DEL_CODIGO = ("PREDICTIVA", "CALIBRACION", "PRODUCTO")'),
    ("U02", "las OPERATIVA del código son texto del código", GU,
     'TIPOS_TEXTO_DEL_CODIGO = ("PREDICTIVA", "CALIBRACION")', 'TIPOS_TEXTO_DEL_CODIGO = ("PREDICTIVA", "CALIBRACION", "OPERATIVA")'),
    ("U03", "no se respeta ambito.agente", GU,
     "if destinatarios is not None and (not isinstance(destinatarios, list) or agente not in destinatarios):",
     "if False:"),
    ("U04", "un ambito.agente que no es lista se da a todos", GU,
     "if destinatarios is not None and (not isinstance(destinatarios, list) or agente not in destinatarios):",
     "if isinstance(destinatarios, list) and agente not in destinatarios:"),
    ("U05", "una alteración posterior no impide dar la lección", GU,
     '        if alta.get("alterada"):\n', '        if False:\n'),
    ("U06", "solo se vigila el texto como dato de alta", GU,
     'CAMPOS_DE_ALTA = ("origen", "tipo", "ambito", "observacion", "recomendacion")',
     'CAMPOS_DE_ALTA = ("observacion", "recomendacion")'),
    ("U07", "las PRODUCTO del código no pasan el detector (se validan solo contra F6 4.4)", GU,
     "                if _texto_del_codigo(leccion):", '                if leccion.get("origen") == ORIGEN_DETERMINISTA:'),
    ("U08", "ningún tipo es texto del código (a los controles no llega nada)", GU,
     'TIPOS_TEXTO_DEL_CODIGO = ("PREDICTIVA", "CALIBRACION")', 'TIPOS_TEXTO_DEL_CODIGO = ()'),
]


def pasar(cmd, cwd) -> int:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True).returncode


def main() -> int:
    ej = COPIA / "bloque_a" / "11_Ejecutor"
    sin_aplicar, vivos = [], []
    for mid, que, rel, viejo, nuevo in MUTANTES:
        f = COPIA / rel
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
            sin_aplicar.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        try:
            muerto = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], ej) != 0
            por_script = None
            if not muerto and SCRIPTS:
                por_script = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                                    str(AQUI / "r04_02_integracion.py")], ej) != 0
        finally:
            f.write_text(original, encoding="utf-8")
        extra = "" if por_script is None else (" · muere con r04_02" if por_script else " · vive también con r04_02")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos con las pruebas del ticket; "
          f"vivos: {', '.join(vivos) or 'ninguno'}; sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or vivos else 0


if __name__ == "__main__":
    sys.exit(main())
