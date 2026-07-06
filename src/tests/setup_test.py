from trees.avl import AVL
from trees.bst import BST
from trees.rbt import RBT

from enum import Enum

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
    n_max = 10000

    lista_val_n = []

    c = (n_max / n_min) ** (1 / (samples - 1))

    for i in range(0, samples):
        n_i = round(n_min * (c**i))

        # Non vado oltre il massimo consentito
        if n_i > n_max:
            break

        lista_val_n.append(n_i)

    return lista_val_n