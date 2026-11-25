# T-196 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-24 · de claude (implementador, ronda de cierre) a QA (cierre de la r03)

- **Hecho:** M-01: un segundo caso en `test_atender_con_un_reloj_que_retrocede_falla_cerrado` (t0+10, t0+10, t0+12 y t0+11 minutos: `PeticionInvalida` tras la segunda servida). P1 pasa a `mutantes.py` como M62.
- **Verificado:** 63 pruebas superadas; `mutantes.py` 62/62 y `r03_mutantes.py` 2/2 muertos; `r03_ataques.py` B1 a B5 OK. El código no cambia.
- **Commit:** «T-196 cierre: …», en `wip/t196`, sin push.

## 2026-11-24 · de claude (implementador, r03) a QA (r03)

- **Fase en la que se entrega:** QA (r03), tras el NO APTO de la r02.
- **Hecho:**
  - N-01: `_servir` en un `try/finally` hasta la ATENDIDA y la final.
  - N-02: un reloj que retrocede da `PeticionInvalida`.
  - N-03: docstring corregido.
  - N-04: pruebas que matan Q2, Q8, Q10 y Q11, pasados a `mutantes.py` como M58 a M61.
  - 62 pruebas. Mutantes: 61 de 61 propios, 12 de 12 de la r02 y 13 de 14 de la r01 (R11, equivalente).
  - Evidencias regeneradas y gate 12/12 (`gate_t196_r03.log`).
- **Cuidado con:** B5 de `r02_ataques.py` da ERROR porque la corrección pedida es lanzar; su expectativa (`len(s) == 3`) es la contraria (ver `pruebas.md`, «Ronda r03»). La carrera de `_acuses` va a otro ticket.
- **Commit:** «T-196 r03: …», en `wip/t196`, sin push.

## 2026-11-24 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), tras el NO APTO de la r01.
- **Hecho:**
  - H-01 a H-09 corregidos, cada uno con su prueba de regresión (tabla en `analisis-tecnico.md`, «Ronda r02»).
  - Ataques del revisor: 10 de 10 OK. Mutantes del revisor: 13 de 14 muertos (R11, equivalente). Mutantes propios: 55 de 55 muertos.
  - Evidencias regeneradas y gate completo (log en la carpeta de trabajo: `gate_t196_r02.log`).
- **Cuidado con:**
  - **H-04 trunca los nanosegundos, no los rechaza.** El qa.md admite las dos opciones; A5 espera que se admita.
  - **H-06 añade `servir`; `tomar` sigue pública.** A6 y A7 la usan. Lo tomado y no servido se ve como huérfano, también en el mismo proceso: `_EN_MARCHA`, como en T-174.
  - **Nueva semántica de A9 y del «instante anterior».** Una PET- recibida después del instante no se ve todavía, y no es un error. Solo `prioridad(pet, t)` rechaza un instante anterior a su recepción.
  - **`atender` devuelve la lista de servidas.** La CLI imprime además `huerfanas`.
  - **Una carrera anterior a T-196.** Está en `Mensajeria._acuses`: el `ALTER TABLE` inicial no es concurrente. Ver `pruebas.md`.
- **Commit:** «T-196 r02: …», en la rama `wip/t196`, sin push.

## 2026-11-24 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:** PB-08 con la cola de peticiones del Coordinador (`bloque_a/11_Ejecutor/bloque_a/cola_peticiones.py`):
  - PET- en F5;
  - ninguna rechazada por número;
  - prioridad efectiva = base + envejecimiento por hora completa hasta su máximo + urgencia por fecha objetivo, con desempate por nivel y llegada;
  - presupuesto del Anexo A por nivel, con la misma regla que `_reparto`;
  - acuse y provisional con plazo; las N0 por el carril rápido;
  - servicio con `atender` y la final de las consultas al atenderlas.
  
  Hay 41 pruebas en `tests/test_t196.py` y 33 mutantes, todos muertos. El mapa (PB-08 sigue PARCIAL, ahora solo por el p90 en tiempo real) y las evidencias están regenerados. El ciclo mock y el backtest dan lo mismo que develop.
- **Falta:** la QA. El commit es local, sin push.
- **Commit:** el último de la rama `wip/t196` («motor: Bloque A, T-196 (PB-08)… [pendiente QA]»), encima de `6045913`.
- **Cuidado con:**
  - Las decisiones `[PROPUESTO]` de INC-T196-01: los números del §6.1 del prompt en la configuración, la urgencia sin P80, el plazo sin hora estimada, la PET- en vez de un RUN- ENCOLADO, el `escalado` de la final con el RUN- que la atendió y HT-08 sin alimentar.
  - `atender` relanza cualquier error del ciclo tras registrarlo (FALLIDA e incidencia): no lo absorbe como hace la consulta síncrona.
  - Una PET- EN_CURSO de un proceso muerto no se recupera.
  - `peticion` y `consulta` por defecto no cambian: la cola solo actúa con `recibir`, `encolar_escalado=True` o la CLI nueva.
- **Scripts útiles:** `.docs/scripts/evidencias_plan_a.py --pb PB-08`; `.docs/tickets/T-196/mutantes.py` (en una copia del paquete: modifica los fuentes mientras corre).
