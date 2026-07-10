#!/bin/python3

# Corso di Algoritmi e Strutture Dati - Università degli Studi di Udine - A.A 2025-26
# Progetto di Sebastiano Babich (172249), Leonardo Mazzon (172587) e Damiano Netto (171948)

import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)

from trees.bst import BST, Node


# AVLNode inherits from the BST Node class
class AVLNode(Node):
    height: int | None
    parent: "AVLNode | None"

    def __init__(self, key: int, left: "AVLNode | None" = None, right: "AVLNode | None" = None):
        super().__init__(key, left, right)
        # Setting the initial height of an AVLNode to 1
        self.height = 1

# Returning the height of a node or 0 if the node is None
def get_height(node : AVLNode | None):
    return node.height if node is not None else 0

# Updating the height of a node based on the height of its left and right children
def update_height(node: AVLNode | None):
    if node is not None:
        node.height = 1 + max(get_height(node.left), get_height(node.right))


# AVL class inherits fundamental operations from the BST class
class AVL(BST):
    root: AVLNode | None

    def __init__(self, root: AVLNode | None = None):
        super().__init__(root)
        self.root = root

    # Calculating the balance factor to detect AVL imbalance
    def balance_factor(self, node: Node | None):
        if node is None:
            return 0
        return get_height(node.left) - get_height(node.right)

	# Performing the same BST rotation while updating node heights to preserve AVL properties
    def rotate_right(self, target: Node | None):
        if target is None:
            return
        y = target.left

        BST.rotate_right(self, target)

        # Updating height of node affected during rotation
        update_height(target)
        update_height(y)

	# Performing the same BST rotation while updating node heights to preserve AVL properties
    def rotate_left(self, target: Node | None):
        if target is None:
            return
        y = target.right

        BST.rotate_left(self, target)

		# Updating height of node used and moved during rotation
        update_height(target)
        update_height(y)

    def insert_key(self, key: int):
        return self._insert(AVLNode(key))
    
	# Performing BST insertion and then restoring AVL balance through rotations
    def _insert(self, n: AVLNode):
        BST.insert(self, n)

        self.balance_avl(n)

    def remove_key(self, key: int):
        target = self.find(key)
        if target is None:
            return
        else:
            self._remove(target)

	# Performing BST removal while tracking the first affected ancestor, for AVL rebalancing
    def _remove(self, target: AVLNode):
        # Start point consists on the parent of the node to remove
        start = target.parent

        if target.left is not None and target.right is not None:
			# Saving the successore node of the target
            succ_node = self.nxt(target)
            
			# The balancing of the AVL will start from successors parent
            start = succ_node.parent

			# Prevents the start of balancing from a deleted node. This happens when the successor is direct (right) child of the target
            if target == start:
                start = target.parent

        BST.remove(self, target)
        self.balance_avl(start)
	
	# Restoring AVL balance properties
    def balance_avl(self, x):
        while x is not None:
            update_height(x)
            
            balance_factor = self.balance_factor(x)
            
			# Handling the four AVL imbalance cases based on the balance factor and child subtrees
            if balance_factor > 1:
                if self.balance_factor(x.left) < 0:
                    self.rotate_left(x.left)
                self.rotate_right(x)
            elif balance_factor < -1:
                if self.balance_factor(x.right) > 0:
                    self.rotate_right(x.right)
                self.rotate_left(x)
                
            # Move up to the root
            x = x.parent
