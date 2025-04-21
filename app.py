from flask import Flask, render_template, request

app = Flask(__name__)

# Store submissions in memory (temporary)
students = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        students.append({"name": name, "email": email, "course": course})
        return render_template("index.html", success=True, students=students)

    return render_template("index.html", success=False, students=students)

if __name__ == "__main__":
    app.run(debug=True)
