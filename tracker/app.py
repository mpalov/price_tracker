"""
app.py

This module defines a Flask web application for monitoring product prices and sending email notifications.

Endpoints:
- '/' : Renders the index.html template.
- '/api/products' : GET endpoint to retrieve product data based on a search term.
- '/api/monitor' : POST endpoint to monitor product prices for a given search term and send email notifications on price drops.

Dependencies:
- Flask: Web framework for handling HTTP requests.
- scraper.extract_data: Function to scrape product data from a website.
- scraper.check_price_drop: Function to check if there's been a price drop.
- scraper.send_email: Function to send email notifications.

Usage:
1. Ensure Flask and other dependencies are installed.
2. Run the Flask app using 'python app.py'.
3. Access endpoints via http://localhost:5000/.

Example:
$ python app.py
 * Running on http://localhost:5000/ (Press CTRL+C to quit)

"""

from flask import Flask, jsonify, request, render_template
from scraper import extract_data, check_price_drop, send_email

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the index.html template.
    """
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Retrieve product data based on a search term.

    Returns:
    - JSON response containing product data.

    Query Parameters:
    - search (optional): Search term to filter products.

    Example:
    GET /api/products?search=laptop
    """
    search_term = request.args.get('search', 'cpu')
    products = extract_data(search_term)
    return jsonify([product.__dict__ for product in products])


@app.route('/api/monitor', methods=['POST'])
def monitor_product():
    """
    Monitor product prices for a given search term and send email notifications on price drops.

    Returns:
    - JSON response confirming monitoring has started.

    Request Body (JSON):
    - search: Search term to monitor (default: 'cpu').
    - threshold: Threshold price for price drop notification (default: 500.0).

    Example:
    POST /api/monitor
    {
        "search": "graphics card",
        "threshold": 600.0
    }
    """
    search_term = request.json.get('search', 'cpu')
    threshold_price = request.json.get('threshold', 500.0)
    sender_email = 'your-email@example.com'  # Update with your email address
    sender_password = 'your-email-password'  # Update with your email password
    recipient_email = 'recipient@example.com'  # Update with recipient email address

    products = extract_data(search_term)
    for product in products:
        if check_price_drop(previous_price=float(product.price), current_price=float(product.price),
                            threshold=threshold_price):
            subject = f'Price Drop Notification for {product.name}'
            body = f'Price dropped for {product.name}! New price: {product.price}. Check it out: {product.link}'
            send_email(sender_email, sender_password, recipient_email, subject, body)

    return jsonify({'message': 'Monitoring started'})


if __name__ == '__main__':
    app.run(debug=True)
