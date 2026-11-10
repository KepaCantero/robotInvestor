# T-87 · Contraste D01–D10 y cambios en evaluación

A 10-11-2026. Base de trabajo `bc90534`, posterior a la auditoría `2065e48`. Las reproducciones usan datos artificiales, sin red ni claves. Se conserva la política T-66 de aprobación del operador, exclusión de contaminación y muestra efectiva por fecha.

| ID | Situación en la base / tratamiento |
|---|---|
| D01 | **Corregido aquí.** El numerador usa el último cierre hasta el vencimiento. El denominador usa lo congelado en F4 para el indicador y el índice, incluidas las fechas de observación cuando se conocen. Los nuevos pronósticos frente a CESTA guardan los miembros observables y sus niveles iniciales. Para registros antiguos sin denominador se reconstruye la base con fecha de conocimiento igual a la de emisión mediante el filtro HT-01, sin mover el reloj del evaluador. |
| D02 | **Corregido aquí.** Se conservan ambas fechas al resolver un relativo y se comprueba la más antigua; en una cesta se comprueba el miembro más antiguo. Un componente congelado que carezca de dato final no desaparece de la cesta para facilitar la resolución. Se mantiene la espera y finalmente NO_RESOLUBLE. |
| D03 | **Ya corregido en la base.** La serie CSV inválida lanza DatosInvalidos y la resolución comprueba finitud y denominador. Corroborado por las pruebas T-53 de HT-01 y resolución. |
| D04 | **Ya corregido en la base.** Una celda de publicación ISO inválida se excluye; la política documentada de celda vacía es «sin retraso». Las pruebas T-53 distinguen ambas cosas. |
| D05 | **Corregido aquí.** F6 separa clase × horizonte × método para muestra, Holm, emisión, aprobación y revocación. Las probabilidades F4 y las numéricas del paquete exigen un certificado vigente del método concreto del pronóstico. Los registros históricos sin método siguen siendo legibles y los informes conservan su clave antigua; un certificado anónimo no autoriza publicar cifras. CT-12 informa de los métodos vigentes y no declara de antemano que esté certificado un pronóstico cuyo método el agente aún no eligió. El ejecutor bloquea en G3 una probabilidad sin método aunque exista un certificado para otro método de la misma clase y horizonte. Las plantillas y herramientas canónicas no se modificaron. |
| D06 | **Ya corregido en la base.** ECE=0 no revoca; se distingue de ECE ausente y se usa el umbral configurado. |
| D07 | **Ya corregido en la base.** Holm tiene parada escalonada y se respeta también tras desglosar por método. PA-03 utiliza ventanas de resolución como conglomerados y n efectiva en el criterio. |
| D08 | **Corregido aquí.** Un backtest independiente exige una salida sin ficheros de un backtest anterior; reserva el subdirectorio de estado con creación exclusiva, también frente a dos inicios simultáneos. Una repetición debe usar otro destino. Una salida parcial se conserva para diagnóstico. |
| D09 | **Corregido aquí.** La huella del vector de cierres incluye todo el calendario ordenado expresado en nanosegundos, además de los valores y el símbolo. Cambiar solo una fecha interior ya cambia la huella. Los registros históricos RC no se reescriben; un hash anterior no acredita identidad exacta bajo el algoritmo actualizado. |
| D10 | **Corregido aquí.** El lector CSV acepta únicamente un nombre de archivo local; rechaza escapes relativos, rutas absolutas y enlaces con destino exterior antes de leer la serie. Es un control de la raíz de datos, no un aislamiento del proceso frente a un atacante con acceso de escritura al sistema. |

**Interacción con O3 (F10).** Se reprodujo la pérdida de la primera degradación cuando dos clases sufrían la degradación H5 con el mismo día de efecto. Ahora la matriz P-31 y la versión P-30 siguientes se componen con los cambios ya conocidos al corte y efectivos en la fecha prevista. Ninguna de las dos degradaciones se adelanta al día en que se calcula.

**Validación.** Antes de corregir, los ocho casos iniciales de `tests/test_t87_datos.py` fallaron (los dos lados de una comparación y la cesta son casos separados). También se reprodujo el fallo de composición de dos cambios H5 al aplicar el filtro de O3. Tras las correcciones se ejecutaron 60 pruebas de datos, evaluación, T-53 y T-66, incluidas once T-87. Hay una prueba de extremo a extremo con el mock de A: aprobar ACC-MOM-001 para H3 permite publicar H3, pero ni otro método ni un certificado antiguo anónimo permiten publicar H2.

```sh
.venv/bin/python -m pytest -q -p no:cacheprovider bloque_a/11_Ejecutor/tests/test_t87_datos.py bloque_a/11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py bloque_a/11_Ejecutor/tests/test_t66_evaluacion.py
```

**Límites.** No se puede reconstruir un vintage histórico si un proveedor sobrescribió el fichero original y el registro antiguo no congeló los componentes de la cesta. La reconstrucción de registros anteriores solo es válida sobre sus datos versionados. La huella acredita los cierres consumidos por el Motor, no todos los campos de mercado de un proveedor. Estas pruebas no miden la capacidad predictiva ni la calibración de un modelo real.
