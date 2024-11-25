import re
from datetime import datetime
import ssl
import smtplib
from email.message import EmailMessage
from .config import Config
from . import scraper

# User Management Functions
def create_user(email, password=None, name=None, mongo=None):
    """
    Creates and store user information in the database.
    """
    user_collection = mongo.db.users
    if user_collection.find_one({"email": email}):
        return False  

    user = {
        "email": email,
        "name": name,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "wishlists": {}  
    }
    user_collection.insert_one(user)
    return True

def check_user(email, password=None, mongo=None):
    """
    Checks if the user exists in the 'users' collection.
    """
    user = mongo.db.users.find_one({"email": email})
    return bool(user)

# Wishlist Functions
def wishlist_add_item(email, wishlist_name, item_data, mongo=None):
    """
    Adds an item to a user's wishlist. Changes reflect in DB.
    """
    mongo.db.users.update_one(
        {"email": email, f"wishlists.{wishlist_name}": {"$exists": False}},
        {"$set": {f"wishlists.{wishlist_name}": []}}
    )

    existing_item = mongo.db.users.find_one({
        "email": email,
        f"wishlists.{wishlist_name}": {
            "$elemMatch": {
                "link": item_data["link"]
            }
        }
    })

    if not existing_item:
        mongo.db.users.update_one(
            {"email": email},
            {"$push": {f"wishlists.{wishlist_name}": item_data}}
        )
        return True
    return False

def read_wishlist(email, wishlist_name, mongo=None):
    """
    Reads a user's wishlist from database.
    """
    try:
        user = mongo.db.users.find_one(
            {"email": email},
            {f"wishlists.{wishlist_name}": 1}
        )
        if user and "wishlists" in user:
            return user["wishlists"].get(wishlist_name, [])
    except Exception as e:
        print(f"Error reading wishlist: {e}")
    return []

def wishlist_remove_list(email, wishlist_name, index, mongo=None):
    """
    Removes an item from a user's wishlist in MongoDB by index.
    """
    try:
        user = mongo.db.users.find_one({"email": email})
        if not user or "wishlists" not in user:
            return False
            
        wishlist = user["wishlists"].get(wishlist_name, [])
        if not wishlist or index >= len(wishlist):
            return False
        wishlist.pop(index)
        
        mongo.db.users.update_one(
            {"email": email},
            {"$set": {f"wishlists.{wishlist_name}": wishlist}}
        )
        return True
    except Exception as e:
        print(f"Error removing item from wishlist: {e}")
        return False

def share_wishlist(email_sender, wishlist_name, email_receiver, mongo=None):
    """
    Sends a user's wishlist via email after fetching from database.
    """
    user = mongo.db.users.find_one({"email": email_sender}, {"wishlists": 1})
    if user and wishlist_name in user.get("wishlists", {}):
        wishlist = user["wishlists"][wishlist_name]
        links_list = "\n".join([item.get("link", "N/A") for item in wishlist])
        
        try:
            email_password = Config.EMAIL_PASS
            subject = f'Slash wishlist of {email_sender}'
            body = "\n".join([
                f"{i}. {link}" for i, link in enumerate(links_list.split(), start=1)
            ])

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

        except Exception as e:
            print("Error occured while sending mail, ", e)
            return 'Failed to send email'

# Comment Functions
def load_comments(product_name=None, mongo=None):
    """
    Loads comments from the comments collection in DB.
    """
    comments_cursor = mongo.db.comments.find()
    comments = {}
    for comment in comments_cursor:
        product_name = comment["product_name"]
        comments.setdefault(product_name, []).append({
            "username": comment["username"],
            "comment": comment["comment"]
        })
    return comments

def find_currency(price):
    """
    Helper function to detect currency from a price string.
    """
    currency = re.match(r'^[a-zA-Z]{3,5}', price)
    return currency.group() if currency else None

def update_price(link, website, price):
    """
    Updates the price of an item by scraping the respective website.
    """
    currency = find_currency(price)
    updated_price = price

    # Update price using scraper based on website
    scraped_price = None
    if website == "amazon":
        scraped_price = scraper.amazon_scraper(link).strip()
    elif website == "google":
        scraped_price = scraper.google_scraper(link).strip()
    elif website == "walmart":
        scraped_price = scraper.walmart_scraper(link).strip()
    elif website == "ebay":
        scraped_price = scraper.ebay_scraper(link).strip()
    elif website == "bestbuy":
        scraped_price = scraper.bestbuy_scraper(link).strip()
    elif website == "target":
        scraped_price = scraper.target_scraper(link).strip()

    if scraped_price:
        updated_price = (
            scraper.getCurrency(currency, scraped_price) if currency else scraped_price
        )

    return updated_price
