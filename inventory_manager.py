import json
from pathlib import Path


INVENTORY_JSON_PATH = "inventory.json"


def load_inventory(path: str) -> dict:
    inventory_file = Path(path)
    if inventory_file.exists():
        with inventory_file.open("r") as file:
            inventory = json.load(file)
    else:
        inventory = dict()
    return inventory


def save_inventory(inventory: dict, path: str) -> None:
    inventory_file = Path(path)
    with inventory_file.open() as file:
        json.dump(inventory, file)

def add_product(): ...


def update_stock(): ...


def search_product(): ...


def display_all(): ...
