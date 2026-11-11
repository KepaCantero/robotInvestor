# T-95 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `dashboard/consola_n/pruebas/unit/` (Vitest) | — (nueva) | 29 de 29 en verde (`npm test`, menos de 1 s) |
| `dashboard/consola_n/pruebas/e2e/` (Playwright) | — (nueva) | 12 de 12 en verde (`npm run build && npm run e2e`, unos 31 s) |
| `npm run typecheck` (TypeScript estricto, `noUncheckedIndexedAccess`) | — | Sin errores |
| Suites de los bloques y del marco | Sin cambios | Sin cambios: el prototipo no toca ningún bloque ni el marco (CA-10) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `npm run build`, `npm run build:pagina` y `npm run typecheck` sin errores |
| CA-2 | e2e «las siete pantallas se abren por el menú y por su enlace, sin errores» |
| CA-3 | unitarias «veredicto de la cifra principal»; e2e «la cifra principal dice que todavía no se sabe» |
| CA-4 | unitarias «importe tecleado al céntimo» y «fricción asimétrica»; API simulada «aprobar… una sola vez», «aumentar exige código y espera», «el día en que se tocó un límite», «caduca sin actuar»; e2e de abrir, aumentar y límite del día |
| CA-5 | unitaria «reducir… un toque»; API simulada «reducir es un toque», «kill-switch»; e2e «reducir es un toque y el kill-switch también» y «vender en caída el largo plazo» |
| CA-6 | unitarias «explicación del Broker sin cifras inventadas»; e2e de la explicación retirada (D-0149) y mostrada (D-0147) |
| CA-7 | API simulada y e2e «acusar un aviso no lo borra» |
| CA-8 | unitarias «semáforo del panel»; API simulada «si la API falla»; e2e «si la API no responde, el semáforo pasa a rojo y no se muestran cifras» |
| CA-9 | e2e «sin desplazamiento horizontal» a 400 px en claro y a 1.280 px en oscuro, las siete pantallas; capturas revisadas a mano |
| CA-10 | `git status` de bloques, marco y Constitución sin cambios; gate en el commit con `commit_limpio.sh` |

Pruebas añadidas fuera de los criterios: vender más de lo que se tiene se veta (asimetría de F, enmienda 5, D-52); subir un límite desde Configuración crea una decisión con fricción; formato español con separador de miles en cuatro cifras.

## Notas

- En el entorno de pruebas no se pueden descargar las fuentes de Google; las pruebas ignoran solo ese error de carga y fallan con cualquier otro. En la página publicada sí cargan.
- La página publicada se genera con `npm run build:pagina` (un solo fichero de unos 1,6 MB, con todo el código dentro).
- El publicador avisa de un posible enlace de descarga: es código de exportación de AG Grid que la consola no usa.

## Gate

Se ejecuta en el commit con `.docs/scripts/commit_limpio.sh` (gate completo en una copia limpia).
