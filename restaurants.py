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
    Wrapper for MenuItem that reverses the comparison logic
    so it works correctly with a max-heap which expects natural ascending order.
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
            menu, idx = candidates[i]
            heap.add((ComparableMenuItem(menu[idx]), i, idx))

        while len(heap) > 0:
            wrapped_item, rest_i, idx_in_menu = heap.extract_max()
            yield wrapped_item.menu_item

            menu, _ = candidates[rest_i]
            next_idx = idx_in_menu + 1
            if next_idx < len(menu):
                heap.add((ComparableMenuItem(menu[next_idx]), rest_i, next_idx))


if __name__ == "__main__":
    # Test your code here
    
    # First restaurant with no initial menu items
        giraffis_menu = ArrayR(3)
        giraffis_menu[0] = MenuItem("Chicken Avo Panini", 5)
        giraffis_menu[1] = MenuItem("Vegetarian Focaccia", 2)
        giraffis_menu[2] = MenuItem("Breakfast Muffin", 1)

        jos_pizza_menu = ArrayR(3)
        jos_pizza_menu[0] = MenuItem("Margarita Pizza", 5)
        jos_pizza_menu[1] = MenuItem("Pepperoni Pizza", 3)
        jos_pizza_menu[2] = MenuItem("Vegetarian Pizza", 2)

        # Create restaurant instances at different blocks
        r1 = Restaurant("Giraffis", 4, giraffis_menu)
        r2 = Restaurant("Jo's Pizza", 7, jos_pizza_menu)

        # Create a FoodFlight object and register the restaurants
        ff = FoodFlight()
        ff.add_restaurant(r1)
        ff.add_restaurant(r2)

        # Place the user at block 6, with a max_walk of 2 (so blocks 4 to 8 are reachable)
        iterator = ff.meal_suggestions(6, 2)
        print("Meal Suggestions within 2 blocks of 6:")
        for item in iterator:
            print(item)