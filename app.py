import streamlit as st
import pandas as pd
import database

# Initialize database
database.create_tables()

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

# Initialize session state for login status only
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

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
            user = database.get_user_by_username(username)
            if user and user[2] == password:  # user[2] is password
                st.session_state.logged_in = True
                st.session_state.user_type = user[3]  # user[3] is user_type
                st.session_state.user_id = user[0]    # user[0] is user_id
                st.session_state.username = username
                st.markdown(f'<div class="success-message">🎉 Welcome back, {username}! Ready to {user[3]}?</div>', unsafe_allow_html=True)
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
        phone_number = st.text_input("📞 Phone Number", placeholder="Enter your phone number")
        username = st.text_input("👤 Choose a username", placeholder="Your display name")
        password = st.text_input("🔐 Choose a password", type="password", placeholder="Secure password")

        if st.button("🎉 Create Account", use_container_width=True):
            if not all([user_id, username, password, phone_number]):
                st.markdown('<div class="error-message">❌ Please fill in all fields!</div>', unsafe_allow_html=True)
            else:
                success = database.add_user(user_id, username, password, user_type.lower(), phone_number)
                if success:
                    st.markdown(f'<div class="success-message">🎉 Welcome {user_type} {username}! Start your journey in the fresh produce marketplace.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Username already exists! Please choose a different one.</div>', unsafe_allow_html=True)

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

def admin_login():
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #1565c0; margin-bottom: 15px;">🔐 Admin Login</h3>
        <p style="color: #1565c0;">Access the admin panel to manage the system.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        username = st.text_input("👤 Admin Username", placeholder="Enter admin username")
        password = st.text_input("🔒 Admin Password", type="password", placeholder="Enter admin password")

        if st.button("🚀 Admin Login", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.session_state.user_id = "admin"
                st.session_state.username = "admin"
                st.markdown('<div class="success-message">🎉 Welcome Admin! You have full access to manage the system.</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown('<div class="error-message">❌ Invalid admin credentials. Please try again.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔧 Admin Features")
        st.markdown("✅ **Manage Users:** View and delete farmers/buyers")
        st.markdown("✅ **View Feedback:** See all user feedback")
        st.markdown("✅ **Bidding Details:** Monitor all bids")
        st.markdown("✅ **Data Management:** Delete data as needed")

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
        image_url = crop_options[selected_crop]  # Default to selected crop image URL
        if uploaded_file is not None:
            # For now, we'll store the uploaded file name as a placeholder
            # In a real app, you'd save the file and store the path
            image_url = uploaded_file.name
        success = database.add_product(product_id, farmer_id, product_name, quantity_kg, base_price, image_url)
        if success:
            st.markdown('<div class="success-message">✅ Product listed successfully! Fresh produce is now available for bidding.</div>', unsafe_allow_html=True)
            st.markdown("### 🔔 Notifying Buyers")
            st.write("📢 Product is now live for bidding!")
        else:
            st.markdown('<div class="error-message">❌ Product ID already exists!</div>', unsafe_allow_html=True)

def place_bid():
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #856404; margin-bottom: 15px;">💰 Buyer: Place Your Bid</h3>
        <p style="color: #856404;">Find the freshest produce and place competitive bids!</p>
    </div>
    """, unsafe_allow_html=True)

    products = database.get_all_products()
    if not products:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px;">
            <h4>🥕 No Products Available Yet</h4>
            <p>Check back soon! Farmers are working hard to bring you fresh produce.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    buyer_id = st.session_state.user_id
    product_options = []
    products_dict = {}
    for product in products:
        pid, fid, pname, qty, price, img = product
        product_options.append(f"{pid} - {pname}")
        products_dict[pid] = {
            'farmer_id': fid,
            'product_name': pname,
            'quantity_kg': qty,
            'base_price': price,
            'image': img
        }

    product_choice = st.selectbox("🌽 Select Fresh Produce", options=product_options)

    if product_choice:
        product_id = product_choice.split(" - ")[0]
        product = products_dict[product_id]

        col1, col2 = st.columns([1, 2])
        with col1:
            if product['image']:
                st.image(product['image'], caption=f"🍅 {product['product_name']}", width=200)
        with col2:
            farmer_user = database.get_user_by_id(product['farmer_id'])
            farmer_name = farmer_user[1] if farmer_user else 'Unknown'
            farmer_phone = farmer_user[4] if farmer_user else 'N/A'

            # Get existing bids for this product
            existing_bids = database.get_all_bids()
            product_bids = [bid for bid in existing_bids if bid[0] == product_id]

            bid_info = ""
            if product_bids:
                highest_bid = max(product_bids, key=lambda x: x[3])
                bid_info = f"""
                <p><strong>Current Highest Bid:</strong> ₹{highest_bid[3]} by {highest_bid[2]}</p>
                <p><strong>Total Bids:</strong> {len(product_bids)}</p>
                """
            else:
                bid_info = "<p><strong>Status:</strong> No bids yet - Be the first!</p>"

            st.markdown(f"""
            <div class="product-card">
                <h4>📦 Product Details</h4>
                <p><strong>Product ID:</strong> {product_id}</p>
                <p><strong>Name:</strong> {product['product_name']}</p>
                <p><strong>Quantity:</strong> {product['quantity_kg']} kg</p>
                <p><strong>Starting Price:</strong> ₹{product['base_price']}</p>
                <p><strong>Farmer:</strong> {farmer_name}</p>
                <p><strong>Phone:</strong> {farmer_phone}</p>
                {bid_info}
            </div>
            """, unsafe_allow_html=True)

    bid_amount = st.number_input("💵 Enter Your Bid Amount (₹)", min_value=0.0, format="%.2f", step=0.50)

    if st.button("🚀 Place Bid"):
        if not product_choice:
            st.markdown('<div class="error-message">❌ Please select a product first!</div>', unsafe_allow_html=True)
            return

        product_id = product_choice.split(" - ")[0]
        base_price = products_dict[product_id]['base_price']

        if bid_amount <= 0:
            st.markdown('<div class="error-message">❌ Please enter a valid bid amount!</div>', unsafe_allow_html=True)
        elif bid_amount < base_price:
            st.markdown(f'<div class="error-message">❌ Bid must be at least the starting price: ₹{base_price}</div>', unsafe_allow_html=True)
        else:
            success = database.add_bid(product_id, buyer_id, bid_amount)
            if success:
                highest_bids = database.get_highest_bids()
                highest = highest_bids.get(product_id)
                if highest is None or bid_amount > highest['bid_amount']:
                    st.markdown(f'<div class="success-message">🎉 Congratulations! You are now the highest bidder with ₹{bid_amount}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-message">✅ Bid placed successfully! Current highest bid: ₹{highest["bid_amount"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-message">❌ Error placing bid. Please try again.</div>', unsafe_allow_html=True)

def show_highest_bids():
    st.markdown("""
    <div style="background-color: #d1ecf1; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #0c5460; margin-bottom: 15px;">🏆 Highest Bids Leaderboard</h3>
        <p style="color: #0c5460;">See who's winning the bidding war for fresh produce!</p>
    </div>
    """, unsafe_allow_html=True)

    highest_bids = database.get_highest_bids()
    products = database.get_all_products()
    products_dict = {p[0]: {'farmer_id': p[1], 'product_name': p[2], 'quantity_kg': p[3], 'base_price': p[4], 'image': p[5]} for p in products}

    if not highest_bids:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px;">
            <h4>📊 No Bids Yet</h4>
            <p>The bidding hasn't started yet. Be the first to bid on fresh produce!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for pid, bid_info in highest_bids.items():
        product = products_dict[pid]
        buyer_user = database.get_user_by_username(bid_info['buyer_id'])
        buyer_name = buyer_user[1] if buyer_user else bid_info['buyer_id']
        farmer_user = database.get_user_by_id(product['farmer_id'])
        farmer_name = farmer_user[1] if farmer_user else product['farmer_id']

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
                <p><strong>Farmer:</strong> {farmer_name}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

def notify_farmer():
    st.subheader("Notify Farmer about Final Sale")
    highest_bids = database.get_highest_bids()
    products = database.get_all_products()
    products_dict = {p[0]: {'farmer_id': p[1], 'product_name': p[2], 'quantity_kg': p[3], 'base_price': p[4], 'image': p[5]} for p in products}

    if not highest_bids:
        st.write("No sales yet.")
        return
    for pid, bid_info in highest_bids.items():
        product = products_dict[pid]
        farmer_user = database.get_user_by_id(product['farmer_id'])
        farmer_name = farmer_user[1] if farmer_user else product['farmer_id']
        buyer_user = database.get_user_by_username(bid_info['buyer_id'])
        buyer_name = buyer_user[1] if buyer_user else bid_info['buyer_id']
        st.write(f"Product '{product['product_name']}' sold to {buyer_name} for {bid_info['bid_amount']} (Farmer: {farmer_name})")

def user_feedback():
    st.subheader("User Feedback")
    user_name = st.text_input("Enter your name")
    feedback = st.text_area("Your feedback")
    if st.button("Submit Feedback"):
        success = database.add_feedback(st.session_state.user_id, feedback)
        if success:
            st.success("Thank you for your feedback!")
        else:
            st.error("Failed to submit feedback. Please try again.")

def view_feedback():
    st.subheader("All Feedback")
    feedbacks = database.get_all_feedback()
    if not feedbacks:
        st.write("No feedback yet.")
    else:
        for fb in feedbacks:
            st.write(f"**Type:** {fb[2]}")  # user_type
            st.write(f"**Name:** {fb[1]}")  # username
            st.write(f"**Feedback:** {fb[3]}")  # feedback_text
            st.write("---")

def view_bidding_details():
    st.subheader("All Bidding Details")
    bids = database.get_all_bids()
    if not bids:
        st.write("No bids yet.")
    else:
        current_product = None
        for bid in bids:
            pid, pname, buyer_name, amount, bid_time = bid
            if current_product != pid:
                if current_product is not None:
                    st.write("---")
                st.write(f"**Product:** {pname} (ID: {pid})")
                current_product = pid
            st.write(f"Bidder: {buyer_name}, Amount: ₹{amount}, Time: {bid_time}")
        st.write("---")

def manage_farmers():
    st.subheader("Manage Farmers")
    farmers = database.get_all_farmers()
    for farmer in farmers:
        fid, fname, fpass, ftype, fphone = farmer
        col1, col2 = st.columns([4,1])
        with col1:
            st.markdown(f"""
            <div class="product-card">
                <p><strong>ID:</strong> {fid}</p>
                <p><strong>Username:</strong> {fname}</p>
                <p><strong>Password:</strong> {fpass}</p>
                <p><strong>Type:</strong> {ftype}</p>
                <p><strong>Phone:</strong> {fphone}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(f"Delete {fid}", key=f"del_farmer_{fid}"):
                success = database.delete_user(fid)
                if success:
                    st.success(f"Farmer {fname} deleted")
                    st.rerun()
                else:
                    st.error("Failed to delete farmer")

def manage_buyers():
    st.subheader("Manage Buyers")
    buyers = database.get_all_buyers()
    for buyer in buyers:
        bid, bname, bpass, btype, bphone = buyer
        col1, col2 = st.columns([4,1])
        with col1:
            st.markdown(f"""
            <div class="product-card">
                <p><strong>ID:</strong> {bid}</p>
                <p><strong>Username:</strong> {bname}</p>
                <p><strong>Password:</strong> {bpass}</p>
                <p><strong>Type:</strong> {btype}</p>
                <p><strong>Phone:</strong> {bphone}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(f"Delete {bid}", key=f"del_buyer_{bid}"):
                success = database.delete_user(bid)
                if success:
                    st.success(f"Buyer {bname} deleted")
                    st.rerun()
                else:
                    st.error("Failed to delete buyer")

def delete_data():
    st.subheader("Delete Data")
    if st.button("Delete All Feedback"):
        success = database.delete_all_feedback()
        if success:
            st.success("All feedback deleted")
        else:
            st.error("Failed to delete feedback")
    if st.button("Delete All Bids"):
        success = database.delete_all_bids()
        if success:
            st.success("All bids deleted")
        else:
            st.error("Failed to delete bids")
    if st.button("Delete All Products"):
        success = database.delete_all_products()
        if success:
            st.success("All products deleted")
        else:
            st.error("Failed to delete products")

menu_logged_out = ["Login", "Sign Up", "Admin Login"]
menu_logged_in_farmer = ["List Product", "Notify Farmer", "Logout"]
menu_logged_in_buyer = ["Place Bid", "View Highest Bids", "User Feedback", "Logout"]
menu_logged_in_admin = ["View Feedback", "View Bidding Details", "Manage Farmers", "Manage Buyers", "Delete Data", "Logout"]

if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Navigate", menu_logged_out)
    if choice == "Login":
        login()
    elif choice == "Sign Up":
        signup()
    elif choice == "Admin Login":
        admin_login()
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
