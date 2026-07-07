import csv
import math
import time
from concurrent.futures import ProcessPoolExecutor
from random import Random
from statistics import median

from tests.setup_test import *

import matplotlib.pyplot as plt

def heights_plot(n_max: int, *trees_type: TreeType):
    executor = ProcessPoolExecutor(max_workers=3)
    heights = {}
    futures = {}
    lista_val_n = calc_lista_val_n(n_max)
    graph_name = ""
    path = "plots/heights/"

    # Creo il plot condiviso
    plt.figure(figsize=(8, 5))

    # Avviamo i test in parallelo
    for t in trees_type:
        print(f"\nAvvio test altezze per {t.value}")
        futures[t] = executor.submit(_test_heights, t, n_max, lista_val_n)

    # Facciamo il join dei thread creati
    for t in trees_type:
        graph_name += t.value + " "
        path += t.value + "_"
        heights[t] = futures[t].result()
    
    # crea il csv
    f = open(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.csv", "w", newline="")
    wr = csv.writer(f)
    wr.writerow(["n"] + lista_val_n)

    for t in trees_type:
        wr.writerow([t.value] + heights[t])
        
        plt.plot(lista_val_n, heights[t], marker=".", label=t.value)
        plt.xlabel("Nodi (n)")
        plt.ylabel("Altezza (n)")

    plt.legend()
    plt.title(f"{graph_name}: altezza massima dell'albero")
    plt.grid(True)

    plt.savefig(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.png")

    # chiudi csv
    f.close()

def _test_heights(tree_type: TreeType, n_max: int, lista_val_n):
    rng = Random()
    list_heights = []

    for n in lista_val_n:
        print(f"{tree_type.value}: {n} ({(n-1000)/(n_max-1000)*100:.2f}%)") #Stampa percentuale

        tree = create_tree(tree_type)

        # Creo lista
        valori = list(range(0, n + 10 + round(math.sqrt(n))))
        rng.shuffle(valori)

        # Metto n valori casuali nell'albero
        for i in range(0, n):
            tree.insert_key(valori[i])

        # Inizialmente inserirò ultimo indice (unico che manca ancora)
        conteggio_altezze = []

        # Faccio mediana su un campione di tempi
        for _ in range(100):
            # Genero i valori da inserire/rimuovere
            ins = rng.randint(n, len(valori) - 1)
            # includo n perchè inserisco e poi rimuovo, quindi quando rimuovo l'albero avra' dimensione n+1
            rem = rng.randint(0, n)

            tree.insert_key(valori[ins])

            conteggio_altezze.append(height_ric(tree.root))

            swap(valori, n, ins)

            tree.remove_key(valori[rem])

            swap(valori, rem, n)

        conteggio_altezze.sort()
        list_heights.append(max(conteggio_altezze))

    return list_heights


def swap(arr, i, j):
    value = arr[i]
    arr[i] = arr[j]
    arr[j] = value
