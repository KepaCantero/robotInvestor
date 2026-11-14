"""QA r02 de T-114 · Mutantes NUEVOS de `bloque_a/contratos.py` (no los de la r01): ¿los ven los goldens que no dependen
de los flujos (tablas, esquemas de respuesta, mensajes de ejemplo y aceptaciones y rechazos)?

Medida rápida en proceso: cada mutante se aplica a una COPIA del módulo, cargada aparte (el paquete no se toca), y se
generan con ella los cuatro goldens que no necesitan los flujos simulados; se comparan con los congelados. Los que no
cambian nada se confirman, con `--confirmar <copia_desechable>`, ejecutando `python tests/goldens_ct.py` entero en una copia
desechable del repositorio (ruta con «qa_f3_mut») con el mutante aplicado al fichero de verdad.

Uso, desde la raíz del repositorio:
    python .docs/tickets/T-114/revisores/r02_01_mutantes_mensajeria_nuevos.py [--confirmar <copia_desechable>]
Termina siempre con 0: es una medida, no un gate.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]
import goldens_ct as g  # noqa: E402

from bloque_a import contratos  # noqa: E402

PY = "/home/user/robotinvestor/.venv/bin/python"
FECHA = "2026-06-05"

# (id, descripción, texto original, texto mutado) sobre bloque_a/contratos.py
MUTANTES = [
    ("C01", "R8: el examen de datos protegidos deja fuera `limitaciones`",
     'cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp")})',
     'cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp", "limitaciones")})'),
    ("C02", "R8: el examen de datos protegidos deja fuera `presupuesto` y `consumo`",
     'cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp")})',
     'cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp", "presupuesto", "consumo")})'),
    ("C03", "R8: el examen deja fuera `autoevaluacion`",
     'cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp")})',
     'cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp", "autoevaluacion")})'),
    ("C04", "run_id: basta con que la clave exista (un run_id vacío pasa por validar)",
     'if not msg.get("run_id") and not msg.get("query_id") and msg["contrato"]',
     'if "run_id" not in msg and "query_id" not in msg and msg["contrato"]'),
    ("C05", "run_id: query_id ya no basta",
     'if not msg.get("run_id") and not msg.get("query_id") and msg["contrato"]',
     'if not msg.get("run_id") and msg["contrato"]'),
    ("C06", "campos comunes: basta con que la clave exista (vacía pasa)",
     '            if not msg.get(c):\n                raise MensajeInvalido(f"Falta el campo común {c}")',
     '            if c not in msg:\n                raise MensajeInvalido(f"Falta el campo común {c}")'),
    ("C07", "orden: los datos protegidos se miran antes que el canal",
     '        if not canal_permitido(msg["contrato"], msg["emisor"], msg["receptor"], self.v6):',
     '        if contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp")}):\n'
     '            raise DatosSensibles(f"Mensaje {msg[\'msg_id\']} con datos protegidos en []")\n'
     '        if not canal_permitido(msg["contrato"], msg["emisor"], msg["receptor"], self.v6):'),
    ("C08", "estado propio: el estado común del cuerpo se descarta sea cual sea el que se pasa por su sitio",
     'if campo in cuerpo and antiguo == (estado or "COMPLETO"):', 'if campo in cuerpo and antiguo in ESTADOS:'),
    ("C09", "CT-01: `horizontes` admite también un texto (\"\" pasa)",
     'not isinstance(msg["horizontes"], list)', 'not isinstance(msg["horizontes"], (list, str))'),
    ("C10", "msg_id del Broker: re.match en vez de fullmatch", 're.fullmatch(r"MSG-BRK-[0-9]{4}-[0-9]{1,12}", externo)',
     're.match(r"MSG-BRK-[0-9]{4}-[0-9]{1,12}", externo)'),
    ("C11", "msg_id del Broker: un vacío cuenta como ausente", 'if externo is not None and (', 'if externo and ('),
    ("C12", "retorno: `autoevaluacion` por defecto nula", 'msg.setdefault("autoevaluacion", "")', 'msg.setdefault("autoevaluacion", None)'),
    ("C13", "retorno: `limitaciones` del cuerpo ya no se conservan (siempre vacías)",
     '        msg.update(cuerpo)\n', '        msg.update(cuerpo)\n        if tipo_mensaje == "RETORNO":\n            msg["limitaciones"] = []\n'),
    ("C14", "reservados: `timestamp` deja de estarlo", '"tipo_mensaje", "run_id", "query_id", "presupuesto", "consumo", "estado"}',
     '"tipo_mensaje", "run_id", "query_id", "presupuesto", "consumo", "estado"} - {"timestamp"}'),
    ("C15", "CT-02: el resumen puede ser una lista", 'or not isinstance(msg.get("resumen"), dict)', 'or not isinstance(msg.get("resumen"), (dict, list))'),
    ("C16", "estado común: None cuenta como válido", 'if tipo != "ENCARGO" and msg.get("estado") not in ESTADOS:',
     'if tipo != "ENCARGO" and msg.get("estado") not in (*ESTADOS, None):'),
    ("C17", "estado propio: también admite el estado común COMPLETO",
     'if msg.get(campo) not in ESTADOS_ESPECIFICOS[msg["contrato"]]:', 'if msg.get(campo) not in (*ESTADOS_ESPECIFICOS[msg["contrato"]], "COMPLETO"):'),
    ("C18", "la mensajería aplica la lista cerrada de `frecuencia` de CT-24",
     '        if tipo == "RETORNO" and msg["contrato"] == "CT-02" and (',
     '        if tipo == "ENCARGO" and msg["contrato"] == "CT-24" and msg.get("frecuencia", "DIARIA") not in ("DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL", "TRIMESTRAL", "PERSONALIZADA"):\n'
     '            raise MensajeInvalido("CT-24: frecuencia")\n'
     '        if tipo == "RETORNO" and msg["contrato"] == "CT-02" and ('),
    ("C19", "CT-01: horizontes vacíos dejan de admitirse", 'not isinstance(msg["horizontes"], list) or any(',
     'not isinstance(msg["horizontes"], list) or not msg["horizontes"] or any('),
    ("C20", "un encargo sin presupuesto ya no lleva la clave", 'msg["presupuesto"] = presupuesto or {}',
     'if presupuesto is not None:\n                msg["presupuesto"] = presupuesto'),
]


def cargar(fuente: str, carpeta: Path):
    ruta = carpeta / "contratos_mutado_qa_r02.py"
    ruta.write_text(fuente, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("contratos_mutado_qa_r02", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def medir(modulo) -> list[str]:
    """Goldens que no dependen de los flujos, generados con `modulo` en lugar de `contratos`; devuelve los que cambian."""
    esquemas, ejemplos = g.leer_a_mano()
    bateria = g.leer_bateria()
    original = g.contratos
    g.contratos = modulo
    try:
        with tempfile.TemporaryDirectory() as tmp:
            textos = {"tablas_contratos.json": g.texto(g.tablas()), "esquemas_respuestas.json": g.texto(g.esquemas_respuestas()),
                      "mensajes_ejemplo.json": g.texto(g.mensajes_ejemplo(ejemplos, Path(tmp), FECHA)),
                      "aceptaciones_rechazos.json": g.texto(g.aceptaciones(bateria, ejemplos, Path(tmp), FECHA, modulo))}
    except Exception as e:   # noqa: BLE001 — un mutante que rompe la generación cuenta como detectado (goldens_ct termina con 1)
        return [f"error al generar: {type(e).__name__}"]
    finally:
        g.contratos = original
    return [n for n, t in textos.items() if (g.CARPETA / n).read_text(encoding="utf-8") != t]


def confirmar(copia: Path, viejo: str, nuevo: str) -> int:
    ruta = copia / "bloque_a" / "11_Ejecutor" / "bloque_a" / "contratos.py"
    original = ruta.read_text(encoding="utf-8")
    try:
        ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        return subprocess.run([PY, "tests/goldens_ct.py"], cwd=copia / "bloque_a" / "11_Ejecutor", capture_output=True, text=True).returncode
    finally:
        ruta.write_text(original, encoding="utf-8")


def main() -> int:
    copia = Path(sys.argv[sys.argv.index("--confirmar") + 1]).resolve() if "--confirmar" in sys.argv else None
    if copia is not None and "qa_f3_mut" not in str(copia):
        print("solo se confirma en una copia desechable (ruta con qa_f3_mut)")
        return 0
    fuente = Path(contratos.__file__).read_text(encoding="utf-8")
    vivos = []
    with tempfile.TemporaryDirectory() as tmp:
        control = medir(cargar(fuente, Path(tmp)))
        print(f"control (copia sin cambios): {'coincide' if not control else control}")
        for mid, desc, viejo, nuevo in MUTANTES:
            if fuente.count(viejo) != 1:
                print(f"{mid} · NO APLICADO ({fuente.count(viejo)} apariciones) · {desc}")
                continue
            cambian = medir(cargar(fuente.replace(viejo, nuevo), Path(tmp)))
            linea = f"{mid} · {'DETECTADO por ' + ', '.join(cambian) if cambian else 'NO DETECTADO'} · {desc}"
            if not cambian and copia is not None:
                rc = confirmar(copia, viejo, nuevo)
                linea += f" · goldens_ct.py entero en la copia: rc={rc} ({'DETECTADO' if rc else 'NO DETECTADO'})"
                cambian = ["goldens_ct"] if rc else []
            if not cambian:
                vivos.append(mid)
            print(linea, flush=True)
    print("vivos: " + (", ".join(vivos) or "ninguno"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
