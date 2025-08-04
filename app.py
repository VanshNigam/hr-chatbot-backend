from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
employees = db["employees"]

@app.route('/')
def home():
    return "HR Flask API is running!"

@app.route("/employee-query", methods=["POST"])
def get_employee_info():
    data = request.json
    emp_id = data.get("emp_id")  # Sent by Botpress

    if not emp_id:
        return jsonify({"error": "emp_id missing"}), 400

    employee = employees.find_one({"employee_id": emp_id})
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    # Example response
    response = {
        "name": employee.get("name"),
        "leave_balance": employee.get("leave_balance"),
        "designation": employee.get("designation")
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)
