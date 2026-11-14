"""QA r02 de T-114 · ¿Qué no ven las formas de los once flujos?

1. Captura los once flujos UNA vez sin el filtro de contratos (todos los contratos de cada flujo) y vuelve a aplicar el filtro
   de `goldens_ct.FLUJOS` a mano: con lo filtrado, `formas()` tiene que dar el golden congelado (control).
2. Lo que el filtro tira: por flujo filtrado, los contratos que emite y no se guardan, y de ellos las rutas, los tipos y los
   valores de las listas cerradas del Anexo B que no aparecen en NINGÚN flujo guardado (lo que ningún golden ve).
3. Cambios sobre los mensajes capturados (como `test_h01_un_cambio_en_lo_que_el_ejecutor_emite_cambia_las_formas`, pero
   otros): los del límite declarado («tipos y claves opcionales mezclados») y variantes que el README no declara.
4. Con `--copia <copia_desechable>` (ruta con «qa_f3_mut»), además, mutantes del CÓDIGO del ejecutor en ramas que los
   flujos recorren pero cuyo contrato no se guarda, contra `python tests/goldens_ct.py` entero.

Uso, desde la raíz del repositorio:  python .docs/tickets/T-114/revisores/r02_02_formas_y_flujos.py [--copia <copia>]
Termina siempre con 0: es una medida.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]
import goldens_ct as g  # noqa: E402

PY = "/home/user/robotinvestor/.venv/bin/python"
FECHA = "2026-06-05"
O = "bloque_a/orquestacion.py"

MUTANTES_CODIGO = [
    ("K01", O, "CT-05 de un ciclo AD_HOC (petición, consulta que escala) sale con tipo PERIODICO",
     '{"tipo": tipo, "alcance": alcance or {"clases": clases},', '{"tipo": "PERIODICO" if tipo == "AD_HOC" else tipo, "alcance": alcance or {"clases": clases},'),
    ("K02", O, "CT-05 de un ciclo ad hoc pierde `alcance.pregunta`",
     '{"tipo": tipo, "alcance": alcance or {"clases": clases},',
     '{"tipo": tipo, "alcance": {k: v for k, v in (alcance or {"clases": clases}).items() if k != "pregunta"},'),
    ("K03", O, "CT-02 del segundo ciclo semanal sale con `top3_por_clase` vacío (el primero, igual que hoy)",
     'for o in paquete["clases"][c]["opciones"]] for c in paquete["clases"]},',
     'for o in paquete["clases"][c]["opciones"]] for c in paquete["clases"] if not (tipo == "PERIODICO" and str(as_of.date()) == "2026-06-12")},'),
]


def filtrar(flujos: dict) -> dict:
    return {n: [m for m in v if g.FLUJOS[n] == g.TODOS or m["contrato"] in g.FLUJOS[n]] for n, v in flujos.items()}


def capturar_sin_filtro() -> dict:
    original = dict(g.FLUJOS)
    try:
        for n in g.FLUJOS:
            g.FLUJOS[n] = g.TODOS
        with tempfile.TemporaryDirectory() as tmp:
            return g.capturar_flujos(Path(tmp), FECHA)
    finally:
        g.FLUJOS.clear()
        g.FLUJOS.update(original)


def lo_que_tira_el_filtro(todos: dict, esquemas: dict) -> None:
    guardados = filtrar(todos)
    forma_g = g.formas(guardados, esquemas)["flujos"]
    vistas: dict[str, dict] = {}
    for n, d in forma_g.items():
        for clave, t in d["mensajes"].items():
            v = vistas.setdefault(clave, {"rutas": set(), "valores": set()})
            v["rutas"] |= {f"{r}:{tp}" for r, tp in {**t["rutas_siempre"], **t["rutas_a_veces"]}.items()}
            for campo, valores in t.get("valores_de_listas_cerradas", {}).items():
                v["valores"] |= {f"{campo}={x}" for x in valores}
    for n in sorted(g.FLUJOS):
        if g.FLUJOS[n] == g.TODOS:
            continue
        tirados = [m for m in todos[n] if m["contrato"] not in g.FLUJOS[n]]
        if not tirados:
            print(f"  {n}: el filtro no tira nada")
            continue
        forma_t = g.formas({n: tirados}, esquemas)["flujos"][n]["mensajes"]
        print(f"  {n}: tira {len(tirados)} mensajes de {sorted(forma_t)}")
        for clave, t in sorted(forma_t.items()):
            ya = vistas.get(clave, {"rutas": set(), "valores": set()})
            rutas = sorted({f"{r}:{tp}" for r, tp in {**t["rutas_siempre"], **t["rutas_a_veces"]}.items()} - ya["rutas"])
            valores = sorted({f"{c}={x}" for c, xs in t.get("valores_de_listas_cerradas", {}).items() for x in xs} - ya["valores"])
            if rutas or valores:
                print(f"    {clave}: {len(rutas)} rutas:tipo y {len(valores)} valores de lista cerrada que ningún flujo guardado tiene")
                for r in rutas[:12]:
                    print(f"      ruta  {r}")
                for x in valores:
                    print(f"      valor {x}")


def _mensajes(flujos, flujo, clave):
    return [m for m in flujos[flujo] if f"{m['contrato']}.{m['tipo_mensaje']}" == clave]


def cambios(flujos: dict) -> list:
    """(id, ¿lo declara el README?, descripción, función que cambia la copia de los flujos)."""
    def t01(f):   # top3 vacío en UNO de los dos CT-02 del ciclo semanal V5
        _mensajes(f, "ciclo_semanal_v5", "CT-02.RETORNO")[1]["resumen"]["top3_por_clase"] = {}

    def t02(f):   # nivel_por_clase vacío en UNO de los dos CT-05 del ciclo semanal V5
        _mensajes(f, "ciclo_semanal_v5", "CT-05.ENCARGO")[1]["nivel_por_clase"] = {}

    def t03(f):   # una clase menos en presupuesto_por_clase en UNO de los CT-05
        m = _mensajes(f, "ciclo_semanal_v5", "CT-05.ENCARGO")[0]["presupuesto_por_clase"]
        m.pop(sorted(k for k in m if k != "COMUN")[0])

    def t04(f):   # clave «siempre» anidada que cambia de tipo en UN solo mensaje
        d = _mensajes(f, "ciclo_semanal_v5", "CT-05.ENCARGO")[0]["delta_gc0"]
        d[sorted(d)[0]]["arrastre_verificado"] = "SI"

    def t05(f):   # clave «a veces» de primer nivel que deja de emitirse en UN caso (límite declarado, primer nivel: se ve)
        m = [x for x in _mensajes(f, "seguimiento_encargado", "CT-24.RETORNO") if "proximo_ciclo" in x][0]
        del m["proximo_ciclo"]

    def t06(f):   # clave anidada opcional que deja de emitirse en UN caso (límite declarado)
        for m in _mensajes(f, "consulta_al_broker", "CT-23.ENCARGO"):
            for p in m.get("preguntas", []):
                if "efecto_si_falso" in p:
                    del p["efecto_si_falso"]
                    return

    def t07(f):   # un null|string que deja de ser null en UN caso (límite declarado)
        for m in _mensajes(f, "seguimiento_encargado", "CT-24.RETORNO"):
            if m.get("aviso") is None and "aviso" in m:
                m["aviso"] = "frecuencia corta"
                return

    def t08(f):   # un valor de lista cerrada del Anexo B que cambia en UN caso a otro valor de la lista ya visto
        m = _mensajes(f, "seguimiento_encargado", "CT-24.ENCARGO")
        m[0]["frecuencia"] = "MENSUAL" if m[0].get("frecuencia") != "MENSUAL" else "SEMANAL"

    def t09(f):   # un identificador emitido con otro formato (valor; límite declarado)
        _mensajes(f, "ciclo_semanal_v5", "CT-02.RETORNO")[0]["run_id"] = "RUN-26-1"

    def t10(f):   # una lista que pasa a vacía en UN caso cuando en otros ya lo era (CT-05 memoria)
        for m in _mensajes(f, "ciclo_semanal_v5", "CT-05.ENCARGO"):
            if m["memoria"].get("opp_vigentes"):
                m["memoria"]["opp_vigentes"] = []
                return

    def t11(f):   # emisor distinto en UN CT-08 del V6, de uno que ya emite (no cambia el conjunto)
        ms = _mensajes(f, "ciclo_semanal_v6", "CT-08.ENCARGO")
        ms[0]["emisor"] = ms[-1]["emisor"]

    def t12(f):   # un número entero que pasa a decimal en UN caso de una ruta «number»
        for m in _mensajes(f, "ciclo_semanal_v5", "CT-06.ENCARGO"):
            if isinstance(m.get("umbral_senal_gc1"), float):
                m["umbral_senal_gc1"] = 1
                return

    return [("T01", "no (artefacto de las claves genéricas <clase>)", "CT-02: top3_por_clase vacío en uno de los dos ciclos V5", t01),
            ("T02", "no (artefacto de las claves genéricas <clase>)", "CT-05: nivel_por_clase vacío en uno de los dos ciclos V5", t02),
            ("T03", "no (artefacto de las claves genéricas <clase>)", "CT-05: presupuesto_por_clase pierde una clase en un ciclo", t03),
            ("T04", "—", "CT-05: delta_gc0.<clase>.arrastre_verificado pasa a texto en un mensaje", t04),
            ("T05", "—", "CT-24 retorno: proximo_ciclo deja de emitirse en un caso (primer nivel)", t05),
            ("T06", "sí", "CT-23: preguntas[].efecto_si_falso deja de emitirse en un caso", t06),
            ("T07", "sí", "CT-24 retorno: aviso null pasa a texto en un caso", t07),
            ("T08", "sí (valores)", "CT-24 encargo: otro valor de frecuencia ya visto", t08),
            ("T09", "sí (valores)", "CT-02: run_id con otro formato", t09),
            ("T10", "sí", "CT-05: memoria.opp_vigentes vacía en el segundo ciclo", t10),
            ("T11", "—", "CT-08 V6: un emisor cambiado por otro que ya emite", t11),
            ("T12", "—", "CT-06: umbral_senal_gc1 de decimal a entero en un mensaje", t12)]


def claves_genericas(flujos: dict, congelado: dict) -> None:
    """Rutas que terminan en una clave genérica (<clase>, <id>): ¿está la clave (alguna) en TODOS los objetos que la podrían
    llevar? Se compara con el grupo en que la pone el golden (`rutas_siempre` / `rutas_a_veces`)."""
    mal = bien = 0
    ejemplos = []
    for n, d in congelado["flujos"].items():
        for clave, t in d["mensajes"].items():
            msgs = _mensajes(flujos, n, clave)
            for ruta in [*t["rutas_siempre"], *t["rutas_a_veces"]]:
                if not ruta.endswith((".<clase>", ".<id>")):
                    continue
                padre, hoja = ruta.rsplit(".", 1)
                objetos = []

                def bajar(valor, partes):
                    if not partes:
                        if isinstance(valor, dict):
                            objetos.append(valor)
                        return
                    p, resto = partes[0], partes[1:]
                    if p.endswith("[]"):
                        lista = valor.get(p[:-2]) if isinstance(valor, dict) else None
                        for x in lista if isinstance(lista, list) else []:
                            bajar(x, resto)
                    elif isinstance(valor, dict):
                        hijos = [v for k, v in valor.items() if g._clave(k) == p]
                        for v in hijos:
                            bajar(v, resto)
                for m in msgs:
                    bajar(m, [x for x in padre.replace("[]", "[].").split(".") if x and x != "."] if padre else [])
                    if not padre:
                        objetos.append(m)
                en_todos = all(any(g._clave(k) == hoja for k in o) for o in objetos) if objetos else False
                grupo = "siempre" if ruta in t["rutas_siempre"] else "a_veces"
                if en_todos and grupo == "a_veces":
                    mal += 1
                    ejemplos.append(f"{n} · {clave} · {ruta} (en {len(objetos)} de {len(objetos)} objetos, y el golden dice «a veces»)")
                else:
                    bien += 1
    print(f"5. rutas con clave genérica: {mal} están en todos sus objetos y el golden las pone en «a veces»; {bien} bien clasificadas")
    for e in ejemplos[:15]:
        print("   " + e)


def main() -> int:
    esquemas, _ = g.leer_a_mano()
    congelado = json.loads((g.CARPETA / "formas_flujos_mock.json").read_text(encoding="utf-8"))
    todos = capturar_sin_filtro()
    print(f"capturados sin filtro: {sum(len(v) for v in todos.values())} mensajes; filtrados: {sum(len(v) for v in filtrar(todos).values())}")
    control = g.formas(filtrar(todos), esquemas) == congelado
    print(f"1. control: formas de lo filtrado == golden: {control}")
    print("2. lo que el filtro tira y ningún flujo guardado tiene:")
    lo_que_tira_el_filtro(todos, esquemas)
    print("3. cambios sobre los mensajes capturados (¿cambian las formas?):")
    base = filtrar(todos)
    for cid, declarado, desc, cambio in cambios(base):
        f = copy.deepcopy(base)
        try:
            cambio(f)
        except (IndexError, KeyError) as e:
            print(f"  {cid} · NO APLICADO ({type(e).__name__}) · {desc}")
            continue
        visto = g.formas(f, esquemas) != congelado
        print(f"  {cid} · {'SE VE' if visto else 'NO SE VE'} · declarado en Límites: {declarado} · {desc}")
    claves_genericas(base, congelado)
    if "--copia" in sys.argv:
        copia = Path(sys.argv[sys.argv.index("--copia") + 1]).resolve()
        assert "qa_f3_mut" in str(copia), "solo en una copia desechable"
        ej = copia / "bloque_a" / "11_Ejecutor"
        print("4. mutantes del código contra goldens_ct.py entero:")
        for mid, fich, desc, viejo, nuevo in MUTANTES_CODIGO:
            ruta = ej / fich
            original = ruta.read_text(encoding="utf-8")
            if original.count(viejo) != 1:
                print(f"  {mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}")
                continue
            try:
                ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
                r = subprocess.run([PY, "tests/goldens_ct.py"], cwd=ej, capture_output=True, text=True)
                print(f"  {mid} · goldens_ct rc={r.returncode} ({'DETECTADO' if r.returncode else 'NO DETECTADO'}) · {desc}", flush=True)
            finally:
                ruta.write_text(original, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
