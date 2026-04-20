#!/bin/python3
import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)


class BST:
    # builtin overridable functions
    def __init__(self, root=None):
        # Init a new BST
        self.root = root
        return

    def __str__(self):
        if self.root is None:
            return "NULL "
        else:
            return (
                f"{self.root.get_key()} "
                + BST(self.root.get_left_child()).__str__()
                + BST(self.root.get_right_child()).__str__()
            )

    def __repr__(self):
        return "BinarySearchTree"

    # elementary operations

    def insert(self, n):
        # Insert a node in a BST
        key = n.get_key()

        if self.root is None:
            self.root = n
            return

        curr = self.root
        p = curr
        while curr is not None:
            p = curr
            if key > curr.get_key():
                curr = curr.get_right_child()
            elif key < curr.get_key():
                curr = curr.get_left_child()
            else:
                # TODO: handle error case (key == n key)
                return

        # create new node
        n.set_parent(p)
        if key > p.get_key():
            p.set_right_child(n)
        elif key < p.get_key():
            p.set_left_child(n)

        return

    def insert_key(self, key):
        # Insert a key in a BST
        return self.insert(Node(key))

    def find(self, key):
        # Returns a BST node of a given key, otherwise it returns None
        n = self.root

        while n is not None:
            if key == n.get_key():
                return n
            elif key < n.get_key():
                n = n.get_left_child()
            elif key > n.get_key():
                n = n.get_right_child()
        return None

    def remove_key(self, key):
        # Removes a key in a BST
        return self.remove(self.find(key))

    def remove(self, z):
        # Removes a node in a BST
        if z.get_left_child() is None:
            self.__transplant(z, z.get_right_child())
        elif z.get_right_child() is None:
            self.__transplant(z, z.get_left_child())
        else:
            y = self.minimum(z.get_right_child())
            if y != z.get_right_child():
                self.__transplant(y, y.get_right_child())
                y.set_right_child(z.get_right_child())
                y.get_right_child().set_parent(y)

            self.__transplant(z, y)
            y.set_left_child(z.get_left_child())
            y.get_left_child().set_parent(y)
        return

    # This function substitutes the node u with v.
    def __transplant(self, u, v):
        parent = u.get_parent()
        if parent is None:
            self.root = v
        elif u == parent.get_left_child():
            parent.set_left_child(v)
        else:
            parent.set_right_child(v)

        if v is not None:
            v.set_parent(parent)
        return

    # traversals (and private helper functions)
    def inorder(self):
        # Returns string containing InOrder traversal of Tree
        return self.__inorder(self.root)

    def __inorder(self, n):
        el = []
        stack = []
        current = n

        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.get_left_child()

            current = stack.pop()
            el.append(current.get_key())
            current = current.get_right_child()

        return el

    def preorder(self):
        # Returns string containing PreOrder traversal of Tree
        return self.__preorder(self.root)

    def __preorder(self, n):
        el = []
        stack = [n]

        while stack:
            current = stack.pop()
            el.append(current.get_key())

            if current.get_right_child() is not None:
                stack.append(current.get_right_child())
            if current.get_left_child() is not None:
                stack.append(current.get_left_child())

        return el

    def postorder(self):
        # Returns string containing PostOrder traversal of Tree
        return self.__postorder(self.root)

    def __postorder(self, n):
        el = []
        stack1 = [n]
        stack2 = []
        while stack1:
            current = stack1.pop()
            stack2.append(current)

            if current.get_left_child() is not None:
                stack1.append(current.get_left_child())
            if current.get_right_child() is not None:
                stack1.append(current.get_right_child())

        # now stack2 should contain the reverse of the postorder traversal
        while stack2:
            el.append(stack2.pop().get_key())

        return el

    # predecessor & successor
    def prv(self, n):
        # Return BST node's predecessor
        if n.get_left_child() is not None:
            return self.maximum(n.get_left_child())

        m = n.get_parent()
        while m is not None and n == m.get_left_child():
            n = m
            m = n.get_parent()
        return m

    def nxt(self, n):
        # Returns BST node's successor
        if n.get_right_child() is not None:
            return self.minimum(n.get_right_child())

        m = n.get_parent()
        while m is not None and n == m.get_right_child():
            n = m
            m = n.get_parent()
        return m

    # minimum & maximum
    def minimum(self, n):
        # Returns minimum
        while n.get_left_child() is not None:
            n = n.get_left_child()
        return n

    def maximum(self, n):
        # Return maximum
        while n.get_right_child() is not None:
            n = n.get_right_child()
        return n

    # getters
    def get_head(self):
        return self.root


class Node:
    def __init__(self, key):
        self.__key = key
        self.__left = None
        self.__right = None
        self.__parent = None
        return

    def __str__(self):
        return str(self.__key)

    # getters
    def get_parent(self):
        # Get parent of BST node
        return self.__parent

    def get_left_child(self):
        # Get right child of BST node
        return self.__left

    def get_right_child(self):
        # Get left child of BST node
        return self.__right

    def get_key(self):
        # Get key of BST node
        return self.__key

    # setters
    def set_parent(self, parent):
        # Set parent of BST node
        self.__parent = parent

    def set_left_child(self, left):
        # Set right child of BST node
        self.__left = left

    def set_right_child(self, right):
        # Set left child of BST node
        self.__right = right
