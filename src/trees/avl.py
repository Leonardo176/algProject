#!/bin/python3
import sys
from src.trees.bst import BST, Node

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)

def height(node):
    if node == None:
        return 0
    if getattr(node, "height", None) is None:
        node.height = 1 + max(height(node.get_left_child()), height(node.get_right_child()))
    return node.height

def invalidate_height(node):
    while node is not None:
        node.height = None
        node = node.get_parent()
    
class AVL(BST):
    def __init__(self, root = None):
        super().__init__(root)
        
    def right_rotate(self, x):
        p = x.get_parent() # Uso i getter che son in bst.py
        y = x.get_left_child()
        
        if y is None: # Se non c'è figlio sinistro non posso ruotare
            return

        if p is None: #Cioè p era il root/radice
            self.root = y #Dopo la rotazione y diventa la radice
            y.set_parent(None)
        else:
            if x == p.get_left_child(): #Metto y al figlio giusto del padre p
                p.set_left_child(y)
            else:
                p.set_right_child(y)
            y.set_parent(p) #Aggiorno genitore nodo y
                
        z = y.get_right_child()
        x.set_left_child(z) #Il sottoalbero viene assegnato come figlio di x
        if z is not None:
            z.set_parent(x) #Il nuovo genitore del sottoalbero diventa x

        y.set_right_child(x) #x viene spostato come figlio destro di y
        x.set_parent(y) #x (spostato) ha un nuovo genitore

        invalidate_height(x)
        invalidate_height(y)

    def left_rotate(self, x): #Caso speculare
        p = x.get_parent() # uso i getter che son in bst.py
        y = x.get_right_child()
        
        if y is None:
            return

        if p is None:
            self.root = y
            y.set_parent(None)
        else:
            if x == p.get_left_child():
                p.set_left_child(y)
            else:
                p.set_right_child(y)
            y.set_parent(p)

        z = y.get_left_child()
        x.set_right_child(z)
        if z is not None:
            z.set_parent(x)

        y.set_left_child(x)
        x.set_parent(y)

        invalidate_height(x)
        invalidate_height(y)

    def insert(self, node):
        pass 

    def remove(self, node):
        pass