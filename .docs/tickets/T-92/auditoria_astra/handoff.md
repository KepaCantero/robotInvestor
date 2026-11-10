# Traspaso a Claude · T-87

**Rama local:** `astra/bloque-a-integridad-y-evidencia`. **Base:** `bc90534`. Estado: preparado para QA independiente. Este trabajo no reabre T-53 o T-66 ni autoriza su conexión a dinero real.

1. En esta copia, inspeccionar `git log --oneline bc90534..HEAD` y `git diff --stat bc90534...HEAD`. Para llevarla a otro clon **local**, desde ese clon usar `git fetch /ruta/a/RoboInvestor-Bloque-A refs/heads/astra/bloque-a-integridad-y-evidencia` y revisar `FETCH_HEAD` en un worktree independiente. Un fetch local no altera los archivos de trabajo.
2. Leer las matrices [datos](datos.md), [agentes](agentes.md), [contratos](contratos.md) y [controles operativos](controles.md). Distinguen defectos previos ya corregidos, cambios nuevos, compatibilidad y límites. Los comandos están en [pruebas](pruebas.md).
3. Reproducir desde otra copia sin caché ni claves. Prioridades de revisión: (a) al cambiar una observación de precio publicada después de la emisión, la base congelada no se mueve; (b) un método histórico desconocido no autoriza probabilidades numéricas; (c) al variar corte, evidencia, origen del cliente o prompt, no se reutiliza indebidamente el resultado; (d) una petición repetida, una escritura interrumpida y un CT-24 forzado no eluden los controles.
4. Para A→B, comprobar tanto un universo coincidente y confirmado por el Broker como un destino ausente, revocado o erróneo. La herramienta prepara una petición de revisión; el proyecto global CT-G y la ejecución de B son piezas distintas.
5. Anotar veredicto y hechos reproducidos en `qa.md`; si la rama principal se mueve, validar la combinación con esa nueva base antes de integrar. No reejecutar sobre la única copia de un estado real. Para ensayar la migración, usar una copia cerrada y completa del estado y probar una segunda apertura y un fallo controlado.

**Decisiones que no se han tomado por el operador.** Se respetan el corpus congelado, la aprobación de certificados y la activación de perfiles de T-66. Las pruebas del SDK son locales y simuladas. Sin una evaluación prospectiva independiente aún no hay una estimación de capacidad predictiva real ni una aprobación para uso financiero.
