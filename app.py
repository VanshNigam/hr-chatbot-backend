from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # ✅ Import CORS
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all origins (or configure securely below)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
employees = db["employees"]

@app.route('/')
def home():
    return "HR Flask API is running!"

@app.route("/employee-query", methods=["POST"])
def get_employee_info():
    data = request.json

    try:
        emp_id = int(data.get("emp_id"))  # Convert to int to match MongoDB type
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid or missing Employee ID"}), 400

    employee = employees.find_one({"employee_id": emp_id})
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    response = {
        "name": employee.get("name"),
        "leave_balance": employee.get("vacation_leave"),
        "designation": employee.get("position")
    }

    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
