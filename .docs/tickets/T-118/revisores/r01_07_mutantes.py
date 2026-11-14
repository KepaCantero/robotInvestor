"""QA r01 de T-118 · Mutantes: cada corrección de H-09 a H-14, deshecha de una en una, ¿la detecta alguna prueba?

Uso: python r01_07_mutantes.py <copia_desechable_de_bloque_a/11_Ejecutor> [--solo M01,M02] [--todo]
La copia debe tener «qa2_mut» en la ruta. Cada mutante ejecuta `tests/test_t118_hallazgos.py` filtrado por su hallazgo
(-k h09, h10…) con -x; con --todo, además `tests/test_t112_motor.py` y `tests/test_fase2_riesgo.py` para los que queden vivos.
MUERTO = alguna prueba falla; VIVO = todas pasan. Restaura el fichero tras cada mutante.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
copia = Path(sys.argv[1]).resolve()
assert "qa2_mut" in str(copia) and (copia / "bloque_a" / "motor" / "servicio.py").exists(), "solo en la copia desechable del ejecutor"
SV, RI, SE, RE = (f"bloque_a/motor/{n}.py" for n in ("servicio", "fichas_riesgo", "fichas_series", "fichas_reales"))

M = [
    # ---------------------------------------------------------------- H-09
    ("M01", RI, "h09", "ML-PRED: sin comprobar las fechas contra el corte", '    _hasta_corte(fechas, corte, f"{F}: fechas")\n', ''),
    ("M02", RI, "h09", "ML-PRED: sin comprobar conocible_desde contra el corte", '        _hasta_corte(cd, corte, f"{q}: conocible_desde")\n', ''),
    ("M03", RI, "h09", "ML-CAL: sin comprobar los pares fechados", '            _hasta_corte([pd.Timestamp(fechas[-1])], corte, f"{q}: predicciones y realizaciones")',
     '            pass'),
    ("M04", RI, "h09", "el día del corte ya no es conocible (> pasa a >=)", 'if ultima.normalize() > corte.normalize():', 'if ultima.normalize() >= corte.normalize():'),
    ("M05", RI, "h09", "se compara con hora, no por día", 'if ultima.normalize() > corte.normalize():', 'if ultima > corte:'),
    ("M06", RI, "h09", "una fecha de corte ilegible se ignora", '        raise ErrorFicha(f"fecha de corte de la petición ilegible ({str(fc)[:40]})") from e', '        return None'),
    # ---------------------------------------------------------------- H-10
    ("M10", RI, "h10", "RISK-VAR: historia sin cota", 'return _rendimientos(ent, F, maximo=_observaciones_maximas(_configuracion(ent))), "historia"', 'return _rendimientos(ent, F), "historia"'),
    ("M11", RI, "h10", "RISK-VAR: distribución sin cota", '                    maximo=UMBRALES[F]["distribucion_maxima"])', '                    maximo=None)'),
    ("M12", RI, "h10", "SIM-MC: residuos sin cota", 'z = _vector(_requerido(d, "residuos", q), f"{q}: residuos", 2, obs_maximas)', 'z = _vector(_requerido(d, "residuos", q), f"{q}: residuos", 2)'),
    ("M13", RI, "h10", "SIM-MC: historia sin cota", 'hist = _vector(v["historia_rendimientos"], f"{F}: historia_rendimientos", 2, obs_maximas)',
     'hist = _vector(v["historia_rendimientos"], f"{F}: historia_rendimientos", 2)'),
    ("M14", RI, "h10", "SCN-H: rendimientos sin cota", '        r = _rendimientos(ent, F, maximo=_observaciones_maximas(cfg))', '        r = _rendimientos(ent, F)'),
    ("M15", RI, "h10", "SCN-H: estados sin cota", '        _acotado(len(probs), u["estados_maximos"], f"{F}: estados del régimen")', '        pass'),
    ("M16", RI, "h10", "BT-DSR: sin cota", '    r = _rendimientos(ent, F, maximo=_observaciones_maximas(_configuracion(ent)))\n    T = len(r)', '    r = _rendimientos(ent, F)\n    T = len(r)'),
    ("M17", RI, "h10", "BT-PBO: configuraciones sin cota", '    _acotado(len(m), UMBRALES[F]["configuraciones_maximas"], f"{F}: configuraciones")', '    pass'),
    ("M18", RI, "h10", "BT-PBO: observaciones sin cota", 'cols = [_vector(m[k], f"{F}: rendimientos.{k}", 1, obs_maximas)', 'cols = [_vector(m[k], f"{F}: rendimientos.{k}", 1)'),
    ("M19", RI, "h10", "BT-VAR: var_previsto sin cota", 'var_p = _vector(v["var_previsto"], f"{F}: var_previsto", maximo=obs_maximas)', 'var_p = _vector(v["var_previsto"], f"{F}: var_previsto")'),
    ("M20", RI, "h10", "BT-VAR: resultados sin cota", 'res = _vector(_requerido(v, "resultados", F), f"{F}: resultados", maximo=obs_maximas)', 'res = _vector(_requerido(v, "resultados", F), f"{F}: resultados")'),
    ("M21", RI, "h10", "BT-VAR: es_previsto sin cota", '_vector(v["es_previsto"], f"{F}: es_previsto", maximo=obs_maximas)', '_vector(v["es_previsto"], f"{F}: es_previsto")'),
    ("M22", RI, "h10", "BT-VAR: historia del modo generado sin cota", '        hist = _rendimientos(ent, F, maximo=obs_maximas)', '        hist = _rendimientos(ent, F)'),
    ("M23", RI, "h10", "ML-CAL: pares sin cota", '_requerido(d, "realizaciones", q), q, obs_maximas)', '_requerido(d, "realizaciones", q), q)'),
    ("M24", RI, "h10", "ML-CAL: horizontes sin cota", '    _acotado(len(hz), u["horizontes_maximos"], f"{F}: horizontes")', '    pass'),
    ("M25", RI, "h10", "ML-CAL: referencia sin cota", 'ref = _vector(d["referencia"], f"{q}: referencia", maximo=obs_maximas)', 'ref = _vector(d["referencia"], f"{q}: referencia")'),
    ("M26", RI, "h10", "ML-CAL: intervalos sin cota", 'f"{q}: inferior", maximo=obs_maximas)', 'f"{q}: inferior")'),
    ("M27", RI, "h10", "ML-PRED: fechas sin cota", '_lista_acotada(_requerido(v, "fechas", F), f"{F}: fechas", obs_maximas)', '_lista(_requerido(v, "fechas", F), f"{F}: fechas")'),
    ("M28", RI, "h10", "ML-PRED: serie del objetivo sin cota", 'f"{F}: objetivo.serie", maximo=obs_maximas)', 'f"{F}: objetivo.serie")'),
    ("M29", RI, "h10", "ML-PRED: variables sin cota", '    _acotado(len(variables), u["variables_maximas"], f"{F}: variables")', '    pass'),
    ("M30", RI, "h10", "ML-PRED: serie de la variable sin cota", 'x = _vector(_requerido(d, "serie", q), f"{q}: serie", maximo=obs_maximas)', 'x = _vector(_requerido(d, "serie", q), f"{q}: serie")'),
    ("M31", RI, "h10", "ML-PRED: conocible_desde sin cota", '_lista_acotada(d["conocible_desde"], f"{q}: conocible_desde", obs_maximas)', '_lista(d["conocible_desde"], f"{q}: conocible_desde")'),
    ("M32", RI, "h10", "DEC-VOI: muestras sin cota", 'f"{F}: muestras.valores", 2, UMBRALES[F]["muestras_maximas"])', 'f"{F}: muestras.valores", 2)'),
    ("M33", RI, "h10", "serie de HT-01 sin cota", '            _acotado(len(s) - 1, maximo, f"{que}: rendimientos de la serie de precios")', '            pass'),
    ("M34", RI, "h10", "la cota del vector rechaza ya en el borde (> pasa a >=)", 'and np.size(x) > maximo:', 'and np.size(x) >= maximo:'),
    ("M35", RI, "h10", "_acotado deja pasar uno más", '    if n > maximo:\n        raise ErrorFicha(f"{que}: {n} (máximo {maximo}, cota de la ficha)")',
     '    if n > maximo + 1:\n        raise ErrorFicha(f"{que}: {n} (máximo {maximo}, cota de la ficha)")'),
    ("M36", RI, "h10", "la cota de observaciones no sigue a la configuración del Motor", '    return _horizonte_maximo(cfg)\n\n\ndef _acotado', '    return _horizonte_maximo(None)\n\n\ndef _acotado'),
    ("M37", RI, "h10", "BT-PBO admite 3 000 configuraciones", '"configuraciones_maximas": 1000})', '"configuraciones_maximas": 3000})'),
    ("M38", RI, "h10", "la cota del vector se comprueba después de leer los elementos (no antes)",
     '    if maximo is not None and isinstance(x, (list, tuple, pd.Series, np.ndarray)) and np.size(x) > maximo:\n        raise ErrorFicha(f"{que}: {np.size(x)} valores (máximo {maximo}, cota de la ficha)")\n    if isinstance(x, (pd.Series, np.ndarray)):\n        x = list(np.asarray(x).ravel())\n    v = np.array([_num(e, f"{que}[{i}]") for i, e in enumerate(_lista(x, que))], dtype=float)\n',
     '    if isinstance(x, (pd.Series, np.ndarray)):\n        x = list(np.asarray(x).ravel())\n    v = np.array([_num(e, f"{que}[{i}]") for i, e in enumerate(_lista(x, que))], dtype=float)\n    if maximo is not None and len(v) > maximo:\n        raise ErrorFicha(f"{que}: {len(v)} valores (máximo {maximo}, cota de la ficha)")\n'),
    # ---------------------------------------------------------------- H-11
    ("M40", SV, "h11", "el artefacto no guarda la configuración usada (campo vacío)", '"configuracion_usada": _configuracion_usada(self.cfg, lectura.leidas)},', '"configuracion_usada": {}},'),
    ("M41", SV, "h11", "CT-10 no aplica la configuración del artefacto", "                cfg_artefacto[k] = copy.deepcopy(reg[\"valor\"])", "                pass"),
    ("M42", SV, "h11", "CT-10 vuelve a culpar al original aunque la configuración no conste o haya cambiado", '        elif difs and (sin_registro or cambiadas):', '        elif False:'),
    ("M43", SV, "h11", "solo cuenta `cambiadas` (no `sin_registro`)", '        elif difs and (sin_registro or cambiadas):', '        elif difs and cambiadas:'),
    ("M44", SV, "h11", "solo cuenta `sin_registro` (no `cambiadas`)", '        elif difs and (sin_registro or cambiadas):', '        elif difs and sin_registro:'),
    ("M45", SV, "h11", "`get` no apunta la lectura", '    def get(self, clave: Any, defecto: Any = None) -> Any:\n        self.leidas.add(str(clave))\n', '    def get(self, clave: Any, defecto: Any = None) -> Any:\n'),
    ("M46", SV, "h11", "`__getitem__` no apunta la lectura", '    def __getitem__(self, clave: Any) -> Any:\n        self.leidas.add(str(clave))\n', '    def __getitem__(self, clave: Any) -> Any:\n'),
    ("M47", SV, "h11", "`__contains__` no apunta la lectura", '    def __contains__(self, clave: object) -> bool:\n        self.leidas.add(str(clave))\n', '    def __contains__(self, clave: object) -> bool:\n'),
    ("M48", SV, "h11", "una configuración vacía no se registra (sin __bool__)", '    def __bool__(self) -> bool:   # `parametro` hace `cfg or {}`: una configuración vacía también se registra\n        return True\n',
     '    def __bool__(self) -> bool:\n        return len(self) > 0\n'),
    ("M49", SV, "h11", "la huella de por_defecto.yaml es constante", 'out[k] = {"por_defecto": clave_hash(config_por_defecto().get(k))[:16]}', 'out[k] = {"por_defecto": "0" * 16}'),
    ("M50", SV, "h11", "una sección registrada sin valor no se quita de la vigente", "            else:\n                cfg_artefacto.pop(k, None)\n", "            else:\n                pass\n"),
    ("M51", SV, "h11", "la re-ejecución no dice de dónde sale la configuración", '"distinta_de_la_vigente": cambiadas, "sin_registro": sin_registro}},', '"distinta_de_la_vigente": [], "sin_registro": []}},'),
    ("M52", SV, "h11", "el valor guardado es la referencia viva de m.cfg (sin copia)", '            out[k]["valor"] = copy.deepcopy(dict.get(cfg, k))', '            out[k]["valor"] = dict.get(cfg, k)'),
    ("M53", SV, "h11", "la segunda pasada de CT-10 usa la configuración vigente", 'nuevo2, _ = IMPLEMENTADAS[ficha]["fn"](self._contexto(copy.deepcopy(ent), orig["as_of"], lectura),',
     'nuevo2, _ = IMPLEMENTADAS[ficha]["fn"](self._contexto(copy.deepcopy(ent), orig["as_of"]),'),
    # ---------------------------------------------------------------- H-12
    ("M60", SE, "h12", "S: la cota H5 se lee de por_defecto, no del Motor", '        return _entero(sesiones_horizonte(cfg, "H5"), "configuración: sesiones de H5", 1)', '        return _entero(sesiones_horizonte(None, "H5"), "configuración: sesiones de H5", 1)'),
    ("M61", SE, "h12", "S: FX-REGIME lee la ventana de por_defecto", '_entero(parametro(cfg, "senales.ventana_anios")', '_entero(parametro(None, "senales.ventana_anios")'),
    ("M62", SE, "h12", "S: `_parametros` no pone la cota del Motor", '    if "obs_maximas" in p:   # T-118 (H-12): la cota que sale de la configuración, con la del Motor\n        p["obs_maximas"] = _obs_maximas(F, cfg)\n', ''),
    ("M63", SE, "h12", "S: `_univariante` usa la cota de UMBRALES", '    maximo = _obs_maximas(F, ent.get("configuracion"))', '    maximo = UMBRALES[F]["obs_maximas"]'),
    ("M64", SE, "h12", "S: la envoltura no pasa la configuración a la ficha", '"fecha_corte": corte, "configuracion": cfg}', '"fecha_corte": corte, "configuracion": None}'),
    ("M65", RE, "h12", "P: el tope de CHR-FLOW usa la constante del módulo", 'tope = SEMANAS_H2_MAX * _entero(parametro(cfg, "calendario.sesiones_por_semana"),', 'tope = SEMANAS_H2_MAX * _entero(parametro(None, "calendario.sesiones_por_semana"),'),
    ("M66", RE, "h12", "P: f_chr_flow no pasa la configuración", 'p, u, v = _parametros(F, params, _configuracion(ent)), UMBRALES[F], ent["valores"]', 'p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]'),
    ("M67", SE, "h12", "S: 2 520 vuelve a estar escrito a mano", 'OBS_MAXIMAS_SERIES = sesiones_horizonte(None, "H5")', 'OBS_MAXIMAS_SERIES = 2520'),
    ("M68", SE, "h12", "S: ST-INF-001 deja de seguir a la configuración", 'FICHAS_OBS_H5 = frozenset({"ST-INF-001", "FX-BRK-001", "FX-STL-001", "FX-COINT-001"})', 'FICHAS_OBS_H5 = frozenset({"FX-BRK-001", "FX-STL-001", "FX-COINT-001"})'),
    # ---------------------------------------------------------------- H-13
    ("M70", SV, "h13", "sin la comprobación de anidamiento", '        if _demasiado_anidado(peticion):', '        if False:'),
    ("M71", SV, "h13", "la copia de los valores vuelve a escapar (sin RecursionError en el except)", '        except (TypeError, ValueError, OverflowError, RecursionError, MemoryError) as e:\n            # H-15', '        except (TypeError, ValueError, OverflowError) as e:\n            # H-15'),
    ("M72", SV, "h13", "las semillas se comparan con != directo", 'and _distintas(semilla_p, semilla_pet)', 'and semilla_p != semilla_pet'),
    ("M73", SV, "h13", "`clase` sin comprobación de tipo", '        if peticion.get("clase") is not None and not isinstance(peticion["clase"], str):\n            return "«clase» no es un texto"\n', ''),
    ("M74", SV, "h13", "`perfil` sin comprobación de tipo", '        if peticion.get("perfil") is not None and not isinstance(peticion["perfil"], (str, list, tuple)):\n            return "«perfil» no es un texto ni una lista"\n', ''),
    ("M75", SV, "h13", "el tope de anidamiento admite un nivel más", '        if nivel >= tope:\n            return True', '        if nivel > tope:\n            return True'),
    ("M76", SV, "h13", "las claves no se recorren", 'hijos = list(v.keys()) + list(v.values()) if isinstance(v, dict) else v', 'hijos = list(v.values()) if isinstance(v, dict) else v'),
    ("M77", SV, "h13", "el tope pasa a 1 000 niveles", 'PROFUNDIDAD_MAXIMA = 32', 'PROFUNDIDAD_MAXIMA = 1000'),
    ("M78", SV, "h13", "el tope baja a 8 niveles (rechazaría casos legítimos)", 'PROFUNDIDAD_MAXIMA = 32', 'PROFUNDIDAD_MAXIMA = 8'),
    ("M79", SV, "h13", "_distintas: lo que no se puede comparar se da por igual", '    except (TypeError, ValueError):\n        return True', '    except (TypeError, ValueError):\n        return False'),
    # ---------------------------------------------------------------- H-14
    ("M80", SV, "h14", "reejecutar no captura ErrorFicha", '        except (op.ErrorFicha, NotImplementedError, ValueError, TypeError, ArithmeticError, KeyError, IndexError,\n                AttributeError, np.linalg.LinAlgError, MemoryError, RecursionError) as exc:',
     '        except (NotImplementedError, ArithmeticError, IndexError, MemoryError, RecursionError) as exc:'),
    ("M81", SV, "h14", "la re-ejecución fallida no lleva su categoría", '            coincide, categoria = "NO", "ERROR_REEJECUCION"', '            coincide, categoria = "NO", None'),
    ("M82", SV, "h14", "la re-ejecución fallida figura como coincidente", '            coincide, categoria = "NO", "ERROR_REEJECUCION"', '            coincide, categoria = "SI", None'),
    ("M83", SV, "h14", "la re-ejecución fallida dice doble_pasada cierta", '"doble_pasada": not fallo and nuevo == nuevo2,', '"doble_pasada": nuevo == nuevo2,'),
]

solo = None
for a in sys.argv[2:]:
    if a.startswith("--solo"):
        solo = set(sys.argv[sys.argv.index(a) + 1].split(",")) if a == "--solo" else set(a.split("=")[1].split(","))
TODO = "--todo" in sys.argv
vivos, muertos, no_aplica = [], [], []
for mid, rel, k, desc, viejo, nuevo in M:
    if solo and mid not in solo:
        continue
    ruta = copia / rel
    original = ruta.read_text(encoding="utf-8")
    if original.count(viejo) != 1:
        no_aplica.append(mid)
        print(f"{mid} NO APLICA ({original.count(viejo)} apariciones) · {desc}", flush=True)
        continue
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    t0 = time.time()
    try:
        orden = [PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t118_hallazgos.py", "-k", k]
        r = subprocess.run(orden, cwd=copia, capture_output=True, text=True)
        donde = "t118"
        if r.returncode == 0 and TODO:
            r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t118_hallazgos.py", "tests/test_t112_motor.py",
                                "tests/test_fase2_riesgo.py", "tests/test_fase2_series.py", "tests/test_fase2_reales.py"], cwd=copia, capture_output=True, text=True)
            donde = "t118 entero + t112 + fase2 R, S y P"
    finally:
        ruta.write_text(original, encoding="utf-8")
    ult = (r.stdout.strip().splitlines() or [""])[-1][:90]
    falla = next((ln for ln in r.stdout.splitlines() if ln.startswith("FAILED") or ln.startswith("ERROR")), "")[:150]
    estado = "MUERTO" if r.returncode != 0 else "VIVO"
    (muertos if r.returncode != 0 else vivos).append(mid)
    print(f"{mid} {estado:6} {time.time() - t0:5.0f} s · {desc} · [{donde}] {ult} {falla}", flush=True)
print(f"== mutantes: {len(muertos)} muertos, {len(vivos)} vivos {vivos}, {len(no_aplica)} no aplican {no_aplica}")
