from flask import Flask, render_template


app = Flask(__name__)
students = [
    {"id": 1, "name": "Ahmed"},
    {"id": 2, "name": "Mohamed"},
    {"id": 3, "name": "Youssef"},
]


@app.route("/")
def home_page():
    return render_template("index.html", students_data=students)


@app.route("/search/<int:id>")
def student_page(id):
    return render_template(
        "search.html", student_data=students[id - 1] if id <= len(students) else None
    )


if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True, port=5000)
