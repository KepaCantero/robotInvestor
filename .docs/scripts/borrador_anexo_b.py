"""Genera el borrador de la corrección del Anexo B del Documento 0 del Bloque A (punto 8 de las tareas del 15-11-2026).

El operador decidió el 13-11-2026 que, si el Documento 0 y el código difieren, manda el código (INC-T114-01): el Anexo B
se corrige en la próxima entrega para que describa lo que hace el ejecutor. Este script lee las diferencias congeladas en
`bloque_a/11_Ejecutor/tests/goldens/divergencias_anexo_b.json` y escribe, contrato a contrato, qué dice hoy el Anexo B,
qué hace el ejecutor y el cambio que se propone. No toca el corpus: el Documento 0 es una entrega congelada.

T-143 (15-11-2026): el borrador se aplicó en el Documento 0 V5.2. Desde entonces el fichero dice primero lo que queda contra
la V5.2 (de las diferencias congeladas de hoy) y conserva, debajo, el borrador aplicado, generado con la copia de las
diferencias contra la V5.1 (`.docs/diseno/bloque_a/divergencias_anexo_b_v51.json`): de `.docs/` no se borra nada.

Uso (desde la raíz): .venv/bin/python .docs/scripts/borrador_anexo_b.py [--comprobar]
Con --comprobar no escribe: termina con 1 si el borrador no coincide con lo que generaría (las diferencias cambiaron).
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DIVERGENCIAS = RAIZ / "bloque_a" / "11_Ejecutor" / "tests" / "goldens" / "divergencias_anexo_b.json"
SALIDA = RAIZ / ".docs" / "diseno" / "bloque_a" / "borrador_correccion_anexo_b.md"
# T-143: las diferencias contra el Anexo B V5.1, tal como estaban congeladas antes de la V5.2 (copia del golden)
DIVERGENCIAS_V51 = RAIZ / ".docs" / "diseno" / "bloque_a" / "divergencias_anexo_b_v51.json"
DOC0_V52 = "bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md"

# T-143: lo que queda contra la V5.2 y no sale del golden (no es una diferencia medida o está fuera del Documento 0)
QUEDA = [
    ("Ejemplo publicado del informe de seguimiento (INC-T114-02)", ("Sigue sin cumplir su propio esquema por la clave "
     "`x_aviso_ejemplo`. Está en `06_Plantillas_entregables`, no en el Documento 0, y la V5.2 no lo toca.")),
    ("Campo del tipo en CT-22", ("La V5.2 documenta los dos campos como están (`tipo` y `tipo_aviso`, uno de los dos por "
     "aviso). Unificarlos en el código sigue siendo posible, pero sería un cambio de formato con re-congelado de los goldens.")),
    ("Listas cerradas", ("La V5.2 dice que la mensajería solo comprueba las de CT-01, CT-02 y los estados; las demás no. "
     "Validarlas en el código sería un cambio de formato.")),
    ("Lo que el golden no mide", ("Los retornos internos (CT-05 a CT-08, CT-11 a CT-15 y CT-17) no tienen más esquema derivado "
     "que sus campos de primer nivel: lo que el Anexo B V5.2 dice de ellos (campos de primer nivel, anidados, también los de la "
     "ficha `FINALISTA`, y valores de sus listas cerradas) lo comparan con `ESQUEMAS` las pruebas `test_t143_*` de "
     "`tests/test_fase3_goldens.py`; las claves de los retornos del Motor, con el Motor de verdad, y la `memoria` de cada "
     "orden CT-05, con las órdenes que emite el ejecutor.")),
    ("Copias y citas", ("La V5.2 no tiene `.docx` (INC-T143-01). Los documentos congelados de la entrega (system prompts, "
     "funciones, archivos operativos…) y el Documento 0 del Bloque B siguen citando la V5.1, y no se editan.")),
]

# Lo que el código hace en los lotes (`Mensajeria`, CT-11 a CT-13): la lista y sus elementos
LOTES = {"CT-11": ("piezas", "una pieza de evidencia"), "CT-12": ("encargos", "un encargo de prospectiva"),
         "CT-13": ("peticiones", "una petición de objeciones")}

# Cambios que no salen del golden sino de otras incidencias (el texto es el de la incidencia)
OTROS = [
    ("CT-04", "INC-T116-01", "El Broker pide horizontes con una lista global (`horizontes`), no por tipo de activo: se rechaza "
     "cada celda que la tabla 8.3 marca «No». Decir en el Anexo B que la lista es global y que el rechazo es por celda."),
    ("CT-24", "INC-T114-02", "El ejemplo publicado del informe de seguimiento no cumple su propio esquema: corregir el ejemplo."),
    ("CT-06", "golden (fases)", "El ciclo emite las fases `CRIBADO_E_INVESTIGACION` y `RESPUESTA_OBJECIONES`, que la lista "
     "cerrada del Anexo B (CRIBADO, INVESTIGACION, PROFUNDIZACION, SEGUIMIENTO) no tiene: añadirlas."),
]

# T-140 (QA r02 de T-131, H-06): los retornos de CT-09 y CT-10 los sirve el Motor (`motor/servicio.py`), sin esquema en
# `ESQUEMAS`; los demás internos son la respuesta de un agente, validada con `ESQUEMAS`
RETORNOS_DEL_MOTOR = {"CT-09", "CT-10"}
RETORNOS_INTERNOS = {f"CT-{n:02d}" for n in range(6, 15)} - RETORNOS_DEL_MOTOR


def _tramos(cts) -> str:
    """{"CT-06", "CT-07", "CT-08", "CT-11"} → «CT-06 a CT-08 y CT-11» (tramos de contratos seguidos)."""
    ns, tramos = sorted(int(c[3:]) for c in cts), []
    for n in ns:
        if tramos and n == tramos[-1][1] + 1:
            tramos[-1][1] = n
        else:
            tramos.append([n, n])
    partes = [p for a, b in tramos for p in ([f"CT-{a:02d} a CT-{b:02d}"] if b > a + 1 else
                                            [f"CT-{n:02d}" for n in range(a, b + 1)])]
    return ", ".join(partes[:-1]) + (" y " if len(partes) > 1 else "") + partes[-1]


GENERALES = [
    ("Lotes (CT-11, CT-12 y CT-13)", "El Anexo B describe una pieza, un encargo o una petición por mensaje; el ejecutor los "
     "agrupa en una lista (`piezas`, `encargos`, `peticiones`) y rechaza el ejemplo tal cual. Propuesta: describir el "
     "mensaje como la lista, con los campos de hoy dentro de cada elemento, y cambiar el ejemplo."),
    ("Estado del objeto en los retornos de CT-23, CT-24 y CT-25", "El bloque JSON del Anexo B pone el estado del objeto en "
     "`estado`; el ejecutor lo lleva en `estado_consulta`, `estado_seguimiento` y `estado_credencial`, como pide el §6.2.6 "
     "del propio Documento 0, y deja `estado` para el estado común. Propuesta: usar esos nombres en el Anexo B."),
    ("Campo del tipo en CT-22", "El Anexo B nombra `tipo` («admite además CONSULTA_RECURRENTE y DECISION_SEGUIMIENTO»); el "
     "ejecutor emite esos dos en `tipo_aviso` y usa `tipo` para DECISIONES_BROKER y PREGUNTA_REPETIDA. Propuesta: un solo "
     "campo. Lo más barato es documentar los dos tal como están; lo más limpio, unificar en el código (cambio de formato, "
     "con re-congelado de los goldens). Se decide al preparar la entrega."),
    ("Retornos RECHAZADO o SIN_RESULTADO", "El Anexo B no dice qué campos llevan. Propuesta: «solo el estado común y el "
     "motivo (§6.2.6); los campos de resultado no se exigen», salvo CT-03, donde el ejecutor exige los campos de retorno "
     "también en un rechazo (decirlo)."),
    ("Listas cerradas", "Fuera de CT-01 y CT-02 la mensajería no aplica las listas cerradas del Anexo B (18 casos en 10 "
     "contratos) ni la condición de `contenido` de CT-23 («solo en ENTRANTE»). Propuesta: decir en cada lista si la "
     "mensajería la valida o si la valida el agente que recibe; o validarlas en el código (cambio de formato)."),
    ("CT-16 a CT-21", "El Anexo B no da sus campos (los remite a los prompts de sistema). Propuesta: dar al menos los campos "
     "de los que el ejecutor emite (CT-16, CT-17 y CT-19), que ya están congelados en `formas_flujos_mock.json`."),
    ("`fecha_corte` de CT-09", "El Anexo B la hace obligatoria solo en evaluaciones y backtesting; el ejecutor la exige "
     "siempre (es más estricto). Propuesta: obligatoria siempre."),
    # T-148 (QA r01 de T-145, H-06): ni `coincide` ni `independiente` están en `esquemas_respuestas.json`
    ("Lo que el Anexo B deja abierto", "La codificación de `coincide` (CT-10) y de `independiente` (CT-11) y los nombres de las "
     "claves de `fechas` (CT-11). Propuesta: fijarlos con los valores que usa el ejecutor. `coincide` lo sirve el Motor "
     "(`motor/servicio.py`, la re-ejecución de CT-10): SI, DENTRO_TOLERANCIA o NO, con su `categoria`. `independiente` no "
     "lo devuelve el Curador: el ejecutor asigna los EVD- y CLM-, los duplicados y las raíces en código "
     "(`Bloque._registrar_evidencia_clase`, `orquestacion.py`) y la independencia queda en `grado_independencia` de cada "
     "EVD de F2."),
    # T-145 (QA r01 de T-140, H-05): CT-09 y CT-10 no son respuestas de un agente: los sirve el Motor
    (f"Retornos internos ({_tramos(RETORNOS_INTERNOS)})", ("No pasan por la mensajería: la respuesta de cada agente se "
     "valida con los esquemas de `ESQUEMAS` (congelados en `bloque_a/11_Ejecutor/tests/goldens/esquemas_respuestas.json`), "
     "que no llevan los mismos nombres que el Anexo B. Propuesta: describir en el Anexo B los campos de esos esquemas, no "
     "marcar opcionales los de hoy.")),
    (f"Retornos del Motor ({_tramos(RETORNOS_DEL_MOTOR)})", ("Tampoco pasan por la mensajería ni son la respuesta de un "
     "agente: los sirve el Motor (`motor/servicio.py`) y no tienen esquema en `ESQUEMAS`. Propuesta: describir en el Anexo B "
     "los campos del retorno que sirve el Motor.")),
    ("Campos mínimos que el ejecutor no exige", "Por la decisión del operador, la propuesta por defecto es marcarlos en el "
     "Anexo B como opcionales («si aplica»). Si alguno debe ser obligatorio de verdad, se cambia el código en su lugar y se "
     "re-congelan los goldens con su motivo. La lista, contrato a contrato, está abajo."),
]



def _ruta(mensaje: str) -> str:
    """«preguntas/0: 'origen' is a required property» → «preguntas[].origen» (mensaje de jsonschema del golden)."""
    donde, _, resto = mensaje.partition(": ")
    campo = resto.split("'")[1]
    if donde == "(raíz)":
        return campo
    partes = [("[]" if x.isdigit() else x) for x in donde.split("/")]
    return ".".join(partes).replace(".[]", "[]") + "." + campo


def _lista(xs):
    return ", ".join(f"`{x}`" for x in xs)


def _borrador(d: dict) -> list[str]:
    """El borrador contrato a contrato de unas diferencias (el texto que se generaba hasta T-143)."""
    por = d["por_contrato"]
    mensajes = d.get("mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b", {})
    otro_campo = d.get("valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro", {})
    out = ["# Borrador · corrección del Anexo B del Documento 0 del Bloque A", "",
           "**Estado: borrador para la próxima entrega del Documento 0. No se aplica al corpus** (el Documento 0 es una "
           "entrega congelada). Generado por `.docs/scripts/borrador_anexo_b.py` a partir de "
           "`bloque_a/11_Ejecutor/tests/goldens/divergencias_anexo_b.json`; no se edita a mano: si cambian las "
           "diferencias, se vuelve a generar.", "",
           "**Por qué.** El operador decidió el 13-11-2026 que, si el Documento 0 y el código difieren, manda el código, "
           "porque el Documento 0 se escribió antes de construir el bloque (INC-T114-01 en `docs/incidencias.md`). El "
           "Anexo B se corrige para que describa lo que hace el ejecutor.", "",
           "## 1. Cambios generales", ""]
    for titulo, texto in GENERALES:
        out += [f"- **{titulo}.** {texto}"]
    out += ["", "## 2. Contrato a contrato", "",
            "| Contrato | Lo que difiere hoy | Cambio propuesto en el Anexo B |", "| --- | --- | --- |"]
    contratos = sorted({k.split(".")[0] for k in por} | {k.split(".")[0] for k in mensajes} | {c for c, _, _ in OTROS})
    for ct in contratos:
        for parte in ("ENCARGO", "RETORNO"):
            clave = f"{ct}.{parte}"
            v = por.get(clave, {})
            filas = []
            if "el_ejecutor_exige_y_el_anexo_b_no_nombra" in v:
                lista, elemento = LOTES.get(ct, (v["el_ejecutor_exige_y_el_anexo_b_no_nombra"][0], "un elemento"))
                rechazo = v.get("el_ejecutor_rechaza_el_ejemplo_del_anexo_b") or {}
                campos = sorted({_ruta(m) for m in mensajes.get(clave, []) if "(raíz)" in m and "required property" in m})
                filas.append((f"el ejecutor exige {_lista(v['el_ejecutor_exige_y_el_anexo_b_no_nombra'])} y rechaza el "
                              f"ejemplo del Anexo B ({rechazo.get('clase', '')}: «{rechazo.get('motivo', '')}»)",
                              f"el mensaje es una lista `{lista}`; cada elemento es {elemento} con los campos de hoy"
                              f"{' (' + _lista(campos) + ')' if campos else ''}; ejemplo nuevo"))
            interno = parte == "RETORNO" and ct in RETORNOS_INTERNOS
            del_motor = parte == "RETORNO" and ct in RETORNOS_DEL_MOTOR
            if v.get("el_ejecutor_admite_que_falte"):
                if interno:
                    cambio = "describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1)"
                elif del_motor:
                    cambio = "describir los campos del retorno que sirve el Motor (`motor/servicio.py`), que no tiene esquema en `ESQUEMAS`"
                else:
                    cambio = "marcarlos «opcional» (o exigirlos en el código)"
                filas.append((f"el ejecutor admite que falte {_lista(v['el_ejecutor_admite_que_falte'])}", cambio))
            for x in otro_campo.get(clave, []):
                filas.append((f"el valor `{x['valor']}` va en `{x['campo_del_ejecutor']}`, no en `{x['campo_del_anexo_b']}`",
                              f"nombrar `{x['campo_del_ejecutor']}`"))
            ya = set(v.get("el_ejecutor_admite_que_falte") or [])
            # T-131 r02 (QA r01, H-02): también los de primer nivel que el ejecutor no exige en la tabla pero no envía (en los
            # lotes, los de primer nivel son los de cada elemento y ya están en su fila)
            vistos = sorted({_ruta(m) for m in mensajes.get(clave, []) if "required property" in m
                             and not ("(raíz)" in m and (ct in LOTES or _ruta(m) in ya))})
            if vistos:
                filas.append((f"en los mensajes emitidos falta {_lista(vistos)}", "marcarlos «si aplica»"))
            for m in mensajes.get(clave, []):
                if ": type '" in m:
                    campo, tipo = m.split(": type '")
                    filas.append((f"`{campo}` llega con otro tipo en algún mensaje emitido (el Anexo B pide "
                                  f"{tipo.rstrip(chr(39))})", "admitir el tipo que envía el ejecutor (ver el golden de formas)"))
            for c, origen, texto in OTROS:
                if c == ct and parte == ("ENCARGO" if c != "CT-24" else "RETORNO"):
                    filas.append((f"{origen}", texto))
            for dif, cambio in filas:
                out.append(f"| {clave} | {dif} | {cambio} |")
    sin = d.get("contratos_sin_campos_en_el_anexo_b", [])
    out += ["", "## 3. Contratos sin campos en el Anexo B", "", f"{_lista(sin)}: ver «CT-16 a CT-21» en el §1.", "",
            "## 4. Cómo se aplica en la entrega", "",
            "1. Se edita el Anexo B (y los §7.6 y §7.9 si se unifica el campo de CT-22) en la nueva versión del Documento 0.",
            "2. Se re-congela el corpus con su motivo (`tools/corpus_integridad.py --update`) y los goldens que dependan "
            "del Anexo B (`anexo_b_esquemas.json`, `huellas.json`, `divergencias_anexo_b.json`) con `goldens_ct.py "
            "--update --motivo`.", "3. `divergencias_anexo_b.json` debería quedar vacío, salvo lo que se decida dejar.",
            ""]
    return out


def _lo_que_queda(d: dict) -> list[str]:
    medidas = any(d.get(k) for k in ("por_contrato", "mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b",
                                     "valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"))
    sin = d.get("contratos_sin_campos_en_el_anexo_b", [])
    out = [f"- **Contratos sin campos en el Anexo B.** {_lista(sin)}: la V5.2 los sigue remitiendo a los prompts de sistema."
           if sin else "- **Contratos sin campos en el Anexo B.** Ninguno."]
    if not medidas:
        out += ["- **Diferencias medidas.** Ninguna: contra la V5.2, `divergencias_anexo_b.json` no tiene diferencias por "
                "contrato, ni mensajes de los flujos que no cumplan el Anexo B, ni valores en otro campo."]
    out += [f"- **{titulo}.** {texto}" for titulo, texto in QUEDA]
    if medidas:   # una diferencia nueva contra la V5.2: se dice contrato a contrato, como en el borrador
        tabla = _borrador(d)
        desde = tabla.index("| Contrato | Lo que difiere hoy | Cambio propuesto en el Anexo B |")
        hasta = tabla.index("## 3. Contratos sin campos en el Anexo B")
        out += ["", "### Diferencias medidas contra la V5.2", ""] + tabla[desde:hasta - 1]
    return out


def generar() -> str:
    actual = json.loads(DIVERGENCIAS.read_text(encoding="utf-8"))
    v51 = json.loads(DIVERGENCIAS_V51.read_text(encoding="utf-8"))
    borrador = _borrador(v51)
    cuerpo = borrador[borrador.index("## 1. Cambios generales"):]
    out = ["# Borrador · corrección del Anexo B del Documento 0 del Bloque A", "",
           f"**Estado: aplicado en el Documento 0 V5.2** (`{DOC0_V52}`, T-143, 15-11-2026). La V5.1 está en "
           "`bloque_a/99_Historico_V5.1/01_Gobernanza/`. Generado por `.docs/scripts/borrador_anexo_b.py`; no se edita a mano: "
           "si cambian las diferencias, se vuelve a generar. Las decisiones de la aplicación están en INC-T114-01 "
           "(`docs/incidencias.md`) y en `.docs/tickets/T-143/analisis-tecnico.md`.", "",
           "## Lo que queda contra la V5.2", ""] + _lo_que_queda(actual)
    out += ["", "## Borrador aplicado (contra el Anexo B V5.1)", "",
            "El borrador tal como se aplicó, generado con las diferencias congeladas contra la V5.1 "
            "(`.docs/diseno/bloque_a/divergencias_anexo_b_v51.json`, copia de `divergencias_anexo_b.json` antes de T-143).", "",
            "> Estado hasta T-143: " + borrador[2].removeprefix("**Estado: ").replace("**", ""), "", *borrador[4:6]]
    out += [("#" + x if x.startswith("## ") else x) for x in cuerpo]
    return "\n".join(out)


def main() -> int:
    texto = generar()
    if "--comprobar" in sys.argv:
        return 0 if SALIDA.exists() and SALIDA.read_text(encoding="utf-8") == texto else 1
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"escrito {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
