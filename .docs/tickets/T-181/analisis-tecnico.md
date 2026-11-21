# Diseño y condiciones de recuperación

El catálogo de referencias contiene un registro durable de bajas. El custodio prepara la nueva versión en memoria, compara el original bajo un cierre entre procesos y sustituye el fichero entero. Antes de una baja por enlace roto exige la confirmación temporal de HT-02, error HTTP y ausencia de alternativa. Una consulta al servicio de archivo fallida o ambigua conserva la ficha.

F2 recibe el mensaje CT-11 y marca las EVD por identificador de fuente. Cada ciclo puede reconstruir los avisos pendientes desde el registro, incluso tras una interrupción entre la sustitución del catálogo y la escritura en el almacén. Cada oportunidad queda vinculada a las evidencias que realmente contaron para PS1. El Analizador aplica la misma regla a los respaldos supervivientes. Para fichas antiguas sin esa lista, la pérdida de un respaldo exige reevaluación. La revisión queda en el historial de F3, aunque una evaluación posterior actualice la oportunidad. Las bajas se agrupan por custodio y mes para CT-21.

## Revisión de contenido

El custodio usa el informe del barrido para revisar el contenido. Puede entregar su decisión mediante `verificar-enlaces --aplicar --revisiones decisiones.json`. Ejemplo de estructura (la huella debe ser la que figure realmente en el informe):

```json
{"F8":{"MOT-DOC-0001":{"accion":"DEGRADAR","hash":"sha256:…","motivo":"La versión nueva omite la descripción de la muestra","puntos":[20,10,15,5,8,7,10]}}}
```

Los puntos se indican en el orden del Documento 0 §13.3. Para RETRACTADA se aportan la huella y el motivo de confirmación del editor. Para REPARAR se añade la URL archivada del informe. El ejecutor comprueba que reproduce la huella de la versión original. La revisión de contenido es entrada del custodio; las comprobaciones realizadas aquí usan revisiones preparadas, sin llamar a un modelo ni a un editor real.
