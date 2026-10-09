
from data.inventory import inventory
from services.openfoodfacts import (
    search_product_by_name,
    get_product_by_barcode,
)


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 45)
    print("       INVENTORY MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. View all inventory")
    print("2. View a product by ID")
    print("3. Add a new product")
    print("4. Update a product")
    print("5. Delete a product")
    print("6. Search Open Food Facts by name")
    print("7. Search Open Food Facts by barcode")
    print("8. Exit")
    print("=" * 45)


def get_next_id():
    """Generate the next available inventory ID."""
    if not inventory:
        return 1

    return max(item["id"] for item in inventory) + 1


def display_product(product):
    """Display the details of one product."""
    print("\n" + "-" * 40)
    print(f"ID: {product.get('id', 'Not assigned')}")
    print(f"Product name: {product.get('product_name', 'N/A')}")
    print(f"Brand: {product.get('brands', 'N/A')}")
    print(f"Barcode: {product.get('barcode', 'N/A')}")
    print(f"Price: KSh {product.get('price', 'N/A')}")
    print(f"Quantity: {product.get('quantity', 'N/A')}")
    print(f"Categories: {product.get('categories', 'N/A')}")
    print(f"Ingredients: {product.get('ingredients_text', 'N/A')}")
    print(f"Image URL: {product.get('image_url', 'N/A')}")
    print(f"Nutri-Score: {product.get('nutriscore_grade', 'N/A')}")
    print("-" * 40)


def view_inventory():
    """Display all products in the inventory."""
    if not inventory:
        print("\nYour inventory is empty.")
        return

    print(f"\nTotal products: {len(inventory)}")

    for product in inventory:
        display_product(product)


def find_product_by_id(item_id):
    """Find a product using its ID."""
    for product in inventory:
        if product["id"] == item_id:
            return product

    return None


def get_non_negative_number(prompt, number_type):
    """Get a valid non-negative number from the user."""
    while True:
        try:
            value = number_type(input(prompt).strip())

            if value < 0:
                print("Value cannot be negative. Try again.")
                continue

            return value

        except ValueError:
            print("Invalid number. Please try again.")


def add_product():
    """Add a new product to the inventory."""
    print("\n--- Add a New Product ---")

    product_name = input("Product name: ").strip()

    if not product_name:
        print("Product name cannot be empty.")
        return

    price = get_non_negative_number("Price (KSh): ", float)
    quantity = get_non_negative_number("Quantity: ", int)

    barcode = input("Barcode (optional): ").strip()
    brands = input("Brand (optional): ").strip()
    categories = input("Categories (optional): ").strip()
    ingredients_text = input("Ingredients (optional): ").strip()
    image_url = input("Image URL (optional): ").strip()
    nutriscore_grade = input("Nutri-Score (optional): ").strip()

    product = {
        "id": get_next_id(),
        "barcode": barcode,
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "categories": categories,
        "image_url": image_url,
        "nutriscore_grade": nutriscore_grade,
        "quantity": quantity,
        "price": price,
    }

    inventory.append(product)

    print(f"\n{product_name} added successfully.")
    print(f"Assigned product ID: {product['id']}")


def update_product():
    """Update an existing product."""
    print("\n--- Update a Product ---")

    item_id = get_non_negative_number("Enter product ID: ", int)
    product = find_product_by_id(item_id)

    if product is None:
        print("Product not found.")
        return

    display_product(product)
    print("Press Enter to keep an existing value.")

    new_name = input(
        f"Product name [{product['product_name']}]: "
    ).strip()

    if new_name:
        product["product_name"] = new_name

    new_brand = input(
        f"Brand [{product['brands']}]: "
    ).strip()

    if new_brand:
        product["brands"] = new_brand

    new_price = input(
        f"Price [{product['price']}]: "
    ).strip()

    if new_price:
        try:
            price = float(new_price)

            if price < 0:
                print("Price cannot be negative.")
                return

            product["price"] = price

        except ValueError:
            print("Invalid price.")
            return

    new_quantity = input(
        f"Quantity [{product['quantity']}]: "
    ).strip()

    if new_quantity:
        try:
            quantity = int(new_quantity)

            if quantity < 0:
                print("Quantity cannot be negative.")
                return

            product["quantity"] = quantity

        except ValueError:
            print("Invalid quantity.")
            return

    print("Product updated successfully.")


def delete_product():
    """Delete a product from the inventory."""
    print("\n--- Delete a Product ---")

    item_id = get_non_negative_number("Enter product ID: ", int)
    product = find_product_by_id(item_id)

    if product is None:
        print("Product not found.")
        return

    display_product(product)

    confirmation = input(
        "Are you sure you want to delete this product? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        inventory.remove(product)
        print("Product deleted successfully.")
    else:
        print("Deletion cancelled.")


def search_openfoodfacts_by_name():
    """Search Open Food Facts using a product name."""
    name = input("\nEnter product name to search: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        product = search_product_by_name(name)

        if product is None:
            print("No matching product found.")
            return

        display_product(product)

        choice = input(
            "Add this product to your inventory? (yes/no): "
        ).strip().lower()

        if choice == "yes":
            product["id"] = get_next_id()
            product["price"] = get_non_negative_number(
                "Enter selling price (KSh): ",
                float,
            )
            product["quantity"] = get_non_negative_number(
                "Enter quantity: ",
                int,
            )

            inventory.append(product)
            print("Product added to inventory successfully.")

    except RuntimeError as error:
        print(f"Search error: {error}")


def search_openfoodfacts_by_barcode():
    """Look up a product using its barcode."""
    barcode = input("\nEnter product barcode: ").strip()

    if not barcode:
        print("Barcode cannot be empty.")
        return

    try:
        product = get_product_by_barcode(barcode)

        if product is None:
            print("No product found for that barcode.")
            return

        display_product(product)

        choice = input(
            "Add this product to your inventory? (yes/no): "
        ).strip().lower()

        if choice == "yes":
            product["id"] = get_next_id()
            product["price"] = get_non_negative_number(
                "Enter selling price (KSh): ",
                float,
            )
            product["quantity"] = get_non_negative_number(
                "Enter quantity: ",
                int,
            )

            inventory.append(product)
            print("Product added to inventory successfully.")

    except RuntimeError as error:
        print(f"Lookup error: {error}")


def main():
    """Run the command-line application."""
    while True:
        display_menu()

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            view_inventory()

        elif choice == "2":
            item_id = get_non_negative_number(
                "Enter product ID: ",
                int,
            )
            product = find_product_by_id(item_id)

            if product:
                display_product(product)
            else:
                print("Product not found.")

        elif choice == "3":
            add_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            search_openfoodfacts_by_name()

        elif choice == "7":
            search_openfoodfacts_by_barcode()

        elif choice == "8":
            print("Thank you for using the Inventory Management System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
