#!/usr/bin/env bash
# Compara el cierre observado con el esperado en cinco casos temporales ficticios de T-64.
source "$(dirname "$0")/common.sh"
cd "$RAIZ/bloque_b/11_Ejecutor"
"$PY" -B - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory

from bloque_b.entorno import Entorno
from bloque_b.orquestacion import Coordinador

incidente = "2025-03-10"
corte = "2025-03-20"
# Caso, día observado, publicación, primera disponibilidad, alta local, cierre esperado.
casos = [
    ("Informe anterior", "2025-02-28", "2025-03-05", "2025-03-05", "2025-03-05", False),
    ("Recuperación documentada", "2025-03-17", "2025-03-18", "2025-03-18", "2025-03-18", True),
    ("Publicado después del corte", "2025-03-17", "2025-03-25", "2025-03-25", "2025-03-25", False),
    ("Publicación reciente sobre febrero", "2025-02-28", "2025-03-18", "2025-03-18", "2025-03-18", False),
    ("Archivo precargado con publicación futura", "2025-03-17", "2025-03-25", "2025-03-25", corte, False),
]
print(f"Incidente: {incidente}. Decisión: {corte}.")
print("Caso | Visible para el agente | Cierre observado | Cierre esperado")
fallos = 0
for caso, hecho, publicado, disponible, alta, esperado in casos:
    with TemporaryDirectory() as tmp:
        carpeta = Path(tmp)
        ent = Entorno(estado=str(carpeta / "estado"), salida=str(carpeta / "salida"), as_of=alta, cliente="mock")
        ref = ent.alm.nuevo_id("EVD-B")
        pet = "PET-B-2025-0001"
        ent.alm.escribir("F2", "AG-B15", {"tipo_entrada": "EVD", "id": ref, "pet_id": pet, "estado": "VIGENTE",
            "fuente": f"Informe ficticio sobre los pedidos a {hecho}",
            "fechas": {"fecha_fenomeno": hecho, "fecha_publicacion": publicado, "conocible_desde": disponible,
                       "recuperacion": alta}})
        ent.fijar_as_of(corte)
        coord = Coordinador(ent)
        catalogo = coord._referencias_contraste({"pet_id": pet, "seleccion": {}})
        obj = {"obj_id": "OBJ-1", "x_fecha_incidente": incidente, "argumento": f"Retrasos comunicados el {incidente}.",
               "fuerza": "fuerte", "resuelta": False}
        coord._aplicar_respuestas([obj], {"OBJ-1": {"resuelta": True, "respuesta": "Los pedidos se entregan a tiempo.",
                                                   "evidencia_nueva": [ref]}}, catalogo)
        observado = obj["resuelta"]
        visible = "sí" if ref in catalogo else "no"
        print(f"{caso} | {visible} | {'cerrada' if observado else 'abierta'} | {'cerrada' if esperado else 'abierta'}")
        visibilidad_esperada = max(alta, publicado, disponible) <= corte
        fallos += observado != esperado or (ref in catalogo) != visibilidad_esperada
print(f"{fallos} discrepancias en {len(casos)} casos.")
raise SystemExit(1 if fallos else 0)
PY
