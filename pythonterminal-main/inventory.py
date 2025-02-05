from item import Item


class Inventory:
    # Initialize the Inventory with an empty list of items and load the inventory from a file
    def __init__(self):
        self.items = []  # List to store item objects
        self.inventory_file = "inventory.txt"  # File name where inventory is saved
        self.load_inventory()  # Load inventory from the file

    def get_all_items(self):
        return self.items  # Return the list of all items
    # Retrieve an item by its name
    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None  # Return None if item not found

    # Add a new item to the inventory
    def add_item(self, name, price, quantity):
        self.items.append(Item(name, price, quantity))  # Create and add new item object to items list
        self.save_inventory()  # Save the updated inventory to the file

    # Edit an existing item's details
    def edit_item(self, name, new_name=None, new_price=None, new_quantity=None):
        item = self.get_item(name)  # Find the item by name
        if item:
            if new_name:
                item.name = new_name  # Update name if provided
            if new_price is not None:
                item.price = new_price  # Update price if provided
            if new_quantity is not None:
                item.quantity = new_quantity  # Update quantity if provided
            self.save_inventory()  # Save the updated inventory to the file

    # Delete an item from the inventory
    def delete_item(self, name):
        self.items = [item for item in self.items if item.name != name]  # Remove item by name
        self.save_inventory()  # Save the updated inventory to the file

    # Save the current state of the inventory to a file
    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            for item in self.items:
                file.write(f"{item.name},{item.price},{item.quantity}\n")  # Write each item as a line in the file

    # Load the inventory from a file
    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                for line in file:
                    name, price, quantity = line.strip().split(',')  # Parse each line to create item objects
                    self.items.append(Item(name, float(price), int(quantity)))
        except FileNotFoundError:
            pass  # Do nothing if file not found, start with an empty inventory

    # Add a specified quantity to an item
    def add_quantity(self, name, quantity):
        item = self.get_item(name)  # Find the item by name
        if item:
            item.quantity += quantity  # Increase the quantity of the item
            self.save_inventory()  # Save the updated inventory to the file
        else:
            raise ValueError(f"Item '{name}' not found in inventory.")

    # Subtract a specified quantity of an item
    def subtract_item(self, name, quantity):
        item = self.get_item(name)  # Find the item by name
        item.quantity -= quantity  # Subtract the specified quantity from the item's quantity
        self.save_inventory()  # Save the updated inventory to the file
