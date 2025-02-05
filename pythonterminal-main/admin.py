import tkinter as tk
from tkinter import messagebox, simpledialog


class Admin:
    def __init__(self, inventory):
        self.inventory = inventory

    def add_inventory(self, parent, name, price, quantity):
        # Create a new window for adding inventory
        window = tk.Toplevel(parent)
        window.title("Add New Item")
        window.geometry("300x200")

        # Labels and entry fields for item details
        tk.Label(window, text="Item Name:").pack(pady=5)
        name_entry = tk.Entry(window)
        name_entry.pack(pady=5)

        tk.Label(window, text="Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(window)
        quantity_entry.pack(pady=5)

        tk.Label(window, text="Price:").pack(pady=5)
        price_entry = tk.Entry(window)
        price_entry.pack(pady=5)

        def submit():
            try:
                name = name_entry.get().strip()
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())

                if self.inventory.get_item(name, quantity, price):
                    messagebox.showerror("Error", "Item already exists!")
                else:
                    messagebox.showinfo("Success", f"Item '{name}' added successfully!")
                    window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Ensure price and quantity are numbers.")

        # Submit button
        tk.Button(window, text="Add Item", command=submit).pack(pady=10)

    def edit_inventory(self, name, new_name=None, new_price=None, new_quantity=None):
        self.inventory.edit_item(name, new_name, new_price, new_quantity)

    def _prompt_field(self, field, callback):
        value = simpledialog.askstring("Edit Field", f"Enter new {field.capitalize()}:")
        if value:
            callback(field, value)

    def delete_inventory(self, parent, delete_name_entry):
        name = delete_name_entry.get().strip()  # Access the entry field from the parent window and strip extra spaces
        self.inventory.delete_item(name)
        messagebox.showinfo("Success", f"Item '{name}' deleted successfully!")
        delete_name_entry.delete(0, tk.END)  # Clear the input field after successful deletion
