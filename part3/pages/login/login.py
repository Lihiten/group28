from flask import Blueprint, request, session, jsonify, redirect, url_for, render_template, flash
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from part3.settings import MONGO_URI, DATABASE_NAME

# התחברות למסד נתונים
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
customers_collection = db["customers"]

# יצירת Blueprint
login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"success": False, "message": "Invalid request format. Expected JSON."}), 415

        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return jsonify({"success": False, "message": "All fields are required!"}), 400

        user = customers_collection.find_one({"email": email})
        if not user:
            return jsonify({"success": False, "message": "User does not exist! Please sign up."}), 404

        if not check_password_hash(user["password"], password):
            return jsonify({"success": False, "message": "Incorrect password!"}), 401

        # שמירת המשתמש בסשן
        session["user"] = email
        flash("Login successful!", "success")

        # שליחת הנתיב הנכון ל- JavaScript
        return jsonify({"success": True, "message": "Login successful", "redirect": url_for('workshops.workshops_page')})


    # אם זה GET, להחזיר את עמוד ההתחברות
    return render_template("login.html")


@login_bp.route('/login/auth/check_login_status')
def check_login_status():
    if "user" in session:
        return jsonify({"logged_in": True, "user": session["user"]})
    else:
        return jsonify({"logged_in": False})


@login_bp.route('/login/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login.login'))
