import json
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict):
        """Load a Cart instance from a dictionary."""
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[get_product(item_id) for item_id in data['contents']],
            cost=data['cost'],
        )

def get_cart(username: str) -> list[Product]:
    """Retrieve the user's cart contents as a list of Product objects."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Safer than eval
            items.extend(contents)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing cart contents: {e}")

    return [get_product(item_id) for item_id in items]

def add_to_cart(username: str, product_id: int):
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    """Delete the user's cart."""
    dao.delete_cart(username)
