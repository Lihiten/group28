from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from part3.settings import MONGO_URI, DATABASE_NAME
import re

# התחברות למסד נתונים
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
customers_collection = db["customers"]

# יצירת Blueprint
login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')

# משתנה לניהול ניסיונות התחברות כושלים לכל משתמש
failed_login_attempts = {}

@login_bp.route('/login/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        # בדיקה אם כל השדות מולאו
        if not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for('login.login'))

        # בדיקה אם האימייל תקין
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format!", "error")
            return redirect(url_for('login.login'))

        # בדיקה אם המשתמש ננעל לאחר מספר ניסיונות כושלים
        if email in failed_login_attempts and failed_login_attempts[email]["count"] >= 5:
            lock_time = failed_login_attempts[email]["time"]
            if datetime.now() < lock_time + timedelta(minutes=5):
                flash("Too many failed attempts. Try again later.", "error")
                return redirect(url_for('login.login'))
            else:
                # אם עבר הזמן - איפוס הניסיונות
                failed_login_attempts[email] = {"count": 0, "time": datetime.now()}

        # בדיקת אם המשתמש קיים
        user = customers_collection.find_one({"email": email})
        if not user:
            flash("User does not exist! Please sign up.", "error")
            return redirect(url_for('signup.signup'))

        # בדיקת סיסמה מוצפנת
        if not check_password_hash(user["password"], password):
            flash("Incorrect email or password!", "error")

            # הגדלת מונה ניסיונות כושלים
            if email not in failed_login_attempts:
                failed_login_attempts[email] = {"count": 1, "time": datetime.now()}
            else:
                failed_login_attempts[email]["count"] += 1
                failed_login_attempts[email]["time"] = datetime.now()

            return redirect(url_for('login.login'))

        # איפוס ניסיונות כושלים לאחר כניסה מוצלחת
        failed_login_attempts[email] = {"count": 0, "time": datetime.now()}

        # שמירת המשתמש בסשן
        session["user"] = email
        flash("Login successful!", "success")
        return redirect(url_for('index.homepage'))

    return render_template('login.html')
