import sqlite3

DATABASE_NAME = 'bidding_system.db'

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables():
    """Create the necessary tables for the bidding system."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    user_type TEXT NOT NULL,
                    phone_number TEXT
                );
            """)

            # Create products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    farmer_id TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity_kg REAL,
                    base_price REAL,
                    image_url TEXT,
                    FOREIGN KEY (farmer_id) REFERENCES users(user_id)
                );
            """)

            # Create bids table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bids (
                    bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    buyer_id TEXT NOT NULL,
                    bid_amount REAL NOT NULL,
                    bid_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    FOREIGN KEY (buyer_id) REFERENCES users(user_id)
                );
            """)
            
            # Create feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    feedback_text TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
            """)

            conn.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    else:
        print("Error! Cannot create the database connection.")

# Additional database functions for CRUD operations

def add_user(user_id, username, password, user_type, phone_number):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, username, password, user_type, phone_number)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, password, user_type, phone_number))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        if conn:
            conn.close()

def get_user_by_username(username):
    conn = create_connection()
    user = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, password, user_type, phone_number FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return user

def get_user_by_id(user_id):
    conn = create_connection()
    user = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, password, user_type, phone_number FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return user

def add_product(product_id, farmer_id, product_name, quantity_kg, base_price, image_url):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (product_id, farmer_id, product_name, quantity_kg, base_price, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product_id, farmer_id, product_name, quantity_kg, base_price, image_url))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        if conn:
            conn.close()

def get_all_products():
    conn = create_connection()
    products = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, farmer_id, product_name, quantity_kg, base_price, image_url FROM products")
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return products

def add_bid(product_id, buyer_id, bid_amount):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bids (product_id, buyer_id, bid_amount)
            VALUES (?, ?, ?)
        """, (product_id, buyer_id, bid_amount))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def get_highest_bids():
    conn = create_connection()
    highest_bids = {}
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, buyer_id, MAX(bid_amount) as max_bid
            FROM bids
            GROUP BY product_id
        """)
        rows = cursor.fetchall()
        for row in rows:
            highest_bids[row[0]] = {'buyer_id': row[1], 'bid_amount': row[2]}
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return highest_bids

def add_feedback(user_id, feedback_text):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (user_id, feedback_text)
            VALUES (?, ?)
        """, (user_id, feedback_text))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def get_all_feedback():
    conn = create_connection()
    feedbacks = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.feedback_id, u.username, u.user_type, f.feedback_text
            FROM feedback f
            JOIN users u ON f.user_id = u.user_id
        """)
        feedbacks = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return feedbacks

def get_all_bids():
    conn = create_connection()
    bids = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.product_id, p.product_name, u.username as buyer_name, b.bid_amount, b.bid_time
            FROM bids b
            JOIN products p ON b.product_id = p.product_id
            JOIN users u ON b.buyer_id = u.user_id
            ORDER BY b.bid_time DESC
        """)
        bids = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return bids

def get_all_farmers():
    conn = create_connection()
    farmers = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, phone_number FROM users WHERE user_type = 'farmer'")
        farmers = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return farmers

def get_all_buyers():
    conn = create_connection()
    buyers = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, phone_number FROM users WHERE user_type = 'buyer'")
        buyers = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return buyers

def delete_user(user_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def delete_all_feedback():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feedback")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def delete_all_bids():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bids")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def delete_all_products():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_tables()
