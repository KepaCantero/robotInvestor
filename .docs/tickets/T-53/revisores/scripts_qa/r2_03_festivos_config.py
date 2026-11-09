"""r2_03 · H-04: PS2 de H1 con la configuración de festivos vacía, ausente o mal formada, y bordes del calendario.
Se llama a Bloque._puertas con H1. Con festivos ausentes se espera el comportamiento previo (busday sin festivos:
más estricto, nunca más laxo). Con tipos inesperados se espera que no se relaje PS2 en silencio."""
import pathlib, tempfile
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque, _sesiones_entre

CASOS = [("Viernes Santo: sáb 2026-04-04, dato jue 02", "2026-04-04", "2026-04-02"),
         ("Navidad: sáb 2025-12-27, dato 24", "2025-12-27", "2025-12-24"),
         ("Lunes de Pascua: mar 2026-04-07, dato jue 02", "2026-04-07", "2026-04-02"),
         ("Lunes 2025-12-29, dato 24", "2025-12-29", "2025-12-24"),
         ("Dato con fecha del festivo: 2025-12-26, dato 25", "2025-12-26", "2025-12-25"),
         ("Año nuevo: vie 2027-01-01 es as_of, dato jue 31-12", "2027-01-01", "2026-12-31"),
         ("Control: mié 2026-06-10, dato dom 07", "2026-06-10", "2026-06-07")]


def bloque(festivos, borrar=False):
    cfg = cargar_config(extra={"modo": "backtest"})
    if borrar:
        cfg.pop("ps2_festivos", None)
    else:
        cfg["ps2_festivos"] = festivos
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    return Bloque(cfg, ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
                  MockClient(), tmp / "e", tmp / "s")


CONFIGS = [("por_defecto (YAML)", None, False),
           ("clave ausente", None, True),
           ("vacía {}", {}, False),
           ("None", None, False),
           ("fijos None", {"viernes_santo": True, "fijos": None}, False),
           ("fijos como texto '12-25'", {"viernes_santo": True, "fijos": "12-25"}, False),
           ("fijos con año '2025-12-25'", {"viernes_santo": False, "fijos": ["2025-12-25", "2025-12-26"]}, False),
           ("viernes_santo 'false' (texto)", {"viernes_santo": "false", "fijos": []}, False),
           ("fijos entero 1225", {"viernes_santo": True, "fijos": 1225}, False)]

for nombre, fest, borrar in CONFIGS:
    if nombre.startswith("por_defecto"):
        b = bloque(None); b.cfg["ps2_festivos"] = cargar_config()["ps2_festivos"]
    else:
        b = bloque(fest, borrar)
    fila = []
    for etq, as_of, dato in CASOS:
        try:
            fila.append(f"{b._puertas({'senales': {'fecha_dato': dato}}, 'N1', as_of, ['H1'])['PS2']}")
        except Exception as e:   # noqa: BLE001
            fila.append(f"EXC:{type(e).__name__}")
    print(f"{nombre:32s} -> " + " | ".join(fila))
print("casos:", [c[0] for c in CASOS])
# Bordes de la función: fechas con hora y zona, y orden invertido
for d0, d1 in [("2026-04-02 23:59:00+00:00", "2026-04-04 00:00:00+00:00"), ("2026-04-04", "2026-04-02"), ("2026-04-02", "2026-04-02")]:
    try:
        print("_sesiones_entre", d0, d1, "=", _sesiones_entre(d0, d1, cargar_config()["ps2_festivos"]))
    except Exception as e:   # noqa: BLE001
        print("_sesiones_entre", d0, d1, "EXC", type(e).__name__, e)
