# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Union
from data_structures import ArrayList, ArrayR
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
    
    def range_query_recursive(self, node, low: K, high: K, result):
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
            Complexity Analysis:
            ...
        """

        
    
    def rebalance(self):
        """
            Restructure the BST such that it is balanced.
            
            Do *not* return a new instance; rather, this method
            should modify the tree it is called on.
            Complexity Analysis:
            ...
        """
        pass
        

if __name__ == "__main__":
    # Test your code here.
        
    bbst = BetterBinarySearchTree()
    bbst[5] = 'A'
    bbst[2] = 'B'
    bbst[4] = 'C'
    bbst[1] = 'D'
    bbst[3] = 'E'

    print("range_query(2,4):", [v for v in bbst.range_query(2, 4)])
    print("range_query(3,4):", [v for v in bbst.range_query(3, 4)])
    print("range_query(0,1):", [v for v in bbst.range_query(0, 1)])