import streamlit as st
import pandas as pd

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .crop-banner {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }
    .crop-image {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: #f0f8f0;
    }
    .product-card {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
        color: black !important;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state to store users, products, bids, and highest bid data
if 'farmers' not in st.session_state:
    st.session_state.farmers = {}  # farmer_id -> farmer details
if 'buyers' not in st.session_state:
    st.session_state.buyers = {}   # buyer_id -> buyer details
if 'products' not in st.session_state:
    st.session_state.products = {} # product_id -> product details
if 'bids' not in st.session_state:
    st.session_state.bids = {}     # product_id -> list of bids {buyer_id, bid_amount}
if 'highest_bids' not in st.session_state:
    st.session_state.highest_bids = {}  # product_id -> highest bid {buyer_id, bid_amount}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'users' not in st.session_state:
    st.session_state.users = {}  # username -> {'password': pwd, 'type': 'farmer' or 'buyer', 'id': id}
if 'feedback' not in st.session_state:
    st.session_state.feedback = []  # list of {'user_type': , 'user_name': , 'feedback': }

# Main Header with Crop Images
st.markdown("""
<div class="main-header">
    <h1>🌱 Online Vegetable Bidding System 🌱</h1>
    <p>Fresh from Farm to Table - Bid on Quality Produce</p>
</div>

""", unsafe_allow_html=True)

def login():
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #1565c0; margin-bottom: 15px;">🔐 Welcome Back!</h3>
        <p style="color: #1565c0;">Login to access your account and start bidding on fresh produce.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

        if st.button("🚀 Login", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.session_state.user_id = "admin"
                st.session_state.username = "admin"
                st.markdown('<div class="success-message">🎉 Welcome Admin! You have full access to manage the system.</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                user = st.session_state.users.get(username)
                if user and user['password'] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_type = user['type']
                    st.session_state.user_id = user['id']
                    st.session_state.username = username
                    st.markdown(f'<div class="success-message">🎉 Welcome back, {username}! Ready to {user["type"]}?</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<div class="error-message">❌ Invalid username or password. Please try again.</div>', unsafe_allow_html=True)



def signup():
    st.markdown("""
    <div style="background-color: #f3e5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #6a1b9a; margin-bottom: 15px;">🌟 Join Our Fresh Community!</h3>
        <p style="color: #6a1b9a;">Create your account and start your journey in the world of fresh produce trading.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        user_type = st.selectbox("🌾 I am a", ("Farmer", "Buyer"), help="Select your role in the marketplace")
        user_id = st.text_input("🆔 Enter your ID", placeholder="Unique identifier")
        username = st.text_input("👤 Choose a username", placeholder="Your display name")
        password = st.text_input("🔐 Choose a password", type="password", placeholder="Secure password")

        if st.button("🎉 Create Account", use_container_width=True):
            if not all([user_id, username, password]):
                st.markdown('<div class="error-message">❌ Please fill in all fields!</div>', unsafe_allow_html=True)
            elif username in st.session_state.users:
                st.markdown('<div class="error-message">❌ Username already exists! Please choose a different one.</div>', unsafe_allow_html=True)
            else:
                st.session_state.users[username] = {'password': password, 'type': user_type.lower(), 'id': user_id}
                if user_type == "Farmer":
                    st.session_state.farmers[user_id] = username
                    st.markdown(f'<div class="success-message">🎉 Welcome Farmer {username}! Start listing your fresh produce for bidding.</div>', unsafe_allow_html=True)
                else:
                    st.session_state.buyers[user_id] = username
                    st.markdown(f'<div class="success-message">🎉 Welcome Buyer {username}! Start bidding on fresh produce from local farmers.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 🌱 Why Join Us?")
        st.markdown("✅ **Farmers:** Sell directly to buyers")
        st.markdown("✅ **Buyers:** Get fresh produce at fair prices")
        st.markdown("✅ **Quality:** Farm-fresh guarantee")
        st.markdown("✅ **Community:** Support local agriculture")

        # Show different images based on user type selection
        if user_type == "Farmer":
            st.image("https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?w=200&h=200&fit=crop&crop=center", width=150, caption="🌾 Ready to Farm!")
        else:
            st.image("https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=200&h=200&fit=crop&crop=center", width=150, caption="🛒 Ready to Shop!")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.success("Logged out successfully")

def list_product():
    st.markdown("""
    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #2e7d32; margin-bottom: 15px;">🌾 Farmer: List Your Fresh Produce</h3>
    </div>
    """, unsafe_allow_html=True)

    farmer_id = st.session_state.user_id
    col1, col2 = st.columns([2, 1])

    with col1:
        product_id = st.text_input("Product ID")
        product_name = st.text_input("Product Name")
        quantity_kg = st.number_input("Quantity (kg)", min_value=0.0, format="%.2f")
        base_price = st.number_input("Set Starting Price (₹)", min_value=0.0, format="%.2f")

    with col2:
        crop_options = {
            "Tomato": "https://images.unsplash.com/photo-1546470427-e9e826f7d9e7?w=200&h=200&fit=crop&crop=center",
            "Broccoli": "https://images.unsplash.com/photo-1566842600175-97dca489844d?w=200&h=200&fit=crop&crop=center"
        }
        selected_crop = "Tomato"

    uploaded_file = st.file_uploader("Or Upload Custom Product Image", type=["jpg", "png", "jpeg"])

    if st.button("🚀 List Product"):
        if product_id in st.session_state.products:
            st.markdown('<div class="error-message">❌ Product ID already exists!</div>', unsafe_allow_html=True)
        else:
            image = crop_options[selected_crop]  # Default to selected crop image
            if uploaded_file is not None:
                image = uploaded_file
            st.session_state.products[product_id] = {
                'farmer_id': farmer_id,
                'product_name': product_name,
                'quantity_kg': quantity_kg,
                'base_price': base_price,
                'image': image
            }
            st.markdown('<div class="success-message">✅ Product listed successfully! Fresh produce is now available for bidding.</div>', unsafe_allow_html=True)
            st.markdown("### 🔔 Notifying Buyers")
            if st.session_state.buyers:
                st.write(f"📢 Buyers Notified: {', '.join(st.session_state.buyers.values())}")
            else:
                st.write("📢 No buyers registered yet. Product will be visible when buyers sign up!")

def place_bid():
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #856404; margin-bottom: 15px;">💰 Buyer: Place Your Bid</h3>
        <p style="color: #856404;">Find the freshest produce and place competitive bids!</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.products:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px;">
            <h4>🥕 No Products Available Yet</h4>
            <p>Check back soon! Farmers are working hard to bring you fresh produce.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    buyer_id = st.session_state.user_id
    product_options = []
    for pid, pdata in st.session_state.products.items():
        product_options.append(f"{pid} - {pdata['product_name']}")

    product_choice = st.selectbox("🌽 Select Fresh Produce", options=product_options)

    if product_choice:
        product_id = product_choice.split(" - ")[0]
        product = st.session_state.products[product_id]

        col1, col2 = st.columns([1, 2])
        with col1:
            if product['image']:
                st.image(product['image'], caption=f"🍅 {product['product_name']}", width=200)
        with col2:
            st.markdown(f"""
            <div class="product-card">
                <h4>📦 Product Details</h4>
                <p><strong>Product ID:</strong> {product_id}</p>
                <p><strong>Name:</strong> {product['product_name']}</p>
                <p><strong>Quantity:</strong> {product['quantity_kg']} kg</p>
                <p><strong>Starting Price:</strong> ₹{product['base_price']}</p>
                <p><strong>Farmer:</strong> {st.session_state.farmers.get(product['farmer_id'], 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)

    bid_amount = st.number_input("💵 Enter Your Bid Amount (₹)", min_value=0.0, format="%.2f", step=0.50)

    if st.button("🚀 Place Bid"):
        if not product_choice:
            st.markdown('<div class="error-message">❌ Please select a product first!</div>', unsafe_allow_html=True)
            return

        product_id = product_choice.split(" - ")[0]
        base_price = st.session_state.products[product_id]['base_price']

        if bid_amount <= 0:
            st.markdown('<div class="error-message">❌ Please enter a valid bid amount!</div>', unsafe_allow_html=True)
        elif bid_amount < base_price:
            st.markdown(f'<div class="error-message">❌ Bid must be at least the starting price: ₹{base_price}</div>', unsafe_allow_html=True)
        else:
            st.session_state.bids.setdefault(product_id, [])
            st.session_state.bids[product_id].append({'buyer_id': buyer_id, 'bid_amount': bid_amount})

            highest = st.session_state.highest_bids.get(product_id)
            if highest is None or bid_amount > highest['bid_amount']:
                st.session_state.highest_bids[product_id] = {'buyer_id': buyer_id, 'bid_amount': bid_amount}
                st.markdown(f'<div class="success-message">🎉 Congratulations! You are now the highest bidder with ₹{bid_amount}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-message">✅ Bid placed successfully! Current highest bid: ₹{highest["bid_amount"]}</div>', unsafe_allow_html=True)

def show_highest_bids():
    st.markdown("""
    <div style="background-color: #d1ecf1; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #0c5460; margin-bottom: 15px;">🏆 Highest Bids Leaderboard</h3>
        <p style="color: #0c5460;">See who's winning the bidding war for fresh produce!</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.highest_bids:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px;">
            <h4>📊 No Bids Yet</h4>
            <p>The bidding hasn't started yet. Be the first to bid on fresh produce!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for pid, bid_info in st.session_state.highest_bids.items():
        product = st.session_state.products[pid]
        buyer_name = st.session_state.buyers[bid_info['buyer_id']]

        col1, col2 = st.columns([1, 2])
        with col1:
            if product['image']:
                st.image(product['image'], width=150, caption=f"🥇 #{pid}")
        with col2:
            st.markdown(f"""
            <div class="product-card">
                <h4>🏆 Winning Bid</h4>
                <p><strong>Product:</strong> {product['product_name']}</p>
                <p><strong>Quantity:</strong> {product['quantity_kg']} kg</p>
                <p><strong>🏅 Highest Bidder:</strong> {buyer_name}</p>
                <p><strong>💰 Winning Bid:</strong> ₹{bid_info['bid_amount']}</p>
                <p><strong>Farmer:</strong> {st.session_state.farmers.get(product['farmer_id'], 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

def notify_farmer():
    st.subheader("Notify Farmer about Final Sale")
    if not st.session_state.highest_bids:
        st.write("No sales yet.")
        return
    for pid, bid_info in st.session_state.highest_bids.items():
        product = st.session_state.products[pid]
        farmer_name = st.session_state.farmers[product['farmer_id']]
        buyer_name = st.session_state.buyers[bid_info['buyer_id']]
        st.write(f"Product '{product['product_name']}' sold to {buyer_name} for {bid_info['bid_amount']} (Farmer: {farmer_name})")

def user_feedback():
    st.subheader("User Feedback")
    user_name = st.text_input("Enter your name")
    feedback = st.text_area("Your feedback")
    if st.button("Submit Feedback"):
        st.session_state.feedback.append({
            'user_type': st.session_state.user_type,
            'user_name': user_name,
            'feedback': feedback
        })
        st.success("Thank you for your feedback!")

def view_feedback():
    st.subheader("All Feedback")
    if not st.session_state.feedback:
        st.write("No feedback yet.")
    else:
        for fb in st.session_state.feedback:
            st.write(f"**Type:** {fb['user_type']}")
            st.write(f"**Name:** {fb['user_name']}")
            st.write(f"**Feedback:** {fb['feedback']}")
            st.write("---")

def view_bidding_details():
    st.subheader("All Bidding Details")
    if not st.session_state.bids:
        st.write("No bids yet.")
    else:
        for pid, bids in st.session_state.bids.items():
            st.write(f"**Product ID:** {pid}")
            for bid in bids:
                buyer_name = st.session_state.buyers[bid['buyer_id']]
                st.write(f"Bidder: {buyer_name}, Amount: {bid['bid_amount']}")
            st.write("---")

def manage_farmers():
    st.subheader("Manage Farmers")
    for fid, fname in list(st.session_state.farmers.items()):
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"ID: {fid}, Name: {fname}")
        with col2:
            if st.button(f"Delete {fid}", key=f"del_farmer_{fid}"):
                del st.session_state.farmers[fid]
                if fname in st.session_state.users:
                    del st.session_state.users[fname]
                st.success(f"Farmer {fname} deleted")
                st.rerun()

def manage_buyers():
    st.subheader("Manage Buyers")
    for bid, bname in list(st.session_state.buyers.items()):
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"ID: {bid}, Name: {bname}")
        with col2:
            if st.button(f"Delete {bid}", key=f"del_buyer_{bid}"):
                del st.session_state.buyers[bid]
                if bname in st.session_state.users:
                    del st.session_state.users[bname]
                st.success(f"Buyer {bname} deleted")
                st.rerun()

def delete_data():
    st.subheader("Delete Data")
    if st.button("Delete All Feedback"):
        st.session_state.feedback = []
        st.success("All feedback deleted")
    if st.button("Delete All Bids"):
        st.session_state.bids = {}
        st.session_state.highest_bids = {}
        st.success("All bids deleted")
    if st.button("Delete All Products"):
        st.session_state.products = {}
        st.success("All products deleted")

menu_logged_out = ["Login", "Sign Up"]
menu_logged_in_farmer = ["List Product", "Notify Farmer", "Logout"]
menu_logged_in_buyer = ["Place Bid", "View Highest Bids", "User Feedback", "Logout"]
menu_logged_in_admin = ["View Feedback", "View Bidding Details", "Manage Farmers", "Manage Buyers", "Delete Data", "Logout"]

if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Navigate", menu_logged_out)
    if choice == "Login":
        login()
    elif choice == "Sign Up":
        signup()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.user_type.capitalize()})")
    if st.session_state.user_type == "farmer":
        choice = st.sidebar.selectbox("Navigate", menu_logged_in_farmer)
        if choice == "List Product":
            list_product()
        elif choice == "Notify Farmer":
            notify_farmer()
        elif choice == "Logout":
            logout()
    elif st.session_state.user_type == "buyer":
        choice = st.sidebar.selectbox("Navigate", menu_logged_in_buyer)
        if choice == "Place Bid":
            place_bid()
        elif choice == "View Highest Bids":
            show_highest_bids()
        elif choice == "User Feedback":
            user_feedback()
        elif choice == "Logout":
            logout()
    elif st.session_state.user_type == "admin":
        choice = st.sidebar.selectbox("Navigate", menu_logged_in_admin)
        if choice == "View Feedback":
            view_feedback()
        elif choice == "View Bidding Details":
            view_bidding_details()
        elif choice == "Manage Farmers":
            manage_farmers()
        elif choice == "Manage Buyers":
            manage_buyers()
        elif choice == "Delete Data":
            delete_data()
        elif choice == "Logout":
            logout()
