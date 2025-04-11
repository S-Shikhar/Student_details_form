from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

clint = MongoClient("localhost", 27017)
db = clint.flask_sample
sample = db.sample


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        section = request.form["section"]
        roll = request.form["roll_number"]
        
        sample.insert_one({
            "Name": name,
            "Section": section,
            "Roll No": roll
        })
        
        return redirect(url_for("index"))
        
    return render_template("index.html")


@app.route("/information")
def info():
    if request.method == "GET":
        records = list(sample.find())
        return render_template("info.html", info=records)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    student = sample.find_one({"_id": ObjectId(id)})
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        # Update student record with form data
        updated_data = {
            "Name": request.form['name'],
            "Section": request.form['section'],
            "Roll No": request.form['roll_number']
        }
        sample.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        return redirect(url_for('info'))  # Redirect to the info page

    return render_template('edit.html', record=student)


@app.post("/<id>/delete/")
def delete(id):
    sample.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("info"))
           

if __name__ == "__main__":
    app.run(debug=True)
