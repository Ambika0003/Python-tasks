from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# temporary storage for tasks
tasks = [
    "Learn Flask basics",
    "Build Todo App",
    "Practice Python",
    "Understand routing"
]

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)


# ADD TASK PAGE
@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task = request.form.get("task")

        if task and task.strip():
            tasks.append(task.strip())

        return redirect(url_for("home"))

    return render_template("add_task.html")


# DELETE TASK ROUTE
@app.route("/delete/<int:index>")
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)