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
        self.height = 1 #Nuovo nodo altezza 1 da foglia

def get_height(node : Node | None):
    return node.height if node is not None else 0

#Aggiorno la altezza basandomi su l'altezza dei figli
def update_height(node: AVLNode | None):
    if node is not None:
        node.height = 1 + max(get_height(node.left), get_height(node.right))

class AVL(BST):
    root: AVLNode | None
    #La proprietà counter_rotations la contiene già la classe padre BST

    def __init__(self, root: AVLNode | None = None):
        super().__init__(root)
        self.root = root

    #fattore bilancio di un singolo nodo
    def balance_factor(self, node: Node | None):
        if node is None:
            return 0
        #get_height ritorna 0 se il nodo è nullo
        return get_height(node.left) - get_height(node.right)

    def rotate_right(self, target: Node | None):
        if target is None:
            return
        y = target.left

        BST.rotate_right(self, target)

        #Aggiorno nodi usati e cambiati di posizione
        update_height(target)
        update_height(y)

    def rotate_left(self, target: Node | None):
        if target is None:
            return
        y = target.right

        BST.rotate_left(self, target)

        update_height(target)
        update_height(y)

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
        start = target.parent

        if target.left is not None and target.right is not None:
            succ_node = self.nxt(target) #Mi salvo il successore che troverà BST da sostituire al nodo
            
            start = succ_node.parent  #qui è da dove parte ribilanciamento

            if target == start:
                start = target.parent

        BST.remove(self, target)
        self.balance_avl(start)

    def balance_avl(self, x ):
        while x is not None:
            update_height(x)
            
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
