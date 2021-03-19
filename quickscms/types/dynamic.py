## --------------------------------------------------------------------------------

from quickscms.types.static import AVLTreeNode

class AVLTree():

    def __init__(self):
         self.root = None
    
    def _get_height(self, root: AVLTreeNode) -> int:
        if not root:
            return 0
        else:
            return root.height

    def _insert(self, root: AVLTreeNode, key, val=None) -> AVLTreeNode:
        if not root:
            return AVLTreeNode(key, val, bf=0)
        if key < root.key:
            left_sub_root = self._insert(root.left, key, val)
            root.left = left_sub_root
            left_sub_root.parent = root
        if key > root.key:
            right_sub_root = self._insert(root.right, key, val)
            root.right = right_sub_root
            right_sub_root.parent = root
        else:
            return root #we have a duplicate key

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        return self.rebalance(root)

    def insert(self, key, val=None):
        self.root = self._insert(self.root, key, val)

    def rebalance(self, root: AVLTreeNode) -> AVLTreeNode:
        """
        Main rebalance routine to rebalance the tree rooted at root appropriately using rotations.
        4 cases:
        1) bf(root) = 2 and bf(root.left) < 0 ==> L-R Imbalance
        2) bf(root) = 2 ==> L-L Imbalance
        3) bf(root) = -2 and bf(root.right) > 0 ==> R-L Imbalance
        4) bf(root) = -2 ==> R-R Imbalance
        :param root: root of tree needing rebalancing.
        :return: root of resulting tree after rotations
        """
        if root.bf == 2:
            if root.left.bf < 0:  # L-R
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            else:  # L-L
                return self.rotate_right(root)
        elif root.bf == -2:
            if root.right.bf > 0:  # R-L
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)
            else:  # R-R
                return self.rotate_left(root)
        else:
            return root  # no need to rebalance

    def rotate_right(self, root: AVLTreeNode) -> AVLTreeNode:
        """
        Performs a right rotation on the tree rooted at root, and returns root of resulting tree
        :param root: root of tree
        :Time: O(1)
        :Space: O(1)
        :return: root of updated tree
        """
        pivot = root.left  # set up pointers
        tmp = pivot.right
        # 1st Move: reassign pivot's right child to root and update parent pointers
        pivot.right = root
        pivot.parent = root.parent  # pivot's parent now root's parent
        root.parent = pivot  # root's parent now pivot
        # 2nd Move: use saved right child of pivot and assign it to root's left and update its parent
        root.left = tmp
        if tmp:  # tmp can be null
            tmp.parent = root

        # Not done yet - need to update pivot's parent (manually check which one matches the root that was passed)
        if pivot.parent:
            if pivot.parent.left == root:  # if the parent's left subtree is the one to be updated
                pivot.parent.left = pivot  # assign the pivot as the new child
            else:
                pivot.parent.right = pivot  # vice-versa for right child

        # Still not done :) -- update heights and bf's using tracked heights
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.bf = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot  # return root of new tree

    def rotate_left(self, root: AVLTreeNode) -> AVLTreeNode:
        """
        Performs a left rotation on the tree rooted at root, and returns root of resulting tree.
        :param root: root of tree
        :Time: O(1)
        :Space: O(1)
        :return: root of updated tree.
        """
        pivot = root.right
        tmp = pivot.left

        pivot.left = root
        pivot.parent = root.parent
        root.parent = pivot

        root.right = tmp
        if tmp:  # tmp can be null
            tmp.parent = root

        # Not done -- need to update pivot's parent as well
        if pivot.parent:
            if pivot.parent.left == root:  # if the parent's left subtree is the one to be updated
                pivot.parent.left = pivot  # assign the pivot as the new child
            else:
                pivot.parent.right = pivot  # vice-versa for right child
        # Still not done :) -- update heights and bf's using tracked heights
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.bf = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot  # return root of new tree

    def _get_height(self, root: AVLTreeNode) -> int:
        """
        Overridden to account for the fact that we are tracking heights during tree construction.
        :param root: root of subtree of which to get height for
        :return: height of tree rooted at root
        """
        if not root:  # empty tree means height of 0
            return 0
        else:
            return root.height  # return instance var height

    @staticmethod
    def burst_insert(a: list):
        """
        Inserts a list of n items into an AVL Tree and returns the root.
        :param a: list of items
        :Time: O(N*log(N))
        :Space: O(N)
        :return: tree root
        """
        root = AVLTree()
        for item in a:
            root.insert(item)
        return root
    
    def get_min(self) -> AVLTreeNode:
        '''
        '''
        return self.root

    def delete(self) -> AVLTreeNode:
        '''
        '''
        returning_node = self.root

        if self.root.left != None:
            self.root.right.parent = self.root.left
            self.root = self.root.left
        if self.root.right != None:
            self.root.left.parent = self.root.right
            self.root = self.root.right
        self.rebalance(self.root)

        return returning_node

        

## --------------------------------------------------------------------------------