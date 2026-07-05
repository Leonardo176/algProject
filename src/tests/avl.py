from random import Random
from sys import stderr
import time
from statistics import median
import matplotlib.pyplot as plt

from trees.avl import AVL

if __name__ == "__main__":
    stderr.write("[ERROR] This file is a module\n")
    exit(-1)


def test_avl_insert():
    r = Random()
    x = AVL()
    rand_range = (0, 50)
    to_insert = 10
    
    start = time.perf_counter()

    for _ in range(to_insert):
        x.insert_key(r.randint(rand_range[0], rand_range[1]))
    print(x)

    stop = time.perf_counter()

    duration = stop - start

    print(duration)

def test_avl_insert_and_remove():
    r = Random()
    duration = list()
    
    for n in range(0,50000,500):
        print(f"Ora faccio il caso n={n}")
        x = AVL()

        #Creo lista
        valori = list(range(0,n+1))
        r.shuffle(valori)

        #Metto n valori casuali nell'albero
        for i in range(0,n):
            x.insert_key(valori[i])

        #Inizialmente inserirò ultimo indice (unico che manca ancora)
        ind = n
        tempi = list()

        #Faccio mediana su un campione di 300 tempi, per ogni n
        for _ in range(300):
            #MISURAZIONE
            start = time.perf_counter()
            x.insert_key(valori[ind])
            stop = time.perf_counter()

            #Aggiungo uno dei 300 tempi: poi farò la mediana di tutti quelli raccolti
            tempi.append(stop - start)

            ind = r.randint(0,n)
            x.remove_key(valori[ind])
        duration.append(median(tempi))
    
    plt.figure(figsize=(8,5))
    plt.plot(list(range(0,50000,500)), duration, marker='.')
    plt.xlabel("Nodi (n)")
    plt.ylabel("Tempo (s)")
    plt.title("AVL tempo inserimento")
    plt.grid(True)

    plt.show()
