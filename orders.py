# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from data_structures import List, ArrayR, ArrayMaxHeap,ArrayList

class Order:
    def __init__(self, hunger: int, location: tuple[float, float]):
        """
            Constructor for Order.
            No analysis required.
        """
        self.hunger = hunger
        self.location = location
        self.distance = None
        
        
    def __str__(self):
        return f"Order <Hunger: {self.hunger} ,Location: {self.location} , Distance: {self.distance:.2f}>"
    
    
class OrderDispatch:
    def __init__(self, dispatch_location: tuple[float, float], max_orders: int):
        """
            Constructor for OrderDispatch.

            Complexity Analysis: Best and Worst case is O(1), as the function is simply performing
            constant-time operations such as assigning variables and initializing an ArrayMaxHeao with
            max_orders constant value.
            ...
        """
        self.dispatch_location = dispatch_location
        self.max_orders = max_orders
        self.orders = ArrayMaxHeap(max_orders)
    
    
    def __len__(self):
        """
            Return the number of pending orders in the dispatch system.
            No analysis required.
        """
        return len(self._orders)
        
    
    def receive_order(self, order: Order):
        """
            Receive a new Food Flight order into the dispatch system.

            Complexity Analysis: Best and Worst case is O(log N), where N is the number of orders
            that are currently in the system. This is the case as inseertion into a heap will always
            take O(log N) time to maintain the heap property, regardless of the state of the heap. 
            Calculating the distance and checking the max order limit of the heap are constant time
            operations, thereby the O(log N) dominates the complexity.
            ...
        """
        if len(self.orders) >= self.max_orders:
            raise Exception("Maximum Limit Of Orders Reached!")
            
        x_diff = order.location[0] - self.dispatch_location[0]
        y_diff = order.location[1] - self.dispatch_location[1]
        order.distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)

        score = 4 * order.distance - 5 * order.hunger
        self.orders.add((-score, order))
        
    
    def deliver_single(self) -> Order:
        """
            Deliver a single pending order with the lowest
            FoodFast (TM) score.
            See specifications for details.

            Complexity Analysis: Best and Worst case is O(log N), where N is the number of orders in the
            heap, this is the case when all elements are distinct, and extract_max always takes O(log N) time to get
            the max element, regardless of the contents of the heap.
            ...
        """
        if len(self.orders) == 0:
            raise Exception("No pending orders")

        _, order = self.orders.extract_max()
        return order
        
    
    def deliver_multiple(self, max_travel: float) -> List[Order]:
        """
            Deliver as many orders, prioritising orders such that
            lower FoodFast (TM) scores are delivered first.
            See specifications for details.

            Complexity Analysis: Best case is O(log N), where N is the number of orders in the heap. This is the case
            when after the first order is extracted and delivered, the max_travel limit is exceeded so the function is terminated.
            extract_max always takes O(log N) time to get the element with the highest priority, therefore the complexity is O(log N).

            Worst case is O(M log N), where N is the number of orders in the heap, and M is the number of orders actually delivered.
            This is the case when all the orders are extracted and delivered, therefore, the extract_max runs for O(log N) per call.
            Therefore, the time complexity if O(M log N).
            ...
        """
        delivered_orders = ArrayList()
        current_location = self.dispatch_location
        remaining_travel = max_travel
        total_travel = 0.0

        while len(self.orders) > 0:
            
            _, next_order = self.orders.extract_max()
            to_order = math.sqrt((next_order.location[0] - current_location[0]) ** 2 +(next_order.location[1] - current_location[1]) ** 2)

            to_home = math.sqrt((next_order.location[0] - self.dispatch_location[0]) ** 2 +(next_order.location[1] - self.dispatch_location[1]) ** 2)

            if total_travel + to_order + to_home > max_travel:
                score = 4 * next_order.distance - 5 * next_order.hunger
                self.orders.add((-score, next_order))
                break

            delivered_orders.insert(len(delivered_orders), next_order)
            remaining_travel -= to_order
            current_location = next_order.location

        return delivered_orders
        

    def order_surge_1054(self, surge_batch: ArrayR[Order]):
        """
            Add all orders from surge batch, ensuring this is done as
            efficiently as possible to minimise downtime.

            Complexity Analysis:
            ...
        """
        pass


if __name__ == "__main__":
    # Test your code here

    # Let's create a dispatch and a few orders
    # Create the dispatch location and system
    dispatch_location = (0, 0)
    dispatch = OrderDispatch(dispatch_location, max_orders=5)
    dispatch.receive_order(Order(4, (10, 10)))  # Far from dispatch
    dispatch.receive_order(Order(3, (15, 16)))  # Even farther

    # Set a very small max_travel (cannot even reach the first and return)
    max_travel = 5

    delivered = dispatch.deliver_multiple(max_travel)

    print(f"Delivered {len(delivered)} order(s) (should be 0):")
    for order in delivered:
        print(order)