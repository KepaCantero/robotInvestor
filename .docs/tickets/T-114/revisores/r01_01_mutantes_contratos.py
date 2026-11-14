"""QA r01 de T-114 · Mutantes de `bloque_a/contratos.py`: ¿los detecta `python tests/goldens_ct.py`?

Uso:  python r01_01_mutantes_contratos.py <copia_desechable_del_repo> [--suite "expresión -k o rutas de pytest"]
Trabaja SOLO en la copia desechable (nunca en el repo): aplica un mutante, ejecuta el comprobador, restaura.
Con --suite, para los mutantes que el comprobador no ve ejecuta además esas pruebas de la suite (pytest -x -q).
Termina siempre con 0: es una medida, no un gate.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"

# (id, descripción, texto original, texto mutado) — todos sobre bloque_a/contratos.py
MUTANTES = [
    ("M01", "CANALES CT-06 sin canal de vuelta", '"CT-06": _par({"AG-02"}, ANALISTAS),', '"CT-06": [({"AG-02"}, ANALISTAS)],'),
    ("M02", "CANALES CT-09 pierde AG-20", '_par({"AG-02", "AG-10", "AG-20", "AG-18", "AG-19",', '_par({"AG-02", "AG-10", "AG-18", "AG-19",'),
    ("M03", "CANALES_V6 CT-15 a AG-27", '"CT-15": _par({"AG-02"}, {"AG-26"}),', '"CT-15": _par({"AG-02"}, {"AG-27"}),'),
    ("M04", "ANALISTAS gana AG-10", 'ANALISTAS = {"AG-03",', 'ANALISTAS = {"AG-10", "AG-03",'),
    ("M05", "CAMPOS_MINIMOS CT-07 sin max_fuentes (solo CT-07)",
     '"CT-07": ["pregunta", "objetivo", "clase", "horizonte", "profundidad", "max_fuentes", "fecha_limite_informacion"],',
     '"CT-07": ["pregunta", "objetivo", "clase", "horizonte", "profundidad", "fecha_limite_informacion"],'),
    ("M06", "CAMPOS_MINIMOS CT-11 piezas→pieza", '"CT-11": ["piezas"],', '"CT-11": ["pieza"],'),
    ("M07", "CAMPOS_RETORNO CT-23 sin estado", '"CT-23": ["cns_id", "estado"]', '"CT-23": ["cns_id"]'),
    ("M08", "orden de CAMPOS_MINIMOS CT-10 invertido", '"CT-10": ["artefacto_id", "motivo"],', '"CT-10": ["motivo", "artefacto_id"],'),
    ("M09", "ESQUEMAS: DIM máximo 100→90", '"minimum": 0, "maximum": 100, "multipleOf": 10', '"minimum": 0, "maximum": 90, "multipleOf": 10'),
    ("M10", "ESQUEMAS: glosario maxItems 5→6", '"glosario": {"type": "array", "maxItems": 5,', '"glosario": {"type": "array", "maxItems": 6,'),
    ("M11", "ESQUEMAS: REGIONES pierde GLB", '"JPN", "OCE", "GLB"]', '"JPN", "OCE"]'),
    ("M12", "ESQUEMAS: DICTAMEN_G3 admite APTO", '"dictamen": {"enum": ["APTO_CON_ADVERTENCIAS", "BLOQUEADO"]}', '"dictamen": {"enum": ["APTO", "APTO_CON_ADVERTENCIAS", "BLOQUEADO"]}'),
    ("M13", "crear: ENCARGO sin presupuesto por defecto", 'msg["presupuesto"] = presupuesto or {}', 'if presupuesto:\n                msg["presupuesto"] = presupuesto'),
    ("M14", "crear: RETORNO sin limitaciones por defecto", 'msg.setdefault("limitaciones", [])', 'pass'),
    ("M15", "crear: estado por defecto PARCIAL", 'msg["estado"] = estado or "COMPLETO"', 'msg["estado"] = estado or "PARCIAL"'),
    ("M16", "crear: msg_id de ancho 5", 'if amb else "MSG", ancho=6)', 'if amb else "MSG", ancho=5)'),
    ("M17", "crear: campo nuevo en el sobre", '"timestamp": self.almacen.reloj.ahora(), "tipo_mensaje": tipo_mensaje}', '"timestamp": self.almacen.reloj.ahora(), "tipo_mensaje": tipo_mensaje, "esquema": "x"}'),
    ("M18", "crear: tipo_mensaje renombrado en la traza (registro)", 'for k in ("msg_id", "contrato", "emisor", "receptor", "tipo_mensaje")})', 'for k in ("msg_id", "contrato", "emisor", "receptor")})'),
    ("M19", "crear: el cuerpo ya no puede repetir un reservado igual (siempre rechaza)", 'if cuerpo[campo] != msg.get(campo):', 'if True:'),
    ("M20", "crear: el cuerpo puede pisar reservados (no rechaza ni retira)",
     '            if cuerpo[campo] != msg.get(campo):\n                raise MensajeInvalido(f"No se puede cambiar {campo} desde el cuerpo")\n            cuerpo.pop(campo)',
     '            pass'),
    ("M21", "crear: msg_id externo del Broker con otro formato", 'r"MSG-BRK-[0-9]{4}-[0-9]{1,12}"', 'r"MSG-EXT-[0-9]{4}-[0-9]{1,12}"'),
    ("M22", "crear: estado de objeto contradictorio ya no se rechaza", 'if campo in cuerpo and cuerpo[campo] != antiguo:', 'if False:'),
    ("M23", "validar: CT-01 admite tipo SEGUIMIENTO", 'not in ("AD_HOC", "PROFUNDIZACION", "PERIODICO")', 'not in ("AD_HOC", "PROFUNDIZACION", "PERIODICO", "SEGUIMIENTO")'),
    ("M24", "validar: CT-01 admite prioridad URGENTE", 'not in ("ALTA", "NORMAL", "BAJA")', 'not in ("ALTA", "NORMAL", "BAJA", "URGENTE")'),
    ("M25", "validar: CT-01 admite horizonte H6", 'h not in ("H1", "H2", "H3", "H4", "H5")', 'h not in ("H1", "H2", "H3", "H4", "H5", "H6")'),
    ("M26", "validar: CT-01 pierde el horizonte H5", 'h not in ("H1", "H2", "H3", "H4", "H5")', 'h not in ("H1", "H2", "H3", "H4")'),
    ("M27", "validar: CT-02 admite estado_g3 BLOQUEADO", 'not in ("APTO", "APTO_CON_ADVERTENCIAS")):', 'not in ("APTO", "APTO_CON_ADVERTENCIAS", "BLOQUEADO")):'),
    ("M28", "validar: CT-05 exento de run_id/query_id", '("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25")', '("CT-01", "CT-03", "CT-04", "CT-05", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25")'),
    ("M29", "validar: CT-23 deja de estar exento de run_id/query_id", '("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25")', '("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-24", "CT-25")'),
    ("M30", "validar: no comprueba credenciales", '        if cred:\n            campos', '        if False:\n            campos'),
    ("M31", "validar: no comprueba el estado específico de CT-23/24/25", 'if msg.get(campo) not in ESTADOS_ESPECIFICOS[msg["contrato"]]:', 'if False:'),
    ("M32", "validar: no comprueba el estado de retorno", 'if tipo != "ENCARGO" and msg.get("estado") not in ESTADOS:', 'if False:'),
    ("M33", "validar: no comprueba la versión del contrato", 'if msg["version_contrato"] != VERSION_CONTRATO or msg.get("tipo_mensaje")', 'if msg.get("tipo_mensaje")'),
    ("M34", "validar: no exige campos mínimos", '        if falta:\n            raise MensajeInvalido(f"{msg[\'contrato\']}: faltan campos mínimos {falta}")', '        if False:\n            pass'),
    ("M35", "validar: texto del rechazo por campos mínimos", 'faltan campos mínimos {falta}', 'faltan campos {falta}'),
    ("M36", "validar: CT-02 no exige resumen dict", 'or not isinstance(msg.get("resumen"), dict)', ''),
    ("M37", "ESTADOS_ESPECIFICOS CT-23 gana ANULADA", '"CT-23": ("RESPONDIDA", "PARCIAL", "VENCIDA", "RECIBIDA")', '"CT-23": ("RESPONDIDA", "PARCIAL", "VENCIDA", "RECIBIDA", "ANULADA")'),
    ("M38", "crear: admite un tercer tipo de mensaje ACUSE", 'msg.get("tipo_mensaje") not in ("ENCARGO", "RETORNO")', 'msg.get("tipo_mensaje") not in ("ENCARGO", "RETORNO", "ACUSE")'),
    ("M39", "crear: CT-01 ya no retira el msg_id externo del cuerpo", 'if contrato == "CT-01" and emisor == "BROKER" else None', 'if contrato == "CT-01" and emisor == "NADIE" else None'),
    ("M40", "validar: CT-01 no comprueba que alcance sea objeto", 'if not isinstance(msg["alcance"], dict) or not isinstance', 'if not isinstance'),
]


def ejecutar(orden: list[str], cwd: Path) -> tuple[int, str]:
    r = subprocess.run(orden, cwd=cwd, capture_output=True, text=True, timeout=1800)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1][:160] if (r.stdout + r.stderr).strip() else ""


def main() -> int:
    copia = Path(sys.argv[1]).resolve()
    suite = sys.argv[sys.argv.index("--suite") + 1].split() if "--suite" in sys.argv else None
    solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
    if "qa_f3_mut" not in str(copia):
        print("solo se muta en la copia desechable"); return 0
    ej = copia / "bloque_a" / "11_Ejecutor"
    ruta = ej / "bloque_a" / "contratos.py"
    original = ruta.read_text(encoding="utf-8")
    rc, _ = ejecutar([PY, "tests/goldens_ct.py"], ej)
    print(f"base: goldens_ct rc={rc}")
    vivos = []
    try:
        for mid, desc, viejo, nuevo in MUTANTES:
            if solo and mid not in solo:
                continue
            if original.count(viejo) != 1:
                print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}"); continue
            ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            rc, ult = ejecutar([PY, "tests/goldens_ct.py"], ej)
            linea = f"{mid} · goldens_ct rc={rc} ({'DETECTADO' if rc else 'NO DETECTADO'}) · {desc}"
            if rc == 0 and suite:
                rs, us = ejecutar([PY, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *suite], ej)
                linea += f" · suite rc={rs} ({'DETECTADO' if rs else 'VIVO'}): {us}"
                if rs == 0:
                    vivos.append(mid)
            elif rc == 0:
                vivos.append(mid)
            print(linea, flush=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    print("no detectados por lo ejecutado: " + (", ".join(vivos) or "ninguno"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
