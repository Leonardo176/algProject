from random import Random
from sys import stderr
import time
from statistics import median
import matplotlib.pyplot as plt
import gc

from trees.avl import AVL
from trees.bst import BST
from trees.rbt import RBT

from enum import Enum

class TreeType(Enum):
    BST = "BST"
    AVL = "AVL"
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
    n_min = 1000
    n_max = 1000000

    lista_val_n = []

    c = (n_max / n_min) ** (1/99)

    for i in range(0,100):
        n_i = round(n_min*(c**i))

        #Non vado oltre il massimo consentito
        if n_i>n_max:
            break

        lista_val_n.append(n_i)

    return lista_val_n

def insertion_plot(*types_of_trees: TreeType):
    lista_val_n = calc_lista_val_n()
    strNome = f""
    strPath = "src/tests/"

    #Creo il plot condiviso
    plt.figure(figsize=(8,5))

    for t in types_of_trees:
        print(f"\nAvvio test per {t.value}")
        duration = _test_insertion(t, lista_val_n)

        plt.plot(lista_val_n, duration, marker='.', label=t.value)
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
        print(f"Ora faccio il caso n={n}")
        
        x = create_tree(type_of_tree)

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
        for _ in range(100):
            #MISURAZIONE (fermo garbage collector temporaneamente)
            gc.disable()
            start = time.perf_counter()
            x.insert_key(valori[ind])
            stop = time.perf_counter()
            gc.enable()

            #Aggiungo uno dei 500 tempi: poi farò la mediana di tutti quelli raccolti
            tempi.append(stop - start)

            ind = r.randint(0,n)
            x.remove_key(valori[ind])
        duration.append(median(tempi))
    
    return duration