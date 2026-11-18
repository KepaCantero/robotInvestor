"""Mutantes propios de T-178: aplica cada mutación, corre tests/test_t178.py y restaura.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-178/mutantes.py ."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
MON, CAR = "bloque_a/herramientas/ht08_monitor.py", "bloque_a/carga.py"
M = [
 ("M1 abre instancias de los con estado", MON, "                if ag in SIN_ESTADO:", "                if True:"),
 ("M2 sin reordenar", MON, "        orden = sorted(antes, key=clave_prioridad)", "        orden = list(antes)"),
 ("M3 el monitor no guarda el orden", MON, "        self.pendientes[ag] = orden\n", ""),
 ("M4 C6 no va al final", MON, "    return (orden.get(\"tipo\") in TIPOS_C6, PRIORIDADES.index", "    return (False, PRIORIDADES.index"),
 ("M5 prioridad invertida", MON, "PRIORIDADES.index(orden[\"prioridad\"]), fecha", "-PRIORIDADES.index(orden[\"prioridad\"]), fecha"),
 ("M6 sin fecha primero", MON, "fecha is None, str(fecha", "fecha is not None, str(fecha"),
 ("M7 sin desempate por llegada", MON, "            orden[\"llegada\"])", "            -orden[\"llegada\"])"),
 ("M8 prioridad no validada", MON, "                if prioridad not in PRIORIDADES:", "                if False:"),
 ("M9 ref no validada", MON, "                if not ref or not isinstance(ref, str):", "                if False:"),
 ("M10 repetida admitida", MON, "                if ref in vistas:", "                if False:"),
 ("M11 ya en la cola admitida", MON, "            if repetidas := {p", "            if False and {p"),
 ("M12 avisa de todos", MON, "\"afecta_plazos\": ag in CAMINO_ENTREGA,", "\"afecta_plazos\": True,"),
 ("M13 sin aviso", MON, "        if car[\"afecta_plazos\"]:\n            car[\"aviso_coordinador\"]", "        if False:\n            car[\"aviso_coordinador\"]"),
 ("M14 aviso a otro", MON, "\"destinatario\": \"AG-01\"", "\"destinatario\": \"AG-18\""),
 ("M15 sin_detalle mal", MON, "\"sin_detalle\": max(q - len(orden), 0)", "\"sin_detalle\": 0"),
 ("M16 retirar no descuenta", MON, "            del pend[i]\n            self.cola[agente] = max(self.cola[agente] - 1, 0)", "            del pend[i]"),
 ("M17 propone a la primera", CAR, "    if not previos:\n        return None", "    if False:\n        return None"),
 ("M18 el mismo run cuenta", CAR, " and e.get(\"run_id\") != run_id]", "]"),
 ("M19 duplica la abierta", CAR, "        if estados.get(pid, {}).get(\"estado\") not in CERRADAS:\n            return pid", "        if False:\n            return pid"),
 ("M20 sin corte tras la decisión", CAR, "    corte = propias[-1] + 1 if propias else 0", "    corte = 0"),
 ("M21 otro agente cuenta", CAR, "e.get(\"tipo_entrada\") == \"CAR\" and e.get(\"agente\") == agente", "e.get(\"tipo_entrada\") == \"CAR\""),
 ("M22 legado no cuenta", CAR, "e.get(\"saturado\", True)", "e.get(\"saturado\", False)"),
 ("M23 CAR- sin p3_id", CAR, "                e[\"p3_id\"] = p3_id", "                pass"),
 ("M24 lector sin filtro de run", CAR, "and (run_id is None or e.get(\"run_id\") == run_id)]", "]"),
 ("M25 APROBADA cierra (r02: con CERRADAS)", CAR, "CERRADAS = (\"RECHAZADA\", \"APLICADA\")", "CERRADAS = (\"RECHAZADA\", \"APLICADA\", \"APROBADA\")"),
 ("M26 el ciclo no registra", "bloque_a/orquestacion.py", "        registrar_carga(self.almacen, self.monitor.evaluar_instancias(), run_id)", "        self.monitor.evaluar_instancias()"),
 ("M27 decisiones no reconocidas por id", CAR, "e.get(\"tipo_entrada\") == \"P3\" and e.get(\"id\") in ids]", "_es_p3_de(e, ag)]"),
 # r02 (QA r01)
 ("M28 H-01 sin transacción", CAR, "        with almacen._transaccion():   # r02 (H-01)", "        if True:   # r02 (H-01)"),
 ("M29 H-02 estado desconocido cierra", CAR, "get(\"estado\") not in CERRADAS:", "get(\"estado\") in (\"PENDING_OPERATOR\", \"APROBADA\"):"),
 ("M30 H-02 APLICADA no cierra", CAR, "CERRADAS = (\"RECHAZADA\", \"APLICADA\")", "CERRADAS = (\"RECHAZADA\",)"),
 ("M31 H-03 fecha sin validar", MON, "    if not (isinstance(f, str) and RE_FECHA.fullmatch(f)):", "    if False:"),
 ("M32 H-03 fecha imposible admitida", MON, "        dt.date.fromisoformat(f)\n", "        pass\n"),
 ("M33 H-03 date sin pasar a ISO", MON, "        return (f.date() if isinstance(f, dt.datetime) else f).isoformat()", "        return f"),
 ("M34 H-04 tipo sin validar", MON, "                if tipo is not None and tipo not in TIPOS:", "                if False:"),
 ("M35 H-05 la P3- cita el CAR- actual", CAR, "    evidencia = {\"car\": [e[\"id\"] for e in previos],", "    evidencia = {\"car\": [e[\"id\"] for e in previos] + [car[\"id\"]],"),
 ("M36 H-06 fin baja por debajo del detalle", MON, "max(self.cola[agente] - 1, len(self.pendientes[agente]))", "max(self.cola[agente] - 1, 0)"),
]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t178.py"],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print("vivos:", vivos)
