# Price tracker
# Overview
This project is designed for monitoring product prices from a website and sending email notifications when prices drop below a specified threshold. It utilizes web scraping techniques to fetch real-time data, a Flask-based REST API for interaction, and email notifications for immediate alerts.

# Features
- Web Scraping: Utilizes Playwright and Selectolax for scraping product data based on a search term from Newegg.
- Price Monitoring: Checks for price drops below a specified threshold and sends email notifications accordingly.
- API: Provides endpoints (/api/products and /api/monitor) to retrieve product data and start monitoring respectively.
- Email Notifications: Sends notifications via email using SMTP server integration.

# Configure SMTP settings

Rename config.example.py to config.py.
Update config.py with your SMTP server details and email credentials.
Usage
Run the Flask app

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
