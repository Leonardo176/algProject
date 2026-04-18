#!/bin/python3
import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)


class BinarySearchTree:
    # builtin overridable functions
    def __init__(self):
        """Init a new BST"""
        self.__head = None
        return

    def __str__(self):
        """Print an inorder traversal of BST"""
        return str(self.inorder())

    def __repr__(self):
        return "BinarySearchTree"

    # elementary operations
    def insert(self, key):
        """Insert a key in a BST"""
        if self.__head is None:
            self.__head = Node(key)

        n = self.__head
        p = None
        while n is not None:
            p = n
            if key > n.get_key():
                n = n.get_right_child()
            elif key < n.get_key():
                n = n.get_left_child()
            else:
                # TODO: handle error case (key == n key)
                return

        # create new node
        n = Node(key)
        n.set_parent(p)
        if key > p.get_key():
            p.set_right_child(n)
        elif key < p.get_key():
            p.set_left_child(n)

        return

    def get(self, key):
        """Returns a BST node of a given key, otherwise it returns None"""
        n = self.__head

        while n is not None:
            if key == n.get_key():
                return n
            elif key < n.get_key():
                n = n.get_left_child()
            elif key > n.get_key():
                n = n.get_right_child()
        return None

    def remove_key(self, key):
        """Removes a key in a BST"""
        return self.remove(self.get(key))

    def remove(self, z):
        """Removes a node in a BST"""
        if z.get_left_child() is None:
            self.transplant(z, z.get_right_child())
        elif z.get_right_child() is None:
            self.transplant(z, z.get_left_child())
        else:
            y = self.minimum(z.get_right_child())
            if y != z.get_right_child():
                self.transplant(y, y.get_right_child())
                y.set_right_child(z.get_right_child())
                y.get_right_child().set_parent(y)

            self.transplant(z, y)
            y.set_left_child(z.get_left_child())
            y.get_left_child().set_parent(y)
        return

    def transplant(self, u, v):
        if u.get_parent() is None:
            self.__head = v
        elif u == u.get_parent().get_left_child():
            u.get_parent().set_left_child(v)
        else:
            u.get_parent().set_right_child(v)

        if v is not None:
            v.set_parent(u.get_parent())
        return

    # traversals (and private helper functions)
    def inorder(self):
        """Returns string containing InOrder traversal of Tree"""
        return self.__inorder([], self.__head)

    def __inorder(self, el, n):
        el = []
        if n is not None:
            el = el + self.__inorder([], n.get_left_child())
            el.append(n.get_key())
            el = el + self.__inorder([], n.get_right_child())
        return el

    def preorder(self, n=-1):
        """Returns string containing PreOrder traversal of Tree"""
        return self.__preorder([], self.__head)

    def __preorder(self, el, n):
        el = []
        if n is not None:
            el.append(n.get_key())
            el = el + self.__preorder([], n.get_left_child())
            el = el + self.__preorder([], n.get_right_child())
        return el

    def postorder(self, n=-1):
        """Returns string containing PostOrder traversal of Tree"""
        return self.__postorder([], self.__head)

    def __postorder(self, el, n):
        el = []
        if n is not None:
            el = el + self.__postorder([], n.get_left_child())
            el = el + self.__postorder([], n.get_right_child())
            el.append(n.get_key())
        return el

    # predecessor & successor
    def predecessor(self, n):
        """Return BST node's predecessor"""
        if n.get_left_child() is not None:
            return self.maximum(n.get_left_child())

        m = n.get_parent()
        while m is not None and n == m.get_left_child():
            n = m
            m = n.get_parent()
        return m

    def successor(self, n):
        """Returns BST node's successor"""
        if n.get_right_child() is not None:
            return self.minimum(n.get_right_child())

        m = n.get_parent()
        while m is not None and n == m.get_right_child():
            n = m
            m = n.get_parent()
        return m

    # minimum & maximum
    def minimum(self, n):
        """Returns minimum"""
        while n.get_left_child() is not None:
            n = n.get_left_child()
        return n

    def maximum(self, n):
        """Return maximum"""
        while n.get_right_child() is not None:
            n = n.get_right_child()
        return n

    # getters
    def get_head(self):
        return self.__head


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
        """Get parent of BST node"""
        return self.__parent

    def get_left_child(self):
        """Get right child of BST node"""
        return self.__left

    def get_right_child(self):
        """Get left child of BST node"""
        return self.__right

    def get_key(self):
        """Get key of BST node"""
        return self.__key

    # setters
    def set_parent(self, parent):
        """Set parent of BST node"""
        self.__parent = parent

    def set_left_child(self, left):
        """Set right child of BST node"""
        self.__left = left

    def set_right_child(self, right):
        """Set left child of BST node"""
        self.__right = right
