import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities.db.db_manager import connect_to_db




def analyze_database():
    """
    מציג את כל הנתונים בטבלאות MongoDB
    """
    db = connect_to_db()

    collections = db.list_collection_names()
    if not collections:
        print("No collections found in the database.")
        return

    for collection_name in collections:
        print(f"\n🔹 Collection: {collection_name}")
        collection = db[collection_name]
        documents = collection.find()

        count = 0
        for doc in documents:
            print(doc)
            count += 1

        if count == 0:
            print("⚠️ Empty Collection")


if __name__ == "__main__":
    analyze_database()
