import re

patron = re.compile(r"(\$\d+)|(\d\d/\d\d/\d\d)")

resultado = patron.findall("El día 13/01/2025 se reportó una ganancia de $25000, aunquel día 14/02/25 se tuvo una pérdida de $150")
print(resultado)

montos = [m[0] for m in resultado if m[0]]
fechas = [m[1] for m in resultado if m[1]]

print("Montos:", montos)
print("Fechas:", fechas)
