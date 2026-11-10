# Revisión independiente — V0.60 (robustez de los seis validadores de mensajes)

Estado: **revisión ejecutada el 9 de noviembre de 2026 y cuatro hallazgos corregidos** (sección 0 de las
directrices). La revisión se hizo en otra conversación, con el ZIP de la pieza ya en verde y el prompt de la
sección 9, sin el historial de la pieza. El revisor verificó contra el código real, no contra lo que declara
la entrega: (1) el lote completo en su propia ejecución —50 baterías, todas en «TODAS LAS PRUEBAS PASAN», sin
una línea FALLA, coincidente con la `salida_pruebas.txt` entregada—; (2) la batería nueva con cuenta exacta
de las 65 comprobaciones por bloque, semilla 20261110, rotación 4:1 del sello, ~30 s y determinismo de dos
salidas byte a byte; (3) la no-vacuidad del defecto_01: restaurada la línea de V0.53, la batería falla
exactamente en la comprobación del defecto y las demás siguen en verde, las baterías antiguas del camino del
sobre siguen pasando con la línea antigua y `validar_sobre.py` se restituyó byte a byte; (4) los seis
validadores leídos contra los predicados de la batería (envoltorios con `RecursionError`/`MemoryError`,
`dimensionar` con `Exception` → E-01, `vigilar` capturando por posición e instante, casos fijos del
calendario reales y los seis anidados con estructura fresca); y (5) cinco sondas adversariales propias
(`sondas_revisor_v060.py`, todas cierran). Resultado: **cuatro hallazgos (2 medios, 2 bajos), ninguno de
producto** —los seis validadores se comportaron como promete la pieza en todo lo sondeado—; los cuatro son
de cobertura de la batería y de exactitud del Documento 0 y del LEEME. El informe íntegro del revisor está
copiado en `informe_revision_independiente.md` de esta carpeta.

## Hallazgos y correcciones

| # | Gravedad | Hallazgo | Corrección aplicada | Regresión |
| --- | --- | --- | --- | --- |
| 1 | media | La batería no demostraba «no muta la entrada» para `dimensionar` (ni para el `ahora`/T1 de `vigilar`, donde la foto cubría solo los datos), aunque el Documento 0 y el LEEME prometían las cuatro promesas para los seis validadores. El producto quedó limpio en la sonda del revisor (300 casos sin mutación) | Foto con `_igual_nan` de las CUATRO entradas en el bucle de E (500 casos) y de T1 en H (200 casos), con su contador y comprobación; §2 punto 2 del Documento 0 y LEEME ajustados a lo que la batería hace | `r01_dimensionar_no_muta_ninguna_de_sus_cuatro_entradas_en_500_casos`, `r01_vigilar_no_muta_ahora_en_200_casos` |
| 2 | media | Claves del contexto que el Orquestador pasa SIEMPRE sin mutar: `sc3` y `sello_encargo` (sobre, camino V-26) y `autoria_c`/`autoria_contradictor` (informe). El §1 prometía «cada clave de su contexto» y el §2 punto 4 enumeraba mal lo que `validar_sobre` lee. El producto falla cerrado en las sondas (sc3 o sello_encargo corruptos → V-01) | `sc3` y `sello_encargo` entran en la rotación del sobre con la vista SC-3 reconstruida por base (`_vista_sc3_de`, una entrada por artefacto citado; ADMITE V-01/V-26; None o vista legible se admite sin regla) y la autoría del informe, en cinco casos fijos; §1 y §2 punto 4 corregidos | `r02_informe_valido_con_la_autoria_que_pasa_el_orquestador`, `r02_autoria_c_mal_formada_…`, `r02_autoria_contradictor_de_forma_rota_…`, `r02_autoria_contradictor_con_dict_mal_formado_falla_cerrado_C01`, `r02_autoria_contradictor_de_otro_modelo_dispara_C11` |
| 3 | baja | `_forma_real` reclasificaba TODO borrado de elemento de lista como «de valor» sin mirar el mínimo: los borrados que dejan la lista vacía o por debajo de su `minItems` rompen la forma del esquema y la batería dejaba de exigir ahí la regla de esquema. El validador de verdad sí falla cerrado en los seis casos sondeados (V-01/C-01/S-01) | Los borrados que dejan la lista vacía o bajo su mínimo vuelven a ser «de forma» en los objetivos MENSAJE, con tablas de mínimos POR MENSAJE (`_MIN_ITEMS`, de los cuatro esquemas 0.2.0; `data_refs` tiene mínimo en el sobre y el encargo pero no en el informe), y los casos de las listas con mínimo de los cuatro mensajes quedan fijados uno a uno (once casos, incluidos `exclusiones` y `instrumentos`) | `r03_borrados_que_dejan_la_lista_bajo_su_minItems_dan_la_regla_de_esquema` |
| 4 | baja | La promesa «toda mutación de valor del sello que respeta la forma da al menos S-12» era falsa para `estado`: `hash_del_sello` excluye `hash_sello` y `estado` («cambia en la vida del sello»), de modo que VIGENTE→CADUCADO dentro del enum deja el sello VÁLIDO y sin S-12; el consumidor lo ve con E-16. La conducta es defendible y por capas; faltaba declarar la excepción como las demás | Excepción declarada en el §2 punto 3 y la §3 del Documento 0 y en el LEEME, y comportamiento real fijado: estado alterado dentro del enum → sello VÁLIDO sin S-12, y el encargo que cita ese sello lo rechaza con E-16 | `r04_sello_con_estado_alterado_en_el_enum_sin_S12_el_hash_lo_excluye`, `r04_el_encargo_ve_el_estado_alterado_del_sello_con_E16` |

Ademas, dos observaciones del revisor quedan anotadas como límites en el Documento 0 §5: la autoría de forma
rota (lista) se queda sin comprobación de coherencia en silencio (sin camino práctico: el Orquestador valida
su configuración con `_autoria_ok`; distinguir «ausente» de «mal formada» queda para una pieza futura) y la
granularidad gruesa de los predicados `_afecta_*` es fragilidad de prueba, no de producto. El ajuste de
`_calendario_afecta` a cualquier operación sobre los festivos de un mercado declarado (no solo borrar) sale
de la misma observación: no puede producir discrepancia detectable con lo declarado.

## Resultado tras corregir

- La batería queda en **75 comprobaciones** (las 65 de la pieza y las 10 de regresión r01–r04) y sigue
  determinista: dos ejecuciones consecutivas con salida idéntica byte a byte.
- El lote completo en verde de nuevo: 50 baterías (las 49 de V0.53 y la nueva), todas en «TODAS LAS PRUEBAS
  PASAN», sin una sola línea FALLA (`salida_pruebas.txt` de esta carpeta, regenerado tras las correcciones).
- Los cinco guiones del revisor, intactos byte a byte en la raíz de `marcoC/` y ejecutados desde ahí: los
  cuatro `hallazgo_*` terminan en **exit 0** y `sondas_revisor_v060.py` cierra sus cinco sondas.
- Sin cambios de esquema del código ni de configuración, sin tocar el Orquestador y sin borrar ni debilitar
  ninguna prueba existente: solo se añaden comprobaciones. `Deuda_tecnica.md` queda intacto (ningún hallazgo
  abre fila: ninguno era de producto y ninguno queda sin corregir).
