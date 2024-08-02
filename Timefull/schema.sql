DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    item_id INTEGER,
    description TEXT,
    image TEXT,
    tag TEXT,
    stock INTEGER
);

INSERT INTO products (name, price, item_id, description, image, tag, stock)
VALUES
    ("Sharpy", 10.99, 0001, "An elegant tool for an elegant wall", "sharp.jpg", "C", 50),
    ("Pinky", 15.49, 0002, "A dash of colour to entice the imagination", "pink.jpg", "C", 40),
    ("Timey", 29.99, 0003, "An old dog with all the tricks he needs", "timey.jpg", "C", 79),
    ("Wakey", 15.49, 0004, "Functional and formal, perfect for the worm-catchers", "wakey.jpeg", "C", 400),
    ("Bitey", 15.49, 0005, "A gizmo with low design but high functionality", "apple.jpeg", "W", 22),
    ("Whimey", 15.49, 0006, "It's a watch", "watch.jpg", "W", 43),
    ("Sparky", 15.49, 0007, "Embrace your inner techno with this striking piece", "electro.jpg", "C", 0);


DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL

);

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    username TEXT,
    review_text TEXT,
    rating INTEGER
);

DROP TABLE IF EXISTS reports;


CREATE TABLE reports (
    report INTEGER PRIMARY KEY AUTOINCREMENT,
    issue TEXT,
    report_text TEXT,
    user TEXT
);



    


    
