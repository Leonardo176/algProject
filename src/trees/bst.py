#!/bin/python3
import sys

if __name__ == "__main__":
    sys.stderr.write("[ERROR] This file is a module\n")
    exit(-1)
    
class Node:
    key: int
    left: "Node | None"
    right: "Node | None"
    parent: "Node | None"

    def __init__(self, key: int, left: "Node | None" = None, right: "Node | None" = None):
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

def height_ric(node: Node | None) -> int:
    if node is None:
        return 0
    else:
        return 1 + max(height_ric(node.left), height_ric(node.right))


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

    def height(self) -> int:
        return height_ric(self.root)

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
            if curr.key < key:
                curr = curr.right
            elif key < curr.key:
                curr = curr.left
            else:
                # TODO: handle error case (key == n key)
                return

        n.parent = p
        if p.key < key:
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

    def remove(self, target: Node | None):
        if target is None:
            return

        # Removes a node in a BST
        if target.left is None:
            self._transplant(target, target.right)
        elif target.right is None:
            self._transplant(target, target.left)
        else:
            next = self.min(target.right)
            if next != target.right:
                self._transplant(next, next.right)
                next.right = target.right
                next.right.parent = next

            self._transplant(target, next)
            next.left = target.left
            next.left.parent = next
        return

    # This function replaces target with node
    # node must be a target's child
    def _transplant(self, target: Node, node: Node | None):
        parent = target.parent
        if parent is None:
            self.root = node
        elif target == parent.left:
            parent.left = node
        else:
            parent.right = node

        if node is not None:
            node.parent = parent
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
    def prv(self, n: Node | None) -> Node | None:
        if n is None:
            return

        # Return BST node's predecessor
        if n.left is not None:
            return self.max(n.left)

        m = n.parent
        while m is not None and n == m.left:
            n = m
            m = n.parent
        return m

    def nxt(self, n: Node | None) -> Node | None:
        if n is None:
            return

        # Returns BST node's successor
        if n.right is not None:
            return self.min(n.right)

        m = n.parent
        while m is not None and n == m.right:
            n = m
            m = n.parent
        return m

    def min(self, n: Node) -> Node:
        while n.left is not None:
            n = n.left
        return n

    def max(self, n: Node) -> Node:
        while n.right is not None:
            n = n.right
        return n

    def rotate_left(self, target: Node | None):
        if target is None or target.right is None:
            return

        # bubble: node that needs to be parent's child
        # bubble_branch: node that needs to be target's child
        bubble = target.right
        bubble_branch = bubble.left

        self._transplant(target, bubble)

        # make target bubble's child
        bubble.left = target
        target.parent = bubble

        # make bubble_branch target's child
        target.right = bubble_branch
        if bubble_branch is not None:
            bubble_branch.parent = target

    def rotate_right(self, target: Node | None):
        if target is None or target.left is None:
            return

        bubble = target.left
        bubble_branch = bubble.right

        self._transplant(target, bubble)

        bubble.right = target
        target.parent = bubble

        target.left = bubble_branch
        if bubble_branch is not None:
            bubble_branch.parent = target