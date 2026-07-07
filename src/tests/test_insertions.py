import csv
import math
import time
from concurrent.futures import ProcessPoolExecutor
from random import Random
from statistics import median

from tests.setup_test import TreeType, calc_lista_val_n, create_tree


import matplotlib.pyplot as plt


def insertion_plot(n_max: int, *trees_type: TreeType):
    executor = ProcessPoolExecutor(max_workers=3)
    durations = {}
    futures = {}
    lista_val_n = calc_lista_val_n(n_max)
    graph_name = ""
    path = "plots/insertions/"
    end_of_path = ""

    # Creo il plot condiviso
    plt.figure(figsize=(8, 5))

    # Avviamo i test in parallelo
    for t in trees_type:
        print(f"\nAvvio test inserimenti per {t.value}")
        futures[t] = executor.submit(_test_insertion, t, n_max, lista_val_n)

    #Ordino per uniformare nome file
    trees_type = sorted(trees_type, key=lambda tree: tree.value)

    # Facciamo il join dei thread creati
    for t in trees_type:
        graph_name += t.value + " "
        end_of_path += t.value + "_"
        durations[t] = futures[t].result()
        
    end_of_path = end_of_path.rstrip("_") #Tolgo _ finale

    # crea il csv
    f = open(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.csv", "w", newline="")
    wr = csv.writer(f)
    wr.writerow(["n"] + lista_val_n)
    
    for t in trees_type:
        wr.writerow([t.value] + durations[t])
        
        plt.plot(lista_val_n, durations[t], marker=".", label=t.value)
        plt.xlabel("Nodi (n)")
        plt.ylabel("Tempo (s)")

    plt.legend()
    plt.title(f"{graph_name}tempo inserimento")
    plt.grid(True)

    plt.savefig(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.png")

    # chiudi csv
    f.close()

def _test_insertion(tree_type: TreeType, n_max: int, lista_val_n):
    rng = Random()
    duration = []

    for n in lista_val_n:
        print(f"{tree_type.value}: {n} ({n/n_max*100:.2f}%)")

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
