#!/bin/python3
import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)

class BinarySearchTree:
    def __init__(self, key):
        """Init a new BST"""
        self.__head = Node(key)

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
