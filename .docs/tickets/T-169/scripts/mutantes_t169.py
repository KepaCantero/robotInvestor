"""T-169 · ejecuta los mutantes del revisor de T-162 (`.docs/tickets/T-162/revisores/r01_03_mutantes.py`) contra las pruebas de
T-169 y de T-162, sin cambiar el script del revisor (su lista de pruebas se llama `T162` y sus sondas fallan a propósito tras T-169,
así que `.docs/scripts/mutantes_revisor_ampliado.py`, que busca `PRUEBAS`, no sirve aquí).

Uso, desde la raíz de la copia de trabajo:
    .venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-162/revisores/r01_03_mutantes.py <copia> [M01 …]
    .venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py --propios <copia> [N01 …]   (los de `PROPIOS`, de T-169)
<copia>: carpeta desechable cuya ruta contiene «t169_mut», con `bloque_a` copiado del árbol de trabajo y `.venv` enlazado. Para
cada mutante: T-169 primero y, si sobrevive, T-162; imprime MUERTO (con la prueba) o VIVO y restaura el fichero. Sin red ni coste.
"""
import re
import subprocess
import sys
from pathlib import Path

RF, OR = "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py"
# Los de T-169: M03 y M24 del revisor sobre el texto nuevo, y los del código nuevo (id, descripción, fichero, texto, sustituto, equiv.)
PROPIOS = [
    ("M03b", "sin idempotencia (M03 sobre el texto de T-169)", RF, "        if previa is not None:\n            if provisional_msg_id",
     "        if False:\n            if provisional_msg_id", False),
    ("M24b", "TND- y CLM- de la opción no se citan (M24 sobre el texto de T-169)", RF, "candidatas += [opp, *tnd, *clm]",
     "candidatas += [opp]", False),
    ("N01", "nada para la consulta (H-01 deshecho)", RF,
     "return isinstance(error, ERRORES_DE_CONTROL) or not all(almacen.verificar_integridad().values())", "return False", False),
    ("N02", "sin mirar la integridad", RF, "or not all(almacen.verificar_integridad().values())", "or False", False),
    ("N03", "solo se relanza la integridad, no los controles", RF, "return isinstance(error, ERRORES_DE_CONTROL) or",
     "return False or", False),
    ("N04", "enviar no compara la provisional dada", RF, "if provisional_msg_id is not None and provisional_msg_id != registrado:",
     "if False:", False),
    ("N05", "enviar no exige la provisional registrada", RF,
     'if not isinstance(registrado, str) or not registrado.startswith("MSG-"):\n            raise',
     'if False:\n            raise', False),
    ("N06", "sin comprobar quién lanzó el RUN-", RF,
     'lanzado = es_run and (entrada_run.get("disparador") or {}).get("qry_id") == qry.get("id")', "lanzado = es_run", False),
    ("N07", "sin filtrar por tipo", RF,
     "return [x for x in textos if x.startswith(prefijo)], [x for x in textos if not x.startswith(prefijo)]", "return textos, []", False),
    ("N08", "la pendiente con la fecha de hoy y no la de su consulta", RF,
     "enviadas.append(enviar(bloque, qry_id, None, fecha))", "enviadas.append(enviar(bloque, qry_id, None, as_of))", False),
    ("N09", "las apartadas se reintentan", RF, ' and not q.get("final_no_enviable"))', ")", False),
    ("N10", "la apartada sin escalado al operador", RF, "escalado_operador=True,", "escalado_operador=False,", False),
    ("N11", "la clase del fallo no se guarda", RF, '**({"fallo_analisis": fallo} if fallo else {})', "**{}", False),
    ("N12", "la consulta no envía las pendientes", OR,
     ('        respuesta_final.enviar_pendientes(self, as_of)   # T-169 (H-02): las finales CT-03 que no salieron (sin ninguna, nada)\n'
      '        msg = self.mensajeria.crear("CT-03"'), '        msg = self.mensajeria.crear("CT-03"', False),
    ("N13", "el ciclo no envía las pendientes", OR,
     ('        respuesta_final.enviar_pendientes(self, as_of)   # T-169 (H-02): las finales CT-03 que no salieron (sin ninguna, nada)\n'
      '        run_id = self.almacen.nuevo_id("RUN")'), '        run_id = self.almacen.nuevo_id("RUN")', False),
    ("N14", "la consulta no registra la provisional", OR,
     'respuesta_final.registrar_provisional(self.almacen, qry_id, respuesta["msg_id"], fallo)', "pass", False),
    ("N15", "un rechazo de la pendiente para la consulta", RF, "except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO) as e:",
     "except ZeroDivisionError as e:", False),
    # r02: Q02–Q05 y Q09 del revisor de T-169 sobre el texto de la r02, y los del código de la r02
    ("Q02b", "pendientes en orden inverso", RF, "    return salida\n\n\ndef _apartar", "    return salida[::-1]\n\n\ndef _apartar", False),
    ("Q03b", "un rechazo de la pendiente sin mirar la integridad", RF,
     ("            except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO) as e:\n                if not all(almacen.verificar_integridad().values()):\n"
      "                    raise\n"), "            except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO) as e:\n", False),
    ("Q04b", "MensajeInvalido deja de ser un error de control", RF,
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion, ReplayFaltante)",
     "ERRORES_DE_CONTROL = (PermissionError, FugaDeInformacion, ReplayFaltante)", False),
    ("Q05b", "FugaDeInformacion deja de ser un error de control", RF,
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion, ReplayFaltante)",
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, ReplayFaltante)", False),
    ("Q09b", "las pendientes con la fecha del ciclo y no la de cada consulta", RF,
     "enviadas.append(enviar(bloque, qry_id, None, fecha))", "enviadas.append(enviar(bloque, qry_id, None, as_of or fecha))", False),
    ("R01", "ReplayFaltante deja de ser un error de control (H-02 deshecho)", RF,
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion, ReplayFaltante)",
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion)", False),
    ("R02", "cualquier error de una pendiente para (H-01 deshecho)", RF,
     "            except Exception as e:\n                if para_la_consulta(almacen, e):\n                    raise\n",
     "            except Exception as e:\n                raise\n", False),
    ("R03", "sin la transacción alrededor del apartado (H-03 deshecho)", RF,
     "        with almacen._transaccion():\n            ahora", "        with __import__('contextlib').nullcontext():\n            ahora", False),
    ("R04", "sin volver a mirar dentro si ya está apartada", RF,
     '            if ahora.get("final_no_enviable"):\n                continue\n', "", False),
    ("S01", "un error corriente de una pendiente se aparta aunque el almacén esté roto (H-02 de la r02)", RF,
     "            except Exception as e:\n                if para_la_consulta(almacen, e):",
     "            except Exception as e:\n                if isinstance(e, ERRORES_DE_CONTROL):", False),
]
COPIA = Path(sys.argv[2]).resolve()
SOLO = set(sys.argv[3:])
assert "t169_mut" in str(COPIA)
if sys.argv[1] == "--propios":
    espacio: dict = {"MUTANTES": PROPIOS}
else:
    fuente = Path(sys.argv[1]).read_text(encoding="utf-8")
    ini, fin = fuente.index("RF, OR = "), fuente.find("\n\n\ndef pytest")
    fin = fin if fin >= 0 else len(fuente)   # r02: la lista del revisor de T-169 va sola, sin bucle propio
    espacio = {"COPIA": COPIA, "Path": Path}
    exec(fuente[ini:fin], espacio)   # noqa: S102 — la lista literal de mutantes del script del revisor
EJ = COPIA / "bloque_a" / "11_Ejecutor"
PRUEBAS = [["tests/test_t169_r02.py", "tests/test_t169_hallazgos_t162.py"], ["tests/test_t162_respuesta_final.py"]]
for mid, desc, fichero, texto, sustituto, equiv in espacio["MUTANTES"]:
    if SOLO and mid not in SOLO:
        continue
    ruta = EJ / fichero
    original = ruta.read_text(encoding="utf-8")
    if original.count(texto) != 1:
        print(f"{mid} TEXTO_CAMBIADO ({original.count(texto)}) {desc}", flush=True)
        continue
    ruta.write_text(original.replace(texto, sustituto), encoding="utf-8")
    try:
        veredicto = "VIVO"
        for nombre, pruebas in zip(("T-169", "T-162"), PRUEBAS):   # T-169 = r02 y r01
            r = subprocess.run([str(COPIA / ".venv" / "bin" / "python"), "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                                "-W", "ignore", *pruebas], cwd=EJ, capture_output=True, text=True, timeout=3000, check=False)
            if r.returncode != 0:
                muertos = re.findall(r"FAILED (\S+)", r.stdout)
                veredicto = f"MUERTO ({nombre}: {muertos[0].split('::')[-1] if muertos else 'error'})"
                break
    finally:
        ruta.write_text(original, encoding="utf-8")
    print(f"{mid} {veredicto} · {desc}{' (equiv.)' if equiv else ''}", flush=True)
