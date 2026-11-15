"""r03_10 · r02_03_cerrojo.py adaptado al registro 0.3.0, sin tocar el original. En la 0.3.0 los lectores también toman el
cerrojo, así que con un «.lock» que es un directorio también falla la lectura (falla cerrado) y r02_03 se corta con una traza en
su caso 3 sin llegar a los casos 4 a 6. Aquí se lee el original, se cambia solo la comprobación de ese caso (contar las líneas del
fichero en vez de llamar a verificar()) y se ejecuta entero.
Uso: .venv/bin/python -B r03_10_r02_03_adaptado.py <raíz>"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
fuente = (AQUI / "r02_03_cerrojo.py").read_text(encoding="utf-8")
viejo = 'caso("«.lock» que es un directorio: no escribe", e is not None and reg.verificar() == 1)'
nuevo = ('caso("«.lock» que es un directorio: no escribe (r03: contando líneas; la lectura también falla cerrado)", '
         'e is not None and len(reg.ruta.read_text(encoding="utf-8").splitlines()) == 1)')
assert fuente.count(viejo) == 1
sys.path.insert(0, str(AQUI))
codigo = compile(fuente.replace(viejo, nuevo), str(AQUI / "r02_03_cerrojo.py") + " (adaptado r03)", "exec")
exec(codigo, {"__name__": "__main__", "__file__": str(AQUI / "r02_03_cerrojo.py")})
