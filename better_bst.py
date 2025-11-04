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

            
        """
        result = ArrayList() 
        self.recursive_search(self.__root, low, high, result)
        return result
    
    def recursive_search(self, node: BinaryNode[K,V] | None, low: K, high: K, result: ArrayList[V]) -> None:
        if node is None:
            return
        if node.key > low:
            self.recursive_search(node.left, low, high, result)
        if low <= node.key <= high:
            result.append(node.item)
        if node.key < high:
            self.recursive_search(node.right, low, high, result)

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
            
        """
        
        def subtree_height(node: BinaryNode[K,V] | None):
            if node is None:
                return -1
            left_height = subtree_height(node.left)
            right_height = subtree_height(node.right)
            return 1 + max(left_height, right_height)
        
        tree_height = subtree_height(self.__root)
        total_nodes = len(self)

        if total_nodes > 0:
            ideal_height = math.floor(math.log2(total_nodes))
        else:
            ideal_height = 0

        return tree_height - ideal_height
    
    
    
    def rebalance(self):
        """
            Restructure the BST such that it is balanced.
            
            Do *not* return a new instance; rather, this method
            should modify the tree it is called on.

            Complexity Analysis: Best case is O(N), where N is the number of nodes in the BST.In this case,
            the method has to iterate through every node in the BST once by the in-order iterator to collect 
            the (key,item) pairs which takes O(N) time. When reconstructing the BST,it takes O(N) time,
            using the helper method build_balanced(). This happens regardless of how balanced the tree is.

            Worst case is also O(N), where N is the numnber of nodes in the BST, the worst and best case is the same,
            as regardless of how balanced or unbalanced the tree is, it still has to iterate and check every node, so that
            it can reconstruct the BST which takes O(N) time.
            
        """
        bst_size = len(self)
        if bst_size == 0:
            return

        inorder_items = ArrayR(bst_size)
        for i, (key, item) in enumerate(self):  
            inorder_items[i] = (key, item)

        self._BetterBinarySearchTree__root = self.build_balanced_bst(inorder_items, 0, bst_size - 1)


    def build_balanced_bst(self, nodes: ArrayR, start: int, end: int) -> BinaryNode[K, V] | None:
        if start > end:
            return None
        
        mid = (start + end) // 2
        key, item = nodes[mid]
        
        root = BinaryNode(item, key)
        
        root.left = self.build_balanced_bst(nodes, start, mid - 1)
        root.right = self.build_balanced_bst(nodes, mid + 1, end)
        
        return root
    

            

if __name__ == "__main__":
    # Test your code here.
    
    # Create a Better BST
    reb_bst = BetterBinarySearchTree()
    for k in [6, 5, 4, 3, 2, 1]:
        reb_bst[k] = str(k)
    pre_rebalance_score = reb_bst.balance_score()
    reb_bst.rebalance()
    post_rebalance_score = reb_bst.balance_score()
    print(f"Rebalance - before: {pre_rebalance_score}, after: {post_rebalance_score} (after should be 0)")
