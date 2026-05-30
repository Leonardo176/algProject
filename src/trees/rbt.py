from enum import Enum

from trees.bst import BST, Node


class Direction(Enum):
    SX = 1
    DX = 2

    def inv(self) -> Direction:
        if self == Direction.SX:
            return Direction.DX
        else:
            return Direction.SX


def direction(node: Node) -> Direction:
    parent = node.parent
    assert parent is not None

    if parent.left == node:
        return Direction.SX
    else:
        return Direction.DX


def sibling(node: Node) -> Node | None:
    parent = node.parent
    if parent is None:
        return None

    if parent.left == node:
        return parent.right
    else:
        return parent.left


class RBTNode(Node):
    # color must "red" or "black"
    color: str

    def __init__(self, key, left=None, right=None):
        super().__init__(key, left, right)
        self.color = "red"


def recolor(node: Node):
    if color(node) == "black":
        set_color(node, "red")
    else:
        set_color(node, "black")


def color(node: Node | None) -> str:
    return getattr(node, "color", "black") if node is not None else "black"


def set_color(node: Node | None, color: str):
    if node is not None:
        setattr(node, "color", color)


class RBTree(BST):
    root: Node | None

    def __init__(self, root=None):
        super().__init__(root)

    def _root_black(self):
        set_color(self.root, "black")

    def insert_key(self, key: int):
        self.insert(RBTNode(key))

    def insert(self, n: Node):
        # ensure that n is red
        set_color(n, "red")

        super().insert(n)
        target = self.find(n.key)

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

    def remove(self, target):
        pass
