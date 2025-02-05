# from item import Item
class Cart:
    # Initialize the Cart with an empty list of items
    def __init__(self):
        self.items = []

    # Retrieve an item by its name
    def add_item(self, name, quantity, price):
        existing_item = self.get_item(name)
        if existing_item:
            existing_item["quantity"] += quantity
        else:
            self.items.append({"name": name, "price": price, "quantity": quantity})

    def get_item(self, name):
        for item in self.items:
            if item["name"] == name:
                return item
        return None  # Item not found

    # Edit an existing item's details in the cart
    def edit_item(self, name, new_price=None, new_quantity=None):
        item = self.get_item(name)  # Find the item by name
        if item:
            # Update item's quantity and price if provided
            item.quantity = new_quantity if new_quantity is not None else item.quantity
            item.price = new_price if new_price is not None else item.price
        else:
            raise ValueError(f"Item '{name}' not found in cart.")  # Item not found in cart

    # Delete an item from the cart
    def delete_item(self, name):
        # Remove the item by matching the 'name' key in the dictionary
        self.items = [item for item in self.items if item["name"] != name]

    # Display the cart items in a formatted manner
    def display_cart(self):
        for item in self.items:
            print(f"Item: {item.name}, Quantity: {item.quantity}, Price: {item.price} PHP")

    # Get all items in the cart (used for updating the cart list in GUI)
    def get_items(self):
        return self.items
