"""
Juego de Pokemon - Gestión de Entrenadores
--------------------------------------------
Programa que administra una lista de tuplas (entrenador, pokemon, ataque, vida)
mediante un menú con las siguientes opciones:
    1. Crear Entrenador
    2. Listar Entrenadores
    3. Borrar por Pokemon
    4. Pelea Pokemon
    5. Fin

Autor: (Dante)
"""

import random


def crearEntrenador(lista):
    """
    Crea un entrenador y su pokemon.
    Recibe la lista de tuplas, pide nombre de entrenador y de pokemon,
    genera un ataque aleatorio entre 150 y 250 y una vida aleatoria
    entre 500 y 900, y agrega la tupla resultante a la lista.
    """
    nombre_entrenador = input("Ingrese el nombre del entrenador: ")
    nombre_pokemon = input("Ingrese el nombre del pokemon: ")

    ataque = random.randint(150, 250)
    vida = random.randint(500, 900)

    lista.append((nombre_entrenador, nombre_pokemon, ataque, vida))

    print(f"\nEntrenador '{nombre_entrenador}' con pokemon '{nombre_pokemon}' "
          f"creado exitosamente. (Ataque: {ataque} | Vida: {vida})\n")


def listaEntrenador(lista):
    """
    Muestra los entrenadores ordenados por el ataque de su pokemon
    (de mayor a menor), usando el método de ordenamiento burbuja.
    Recibe la lista de tuplas.
    """
    n = len(lista)

    # --- Ordenamiento burbuja por ataque (descendente) ---
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j][2] < lista[j + 1][2]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    if n == 0:
        print("\nNo hay entrenadores registrados todavía.\n")
        return

    print()
    print("{:<5}{:<15}{:<15}{:<10}{:<10}".format(
        "N°", "Entrenador", "Pokemon", "Ataque", "Vida"))
    print("-" * 55)
    for indice, entrenador in enumerate(lista, start=1):
        print("{:<5}{:<15}{:<15}{:<10}{:<10}".format(
            indice, entrenador[0], entrenador[1], entrenador[2], entrenador[3]))
    print()


def borraPorPokemon(lista):
    """
    Borra el primer entrenador/pokemon cuya vida coincida con el valor
    buscado. Recibe la lista de tuplas, ordena la lista por vida usando
    el método de selección y luego busca el valor con búsqueda binaria.
    """
    if not lista:
        print("\nNo hay entrenadores registrados para borrar.\n")
        return

    try:
        vida_buscada = int(input("Ingrese el valor de vida a buscar: "))
    except ValueError:
        print("\nDebe ingresar un número válido.\n")
        return

    n = len(lista)

    # --- Ordenamiento por selección, según la vida (ascendente) ---
    for i in range(n):
        indice_menor = i
        for j in range(i + 1, n):
            if lista[j][3] < lista[indice_menor][3]:
                indice_menor = j
        lista[i], lista[indice_menor] = lista[indice_menor], lista[i]

    # --- Búsqueda binaria por vida ---
    izquierda, derecha = 0, n - 1
    posicion_encontrada = -1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio][3] == vida_buscada:
            posicion_encontrada = medio
            break
        elif lista[medio][3] < vida_buscada:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    if posicion_encontrada != -1:
        eliminado = lista.pop(posicion_encontrada)
        print(f"\nSe eliminó al entrenador '{eliminado[0]}' y su pokemon "
              f"'{eliminado[1]}' (vida: {eliminado[3]}).\n")
    else:
        print(f"\nNo se encontró ningún pokemon con vida = {vida_buscada}.\n")


def peleaPokemon(lista):
    """
    Hace pelear a 2 pokemones. Muestra la lista, pide los números
    correlativos de los 2 pokemones a pelear, calcula el daño de cada
    uno (ataque * aleatorio entre 0 y 5) y lo resta de la vida del rival.
    Gana quien le quede más vida; el perdedor se elimina de la lista.
    Si ambos quedan sin vida, ambos se eliminan. Si empatan, ambos pierden.
    """
    if len(lista) < 2:
        print("\nSe necesitan al menos 2 pokemones registrados para pelear.\n")
        return

    listaEntrenador(lista)

    try:
        num1 = int(input("Ingrese el número del primer pokemon: "))
        num2 = int(input("Ingrese el número del segundo pokemon: "))
    except ValueError:
        print("\nDebe ingresar números válidos.\n")
        return

    if num1 == num2 or not (1 <= num1 <= len(lista)) or not (1 <= num2 <= len(lista)):
        print("\nSelección inválida. Verifique los números ingresados.\n")
        return

    indice1, indice2 = num1 - 1, num2 - 1
    entrenador1 = lista[indice1]
    entrenador2 = lista[indice2]

    daño_recibido_2 = entrenador1[2] * random.randint(0, 5)
    daño_recibido_1 = entrenador2[2] * random.randint(0, 5)

    vida1_final = entrenador1[3] - daño_recibido_1
    vida2_final = entrenador2[3] - daño_recibido_2

    print(f"\n¡Comienza la pelea entre {entrenador1[0]} ({entrenador1[1]}) "
          f"y {entrenador2[0]} ({entrenador2[1]})!\n")
    print(f"{entrenador1[0]} ({entrenador1[1]}) ataca causando {daño_recibido_2} de daño.")
    print(f"{entrenador2[0]} ({entrenador2[1]}) ataca causando {daño_recibido_1} de daño.")
    print(f"Vida restante de {entrenador1[0]} ({entrenador1[1]}): {max(vida1_final, 0)}")
    print(f"Vida restante de {entrenador2[0]} ({entrenador2[1]}): {max(vida2_final, 0)}\n")

    if vida1_final <= 0 and vida2_final <= 0:
        print(f"¡Ambos pokemones se quedaron sin vida! {entrenador1[0]} ({entrenador1[1]}) "
              f"y {entrenador2[0]} ({entrenador2[1]}) pierden y son eliminados.\n")
        for indice in sorted([indice1, indice2], reverse=True):
            lista.pop(indice)
    elif vida1_final == vida2_final:
        print(f"¡Empate! Ambos entrenadores pierden: {entrenador1[0]} ({entrenador1[1]}) "
              f"y {entrenador2[0]} ({entrenador2[1]}) son eliminados.\n")
        for indice in sorted([indice1, indice2], reverse=True):
            lista.pop(indice)
    elif vida1_final > vida2_final:
        print(f"¡Ganador: {entrenador1[0]} con su pokemon {entrenador1[1]}!\n")
        lista.pop(indice2)
    else:
        print(f"¡Ganador: {entrenador2[0]} con su pokemon {entrenador2[1]}!\n")
        lista.pop(indice1)


def mostrarMenu():
    print("=== MENÚ POKEMON ===")
    print("1. Crear Entrenador")
    print("2. Listar Entrenadores")
    print("3. Borrar por Pokemon")
    print("4. Pelea Pokemon")
    print("5. Fin")


def main():
    entrenadores = []  # Lista de tuplas: (entrenador, pokemon, ataque, vida)

    while True:
        mostrarMenu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crearEntrenador(entrenadores)
        elif opcion == "2":
            listaEntrenador(entrenadores)
        elif opcion == "3":
            borraPorPokemon(entrenadores)
        elif opcion == "4":
            peleaPokemon(entrenadores)
        elif opcion == "5":
            print("\n¡Gracias por jugar!")
            break
        else:
            print("\nOpción inválida, intente nuevamente.\n")


if __name__ == "__main__":
    main()
