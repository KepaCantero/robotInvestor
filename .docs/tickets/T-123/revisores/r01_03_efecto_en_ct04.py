"""QA r01 de T-123 · efecto de los falsos negativos y positivos de r01_01 en un CT-04 real.

 a) una tarjeta seguida de su caducidad o su CVV, y un IBAN alemán seguido de una cifra: ¿se acepta el CT-04 y el dato queda
    en el Almacén?
 b) un CT-04 con una huella SHA-256 (de las que el sistema escribe) cuyo tramo de cifras pasa por tarjeta: ¿se rechaza?
Uso: .venv/bin/python -I .docs/tickets/T-123/revisores/r01_03_efecto_en_ct04.py
"""
import hashlib
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

EJE = C.preparar(sys.argv)
sys.path.insert(0, str(EJE / "tests"))
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.contratos import DatosSensibles, tarjetas_en_texto  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

K = C.Contador("r01_03 T-123 efecto en CT-04")
uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
VISA, DE = "4111" + "1111" + "1111" + "1111", "DE89" + "370400440532013000"


def g(s):
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


def ct04(comentario):
    tmp = Path(tempfile.mkdtemp(prefix="qa_t123_ct04_"))
    b = nuevo_bloque(tmp, uni)
    b.fijar_fecha(AS_OF)
    try:
        b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": comentario}}, AS_OF)
        res = "aceptado"
    except DatosSensibles:
        res = "rechazado"
    return res, tmp


def queda(tmp, compacto):
    return [str(p.relative_to(tmp)) for p in tmp.rglob("*") if p.is_file()
            and compacto[4:] in re.sub(r"[\s.\-/]", "", p.read_text(encoding="utf-8", errors="ignore"))]


print("[a] falsos negativos")
for nombre, texto, dato in (("visa con caducidad", f"pago con {g(VISA)} 12/27", VISA), ("visa con CVV", f"pago con {g(VISA)} 123", VISA),
                            ("visa con caducidad y CVV", f"tarjeta {g(VISA)} 12/27 123", VISA),
                            ("IBAN DE seguido de una cifra", f"IBAN {g(DE)} 15 de noviembre", DE)):
    res, tmp = ct04(texto)
    donde = queda(tmp, dato) if res == "aceptado" else []
    print(f"    {nombre:28s} → {res}; archivos con el dato: {donde[:4]}")
    K.comprobar(f"{nombre}: CT-04 rechazado", res == "rechazado", f"{res} {donde[:3]}")

print("[b] falso positivo con una huella")
huella = next(h for h in (hashlib.sha256(str(i).encode()).hexdigest() for i in range(100000)) if tarjetas_en_texto(h))
print(f"    huella: {huella} → {tarjetas_en_texto(huella)}")
res, _ = ct04(f"revisado el artefacto con huella {huella}")
print(f"    CT-04 con esa huella → {res}")
K.comprobar("una huella SHA-256 no bloquea un CT-04", res == "aceptado", res)
n = sum(bool(tarjetas_en_texto(hashlib.sha256(str(i).encode()).hexdigest())) for i in range(100000))
print(f"    huellas SHA-256 (hex) que pasan por tarjeta: {n} de 100 000")
sys.exit(K.fin())
