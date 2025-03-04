from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from part3.settings import MONGO_URI, DATABASE_NAME, SECRET_KEY

# יצירת אפליקציה של Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["MONGO_URI"] = MONGO_URI

# התחברות ל-MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]  # גישה למסד הנתונים
customers_collection = db["customers"]  # גישה לאוסף customers
mongo = PyMongo(app)

###### רישום דפים (Blueprints)
## עמוד ראשי
from part3.pages.index.index import index_bp
app.register_blueprint(index_bp, url_prefix="/")

## יצירת קשר
from part3.pages.contact.contact import contact_bp
app.register_blueprint(contact_bp, url_prefix='/contact')

## התחברות
from part3.pages.login.login import login_bp
app.register_blueprint(login_bp, url_prefix="/login")


## הרשמה
from part3.pages.signup.signup import signup_bp
app.register_blueprint(signup_bp, url_prefix="/signup")

## סדנאות
from part3.pages.workshops.workshops import workshops_bp
app.register_blueprint(workshops_bp, url_prefix="/workshops")

## פרטי סדנה
from part3.pages.workshop_details.workshop_details import workshop_details
app.register_blueprint(workshop_details, url_prefix='/workshop_details')

## סיכום הזמנה
from part3.pages.summary.summary import summary_bp
app.register_blueprint(summary_bp, url_prefix='/summary')

from part3.pages.logout.logout import logout_bp
app.register_blueprint(logout_bp, url_prefix="/logout")

## טיפול בשגיאות דף
from part3.pages.page_error_handlers.page_error_handlers import page_error_handlers
app.register_blueprint(page_error_handlers)

###### רכיבים נוספים
## תפריט ראשי
from part3.components.main_menu.main_menu import main_menu
app.register_blueprint(main_menu)

# הפעלת השרת
if __name__ == "__main__":
    app.run(debug=True)
