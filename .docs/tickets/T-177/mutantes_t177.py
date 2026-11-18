"""Mutantes propios de T-177: cada uno cambia una línea del código y las pruebas de `test_t177_c4_credenciales.py` deben
matarlo. Se ejecuta con el Python del `.venv` desde cualquier sitio; restaura cada archivo al terminar (también si falla).

    python .docs/tickets/T-177/mutantes_t177.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

EJ = Path(__file__).resolve().parents[3] / "bloque_a" / "11_Ejecutor"
PRUEBAS = ["tests/test_t177_c4_credenciales.py"]
IB, MC, AG, MR = "bloque_a/interfaz_broker.py", "bloque_a/mantenimiento_c4.py", "bloque_a/agentes.py", "bloque_a/mock_respuestas.py"
LL, CO = "bloque_a/llm.py", "bloque_a/contratos.py"
MUTANTES = [
    ("M01 sin deduplicar", IB, "            if alias in vistos:   # deduplicación", "            if False:   # deduplicación"),
    ("M02 sin comprobar HT-01", "bloque_a/interfaz_broker.py",
     '        if e["estado"] == "PROVISTA":\n            return {"estado": "PROVISTA", "credencial_ref": e["alias"], "solicitud": None}',
     '        if False:\n            return {"estado": "PROVISTA", "credencial_ref": e["alias"], "solicitud": None}'),
    ("M03 sin rechazo del valor en el Coordinador", IB, "            sensible = bool(claves_valor_credencial(retorno)) or bool(contiene_credenciales(retorno))",
     "            sensible = False"),
    ("M04 sin la segunda barrera de agentes", AG, "solicitud_con_valor(json.dumps(datos, ensure_ascii=False, default=str))))",
     "False))"),
    ("M05 solicitante distinto", MC, 'AGENTE_BFA, as_of, origen=c4_id)', '"AG-02", as_of, origen=c4_id)'),
    ("M06 sin C4- en F5", MC, '    bloque.almacen.escribir("F5", "AG-01", entrada)\n', ""),
    ("M07 el Coordinador no lee el retorno", MC, "desde_retorno(datos, AGENTE_BFA", "desde_retorno(None, AGENTE_BFA"),
    ("M08 urgencia sin filtrar", IB, 'urgencia = "ALTA" if s.get("urgencia") == "ALTA" else "NORMAL"', 'urgencia = s.get("urgencia") or "NORMAL"'),
    ("M09 el BFA ve la ficha entera del índice", MC, '        vista.append({**s, "credencial_ref": e.get("alias"), "estado": e.get("estado")})',
     '        vista.append({**s, **e, "credencial_ref": e.get("alias"), "estado": e.get("estado")})'),
    ("M10 sin validar la configuración", MC, "    servicios = servicios_bfa(bloque.cfg)   # valida antes de mutar",
     "    servicios = list((bloque.cfg.get('credenciales') or {}).get('servicios_bfa') or [])"),
    ("M11 motivo descartado sin pedir impacto", IB,
     '                      "impacto_si_falta": s.get("impacto_si_falta", s.get("impacto"))}',
     '                      "impacto_si_falta": s.get("impacto_si_falta", s.get("impacto")) or "—"}'),
    ("M12 el simulado pide también lo PROVISTA", MR, 'if s.get("estado") != "PROVISTA"]', "]"),
    # r02 (QA r01)
    ("M13 respuesta_segura sin solicitud_con_valor (H-01, H-04)", LL,
     "if contenido_sensible(r.texto) or solicitud_con_valor(r.texto):", "if contenido_sensible(r.texto):"),
    ("M16 deduplicación literal entre C4 (H-02)", IB,
     'if alias_de(str(c.get("servicio") or "")) == alias_de(servicio)]', 'if c.get("servicio") == servicio]'),
    ("M17 sin transacción en solicitar (H-03)", IB, "        with self.b.almacen._transaccion():\n            # H-02",
     "        with self.boveda._lock:\n            # H-02"),
    ("M18 clave sin normalizar (H-05)", CO, 'return re.sub(r"[^a-z0-9ñ]", "", str(k).lower())', "return str(k).lower()"),
    ("M19 sin «credencial» en la lista (H-05)", CO, '"valorcredencial", "credencial", "credential",', '"valorcredencial", "credential",'),
    ("M22 se llama al BFA sin servicios (H-07 a)", MC, "    if not vista:   # T-177 r02", "    if False:   # T-177 r02"),
    ("M23 bolsa por llamada, no semanal (H-07 b)", MC, "    restante = semana - uc_c4_semana(bloque, as_of)", "    restante = semana"),
    ("M24 la respuesta del Broker sin normalizar (H-05)", IB,
     "con_valor = sorted(str(k) for k in respuesta if clave_normalizada(k) in CAMPOS_VALOR)",
     "con_valor = sorted(str(k) for k in respuesta if str(k) in CAMPOS_VALOR)"),
    ("M25 la caché envenenada se sirve", AG,
     "                    and not solicitud_con_valor(json.dumps(previo, ensure_ascii=False, default=str))   # T-177 r02\n", ""),
    # r03 (QA r02)
    ("M14 la clave de solicitudes sin normalizar (H-01)", CO, "if clave_normalizada(k) == CLAVE_SOLICITUDES:\n                out.append(v)",
     'if k == "solicitudes_credenciales":\n                out.append(v)'),
    ("M15 ilegible no falla cerrado", LL, "    return (CLAVE_SOLICITUDES in clave_normalizada(texto)",
     "    return False and (CLAVE_SOLICITUDES in clave_normalizada(texto)"),
    ("M20 sin ficha opaca en el Coordinador (H-06, H-08)", IB, "            opaca = retorno_con_credencial(retorno)",
     "            opaca = False"),
    ("M27 prefiltro textual antes del JSON (H-09)", LL, "    try:\n        leido, datos = _leer_json(texto)",
     "    if CLAVE_SOLICITUDES not in clave_normalizada(texto):\n        return False\n    try:\n        leido, datos = _leer_json(texto)"),
    ("M28 sin base64 con barras (H-10)", CO, 'if "." not in p and ":" not in p and RE_PALABRA_BASE64.fullmatch(p):',
     "if False:"),
    ("M29 números no cuentan en el subárbol (H-11)", CO, "con_contenido = _tiene_texto(x) or _tiene_numero(x)",
     "con_contenido = _tiene_texto(x)"),
    ("M30 claves ambiguas como inequívocas fuera (H-12)", CO, "                if n not in CAMPOS_VALOR_AMBIGUOS and _tiene_texto(x):",
     "                if _tiene_texto(x):"),
    ("M31 guiones dentro de la ficha (H-13)", CO, 'RE_FICHA_OPACA = re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9]*[A-Za-z])(?=[A-Za-z0-9]*\\d)[A-Za-z0-9]"',
     'RE_FICHA_OPACA = re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9_\\-]*[A-Za-z])(?=[A-Za-z0-9_\\-]*\\d)[A-Za-z0-9_\\-]"'),
    ("M32 sin el retorno entero si pide algo (r03)", CO, "    if any(s not in (None, [], {}, \"\") for s in subarboles) and any(ficha_opaca(x) for x in _textos_de(datos)):",
     "    if False:"),
    ("M33 sin reserva de la bolsa (observación r02)", MC, "        reservado = bool(vista) and restante > 0\n        if reservado:",
     "        reservado = bool(vista) and restante > 0\n        if False:"),
    ("M34 la reserva cuenta dos veces", MC, '    total = 0.0\n    for e in bloque.almacen.estado("F5").values():',
     '    total = 0.0\n    for e in bloque.almacen.leer("F5"):'),
    ("M35 el mock de Analistas sin solicitudes_credenciales (H-12)", MR,
     '"senales_para_otras_clases": [], "solicitudes_credenciales": [],', '"senales_para_otras_clases": [],'),
    # ronda de cierre (QA r03)
    ("M36 sin resolver los escapes en el prefiltro (H-14)", LL,
     "    return (CLAVE_SOLICITUDES in clave_normalizada(texto)\n            or CLAVE_SOLICITUDES in",
     "    return (CLAVE_SOLICITUDES in clave_normalizada(texto)\n            and CLAVE_SOLICITUDES in"),
    ("M37 sin identificadores públicos fuera (H-15)", CO, "any(ficha_opaca(_sin_publicos(s)) for s in _textos_de(x)):",
     "any(ficha_opaca(s) for s in _textos_de(x)):"),
    ("M38 LEI sin comprobar el módulo 97 (H-15)", CO, 'return int("".join(str(int(c, 36)) for c in t)) % 97 == 1', "return True"),
    ("M39 sin aviso de la reserva huérfana (H-16)", MC, "        if _pid_vivo(e.get(\"pid\")) is False and e[\"id\"] not in avisadas:",
     "        if False:"),
    ("M40 el aviso se repite (H-16)", MC, " and e[\"id\"] not in avisadas:", ":"),
    ("M41 sin CAMPOS_SOLICITUD (H-17)", CO, "if con_contenido and (n in CAMPOS_VALOR_CREDENCIAL or k not in CAMPOS_SOLICITUD_LITERALES",
     "if con_contenido and (n in CAMPOS_VALOR_CREDENCIAL or False"),
    # segunda ronda de cierre (H-18)
    ("M42 clave normalizada en lugar de literal (H-18 c)", CO, "or k not in CAMPOS_SOLICITUD_LITERALES",
     "or n not in CAMPOS_SOLICITUD"),
    ("M43 urgencia sin comprobar (H-18 a)", CO, 'or (k == "urgencia" and x not in URGENCIAS)', "or False"),
    ("M44 impacto duplicado sin comprobar (H-18 b)", CO, 'or (k == "impacto" and "impacto_si_falta" in v)', "or False"),
]


def main() -> int:
    vivos = []
    for nombre, rel, viejo, nuevo in MUTANTES:
        p = EJ / rel
        original = p.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{nombre}: el texto a mutar no aparece una sola vez en {rel}")
            return 2
        try:
            p.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=EJ,
                               capture_output=True, text=True, check=False)
        finally:
            p.write_text(original, encoding="utf-8")
        estado = "MUERTO" if r.returncode != 0 else "VIVO"
        print(f"{nombre}: {estado}")
        if estado == "VIVO":
            vivos.append(nombre)
    print(f"{len(MUTANTES) - len(vivos)}/{len(MUTANTES)} muertos")
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
