# Revisión independiente — V0.62 (robustez de la infraestructura T-03)

Estado: **revisión ejecutada el 9 de noviembre de 2026 y cuatro hallazgos corregidos** (sección 0 de las
directrices). La revisión se hizo en otra conversación, con el ZIP de la pieza ya en verde y el prompt de la
sección 9, sin el historial de la pieza. El revisor verificó contra el código real, no contra lo que declara
la entrega: (1) el lote completo en su propia ejecución —52 baterías, todas en «TODAS LAS PRUEBAS PASAN»,
sin una línea FALLA, coincidente con la `salida_pruebas.txt` entregada—; (2) la batería nueva corrida dos
veces con salida idéntica byte a byte, con recuentos propios (39 comprobaciones; 870 casos por constantes y
rotación exacta); (3) el contraste de cada `esperados` de la batería con lo que los módulos T-03 devuelven
de verdad (lectura de `persistencia.py`, `diario.py`, `migraciones.py`, `reloj.py` y `rotacion.py`); y (4)
cinco sondas adversariales propias (`sondas_revisor_v062.py`, en la raíz del árbol): un barrido de 60
semillas × 24 casos por objetivo (1.440 por objetivo) para medir la fragilidad de las expectativas, casos
construidos a mano sin azar y las dos sondas de no-vacuidad repetidas sobre copias temporales. El informe
íntegro del revisor está copiado en `informe_revision_independiente.md` de esta carpeta. Resultado: **cuatro
hallazgos (uno medio, tres bajos), ninguno de producto**: los cinco módulos T-03 cumplen las cuatro promesas
en todo lo ejecutado y la batería es determinista, no-vacua y fiel al diseño en 36 de sus 39 comprobaciones;
los hallazgos 1 a 3 son de la batería (expectativas), el 4 es de la entrega. El auto-repaso previo a la
entrega (Documento 0, §4) no sustituía a la revisión y así quedó: la revisión destapó el resto de lo que ese
auto-repaso venía corrigiendo en tres sitios.

## Hallazgos y correcciones

| # | Gravedad | Hallazgo | Corrección aplicada | Regresión |
| --- | --- | --- | --- | --- |
| 1 | media | **Cuatro `esperados` más estrechos que el contrato real del módulo: la batería podía fallar en falso con otra semilla.** Los cuatro objetivos que mutan el documento ENTERO (`diario_estado`, `migraciones_texto`, `rotacion_texto` y `rotacion_sin_firmar`) pueden caer en la cabecera, y una cabecera con `formato` cambiado por otro texto da PE-03 (`persistencia.py:315-316`), que no estaba admitido. Medido por el revisor con 60 semillas × 24 casos por objetivo: entre el 55 % y el 68 % de las semillas darían un fallo falso en el objetivo del diario; la entrega pasó con la semilla 20261111 tras una tirada con ~2/3 de probabilidad de salir mal | PE-03 añadido a los `esperados` de los cuatro objetivos. PE-04 y PE-08 revisados por la misma vía: **no son producibles aquí** — la forma exige el conjunto EXACTO de claves del documento (un veneno da PE-01, no un formato 0.1.0 ni un esquema distinto) y la huella va antes que montar (PE-04 necesita la huella intacta) —, barrido propio de la corrección (300 semillas × 6 casos, 1.800 casos por objetivo, sin lanzamientos) sin verlos ni una vez: no se añaden | `r01_los_esperados_cubren_todo_lo_que_el_modulo_puede_responder`: barrido con 25 semillas nuevas (20261112…20261136) × 6 casos por objetivo y semilla sobre los 15 objetivos con `esperados`, con los MISMOS generadores de la batería: códigos observados ⊆ esperados y ok solo donde el objetivo lo admite (en la batería entregada, r01 habría fallado en los cuatro objetivos) |
| 2 | baja | **La sonda de no-vacuidad de la huella no fallaba «exactamente» en las dos comprobaciones declaradas, sino en cuatro.** Con `_huella` desactivado (sonda S2 del revisor), además de `persistencia_falla_cerrado_con_la_regla_correcta_en_240_casos` y `persistencia_toda_mutacion_del_estado_sin_rehacer_huella_es_PE02_o_PE01_nunca_ok` también caían `diario_el_estado_tocado_no_abre_…` (el estado tocado carga y el punto ya no cuadra) y `rotacion_un_texto_mutado_no_se_rota_…` (el caso `sin_firmar` llega a responder códigos de un estado que la huella impedía). Contradecía al «exactamente» de revision.md, del Documento 0 §5 y de notas_briefing; la frase del LEEME («falla en las comprobaciones de PE-02») sí era cierta | Las tres frases ajustadas a lo que la sonda muestra de verdad. Sobre la batería corregida, S2 muere en **cinco** comprobaciones: las dos de PE-02, la del estado del diario, la de rotación sin firmar y la regresión r01 (los casos de estado responden O-13 con la huella desactivada); la sonda del diario (S3) muere en **tres**: las dos declaradas de DI-02 y r01 (una línea tocada se cuela como OK). Las frases de la entrega original decían «exactamente en dos» en los tres sitios, y se corrigen todas | Ninguna (documental); r01 vigila el fondo |
| 3 | baja | **Franquicias muertas en los `esperados`, descritas en los documentos como si fueran alcanzables.** (a) PE-07 en `rotacion_claves`: `_previas` (`rotacion.py:66-77`) da CL-01 para toda clave inválida ANTES de que `cargar` pudiera dar PE-07 (los cuatro combos a mano del revisor dan CL-01). (b) El OK de la «última línea mutada» del diario es inalcanzable: la batería escribe siempre el salto final, así que la última línea mutada es DI-02 siempre (30/30 en el revisor; 1.800/1.800 en el barrido de la corrección); el OK de la «regla del corte» solo llega con un fichero SIN salto final, caso que ese objetivo no construye (lo cubre el caso fijo de la línea cortada). (c) MG-02 en `migraciones_registro` (con el esquema actual el camino no llega a mirar el registro y `_registro_ok` no lanza), PE-02 y CL-02 en `rotacion_texto` (la firma se comprueba antes que la huella, y sin carga no hay rotación que se caiga), CL-02 en `sin_firmar` y PE-06 en `diario_estado` (el documento va sin firmar) | Franquicias muertas retiradas de los seis `esperados`; la cabecera de la batería y el Documento 0 (§2) dejan de citarlas como activas y anotan por qué son muertas. Ninguna causa fallos falsos (eran permisivas): los esperados resultantes son los que r01 vigila | Ninguna (documental) |
| 4 | baja | **Tres verificaciones declaradas no eran reproducibles desde el ZIP:** «diff por fichero frente al ZIP de V0.61», «sin borrar ni debilitar ninguna prueba antigua (regla 7)» y «`Deuda_tecnica.md` queda intacto» exigen el estado anterior, que no viaja; tampoco viajaba `corre_baterias.py`, citado en la cabecera de `salida_pruebas.txt`. Todo lo que SÍ era verificable desde el ZIP salió en verde (§1 del informe del revisor) | `manifiesto_sha256.txt` nuevo en esta carpeta con el SHA-256 de los 107 ficheros heredados sin cambios (`validador/`, `esquemas/`, `pruebas/` salvo la batería de la pieza y los ficheros de revisiones anteriores en la raíz): la corrección lo verificó byte a byte contra el ZIP pos-revisión de V0.61; `corre_baterias.py` añadido a la raíz del árbol; Documento 0 §5 cita que el contenido de la deuda viaja resumido en `notas_deuda.md` de esta carpeta | Ninguna (documental) |

**Ningún hallazgo es de producto:** ninguna conducta de `validador/` ni del Orquestador cambia; en todos
los barridos y casos construidos los cinco módulos respondieron con códigos previstos por SU contrato
(PE-03 ante una cabecera mentirosa es exactamente lo que `verificar` documenta) y ninguna de las cuatro
promesas quedó refutada.

## Observaciones del revisor, todas atendidas

1. `cargar_de` y `verificar` se ejercitan de forma transitiva o ligera (como `cargar` las envuelve, la
   cobertura real es buena): la cabecera de la batería ya no da a entender que son objetivos directos, y el
   Documento 0 (§2) lo matiza. Sin cambio de comprobaciones.
2. Los casos «estado» del diario restauraban el fichero de estado pero no el de diario (quedaba el del caso
   «línea» anterior, también mutado): el caso de «estado» restaura ahora LOS DOS ficheros, y con ello el
   caso solo depende del estado (con los módulos en su contrato no cambiaba nada, porque el estado falla
   antes de leer el diario, pero complicaba razonar las sondas).
3. La frecuencia del hallazgo 1 depende del tamaño del estado (más atributos → menos probabilidad por caso
   de caer en la cabecera): la regresión r01 no depende de eso.
4. La promesa «la batería entera, la misma salida byte a byte» se mantiene con la semilla y el código
   congelados: al corregir la batería se REGENERÓ `salida_pruebas.txt` y se actualizaron la frase de
   determinismo y todos los recuentos (39 → 40 comprobaciones; ~11 s → ~21 s).

## Resultado tras corregir

- La batería queda en **40 comprobaciones** (las 39 de la pieza y la regresión r01) y sigue determinista:
  dos ejecuciones consecutivas con salida idéntica byte a byte (~21 s de reloj; la pieza declaraba ~11 s
  sin r01).
- El lote completo en verde de nuevo: **52 baterías**, todas terminan en «TODAS LAS PRUEBAS PASAN» y sin
  una sola línea FALLA (`salida_pruebas.txt` de esta carpeta, regenerada tras las correcciones).
- **No-vacuidad de la regresión, verificada revirtiendo la corrección a medias**: estrechar de nuevo el
  `esperado` del estado del diario en r01 (quitando PE-03) hace fallar r01 con un PE-03 observado (semilla
  20261124, en copia temporal). Las sondas del revisor re-ejecutadas sobre el estado corregido: S1 (60
  semillas × 24 casos por objetivo) queda limpia contra los esperados CORREGIDOS —los códigos observados de
  los diez objetivos están dentro de los nuevos `esperados`; el «FUERA» que imprime la sonda es contra sus
  esperados congelados de la entrega original, que es exactamente el defecto demostrado y corregido—; S1b
  (casos a mano) confirma que el PE-03 de los cuatro objetivos, el CL-01 de las claves y el DI-02 de la
  última línea son los únicos códigos posibles en esos puntos; S2 y S3 caen como se describe en el hallazgo 2.
- Sin cambios de producto: ni el Orquestador ni ningún módulo de `validador/` cambian (el manifiesto
  SHA-256 de esta carpeta, verificado contra el ZIP de V0.61 pos-revisión, lo deja demostrable desde el
  propio ZIP); el diff V0.62 → V0.62 pos-revisión toca solo `pruebas/pruebas_robustez_t03.py`, `LEEME.md`,
  los documentos de `entrega_glm/V0.62/` y los añadidos de la revisión (`corre_baterias.py` y
  `sondas_revisor_v062.py` en la raíz; `informe_revision_independiente.md` y `manifiesto_sha256.txt` en
  esta carpeta).
