"""QA r01 de T-204: revisa `enmienda4_constitucion.patch` sin aplicarlo al repositorio.
- `git apply --check` en verde;
- el nombre de la enmienda que añade no es el de una propuesta pendiente (`.docs/diseno/enmienda_N/`);
- las decisiones D-NN y los cambios que añade no están ya reservados por una propuesta de `.docs/diseno/enmienda_*/`
  sin que INC-T204-01 lo declare;
- toda fila ratificada que reescribe (cambios o decisiones antiguas) lleva la anotación de la enmienda que la reduce;
- la línea de fecha de la cabecera cambia con la versión.
Uso (desde la raíz): python3 -I .docs/tickets/T-204/revisores/r01_04_parche_constitucion.py. Sale con 1 si hay casos."""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PARCHE = RAIZ / ".docs" / "tickets" / "T-204" / "enmienda4_constitucion.patch"
INC = (RAIZ / "docs" / "incidencias.md").read_text(encoding="utf-8")
inc01 = INC[INC.find("**INC-T204-01"):INC.find("**INC-T204-02")]
casos = []
r = subprocess.run(["git", "apply", "--check", str(PARCHE)], cwd=RAIZ, capture_output=True, text=True, check=False)
if r.returncode:
    casos.append(f"el parche no aplica: {r.stderr.strip()}")
lineas = PARCHE.read_text(encoding="utf-8").splitlines()
mas = [l[1:] for l in lineas if l.startswith("+") and not l.startswith("+++")]
menos = [l[1:] for l in lineas if l.startswith("-") and not l.startswith("---")]
propuestas = {int(p.name.split("_")[1]): p for p in (RAIZ / ".docs" / "diseno").glob("enmienda_*") if p.is_dir()}
for n in sorted({int(x) for l in mas for x in re.findall(r"\*\*enmienda (\d+)\*\*", l)}):
    if n in propuestas and "diseno/enmienda_" not in inc01:
        casos.append(f"«enmienda {n}» ya es el nombre de una propuesta pendiente ({propuestas[n].relative_to(RAIZ)}) y INC-T204-01 no lo dice")
reservados = {}
for p in propuestas.values():
    for f in p.glob("*.md"):
        for d in re.findall(r"^\| (D-\d+) \|", f.read_text(encoding="utf-8"), re.MULTILINE):
            reservados.setdefault(d, f.relative_to(RAIZ))
nuevas_d = {re.match(r"\| (D-\d+) \|", l).group(1) for l in mas if re.match(r"\| (D-\d+) \|", l)} - \
           {re.match(r"\| (D-\d+) \|", l).group(1) for l in menos if re.match(r"\| (D-\d+) \|", l)}
for d in sorted(nuevas_d):
    if d in reservados and str(reservados[d]) not in inc01:
        casos.append(f"{d} ya está reservada en {reservados[d]} y INC-T204-01 no lo dice")
for l in mas:
    m = re.match(r"\| (\d+|D-\d+) \|", l)
    if m and any(x.startswith(f"| {m.group(1)} |") for x in menos) and "enmienda" not in l:
        casos.append(f"la fila {m.group(1)} ratificada se reescribe sin anotar la enmienda que la reduce")
if any(l.startswith("# ") for l in mas) and not any(re.match(r"\w{3} \d+, \d{4} ·", l) for l in mas):
    casos.append("la cabecera pasa a otra versión y la línea de fecha no cambia")
print(f"{len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
