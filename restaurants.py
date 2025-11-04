# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Iterator
from data_structures import ArrayR,ArrayMaxHeap
from better_bst import BetterBinarySearchTree
from algorithms import mergesort

@total_ordering
class MenuItem:
    def __init__(self, name: str, rating: float):
        """
            Constructor for Restaurant.
            No analysis required.
        """
        self.name = name
        self.rating = rating
        
    def __eq__(self, other):
        return self.rating == other.rating and self.name == other.name
    
    def __lt__(self, other):
        if self.rating != other.rating:
            return self.rating > other.rating
        return self.name < other.name
    
    def __str__(self):
        """
            String representation method for MenuItem class.
            Implementation optional - perhaps useful for debugging.
            No analysis required.
        """
        return f"MenuItem <{self.name}, {self.rating}>"

@total_ordering
class ComparableMenuItem:
    """
    This is a wrapper that reverses the comparison logic so that we can use it correctly with max-heap
    which typically expects a natural ascending order.
    """
    def __init__(self, menu_item):
        self.menu_item = menu_item

    def __eq__(self, other):
        return self.menu_item == other.menu_item

    def __lt__(self, other):
        return self.menu_item > other.menu_item
        

class Restaurant:
    def __init__(self, name: str, block_number: int, initial_menu: ArrayR[MenuItem]):
        """
            Constructor for Restaurant.
            
            Complexity Analysis: Best and Worst case is both O(N log N), where N is the len(initial_menu),
            this is the case as regardless of the contents, we are always performing merge_sort on the menu,
            thereby, O(N log N) dominates the complexity. Best and worst case is the same as regardless of whether
            it is already sorted or reverse sorted, the method will perform the same number of operations.
            ...
        """
        self.name = name
        self.block_number = block_number
        self.menu = ArrayR(len(initial_menu))

        for i in range(len(initial_menu)):
            self.menu[i] = initial_menu[i]
        self.menu = mergesort(self.menu)

    
    def __str__(self):
        """
            String representation method for Restaurant class.
            Implementation optional - perhaps useful for debugging.
            No analysis required.
        """
        return f"Restaurant <{self.name},{self.block_number},{self.menu}>"
        

class FoodFlight:
    def __init__(self):
        """
            Constructor for FoodFlight.

            Complexity Analysis: Best and Worst case is O(1), this is the case as we are simply performing
            the same constant-time initializing of the BetterBinarySearchTree and does not depend on any input size.
            ...
        """
        self.restaurants = BetterBinarySearchTree()

    
        
    
    def add_restaurant(self, restaurant: Restaurant):
        """
            Register a `restaurant` in the FoodFlight app.

            Complexity Analysis: Best case is O(log R + M), where R is the number of restaurants registered, and
            M is len(restaurant.name), this is the case when the tree is balanced, requiring O(log R) time for insertion
            and O(M) time to process the restaurant name.

            Worst case is also O(log R + M),where R is the number of restaurants registered, and M is len(restaurant.name),
            this is the case as we can assume the BST is always magically balanced, thus maintaining the logarithmic insertion time
            regardless of the order.
            ...
        """
        self.restaurants[restaurant.name] = restaurant
        
    
    def get_menu(self, restaurant_name: str):
        """
            Return all menu items for a restaurant in decreasing order of their ratings.

            Complexity Analysis: Best case and Worst case is O(log R + M), where M is len(restaurant.name) and R
            is the number of restaurants stored in the BST. Both cases are the same as, the BST is magically balanced
            therefore resulting in O(log R) traversal and the time complexity to process the string is always O(M) regardless
            of the size. Therefore, BST lookup takes O(log R) steps, with each step involving O(M) string comparison.
            ...
        """
        restaurant = self.restaurants[restaurant_name]
        if restaurant is None:
            raise KeyError(f'Restaurant {restaurant_name} not found')
        return restaurant.menu
        

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]):
        """
            Add an ArrayR of MenuItems to a Restaurant's menu.

            Complexity Analysis: Best and worst case is O(N + (n+m) log (n+m)), where N is len(restaurant.name),
            n is the number of menu items that the restaurant has prior to adding the new ones and m is the number 
            of new menu items being added to the restaurant's menu, this is the case as the merge_sort algortihm dominates
            the complexity, and always performs the same number of operations regardless of the contents. As a result, the best
            and worst case is the same.

            ...
        """
        restaurant = self.restaurants[restaurant_name]
        if restaurant is None:
            raise KeyError(f'Restaurant {restaurant_name} not found')
        
        current_count = len(restaurant.menu)
        new_count = len(new_items)
        combined = ArrayR(current_count + new_count)
        
        for i in range(current_count):
            combined[i] = restaurant.menu[i]
        for i in range(new_count):
            combined[current_count + i] = new_items[i]
        
        restaurant.menu = mergesort(combined)
    
    
    def meal_suggestions(self, user_block_number: int, max_walk: int) -> Iterator[MenuItem]:
        """
            Yield all menu items within max_walk blocks of the user's current block.

            Complexity Analysis (across all __next__ calls): Best and Worst case is O(T + n log R), where T is the total
            number of restaurants, R is the number of candidate restaurants within walking distance, and n is the total 
            number of menu items from those R restaurants. This is the case as the function always has to look
            through all the restaurants to find which is within walking distance which takes O(T) time and return all the menus
            from those restaurants and return the best items, which takes O(n log R) time. Thereby, the time complexity is O(T + n log R).
             

            ...
        """
        candidates = ArrayR(0)
        count = 0

        for _, restaurant in self.restaurants:
            if abs(restaurant.block_number - user_block_number) <= max_walk:

                if len(restaurant.menu) > 0:

                    if count == len(candidates):
                        new_size = max(2 * count, 1)
                        new_candidates = ArrayR(new_size)
                        for i in range(count):
                            new_candidates[i] = candidates[i]
                        candidates = new_candidates
                    
                    candidates[count] = (restaurant.menu, 0)
                    count += 1

        if count == 0:
            return

        exact_candidates = ArrayR(count)
        for i in range(count):
            exact_candidates[i] = candidates[i]
        candidates = exact_candidates

        heap = ArrayMaxHeap(count)

        for i in range(count):
            menu, index = candidates[i]
            heap.add((ComparableMenuItem(menu[index]), i, index))

        while len(heap) > 0:
            wrapped_item, rest_i, index_in_menu = heap.extract_max()
            yield wrapped_item.menu_item

            menu, _ = candidates[rest_i]
            next_index = index_in_menu + 1
            if next_index < len(menu):
                heap.add((ComparableMenuItem(menu[next_index]), rest_i, next_index))


if __name__ == "__main__":
    # Test your code here
    
    # First restaurant with no initial menu items
    menu1 = ArrayR(3)
    menu1[0] = MenuItem("A", 7)
    menu1[1] = MenuItem("B", 8)
    menu1[2] = MenuItem("Z", 8)

    menu2 = ArrayR(2)
    menu2[0] = MenuItem("Noodles", 6)
    menu2[1] = MenuItem("Soup", 8)

    r1 = Restaurant("EatPlace", 1, menu1)
    r2 = Restaurant("SuperSoup", 10, menu2)

    ff = FoodFlight()
    ff.add_restaurant(r1)
    ff.add_restaurant(r2)

    print("EatPlace menu (should be: [B, Z, A]):")
    print([m.name for m in ff.get_menu("EatPlace")])

    print("SuperSoup menu (should be: [Soup, Noodles]):")
    print([m.name for m in ff.get_menu("SuperSoup")])

    # Add more items and test sorting & tie-breaker
    add_items = ArrayR(2)
    add_items[0] = MenuItem("Apple", 8)
    add_items[1] = MenuItem("Banana", 8)
    ff.add_to_menu("EatPlace", add_items)

    print("EatPlace updated menu (should be: [Apple, B, Banana, Z, A]):")
    print([m.name for m in ff.get_menu("EatPlace")])

    try:
        ff.get_menu("Nope")
    except KeyError as e:
        print("Caught missing restaurant:", e)

    print("Meal Suggestions for block 99, max_walk=1 (empty):")
    for item in ff.meal_suggestions(99, 1):
        print(item)  # Should print nothing

    add_new = ArrayR(2)
    add_new[0] = MenuItem("Avocado", 10)
    add_new[1] = MenuItem("Zucchini", 10)
    ff.add_to_menu("EatPlace", add_new)
    print("EatPlace final menu:",[m.name for m in ff.get_menu("EatPlace")])  # Should be ['Avocado', 'Zucchini', ... rest]

    print("Meal Suggestions for block 1, max_walk=0:")
    for item in ff.meal_suggestions(1, 0):
        print(item)  # Should print Avocado (10), Zucchini (10), Apple (8), ... etc


    