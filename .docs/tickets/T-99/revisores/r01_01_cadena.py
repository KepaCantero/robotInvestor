"""r01_01 · Cadena de huellas: reescribir, quitar, reordenar, insertar, truncar, duplicar, recadenar, final de línea y
separadores de línea Unicode. Uso: python3 r01_01_cadena.py <raíz>"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import (AHORA, DESPUES, caso, escribir, fin, lanza, lineas, pre, recadenar,  # noqa: E402
                       registro_temporal, rx)


def base():
    reg = registro_temporal()
    exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.resultado(exp, 1, "peor", ahora=DESPUES)
    reg.intento(exp, "v2", DESPUES)
    reg.resultado(exp, 2, "fallido", ahora=DESPUES)
    return reg, exp


# 1. reescribir un resultado sin recalcular
reg, exp = base()
ls = lineas(reg); e = json.loads(ls[2]); e["veredicto"] = "mejor"; ls[2] = json.dumps(e, ensure_ascii=False)
escribir(reg, ls)
caso("reescribir un resultado se detecta", isinstance(lanza(reg.verificar, rx.RegistroError), rx.RegistroError))

# 2. quitar un intento del medio
reg, exp = base(); ls = lineas(reg); escribir(reg, ls[:3] + ls[4:])
caso("quitar una anotación del medio se detecta", isinstance(lanza(reg.verificar, rx.RegistroError), rx.RegistroError))

# 3. reordenar dos líneas
reg, exp = base(); ls = lineas(reg); ls[1], ls[2] = ls[2], ls[1]; escribir(reg, ls)
caso("reordenar dos anotaciones se detecta", isinstance(lanza(reg.verificar, rx.RegistroError), rx.RegistroError))

# 4. insertar una línea copiada
reg, exp = base(); ls = lineas(reg); escribir(reg, ls[:2] + [ls[1]] + ls[2:])
caso("insertar una línea duplicada en medio se detecta", isinstance(lanza(reg.verificar, rx.RegistroError), rx.RegistroError))

# 5. duplicar la última línea
reg, exp = base(); ls = lineas(reg); escribir(reg, ls + [ls[-1]])
caso("duplicar la última línea se detecta", isinstance(lanza(reg.verificar, rx.RegistroError), rx.RegistroError))

# 6. truncar la última línea (quitar el resultado «fallido» del final)
reg, exp = base(); ls = lineas(reg); escribir(reg, ls[:-1])
err = lanza(reg.verificar, rx.RegistroError)
caso("truncar la última anotación (el resultado «fallido») se detecta", err is not None,
     f"verificar() = {reg.verificar() if err is None else err}; resumen: {reg.resumen(exp)['sin_resultado'] if err is None else '-'}")

# 7. truncar las dos últimas (el intento v2 y su resultado: desaparece un intento entero)
reg, exp = base(); ls = lineas(reg); escribir(reg, ls[:-2])
err = lanza(reg.verificar, rx.RegistroError)
caso("quitar el último intento con su resultado se detecta (CA-3, «quitar un intento»)", err is not None,
     f"intentos que quedan: {reg.resumen(exp)['intentos'] if err is None else '-'}")

# 8. recadenar entero tras cambiar un veredicto (sin secreto ni ancla, cualquiera puede)
reg, exp = base(); objs = [json.loads(x) for x in lineas(reg)]; objs[2]["veredicto"] = "mejor"
escribir(reg, recadenar(objs))
err = lanza(reg.verificar, rx.RegistroError)
caso("recalcular toda la cadena tras cambiar un veredicto se detecta", err is not None,
     f"adoptable tras la manipulación = {reg.adoptable(exp) if err is None else '-'} (solo lo delataría git)")

# 9. cambiar el criterio y recalcular huella_prerregistro y cadena
reg, exp = base(); objs = [json.loads(x) for x in lineas(reg)]
objs[0]["contenido"]["criterio_exito"] = "cualquier mejora, aunque sea ruido"
objs[0]["huella_prerregistro"] = rx.huella(objs[0]["contenido"])
escribir(reg, recadenar(objs))
err = lanza(reg.verificar, rx.RegistroError)
caso("cambiar el criterio y recalcular huellas: los intentos citan la huella vieja y se detecta", err is not None,
     "el registro no compara la huella_prerregistro de cada intento con la del prerregistro" if err is None else "")

# 10. líneas vacías insertadas: se toleran (no cambian el contenido)
reg, exp = base(); ls = lineas(reg); escribir(reg, ls[:2] + ["", "   "] + ls[2:])
caso("líneas vacías intercaladas: se toleran sin perder anotaciones", reg.verificar() == 5)

# 11. quitar solo el salto de línea final (lo hacen muchos editores) y anotar otra vez
reg, exp = base(); ls = lineas(reg); escribir(reg, ls, final="")
e = lanza(lambda: reg.intento(exp, "v1", DESPUES), Exception)
err = lanza(reg.verificar, rx.RegistroError)
caso("sin salto de línea final, el siguiente anexo no corrompe el registro", e is None and err is None,
     f"anexo: {e!r}; verificar después: {err}")

# 12. separadores de línea Unicode en un texto válido (U+2028, U+0085): json.dumps(ensure_ascii=False) no los escapa
for nombre, sep in (("U+2028", " "), ("U+0085", "\x85"), ("U+001C", "\x1c")):
    reg = registro_temporal()
    exp = reg.prerregistrar(pre(hipotesis=f"Hipótesis larga{sep}con un separador dentro"), "qa", AHORA)["exp_id"]
    err = lanza(reg.verificar, rx.RegistroError)
    err2 = lanza(lambda: reg.intento(exp, "v1", DESPUES), Exception)
    caso(f"un prerregistro válido con {nombre} en la hipótesis no bloquea el registro", err is None and err2 is None,
         f"verificar: {err}; siguiente intento: {err2!r}" if err or err2 else "")

# 13. variante con U+2028 desde intento()
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
reg.intento(exp, "v 1", DESPUES)
err = lanza(reg.verificar, rx.RegistroError)
caso("una variante con U+2028 no bloquea el registro", err is None, f"{err}" if err else "")
# 14. cambiar el criterio y recalcular SOLO la cadena (la huella_prerregistro queda vieja)
reg, exp = base(); objs = [json.loads(x) for x in lineas(reg)]
objs[0]["contenido"]["criterio_exito"] = "cualquier mejora, aunque sea ruido"
escribir(reg, recadenar(objs))
err = lanza(reg.verificar, rx.RegistroError)
caso("contenido cambiado con la huella_prerregistro vieja (cadena recalculada) se detecta", err is not None,
     "verificar() no compara huella_prerregistro con huella(contenido)" if err is None else "")
fin()
