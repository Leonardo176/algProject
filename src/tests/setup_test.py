from enum import Enum

from trees.avl import AVL
from trees.bst import BST, height_ric
from trees.rbt import RBT

class TreeType(Enum):
    BST = "BST"
    AVL = "AVL"
    RBT = "RBT"

# Creating the empty tree instance of the selected type_of_tree
def create_tree(type_of_tree: TreeType):
    if type_of_tree == TreeType.BST:
        return BST()
    elif type_of_tree == TreeType.AVL:
        return AVL()
    elif type_of_tree == TreeType.RBT:
        return RBT()
    else:
        raise ValueError(f"Tipo sconosciuto:  {type_of_tree}")


# Generating values of n (number of nodes) via geometric progression to cover a wide range of input sizes
def get_n_values(n_max: int):
    samples = 100
    n_min = 1000

    n_values = []

    c = (n_max / n_min) ** (1 / (samples - 1))

	# Computing n_i for each i in range
    for i in range(0, samples):
        n_i = round(n_min * (c**i))

        # Stop if the generated value exceeds the maximum allowed size.
        if n_i > n_max:
            break

        n_values.append(n_i)

    return n_values