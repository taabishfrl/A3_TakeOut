# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Iterator
from data_structures import ArrayR
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
        


class Restaurant:
    def __init__(self, name: str, block_number: int, initial_menu: ArrayR[MenuItem]):
        """
            Constructor for Restaurant.
            Complexity Analysis: 
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
            Complexity Analysis:
            ...
        """
        restaurant = self.restaurants[restaurant_name]
        if restaurant is None:
            raise KeyError(f'Restaurant {restaurant_name} not found')
        return restaurant.menu
        

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]):
        """
            Add an ArrayR of MenuItems to a Restaurant's menu.
            Complexity Analysis:
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
            Complexity Analysis (across all __next__ calls):
            ...
        """
        pass


if __name__ == "__main__":
    # Test your code here
    
    # First restaurant with no initial menu items
    first_restaurant = Restaurant("Testaurant", 3, ArrayR(0))
    
    # Add to the FF app
    ff = FoodFlight()

    ff.add_restaurant(first_restaurant)
    
    # Add to Testaurant's menu
    new_items = ArrayR(3)
    new_items[0] = MenuItem("Chips", 2)
    new_items[1] = MenuItem("Pizza", 4)
    new_items[2] = MenuItem("Burger", 3)
    
    ff.add_to_menu("Testaurant", new_items)
    
    # Get the best item from the menu
    print("Best menu item:", ff.get_menu("Testaurant")[0])
    
