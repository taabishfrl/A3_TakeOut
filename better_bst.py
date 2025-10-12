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
            Complexity Analysis:
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
        pass
        
    
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