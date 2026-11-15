# RoboInvestor

La carpeta `robotTrading/` contiene la plataforma de simulación, estrategias, cartera, riesgo, API, paneles, operaciones en papel e históricos. El código está incorporado en este repositorio. Los ejemplos de los bloques A y B leen las salidas de RoboInvestor y simulan las operaciones con el motor de robotTrading.

## Primera ejecución

Desde la raíz de RoboInvestor, con [uv](https://docs.astral.sh/uv/) instalado:

```sh
uv sync --project robotTrading --locked --python 3.12 --extra paper
uv run --project robotTrading --no-sync python backtest.py a
uv run --project robotTrading --no-sync python backtest.py b
```

Elige `--python 3.12` o `--python 3.11`. La instalación inicial descarga esa versión si hace falta y las dependencias fijadas. Los dos ejemplos usan históricos diarios incluidos y no requieren credenciales. Imprimen las fechas de compra y venta, los precios y el capital final. Las gráficas quedan en `robotTrading/resultados/graficas/`.

A simula una oportunidad nueva de compra usando el activo de referencia del bloque. B simula una selección de su ranking. El ejemplo de B incluye la equivalencia comprobada entre Siemens Energy y ENR.DE. La selección se produce en la fecha indicada y la compra simulada, en la siguiente sesión. Añade `--help` al comando de A o B para elegir otras entradas e históricos. Estos dos ejemplos prueban operaciones individuales.

## Plataforma completa

Desde `robotTrading/` están disponibles los comandos y las configuraciones propios de la plataforma. Para abrir la API, usa `uv run --no-sync python -m uvicorn app.main:app`. Para el panel, usa `uv run --no-sync python -m app.presentation.dashboard.nicegui_app`. La imagen Docker admite `docker build --target production --build-arg PYTHON_MINOR=3.12 -t roboinvestor-trading .` desde esa misma carpeta. La guía de la plataforma describe sus servicios, configuración y despliegue. [Manual de robotTrading](robotTrading/README.md)

La versión incorporada procede de [robotTrading, revisión 3bf48f2](https://github.com/KepaCantero/robotTrading/commit/3bf48f2cfff4d5c003c2ffaea7cd35a55f0b67f4). Los dos adaptadores de RoboInvestor, la generación de sus gráficas y sus pruebas proceden del piloto local. [Protocolo de RoboInvestor](CLAUDE.md)
