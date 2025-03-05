from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from pymongo import MongoClient
from part3.settings import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
customers_collection = db["customers"]
workshop_registrations = db["workshop_registrations"]

workshop_details = Blueprint('workshop_details', __name__, template_folder='templates', static_folder='static')

@workshop_details.route('/workshop_details/<type>')
def workshop_details_page(type):
    return render_template('workshop_details.html', type=type)

@workshop_details.route('/register_workshop', methods=['POST'])
def register_workshop():
    if "user" not in session:
        if request.is_json:  # אם זו בקשת AJAX
            return jsonify({"success": False, "message": "You must be logged in to register for a workshop."}), 403
        else:
            flash("You must be logged in to register for a workshop!", "error")
            return redirect(url_for("login.login"))  # מפנה לדף ההתחברות

    data = request.json
    workshop = data.get("workshop")
    date = data.get("date")
    time = data.get("time")
    participants = int(data.get("participants", 1))
    user_email = session["user"]

    if not workshop or not date or not time:
        return jsonify({"error": "Missing required fields"}), 400

    user = customers_collection.find_one({"email": user_email})
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 403

    registration = workshop_registrations.find_one({"workshop": workshop, "date": date, "time": time})

    if registration:
        if registration["participants"] + participants > 10:
            return jsonify({"success": False, "message": "Not enough spots available."}), 400
        workshop_registrations.update_one(
            {"_id": registration["_id"]},
            {"$inc": {"participants": participants}, "$push": {"users": user_email}}
        )
        updated_participants = registration["participants"] + participants
    else:
        workshop_registrations.insert_one({
            "workshop": workshop,
            "date": date,
            "time": time,
            "participants": participants,
            "users": [user_email],
            "user_details": {
                "full_name": user["full_name"],
                "email": user["email"],
                "phone": user["phone"]
            }
        })
        updated_participants = participants

    # לאחר הרשמה מוצלחת – הפניה אוטומטית לעמוד SUMMARY
    return jsonify({"success": True, "participants": updated_participants, "redirect": url_for('summary.summary')})
