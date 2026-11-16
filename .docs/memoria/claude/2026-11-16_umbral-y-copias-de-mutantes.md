---
id: claude/2026-11-16_umbral-y-copias-de-mutantes
autor: claude
fecha: 2026-11-16
tipo: leccion
etiquetas: [mutantes, bloque-a, idx-conc, umbrales, qa]
fuente: .docs/tickets/T-152/analisis-tecnico.md
vigencia: vigente
---

Tres lecciones de T-152 (QA r01 de T-150):

1. **Una copia desechable para mutantes ha de ser completa** (`git archive HEAD | tar -x` y los cambios encima). Si solo se copian `bloque_a` y
   `.docs/scripts`, falta `bloque_b/11_Ejecutor/config/ambitos_ejemplo.yaml` y todos los mutantes «mueren» por ese fallo, incluidos los
   equivalentes. Antes de leer un resultado, comprobar que la copia sin mutar pasa las pruebas, y desconfiar de que todos mueran a la vez
   en menos de un segundo.
2. **Un umbral solo se puede fijar donde cambia el resultado, y «no cambia nada por encima» hay que medirlo en los bordes.**
   Medir primero, con un barrido de umbrales y de tramos (`T-152/medir_umbral.py`), antes de escribir la prueba del borde, y declarar su
   resolución. Error de T-152 (QA r01, H-01; corrección en T-190): declaré equivalente un umbral más alto porque los tramos de precio
   medidos no cruzaban el 2 % de q/p. Una serie que cruza el 2 % por poco ([0,48, 0,9] con paso 0,01) sí cambia de resultado. Medir
   también tramos que cruzan el umbral, no solo tramos a un lado.
3. **Una decisión del operador que llega con la QA ya lanzada:** detener la QA y revisar la versión definitiva, en vez de dejarla terminar
   sobre código que va a cambiar. Así se revisa una vez.
