from flask import Blueprint, request, redirect, url_for, render_template, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from part3.settings import MONGO_URI, DATABASE_NAME
import re

# התחברות למסד הנתונים
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
customers_collection = db["customers"]

# יצירת Blueprint להרשמה
signup_bp = Blueprint('signup', __name__, template_folder='templates', static_folder='static')

# פונקציה לבדיקה אם סיסמה תקינה (לפחות 8 תווים, עם מספר ואות)
def is_valid_password(password):
    return len(password) >= 8 and bool(re.search(r"\d", password)) and bool(re.search(r"[A-Za-z]", password))

@signup_bp.route('/signup/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # שליפת הנתונים מהטופס
        full_name = request.form.get('full-name').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        age = request.form.get('age').strip()
        phone = request.form.get('phone').strip()

        # בדיקה אם כל השדות מולאו
        if not full_name or not email or not password or not age or not phone:
            flash("All fields are required!", "error")
            return redirect(url_for("signup.signup"))

        # בדיקת תקינות האימייל
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format!", "error")
            return redirect(url_for("signup.signup"))

        # בדיקת תקינות הסיסמה
        if not is_valid_password(password):
            flash("Password must be at least 8 characters long and include both letters and numbers.", "error")
            return redirect(url_for("signup.signup"))

        # בדיקה אם המשתמש כבר קיים
        existing_user = customers_collection.find_one({"email": email})
        if existing_user:
            flash("User already exists! Please log in.", "error")
            return redirect(url_for("login.login"))

        # הצפנת הסיסמה ושמירת המשתמש
        password_hashed = generate_password_hash(password)
        new_user = {
            "full_name": full_name,
            "email": email,
            "password": password_hashed,  # שמירת סיסמה מוצפנת
            "age": age,
            "phone": phone
        }
        customers_collection.insert_one(new_user)

        print(f"📩 New signup: {full_name}, {email}, {age}, {phone}")

        # הודעת הצלחה והפניה לעמוד ההתחברות
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login.login"))

    return render_template('signup.html')
