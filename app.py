from flask import Flask, render_template, request, redirect, url_for
from controller import Controller

app = Flask(__name__)
controller = Controller()
controller.database.create_tables()  # Создание таблиц

@app.route('/')
def index():
    return render_template('index.html', products=controller.products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    controller.add_to_cart(product_name, quantity)
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<product_name>')
def remove_from_cart(product_name):
    controller.remove_from_cart(product_name)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    total_price = controller.calculate_total_price()
    return render_template('cart.html', cart_items=controller.cart_items, total_price=total_price)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        controller.checkout(first_name, last_name, address)
        return redirect(url_for('receipt'))
    else:
        return render_template('checkout.html')

@app.route('/receipt')
def receipt():
    checkout = controller.current_checkout
    return render_template('receipt.html', checkout=checkout)

if __name__ == '__main__':
    app.run()
