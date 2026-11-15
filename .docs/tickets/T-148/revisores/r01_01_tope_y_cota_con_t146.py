"""QA r01 de T-148 (revisor) · integración del estimador de coste con T-146 (`consumo.ReservaLlamada`).

Uso, desde la raíz de la copia:
  .venv/bin/python -I .docs/tickets/T-148/revisores/r01_01_tope_y_cota_con_t146.py <medida divisas> <medida 12 tipos> <doce.yaml> <trabajo>
(las medidas, de `medir_consumo_a.py`; `doce.yaml`, `perfiles.activos` con los doce). Sin red ni coste.

Comprueba:
  A. el tope del encargo (S4b) de cada bolsa, con 1 y con 12 tipos, frente al mayor mensaje que `ReservaLlamada` deja
     salir de verdad en esa bolsa vacía con la ampliación máxima (búsqueda binaria), con y sin herramienta de búsqueda;
  B. `--sin-t146`, `--con-t146` y por defecto, y las dos cifras del README (28,04 y 46,08 USD);
  C. que la cota «solo los límites» (con T-146) es una cota del gasto de la bolsa cuando la búsqueda trae lectura: una
     petición admitida con la bolsa casi llena y búsquedas que leen;
  D. `--estado` con F10 manipulado (un tipo ajeno, repetido, vacío) y estado inexistente: fallan cerrado.
Imprime OK / HALLAZGO / OBS por caso y termina con 1 si hay algún hallazgo."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada
from bloque_a.llm import Uso

M_DIV, M_12, DOCE, TRABAJO = (Path(x).resolve() for x in sys.argv[1:5])
TRABAJO.mkdir(parents=True, exist_ok=True)
EST = RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py"
spec = importlib.util.spec_from_file_location("estimar_coste_ciclo_a", EST)
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)
hallazgos = 0


def caso(nombre, ok, detalle="", obs=False):
    global hallazgos
    hallazgos += (not ok) and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""))


# ---------------------------------------------------------------- A. el tope del encargo frente a la reserva del código
def mayor_admitido(cfg, base, herramientas=None):
    """El mayor número de tokens de mensaje (aprox. 3,6 caracteres) que sale en una bolsa vacía de `base` UC cuyo límite
    es el de la ampliación máxima."""
    p = cfg["presupuesto_uc"]
    limite = base * (1 + max(p["ampliacion_sin_autorizacion"], p["ampliacion_max_autorizable"]))
    base_sin = limite / (1 + p["ampliacion_sin_autorizacion"])

    def sale(tok):
        g = ReservaLlamada(Presupuesto({"B": base_sin}, cfg), "B", Contabilidad(cfg), "AG-11")
        return g.reservar([], [{"role": "user", "content": "a" * int(tok * 3.6)}], herramientas, 12000) is not None
    lo, hi = 0, 10_000_000
    while hi - lo > 50:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if sale(mid) else (lo, mid)
    return lo


for etiqueta, medida, cfg_ruta in (("divisas", M_DIV, None), ("12 tipos", M_12, DOCE)):
    cfg = est._config(str(cfg_ruta) if cfg_ruta else None)
    tarifa = __import__("yaml").safe_load((EJ / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))
    llamadas = json.loads((medida / "llamadas.json").read_text(encoding="utf-8"))
    c = est.cota_ciclo(llamadas, cfg, tarifa["precios_por_millon"], 10.0, 1.35)
    p = cfg["presupuesto_uc"]
    n = len(c["tipos"])
    bases = {"tipo (N2)": p["N2"], "COMUN": max(p["fraccion_minima_comun"] * p["ciclo_semanal_max"], p["ciclo_semanal_max"] - n * p["N1"])}
    for nombre, base in bases.items():
        clave = c["tipos"][0] if nombre.startswith("tipo") else "COMUN"
        tope = c["encargo_max_por_bolsa"][clave]
        real = mayor_admitido(cfg, base)
        web = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
        real_web = mayor_admitido(cfg, base, web)
        caso(f"A {etiqueta}, bolsa {nombre}: el tope cubre lo que la reserva deja salir y es ajustado",
             real <= tope and real >= 0.99 * tope and real_web <= tope,
             f"tope {tope:,.0f} · admitido {real:,} (con búsqueda {real_web:,})")
    # la COMÚN real: con los tipos en N2 (C1 con cambio material) la COMÚN es 240 − 18·n; el estimador usa 240 − 5·n (más holgada)
    caso(f"A {etiqueta}: la COMÚN del estimador no es menor que la del ciclo en N1 o N2", bases["COMUN"] >= max(
        p["fraccion_minima_comun"] * p["ciclo_semanal_max"], p["ciclo_semanal_max"] - n * p["N2"]))

# ---------------------------------------------------------------- B. las opciones y las cifras del README
def cota(medida, *extra):
    r = subprocess.run([sys.executable, str(EST), str(medida), *extra], capture_output=True, text=True, check=False, cwd=EJ)
    linea = next((x for x in r.stdout.splitlines() if x.startswith("Cota superior del ciclo")), "")
    return r.returncode, linea, r.stdout


rc0, d_def, _ = cota(M_DIV)
_, d_con, _ = cota(M_DIV, "--con-t146")
_, d_sin, out_sin = cota(M_DIV, "--sin-t146")
_, d_ambas, _ = cota(M_DIV, "--sin-t146", "--con-t146")
_, t_def, out_t = cota(M_12, "--config", str(DOCE))
_, t_sin, _ = cota(M_12, "--config", str(DOCE), "--sin-t146")
caso("B divisas: por defecto = --con-t146 = 28,04 USD", rc0 == 0 and d_def == d_con and " 28.04 USD" in d_def, d_def[:60])
caso("B 12 tipos: por defecto 46,08 USD (por presupuesto)", " 46.08 USD" in t_def and "por presupuesto  46.08" in out_t, t_def[:60])
caso("B --sin-t146 da la cota de antes (más holgada) con su desglose", "última llamada de cada bolsa" in out_sin
     and float(t_sin.split()[4]) > 46.08, t_sin[:60])
caso("B --sin-t146 y --con-t146 a la vez: se rechaza o se dice cuál manda", d_ambas != d_sin,
     "se aceptan las dos y manda --sin-t146 en silencio", obs=True)

# ---------------------------------------------------------------- C. ¿«solo los límites» acota la lectura de las búsquedas?
cfg = cargar_config()
base = 18.0
pres = Presupuesto({"DIV": base}, cfg)
cont = Contabilidad(cfg)
limite = pres.limite("DIV")
# se gasta casi toda la bolsa y sale una última petición con búsqueda que cabe en su peor caso reservado
g = ReservaLlamada(pres, "DIV", cont, "AG-14")
web = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
mensaje = [{"role": "user", "content": "a" * int(8000 * 3.6)}]
peor = ReservaLlamada(Presupuesto({"DIV": base}, cfg), "DIV", cont, "AG-14")
peor.reservar([], mensaje, web, 4000)
pres.consumido["DIV"] = limite - peor.peor_total - 0.01   # cabe justo su peor caso reservado
mt = g.reservar([], mensaje, web, 4000)
lectura = 5 * 8000   # cinco búsquedas que leen 8 000 tokens cada una: la API los cobra como entrada de esa misma petición
real = Uso(entrada=8000 + lectura, salida=mt or 0, busquedas_web=5)
g.pagar(real)
g.cerrar()
pres.consumido["DIV"] += cont.uc_de(real)   # lo que hace `Bloque._cargar` después de `cerrar`
pasa = pres.consumido["DIV"] - limite
caso("C con T-146 la bolsa no pasa de su límite aunque la búsqueda lea (lo que da por hecho «solo los límites»)", pasa <= 1e-9,
     f"admitida={mt is not None}; la bolsa acaba {pasa:+.2f} UC sobre su límite ({limite:.2f}); el estimador imprime "
     f"«{'con T-146, el presupuesto acota también lo que lee cada búsqueda' if 'acota también' in t_def else '?'}»")

# ---------------------------------------------------------------- D. --estado manipulado
for nombre, p02 in (("tipo ajeno", ["DIV", "XX"]), ("repetido", ["DIV", "DIV"]), ("DIV y MON", ["DIV", "MON"])):
    estado = TRABAJO / f"estado_{nombre.replace(' ', '_')}"
    estado.mkdir(parents=True, exist_ok=True)
    try:
        Almacen(estado).escribir("F10", "OPERADOR", {"tipo_entrada": "PARAMETRO", "param_id": "P-02", "valor_vigente": p02,
                                                     "regimen": "SERVICIO"})
    except Exception as e:   # noqa: BLE001
        caso(f"D --estado con P-02 {nombre}", False, f"no se pudo preparar el estado: {type(e).__name__}: {e}", obs=True)
        continue
    rc, linea, out = cota(M_DIV, "--estado", str(estado))
    esperado = 0 if p02 == ["DIV", "MON"] else 1
    ok = (rc == 0 and "Tipos de activo: DIV, MON" in out) if esperado == 0 else (rc != 0 and "Traceback" not in out)
    caso(f"D --estado con P-02 {nombre}", ok, f"código {rc} · {(linea or out.strip().splitlines()[-1] if out.strip() else '')[:90]}")
rc, _, out = cota(M_DIV, "--estado", str(TRABAJO / "no_existe"))
caso("D --estado inexistente falla cerrado y no lo crea", rc != 0 and not (TRABAJO / "no_existe").exists())

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
