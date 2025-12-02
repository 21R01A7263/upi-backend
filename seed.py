from database import SessionLocal
from crud import create_user, create_merchant

db = SessionLocal()

print("Seeding data...")

# Create a Dummy User (The Payer)
# Username: @user, PIN: 1234, Balance: 10,000
try:
    user = create_user(db, "user", "Test User", "1234", 10000.0)
    print(f"Created User: {user.username} (ID: {user.id})")
except Exception as e:
    print(f"User might already exist: {e}")

# Create a Dummy Merchant (The Receiver)
# Handle: @merchant, Balance: 0
try:
    merchant = create_merchant(db, "@merchant", "Randy's Shop", 0.0)
    print(f"Created Merchant: {merchant.handle} (ID: {merchant.id})")
except Exception as e:
    print(f"Merchant might already exist: {e}")

db.close()