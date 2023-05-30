import psycopg2

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

class Checkout:
    def __init__(self, cart_items, total_price, first_name, last_name, address):
        self.cart_items = cart_items
        self.total_price = total_price
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def create_tables(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkouts (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR,
                last_name VARCHAR,
                address VARCHAR,
                total_price NUMERIC
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                id SERIAL PRIMARY KEY,
                checkout_id INTEGER REFERENCES checkouts(id),
                product_name VARCHAR,
                price NUMERIC,
                quantity INTEGER
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()

    def save_checkout(self, checkout):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO checkouts (first_name, last_name, address, total_price) VALUES (%s, %s, %s, %s) RETURNING id",
            (checkout.first_name, checkout.last_name, checkout.address, checkout.total_price)
        )
        checkout_id = cursor.fetchone()[0]

        for cart_item in checkout.cart_items:
            cursor.execute(
                "INSERT INTO cart_items (checkout_id, product_name, price, quantity) VALUES (%s, %s, %s, %s)",
                (checkout_id, cart_item.product.name, cart_item.product.price, cart_item.quantity)
            )

        connection.commit()
        cursor.close()
        connection.close()

