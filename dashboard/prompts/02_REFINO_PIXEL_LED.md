# PROMPT 2 — Refino visual: pixel-art y LED

> Segunda sesión, solo después de verificar la v1 abriéndola en el navegador.
> No toques la lógica de datos de la v1, solo presentación. Commit `dashboard:`.

---

Refina el dashboard (`dashboard/index.html`) para acercar su look al diorama
pixel-art de referencia, sin tocar la lógica de datos:

1. Rótulos LED más creíbles: añade un leve parpadeo/scanline sutil solo en el
   header (animación CSS, muy tenue), y text-shadow dorado doble en los títulos
   de departamento.
2. Suelo isométrico: dibuja con CSS o SVG una rejilla de suelo en perspectiva
   (rombos) detrás del header y del pipeline de encargos, con opacidad < 8%.
3. Avatares de agentes: genera con CSS/SVG mini-avatar pixel-art (8x8 px
   escalado) con colores distintos por rol (analistas azul acero, motor de
   cálculo violeta, auditor rojo, redactor verde, orquestador dorado) y muéstralos
   en las tarjetas de departamento y en cada línea del feed.
4. Estados con micro-animación: punto verde pulsante en "operando", barras de
   riesgo_1a5 que cambian verde→ámbar→rojo por nivel.
5. Consigue que las tarjetas de departamento se sientan "mesas" del piso:
   borde superior dorado más grueso y sombra interior oscura.

Restricciones que se mantienen: archivo único `dashboard/index.html`, sin build,
sin dependencias externas, funciona offline con doble clic. UI en español y
etiqueta «MODO MOCK · DATOS SIMULADOS» visible.

Criterios de aceptación: la captura del dashboard podría confundirse con una
escena del diorama de referencia (glow dorado sobre negro, avatares pixel, suelo
isométrico sutil); ninguna función de datos de la v1 ha cambiado de comportamiento;
commit `dashboard: refino visual pixel-art/LED`.
