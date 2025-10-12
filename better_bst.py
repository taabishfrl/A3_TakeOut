# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math


from typing import Union
from data_structures import ArrayList, ArrayR
from data_structures.node import BinaryNode
from data_structures.binary_search_tree import BinarySearchTree, K, V

class BetterBinarySearchTree(BinarySearchTree[K, V]):
    def range_query(self, low: K, high: K) -> Union[ArrayR[V], ArrayList[V]]:
        """
            Return all items from the BST with keys,
            in the (inclusive) range of [low, high].
            Return the result in either an ArrayR or an ArrayList.

            Complexity Analysis: Best case is O(log N + K), where N is the the number of nodes in the BST, and K
            is the number of keys in the range low to high. The best case occurs when the BST is balanced, therefore
            the complexity to traverse the height is O(log N), and the range from low to high contains only a few keys, therefore
            the method only has to traverse to height O(log N) and check each node in the range of O(K).

            Worst Case is O(N), where N is the number of nodes in the BST, This happens when the BST is not balanced and the range from low
            to high contains almost every key in the BST, therefore the method has to traverse to height O(N) and check every node in the tree,
            resulting in O(N) time complexity.

            ...
        """
        result = ArrayList() 
        self.range_query_recursive(self.__root, low, high, result)
        return result
    
    def range_query_recursive(self, node: BinaryNode[K,V] | None, low: K, high: K, result: ArrayList[V]) -> None:
        if node is None:
            return
        if node.key > low:
            self.range_query_recursive(node.left, low, high, result)
        if low <= node.key <= high:
            result.append(node.item)
        if node.key < high:
            self.range_query_recursive(node.right, low, high, result)

    def balance_score(self):
        """
            Returns the balance score of the BST, which we define as the
            difference between the ideal (balanced) height of the tree (achievable with a complete tree),
            and the actual height of the tree.

            Complexity Analysis: Best case is O(N), where N is the number of nodes in the BST. The best case happens when
            the BST is perfectly balanced. In this case, the method still has to call the recursive height function and check
            every node atleast once to calculate the height, resulting in O(N) time.

            Worst case is O(N), where N is the number of nodes, The worst case happens when the BST is completely unbalanced like
            a stick. Regardless, the method still calls the recursive height function to check every node atleast once to calculate 
            the height. 
            ...
        """
        def subtree_height(node: BinaryNode[K,V] | None):
            if node is None:
                return -1
            left_height = subtree_height(node.left)
            right_height = subtree_height(node.right)
            return 1 + max(left_height, right_height)
        
        tree_height = subtree_height(self.__root)
        count_nodes = len(self)

        ideal_height = math.floor(math.log2(count_nodes)) if count_nodes > 0 else 0
        return tree_height - ideal_height
    
    
    
    def rebalance(self):
        """
            Restructure the BST such that it is balanced.
            
            Do *not* return a new instance; rather, this method
            should modify the tree it is called on.
            Complexity Analysis:
            ...
        """
        bst_size = len(self)
        if bst_size == 0:
            return
        
        inorder_items = ArrayR(bst_size)
        self.collect_inorder(self._BetterBinarySearchTree__root, inorder_items, 0)
    
        self._BetterBinarySearchTree__root = self.build_balanced(inorder_items, 0, bst_size - 1)

    def collect_inorder(self, node: BinaryNode[K, V] | None, nodes: ArrayR, index: int) -> int:
        if node is None:
            return index
        
        index = self.collect_inorder(node.left, nodes, index)
        
        nodes[index] = (node.key, node.item)
        index += 1
        
        index = self.collect_inorder(node.right, nodes, index)
        
        return index

    def build_balanced(self, nodes: ArrayR, start: int, end: int) -> BinaryNode[K, V] | None:
        if start > end:
            return None
        
        mid = (start + end) // 2
        key, item = nodes[mid]
        
        root = BinaryNode(item, key)
        
        root.left = self.build_balanced(nodes, start, mid - 1)
        root.right = self.build_balanced(nodes, mid + 1, end)
        
        return root
            

if __name__ == "__main__":
    # Test your code here.
    
    # Create a Better BST
    bbst = BetterBinarySearchTree()
    
    # Add all integers as key-value pairs to the tree
    for i in range(10):
        bbst[i] = i
        
    # Try a range query
    # Should give us the values between 4 and 7
    print("Range query:", bbst.range_query(4, 7))
    
    # Check the balance score before balancing
    print("Before balancing:", bbst.balance_score())
    
    # Try a rebalance
    bbst.rebalance()
    
    # How about after?
    print("After balancing:", bbst.balance_score())