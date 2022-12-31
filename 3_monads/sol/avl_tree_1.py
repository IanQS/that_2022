# AVL tree implementation in Python taken from https://www.programiz.com/dsa/avl-tree
import copy
import sys
from typing import List, Callable


# Create a tree node
class _TreeNode(object):
    def __init__(self, key, maybe_ihm: "MaybeIhm"):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.ihm_data = maybe_ihm


class _AVLTree(object):

    # Function to insert a node
    def insert_node(self, root, key, ihm_data: "OptionalIHM"):

        # Find the correct location and insert the node
        if not root:
            return _TreeNode(key, ihm_data)
        elif key < root.key:
            root.left = self.insert_node(root.left, key, ihm_data)
        else:
            root.right = self.insert_node(root.right, key, ihm_data)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    # Function to delete a node
    def delete_node(self, root, key):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to perform left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def cardinality(self, root: _TreeNode):
        """Custom code"""
        horizon: List[_TreeNode] = [root]
        count = 0
        while horizon:
            curr_node: _TreeNode = horizon.pop()
            if curr_node:
                count += 1
                horizon.append(curr_node.left)
                horizon.append(curr_node.right)
        return count

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key, currPtr.ihm_data)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)


class AVLTree:
    """
    Custom code
    """

    def __init__(self):
        self._root = None
        self._avl_tree = _AVLTree()

    def insert_node(self, key, ihm_data):
        self._root = self._avl_tree.insert_node(self._root, key, ihm_data)

    def delete_node(self, key):
        self._root = self._avl_tree.delete_node(self._root, key)

    def get_height(self):
        return self._avl_tree.getHeight(self._root)

    def get_balance(self):
        return self._avl_tree.getBalance(self._root)

    def __len__(self):
        return self._avl_tree.cardinality(self._root)

    def get_min_value(self):
        return self._avl_tree.getMinValueNode(self._root)

    def map(self, func_to_map: Callable):
        horizon: List[_TreeNode] = [self._root]
        new_tree = AVLTree()
        while horizon:
            curr_node: _TreeNode = horizon.pop()
            if curr_node:
                dc_data = copy.deepcopy(curr_node.ihm_data)
                modified_data = dc_data.bind(func_to_map)
                new_tree.insert_node(modified_data.loss, modified_data)
                horizon.append(curr_node.left)
                horizon.append(curr_node.right)

        return new_tree

    def debug(self):
        self._avl_tree.printHelper(self._root, "", None)

    def filter(self, func_to_filter_with: Callable):
        horizon: List[_TreeNode] = [self._root]
        new_tree = AVLTree()
        while horizon:
            curr_node: _TreeNode = horizon.pop()
            if curr_node:
                ihm_data = curr_node.ihm_data
                if func_to_filter_with(ihm_data):
                    new_tree.insert_node(
                        ihm_data.loss,
                        ihm_data=ihm_data
                    )
                horizon.append(curr_node.left)
                horizon.append(curr_node.right)

        return new_tree


def apply_map(avl_tree: AVLTree, func_to_map: Callable):
    """
    Original Code:
    return list(map(func_to_map, ihm_list))
    """
    return avl_tree.map(func_to_map)


def apply_filter(avl_tree: AVLTree, func_to_filter_with: Callable):
    """
    Original Code:
    return list(filter(func_to_map, ihm_list))
    """
    return avl_tree.filter(func_to_filter_with)
