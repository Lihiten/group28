from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from part3.settings import MONGO_URI, DATABASE_NAME

# התחברות למסד נתונים
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
customers_collection = db["customers"]

# יצירת Blueprint
login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')

@login_bp.route('/login/login', methods=['GET', 'POST'])  # ודא שהנתיב תואם ל-flask routes
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = customers_collection.find_one({"email": email})

        if not user:
            flash("User does not exist! Please sign up.", "error")
            return redirect(url_for('login.login'))

        # שימוש ב-check_password_hash כדי לבדוק את ההתאמה
        if not check_password_hash(user["password"], password):
            flash("Incorrect password!", "error")
            return redirect(url_for('login.login'))

        # שמירת המשתמש בסשן
        session["user"] = user["email"]
        flash("Login successful!", "success")
        return redirect(url_for('index.homepage'))

    return render_template('login.html')
