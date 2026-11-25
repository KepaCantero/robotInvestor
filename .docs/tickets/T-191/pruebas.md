# Pruebas · T-191

Pruebas de regresión en bloque_a/11_Ejecutor/tests/test_t191_degradado.py.

Dos ciclos con caída inyectada en la primera o segunda pasada verifican CT-14, HA, F5 y ausencia de pronósticos congelados.

## Ronda r02

La regresión inyecta la indisponibilidad en la frontera de la herramienta y comprueba F6 y F7, el esquema de CT-14, la incidencia, el dictamen, la limitación y la ausencia de F4. Un caso combinado deja a RF sin datos y bloquea el ciclo. La prueba de integridad comprueba precedencia incluso si falla la herramienta al mismo tiempo. El programa de mutantes usa los operadores de Claude, adaptando la captura al tipo de excepción vigente.

En r01 las nueve regresiones nuevas fallaron. En r02 pasaron las nueve. El revisor original detecta siete mutantes y deja sin aplicar el operador que buscaba la antigua captura múltiple. El programa del ticket porta esa mutación al nuevo límite y detecta los ocho operadores del revisor más dos controles propios. Los casos de integridad, permisos y programación del revisor se relanzan. Su caso nominal conserva un RuntimeError genérico que, conforme a H-01, ahora se propaga. Al usar la excepción específica para simular la indisponibilidad pasan las comprobaciones nominales y las de error.
