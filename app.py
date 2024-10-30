from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Constants
GROUP_SIZE = 5
TOTAL_STUDENTS = 43
TOTAL_GROUPS = TOTAL_STUDENTS // GROUP_SIZE + (1 if TOTAL_STUDENTS % GROUP_SIZE != 0 else 0)
DATA_FILE = 'data.json'


# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"groups": [[] for _ in range(TOTAL_GROUPS)]}


# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()

    if request.method == "POST":
        name = request.form['name']
        reg_no = request.form['reg_no']
        student = {"name": name, "reg_no": reg_no}

        # Check if student is already in a group
        for group in data["groups"]:
            if any(s["reg_no"] == reg_no for s in group):
                return "Student already assigned to a group!"

        # Assign student to a group
        available_groups = [group for group in data["groups"] if len(group) < GROUP_SIZE]
        if not available_groups:
            return "All groups are full."

        # Add student to a random available group
        chosen_group = random.choice(available_groups)
        chosen_group.append(student)
        save_data(data)

        return "Student successfully assigned to a group!"

    return render_template("index.html")

# Route for printable format
@app.route("/printable", methods=["GET"])
def printable():
    data = load_data()
    return render_template("STUDENTS.html", groups=data["groups"])


@app.route("/groups", methods=["GET"])
def get_groups():
    data = load_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
