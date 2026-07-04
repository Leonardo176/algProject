from random import Random
from sys import stderr

from trees.avl import AVL

if __name__ == "__main__":
    stderr.write("[ERROR] This file is a module\n")
    exit(-1)


def test_avl_insert():
    r = Random()
    x = AVL()
    rand_range = (0, 50)
    to_insert = 10
    
    for _ in range(to_insert):
        x.insert_key(r.randint(rand_range[0], rand_range[1]))
    print(x)

def test_avl_insert_and_remove():
    r = Random()
    x = AVL()
    rand_range = (0, 50)
    to_insert = 10
    to_remove = 5
    
    for _ in range(to_insert):
        x.insert_key(r.randint(rand_range[0], rand_range[1]))
    print(x)
    
    for _ in range(to_remove):
        x.remove_key(r.randint(rand_range[0], rand_range[1]))
    print(x)