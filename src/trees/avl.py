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

    def rotate_right(self, target: Node | None):
        if target is None:
            return
        y = target.left

        self.rotate_right(target)

        invalidate_height(target)
        invalidate_height(y)

    def rotate_left(self, target: Node | None):
        if target is None:
            return
        y = target.right

        self.rotate_left(target)

        invalidate_height(target)
        invalidate_height(y)

    def insert(self, n: Node):
        pass

    def remove(self, target: Node | None):
        pass
