# Pausa del 17-11-2026 (≈ 00:00): trabajo a medias del Bloque A

El operador pidió parar y guardar todo hasta las 4:10. Los agentes se pararon a mitad. Su trabajo, con lo que tenían sin commit en sus copias, está en `wip.bundle`, uno por rama `wip/<copia>`. Ninguna de esas ramas está en develop ni se ha subido.

## Cómo recuperarlo

```bash
git fetch .docs/tickets/_relevo/wip_2026-11-17/wip.bundle 'refs/heads/wip/*:refs/heads/wip/*'
git worktree add --detach /ruta/copia wip/t143
```

Si el contenedor sigue vivo, las ramas `wip/*` locales y las copias del scratchpad todavía existen. Los ficheros `*.patch` de esta carpeta son una primera instantánea en texto. No se suben, porque los de las QA repiten los del implementador. El bundle es la fuente.

## Estado por ticket y siguiente paso

| Ticket | Rama `wip/` | Estado | Siguiente paso |
| --- | --- | --- | --- |
| T-143 (Documento 0 V5.2) | `t143` (r04 completa, sobre `1ccffd5`) | r04 implementada y probada (H-12..H-15) | La QA r04 se cortó al empezar (`qa143r04`). Hay que relanzarla desde cero con revisor nuevo. |
| T-162 + T-169 (respuesta final CT-03) | `t162` (r02 completa de T-169, sobre `cb92902`) | T-169 r02 implementada (H-01..H-04) | La QA r02 estaba a mitad, esperando los mutantes (`qa169r02`, con sus scripts parciales). Hay que relanzarla. Después se integran T-162 y T-169 juntos, tras T-143, re-congelando `formas_flujos_mock.json`. |
| T-165 (G3-MET-13) | `t165r02` (r02 completa, sobre `5aa9681`) | r02 implementada (H-01..H-12) | La QA r02 acababa de empezar y no dejó ficheros. Hay que relanzarla. |
| T-161 (guías CT-18) | `t161r04` (a medias, sobre `8775dba`) | QA r03 NO APTO (H-11 alto, H-12/H-13 medios, H-14..H-16 bajos; en `qa.md`) | La r04 estaba empezada, con 4 ficheros. Hay que relanzarla partiendo de esa rama o desde develop. |
| T-168 | — | CERRADO | Su commit (`commit_limpio`) estaba en marcha al parar. Si no llegó a develop, hay que repetirlo con los ficheros de `.docs/tickets/T-168/`, la deuda, el diario y la QA r03 de T-161. |

Después siguen T-164, T-166 (tras T-143), T-167 y el resto del plan (`plan_noche_bloque_a_2026-11-15.md`). Cuando entre T-143, se cambia «695» por «696» en `CLAUDE.md` (aprobado por el operador).
