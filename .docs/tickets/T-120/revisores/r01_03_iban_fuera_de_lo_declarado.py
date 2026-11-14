"""QA r01 de T-120 · Formas corrientes del IBAN español que el patrón no cubre, por el camino real (CT-04 comentario, CT-03
pregunta, CT-23 entrante): ¿se admiten y se quedan en algún archivo? No son un fallo del alcance declarado («espacio, punto o
guion entre grupos de cuatro»); sirven para juzgar si los límites están declarados.
Uso (desde bloque_a/11_Ejecutor de la copia): QA_TMP=<carpeta> python .../r01_03_iban_fuera_de_lo_declarado.py
El IBAN es el de ejemplo de la documentación bancaria y va partido."""
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.contratos import DatosSensibles  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

I = "ES91" + "2100" + "0418" + "4502" + "0005" + "1332"
G = [I[i:i + 4] for i in range(0, 24, 4)]
FORMAS = {
    "espacio duro (U+00A0, copiado de una web o un PDF)": " ".join(G),
    "tabulador": "\t".join(G),
    "dos espacios": "  ".join(G),
    "formato CCC impreso (ES91 2100 0418 45 0200051332)": f"{G[0]} {G[1]} {G[2]} {G[3][:2]} {G[3][2:]}{G[4]}{G[5]}",
    "minúsculas": " ".join(G).lower(),
    "control: espacios simples (declarado)": " ".join(G),
}
tmp = Path(tempfile.mkdtemp(prefix="qa_t120_r03_", dir=os.environ.get("QA_TMP")))
uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
admitidas = 0
for k, (nombre, iban) in enumerate(FORMAS.items()):
    carp = tmp / f"f{k}"
    b = nuevo_bloque(carp, uni)
    b.fijar_fecha(AS_OF)
    for canal, f in {
        "CT-04 comentario": lambda: b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"cobren en {iban}"}}, AS_OF),
        "CT-03 pregunta": lambda: b.consulta(f"¿Pueden pagar en {iban}?", as_of=AS_OF),
        "CT-23 entrante": lambda: b.consultas.entrante(f"apunten {iban}", as_of=AS_OF),
    }.items():
        try:
            f()
            res = "ADMITIDO"
        except DatosSensibles:
            res = "rechazado"
        except Exception as e:  # noqa: BLE001
            res = f"{type(e).__name__}: {str(e)[:60]}"
        quedan = sorted({p.name for p in carp.rglob("*") if p.is_file()
                         and re.search(r"2100\D{0,12}0418", p.read_bytes().decode("utf-8", errors="ignore"))})
        admitidas += res == "ADMITIDO"
        print(f"{res:10s} {canal:17s} {nombre:52s} archivos con el dato: {quedan}")
print("formas admitidas:", admitidas)
