#!/bin/python3
import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)


class BST:
    root: Node | None

    def __init__(self, root=None):
        self.root = root
        return

    def __str__(self):
        if self.root is None:
            return "NULL "
        else:
            return (
                f"{self.root.key} "
                + BST(self.root.left).__str__()
                + BST(self.root.right).__str__()
            )

    # elementary operations

    def insert(self, n: Node):
        # Insert a node in a BST
        key = n.key

        if self.root is None:
            self.root = n
            return

        curr = self.root
        p = curr
        while curr is not None:
            p = curr
            if key > curr.key:
                curr = curr.right
            elif key < curr.key:
                curr = curr.left
            else:
                # TODO: handle error case (key == n key)
                return

        n.parent = p
        if key > p.key:
            p.right = n
        elif key < p.key:
            p.left = n

        return

    def insert_key(self, key: int):
        # Insert a key in a BST
        return self.insert(Node(key))

    def find(self, key: int):
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

    def remove_key(self, key: int):
        # Removes a key in a BST
        return self.remove(self.find(key))

    def remove(self, z: Node | None):
        if z is None:
            return

        # Removes a node in a BST
        if z.left is None:
            self.__transplant(z, z.right)
        elif z.right is None:
            self.__transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            if y != z.right:
                self.__transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__transplant(z, y)
            y.left = z.left
            y.left.parent = y
        return

    # This function substitutes the node u with v.
    def __transplant(self, u: Node, v: Node | None):
        parent = u.parent
        if parent is None:
            self.root = v
        elif u == parent.left:
            parent.left = v
        else:
            parent.right = v

        if v is not None:
            v.parent = parent
        return

    # traversals (and private helper functions)
    def inorder(self) -> list[int]:
        # Returns string containing InOrder traversal of Tree
        return self.__inorder(self.root)

    def __inorder(self, n: Node | None) -> list[int]:
        el = []
        stack = []
        current = n

        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left

            current = stack.pop()
            el.append(current.key)
            current = current.right

        return el

    def preorder(self) -> list[int]:
        # Returns string containing PreOrder traversal of Tree
        return self.__preorder(self.root)

    def __preorder(self, n: Node | None) -> list[int]:
        el = []
        if n is None:
            return el

        stack = [n]

        while stack:
            current = stack.pop()
            el.append(current.key)

            if current.right is not None:
                stack.append(current.right)
            if current.left is not None:
                stack.append(current.left)

        return el

    def postorder(self) -> list[int]:
        # Returns string containing PostOrder traversal of Tree
        return self.__postorder(self.root)

    def __postorder(self, n: Node | None) -> list[int]:
        el = []

        if n is None:
            return el

        stack1 = [n]
        stack2 = []
        while stack1:
            current = stack1.pop()
            stack2.append(current)

            if current.left is not None:
                stack1.append(current.left)
            if current.right is not None:
                stack1.append(current.right)

        # now stack2 should contain the reverse of the postorder traversal
        while stack2:
            el.append(stack2.pop().key)

        return el

    # predecessor & successor
    def prv(self, n: Node) -> Node | None:
        # Return BST node's predecessor
        if n.left is not None:
            return self.maximum(n.left)

        m = n.parent
        while m is not None and n == m.left:
            n = m
            m = n.parent
        return m

    def nxt(self, n: Node) -> Node | None:
        # Returns BST node's successor
        if n.right is not None:
            return self.minimum(n.right)

        m = n.parent
        while m is not None and n == m.right:
            n = m
            m = n.parent
        return m

    # minimum & maximum
    def minimum(self, n: Node) -> Node:
        # Returns minimum
        while n.left is not None:
            n = n.left
        return n

    def maximum(self, n: Node) -> Node:
        # Return maximum
        while n.right is not None:
            n = n.right
        return n

    def rotate_left(self, x: Node | None):
        if x is None or x.right is None:
            return

        p = x.parent
        y = x.right

        if p is None:
            self.root = y
            y.parent = None
        else:
            if x == p.left:
                p.left = y
            else:
                p.right = y
            y.parent = p

        z = y.left
        x.right = z
        if z is not None:
            z.parent = x

        y.left = x
        x.parent = y

    def rotate_right(self, x: Node | None):
        if x is None or x.left is None:
            return

        p = x.parent
        y = x.left

        if p is None:  # Cioè p era il root/radice
            self.root = y  # Dopo la rotazione y diventa la radice
            y.parent = None
        else:
            if x == p.left:  # Metto y al figlio giusto del padre p
                p.left = y
            else:
                p.right = y
            y.parent = p  # Aggiorno genitore nodo y

        z = y.right
        x.left = z  # Il sottoalbero viene assegnato come figlio di x
        if z is not None:
            z.parent = x  # Il nuovo genitore del sottoalbero diventa x

        y.right = x  # x viene spostato come figlio destro di y
        x.parent = y  # x (spostato) ha un nuovo genitore


class Node:
    key: int
    left: Node | None
    right: Node | None
    parent: Node | None

    def __init__(self, key: int, left: Node | None = None, right: Node | None = None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = None
        if left is not None:
            left.parent = self
        if right is not None:
            right.parent = self

    def __str__(self):
        return str(self.key)
