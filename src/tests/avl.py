from random import Random
from sys import stderr

from trees.avl import AVL

if __name__ == "__main__":
    stderr.write("[ERROR] This file is a module\n")
    exit(-1)


def test_avl_insert():
    x = AVL()
    x.insert_key(5)
    x.insert_key(6)
    print(x)
    x.remove_key(5)
    print(x)

def test_avl_insert_and_remove():
    print("test_avl_2")