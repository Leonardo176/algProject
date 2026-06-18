#!/bin/python3
import sys

from trees.bst import BST, Node

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)
    
class AVLNode(Node):
    height: int | None
    parent: "AVLNode | None"

    def __init__(self, key: int, left: "AVLNode | None" = None, right: "AVLNode | None" = None):
        super().__init__(key, left, right)
        self.height = None

def height(node : Node | None):
    if node is None:
        return 0
    if getattr(node, "height", None) is None:
        node.height = 1 + max(height(node.left), height(node.right))
    return node.height

#Rende nulle tutte le altezze
def invalidate_height(node : AVLNode | None):
    while node is not None:
        node.height = None
        node = node.parent


class AVL(BST):
    root: AVLNode | None

    def __init__(self, root: AVLNode | None = None):
        super().__init__(root)
        self.root = root

    #fattore bilancio di un singolo nodo
    def balance_factor(self, node: Node | None):
        if node is None:
            return 0
        #height ritorna 0 se il nodo è nullo!
        return height(node.left) - height(node.right)

    def rotate_right(self, target: Node | None):
        if target is None:
            return
        y = target.left

        BST.rotate_right(self, target)

        invalidate_height(target)
        invalidate_height(y)

    def rotate_left(self, target: Node | None):
        if target is None:
            return
        y = target.right

        BST.rotate_left(self, target)

        invalidate_height(target)
        invalidate_height(y)

    def insert_key(self, key: int):
        return self._insert(AVLNode(key))
    
    def _insert(self, n: AVLNode):
        BST.insert(self, n)

        self.balance_avl(n)

    def remove_key(self, key: int):
        target = self.find(key)
        if target is None: #Previene cancellazione chiave che non esiste (non trovata)
            return
        else:
            self._remove(target)

    def _remove(self, target: AVLNode):
        start = target.parent #attenzione se target era radice (?)

        if target.left is not None and target.right is not None:
            succ_node = self.nxt(target) #Mi salvo il successore che troverà BST da sostituire al nodo
            start = succ_node.parent  #qui è da dove parte ribilanciamento

        BST.remove(self, target)

        self.balance_avl(start)

    def balance_avl(self, x ):
        while x is not None:
            invalidate_height(x)
            
            balance_factor = self.balance_factor(x)
            
            if balance_factor > 1:
                if self.balance_factor(x.left) < 0:
                    self.rotate_left(x.left)
                self.rotate_right(x)
            elif balance_factor < -1:
                if self.balance_factor(x.right) > 0:
                    self.rotate_right(x.right)
                self.rotate_left(x)
                
            #Mi sposto in su, fin tanto che x è la radice, poi mi fermerò (vedi while)
            x = x.parent
