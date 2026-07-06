from enum import Enum

from trees.bst import BST, Node


class Direction(Enum):
    SX = 1
    DX = 2

    def inv(self) -> "Direction":
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


def db_dir(parent: Node, db: Node | None) -> Direction:
    if db is not None:
        return direction(db)
    elif parent.left is None:
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


def db_sibling(parent: Node, db: Node | None) -> Node:
    if db_dir(parent, db) == Direction.SX:
        assert parent.right is not None
        return parent.right
    else:
        assert parent.left is not None
        return parent.left


class RBTNode(Node):
    # color must be "red" or "black"
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


class RBT(BST):
    root: Node | None
    counter_rotations: int

    def __init__(self, root=None):
        super().__init__(root)
        counter_rotations = 0

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

    def remove(self, target: Node | None):
        if target is None:
            return

        if target.left is not None and target.right is not None:
            nxt = self.nxt(target)
            assert nxt is not None

            key = target.key
            target.key = nxt.key
            nxt.key = key

            target = nxt

        parent, c = target.parent, color(target)
        db = target.left if target.left is not None else target.right

        self._transplant(target, db)

        if parent is None or (c == "red" and db is None):
            self._root_black()
            return

        # fix double black

        sibling = db_sibling(parent, db)

        if color(sibling) == "red":
            self.red_sibling(parent, db)
        elif color(sibling.left) == "black" and color(sibling.right) == "black":
            self.unlucky(parent, db)
        else:
            self.almost_lucky_and_lucky(parent, db)

    # }

    # subcases for remove

    def lucky(self, parent: Node, db: Node | None):  # {
        sibling = db_sibling(parent, db)
        if db_dir(parent, db) == Direction.SX:
            n = sibling.right
            assert n is not None
            recolor(n)
            set_color(sibling, color(parent))
            set_color(parent, "black")
            self.rotate_left(parent)
        else:
            n = sibling.left
            assert n is not None
            recolor(n)
            set_color(sibling, color(parent))
            set_color(parent, "black")
            self.rotate_right(parent)

    # }

    def almost_lucky_and_lucky(self, parent: Node, db: Node | None):
        sibling = db_sibling(parent, db)

        if db_dir(parent, db) == Direction.SX:
            if color(sibling.right) == "red":
                self.lucky(parent, db)
                return

            n = sibling.left
            assert n is not None

            recolor(n)
            recolor(sibling)

            self.rotate_right(sibling)
            self.lucky(parent, db)
        else:
            if color(sibling.left) == "red":
                self.lucky(parent, db)
                return

            n = sibling.right
            assert n is not None

            recolor(n)
            recolor(sibling)

            self.rotate_left(sibling)
            self.lucky(parent, db)

    # }

    def unlucky(self, parent: Node, db: Node | None):
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

    # }

    def red_sibling(self, parent: Node, db: Node | None):
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