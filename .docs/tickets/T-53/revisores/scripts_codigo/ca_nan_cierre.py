"""HT-01: un cierre no numérico ('-', '1.234,5') pasa el dropna (se hace antes de la conversión) y queda como NaN."""
import tempfile, pathlib, math
from bloque_a.herramientas.ht01_datos import ProveedorCSV
d = pathlib.Path(tempfile.mkdtemp(dir="."))
(d / "XYZ.csv").write_text("fecha,cierre\n2026-06-01,100\n2026-06-02,101\n2026-06-03,-\n", encoding="utf-8")
(d / "ABC.csv").write_text("fecha,cierre,fecha_publicacion\n2026-06-01,1,\n2026-06-02,2,2026-07-01\n2026-06-03,3,31/06/2026\n", encoding="utf-8")
p = ProveedorCSV(d); p.fijar_as_of("2026-06-05")
f, v = p.valor_en("XYZ", "2026-06-05")
print("valor_en XYZ:", f.date(), v, "-> NaN:", math.isnan(v))
x = v / 100 - 1
print("evaluador: o = int(x > 0) =", int(x > 0.0), "(se resolvería NO_OCURRIDO con un dato inválido)")
print("ABC visible con as_of 2026-06-05:", list(p.cierres("ABC").items()))
