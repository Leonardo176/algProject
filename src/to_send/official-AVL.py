# Corso di Algoritmi e Strutture Dati - Università degli Studi di Udine - A.A 2025-26
# Progetto di Sebastiano Babich (172249), Leonardo Mazzon (172587) e Damiano Netto (171948)

class TreeNode:
    def __init__(self, key, left = None, right = None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = None
        if left is not None:
            left.parent = self
        if right is not None:
            right.parent = self

def height(node):
    if node == None:
        return 0
    if getattr(node, "height", None) is None:
        node.height = 1 + max(height(node.left), height(node.right))
    return node.height

def invalidate_height(node):
    while node != None:
        node.height = None
        node = node.parent

class BST:
    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root == None:
            return "NULL "
        else:
            return f"{self.root.key} " + BST(self.root.left).__str__() + BST(self.root.right).__str__()

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


# AVLNode extends the TreeNode class used by the BST
class AVLNode(TreeNode):
    def __init__(self, key, left = None, right = None):
        super().__init__(key, left, right)
        # Setting the initial height of an AVLNode to 1
        self.height = 1

# Returning the height of a node or 0 if the node is None
def get_height(node):
    return node.height if node is not None else 0

# Updating the height of a node based on the height of its left and right children
def update_height(node):
    if node is not None:
        node.height = 1 + max(get_height(node.left), get_height(node.right))

# AVL class inherits fundamental operations from the BST class
class AVL(BST):
    def __init__(self, root = None):
        super().__init__(root)

    # Calculating the balance factor to detect AVL imbalance
    def balance_factor(self, node):
        if node is None:
            return 0
        return get_height(node.left) - get_height(node.right)

    # Performing the same BST rotation while updating node heights to preserve AVL properties
    def rotate_right(self, target):
        if target is None:
            return
        y = target.left

        BST.rotate_right(self, target)

        # Updating height of the node affected during rotation
        update_height(target)
        update_height(y)

	# Performing the same BST rotation while updating node heights to preserve AVL properties
    def rotate_left(self, target):
        if target is None:
            return
        y = target.right

        BST.rotate_left(self, target)

		# Updating height of node used and moved during rotation
        update_height(target)
        update_height(y)
    
    def insert_key(self, key):
        return self.insert(AVLNode(key))
    
    # Performing BST insertion and then restoring AVL balance through rotations
    def insert(self, n):
        BST.insert(self, n)

        self.balance_avl(n)

    def remove_key(self, key):
        target = self.find(key)
        if target is None:
            return
        else:
            self.remove(target)

    # Performing BST removal while tracking the first affected ancestor, for AVL rebalancing
    def remove(self, target):
        if target is None:
            return

        # Start point consists on the parent of the node to remove
        start = target.parent

        if target.left is not None and target.right is not None:
            # Saving the successor node of the target
            succ_node = self.nxt(target)
            
            # The balancing of the AVL will start from successors parent
            start = succ_node.parent

            # Preventing the start of balancing from a deleted node. This happens when the successor is direct (right) child of the target
            if target == start:
                start = succ_node

        BST.remove(self, target)
        self.balance_avl(start)
    
    # Restoring AVL balance properties
    def balance_avl(self, x):
        while x is not None:
            update_height(x)
            
            balance_factor = self.balance_factor(x)
            
			# Handling the four AVL imbalance cases based on the balance factor and child subtrees
            if balance_factor > 1:
                if self.balance_factor(x.left) < 0:
                    self.rotate_left(x.left)
                self.rotate_right(x)
            elif balance_factor < -1:
                if self.balance_factor(x.right) > 0:
                    self.rotate_right(x.right)
                self.rotate_left(x)
                
            # Move up to the root
            x = x.parent
