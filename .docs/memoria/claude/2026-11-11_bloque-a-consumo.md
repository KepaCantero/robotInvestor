---
id: claude/2026-11-11_bloque-a-consumo
autor: claude
fecha: 2026-11-11
tipo: contexto
etiquetas: [bloque-a, consumo, arquitectura]
fuente: .docs/scripts/medir_consumo_a.py y .docs/diseno/bloque_a/propuesta_claude.md
vigencia: vigente
---

Medida con el cliente simulado (ciclo C1, datos sintéticos, as_of 2024-03-29):
- solo divisas (configuración por defecto, Fase 1): 8 llamadas, unos 184.000 tokens de entrada;
- los doce perfiles activos (`--config` con `perfiles.activos` a los doce): 77 llamadas a 20 agentes, 1.662.000 tokens de entrada, el 90 % prompts de sistema. Hipótesis contrarias (Opus) hace 19 llamadas y 387.000 tokens; los doce analistas, 593.000; Prospectiva, 291.000; Curador, 150.000.
- Solo entrada, a precio de lista: unos 3,9 $ sin caché, 2,3 $ con la caché actual y 2,1 $ cacheando solo lo que se repite.

Por qué importa: el coste de A crece con cada perfil que se activa. El operador pidió revisar si en A se fue conservador; la respuesta es sí (PA-06 y PA-07 de T-53 aplazados en T-67). El rediseño propuesto (6 papeles de IA, GC1 por código, núcleo más kits) está en `.docs/diseno/bloque_a/`, y el de B (5 papeles) en `.docs/diseno/bloque_b/`. Ambos están pendientes de la revisión de Astra y de la decisión del operador.
