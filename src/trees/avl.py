#!/bin/python3
import sys

from src.trees.bst import BST, Node

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)


class AVLNode(Node):
    height: int | None

    def __init__(
        self, key: int, left: AVLNode | None = None, right: AVLNode | None = None
    ):
        super().__init__(key, left, right)
        self.height = None


def height(node):
    if node is None:
        return 0
    if getattr(node, "height", None) is None:
        node.height = 1 + max(height(node.left), height(node.right))
    return node.height


def invalidate_height(node):
    while node is not None:
        node.height = None
        node = node.parent


class AVL(BST):
    def __init__(self, root: AVLNode | None = None):
        super().__init__(root)

    def rotate_right(self, x: Node | None):
        if x is None:
            return
        y = x.left

        self.rotate_right(x)

        invalidate_height(x)
        invalidate_height(y)

    def rotate_left(self, x: Node | None):
        if x is None:
            return
        y = x.right

        self.rotate_left(x)

        invalidate_height(x)
        invalidate_height(y)

    def insert(self, n: Node):
        pass

    def remove(self, z: Node | None):
        pass
