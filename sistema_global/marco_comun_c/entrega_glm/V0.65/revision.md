# Revisiones — V0.65 (pasada de coherencia contra la Constitución)

## Revisión independiente (hecha el 10 de noviembre de 2026)

La hizo otro GLM en conversación independiente (su informe: `informe_revision_independiente_V0.65.md`),
con el mandato de la pieza: 20 filas de la tabla elegidas al azar (`random.Random(20261113)` sobre los
números de fila), los ocho scripts de los hallazgos ejecutados desde `marcoC` y la búsqueda de requisitos
de la Constitución que la tabla no recoja; más sus sondas propias: lote completo de 54 baterías repetido
por el revisor, regeneración del documento con el generador entregado (idéntico byte a byte), camino
negativo del verificador de citas (cita inventada → exit 1 sin escribir nada) y verificación con `ast` y
con ejecución de las comprobaciones citadas en cada fila muestreada. Límite declarado por el revisor: la
Constitución no viaja en el ZIP, así que el mandato 3 lo hizo con la evidencia interna del árbol.

**Resultado: dos hallazgos documentales bajos y tres observaciones; ninguno de producto.** Las 183 filas
entonces entregadas resistieron la verificación mecánica completa y la muestra de 20 cuadró en citas y
estados; los ocho scripts dan FALLA como declara la entrega.

1. **Hallazgo 1 (baja) — la atribución del falso OK de PC2-06 era injusta con H.** El relato de
   Documento_0 §4, de este fichero (autocontrol, abajo) y de `notas_briefing.md` achacaba el falso OK a
   «la palabra «noticia» en docstrings de H y de pruebas» («el docstring de H-16 habla de «una noticia»»).
   Falso: `validador/` no contiene ninguna ocurrencia de «noti»; el docstring de H-16 habla de «una
   invalidez por una métrica que no es el precio». El «una noticia» real está en un argumento de una
   llamada de prueba: `pruebas_orquestador.py:529` (`o.proponer_sobre_posicion(P, "la tesis parece
   debilitada por una noticia", "H", AHORA)`); los «lectores», en los comentarios de
   `pruebas_robustez_t03.py` (líneas 36 y 226). La corrección técnica que se hizo en su día (acotar el
   barrido a `validador/` con los patrones del servicio) ya era correcta y el script da FALLA.
   **Corrección aplicada (documental):** reescrita la frase en Documento_0 §4, en el autocontrol de abajo,
   en `notas_briefing.md` y en el comentario del propio `scripts/pc2_06_sc11_noticias.py`.
2. **Hallazgo 2 (baja) — la tabla saltaba §9.5 y §9.10 de la Constitución.** Los puntos 5 y 10 de la §9
   («Dónde se aprende de verdad» y «Pronósticos del radar tecnológico») no tenían fila ni mención en todo
   el árbol. Comprobado con la Constitución delante (la que viaja con el kit 2, V0.4 del 7 de noviembre de
   2026): ambos puntos existen, y ambos son de aprendizaje fuera de la Fase 1.
   **Corrección aplicada:** dos filas nuevas en la tabla — §9.5 (FUERA DE FASE 1; el aprendizaje es de I,
   Fase 5; de los «procesos» que cita ya hay soporte parcial: la calidad de datos la mide K y el
   cumplimiento de las condiciones de invalidez lo vigila H-16; el registro sistemático es SC-4, Fase 3) y
   §9.10 (FUERA DE FASE 1; SC-4 es de la Fase 3 y el radar alimenta el registro común de D-23, PC2-05/
   T-68) —, insertadas en su sitio de la §9 y con la tabla renumerada: de 183 a **185 filas** (91 CUMPLE,
   48 PARCIAL, 20 FALTA, 1 CONTRADICE y 25 FUERA DE FASE 1; siguen siendo 160 las que tocan a la Fase 1).
   El documento se regeneró con el generador (verificación de citas en verde) y los recuentos de
   Documento_0, `notas_briefing.md`, `LEEME.md` y `salida_pruebas.txt` se actualizaron.

**Observaciones del revisor (sin corrección exigida; la 5 y la 6 se aplican de cortesía):**

3. Citas de deuda no verificables desde el ZIP (recurrencia del hallazgo 4 de V0.62): la tabla y los
   hallazgos remiten a filas T-xx/P-xx cuyo texto no viaja, y el manifiesto SHA-256 de V0.62 no se ha
   vuelto a usar. Queda para el operador: viajar con `Deuda_tecnica.md` o reactivar el manifiesto.
4. «El registro marca todas las envolturas COMPLETA» (fila 68 y PC2-08) es cierto para las vigentes; dos
   versiones RETIRADA llevan otro valor (CT-G-08 0.1.0 «PARCIAL», CT-G-14 0.1.0 «PROPIA»). No se corrige:
   la fila y el hallazgo hablan de las vigentes.
5. Trazabilidad de subsecciones: el código cita §6.1/§6.2/§6.3 (enfriamiento, anulaciones, límites de
   pérdida) y las entregas de V0.39 citaban §7.3 (cortacircuitos por estrategia) sin que la tabla nombrara
   esas subsecciones. **Aplicado:** las filas de la §6 de esos controles se etiquetan §6.1 y §6.2-6.3, la
   fila del ciclo de vida de estrategias nombra §7.1-7.4 (y señala el §7.3) y la nota de la fila de
   cortacircuitos de la §8 remite al §7.3.
6. Micro-recuento: «hay 50 versiones (V0.14 a V0.64)» — son 51 números si ninguna se saltó, y no es
   verificable desde el ZIP. **Aplicado:** la frase dice ahora «las versiones van de la V0.14 a la
   V0.64», que es lo verificable.

No había nada que corregir en código, esquemas ni pruebas, así que no tocó prueba de regresión (r01); el
lote completo se repitió entero tras las correcciones con el mismo resultado (54 baterías, 0 con fallos;
`salida_pruebas.txt` regenerado, líneas de resultado idénticas a las de V0.64 y a la entrega original
salvo los tiempos).

## Autocontrol de la pieza (antes de entregar)

- **Citas verificadas por el generador.** `generar_pasada.py` comprueba con `ast` las 185 filas (cada
  «dónde» módulo·función existe; cada «prueba» batería·comprobación aparece en su fichero). En la primera
  pasada el verificador detectó cinco citas erróneas, todas de nombres de comprobación citados de memoria:
  1. `inv_V02_perfil_no_activo` → el caso real es `inv_V02_perfil_no_construido` (`pruebas/generar_casos.py`).
  2. `reduccion_parcial_vuelve_a_abierta` está en `pruebas_orquestador.py`, no en `pruebas_reduccion.py`.
  3. `estado_sello_del_corte_vigente` no existe; se citó `pruebas_degradacion.py ·
     sello_caducado_con_candidato_en_juego_degrada_su_cartera`, que es lo que la fila quería demostrar.
  4. `colision_de_ids_ya_no_se_puede_crear` está en `pruebas_consola.py`, no en `pruebas_orquestador.py`.
  5. `registro_version_REG030` está en `pruebas_envoltura.py`, no en `pruebas_contratos.py`.
  Corregidas las cinco y regenerado el documento.
- **Falso OK corregido en PC2-06.** El primer script buscaba «noticia» y «lector» sin acotar y daba OK
  por menciones ajenas de las pruebas: el «una noticia» es el motivo que una prueba le pasa a H
  (`pruebas_orquestador.py:529`, en la batería de las propuestas de H) y los «lectores» salen en los
  comentarios de `pruebas_robustez_t03.py`. El docstring de H-16 no dice «noticia» (la atribución inicial
  de este autocontrol era errónea; la corrigió el hallazgo 1 de la revisión independiente). Se restringió
  a `validador/` con los patrones concretos del servicio (SC-11, sc11, riesgos_geopoliticos, lectores de
  contenido) y volvió a dar FALLA.
- **Nada cambió en el código.** El lote completo (54 baterías) pasa antes y después de la pieza
  (`salida_pruebas.txt`); el único fichero del marco modificado es `LEEME.md`.
