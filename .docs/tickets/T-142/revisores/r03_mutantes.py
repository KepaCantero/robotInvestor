"""QA r01 de T-142: mutantes de `bloque_a/cadena_b.py` contra `tests/test_t142_cadena_b.py`, en una copia desechable.

Uso: <python> r03_mutantes.py <copia_desechable>   (la copia lleva bloque_a/, bloque_b/ y .docs/scripts/; se restaura el
módulo al terminar). Imprime MUERTO o VIVO por mutante."""
import subprocess, sys, shutil
from pathlib import Path
M = Path(sys.argv[1]); f = M / "bloque_a/11_Ejecutor/bloque_a/cadena_b.py"; orig = f.read_text()
muts = {
 "sin_validar_entrada": ('    if errores:\n        raise ErrorCadenaB("ENTRADA_B_INVALIDA"', '    if False:\n        raise ErrorCadenaB("ENTRADA_B_INVALIDA"'),
 "clave_inventada": ('    clave = tabla.get(simbolo)\n    if clave is None:', '    clave = tabla.get(simbolo, next(iter(tabla.values())))\n    if clave is None:'),
 "sin_x_clave": ('        encargo[CLAVE_EXTENSION_B] = clave\n', ''),
 "duplicada_toma_primera": ('    if len(hallados) > 1:', '    if len(hallados) > 99:'),
 "nivel_fijo": ('"nivel": defecto["nivel"]', '"nivel": "N2"'),
 "preguntas_de_A": ('"preguntas": [],', '"preguntas": list(entrada.get("preguntas_para_B") or []),'),
 "muta_paquete": ('    encargo = copy.deepcopy(entrada)', '    encargo = entrada'),
 "sin_tipos_sec": ('    tipos = [entrada["tipo_activo"]] + [t for t in opcion.get("tipos_secundarios") or [] if t != entrada["tipo_activo"]]', '    tipos = [entrada["tipo_activo"]]'),
 "ct04_sin_pet": ('not respuesta_b.get("pet_id")', 'False'),
 "enviables_todas": ('if o.get("siguiente_paso_sugerido") == SIGUIENTE_PASO_ENVIO]', ']'),
}
for n, (a, b) in muts.items():
    assert orig.count(a) == 1, n
    f.write_text(orig.replace(a, b))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t142_cadena_b.py"],
                       cwd=M / "bloque_a/11_Ejecutor", capture_output=True, text=True)
    print(f"{n:24} {'MUERTO' if r.returncode else 'VIVO'}  {r.stdout.strip().splitlines()[-1][:90]}")
f.write_text(orig)
