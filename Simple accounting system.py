import ast
import os
from typing import List

DATA_FILE = os.path.join(os.path.dirname(__file__), "accounting_data.txt")

DEFAULT_DATA = {
    "balance": 0.0,
    "inventory": {},
    "history": [],
}


def load_data(file_name: str) -> dict:
    """Load data from file. If file is missing or broken, return default data."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return copy_default_data()

            data = ast.literal_eval(content)

            if not isinstance(data, dict):
                raise ValueError("File content is not a dictionary.")

            balance = data.get("balance", 0.0)
            inventory = data.get("inventory", {})
            history = data.get("history", [])

            if not isinstance(inventory, dict):
                raise ValueError("Inventory must be a dictionary.")
            if not isinstance(history, list):
                raise ValueError("History must be a list.")

            return {
                "balance": float(balance),
                "inventory": inventory,
                "history": history,
            }

    except FileNotFoundError:
        print(f"File '{file_name}' not found. Starting with empty data.")
        return copy_default_data()
    except (SyntaxError, ValueError, TypeError, OSError) as error:
        print(f"Error reading file '{file_name}': {error}")
        print("Starting with empty data.")
        return copy_default_data()


def copy_default_data() -> dict:
    return {
        "balance": DEFAULT_DATA["balance"],
        "inventory": dict(DEFAULT_DATA["inventory"]),
        "history": list(DEFAULT_DATA["history"]),
    }


def save_data(file_name: str, data: dict) -> None:
    """Save data to file."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(str(data))
        print(f"Data saved to {file_name}")
    except OSError as error:
        print(f"Error saving data: {error}")


def show_menu() -> None:
    print("\n===== Accounting and Warehouse =====")
    print("1. Show balance")
    print("2. Add income")
    print("3. Add expense")
    print("4. Add product")
    print("5. Update product quantity")
    print("6. Show inventory")
    print("7. Show history")
    print("8. Exit")


def add_to_history(history: List[str], text: str) -> None:
    history.append(text)


def main() -> None:
    data = load_data(DATA_FILE)
    balance = data["balance"]
    inventory = data["inventory"]
    history = data["history"]

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"Current balance: {balance}")

        elif choice == "2":
            try:
                amount = float(input("Enter income amount: "))
                if amount < 0:
                    print("Amount cannot be negative.")
                    continue
                description = input("Enter description: ")
                balance += amount
                add_to_history(history, f"Income: +{amount} ({description})")
                print("Income added.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            try:
                amount = float(input("Enter expense amount: "))
                if amount < 0:
                    print("Amount cannot be negative.")
                    continue
                description = input("Enter description: ")
                balance -= amount
                add_to_history(history, f"Expense: -{amount} ({description})")
                print("Expense added.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            product = input("Enter product name: ").strip()
            if not product:
                print("Product name cannot be empty.")
                continue
            try:
                quantity = int(input("Enter quantity: "))
                if quantity < 0:
                    print("Quantity cannot be negative.")
                    continue
                inventory[product] = inventory.get(product, 0) + quantity
                add_to_history(history, f"Added to inventory: {product} x{quantity}")
                print("Product added.")
            except ValueError:
                print("Please enter a valid whole number.")

        elif choice == "5":
            product = input("Enter product name: ").strip()
            if not product:
                print("Product name cannot be empty.")
                continue
            if product not in inventory:
                print("This product is not in the inventory.")
                continue
            try:
                quantity = int(input("Enter new quantity: "))
                if quantity < 0:
                    print("Quantity cannot be negative.")
                    continue
                inventory[product] = quantity
                add_to_history(history, f"Updated inventory: {product} -> {quantity}")
                print("Quantity updated.")
            except ValueError:
                print("Please enter a valid whole number.")

        elif choice == "6":
            if not inventory:
                print("Inventory is empty.")
            else:
                print("Inventory:")
                for name, qty in inventory.items():
                    print(f"- {name}: {qty}")

        elif choice == "7":
            if not history:
                print("History is empty.")
            else:
                print("History:")
                for item in history:
                    print(f"- {item}")

        elif choice == "8":
            data = {
                "balance": balance,
                "inventory": inventory,
                "history": history,
            }
            save_data(DATA_FILE, data)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
