"""Holm aplicado celda a celda (no step-down): una celda pasa aunque la de p menor haya fallado."""
from bloque_a.motor import evaluacion as ev
p = {"RV|H3": 0.06, "RF|H3": 0.07}
u = ev.holm(p, 0.10)
print("umbrales:", u)
for k, v in sorted(p.items(), key=lambda kv: kv[1]):
    print(k, "p =", v, "rechaza H0 segun codigo:", v <= u[k])
print("Holm correcto (step-down): la primera (0.06 > 0.05) no se rechaza -> se detiene; ninguna celda se rechaza")
