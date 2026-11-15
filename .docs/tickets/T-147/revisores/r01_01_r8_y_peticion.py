"""QA r01 de T-147 (revisor) · R8 en el detector de A y en la petición CT-B-01 del Broker (`cadena_b.construir_peticion`).

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-147/revisores/r01_01_r8_y_peticion.py
Sin red ni coste. Los correos, claves e IBAN de prueba van partidos en dos cadenas (repositorio público).

Comprueba:
  A. formas de correo y de asignación de clave que el detector debería ver (y que se le escapan);
  B. textos corrientes de un paquete que no deberían marcarse;
  C. que ningún camino de error de `construir_peticion` reproduce el dato protegido en su detalle (CA-1: «sin reproducir
     el dato»), también cuando el encargo, además de llevarlo, no cumple el esquema;
  D. `tipos_secundarios` y configuración raros: fallan cerrado con su código, sin excepciones de otro tipo.
Imprime cada caso con OK / HALLAZGO y termina con 1 si hay alguno."""
import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))

from bloque_a.configuracion import cargar_config, fusionar

from bloque_a import cadena_b, contratos

CORREO = "inversor.prueba" + "@example.com"
IBAN = "ES91 2100 0418 " + "4502 0005 1332"
AK, PW = "api" + "_key", "pass" + "word"
OPP = "OPP-2026-9112"
EJEMPLO = EJ.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json"
hallazgos = 0


# límites declarados en INC-T123-01 y en el análisis de T-147 («@» codificada, nombres de clave fuera de la lista, valor
# genérico sin cifras): se informan como OBS y no cuentan como hallazgo
DECLARADOS = ("correo con escape", "correo con %40", "Authorization: Basic", "token sin cifras")


def caso(nombre, ok, detalle=""):
    global hallazgos
    obs = not ok and any(d in nombre for d in DECLARADOS)
    hallazgos += not ok and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""))


# ---------------------------------------------------------------- A. lo que debería detectarse
DEBEN = {
    "correo en mayúsculas": ("INVERSOR.PRUEBA" + "@EXAMPLE.COM"),
    "correo con subdominio": ("a.b" + "@mail.empresa-ejemplo.co.uk"),
    "correo entre comillas JSON": json.dumps({"contacto": CORREO}),
    "correo con escape \\u0040": "inversor.prueba" + "\\u0040example.com",
    "correo con %40 (URL)": "mailto:inversor.prueba" + "%40example.com",
    "api_key con espacio y comillas": f'{AK} = "ABCDEF12' + '34567890"',
    "apiKey camelCase": "api" + "Key: Zz12Zz12Zz12",
    "password tras salto de línea en JSON": json.dumps({"nota": f"linea\n{PW}=hunter2x"}),
    "Authorization: Basic": "Authorization: Basic " + "dXN1YXJp" + "bzpjbGF2ZTEyMw==",
    "token sin cifras de 24 letras": "token: " + "abcdefghijklmnopqrstuvwx",
    "IBAN en la petición": IBAN,
}
for nombre, texto in DEBEN.items():
    caso(f"A detecta: {nombre}", bool(contratos.secretos_en_texto(texto)) and bool(contratos.contiene_credenciales({"t": texto})),
         repr(texto[:12] + "…"))

# ---------------------------------------------------------------- B. lo que no debería marcarse
NO_DEBEN = {
    "versión de paquete npm": "react@18.3.1",
    "imagen @2x": "logo@2x.png",
    "tokens de un modelo": "max_tokens: 12000, tokens: 123456",
    "dirección 0x de un contrato": "token: 0x" + "a0b86991c6218b36c1d1" + "9d4a2e9eb0ce3606eb48",
    "contraseña obligatoria": "contraseña: obligatoria",
    "token_ratio": "token_ratio=0.123456",
    "secreto industrial": "secreto: industrial",
    "Twitter @usuario": "según @analista_ejemplo en su nota",
    "fecha con @": "cierre@2024-03-29",
}
for nombre, texto in NO_DEBEN.items():
    caso(f"B no marca: {nombre}", not contratos.secretos_en_texto(texto), str(contratos.secretos_en_texto(texto))[:60])

# ---------------------------------------------------------------- C. el detalle de los errores no reproduce el dato
cfg = fusionar(cargar_config(), {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}})
base = json.loads(EJEMPLO.read_text(encoding="utf-8"))


def entrada(p):
    return next(e for e in p["paquete_para_bloque_B"] if e["opp_id"] == OPP)


def opcion(p):
    return next(o for c in p["clases"].values() for o in c["opciones"] if o["opp_id"] == OPP)


def error(p, c=cfg, opp=OPP, **kw):
    try:
        cadena_b.construir_peticion(p, opp, c, **kw)
    except cadena_b.ErrorCadenaB as e:
        return e
    except Exception as e:   # noqa: BLE001 · cualquier otra excepción es un fallo no controlado
        return e
    return None


def sin_dato(e, dato):
    texto = f"{getattr(e, 'codigo', '')} {getattr(e, 'detalle', '')} {e}"
    return dato not in texto and dato.split("@")[0] not in texto


p = copy.deepcopy(base)
entrada(p)["nombre"] = f"Letras {CORREO}"
e = error(p)
caso("C1 correo en el nombre: DATOS_PROTEGIDOS sin el dato", getattr(e, "codigo", None) == "DATOS_PROTEGIDOS" and sin_dato(e, CORREO),
     getattr(e, "codigo", repr(e)))

for campo in ("tipo_activo", "nivel_confianza", "horizonte_principal"):
    p = copy.deepcopy(base)
    if campo not in entrada(p):
        continue
    entrada(p)[campo] = CORREO   # además de llevar el dato, el encargo no cumple el esquema
    e = error(p)
    caso(f"C2 correo en «{campo}» (encargo inválido): el detalle no lo reproduce",
         e is not None and sin_dato(e, CORREO), f"{getattr(e, 'codigo', repr(e))}: {str(getattr(e, 'detalle', ''))[:110]}")

p = copy.deepcopy(base)
opcion(p)["tipos_secundarios"] = [CORREO]
e = error(p)
caso("C3 correo en tipos_secundarios: el detalle no lo reproduce", e is not None and sin_dato(e, CORREO),
     f"{getattr(e, 'codigo', repr(e))}: {str(getattr(e, 'detalle', ''))[:110]}")

c2 = fusionar(cfg, {"cadena_b": {"peticion": {"nivel": CORREO}}})
e = error(copy.deepcopy(base), c2)
caso("C4 correo en cadena_b.peticion.nivel: el detalle no lo reproduce", e is not None and sin_dato(e, CORREO),
     f"{getattr(e, 'codigo', repr(e))}: {str(getattr(e, 'detalle', ''))[:110]}")

c3 = fusionar(cfg, {"idioma": f"{AK}=ABCDEF1234567890"})
e = error(copy.deepcopy(base), c3)
caso("C5 clave en «idioma»: el detalle no la reproduce", e is not None and "ABCDEF1234567890" not in f"{getattr(e, 'detalle', '')}",
     f"{getattr(e, 'codigo', repr(e))}: {str(getattr(e, 'detalle', ''))[:110]}")

# ---------------------------------------------------------------- D. entradas raras: fallan cerrado con su código
for nombre, valor in (("None", None), ("cadena", "MON"), ("repetidos", ["DIV", "DIV"]), ("fuera de los doce", ["XYZ"]),
                      ("vacía", [])):
    p = copy.deepcopy(base)
    opcion(p)["tipos_secundarios"] = valor
    e = error(p)
    esperado_ok = valor == []
    ok = (e is None) if esperado_ok else isinstance(e, cadena_b.ErrorCadenaB) and e.codigo == "ENTRADA_B_INVALIDA"
    caso(f"D1 tipos_secundarios {nombre}", ok, "sin error" if e is None else f"{type(e).__name__} {getattr(e, 'codigo', '')}")

for nombre, parche in (("nivel en minúsculas", {"cadena_b": {"peticion": {"nivel": "n2"}}}),
                       ("prioridad numérica", {"cadena_b": {"peticion": {"prioridad": 1}}}),
                       ("peticion lista", {"cadena_b": {"peticion": ["N2"]}}),
                       ("idioma es-es", {"idioma": "es-es"}), ("idioma numérico", {"idioma": 34}),
                       ("clave con espacio", {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez eur"}}}),
                       ("clave no str", {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": 7}}})):
    c = copy.deepcopy(cfg)
    if nombre == "peticion lista":
        c["cadena_b"]["peticion"] = ["N2"]
    elif nombre.startswith("clave"):
        c["cadena_b"]["correspondencia_ambitos"] = parche["cadena_b"]["correspondencia_ambitos"]
    else:
        c = fusionar(c, parche)
    e = error(copy.deepcopy(base), c)
    caso(f"D2 configuración: {nombre}", isinstance(e, cadena_b.ErrorCadenaB) and e.codigo == "CONFIGURACION_CADENA_B",
         "sin error" if e is None else f"{type(e).__name__} {getattr(e, 'codigo', '')}")

# la petición válida sigue saliendo y no muta el paquete
p = copy.deepcopy(base)
antes = json.dumps(p, sort_keys=True)
pet = cadena_b.construir_peticion(p, OPP, cfg)
caso("D3 la petición válida sale, sin mutar el paquete y sin R8", json.dumps(p, sort_keys=True) == antes
     and not contratos.contiene_credenciales(pet))

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
