from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATA_FILE = "amenities_data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        amenities_data = json.load(f)
else:
    amenities_data = {}

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/update-section", methods=["POST"])
def log_edit():
    try:
        data = request.get_json()

        component = data.get("component")
        field = data.get("field")
        new_value = data.get("value")

        print("FRONTEND EDIT DETECTED")
        print(f"Component: {component}")
        print(f"Field: {field}")
        print("New Value:")
        print(new_value)
        print("-" * 50)
        
        if component not in amenities_data:
            amenities_data[component] = {}
        amenities_data[component][field] = new_value
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(amenities_data, f, indent=4, ensure_ascii=False)

        return jsonify({"message": "Edit logged and saved successfully"}), 200

    except Exception as e:
        print("Error logging edit:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
