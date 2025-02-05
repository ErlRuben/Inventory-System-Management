import tkinter as tk
from tkinter import ttk, messagebox
from admin import Admin
from inventory import Inventory
from cart import Cart
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.resizable(False, False)
        # Set fixed size for the window (e.g., 800x600)
        window_width = 800
        window_height = 600

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center the window
        position_top = int((screen_height - window_height) / 2)
        position_left = int((screen_width - window_width) / 2)

        # Set the geometry with a fixed size and centered position
        self.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        # Load and resize the background image
        bg_image = Image.open("Images/MenuBG.jpg")
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        # Create a label to display the background
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Keep reference to the image to prevent garbage collection
        bg_label.image = bg_image

        center_frame = tk.Frame(self, width=650, height=400)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")


        # Add text label in the middle of the frame
        self.text_label = tk.Label(center_frame, text="Welcome to the Inventory Management System",
                                   font=("Helvetica", 20), fg="black")
        self.text_label.place(relx=0.5, rely=0.4, anchor="center")  # Adjust the positioning to be above the button

        # Go to Shopping - Inside the centered frame
        self.customer_button = tk.Button(center_frame, text="Click to Shop!", command=self.open_customer_dashboard,
                                         font=("Helvetica", 20), fg="black", bg=self.cget("bg"),
                                         bd=1, highlightthickness=1)
        self.customer_button.place(relx=0.5, rely=0.6, anchor="center")  # Center the button inside the frame

        # Admin Login - Upper Right with 80% opacity for the button
        self.admin_button = tk.Button(self, text="Admin Login", command=self.open_admin_login, fg="black",
                                      bd=0, highlightthickness=0,font=("Helvetica", 14))
        self.admin_button.place(x=screen_width - 1960, y=110)

        # Initialize inventory and cart
        self.inventory = Inventory()  # Initialize the Inventory
        self.cart = Cart()  # Initialize the Cart

        # Track open windows
        self.current_window = None

    def close_previous_window(self):
        if self.current_window:
            self.current_window.destroy()

    def open_admin_login(self):
        self.close_previous_window()
        self.withdraw()
        # Create the admin login window as a popup
        admin_login_window = tk.Toplevel(self)
        admin_login_window.title("Admin Login")
        admin_login_window.resizable(False, False)

        # Set fixed size for the window (e.g., 800x600)
        window_width = 800
        window_height = 600

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center the window
        position_top = int((screen_height - window_height) / 2)
        position_left = int((screen_width - window_width) / 2)

        # Set the geometry with a fixed size and centered position
        admin_login_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        # Store reference to the current window
        self.current_window = admin_login_window

        # Handle the close button (X button)
        def on_close():
            self.deiconify()  # Re-show the main window
            admin_login_window.destroy()  # Destroy the admin login window

        admin_login_window.protocol("WM_DELETE_WINDOW", on_close)  # Bind the close button event

        # Add a background image
        bg_image = Image.open("Images/MenuBG.jpg")  # Adjust the image path
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # Resize to fit the window
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(admin_login_window, image=bg_image_tk)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window with the image
        bg_label.image = bg_image_tk  # Keep reference to avoid garbage collection

        # Frame to center content
        center_frame = tk.Frame(admin_login_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add Image Above the Text Fields
        image = Image.open("Images/UserIcon.png")  # Adjust the image path
        image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Resize as needed
        image_tk = ImageTk.PhotoImage(image)

        # Create a Label to display the image
        image_label = tk.Label(center_frame, image=image_tk)
        image_label.grid(row=0, column=0, columnspan=2, pady=15)  # Place image above the text fields

        # Keep reference to the image to prevent garbage collection
        image_label.image = image_tk
        def limit_input(entry_text, max_length):
            return len(entry_text) <= max_length

        # Validation commands
        username_vcmd = (self.register(lambda text: limit_input(text, 10)), "%P")
        password_vcmd = (self.register(lambda text: limit_input(text, 12)), "%P")

        # Username and Password fields for Admin Login
        tk.Label(center_frame, text="Username:").grid(row=2, column=0, pady=5, padx=10)
        username_entry = tk.Entry(center_frame, validate="key", validatecommand=username_vcmd)
        username_entry.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(center_frame, text="Password:").grid(row=3, column=0, pady=5, padx=10)
        password_entry = tk.Entry(center_frame, show="*", validate="key", validatecommand=password_vcmd)
        password_entry.grid(row=3, column=1, pady=5, padx=10)

        def login():
            username = username_entry.get().strip().capitalize()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Both fields are required!")
                return

            # Check if credentials are valid
            if self.check_credentials(username, password):
                user_type = self.get_user_type(username)
                if user_type == 'admin':
                    self.close_previous_window()  # Close login window before opening dashboard
                    self.open_admin_dashboard()
                else:
                    messagebox.showerror("Error", "Only admins can log in here.")
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        # Login Button
        login_button = tk.Button(center_frame, text="Login", command=login)
        login_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")  # Place the Login button in the first column

        # Register Button
        register_button = tk.Button(center_frame, text="Click to Sign Up!", command=self.open_register_window)
        register_button.grid(row=4, column=1, padx=10, pady=10,
                             sticky="ew")  # Place the Register button in the second column

    def open_register_window(self):
        self.close_previous_window()
        self.withdraw()

        register_window = tk.Toplevel(self)
        register_window.title("Register Admin")
        register_window.resizable(False, False)

        # Set fixed size for the window (e.g., 800x600)
        window_width = 800
        window_height = 600

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center the window
        position_top = int((screen_height - window_height) / 2)
        position_left = int((screen_width - window_width) / 2)

        # Set the geometry with a fixed size and centered position
        register_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        # Store reference to the current window
        self.current_window = register_window

        def on_close():
            self.deiconify()  # Re-show the main wdowindow
            register_window.destroy()  # Destroy the register win

        register_window.protocol("WM_DELETE_WINDOW", on_close)  # Bind the close button event

        # Add a background image
        bg_image = Image.open("Images/MenuBG.jpg")  # Adjust the image path
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # Resize to fit the window
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(register_window, image=bg_image_tk)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window with the image
        bg_label.image = bg_image_tk  # Keep reference to avoid garbage collection

        # Frame to center content
        center_frame = tk.Frame(register_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Validation functions
        def limit_input(entry_text, max_length):
            return len(entry_text) <= max_length

        # Validation commands
        username_vcmd = (self.register(lambda text: limit_input(text, 10)), "%P")
        password_vcmd = (self.register(lambda text: limit_input(text, 12)), "%P")
        user_type_vcmd = (self.register(lambda text: limit_input(text, 5)), "%P")

        # Username, Password, and User Type fields for Registration
        tk.Label(center_frame, text="Username:").grid(row=0, column=0, pady=5, padx=10)
        username_entry = tk.Entry(center_frame, validate="key", validatecommand=username_vcmd)
        username_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(center_frame, text="Password:").grid(row=1, column=0, pady=5, padx=10)
        password_entry = tk.Entry(center_frame, show="*", validate="key", validatecommand=password_vcmd)
        password_entry.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(center_frame, text="Confirm Password:").grid(row=2, column=0, pady=5, padx=10)
        confirm_password_entry = tk.Entry(center_frame, show="*", validate="key", validatecommand=password_vcmd)
        confirm_password_entry.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(center_frame, text="User Type (admin):").grid(row=3, column=0, pady=5, padx=10)
        user_type_entry = tk.Entry(center_frame, validate="key", validatecommand=user_type_vcmd)
        user_type_entry.grid(row=3, column=1, pady=5, padx=10)

        def cancel_registration():
            # Close the registration window and bring back the main GUI
            self.deiconify()
            register_window.destroy()

        def register():
            username = username_entry.get().strip().capitalize()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            user_type = user_type_entry.get().strip().lower()

            if not username or not password or not confirm_password or not user_type:
                messagebox.showerror("Error", "All fields are required!")
                cancel_registration()
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                cancel_registration()
                return

            if user_type not in ['admin', 'customer']:
                messagebox.showerror("Error", "Invalid user type! Must be 'admin'.")
                cancel_registration()
                return

            # Save user data to file
            self.save_user_data(username, password, user_type)
            messagebox.showinfo("Success", f"User '{username}' registered successfully!")
            cancel_registration()

        # Register Button
        register_button = tk.Button(center_frame, text="Register", command=register)
        register_button.grid(row=4, column=0, pady=10)
        cancel_button = tk.Button(center_frame, text="Cancel", command=cancel_registration)
        cancel_button.grid(row=4, column=1, pady=10)

    def save_user_data(self, username, password, user_type):
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{user_type}\n")

    def check_credentials(self, username, password):
        try:
            with open('users.txt', 'r') as file:
                users = file.readlines()
            for user in users:
                stored_username, stored_password, stored_user_type = user.strip().split(',')
                if stored_username == username and stored_password == password:
                    return True
        except FileNotFoundError:
            return False
        return False

    def get_user_type(self, username):
        try:
            with open('users.txt', 'r') as file:
                users = file.readlines()
            for user in users:
                stored_username, stored_password, stored_user_type = user.strip().split(',')
                if stored_username == username:
                    return stored_user_type
        except FileNotFoundError:
            return None
        return None

    def open_admin_dashboard(self):
        self.close_previous_window()
        self.withdraw()

        admin_window = tk.Toplevel(self)
        admin_window.title("Admin Dashboard")
        admin_window.resizable(False, False)

        # Set fixed size for the window (e.g., 800x600)
        window_width = 800
        window_height = 600

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center the window
        position_top = int((screen_height - window_height) / 2)
        position_left = int((screen_width - window_width) / 2)

        # Set the geometry with a fixed size and centered position
        admin_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        admin = Admin(self.inventory)

        def on_close():
            self.deiconify()  # Re-show the main wdowindow
            admin_window.destroy()  # Destroy the register win

        admin_window.protocol("WM_DELETE_WINDOW", on_close)  # Bind the close button

        # Add dashboard features like Add, Edit, Delete, and Display Inventory
        notebook = ttk.Notebook(admin_window)
        notebook.pack(expand=True, fill="both")

        # Tab: Add New Item
        add_tab = ttk.Frame(notebook)
        notebook.add(add_tab, text="Add New Item")

        tk.Label(add_tab, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_tab)
        name_entry.pack(pady=5)

        tk.Label(add_tab, text="Price:").pack(pady=5)
        price_entry = tk.Entry(add_tab)
        price_entry.pack(pady=5)

        tk.Label(add_tab, text="Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(add_tab)
        quantity_entry.pack(pady=5)

        def add_item():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            quantity = quantity_entry.get().strip()
            if not name or not price or not quantity:
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                # Add item directly to the inventory without opening a new popup
                if self.inventory.get_item(name):
                    messagebox.showerror("Error", "Item already exists!")
                else:
                    self.inventory.add_item(name, float(price), int(quantity))
                    messagebox.showinfo("Success", f"Item '{name}' added successfully!")
                    # Optionally, you can clear the entry fields if needed
                    name_entry.delete(0, tk.END)
                    price_entry.delete(0, tk.END)
                    quantity_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Price and Quantity must be valid numbers!")

        add_button = tk.Button(add_tab, text="Add Item", command=add_item)
        add_button.pack(pady=10)

        # Tab: Edit Item
        edit_tab = ttk.Frame(notebook)
        notebook.add(edit_tab, text="Edit Item")

        tk.Label(edit_tab, text="Name of Item to Edit:").pack(pady=5)
        edit_name_entry = tk.Entry(edit_tab)
        edit_name_entry.pack(pady=5)

        tk.Label(edit_tab, text="New Name (Optional):").pack(pady=5)
        new_name_entry = tk.Entry(edit_tab)
        new_name_entry.pack(pady=5)

        tk.Label(edit_tab, text="New Price (Optional):").pack(pady=5)
        new_price_entry = tk.Entry(edit_tab)
        new_price_entry.pack(pady=5)

        tk.Label(edit_tab, text="New Quantity (Optional):").pack(pady=5)
        new_quantity_entry = tk.Entry(edit_tab)
        new_quantity_entry.pack(pady=5)

        def edit_item():
            edit_name = edit_name_entry.get()
            new_name = new_name_entry.get()
            new_price = new_price_entry.get()
            new_quantity = new_quantity_entry.get()

            if not edit_name:
                messagebox.showerror("Error", "Item name to edit is required!")
                return
            if not admin.inventory.get_item(
                    edit_name):  # Assuming `admin.inventory.get_item()` checks if the item exists
                messagebox.showerror("Error", f"Item '{edit_name}' does not exist!")
                return
            try:
                admin.edit_inventory(
                    edit_name,
                    new_name=new_name if new_name else None,
                    new_price=float(new_price) if new_price else None,
                    new_quantity=int(new_quantity) if new_quantity else None,
                )
                messagebox.showinfo("Success", f"Item '{edit_name}' updated successfully!")
            except ValueError:
                messagebox.showerror("Error", "Price and Quantity must be valid numbers!")

        edit_button = tk.Button(edit_tab, text="Edit Item", command=edit_item)
        edit_button.pack(pady=10)

        # Tab: Delete Item
        delete_tab = ttk.Frame(notebook)
        notebook.add(delete_tab, text="Delete Item")

        tk.Label(delete_tab, text="Name of Item to Delete:").pack(pady=5)
        delete_name_entry = tk.Entry(delete_tab)
        delete_name_entry.pack(pady=5)

        def delete_item():
            delete_name = delete_name_entry.get()
            if not delete_name:
                messagebox.showerror("Error", "Item name is required!")
                return
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{delete_name}'?")
            if confirm:
                # Pass the admin window's delete_tab to delete_inventory
                admin.delete_inventory(admin_window, delete_name_entry)  # Pass the entry field directly

        delete_button = tk.Button(delete_tab, text="Delete Item", command=delete_item)
        delete_button.pack(pady=10)

        # Tab: Display Inventory
        display_tab = ttk.Frame(notebook)
        notebook.add(display_tab, text="Display Inventory")

        listbox = tk.Listbox(display_tab)
        listbox.pack(pady=10, fill="both", expand=True)

        def refresh_inventory():
            listbox.delete(0, tk.END)
            for item in self.inventory.items:
                listbox.insert(tk.END, f"{item.name} - price {item.price} and {item.quantity} in stock")

        refresh_button = tk.Button(display_tab, text="Refresh Inventory", command=refresh_inventory)
        refresh_button.pack(pady=10)

    def open_customer_dashboard(self):
            self.close_previous_window()
            self.withdraw()

            customer_window = tk.Toplevel(self)
            customer_window.title("Customer Shopping")
            customer_window.resizable(False, False)

            # Set fixed size for the window (e.g., 800x600)
            window_width = 800
            window_height = 600

            # Get screen width and height
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Calculate position to center the window
            position_top = int((screen_height - window_height) / 2)
            position_left = int((screen_width - window_width) / 2)

            # Set the geometry with a fixed size and centered position
            customer_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

            # Store reference to the current window
            self.current_window = customer_window

            def on_close():
                confirm = messagebox.askyesno("Are you sure?",
                                              f"You Items will be Returned. Do you want to leave?")
                if confirm:
                    self.deiconify()  # Re-show the main window
                    customer_window.destroy()  # Destroy the customer

            customer_window.protocol("WM_DELETE_WINDOW", on_close)  # Bind the close button event

            # Create a Notebook (Tab) Widget
            notebook = ttk.Notebook(customer_window)
            notebook.pack(fill='both', expand=True)

            # Create Tabs
            shop_tab = ttk.Frame(notebook)
            cart_tab = ttk.Frame(notebook)

            notebook.add(shop_tab, text="Shop")
            notebook.add(cart_tab, text="View Cart")

            # Shop Tab (List of Inventory)
            frame = tk.Frame(shop_tab)  # Create a frame to contain the Listbox and Scrollbar
            frame.pack(pady=20)

            # Create a Listbox with a Scrollbar
            inventory_listbox = tk.Listbox(frame, height=15, width=50)
            inventory_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=inventory_listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            inventory_listbox.config(yscrollcommand=scrollbar.set)

            # Quantity Entry
            quantity_label = tk.Label(shop_tab, text="Quantity:")
            quantity_label.pack(pady=5)
            quantity_entry = tk.Entry(shop_tab)
            quantity_entry.pack(pady=5)

            def refresh_inventory():
                inventory_listbox.delete(0, tk.END)  # Clear the existing list
                for item in self.inventory.get_all_items():
                    inventory_listbox.insert(tk.END, f"{item.name} - {item.price} PHP, Stock: {item.quantity}")

            # Refresh Button
            refresh_button = tk.Button(shop_tab, text="Refresh Inventory", command=refresh_inventory)
            refresh_button.pack(pady=10, side=tk.BOTTOM, anchor="se")  # Anchors to the bottom-right

            # Add items to the Listbox initially
            refresh_inventory()

            def purchase_item():
                selected_item = inventory_listbox.get(tk.ACTIVE)
                if selected_item:
                    item_name = selected_item.split(" - ")[0]
                    item = self.inventory.get_item(item_name)
                    quantity = quantity_entry.get()

                    if item and quantity.isdigit() and int(quantity) > 0:
                        quantity = int(quantity)
                        confirm = messagebox.askyesno("Confirm Purchase",
                                                      f"Do you want to purchase {quantity} of {item_name}?")
                        if confirm:
                            # Ensure enough stock is available
                            if item.quantity >= quantity:
                                item.quantity -= quantity  # Decrease stock
                                self.cart.add_item(item.name, quantity, item.price)  # Pass name, quantity, and price
                                messagebox.showinfo("Success", f"{quantity} of '{item_name}' added to cart!")
                                update_cart_list()

                                # Save updated inventory to file
                                self.inventory.save_inventory()  # Save updated inventory to inventory.txt
                            else:
                                messagebox.showerror("Error", "Not enough stock available!")
                        else:
                            refresh_inventory()
                    else:
                        messagebox.showerror("Error", "Invalid quantity!")
                else:
                    messagebox.showerror("Error", "No item selected!")
                refresh_inventory()
            purchase_button = tk.Button(shop_tab, text="Purchase Selected Item", command=purchase_item)
            purchase_button.pack(pady=10)

            # Cart Tab (List of Purchased Items)
            cart_listbox = tk.Listbox(cart_tab, height=15, width=50)
            cart_listbox.pack(pady=20)

            # Label to Display Total Price
            total_price_label = tk.Label(cart_tab, text="Total Price: 0 PHP", font=("Arial", 12))
            total_price_label.pack(pady=5)

            def update_total_price():
                # Calculate the total price of items in the cart
                total_price = sum(item["price"] * item["quantity"] for item in self.cart.items)
                total_price_label.config(text=f"Total Price: {total_price} PHP")

            def update_cart_list():
                cart_listbox.delete(0, tk.END)  # Clear the listbox
                for item in self.cart.get_items():
                    cart_listbox.insert(
                        tk.END,
                        f"{item['name']} - {item['price']} PHP x {item['quantity']}"
                    )
                update_total_price()  # Update the total price

            def update_cart_list():
                cart_listbox.delete(0, tk.END)  # Clear the listbox
                update_total_price()
                for item in self.cart.get_items():
                    cart_listbox.insert(
                        tk.END,
                        f"{item['name']} - {item['price']} PHP x {item['quantity']}"
                    )

            def refresh_cart():
                # Simply call update_cart_list to refresh the list of items
                update_cart_list()
                update_total_price()

            def update_inventory_list():
                inventory_listbox.delete(0, tk.END)  # Clear the current inventory list
                update_total_price()
                for item in self.inventory.items:  # Loop through the items in the inventory
                    inventory_listbox.insert(tk.END, f"{item.name} - {item.price} PHP, Stock: {item.quantity}")

            def remove_item():
                selected_item = cart_listbox.get(tk.ACTIVE)  # Get the selected item from the cart listbox
                if selected_item:
                    item_name = selected_item.split(" - ")[0]  # Extract the name of the item
                    if item_name:
                        confirm = messagebox.askyesno("Confirm Removal",
                                                      f"Do you want to remove {item_name} from the cart?")
                        if confirm:
                            # Find the item in the cart
                            item = next((item for item in self.cart.items if item["name"] == item_name), None)
                            if item:
                                # Return the quantity to inventory
                                try:
                                    self.inventory.add_quantity(item["name"], item["quantity"])  # Use self.inventory
                                except ValueError as e:
                                    messagebox.showerror("Error", str(e))
                                    return

                                # Remove the item from the cart
                                self.cart.delete_item(item_name)

                                messagebox.showinfo("Success",
                                                    f"Item '{item_name}' removed from cart and returned to inventory!")
                                update_cart_list()  # Refresh the cart list
                                update_inventory_list()  # Refresh the inventory list
                            else:
                                messagebox.showerror("Error", "Item not found in cart!")
                    else:
                        messagebox.showerror("Error", "Item name could not be extracted!")
                else:
                    messagebox.showerror("Error", "No item selected!")

            # Create the Remove button
            remove_button = tk.Button(cart_tab, text="Remove Selected Item", command=remove_item)
            remove_button.pack(pady=10)

            # Create the Refresh button
            refresh_button = tk.Button(cart_tab, text="Refresh Cart", command=refresh_cart)
            refresh_button.pack(pady=10)

            # Checkout Tab (with paid amount field)
            checkout_label = tk.Label(cart_tab, text="Enter amount paid:")
            checkout_label.pack(pady=5)

            paid_amount_entry = tk.Entry(cart_tab)  # Create an entry field for user to input their money
            paid_amount_entry.pack(pady=5)

            def checkout():
                try:
                    # Retrieve the total cost from the cart (calculated as per cart items)
                    total_cost = sum(item["price"] * item["quantity"] for item in self.cart.items)

                    # Get the amount the user is paying
                    paid_amount_str = paid_amount_entry.get()  # Get the string from the entry
                    if not paid_amount_str:
                        messagebox.showerror("Error", "Please enter the paid amount.")
                        return

                    paid_amount = float(paid_amount_str)  # Convert to float

                    # Check if the paid amount is sufficient
                    if paid_amount < total_cost:
                        messagebox.showerror("Error", "Paid amount is less than the total cost!")
                        return

                    # Calculate the change
                    change = paid_amount - total_cost

                    # Print receipt to file
                    with open("receipt.txt", "w") as file:  # Open receipt.txt in write mode, replace if exists
                        file.write(f"=====================================================\n")
                        file.write(f"{'Name':<20}{'Quantity':<15}{'Price':<15}{'Subtotal':<15}\n")
                        for item in self.cart.items:
                            subtotal = item["price"] * item["quantity"]
                            file.write(
                                f"{item['name']:<20}{item['quantity']:<15}{item['price']:<15.2f}{subtotal:<15.2f}\n")
                        file.write(f"=====================================================\n")
                        file.write(f"{'Total Cost':<50}{total_cost:<15.2f}\n")
                        file.write(f"{'Paid Amount':<50}{paid_amount:<15.2f}\n")
                        file.write(f"{'Change':<50}{change:<15.2f}\n")
                        file.write(f"=====================================================\n")

                    # Show a message to the user
                    messagebox.showinfo("Receipt", f"Receipt has been saved to receipt.txt.\nChange: {change:.2f}")

                    # Clear the cart after successful checkout
                    self.cart.items.clear()
                    update_cart_list()  # Refresh the cart list

                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a valid paid amount.")


                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid amount for payment.")

            # Checkout Button
            checkout_button = tk.Button(cart_tab, text="Proceed to Checkout", command=checkout)
            checkout_button.pack(pady=20)

            # Update Cart Tab initially
            update_cart_list()


# Run the Application
if __name__ == "__main__":
    try:
        app = Application()
        app.mainloop()
    except KeyboardInterrupt:
        print("Application interrupted and closed.")
