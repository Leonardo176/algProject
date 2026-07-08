# Corso di Algoritmi e Strutture Dati - Università degli Studi di Udine - A.A 2025-26
# Progetto di Sebastiano Babich (172249), Leonardo Mazzon (172587) e Damiano Netto (171948)

class TreeNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = None
        if left is not None:
            left.parent = self
        if right is not None:
            right.parent = self


# Recursive height computation used for testing in the project
def height_ric(node):
    if node is None:
        return 0
    else:
        return 1 + max(height_ric(node.left), height_ric(node.right))

class BST:
    def __init__(self, root=None):
        self.root = root
        # Used in testing of rotations
        self.rotations_counter = 0

    def __str__(self):
        if self.root == None:
            return "NULL "
        else:
            return f"{self.root.key} " + BST(self.root.left).__str__() + BST(self.root.right).__str__()

    def find(self, key):
        # Returns a BST node of a given key, otherwise it returns None
        n = self.root
        while n is not None:
            if key == n.key:
                return n
            elif key < n.key:
                n = n.left
            else:
                n = n.right
        return None

    def _min(self, n):
        while n.left is not None:
            n = n.left
        return n

    def _max(self, n):
        while n.right is not None:
            n = n.right
        return n

    def nxt(self, node):
        if node is None:
            return None
        # Returns BST node's successor
        if node.right is not None:
            return self._min(node.right)
        m = node.parent
        while m is not None and node == m.right:
            node = m
            m = node.parent
        return m

    def prv(self, node):
        if node is None:
            return None
        # Return BST node's predecessor
        if node.left is not None:
            return self._max(node.left)
        m = node.parent
        while m is not None and node == m.left:
            node = m
            m = node.parent
        return m

    def insert(self, node):
        # Insert a node in a BST
        key = node.key
        if self.root is None:
            self.root = node
            return

        curr = self.root
        p = curr
        while curr is not None:
            p = curr
            if curr.key < key:
                curr = curr.right
            elif key < curr.key:
                curr = curr.left
            else:
                # TODO: handle error case (key == n key)
                return

        node.parent = p
        if p.key < key:
            p.right = node
        elif key < p.key:
            p.left = node

    # This function replaces target with node
    # node must be a target's child
    def _transplant(self, target, node):
        parent = target.parent
        if parent is None:
            self.root = node
        elif target == parent.left:
            parent.left = node
        else:
            parent.right = node
        if node is not None:
            node.parent = parent

    def remove(self, node):
        if node is None:
            return

        # Removes a node in a BST
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            next = self._min(node.right)
            if next != node.right:
                self._transplant(next, next.right)
                next.right = node.right
                next.right.parent = next

            self._transplant(node, next)
            next.left = node.left
            next.left.parent = next

    def rotate_left(self, node):
        if node is None or node.right is None:
            return

        # bubble: node that needs to be parent's child
        # bubble_branch: node that needs to be target's child
        bubble = node.right
        bubble_branch = bubble.left

        self._transplant(node, bubble)

        # make target bubble's child
        bubble.left = node
        node.parent = bubble

        # make bubble_branch target's child
        node.right = bubble_branch
        if bubble_branch is not None:
            bubble_branch.parent = node

        self.rotations_counter += 1

    def rotate_right(self, node):
        if node is None or node.left is None:
            return

        bubble = node.left
        bubble_branch = bubble.right

        self._transplant(node, bubble)

        bubble.right = node
        node.parent = bubble

        node.left = bubble_branch
        if bubble_branch is not None:
            bubble_branch.parent = node
        
        self.rotations_counter += 1
