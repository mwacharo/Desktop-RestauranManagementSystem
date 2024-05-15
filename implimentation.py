# start

import json

def save_data(restaurant):
    data = {
        "customers": [vars(c) for c in restaurant.customers],
        "staff": [vars(s) for s in restaurant.staff_members],
        "orders": [{"items": [(item.name, quantity) for item, quantity in order.order_items], "status": order.status} for order in restaurant.orders]
    }
    with open('restaurant_data.json', 'w') as f:
        json.dump(data, f, indent=4)
def load_data(restaurant):
    try:
        with open('restaurant_data.json', 'r') as f:
            data = json.load(f)
            restaurant.customers = [Customer(c['name'], c['contact'], c['email'], c['password']) for c in data['customers']]
            restaurant.staff_members = [Staff(s['name'], s['employee_id'], s['role']) for s in data['staff']]
            # Load orders - this part might need more elaborate reconstruction based on your design
    except FileNotFoundError:
        print("No previous data found. Starting a new session.")
        
  # This  menu item with name, description, and price      
class MenuItem:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

# represents a customer with their name, contact, email, and password
class Customer:
    def __init__(self, name, contact, email, password):
        self.name = name
        self.contact = contact
        self.email = email
        self.password = password
        self.orders = []

    def register(self, restaurant):
        for customer in restaurant.customers:
            if customer.email == self.email:
                print("Email already registered.")
                return False
        restaurant.customers.append(self)
        # print("Registration successful.")
        #
        return True

    def place_order(self, restaurant, menu_manager):
        print("Available Menu:")
        menu_manager.display_menu()
        while True:
          item_name = input("Choose an item to order by name (type 'done' to finish): ")
          if item_name == "done":
            break
          item = menu_manager.find_menu_item(item_name)
          if item:
            order_type = input("Enter type of order (DineIn, Takeaway, Delivery): ")
            quantity = int(input("Enter quantity: "))
            if order_type == "DineIn":
                table = assign_table(restaurant)
                if table:
                    new_order = DineInOrder(table)
                    new_order.add_item(item, quantity)
                    restaurant.place_order(new_order)
                    self.orders.append(new_order)
                    print("Dine-In order placed with table assignment.")
                    # how can implement table assignment  remember a table has capacity and status and table number
                else:
                    print("No tables available.")
            elif order_type == "Takeaway":
                new_order = TakeawayOrder()
                new_order.add_item(item, quantity)
                restaurant.place_order(new_order)
                self.orders.append(new_order)
                print("Takeaway order placed.")
                
            elif order_type == "Delivery":
                address = input("Enter delivery address: ")
                new_order = DeliveryOrder(address)
                new_order.add_item(item, quantity)
                restaurant.place_order(new_order)
                self.orders.append(new_order)
                new_order.dispatch_rider()
                print("Delivery order placed and rider dispatched.")
                
            else:
                print("Invalid order type specified.")

#  represents a staff member with their name, employee ID, and role
class Staff:
    def __init__(self, name, employee_id, role):
        self.name = name
        self.employee_id = employee_id
        self.role = role

    def manage_orders(self, restaurant):
        if not restaurant.orders:
           print("No orders placed yet.")
           return 
        print("Listing all orders:")
        for index, order in enumerate(restaurant.orders, 1):
            print(f"{index}. {order}")
        choice = int(input("Enter order number to manage: "))
        order = restaurant.orders[choice - 1]
        action = input("Choose action: complete, cancel: ")
        if action == "complete":
            order.complete_order()
        elif action == "cancel":
            order.cancel_order()

# base class for orders
class Order:
    def __init__(self):
        self.order_items = []
        self.status = "Pending"
        self.total_cost = 0


# Method to add an item to the order
    def add_item(self, menu_item, quantity):
        self.order_items.append((menu_item, quantity))
        self.calculate_total()
# Method to calculate the total cost of the order
    def calculate_total(self):
        self.total_cost = sum(
            item.price * quantity for item, quantity in self.order_items
        )
        # Method to complete the order    
    def complete_order(self):
        self.status = "Completed"
        print("Order completed.")
        # Method to cancel the order
    def cancel_order(self):
        self.status = "Canceled"
        print("Order canceled.")    

# represents a dine-in order with a table assigned
class DineInOrder(Order):
    def __init__(self, table):
        super().__init__()
        self.table = table

# represents a takeaway order
class TakeawayOrder(Order):
    def __init__(self):
        super().__init__()

# This class represents a delivery order with a delivery address
class DeliveryOrder(Order):
      def __init__(self, address):
        super().__init__()
        self.delivery_address = address

      def dispatch_rider(self):
         print(f"Dispatching rider for delivery to {self.delivery_address}.")


def assign_table(restaurant):
    for table in restaurant.tables:
        if not table.is_occupied:
            table.is_occupied = True
            return table
    return None

  

# represents table with a number and capacity
class Table:
    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity
        self.is_occupied = False

    # Method to assign a table to an order
    def assign_to_order(self):
        if not self.is_occupied:
            self.is_occupied = True
            return True
        return False

    def release(self):
        self.is_occupied = False
    
     # Representation of the table object
    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity}, Occupied: {self.is_occupied})"
   

class Billing:
    def __init__(self, order):
        self.order = order
        self.total = order.total_cost
        self.is_paid = False

    def process_payment(self, payment_method):
        if not self.is_paid:
            self.is_paid = True
            print(f"Payment of ${self.total} processed via {payment_method}.")
            return True
        return False


class Payment:
    def __init__(self, method, details):
        self.method = method
        self.details = details
        self.is_processed = False

    def process(self, amount):
        if not self.is_processed:
            print(f"Processing ${amount} payment via {self.method}.")
            self.is_processed = True
            return True
        return False

#  manages the menu items
class MenuManager:
    def __init__(self):
        self.menu_items = []

    # Method to add a menu item
    def add_menu_item(self, item):
        self.menu_items.append(item)

    #  find a menu item by name
    def find_menu_item(self, name):
        for item in self.menu_items:
            if item.name == name:
                return item
        return None

     # Method to display the menu
    def display_menu(self):
        for item in self.menu_items:
            print(f"{item.name}: {item.description} at ${item.price}")


class Restaurant:
    def __init__(self):
        self.load_data()

    def save_data(self):
        save_data(self)

    def load_data(self):
        load_data(self)
        
        self.customers = []
        self.staff_members = []
        self.orders = []
        self.tables = [
            Table(i, 4) for i in range(1, 11)
        ]  # Example: 10 tables with 4 seats each
        self.menu_manager = MenuManager()

    def place_order(self, order):
        self.orders.append(order)
        print("Order added to the system.")

    def add_staff(self, staff):
        self.staff_members.append(staff)
        print(f"Staff member {staff.name} added to the system. ")


def main():
    # Create an instance of Restaurant
    restaurant = Restaurant()

    # Add some menu items
    restaurant.menu_manager.add_menu_item(
        MenuItem("Pizza", "A delicious cheese pizza", 10)
    )
    restaurant.menu_manager.add_menu_item(MenuItem("Burger", "A large beef burger", 8))
    restaurant.menu_manager.add_menu_item(MenuItem("Pasta", "Italian pasta with marinara sauce", 12)

    )

    # Simulate interaction
    print("Welcome to the Restaurant Management System")
    while True:
        user_type = input("Are you a 'customer' or 'staff'? (type 'exit' to quit): ")
        if user_type == "exit":
            break
        elif user_type == "customer":
            action = input("Do you want to 'register' or 'place order'?: ")
            if action == "register":
                name = input("Name: ")
                contact = input("Contact: ")
                email = input("Email: ")
                password = input("Password: ")
                customer = Customer(name, contact, email, password)
                if customer.register(restaurant):
                
                    print("Registratio # Method to display the menun successful! Here's our menu:")
                    restaurant.menu_manager.display_menu()
                    customer.place_order(restaurant, restaurant.menu_manager)

                  

                else:
                    print("Registration failed. Email already registered.")
            elif action == "place order":
                email = input("Enter your email: ")
                found = False
                for customer in restaurant.customers:
                    if customer.email == email:
                        customer.place_order(restaurant.menu_manager)
                        found = True
                        break
                if not found:
                    print("Customer not found. Please register first.")
        elif user_type == "staff":
            employee_id = input("Enter your employee ID: ")
            found = False
            for staff in restaurant.staff_members:
                if staff.employee_id == employee_id:
                    staff.manage_orders(restaurant)
                    found = True
                    break
            if not found:
                print("Staff not found.")

            register_option = input(
                "Staff not found. Do you want to register? (yes/no): "
            )

            if register_option.lower() == "yes":
                name = input("Name: ")
                position = input("Position: ")
                employee_id = input("Employee ID: ")
                password = input("Password: ")

                new_staff = Staff(name, position, employee_id)
                restaurant.add_staff(new_staff)
                print("Registration successful!")
                # dispay menu items

                restaurant.menu_manager.display_menu()
                new_staff.manage_orders(restaurant)

            else:
                print("Returning to main menu.")


if __name__ == "__main__":
    main()
    
    restaurant = Restaurant()
    try:
        main(restaurant)
    finally:
        restaurant.save_data()
