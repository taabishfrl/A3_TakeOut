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
        self.arrival_order = 0
    
    
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
        self.orders.add((-score,self.arrival_order, order))
        self.arrival_order += 1
        
    
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
            raise Exception("No orders pending!")

        _,_, order = self.orders.extract_max()
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
            
            _,_, next_order = self.orders.extract_max()

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
    print("=== TASK 3 — Orders & Dispatch Deep Tests ===")

    def show(o: Order) -> str:
        d = "?" if o.distance is None else f"{o.distance:.3f}"
        return f"Order(h={o.hunger}, loc={o.location}, d={d})"

    # 1) Zero-distance highest hunger priority
    ord_disp = OrderDispatch((2, 3), max_orders=10)
    for o in [Order(3, (5, 6)), Order(4, (6, 4)), Order(1, (4, 4))]:
        ord_disp.receive_order(o)
    zero_order = Order(10, (2, 3))
    ord_disp.receive_order(zero_order)
    print("\n[1] deliver_single prefers zero-distance highest hunger")
    print("Actual:", show(ord_disp.deliver_single()))
    print("Expected: Order(h=10, loc=(2, 3), d=0.000)")

    # 2) Tie-breaking (arrival order)
    tied_disp = OrderDispatch((2, 3), max_orders=10)
    tieA = Order(2, (3, 3))
    tieB = Order(2, (3, 3))
    tied_disp.receive_order(tieA)
    tied_disp.receive_order(tieB)
    print("\n[2] Tie behavior by arrival order:")
    print("Actual #1:", show(tied_disp.deliver_single()))
    print("Actual #2:", show(tied_disp.deliver_single()))
    print("Expected: tieA first, then tieB")

    # 3) Capacity limit
    cap_disp = OrderDispatch((0, 0), max_orders=2)
    cap_disp.receive_order(Order(1, (1, 0)))
    cap_disp.receive_order(Order(1, (0, 1)))
    print("\n[3] Capacity check (3rd insert should raise)")
    try:
        cap_disp.receive_order(Order(1, (2, 0)))
        print("Actual:   no error")
    except Exception as e:
        print("Actual:  ", type(e).__name__)
    print("Expected: Exception")

    # 4) Early rejection in deliver_multiple
    reject_disp = OrderDispatch((0, 0), max_orders=5)
    far_order = Order(10, (3, 4))  # distance=5, needs 10 to do round trip
    reject_disp.receive_order(far_order)
    result = reject_disp.deliver_multiple(9.0)
    print("\n[4] deliver_multiple early gate (round trip too far)")
    print("Actual:", [show(x) for x in result], "len=", len(result))
    print("Expected: [] len= 0")

    # 5) Multi-order feasible run
    multi_disp = OrderDispatch((0, 0), max_orders=10)
    A = Order(8, (1, 0))
    B = Order(7, (2, 0))
    C = Order(3, (4, 0))
    for o in [A, B, C]:
        multi_disp.receive_order(o)
    plan = multi_disp.deliver_multiple(5.0)
    print("\n[5] deliver_multiple feasible plan (A then B)")
    print("Actual:", [show(x) for x in plan])
    print("Expected: [Order(h=8, loc=(1, 0), d=1.000), Order(h=7, loc=(2, 0), d=2.000)]")
