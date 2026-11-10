#!/usr/bin/env python3
"""T-65 · Mutaciones: quita cada corrección (sustitución de texto en el archivo), ejecuta su prueba y comprueba que FALLA;
después restaura el archivo (y comprueba su huella). Uso: python3 .docs/tickets/T-65/mutaciones.py [filtro de nombre].
Sale con 1 si alguna mutación no la detecta su prueba. Se ejecuta desde la raíz del repositorio."""
import hashlib
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
PKG = EJ / "bloque_a"
PY = str(RAIZ / ".venv" / "bin" / "python")
H, R = "tests/test_t65_hallazgos.py", "tests/test_t65_resto_t53.py"

# (nombre, archivo, texto actual, texto mutado, prueba)
MUTACIONES = [
    ("H-07 tabla de la instancia", PKG / "evaluador.py", 'self.bandas = tuple(validar_bandas(cfg.get("bandas_verbales")))',
     "self.bandas = _BANDAS", f"{H}::test_h07_dos_evaluadores_con_tablas_distintas_no_se_pisan"),
    ("H-07 la síntesis usa la del bloque", PKG / "sintesis.py", 'bloque.evaluador.banda_publicable(d["prob_interna"]), "prob"',
     'banda_publicable(d["prob_interna"]), "prob"', f"{H}::test_h07_la_sintesis_usa_la_tabla_de_su_bloque"),
    ("H-08 literal en el siguiente paso", PKG / "sintesis.py", 'paso = {k: parametro(cfg, f"seleccion.siguiente_paso.{k}") for k in ("E_enviar", "A_profundizar")}',
     'paso = {"E_enviar": 70, "A_profundizar": 65, **((cfg.get("seleccion") or {}).get("siguiente_paso") or {})}',
     f"{H}::test_h08_umbrales_de_presentacion_sin_respaldo_en_el_codigo"),
    ("H-08 parámetro nulo", PKG / "configuracion.py", "if v is _SIN_VALOR or v is None:   # una clave",
     "if v is _SIN_VALOR:   # una clave", f"{H}::test_h08_un_parametro_que_falta_en_todas_partes_falla_cerrado"),
    ("H-09 [PROPUESTO] de INC-T53-03", EJ / "config" / "por_defecto.yaml", "# [PROPUESTO] INC-T53-03 hasta T-57",
     "# INC-T53-03 hasta T-57", f"{H}::test_h09_incidencias_marcadas_propuesto_junto_a_su_clave"),
    ("H-10a estado_g3 en memoria", PKG / "redaccion.py", '            paquete.pop("estado_g3", None)\n            Path(rutas["paquete_json"])',
     '            Path(rutas["paquete_json"])', f"{H}::test_h10a_el_paquete_bloqueado_no_conserva_un_estado_g3_favorable"),
    ("H-10b carpeta del C6 bloqueado", PKG / "seguimiento.py", "base = carpeta_bloqueados(b, as_of, run_id)",
     'base = Path(b.carpeta_entregables) / "_bloqueados" / run_id',
     f"{H}::test_h10b_el_c6_bloqueado_en_backtest_va_a_la_misma_carpeta_que_la_redaccion"),
    ("H-10c motivo propio", PKG / "orquestacion.py", "            except DatosInvalidos as e:\n                invalidos.append((f[\"simbolo\"], str(e)))\n",
     "", f"{H}::test_h10c_datos_invalidos_con_motivo_propio_e_incidencia"),
    ("H-13 efecto as_of + 1", PKG / "evaluador.py", '"efecto_desde": str(as_of.date()),',
     '"efecto_desde": str((as_of + pd.Timedelta(days=1)).date()),', f"{H}::test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo"),
    ("H-14 rechazo sin declarar", PKG / "orquestacion.py", "                self._fichas_rechazadas[(clase, run_id)].append(ficha)\n",
     "", f"{H}::test_h14_una_ficha_rechazada_por_el_motor_se_declara"),
    ("H-15 cierres ≤ 0 en HT-01", PKG / "herramientas" / "ht01_datos.py", "malos = ~np.isfinite(s.to_numpy()) | (s.to_numpy() <= 0)",
     "malos = ~np.isfinite(s.to_numpy())", f"{H}::test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara"),
    ("H-15 fechas duplicadas", PKG / "herramientas" / "ht01_datos.py", "        raise DatosInvalidos(f\"HT-01 {origen}: fechas duplicadas",
     "        raise ValueError(f\"HT-01 {origen}: fechas duplicadas", f"{H}::test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara"),
    ("H-15 cualquier error del proveedor", PKG / "orquestacion.py",
     "            except Exception as e:  # noqa: BLE001 — error del proveedor para un símbolo: se excluye y se declara\n"
     "                invalidos.append((f[\"simbolo\"], f\"{type(e).__name__}: {e}\"))\n", "",
     f"{H}::test_h15_cualquier_error_del_proveedor_para_un_simbolo_se_declara"),
    ("H-15 CSV con fechas ilegibles", PKG / "herramientas" / "ht01_datos.py", "    except (ValueError, TypeError) as e:\n        raise DatosInvalidos(f\"HT-01 {origen}: fechas no interpretables",
     "    except KeyboardInterrupt as e:\n        raise DatosInvalidos(f\"HT-01 {origen}: fechas no interpretables",
     f"{H}::test_h15_csv_con_fechas_ilegibles_se_excluye_y_se_declara"),
    ("H-16 proxies cortos", PKG / "orquestacion.py", "(medibles if n_sem >= int(cl[\"min_semanas_proxy\"]) else cortos)",
     "(medibles if True else cortos)", f"{H}::test_h16_un_finalista_con_poca_historia_no_desactiva_los_clusteres"),
    ("H-17 sin validar", PKG / "orquestacion.py", '    if errores:\n        raise ValueError("ps2_festivos: "',
     '    if False:\n        raise ValueError("ps2_festivos: "', f"{H}::test_h17_ps2_festivos_mal_formado_impide_crear_el_bloque"),
    ("H-17 lunes de Pascua", PKG / "orquestacion.py", '    if festivos["lunes_de_pascua"]:', "    if False:",
     f"{H}::test_h17_lunes_de_pascua_configurable_y_propuesto_desactivado"),
    ("H-20 contenedor", PKG / "orquestacion.py",
     "        if objeciones is not None and not isinstance(objeciones, list):", "        if False:",
     f"{H}::test_h20_contenedor_mal_formado_cuenta_como_fuerte_abierta"),
    ("H-21 sanea el texto propio", PKG / "orquestacion.py", 'propio = str(pieza.get("origen") or "") in ORIGENES_SIN_SANEAR',
     "propio = False", f"{H}::test_h21_texto_propio_del_analista_llega_intacto"),
    ("H-21 una incidencia por fuente y run", PKG / "orquestacion.py", "if hall and (eid, run_id) not in self._r9_contrarreplica:",
     "if hall:", f"{H}::test_h21_lo_externo_se_sanea_con_run_id_y_una_incidencia_por_fuente"),
    ("H-21 run_id", PKG / "orquestacion.py", "                self._registrar_r9(hall, run_id)\n            return t",
     "                self._registrar_r9(hall, None)\n            return t", f"{H}::test_h21_lo_externo_se_sanea_con_run_id_y_una_incidencia_por_fuente"),
    ("CA-14 sesiones por mes", PKG / "configuracion.py", 'int(h["meses"]) * int(parametro(cfg, "calendario.sesiones_por_mes"))',
     'int(h["meses"]) * 21', f"{R}::test_ca14_sesiones_por_horizonte_salen_de_la_configuracion"),
    ("CA-14 tasa base sin historia", PKG / "evaluador.py", 'p = float(tb["sin_historia"])', "p = 0.5",
     f"{R}::test_ca14_tasa_base_con_parametros_de_la_configuracion"),
    ("CA-14 zona de interés", PKG / "sintesis.py", 'round(precio * (1 - pres["zona_interes"]), 6)', "round(precio * 0.95, 6)",
     f"{R}::test_ca14_zona_de_interes_y_confianza_de_la_configuracion"),
    ("CA-14 C6 sin σ", PKG / "seguimiento.py", '"material": True, "umbral_material": None}', '"material": abs(delta) > 0.05, "umbral_material": 0.05}',
     f"{R}::test_ca14_c6_sin_sigma_trata_el_delta_como_material"),
    ("CA-15 ámbito de los mensajes", PKG / "contratos.py", 'self.almacen.nuevo_id(f"MSG-{amb}" if amb else "MSG", ancho=6)',
     'self.almacen.nuevo_id("MSG", ancho=6)', f"{R}::test_ca15_msg_id_del_paralelo_no_dependen_del_orden_de_los_hilos"),
    ("CA-15 participantes ordenados", PKG / "orquestacion.py", 'for a, d in sorted(cons["por_agente"].items())]',
     'for a, d in cons["por_agente"].items()]', f"{R}::test_ca15_participantes_de_f5_en_orden_de_agente"),
    ("CS-08 fichas documentadas", PKG / "motor" / "servicio.py", 'DOCUMENTADAS_CON_CODIGO = frozenset({"ACC-ERP-001", "FX-MOM-001", "REI-CAP-001"})',
     "DOCUMENTADAS_CON_CODIGO: frozenset = frozenset()", f"{R}::test_cs08_fichas_documentadas_no_entregan_cifras"),
    ("CS-08 alternativa no servible", PKG / "motor" / "servicio.py", "alt = alt if alt and servible(alt) else None", "alt = alt",
     f"{R}::test_cs08_no_se_ofrece_como_alternativa_una_ficha_que_no_se_sirve"),
    ("CS-10 réplicas de la resolución", PKG / "evaluador.py",
     '"parametros": {"replicas": int(parametro(self.cfg, "evaluacion.bootstrap_replicas")),',
     '"parametros": {"replicas": 200,', f"{R}::test_cs10_la_resolucion_usa_las_replicas_de_la_configuracion"),
    ("CS-10 celdas de rotación", PKG / "orquestacion.py", '[:int(parametro(self.cfg, "seleccion.rotacion_exploratoria_celdas"))]', "[:2]",
     f"{R}::test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion"),
    ("CS-10 clave que falta en el YAML", EJ / "config" / "por_defecto.yaml", "ps1: {raices_min: 2}", "ps1: {}",
     f"{R}::test_cs10_todas_las_claves_leidas_existen_en_por_defecto"),
    ("CS-11 sección parametros_ht03", PKG / "orquestacion.py", "ht03.fusionar_parametros(parametros_ht03(cfg))",
     'ht03.fusionar_parametros(cfg.get("_parametros_ht03"))', f"{R}::test_cs11_parametros_ht03_se_leen_de_la_seccion_del_yaml"),
    ("CS-11 YAML distinto del corpus", EJ / "config" / "por_defecto.yaml", "  umbrales: {E: 60, A: 55,", "  umbrales: {E: 61, A: 55,",
     f"{R}::test_cs11_parametros_ht03_del_yaml_iguales_al_corpus"),
    ("CS-11 regímenes", PKG / "almacen.py", '"P-29", "P-34", "P-38", "P-44"}', '"P-29"}',
     f"{R}::test_cs11_regimenes_de_f10_completos_segun_el_esquema"),
    ("CS-11 P-30 con «4.0»", PKG / "orquestacion.py", 'parametro(a, "methodology_version")', 'a.get("methodology_version", "4.0")',
     f"{R}::test_cs11_p30_sin_respaldo_4_0"),
    ("CS-18 ventana fija", PKG / "orquestacion.py", "ini = (pd.Timestamp(as_of) - pd.Timedelta(weeks=ventana + 2)).normalize()",
     "ini = (pd.Timestamp(as_of) - pd.DateOffset(years=2, days=14)).normalize()",
     f"{R}::test_cs18_la_ventana_de_clusteres_sale_de_la_configuracion"),
    ("CS-19 mapa antiguo", EJ / "tests" / "MAPA_PLAN_DE_PRUEBAS.md", "| PB-56 Oportunidad duplicada entre tipos |", "| Duplicada entre tipos |",
     f"{R}::test_cs19_mapa_cubre_las_67_pruebas_del_plan"),
    ("CS-23 cita antigua", PKG / "herramientas" / "__init__.py",
     "la prueba `test_unitarias.py::test_herramientas_de_referencia_sin_divergencia`", "la prueba `test_herramientas.py`",
     f"{R}::test_cs23_herramientas_cita_una_prueba_que_existe"),
]


def huella(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    no_detectadas = []
    for nombre, archivo, actual, mutado, prueba in MUTACIONES:
        if filtro and filtro not in nombre:
            continue
        original = archivo.read_text(encoding="utf-8")
        h0 = huella(archivo)
        if original.count(actual) != 1:
            print(f"ERROR  {nombre}: el texto a mutar aparece {original.count(actual)} veces en {archivo.name}")
            no_detectadas.append(nombre)
            continue
        try:
            archivo.write_text(original.replace(actual, mutado), encoding="utf-8")
            r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", prueba], cwd=EJ, capture_output=True,
                               text=True, timeout=900)
        finally:
            archivo.write_text(original, encoding="utf-8")
        assert huella(archivo) == h0, f"no se restauró {archivo}"
        detectada = r.returncode != 0
        print(f"{'FALLA ' if detectada else 'PASA! '} {nombre} → {prueba.split('::')[1]}")
        if not detectada:
            no_detectadas.append(nombre)
    print(f"{'Todas las mutaciones detectadas' if not no_detectadas else 'NO detectadas: ' + ', '.join(no_detectadas)}")
    return 1 if no_detectadas else 0


if __name__ == "__main__":
    sys.exit(main())
