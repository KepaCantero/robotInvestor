"""Revocación de certificados: `(ece or 1) >= 0.12` trata un ECE = 0 (calibración perfecta) como 1 y revoca."""
from bloque_a.motor import evaluacion as ev
p = [0.75] * 100; o = [1] * 75 + [0] * 25
e = ev.ece(p, o)["ece"]
print("ECE =", e, "| condición de revocación del código (ece or 1) >= 0.12:", (e or 1) >= 0.12)
