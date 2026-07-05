from random import Random
from sys import stderr
import time
from statistics import median
import matplotlib.pyplot as plt

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

def test_insertion(type_of_tree: TreeType):
    r = Random()
    duration = list()
    
    n_min = 1000
    n_max = 10000000

    lista_num_elementi = []

    c = (n_max - n_min) ** (1/99)

    for i in range(0,100):
        n_i = round(n_min*(c**i))

        #Non vado oltre il massimo consentito
        if n_i>100000:
            break

        lista_num_elementi.append(n_i)

    for n in lista_num_elementi:
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
    plt.plot(lista_num_elementi, duration, marker='.')
    plt.xlabel("Nodi (n)")
    plt.ylabel("Tempo (s)")
    plt.title(f"{type_of_tree.value} tempo inserimento")
    plt.grid(True)

    filename = f"src/tests/{type_of_tree.value}_plot.png"

    plt.savefig(filename)