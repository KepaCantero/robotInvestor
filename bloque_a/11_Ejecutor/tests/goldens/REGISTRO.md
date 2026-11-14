# Registro de re-congelados de los goldens de contratos

Una línea por re-congelado: fecha · ficheros · motivo. La escribe `python tests/goldens_ct.py --update --motivo "…"`.

- 2026-11-13 · divergencias_anexo_b.json, esquemas_respuestas.json, formas_ciclo_mock.json, huellas.json, mensajes_ejemplo.json, tablas_contratos.json · Primer congelado de los goldens de contratos (T-114, Fase 3)
- 2026-11-14 · aceptaciones_rechazos.json, divergencias_anexo_b.json, formas_flujos_mock.json, huellas.json, mensajes_ejemplo.json · T-114 r02 (QA r01): golden nuevo de aceptaciones y rechazos de la mensajería (batería de 362 casos); formas de once flujos simulados con rutas anidadas y tipos JSON (sustituye a formas_ciclo_mock.json); CT-22 pasa a tener el campo tipo que nombra el Anexo B y su diferencia con el ejecutor (tipo_aviso); contenido de CT-23 con condición
- 2026-11-14 · formas_flujos_mock.json · Al integrar la r02 de T-114 con la r02 de T-117: en el ciclo V6 simulado, los Analistas de RF (AG-04) y de TCV (AG-25) dejan de emitir CT-08, porque el encargo CT-06 les comunica ahora el umbral de su tipo (0,65) y el cliente simulado deriva su semilla del texto del encargo; no cambia ningún formato
