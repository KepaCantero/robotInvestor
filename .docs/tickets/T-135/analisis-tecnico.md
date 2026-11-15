# T-135 · Análisis técnico

## Causa raíz o motivo

- **T-128 H-05 (media).** En IDX-CONC-001 el mínimo `IDX_CONC_COMPONENTES_MINIMOS` (T-128 r02) contaba **series**, no
  series distintas: con C00 y una copia suya (exacta o ×0,5) había 2, y la amplitud (porcentaje sobre la media y línea de
  avance y retroceso) era la de C00 (la línea, el doble). La contribución sí agrupaba por la misma cifra (`_concentradas`);
  la amplitud no aplicaba ninguna regla de copias. La prueba `test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido`
  fijaba el caso (`{"C00": largo, "C01": largo * 0.5}` → 1,0) como correcto.
- **T-128 H-06 (baja).** La dominancia por grupos de copias de CHR-FLOW-001 (`_sin_dominio(..., grupos)`) no tenía prueba.
- **T-127 H-06 (baja).** La firma del aviso de CHR-TOKEN-001 (precio, circulante, total, máxima, emisión, quema) tiene cuatro
  datos que en tokens reales coinciden a menudo sin informar (la máxima es la total o no la hay, la total es la circulante,
  emisión 0, quema 0): dos tokens de oferta fija y redonda solo difieren en el precio y daban el aviso.
- **T-127 H-07 (baja).** REI-NAV-001 metía en la firma `otros_pasivos` **derivados** (GAV − deuda − NAV) cuando faltaban:
  al mover el NAV por acción, el derivado se movía solo y la firma cambiaba en dos datos.
- **T-127 H-08 (baja).** El docstring de `frontera_b.py` (líneas 5 a 7) mantenía la frase absoluta.

## Evidencia

- Antes: `r02_01_chr_flow_e_idx_conc.py` (T-128) **16/18** (las dos FALLA de IDX-CONC con la copia exacta y a escala);
  `r03_01_cota_aviso_y_origen.py` (T-127) **10/11** (A3: falso aviso; A4: «sin aviso»). Después: **18/18** y **11/11**
  (A4: «con aviso o rechazo», 1 aviso). Comandos en `pruebas.md`.
- Con los módulos del Motor de `eb66257` (`impl_mutantes.py --base eb66257`), 16 de las 28 pruebas nuevas fallan (todas las de
  H-05, H-06 de T-127, H-07 y H-08; la de T-128 H-06 pasa porque el código ya era correcto: es la del mutante).

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`: docstring matizado (H-08) y con la regla de series; `AVISO_B`
    gana `coincidencias_informativas_minimas: 2` con su motivo `[PROPUESTO INC-T127-01]`; `_aviso_casi_clones` exige esas
    coincidencias no triviales (H-06); nueva `_etiquetas_series_copiadas` (H-05).
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_mon_idx.py`: IDX-CONC-001 agrupa sus series de precios por rentabilidades
    y aplica el mínimo y la dominancia por grupos a la amplitud y al porcentaje sobre la media (`_distintos_y_dominio`).
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_p2.py`: CHR-TOKEN-001 construye `firmas_aviso` (H-06); los casi clones
    (`_sin_clones`) siguen con la firma de antes.
  - `bloque_a/11_Ejecutor/bloque_a/motor/fichas_reales.py`: REI-NAV-001 marca `otros_derivados` y la firma del aviso lleva
    los datos aportados (H-07).
  - `bloque_a/11_Ejecutor/tests/test_t135_motor.py` (nueva, 28 pruebas); `tests/test_t128_r02.py` (la prueba de H-05,
    comentada «T-135») y `tests/test_t127_r03.py` (la aserción de `AVISO_B`, comentada «T-135»).
  - `bloque_a/11_Ejecutor/README.md` (limitación 3), `docs/incidencias.md` (INC-T128-01 e INC-T127-01, «Ronda T-135»),
    este ticket, `revisores/impl_mutantes.py` (27 mutantes) y `revisores/impl_frecuencia_aviso_token.py` (frecuencia del aviso).
- **Decisiones (todas `[PROPUESTO]`, por defecto):**
  - **H-05, por qué las rentabilidades.** Son la cifra de una serie que no depende de su escala (como los cocientes de
    `_sin_copias_a_escala`), y lo único que usa la amplitud (el signo de la rentabilidad y la posición frente a la media
    propia, invariantes a la escala). Se comparan en las fechas en que **las dos** tienen rentabilidad (así una copia
    recortada en el tiempo también es copia), con la tolerancia de los casi clones (1 % relativo al mayor, la de
    `_datos_que_coinciden`) y cierre transitivo. Para no tomar por copias dos series casi sin fechas en común, sus precios
    comunes tienen que abarcar al menos `anios_precios_min` (1 año): es la entrada mínima de la ficha («precios de los
    componentes ≥ 1 año para amplitud») y un umbral fijo (la petición no lo cambia). Ningún número nuevo.
  - **H-05, mínimo y dominancia, no deduplicar.** Se pidió que un grupo de copias cuente como un componente para el mínimo.
    Además se aplica la dominancia (1, k) de `FRONTERA_B` con el mismo peso por serie: sin ella, C00 con 20 copias y otro
    valor daría su porcentaje y su línea (las copias serían 20 de 21). El cálculo sigue contando cada serie (el método (ii)
    cuenta componentes): deduplicar habría cambiado las cifras de `test_idx_conc_valores_a_mano` (X e Y iguales), que siguen
    igual. El porcentaje sobre la media usa los grupos de las series con 200 sesiones.
  - **H-05, con la ficha del Catálogo** (leída solo IDX-CONC-001): «Salidas» pide la amplitud; «Supuestos y limitaciones»
    dice que los componentes son datos de composición, nunca candidatos a selección (1.6); no fija un mínimo. Dejar la
    amplitud en `null` con su limitación cuando sería la de un valor es un fallo cerrado compatible; la concentración (peso
    de los n mayores, HHI, N_ef, HHI sectorial), que es lo que la ficha mide, y su verificación no cambian (prueba).
  - **H-06 de T-127, dos cambios.** (1) Regla común: las coincidencias triviales (``None``/``None``, 0/0) siguen contando para
    «todos menos d» (así el criterio de antes no cambia), pero hace falta además coincidir en `d + 1` = 2 datos no triviales:
    lo que coincide pesa más que lo que se permite mover. Solo quita avisos (en FIR-CRED, REI-LEV y REI-NAV no cambia ningún
    caso del revisor). (2) En CHR-TOKEN-001, la firma del aviso deja en ``None`` lo que repite otro dato (total = circulante,
    máxima = total o ausente) y añade el *staking* y la concentración declarados, que distinguen a dos tokens. Sin el (2),
    dos tokens de 1e9 fijos sin *staking* coinciden en tres datos no triviales (las tres ofertas) y el aviso seguiría. Se
    descartó «exigir que el dato distinto difiera poco»: necesitaba otro número sin origen (la perturbación de la r02 llega
    al 10 %).
  - **H-07, la firma son los datos de quien pide.** Con `otros_pasivos`, el GAV es el derivado (la identidad lo fija) y va
    como ``None``; sin ellos, son los otros pasivos los derivados y entra el GAV. Así la firma tiene siempre los mismos datos
    aportados, y el criterio de la r03 («el GAV no entra porque lo fija la identidad») se mantiene cuando se aportan.
- **Desviaciones del plan:** ninguna en el alcance. La regla de copias de la amplitud lleva también la dominancia (arriba).
- **Límites conocidos:**
  - una copia de una serie con las rentabilidades perturbadas a propósito (más del 1 % en una sesión) o muestreada en otras
    fechas no se detecta: el límite declarado de INC-T127-01 r03 (componentes construidos a propósito);
  - dos líneas de cotización de un mismo emisor con las mismas rentabilidades cuentan como una (coste, deseable para 1.6);
  - CHR-TOKEN-001: dos tokens reales con la misma oferta circulante y total redondas y sin *staking* ni concentración siguen
    dando el aviso (2 datos que informan); con el generador A2 del revisor llevado a la firma de la ficha, 5,8 % de las
    peticiones de 20 tokens (antes 45,8 %) y 0 % si declaran *staking* y concentración. Una copia de un token de oferta fija
    y entera en circulación sin *staking* ni concentración, con el precio movido, no da el aviso (solo tiene 2 datos que
    informan; su copia a escala la agrupa igual, ronda r02 de T-127);
  - fuera del alcance (observación): `fichas_mon_idx._params` acepta claves desconocidas en la petición (las de `FRONTERA_B`
    se ignoran: IDX-CONC las lee del módulo). FIR-CRED y las de `fichas_reales` las rechazan. No se cambia aquí.
- **Comandos exactos para probarlo:** en `pruebas.md`.
