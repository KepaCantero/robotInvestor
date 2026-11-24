"""Mutantes propios de T-197: aplica cada mutación, corre las pruebas de PB-09 y restaura.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-197/mutantes.py . [M4 M10 …]
(con nombres, solo esos mutantes)."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
HT05, PLAN, ORQ, CLI = ("bloque_a/herramientas/ht05_planificador.py", "bloque_a/planificacion_c1.py", "bloque_a/orquestacion.py",
                        "bloque_a/cli.py")
PRUEBAS = ["tests/test_t197_periodicidad.py",
           "tests/test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto"]
M = [
 # CT-04: el P-01 completo (CA-1)
 ("M1 el CT-04 vuelve a perder la ejecución", ORQ, "ht05.componer_p01(periodicidad, ejecucion, horario)", "f\"{periodicidad} · {horario}\""),
 ("M2 la ejecución no se valida", ORQ, "                    ejecucion = ht05.ejecucion_para_entrega(periodicidad, horario, parametro(self.cfg, \"planificador\"))\n                except ht05.P01Invalido as e:\n                    rechazos.append({\"parametro\": k, \"motivo\": str(e)})\n                    continue\n",
  "                    ejecucion = ht05.ejecucion_para_entrega(periodicidad, horario, parametro(self.cfg, \"planificador\"))\n                except ht05.P01Invalido as e:\n                    ejecucion = \"SAB 06:00\"\n"),
 ("M3 P-01 ilegible se completa con el inicial", ORQ, "            periodicidad_vig = entrega_vig = None\n", "            periodicidad_vig, _, entrega_vig = ht05.leer_p01(ht05.P01_INICIAL)\n"),
 ("M4 adelanto sin redondeo", HT05, "    return f\"{NOMBRES_DIA[dia]} {hora // 60:02d}:00\"", "    return f\"{NOMBRES_DIA[dia]} {hora // 60:02d}:{hora % 60:02d}\""),
 ("M5 redondeo hacia arriba", HT05, "    dia, hora = divmod(minuto, MIN_DIA)", "    dia, hora = divmod(minuto + (60 - minuto % 60) % 60, MIN_DIA)"),
 ("M6 sin franja sin disparos", HT05, "    if desde_h <= hora // 60 < hasta_h:", "    if False:"),
 ("M7 diaria del día anterior admitida", HT05, "    if periodicidad == \"DIARIA\" and hh * 60 + mm - adelanto < 0:", "    if False:"),
 ("M8 adelanto de otra periodicidad", HT05, "[\"adelanto_ejecucion_h\"][periodicidad]", "[\"adelanto_ejecucion_h\"][\"SEMANAL\"]"),
 ("M9 P-01 de dos partes no se lee", HT05, "    elif len(partes) == 2:", "    elif False:"),
 ("M10 periodicidad del P-01 sin validar", HT05, "    if periodicidad not in PERIODICIDADES_C1:\n        raise P01Invalido(f\"periodicidad no programable por HT-05: {periodicidad!r}\")\n    dia_hora(entrega)\n",
  "    dia_hora(entrega)\n"),
 ("M11 componer sin comprobar", HT05, "    if not (periodicidad and ejecucion and entrega):", "    if False:"),
 # HT-05: calendario (CA-2)
 ("M12 diaria también en fin de semana", HT05, "        return dia.weekday() < 5", "        return True"),
 ("M13 quincenal como semanal", HT05, "        return ((dia - base).days // 7) % 2 == 0", "        return True"),
 ("M14 quincenal por paridad ISO", HT05, "        return ((dia - base).days // 7) % 2 == 0", "        return dia.isocalendar()[1] % 2 == 0"),
 ("M15 mensual sin límite de día", HT05, "        return dia.day <= 7", "        return True"),
 ("M16 antes del inicio vale", HT05, "    if dia < inicio:\n        return False\n", ""),
 ("M17 siguiente admite el mismo instante", HT05, "_en_hora(dia, ejecucion) > desde:", "_en_hora(dia, ejecucion) >= desde:"),
 ("M18 entrega sin mirar el día", HT05, "(periodicidad == \"DIARIA\" or dia.weekday() == d)", "True"),
 # planificador (CA-2 y CA-3)
 ("M19 sin cambios futuros de P-01", PLAN, "        cambio = next((f for f in cambios if dia < f <= c.date()), None)", "        cambio = None"),
 ("M20 F10 sin fecha de efecto", PLAN, "efectivo_el=str(dia)).get(\"P-01\")\n    if not est", "efectivo_el=None).get(\"P-01\")\n    if not est"),
 ("M21 inicio sin fecha de efecto", PLAN, "str(est.get(\"fecha_efecto\") or est[\"_historial\"][0][\"fecha\"])", "str(est[\"_historial\"][0][\"fecha\"])"),
 ("M22 último sin bajar al P-01 anterior", PLAN, "        hasta, dia = dt.datetime.combine(p[\"inicio\"], dt.time()) - dt.timedelta(minutes=1), anterior", "        return None"),
 ("M23 sin disparador con el P-01", PLAN, "        res = bloque.ciclo(pd.Timestamp(t), disparador=disparador)", "        res = bloque.ciclo(pd.Timestamp(t))"),
 # idempotencia, recuperación y fallo cerrado (CA-5)
 ("M24 sin idempotencia", PLAN, "        if previo is not None:", "        if False:"),
 ("M25 sin transacción", PLAN, "    with bloque.almacen._transaccion():\n        prog = ultimo_programado(bloque, t)", "    if True:\n        prog = ultimo_programado(bloque, t)"),
 ("M26 perdido se ejecuta", PLAN, "    if estado == \"PERDIDO\":\n        return", "    if False:\n        return"),
 ("M27 límite de 24 h exclusivo", PLAN, "\"PERDIDO\" if t > entrega + margen", "\"PERDIDO\" if t >= entrega + margen"),
 ("M28 sin margen de recuperación", PLAN, "\"PERDIDO\" if t > entrega + margen", "\"PERDIDO\" if t > entrega"),
 ("M29 recuperado como emitido", PLAN, "(\"RECUPERADO\" if t >= entrega else \"EMITIDO\")", "\"EMITIDO\""),
 ("M30 sin ejecutar escribe", PLAN, "        if not ejecutar:\n", "        if False:\n"),
 ("M31 fallo sin registrar", PLAN, "\"estado_run\": res[\"estado\"] if res else \"FALLIDO\"", "\"estado_run\": res[\"estado\"] if res else None"),
 ("M32 instante con zona admitido", PLAN, "    if t.tzinfo is not None:\n        raise", "    if False:\n        raise"),
 # r02 (QA r01): los mutantes vivos del revisor (H-03 y H-06; R4 es equivalente) y los de las correcciones
 ("M33 R1 la CLI dispara siempre", CLI, "disparar(bloque, as_of, ejecutar=a.ejecutar)", "disparar(bloque, as_of, ejecutar=True)"),
 ("M34 R2 la CLI nunca dispara", CLI, "disparar(bloque, as_of, ejecutar=a.ejecutar)", "disparar(bloque, as_of, ejecutar=False)"),
 ("M35 R3 cambio el mismo día del C1 ignorado", PLAN, "if dia < f <= c.date()", "if dia < f < c.date()"),
 ("M36 R6 entrega exacta como EMITIDO", PLAN, "(\"RECUPERADO\" if t >= entrega else \"EMITIDO\")", "(\"RECUPERADO\" if t > entrega else \"EMITIDO\")"),
 ("M37 R7 mensual sin el día 7", HT05, "        return dia.day <= 7", "        return dia.day < 7"),
 ("M38 R8 C1 a su minuto exacto no", HT05, "and _en_hora(dia, ejecucion) <= hasta:", "and _en_hora(dia, ejecucion) < hasta:"),
 ("M39 R9 entrega diaria con día", HT05, "(periodicidad == \"DIARIA\" or dia.weekday() == d)", "dia.weekday() == d"),
 ("M40 R10 F10 sin as_of", PLAN, "    est = bloque.almacen.estado(\"F10\", str(conocido.date()), efectivo_el=str(dia)).get(\"P-01\")",
  "    est = bloque.almacen.estado(\"F10\", None, efectivo_el=str(dia)).get(\"P-01\")"),
 ("M41 R11 sin segundos a cero", PLAN, "    return t.to_pydatetime().replace(second=0, microsecond=0)", "    return t.to_pydatetime()"),
 ("M42 R14 diaria estricta", HT05, "and hh * 60 + mm - adelanto < 0:", "and hh * 60 + mm - adelanto <= 0:"),
 ("M43 R15 dos partes sin deducir", PLAN, "        ejecucion = ht05.ejecucion_para_entrega(periodicidad, entrega, parametro(bloque.cfg, \"planificador\"))",
  "        ejecucion = \"SAB 06:00\""),
 ("M44 R16 sin fecha del disparo", PLAN, "    bloque.fijar_fecha(t)\n", ""),
 ("M45 R5 ancla en la semana del inicio", HT05, "    return primero - dt.timedelta(days=primero.weekday())",
  "    return inicio - dt.timedelta(days=inicio.weekday())"),
 ("M46 R17 el disparo sin P-01", PLAN, "**{k: prog[k] for k in (\"programado\", \"entrega\", \"p01\", \"cfg_id\")}",
  "**{k: prog[k] for k in (\"programado\", \"entrega\")}"),
 ("M47 H-01 CFG- aunque no cambie", ORQ, "                if pid in sin_cambio or valor == calendario:", "                if pid in sin_cambio:"),
 ("M48 H-01 el ancla no se copia", ORQ, "if periodicidad_vig == \"QUINCENAL\" and p01_vig", "if False"),
 ("M49 H-01 el planificador ignora el ancla", PLAN, "    ancla = est.get(\"semana_ancla_quincenal\") if periodicidad == \"QUINCENAL\" else None",
  "    ancla = None"),
 ("M50 H-01 ancla guardada sin usar", HT05, "        base = _ancla(ejecucion, inicio) if ancla is None else", "        base = _ancla(ejecucion, inicio) if True else"),
 ("M51 H-01 ancla no explícita fuera de la quincenal", ORQ, "else ht05.ancla_quincenal(ejecucion, efecto)) if periodicidad == \"QUINCENAL\" else None)",
  "else ht05.ancla_quincenal(ejecucion, efecto)) if True else None)"),
 ("M52 H-02 sin pid", PLAN, ", \"pid\": os.getpid(), **identidad_proceso", ", **identidad_proceso"),
 ("M53 H-02 huérfano como duplicado", PLAN, "    if vivo is False:", "    if False:"),
 ("M54 H-02 vivo como duplicado", PLAN, "    if vivo is True:", "    if False:"),
 ("M55 H-02 sin incidencia", PLAN, "        bloque.almacen.incidencia(\"HERRAMIENTA\"", "        (lambda *a, **k: None)(\"HERRAMIENTA\""),
 ("M56 H-08 el cierre no deja estado_run", PLAN, "\"id\": previo[\"id\"], \"estado_run\": \"FALLIDO\",", "\"id\": previo[\"id\"], \"estado_runX\": \"FALLIDO\","),
 ("M57 H-04 entrega en la franja admitida", HT05, "    if desde_h <= hh < hasta_h:", "    if False:"),
 ("M58 H-01 sin_cambio no se informa", ORQ, "\"sin_cambio\": sin_cambio}, \"aviso_ct22\"", "\"sin_cambio\": []}, \"aviso_ct22\""),
 # ronda de cierre de la QA r02
 ("M59 H-07 pid propio siempre vivo", PLAN, "        return previo.get(\"id\") in _ABIERTOS", "        return True"),
 ("M60 H-07 sin comparar la identidad", PLAN, "    return ahora == guardada", "    return True"),
 ("M61 H-07 la reserva sin identidad", PLAN, ", **identidad_proceso(os.getpid())})", "})"),
 ("M62 H-07 no se anota como abierto", PLAN, "            _ABIERTOS.add(prog[\"disparo_id\"])", "            pass"),
 ("M63 H-07 no se retira al cerrar", PLAN, "        _ABIERTOS.discard(prog[\"disparo_id\"])\n", ""),
 ("M64 H-08 sin motivo del cierre", PLAN, "\"motivo_cierre\": \"proceso terminado\"", "\"motivo_cierreX\": \"proceso terminado\""),
 ("M65 H-07 boot_id sin leer", PLAN, "    return {\"boot_id\": boot.strip() if boot else None,", "    return {\"boot_id\": None,"),
 # segunda ronda de cierre de la QA r02: los vivos de revisores/r02_02_mutantes_cierre.py (H-09 y H-10)
 ("M66 C1 hora de arranque de otro campo", PLAN, "int(campos[19]) if len(campos) > 19 and campos[19].isdigit()",
  "int(campos[20]) if len(campos) > 20 and campos[20].isdigit()"),
 ("M67 C2 sin poder saberlo, huérfano", PLAN, "    if None in ahora.values() or None in guardada.values():\n        return None",
  "    if None in ahora.values() or None in guardada.values():\n        return False"),
 ("M68 C3 sin poder saberlo, vivo", PLAN, "    if None in ahora.values() or None in guardada.values():\n        return None",
  "    if None in ahora.values() or None in guardada.values():\n        return True"),
]
SOLO = set(sys.argv[2:])
if SOLO:
    M = [m for m in M if m[0].split()[0] in SOLO]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} muertos de {len(M)}; vivos: {vivos}")
sys.exit(1 if vivos else 0)
