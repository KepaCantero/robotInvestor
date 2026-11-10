"""r01 (QA T-79): cobertura de la pasada PC3 (§5 del Documento 0 de la V0.67) frente a la Constitución V0.6.

1. Cada decisión D-28 a D-47 de la tabla del §15 y cada cambio 26 a 42 de la tabla «De la V0.4 a la V0.5/V0.6»: ¿lo cita
   alguna fila PC3 (por su D-xx o por «Cambio(s) NN»)?
2. Cada pieza de la Fase 1 en «Reparto por fases de la enmienda 2»: se lista para cotejarla a mano con las filas PC3.

Uso: python3 -I r01_pc3_cobertura.py <raíz del repositorio>
"""
import re
import sys
from pathlib import Path

R = Path(sys.argv[1]).resolve()
con = (R / "sistema_global/constitucion/Constitucion_Global.md").read_text(encoding="utf-8")
doc0 = (R / "sistema_global/documentos_0/V0.67_Integracion_del_kit_2_de_GLM.md").read_text(encoding="utf-8")
filas = [l for l in doc0.splitlines() if l.startswith("| PC3-")]
print(f"filas PC3: {len(filas)}")


def citado_d(n):
    return any(re.search(rf"\bD-{n}\b", f) for f in filas)


def citado_cambio(n):
    for f in filas:
        for a, b in re.findall(r"[Cc]ambios? (\d+)(?: a (\d+))?", f):
            if int(a) <= n <= int(b or a):
                return True
    return False


sin_d = []
for m in re.finditer(r"^\| (D-(\d+)) \| (.+?) \| RATIFICADO", con, re.M):
    n = int(m.group(2))
    if 28 <= n <= 47:
        ok = citado_d(n)
        print(f"{'citada   ' if ok else 'SIN FILA '} {m.group(1)}: {m.group(3)[:110]}")
        if not ok:
            sin_d.append(m.group(1))
sin_c = []
for m in re.finditer(r"^\| (\d+) \| (.+?) \|", con, re.M):
    n = int(m.group(1))
    if 26 <= n <= 42:
        ok = citado_cambio(n)
        if not ok:
            sin_c.append(n)
        print(f"{'citado   ' if ok else 'SIN FILA '} cambio {n}: {re.sub(r'[*]', '', m.group(2))[:110]}")
rep = con.split("**Reparto por fases de la enmienda 2.**", 1)[1]
f1 = re.search(r"^\| 1 \| (.+?) \|$", rep, re.M).group(1)
print("\nFase 1 del reparto de la enmienda 2 (cotejar con las filas PC3):")
for pieza in f1.split("; "):
    print(f"  - {pieza}")
print(f"\nRESULTADO r01 PC3: decisiones sin fila {sin_d}; cambios sin fila {sin_c}")
