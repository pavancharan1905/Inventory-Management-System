

import json
import os

# File paths
INVENTORY_FILE = 'inventory.json'
USERS_FILE = 'users.json'
GST_RATE = 0.18

# Load JSON data
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

# Save JSON data
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Initialize user
def initialize_user(username):
    users = load_json(USERS_FILE)
    if username not in users:
        users[username] = {'balance': 100000, 'cart': {}, 'transactions': []}
        save_json(USERS_FILE, users)

# View products
def view_products():
    inventory = load_json(INVENTORY_FILE)
    print("\nAvailable Products:")
    for product, details in inventory.items():
        print(f"{product}: ₹{details['price']} | Quantity: {details['quantity']} | Discount: {details['discount']}%")

# Add to cart
def add_to_cart(username):
    inventory = load_json(INVENTORY_FILE)
    users = load_json(USERS_FILE)

    product = input("Enter product name to add: ")
    if product in inventory:
        quantity = int(input("Enter quantity: "))
        if quantity <= inventory[product]['quantity']:
            users[username]['cart'][product] = {
                'quantity': quantity,
                'price': inventory[product]['price']
            }
            save_json(USERS_FILE, users)
            print("Product added to cart!")
        else:
            print("Insufficient stock!")
    else:
        print("Product not found!")

# View cart
def view_cart(username):
    users = load_json(USERS_FILE)
    cart = users[username]['cart']
    print("\nYour Cart:")
    for product, details in cart.items():
        print(f"{product}: Quantity: {details['quantity']} | Price: ₹{details['price']}")

# Clear cart
def clear_cart(username):
    users = load_json(USERS_FILE)
    users[username]['cart'] = {}
    save_json(USERS_FILE, users)
    print("Cart cleared!")

# Checkout
def checkout(username):
    inventory = load_json(INVENTORY_FILE)
    users = load_json(USERS_FILE)
    cart = users[username]['cart']

    if not cart:
        print("Cart is empty!")
        return

    total = sum(details['quantity'] * details['price'] for details in cart.values())
    gst = total * GST_RATE
    total_with_gst = total + gst

    if users[username]['balance'] >= total_with_gst:
        users[username]['balance'] -= total_with_gst
        users[username]['transactions'].append({
            'cart': cart,
            'total': total_with_gst
        })
        # Update inventory
        for product, details in cart.items():
            inventory[product]['quantity'] -= details['quantity']

        users[username]['cart'] = {}
        save_json(INVENTORY_FILE, inventory)
        save_json(USERS_FILE, users)
        print(f"Checkout successful! Total paid: ₹{total_with_gst}")
    else:
        print("Insufficient balance!")

# Main menu
def main():
    username = input("Enter your username: ")
    initialize_user(username)

    while True:
        print("\nMain Menu:")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Clear Cart")
        print("5. Checkout")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            view_products()
        elif choice == '2':
            add_to_cart(username)
        elif choice == '3':
            view_cart(username)
        elif choice == '4':
            clear_cart(username)
        elif choice == '5':
            checkout(username)
        elif choice == '6':
            print("Thank you for shopping with us!")
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    main()
    
