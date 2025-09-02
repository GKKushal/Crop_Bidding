# TODO List for Integrating SQLite Database into Bidding App

## 1. Update database.py
- [x] Add functions to insert/retrieve users, products, bids, feedback from database
- [x] Add function to initialize database connection and create tables if not exist

## 2. Modify app.py for Database Integration
- [x] Import database functions
- [x] Initialize database on app start
- [x] Replace session_state users with database queries
- [x] Replace session_state products with database queries
- [x] Replace session_state bids with database queries
- [x] Replace session_state feedback with database queries
- [x] Update login function to query database
- [x] Update signup function to insert into database
- [x] Update list_product to insert into database
- [x] Update place_bid to insert into database
- [x] Update feedback functions to use database
- [x] Add phone number field to signup and store in database

## 3. Testing and Verification
- [x] Test user registration and login
- [x] Test product listing
- [x] Test bidding functionality
- [x] Test feedback submission
- [x] Verify data persistence across app restarts
- [x] Fix UploadedFile binding error in database
- [x] Fix missing session_state references
