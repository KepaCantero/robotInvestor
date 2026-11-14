"""QA r01 de T-116 · Mutantes en el código que cubren las ocho pruebas de `test_fase4_huecos.py` (¿afirman lo que dicen?) y
dos mutantes que ponen a prueba filas AUTOMATICA del mapa (PB-23 y PB-37) con las pruebas que el mapa cita.

Uso:  python r01_03_mutantes_huecos.py <copia_desechable> [--solo H01,H02]
Cada mutante ejecuta SOLO las pruebas indicadas; MUERTO = alguna falla (la prueba protege), VIVO = todas pasan.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
O, C, E, I, A, K = ("bloque_a/orquestacion.py", "bloque_a/contratos.py", "bloque_a/evaluador.py", "bloque_a/interfaz_broker.py",
                    "bloque_a/almacen.py", "bloque_a/consumo.py")
T = "tests/test_fase4_huecos.py::"
PB10, PB16 = T + "test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas", T + "test_pb16_con_el_presupuesto_agotado_g3_hace_las_mismas_comprobaciones"
PB17A, PB17B = T + "test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha", T + "test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido"
PB22 = T + "test_pb22_tres_mensajes_por_canales_no_previstos_tres_incidencias_y_ningun_efecto"
PB33, PB45 = T + "test_pb33_la_revocacion_registra_estado_motivo_y_fecha_de_efecto", T + "test_pb45_el_encargo_lleva_diez_lecciones_como_maximo_y_las_de_mas_fuerza"
PB59 = T + "test_pb59_la_credencial_expuesta_deja_incidencia_en_ha_sin_copiar_el_valor"
U23 = "tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of"
MUTANTES = [
    ("H01", O, [PB10], "PB-10: la celda «No» ya no se rechaza", 'if aplicabilidad(self.cfg, c, h) == "NO":\n                            rechazos.append', 'if aplicabilidad(self.cfg, c, h) == "NUNCA":\n                            rechazos.append'),
    ("H02", O, [PB10], "PB-10: al aplicar la configuración se toca además otro parámetro de F10 (P-29)",
     '            aplicado[pid] = cfg_id\n',
     '            aplicado[pid] = cfg_id\n            self.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": self.almacen.nuevo_id("CFG"), "param_id": "P-29", "de": None, "a": "xx", "valor_vigente": "xx", "autor": "AG-01", "origen": ret_id, "fecha_efecto": str((as_of + pd.Timedelta(days=1)).date())})\n'),
    ("H03", O, [PB10], "PB-10: un rechazo de configuración deja una incidencia de escritura en HA",
     'rechazos.append({"parametro": f"horizontes:{c}:{h}", "motivo": f"{h} es «No» para {c} en la tabla 8.3 (no se activa para esa clase)"})',
     'rechazos.append({"parametro": f"horizontes:{c}:{h}", "motivo": f"{h} es «No» para {c} en la tabla 8.3 (no se activa para esa clase)"}); self.almacen.incidencia("ACCESO_FUERA_DE_MATRIZ", "QA", "AG-01")'),
    ("H04", O, [PB16], "PB-16: con el estado PARCIAL, G3 (F6) registra una comprobación menos",
     '                                       "detalle": [i["detalle"] for i in c["incidencias"]][:5]} for c in res["comprobaciones"]]}',
     '                                       "detalle": [i["detalle"] for i in c["incidencias"]][:5]} for c in res["comprobaciones"][:(-1 if paquete.get("limitaciones") and any("Presupuesto agotado" in x for x in paquete["limitaciones"]) else None)]]}'),
    ("H05", K, [PB17A, PB17B], "PB-17: la fase ya no cuenta (se autoriza aunque no pueda cambiar el top-3)", 'concede = fase_admitida and falta > 0 and actual', 'concede = falta > 0 and actual'),
    ("H06", K, [PB17A, PB17B], "PB-17: el tope ya no cuenta", 'and actual + falta <= base * (1 + maximo) + 1e-9', 'and True'),
    ("H07", O, [PB17A, PB17B], "PB-17: la denegada no deja AUT- en HA",
     '        self.almacen.escribir("HA", "AG-18", {"tipo_entrada": "AUT", "id": self.almacen.nuevo_id("AUT"), "run_id": run_id,',
     '        if autoriza: self.almacen.escribir("HA", "AG-18", {"tipo_entrada": "AUT", "id": self.almacen.nuevo_id("AUT"), "run_id": run_id,'),
    ("H08", O, [PB17A, PB17B], "PB-17: la AUT- sin motivo", '"motivo": "dentro del tope de ampliación" if autoriza else "supera el tope o la fase no cambia la decisión"})', '"motivo": ""})'),
    ("H09", K, [PB17A, PB17B], "PB-17: una ampliación concedida no amplía nada", '            if concede:\n                self.ampliado[clase] += falta', '            if concede:\n                self.ampliado[clase] += 0.0'),
    ("H10", C, [PB22], "PB-22: canal no previsto sin incidencia en HA",
     '            self.almacen.incidencia("CANAL_NO_PREVISTO",\n                                    f"{msg[\'emisor\']} → {msg[\'receptor\']} por {msg[\'contrato\']} no previsto (R2)", msg["emisor"])\n', '            pass\n'),
    ("H11", C, [PB22], "PB-22: el mensaje rechazado queda en la traza de mensajes",
     '        msg.update(cuerpo)\n        self.validar(msg)\n', '        msg.update(cuerpo)\n        self.registro.append({k: msg.get(k) for k in ("msg_id", "contrato")})\n        self.validar(msg)\n'),
    ("H12", C, [PB22], "PB-22: un canal no previsto escribe además en F5",
     '            raise CanalNoPrevisto(f"{msg[\'emisor\']} → {msg[\'receptor\']} por {msg[\'contrato\']} no previsto (R2)")',
     '            self.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QA", "id": "QA-1"})\n            raise CanalNoPrevisto(f"{msg[\'emisor\']} → {msg[\'receptor\']} por {msg[\'contrato\']} no previsto (R2)")'),
    ("H13", C, [PB22], "PB-22: Redactor → Broker por CT-02 pasa a estar previsto", '"CT-02": [({"AG-01"}, {"BROKER"})],', '"CT-02": [({"AG-01", "AG-17"}, {"BROKER"})],'),
    ("H14", E, [PB33], "PB-33: la revocación por deterioro sin fecha",
     '"motivo_cambio": f"deterioro: BSS ≤ 0, ECE no disponible o ECE ≥ {ece_rev}",\n                                                              "fecha": str(pd.Timestamp(as_of).date())})',
     '"motivo_cambio": f"deterioro: BSS ≤ 0, ECE no disponible o ECE ≥ {ece_rev}"})'),
    ("H15", E, [PB33], "PB-33: la revocación sin motivo de deterioro", '"motivo_cambio": f"deterioro: BSS ≤ 0, ECE no disponible o ECE ≥ {ece_rev}",', '"motivo_cambio": "",'),
    ("H16", E, [PB33], "PB-33: no se revoca nunca por deterioro", 'if (bssv is not None and bssv <= 0) or ece_m is None or ece_m >= ece_rev:', 'if False:'),
    ("H17", E, [PB33], "PB-33: solo se revoca por BSS (se ignora la calibración)", 'if (bssv is not None and bssv <= 0) or ece_m is None or ece_m >= ece_rev:', 'if (bssv is not None and bssv <= 0):'),
    ("H18", E, [PB33], "PB-33: solo se revoca por calibración (se ignora el BSS)", 'if (bssv is not None and bssv <= 0) or ece_m is None or ece_m >= ece_rev:', 'if ece_m is None or ece_m >= ece_rev:'),
    ("H19", E, [PB45], "PB-45: el máximo pasa de 10 a 12", 'clase: str | None = None, max_n: int = 10)', 'clase: str | None = None, max_n: int = 12)'),
    ("H20", E, [PB45], "PB-45: primero las anecdóticas", 'orden = {"estadistica": 0, "recurrente": 1, "anecdotica": 2}', 'orden = {"estadistica": 2, "recurrente": 1, "anecdotica": 0}'),
    ("H21", E, [PB45], "PB-45: viajan las lecciones de otros tipos de activo", 'if clase and amb.get("clase") not in (None, clase):', 'if False:'),
    ("H22", E, [PB45], "PB-45: viajan lecciones caducadas", 'if pd.Timestamp(l["caducidad"]) < pd.Timestamp(as_of):\n                continue\n            amb', 'if False:\n                continue\n            amb'),
    ("H23", I, [PB59], "PB-59: la incidencia copia el valor", 'campo_afectado=sorted(set(respuesta) & CAMPOS_VALOR))', 'campo_afectado=sorted(set(respuesta) & CAMPOS_VALOR), fragmento=str(respuesta.get("valor")))'),
    ("H24", I, [PB59], "PB-59: sin incidencia en HA",
     '                self.b.almacen.incidencia("SEGURIDAD", "Respuesta CT-25 con un campo de valor de credencial rechazada íntegra (R8, 6.2.5)",\n                                          "BROKER", campo_afectado=sorted(set(respuesta) & CAMPOS_VALOR))\n', ''),
    ("H25", I, [PB59], "PB-59: la respuesta al Broker no pide renovar", 'y renuévela: ha quedado expuesta', ': ha quedado expuesta'),
    ("H26", I, [PB59], "PB-59: el valor queda en F5", '"estado": c["estado"], "incidencia": "Respuesta con el valor de la credencial "', '"estado": c["estado"], "copia": str(respuesta), "incidencia": "Respuesta con el valor de la credencial "'),
    # Filas AUTOMATICA del mapa, con las pruebas que el mapa cita
    ("A01", A, [U23], "PB-23 («hash de F4 sin cambios»): la escritura rechazada del Analizador en F4 SE GUARDA y después se rechaza",
     '                self._incidencia_interna("ACCESO_FUERA_DE_MATRIZ", f"{archivo}: {motivo}", autor)\n            raise EscrituraFueraDeReserva(motivo)',
     '                self._incidencia_interna("ACCESO_FUERA_DE_MATRIZ", f"{archivo}: {motivo}", autor)\n            if archivo == "F4" and autor == "AG-02":\n                self.escribir("F4", "AG-10", {**entrada, "estado": "ABIERTO"})\n            raise EscrituraFueraDeReserva(motivo)'),
]


def main() -> int:
    copia = Path(sys.argv[1]).resolve()
    assert "qa_f3_mut" in str(copia), "solo en la copia desechable"
    solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
    ej = copia / "bloque_a" / "11_Ejecutor"
    vivos = []
    for mid, fich, pruebas, desc, viejo, nuevo in MUTANTES:
        if solo and mid not in solo:
            continue
        ruta = ej / fich
        original = ruta.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}", flush=True); continue
        try:
            ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *pruebas], cwd=ej, capture_output=True, text=True, timeout=1800)
            ult = (r.stdout + r.stderr).strip().splitlines()[-1][:90]
            print(f"{mid} · {'MUERTO' if r.returncode else 'VIVO  '} · {desc} · {ult}", flush=True)
            if r.returncode == 0:
                vivos.append(mid)
        finally:
            ruta.write_text(original, encoding="utf-8")
    print("vivos: " + (", ".join(vivos) or "ninguno"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
