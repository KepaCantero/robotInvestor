---
id: claude/2026-11-16_orden-bajos-sin-qa
autor: claude
fecha: 2026-11-16
tipo: decision
etiquetas: [operador, qa, tickets]
fuente: conversación con el operador, 16-11-2026
vigencia: vigente
---

Órdenes del operador del 16-11-2026, después del cierre de T-152 con la QA r01 APTO:

- «Haz T-190 también y el resto de hallazgos que pudieran salir. Si son bajos no los pases por QA. Corrígelos tú.»
  - T-190 (hallazgos bajos de la QA r01 de T-152) se corrige sin QA.
  - Lo que salga al corregirlo: si es bajo, también se corrige sin QA. Si es medio o alto, se pasa por QA con un revisor nuevo.
  - La regla vale para la cadena que nace de T-152. No cambia la de los demás tickets: la QA independiente sigue siendo la norma.
- Antes: «Acepto subir el umbral». El umbral del desplazamiento de la hipótesis truncada de IDX-CONC-001 pasa a q/p ≤ 2·`tolerancia_clon` (T-152, INC-T127-01).
- Después de esta cadena se vuelve a parar, como tras T-133, hasta que el operador diga otra cosa. Siguen pendientes T-137, T-153, T-155 y T-170.
