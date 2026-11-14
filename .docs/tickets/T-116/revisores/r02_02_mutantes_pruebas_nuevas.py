"""QA r02 de T-116 · ¿Afirman lo que dicen las pruebas nuevas de la r02 (PB-21, 23, 37, 54)? Y el mutante A01 de la r01,
ahora contra TODAS las pruebas que el mapa cita para PB-23 (la r01 solo podía ejecutarlo contra la única que había).

Uso:  python r02_02_mutantes_pruebas_nuevas.py <copia desechable de bloque_a/11_Ejecutor, con «qa2_mut» en la ruta>
MUERTO = alguna prueba falla; VIVO = todas pasan.
"""
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
ej = Path(sys.argv[1]).resolve()
assert "qa2_mut" in str(ej) and (ej / "bloque_a" / "almacen.py").exists()
T = "tests/test_fase4_huecos.py::"
PB21 = T + "test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo"
PB23 = T + "test_pb23_los_tres_intentos_del_plan_se_rechazan_y_f4_no_cambia"
PB37 = T + "test_pb37_la_correccion_es_un_prg_nuevo_y_el_original_no_cambia"
PB54 = T + "test_pb54_cada_encargo_para_b_lleva_sus_once_campos_no_vacios"
U23 = "tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of"
A, S, C = "bloque_a/almacen.py", "bloque_a/sintesis.py", "bloque_a/contratos.py"
MUT = [
    ("A01", A, [U23, PB23], "PB-23: la escritura rechazada del Analizador en F4 SE GUARDA y después se rechaza (mutante de la r01)",
     '                self._incidencia_interna("ACCESO_FUERA_DE_MATRIZ", f"{archivo}: {motivo}", autor)\n            raise EscrituraFueraDeReserva(motivo)',
     '                self._incidencia_interna("ACCESO_FUERA_DE_MATRIZ", f"{archivo}: {motivo}", autor)\n            if archivo == "F4" and autor == "AG-02":\n                self.escribir("F4", "AG-10", {**entrada, "estado": "ABIERTO"})\n            raise EscrituraFueraDeReserva(motivo)'),
    ("N01", A, [PB23], "PB-23: el Evaluador puede escribir campos de alta (la afirmación)", "                if extra:\n", "                if False:\n"),
    ("N02", A, [PB23], "PB-23: Prospectiva puede escribir una resolución", 'if autor == "AG-10" and tipo != "ALTA":', 'if False:'),
    ("N03", A, [PB37], "PB-37: se admite una segunda ALTA del mismo PRG", "            if previas:\n", "            if False:\n"),
    ("N04", S, [PB54], "PB-54: el encargo sale sin preguntas para B",
     '"preguntas_para_B": _lista(f, "preguntas_para_B", [f"¿Qué activos del ámbito capturan mejor la tesis «{(op[\'tesis\'] or \'\')[:80]}»?"])}', '"preguntas_para_B": []}'),
    ("N05", C, [PB21], "PB-21: no se detectan credenciales en los mensajes",
     '    return list(dict.fromkeys(h[:6] + "…" for h in hallados))', '    return []'),
]
vivos = []
for mid, fich, pruebas, desc, viejo, nuevo in MUT:
    ruta = ej / fich
    original = ruta.read_text(encoding="utf-8")
    if original.count(viejo) != 1:
        print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}", flush=True)
        continue
    try:
        ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *pruebas], cwd=ej, capture_output=True, text=True)
        ult = (r.stdout + r.stderr).strip().splitlines()[-1][:90]
        print(f"{mid} · {'MUERTO' if r.returncode else 'VIVO  '} · {desc} · {ult}", flush=True)
        if r.returncode == 0:
            vivos.append(mid)
    finally:
        ruta.write_text(original, encoding="utf-8")
print("vivos: " + (", ".join(vivos) or "ninguno"))
