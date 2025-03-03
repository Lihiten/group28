from pymongo import MongoClient
from settings import MONGO_URI, DATABASE_NAME, COLLECTION_NAME



def connect_to_db():
    """
    פונקציה להתחברות למסד הנתונים MongoDB
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db

def insert_data_to_db(data):
    """
    פונקציה להוספת נתונים לאוסף
    """
    db = connect_to_db()
    collection = db[COLLECTION_NAME]
    collection.insert_one(data)

def get_all_data():
    """
    פונקציה לשליפת כל הנתונים
    """
    db = connect_to_db()
    collection = db[COLLECTION_NAME]
    return list(collection.find())

def insert_sample_data():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    # הוספת נתונים לדוגמה
    collection.insert_one({"name": "Example Data", "value": 123})
    print("Sample data inserted!")

def check_user_exists(email):
    db = connect_to_db()
    users = db["users"]
    return users.find_one({"email": email}) is not None

def insert_user(user_data):
    db = connect_to_db()
    users = db["users"]
    users.insert_one(user_data)

    db.workshop_registrations.update_many(
        {},  # בוחר את כל המסמכים
        {"$set": {"available_spots": 10}}  # מוסיף שדה עם ערך ברירת מחדל
    )

    def delete_user(email):
        """
        מוחק משתמש מהמערכת על פי כתובת האימייל
        """
        db = connect_to_db()
        users = db["customers"]
        workshop_registrations = db["workshop_registrations"]

        # מחיקת המשתמש מהאוסף customers
        result = users.delete_one({"email": email})

        if result.deleted_count > 0:
            # מחיקת כל ההרשמות לסדנאות של המשתמש
            workshop_registrations.delete_many({"users": email})
            return True
        return False

    def update_user(email, updated_data):
        """
        מעדכן פרטי משתמש במערכת
        updated_data - מילון עם השדות שצריך לעדכן (name, phone, age)
        """
        db = connect_to_db()
        users = db["customers"]

        update_fields = {}
        if "full_name" in updated_data:
            update_fields["full_name"] = updated_data["full_name"]
        if "phone" in updated_data:
            update_fields["phone"] = updated_data["phone"]
        if "age" in updated_data:
            update_fields["age"] = updated_data["age"]

        if not update_fields:
            return False  # אם אין שדות לעדכן, לא לעשות כלום

        result = users.update_one({"email": email}, {"$set": update_fields})

        return result.modified_count > 0  # מחזיר True אם משהו עודכן

    def get_user_workshops(email):
        """
        מחזירה רשימה של כל הסדנאות שהמשתמש רשום אליהן
        """
        db = connect_to_db()
        workshop_registrations = db["workshop_registrations"]

        registrations = workshop_registrations.find({"users": email}, {"_id": 0, "workshop": 1, "date": 1, "time": 1})

        return list(registrations)  # החזרת הרשימה של הסדנאות

    def update_available_spots(workshop_id):
        """
        מעדכן את מספר המקומות הפנויים בסדנה לאחר רישום משתתף
        """
        db = connect_to_db()
        workshops = db["workshop_registrations"]

        # חיפוש הסדנה ובדיקת מספר המקומות הפנויים
        workshop = workshops.find_one({"_id": workshop_id})

        if workshop and workshop.get("available_spots", 0) > 0:
            workshops.update_one(
                {"_id": workshop_id},
                {"$inc": {"available_spots": -1}}
            )
            return True
        return False  # אם אין מקומות פנויים, לא לבצע עדכון

