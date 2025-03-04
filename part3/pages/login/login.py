from flask import Blueprint, request, session, jsonify, redirect, url_for

# יצירת Blueprint עבור התחברות
login_bp = Blueprint('login', __name__)


@login_bp.route('/auth/check_login_status')
def check_login_status():
    """
    פונקציה שבודקת אם המשתמש מחובר
    מחזירה JSON עם True אם מחובר, אחרת False
    """
    if "user" in session:
        return jsonify({"logged_in": True, "user": session["user"]})
    else:
        return jsonify({"logged_in": False})


@login_bp.route('/auth/login', methods=['POST'])
def login():
    """
    פונקציית התחברות
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # בדיקה אם המשתמש קיים (כאן כדאי לבדוק בבסיס נתונים אמיתי)
    if email == "test@example.com" and password == "1234":
        session["user"] = email  # שמירת המשתמש ב-session
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})


@login_bp.route('/auth/logout')
def logout():
    """
    פונקציה להתנתקות מהמערכת
    """
    session.pop("user", None)
    return redirect(url_for('login.login'))
