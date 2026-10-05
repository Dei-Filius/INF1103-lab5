import json
from pathlib import Path

INVENTORY_FILE_PATH: str = "data/inventory.json"
inventory_file = Path(INVENTORY_FILE_PATH)


def load_inventory() -> dict:
    print()
    print("Loading inventory...")
    if inventory_file.exists():
        print(f"{INVENTORY_FILE_PATH} found.")
        with inventory_file.open("r") as file:
            inventory = json.load(file)
        print("Inventory loaded successfully.")
    else:
        inventory_file.parent.mkdir(parents=True, exist_ok=True)
        inventory_file.touch()
        inventory = dict()
    return inventory


def save_inventory(inventory: dict) -> dict:
    print()
    print("Saving inventory...")
    with inventory_file.open("w") as file:
        json.dump(inventory, file)
    print("Inventory saved successfully to", INVENTORY_FILE_PATH)
    return inventory


def add_product(inventory: dict) -> dict:
    print()
    print("Add New Product")
    product_id = get_product_id_input()
    if product_id in inventory:
        print("Product already exists.")
    else:
        name = input("Product Name: ").strip()
        price = get_price_input("Price (omit $ sign): ")
        stock = get_int_input("Stock Quantity: ")
        inventory[product_id] = {
            "name": name,
            "price": price,
            "stock": stock,
        }
        print("Product added successfully!")
    return inventory


def update_stock(inventory: dict) -> dict:
    print()
    print("Update Stock")
    product_id = get_product_id_input()
    product = inventory.get(product_id)
    if product is None:
        print("Not found.")
    else:
        print(f"""
Product Found:
Name: {product["name"]}
Current Stock: {product["stock"]}
""")
        stock = get_int_input("New Stock Quantity: ")
        product["stock"] = stock
    return inventory


def search_product(inventory: dict) -> dict:
    print()
    product_id = get_product_id_input()
    product = inventory.get(product_id)
    if product is None:
        print("Not found.")
    else:
        print(f"""
Product Found
------------------------------------------------
ID: {product_id}
Name: {product["name"]}
Price: ${product["price"]:.2f}
Stock: {product["stock"]}
------------------------------------------------
""")
    return inventory


def display_all(inventory: dict) -> dict:
    print()
    print("Current Inventory")
    print("------------------------------------------------")
    if len(inventory) > 0:
        for product_id, product in inventory.items():
            print(
                f"ID: {product_id} | Name: {product["name"]} | Price: ${product["price"]:.2f} | Stock: {product["stock"]}"
            )
    else:
        print("Nothing...")
    print("------------------------------------------------")
    return inventory


def exit_app(inventory: dict):
    save_inventory(inventory)
    print()
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")
    exit()


def get_int_input(msg: str) -> int:
    """
    valid range >=0
    """
    while True:
        try:
            user_input = int(input(msg))
            if user_input < 0:
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid. Try again.")


def get_price_input(msg: str) -> float:
    """
    valid range >=0
    """
    while True:
        try:
            user_input = round(float(input(msg)), 2)
            if user_input < 0:
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid. Try again.")


def get_product_id_input() -> str:
    while True:
        try:
            user_input = input("Product ID: ").strip().upper()
            if not (user_input.startswith("P") or user_input[1:].isdigit()):
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid Product ID. Try again.")


def display_menu(menu: list[dict]) -> None:
    print()
    print("----------- MENU -----------")
    for i, page in enumerate(menu, 1):
        print(f"{i}. {page["text"]}")
    print("----------------------------")


def main() -> None:
    try:
        inventory = load_inventory()

        menu: list[dict] = [
            {"text": "Display All Products", "action": display_all},
            {"text": "Add Product", "action": add_product},
            {"text": "Update Stock", "action": update_stock},
            {"text": "Search Product", "action": search_product},
            {"text": "Save Inventory", "action": save_inventory},
            {"text": "Exit", "action": exit_app},
        ]

        print("""
========================================
INVENTORY MANAGEMENT SYSTEM
========================================
        """)
        display_menu(menu)

        while True:
            try:
                print()
                option = get_int_input("Enter option (0 to display menu): ")
                try:
                    if option == 0:
                        display_menu(menu)
                    else:
                        menu[option - 1]["action"](inventory)
                except KeyboardInterrupt:
                    continue
            except KeyboardInterrupt:
                exit_app(inventory)
                break

    except json.decoder.JSONDecodeError:
        print(f"Error decoding json file {INVENTORY_FILE_PATH}")
        print("Exiting...")
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
