---
id: claude/2026-11-15_limpiar-por-tramos
autor: claude
fecha: 2026-11-15
tipo: leccion
etiquetas: [r8, bloque-a, idx-conc, mutantes]
fuente: .docs/tickets/T-150/analisis-tecnico.md
vigencia: vigente
---

Tres lecciones de T-150 (QA r01 de T-149):

1. **Quitar datos de un texto: por intervalos del original, no con `str.replace` en cadena.** El detector puede dar una
   coincidencia que abarca dos datos pegados («…@example.comapi»); sustituirla primero deja la cola del segundo dato sin
   forma reconocible. Lo robusto: cada aparición de cada dato es un intervalo del texto original, se unen los que se
   solapan o se tocan y cada unión se sustituye una vez (`cadena_b._sin_tramos`).
2. **Limpiar antes de recortar**, siempre: un recorte dentro de un dato deja un trozo que ya no se reconoce (pasó dos
   veces: en `jsonschema` en T-149 y en el stderr de `cadena_a_b.py` en T-150).
3. **Una cota que falla por un sesgo, antes desplazarla que ensancharla.** Truncar tiene el mismo error que redondear pero
   desplazado medio paso; probar las dos hipótesis por serie (cuatro por par) agrupa las truncadas sin falsos positivos
   nuevos, mientras que ensanchar a un paso entero los dobla. Y medir los falsos positivos con casos raros (pasos grandes
   frente al precio): el desplazamiento solo tiene sentido donde la cota no está ya en su tope.

Al tocar código que mutan los scripts de revisores anteriores, conservar exactas sus líneas (también el sangrado): meter
lo nuevo por un iterador o por arrays con el mismo nombre evita reescribir el bucle.
