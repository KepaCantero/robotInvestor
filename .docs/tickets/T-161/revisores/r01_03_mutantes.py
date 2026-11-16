"""QA r01 de T-161 · Mutantes propios del revisor (Q01–Q14) sobre `guias.py` y `cli.py`: lo que T-161 promete y que M01–M14
(`mutantes_t161.py`) y G01–G30 (T-158/r01_04) no tocan.

Uso, desde la raíz: python .docs/tickets/T-161/revisores/r01_03_mutantes.py <copia desechable con «qa29_» y «_mut» y `bloque_a/`
entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Con `--scripts`, a cada vivo se le
pasa además `r01_02_integracion.py` de esta ronda. Termina con 1 si alguno no aplica o vive.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
AQUI = Path(__file__).resolve().parent
GU, CL = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("guias", "cli"))
PRUEBAS = ["tests/test_t161_guias.py", "tests/test_t158_guias.py", "tests/test_t126_pb26_pb48.py"]
MUTANTES = [
    ("Q01", "el receptor pasa al contexto todos los campos del ítem (campos extra de HA)", GU,
     '{"guia_id": g["guia_id"], **{k: copy.deepcopy(it[k]) for k in ("item_id", "tipo", "que_cambia", "donde_se_comprueba", "como_se_sabe")}}',
     '{"guia_id": g["guia_id"], **copy.deepcopy(it)}'),
    ("Q02", "el emisor guarda los campos extra del ítem", GU,
     '**{k: copy.deepcopy(it[k]) for k in CAMPOS_ITEM if k in it}}', '**{k: copy.deepcopy(v) for k, v in it.items() if k != "item_id"}}'),
    ("Q03", "sin AG-19 entre los agentes de control", GU, ',\n                      "AG-19": "auditoría"}', "}"),
    ("Q04", "el emisor no mira si el receptor es un control", GU,
     "        if receptor in AGENTES_DE_CONTROL:\n            return [", "        if False:\n            return ["),
    ("Q05", "el receptor no mira si es un control (solo el texto)", GU,
     "for c in [conflicto_para(it, agente)] if c]", "for c in [conflicto_del_item(it)] if c]"),
    ("Q06", "sin escritura en los campos descriptivos", GU, "        letras = _otra_escritura(crudo)\n", "        letras = []\n"),
    ("Q07", "la simulación no queda anotada en la GUI-", GU, "            if rechazos:\n                entrada[", "            if False:\n                entrada["),
    ("Q08", "el P3- se escribe aunque ya esté en HA", GU, "            if p3_id not in en_ha:\n", "            if True:\n"),
    ("Q09", "origen no se revisa", GU, '"como_se_sabe", "origen")   # T-161', '"como_se_sabe")   # T-161'),
    ("Q10", "la CLI siempre simula el fallo del emisor", CL, "simular_fallo_del_emisor=a.simular_fallo_del_emisor)",
     "simular_fallo_del_emisor=True)"),
    ("Q11", "la CLI ignora la opción de simulación", CL, "simular_fallo_del_emisor=a.simular_fallo_del_emisor)",
     "simular_fallo_del_emisor=False)"),
    ("Q12", "otra lengua solo en que_cambia", GU, "    idioma = IDIOMA.search(t)\n", "    idioma = IDIOMA.search(t) if estricto else None\n"),
    ("Q13", "sin lista de permitidos (nombrar un control siempre es conflicto)", GU,
     'and "RELAJA_CONTROL" not in familias and not _refuerza(t) else []', 'and "RELAJA_CONTROL" not in familias else []'),
    ("Q14", "la simulación se admite con cualquier cliente que tenga «generar»", GU,
     "not isinstance(self.b.cliente, MockClient):", 'not hasattr(self.b.cliente, "generar"):'),
]


def pasar(cmd, cwd) -> int:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3600).returncode


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
                                    str(AQUI / "r01_02_integracion.py")], ej) != 0
        finally:
            f.write_text(original, encoding="utf-8")
        extra = "" if por_script is None else (" · muere con r01_02" if por_script else " · vive también con r01_02")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos con las pruebas del ticket; "
          f"vivos: {', '.join(vivos) or 'ninguno'}; sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or vivos else 0


if __name__ == "__main__":
    sys.exit(main())
