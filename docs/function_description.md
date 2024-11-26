## **slash.py**
### *def main()*: 
Provides help for every argument

## **scaper.py**
### *def searchTarget(query, df_flag, currency)*:
The searchTarget function scrapes target.com using the API\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

### *def searchBestbuy(query, df_flag, currency)*:
The searchBestbuy function scrapes bestbuy.com using the scraping\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

### *def searchEbay(query, df_flag, currency)*:
The searchEbay function scrapes ebay.com using the API\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

### *def httpsGet(URL)*: 
The httpsGet function makes HTTP called to the requested URL with custom headers

### *def searchAmazon(query, df_flag, currency)*:  
The searchAmazon function scrapes amazon.com\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

Returns a list of items available on Amazon.com that match the product entered by the user.

### *def searchWalmart(query, df_flag, currency)*:
The searchWalmart function scrapes walmart.com\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

Returns a list of items available on walmart.com that match the product entered by the user.

### *def searchEtsy(query, df_flag, currency)*:
 The searchEtsy function scrapes Etsy.com\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

Returns a list of items available on Etsy.com that match the product entered by the user

### *def amazon_scraper(link)*: 
The amazon scraper function scrapes amazon.com.
**Parameters**:\
link- link of the product for which price has to be fetched

Returns Updated Price from the Link

Return
### *def google_scraper(link)*: 
The google scraper function scrapes google.com.
**Parameters**:\
link- link of the product for which price has to be fetched

Returns Updated Price from the Link

### *def walmart_scraper(link)*: 
The walmart scraper function scrapes walmart.com.
**Parameters**:\
link- link of the product for which price has to be fetched

Returns Updated Price from the Link

### *def ebay_scraper(link)*: 
The ebay scraper function scrapes ebay.com.
**Parameters**:\
link- link of the product for which price has to be fetched

Returns Updated Price from the Link

### *def bestbuy_scraper(link)*: 
The ebay scraper function scrapes bestbuy.com.
**Parameters**:\
link- link of the product for which price has to be fetched

Returns Updated Price from the Link

### *def target_scraper(link)*: 
The target scraper function scrapes target.com.
**Parameters**:\
link- link of the product for which price has to be fetched

Returns Updated Price from the Link

### *def driver(product, currency, num=None, df_flag=0,csv=False,cd=None)*:
Returns csv if the user enters the --csv arg, else will display the result table in the terminal based on the args entered by the user.

## **formatter.py**
### *def formatResult(website, titles, prices, links,ratings,df_flag, currency)*:
The formatResult function takes the scraped HTML as input, and extracts the necessary values from the HTML code. Ex. extracting a price '$19.99' from a paragraph tag.\
**Parameters**: \
titles- scraped titles of the products\
prices- scraped prices of the products\
links- scraped links of the products on the respective e-commerce sites\
ratings-scraped ratings of the product

Returns a dictionary of all the parameters stated above for the product.

### *def sortList(arr, sortBy, reverse)*:
It sorts the products list based on the flags provided as arguements. Currently, it supports sorting by price.\
**Parameters-**\
SortBy- "pr": sorts by price, SortBy- "ra": sorts by rating

Returns- Sorted list of the products based on the parameter requested by the user

### *def formatSearchQuery(query)*:
It formats the search string into a string that can be sent as a url paramenter.

### *def formatTitle(title)*:
It formats titles extracted from the scraped HTML code.

### *def getNumbers(st)*:
It extracts float values for the price from a string.\
Ex. it extracts 10.99 from '$10.99' or 'starting at $10.99'

### *def getCurrency(currency, price)*:
The getCurrency function converts the prices listed in USD to user specified currency. \
Currently it supports INR, EURO, AUD, YUAN, YEN, POUND.

## full_version.py 

### *def login(self)*:
Used for User Login with password\
Returns the username.

### *def scrape(self,prod)*:
calls the scraper function from scraper.py

## csv_writer.py
### *def write_csv(arr,product,file_path)*:
Returns the CSV file with the naming nomenclature as 'ProductDate_Time'\
**Parameters**-\
product: product entered by the user\
file_path: path where the csv needs to be stored\
**Returns**-\
file_name: CSV file

## full_version.py

### *def usr_dir(username)*:
Returns path for user profiles 

### *def create_user(username)*:
Creates a new user if username does not exist

### *def list_users()*:
Returns lists of users

### *def create_wishlist(username, wishlist_name)*:
Creates a wishlist

### *def list_wishlists(username)*:
Listing all the wishlists for a user

### *def delete_wishlist(username, wishlist_name)*:
Deletes the mentioned wishlist

### *def wishlist_add_item(username, wishlist_name, item_data)*:
Adds the item to the wishlist

### *def read_wishlist(username, wishlist_name)*:
Returns the wishlist with all items in it

### *def wishlist_remove_list(username, wishlist_name, indx)*:
Deletes the item from the wishlist

### _def_ create_user(email, password=None, name=None, mongo=None):
Creates and stores user information in the database.

### _def_ check_user(email, password=None, mongo=None):
Checks if the user exists in the 'users' collection

### _def_ wishlist_add_item(email, wishlist_name, item_data, mongo=None):
Adds an item to a user's wishlist and updates the database.

### _def_ read_wishlist(email, wishlist_name, mongo=None):
Fetches a user's wishlist from the database.

### _def_ wishlist_remove_list(email, wishlist_name, index, mongo=None):
Removes an item from a user's wishlist by index.

### _def_ share_wishlist(email_sender, wishlist_name, email_receiver, mongo=None):
Shares a user's wishlist via email.












