"""Ronda r04 de T-116 (implementador): un mutante por cláusula nueva del mapa, enfrentado a las pruebas del ejecutor que el mapa
cita para esa fila (se leen del mapa de la copia). MUERTO = alguna falla; VIVO = todas pasan. No es la QA: es la comprobación de
que cada prueba nueva afirma lo que dice; la QA tiene sus propios scripts en `revisores/`.

Uso:  python r04_mutantes_implementador.py <copia desechable de bloque_a/11_Ejecutor, con «_mut» en la ruta> [--solo M01,M08]
Trabaja solo en la copia y restaura cada fichero al acabar. Termina con 1 si queda algún mutante vivo.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PY = sys.executable
ej = Path(sys.argv[1]).resolve()
assert "_mut" in str(ej) and (ej / "bloque_a" / "almacen.py").exists(), "solo en una copia desechable de 11_Ejecutor"
solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
MAPA = json.loads((ej / "tests" / "mapa_plan_pruebas.json").read_text(encoding="utf-8"))
ORQ, RED, SIN, EVL = "bloque_a/orquestacion.py", "bloque_a/redaccion.py", "bloque_a/sintesis.py", "bloque_a/evaluador.py"
IB, CON, SEG = "bloque_a/interfaz_broker.py", "bloque_a/contratos.py", "bloque_a/seguimiento.py"

MUT = [
    ("M01", "PB-01", ORQ, "el nivel ya no sigue a GC0 (todo N2)",
     'nivel = {c: "N2" if gc0[c]["cambio_material"] else "N1" for c in clases}', 'nivel = {c: "N2" for c in clases}'),
    ("M02", "PB-01", ORQ, "se congelan los PRG aunque G3 bloquee los entregables",
     '        if g3b["dictamen"] == "BLOQUEADO":\n            resultado["estado"] = "PARCIAL"',
     '        if g3b["dictamen"] == "BLOQUEADO":\n            self._congelar(extras, as_of, run_id)\n            resultado["estado"] = "PARCIAL"'),
    ("M03", "PB-06", ORQ, "la respuesta N0 lleva una referencia que no existe",
     'refs = [x for x in d.get("referencias", []) if x in conocidos]',
     'refs = [x for x in d.get("referencias", []) if x in conocidos] + ["OPP-2099-9999"]'),
    ("M04", "PB-07", ORQ, "la respuesta provisional ya no da el plazo",
     '"plazo_estimado": "mismo día (ejecución síncrona del ejecutor)"', '"plazo_estimado": ""'),
    ("M05", "PB-12", SIN, "la relevancia ya no sigue la regla del Anexo A",
     'op["relevancia_decisional"] = "ALTA" if motivos else ("BAJA" if f.get("_arrastre") else "MEDIA")',
     'op["relevancia_decisional"] = "MEDIA"'),
    ("M06", "PB-22", CON, "la incidencia CANAL_NO_PREVISTO ya no se escala",
     'msg["emisor"],\n                                    tratamiento="rechazada y registrada", escalado_operador=True)',
     'msg["emisor"],\n                                    tratamiento="rechazada y registrada", escalado_operador=False)'),
    ("M07", "PB-53", SIN, "el ejecutor deja de retirar la propuesta de una empresa concreta",
     "        if any(isinstance(t, str) and _UNITARIA.search(t) for t in textos):", "        if False:"),
    ("M08", "PB-55", RED, "el técnico deja de poner el semáforo en el apartado de cada tipo",
     "({c}) — semáforo {d['estado_semaforo']}", "({c})"),
    ("M09", "PB-58", IB, "un servicio pendiente de credencial deja de declararse",
     'if c.get("estado") in ("SOLICITADA", "APLAZADA") and c.get("servicio"):', "if False:"),
    ("M10", "PB-60", RED, "el visual deja de declarar el servicio degradado",
     "for d in (cred.degradaciones(as_of) if cred else []):", "for d in []:"),
    ("M11", "PB-60", IB, "un servicio ya provisto se sigue declarando degradado",
     'if self.boveda.estado_servicio(s, as_of.date())["estado"] != "PROVISTA"]', "]"),
    ("M12", "PB-61", RED, "el técnico deja de listar los supuestos declarados", 'if p.get("supuestos_declarados"):', "if False:"),
    ("M13", "PB-64", EVL, "un hito necesario fallado ya no invalida el H5", 'est = "INVALIDADO"', 'est = "DESVIADO"'),
    ("M14", "PB-66", SEG, "la cancelación deja la fecha del siguiente ciclo",
     'e.update({"estado": "CANCELADO", "proximo_ciclo": None,', 'e.update({"estado": "CANCELADO",'),
    ("M15", "PB-11", ORQ, "la decisión del Broker cambia el estado de la opción en F3",
     '{"tipo_entrada": "DECISION_BROKER", "opp_id": d["opp_id"],', '{"tipo_entrada": "DECISION_BROKER", "opp_id": d["opp_id"], "estado": d["decision"],'),
    ("M16", "PB-31", SIN, "sin certificado, la confianza sale «establecido» (el visual pinta «Alta»)",
     '"confianza": "probable" if pu["E"] >= pres["confianza_probable_E"] else "especulativo"',
     '"confianza": "establecido" if pu["E"] >= pres["confianza_probable_E"] else "especulativo"'),
    ("M17", "PB-37", EVL, "la corrección (`version_de`) no entra en las métricas",
     'if p.get("estado") == "RESUELTO" and not p.get("es_hito")', 'if p.get("estado") == "RESUELTO" and not p.get("es_hito") and not p.get("version_de")'),
    ("M18", "PB-43", ORQ, "la lección de producto solo enlaza la última consulta",
     'lec = self.evaluador.leccion_producto(as_of, tema, [q["id"] for q in previas] + [qry_id])',
     'lec = self.evaluador.leccion_producto(as_of, tema, [qry_id])'),
    ("M19", "PB-16", ORQ, "el cierre por presupuesto ya no se anota en F5",
     '"cierres_parciales": sorted(presupuesto.cierres, key=', '"cierres_parciales": [] or sorted([], key='),
    ("M20", "PB-56", ORQ, "el ciclo C1 ya no quita los duplicados entre tipos",
     "            self._deduplicar_entre_tipos(seleccion)\n", "            pass\n"),
]


def citadas(pb: str) -> list[str]:
    return [p.split("11_Ejecutor/", 1)[1] for p in MAPA[pb]["pruebas"] if p.startswith("11_Ejecutor/")]


def main() -> int:
    vivos = []
    for mid, pb, fich, desc, viejo, nuevo in MUT:
        if solo and mid not in solo:
            continue
        ruta = ej / fich
        original = ruta.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}", flush=True)
            vivos.append(mid)
            continue
        try:
            ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *citadas(pb)], cwd=ej, capture_output=True, text=True)
            ult = (r.stdout + r.stderr).strip().splitlines()[-1][:90]
            print(f"{mid} · {pb} · {'MUERTO' if r.returncode else 'VIVO  '} · {desc} · {len(citadas(pb))} citadas · {ult}", flush=True)
            if r.returncode == 0:
                vivos.append(mid)
        finally:
            ruta.write_text(original, encoding="utf-8")
    print("vivos o no aplicados: " + (", ".join(vivos) or "ninguno"))
    return 1 if vivos else 0


if __name__ == "__main__":
    raise SystemExit(main())
