"""Registro de experimentos (T-99; decisión 5 de la tanda 1, D-53 propuesta): toda prueba que pueda cambiar cómo decide o cuánto
cuesta el robot se prerregistra y se sella ANTES de ejecutarse, y cuentan todos sus intentos, también los fallidos.

Fichero de solo anexar, una línea JSON por anotación, encadenada por huellas (`_seq`, `_hash_prev`, `_hash`): reescribir o
quitar una línea rompe la cadena y `verificar()` lo dice. Tres tipos de anotación:
- PRERREGISTRO: hipótesis, objeto, métrica, datos, fechas, semilla, criterio de éxito, máximo de variantes y su huella;
- INTENTO: una ejecución de una variante del experimento (cuenta aunque no llegue a dar resultado);
- RESULTADO: lo que dio un intento, con su veredicto («mejor», «peor», «todavía no se sabe» o «fallido»).
No hay intento sin prerregistro ni resultado sin intento. El formato definitivo lo fijará el contrato CT-G-24 (borrador en
`.docs/diseno/contratos/`) cuando se cierre el diseño de J; hasta entonces, cada anotación se valida con sus reglas antes de
escribirla y al leerla.

Decisiones de la ronda r02 (QA r01), `[PROPUESTO]` en la fila T-99 de la deuda (las decide el operador):
- **Regla de adopción.** De cada variante cuenta su PRIMER resultado que no sea «fallido». Repetirla no puede hacerla adoptable:
  si un resultado posterior de la misma variante dice otra cosa que «mejor», la variante queda «contradictoria» y no es
  adoptable. Un resultado solo sirve para adoptar un cambio si además el intento empezó después del prerregistro (por instante,
  no por texto) y la variante está dentro del máximo prerregistrado.
- **Ancla.** La cadena no tiene secreto: quien reescribe el fichero puede recalcularla entera, y quitar las últimas líneas deja
  una cadena válida. El ancla es git: si el fichero está en el repositorio, lo que hay en HEAD tiene que ser un prefijo exacto
  del fichero (solo crece). Lo que aún no se ha subido no tiene ancla: se sube el registro al terminar cada experimento.
- **Sello.** Junto al registro va «<registro>.sello» con el número y la huella de la última anotación, que se escribe con cada
  anotación bajo el cerrojo. Quitar las últimas líneas (o un corte a mitad de escritura) deja la cadena válida, pero no casa con
  el sello. Quien reescribe a propósito puede rehacer también el sello: contra eso solo vale el ancla de git.
- **Un solo escritor por fichero.** Un cerrojo del sistema (`fcntl`) impide dos escrituras a la vez en la misma máquina. Dos
  máquinas que anotan el mismo fichero en ramas distintas no se pueden fusionar sin romper la cadena (y `verificar` lo detecta):
  cada agente anota en su propio registro (`--registro`).

Uso (desde la raíz; `--registro` va delante o detrás de la orden):
  python3 .docs/scripts/registro_experimentos.py [--registro R] prerregistrar <prerregistro.json> [--autor A]
  python3 .docs/scripts/registro_experimentos.py [--registro R] intento <EXP-…> --variante V
  python3 .docs/scripts/registro_experimentos.py [--registro R] resultado <EXP-…> <n> <veredicto> [--detalle JSON]
  python3 .docs/scripts/registro_experimentos.py [--registro R] ver [<EXP-…>]
  python3 .docs/scripts/registro_experimentos.py [--registro R] verificar
Solo biblioteca estándar.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from datetime import UTC, date, datetime
from pathlib import Path

try:
    import fcntl
except ImportError:   # pragma: no cover - fuera de POSIX no hay cerrojo: se dice al escribir
    fcntl = None

RAIZ = Path(__file__).resolve().parents[2]
AGENTE = os.environ.get("RI_AGENTE", "claude")   # un registro por agente (H-17): Astra exporta RI_AGENTE=astra
if not re.fullmatch(r"[a-z0-9_-]{1,32}", AGENTE):
    AGENTE = "claude"
REGISTRO_DEFECTO = RAIZ / ".docs" / "experimentos" / f"registro_{AGENTE}.jsonl"
VERSION = "0.3.0"   # 0.3.0 (T-99 r03): ancla en todo el historial de git, sello tolerante a un corte, cerrojo con espera y
                    # lectores, intentos pendientes en la regla de adopción, búsqueda o prerregistro atómicos
CERROJO_ESPERA_S = 30   # espera máxima del cerrojo ([PROPUESTO] en la fila T-99 de la deuda)
OBJETOS = ("RECORTE", "INSTRUCCION", "MODELO", "ESTRATEGIA", "PARAMETRO", "BLOQUE", "OTRO")
VEREDICTOS = ("mejor", "peor", "todavía no se sabe", "fallido")
CAMPOS_PRERREGISTRO = ("hipotesis", "objeto", "metrica", "datos", "desde", "hasta", "semilla", "criterio_exito", "max_variantes")
TIPOS = ("PRERREGISTRO", "INTENTO", "RESULTADO")
# Topes del borrador de CT-G-24 ([PROPUESTO] en la fila T-99 de la deuda): máximo de variantes y textos con un mínimo de palabras.
MAX_VARIANTES_TOPE = 1000
MIN_TEXTO = 10
MAX_EXP_POR_ANIO = 9999   # EXP-AAAA-NNNN: cuatro cifras
RE_EXP = re.compile(r"^EXP-\d{4}-\d{4}\Z")
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")
RE_INSTANTE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
RE_HASH = re.compile(r"^[0-9a-f]{64}\Z")
RE_VERSION = re.compile(r"^\d+\.\d+\.\d+\Z")
CERO = "0" * 64
CAMPOS = {
    "PRERREGISTRO": {"tipo", "exp_id", "autor", "creado_en", "version_registro", "contenido", "huella_prerregistro"},
    "INTENTO": {"tipo", "exp_id", "n", "variante", "inicio", "huella_prerregistro", "dentro_del_maximo"},
    "RESULTADO": {"tipo", "exp_id", "n", "veredicto", "detalle", "registrado_en"},
}
CADENA = {"_seq", "_hash_prev", "_hash"}


class RegistroError(ValueError):
    """Anotación que el registro no admite, o registro dañado. Nunca se escribe nada en ese caso."""


def huella(obj) -> str:
    try:
        txt = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as e:   # NaN, infinitos u objetos que no son JSON: no se sella lo que no se puede leer
        raise RegistroError(f"no es JSON estándar: {e}") from e
    try:
        return hashlib.sha256(txt.encode("utf-8")).hexdigest()
    except UnicodeEncodeError as e:   # un sustituto suelto (H-20)
        raise RegistroError(f"tiene un carácter que no es UTF-8 válido: {e}") from e


def _ahora() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _instante(txt, campo: str) -> datetime:
    """Instante ISO 8601 con zona (como pide CT-G-24), en UTC. Se compara por instante, nunca por texto (H-07)."""
    if not isinstance(txt, str) or not RE_INSTANTE.match(txt):
        raise RegistroError(f"«{campo}» tiene que ser un instante ISO con zona (AAAA-MM-DDThh:mm:ss+hh:mm o Z): {txt!r}")
    try:
        return datetime.fromisoformat(txt).astimezone(UTC)
    except ValueError as e:
        raise RegistroError(f"«{campo}» no es un instante posible: {txt!r}") from e


def _fecha(txt, campo: str) -> date:
    if not isinstance(txt, str) or not RE_FECHA.match(txt):
        raise RegistroError(f"«{campo}» tiene que ser una fecha AAAA-MM-DD: {txt!r}")
    try:
        return date.fromisoformat(txt)
    except ValueError as e:
        raise RegistroError(f"«{campo}» no es una fecha posible: {txt!r}") from e


def _entero(v, campo: str, minimo: int | None = None, maximo: int | None = None) -> int:
    if isinstance(v, bool) or not isinstance(v, int) or (minimo is not None and v < minimo) or (maximo is not None and v > maximo):
        rango = "" if minimo is None else f" entre {minimo} y {maximo}" if maximo is not None else f" mayor o igual que {minimo}"
        raise RegistroError(f"«{campo}» tiene que ser un entero{rango}: {v!r}")
    return v


def _texto(v, campo: str, minimo: int = 1) -> str:
    if not isinstance(v, str) or len(v.strip()) < minimo:
        raise RegistroError(f"«{campo}» tiene que ser un texto de {minimo} carácter(es) o más")
    return v


def _variante(v) -> str:
    """Una variante es un texto no vacío, normalizado a NFC: «única» en NFC y en NFD es la misma (H-09)."""
    if not isinstance(v, str) or not v.strip():
        raise RegistroError(f"la variante tiene que ser un texto no vacío: {v!r}")
    return unicodedata.normalize("NFC", v)


def _validar_contenido(c) -> None:
    if not isinstance(c, dict):
        raise RegistroError("el prerregistro tiene que ser un objeto JSON")
    falta = [k for k in CAMPOS_PRERREGISTRO if k not in c]
    if falta:
        raise RegistroError(f"al prerregistro le faltan {falta}")
    if c["objeto"] not in OBJETOS:
        raise RegistroError(f"objeto {c['objeto']!r} no válido ({', '.join(OBJETOS)})")
    for k in ("hipotesis", "metrica", "criterio_exito"):
        _texto(c[k], k, MIN_TEXTO)
    _texto(c["datos"], "datos")
    _entero(c["max_variantes"], "max_variantes", 1, MAX_VARIANTES_TOPE)
    _entero(c["semilla"], "semilla")
    if _fecha(c["desde"], "desde") > _fecha(c["hasta"], "hasta"):
        raise RegistroError("«desde» no puede ser posterior a «hasta»")


def validar_anotacion(e) -> None:
    """Forma de una anotación según el borrador de CT-G-24 (falla cerrado, H-05 y H-06). La semántica la mira `anotaciones()`."""
    if not isinstance(e, dict) or e.get("tipo") not in TIPOS:
        raise RegistroError(f"anotación sin un tipo válido ({', '.join(TIPOS)}): {str(e)[:80]}")
    tipo = e["tipo"]
    claves = set(e) - CADENA
    if claves != CAMPOS[tipo]:
        raise RegistroError(f"la anotación {tipo} no tiene la forma de CT-G-24: sobran {sorted(claves - CAMPOS[tipo])}, "
                            f"faltan {sorted(CAMPOS[tipo] - claves)}")
    if not isinstance(e["exp_id"], str) or not RE_EXP.match(e["exp_id"]):
        raise RegistroError(f"exp_id mal formado: {e['exp_id']!r}")
    if tipo == "PRERREGISTRO":
        _texto(e["autor"], "autor")
        _instante(e["creado_en"], "creado_en")
        if not isinstance(e["version_registro"], str) or not RE_VERSION.match(e["version_registro"]):
            raise RegistroError("version_registro mal formada")
        _validar_contenido(e["contenido"])
        if e["huella_prerregistro"] != huella(e["contenido"]):
            raise RegistroError(f"la huella del prerregistro {e['exp_id']} no es la de su contenido: se cambió después")
    elif tipo == "INTENTO":
        _entero(e["n"], "n", 1)
        if not isinstance(e["variante"], str) or not e["variante"].strip():
            raise RegistroError("variante vacía")
        _instante(e["inicio"], "inicio")
        if not isinstance(e["huella_prerregistro"], str) or not RE_HASH.match(e["huella_prerregistro"]):
            raise RegistroError("huella_prerregistro mal formada")
        if not isinstance(e["dentro_del_maximo"], bool):
            raise RegistroError("dentro_del_maximo tiene que ser verdadero o falso")
    else:
        _entero(e["n"], "n", 1)
        if e["veredicto"] not in VEREDICTOS:
            raise RegistroError(f"veredicto {e['veredicto']!r} no válido ({', '.join(VEREDICTOS)})")
        if not isinstance(e["detalle"], dict):
            raise RegistroError("«detalle» tiene que ser un objeto JSON")
        _instante(e["registrado_en"], "registrado_en")
    if CADENA <= set(e):
        _entero(e["_seq"], "_seq", 1)
        for k in ("_hash", "_hash_prev"):
            if not isinstance(e[k], str) or not RE_HASH.match(e[k]):
                raise RegistroError(f"{k} mal formado")


def _linea(e: dict) -> str:
    """Una anotación en una línea. Sin NaN (no es JSON) y con los separadores de línea Unicode escapados (H-04): la lectura
    parte solo por «\\n», y U+2028, U+2029 y U+0085 no pueden cortar una anotación."""
    try:
        txt = json.dumps(e, ensure_ascii=False, sort_keys=True, allow_nan=False)
    except (TypeError, ValueError) as ex:
        raise RegistroError(f"la anotación no se puede escribir como JSON estándar: {ex}") from ex
    txt = txt.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029").replace("\u0085", "\\u0085")
    try:
        txt.encode("utf-8")
    except UnicodeEncodeError as ex:   # un sustituto suelto (H-20): no se escribe lo que no se podría leer
        raise RegistroError(f"la anotación tiene un carácter que no es UTF-8 válido: {ex}") from ex
    return txt


class Registro:
    def __init__(self, ruta: Path | str = REGISTRO_DEFECTO, ancla_git: bool = True):
        if not str(ruta).strip():
            raise RegistroError("ruta del registro vacía")
        self.ruta = Path(ruta)
        self.ancla_git = ancla_git

    # ------------------------------------------------------------------ lectura y verificación
    def _texto(self) -> str:
        if not self.ruta.exists():
            return ""
        try:
            texto = self.ruta.read_bytes().decode("utf-8")
        except UnicodeDecodeError as e:
            raise RegistroError(f"el registro no está en UTF-8: está dañado ({e})") from e
        if texto and not texto.endswith("\n"):
            raise RegistroError("el registro no acaba en salto de línea: una escritura se cortó o se editó a mano")
        return texto

    def _repositorio(self) -> Path | None:
        """La raíz del repositorio git que contiene el registro, buscando «.git» hacia arriba (sin fiarse de GIT_DIR)."""
        d = self.ruta.resolve().parent
        while not d.exists() and d != d.parent:
            d = d.parent
        for c in (d, *d.parents):
            if (c / ".git").exists():
                return c
        return None

    @staticmethod
    def _git(raiz: Path, *args: str) -> subprocess.CompletedProcess:
        entorno = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}   # H-14: ni GIT_DIR ni GIT_WORK_TREE
        try:
            return subprocess.run(["git", "-C", str(raiz), *args], capture_output=True, check=False, env=entorno)
        except OSError as e:
            raise RegistroError(f"no se puede ejecutar git para comprobar el ancla del registro: {e}") from e

    def _comprobar_ancla(self, texto: str) -> bytes | None:
        """H-01 y H-13: si el registro está en un repositorio git, su historial solo puede crecer. En cada commit que lo toca,
        el registro tiene que existir y empezar por la versión de cada padre (también en las fusiones), y el fichero de
        ahora tiene que empezar por la versión de HEAD. Devuelve esa versión (None si nunca se subió). Si git no está o el
        repositorio está dañado, falla cerrado (H-14)."""
        if not self.ancla_git:
            return None
        raiz = self._repositorio()
        if raiz is None:
            return None
        if shutil.which("git") is None:
            raise RegistroError("el registro está en un repositorio git y git no está instalado: no se puede comprobar el ancla")
        try:
            rel = self.ruta.resolve().relative_to(raiz.resolve()).as_posix()
        except ValueError as e:
            raise RegistroError(f"no se puede situar el registro dentro de {raiz}: {e}") from e
        if self._git(raiz, "rev-parse", "--verify", "-q", "HEAD").returncode != 0:
            return None   # repositorio sin commits: todavía no hay ancla
        lista = self._git(raiz, "rev-list", "--full-history", "--parents", "HEAD", "--", rel)
        if lista.returncode != 0:
            raise RegistroError(f"git no puede leer el historial del registro: {lista.stderr.decode('utf-8', 'replace').strip()}")
        cache: dict[str, bytes | None] = {}

        def version(commit: str) -> bytes | None:
            if commit not in cache:
                arbol = self._git(raiz, "ls-tree", commit, "--", rel)
                if arbol.returncode != 0:
                    raise RegistroError(f"git no puede leer el commit {commit[:8]}: el repositorio está dañado")
                if not arbol.stdout.strip():
                    cache[commit] = None
                else:
                    blob = self._git(raiz, "cat-file", "blob", f"{commit}:{rel}")
                    if blob.returncode != 0:
                        raise RegistroError(f"git no puede leer el registro del commit {commit[:8]}: el repositorio está dañado")
                    cache[commit] = blob.stdout
            return cache[commit]

        for linea in lista.stdout.decode("utf-8", "replace").splitlines():
            commit, *padres = linea.split()
            actual = version(commit)
            if actual is None:
                raise RegistroError(f"el registro se quitó del repositorio en el commit {commit[:8]}")
            for p in padres:
                anterior = version(p)
                if anterior is not None and not actual.startswith(anterior):
                    raise RegistroError(f"en el commit {commit[:8]} el registro perdió o cambió anotaciones que ya estaban subidas")
        en_head = version("HEAD")
        if en_head is not None and not texto.encode("utf-8").startswith(en_head):
            raise RegistroError("el registro ya no empieza por lo que está subido en git (HEAD): se quitó o reescribió algo")
        return en_head

    def anotaciones(self) -> list[dict]:
        """Las anotaciones, comprobadas. Lee con un cerrojo compartido: un lector no ve una escritura a medias (H-21)."""
        if not self.ruta.exists():
            return self._leer()
        with self._cerrojo(compartido=True):
            return self._leer()

    def _leer(self) -> list[dict]:
        texto = self._texto()
        en_git = self._comprobar_ancla(texto)
        out: list[dict] = []
        prev = CERO
        pre: dict[str, dict] = {}
        intentos: dict[tuple[str, int], dict] = {}
        resultados: set[tuple[str, int]] = set()
        for i, linea in enumerate(texto.split("\n")[:-1] if texto else [], 1):
            try:
                e = json.loads(linea)
            except ValueError as ex:
                raise RegistroError(f"línea {i} no es JSON: el registro está dañado") from ex
            cuerpo = {k: v for k, v in e.items() if k != "_hash"} if isinstance(e, dict) else None
            if not isinstance(e, dict) or e.get("_seq") != len(out) + 1 or e.get("_hash_prev") != prev or e.get("_hash") != huella(cuerpo):
                raise RegistroError(f"cadena rota en la anotación {len(out) + 1}: alguien la reescribió o la quitó")
            validar_anotacion(e)
            exp = e["exp_id"]
            if e["tipo"] == "PRERREGISTRO":
                if exp in pre:
                    raise RegistroError(f"{exp} está prerregistrado dos veces")
                pre[exp] = e
            elif exp not in pre:
                raise RegistroError(f"la anotación {i} es de {exp}, que no está prerregistrado antes")
            elif e["tipo"] == "INTENTO":
                previos = [x for (x_exp, _), x in intentos.items() if x_exp == exp]
                if e["n"] != len(previos) + 1:
                    raise RegistroError(f"el intento {e['n']} de {exp} no es correlativo")
                if e["huella_prerregistro"] != pre[exp]["huella_prerregistro"]:
                    raise RegistroError(f"el intento {e['n']} de {exp} cita otro prerregistro")
                if e["dentro_del_maximo"] != _dentro(previos, e["variante"], pre[exp]["contenido"]["max_variantes"]):
                    raise RegistroError(f"el intento {e['n']} de {exp} dice mal si está dentro del máximo de variantes")
                intentos[(exp, e["n"])] = e
            else:
                if (exp, e["n"]) not in intentos:
                    raise RegistroError(f"resultado de un intento que no existe: {exp}, {e['n']}")
                if (exp, e["n"]) in resultados:
                    raise RegistroError(f"el intento {e['n']} de {exp} tiene dos resultados")
                resultados.add((exp, e["n"]))
            out.append(e)
            prev = e["_hash"]
        self._comprobar_sello(out, texto, en_git)
        return out

    def verificar(self) -> int:
        return len(self.anotaciones())

    @property
    def sello(self) -> Path:
        return self.ruta.with_name(self.ruta.name + ".sello")

    def _comprobar_sello(self, out: list[dict], texto: str, en_git: bytes | None) -> None:
        """El sello tiene que casar con la última anotación (H-01: quitar las últimas se detecta). Se admite:
        - un sello una anotación por detrás: la escritura se cortó entre la línea y el sello, y la siguiente lo pone al día
          (H-16); quitar líneas deja el registro por DETRÁS del sello, y eso nunca se admite;
        - sin sello, un registro idéntico al que está subido en git (un clon recién hecho, H-18) o con una sola anotación
          (el corte de la primera escritura)."""
        ultima = out[-1] if out else None
        if not self.sello.exists():
            if ultima is None or len(out) == 1 or (en_git is not None and texto.encode("utf-8") == en_git):
                return
            raise RegistroError(f"falta el sello del registro ({self.sello.name}): no se puede saber si le quitaron las últimas "
                                "líneas. Si es un registro de la versión 0.1.0, sin sello, se sella una vez con la orden «sellar»")
        try:
            s = json.loads(self.sello.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeDecodeError) as e:
            raise RegistroError(f"el sello del registro está dañado: {e}") from e
        esperado = {"seq": 0, "hash": CERO} if ultima is None else {"seq": ultima["_seq"], "hash": ultima["_hash"]}
        un_corte = None if ultima is None else {"seq": ultima["_seq"] - 1, "hash": ultima["_hash_prev"]}
        if s != esperado and s != un_corte:
            raise RegistroError(f"el registro no casa con su sello (anotación {esperado['seq']} frente a "
                                f"{s.get('seq') if isinstance(s, dict) else s!r}): le quitaron o cambiaron las últimas líneas")

    def _preparar_sello(self, e: dict | None) -> Path:
        s = {"seq": 0, "hash": CERO} if e is None else {"seq": e["_seq"], "hash": e["_hash"]}
        temporal = self.sello.with_name(self.sello.name + ".tmp")
        try:
            temporal.write_text(json.dumps(s) + "\n", encoding="utf-8")
        except OSError as ex:
            raise RegistroError(f"no se puede preparar el sello del registro ({ex}): no se escribe nada") from ex
        return temporal

    def _escribir_sello(self, e: dict | None, temporal: Path | None = None) -> None:
        temporal = temporal or self._preparar_sello(e)
        try:
            os.replace(temporal, self.sello)   # atómico: el sello nunca queda a medias
        except OSError as ex:
            raise RegistroError(f"la anotación está escrita, pero no se pudo poner al día el sello ({ex}); la siguiente "
                                "escritura lo pondrá al día") from ex

    def sellar(self) -> int:
        """Sella un registro sin sello (versión 0.1.0). Solo si no tiene: no puede saber si antes le quitaron líneas."""
        with self._cerrojo():
            if self.sello.exists():
                raise RegistroError("el registro ya tiene sello: no se vuelve a sellar")
            texto = self._texto()
            self._comprobar_ancla(texto)
            sin_sello = Registro(self.ruta, ancla_git=False)
            out = sin_sello._leer_sin_sello()
            self._escribir_sello(out[-1] if out else None)
            return len(out)

    def _leer_sin_sello(self) -> list[dict]:
        original = self._comprobar_sello
        self._comprobar_sello = lambda *a, **k: None   # type: ignore[method-assign]
        try:
            return self._leer()
        finally:
            self._comprobar_sello = original   # type: ignore[method-assign]

    @contextlib.contextmanager
    def _cerrojo(self, compartido: bool = False):
        """H-02 y H-21: una sola escritura a la vez en la misma máquina, y los lectores esperan a que acabe. El cerrojo va en
        un fichero aparte («.lock») y espera como mucho CERROJO_ESPERA_S segundos."""
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            fl = open(self.ruta.with_name(self.ruta.name + ".lock"), "a", encoding="utf-8")   # noqa: SIM115 - se cierra en el with de abajo
        except OSError as e:
            raise RegistroError(f"no se puede abrir el cerrojo del registro: {e}") from e
        with fl:
            if fcntl is not None:
                modo = (fcntl.LOCK_SH if compartido else fcntl.LOCK_EX) | fcntl.LOCK_NB
                limite = time.monotonic() + CERROJO_ESPERA_S
                while True:
                    try:
                        fcntl.flock(fl.fileno(), modo)
                        break
                    except BlockingIOError:
                        if time.monotonic() > limite:
                            raise RegistroError(f"el registro lleva más de {CERROJO_ESPERA_S} s ocupado por otra escritura") from None
                        time.sleep(0.05)
            try:
                yield
            finally:
                if fcntl is not None:
                    fcntl.flock(fl.fileno(), fcntl.LOCK_UN)

    def _anexar(self, construir) -> dict:
        """Lee, construye y escribe bajo el cerrojo: dos procesos no pueden leer el mismo estado y escribir a la vez."""
        with self._cerrojo():
            previas = self._leer()   # falla cerrado si el registro está dañado
            return self._escribir(previas, construir(previas))

    def _escribir(self, previas: list[dict], cuerpo: dict) -> dict:
        e = {**cuerpo, "_seq": len(previas) + 1, "_hash_prev": previas[-1]["_hash"] if previas else CERO}
        e["_hash"] = huella(e)
        validar_anotacion(e)
        linea = _linea(e)
        temporal = self._preparar_sello(e)   # antes de tocar el registro: si el sello no se puede escribir, no se escribe nada
        try:
            with open(self.ruta, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
                f.flush()
                os.fsync(f.fileno())
        except OSError as ex:
            temporal.unlink(missing_ok=True)
            raise RegistroError(f"no se pudo escribir en el registro: {ex}") from ex
        self._escribir_sello(e, temporal)
        return e

    def experimento(self, exp_id: str, previas: list[dict] | None = None) -> dict:
        """El prerregistro, los intentos y los resultados de un experimento."""
        a = self.anotaciones() if previas is None else previas
        pre = next((x for x in a if x["tipo"] == "PRERREGISTRO" and x["exp_id"] == exp_id), None)
        if pre is None:
            raise RegistroError(f"{exp_id} no está prerregistrado")
        return {"prerregistro": pre, "intentos": [x for x in a if x["tipo"] == "INTENTO" and x["exp_id"] == exp_id],
                "resultados": [x for x in a if x["tipo"] == "RESULTADO" and x["exp_id"] == exp_id]}

    # ------------------------------------------------------------------ escritura
    def prerregistrar(self, datos: dict, autor: str, ahora: str | None = None) -> dict:
        return self._anexar(self._construir_prerregistro(datos, autor, ahora))

    def buscar_o_prerregistrar(self, coincide, datos: dict, autor: str, ahora: str | None = None) -> tuple[dict, bool]:
        """El primer prerregistro cuyo contenido cumple «coincide», o uno nuevo con «datos», todo bajo el mismo cerrojo: dos
        procesos a la vez no crean dos experimentos de la misma hipótesis (H-19). Devuelve (prerregistro, si es nuevo)."""
        construir = self._construir_prerregistro(datos, autor, ahora)
        with self._cerrojo():
            previas = self._leer()
            for x in previas:
                if x["tipo"] == "PRERREGISTRO" and coincide(x["contenido"]):
                    return x, False
            return self._escribir(previas, construir(previas)), True

    def _construir_prerregistro(self, datos: dict, autor: str, ahora: str | None):
        _validar_contenido(datos)
        _texto(autor, "autor")
        ahora = ahora or _ahora()
        anio = _instante(ahora, "ahora").year   # el año del EXP es el de UTC (H-07)
        contenido = {k: datos[k] for k in sorted(datos)}
        huella_contenido = huella(contenido)   # falla con NaN u objetos que no son JSON

        def construir(previas):
            n = sum(1 for x in previas if x["tipo"] == "PRERREGISTRO" and x["exp_id"].startswith(f"EXP-{anio}-")) + 1
            if n > MAX_EXP_POR_ANIO:
                raise RegistroError(f"el año {anio} ya tiene {MAX_EXP_POR_ANIO} experimentos: EXP-AAAA-NNNN no admite más")
            return {"tipo": "PRERREGISTRO", "exp_id": f"EXP-{anio}-{n:04d}", "autor": autor, "creado_en": ahora,
                    "version_registro": VERSION, "contenido": contenido, "huella_prerregistro": huella_contenido}
        return construir

    def intento(self, exp_id: str, variante: str = "única", ahora: str | None = None) -> dict:
        variante = _variante(variante)
        ahora = ahora or _ahora()
        _instante(ahora, "ahora")
        if not self.ruta.exists():   # no se crea carpeta ni cerrojo para un intento que se va a rechazar (H-21)
            raise RegistroError(f"{exp_id} no está prerregistrado (no existe el registro {self.ruta.name})")

        def construir(previas):
            exp = self.experimento(exp_id, previas)   # sin prerregistro no hay intento
            return {"tipo": "INTENTO", "exp_id": exp_id, "n": len(exp["intentos"]) + 1, "variante": variante, "inicio": ahora,
                    "huella_prerregistro": exp["prerregistro"]["huella_prerregistro"],
                    "dentro_del_maximo": _dentro(exp["intentos"], variante, exp["prerregistro"]["contenido"]["max_variantes"])}
        return self._anexar(construir)

    def resultado(self, exp_id: str, n: int, veredicto: str, detalle: dict | None = None, ahora: str | None = None) -> dict:
        _entero(n, "n", 1)
        if veredicto not in VEREDICTOS:
            raise RegistroError(f"veredicto {veredicto!r} no válido ({', '.join(VEREDICTOS)})")
        detalle = {} if detalle is None else detalle
        if not isinstance(detalle, dict):
            raise RegistroError("«detalle» tiene que ser un objeto JSON")
        ahora = ahora or _ahora()
        _instante(ahora, "ahora")
        if not self.ruta.exists():
            raise RegistroError(f"{exp_id} no está prerregistrado (no existe el registro {self.ruta.name})")

        def construir(previas):
            exp = self.experimento(exp_id, previas)
            if not any(x["n"] == n for x in exp["intentos"]):
                raise RegistroError(f"{exp_id} no tiene el intento {n}")
            if any(x["n"] == n for x in exp["resultados"]):
                raise RegistroError(f"el intento {n} de {exp_id} ya tiene resultado: no se reescribe")
            return {"tipo": "RESULTADO", "exp_id": exp_id, "n": n, "veredicto": veredicto, "detalle": detalle, "registrado_en": ahora}
        return self._anexar(construir)

    # ------------------------------------------------------------------ lo que dice el registro
    def resumen(self, exp_id: str) -> dict:
        exp = self.experimento(exp_id)
        pre = exp["prerregistro"]
        maximo = pre["contenido"]["max_variantes"]
        creado = _instante(pre["creado_en"], "creado_en")
        res = {x["n"]: x for x in exp["resultados"]}
        intentos = exp["intentos"]
        orden_variantes = list(dict.fromkeys(_nfc(i["variante"]) for i in intentos))
        por_variante: dict[str, dict] = {}
        for v in orden_variantes:
            suyos = [i for i in intentos if _nfc(i["variante"]) == v]
            con_veredicto = [(i, res[i["n"]]["veredicto"]) for i in suyos if i["n"] in res and res[i["n"]]["veredicto"] != "fallido"]
            # H-15: un intento sin resultado deja la variante pendiente; si es el primero que no falló, todavía no hay veredicto
            pendiente = any(i["n"] not in res for i in suyos)
            primero_vivo = next((i for i in suyos if res.get(i["n"], {}).get("veredicto") != "fallido"), None)
            primero = con_veredicto[0] if con_veredicto and primero_vivo is not None and primero_vivo["n"] in res else None
            contradictoria = bool(primero) and any(ver != primero[1] for _, ver in con_veredicto[1:])
            por_variante[v] = {"intentos": [i["n"] for i in suyos], "cuenta": primero[0]["n"] if primero else None,
                               "veredicto": primero[1] if primero else None, "contradictoria": contradictoria,
                               "pendiente": pendiente,
                               "dentro_del_maximo": orden_variantes.index(v) < maximo,
                               "despues_del_prerregistro": bool(primero) and _instante(primero[0]["inicio"], "inicio") >= creado}
        adoptables = [d["cuenta"] for d in por_variante.values()
                      if d["veredicto"] == "mejor" and not d["contradictoria"] and not d["pendiente"] and d["dentro_del_maximo"] and d["despues_del_prerregistro"]]
        return {"exp_id": exp_id, "hipotesis": pre["contenido"]["hipotesis"], "objeto": pre["contenido"]["objeto"],
                "max_variantes": maximo, "intentos": len(intentos), "variantes": len(orden_variantes),
                "sin_resultado": [i["n"] for i in intentos if i["n"] not in res],
                "fuera_del_maximo": [i["n"] for i in intentos if orden_variantes.index(_nfc(i["variante"])) >= maximo],
                "veredictos": {str(n): r["veredicto"] for n, r in sorted(res.items())},
                "por_variante": por_variante,
                "contradictorias": [v for v, d in por_variante.items() if d["contradictoria"]],
                "adoptables": sorted(adoptables), "adoptable": bool(adoptables)}

    def adoptable(self, exp_id: str) -> bool:
        return self.resumen(exp_id)["adoptable"]


def _nfc(v: str) -> str:
    return unicodedata.normalize("NFC", v)


def _dentro(intentos_previos: list[dict], variante: str, maximo: int) -> bool:
    """¿La variante está entre las «maximo» primeras que aparecen? Se recalcula siempre (H-06): no se fía de lo guardado. Las
    variantes se comparan en NFC, también las de un registro de la 0.1.0 (QA r02)."""
    orden = list(dict.fromkeys([_nfc(x["variante"]) for x in intentos_previos] + [_nfc(variante)]))
    return orden.index(_nfc(variante)) < maximo


def _sin_constantes(c: str):
    raise RegistroError(f"{c} no es JSON estándar")


def main(argv: list[str] | None = None) -> int:
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument("--registro", default=argparse.SUPPRESS)
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], parents=[comun])
    sub = ap.add_subparsers(dest="orden", required=True)
    p = sub.add_parser("prerregistrar", parents=[comun])
    p.add_argument("fichero")
    p.add_argument("--autor", default="operador")
    p = sub.add_parser("intento", parents=[comun])
    p.add_argument("exp_id")
    p.add_argument("--variante", required=True)
    p = sub.add_parser("resultado", parents=[comun])
    p.add_argument("exp_id")
    p.add_argument("n", type=int)
    p.add_argument("veredicto")
    p.add_argument("--detalle", default="{}")
    p = sub.add_parser("ver", parents=[comun])
    p.add_argument("exp_id", nargs="?")
    sub.add_parser("verificar", parents=[comun])
    sub.add_parser("sellar", parents=[comun], help="sella una vez un registro sin sello (versión 0.1.0)")
    a = ap.parse_args(argv)
    try:
        r = Registro(getattr(a, "registro", REGISTRO_DEFECTO))
        if a.orden == "prerregistrar":
            e = r.prerregistrar(json.loads(Path(a.fichero).read_text(encoding="utf-8")), a.autor)
            print(f"{e['exp_id']} prerregistrado; huella {e['huella_prerregistro'][:16]}…")
        elif a.orden == "intento":
            e = r.intento(a.exp_id, a.variante)
            print(f"{a.exp_id}: intento {e['n']}" + ("" if e["dentro_del_maximo"] else " (FUERA del máximo de variantes prerregistrado)"))
        elif a.orden == "resultado":
            detalle = json.loads(a.detalle, parse_constant=_sin_constantes)
            if not isinstance(detalle, dict):
                raise RegistroError("«--detalle» tiene que ser un objeto JSON")
            r.resultado(a.exp_id, a.n, a.veredicto, detalle)
            print(f"{a.exp_id}: resultado del intento {a.n} registrado")
        elif a.orden == "ver":
            ids = [a.exp_id] if a.exp_id else sorted({x["exp_id"] for x in r.anotaciones() if x["tipo"] == "PRERREGISTRO"})
            print(json.dumps([r.resumen(i) for i in ids], ensure_ascii=False, indent=1))
        elif a.orden == "sellar":
            n = r.sellar()
            print(f"registro sellado con {n} anotaciones (lo anterior al sello no se puede comprobar)")
        else:
            if not r.ruta.exists():
                raise RegistroError(f"no existe el registro {r.ruta}")
            n = r.verificar()
            print(f"registro íntegro: {n} anotaciones" + ("" if n else " (vacío)"))
    except Exception as e:   # noqa: BLE001 - la línea de órdenes nunca sale con una traza: motivo y código 2 (H-06)
        print(f"registro de experimentos: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
