"""QA r01 de T-83 (V0.72): mutaciones de una copia del código contra la batería `pruebas/pruebas_parametros_doc_t83.py`.

Copia `validador/` y `esquemas/` a una carpeta temporal, aplica una mutación cada vez y ejecuta la batería real con
T83_VALIDADOR apuntando a la copia (la batería lee la Constitución y la deuda del repositorio). Para cada mutación se dice si
debería matarla (MUERE) o si se espera que sobreviva porque está fuera de lo que la batería promete (VIVE), y se compara.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.72/qa/r01_mutaciones_bateria.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCO = AQUI.parents[2]
BATERIA = MARCO / "pruebas" / "pruebas_parametros_doc_t83.py"

# (nombre, fichero de validador/, texto antes, texto después, esperado: "MUERE" o "VIVE", motivo)
MUTACIONES = [
    # --- estado
    ("estado_apalancamiento_a_ratificado", "parametros_doc.py",
     '"apalancamiento_max": _r(P,', '"apalancamiento_max": _r(R,', "MUERE", "conjunto de RATIFICADO fijado"),
    ("estado_autoria_c_a_tecnico_sin_pregunta", "parametros_doc.py",
     '"autoria_c": _r(P, ["Deuda D-25", "Deuda T-48"],\n            "Sin declarar qué modelo y qué proveedor hacen cada análisis no se puede comprobar que el revisor sea distinto; queda "\n            "vacío y cada informe lo avisa.",\n            "¿Qué modelo y qué proveedor de inteligencia artificial hacen los análisis de cada tipo de activo?"),',
     '"autoria_c": _r(TEC, ["Deuda D-25", "Deuda T-48"],\n            "Sin declarar qué modelo y qué proveedor hacen cada análisis no se puede comprobar que el revisor sea distinto; queda "\n            "vacío y cada informe lo avisa."),',
     "MUERE", "lista de TECNICO fijada (autoria_c es {} y no tiene números)"),
    ("estado_ratificado_a_propuesto_en_doc", "parametros_doc.py",
     '"o_dias_sequia": _r(R,', '"o_dias_sequia": _r(P,', "MUERE", "marca [RATIFICADO] del comentario"),
    ("estado_desconocido", "parametros_doc.py", '"max_posiciones": _r(P,', '"max_posiciones": _r("PENDIENTE",', "MUERE", "estado válido"),
    # --- fuente
    ("fuente_inexistente_deuda", "parametros_doc.py", '"valor_min_eur": _r(P, ["Deuda D-01"]', '"valor_min_eur": _r(P, ["Deuda T-99"]',
     "MUERE", "fuente que no existe"),
    ("fuente_inexistente_constitucion", "parametros_doc.py", '"umbral_l2_eur": _r(P, ["Deuda D-33", "Constitución P-01"',
     '"umbral_l2_eur": _r(P, ["Deuda D-33", "Constitución P-77"', "MUERE", "fuente que no existe"),
    ("fuente_mal_formada", "parametros_doc.py", '"valor_min_eur": _r(P, ["Deuda D-01"]', '"valor_min_eur": _r(P, ["D-01"]',
     "MUERE", "fuente sin documento delante"),
    ("fuente_vacia", "parametros_doc.py", '"valor_min_eur": _r(P, ["Deuda D-01"]', '"valor_min_eur": _r(P, []', "MUERE", "fuente vacía"),
    ("fuente_existente_pero_equivocada", "parametros_doc.py", '"valor_min_eur": _r(P, ["Deuda D-01"]',
     '"valor_min_eur": _r(P, ["Constitución D-02"]', "VIVE", "contenido: solo lo ve una persona (límite declarado)"),
    ("ratificado_cita_solo_pendiente", "parametros_doc.py",
     '"n_dias_embudo": _r(R, ["Constitución D-22", "Deuda T-75"]', '"n_dias_embudo": _r(R, ["Constitución P-17", "Deuda T-75"]',
     "MUERE", "RATIFICADO sin decisión D- ratificada"),
    # --- pregunta y justificación
    ("pregunta_con_nombre_de_codigo", "parametros_doc.py", '"¿Cuántas inversiones abiertas a la vez quieres como máximo?"',
     '"¿Cuántas max_posiciones quieres como máximo?"', "MUERE", "pregunta con nombre de código"),
    ("pregunta_sin_interrogacion", "parametros_doc.py", '"¿Cuántas inversiones abiertas a la vez quieres como máximo?"',
     '"Cuántas inversiones abiertas a la vez quieres como máximo."', "MUERE", "forma de la pregunta"),
    ("pregunta_duplicada", "parametros_doc.py", '"¿Cuántas inversiones abiertas a la vez quieres como máximo?"',
     '"¿Cuántas órdenes por hora quieres permitir como máximo?"', "MUERE", "preguntas distintas"),
    ("tecnico_con_pregunta", "parametros_doc.py",
     '"Identifica la versión de esta configuración en la huella de cada decisión; la cambia el código, no el operador."),',
     '"Identifica la versión de esta configuración en la huella de cada decisión; la cambia el código, no el operador.",\n            "¿Qué versión quieres?"),',
     "MUERE", "TECNICO sin pregunta"),
    ("justificacion_tres_frases", "parametros_doc.py", '"Ninguna posición pasa del 10 % del capital: es la diversificación mínima."',
     '"Ninguna posición pasa del 10 % del capital. Es la diversificación mínima. Y es prudente."', "MUERE", "una o dos frases"),
    # --- marcas de los comentarios del código
    ("marca_config_referencias", "orquestador.py", "# benchmark de cada cartera [PROPUESTO]", "# benchmark de cada cartera [RATIFICADO]",
     "MUERE", "marca en CONFIG_DEFECTO"),
    ("marca_config_nivel_autonomia", "orquestador.py", "; sin dato = L1", "; sin dato = L1 [PROPUESTO]", "MUERE",
     "marca contra un RATIFICADO"),
    ("marca_politica_f_linea_anterior", "control_f.py", "[PROPUESTO, D-11 y D-31]", "[RATIFICADO, D-11 y D-31]", "MUERE",
     "marca de línea anterior en POLITICA_DEFECTO"),
    ("marca_lectura_vigilancia", "vigilancia.py", 'MAX_EDAD_MIN = _P["h_max_edad_dato_min"]   # [PROPUESTO]',
     'MAX_EDAD_MIN = _P["h_max_edad_dato_min"]   # [RATIFICADO]', "MUERE", "marca en una lectura de PARAMETROS"),
    ("marca_lectura_comparador", "comparador.py", "# [PROPUESTO] topes de confianza por clase", "# [RATIFICADO] topes de confianza por clase",
     "MUERE", "marca en una lectura de PARAMETROS"),
    ("marca_ratificado_quitada", "parametros.py", "# [RATIFICADO: 24 meses] (D-27, P-18)", "# (D-27, P-18)", "MUERE",
     "no vacuidad: menos de 3 RATIFICADO vistos"),
    ("docstring_de_F_sin_propuesto", "control_f.py", "Todos los límites son valores de partida [PROPUESTO].",
     "Todos los límites son valores de partida.", "MUERE", "los módulos declaran sus valores de partida"),
    # --- cobertura
    ("clave_renombrada_en_config", "orquestador.py", '"max_reaperturas": 2,', '"max_reaperturas_x": 2,', "MUERE", "cobertura en los dos sentidos"),
    ("clave_quitada_de_politica", "control_f.py", ' "valor_min_eur": 100.0,', "", "MUERE", "documentada que no existe"),
    # --- lo que la batería no promete (se espera que viva; se mide para el informe)
    ("subclave_nueva_en_aprobacion", "orquestador.py", '"aprobacion": {"caduca_min": 15,', '"aprobacion": {"caduca_min": 15, "x_t83_tope_eur": 5,',
     "VIVE", "las subclaves no se cubren (límite declarado solo en analisis-tecnico)"),
    ("subclave_nueva_en_promocion", "orquestador.py", '"promocion_nivel": {"periodo_min_dias": 30}',
     '"promocion_nivel": {"periodo_min_dias": 30, "incidentes_max": 0}', "VIVE", "las subclaves no se cubren"),
    ("valor_cambiado_justificacion_rancia", "parametros.py", '"k_min_observaciones": 20,', '"k_min_observaciones": 40,', "VIVE",
     "la justificación dice 20 y nadie lo compara"),
    ("valor_cambiado_politica_justificacion_rancia", "control_f.py", '"max_posiciones": 10,', '"max_posiciones": 25,', "VIVE",
     "la justificación dice «diez» y nadie lo compara"),
]


def correr(carpeta):
    r = subprocess.run([sys.executable, "-I", str(BATERIA)], cwd=BATERIA.parent, capture_output=True, text=True, timeout=300,
                       env={**os.environ, "T83_VALIDADOR": str(carpeta)}, check=False)
    fallan = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FALLA") and len(l.split()) > 1]
    return r.returncode, fallan, r.stdout + r.stderr


def main():
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    malos = 0
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "limpia"
        shutil.copytree(MARCO / "validador", base / "validador", ignore=ign)
        shutil.copytree(MARCO / "esquemas", base / "esquemas", ignore=ign)
        rc, fallan, sal = correr(base / "validador")
        ok = rc == 0 and not fallan
        print(("OK   " if ok else "MAL  "), "copia_sin_cambios_pasa", "" if ok else (rc, fallan, sal[-400:]))
        malos += not ok
        for nombre, fichero, antes, despues, esperado, motivo in MUTACIONES:
            d = Path(td) / nombre
            shutil.copytree(base, d, ignore=ign)
            ruta = d / "validador" / fichero
            t = ruta.read_text(encoding="utf-8")
            if t.count(antes) != 1:
                print("MAL  ", nombre, f"no encuentro una vez el texto en {fichero}")
                malos += 1
                continue
            ruta.write_text(t.replace(antes, despues), encoding="utf-8")
            rc, fallan, sal = correr(d / "validador")
            obtenido = "MUERE" if rc != 0 else "VIVE"
            ok = obtenido == esperado
            malos += not ok
            print(("OK   " if ok else "MAL  "), f"{nombre}: {obtenido} (esperado {esperado}; {motivo})", fallan[:3] if fallan else "")
    print("\nRESULTADO r01 MUTACIONES T-83:", "COMO SE ESPERABA" if not malos else f"{malos} DISTINTAS DE LO ESPERADO")
    return 0 if not malos else 1


if __name__ == "__main__":
    sys.exit(main())
