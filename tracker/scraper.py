"""
scraper.py

This module contains functions for scraping product data from a website,
checking price drops, and sending email notifications.

Functions:
- extract_data: Scrapes product information based on a search term.
- check_price_drop: Checks if there has been a price drop below a specified threshold.
- send_email: Sends an email notification.

Dependencies:
- playwright.sync_api: Playwright library for web scraping.
- selectolax.parser: HTML parsing library.
- smtplib: Library for sending emails.
- email.mime: MIME libraries for email content formatting.

Usage:
- Import and use functions as needed for web scraping, price monitoring, and email notifications.

Example:
from scraper import extract_data, check_price_drop, send_email

"""

from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@dataclass
class Item:
    """
    Dataclass representing a product item.

    Attributes:
    - name: Name of the product.
    - price: Price of the product.
    - rating: Rating of the product.
    - link: Link to the product page.
    - image: URL of the product image.
    """
    name: str
    price: str
    rating: str
    link: str
    image: str


def clean_text(text: str) -> str:
    """
    Clean up text by removing extra whitespace.

    Args:
    - text: Input text to clean.

    Returns:
    - Cleaned text with reduced whitespace.
    """
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_price(price: str) -> str:
    """
    Clean up price string by removing non-numeric characters.

    Args:
    - price: Input price string.

    Returns:
    - Cleaned price string containing only numeric characters and decimal point.
    """
    price = re.sub(r'[^0-9.,]', '', price)
    return price.strip()


def clean_rating(rating: str) -> str:
    """
    Extract numeric rating from a string.

    Args:
    - rating: Input rating string.

    Returns:
    - Extracted numeric rating or 'No rating' if no valid rating found.
    """
    match = re.search(r'\d+(\.\d+)?', rating)
    return match.group(0) if match else 'No rating'


def extract_data(search_term: str):
    """
    Extract product data from a website based on a search term.

    Args:
    - search_term: Search term used to filter products.

    Returns:
    - List of Item objects containing product details.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0')
        page = context.new_page()
        page.goto(f'https://www.newegg.com/p/pl?d={search_term}')

        html = HTMLParser(page.content())
        product_elements = html.css('div.item-container')
        items = []

        for product in product_elements:
            name = clean_text(product.css_first('.item-title').text())
            price = clean_price(product.css_first('li.price-current').text())
            rating = clean_rating(product.css_first('.item-rating').text()) if product.css_first(
                '.item-rating') else 'No rating'
            product_link = product.css_first('div.item-info a.item-title').attributes['href']
            image_url = product.css_first('a.item-img img').attributes['src']
            items.append(Item(name=name, price=price, rating=rating, link=product_link, image=image_url))

        browser.close()
    return items


def check_price_drop(previous_price: float, current_price: float, threshold: float) -> bool:
    """
    Check if there has been a price drop below a specified threshold.

    Args:
    - previous_price: Previous price of the product.
    - current_price: Current price of the product.
    - threshold: Price threshold for considering a price drop.

    Returns:
    - True if current_price is less than both previous_price and threshold, False otherwise.
    """
    if current_price < previous_price and current_price <= threshold:
        return True
    return False


def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Send an email notification.

    Args:
    - sender_email: Sender's email address.
    - sender_password: Sender's email password.
    - recipient_email: Recipient's email address.
    - subject: Email subject line.
    - body: Email body content.

    Returns:
    - None
    """
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Update with your SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')


if __name__ == '__main__':
    # Example usage if executed as a standalone script
    pass
