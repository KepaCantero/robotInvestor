---
id: claude/2026-11-09_lecciones-integracion
autor: claude
fecha: 2026-11-09
tipo: leccion
etiquetas: [integracion, git, otro-agente]
fuente: integración de la V0.53 (commit df6a0da)
vigencia: vigente
---

- **Fusión a tres bandas.** Para integrar trabajo hecho por otro agente sobre una versión anterior, se monta un repositorio de trabajo con tres ramas: la base común, la del otro agente y la propia. Después se fusiona, se resuelven los conflictos y se pasan todas las suites de las dos líneas.
- **Cuidado con los cambios de permisos.** Un checkout con diferencias solo de modo de archivo (permisos) revirtió en silencio cambios del otro agente. Antes de fusionar, igualar permisos (`chmod`) y comprobar el diff de contenido.
- **Los scripts del otro agente pueden traer rutas de su máquina** (como `/home/z/...`). Cámbialas por rutas relativas (`Path(__file__).parents[n]`).
- **Después de integrar, se revisa** lo integrado con un revisor independiente, como cualquier versión. La de GLM encontró fallos reales que se corrigieron con pruebas.
