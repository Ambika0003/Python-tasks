#===========================================
#Title : Simple Flask Todo Application
#===========================================
#Features:
#- View tasks
#- Add new task
#- Delete task

from flask import Flask, render_template, request, redirect, url_for

# Create Flask app instanc
# e
app = Flask(__name__)

# ===========================================
# Temporary in-memory task storage
# ===========================================
tasks = [
    "Learn Flask basics",
    "Build Todo App",
    "Practice Python",
    "Understand routing"
]

# ===========================================
# HOME PAGE - Show all tasks
# ===========================================
@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)

# ===========================================
# ADD TASK PAGE
# GET  -> show form
# POST -> add task to list
# ===========================================
@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task = request.form.get("task")

        # Validate input (avoid empty tasks)
        if task and task.strip():
            tasks.append(task.strip())

        return redirect(url_for("home"))

    return render_template("add_task.html")

# ===========================================
# DELETE TASK ROUTE
# Removes task using index
# ===========================================
@app.route("/delete/<int:index>")
def delete_task(index):
    # Check valid index before deleting
    if 0 <= index < len(tasks):
        tasks.pop(index)

    return redirect(url_for("home"))

# ===========================================
# Run Flask application
# ===========================================
if __name__ == "__main__":
    app.run(debug=True)