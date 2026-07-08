# Corso di Algoritmi e Strutture Dati - Università degli Studi di Udine - A.A 2025-26
# Progetto di Sebastiano Babich (172249), Leonardo Mazzon (172587) e Damiano Netto (171948)

from enum import Enum


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


class BST:
    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root is None:
            return "NULL "
        else:
            return (
                f"{self.root.key} "
                + BST(self.root.left).__str__()
                + BST(self.root.right).__str__()
            )

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


class Direction(Enum):
    SX = 1
    DX = 2

    def inv(self):
        if self == Direction.SX:
            return Direction.DX
        else:
            return Direction.SX


def direction(node):
    parent = node.parent
    assert parent is not None

    if parent.left == node:
        return Direction.SX
    else:
        return Direction.DX


def db_dir(parent, db):
    if db is not None:
        return direction(db)
    elif parent.left is None:
        return Direction.SX
    else:
        return Direction.DX


def sibling(node):
    parent = node.parent
    if parent is None:
        return None

    if parent.left == node:
        return parent.right
    else:
        return parent.left


def db_sibling(parent, db):
    if db_dir(parent, db) == Direction.SX:
        assert parent.right is not None
        return parent.right
    else:
        assert parent.left is not None
        return parent.left


def color(node):
    return getattr(node, "color", "black") if node is not None else "black"


def set_color(node, color_val):
    if node is not None:
        setattr(node, "color", color_val)


def recolor(node):
    if color(node) == "black":
        set_color(node, "red")
    else:
        set_color(node, "black")


class RBTree(BST):
    def __init__(self, root=None):
        super().__init__(root)

    def _root_black(self):
        set_color(self.root, "black")

    def insert_key(self, key):
        self.insert(TreeNode(key))

    def insert(self, node):
        # ensure that n is red
        set_color(node, "red")

        super().insert(node)
        target = self.find(node.key)

        assert target is not None

        parent = target.parent

        self._root_black()

        if color(parent) == "black":
            return

        assert parent is not None

        grandparent = parent.parent

        assert grandparent is not None

        parent_sibling = sibling(parent)

        while color(parent) == "red" and color(parent_sibling) == "red":
            assert parent_sibling is not None

            recolor(grandparent)
            recolor(parent)
            recolor(parent_sibling)

            target = grandparent

            if target.parent is not None and color(target.parent) == "red":
                parent = target.parent
            else:
                self._root_black()
                return

            if parent.parent is not None:
                grandparent = parent.parent
            else:
                self._root_black()
                return

            parent_sibling = sibling(parent)

        recolor(grandparent)

        match direction(target), direction(parent).inv():
            case Direction.SX, Direction.SX:
                recolor(target)
                self.rotate_right(parent)
                self.rotate_left(grandparent)
            case Direction.SX, Direction.DX:
                recolor(parent)
                self.rotate_right(grandparent)
            case Direction.DX, Direction.SX:
                recolor(parent)
                self.rotate_left(grandparent)
            case Direction.DX, Direction.DX:
                recolor(target)
                self.rotate_left(parent)
                self.rotate_right(grandparent)

    def remove(self, node):
        if node is None:
            return

        if node.left is not None and node.right is not None:
            nxt = self.nxt(node)
            assert nxt is not None

            key = node.key
            node.key = nxt.key
            nxt.key = key

            node = nxt

        parent, c = node.parent, color(node)
        db = node.left if node.left is not None else node.right

        self._transplant(node, db)

        if parent is None or (c == "red" and db is None):
            self._root_black()
            return

        # fix double black

        sib = db_sibling(parent, db)

        if color(sib) == "red":
            self.red_sibling(parent, db)
        elif color(sib.left) == "black" and color(sib.right) == "black":
            self.unlucky(parent, db)
        else:
            self.almost_lucky_and_lucky(parent, db)

    # subcases for remove

    def lucky(self, parent, db):
        sib = db_sibling(parent, db)
        if db_dir(parent, db) == Direction.SX:
            n = sib.right
            assert n is not None
            recolor(n)
            set_color(sib, color(parent))
            set_color(parent, "black")
            self.rotate_left(parent)
        else:
            n = sib.left
            assert n is not None
            recolor(n)
            set_color(sib, color(parent))
            set_color(parent, "black")
            self.rotate_right(parent)

    def almost_lucky_and_lucky(self, parent, db):
        sib = db_sibling(parent, db)

        if db_dir(parent, db) == Direction.SX:
            if color(sib.right) == "red":
                self.lucky(parent, db)
                return

            n = sib.left
            assert n is not None

            recolor(n)
            recolor(sib)

            self.rotate_right(sib)
            self.lucky(parent, db)
        else:
            if color(sib.left) == "red":
                self.lucky(parent, db)
                return

            n = sib.right
            assert n is not None

            recolor(n)
            recolor(sib)

            self.rotate_left(sib)
            self.lucky(parent, db)

    def unlucky(self, parent, db):
        sib = db_sibling(parent, db)

        while (
            color(sib) == "black"
            and color(sib.left) == "black"
            and color(sib.right) == "black"
        ):
            recolor(sib)

            if color(parent) == "red":
                recolor(parent)
                return

            grandparent = parent.parent

            if grandparent is not None:
                sib = sibling(parent)
                assert sib is not None
                db = parent
                parent = grandparent
            else:
                return

        if color(sib) == "red":
            self.red_sibling(parent, db)
        else:
            self.almost_lucky_and_lucky(parent, db)

    def red_sibling(self, parent, db):
        sib = db_sibling(parent, db)
        recolor(sib)
        recolor(parent)

        if db_dir(parent, db) == Direction.SX:
            self.rotate_left(parent)
            sib = parent.right
        else:
            self.rotate_right(parent)
            sib = parent.left

        assert sib is not None

        if color(sib.left) == "black" and color(sib.right) == "black":
            self.unlucky(parent, db)
        else:
            self.almost_lucky_and_lucky(parent, db)
