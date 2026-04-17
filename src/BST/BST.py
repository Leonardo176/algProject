#!/bin/python3
import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)

class BinarySearchTree:
    # builtin overridable functions
    def __init__(self, key):
        """Init a new BST"""
        self.__head = Node(key)
        return

    def __str__(self):
        """Print an inorder traversal of BST"""
        return str(self.inorder())

    def __repr__(self):
        return "BinarySearchTree"

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
                return bst

        # create new node
        n = Node(key)
        n.set_parent(p)
        if key > p.get_key():
            p.set_right_child(n)
        elif key < p.get_key():
            p.set_left_child(n)

      
    def remove(self, key):
        """Remove a key in a BST"""
        return

    # traversals
    def inorder(self):
        """Returns string containing InOrder traversal of Tree"""
        return self.__inorder([],self.__head)

    def __inorder(self,el, n):
        el = []
        if n is not None:
            el = el + self.__inorder([],n.get_left_child())
            el = el + [n.get_key()]
            el = el + self.__inorder([],n.get_right_child())
        return el

    def preorder(self, n=-1):
        """Returns string containing PreOrder traversal of Tree"""
        return __preorder([],self.__head)

    def __preorder(self,el, n):
        el = []
        if n is not None:
            el = el + [n.get_key()]
            el = el + self.__inorder([],n.get_left_child())
            el = el + self.__inorder([],n.get_right_child())
        return el


    def postorder(self, n=-1):
        """Returns string containing PostOrder traversal of Tree"""
        return __postorder([],self.__head)

    def __postorder(self,el, n):
        el = []
        if n is not None:
            el = el + self.__inorder([],n.get_left_child())
            el = el + self.__inorder([],n.get_right_child())
            el = el + [n.get_key()]
        return el

    # predecessor & successor
    def predecessor(self, n):
        """Return BST node's predecessor"""
        return

    def successor(self, n):
        """Returns BST node's successor"""
        return

    # minimum & maximum
    
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
