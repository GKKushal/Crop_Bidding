# TODO List for Adding Login/Signup and Reorganizing Bidding App

## 1. Add Authentication Functionality
- [x] Implement login and signup pages with session-based authentication.
- [x] Add user roles (farmer, buyer) during signup.
- [x] Store user credentials in session state (for simplicity, in production use a database).

## 2. Reorganize App Structure
- [x] Modify the main app to check if user is logged in.
- [x] Update sidebar menu to show login/signup or main pages based on auth state.
- [x] Separate bidding details (place bid, highest bid) into a new page.
- [x] Separate feedback into a new page.

## 3. Integrate Existing Functionality
- [x] Ensure farmer/buyer registration is part of signup or separate pages.
- [x] Preserve product listing, bidding, and highest bids functionality.
- [x] Update notifications and success messages.

## 4. Testing and Followup
- [x] Test login/signup flow.
- [x] Test bidding details and feedback pages.
- [x] Run the app and verify all features work correctly.

## 5. Additional Features
- [x] Add product name display for buyers in place bid.
- [x] Add image upload for farmers when listing products.
- [x] Display product images in buyer details (place bid, highest bids).
- [x] Display logged-in user's name and role on the page.
- [x] Add quantity (kg) field when listing products.
- [x] Add admin login and admin page with feedback, bidding details, manage farmers/buyers, delete data.
