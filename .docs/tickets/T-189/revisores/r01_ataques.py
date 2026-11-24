"""QA r01 de T-189 (Claude). Ejecutar desde bloque_a/11_Ejecutor con la venv: python ../../.docs/tickets/T-189/revisores/r01_ataques.py
Imprime una línea por comprobación; «HALLAZGO» marca lo que contradice el criterio. Secretos ficticios partidos en dos cadenas."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
import conftest  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a.contratos import DatosSensibles, tipos_protegidos  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

U = cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO)


def bloque():
    return nuevo_bloque(Path(tempfile.mkdtemp()), U)


def linea(ok, texto):
    print(("ok       " if ok else "HALLAZGO ") + texto, flush=True)


# --- PB-10 · lista global
b = bloque(); b.fijar_fecha(AS_OF)
f10 = b.f10("2026-12-31")
print("P-02 inicial:", f10.get("P-02"), "· P-03 inicial:", f10.get("P-03"))
d = b.decision({"configuracion": {"horizontes": ["H1", "H2", "H3", "H4"]}}, AS_OF)
p03 = b.f10("2026-12-31").get("P-03")
linea(p03 == ["H1", "H2", "H3", "H4"],
      f"A1 quitar H5 con las clases por defecto: estado={d['estado']} P-03={p03} rechazos={[x['parametro'] for x in d['rechazos']]}")

b = bloque(); b.fijar_fecha(AS_OF)
d = b.decision({"configuracion": {"horizontes": ["H1", "H3"], "clases_activas": ["RV", "ALT"]}}, AS_OF)
params = [x["parametro"] for x in d["rechazos"]]
linea(any(p == "horizontes" or "H3" in p for p in params) or "P-03" in d["aplicado"],
      f"A2 H3 (válido para todas) se descarta sin motivo propio: aplicado={list(d['aplicado'])} rechazos={params}")

for v in ([], "H1", None, ["H1", "H1"], ["H3", "H3"]):
    b = bloque(); b.fijar_fecha(AS_OF)
    antes = b.f10("2026-12-31").get("P-03")
    try:
        d = b.decision({"configuracion": {"horizontes": v}}, AS_OF)
        print(f"   A3 horizontes={v!r}: estado={d['estado']} P-03 {antes} -> {b.f10('2026-12-31').get('P-03')} rechazos={d['rechazos']}")
    except Exception as e:  # noqa: BLE001
        linea(False, f"A3 horizontes={v!r}: excepción {type(e).__name__}: {e}")

# --- PB-21 · tipos protegidos
clave = "sk-ant-" + "api03-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
casos = {
    "IBAN ES": ("ES91 2100 " + "0418 4502 0005 1332", {"IBAN"}),
    "IBAN DE": ("DE89 3704 " + "0044 0532 0130 00", {"IBAN"}),
    "clave": (f"mi clave {clave}", {"CLAVE_API"}),
    "password": ('password: "' + 'hunter2' + 'hunter2"', {"CLAVE_API"}),
    "correo": ("escribe a fulano" + "@example.com", {"CORREO"}),
    "tarjeta": ("4111 1111 " + "1111 1111", {"TARJETA"}),
    "dni": ("mi DNI 1234" + "5678Z", {"IDENTIFICACION_PERSONAL"}),
    "telefono": ("llama al +34 600 " + "123 456", None),
}
for nombre, (texto, esperado) in casos.items():
    b = bloque()
    try:
        b.decision({"valoracion_informe": {"comentario": texto}}, AS_OF)
        print(f"   B {nombre}: no se rechaza")
        continue
    except DatosSensibles:
        pass
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"][-1]
    volcado = "".join(p.read_text(errors="ignore") for p in Path(b.almacen.base if hasattr(b.almacen, "base") else ".").rglob("*") if p.is_file()) if hasattr(b.almacen, "base") else json.dumps(b.almacen.leer("HA"))
    fuga = any(tok in json.dumps(inc, ensure_ascii=False) for tok in texto.split() if len(tok) > 5)
    ok = (esperado is None or set(inc.get("tipos_dato", [])) == esperado) and not fuga
    linea(ok, f"B {nombre}: tipos_dato={inc.get('tipos_dato')} esperado={esperado} campo={inc.get('campo_afectado')} fuga_en_incidencia={fuga}")

print("   B falso positivo de IBAN por el prefijo ES+2 dígitos:", tipos_protegidos({"x": "ES12" + "zzzz" + "token" + "QQQQQQQQQQQQQQQQQQQQ"}))

# clave como nombre de campo
b = bloque()
try:
    b.decision({"valoracion_informe": {clave: "hola"}}, AS_OF)
except DatosSensibles:
    pass
inc = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"][-1]
linea(clave not in json.dumps(inc), f"B clave como nombre de campo: campo={inc.get('campo_afectado')} tipos={inc.get('tipos_dato')}")

# búsqueda del valor en todos los archivos del almacén (criterio de PB-21)
tmp = Path(tempfile.mkdtemp())
b = nuevo_bloque(tmp, U)
iban = "ES91 2100 " + "0418 4502 0005 1332"
try:
    b.decision({"valoracion_informe": {"comentario": f"clave {clave} e IBAN {iban}"}}, AS_OF)
except DatosSensibles:
    pass
hits = [str(p) for p in tmp.rglob("*") if p.is_file() and (clave.encode() in p.read_bytes() or iban.replace(" ", "").encode() in p.read_bytes().replace(b" ", b""))]
inc = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"][-1]
linea(not hits and set(inc.get("tipos_dato", [])) == {"IBAN", "CLAVE_API"}, f"B caso del plan: coincidencias={hits} tipos={inc.get('tipos_dato')}")

# --- PB-17 · AUT en un ciclo
b = bloque()
r = b.ciclo(AS_OF, alcance={"clases": ["MP"]}, presupuesto_override={"MP": 6.0})
aut = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT"]
for e in aut:
    print("   C AUT", {k: e.get(k) for k in ("bolsa", "decision", "valor_informacion", "ev", "ac", "bac", "cpi", "eac", "condiciones", "motivo")})
linea(any(e.get("ev") for e in aut), "C1 alguna AUT con EV > 0 (si no, la prueba de CPI/EAC del ticket es vacía)")
linea(all("condiciones" in e for e in aut if e["decision"] == "AUTORIZADA"), "C2 la AUT AUTORIZADA lleva `condiciones` (HA 4.6 y plan: «con condiciones»)")
linea(all(e.get("cpi") is not None and e.get("eac") is not None for e in aut), "C3 todas las AUT llevan CPI y EAC con valor (criterio: «Dos AUT- en HA con CPI, EAC y motivo»)")
