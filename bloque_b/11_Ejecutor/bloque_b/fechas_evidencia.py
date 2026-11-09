"""Fechas de la fuente en el contraste diario de objeciones (F2 / CT-B-17)."""
from datetime import date, datetime

CAMPOS_FECHA = ("fecha_fenomeno", "fecha_publicacion", "conocible_desde")


def dia_local(valor, zona):
    """Fecha ISO o instante ISO con zona. Una hora sin zona no fija el día del expediente."""
    if not isinstance(valor, str):
        return None
    try:
        if len(valor) == 10:
            return date.fromisoformat(valor).isoformat()
        instante = datetime.fromisoformat(valor[:-1] + "+00:00" if valor.endswith("Z") else valor)
        if instante.tzinfo is not None:
            return instante.astimezone(zona).date().isoformat()
    except (ValueError, OverflowError):
        pass
    return None


def fechas_de_fuente(registro, corte, zona):
    """Solo las fechas declaradas por la fuente; nunca se sustituyen por el alta local."""
    fechas = registro.get("fechas", {})
    if not isinstance(fechas, dict):
        return None
    dias = {campo: dia_local(fechas.get(campo, registro.get(campo)), zona)
            for campo in CAMPOS_FECHA}
    hecho, publicacion, disponible = (dias[campo] for campo in CAMPOS_FECHA)
    if hecho and publicacion and disponible and hecho <= publicacion <= disponible <= corte:
        return dias
    return None
