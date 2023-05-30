from model import Product, CartItem, Checkout, Database

class Controller:
    def __init__(self):
        self.products = [
            Product('лук', 10),
            Product('томаты', 20),
            Product('яблоки', 30)
        ]
        self.cart_items = []
        self.current_checkout = None  # Обновленное имя атрибута
        self.database = Database("IoT", "postgres", "31tiraspol", "localhost", 5432)

    def add_to_cart(self, product_name, quantity):
        product = next((p for p in self.products if p.name == product_name), None)
        if product:
            cart_item = CartItem(product, quantity)
            self.cart_items.append(cart_item)

    def remove_from_cart(self, product_name):
        self.cart_items = [item for item in self.cart_items if item.product.name != product_name]

    def calculate_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.cart_items)
        return total

    def checkout(self, first_name, last_name, address):  # Обновленное имя метода
        total_price = self.calculate_total_price()
        self.current_checkout = Checkout(self.cart_items, total_price, first_name, last_name, address)  # Обновленное имя атрибута
        self.database.save_checkout(self.current_checkout)
        self.cart_items = []


#self.database = Database("IoT", "postgres", "31tiraspol", "localhost", 5432)

