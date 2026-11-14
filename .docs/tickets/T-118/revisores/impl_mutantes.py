"""T-118 · Mutantes del implementador: deshace cada corrección (H-09 a H-14) en una copia desechable del ejecutor y
comprueba que alguna prueba de `tests/test_t118_hallazgos.py` la detecta. No toca el árbol: copia `bloque_a/11_Ejecutor` y
el Catálogo a la carpeta que se le pasa, y la borra al acabar.
Uso: .venv/bin/python .docs/tickets/T-118/revisores/impl_mutantes.py <raíz del repo> <carpeta desechable> [prefijos…]
     (p. ej. «M11» para ejecutar solo los de H-11)"""
import shutil, subprocess, sys, time
from pathlib import Path
W, MUT = Path(sys.argv[1]), Path(sys.argv[2])
PY = sys.executable
R, S, P, X = ("bloque_a/motor/fichas_riesgo.py", "bloque_a/motor/fichas_series.py", "bloque_a/motor/fichas_reales.py",
              "bloque_a/motor/servicio.py")
M = [
 ("M09a H-09 ML-PRED sin el corte en fechas", R, '    _hasta_corte(fechas, corte, f"{F}: fechas")\n', ''),
 ("M09b H-09 ML-PRED sin el corte en conocible_desde", R, '        _hasta_corte(cd, corte, f"{q}: conocible_desde")\n', ''),
 ("M09c H-09 ML-CAL sin el corte", R, '            _hasta_corte([pd.Timestamp(fechas[-1])], corte, f"{q}: predicciones y realizaciones")\n', '            pass\n'),
 ("M09d H-09 el día del corte se rechaza", R, 'if ultima.normalize() > corte.normalize():', 'if ultima.normalize() >= corte.normalize():'),
 ("M09e H-09 _corte no lee la fecha", R, '    fc = ent.get("fecha_corte")\n    if fc is None:\n        return None\n    try:', '    fc = None\n    if fc is None:\n        return None\n    try:'),
 ("M10a H-10 _vector sin cota", R, 'if maximo is not None and isinstance(x, (list, tuple, pd.Series, np.ndarray)) and np.size(x) > maximo:', 'if False:'),
 ("M10b H-10 _acotado no rechaza", R, '    if n > maximo:\n        raise ErrorFicha(f"{que}: {n} (máximo {maximo}, cota de la ficha)")', '    return'),
 ("M10c H-10 cota de observaciones fija (no la configuración)", R, '    return _horizonte_maximo(cfg)\n\n\ndef _acotado', '    return _horizonte_maximo(None)\n\n\ndef _acotado'),
 ("M10d H-10 RISK-VAR distribución sin cota", R, '                    maximo=UMBRALES[F]["distribucion_maxima"])', '                    maximo=None)'),
 ("M10e H-10 RISK-VAR historia sin cota", R, 'return _rendimientos(ent, F, maximo=_observaciones_maximas(_configuracion(ent))), "historia"', 'return _rendimientos(ent, F), "historia"'),
 ("M10f H-10 serie de HT-01 sin cota", R, '            _acotado(len(s) - 1, maximo, f"{que}: rendimientos de la serie de precios")', '            pass'),
 ("M10g H-10 SIM-MC residuos sin cota", R, 'f"{q}: residuos", 2, obs_maximas)', 'f"{q}: residuos", 2)'),
 ("M10h H-10 SIM-MC historia sin cota", R, 'f"{F}: historia_rendimientos", 2, obs_maximas)', 'f"{F}: historia_rendimientos", 2)'),
 ("M10i H-10 SCN-H rendimientos sin cota", R, '        r = _rendimientos(ent, F, maximo=_observaciones_maximas(cfg))', '        r = _rendimientos(ent, F)'),
 ("M10j H-10 SCN-H estados sin cota", R, '        _acotado(len(probs), u["estados_maximos"], f"{F}: estados del régimen")   # T-118 (H-10)\n', ''),
 ("M10k H-10 BT-DSR sin cota", R, '    r = _rendimientos(ent, F, maximo=_observaciones_maximas(_configuracion(ent)))\n    T = len(r)', '    r = _rendimientos(ent, F)\n    T = len(r)'),
 ("M10l H-10 BT-PBO configuraciones sin cota", R, '    _acotado(len(m), UMBRALES[F]["configuraciones_maximas"], f"{F}: configuraciones")   # T-118 (H-10)\n', ''),
 ("M10m H-10 BT-PBO observaciones sin cota", R, 'f"{F}: rendimientos.{k}", 1, obs_maximas)', 'f"{F}: rendimientos.{k}", 1)'),
 ("M10n H-10 BT-VAR previsto sin cota", R, 'var_p = _vector(v["var_previsto"], f"{F}: var_previsto", maximo=obs_maximas)\n        res = _vector(_requerido(v, "resultados", F), f"{F}: resultados", maximo=obs_maximas)',
  'var_p = _vector(v["var_previsto"], f"{F}: var_previsto")\n        res = _vector(_requerido(v, "resultados", F), f"{F}: resultados")'),
 ("M10o H-10 BT-VAR historia generada sin cota", R, '        hist = _rendimientos(ent, F, maximo=obs_maximas)', '        hist = _rendimientos(ent, F)'),
 ("M10p H-10 ML-CAL pares sin cota", R, '    if maximo is not None:\n        _acotado(len(pl), maximo, f"{que}: predicciones")\n        _acotado(len(rl), maximo, f"{que}: realizaciones")\n', ''),
 ("M10q H-10 ML-CAL horizontes sin cota", R, '    _acotado(len(hz), u["horizontes_maximos"], f"{F}: horizontes")\n', ''),
 ("M10r H-10 ML-PRED observaciones sin cota", R, 'obs_maximas, corte = _observaciones_maximas(_configuracion(ent)), _corte(ent)   # T-118 (H-10 y H-09)\n    fechas', 'obs_maximas, corte = 10 ** 12, _corte(ent)\n    fechas'),
 ("M10s H-10 ML-PRED variables sin cota", R, '    _acotado(len(variables), u["variables_maximas"], f"{F}: variables")\n', ''),
 ("M10t H-10 DEC-VOI muestras sin cota", R, 'f"{F}: muestras.valores", 2, UMBRALES[F]["muestras_maximas"])', 'f"{F}: muestras.valores", 2)'),
 ("M11a H-11 el artefacto no guarda la configuración", X, '"configuracion_usada": _configuracion_usada(self.cfg, lectura.leidas)},', '"configuracion_usada": {}},'),
 ("M11b H-11 la re-ejecución no usa la configuración del artefacto", X, '            if isinstance(reg, dict) and "valor" in reg:\n                cfg_artefacto[k] = copy.deepcopy(reg["valor"])\n            else:\n                cfg_artefacto.pop(k, None)', '            pass'),
 ("M11c H-11 sin la rama CONVENCION_DISTINTA por configuración", X, '        elif difs and (sin_registro or cambiadas):', '        elif False:'),
 ("M11d H-11 solo mira las cambiadas (no lo no registrado)", X, '        elif difs and (sin_registro or cambiadas):', '        elif difs and cambiadas:'),
 ("M11e H-11 solo mira lo no registrado (no las cambiadas)", X, '        elif difs and (sin_registro or cambiadas):', '        elif difs and sin_registro:'),
 ("M11f H-11 el registro no apunta las lecturas con get", X, '    def get(self, clave: Any, defecto: Any = None) -> Any:\n        self.leidas.add(str(clave))\n', '    def get(self, clave: Any, defecto: Any = None) -> Any:\n'),
 ("M11g H-11 el registro no apunta las lecturas con []", X, '    def __getitem__(self, clave: Any) -> Any:\n        self.leidas.add(str(clave))\n', '    def __getitem__(self, clave: Any) -> Any:\n'),
 ("M11h H-11 la ficha recibe la configuración sin registro", X, '        ent["configuracion"] = self.cfg if cfg is None else cfg', '        ent["configuracion"] = self.cfg'),
 ("M11i H-11 las cambiadas no se anotan", X, 'cambiadas = sorted(k for k, reg in (registrada or {}).items() if clave_hash(reg) != clave_hash(vigente[k]))', 'cambiadas = []'),
 ("M11j H-11 una configuración vacía no se registra", X, '    def __bool__(self) -> bool:   # `parametro` hace `cfg or {}`: una configuración vacía también se registra\n        return True\n\n', ''),
 ("M12a H-12 S: cota H5 fija", S, '        return _entero(sesiones_horizonte(cfg, "H5"), "configuración: sesiones de H5", 1)', '        return OBS_MAXIMAS_SERIES'),
 ("M12b H-12 S: cota de FX-REGIME fija", S, '        return _entero(parametro(cfg, "senales.ventana_anios"), "configuración: senales.ventana_anios", 1) * SESIONES_POR_ANIO', '        return OBS_MAXIMAS_REGIME'),
 ("M12c H-12 S: _univariante con la cota de UMBRALES", S, '    maximo = _obs_maximas(F, ent.get("configuracion"))', '    maximo = UMBRALES[F]["obs_maximas"]'),
 ("M12d H-12 S: _parametros sin la cota de la configuración", S, '        p["obs_maximas"] = _obs_maximas(F, cfg)', '        pass'),
 ("M12e H-12 S: la envoltura no pasa la configuración", S, '            cfg = _configuracion(ent)   # T-118 (H-12)', '            cfg = None'),
 ("M12f H-12 P: sesiones por semana fijas", P, '        tope = SEMANAS_H2_MAX * _entero(parametro(cfg, "calendario.sesiones_por_semana"),', '        tope = SEMANAS_H2_MAX * _entero(SESIONES_SEMANA,'),
 ("M12g H-12 P: CHR-FLOW no pasa la configuración", P, '    p, u, v = _parametros(F, params, _configuracion(ent)), UMBRALES[F], ent["valores"]', '    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]'),
 ("M13a H-13 sin la comprobación de profundidad", X, '        if _demasiado_anidado(peticion):   # T-118 (H-13): antes de copiar, serializar o escribir nada de ella\n            return f"anidamiento excesivo (más de {PROFUNDIDAD_MAXIMA} niveles)"\n', ''),
 ("M13b H-13 semillas comparadas con !=", X, '_distintas(semilla_p, semilla_pet)', '(semilla_p != semilla_pet)'),
 ("M13c H-13 sin el tipo de clase", X, '        if peticion.get("clase") is not None and not isinstance(peticion["clase"], str):\n            return "«clase» no es un texto"\n', ''),
 ("M13d H-13 sin el tipo de perfil", X, '        if peticion.get("perfil") is not None and not isinstance(peticion["perfil"], (str, list, tuple)):\n            return "«perfil» no es un texto ni una lista"\n', ''),
 ("M13e H-13 la copia de los valores vuelve a escapar", X, '        except (TypeError, ValueError, OverflowError, RecursionError, MemoryError) as e:', '        except (TypeError, ValueError, OverflowError) as e:'),
 ("M13f H-13 cota de profundidad un nivel más laxa", X, '        if nivel >= tope:\n            return True', '        if nivel > tope:\n            return True'),
 ("M13g H-13 las claves no cuentan", X, 'hijos = list(v.keys()) + list(v.values()) if isinstance(v, dict) else v', 'hijos = list(v.values()) if isinstance(v, dict) else v'),
 ("M14a H-14 ErrorFicha vuelve a escapar de reejecutar", X, '        except (op.ErrorFicha, NotImplementedError, ValueError, TypeError, ArithmeticError, KeyError, IndexError,\n                AttributeError,', '        except (NotImplementedError, ArithmeticError, IndexError,\n                AttributeError,'),
 ("M14b H-14 categoría que no lo dice", X, 'coincide, categoria = "NO", "ERROR_REEJECUCION"', 'coincide, categoria = "NO", "ERROR_ORIGINAL"'),
]
solo = sys.argv[3:]
vivos = []
for nombre, fich, a, b in M:
    if solo and not any(nombre.startswith(x) for x in solo):
        continue
    if MUT.exists():
        shutil.rmtree(MUT)
    (MUT / "bloque_a").mkdir(parents=True)
    shutil.copytree(W / "bloque_a/11_Ejecutor", MUT / "bloque_a/11_Ejecutor", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.docx", ".mypy_cache", ".ruff_cache"))
    shutil.copytree(W / "bloque_a/04_Motor_conocimiento_y_catalogo", MUT / "bloque_a/04_Motor_conocimiento_y_catalogo", ignore=shutil.ignore_patterns("*.docx"))
    f = MUT / "bloque_a/11_Ejecutor" / fich
    s = f.read_text(encoding="utf-8")
    if s.count(a) != 1:
        print(f"NO APLICA ({s.count(a)} veces)  {nombre}", flush=True); vivos.append(nombre); continue
    f.write_text(s.replace(a, b), encoding="utf-8")
    t0 = time.time()
    # primero, las pruebas de su hallazgo (M09… → test_h09_…); si sobrevive, el fichero entero
    orden = [PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t118_hallazgos.py"]
    r = subprocess.run([*orden, "-k", f"h{nombre[1:3]}"], cwd=MUT / "bloque_a/11_Ejecutor", capture_output=True, text=True)
    if r.returncode == 0:
        r = subprocess.run(orden, cwd=MUT / "bloque_a/11_Ejecutor", capture_output=True, text=True)
    falla = [x for x in r.stdout.splitlines() if x.startswith("FAILED") or x.startswith("ERROR")]
    estado = "MUERTO" if r.returncode != 0 else "VIVO  "
    if r.returncode == 0:
        vivos.append(nombre)
    print(f"{estado} {nombre}  [{time.time()-t0:.0f} s] {falla[0][:110] if falla else ''}", flush=True)
shutil.rmtree(MUT, ignore_errors=True)
print(f"== {len(M) if not solo else 'selección'}: vivos {len(vivos)}: {vivos}")
