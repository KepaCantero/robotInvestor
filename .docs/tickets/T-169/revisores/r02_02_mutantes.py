"""QA r02 de T-169 (revisor) · mutantes propios del código de la r02 (`enviar_pendientes` y `_apartar`), distintos de Q02b–R04
del implementador.

No se ejecuta solo: lo ejecuta el script del implementador, que lee esta lista y prueba cada mutante con las pruebas de T-169
(r02 y r01) y de T-162. Desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-169/revisores/r02_02_mutantes.py <copia>
<copia>: `git archive HEAD bloque_a` con `.venv` enlazado. Para matarlos con las sondas de esta ronda, copiar antes
`r02_01_sondas.py` a `<copia>/bloque_a/11_Ejecutor/tests/` y añadirlo a PRUEBAS (ver qa.md, r02). Sin red ni coste.
"""
RF, OR = "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py"
MUTANTES = [   # (id, descripción, fichero, texto, sustituto, ¿equivalente o de defensa?)
    ("S01", "un error corriente de una pendiente se aparta aunque el almacén esté roto (solo mira la clase)", RF,
     "            except Exception as e:\n                if para_la_consulta(almacen, e):",
     "            except Exception as e:\n                if isinstance(e, ERRORES_DE_CONTROL):", False),
    ("S02", "un error de control de una pendiente se aparta si el almacén está íntegro (solo mira la integridad)", RF,
     "            except Exception as e:\n                if para_la_consulta(almacen, e):",
     "            except Exception as e:\n                if not all(almacen.verificar_integridad().values()):", False),
    ("S03", "la incidencia del apartado no se escala al operador", RF,
     'severidad="Operativa", escalado_operador=True,', 'severidad="Operativa", escalado_operador=False,', False),
    ("S04", "el apartado no deja incidencia", RF,
     '    almacen.incidencia("OTRO", f"La respuesta final pendiente de {qry_id}',
     '    return\n    almacen.incidencia("OTRO", f"La respuesta final pendiente de {qry_id}', False),
    ("S05", "el apartado de un error corriente guarda el texto del error (R8)", RF,
     "                _apartar(almacen, qry_id, type(e).__name__)\n    return enviadas",
     "                _apartar(almacen, qry_id, str(e))\n    return enviadas", False),
    ("S06", "solo se apartan KeyError y RuntimeError (defensa: los demás corrientes paran)", RF,
     "            except Exception as e:\n                if para_la_consulta",
     "            except (KeyError, RuntimeError) as e:\n                if para_la_consulta", True),
    ("S07", "dentro de la transacción no se mira si ya tiene final (equiv.: `enviar` devuelve repetido)", RF,
     '            if ahora.get("final_no_enviable"):', '            if ahora.get("final_no_enviable") or ahora.get("respuesta_final"):', True),
]
