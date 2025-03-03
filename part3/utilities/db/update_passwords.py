import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities.db.db_manager import connect_to_db
from werkzeug.security import generate_password_hash

db = connect_to_db()
customers_collection = db["customers"]

# שליפת כל המשתמשים עם סיסמאות לא מוצפנות
users = customers_collection.find()

for user in users:
    if not user["password"].startswith("scrypt:"):  # בדיקה אם הסיסמה כבר מוצפנת
        hashed_password = generate_password_hash(user["password"])
        customers_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": hashed_password}}
        )
        print(f"🔐 Updated password for {user['email']}")

print("✅ All passwords updated successfully!")
