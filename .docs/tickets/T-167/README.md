# T-167 · Bloque A: versión del paquete del ejecutor 1.1.0 → 1.2.0 (INC-001)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r01 APTO; bajos subsanados en la ronda de cierre) |
| Pieza | bloque_a (empaquetado): `bloque_a/11_Ejecutor/pyproject.toml`, `bloque_a/11_Ejecutor/bloque_a/__init__.py` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo |
| Aprobación del operador | 2026-11-16: decisión delegada en el agente (`sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` §1) |
| Deuda técnica | T-167 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar INC-001: el README del ejecutor declara «ejecutor V1.2» desde la V5.1, pero `pyproject.toml` y `bloque_a.__version__` decían 1.1.0. El código entregado es el V1.2.

## Alcance

- **Entra:** `version` de `pyproject.toml` y `__version__` del paquete a 1.2.0; una prueba que ata los dos al título del README; la nota de resolución en INC-001; la trampa de `CLAUDE.md`.
- **No entra:** reinstalar el paquete en los entornos ya creados.

## Diseño

- La prueba lee la versión del título del README («(V1.2)») y exige que `pyproject.toml` diga 1.2.0 y que `bloque_a.__version__` diga lo mismo que el `pyproject.toml`. No lee los metadatos instalados (`importlib.metadata`), que dependen de cuándo se instaló el paquete.
- **Estado persistido:** ninguno. **Números:** la versión no es un parámetro del Anexo A.

## Criterios de aceptación

1. `pyproject.toml` y `bloque_a.__version__` dicen 1.2.0.
2. `tests/test_t167_version.py` pasa, y falla si cualquiera de los dos vuelve a 1.1.0 o deja de coincidir con el README.
3. INC-001 queda resuelta con su motivo; INC-002 sigue abierta.
4. Gate en verde, cuotas iguales.

## Registro

- 2026-11-17 · claude · Plan, implementación y pruebas. Pasa a QA.
- 2026-11-17 · revisor · QA r01 APTO con tres bajos; subsanados en la ronda de cierre y comprobados por el mismo revisor. CERRADO.
