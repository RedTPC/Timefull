from flask import Flask, render_template, request, url_for, session, redirect, g
from flask_session import Session
from flask_wtf import FlaskForm 
from forms import LoginForm, RegistrationForm, ReviewForm, PaymentForm, EditPriceForm, SearchForm, EditStockForm, ContactForm
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.teardown_appcontext(close_db)


@app.before_request
def load_logged_in_user():
    g.user = session.get("username", None)
    session['logged_in'] = 'username' in session
    #need to set username and then associate logged in with it

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/dev", methods=["GET", "POST"])
def dev():
    
    form = ContactForm()

    if form.validate_on_submit():
        attribute = form.attribute.data
        contact_text = form.contact_text.data
        user = session["username"]

        db = get_db()

        db.execute("""INSERT INTO reports (issue, report_text, user)
                      VALUES (?, ?, ?);""", (attribute, contact_text, user))
            
        db.commit()




    return(render_template("dev.html", form=form))

@app.route("/reports", methods=["GET", "POST"])
def reports():
    
 

    db = get_db()

    users = db.execute("""SELECT * FROM users;""")

    reports = db.execute("""SELECT * FROM reports;""")
        



    return(render_template("reports.html", users=users, reports=reports))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    
    db= get_db()
    form = EditPriceForm()

    if form.validate_on_submit():
        attribute = form.attribute.data
        price = form.price.data

        db.execute("""UPDATE products SET price = ? WHERE name = ? COLLATE NOCASE;""", (price, attribute))
        db.commit()

    db= get_db()

    products = db.execute("""SELECT *
                           FROM products;""", ()).fetchall()
    
    users =  db.execute("""SELECT *
                           FROM users;""", ()).fetchall()

    return(render_template("admin.html", products=products, form=form, users=users))

# @app.route("/edit_price", methods=["GET", "POST"])
# def edit_price():

#     form = EditPriceForm()
#     if form.validate_on_submit():
#         attribute = form.atrribute.data
#         price = price.password.data

#     db= get_db()
#     products = db.execute("""SELECT *
#                            FROM products;""", ()).fetchall()
    

    

#    return(render_template("admin.html", products=products))

@app.route("/", methods=["GET", "POST"])
def root():

    return(redirect(url_for("clocks")))

@app.route("/clocks", methods=["GET", "POST"])
def clocks():

    form = SearchForm()

    db = get_db()

    clocks = db.execute("""SELECT *
                           FROM products;""", ()).fetchall()

    search_result = []


    
  
    if form.validate_on_submit():
        attribute = form.attribute.data
        # max_price = float(form.max_price.data)
        # min_price = float(form.min_price.data)
        max_price = form.max_price.data
        min_price = form.min_price.data

        db = get_db()

        if attribute == "All":
            search_result = db.execute("""SELECT *
                                          FROM products
                                          WHERE price BETWEEN ? AND ?;""", (min_price, max_price)).fetchall()
            
        else:
            search_result = db.execute("""SELECT *
                                          FROM products
                                          WHERE tag = ? AND price BETWEEN ? AND ?;""", (attribute, min_price, max_price)).fetchall()
        
    else:
        attribute = ""
        max_price = ""
        min_price = ""


    return(render_template("HomePage.html", clocks=clocks, form=form, attribute=attribute, max_price=max_price, min_price=min_price, search_result=search_result))

@app.route("/stock", methods=["GET", "POST"])
def stock():

    db = get_db()
    products = db.execute("""SELECT *
                             FROM products;""", ()).fetchall()

    form2 = EditStockForm()

    if form2.validate_on_submit():
        attribute = form2.attribute.data
        stock = form2.stock.data

        
        db = get_db()
        db.execute("""UPDATE products SET stock = ? WHERE name = ? COLLATE NOCASE;""", (stock, attribute))
        db.commit()

    return(render_template("stock.html", form2=form2, products=products))

@app.route("/login", methods=["GET", "POST"])
def login():
    error=""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db=get_db()

        user = db.execute("""SELECT * FROM users
                             WHERE username = ?;""", (username,)).fetchone()
        
        if user is None:
            form.username.errors.append("Invalid Username")

        elif not check_password_hash(user["password"], password):
            form.username.errors.append("Incorrect Password")

        else:
            session.clear()
            session["username"] = username
            
            #admin login
            if username == "admin" and password == "admin":
                session["admin_clearance"] = True
                return(redirect(url_for("admin")))
            
            else:
                session["admin_clearance"] = False
            
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("clocks")
            return redirect(next_page)
    
        
    print("A user logged in :)")


        
    return render_template("login.html", form=form, error=error)

# @app.route("/logout", methods=["GET", "POST"])
# def logout():   
#     session.clear()
#     return redirect( url_for("clocks") )



@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        db = get_db()
        conflict_user = db.execute("""SELECT *
                             FROM users
                             WHERE username = ?;""", (username,)).fetchone()
        
        if conflict_user is not None:
            form.username.errors.append("Username is taken.")

        else:
            db.execute("""INSERT INTO users (username, password)
                          VALUES (?, ?);""", (username, generate_password_hash(password1)))
            
            db.commit()
            return(redirect( url_for("login") ))
            #return("hello")


    return(render_template("register.html", form=form))


# @app.route("/clocks2", methods=["GET", "POST"])
# def find_account():

#     db = get_db()

#     account_id = 1
    
#     clocks = db.execute("""SELECT *
#                              FROM products
#                              WHERE name = ?;""", (holder,)).fetchall()
    
#     print(type(clocks))
#     print(clocks)

#     return(render_template("HomePage.html", clocks=clocks))

@app.route("/clock/<int:item_id>", methods=["GET", "POST"])
def item(item_id):

    db = get_db()
   
    item = db.execute("""SELECT *
                         FROM products
                         WHERE item_id = ?;""", (item_id,)).fetchone()

    reviews = db.execute("""SELECT *
                        FROM reviews
                        WHERE item_id = ?;""", (item_id,)).fetchall()
    

    return(render_template("item.html", item=item, reviews=reviews))

@app.route("/add_to_cart/<int:item_id>", methods=["GET", "POST"])
# @login_required
def add_to_cart(item_id):

    if "cart" not in session:
        session["cart"] = {}

    if item_id not in session["cart"]: 
        session["cart"][item_id] = 1

    else:
        session["cart"][item_id] = session["cart"][item_id] + 1 
    
    return redirect( url_for("cart") )

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    names = {}
    prices = {}
    db = get_db()

    subtotal = 0


    

    for item_id, quantity in cart.items():
        item = db.execute("""SELECT *
                             FROM products 
                             WHERE item_id = ?;""", (item_id,)).fetchone()
        
        if item:

            names[item_id] = item['name']
            prices[item_id] = item['price']


        # prices = db.execute("""SELECT price
        #                      FROM products 
        #                      WHERE item_id = ?;""", (item_id,)).fetchone()

        

        # subtotal = 0 #is this problematic because it isn't a cookie??
        # for i in 

            item_tot = prices[item_id] * quantity
            print(item_tot)
            subtotal += item_tot
            print(subtotal)
            session["subtotal"] = subtotal

    vat = subtotal * 1.135
    vat = round(vat, 2)
    return render_template("cart.html", cart=cart, names=names, prices=prices, subtotal=subtotal, vat=vat)

#uncommenting this at my own peril, please dont make me regret it mr reviews

@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    db = get_db()
    reviews = db.execute("""SELECT *
                           FROM reviews;""").fetchall()
    
    #item id search :///////
    # item = db.execute("""SELECT name FROM products WHERE item_id = ?""", (reviews["item_id"], )).fetchone()
    #idk bro imma just display the item id

    if reviews:
        return render_template("reviews.html", reviews=reviews)
    else:
        return "No reviews were found, 404!", 404


    
@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    form = ReviewForm()

    if form.validate_on_submit():
        item_name = form.attribute.data
        review_text = form.review_text.data
        rating = form.rating.data
        username = session.get('username')

        #if they arent logged in tell them to go away
        if not username:
            return redirect(url_for("login"))

        db = get_db()

        # for debug only use if it break again oh god please no
        #print(f"lookin for item_name: {item_name}")

        #COLLATE NOCASE REALLY IMPORTANT BECAUSE CASES ARE FUCKED check lab6 databases slides
        item = db.execute("""SELECT item_id FROM products WHERE name = ? COLLATE NOCASE""", (item_name,)).fetchone()

        #more debug
        #print(f"got the item !!!: {item}")

        if item:
            item_id = item["item_id"]

            db.execute("""INSERT INTO reviews (item_id, review_text, rating, username)
                          VALUES (?, ?, ?, ?)""", (item_id, review_text, rating, username))
            db.commit()

            return redirect(url_for("item", item_id=item_id)) 
        else:
            form.attribute.errors.append("That item does not exist")

    return render_template('write_review.html', form=form)











@app.route("/profile_viewer", methods=["GET", "POST"])
def profile_viewer():
    if 'username' not in session:
        return render_template("empty_profile.html")

    username = session['username']

    return render_template("profile.html", username=username)
  
@app.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):

    #creates an epic cart in sesh if it doesn't have one
    if "cart" not in session:
        session["cart"] = {}


    if item_id in session["cart"]:
        #nuke the item id from the cart, doesnt delete the cart
        del session["cart"][item_id]

    return redirect(url_for("cart"))

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    print("A user logged out :(")
    return redirect(url_for("clocks")) 

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "cart" not in session:
        return redirect(url_for("cart"))
        #sends the user back to the shadow realm if their cart is empty


    cart = session["cart"]
    names = {}
    db = get_db()

    for item_id in cart:
        item = db.execute("""SELECT *
                             FROM products 
                             WHERE item_id = ?;""", (item_id,)).fetchone()
        names[item_id] = item['name']

    form = PaymentForm()

    firstname = ""
    surname = ""
    email = ""
    postcode = ""

    card_number = 0
    expiry_date = ""
    CCV = 0

    if form.validate_on_submit():

        firstname = form.firstname.data
        surname = form.surname.data
        email = form.email.data
        postcode = form.postcode.data

        card_number = form.card_number.data
        expiry_date = form.expiry_date.data
        CCV = form.CCV.data

        username = session.get('username')

        #LUHN CHECKSUM ALGORITHM
        #REVERSE DIGITS (PALINDROME)
        reversed = card_number[::-1]
        #print(reversed)
        #reversed = int(reversed)

        # for every 2nd digit double it and put it back as str
        temp = (str(reversed))
        length = len(temp)
        total = 0
        for i in range(length):
            digit = int(reversed[i])
        

            if i % 2 == 1:                 # Double every second digit
                digit = digit * 2



                if digit > 9:                  # remove 9 if the num is bigger than 9
                    digit = digit - 9
            
            total += digit
    
        # checkif the total is divisible by tenn
        if total % 10 != 0:
            return render_template("reciept.html", form=form, names=names,cart=cart,firstname=firstname, email=email,postcode=postcode, surname=surname, card_number=card_number, expiry_date=expiry_date, CCV=CCV)
        
        if total % 10 == 0:
            form.card_number.errors.append("Invalid Card Number")

        #this didn't work at all idk why :/

    return render_template("checkout.html", form=form, names=names,cart=cart,firstname=firstname, email=email,postcode=postcode, surname=surname, card_number=card_number, expiry_date=expiry_date, CCV=CCV)
    
    