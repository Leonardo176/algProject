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
    samples = 200
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


def insertion_plot(*types_of_trees: TreeType):
    executor = ProcessPoolExecutor(max_workers=3)
    futures = []
    lista_val_n = calc_lista_val_n()
    strNome = ""
    strPath = "src/tests/"

    dict = {"AVL": 0, "BST": 1, "RBT": 2}

    # Creo il plot condiviso
    plt.figure(figsize=(8, 5))

    for t in types_of_trees:
        print(f"\nAvvio test per {t.value}")
        futures.append(executor.submit(_test_insertion, t, lista_val_n))

    durations = [f.result() for f in futures]

    for t in types_of_trees:
        plt.plot(lista_val_n, durations[dict[t.value]], marker=".", label=t.value)
        plt.xlabel("Nodi (n)")
        plt.ylabel("Tempo (s)")
        strNome += t.value + " "
        strPath += t.value + "_"

    plt.legend()
    plt.title(f"{strNome}tempo inserimento")
    plt.grid(True)

    filename = f"{strPath}plot.png"
    plt.savefig(filename)


def _test_insertion(type_of_tree: TreeType, lista_val_n):
    r = Random()
    duration = list()

    for n in lista_val_n:
        print(f"{type_of_tree.value}: {n}")

        x = create_tree(type_of_tree)

        # Creo lista
        valori = list(range(0, n + 1))
        r.shuffle(valori)

        # Metto n valori casuali nell'albero
        for i in range(0, n):
            x.insert_key(valori[i])

        # Inizialmente inserirò ultimo indice (unico che manca ancora)
        ind = n
        tempi = list()

        # Faccio mediana su un campione di 300 tempi, per ogni n
        for _ in range(100):
            # MISURAZIONE (fermo garbage collector temporaneamente)
            start = time.perf_counter()
            x.insert_key(valori[ind])
            stop = time.perf_counter()

            # Aggiungo uno dei 500 tempi: poi farò la mediana di tutti quelli raccolti
            tempi.append(stop - start)

            ind = r.randint(0, n)
            x.remove_key(valori[ind])

        tempi.sort()
        duration.append(median(tempi))

    return duration
