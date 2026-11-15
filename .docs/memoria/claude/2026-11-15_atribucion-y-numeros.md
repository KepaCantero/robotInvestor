---
id: claude/2026-11-15_atribucion-y-numeros
autor: claude
fecha: 2026-11-15
tipo: leccion
etiquetas: [git, commit_limpio, tickets]
fuente: commits de develop del 15-11-2026 (de 010108a a 92c1c12)
vigencia: vigente
---

**Líneas de atribución.** `commit_limpio.sh` añade las líneas finales del commit solo si `.env` define `GIT_TRAILERS`. En las sesiones en la nube no hay `.env`, así que hay que escribirlas en el propio mensaje: `Co-Authored-By` y `Claude-Session`, las que diga la sesión. El 15-11 salieron unos diez commits sin ellas, de 010108a a 92c1c12. No se reescribe el historial, porque otra sesión sube a la misma rama.

**Números de ticket.** Con otra sesión en la misma rama, un número reservado en el árbol local no está reservado hasta que se sube. El 15-11 las dos sesiones cogieron T-153 a la vez. Antes de reservar, conviene mirar `origin/develop` (la deuda y `.docs/tickets/`) y subir la reserva cuanto antes. Si hay colisión, se renumera el propio y se conserva el ajeno.

**Falso «subido».** Un bucle que da por hecho el push porque `git status -sb` no dice «ahead» se engaña durante una rebase a medias: con HEAD separado no aparece «ahead». Hay que comprobar `git status` completo, o el estado contra `origin/develop` después de `fetch`.
