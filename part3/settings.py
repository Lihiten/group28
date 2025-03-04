import os
from dotenv import load_dotenv
from pymongo import MongoClient

# טוען משתני סביבה מקובץ .env
load_dotenv()

# Flask secret key (לשנות לערך מאובטח!)
SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')

# קבלת נתונים מ- `.env`
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# יצירת ה-URI עם שם משתמש וסיסמה באופן דינמי
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority"

# חיבור למסד הנתונים
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]  # בחירת מסד הנתונים

# בדיקה אם קיימת קולקציה ל- `workshop_registrations`, אם לא - יוצרת אותה
if "workshop_registrations" not in db.list_collection_names():
    db.create_collection("workshop_registrations")

# יצירת קולקציה חדשה לפניות מהמשתמשים אם היא לא קיימת
if "contact_forms" not in db.list_collection_names():
    db.create_collection("contact_forms")

contact_collection = db["contact_forms"]
