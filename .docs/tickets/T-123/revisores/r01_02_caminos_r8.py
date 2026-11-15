"""QA r01 de T-123 · caminos de R8: CT-04, CT-03 y CT-23 con una tarjeta o un IBAN extranjero; el dato no queda en ningún
archivo. Y los mensajes reales de un ciclo simulado (los que deja el Almacén): ¿algún falso positivo?

Uso: .venv/bin/python -I .docs/tickets/T-123/revisores/r01_02_caminos_r8.py [ejecutor carpeta_ciclo]
`carpeta_ciclo`: salida de un backtest mock (p. ej. la de r01_06 de T-118); se recorre entera con `secretos_en_texto`.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

EJE = C.preparar(sys.argv)
sys.path.insert(0, str(EJE / "tests"))
from bloque_a.contratos import DatosSensibles, secretos_en_texto  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

K = C.Contador("r01_02 T-123 caminos de R8")
NBSP = " "
DATOS = {"tarjeta visa": "4111" + "1111" + "1111" + "1111", "tarjeta amex": "3782" + "822463" + "10005",
         "IBAN DE": "DE89" + "370400440532013000", "IBAN FR": "FR76" + "30006000011234567890189", "IBAN GB": "GB29" + "NWBK60161331926819"}


def grupos(s, sep=" "):
    return sep.join(s[i:i + 4] for i in range(0, len(s), 4))


def rastro(raiz: Path, compacto: str) -> list[str]:
    """Archivos en los que aparece el dato (comparando sin separadores ni mayúsculas)."""
    clave = compacto[4:].lower()
    out = []
    for p in raiz.rglob("*"):
        if p.is_file():
            t = re.sub(r"[\s.\-]", "", p.read_text(encoding="utf-8", errors="ignore")).lower()
            if clave in t:
                out.append(str(p.relative_to(raiz)))
    return out


uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)

print("[1] CT-04, CT-03 y CT-23")
for nombre, dato in DATOS.items():
    for forma, txt in (("espacios", grupos(dato)), ("espacio duro", grupos(dato, NBSP)), ("junto", dato)):
        tmp = Path(tempfile.mkdtemp(prefix="qa_t123_"))
        b = nuevo_bloque(tmp, uni)
        b.fijar_fecha(AS_OF)
        res = {}
        try:
            b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"cobren en {txt}"}}, AS_OF)
            res["CT-04"] = "aceptado"
        except DatosSensibles:
            res["CT-04"] = "rechazado"
        except Exception as e:  # noqa: BLE001
            res["CT-04"] = f"otra {type(e).__name__}: {e}"[:80]
        try:
            r = b.consulta(f"¿Cobro en {txt}?", {"nota": txt}, AS_OF)
            res["CT-03"] = "aceptado" if not (isinstance(r, dict) and r.get("rechazado")) else "rechazado"
        except DatosSensibles:
            res["CT-03"] = "rechazado"
        except Exception as e:  # noqa: BLE001
            res["CT-03"] = f"otra {type(e).__name__}: {e}"[:80]
        try:
            b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
                                "preguntas": [{"texto": f"¿Pagamos a {txt}?", "supuesto_declarado": "ninguno"}]}, AS_OF)
            res["CT-23"] = "aceptado"
        except DatosSensibles:
            res["CT-23"] = "rechazado"
        except Exception as e:  # noqa: BLE001
            res["CT-23"] = f"otra {type(e).__name__}: {e}"[:80]
        donde = rastro(tmp, dato)
        print(f"    {nombre:13s} {forma:12s} {res} · archivos con el dato: {donde}")
        K.comprobar(f"{nombre} ({forma}): CT-04, CT-03 y CT-23 rechazados", all(v == "rechazado" for v in res.values()), str(res))
        K.comprobar(f"{nombre} ({forma}): el dato no queda en ningún archivo", not donde, str(donde))

if len([a for a in sys.argv[1:] if Path(a).is_dir()]) >= 2:
    raiz = Path(sys.argv[-1])
    print(f"\n[2] falsos positivos en lo que dejó un ciclo simulado: {raiz}")
    n, hits, hexes = 0, [], 0
    for p in raiz.rglob("*"):
        if p.is_file() and p.suffix in (".json", ".jsonl", ".csv", ".md", ".txt", ".log", ""):
            for linea in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                n += 1
                hexes += len(re.findall(r"\b[0-9a-f]{32,64}\b", linea))
                h = secretos_en_texto(linea)
                if h:
                    hits.append((str(p.relative_to(raiz)), h[:2]))
    print(f"    líneas: {n}; huellas hexadecimales de 32 a 64: {hexes}; líneas marcadas: {len(hits)}")
    for x in hits[:15]:
        print(f"      {x}")
    K.comprobar("ningún falso positivo en las salidas del ciclo simulado", not hits, str(hits[:5]))
sys.exit(K.fin())
