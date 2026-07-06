import csv
import math
import time
from concurrent.futures import ProcessPoolExecutor
from enum import Enum
from random import Random
from statistics import median

import matplotlib.pyplot as plt

from trees.avl import AVL
from trees.bst import BST
from trees.rbt import RBT


class TreeType(Enum):
    AVL = "AVL"
    BST = "BST"
    RBT = "RBT"


def create_tree(type_of_tree: TreeType):
    if type_of_tree == TreeType.BST:
        return BST()
    elif type_of_tree == TreeType.AVL:
        return AVL()
    elif type_of_tree == TreeType.RBT:
        return RBT()
    else:
        raise ValueError(f"Tipo sconosciuto:  {type_of_tree}")


def calc_lista_val_n():
    samples = 100
    n_min = 1000
    n_max = 1000000

    lista_val_n = []

    c = (n_max / n_min) ** (1 / (samples - 1))

    for i in range(0, samples):
        n_i = round(n_min * (c**i))

        # Non vado oltre il massimo consentito
        if n_i > n_max:
            break

        lista_val_n.append(n_i)

    return lista_val_n


def insertion_plot(*trees_type: TreeType):
    executor = ProcessPoolExecutor(max_workers=3)
    durations = {}
    futures = {}
    lista_val_n = calc_lista_val_n()
    graph_name = ""
    path = "plots/"

    # Creo il plot condiviso
    plt.figure(figsize=(8, 5))

    # Avviamo i test in parallelo
    for t in trees_type:
        print(f"\nAvvio test per {t.value}")
        futures[t] = executor.submit(_test_insertion, t, lista_val_n)

    # Facciamo il join dei thread creati
    for t in trees_type:
        durations[t] = futures[t].result()

    # crea il csv
    f = open(f"{path}{time.strftime('%H-%M-%S', time.localtime())}.csv", "w", newline="")
    wr = csv.writer(f)
    wr.writerow(["n"] + lista_val_n)
    
    for t in trees_type:
        wr.writerow([t.value] + durations[t])
        
        plt.plot(lista_val_n, durations[t], marker=".", label=t.value)
        plt.xlabel("Nodi (n)")
        plt.ylabel("Tempo (s)")
        graph_name += t.value + " "
        path += t.value + "_"

    plt.legend()
    plt.title(f"{graph_name}tempo inserimento")
    plt.grid(True)

    plt.savefig(f"{path}{time.strftime('%H-%M-%S', time.localtime())}-plot.png")

    # chiudi csv
    f.close()

def _test_insertion(tree_type: TreeType, lista_val_n):
    rng = Random()
    duration = []

    for n in lista_val_n:
        print(f"{tree_type.value}: {n}")

        tree = create_tree(tree_type)

        # Creo lista
        valori = list(range(0, n + 10 + round(math.sqrt(n))))
        rng.shuffle(valori)

        # Metto n valori casuali nell'albero
        for i in range(0, n):
            tree.insert_key(valori[i])

        # Inizialmente inserirò ultimo indice (unico che manca ancora)
        tempi = []

        # Faccio mediana su un campione di tempi
        for _ in range(100 + round(2 * math.sqrt(n))):
            # Genero i valori da inserire/rimuovere
            ins = rng.randint(n, len(valori) - 1)
            # includo n perchè inserisco e poi rimuovo, quindi quando rimuovo l'albero avra' dimensione n+1
            rem = rng.randint(0, n)

            # MISURAZIONE
            start = time.perf_counter()
            tree.insert_key(valori[ins])
            stop = time.perf_counter()

            swap(valori, n, ins)

            # Aggiungo uno dei tempi: poi farò la mediana di tutti quelli raccolti
            tempi.append(stop - start)

            tree.remove_key(valori[rem])

            swap(valori, rem, n)

        tempi.sort()
        duration.append(median(tempi))

    return duration


def swap(arr, i, j):
    value = arr[i]
    arr[i] = arr[j]
    arr[j] = value
