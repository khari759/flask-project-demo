from flask import Flask, request, render_template, jsonify, redirect, url_for
from pymongo.mongo_client import MongoClient
import os
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client.test
collection = db['flask_tutorial']

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api')
def get_api_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        collection.insert_one(form_data)
        return redirect(url_for('success'))
    except Exception as e:
        error_message = f"Error submitting data: {str(e)}"
        return render_template("index.html", error=error_message)

@app.route('/success')
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
