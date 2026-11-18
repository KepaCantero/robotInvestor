"""T-187 · PB-51 del plan de pruebas del Bloque A: revisión documental de los system prompts.

Sin red y determinista. Lee los prompts como datos (`bloque_a/02_System_prompts/*.md`) y deja, en la carpeta del ticket
(`.docs/tickets/T-187/`, `--salida` por defecto; el script vive en `.docs/scripts/` desde la QA r01, H-06):

- `informe_pb51.md`: estructura del Anexo G (paso 1), recuento de la sección 10 por subárea (paso 2), referencias y DOI,
  tamaños y el resumen;
- `muestra_afirmaciones.json`: la muestra reproducible de 10 afirmaciones técnicas por prompt (preparación del paso 3).
  Las afirmaciones NO se juzgan aquí: los campos `veredicto` y `nota` quedan vacíos para los revisores independientes.

Si existe la carpeta de veredictos (`veredictos/` junto a la salida, o `--veredictos V`), el informe añade el contraste del
paso 3: lee los lotes `lote_*.json` de los revisores y el `comentario.json` (erratas, casos dudosos y discutibles) y
cuenta por lote, por prompt y en total, con los dos denominadores (verificables, que es el criterio de INC-T187-02, y
todas). Falla cerrado (2) si falta o sobra un id respecto a la muestra, si un id se repite, si hay un veredicto
desconocido, si una nota pasa de 40 palabras o si el comentario no casa con los veredictos.

Uso, desde la raíz del repositorio y con el Python del `.venv`:
    .venv/bin/python .docs/scripts/revision_prompts_pb51.py            # genera el informe y la muestra
    .venv/bin/python .docs/scripts/revision_prompts_pb51.py --comprobar  # 1 si lo generado difiere de lo que hay
Opciones: --raiz R (repositorio), --salida S (carpeta de salida), --semilla TEXTO, --ejecutor E (de dónde se importan
los nombres de agente y la aproximación de tokens; por defecto el de --raiz), --veredictos V (carpeta de los lotes).

Los criterios de cada recuento están en las constantes de abajo y en `analisis-tecnico.md`. Ningún umbral de aprobación
se escribe aquí: el 10 de la muestra sale de PB-51 (paso 3) y los topes de tamaño de la configuración del ejecutor
(`v6.tope_tokens_system`); el 95 % del criterio y las 40 palabras de la nota, de PB-51 y del encargo a los revisores.
Termina con 2 si falta una entrada o si los veredictos no son válidos (falla cerrado).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------------------------------------------------
# Origen de las constantes
# --------------------------------------------------------------------------------------------------------------------
MUESTRA_POR_PROMPT = 10                     # PB-51, paso 3: «Muestreo de 10 afirmaciones técnicas por prompt»
UMBRAL_CORRECTAS = 95                       # PB-51, criterio de aprobación: «≥ 95 % de afirmaciones muestreadas correctas»
MAX_PALABRAS_NOTA = 40                      # encargo del paso 3 a los revisores: la nota, de 40 palabras como máximo
MIN_PALABRAS_CITA = 3                       # [PROPUESTO] (QA r02, H-09): la cita de la nota, al menos 3 palabras con letra
#                                             o cifra («a» o « de » no sostienen nada); la más corta de hoy tiene 4
VEREDICTOS = ("CORRECTA", "ERRONEA", "NO_VERIFICABLE")   # los de la muestra (`veredictos_validos`)
# Caso dudoso (QA r01, H-03): una CORRECTA cuya nota trae un matiz explícito. El comentario tiene que listar exactamente esas.
RE_MATIZ = re.compile(r"\bmatiz\b|\bexager|\bdifieren\b|\bojo\b", re.IGNORECASE)
# Atribución a un revisor de que una ERRONEA es discutible: su nota tiene que decirlo.
RE_DISCUTIBLE = re.compile(r"discutib", re.IGNORECASE)
# Fuente que declara la nota (QA r01, H-04), por este orden: búsqueda web (no «sin búsqueda web»), conocimiento propio
# (memoria), cálculo a mano; si no, sin fuente declarada.
FUENTES = (("búsqueda web", re.compile(r"(?<!sin )búsqueda web|\bweb:", re.IGNORECASE)),
           ("memoria (conocimiento propio)", re.compile(r"conocimiento propio", re.IGNORECASE)),
           ("cálculo a mano", re.compile(r"cálculo propio|cálculo verificado|comprobado a mano|aritmética|álgebra verificada",
                                         re.IGNORECASE)))
SIN_FUENTE = "sin fuente declarada"
SEMILLA_POR_DEFECTO = "T-187 · PB-51"       # texto, no número: Random(str) es determinista (versión 2 de la semilla)
RAIZ_POR_DEFECTO = Path(__file__).resolve().parents[2]          # el script está en .docs/scripts/
SALIDA_POR_DEFECTO = RAIZ_POR_DEFECTO / ".docs" / "tickets" / "T-187"   # los datos de PB-51 se quedan en el ticket
PREFIJO_PROMPT = "System prompt - "         # lo demás (el «Marco común … (plantilla)») es plantilla, no prompt de agente
LONG_RAIZ = 6                               # técnico: dos títulos coinciden si comparten una palabra por sus 6 primeras
#                                             letras («formato»/«formatos», «metodología»/«metodológico»)
VACIAS = {"de", "del", "la", "las", "el", "los", "y", "e", "en", "que", "te", "tu", "tus", "con", "por", "para", "un",
          "una", "como", "qué", "cómo", "tú", "al", "lo", "su", "sus", "o", "a", "propios", "propias", "propio"}

RE_SECCION = re.compile(r"^## +(\d+)\.\s*(.*?)\s*$")
RE_FIN_SECCION = re.compile(r"^#{1,2} ")
RE_SUBAREA = re.compile(r"^#{3,4} +(\d+)\.(\d+)(?:\.\d+)*(?:\s+(bis))?\.?\s*(.*?)\s*$")
RE_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
RE_CODIGO = re.compile(r"`([^`\n]+)`")

# Subáreas que se excluyen de los recuentos y de la muestra: el inventario resume lo anterior (13.8 del Documento 0 de B
# lo define como lista de lo que la sección contiene), no añade definiciones ni fórmulas.
RE_INVENTARIO = re.compile(r"inventario de competencias", re.IGNORECASE)
# Subáreas de trampas: todo elemento suyo cuenta como trampa.
RE_TITULO_TRAMPAS = re.compile(r"trampa|error|sesgo", re.IGNORECASE)
RE_TEXTO_TRAMPA = re.compile(r"\btrampas?\b|\berror(?:es)? (?:frecuentes?|típicos?|comunes?)\b", re.IGNORECASE)
# Subáreas de referencias canónicas: cada entrada se comprueba (autor, año y título).
RE_TITULO_REFERENCIAS = re.compile(r"referencias (?:académicas )?canónicas|literatura de referencia|bibliograf", re.IGNORECASE)

# Definición operativa: el elemento empieza por un término en negrita (con un paréntesis opcional) y sigue con «:», «=»
# o una raya.
RE_DEFINICION = re.compile(r"^\*\*[^*\n]{1,160}\*\*(?:\s*\([^()\n]*(?:\([^()\n]*\)[^()\n]*)*\))?\s*(?::|=|—|–|≈)")
# Fórmula: un tramo de código con un operador entre dos operandos o con un símbolo de cálculo, o un «=»/«≈» con espacios
# fuera del código. Un tramo que es una ruta o una dirección web no es fórmula.
RE_OPERADOR = re.compile(r"[\w)\]}|'′²³]\s*(?:=|≈|≤|≥|<|>|×|·|/|\+|−|\^|÷|\*)\s*[\w(\[{|√Σ∑−\-.]")
RE_SIMBOLO_CALCULO = re.compile(r"[√Σ∑∫∂∏]|\b(?:ln|exp|log|max|min|Var|Cov|E)\s*[\[(]")
RE_RUTA = re.compile(r"://|^www\.|^[\w.-]+\.(?:org|com|net|io|es|eu|gov|int|md|py|json|csv|yaml)\b|^[\w.-]+/<")
RE_IGUAL_TEXTO = re.compile(r"\s[=≈]\s")
# Umbral: un comparador seguido de una cifra, o un comparador en palabras seguido de una cifra.
RE_UMBRAL = re.compile(r"(?:≥|≤|>=|<=|<|>)\s*[−\-]?\s*\d"
                       r"|\b(?:al menos|como mínimo|como máximo|más de|menos de|por encima de|por debajo de|superior a"
                       r"|inferior a|mayor que|menor que)\s+(?:(?:un|una|el|la|del|los|las)\s+)?[−\-]?\d", re.IGNORECASE)
# Hecho con cifra (para elegir afirmaciones candidatas, no para los recuentos).
RE_CIFRA = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|pp\b|pb\b|p\. ?b\.|años?\b|meses\b|días\b|veces\b|billones\b|millones\b"
                      r"|mil millones\b|sesiones\b|semanas\b)")

# Citas. Autor: apellido con mayúscula (partículas opcionales), varios unidos por «,», «y», «e», «and», «&», y «et al.».
_PALABRA_AUTOR = r"[A-ZÁÉÍÓÚÑÄÖÜÇ][\w'’\-]*[A-Za-záéíóúñäöüç'’\-]"
# Las partículas solo dentro del apellido («López de Prado»): al principio serían la preposición de la frase.
_AUTOR = rf"{_PALABRA_AUTOR}(?:\s+(?:de|van|von|der|del|la|le|di|da|du|ten)(?:\s+(?:la|der|den))?\s+{_PALABRA_AUTOR})*"
_AUTORES = rf"{_AUTOR}(?:(?:,\s*|\s+y\s+|\s+e\s+|\s+and\s+|\s*&\s*){_AUTOR})*(?:\s+et\s+al\.)?"
_ANIO = r"(1[5-9]\d\d|20\d\d)[a-z]?"        # estructura de un año (siglos XVI a XXI), no un umbral
_TITULO = r"(«[^»]+»|(?<!\*)\*(?!\*)[^*\n]+(?<!\*)\*(?!\*)|\"[^\"\n]+\"|“[^”\n]+”)"   # «…», *cursiva*, comillas
RE_CITA_A = re.compile(rf"(?<![\w(])({_AUTORES})\s+\({_ANIO}((?:[^()]|\([^()]*\))*)\)(?:[.,]?\s*{_TITULO})?")  # Autor (1996, «T») · Autor (1996). «T»
RE_CITA_B_PARTE = re.compile(rf"^\s*({_AUTORES}),?\s+{_ANIO}\b(.*)$", re.DOTALL)                  # (Autor, 1996, «T»)
RE_CITA_C = re.compile(rf"(?<![\w(])({_AUTORES}),\s+{_TITULO},?\s+(?:[^,()]*,\s*)?{_ANIO}")  # Autor, «T», 1996
RE_PARENTESIS = re.compile(r"\(((?:[^()]|\([^()]*\))*)\)")
RE_TIENE_TITULO = re.compile(_TITULO)
NO_AUTOR = {"Anexo", "Tabla", "Sección", "Versión", "Fase", "Ciclo", "Regla", "Paso", "Nivel", "Caso", "Ley", "Hito"}

# DOI (Handbook del DOI, 2.2): «10.» + registrante numérico (con subdivisiones «.») + «/» + sufijo sin espacios. El DOI no
# lleva dígito de control: solo se valida la estructura. Que exista no se comprueba (sin red). ISBN e ISSN sí llevan
# dígito de control, y se valida.
RE_DOI_CANDIDATO = re.compile(r"\b10\.\d+(?:\.\d+)*/\S*|(?i:\bdoi:\s*)([^\s,;]*[\d/][^\s,;]*)")   # «10.N/…» o «doi: <algo con cifra o barra>»
RE_DOI_VALIDO = re.compile(r"^10\.\d{4,9}(?:\.\d+)*/[^\s/][^\s]*$")
RE_ISBN = re.compile(r"\bISBN(?:-1[03])?:?\s*([0-9Xx][0-9Xx \-]{8,20}[0-9Xx])")
RE_ISSN = re.compile(r"\bISSN:?\s*(\d{4}-?\d{3}[\dXx])\b")

# Partición en frases: un punto (u otro final) seguido de espacio y mayúscula. Se vuelven a unir los cortes tras una
# abreviatura o una inicial, o dentro de un tramo de código, unas comillas o un paréntesis abiertos.
RE_CORTE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡«*`(\[])")
ABREVIATURAS = ("p. ej.", "et al.", "EE. UU.", "etc.", "vs.", "aprox.", "núm.", "pág.", "págs.", "cf.", "e. g.",
                "i. e.", "Sr.", "Dr.", "Ed.", "eds.", "vol.", "cap.", "art.", "apdo.", "U.S.", "S.A.", "Inc.", "No.")


# --------------------------------------------------------------------------------------------------------------------
# Estructuras
# --------------------------------------------------------------------------------------------------------------------
@dataclass
class Seccion:
    numero: int
    titulo: str
    linea: int               # 1-based, la del título
    lineas: list[str]        # el cuerpo (sin el título)


@dataclass
class Elemento:
    linea: int               # 1-based, la primera
    texto: str               # copia exacta de las líneas del archivo, sin la viñeta inicial
    tabla: bool = False


@dataclass
class Subarea:
    clave: str               # «10.4», «10.1 bis», «10.0» (lo que va antes de la primera subárea)
    titulo: str
    elementos: list[Elemento] = field(default_factory=list)


@dataclass
class Cita:
    autores: str
    anio: str
    titulo: bool
    texto: str


# --------------------------------------------------------------------------------------------------------------------
# Lectura
# --------------------------------------------------------------------------------------------------------------------
def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def leer(p: Path) -> str:
    return nfc(p.read_text(encoding="utf-8"))


def leer_anexo_g(texto_d0: str) -> list[tuple[int, str]]:
    """Las secciones del Anexo G del Documento 0: lista numerada bajo «## ANEXO G…», hasta el título siguiente."""
    lineas = texto_d0.splitlines()
    ini = next((i for i, x in enumerate(lineas) if re.match(r"^#{1,3}\s+\**ANEXO G\b", x, re.IGNORECASE)), None)
    if ini is None:
        raise ValueError("el Documento 0 no tiene «ANEXO G»")
    out: list[tuple[int, str]] = []
    for x in lineas[ini + 1:]:
        if x.startswith("#"):
            break
        m = re.match(r"^(\d+)\.\s+(.*)$", x.strip())
        if m:
            out.append((int(m.group(1)), m.group(2).replace("**", "").strip()))
    if [n for n, _ in out] != list(range(1, len(out) + 1)) or not out:
        raise ValueError(f"el Anexo G no es una lista numerada 1..n: {[n for n, _ in out]}")
    return out


def secciones(texto: str) -> list[Seccion]:
    """Secciones `## N. Título` (fuera de bloques de código), con su cuerpo hasta el título de nivel 1 o 2 siguiente."""
    out: list[Seccion] = []
    actual: Seccion | None = None
    en_codigo = False
    for i, x in enumerate(texto.splitlines(), start=1):
        if x.lstrip().startswith("```"):
            en_codigo = not en_codigo
        if not en_codigo and RE_FIN_SECCION.match(x):
            m = RE_SECCION.match(x)
            actual = Seccion(int(m.group(1)), m.group(2), i, []) if m else None
            if actual:
                out.append(actual)
            continue
        if actual is not None:
            actual.lineas.append(x)
    return out


def raices(titulo: str) -> set[str]:
    t = re.sub(r"\([^)]*\)", " ", nfc(titulo).casefold()).replace("**", " ")
    palabras = re.findall(r"[^\W\d_]+", t)
    return {w[:LONG_RAIZ] for w in palabras if w not in VACIAS}


def elementos(lineas: list[str], primera: int) -> list[Elemento]:
    """Elementos de un bloque: cada viñeta (con sus líneas de continuación), cada párrafo, cada fila de tabla (sin la de
    separación) y cada bloque de código. `primera` es el número de línea (1-based) de `lineas[0]`."""
    out: list[Elemento] = []
    cur: list[str] = []
    cur_ini = 0
    cur_item = False
    en_codigo = False

    def cerrar() -> None:
        nonlocal cur, cur_item
        if cur:
            txt = "\n".join(cur)
            if cur_item:
                txt = RE_ITEM.sub("", txt, count=1)
            out.append(Elemento(cur_ini, txt))
        cur, cur_item = [], False

    for k, x in enumerate(lineas):
        n = primera + k
        if x.lstrip().startswith("```"):
            if en_codigo:
                cur.append(x)
                cerrar()
                en_codigo = False
            else:
                cerrar()
                en_codigo, cur, cur_ini = True, [x], n
            continue
        if en_codigo:
            cur.append(x)
            continue
        if not x.strip() or x.startswith("#") or re.match(r"^\s*-{3,}\s*$", x):
            cerrar()
            continue
        if x.lstrip().startswith("|"):
            cerrar()
            if not re.match(r"^\s*\|[\s:|\-]+\|\s*$", x):
                out.append(Elemento(n, x, tabla=True))
            continue
        if RE_ITEM.match(x):
            cerrar()
            cur, cur_ini, cur_item = [x], n, True
            continue
        if not cur:
            cur_ini = n
        cur.append(x)
    cerrar()
    return out


def subareas(sec: Seccion) -> list[Subarea]:
    """La sección 10 partida por sus subáreas `### 10.x` (las `#### 10.x.y` se suman a su 10.x)."""
    out: list[Subarea] = [Subarea(f"{sec.numero}.0", "(antes de la primera subárea)")]
    bloque: list[str] = []
    ini = sec.linea + 1

    def volcar() -> None:
        out[-1].elementos.extend(elementos(bloque, ini))

    for k, x in enumerate(sec.lineas):
        m = RE_SUBAREA.match(x)
        if m and int(m.group(1)) == sec.numero:
            clave = f"{m.group(1)}.{m.group(2)}" + (" bis" if m.group(3) else "")
            volcar()
            bloque, ini = [], sec.linea + 1 + k + 1
            if clave != out[-1].clave:
                out.append(Subarea(clave, m.group(4)))
            continue
        bloque.append(x)
    volcar()
    return [s for s in out if s.elementos or s.clave != f"{sec.numero}.0"]


# --------------------------------------------------------------------------------------------------------------------
# Clasificadores
# --------------------------------------------------------------------------------------------------------------------
def sin_codigo(t: str) -> str:
    return RE_CODIGO.sub(" ", t)


def es_formula(span: str) -> bool:
    s = span.strip()
    if RE_RUTA.search(s):
        return False
    return bool(RE_OPERADOR.search(s) or RE_SIMBOLO_CALCULO.search(s))


def n_formulas(t: str) -> int:
    return sum(es_formula(s) for s in RE_CODIGO.findall(t)) + len(RE_IGUAL_TEXTO.findall(sin_codigo(t)))


def n_umbrales(t: str) -> int:
    return len(RE_UMBRAL.findall(t))


def es_definicion(t: str) -> bool:
    return bool(RE_DEFINICION.match(t.lstrip()))


def _autor_valido(a: str) -> bool:
    primero = re.split(r",|\s+y\s+|\s+e\s+|\s+and\s+|&", a)[0].strip().split()[-1]
    return primero not in NO_AUTOR


def citas(t: str) -> list[Cita]:
    """Citas autor-año de un texto, con si llevan título («…», *…* o comillas) en la propia cita."""
    out: list[Cita] = []
    vistos: set[tuple[int, int]] = set()
    for m in RE_CITA_A.finditer(t):
        resto = m.group(3) or ""
        out.append(Cita(m.group(1).strip(), m.group(2), bool(RE_TIENE_TITULO.search(resto) or m.group(4)), m.group(0)))
        vistos.add(m.span())
    for m in RE_PARENTESIS.finditer(t):
        if any(a <= m.start() < b for a, b in vistos):
            continue
        for parte in m.group(1).split(";"):
            mb = RE_CITA_B_PARTE.match(parte)
            if mb:
                mt = RE_TIENE_TITULO.search(mb.group(3) or "")
                out.append(Cita(mb.group(1).strip(), mb.group(2), bool(mt),
                                f"{mb.group(1).strip()}, {mb.group(2)}" + (f", {mt.group(0)}" if mt else "")))
    for m in RE_CITA_C.finditer(t):
        out.append(Cita(m.group(1).strip(), m.group(3), True, m.group(0)))
    return [c for c in out if _autor_valido(c.autores)]


def clave_cita(c: Cita) -> tuple[str, str]:
    primero = re.split(r",|\s+y\s+|\s+e\s+|\s+and\s+|&|\s+et\s+al\.", c.autores)[0].strip()
    return (nfc(primero).casefold(), c.anio)


def es_trampa(t: str, sub: Subarea) -> bool:
    return bool(RE_TITULO_TRAMPAS.search(sub.titulo) or RE_TEXTO_TRAMPA.search(t))


def doi_valido(d: str) -> bool:
    return bool(RE_DOI_VALIDO.match(d))


def isbn_valido(s: str) -> bool:
    d = re.sub(r"[\s\-]", "", s).upper()
    if len(d) == 10 and re.fullmatch(r"\d{9}[\dX]", d):
        return sum((10 - i) * (10 if c == "X" else int(c)) for i, c in enumerate(d)) % 11 == 0
    if len(d) == 13 and d.isdigit():
        return sum((1 if i % 2 == 0 else 3) * int(c) for i, c in enumerate(d)) % 10 == 0
    return False


def issn_valido(s: str) -> bool:
    d = s.replace("-", "").upper()
    if not re.fullmatch(r"\d{7}[\dX]", d):
        return False
    suma = sum((8 - i) * int(c) for i, c in enumerate(d[:7]))
    control = (11 - suma % 11) % 11
    return d[7] == ("X" if control == 10 else str(control))


def identificadores(texto: str) -> dict[str, list[dict[str, Any]]]:
    dois = []
    for m in RE_DOI_CANDIDATO.finditer(texto):
        d = (m.group(1) or m.group(0)).rstrip(".,;:)»”\"'`")
        dois.append({"doi": d, "estructura_valida": doi_valido(d)})
    isbns = [{"isbn": m.group(1), "control_valido": isbn_valido(m.group(1))} for m in RE_ISBN.finditer(texto)]
    issns = [{"issn": m.group(1), "control_valido": issn_valido(m.group(1))} for m in RE_ISSN.finditer(texto)]
    return {"doi": dois, "isbn": isbns, "issn": issns}


# --------------------------------------------------------------------------------------------------------------------
# Frases y afirmaciones candidatas
# --------------------------------------------------------------------------------------------------------------------
def _abierto(t: str) -> bool:
    return (t.count("`") % 2 == 1 or t.count("«") > t.count("»") or t.count("(") > t.count(")")
            or t.count("**") % 2 == 1)


def frases(t: str) -> list[str]:
    """Frases de un elemento, cada una copia exacta de un tramo suyo."""
    tramos: list[list[int]] = []
    pos = 0
    for m in RE_CORTE.finditer(t):
        tramos.append([pos, m.start()])
        pos = m.end()
    tramos.append([pos, len(t)])
    unidos: list[list[int]] = []
    for tr in tramos:
        if unidos:
            prev = t[unidos[-1][0]:unidos[-1][1]]
            if _abierto(prev) or prev.endswith(ABREVIATURAS) or re.search(r"(?:^|[\s(])[A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]?\.$", prev):
                unidos[-1][1] = tr[1]
                continue
        unidos.append(tr)
    return [t[a:b].strip() for a, b in unidos if t[a:b].strip()]


def marcas(t: str) -> list[str]:
    m = []
    if n_formulas(t):
        m.append("formula")
    if n_umbrales(t):
        m.append("umbral")
    if es_definicion(t):
        m.append("definicion")
    if citas(t):
        m.append("cita")
    if RE_CIFRA.search(sin_codigo(t)):
        m.append("cifra")
    return m


def _cita_texto(cs: list[Cita]) -> str | None:
    return " · ".join(dict.fromkeys(c.texto for c in cs)) or None


# --------------------------------------------------------------------------------------------------------------------
# Revisión de un prompt
# --------------------------------------------------------------------------------------------------------------------
def numero_por_raiz(anexo: list[tuple[int, str]], palabra: str) -> int:
    r = palabra.casefold()[:LONG_RAIZ]
    ns = [n for n, t in anexo if r in raices(t)]
    if len(ns) != 1:
        raise ValueError(f"«{palabra}» no identifica una sola sección del Anexo G: {ns}")
    return ns[0]


def revisar_estructura(secs: list[Seccion], anexo: list[tuple[int, str]]) -> dict[str, Any]:
    nums = [s.numero for s in secs]
    esperados = [n for n, _ in anexo]
    faltan = [n for n in esperados if n not in nums]
    sobran = sorted({n for n in nums if n not in esperados})
    repetidas = sorted({n for n in nums if nums.count(n) > 1})
    en_orden = nums == sorted(nums)
    titulos = dict(anexo)
    coherencia = {}
    for s in secs:
        if s.numero in titulos:
            comun = raices(s.titulo) & raices(titulos[s.numero])
            coherencia[s.numero] = {"titulo": s.titulo, "coincide": bool(comun)}
    completa = not faltan and not sobran and not repetidas and en_orden
    return {"secciones": nums, "faltan": faltan, "sobran": sobran, "repetidas": repetidas, "en_orden": en_orden,
            "completa": completa, "titulos": coherencia}


def recuento_seccion10(sec: Seccion | None) -> list[dict[str, Any]]:
    if sec is None:
        return []
    filas = []
    for sub in subareas(sec):
        excl = bool(RE_INVENTARIO.search(sub.titulo))
        es_ref = bool(RE_TITULO_REFERENCIAS.search(sub.titulo))
        d = f = u = tr = r = 0
        for e in sub.elementos:
            d += es_definicion(e.texto)
            f += n_formulas(e.texto)
            u += n_umbrales(e.texto)
            tr += es_trampa(e.texto, sub)
            r += len(entradas_lista(e.texto)) if es_ref else len(citas(e.texto))
        fila = {"subarea": sub.clave, "titulo": sub.titulo, "elementos": len(sub.elementos), "definiciones": d,
                "formulas": f, "umbrales": u, "trampas": tr, "referencias": r, "excluida": excl, "es_referencias": es_ref}
        if excl:
            fila.update(definiciones=0, formulas=0, umbrales=0, trampas=0, referencias=0)
        filas.append(fila)
    return filas


def entradas_referencia(t: str) -> list[str]:
    """Entradas de una lista de referencias canónicas: separadas por « · » o por «;» al nivel exterior del texto."""
    partes: list[str] = []
    nivel, ini = 0, 0
    for i, ch in enumerate(t):
        if ch in "(«":
            nivel += 1
        elif ch in ")»":
            nivel = max(0, nivel - 1)
        elif nivel == 0 and (t.startswith(" · ", i) or ch == ";"):
            partes.append(t[ini:i])
            ini = i + (3 if ch == " " else 1)
    partes.append(t[ini:])
    return [p.strip().rstrip(".") for p in partes if p.strip().strip(".")]


RE_AUTOR_INICIAL = re.compile(rf"^\s*(?:\*\*)?((?:[A-ZÁÉÍÓÚÑ]\.\s?)*{_AUTOR})")   # admite iniciales: «J.P. Morgan»
RE_MISMOS_AUTORES = re.compile(rf"^\s*\({_ANIO}\)")   # «…; (1983). «T»»: los autores de la entrada anterior
RE_ANIO = re.compile(rf"\b{_ANIO}\b")


def entradas_lista(t: str) -> list[dict[str, Any]]:
    """Las entradas de un elemento de una lista de referencias canónicas que parecen referencias (llevan un año o un
    título); las demás partes son instrucciones («si necesitas una referencia no listada…») y no cuentan. De cada una:
    si empieza por un autor (apellido o institución con mayúscula), si lleva año, si lleva título y su clave (primer
    apellido, año)."""
    out: list[dict[str, Any]] = []
    if t.lstrip().startswith("|"):                       # fila de tabla: cada celda es una entrada posible
        t = " · ".join(c.strip() for c in t.strip().strip("|").split("|"))
    for ent in entradas_referencia(t):
        ma, my, mt = RE_AUTOR_INICIAL.match(ent), RE_ANIO.search(ent), RE_TIENE_TITULO.search(ent)
        if not (my or mt):
            continue
        nombre = ma.group(1) if ma else None
        if nombre is None and out and out[-1]["autor"] and RE_MISMOS_AUTORES.match(ent):
            nombre = out[-1]["nombre"]
        autor = nombre is not None and nombre.split()[-1] not in NO_AUTOR
        clave = (nfc(nombre).casefold(), my.group(1)) if nombre and my else None
        out.append({"entrada": ent, "autor": autor, "anio": bool(my), "titulo": bool(mt), "clave": clave,
                    "nombre": nombre})
    return out


def revisar_referencias(sec10: Seccion | None, texto: str) -> dict[str, Any]:
    """Cada entrada de las subáreas de referencias canónicas: autor y año reconocibles y título, en la entrada (estricto)
    o en otra cita del mismo autor y año del prompt (amplio)."""
    todas = citas(texto)
    con_titulo = {clave_cita(c) for c in todas if c.titulo}
    if sec10 is not None:                # las entradas con título de las listas también dan título a su clave
        con_titulo |= {x["clave"] for sub in subareas(sec10) if RE_TITULO_REFERENCIAS.search(sub.titulo)
                       for e in sub.elementos for x in entradas_lista(e.texto) if x["titulo"] and x["clave"]}
    entradas = []
    if sec10 is not None:
        for sub in subareas(sec10):
            if not RE_TITULO_REFERENCIAS.search(sub.titulo):
                continue
            for e in sub.elementos:
                for x in entradas_lista(e.texto):
                    autor_anio = x["autor"] and x["anio"]
                    entradas.append({"subarea": sub.clave, "linea": e.linea, "entrada": x["entrada"],
                                     "autor_anio": autor_anio, "titulo_en_la_entrada": autor_anio and x["titulo"],
                                     "titulo_en_el_prompt": autor_anio and (x["titulo"] or x["clave"] in con_titulo)})
    tiene_lista = sec10 is not None and any(RE_TITULO_REFERENCIAS.search(s.titulo) for s in subareas(sec10))
    return {"entradas": entradas, "tiene_lista": tiene_lista, "citas_en_el_prompt": len(todas),
            "citas_sin_titulo_en_el_prompt": sum(1 for c in todas if not c.titulo and clave_cita(c) not in con_titulo)}


def candidatas(texto: str, secs: list[Seccion], n_metodo: int, n10: int) -> list[dict[str, Any]]:
    """Frases con marca técnica de la sección de método (entera) y de la base de conocimientos (por subáreas, sin el
    inventario ni las listas de referencias); las tablas y los bloques de código no se parten en frases."""
    out = []
    for s in secs:
        if s.numero not in (n_metodo, n10):
            continue
        if s.numero == n10:
            subs = subareas(s)
        else:
            subs = [Subarea(f"{s.numero}", s.titulo, elementos(s.lineas, s.linea + 1))]
        for sub in subs:
            if RE_INVENTARIO.search(sub.titulo) or RE_TITULO_REFERENCIAS.search(sub.titulo):
                continue                 # resumen y lista de referencias: no son afirmaciones
            for e in sub.elementos:
                if e.tabla or e.texto.lstrip().startswith("```"):
                    continue
                cs_elem = citas(e.texto)
                for fr in frases(e.texto):
                    mk = marcas(fr)
                    if not mk:
                        continue
                    if fr not in texto:
                        raise ValueError(f"una frase no es copia exacta del prompt: {fr[:60]!r}")
                    cs = citas(fr)
                    out.append({"seccion": f"{s.numero}. {s.titulo}",
                                "subarea": f"{sub.clave} {sub.titulo}".strip() if s.numero == n10 else None,
                                "linea": e.linea + e.texto[:e.texto.find(fr)].count("\n") if fr in e.texto else e.linea,
                                "texto": fr, "marcas": mk,
                                "referencia_citada": _cita_texto(cs),
                                "referencia_del_elemento": None if cs else _cita_texto(cs_elem)})
    return out


def muestra(cands: list[dict[str, Any]], semilla: str, archivo: str) -> list[dict[str, Any]]:
    rng = random.Random(f"{semilla}|{archivo}")
    k = min(MUESTRA_POR_PROMPT, len(cands))
    idx = sorted(rng.sample(range(len(cands)), k))
    return [cands[i] for i in idx]


def nombre_agente(archivo: str) -> str:
    m = re.match(rf"^{re.escape(PREFIJO_PROMPT)}(.*?) - Versión", archivo)
    return m.group(1) if m else archivo


def tokens_aprox(texto: str, ejecutor: Path) -> int:
    """La misma aproximación del ejecutor (`bloque_a/llm.py`), importada para no copiar su factor."""
    sys.path.insert(0, str(ejecutor))
    try:
        from bloque_a.llm import _tokens_aprox
    finally:
        sys.path.pop(0)
    return int(_tokens_aprox(texto))


def agente_id(nombre: str, ejecutor: Path) -> str | None:
    sys.path.insert(0, str(ejecutor))
    try:
        from bloque_a.prompts import NOMBRES_ALTERNATIVOS
    finally:
        sys.path.pop(0)
    for ag, ns in NOMBRES_ALTERNATIVOS.items():
        if nombre in ns:
            return ag
    return None


def analistas_tipo(ejecutor: Path) -> set[str]:
    sys.path.insert(0, str(ejecutor))
    try:
        from bloque_a.prompts import ANALISTAS_TIPO
    finally:
        sys.path.pop(0)
    return set(ANALISTAS_TIPO)


def revisar_tamano(texto: str, secs: list[Seccion], ag: str | None, topes: dict[str, int], analistas: set[str],
                   n10: int, ejecutor: Path) -> dict[str, Any]:
    tok = tokens_aprox(texto, ejecutor)
    out: dict[str, Any] = {"palabras": len(texto.split()), "lineas": len(texto.splitlines()), "caracteres": len(texto),
                           "tokens_aprox": tok, "tope": None, "medida": None, "dentro": None, "criterio": "sin orientación"}
    if ag in topes:
        out.update(tope=topes[ag], medida=tok, dentro=tok <= topes[ag], criterio=f"prompt íntegro ≤ tope de {ag}")
    elif ag in analistas and "analista" in topes:
        s10 = next((s for s in secs if s.numero == n10), None)
        quitar = "\n".join([f"## {s10.numero}. {s10.titulo}", *s10.lineas]) if s10 else ""
        sin10 = tokens_aprox(texto.replace(quitar, ""), ejecutor) if quitar else tok
        out.update(tope=topes["analista"], medida=sin10, dentro=sin10 <= topes["analista"],
                   criterio="prompt sin la §10 ≈ núcleo + kit V6 (aprox.) ≤ tope «analista»")
    return out


@dataclass
class Revision:
    archivo: str
    agente: str
    agente_id: str | None
    plantilla: bool
    estructura: dict[str, Any]
    recuento: list[dict[str, Any]]
    referencias: dict[str, Any]
    identificadores: dict[str, list[dict[str, Any]]]
    tamano: dict[str, Any]
    candidatas: int
    muestra: list[dict[str, Any]]


def revisar_prompt(p: Path, anexo: list[tuple[int, str]], semilla: str, topes: dict[str, int], analistas: set[str],
                   ejecutor: Path) -> Revision:
    texto = leer(p)
    secs = secciones(texto)
    n10 = numero_por_raiz(anexo, "conocimientos")
    n_met = numero_por_raiz(anexo, "metodología")
    sec10 = next((s for s in secs if s.numero == n10), None)
    nombre = nombre_agente(p.name)
    ag = agente_id(nombre, ejecutor)
    plantilla = not p.name.startswith(PREFIJO_PROMPT)
    cands = [] if plantilla else candidatas(texto, secs, n_met, n10)
    return Revision(
        archivo=p.name, agente=nombre, agente_id=ag, plantilla=plantilla,
        estructura=revisar_estructura(secs, anexo), recuento=recuento_seccion10(sec10),
        referencias=revisar_referencias(sec10, texto), identificadores=identificadores(texto),
        tamano=revisar_tamano(texto, secs, ag, topes, analistas, n10, ejecutor),
        candidatas=len(cands), muestra=muestra(cands, semilla, p.name))


# --------------------------------------------------------------------------------------------------------------------
# Informe
# --------------------------------------------------------------------------------------------------------------------
def _pct(a: int, b: int) -> str:
    return f"{100 * a / b:.1f} %" if b else "—"


def informe(revs: list[Revision], anexo: list[tuple[int, str]], fuentes: dict[str, str], semilla: str,
            contr: dict[str, Any] | None = None) -> str:
    prompts = [r for r in revs if not r.plantilla]
    plant = [r for r in revs if r.plantilla]
    L: list[str] = []
    a = L.append
    a("# T-187 · Informe de PB-51: conocimiento específico en los system prompts del Bloque A")
    a("")
    a("Generado por `.docs/scripts/revision_prompts_pb51.py` (sin red, determinista). No editar a mano: se regenera.")
    a("")
    a("| Entrada | Ruta |")
    a("| --- | --- |")
    for k, v in fuentes.items():
        a(f"| {k} | `{v}` |")
    a(f"| Semilla de la muestra | «{semilla}» |")
    a("")
    # Resumen
    completos = [r for r in prompts if r.estructura["completa"]]
    variantes = sum(1 for r in prompts for t in r.estructura["titulos"].values() if not t["coincide"])
    ent = [e for r in prompts for e in r.referencias["entradas"]]
    dois = [d for r in revs for d in r.identificadores["doi"]]
    tam = [r for r in prompts if r.tamano["dentro"] is not None]
    a("## Resumen")
    a("")
    a("| Comprobación | Resultado | Criterio |")
    a("| --- | --- | --- |")
    a(f"| Paso 1 · estructura del Anexo G ({len(anexo)} secciones) | {len(completos)} de {len(prompts)} prompts "
      f"({_pct(len(completos), len(prompts))}) | 100 % (PB-51) |")
    a(f"| Paso 1 · títulos que no comparten palabra con el del Anexo G | {variantes} títulos | se informa, no suspende "
      "(INC-T187-01) |")
    a(f"| Plantillas (fuera del denominador) | {len(plant)}: "
      + "; ".join(f"{r.archivo} con {len(r.estructura['secciones'])} secciones, faltan {r.estructura['faltan']}" for r in plant)
      + " | por diseño (su «Uso») |")
    a(f"| Paso 2 · prompts con sección {numero_por_raiz(anexo, 'conocimientos')} partida en subáreas | "
      f"{sum(1 for r in prompts if len([f for f in r.recuento if not f['subarea'].endswith('.0')]) > 0)} de {len(prompts)} | "
      "organizada por áreas (PB-51) |")
    sin_lista = [r.agente for r in prompts if not r.referencias["tiene_lista"]]
    a(f"| Prompts sin subárea de referencias canónicas en la sección {numero_por_raiz(anexo, 'conocimientos')} | "
      f"{len(sin_lista)}: {', '.join(sin_lista) or '—'} | referencias (autor, año, título) en la sección 10 (PB-51) |")
    a(f"| Referencias canónicas con autor y año reconocibles | {sum(e['autor_anio'] for e in ent)} de {len(ent)} entradas "
      f"({_pct(sum(e['autor_anio'] for e in ent), len(ent))}) | autor, año y título (PB-51) |")
    a(f"| … y con título en la propia entrada | {sum(e['titulo_en_la_entrada'] for e in ent)} de {len(ent)} "
      f"({_pct(sum(e['titulo_en_la_entrada'] for e in ent), len(ent))}) | estricto |")
    a(f"| … y con título en el prompt (otra cita del mismo autor y año) | {sum(e['titulo_en_el_prompt'] for e in ent)} de "
      f"{len(ent)} ({_pct(sum(e['titulo_en_el_prompt'] for e in ent), len(ent))}) | amplio `[PROPUESTO]` |")
    a(f"| DOI escritos en los prompts | {len(dois)} ({sum(not d['estructura_valida'] for d in dois)} con estructura "
      "inválida) | sin DOI inventados; la existencia no se comprueba (sin red) |")
    a(f"| Tamaños con orientación escrita | {sum(r.tamano['dentro'] for r in tam)} de {len(tam)} dentro del tope; "
      f"{len(prompts) - len(tam)} prompts sin orientación | `v6.tope_tokens_system` (INC-T187-01) |")
    a(f"| Paso 3 · afirmaciones en la muestra | {sum(len(r.muestra) for r in prompts)} "
      f"({MUESTRA_POR_PROMPT} por prompt; {sum(1 for r in prompts if len(r.muestra) < MUESTRA_POR_PROMPT)} prompts con "
      "menos candidatas) | ≥ 95 % correctas: lo juzgan revisores independientes |")
    if contr is not None:
        a(f"| Paso 3 · afirmaciones correctas | {contr['correctas']} de {contr['verificables']} verificables "
          f"(**{_pct1(contr['pct_verificables'])}**; {contr['erroneas']} ERRONEA, {contr['total']['NO_VERIFICABLE']} "
          f"NO_VERIFICABLE; {_pct1(contr['pct_total'])} sobre las {contr['n']}): "
          f"**{'supera' if contr['supera'] else 'no supera'}** | ≥ {UMBRAL_CORRECTAS} % sobre las verificables "
          "(PB-51; denominador de INC-T187-02) |")
    a("")
    # Paso 1
    a("## Paso 1 · Estructura del Anexo G")
    a("")
    a("Anexo G del Documento 0: " + " · ".join(f"{n}. {t}" for n, t in anexo) + ".")
    a("")
    a("| Prompt | Agente | Secciones | Faltan | Sobran | Repetidas | En orden | Completa | Títulos que no coinciden |")
    a("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in revs:
        e = r.estructura
        nc = ", ".join(f"{n} «{t['titulo']}»" for n, t in e["titulos"].items() if not t["coincide"]) or "—"
        a(f"| {r.agente}{' (plantilla)' if r.plantilla else ''} | {r.agente_id or '—'} | {len(e['secciones'])} | "
          f"{e['faltan'] or '—'} | {e['sobran'] or '—'} | {e['repetidas'] or '—'} | {'sí' if e['en_orden'] else 'no'} | "
          f"{'sí' if e['completa'] else 'no'} | {nc} |")
    a("")
    a("### Títulos por sección (coherencia entre prompts)")
    a("")
    a("| Sección | Anexo G | Títulos distintos en los prompts (n.º de prompts) |")
    a("| --- | --- | --- |")
    for n, t in anexo:
        cuenta: dict[str, int] = {}
        for r in revs:
            ti = r.estructura["titulos"].get(n)
            if ti:
                k = ti["titulo"] if ti["coincide"] else f"**{ti['titulo']}** (no coincide)"
                cuenta[k] = cuenta.get(k, 0) + 1
        a(f"| {n} | {t} | " + "; ".join(f"{k} ({v})" for k, v in sorted(cuenta.items(), key=lambda kv: (-kv[1], kv[0])))
          + " |")
    a("")
    # Paso 2
    n10 = numero_por_raiz(anexo, "conocimientos")
    a(f"## Paso 2 · Sección {n10}: recuento por subárea")
    a("")
    a("Criterios (detalle en `analisis-tecnico.md`): **definición** = elemento que empieza por un término en negrita "
      "seguido de «:», «=» o raya; **fórmula** = tramo de código con un operador o símbolo de cálculo, más cada «=»/«≈» "
      "con espacios fuera del código; **umbral** = comparador (≥, ≤, <, >, «al menos», «más de»…) seguido de una cifra; "
      "**trampa** = elemento de una subárea de trampas, errores o sesgos, o que nombra una trampa o un error típico; "
      "**referencia** = cita autor-año (en las subáreas de referencias canónicas, cada entrada). El inventario de "
      "competencias no se cuenta (resume lo anterior).")
    a("")
    a("| Prompt | Subáreas | Elementos | Definiciones | Fórmulas | Umbrales | Trampas | Referencias |")
    a("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in prompts:
        fs = [f for f in r.recuento if not f["excluida"]]
        a(f"| {r.agente} | {sum(1 for f in r.recuento if not f['subarea'].endswith('.0'))} | "
          f"{sum(f['elementos'] for f in fs)} | {sum(f['definiciones'] for f in fs)} | {sum(f['formulas'] for f in fs)} | "
          f"{sum(f['umbrales'] for f in fs)} | {sum(f['trampas'] for f in fs)} | {sum(f['referencias'] for f in fs)} |")
    tot = [f for r in prompts for f in r.recuento if not f["excluida"]]
    a(f"| **Total** | {sum(1 for r in prompts for f in r.recuento if not f['subarea'].endswith('.0'))} | "
      f"{sum(f['elementos'] for f in tot)} | {sum(f['definiciones'] for f in tot)} | {sum(f['formulas'] for f in tot)} | "
      f"{sum(f['umbrales'] for f in tot)} | {sum(f['trampas'] for f in tot)} | {sum(f['referencias'] for f in tot)} |")
    a("")
    for r in prompts:
        a(f"### {r.agente}")
        a("")
        a("| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |")
        a("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for f in r.recuento:
            nota = " (inventario, no se cuenta)" if f["excluida"] else (" (referencias canónicas)" if f["es_referencias"] else "")
            a(f"| {f['subarea']} | {f['titulo']}{nota} | {f['elementos']} | {f['definiciones']} | {f['formulas']} | "
              f"{f['umbrales']} | {f['trampas']} | {f['referencias']} |")
        a("")
    # Referencias
    a("## Referencias canónicas y DOI")
    a("")
    a("Cada entrada de las subáreas de referencias canónicas. Estricto: el título va en la propia entrada. Amplio "
      "`[PROPUESTO]`: otra cita del mismo primer autor y año, en el mismo prompt, lo lleva.")
    a("")
    a("| Prompt | Entradas | Con autor y año | Con título (estricto) | Con título (amplio) | Citas en el prompt | "
      "Citas sin título en ningún sitio del prompt |")
    a("| --- | --- | --- | --- | --- | --- | --- |")
    for r in prompts:
        e = r.referencias["entradas"]
        a(f"| {r.agente} | {len(e)} | {sum(x['autor_anio'] for x in e)} | {sum(x['titulo_en_la_entrada'] for x in e)} | "
          f"{sum(x['titulo_en_el_prompt'] for x in e)} | {r.referencias['citas_en_el_prompt']} | "
          f"{r.referencias['citas_sin_titulo_en_el_prompt']} |")
    a("")
    malas = [(r, x) for r in prompts for x in r.referencias["entradas"] if not x["autor_anio"]]
    a(f"### Entradas sin autor y año reconocibles ({len(malas)})")
    a("")
    if malas:
        a("| Prompt | Línea | Entrada |")
        a("| --- | --- | --- |")
        for r, x in malas:
            a(f"| {r.agente} | {x['linea']} | {x['entrada'].replace('|', '/')} |")
    else:
        a("Ninguna.")
    a("")
    a("### Identificadores")
    a("")
    ids = [(r, k, x) for r in revs for k in ("doi", "isbn", "issn") for x in r.identificadores[k]]
    if ids:
        a("| Prompt | Tipo | Identificador | Estructura o control válidos |")
        a("| --- | --- | --- | --- |")
        for r, k, x in ids:
            valido = x.get("estructura_valida", x.get("control_valido"))
            a(f"| {r.agente} | {k.upper()} | `{x[k]}` | {'sí' if valido else 'no'} |")
    else:
        a("Ningún prompt escribe un DOI, un ISBN ni un ISSN concretos (las menciones a «DOI» son instrucciones de método, "
          "como «no inventas referencias, DOI…»). Con el DOI se valida la estructura (no tiene dígito de control); con "
          "ISBN e ISSN, el dígito de control. Que un DOI exista no se puede comprobar sin red.")
    a("")
    # Tamaños
    a("## Tamaños")
    a("")
    a("Tokens aproximados con la función del ejecutor (`bloque_a/llm.py`, `_tokens_aprox`). Orientación: "
      "`v6.tope_tokens_system` de la configuración (`[PROPUESTO]`, T-101). AG-10 y AG-11 reciben en la V6 el prompt "
      "íntegro; los Analistas de tipo de activo reciben el núcleo y el kit (sin la §10 por defecto), que aquí se aproxima "
      "por el prompt sin la §10 (la medida exacta la vigila `tests/test_t101_v6.py`). El resto de papeles no tiene "
      "orientación escrita (INC-T187-01).")
    a("")
    a("| Prompt | Agente | Palabras | Líneas | Caracteres | Tokens aprox. | Medida | Tope | Dentro |")
    a("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in revs:
        tm = r.tamano
        d = "—" if tm["dentro"] is None else ("sí" if tm["dentro"] else "**no**")
        a(f"| {r.agente}{' (plantilla)' if r.plantilla else ''} | {r.agente_id or '—'} | {tm['palabras']} | {tm['lineas']} | "
          f"{tm['caracteres']} | {tm['tokens_aprox']} | {tm['medida'] if tm['medida'] is not None else '—'} | "
          f"{tm['tope'] if tm['tope'] is not None else '—'} | {d} |")
    a("")
    # Muestra
    a("## Paso 3 · Muestra")
    a("")
    a(f"Muestra aleatoria simple sin reemplazo de {MUESTRA_POR_PROMPT} afirmaciones por prompt entre las frases candidatas "
      "(con fórmula, umbral, definición, cita o cifra) de las secciones de método y de base de conocimientos; semilla "
      "por prompt «semilla|archivo». Texto exacto en `muestra_afirmaciones.json`, con los campos del veredicto vacíos: los "
      "veredictos van aparte, en `veredictos/` (contraste más abajo, si está).")
    a("")
    a("| Prompt | Candidatas | En la muestra | Con referencia citada en la frase | Con referencia en el elemento |")
    a("| --- | --- | --- | --- | --- |")
    for r in prompts:
        a(f"| {r.agente} | {r.candidatas} | {len(r.muestra)} | {sum(1 for m in r.muestra if m['referencia_citada'])} | "
          f"{sum(1 for m in r.muestra if m['referencia_del_elemento'])} |")
    a("")
    if contr is not None:
        L += informe_contraste(contr)
    return "\n".join(L) + "\n"


def codigo_prompt(r: Revision) -> str:
    """AG-xx del ejecutor; los submotores MC-xx no son agentes del ejecutor y se identifican por su código."""
    m = re.match(r"^(MC-\d+)\b", r.agente)
    return r.agente_id or (m.group(1) if m else re.sub(r"\W+", "-", r.agente).strip("-")[:24])


def afirmaciones(revs: list[Revision]) -> list[dict[str, Any]]:
    afs = []
    for r in revs:
        if r.plantilla:
            continue
        for i, m in enumerate(r.muestra, start=1):
            afs.append({"id": f"AF-{codigo_prompt(r)}-{i:02d}", "prompt": r.archivo, "agente": r.agente,
                        "agente_id": r.agente_id, **m, "veredicto": None, "nota": None, "revisor": None})
    ids = [a["id"] for a in afs]
    if len(ids) != len(set(ids)):
        raise ValueError("identificadores de afirmación repetidos")
    return afs


def json_muestra(revs: list[Revision], semilla: str, fuentes: dict[str, str]) -> str:
    afs = afirmaciones(revs)
    doc = {"ticket": "T-187", "prueba": "PB-51", "paso": 3, "semilla": semilla, "por_prompt": MUESTRA_POR_PROMPT,
           "fuentes": fuentes, "veredictos_validos": list(VEREDICTOS),
           "total": len(afs), "afirmaciones": afs}
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


# --------------------------------------------------------------------------------------------------------------------
# Paso 3 · contraste de los revisores
# --------------------------------------------------------------------------------------------------------------------
class ContrasteInvalido(ValueError):
    """Los veredictos no casan con la muestra o no cumplen el formato: el script termina con 2."""


def _cuenta(vs: list[str]) -> dict[str, int]:
    return {v: sum(1 for x in vs if x == v) for v in VEREDICTOS}


def porcentajes(c: dict[str, int]) -> dict[str, Any]:
    """Correctas sobre las verificables (CORRECTA + ERRONEA, criterio de INC-T187-02) y sobre todas."""
    verif = c["CORRECTA"] + c["ERRONEA"]
    total = verif + c["NO_VERIFICABLE"]
    return {"correctas": c["CORRECTA"], "erroneas": c["ERRONEA"], "verificables": verif, "todas": total,
            "pct_verificables": 100 * c["CORRECTA"] / verif if verif else None,
            "pct_total": 100 * c["CORRECTA"] / total if total else None,
            "supera": bool(verif) and 100 * c["CORRECTA"] >= UMBRAL_CORRECTAS * verif}


def _texto(x: Any) -> bool:
    """Un texto con al menos una letra o cifra (QA r01, H-05: «—» o «  » no valen)."""
    return isinstance(x, str) and re.search(r"\w", x) is not None


def _leer_json(p: Path) -> Any:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:      # QA r01, H-05: sin traza
        raise ContrasteInvalido(f"{p.name}: no se puede leer como JSON en UTF-8 ({type(e).__name__}: {e})"[:300]) from e


def fuente(nota: str) -> str:
    return next((nombre for nombre, rx in FUENTES if rx.search(nota)), SIN_FUENTE)


def leer_lotes(carpeta: Path) -> list[dict[str, Any]]:
    archivos = sorted(carpeta.glob("lote_*.json"), key=lambda p: (len(p.name), p.name))
    if not archivos:
        raise ContrasteInvalido(f"no hay lotes de veredictos en {carpeta}")
    lotes = []
    for p in archivos:
        d = _leer_json(p)
        if not isinstance(d, dict) or not isinstance(d.get("veredictos"), list) or not _texto(d.get("revisor")):
            raise ContrasteInvalido(f"{p.name}: se esperan «revisor» (no vacío) y la lista «veredictos»")
        for v in d["veredictos"]:
            if not isinstance(v, dict) or not isinstance(v.get("id"), str):
                raise ContrasteInvalido(f"{p.name}: un veredicto sin «id»: {v!r}"[:200])
        lotes.append({"archivo": p.name, "lote": d.get("lote", p.stem), "revisor": d["revisor"], "veredictos": d["veredictos"]})
    return lotes


def contraste(afs: list[dict[str, Any]], lotes: list[dict[str, Any]], comentario: dict[str, Any]) -> dict[str, Any]:
    """Valida los veredictos contra la muestra (falla cerrado) y los cuenta por lote, por prompt y en total."""
    por_id: dict[str, dict[str, Any]] = {}
    lote_de: dict[str, Any] = {}
    for lt in lotes:
        for v in lt["veredictos"]:
            i = v["id"]
            if i in por_id:
                raise ContrasteInvalido(f"id duplicado: {i} ({lote_de[i]} y {lt['archivo']})")
            if v.get("veredicto") not in VEREDICTOS:
                raise ContrasteInvalido(f"{i}: veredicto desconocido {v.get('veredicto')!r}")
            nota = v.get("nota")
            if not _texto(nota):
                raise ContrasteInvalido(f"{i}: sin nota (hace falta al menos una letra o cifra)")
            if len(nota.split()) > MAX_PALABRAS_NOTA:
                raise ContrasteInvalido(f"{i}: la nota tiene {len(nota.split())} palabras (máximo {MAX_PALABRAS_NOTA})")
            por_id[i] = v
            lote_de[i] = lt["archivo"]
    ids = [a["id"] for a in afs]
    faltan = [i for i in ids if i not in por_id]
    sobran = sorted(set(por_id) - set(ids))
    if faltan or sobran:
        raise ContrasteInvalido(f"los veredictos no casan con la muestra: faltan {faltan[:10]}, sobran {sobran[:10]}")
    veredicto = {i: str(por_id[i]["veredicto"]) for i in ids}
    erroneas = [i for i in ids if veredicto[i] == "ERRONEA"]
    erratas = comentario.get("erratas")
    dudosas = comentario.get("dudosas")
    discutibles = comentario.get("discutibles")
    sens = comentario.get("sensibilidad")
    if not isinstance(erratas, dict) or not isinstance(dudosas, dict) or not isinstance(discutibles, list) \
            or not isinstance(sens, dict):
        raise ContrasteInvalido("el comentario necesita «erratas», «dudosas», «discutibles» y «sensibilidad»")
    if sorted(erratas) != sorted(erroneas):
        raise ContrasteInvalido(f"las erratas del comentario no son las ERRONEA: {sorted(erratas)} frente a {erroneas}")
    if any(not isinstance(e, dict) or not _texto(e.get("error")) or not _texto(e.get("correccion")) for e in erratas.values()):
        raise ContrasteInvalido("cada errata necesita «error» y «correccion»")
    if any(veredicto.get(i) != "CORRECTA" for i in dudosas):
        raise ContrasteInvalido(f"un caso dudoso no es CORRECTA: {sorted(dudosas)}")
    con_matiz = sorted(i for i in ids if veredicto[i] == "CORRECTA" and RE_MATIZ.search(str(por_id[i]["nota"])))
    if sorted(dudosas) != con_matiz:
        raise ContrasteInvalido(f"los casos dudosos no siguen el criterio (CORRECTA con matiz en la nota): "
                                f"{sorted(dudosas)} frente a {con_matiz}")
    if any(not _texto(m) for m in dudosas.values()):
        raise ContrasteInvalido("cada caso dudoso necesita su «matiz» (un texto)")
    # «dudosas» es {id: matiz} (como lo leen los scripts de la QA r01); su cita, en «dudosas_cita_nota» {id: cita}.
    citas_d = comentario.get("dudosas_cita_nota")
    if not isinstance(citas_d, dict):
        raise ContrasteInvalido("el comentario necesita «dudosas_cita_nota»")
    citas = [(i, e.get("cita_nota")) for i, e in erratas.items()] + [(i, citas_d.get(i)) for i in dudosas]
    for i, cita in citas:      # QA r01, H-03: lo que se atribuye al revisor está en su nota
        if not _texto(cita) or str(cita) not in str(por_id[i]["nota"]):
            raise ContrasteInvalido(f"{i}: «cita_nota» no es un fragmento literal de la nota del revisor: {cita!r}"[:300])
        if sum(1 for w in str(cita).split() if re.search(r"\w", w)) < MIN_PALABRAS_CITA:
            raise ContrasteInvalido(f"{i}: «cita_nota» tiene menos de {MIN_PALABRAS_CITA} palabras: {cita!r}"[:300])
    if any(not isinstance(i, str) for i in discutibles):
        raise ContrasteInvalido(f"«discutibles» tiene que ser una lista de ids: {discutibles!r}"[:300])
    if not set(discutibles) <= set(erroneas):
        raise ContrasteInvalido(f"una discutible no es ERRONEA: {discutibles}")
    if any(not RE_DISCUTIBLE.search(str(por_id[i]["nota"])) for i in discutibles):
        raise ContrasteInvalido(f"una discutible cuya nota no lo dice: {discutibles}")
    sens_ids = sens.get("ids")
    if not isinstance(sens_ids, list) or any(not isinstance(i, str) for i in sens_ids) or not _texto(sens.get("motivo")):
        raise ContrasteInvalido("«sensibilidad» necesita «ids» (lista de ids) y «motivo»")
    if not set(sens_ids) <= set(erroneas):
        raise ContrasteInvalido(f"un caso de la sensibilidad no es ERRONEA: {sens_ids}")
    total = _cuenta(list(veredicto.values()))
    por_lote = [{"archivo": lt["archivo"], "lote": lt["lote"], "revisor": lt["revisor"],
                 **_cuenta([str(v["veredicto"]) for v in lt["veredictos"]]),
                 "prompts": sorted({codigo for codigo in (a["id"].rsplit("-", 1)[0][3:] for a in afs
                                                          if lote_de[a["id"]] == lt["archivo"])})}
                for lt in lotes]
    por_prompt: dict[str, dict[str, Any]] = {}
    for a in afs:
        f = por_prompt.setdefault(a["prompt"], {"agente": a["agente"], "codigo": a["id"].rsplit("-", 1)[0][3:],
                                                "lotes": [], "vs": []})
        f["vs"].append(veredicto[a["id"]])
        if lote_de[a["id"]] not in f["lotes"]:
            f["lotes"].append(lote_de[a["id"]])
    filas = [{"prompt": k, "agente": f["agente"], "codigo": f["codigo"], "lotes": f["lotes"], **_cuenta(f["vs"]),
              "verificables": sum(1 for x in f["vs"] if x != "NO_VERIFICABLE")} for k, f in por_prompt.items()]
    cortos = sorted((f for f in filas if f["verificables"] < MUESTRA_POR_PROMPT), key=lambda f: (f["verificables"], f["agente"]))
    por_fuente = {(v, fu): 0 for v in VEREDICTOS for fu in [*(n for n, _ in FUENTES), SIN_FUENTE]}
    for i in ids:
        por_fuente[(veredicto[i], fuente(str(por_id[i]["nota"])))] += 1
    d = [i for i in ids if i in set(sens_ids) | set(discutibles)]
    como_correctas = dict(total, CORRECTA=total["CORRECTA"] + len(d), ERRONEA=total["ERRONEA"] - len(d))
    sin_ellas = dict(total, ERRONEA=total["ERRONEA"] - len(d))
    por_af = {a["id"]: a for a in afs}
    return {"total": total, "n": len(ids), **porcentajes(total), "por_lote": por_lote, "por_prompt": filas,
            "erratas": [{**por_af[i], "veredicto": veredicto[i], "nota": por_id[i]["nota"], "lote": lote_de[i],
                         "error": erratas[i]["error"], "correccion": erratas[i]["correccion"],
                         "cita": erratas[i]["cita_nota"]} for i in erroneas],
            "dudosas": [{**por_af[i], "nota": por_id[i]["nota"], "lote": lote_de[i], "matiz": dudosas[i], "cita": citas_d[i]}
                        for i in ids if i in dudosas],
            "cortos": cortos, "por_fuente": por_fuente,
            "discutibles": [i for i in ids if i in set(discutibles)], "sensibilidad_ids": d,
            "motivo_sensibilidad": str(sens["motivo"]), "criterio_dudosas": str(comentario.get("criterio_dudosas") or ""),
            "sensibilidad": {"como_correctas": porcentajes(como_correctas), "sin_ellas": porcentajes(sin_ellas)}}


def leer_contraste(carpeta: Path, afs: list[dict[str, Any]]) -> dict[str, Any]:
    lotes = leer_lotes(carpeta)
    p = carpeta / "comentario.json"
    if not p.is_file():
        raise ContrasteInvalido(f"falta {p.name} en {carpeta}")
    comentario = _leer_json(p)
    if not isinstance(comentario, dict):
        raise ContrasteInvalido(f"{p.name}: se espera un objeto")
    return contraste(afs, lotes, comentario)


def _celda(t: str) -> str:
    return nfc(t).replace("\n", " ").replace("|", "\\|")


def _pct1(x: float | None) -> str:
    return "—" if x is None else f"{x:.1f} %"


def informe_contraste(c: dict[str, Any]) -> list[str]:
    L: list[str] = []
    a = L.append
    t = c["total"]
    a("## Paso 3 · Contraste de la muestra")
    a("")
    a("Veredictos de cuatro revisores independientes (`veredictos/lote_*.json`: CORRECTA, ERRONEA o NO_VERIFICABLE, con "
      "una nota de hasta 40 palabras y la fuente consultada) y comentario del contraste (`veredictos/comentario.json`). "
      "Denominador (INC-T187-02 `[PROPUESTO]`): las afirmaciones verificables (CORRECTA + ERRONEA); las NO_VERIFICABLE "
      "son reglas internas del sistema que no se pueden contrastar con la literatura, y se declaran aparte con la otra "
      f"cifra. Criterio de PB-51: ≥ {UMBRAL_CORRECTAS} % correctas.")
    a("")
    a("| Recuento | Valor |")
    a("| --- | --- |")
    a(f"| Afirmaciones juzgadas | {c['n']} |")
    a(f"| CORRECTA | {t['CORRECTA']} |")
    a(f"| ERRONEA | {t['ERRONEA']} |")
    a(f"| NO_VERIFICABLE | {t['NO_VERIFICABLE']} |")
    a(f"| Correctas sobre las verificables ({c['verificables']}) | **{_pct1(c['pct_verificables'])}** |")
    a(f"| Correctas sobre todas ({c['n']}) | {_pct1(c['pct_total'])} |")
    a(f"| Veredicto (≥ {UMBRAL_CORRECTAS} % sobre las verificables) | **{'SUPERA' if c['supera'] else 'NO SUPERA'}** |")
    a("")
    a("### Por lote")
    a("")
    a("| Lote | Revisor | Prompts | CORRECTA | ERRONEA | NO_VERIFICABLE | % sobre verificables |")
    a("| --- | --- | --- | --- | --- | --- | --- |")
    for lt in c["por_lote"]:
        a(f"| {lt['lote']} | {_celda(lt['revisor'])} | {', '.join(lt['prompts'])} | {lt['CORRECTA']} | {lt['ERRONEA']} | "
          f"{lt['NO_VERIFICABLE']} | {_pct1(porcentajes(lt)['pct_verificables'])} |")
    a("")
    a("### Por prompt")
    a("")
    a("| Prompt | Código | Lote | CORRECTA | ERRONEA | NO_VERIFICABLE | Verificables | % sobre verificables |")
    a("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for f in c["por_prompt"]:
        a(f"| {f['agente']} | {f['codigo']} | {', '.join(x.removeprefix('lote_').removesuffix('.json') for x in f['lotes'])} | "
          f"{f['CORRECTA']} | {f['ERRONEA']} | {f['NO_VERIFICABLE']} | {f['verificables']} | "
          f"{_pct1(porcentajes(f)['pct_verificables'])} |")
    a("")
    cortos = c["cortos"]
    a(f"El paso 3 pide {MUESTRA_POR_PROMPT} afirmaciones técnicas por prompt. Las NO_VERIFICABLE no lo son, así que "
      f"{len(cortos)} de {len(c['por_prompt'])} prompts quedan por debajo de {MUESTRA_POR_PROMPT} verificables"
      + (": " + "; ".join(f"{f['agente']} {f['verificables']}" for f in cortos) if cortos else "")
      + ". Se declara (INC-T187-02); no hay muestra de reposición.")
    a("")
    a("### Por fuente declarada en la nota")
    a("")
    a("Clasificación mecánica de la nota: «búsqueda web» (no «sin búsqueda web») o «Web:»; «conocimiento propio» "
      "(de memoria, sin consultar la referencia); cálculo a mano; si no, sin fuente declarada.")
    a("")
    nombres = [*(n for n, _ in FUENTES), SIN_FUENTE]
    a("| Veredicto | " + " | ".join(nombres) + " |")
    a("| --- | " + " | ".join("---" for _ in nombres) + " |")
    for v in VEREDICTOS:
        a(f"| {v} | " + " | ".join(str(c["por_fuente"][(v, n)]) for n in nombres) + " |")
    a("")
    a(f"### Afirmaciones ERRONEA ({len(c['erratas'])})")
    a("")
    a("Hallazgos de los prompts: no se corrigen aquí (corpus congelado); quedan para la próxima entrega del corpus "
      "(INC-T187-03).")
    a("")
    a("| Id | Prompt (línea) | Frase | Error | Corrección (de la nota del revisor) | Cita de la nota |")
    a("| --- | --- | --- | --- | --- | --- |")
    for e in c["erratas"]:
        a(f"| {e['id']} | {e['agente']} ({e['linea']}) | {_celda(e['texto'])} | {_celda(e['error'])} | "
          f"{_celda(e['correccion'])} | {_celda(e['cita'])} |")
    a("")
    a(f"### Casos dudosos marcados CORRECTA con matiz ({len(c['dudosas'])})")
    a("")
    a("Criterio: " + (_celda(c["criterio_dudosas"]) or "CORRECTA cuya nota trae un matiz explícito") + " El script exige "
      "que el comentario liste exactamente esas.")
    a("")
    a("| Id | Prompt (línea) | Matiz | Cita de la nota | Nota del revisor |")
    a("| --- | --- | --- | --- | --- |")
    for e in c["dudosas"]:
        a(f"| {e['id']} | {e['agente']} ({e['linea']}) | {_celda(e['matiz'])} | {_celda(e['cita'])} | {_celda(e['nota'])} |")
    a("")
    a("### Sensibilidad")
    a("")
    s = c["sensibilidad"]
    a(f"Casos: {', '.join(c['sensibilidad_ids']) or '—'}. {_celda(c['motivo_sensibilidad'])} ERRONEA que un revisor llama "
      f"discutibles en su nota: {', '.join(c['discutibles']) or 'ninguna'}.")
    a("")
    a("| Supuesto | CORRECTA | ERRONEA | Verificables | % sobre verificables | Veredicto |")
    a("| --- | --- | --- | --- | --- | --- |")
    for nombre, x in (("Tal como las juzgan los revisores", porcentajes(c["total"])),
                      ("Esos casos cuentan como correctas", s["como_correctas"]),
                      ("Esos casos se quitan", s["sin_ellas"])):
        a(f"| {nombre} | {x['correctas']} | {x['erroneas']} | {x['verificables']} | {_pct1(x['pct_verificables'])} | "
          f"{'SUPERA' if x['supera'] else 'NO SUPERA'} |")
    cambia = len({c["supera"], s["como_correctas"]["supera"], s["sin_ellas"]["supera"]}) > 1
    a("")
    a(f"Entre los tres supuestos el veredicto {'**cambia**' if cambia else 'no cambia'}.")
    a("")
    return L


# --------------------------------------------------------------------------------------------------------------------
class EntradaFaltante(ValueError):
    """Falta el Documento 0 (o hay más de uno), los prompts, la configuración o su clave de topes: termina con 2."""


def revisar(raiz: Path, semilla: str = SEMILLA_POR_DEFECTO, ejecutor_arg: Path | None = None
            ) -> tuple[list[Revision], list[tuple[int, str]], dict[str, str]]:
    """Revisión de todos los prompts de `raiz` (pasos 1 y 2 y la muestra del paso 3), sin escribir nada."""
    raiz = raiz.resolve()
    dir_p = raiz / "bloque_a" / "02_System_prompts"
    d0s = sorted((raiz / "bloque_a" / "01_Gobernanza").glob("Documento 0 - Protocolo maestro del Bloque A - *.md"))
    cfg = raiz / "bloque_a" / "11_Ejecutor" / "config" / "por_defecto.yaml"
    ejecutor = (ejecutor_arg or raiz / "bloque_a" / "11_Ejecutor").resolve()
    archivos = sorted(dir_p.glob("*.md"), key=lambda p: nfc(p.name))
    if len(d0s) != 1 or not archivos or not cfg.is_file():
        raise EntradaFaltante(f"falta una entrada: Documento 0 {[p.name for p in d0s]}, {len(archivos)} prompts, "
                              f"config {cfg.is_file()}")
    import yaml
    topes_raw = (yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}).get("v6", {}).get("tope_tokens_system")
    if not isinstance(topes_raw, dict) or not topes_raw:
        raise EntradaFaltante("falta v6.tope_tokens_system en la configuración")
    topes = {str(k): int(v) for k, v in topes_raw.items()}
    anexo = leer_anexo_g(leer(d0s[0]))
    analistas = analistas_tipo(ejecutor)
    revs = [revisar_prompt(p, anexo, semilla, topes, analistas, ejecutor) for p in archivos]
    fuentes = {"Documento 0 (Anexo G)": str(d0s[0].relative_to(raiz)), "Prompts": str(dir_p.relative_to(raiz)),
               "Configuración (topes)": str(cfg.relative_to(raiz)),
               "Huella de los prompts (SHA-256 de nombres y contenidos)": _huella(archivos)}
    return revs, anexo, fuentes


def principal(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", type=Path, default=RAIZ_POR_DEFECTO)
    ap.add_argument("--salida", type=Path, default=SALIDA_POR_DEFECTO)
    ap.add_argument("--semilla", default=SEMILLA_POR_DEFECTO)
    ap.add_argument("--ejecutor", type=Path, default=None,
                    help="carpeta del ejecutor de la que se importan los nombres de agente y la aproximación de tokens "
                         "(por defecto, la de --raiz)")
    ap.add_argument("--veredictos", type=Path, default=None,
                    help="carpeta de los lotes de veredictos del paso 3 (por defecto, «veredictos» junto a la salida; "
                         "si no existe, el informe no lleva el contraste)")
    ap.add_argument("--comprobar", action="store_true")
    args = ap.parse_args(argv)
    try:
        revs, anexo, fuentes = revisar(args.raiz, args.semilla, args.ejecutor)
    except EntradaFaltante as e:
        print(e, file=sys.stderr)
        return 2
    dir_v = args.veredictos or args.salida / "veredictos"
    contr = None
    if args.veredictos is not None or dir_v.is_dir():
        try:
            contr = leer_contraste(dir_v, afirmaciones(revs))
        except ContrasteInvalido as e:
            print(f"veredictos no válidos: {e}", file=sys.stderr)
            return 2
    salidas = {args.salida / "informe_pb51.md": informe(revs, anexo, fuentes, args.semilla, contr),
               args.salida / "muestra_afirmaciones.json": json_muestra(revs, args.semilla, fuentes)}
    if args.comprobar:
        dif = [p.name for p, t in salidas.items() if not p.is_file() or p.read_text(encoding="utf-8") != t]
        print("igual" if not dif else f"difiere: {dif}")
        return 1 if dif else 0
    args.salida.mkdir(parents=True, exist_ok=True)
    for p, t in salidas.items():
        p.write_text(t, encoding="utf-8")
    prompts = [r for r in revs if not r.plantilla]
    print(f"{len(prompts)} prompts ({sum(r.estructura['completa'] for r in prompts)} con estructura completa), "
          f"{sum(len(r.muestra) for r in prompts)} afirmaciones en la muestra"
          + ("" if contr is None else f"; contraste: {contr['correctas']}/{contr['verificables']} verificables correctas "
             f"({_pct1(contr['pct_verificables'])}), {'supera' if contr['supera'] else 'no supera'}"))
    return 0


def _huella(archivos: list[Path]) -> str:
    h = hashlib.sha256()
    for p in archivos:
        h.update(nfc(p.name).encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


if __name__ == "__main__":
    sys.exit(principal())
