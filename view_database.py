import sqlite3
import pandas as pd

def view_database():
    """Display all data from the bidding system database"""

    DATABASE_NAME = 'bidding_system.db'

    def get_connection():
        return sqlite3.connect(DATABASE_NAME)

    print("=== BIDDING SYSTEM DATABASE CONTENTS ===\n")

    # View Users
    print("1. USERS TABLE:")
    print("-" * 50)
    conn = get_connection()
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    if users_df.empty:
        print("No users found.")
    else:
        print(users_df.to_string(index=False))
    conn.close()
    print("\n")

    # View Products
    print("2. PRODUCTS TABLE:")
    print("-" * 50)
    conn = get_connection()
    products_df = pd.read_sql_query("SELECT * FROM products", conn)
    if products_df.empty:
        print("No products found.")
    else:
        print(products_df.to_string(index=False))
    conn.close()
    print("\n")

    # View Bids
    print("3. BIDS TABLE:")
    print("-" * 50)
    conn = get_connection()
    bids_df = pd.read_sql_query("SELECT * FROM bids", conn)
    if bids_df.empty:
        print("No bids found.")
    else:
        print(bids_df.to_string(index=False))
    conn.close()
    print("\n")

    # View Feedback
    print("4. FEEDBACK TABLE:")
    print("-" * 50)
    conn = get_connection()
    feedback_df = pd.read_sql_query("SELECT * FROM feedback", conn)
    if feedback_df.empty:
        print("No feedback found.")
    else:
        print(feedback_df.to_string(index=False))
    conn.close()
    print("\n")

    # View Highest Bids Summary
    print("5. HIGHEST BIDS SUMMARY:")
    print("-" * 50)
    conn = get_connection()
    highest_bids_df = pd.read_sql_query("""
        SELECT
            p.product_name,
            u.username as highest_bidder,
            MAX(b.bid_amount) as highest_bid,
            b.bid_time
        FROM bids b
        JOIN products p ON b.product_id = p.product_id
        JOIN users u ON b.buyer_id = u.user_id
        GROUP BY b.product_id
        ORDER BY b.bid_time DESC
    """, conn)
    if highest_bids_df.empty:
        print("No bids found.")
    else:
        print(highest_bids_df.to_string(index=False))
    conn.close()
    print("\n")

    print("=== END OF DATABASE CONTENTS ===")

if __name__ == "__main__":
    view_database()
