---
id: claude/2026-11-09_lecciones-marco-c
autor: claude
fecha: 2026-11-09
tipo: leccion
etiquetas: [marco-c, esquema, migraciones, pruebas]
fuente: sistema_global/marco_comun_c/LEEME.md; validador/migraciones.py
vigencia: vigente
---

- **La huella del esquema cambia más de lo que parece.** Cambiar una constante, o importar una (por ejemplo `TOL` en vigilancia), cambia la huella. Después hay que ejecutar `python3 validador/migraciones.py --registrar-esquema V0.xx`; si cambia la forma del estado, también hay que añadir una migración MIG-xxx con su lista `cambia`.
- **La cadena de migraciones es MIG-001 → MIG-004** (la última, V0_51 → V0_53). Las rutas nuevas que llevan datos van en `cambia`; las `PROHIBIDAS` (como `cfg.nivel_autonomia`) no se tocan nunca.
- **Las versiones se comparan como tuplas.** En la V0.51 las pruebas las comparaban como texto y fallaban: como texto, «0.9» va después de «0.10».
- **El primer evento de un estado necesita su instante.** `INICIO` con `ahora=None` rompía la cadena: hay que usar `_primer_instante`.
- **Con sustituciones masivas, revisar el resultado.** Un `re.sub` mal acotado produjo `ESQUEMA_V0.53` en lugar de `ESQUEMA_V0_53`.
- **Pruebas antiguas al cambiar una política** (p. ej. `valor_min_eur`): ajusta los datos de la prueba, no la aserción, y deja constancia en el LEEME.
- **Los revisores encuentran fallos reales.** En la V0.52, el revisor independiente encontró 6 (h01–h06). Sus scripts se guardan numerados (`revNN`) sin sobrescribir y se vuelven a ejecutar tras corregir.
