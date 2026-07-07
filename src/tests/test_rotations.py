import csv
import math
import time
from concurrent.futures import ProcessPoolExecutor
from random import Random
from statistics import median

from tests.setup_test import TreeType, calc_lista_val_n, create_tree

import matplotlib.pyplot as plt

def rotations_plot(n_max: int, *trees_type: TreeType):
    executor = ProcessPoolExecutor(max_workers=3)
    n_rotations = {}
    futures = {}
    lista_val_n = calc_lista_val_n(n_max)
    graph_name = ""
    path = "plots/rotations/"
    end_of_path = ""

    # Creo il plot condiviso
    plt.figure(figsize=(8, 5))

    # Avviamo i test in parallelo
    for t in trees_type:
        print(f"\nAvvio test rotazioni per {t.value}")
        futures[t] = executor.submit(_test_rotations, t, n_max, lista_val_n)

    #Ordino per uniformare nome file

    # Facciamo il join dei thread creati
    trees_type = sorted(trees_type, key=lambda tree: tree.value)

    for t in trees_type:
        graph_name += t.value + " "
        end_of_path += t.value + "_"
        n_rotations[t] = futures[t].result()
        
    end_of_path = end_of_path.rstrip("_") #Tolgo _ finale
    
    # crea il csv
    f = open(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.csv", "w", newline="")
    wr = csv.writer(f)
    wr.writerow(["n"] + lista_val_n)

    for t in trees_type:
        wr.writerow([t.value] + n_rotations[t])
        
        plt.plot(lista_val_n, n_rotations[t], marker=".", label=t.value)
        plt.xlabel("Nodi (n)")
        plt.ylabel("Numero di rotazioni (n)")

    plt.legend()
    plt.title(f"{graph_name}: numero di rotazioni effettuate\nper la costruzione (albero di n nodi) e inserimento/cancellazione di 100 nodi")
    plt.grid(True)

    plt.savefig(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.png")

    # chiudi csv
    f.close()

def _test_rotations(tree_type: TreeType, n_max: int, lista_val_n):
    rng = Random()
    n_rotations = []

    for n in lista_val_n:
        print(f"{tree_type.value}: {n} ({n/n_max*100:.2f}%)")

        tree = create_tree(tree_type)
        
        tree.conteggio_rotazioni = 0

        # Creo lista
        valori = list(range(0, n + 10 + round(math.sqrt(n))))
        rng.shuffle(valori)

        # Metto n valori casuali nell'albero
        for i in range(0, n):
            tree.insert_key(valori[i])

        # Inizialmente inserirò ultimo indice (unico che manca ancora)
        conteggio_rotazioni = []

        # Faccio mediana su un campione di tempi
        for _ in range(10):
            # Genero i valori da inserire/rimuovere
            ins = rng.randint(n, len(valori) - 1)
            # includo n perchè inserisco e poi rimuovo, quindi quando rimuovo l'albero avra' dimensione n+1
            rem = rng.randint(0, n)

            #tree.counter_rotations = 0

            tree.insert_key(valori[ins])

            swap(valori, n, ins)

            tree.remove_key(valori[rem])

            conteggio_rotazioni.append(tree.counter_rotations) #Calcolo aumento rotazioni dopo inserimento e rimozione

            swap(valori, rem, n)

        conteggio_rotazioni.sort()
        n_rotations.append(median(conteggio_rotazioni))

    return n_rotations


def swap(arr, i, j):
    value = arr[i]
    arr[i] = arr[j]
    arr[j] = value
