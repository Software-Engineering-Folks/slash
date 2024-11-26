import os
from datetime import datetime
from flask import jsonify
from flask import Flask, session, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests
from dotenv import load_dotenv
from .formatter import sortList, filterList
from .scraper import driver
from .features_db import ( create_user, check_user, wishlist_add_item, read_wishlist, wishlist_remove_list, share_wishlist, load_comments)

load_dotenv()

app = Flask(__name__, template_folder=".")
app.secret_key = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI") + os.getenv("DB_NAME")

mongo = PyMongo(app)

fetched_data = {}

# Google OAuth2 setup (Use secure transport in production)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__).removesuffix('modules'), "client_secret_92320207172-8cnk4c9unfaa7llua906p6kjvhnvkbqd.apps.googleusercontent.com.json")
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
)

# Routes
@app.route('/test')
def test_db():
    '''
    Route for testing if DB is connected properly
    '''
    try:
        user = mongo.db.users.find_one({"email": "test_user"})
        if user:
            return "Connected! Found test user."
        return "Connected! No test user found."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def landingpage():
    return render_template("./static/landing.html", login='username' in session)

@app.route('/homepage')
def homepage():
    return render_template('./static/login.html')

@app.route('/callback', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if check_user(username, request.form['password'], mongo=mongo):
            session['username'] = username
            return redirect(url_for('landingpage'))
        return render_template("./static/landing.html", login=False, invalid=True)
    return render_template('./static/login.html')

@app.route('/login/google')
def login_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/login')
def callback():
    print("Callback URL:", request.url)
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.Request()
    id_info = id_token.verify_oauth2_token(credentials.id_token, request_session, flow.client_config['client_id'])

    session['username'] = id_info['email']
    session['user_info'] = {'name': id_info['name'], 'email': id_info['email']}
    if not check_user(session['username'], None, mongo=mongo):
        create_user(session['username'], None, name=id_info['name'], mongo=mongo)

    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if create_user(request.form['username'], request.form['password'], mongo=mongo):
            return redirect(url_for('login'))
        return render_template("./static/landing.html", login=False, invalid=True)
    return render_template('./static/login.html')

@app.route('/wishlist')
def wishlist():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session.get('username')
    wishlist_name = session.get('wishlist_name', 'default')

    items = read_wishlist(username, wishlist_name, mongo=mongo)
    items = sorted(items, key=lambda x: x.get('added_date', ''), reverse=True)
    return render_template('./static/wishlist.html', items=items)

@app.route('/share', methods=['POST'])
def share():
    share_wishlist(session['username'], "default", request.form['email'], mongo=mongo)
    return redirect(url_for('wishlist'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landingpage'))

@app.route("/search", methods=["POST", "GET"])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))

    product = request.args.get("product_name") or request.form.get("product_name")
    if not product:
        return render_template("./static/result.html", error="Please enter a search term.", total_pages=0)

    try:
        data = driver(product, currency=None)
        fetched_data[product] = data
    except Exception as e:
        print("Exception occured in Driver: ", e)
        data = None

    if data is None or data.empty:
        return render_template("./static/result.html", error="No results found for your search.", total_pages=0)

    comments = load_comments(product_name=product, mongo=mongo)
    total_pages = (len(data) + 19) // 20
    return render_template(
        "./static/result.html", data=data.to_dict(orient='records'), prod=product,
        total_pages=total_pages, comments=comments
    )

@app.route('/add_comment', methods=['POST'])
def add_comment():
    product_name = request.form.get('product_name')
    comment = request.form.get('comment')
    username = session.get('username')

    if product_name and comment and username:
        mongo.db.comments.insert_one({
            "product_name": product_name,
            "username": username,
            "comment": comment,
            "commented_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return redirect(url_for('search'))

@app.route("/filter", methods=["POST", "GET"])
def product_search_filtered():
    product = request.args.get("product_name")
    sort = request.form.get("sort")
    currency = request.form.get("currency")
    min_price, max_price, min_rating = map(
        lambda x: float(x) if x else None, [
            request.form.get("min_price"),
            request.form.get("max_price"),
            request.form.get("min_rating")
        ]
    )
    data = sortList(fetched_data[product], sort[0:2], reverse=(sort[2:] == 'asc'))
    data = filterList(data, min_price, max_price, min_rating)
    comments = load_comments(product_name=product, mongo=mongo)
    total_pages = (len(data) + 19) // 20
    return render_template(
        "./static/result.html", data=data.to_dict(orient='records'), prod=product,
        total_pages=total_pages, comments=comments
    )

@app.route("/add-wishlist-item", methods=["POST"])
def add_wishlist_item():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    item_data = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'website': request.form.get('website'),
        'link': request.form.get('link'),
        'img_link': request.form.get('img_link'),
        'rating': request.form.get('rating'),
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    wishlist_add_item(username, 'default', item_data, mongo=mongo)
    return jsonify({'status': 'success'})

@app.route("/delete-wishlist-item", methods=["POST"])
def remove_wishlist_item():
    username = session['username']
    index = int(request.form["index"])
    wishlist_remove_list(username, 'default', index, mongo=mongo)
    return redirect(url_for('wishlist'))

if __name__ == '__main__':
    app.run(debug=True)