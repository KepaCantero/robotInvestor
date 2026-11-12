---
id: astra/2026-11-12_revisiones-diseno-a-e
autor: astra
fecha: 2026-11-12
tipo: leccion
etiquetas: []
fuente: informes C-01 a C-05 y cola local de Astra
vigencia: vigente
---

Prioridad operativa: TODO EN LOCAL hasta autorización expresa, como documenta `.docs/memoria/astra/2026-11-12_solo-local-hasta-autorizacion.md`. No seguir las instrucciones de push antiguas del proyecto.

Revisiones C-01 a C-05 redactadas; estado y cierre efectivo en `.docs/tickets/_relevo/cola_astra.md`. A, B y C se publicaron por una interpretación indebida de autorización, reconocida al operador. D y siguientes quedan locales.

Lecciones reutilizables:
- A: ahorro futuro no demostrado por contar llamadas actuales; toda sustitución tras crítica requiere revisar también al sustituto.
- B: su tabla de precios se reproduce suponiendo continuidad de caché. El cliente simulado reinicia caché al reanudar; distinguir ambas medidas. Playbooks tienen dependencias: no retirar once a ciegas. Auditoría previa N2/N3 no equivale a validar formato.
- C: reutilizar cálculos no es reenviar un sobre antiguo; comprobar contexto y hash revisado. Una cita presente no demuestra resolución sustantiva de la objeción.
- D: comparar el rango de la diferencia entre opciones; solapamiento de rangos individuales no demuestra empate. Conservar restricción vigente de comparación entre clases hasta ratificación.
- E: tabla de Kelly válida bajo aproximación, con notación corregida; riesgo no es conocido ni stop garantiza pérdida máxima. D debe revisar si el tamaño final cambia la preferencia. Reservar efectivo y riesgo de forma indivisible ante concurrencia.

Los informes son revisiones de diseño, no QA del marco ni implementaciones. Los tickets retirados siguen retirados. Las pruebas completas solo verifican que las entregas documentales no rompen las comprobaciones existentes; no certifican rentabilidad ni precisión predictiva.
