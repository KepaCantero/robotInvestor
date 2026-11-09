"""r07 · CA-10 (bóveda HT-01): flujos legítimos y fallos a mitad de operación.
(a) flujo CT-25 completo por `Credenciales` (solicitar → depositar ISO → estado) en backtest con as_of pasado;
(b) caducidad como dt.date; (c) índice heredado con caducidad no ISO; (d) chmod que falla: ¿queda intacto el archivo anterior?
(e) permisos finales y ausencia de temporales."""
import datetime as dt, json, os, pathlib, stat, tempfile
from unittest import mock
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.herramientas import ht01_boveda as hb
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
c = b.credenciales
s = c.solicitar("Proveedor X", "AG-16", "datos", "degradado", as_of="2024-03-01")
print("(a) solicitar:", s["estado"])
r = c.depositar(s["crd_id"], "VALOR-QA-1", "2025-01-31", as_of="2024-03-04")
print("(a) depositar:", r.get("estado"), "| estado a as_of 2024-03-04:", c.estado("Proveedor X")[0]["estado"],
      "| valor_para_herramienta(hoy=as_of):", "sí" if c.boveda.valor_para_herramienta(r["credencial_ref"], dt.date(2024, 3, 4)) else "None",
      "| sin hoy (fecha real 2026):", c.boveda.valor_para_herramienta(r["credencial_ref"]))
bv = hb.Boveda(tmp / "bv")
print("(b) date:", bv.depositar("S1", "V1", dt.date(2030, 1, 1))["caducidad"])
idx = json.loads((bv.carpeta / "indice.json").read_text()) if (bv.carpeta / "indice.json").exists() else None
nombre_idx = bv._indice.name
d = json.loads(bv._indice.read_text()); d["boveda://ht01/s1"]["caducidad"] = "31/12/2030"; bv._indice.write_text(json.dumps(d))
print("(c) índice heredado ilegible ->", bv.estado("boveda://ht01/s1")["estado"], "| listar no falla:", len(bv.listar()))
antes = bv._secretos.read_text()
with mock.patch.object(hb.os, "chmod", side_effect=PermissionError("simulado")):
    try:
        bv.depositar("S2", "V2", "2030-01-01"); print("(d) depositar con chmod fallido: ACEPTADO")
    except PermissionError as e:
        print("(d) depositar con chmod fallido: rechazado ->", e)
print("(d) secretos intacto:", bv._secretos.read_text() == antes, "| índice sin S2:", "boveda://ht01/s2" not in json.loads(bv._indice.read_text()))
print("(e) modo secretos:", oct(stat.S_IMODE(os.stat(bv._secretos).st_mode)), "| temporales:", [p.name for p in bv.carpeta.iterdir() if p.name.endswith(".tmp")])
