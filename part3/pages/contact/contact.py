from flask import Blueprint, render_template, request, jsonify
from part3.settings import contact_collection  # חיבור למסד הנתונים

# יצירת Blueprint עבור עמוד יצירת קשר
contact_bp = Blueprint('contact', __name__, static_folder='static', template_folder='templates')

@contact_bp.route('/contact/', methods=['GET'])
def contact():
    return render_template('contact.html')

@contact_bp.route('/contact/submit', methods=['POST'])
def submit_contact():
    try:
        data = request.json  # קבלת הנתונים שנשלחו מה-Frontend
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        message = data.get("message")

        # שמירה למסד הנתונים
        contact_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "message": message
        })

        return jsonify({"success": True, "message": "Your message has been sent!"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
