"""QA r01 de T-169 (revisor) · mutantes propios del código nuevo de T-169, distintos de los N01–N15 del implementador.

No se ejecuta solo: lo ejecuta el script del implementador, que lee esta lista y prueba cada mutante con las pruebas de T-169 y
de T-162. Desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-169/revisores/r01_03_mutantes.py <copia «t169_mut»>
<copia>: `git archive HEAD bloque_a` con `.venv` enlazado. Los marcados «(equiv.)» se esperan vivos. Sin red ni coste.
"""
RF, OR = "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py"
MUTANTES = [   # (id, descripción, fichero, texto, sustituto, ¿equivalente o de defensa?)
    ("Q01", "pendientes también sin la provisional registrada", RF,
     ' and q.get("provisional_msg_id") and not q.get("respuesta_final")', ' and not q.get("respuesta_final")', False),
    ("Q02", "pendientes en orden inverso", RF, "    return salida\n\n\ndef enviar_pendientes", "    return salida[::-1]\n\n\ndef enviar_pendientes",
     False),
    ("Q03", "un rechazo de la pendiente sin mirar la integridad", RF,
     ("        except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO) as e:\n            if not all(almacen.verificar_integridad().values()):\n"
      "                raise\n"), "        except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO) as e:\n", False),
    ("Q04", "MensajeInvalido deja de ser un error de control", RF,
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion)",
     "ERRORES_DE_CONTROL = (PermissionError, FugaDeInformacion)", False),
    ("Q05", "FugaDeInformacion deja de ser un error de control", RF,
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion)",
     "ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido)", False),
    ("Q06", "la final ya enviada no compara la provisional dada", RF,
     'if provisional_msg_id is not None and previa["respuesta_final"]["provisional_msg_id"] != provisional_msg_id:',
     "if False:", False),
    ("Q07", "lo de otro tipo no queda en las descartadas", RF,
     " + [x for x in dict.fromkeys(ajenas) if x not in vistas]", "", False),
    ("Q08", "la provisional se registra antes de crearla (con el msg_id del encargo)", OR,
     'respuesta_final.registrar_provisional(self.almacen, qry_id, respuesta["msg_id"], fallo)',
     'respuesta_final.registrar_provisional(self.almacen, qry_id, msg["msg_id"], fallo)', False),
    ("Q09", "el ciclo envía las pendientes con su fecha y no con la de cada consulta", RF,
     "    for qry_id, fecha in pendientes(almacen, as_of):\n        try:",
     "    for qry_id, fecha in pendientes(almacen, as_of):\n        fecha = as_of or fecha\n        try:", False),
    ("Q10", "las pendientes se listan sin fecha de corte (también las futuras)", RF,
     "    for qry_id, q in almacen.estado(\"F5\", as_of).items():", "    for qry_id, q in almacen.estado(\"F5\").items():", False),
]


def pytest(*_):   # marca de fin de la lista para `mutantes_t169.py`, que la lee hasta aquí
    raise SystemExit("se ejecuta con .docs/tickets/T-169/scripts/mutantes_t169.py")
