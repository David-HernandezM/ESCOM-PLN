import os
import keyboard

def mostrar_menu(opciones, seleccion):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Usa las flechas ↑ ↓ para elegir una opción. Presiona ENTER para confirmar.\n")
    for i, opcion in enumerate(opciones):
        if i == seleccion:
            print(f"> {opcion}")
        else:
            print(f"  {opcion}")

def main():
    opciones = ["Buscar en arXiv", "Buscar en PubMed"]
    seleccion = 0

    mostrar_menu(opciones, seleccion)

    while True:
        if keyboard.is_pressed("up"):
            seleccion = (seleccion - 1) % len(opciones)
            mostrar_menu(opciones, seleccion)
            keyboard.wait("up")  # Espera a que se suelte la tecla
        elif keyboard.is_pressed("down"):
            seleccion = (seleccion + 1) % len(opciones)
            mostrar_menu(opciones, seleccion)
            keyboard.wait("down")
        elif keyboard.is_pressed("enter"):
            break

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Opción seleccionada: {opciones[seleccion]}")

if __name__ == "__main__":
    main()







# archivos a checar en los documentos:
# DOI = LID
# Title = TI
# Authors = AU (Hay uno o mas)
# Abstract = AB
# journal name = JT
# Publication date = DP